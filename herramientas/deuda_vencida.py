#!/usr/bin/env python3
"""Reclamos de faltante que la propia carpeta `fuentes/` ya desmiente.

Un módulo dice "la Ley X no está bajada", alguien la baja, y **el reclamo sobrevive al hecho**.
Lo caro no es el renglón viejo: es que una lista de deuda con entradas falsas se deja de leer
entera, y con ella las que sí importan.

**No infiere de la prosa cuál norma se reclama: la cruza contra el catálogo.** Inferir el
sujeto de la frase no funciona -está medido en `docs/PENDIENTES.md`- porque puede ir después,
o no ser una norma sino un fallo o un régimen provincial. Acá se hace al revés: se toman los
números que el catálogo de `normas.json` ya declara y se busca cuál de ellos aparece en un
renglón que reclama un faltante. Si esa norma está bajada, el renglón es candidato.

**El cruce llega al párrafo, no al renglón.** La prosa envuelve por ancho y el número de la
norma queda arriba del reclamo; acotado al renglón, el control no veía esos casos y **no lo
decía**: el renglón simplemente no producía candidato. Comprobado con la mutación que está
nombrada en `TestElAlcanceDelCruce`, de `test_deuda.py`, y que ocurrió sola en el árbol.

**Cruza contra dos catálogos, no contra uno.** El de normas, por número, y el de
jurisprudencia —`fuentes/jurisprudencia/fallos.json`—, por el apellido de la carátula, que es
como el repositorio nombra un fallo: entrecomillado. En los dos casos el cruce exige que el
documento esté **en disco**, porque estar declarado es lo que el reclamo dice.

**Las series de `fuentes/datos/` NO se cruzan, y es una decisión medida.** Derivar el índice de
los nombres de archivo dispara cuatro veces sobre los reclamos del árbol y **las cuatro
equivocado** —«UMA porteña» contra `uma-csjn.csv`, que es la nacional; «acordadas de la CSJN»
contra el `csjn` de ese mismo nombre—, y no alcanza a ninguno de los tres reclamos de serie que
sí existen. Una medida que se equivoca sobre un caso conocido no sirve para los desconocidos.

**Y dice qué NO mira.** Los reclamos cuya unidad no nombra nada catalogado se informan siempre,
con `--sin-cruzar` para verlos. Lo que queda es la categoría abierta —«su ley arancelaria
local», «los estatutos locales»—, que no tiene contra qué cruzarse porque lo que falta es un
conjunto, no una pieza. Se lee.

**Candidatos, no culpables**, igual que `fuga_textual.py`. La mayoría son legítimos: el
renglón nombra la norma bajada y lo que falta es OTRA cosa -la reglamentación de la Ley
27.793, los umbrales del Título IX de la 27.430, la lista de jurisdicciones adheridas al art.
34 de la 23.737-. Esos se leen una vez, se aceptan con `--aceptar` y no vuelven a aparecer.
Lo que queda después es lo nuevo.

Uso:
    python3 herramientas/deuda_vencida.py
    python3 herramientas/deuda_vencida.py --aceptar --nota 'por qué quedó así'
"""
from __future__ import annotations

import argparse
import json
import hashlib
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _veredictos  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
NORMAS = RAIZ / "derecho" / "fuentes" / "normas"
JURIS = RAIZ / "derecho" / "fuentes" / "jurisprudencia"
BASE = pathlib.Path(__file__).resolve().parent / "deuda-revisada.json"

# Un reclamo de faltante, en cualquiera de las formas en que el repositorio lo escribe.
RECLAMO = re.compile(r"no est[áa]n? (?:bajad|cargad)[ao]s?|falta[n]? (?:bajar|cargar)|"
                     r"no est[áa] en `?fuentes", re.I)
