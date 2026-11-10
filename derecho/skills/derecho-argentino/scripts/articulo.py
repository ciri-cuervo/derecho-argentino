#!/usr/bin/env python3
"""Devuelve un artículo de una norma bajada, con su procedencia, sin abrir el archivo entero.

**Existe por una medida y no por comodidad.** `Read` trae 2.000 renglones y trunca sin avisar;
el CCyCN consolidado tiene más de 27.000 y la LCT casi 5.000. Para transcribir el art. 245 el
modelo abría el archivo, leía la primera parte, volvía con `Grep` y cargaba miles de renglones que
no iba a usar, o daba por leído un texto cortado. Acá entra al contexto sólo el artículo pedido,
y arriba va lo que la sección 2 de la skill exige para citarlo: título de la norma, URL oficial,
fecha de descarga y hash.

Uso:
    python3 articulo.py lct-20744 245
    python3 articulo.py lct-20744 245 245bis 232       # varios de una vez
    python3 articulo.py cp-11179 "145 bis"
    python3 articulo.py ccycn-26994 --listar           # qué artículos reconoce el corte
    python3 articulo.py ley-24669 6 --anexo 1          # el art. 6 del tratado que aprueba
    python3 articulo.py --comparar ley-24449:41 "pba-ley-15657:28 quater"

Reconoce los encabezados con que las fuentes oficiales abren un artículo —`ARTICULO 1° —`,
`ARTÍCULO 22 BIS:`, `Art. 245. —`, `Artículo 1° —`, `ARTÍCULO 1º Las...`— y **sólo al principio
del renglón**. Un
`Artículo 145 bis:` citado dentro del cuerpo de otro artículo no corta: viene después de un
renglón que termina en dos puntos anunciando la transcripción, y un encabezado real no.

No corrige nada del texto: lo que sale es lo que está en el `.txt`, con las notas de InfoLEG
sobre sustituciones y derogaciones, que son parte de lo que hay que leer antes de citar. Y no
sabe si el artículo está vigente: eso lo dice la nota que trae, o `changelog-normativo.md`.

**Una ley aprobatoria trae dos numeraciones**: la suya —«Apruébase el Protocolo...»— y la del
texto anexo, que vuelve a empezar en 1. Sin `--anexo`, el corte de siempre: los números que
se repiten se quedan con su primera aparición, así que en `ccycn-26994` los arts. 1 a 8 son los
de la Ley 26.994 y del 9 en adelante los del Código, y en `ley-24669` no hay art. 6 que pedir.
Con `--anexo N` sale sólo la numeración N, contada desde cada vez que el texto vuelve al art. 1,
y ahí también cuenta el encabezado que es el número solo en su renglón —`Artículo 6`—, que es
como vienen los tratados en InfoLEG.

**Las modificatorias que el consolidado todavía no trae.** `normas.json` declara en la norma que
modifica a cuál modifica (`"modifica"`, ver `_modificatorias.py`). Si el artículo pedido no está
en el consolidado, se lo busca en esas modificatorias y se dice dónde está: el art. 28 quater de
la Ley 13.927 lo incorporó la Ley 15.657 y, mientras el consolidado no la recorra, vive sólo ahí.
Y si el artículo sí está pero el consolidado no menciona una modificatoria declarada, sale un
`OJO` al final: el texto puede no traer esa reforma.

**`--comparar` pone dos artículos uno al lado del otro, inciso por inciso.** Sirve para una
adhesión condicionada —el art. 41 de la Ley 24.449 contra el 28 quater bonaerense— o para el
texto anterior y el nuevo de una reforma. **La correspondencia es por la letra del inciso, no por
lo que dice**, y la salida lo advierte: la misma letra puede traer otra regla, y una regla puede
haber cambiado de letra. Se probó emparejar por contenido, con una medida de palabras en común, y
sobre el caso conocido —el 41 contra el 28 quater— se equivocó en cuatro de diez incisos: mandó
el h) y el i) bonaerenses a otros incisos y dejó sin par el g) 3 nacional, que es justo su
antecedente. Se descartó; la comparación la hace quien lee, con los dos textos a la vista. El
texto sale tal cual, salvo los saltos de renglón dentro de un párrafo, que se unen.

Códigos de salida: 0 encontró todo lo pedido; 2 no hay repo, no existe la norma o falta un
artículo, y en los tres casos dice cuál.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _raiz import datos
import _modificatorias

# El encabezado de un artículo, tal como lo escriben InfoLEG, normas.gba y los digestos
# porteños: `ARTICULO 1° —`, `Art. 245. —`, `ARTÍCULO 22 BIS:` y también `Artículo 1° —`, que
# es la grafía de más de cien textos del repositorio. El sufijo latino admite las dos mayúsculas
# que conviven en el mismo cuerpo (`bis`, `BIS`, `quáter`, `QUÁTER`).
ENCABEZADO = re.compile(
    r"^(?:ART[IÍ]CULO|Art\.|Artículo)\s*(?P<numero>\d+)\s*[°º]?\s*"
    r"(?:(?P<sufijo>(?i:bis|ter|qu[aá]ter|quinquies|sexies|septies|octies|nonies|decies))\b)?"
    r"\s*(?:[.:\-—–]|(?=\s+[A-ZÁÉÍÓÚÜÑ¿(«\"]))")

# Una ley que incorpora un artículo a otra lo transcribe: `Incorpórase como artículo 145 bis
# del Código Penal, el siguiente:` y en el renglón de abajo `Artículo 145 bis: El que...`. Ese
# renglón tiene forma de encabezado y no lo es. Lo delata el renglón anterior, que anuncia la
# transcripción —«el siguiente:», «redactado de la siguiente manera:»— y termina en dos puntos.
# Que termine en dos puntos no alcanza: «sancionan con fuerza de Ley:» precede al art. 1 de
# toda ley de InfoLEG, y con esa sola señal el art. 1 desaparecía de todas.
ANUNCIA_TRANSCRIPCION = re.compile(
    r"(siguiente|redactad[oa]|sustit[uú]|incorp[oó]r|reempl[aá]z|modif[ií]c)[^\n]*:\s*$", re.I)

PROCEDENCIA = ("Fuente:", "Descargado:", "SHA-256")

# Sólo para los anexos: además, el número solo en su renglón. No entra al corte principal porque
# en él ese renglón partía artículos de más de cuarenta normas que hoy se citan bien.
ENCABEZADO_ANEXO = re.compile(ENCABEZADO.pattern[:-1] + r"|\s*$)")


def clave(numero: str, sufijo: str | None) -> str:
    s = (sufijo or "").lower().replace("á", "a")
    return f"{int(numero)}{' ' + s if s else ''}"


def pedido(texto: str) -> str:
    """Normaliza lo que tipea el usuario: `245bis`, `245 BIS` y `245 bis` son el mismo."""
    m = re.fullmatch(r"\s*(\d+)\s*([A-Za-zÁá]+)?\s*", texto)
    if not m:
        raise ValueError(f"no entiendo el artículo «{texto}»: se espera un número y, si hace "
                         f"falta, bis/ter/quater")
    return clave(m.group(1), m.group(2))


# Respaldo para los textos donde el corte principal no encuentra ningún artículo: el número solo
# con su raya —`2º —`, el Reglamento para la Justicia Nacional—, el ordinal escrito con la letra
# o —`Artículo 1o:`— y el encabezado partido en dos renglones —`ARTICULO` y abajo `1º.- La`—.
# Corre únicamente si el principal devuelve vacío, así que no toca ningún texto que ya se lea.
ENCABEZADO_RESPALDO = re.compile(
    r"^(?:(?:ART[IÍ]CULO|Art\.|Artículo)\s*)?(?P<numero>\d+)\s*(?:[°º]|o(?=\s*[.:\-—–]))?\s*"
    r"(?:(?P<sufijo>(?i:bis|ter|qu[aá]ter|quinquies|sexies|septies|octies|nonies|decies))\b)?"
    r"\s*[.:\-—–]+\s")


def _unir_encabezados_partidos(cuerpo: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(cuerpo):
        if (re.fullmatch(r"\s*ART[IÍ]CULO\s*", cuerpo[i], re.I) and i + 1 < len(cuerpo)
                and re.match(r"\s*\d", cuerpo[i + 1])):
            out.append(cuerpo[i].strip() + " " + cuerpo[i + 1].strip())
            i += 2
            continue
        out.append(cuerpo[i])
        i += 1
    return out


# `Art.` solo en su renglón y abajo `102. – El título...`: el Decreto-Ley 5965/63 de InfoLEG parte
# así dos encabezados, y sin unirlos el artículo queda pegado al anterior y no se encuentra. Va
# antes del corte principal porque un renglón que es sólo `Art.` no puede ser otra cosa.
def _unir_art_partido(cuerpo: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(cuerpo):
        if (cuerpo[i].strip() == "Art." and i + 1 < len(cuerpo)
                and re.match(r"\s*\d+\s*[°º]?\s*\.\s*[\-—–]", cuerpo[i + 1])):
            out.append("Art. " + cuerpo[i + 1].strip())
            i += 2
            continue
        out.append(cuerpo[i])
        i += 1
    return out


# El encabezado de la división que sigue —«TÍTULO X», «CAPITULO 3», «SECCION 2ª»— queda abajo del
# último artículo de la anterior, y el corte lo arrastraba: el art. 28 quater del consolidado de
# la Ley 13.927 terminaba en «TÍTULO X BASES PARA EL PROCEDIMIENTO». Medido sobre `fuentes/` el
# 10/11/2026, pasaba en miles de artículos: la cifra, en `docs/BITACORA.md`. Tres condiciones
# para cortar, y cada una salió de un caso que se equivocaba sin ella:
#   - la palabra va en mayúsculas o con inicial: «parte,» en minúscula es prosa;
#   - el renglón anterior está en blanco: «...según lo dispuesto en el / Capítulo 2 de este
#     Titulo.» es una oración partida, no un encabezado (art. 566 CCyCN);
#   - lo que precede no anuncia una transcripción con dos puntos: en «Apruébase como Régimen
#     Penal Tributario el siguiente texto: / Título I - Delitos Tributarios» (art. 279 de la Ley
#     27.430) el encabezado es lo que el artículo incorpora.
# Debajo del encabezado sólo puede haber renglones de encabezado: notas entre paréntesis,
# mayúsculas, o un subtítulo corto, sin puntuación final y después de un blanco, como «Del
# financiamiento».
DIVISION = re.compile(r"^(?:T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N|LIBRO|PARTE|T[íi]tulo|Cap[íi]tulo"
                      r"|Secci[óo]n|Libro|Parte)\b")


def _corto_sin_cierre(l: str) -> bool:
    return 0 < len(l) < 80 and not re.search(r"[.;:,]$", l)


def _de_encabezado(ls: list[str], i: int) -> bool:
    l = ls[i].strip()
    if (not l or (l.startswith("(") and l.endswith(")"))
            or (len(l) < 150 and (DIVISION.match(l) or not re.search(r"[a-záéíóúüñ]", l)))):
        return True
    if not _corto_sin_cierre(l):
        return False
    # Un subtítulo va después de un blanco, y puede seguir en el renglón de abajo: «Sistema
    # Integral de Prestaciones por / Desempleo» (Ley 25.191). Un renglón corto pegado a un
    # párrafo es prosa partida.
    j = i - 1
    while j >= 0 and _corto_sin_cierre(ls[j].strip()):
        j -= 1
    return j >= 0 and not ls[j].strip()


def _sin_division_siguiente(ls: list[str]) -> list[str]:
    """El artículo sin el encabezado de la división que lo sigue, si lo arrastró."""
    corte, i = None, len(ls)
    while i > 1 and _de_encabezado(ls, i - 1):
        if DIVISION.match(ls[i - 1].strip()) and not ls[i - 2].strip():
            corte = i - 1
        i -= 1
    if corte is None:
        return ls
    previo = next((l.strip() for l in reversed(ls[:corte]) if l.strip()), "")
    if previo.endswith(":"):
        return ls
    ls = ls[:corte]
    while ls and not ls[-1].strip():
        ls.pop()
    return ls


def partir(cuerpo: list[str]) -> dict[str, list[str]]:
    """Cada artículo con sus renglones, en orden de aparición. Lo anterior al primero se descarta."""
    articulos = _partir(_unir_art_partido(cuerpo), ENCABEZADO)
    if not articulos:
        articulos = _partir(_unir_encabezados_partidos(cuerpo), ENCABEZADO_RESPALDO)
    return articulos


def _partir(cuerpo: list[str], encabezado_re) -> dict[str, list[str]]:
    articulos: dict[str, list[str]] = {}
    actual = None
    anterior = ""
    for linea in cuerpo:
        m = encabezado_re.match(linea)
        if m and ANUNCIA_TRANSCRIPCION.search(anterior):
            m = None
        if linea.strip():
            anterior = linea
        if m:
            actual = clave(m.group("numero"), m.group("sufijo"))
            # Un mismo número dos veces es el consolidado intercalando texto viejo: se queda
            # el primero, que es el vigente en las fuentes que hacen eso.
            if actual in articulos:
                actual = None
                continue
            articulos[actual] = [linea]
        elif actual is not None:
            articulos[actual].append(linea)
    for k, ls in articulos.items():
        while ls and not ls[-1].strip():
            ls.pop()
        articulos[k] = _sin_division_siguiente(ls)
    return articulos


def anexos(cuerpo: list[str]) -> list[dict[str, list[str]]]:
    """Cada numeración del texto por separado: la 0 es la de la norma y la N, la del anexo N.

    Una numeración nueva empieza cuando vuelve el art. 1 ya visto; otro número repetido es el
    consolidado intercalando texto viejo, y se queda el primero."""
    bloques: list[dict[str, list[str]]] = [{}]
    actual = None
    anterior = ""
    for linea in cuerpo:
        m = ENCABEZADO_ANEXO.match(linea)
        if m and ANUNCIA_TRANSCRIPCION.search(anterior):
            m = None
        if linea.strip():
            anterior = linea
        if m:
            actual = clave(m.group("numero"), m.group("sufijo"))
            if actual in bloques[-1]:
                if actual != "1":
                    actual = None
                    continue
                bloques.append({})
            bloques[-1][actual] = [linea]
        elif actual is not None:
            bloques[-1][actual].append(linea)
    for articulos in bloques:
        for k, ls in articulos.items():
            while ls and not ls[-1].strip():
                ls.pop()
            articulos[k] = _sin_division_siguiente(ls)
    return bloques


def encabezado(lineas: list[str]) -> list[str]:
    """Título y procedencia, que son las primeras líneas del `.txt` que escribe el descargador."""
    salida = [lineas[0].rstrip()] if lineas else []
    for l in lineas[1:20]:
        if l.startswith(PROCEDENCIA):
            salida.append(l.rstrip())
    return salida


def carpeta_normas(repo=None) -> Path | None:
    d = datos(repo)
    return None if d is None else d.parent / "normas"


# --- Comparación inciso por inciso -------------------------------------------------------
INCISO = re.compile(r"^([a-zA-ZñÑ])\)\s*(.*)", re.S)
SUBINCISO = re.compile(r"^(\d{1,2})\s*[.)]\s+(.*)", re.S)


def parrafos(lineas: list[str]) -> list[str]:
    """Los párrafos del artículo, sin su encabezado y con los renglones de cada uno unidos."""
    salida, actual = [], []
    for linea in lineas:
        if linea.strip():
            actual.append(linea.strip())
        elif actual:
            salida.append(" ".join(actual))
            actual = []
    if actual:
        salida.append(" ".join(actual))
    if salida:
        # Sin el encabezado ni la raya que lo separa del epígrafe: «ARTICULO 41. — PRIORIDADES.»
        salida[0] = ENCABEZADO.sub("", salida[0], count=1).strip().lstrip("—–-").strip()
    return [s.strip().strip("“”\"").strip() for s in salida if s.strip().strip("“”\"")]


def unidades(lineas: list[str]) -> tuple[list[str], list[tuple[str, str]], list[str]]:
    """(antes de los incisos, [(rótulo, texto)], después de los incisos).

    Un párrafo que no abre inciso y cae entre dos incisos es continuación del anterior y se le
    suma; después del último inciso, todo va a «después». Un inciso de varios párrafos al final
    del artículo queda partido entre su rótulo y «después», y por eso la salida imprime los dos
    bloques enteros."""
    antes, incisos, pendientes = [], [], []
    ultimo = None
    for par in parrafos(lineas):
        m = INCISO.match(par)
        s = None if m else SUBINCISO.match(par)
        if not m and not s:
            (pendientes if incisos else antes).append(par)
            continue
        if pendientes:
            rotulo, texto = incisos[-1]
            incisos[-1] = (rotulo, " ".join([texto, *pendientes]))
            pendientes = []
        if m:
            ultimo = m.group(1).lower()
            incisos.append((f"{ultimo})", m.group(2).strip()))
        else:
            rotulo = f"{ultimo}) {s.group(1)}." if ultimo else f"{s.group(1)}."
            incisos.append((rotulo, s.group(2).strip()))
    return antes, incisos, pendientes


def _cargar_articulo(normas: Path, spec: str):
    partes = spec.split(":")
    if len(partes) not in (2, 3):
        raise ValueError(f"«{spec}»: se espera norma:artículo, o norma:artículo:anexo")
    slug, art = partes[0], partes[1]
    if len(partes) == 3 and not partes[2].isdigit():
        raise ValueError(f"«{spec}»: el anexo va en número, como en ley-24669:6:1")
    anexo = int(partes[2]) if len(partes) == 3 else 0
    archivo = normas / f"{slug}.txt"
    if not archivo.is_file():
        raise ValueError(f"no existe {archivo.name} en {normas}")
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    bloques = anexos(lineas)
    if anexo and not 0 < anexo < len(bloques):
        raise ValueError(f"{archivo.name} no tiene anexo {anexo}: tiene {len(bloques) - 1}")
    articulos = bloques[anexo] if anexo else partir(lineas)
    k = pedido(art)
    if k not in articulos:
        raise ValueError(f"no se encontró el art. {k} en {archivo.name}"
                         + (f", anexo {anexo}" if anexo else ""))
    donde = f"{slug}, art. {k}" + (f", anexo {anexo}" if anexo else "")
    return encabezado(lineas), donde, articulos[k]


def comparar(normas: Path, spec_a: str, spec_b: str) -> int:
    try:
        cab_a, donde_a, art_a = _cargar_articulo(normas, spec_a)
        cab_b, donde_b, art_b = _cargar_articulo(normas, spec_b)
    except ValueError as e:
        print(f"No se puede comparar: {e}. Lo que no salió de acá no se cita de memoria.")
        return 2
    for cab in (cab_a, cab_b):
        for linea in cab:
            print(linea)
        print()
    antes_a, inc_a, desp_a = unidades(art_a)
    antes_b, inc_b, desp_b = unidades(art_b)
    print("COMPARACIÓN INCISO POR INCISO")
    print(f"  A = {donde_a}")
    print(f"  B = {donde_b}")
    print()
    print("  La correspondencia es por la letra del inciso y no por lo que dice: la misma letra")
    print("  puede traer otra regla, y una regla puede haber cambiado de letra. Se lee cada par")
    print("  entero antes de afirmar qué cambió.")

    def bloque(titulo, a, b):
        print(f"\n--- {titulo}")
        for t in a or ["(nada)"]:
            print(f"  A | {t}")
        for t in b or ["(nada)"]:
            print(f"  B | {t}")

    bloque("antes de los incisos", antes_a, antes_b)
    da, db = dict(inc_a), dict(inc_b)
    orden = list(da) + [r for r in db if r not in da]
    for rotulo in orden:
        bloque(f"inc. {rotulo}", [da[rotulo]] if rotulo in da else ["(no tiene)"],
               [db[rotulo]] if rotulo in db else ["(no tiene)"])
    bloque("después de los incisos", desp_a, desp_b)
    solo_a = [r for r in da if r not in db]
    solo_b = [r for r in db if r not in da]
    print()
    print(f"Incisos sólo en A: {', '.join(solo_a) or 'ninguno'}")
    print(f"Incisos sólo en B: {', '.join(solo_b) or 'ninguno'}")
    iguales = [r for r in da if r in db and " ".join(da[r].split()) == " ".join(db[r].split())]
    print(f"Mismo inciso con el mismo texto: {', '.join(iguales) or 'ninguno'}")
    return 0


def _ojo_modificatorias(normas: Path, slug: str, texto: str) -> list[str]:
    try:
        entradas = _modificatorias.catalogo(normas)
    except (OSError, ValueError, KeyError):
        return []
    propia = next((n for n in entradas if n.get("slug") == slug), {})
    if _modificatorias.es_original(propia):
        return [f"  OJO: éste es el texto original y {_modificatorias.nombre(m)} "
                f"({m['slug']}) lo modifica: lo que trae acá puede no ser lo vigente. Cotejar "
                f"con articulo.py {m['slug']} --listar."
                for m in _modificatorias.sin_reflejar(slug, texto, entradas)]
    return [f"  OJO: {_modificatorias.nombre(m)} ({m['slug']}) modifica esta norma y el "
            f"consolidado no la menciona: lo que trae acá puede no reflejar esa reforma. "
            f"Cotejar con articulo.py {m['slug']} --listar."
            for m in _modificatorias.sin_reflejar(slug, texto, entradas)]


def _transcribe(lineas: list[str], k: str) -> int | None:
    """El renglón donde el artículo transcribe el encabezado del art. `k` de otra norma."""
    for i, l in enumerate(lineas[1:], 1):
        h = ENCABEZADO.match(l.lstrip("“\"« "))
        if h and clave(h.group("numero"), h.group("sufijo")) == k:
            return i
    return None


def _buscar_en_modificatorias(normas: Path, slug: str, k: str) -> list[str]:
    try:
        entradas = _modificatorias.catalogo(normas)
    except (OSError, ValueError, KeyError):
        return []
    salida = []
    for m in _modificatorias.modificadoras_de(slug, entradas):
        archivo = normas / f"{m['slug']}.txt"
        if not archivo.is_file():
            continue
        propios = partir(archivo.read_text(encoding="utf-8").splitlines())
        # Primero, el artículo transcripto adentro de uno propio: «Modifíquese el artículo 9º
        # [...] de la siguiente forma: / Artículo 9º: ...». El número propio de la modificatoria
        # no sirve para esto: la Ley 27.793 tiene su art. 9, y no es el art. 9 de la 13.478 que
        # transcribe su art. 5.
        # Y el artículo propio tiene que nombrar a esta norma antes de la transcripción: el art.
        # 15 de la misma Ley 27.793 también transcribe un «Artículo 9º», y es el de la 24.901.
        titulo = next((n.get("titulo", "") for n in entradas if n.get("slug") == slug), "")
        transcriben = [n for n, ls in propios.items()
                       if _transcribe(ls, k) is not None
                       and _modificatorias.menciona(" ".join(ls[:_transcribe(ls, k)]), titulo)]
        for n in transcriben:
            salida.append(f"  Lo transcribe el art. {n} de {_modificatorias.nombre(m)}, que "
                          f"modifica esta norma: python3 articulo.py {m['slug']} \"{n}\"")
        # Si no, el artículo incorporado con encabezado propio, como el 28 quater de la Ley
        # 13.927 en la Ley 15.657.
        if not transcriben and k in propios:
            salida.append(f"  Lo trae {_modificatorias.nombre(m)}, que modifica esta norma: "
                          f"python3 articulo.py {m['slug']} \"{k}\"")
    return salida


def main(argv=None) -> int:
    # Hay textos bajados con caracteres que cp1252 no tiene (■, ✓, №). Escaparlos deja la cita
    # visiblemente marcada; sin esto la consola de Windows corta con UnicodeEncodeError.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("norma", nargs="?",
                   help="slug del texto en fuentes/normas/, sin .txt: lct-20744")
    p.add_argument("articulo", nargs="*", help="245, 245bis, «145 bis»")
    p.add_argument("--listar", action="store_true",
                   help="lista los artículos que reconoce en vez de imprimir uno")
    p.add_argument("--anexo", type=int, default=0,
                   help="numeración del texto anexo: 1 es el tratado o el código que la ley "
                        "aprueba")
    p.add_argument("--repo", help="ruta al repo, si no está configurada")
    p.add_argument("--comparar", nargs=2, metavar="NORMA:ART",
                   help="dos artículos, uno al lado del otro por inciso: "
                        "ley-24449:41 \"pba-ley-15657:28 quater\"")
    a = p.parse_args(argv)
    if a.comparar and (a.norma or a.articulo or a.listar or a.anexo):
        p.error("--comparar va solo: norma, artículo y anexo van adentro de cada NORMA:ART")
    if not a.comparar and not a.norma:
        p.error("falta la norma: por ejemplo lct-20744 245, o --comparar")

    normas = carpeta_normas(a.repo)
    if normas is None:
        print("No hay repo configurado: correr configurar.py --repo <ruta>, o pasar --repo.")
        return 2
    if a.comparar:
        return comparar(normas, *a.comparar)
    archivo = normas / f"{a.norma}.txt"
    if not archivo.is_file():
        print(f"No existe {archivo}. El slug es el del manifiesto normas.json; los bajados "
              f"están en {normas}.")
        # Una norma sin texto bajado puede tener su artículo vigente transcripto en la que lo
        # modificó: el art. 9 de la Ley 13.478, que no tiene fuente oficial descargable.
        for pedido_ in a.articulo:
            for pista in _buscar_en_modificatorias(normas, a.norma, pedido(pedido_)):
                print(pista)
        return 2
    texto = archivo.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    if a.anexo:
        bloques = anexos(lineas)
        if not 0 < a.anexo < len(bloques):
            print(f"{archivo.name} no tiene anexo {a.anexo}: tiene {len(bloques) - 1} con "
                  f"numeración propia.")
            return 2
        articulos = bloques[a.anexo]
        donde = f"{a.norma}, anexo {a.anexo}"
    else:
        articulos = partir(lineas)
        donde = a.norma
        bloques = anexos(lineas)

    for l in encabezado(lineas):
        print(l)
    print()

    if a.listar:
        print(f"{len(articulos)} artículos reconocidos en {donde}:")
        print("  " + ", ".join(articulos))
        otros = len(anexos(lineas)) - 1
        if otros and not a.anexo:
            print(f"\nTiene {otros} anexo(s) con numeración propia: ver --anexo 1.")
        ojos = _ojo_modificatorias(normas, a.norma, texto)
        if ojos:
            print()
            print("\n".join(ojos))
        return 0
    if not a.articulo:
        print("Falta decir qué artículo: por ejemplo 245, o --listar para ver cuáles hay.")
        return 2

    faltan = []
    for pedido_ in a.articulo:
        try:
            k = pedido(pedido_)
        except ValueError as e:
            print(f"  {e}")
            faltan.append(pedido_)
            continue
        if k not in articulos:
            print(f"  No se encontró el art. {k} en {archivo.name}: puede estar numerado de "
                  f"otra forma, o el corte no lo reconoce. Ver --listar.")
            for pista in _buscar_en_modificatorias(normas, a.norma, k):
                print(pista)
            faltan.append(pedido_)
            continue
        print(f"--- art. {k} · {donde}")
        print("\n".join(articulos[k]))
        print()
        if not a.anexo and articulos[k] == bloques[0].get(k):
            con_el_mismo = [str(n) for n, b in enumerate(bloques[1:], 1) if k in b]
            if con_el_mismo:
                lista = " y ".join(con_el_mismo)
                print(f"  OJO: este es el art. {k} de la norma. También hay un art. {k} en "
                      f"{'el anexo' if len(con_el_mismo) == 1 else 'los anexos'} {lista}: si se "
                      f"busca el del texto aprobado —el código o el tratado—, repetir con "
                      f"--anexo {con_el_mismo[0]}.")
                print()
    ojos = _ojo_modificatorias(normas, a.norma, texto)
    if ojos:
        print("\n".join(ojos))
        print()
    if faltan:
        print(f"Sin encontrar: {', '.join(faltan)}. Lo que no salió de acá no se cita de memoria.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
