#!/usr/bin/env python3
"""Compara lo que los módulos CITAN contra lo que normas.json DECLARA.

Contra lo DECLARADO y no contra lo bajado, y la diferencia importa: una norma
declarada sin texto -- las dos que no tienen URL oficial -- cuenta como cubierta
acá. Que le falte el texto lo dicen `fuentes/MANIFIESTO.md` y `estado.py`, que
es donde vive esa cuenta. Acá la pregunta es otra: qué norma se usa con
articulado y ni siquiera está en el catálogo.

POR QUÉ EXISTE

La disciplina del proyecto dice que no se afirma una norma sin fuente primaria
a la vista. Los descargadores cumplen su parte -hashean, reintentan, verifican
identidad y encoding- pero ninguno responde la pregunta previa: QUE debería
estar en el manifiesto. Eso se venía decidiendo a ojo, y así quedaron afuera
normas que los módulos usan con articulado.

El caso que lo destapó: la Ley 25.323. laboral.md describe su duplicación, su
recargo del 50% y su exigencia de intimación previa, y concursos.md rutea a
sus arts. 1 y 2 para el pronto pago. No estaba declarada en normas.json. Se
estaba afirmando su contenido de memoria.

QUÉ MIDE Y QUÉ NO

Busca citas de ley en los módulos y las cruza contra normas.json. Separa dos
usos, porque no piden lo mismo:

  CON ARTICULADO   "art. 2 de la Ley 25.323". Se está usando la norma como
                   fuente de una regla: hace falta el texto.

  SOLO NOMBRADA    "texto según Ley 27.785", "derogada por la Ley 27.742".
                   Es una modificatoria, y el consolidado de la ley base ya
                   la incorpora. NO hace falta bajarla aparte.

La distinción es imperfecta: se mira una ventana de texto alrededor de la cita
y puede equivocarse en los dos sentidos. Por eso la salida es una LISTA PARA
REVISAR, no una orden de descarga. Antes de agregar algo a normas.json hay que
abrir el módulo y ver como se usa.

Los códigos -CCyCN, CP, CPCCN, CPCCBA, LCT, LDC- no se detectan acá porque no
se citan por número de ley. Están todos bajados; si eso cambia, lo dice
estado.py.

Uso:
  python3 herramientas/cobertura_normativa.py             faltantes con articulado
  python3 herramientas/cobertura_normativa.py --todo      también las solo nombradas
"""
import argparse
import json
import pathlib
import re
import sys
from collections import Counter

RAIZ = pathlib.Path(__file__).resolve().parent.parent
NORMAS = RAIZ / "derecho" / "fuentes" / "normas" / "normas.json"
REFS = RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"

CITA = re.compile(r"[Ll]ey(?:es)?\s+(?:N[°º]\s*)?(\d{2}\.?\d{3})")
# Y los instrumentos que no son leyes. Un decreto reglamentario o un acuerdo de la SCBA se cita
# como fuente de una regla igual que una ley, así que pesan igual acá. El número lleva el año
# porque es lo que los distingue -hay un 274 de cada año-, y se normaliza a cuatro dígitos para
# que `274/24` y `274/2024` sean el mismo.
CITA_OTROS = re.compile(r"\b(?:Decretos?|Dec\.|DNU|Resoluci[óo]n|Res\.|Acuerdos?|Ac\.)\s*"
                        r"(?:N[°º]\s*)?(\d{1,5})\s*[/-]\s*(\d{2,4})")
ARTICULO = re.compile(r"\barts?\.\s*\d+|\bartículos?\s+\d+|\binc\.")
VENTANA = 110