# Un fallo citado por su nombre corto, que el repositorio escribe SIEMPRE entre comillas
# rectas: "Rayford", **"Quaranta"**, *"Obarrio"*. El énfasis va por fuera de las comillas.
ENTRECOMILLADO = re.compile(r'"([^"\n]{2,90})"')
# La clase va SIN acentos y sin Ñ a propósito: lo que los resuelve es `pelado()`, que corre
# antes y de los dos lados -«Agüero» y AGÜERO llegan los dos como AGUERO, y PEÑA como PENA-.
# Agregarle `ÜÁÑ` no arreglaría nada y haría creer que el acento se maneja acá.
# Punto ciego declarado: el apellido es el PRIMER token, así que un compuesto que arranca con
# partícula corta -«San Martín», «De la Rosa»- no se indexa. Hoy no hay ninguno en el catálogo.
APELLIDO = re.compile(r"[A-Z][A-Z'.-]{3,}")
# Una norma citada por su número. El número decide, no el nombre.
CITA = re.compile(r"\b(?:Ley|Decreto|Dec\.|Res\.|Acuerdo)\s*n?[º°]?\s*([\d.]+(?:/\d{2,4})?)", re.I)
# Fuera del alcance: capa 2 y lo que documenta el problema en vez de cometerlo. El registro de
# verificación entra en lo segundo: cada fila dice qué se cotejó y qué falta, con su fecha, y
# eso es su contenido, no un reclamo que se olvidó de actualizar. Lo que esas filas afirman
# sobre normas sin bajar lo mide `cobertura_normativa.py`, así que excluirlas no deja hueco.
EXCLUIDOS = ("derecho/kb/", "derecho/fuentes/_local", "docs/PENDIENTES.md",
             "derecho/skills/derecho-argentino/references/changelog-normativo.md")
# Dónde corta una unidad de lectura. El blanco, un título, una fila de tabla y el comienzo de
# un ítem separan; `>` no, porque una cita envuelve igual que un párrafo.
CORTE = re.compile(r"^\s*(?:$|#{1,6}\s|\||[-*+]\s|\d+[.)]\s)")


def catalogo() -> dict[str, list[str]]:
    """Número de norma -> slugs que lo declaran. Sale de `normas.json`, no de la prosa."""
    idx: dict[str, list[str]] = {}
    for e in json.loads((NORMAS / "normas.json").read_text(encoding="utf-8"))["normas"]:
        for m in re.finditer(r"\b(\d{1,3}\.\d{3}|\d{4,5})\b", e["titulo"]):
            idx.setdefault(m.group(1).replace(".", ""), []).append(e["slug"])
        for m in re.finditer(r"(\d{3,5})[-/](\d{4})", e["slug"] + " " + e["titulo"]):
            idx.setdefault(f"{m.group(1)}/{m.group(2)}", []).append(e["slug"])
    return idx


def pelado(s: str) -> str:
    """Mayúsculas y sin diacríticos. Un apellido se compara pelado y se muestra como está."""
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").upper()


def jurisprudencia() -> dict[str, list[str]]:
    """Apellido -> slugs de los fallos **que están en disco**. Sale del catálogo, no de la prosa.

    Punto ciego declarado y medido: las carátulas anonimizadas -«E., M. R. c/ L., M. F.»- no
    tienen apellido que indexar. Son las de familia y violencia, y tampoco se citan por
    apellido, así que un reclamo sobre una de ellas no se cruza.
    """
    archivo = JURIS / "fallos.json"
    if not archivo.is_file():
        return {}
    d = json.loads(archivo.read_text(encoding="utf-8"))
    fallos = d["fallos"] if isinstance(d, dict) and "fallos" in d else d
    idx: dict[str, list[str]] = {}
    for f in fallos:
        slug = f.get("slug")
        if not slug or not list(JURIS.glob(f"{slug}.*")):
            continue
        m = APELLIDO.match(pelado(f.get("caratula", "")))
        if m:
            idx.setdefault(m.group(0), []).append(slug)
    return idx


def nombrados(unidad: str) -> list[str]:
    """Los apellidos entrecomillados de la unidad, pelados. Es la clave contra el catálogo."""
    out = []
    for m in ENTRECOMILLADO.finditer(unidad):
        a = APELLIDO.match(pelado(m.group(1)).lstrip("*_ "))
        if a:
            out.append(a.group(0))
    return out


