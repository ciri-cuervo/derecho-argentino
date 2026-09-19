#!/usr/bin/env python3
"""Detecta reformas que están en el texto bajado y ningún módulo leyó.

    python3 herramientas/reformas_no_leidas.py
    python3 herramientas/reformas_no_leidas.py --desde 2024

La capa de fuente primaria se actualiza sola: `descargar_normas.py` vuelve a traer el texto
consolidado de InfoLEG, que YA incorpora la última reforma. Los módulos no. Entre las dos cosas
se abre una ventana en la que el repositorio tiene el artículo nuevo y la skill sigue explicando
el viejo, sin que nada avise.

Método: cada consolidado trae al pie de sus artículos una nota de reforma. **Hay dos estilos y
hay que leer los dos.** InfoLEG escribe "(Artículo sustituido por art. X de la Ley N° NN.NNN
B.O. DD/MM/AAAA)"; los textos de la Provincia escriben "(Texto según Ley 14765)", sin B.O. y sin
fecha. Un detector que exija el B.O. deja afuera un tercio de las notas del corpus, y las deja
afuera CALLADO: las normas procesales bonaerenses y la LCT son las más anotadas al estilo
provincial.

Sin fecha no hay cómo ordenar por recencia, así que se ordena por NÚMERO de ley. Dentro de una
jurisdicción los números son secuenciales, así que el mayor es el más nuevo. Es una regla del
sistema de numeración, no una estimación, y sólo se usa cuando la nota no trae fecha.

**Y hay un segundo motivo de sub-reporte, además del bloque de `cubre_el_articulo`: la pregunta
«¿nombró la reforma?» se hace sobre el MÓDULO ENTERO.** Si el módulo menciona a la ley
reformadora en cualquier parte —aunque sea por otra norma— la reforma cuenta como leída y el
artículo no se reporta. Medido el 17/09/2026 sobre la Ley 26.727 en `laboral.md`: los diez
artículos reformados enganchan con `cubre_el_articulo`, y aun sacándole a la sección la mención
de las Leyes 27.802 y 27.742 **no aparece ningún candidato**, porque ese módulo las nombra
decenas de veces por el art. 245 y por el 245 bis. En un módulo así este control **no puede
disparar**, y lo que queda cuidando esa ventana es la fecha de la fila en
`changelog-normativo.md` con su reloj de 180 días.

El script extrae esas notas, se queda con la reforma más reciente de cada norma, y pregunta si
algún módulo nombra esa ley.

Hay dos comparaciones y contestan preguntas distintas:

**Por norma** (`--modo norma`): de cada texto se mira la reforma más nueva y se pregunta si algún
módulo la nombra. Es barata y ve poco: un consolidado puede traer cuarenta notas y se mira una.

**Por artículo** (`--modo articulo`, el de por defecto): de cada nota se saca el artículo al que
está pegada, y se pregunta si algún módulo que trabaje esa norma **cubre ese artículo sin nombrar
la reforma**. Es la comparación que importa, y lo que la vuelve usable es el corte de recencia:
sin él da 621 candidatos, porque un consolidado arrastra toda su historia y el módulo no tiene
que nombrar una reforma de 2004 — tiene que decir el texto vigente.

**Los cuatro cortes, cada uno medido contra el anterior**, que son lo que vuelve usable la lista:

    Todas las notas, sin corte                                      621
    Con corte de recencia                                            57
    Con la norma y el artículo en el mismo bloque de prosa            13
    Separando cada fila de tabla, y con el piso por jurisdicción       3

El corte se hace por año cuando la nota trae B.O., y por número de ley cuando no — **por
jurisdicción**, porque la 15.000 bonaerense está alrededor de 2018 y la 15.000 nacional en los
años sesenta.

**Y la propiedad es por bloque, no por documento.** Que un módulo nombre una ley no lo vuelve
dueño de sus trescientos artículos: `transito.md` nombra la Ley 10.397 una sola vez, por el
domicilio fiscal, y figuraba cubriendo quince artículos del Código Fiscal. El artículo cuenta
sólo si el número de la norma está en el mismo bloque de prosa, y **cada fila de tabla es su
propio bloque**, porque una tabla no lleva líneas en blanco.

Reporta CANDIDATOS, no culpables. Una reforma puede tocar un artículo que el módulo no cubre, y
entonces es correcto que no la nombre. Lo que decide es abrir el módulo. Los veredictos se
anotan en `reformas-revisadas.json` para que el reporte no repita lo ya visto.

**Dos imprecisiones conocidas, que se resuelven leyendo.** Un artículo con sufijo —«48 bis»— no
entra en la numeración simple y su nota queda atribuida al artículo llano anterior. Y el método
**sub-reporta**, por ese sufijo y por las dos razones de arriba: un módulo que nombra la ley en el
encabezado de la sección y cita los artículos más abajo no engancha. **Que este control no reporte
nada no prueba que no haya reformas sin leer.**

Sale con código 1 si hay candidatos sin veredicto. Cero dependencias externas.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = RAIZ / "derecho" / "fuentes" / "normas"
SKILL = RAIZ / "derecho" / "skills" / "derecho-argentino"
REGISTRO = Path(__file__).resolve().parent / "reformas-revisadas.json"

# El paréntesis entero de una nota de reforma, en los dos estilos. Se captura el paréntesis y
# después se leen ley y fecha adentro: buscar la ley suelta emparejaba cualquier remisión del
# articulado -"conforme la Ley 11.922"- con la fecha de otra nota.
NOTA = re.compile(r"\(([^)]{0,200}?(?:[Tt]exto según|[Ss]ustituid[oa] por|[Ii]ncorporad[oa] por|"
                  r"[Dd]erogad[oa] por|[Mm]odificad[oa] por)[^)]{0,200}?)\)")
LEY = re.compile(r"Ley\s*N?[°º.]?\s*(\d{2}\.?\d{3})", re.I)
FECHA = re.compile(r"B\.?O\.? ?(\d{1,2})/(\d{1,2})/((?:19|20)\d{2})")


def texto_de_los_modulos() -> str:
    partes = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
    partes += [p.read_text(encoding="utf-8") for p in sorted((SKILL / "references").glob("*.md"))]
    return "\n".join(partes)


def reformas_del_texto(cuerpo: str) -> dict[str, date | None]:
    """Cada ley reformadora que anota el texto, con su fecha de B.O. si la nota la trae.

    La clave va sin puntos -«14765», no «14.765»- porque los dos estilos la escriben distinto y
    compararlas con puntos perdía la mitad.
    """
    leyes: dict[str, date | None] = {}
    for nota in NOTA.findall(cuerpo):
        ley = LEY.search(nota)
        if not ley:
            continue                          # el paréntesis no nombra ley: no es una reforma
        clave = ley.group(1).replace(".", "")
        cuando = None
        fecha = FECHA.search(nota)
        if fecha:
            dia, mes, anio = (int(g) for g in fecha.groups())
            try:
                cuando = date(anio, mes, dia)
            except ValueError:
                cuando = None                 # fecha imposible en la nota: no se adivina
        # Si la misma ley aparece dos veces y una trae fecha, se conserva la fechada.
        if clave not in leyes or (leyes[clave] is None and cuando is not None):
            leyes[clave] = cuando
    return leyes


def ultima_reforma_por_norma(desde: int) -> list[tuple[date | None, str, str, int]]:
    """(fecha o None, slug, ley reformadora, cuántas reformas anota el texto) para la más nueva.

    «La más nueva» se resuelve por fecha cuando la hay y por NÚMERO de ley cuando no: dentro de
    una jurisdicción los números son secuenciales. Se ordena con las dos claves a la vez porque
    un mismo texto puede traer notas de los dos estilos.
    """
    hallados = []
    for archivo in sorted(NORMAS.glob("*.txt")):
        leyes = reformas_del_texto(archivo.read_text(encoding="utf-8", errors="replace"))
        if not leyes:
            continue
        ultima = max(leyes, key=lambda l: (leyes[l] or date.min, int(l)))
        cuando = leyes[ultima]
        if desde and (cuando.year if cuando else 0) < desde:
            continue
        hallados.append((cuando, archivo.stem, ultima, len(leyes)))
    return sorted(hallados, key=lambda h: (h[0] or date.min, int(h[2])), reverse=True)


ARTICULO = re.compile(r"(?im)^\s*(?:ART[IÍ]CULO|ARTICULO|Art\.)\s*(\d+)\s*[.\-º°]")
# Corte de recencia para las notas SIN fecha, que son casi todas de PBA: 978 sobre 2.185. Se usa
# el número de ley porque dentro de una jurisdicción es secuencial, que es la misma regla con la
# que `ultima_reforma_por_norma` ordena.
#
# **Y es POR JURISDICCIÓN, porque las dos numeraciones corren en paralelo.** La 15.000 bonaerense
# está alrededor de 2018; la 15.000 nacional, en los años sesenta. Un piso único deja pasar la
# Ley 23.890, de 1990, como si fuera reciente.
PISO_SIN_FECHA = {"pba": 15000, "nacional": 27000}
PISO_POR_DEFECTO = 27000


def duenos_de_cada_norma() -> dict[str, set[str]]:
    """Qué módulos trabajan cada norma, por citar su número en algún lado.

    No hay un dueño por norma y no es un defecto de los datos: el CCyCN se cita en diez módulos
    porque diez materias lo usan. Este conjunto es sólo el primer filtro y **no alcanza solo**:
    un módulo que nombra una ley una vez, de paso, queda anotado como dueño de sus trescientos
    artículos. Quien decide de verdad es `cubre_el_articulo`.
    """
    catalogo = json.loads((NORMAS / "normas.json").read_text(encoding="utf-8"))["normas"]
    textos = {p.name: p.read_text(encoding="utf-8")
              for p in sorted((SKILL / "references").glob("*.md"))}
    fuera = {}
    for entrada in catalogo:
        hallado = re.search(r"\b(\d{4,5})\b", entrada["slug"])
        if not hallado:
            continue
        n = hallado.group(1)
        patron = re.compile(rf"\b{n[:2]}\.?{n[2:]}\b")
        fuera[entrada["slug"]] = {nombre for nombre, cuerpo in textos.items()
                                  if patron.search(cuerpo)}
    return fuera


def cubre_el_articulo(cuerpo: str, numero_norma: str, articulo: str) -> bool:
    """El `art. N` cuenta sólo si el número de la norma está en el MISMO bloque de prosa.

    Es lo que separa `art. 32 de la ley de tránsito` de `art. 32 del Código Fiscal`. Sin esto,
    `transito.md` —que nombra la Ley 10.397 una sola vez, por el domicilio fiscal— figura
    cubriendo quince artículos del Código Fiscal que no trata.

    El bloque es la unidad de prosa entre líneas en blanco, no una ventana de N caracteres:
    un umbral en caracteres se calibra hasta que da el número que uno quiere, y el bloque es una
    forma que el texto ya tiene. Probado contra la sección entera: la sección es lo bastante
    larga como para juntar la mención de una ley con artículos de otra, y devuelve los falsos.

    **Sub-reporta, y así está elegido.** Un módulo que nombra la ley en el encabezado de la
    sección y cita los artículos en los párrafos de abajo no engancha: pasa con el art. 107 de
    la Ley 24.660 en `penal.md`. Que este control no reporte nada no prueba que no haya reformas
    sin leer; prueba que no hay ninguna con la norma y el artículo en el mismo bloque.
    """
    # Una fila de tabla es su propio bloque: la tabla entera no lleva líneas en blanco, así que
    # sin esto sus filas se leen juntas y un `art. 43` de una columna queda emparejado con el
    # número de ley que aparece en otra fila. Es lo que hacía figurar a `transito.md` cubriendo
    # el art. 43 de la Ley 13.927 -una cuenta bancaria- por una fila que dice «Giros y rotondas».
    bloques = [b for parrafo in re.split(r"\n\s*\n", cuerpo)
               for b in (parrafo.split("\n") if parrafo.lstrip().startswith("|") else [parrafo])]
    patron_ley = re.compile(rf"\b{numero_norma[:2]}\.?{numero_norma[2:]}\b")
    patron_art = re.compile(rf"\barts?\.\s*{articulo}\b")
    return any(patron_art.search(b) and patron_ley.search(b) for b in bloques)


def reformas_por_articulo(desde: int) -> list[tuple[str, str, str, date | None, list[str]]]:
    """(slug, artículo, ley reformadora, fecha o None, módulos que cubren el artículo).

    Devuelve sólo los candidatos: alguien cubre el artículo y nadie nombra la reforma. Un
    artículo puede traer varias notas, así que se deduplica por (slug, artículo, ley).
    """
    duenos = duenos_de_cada_norma()
    catalogo = json.loads((NORMAS / "normas.json").read_text(encoding="utf-8"))["normas"]
    num_de_norma = {e["slug"]: re.search(r"\b(\d{4,5})\b", e["slug"]).group(1)
                    for e in catalogo if re.search(r"\b(\d{4,5})\b", e["slug"])}
    jurisdiccion = {e["slug"]: e.get("jurisdiccion", "") for e in catalogo}
    textos = {p.name: p.read_text(encoding="utf-8")
              for p in sorted((SKILL / "references").glob("*.md"))}
    vistos, salida = set(), []
    for archivo in sorted(NORMAS.glob("*.txt")):
        slug = archivo.stem
        if not duenos.get(slug):
            continue
        cuerpo = archivo.read_text(encoding="utf-8", errors="replace")
        arts = [(m.start(), m.group(1)) for m in ARTICULO.finditer(cuerpo)]
        for m in NOTA.finditer(cuerpo):
            nota = m.group(1)
            ley = LEY.search(nota)
            if not ley:
                continue
            numero = ley.group(1).replace(".", "")
            fecha, cuando = FECHA.search(nota), None
            if fecha:
                dia, mes, anio = (int(g) for g in fecha.groups())
                try:
                    cuando = date(anio, mes, dia)
                except ValueError:
                    cuando = None
            # Recencia: por año cuando la nota trae B.O., por número de ley cuando no.
            if cuando is not None:
                if desde and cuando.year < desde:
                    continue
            elif int(numero) < PISO_SIN_FECHA.get(jurisdiccion.get(slug, ""), PISO_POR_DEFECTO):
                continue
            previos = [a for pos, a in arts if pos < m.start()]
            if not previos:
                continue                      # nota antes del primer artículo: no se adivina
            # Un artículo con sufijo -«48 bis»- no entra en la numeración simple, así que su
            # nota queda atribuida al último artículo llano anterior. Es una imprecisión del
            # método y se resuelve leyendo: el candidato aparece y el veredicto dice que la
            # reforma era del bis.
            art = previos[-1]
            clave = (slug, art, numero)
            if clave in vistos:
                continue
            vistos.add(clave)
            pat_ley = re.compile(rf"\b{numero[:2]}\.?{numero[2:]}\b")
            cubren = sorted(n for n in duenos[slug]
                            if cubre_el_articulo(textos[n], num_de_norma[slug], art))
            if not cubren or any(pat_ley.search(textos[n]) for n in cubren):
                continue
            salida.append((slug, art, f"{numero[:2]}.{numero[2:]}", cuando, cubren))
    return sorted(salida, key=lambda s: (s[3] or date.min, s[0], int(s[1])), reverse=True)


def claves_vivas(desde_articulo: int) -> set:
    """Todas las claves que HOY puede producir el registro, de sus dos modos.

    Hacen falta las dos: el registro guarda `slug:ley` del modo por norma y `slug:art:ley` del
    modo por artículo, y mirar un solo modo daría por muertas las claves del otro.

    **Y cada modo tiene su propio corte de recencia**, que es lo que hace peligrosa esta función:
    el modo por norma barre desde el año CERO y el modo por artículo desde 2024. Pasarle el corte
    del artículo a los dos dio por muertos 28 de 34 veredictos —todos del modo por norma, que
    simplemente quedaban fuera de la ventana—. Se midió purgándolos de verdad y mirando el diff.
    Por eso el parámetro se llama `desde_articulo` y el otro corte está fijo acá.
    """
    vivas = set()
    for _cuando, slug, ley, _c in ultima_reforma_por_norma(0):
        con_punto = f"{ley[:2]}.{ley[2:]}"
        vivas |= {f"{slug}:{con_punto}", f"{slug}:{ley}"}
    for slug, art, ley, _cuando, _mods in reformas_por_articulo(desde_articulo):
        vivas.add(f"{slug}:{art}:{ley}")
    return vivas


def por_articulo(desde: int) -> int:
    """La comparación que importa, con su veredicto en el mismo registro y otra clave.

    La clave es `slug:art:ley` y no `slug:ley`, así que un veredicto por norma no tapa a uno por
    artículo ni al revés: son dos afirmaciones distintas sobre la misma reforma.
    """
    _, revisadas = _veredictos.cargar(REGISTRO, "reformas", vacio={})
    candidatos = reformas_por_articulo(desde)
    sin_veredicto = [c for c in candidatos if f"{c[0]}:{c[1]}:{c[2]}" not in revisadas]

    print("\n  De cada nota de reforma se toma el ARTÍCULO al que está pegada, y se pregunta si")
    print("  algún módulo que trabaje esa norma cubre ese artículo sin nombrar la reforma. El")
    print(f"  corte de recencia es {desde} para las notas con B.O.; para las que no traen fecha,")
    print("  que no traen fecha, que son casi todas de PBA.")
    print(f"  Candidatos: {len(candidatos)}. Con veredicto escrito: {len(candidatos) - len(sin_veredicto)}.")

    for renglon in _veredictos.aviso_de_muertos(
            len(_veredictos.muertos(revisadas, claves_vivas(desde))), len(revisadas),
            "python3 herramientas/reformas_no_leidas.py --purgar"):
        print(renglon)

    if not sin_veredicto:
        print("\n  Sin pendientes: no hay artículo cubierto con una reforma reciente sin leer.\n")
        return 0

    print(f"\n  SIN DECIDIR ({len(sin_veredicto)}) — abrir el módulo en ese artículo:\n")
    for slug, art, ley, cuando, mods in sin_veredicto:
        fecha = cuando.strftime("%d/%m/%Y") if cuando else "sin fecha "
        print(f"  {fecha}  {slug:<22} art. {art:<6} Ley {ley:<8} -> {', '.join(mods)}")
    print("\n  Un veredicto se anota en reformas-revisadas.json con la clave 'slug:art:ley'.")
    print("  Reporta candidatos: el módulo puede citar ese número de artículo por otra norma,")
    print("  o explicar ya la regla nueva sin nombrar la ley que la introdujo.\n")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    # Sin default propio: cada modo tiene el suyo, porque miden cosas distintas. Por norma se
    # mira UNA reforma por texto y un corte de año deja fuera normas enteras; por artículo se
    # miran todas y sin corte el reporte se vuelve la alarma que suena siempre.
    ap.add_argument("--desde", type=int, default=None,
                    help="ignorar reformas anteriores a ese año. "
                         "Por defecto 2024 con --modo articulo, sin corte con --modo norma. "
                         "Las notas sin fecha se cortan por número de ley y no por este año")
    ap.add_argument("--purgar", action="store_true",
                    help="Saca del registro los veredictos que ya no enganchan ninguna reforma")
    ap.add_argument("--modo", choices=["articulo", "norma"], default="articulo",
                    help="Con --modo articulo, la nota se compara contra el artículo que "
                         "cubre el módulo; con --modo norma, sólo la reforma más nueva")
    args = ap.parse_args()

    if args.purgar:
        desde = 2024 if args.desde is None else args.desde
        sobre, revisadas = _veredictos.cargar(REGISTRO, "reformas", vacio={})
        sin_uso = _veredictos.muertos(revisadas, claves_vivas(desde))
        if not sin_uso:
            print("\n  no hay veredictos muertos que purgar")
            return 0
        _veredictos.guardar(REGISTRO, sobre, "reformas",
                            {k: v for k, v in revisadas.items() if k not in set(sin_uso)})
        print(f"\n  purgados {len(sin_uso)} veredictos muertos de {REGISTRO.name}")
        return 0

    if args.modo == "articulo":
        return por_articulo(2024 if args.desde is None else args.desde)
    args.desde = args.desde or 0

    modulos = texto_de_los_modulos()
    _, revisadas = _veredictos.cargar(REGISTRO, "reformas", vacio={})

    sin_veredicto, conocidas, decididas, total_notas = [], 0, 0, 0
    for cuando, slug, ley, cuantas in ultima_reforma_por_norma(args.desde):
        total_notas += cuantas
        # La ley se escribe con punto en los módulos y sin punto en varias notas.
        con_punto = f"{ley[:2]}.{ley[2:]}"
        if con_punto in modulos or ley in modulos:
            conocidas += 1
            continue
        clave = f"{slug}:{con_punto}"
        if clave in revisadas or f"{slug}:{ley}" in revisadas:
            decididas += 1
            continue
        sin_veredicto.append((cuando, slug, con_punto, cuantas))

    print("\n  Normas con notas de reforma: la última de cada una se compara contra los módulos,")
    print("  y las notas de los dos estilos cuentan —con B.O. y sin él—. Reformas anotadas en")
    print(f"  los textos: {total_notas}; de cada norma se mira UNA, la más nueva.")
    print(f"  Reformas que los módulos nombran: {conocidas}. Con veredicto escrito: {decididas}.")

    if not sin_veredicto:
        print("\n  Sin pendientes: no hay reforma reciente que los módulos no nombren.\n")
        return 0

    print(f"\n  SIN DECIDIR ({len(sin_veredicto)}) — abrir el módulo y ver si la reforma lo toca:\n")
    for cuando, slug, ley, cuantas in sin_veredicto:
        fecha = cuando.strftime("%d/%m/%Y") if cuando else "sin fecha "
        resto = f"(de {cuantas} reformas del texto)" if cuantas > 1 else ""
        print(f"  {fecha}  {slug:<24} Ley {ley:<8} {resto}")
    print("\n  Un veredicto se anota en reformas-revisadas.json con su motivo, con la clave")
    print("  'slug:ley'. Reporta candidatos: una reforma puede tocar un artículo que el módulo")
    print("  no cubre, y entonces es correcto que no la nombre.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
