#!/usr/bin/env python3
"""Compara lo que los modulos CITAN contra lo que fuentes/ tiene BAJADO.

POR QUE EXISTE

La disciplina del proyecto dice que no se afirma una norma sin fuente primaria
a la vista. Los descargadores cumplen su parte -hashean, reintentan, verifican
identidad y encoding- pero ninguno responde la pregunta previa: QUE deberia
estar en el manifiesto. Eso se venia decidiendo a ojo, y asi quedaron afuera
normas que los modulos usan con articulado.

El caso que lo destapo: la Ley 25.323. laboral.md describe su duplicacion, su
recargo del 50% y su exigencia de intimacion previa, y concursos.md rutea a
sus arts. 1 y 2 para el pronto pago. No estaba declarada en normas.json. Se
estaba afirmando su contenido de memoria.

QUE MIDE Y QUE NO

Busca citas de ley en los modulos y las cruza contra normas.json. Separa dos
usos, porque no piden lo mismo:

  CON ARTICULADO   "art. 2 de la Ley 25.323". Se esta usando la norma como
                   fuente de una regla: hace falta el texto.

  SOLO NOMBRADA    "texto segun Ley 27.785", "derogada por la Ley 27.742".
                   Es una modificatoria, y el consolidado de la ley base ya
                   la incorpora. NO hace falta bajarla aparte.

La distincion es imperfecta: se mira una ventana de texto alrededor de la cita
y puede equivocarse en los dos sentidos. Por eso la salida es una LISTA PARA
REVISAR, no una orden de descarga. Antes de agregar algo a normas.json hay que
abrir el modulo y ver como se usa.

Los codigos -CCyCN, CP, CPCCN, CPCCBA, LCT, LDC- no se detectan acá porque no
se citan por numero de ley. Estan todos bajados; si eso cambia, lo dice
estado.py.

Uso:
  python3 herramientas/cobertura_normativa.py             faltantes con articulado
  python3 herramientas/cobertura_normativa.py --todo      tambien las solo nombradas
"""
import json
import pathlib
import re
import sys
from collections import Counter

RAIZ = pathlib.Path(__file__).resolve().parent.parent
NORMAS = RAIZ / "argentina" / "fuentes" / "normas" / "normas.json"
REFS = RAIZ / "argentina" / "skills" / "derecho-argentino" / "references"

CITA = re.compile(r"[Ll]ey(?:es)?\s+(?:N[°º]\s*)?(\d{2}\.?\d{3})")
ARTICULO = re.compile(r"\barts?\.\s*\d+|\bartículos?\s+\d+|\binc\.")
VENTANA = 110

# Una ley se nombra por dos motivos distintos y solo uno pide bajar su texto.
#
#   "art. 163, texto Ley 15.232"  -> la 15.232 REFORMO al CPP PBA. El articulado
#                                    es del codigo, que ya esta bajado. No hace falta.
#   "art. 22 Ley 23.661"          -> la 23.661 es la FUENTE de la regla. Hace falta.
#
# Sin esta distincion la lista da 88 y es inservible; con ella da 32 y se puede
# trabajar. La frase real del repo es "texto Ley N", sin "segun" en el medio:
# exigirlo dejaba pasar las reformas mas comunes.
REFORMA = re.compile(
    r"text[oa]\s+(seg[úu]n\s+|ordenado\s+|conforme\s+)?(la\s+)?[Ll]ey|"
    r"seg[úu]n\s+(la\s+)?[Ll]ey|reformad|sustitu|modificad|modificó|modifica\b|"
    r"incorporad|incorporó|derogad|derogó|agregad|reescrib|"
    r"por\s+(el\s+)?arts?\.?\s*\d+\s+de\s+la\s+[Ll]ey", re.I)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _veredictos

DECISIONES = pathlib.Path(__file__).resolve().parent / "cobertura-revisada.json"


def declaradas() -> set[str]:
    """Numeros de ley que el manifiesto ya conoce."""
    m = json.loads(NORMAS.read_text(encoding="utf-8"))["normas"]
    n = set()
    for entrada in m:
        campo = f"{entrada.get('titulo','')} {entrada.get('slug','')}"
        for x in re.findall(r"\b(\d{2}\.?\d{3})\b", campo):
            n.add(x.replace(".", ""))
    return n


def decisiones() -> dict:
    """Veredicto ya tomado para cada ley, con el motivo. Vacio si no hay archivo."""
    try:
        return _veredictos.cargar(DECISIONES, "leyes", vacio={})[1]
    except (OSError, ValueError, KeyError):
        return {}


def main(argv: list[str]) -> int:
    todo = "--todo" in argv
    tengo = declaradas()
    ya = decisiones()

    regla: Counter = Counter()
    reforma: Counter = Counter()
    solo_nombre: Counter = Counter()
    donde: dict[str, set[str]] = {}

    for archivo in sorted(REFS.glob("*.md")):
        texto = archivo.read_text(encoding="utf-8")
        for m in CITA.finditer(texto):
            numero = m.group(1).replace(".", "")
            if numero in tengo:
                continue
            ventana = texto[max(0, m.start() - VENTANA):m.end() + VENTANA]
            if not ARTICULO.search(ventana):
                solo_nombre[numero] += 1
                continue
            if REFORMA.search(ventana):
                reforma[numero] += 1
            else:
                regla[numero] += 1
                donde.setdefault(numero, set()).add(archivo.name)

    def linea(numero: str, veces: int) -> str:
        mods = ", ".join(sorted(donde.get(numero, ())))
        return f"  Ley {numero[:2]}.{numero[2:]}  ({veces}x)  {mods}"

    pendientes = [(n, v) for n, v in regla.most_common() if n not in ya]
    decididas = [n for n in regla if n in ya]

    print(f"\n  Manifiesto: {len(tengo)} leyes declaradas.")
    print(f"  Citadas y no declaradas: {len(regla)} como fuente de una regla, "
          f"{len(reforma)} como reforma de una ley que ya esta bajada.\n")

    if pendientes:
        print(f"  SIN DECIDIR ({len(pendientes)}) — abrir el modulo y ver como se usa:\n")
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
            print(f"    Ley {numero[:2]}.{numero[2:]} — {ya[numero].get('motivo','')}")

    if todo:
        print(f"\n  SOLO NOMBRADAS ({len(solo_nombre)}), sin articulado alrededor:\n")
        for numero, veces in solo_nombre.most_common():
            print(f"  Ley {numero[:2]}.{numero[2:]}  ({veces}x)")

    print("\n  Un veredicto se anota en cobertura-revisada.json con su motivo. La")
    print("  deteccion de reformas mira una ventana de texto y se equivoca en los dos")
    print("  sentidos: lo que decide es abrir el modulo, no el conteo.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