def huella(linea: str) -> str:
    """Ocho hexadecimales del renglón normalizado. Es la identidad del reclamo.

    La clave NO lleva el número de renglón: con la posición adentro, agregar una fila más arriba
    reabre todo lo ya leído y la línea de base se vuelve ruido. Con la huella, lo que reabre un
    reclamo es que alguien **cambie lo que dice**, que es cuando hay que volver a leerlo.
    """
    return hashlib.sha1(" ".join(linea.split()).encode("utf-8")).hexdigest()[:8]


def unidades(lineas: list[str]) -> list[str]:
    """Para cada renglón, el texto de la unidad que integra. Es el alcance del cruce.

    **El reclamo y el número de su norma se separan al cortar el renglón**: la prosa envuelve
    por ancho y el número queda arriba. Buscar la cita en el renglón del reclamo deja ciega a
    la mitad de los casos, y la ceguera no se ve: el renglón simplemente no produce candidato.

    Una unidad es lo que se escribe junto —un párrafo, un ítem de lista, una fila de tabla—.
    La tabla va fila por fila a propósito: unida entera, un número de la fila 5 se cruzaría
    contra un reclamo de la 40.
    """
    texto = [""] * len(lineas)
    bloque: list[int] = []

    def cerrar() -> None:
        if not bloque:
            return
        junto = " ".join(lineas[i].strip() for i in bloque)
        for i in bloque:
            texto[i] = junto
        bloque.clear()

    for i, linea in enumerate(lineas):
        if CORTE.match(linea):
            cerrar()
            if not linea.strip():
                continue
        bloque.append(i)
    cerrar()
    return texto


def _reclamos() -> tuple[set[str], list[str]]:
    """Los candidatos y los reclamos que este control NO cruza, en una sola pasada del árbol."""
    idx, juris = catalogo(), jurisprudencia()
    out: set[str] = set()
    ciegos: list[str] = []
    for f in sorted(RAIZ.rglob("*.md")):
        rel = f.relative_to(RAIZ).as_posix()
        if rel.startswith(EXCLUIDOS) or "/.git/" in rel:
            continue
        lineas = f.read_text(encoding="utf-8").splitlines()
        texto = unidades(lineas)
        for n, linea in enumerate(lineas, 1):
            if not RECLAMO.search(linea):
                continue
            unidad = texto[n - 1]
            apellidos = [a for a in nombrados(unidad) if a in juris]
            if not CITA.search(unidad) and not apellidos:
                ciegos.append(f"{rel}:{n}")
                continue
            for m in CITA.finditer(unidad):
                clave = m.group(1).rstrip(".").replace(".", "")
                for slug in idx.get(clave, []):
                    if (NORMAS / f"{slug}.txt").is_file():
                        # La huella sigue siendo del RENGLÓN y no de la unidad: con la unidad
                        # adentro, editar el renglón de al lado reabriría un reclamo intacto.
                        out.add(f"{rel}:{slug}:{huella(linea)}")
            for a in apellidos:
                for slug in juris[a]:
                    out.add(f"{rel}:{slug}:{huella(linea)}")
    return out, ciegos


def candidatos() -> list[str]:
    """Cada candidato es `ruta:slug:huella`, y la huella es del renglón, no de su posición."""
    return sorted(_reclamos()[0])


def sin_cruzar() -> list[str]:
    """Los reclamos cuya unidad no nombra nada catalogado: este control no los mira.

    Se informan siempre, porque una medida que saltea en silencio reporta verde con el
    instrumento apagado. No todos son deuda: un fallo nombrado y una serie de datos tienen
    catálogo propio y todavía no se cruzan; una categoría abierta —«su ley arancelaria
    local»— no tiene contra qué cruzarse y se lee. Un número que el catálogo no declara **no**
    entra acá: eso lo mide `cobertura_normativa.py`.
    """
    return _reclamos()[1]


