#!/usr/bin/env python3
"""Valor de la UMA de la CIUDAD y conversión pesos <-> UMA (Ley 5.134, art. 20).

**No es el mismo script que `uma_csjn.py` porque no es la misma unidad**, y ése es el punto: la
UMA porteña es el 1,5% de la remuneración TOTAL de un juez de primera instancia de la Ciudad y
la fija el Consejo de la Magistratura de CABA; la nacional es el 3% de la BÁSICA de un juez
federal y la fija la CSJN. Buscar una en la fuente de la otra devuelve un número oficial,
vigente y de otra ley. Que cada jurisdicción tenga su script es lo que impide agarrar la
equivocada sin darse cuenta.

**Y la cuenta se hace por otro motivo.** El art. 51 de la Ley 27.423 obliga a expresar la
regulación nacional en pesos Y en UMA bajo pena de nulidad; **la Ley 5.134 no tiene esa regla**
—medido contra `fuentes/normas/caba-ley-5134.txt`: sus dos «bajo pena de nulidad» son el art. 16,
fundar la regulación citando la norma, y la integración de intereses a la base—. Acá la
conversión hace falta para otra cosa: **los mínimos están escritos en UMA** —art. 21 por tipo de
juicio, art. 60 para los no previstos— y sin el valor no se sabe si una regulación los respeta.

El valor NO se toma de memoria: sale de `derecho/fuentes/datos/uma-caba.csv`. Si la serie está
vacía, o la fecha es anterior a la primera vigencia cargada, el script SE PLANTA.

Uso:
    python3 uma_caba.py --fecha 2026-09-01
    python3 uma_caba.py --fecha 2026-09-01 --pesos 4500000
    python3 uma_caba.py --fecha 2026-09-01 --uma 10

Este script NO regula: no trae la escala del art. 23 ni el tope global del 50%. Para eso está
`references/honorarios-caba.md` 42, y la escala se aplica leyéndola.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from _raiz import datos

CENT = Decimal("0.01")
MILESIMA = Decimal("0.001")
ARCHIVO = "uma-caba.csv"
CONSULTA = "https://consejo.jusbaires.gob.ar/servicios/uma/"


def _filas(repo=None):
    """Las filas con valor, ordenadas por vigencia. Vacío si la serie no se cargó."""
    d = datos(repo)
    if d is None:
        return None, "no hay repo configurado: correr configurar.py"
    cand = d / ARCHIVO
    if not cand.is_file():
        return None, f"no existe {cand}"
    lineas = [l for l in cand.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.lstrip().startswith("#")]
    filas = [f for f in csv.DictReader(lineas) if (f.get("uma") or "").strip()]
    if not filas:
        return None, (f"{cand} no tiene ningún valor cargado. La serie se carga a mano desde "
                      f"{CONSULTA} - sin eso no hay número")
    filas.sort(key=lambda f: f["vigencia_desde"])
    return filas, ""


def uma_a_fecha(fecha: date, repo=None):
    """El valor vigente a esa fecha: la última vigencia que NO es posterior.

    **Acá plantarse es el caso frecuente y no el raro.** La consulta oficial publica un solo
    valor, el vigente, así que la serie histórica no se reconstruye desde el organismo que la
    fija: una regulación de hace un año no se puede expresar en pesos con lo que hay. Suponer
    que el valor más viejo cargado regía antes sería inventar un número sobre un mínimo legal.
    """
    filas, motivo = _filas(repo)
    if filas is None:
        return None, None, motivo
    previas = [f for f in filas if f["vigencia_desde"] <= fecha.isoformat()]
    if not previas:
        return None, None, (f"la serie arranca el {filas[0]['vigencia_desde']} y se pidió "
                            f"{fecha.isoformat()}: no se extrapola hacia atrás. La consulta "
                            f"oficial publica sólo el valor vigente, así que el anterior se "
                            f"pide o se marca")
    u = previas[-1]
    return Decimal(u["uma"]), u, ""


def uma_del_repo(repo=None):
    """El último valor cargado, sin preguntar fecha. Para diagnóstico, no para regular."""
    filas, motivo = _filas(repo)
    if filas is None:
        return None, None, motivo
    u = filas[-1]
    return Decimal(u["uma"]), u["vigencia_desde"], u.get("fuente") or ""


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fecha", required=True,
                   help="Fecha a la que se busca el valor, AAAA-MM-DD")
    p.add_argument("--pesos", type=Decimal, default=None,
                   help="Importe en pesos a expresar en UMA")
    p.add_argument("--uma", type=Decimal, default=None,
                   help="Cantidad de UMA a expresar en pesos - por ejemplo un mínimo del art. 21")
    p.add_argument("--repo", default=None)
    a = p.parse_args()

    if a.pesos is not None and a.uma is not None:
        p.error("--pesos y --uma son las dos direcciones de la misma cuenta: una por vez")
    try:
        fecha = date.fromisoformat(a.fecha)
    except ValueError:
        p.error(f"--fecha no es una fecha AAAA-MM-DD: {a.fecha!r}")

    valor, fila, motivo = uma_a_fecha(fecha, a.repo)
    if valor is None:
        print(f"[CONFIGURACIÓN INCOMPLETA: {motivo}]")
        return 2

    resolucion = (fila.get("resolucion") or "").strip()
    print(f"UMA de la Ciudad vigente al {fecha.isoformat()}: ${valor}")
    print(f"  fijada desde {fila['vigencia_desde']}"
          + (f", {resolucion}" if resolucion else ""))
    if a.pesos is not None:
        print(f"  ${a.pesos} = {(a.pesos / valor).quantize(MILESIMA, ROUND_HALF_UP)} UMA")
    if a.uma is not None:
        print(f"  {a.uma} UMA = ${(a.uma * valor).quantize(CENT, ROUND_HALF_UP)}")
    if a.pesos is not None or a.uma is not None:
        print("  Es la UMA de la Ley 5.134, no la de la Ley 27.423. La Ley 5.134 NO exige "
              "expresar la regulación en las dos unidades: la conversión sirve para "
              "contrastar los mínimos de los arts. 21 y 60.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