# Una ley se nombra por dos motivos distintos y solo uno pide bajar su texto.
#
#   "art. 163, texto Ley 15.232"  -> la 15.232 REFORMÓ al CPP PBA. El articulado
#                                    es del código, que ya está bajado. No hace falta.
#   "art. 22 Ley 23.661"          -> la 23.661 es la FUENTE de la regla. Hace falta.
#
# Sin esta distinción la lista da 88 y es inservible; con ella da 32 y se puede
# trabajar. La frase real del repo es "texto Ley N", sin "según" en el medio:
# exigirlo dejaba pasar las reformas más comunes.
REFORMA = re.compile(
    r"text[oa]\s+(seg[úu]n\s+|ordenado\s+|conforme\s+)?(la\s+)?[Ll]ey|"
    r"seg[úu]n\s+(la\s+)?[Ll]ey|reformad|sustitu|modificad|modificó|modifica\b|"
    r"incorporad|incorporó|derogad|derogó|agregad|reescrib|"
    r"por\s+(el\s+)?arts?\.?\s*\d+\s+de\s+la\s+[Ll]ey", re.I)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _veredictos

DECISIONES = pathlib.Path(__file__).resolve().parent / "cobertura-revisada.json"


def declaradas() -> set[str]:
    """Números de ley que el manifiesto declara, leídos del SLUG.

    El slug es el identificador; el título es prosa, y la prosa de un título nombra OTRAS
    leyes: "Reglamentación de la Ley 25.326", "abrogado por la Ley 27.063", "Prórroga la
    emergencia de la Ley 14.407". Sacando números del título, cada una de esas quedaba
    declarada por aparecer mencionada en la entrada de otra, y este control dejaba de
    reclamarlas. La Ley 24.430 era el caso vivo: no tiene entrada propia y figuraba como
    declarada porque `cn-1994` la nombra en su título.

    Es la regla general del repositorio: un dato de máquina no se infiere de la prosa.
    """
    m = json.loads(NORMAS.read_text(encoding="utf-8"))["normas"]
    n = set()
    for entrada in m:
        slug = entrada.get("slug", "")
        for x in re.findall(r"\b(\d{2}\.?\d{3})\b", slug):
            n.add(x.replace(".", ""))
        # Un decreto o acuerdo se declara `pba-decreto-532-2009`, `decreto-84-2026`: número y
        # año pegados con guion. Se guarda con el año a cuatro dígitos, igual que la cita.
        for num, anio in re.findall(r"(\d{1,5})-(\d{4})\b", slug):
            n.add(f"{num}/{anio}")
    return n


def anio_largo(anio: str) -> str:
    """`24` -> `2024`, `96` -> `1996`. El corte en 50 cubre lo que el repositorio cita."""
    if len(anio) == 4:
        return anio
    v = int(anio)
    return f"{'20' if v < 50 else '19'}{anio.zfill(2)}"


def etiqueta(numero: str) -> str:
    """`27423` -> `Ley 27.423`; `1350/2018` -> `Decreto o acuerdo 1350/2018`.

    El `/` es lo que distingue una clase de la otra, porque un número de ley no lo lleva.
    Tratar un decreto como ley imprime «Ley 13.50/2018» por el Decreto 1350/2018: el rótulo y el
    punto de millar puestos donde no van, que es peor que no mostrar nada porque se lee como una
    ley que no existe.

    Vive a nivel de módulo porque la salida arma el nombre en TRES lugares, y un arreglo que
    toque uno solo deja a los otros dos imprimiendo mal sin que se note.
    """
    if "/" in numero:
        return f"Decreto o acuerdo {numero}"
    return f"Ley {numero[:2]}.{numero[2:]}"


def clase_de_cita(ventana: str) -> str:
    """Para qué se nombra la ley: `regla`, `reforma` o `solo_nombre`.

    Es la decisión que hace que la lista sirva o que nadie la mire. Sin separar la reforma de
    la fuente de la regla, la lista da tres veces más entradas y todas las que importan quedan
    tapadas: la alarma que suena siempre.

    Se mira una ventana de texto alrededor de la cita, así que se equivoca en los dos sentidos.
    Va aparte de `main()` para poder fijar por test qué ventana clasifica cómo.
    """
    if not ARTICULO.search(ventana):
        return "solo_nombre"
    return "reforma" if REFORMA.search(ventana) else "regla"


