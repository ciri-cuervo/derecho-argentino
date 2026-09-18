#!/usr/bin/env python3
"""Valor de la UMA y conversión pesos <-> UMA - justicia nacional y federal (Ley 27.423).

El art. 51 exige que una regulación diga las DOS cosas, bajo pena de nulidad: el monto en
moneda de curso legal y la cantidad de UMA que representa a la fecha de la resolución. Y el
pago cancela por la UMA, al valor vigente AL MOMENTO DEL PAGO, no al de la regulación. Son dos
fechas distintas y las dos hacen falta, así que este script pide la fecha y no la supone.

El valor NO se toma de memoria: sale de `derecho/fuentes/datos/uma-csjn.csv`, que se carga a
mano desde la consulta oficial de la CSJN. Si la serie está vacía el script SE PLANTA: no hay
número por ausencia de dato.

Uso:
    python3 uma_csjn.py --fecha 2026-09-01
    python3 uma_csjn.py --fecha 2026-09-01 --pesos 4500000
    python3 uma_csjn.py --fecha 2026-09-01 --uma 47.5

Este script NO regula: no trae la escala del art. 21 ni las etapas del art. 29. Para eso está
`references/honorarios-nacional.md` 37, y la escala se aplica leyéndola. Lo que hace acá es la
única cuenta que el art. 51 vuelve obligatoria y que sin la serie no se puede hacer.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from _raiz import datos

CENT = Decimal("0.01")
MILESIMA = Decimal("0.001")
ARCHIVO = "uma-csjn.csv"


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
                      f"https://www.csjn.gov.ar/transparencia/uma - sin eso no hay número")
    filas.sort(key=lambda f: f["vigencia_desde"])
    return filas, ""


def uma_a_fecha(fecha: date, repo=None):
    """El valor vigente a esa fecha: la última vigencia que NO es posterior.

    Devuelve `(valor, fila, "")` o `(None, None, motivo)`. Una fecha anterior a la primera
    vigencia cargada no se extrapola hacia atrás: se dice que falta, porque suponer que el
    valor más viejo regía antes es inventar un número.
    """
    filas, motivo = _filas(repo)
    if filas is None:
        return None, None, motivo
    previas = [f for f in filas if f["vigencia_desde"] <= fecha.isoformat()]
    if not previas:
        return None, None, (f"la serie arranca el {filas[0]['vigencia_desde']} y se pidió "
                            f"{fecha.isoformat()}: no se extrapola hacia atrás")
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
                   help="Fecha a la que se busca el valor, AAAA-MM-DD. La de la resolución "
                        "para expresar la regulación; la del pago para cancelar (art. 51)")
    p.add_argument("--pesos", type=Decimal, default=None,
                   help="Importe en pesos a expresar en UMA")
    p.add_argument("--uma", type=Decimal, default=None,
                   help="Cantidad de UMA a expresar en pesos")
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
    print(f"UMA vigente al {fecha.isoformat()}: ${valor}")
    print(f"  fijada desde {fila['vigencia_desde']}"
          + (f", {resolucion}" if resolucion else ""))
    if a.pesos is not None:
        print(f"  ${a.pesos} = {(a.pesos / valor).quantize(MILESIMA, ROUND_HALF_UP)} UMA")
    if a.uma is not None:
        print(f"  {a.uma} UMA = ${(a.uma * valor).quantize(CENT, ROUND_HALF_UP)}")
    if a.pesos is not None or a.uma is not None:
        print("  El art. 51 pide las DOS expresiones en la resolución, y el pago cancela al "
              "valor de la UMA vigente al momento del pago.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