def ciego_dice(ciegos: list[str]) -> str:
    """Lo que el control NO miró, dicho en su propia salida y no sólo en `docs/PENDIENTES.md`."""
    if not ciegos:
        return "y ningún reclamo fuera de su alcance: todos nombran algo del catálogo"
    return (f"y {len(ciegos)} reclamos que NO cruza: su unidad no nombra ni una norma del "
            f"catálogo ni un fallo con carátula -verlos con --sin-cruzar-")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--purgar", action="store_true",
                   help="Saca de la línea de base los reclamos que ya no enganchan ningún renglón")
    p.add_argument("--aceptar", action="store_true",
                   help="Fija los candidatos actuales como leídos: dejan de reportarse")
    p.add_argument("--nota", default=None, help="Por qué quedó en este estado")
    p.add_argument("--sin-cruzar", action="store_true",
                   help="Lista los reclamos que este control no mira, uno por renglón")
    a = p.parse_args(argv)

    sobre, revisados = _veredictos.cargar(BASE, "reclamos", vacio=[])
    # El sobre se siembra acá y no a mano: un archivo de veredicto sin `_descripcion` no dice
    # quién lo consume, y `_veredictos.cargar` se planta la próxima vez que alguien lo lea.
    sobre.setdefault("_descripcion", "")
    if not sobre["_descripcion"]:
        sobre["_descripcion"] = (
            "Reclamos de faltante ya revisados: el renglón nombra una norma bajada pero lo "
            "que reclama es otra cosa. Lo consume herramientas/deuda_vencida.py.")
        sobre["_criterio"] = (
            "Un candidato entra acá SOLO si se leyó el renglón y lo que falta no es la norma "
            "nombrada. Si la norma se bajó y nadie actualizó el renglón, se corrige el "
            "renglón y no se acepta el candidato.")
    cand, ciegos = _reclamos()
    actuales = sorted(cand)
    nuevos = [c for c in actuales if c not in set(revisados)]

    if a.sin_cruzar:
        for c in ciegos:
            print(f"  {c}")
        print(f"\nreclamos que este control no cruza: {len(ciegos)}")
        return 0

    muertos = [k for k in revisados if k not in set(actuales)]
    if revisados:
        print(f"línea de base: {len(revisados)} reclamos revisados el {sobre.get('fijado')}"
              + (f", de los cuales {len(muertos)} MUERTOS" if muertos else "") + "\n")
        if muertos:
            print("  Un reclamo muerto es una clave que ya no engancha ningún renglón: el texto")
            print("  cambió de redacción o se mudó de archivo. No esconde nada —nunca va a")
            print("  coincidir— pero infla la línea de base, y una lista inflada se deja de leer.")
            print("  Lo que SÍ guarda es memoria: si el renglón volviera escrito igual, seguiría")
            print("  aceptado sin que nadie lo relea. Por eso se purgan a pedido y no solos:")
            print("      python3 herramientas/deuda_vencida.py --purgar\n")
    fallos = {s for ss in jurisprudencia().values() for s in ss}
    for c in nuevos:
        ruta, slug, _ = c.rsplit(":", 2)
        que = "el fallo" if slug in fallos else "la norma"
        print(f"  {ruta}")
        print(f"      reclama un faltante y nombra {que} `{slug}`, que SÍ está en fuentes/")

    if a.purgar:
        if not muertos:
            print("no hay reclamos muertos que purgar")
            return 0
        _veredictos.guardar(BASE, sobre, "reclamos", sorted(set(actuales) & set(revisados)))
        print(f"\npurgados {len(muertos)} reclamos muertos de {BASE.name}")
        return 0

    if a.aceptar and nuevos:
        if a.nota:
            sobre["nota"] = a.nota
        _veredictos.guardar(BASE, sobre, "reclamos", sorted(set(revisados) | set(actuales)))
        print(f"\nfijados {len(nuevos)} reclamos nuevos en {BASE.name}")
        return 0
    if not nuevos:
        print("deuda vencida: 0 reclamos nuevos")
        print(ciego_dice(ciegos))
        return 0
    print(f"\ndeuda vencida: {len(nuevos)} reclamos NUEVOS, sin revisar")
    print(ciego_dice(ciegos))
    print("Leerlos uno por uno. Si lo que falta es otra cosa -la reglamentación, un umbral,")
    print("una lista- el reclamo es legítimo y va a la línea de base con --aceptar. Si la")
    print("norma se bajó y nadie actualizó el renglón, se corrige el renglón.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