def decisiones() -> dict:
    """Veredicto ya tomado para cada ley, con el motivo. Vacío si no hay archivo."""
    try:
        return _veredictos.cargar(DECISIONES, "leyes", vacio={})[1]
    except (OSError, ValueError, KeyError):
        return {}


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--todo", action="store_true",
                   help="agregar las leyes solo nombradas, sin articulado alrededor")
    p.add_argument("--purgar", action="store_true",
                   help="Saca de cobertura-revisada.json los veredictos que ya no enganchan "
                        "ninguna cita")
    a = p.parse_args(argv[1:])
    todo = a.todo
    tengo = declaradas()
    ya = decisiones()

    regla: Counter = Counter()
    reforma: Counter = Counter()
    solo_nombre: Counter = Counter()
    donde: dict[str, set[str]] = {}

    for archivo in sorted(REFS.glob("*.md")):
        texto = archivo.read_text(encoding="utf-8")
        for m in list(CITA.finditer(texto)) + list(CITA_OTROS.finditer(texto)):
            if m.re is CITA:
                numero = m.group(1).replace(".", "")
            else:
                numero = f"{m.group(1)}/{anio_largo(m.group(2))}"
            if numero in tengo:
                continue
            ventana = texto[max(0, m.start() - VENTANA):m.end() + VENTANA]
            clase = clase_de_cita(ventana)
            if clase == "solo_nombre":
                solo_nombre[numero] += 1
            elif clase == "reforma":
                reforma[numero] += 1
            else:
                regla[numero] += 1
                donde.setdefault(numero, set()).add(archivo.name)

    def linea(numero: str, veces: int) -> str:
        mods = ", ".join(sorted(donde.get(numero, ())))
        return f"  {etiqueta(numero)}  ({veces}x)  {mods}"

    pendientes = [(n, v) for n, v in regla.most_common() if n not in ya]
    decididas = [n for n in regla if n in ya]

    print(f"\n  Manifiesto: {len(tengo)} leyes declaradas.")
    print(f"  Citadas y no declaradas: {len(regla)} como fuente de una regla, "
          f"{len(reforma)} como reforma de una ley que ya está bajada.\n")

    if pendientes:
        print(f"  SIN DECIDIR ({len(pendientes)}) — abrir el módulo y ver cómo se usa:\n")
        for numero, veces in pendientes:
            print(linea(numero, veces))
    else:
        print("  Sin pendientes: todas las citadas tienen veredicto en "
              f"{DECISIONES.name}.")

    if decididas:
        bajar = [n for n in decididas if ya[n].get("veredicto") == "bajar"]
        print(f"\n  Ya decididas: {len(decididas)}"
              + (f", de las cuales {len(bajar)} esperan descarga" if bajar else ""))
        for numero in sorted(bajar):
            print(f"    {etiqueta(numero)} — {ya[numero].get('motivo','')}")

    if todo:
        print(f"\n  SOLO NOMBRADAS ({len(solo_nombre)}), sin articulado alrededor:\n")
        for numero, veces in solo_nombre.most_common():
            print(f"  {etiqueta(numero)}  ({veces}x)")

    # Una cita citada hoy es lo VIVO; todo veredicto que no corresponda a una está muerto.
    # Esta herramienta barre SIEMPRE todos los módulos, así que puede medirlo sin falsos.
    vivas = set(regla) | set(reforma) | set(solo_nombre)
    sin_uso = _veredictos.muertos(ya, vivas)
    if a.purgar:
        if not sin_uso:
            print("\n  no hay veredictos muertos que purgar")
            return 0
        sobre, _ = _veredictos.cargar(DECISIONES, "leyes", vacio={})
        _veredictos.guardar(DECISIONES, sobre, "leyes",
                            {k: v for k, v in ya.items() if k not in set(sin_uso)})
        print(f"\n  purgados {len(sin_uso)} veredictos muertos de {DECISIONES.name}")
        return 0
    for renglon in _veredictos.aviso_de_muertos(
            len(sin_uso), len(ya), "python3 herramientas/cobertura_normativa.py --purgar"):
        print(renglon)

    print("\n  Un veredicto se anota en cobertura-revisada.json con su motivo. La")
    print("  detección de reformas mira una ventana de texto y se equivoca en los dos")
    print("  sentidos: lo que decide es abrir el módulo, no el conteo.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
