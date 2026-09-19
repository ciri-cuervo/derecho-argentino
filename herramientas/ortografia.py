#!/usr/bin/env python3
"""Revisa la ortografía y la gramática de la prosa del repositorio con LanguageTool.

POR QUÉ EXISTE

Los controles de acentos de la suite son reglas —`-ción`, la ñ transliterada, determinante más
sustantivo, `se` más pretérito— y cubren lo que una regla puede decidir. Dejan afuera, a
propósito, las palabras que existen de las dos formas y toda la gramática: eso no es una
limitación que se pueda calibrar, es el límite de una regla. La lectura tapaba ese hueco y la
lectura se olvida.

Esto lo cierra con un diccionario y una gramática de verdad. No reemplaza a los tests: ellos
son el piso que corre siempre y sin red; esto es el techo, y se corre a mano.

QUÉ NO ES

No corre en CI ni en el checklist. Necesita Java 17 o superior y baja LanguageTool la primera
vez, que son 259 MB: meterlo al candado obligatorio haría que el candado tarde minutos y
dependa de la red, y un control que molesta se termina salteando. Se sugiere, no se corre solo,
igual que `verificar_normas.py`.

QUÉ MIRA Y QUÉ NO

Mira la PROSA de lo que el repositorio VERSIONA —se lo pregunta a git—: los `.md` fuera de
`kb/`, los comentarios y docstrings de los `.py`, las cadenas
que un script imprime y los campos de prosa de los `.json`. No mira lo que se compara —
identificadores, valores de bandera, claves de veredicto, carátulas — ni lo que va entre
backticks o entre comillas, que son citas.

Uso, desde la raíz del repositorio:

    python3 herramientas/ortografia.py                 # todo
    python3 herramientas/ortografia.py --solo py       # py | md | json
    python3 herramientas/ortografia.py --archivo X.md

Sale con código 1 si encontró algo.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tokenize
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
# Términos del dominio y del repositorio que LanguageTool no conoce y no son faltas.
PROPIOS = {
    "skill", "skills", "plugin", "plugins", "marketplace", "commit", "docstring", "docstrings",
    "hash", "sha", "slug", "slugs", "eval", "evals", "json", "csv", "md", "py", "cp",
    "mojibake", "OCR", "ocr", "pdftotext", "tesseract", "argparse", "pyflakes", "backticks",
    "regex", "regexp", "cron", "repo", "repos", "InfoLEG", "SAIJ", "JUBA", "SCBA", "CSJN",
    "CCyCN", "LCT", "LRT", "CPCCBA", "CPCCN", "CCT", "SMVM", "RIPTE", "IPC", "CER", "jus",
    "DNU", "BORA", "MEV", "SECLO", "CUD", "IOMA", "IPS", "SUTEBA", "ARBA", "ANSES",
    "python3", "pip", "uv", "git", "grep", "stdout", "stderr", "argv", "kwargs",
    "LanguageTool", "Codex", "Claude", "Anthropic", "GitHub", "Windows", "Linux",
    "hash", "hashes", "Hash", "token", "tokens", "nonce", "nonces", "timeout", "timeouts",
    "div", "class", "style", "bundle", "certifi", "codepage", "request", "requests",
    "JURISTECA", "juristeca", "gba", "CEDOM", "BNA", "UF", "cp1252", "UTF", "utf",
    "layout", "psm", "pdftoppm", "tesseract", "poppler", "sha256", "SHA", "URL", "URLs",
    "HTML", "html", "PDF", "PDFs", "API", "APIs", "CLI", "CI", "JSON", "CSV", "TLS",
    "DNS", "TCP", "GET", "HTTP", "HTTPS", "id", "ids", "slugger", "markdownlint",
    "frontmatter", "backtick", "voseo", "rioplatense", "mojibake", "OCR", "reOCR",
    "reextrayendo", "reextraer", "redescarga", "rebajar", "rebajaba", "prepaga",
    "prepagas", "cautelar", "cautelares", "articulado", "carátulas", "IUS",
    # Abreviaturas del articulado y de la cita. Van sin acento y sin desarrollar porque así
    # se escriben en el derecho argentino, y son lo que más aparece en todo el repositorio.
    "art", "arts", "Art", "Arts", "inc", "incs", "Inc", "Incs", "cons", "Cons", "ss", "sigs",
    "expte", "exptes", "Expte", "fs", "cfr", "Ac", "Acs", "Res", "Disp", "Dto", "Ac°",
    # Latinajos del articulado: el texto oficial los escribe así, sin tilde.
    "bis", "ter", "quater", "quinquies", "sexies", "septies", "octies", "nonies", "decies",
    "quantum", "iuris", "tantum", "ultra", "petita", "obiter", "dictum", "erga", "omnes",
    "habeas", "corpus", "data", "ratio", "decidendi", "in", "re", "supra", "infra",
    # Siglas de tribunales, organismos y normas.
    "PBA", "CABA", "CN", "CNCiv", "CNCom", "CNAT", "CNACAF", "CCAyT", "Cám", "CCyC", "LDC",
    "LNPA", "CPP", "CPPF", "CP", "REIL", "COPREC", "PMO", "SRT", "SAC", "MJ", "SC", "BO",
    "BCRA", "INDEC", "AFIP", "ARCA", "CNDC", "IGJ", "DPPJ", "PAMI", "UPDP", "UCAP", "ISBIC",
    "CUIL", "CUIT", "CIF", "ANDIS", "ReNaPDiS", "CH", "CIDIP", "OEA", "SMVM", "OTROSÍ",
    "KB", "kB", "MB", "GB", "linter", "shell", "llm", "álea", "Skill", "grader", "graders",
    "kb", "release", "releases", "posix", "POSIX", "Pc", "Pd", "sion", "cion",
    # `sólo` se escribe así en todo el repositorio, a propósito. La regla SOLO está
    # apagada más abajo, pero el diccionario lo marca igual como palabra desconocida.
    "sólo", "Sólo",
    # Los demostrativos con tilde: misma decisión que `sólo`, escrita en docs/DESARROLLO.md.
    "éste", "ésta", "éstos", "éstas", "ése", "ésa", "ésos", "ésas",
    "aquél", "aquélla", "aquéllos", "aquéllas", "Éste", "Ésta", "Ése", "Ésa",
    "ruteo", "rutea", "rutean", "ruteado", "ruteada", "ruteadas",
    "ruteados", "matchea", "grader", "graders", "transcripto", "transcriptos",
    "sobreviniente", "juzgamiento", "resarcitoria", "oponibilidad", "eximición",
    "hábeas", "DIPr", "dies", "SIPA", "SIJP", "AFJP", "REFEPS", "SPL", "RG",
}
# Giros de dos palabras que el repositorio escribe así a propósito y la gramática marca como
# discordancia de género. No se apaga la regla entera --`AGREEMENT_DET_NOUN` atrapó un «un
# cita» de verdad--: se exceptúan los giros, medidos y con su motivo.
#
#   `el fuente`     el código fuente, por elipsis de «el [código] fuente». Es la mitad de una
#                   distinción que este repositorio necesita: `la fuente` es la fuente del
#                   derecho --primaria, oficial-- y `el fuente` es el código. Medido: 18
#                   masculinos, todos código; 64 femeninos, todos fuente del derecho.
#   `el checklist`  26 veces en masculino y ninguna en femenino. Es la voz del repositorio.
FRASES_PROPIAS = {
    "el fuente", "El fuente", "del fuente", "Del fuente", "un fuente", "este fuente",
    "ese fuente", "el checklist", "El checklist", "del checklist", "Del checklist",
    "un checklist", "los checklists", "al checklist",
    # `los agravantes` en masculino es el uso forense argentino para las circunstancias que
    # agravan la pena. La RAE admite los dos géneros; el repositorio usa uno solo.
    "los agravantes", "Los agravantes", "estos agravantes", "esos agravantes",
    "dos agravantes", "tres agravantes",
}
# Lo que no es prosa: se saca antes de medir.
NO_ES_PROSA = (
    re.compile(r"`[^`]*`"),            # identificadores
    re.compile(r'"[^"]*"'),            # citas
    re.compile(r"«[^»]*»"),            # citas
    re.compile(r"```.*?```", re.S),    # bloques de código
    re.compile(r"https?://\S+"),
    re.compile(r"--[\w-]+(\s+[^\s,;.]+)?"),
    re.compile(r"[\w./-]*\.(py|md|json|csv|txt|html|pdf|yml)\b"),
    # Un slug: tres o más tramos en minúscula unidos por guiones. Es el nombre de un eval, de
    # una norma o de un fallo, va en ASCII por regla y aparece en el encabezado de casi todos
    # los `.md` de `evals/`. Sin esto, `civil-danos-transito-factor-objetivo-pba` se reclamaba
    # como tres faltas de acento por archivo.
    re.compile(r"\b[a-z0-9]+(?:-[a-z0-9]+){2,}\b"),
)
# Las filas de tabla NO están acá. Estuvieron, descartadas enteras "porque son dato", y eso
# dejaba sin medir el 85% de `changelog-normativo.md`. Las desarma `prosa_de_md()`, que tira
# los pipes y la fila delimitadora y conserva el texto de las celdas.
# Campos de un .json que NO son prosa: se comparan, se citan o son texto ajeno.
#   `problema`      se coteja contra revisiones.json
#   `caratula`      sale del documento, no del idioma
#   `tribunal`      idem
#   `secuencias`    fragmentos de kb/, que es de otro autor
#   `de` / `a`      el cotejo del OCR: texto que se compara byte a byte
SALTAR_CAMPO = {"problema", "caratula", "tribunal", "secuencias", "de", "a"}


def vocabulario_de_veredictos() -> set[str]:
    """Los valores de veredicto que los archivos declaran en su `_vocabulario`.

    Son claves --`locucion`, `congelada`, `de-terceros`-- y por eso van en ASCII; pero además
    encabezan cada motivo, así que el diccionario los lee como prosa mal escrita. Se leen de
    los propios archivos en vez de copiarse acá: una lista copiada se separa del original, y
    entonces o la herramienta reclama un valor legítimo o deja de reclamar una falta.
    """
    valores: set[str] = set()
    for f in RAIZ.rglob("*.json"):
        if ".git" in f.parts or es_de_otro_autor(f):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if isinstance(d, dict) and isinstance(d.get("_vocabulario"), dict):
            valores.update(d["_vocabulario"])
    return valores


# Capa 2: material de otro autor, que no se corrige ni en el contenido ni en la ortografía.
# `kb/` entero y las cinco excepciones que `LICENCIAS.md` nombra por ruta. Faltaban las cinco,
# y por eso esta herramienta reclamaba un `OTROSI` sin tilde en un eval que no se puede tocar:
# un aviso que nadie puede atender es la definición de la alarma que se deja de mirar.
CAPA_2 = (
    "derecho/kb",
    "derecho/evals/administrativo-caba-recursos-agotamiento-via",
    "derecho/evals/consumidor-dano-punitivo-prescripcion",
    "derecho/evals/consumidor-garantia-producto-defectuoso",
    "derecho/evals/consumidor-prepaga-aumento-dnu70",
    "derecho/evals/README.md",
)


_VERSIONADOS: frozenset[str] | None = None


def versionados() -> frozenset[str]:
    """Lo que el repositorio versiona, preguntado a git y no adivinado con una lista.

    Un `rglob` sobre el árbol mide la carpeta de quien corre la herramienta, no el repositorio.
    `derecho/evals/results/` lo escribe `claude plugin eval` y `.gitignore` ya lo excluye: eran
    115 de los 582 candidatos de una corrida, todos sobre un JSON de resultados que nadie va a
    corregir. Un aviso que nadie puede atender es la definición de la alarma que se deja de
    mirar, igual que pasaba con las cinco excepciones de capa 2.

    **Y agregar `results` a una lista de patrones sería calibrar contra el caso conocido**: la
    lista siempre va atrás de la próxima herramienta que escriba algo en el árbol. Es la misma
    decisión que ya tomó `cifras.py` para `mb_instalados`, y por el mismo motivo.
    """
    global _VERSIONADOS
    if _VERSIONADOS is None:
        if shutil.which("git") is None:
            raise SystemExit("falta `git`: esta herramienta mide lo que el repositorio versiona "
                             "y no puede deducirlo del disco.")
        hecho = subprocess.run(
            ["git", "-C", str(RAIZ), "ls-files", "-z", "--cached", "--others",
             "--exclude-standard"], capture_output=True, text=True)
        if hecho.returncode != 0:
            raise SystemExit(f"`git ls-files` falló sobre {RAIZ}: {hecho.stderr.strip()}")
        _VERSIONADOS = frozenset(r for r in hecho.stdout.split("\0") if r)
    return _VERSIONADOS


def es_del_repositorio(archivo: pathlib.Path) -> bool:
    try:
        rel = archivo.resolve().relative_to(RAIZ.resolve()).as_posix()
    except ValueError:
        return False
    return rel in versionados()


def es_de_otro_autor(archivo: pathlib.Path) -> bool:
    rel = archivo.relative_to(RAIZ).as_posix()
    return any(rel == c or rel.startswith(c + "/") for c in CAPA_2)


def limpiar(texto: str) -> str:
    """Saca lo que no es prosa y vuelve a juntar lo que queda.

    Colapsar los espacios NO es cosmético: cada recorte deja un hueco, y el hueco delante de
    un signo de puntuación dispara `INCORRECT_SPACES`. Eran 744 avisos de 5.730, todos
    fabricados por esta misma función --se reclamaba a sí misma-- y ninguno un defecto del
    texto. El maquetado no se mide acá: para eso está `WHITESPACE_RULE`, que está apagada con
    ese motivo escrito.
    """
    for patron in NO_ES_PROSA:
        texto = patron.sub(" ", texto)
    return re.sub(r"[ \t]+", " ", texto)


def pelar(palabra: str) -> str:
    """La palabra sin diacríticos, para comparar `union` contra `unión`."""
    return "".join(c for c in unicodedata.normalize("NFD", palabra)
                   if unicodedata.category(c) != "Mn").lower()


_VEREDICTOS: set[str] | None = None


def es_propio(palabra: str) -> bool:
    global _VEREDICTOS
    if _VEREDICTOS is None:
        _VEREDICTOS = vocabulario_de_veredictos()
    limpia = palabra.strip("()[],.:;·°º\"'")
    # Una letra suelta viene de `inc. b` o de `n° 1`: no hay ortografía que discutir ahí.
    return (len(limpia) <= 1 or palabra in PROPIOS or limpia in PROPIOS
            or limpia in _VEREDICTOS)


def palabra_desconocida(m, palabra: str) -> bool:
    """True si el diccionario no la tiene y NO le propone la misma palabra con tildes.

    Es la línea que separa las dos mitades de `MORFOLOGIK_RULE_ES`, que solo son una regla
    de nombre. Una mitad son faltas de acento -- `union`, `credito`, `Boletin`, `dieciseis`
    -- y se reconocen porque entre las sugerencias está la misma palabra con sus tildes.
    La otra son siglas, latinajos, apellidos y nombres de archivo, donde las sugerencias no
    tienen nada que ver (`PBA` -> `IBA, PBI, PÚA`) y lo único que hace falta es enseñarle
    la palabra al diccionario.

    Mezcladas eran 3.387 de 4.180 renglones, y el resultado es el conocido: una alarma que
    suena siempre y que nadie termina de leer.
    """
    if m.rule_id != "MORFOLOGIK_RULE_ES":
        return False
    base = pelar(palabra)
    return not any(pelar(s) == base and s != palabra for s in m.replacements)


def prosa_de_py(archivo: pathlib.Path):
    """(línea, texto) de comentarios, docstrings y cadenas que se imprimen."""
    fuente = archivo.read_text(encoding="utf-8")
    for tok in tokenize.generate_tokens(io.StringIO(fuente).readline):
        if tok.type == tokenize.COMMENT:
            yield tok.start[0], tok.string.lstrip("# ")
    arbol = ast.parse(fuente)
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(nodo)
            if doc:
                yield getattr(nodo, "lineno", 1), doc
        if (isinstance(nodo, ast.Call) and getattr(nodo.func, "id", "") in ("print", "SystemExit")):
            for arg in nodo.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    yield nodo.lineno, arg.value
                elif isinstance(arg, ast.JoinedStr):
                    for pieza in arg.values:
                        if isinstance(pieza, ast.Constant) and isinstance(pieza.value, str):
                            yield nodo.lineno, pieza.value


def prosa_de_json(archivo: pathlib.Path):
    try:
        datos = json.loads(archivo.read_text(encoding="utf-8"))
    except ValueError:
        return
    pendientes = [(datos, None)]
    while pendientes:
        nodo, campo = pendientes.pop()
        if isinstance(nodo, dict):
            pendientes += [(v, k) for k, v in nodo.items()]
        elif isinstance(nodo, list):
            pendientes += [(v, campo) for v in nodo]
        elif isinstance(nodo, str) and " " in nodo and campo not in SALTAR_CAMPO:
            yield campo or "?", nodo


def prosa_de_md(texto: str):
    """(línea, párrafo) de un `.md`, con la línea de verdad y las tablas adentro.

    Las dos cosas que arregla eran, cada una a su modo, la alarma apagada.

    LA LÍNEA. Antes esto devolvía el archivo entero como una sola pieza en la línea 1, así
    que los hallazgos de los `.md` -el 74% del total- salían todos apuntando a la línea 1 y
    no había cómo ubicarlos. Se parte en párrafos y cada uno lleva la línea donde arranca.

    LAS TABLAS. `NO_ES_PROSA` descartaba la fila entera por venir entre pipes, "porque es
    dato". En `changelog-normativo.md` eso son 27.528 de 32.236 caracteres -- el 85% del
    archivo, y justo la columna «Cómo revalidar», que es el bloque de prosa más grande de
    todas las referencias. Acá la fila se conserva y lo que se tira son los pipes y la fila
    delimitadora, que no es texto.

    Los bloques cercados se vacían ANTES de partir, y se reemplazan por líneas en blanco en
    vez de borrarse: sacarlos corre todo lo que sigue y la línea vuelve a mentir.
    """
    def vaciar(m):
        return "\n" * m.group(0).count("\n")

    texto = re.sub(r"^ {0,3}```.*?^ {0,3}```[^\n]*$", vaciar, texto, flags=re.S | re.M)
    lineas = texto.splitlines()
    pieza, arranque = [], 0
    fin_frontmatter = 0
    if lineas and lineas[0].strip() == "---":
        for i, l in enumerate(lineas[1:], 2):
            if l.strip() == "---":
                fin_frontmatter = i
                break
    for n, linea in enumerate(lineas, 1):
        if n <= fin_frontmatter:
            # En el frontmatter la CLAVE es contrato y el valor es prosa. Sin sacar la clave,
            # `titulo:` y `area:` se reclamaban como faltas de acento en cada eval --73
            # avisos-- y acentuarlas rompe el parseo. `name:` y `tags:` se van enteros: sus
            # valores son lo que el usuario tipea para filtrar una corrida.
            if re.match(r"^\s*(name|tags):", linea):
                linea = ""
            else:
                linea = re.sub(r"^\s*[A-Za-z_][\w-]*:\s*", "", linea)
            if linea.strip() in ("", "---"):
                continue
            yield n, linea
            continue
        if re.match(r"^\s*\|?[\s:|-]*-{3,}[\s:|-]*\|?\s*$", linea):
            linea = ""                       # fila delimitadora de tabla: no es texto
        elif linea.lstrip().startswith("|"):
            # Una fila es una pieza suya: pegarla al párrafo de al lado inventa una oración.
            if pieza:
                yield arranque, "\n".join(pieza)
                pieza = []
            yield n, linea.strip().strip("|").replace("|", ". ")
            continue
        elif re.match(r"^(\t| {4,})\S", linea):
            linea = ""                       # bloque de código con sangría
        if linea.strip():
            if not pieza:
                arranque = n
            pieza.append(linea)
        elif pieza:
            yield arranque, "\n".join(pieza)
            pieza = []
    if pieza:
        yield arranque, "\n".join(pieza)


def archivos(solo: str | None):
    if solo in (None, "md"):
        for f in sorted(RAIZ.rglob("*.md")):
            if f.name.startswith("LICENSE") or not es_del_repositorio(f):
                continue
            if es_de_otro_autor(f):
                continue
            crudo = f.read_text(encoding="utf-8", errors="replace")
            yield f, [(n, limpiar(t)) for n, t in prosa_de_md(crudo)]
    if solo in (None, "py"):
        for f in sorted(RAIZ.rglob("*.py")):
            if not es_del_repositorio(f) or es_de_otro_autor(f):
                continue
            yield f, [(n, limpiar(t)) for n, t in prosa_de_py(f)]
    if solo in (None, "json"):
        for f in sorted(RAIZ.rglob("*.json")):
            if (f.name == "procedencia.json" or not es_del_repositorio(f)
                    or es_de_otro_autor(f)):
                continue
            yield f, [(c, limpiar(t)) for c, t in prosa_de_json(f)]


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--solo", choices=("py", "md", "json"), default=None)
    p.add_argument("--archivo", default=None, help="revisar un solo archivo")
    a = p.parse_args(argv)

    try:
        import jdk4py
        import language_tool_python
    except ImportError:
        print("faltan dependencias. Esta herramienta no está en el checklist a propósito:\n"
              "    uv run --with language-tool-python --with jdk4py python "
              "herramientas/ortografia.py", file=sys.stderr)
        return 2
    import os
    os.environ["JAVA_HOME"] = str(jdk4py.JAVA_HOME)
    os.environ["PATH"] = str(jdk4py.JAVA_HOME / "bin") + os.pathsep + os.environ["PATH"]

    print("  levantando LanguageTool (la primera vez baja 259 MB)...", file=sys.stderr)
    herramienta = language_tool_python.LanguageTool("es")
    # Se apaga lo que no aplica, con su motivo. Dejar ruido prendido es la forma más rápida de
    # que nadie mire la salida.
    herramienta.disabled_rules.update({
        "VOSEO",                       # el repositorio ESCRIBE en voseo: `corré` es correcto
        "SOLO",                        # `sólo` se conserva: uso aceptado y es la voz del repo
        # Y con `sólo` van los demostrativos: `éste`, `ésa`, `aquéllas`. La RAE les sacó la
        # tilde en 2010 y el repositorio conserva las dos grafías por la misma razón --es la
        # ortografía del foro y la que usan los escritos-- así que la decisión está tomada y
        # escrita en docs/DESARROLLO.md. Medido: 32 demostrativos acentuados y ninguno mezclado.
        "ESTE_ESE_AQUEL_NOTILDE",
        # `se` impersonal al final de un renglón: la regla propone `sé`. Medido sobre este
        # corpus, 18 avisos y 18 falsos. Una medida que se equivoca sobre todos los casos
        # conocidos no sirve para los desconocidos.
        "SE",
        # `el id`, `un id`: `id` es el identificador de un documento y la regla lo lee como
        # imperativo de `ir`. 15 avisos, 15 falsos.
        "WRONG_IMPERATIVE",
        # Sacar los identificadores deja huecos, y las reglas que miran la palabra VECINA
        # leen esos huecos como frase rota: sobre «la copia de ` ` tiene precedencia»
        # piden `dé` por `de` y `él` por `el`. Medido: de los hallazgos de estas reglas,
        # casi todos eran del hueco y no del texto. Rellenar con una palabra neutra no
        # arregla nada: mueve el ruido a la repetición. Se apagan, con el costo dicho:
        # un `dé` o un `él` de verdad hay que verlo leyendo.
        "PREP_VERB", "EL_TILDE", "DE_TILDE", "HACIA_TILDE", "PHRASE_REPETITION",
        "ESTO_ESTE", "COMA_Y_PUNTO", "MAYUSCULAS_INICIO_FRASE", "ABREVIATURA_NUMERO",
        "WHITESPACE_RULE",             # se mide prosa recortada, no maquetado
        # Mismo motivo, y además se lo fabrica esta herramienta: sacar un span de código deja
        # el espacio que lo rodeaba pegado al signo que venía después. Eran 725 avisos de
        # 1.420 y ninguno era un defecto del texto. El espaciado del Markdown no se mide acá.
        "INCORRECT_SPACES",
        "UPPERCASE_SENTENCE_START",    # un comentario o una nota no empieza oración
        "ES_UNPAIRED_BRACKETS",        # los marcadores son `[NOMBRE: ...]` y se recortan
        "COMMA_PARENTHESIS_WHITESPACE",
        "PUNTOS_SUSPENSIVOS",
        "SPACE_AFTER_COMMA",
        # NUMERAL + SUSTANTIVO. Este repositorio está hecho de citas legales, donde «art. 441
        # texto Ley 13.818», «Tomo 5 completo», «art. 100 bonaerense» y «el art. 16 remite» son
        # la forma normal. La regla las lee como concordancia rota. Medido: 49 avisos, 49
        # falsos. Una medida que se equivoca sobre todos los casos conocidos no sirve para los
        # desconocidos.
        "AGREEMENT_NUMERAL_PLURAL",
        # Misma causa, otra regla: «número de causa», «número de artículo», «número de
        # acápite». Lee «número de» como cuantificador y pide el plural. 7 avisos, 7 falsos.
        "NUMERO_DE_SG_PL",
        # Las fabrica este mismo recorte, como `INCORRECT_SPACES`: sacar un span de código
        # entre dos palabras iguales deja «en en», «del del». Medido contra los archivos: no
        # hay ni una repetición de verdad, las 11 son del hueco.
        "SPANISH_WORD_REPEAT_RULE",
        # `> [!NOTE]` y `> [!IMPORTANT]` son los avisos de GitHub, y `.template` y
        # `?idDocumento` un archivo y un parámetro de URL. 13 avisos, 13 falsos.
        "ESPACIO_DESPUES_DE_PUNTO",
        # Adjetivo o preposición pospuestos en frase jurídica: «ubicaciones habituales bajo el
        # home», «conforme las Leyes 23.660», «doce caracteres más largo». 19 avisos, 19
        # falsos: la regla busca el sustantivo más cercano y acá no es con el que concuerda.
        "AGREEMENT_POSTPONED_ADJ",
        # «no A sino B» no lleva coma cuando es correlativo simple -«no es el texto sino el
        # trabajo»-, que es como se usa acá. 23 avisos, ninguno real.
        "COMMA_SINO2",
        # Y `COMMA_SINO` a secas, que es la misma regla por otra vía. Medido sobre los 67
        # `sino` del plugin: 18 llevan coma y 49 no, y el reparto está bien. La coma aparece
        # cuando el primer miembro es largo -«no la suma reclamada en el pleito perdido, sino
        # la probabilidad de éxito»- y falta en el correlativo simple -«no es el monto sino la
        # validez»-. La regla reclama los 16 del segundo grupo. 16 avisos, ninguno real.
        "COMMA_SINO",
        # Participio + sustantivo. Lo que dispara es la locución `X por X` y `X a X`, que en
        # este repositorio es la forma normal de decir cómo se coteja: «conservado palabra por
        # palabra», «cotejados artículo por artículo», «actualizados mes a mes». La regla toma
        # el segundo sustantivo de la locución como el núcleo con el que debe concordar. El
        # resto son huecos del recorte, igual que `INCORRECT_SPACES`. 11 avisos, 11 falsos.
        "AGREEMENT_PARTICIPLE_NOUN",
        # `contencioso administrativo` sin guion es DECISIÓN de este repositorio, medida y
        # escrita en docs/DESARROLLO.md, y `TestContenciosoAdministrativoSinGuion` la sostiene.
        # La regla pide el guion que la RAE pediría, así que acá suena siempre: 15 avisos, y
        # los 15 contra una forma que elegimos. Una alarma que reclama lo que ya se decidió es
        # la que hace que se deje de mirar la salida entera.
        "ES_COMPOUNDS_CONTENCIOSO_ADMINISTRATIVO",
    })
    hallazgos = 0
    revisados = 0
    vocabulario: dict[str, int] = {}
    try:
        for archivo, piezas in archivos(a.solo):
            if a.archivo and a.archivo not in str(archivo):
                continue
            for donde, texto in piezas:
                if not texto.strip():
                    continue
                revisados += 1
                for m in herramienta.check(texto):
                    palabra = texto[m.offset:m.offset + m.error_length]
                    if es_propio(palabra) or palabra in FRASES_PROPIAS:
                        continue
                    if palabra_desconocida(m, palabra):
                        vocabulario[palabra] = vocabulario.get(palabra, 0) + 1
                        continue
                    hallazgos += 1
                    print(f"{archivo.relative_to(RAIZ)}:{donde}  «{palabra}»"
                          f" -> {', '.join(m.replacements[:3]) or '?'}"
                          f"   [{m.rule_id}]")
    finally:
        herramienta.close()
    print(f"\n  {revisados} piezas de prosa revisadas, {hallazgos} candidatos.")
    if hallazgos:
        print("  Un candidato es un CANDIDATO: LanguageTool no conoce el vocabulario jurídico\n"
              "  ni el del repositorio, y las palabras que existen de las dos formas las\n"
              "  decide la lectura. Lo que sea término propio va a la lista PROPIOS.")
    if vocabulario:
        # Agregadas y no una por aparición. Son palabras que el diccionario no tiene y para
        # las que NO propone la misma palabra con tildes: siglas, latinajos, apellidos,
        # nombres de archivo. Antes salía una línea por cada una y eran el 81% de la salida,
        # que es la forma exacta de que nadie mire las 19 que importan. No se silencian --
        # una falta de verdad que no sea de acento cae acá -- pero se leen de un saque.
        print(f"\n  Vocabulario que el diccionario no conoce: {len(vocabulario)} palabras "
              f"distintas en {sum(vocabulario.values())} apariciones.")
        orden = sorted(vocabulario.items(), key=lambda kv: (-kv[1], kv[0]))
        print("   ", ", ".join(f"{p}({n})" for p, n in orden[:60]))
        if len(orden) > 60:
            print(f"    ... y {len(orden) - 60} más.")
    return 1 if hallazgos or vocabulario else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
