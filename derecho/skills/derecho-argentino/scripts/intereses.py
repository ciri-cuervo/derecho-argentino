#!/usr/bin/env python3
"""Actualización e intereses sobre un crédito - derecho argentino.

Calculadora determinista para la skill `derecho-argentino`. NO trae series: los índices se
leen de `derecho/fuentes/datos/serie-<nombre>.csv` y las tasas se pasan como entrada. Si la
serie no está cargada, el script no estima: emite el marcador y corta.

Dos modos, que corresponden a dos regímenes distintos. Elegir el modo NO es una decisión
técnica: depende de que norma o doctrina rige el crédito. Ver `references/laboral.md` 5.5
(fuero nacional) y 5.5 bis (PBA), y `references/sede-judicial-pba.md` 1.6.8.

    # Actualización por índice + interés puro (esquema tipo "Barrios", o art. 276 LCT)
    python3 intereses.py --modo índice --capital 22768351.81 \
        --desde 2024-05-10 --hasta 2026-08-31 --serie ipc --interes-puro 6

    # Tasa nominal anual sobre capital nominal
    python3 intereses.py --modo tasa --capital 22768351.81 \
        --desde 2024-05-10 --hasta 2026-08-31 --tna 21
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from _raiz import datos

CENT = Decimal("0.01")


def q(x) -> Decimal:
    return Decimal(str(x)).quantize(CENT, rounding=ROUND_HALF_UP)


def cargar_serie(nombre: str, repo=None):
    d = datos(repo)
    if d is None:
        return {}, None
    cand = d / f"serie-{nombre}.csv"
    if not cand.is_file():
        return {}, None
    lineas = [l for l in cand.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.lstrip().startswith("#")]
    filas = [f for f in csv.DictReader(lineas) if f.get("indice")]
    raiz = cand.parents[3]
    return ({f["periodo"]: Decimal(f["indice"]) for f in filas},
            str(cand.relative_to(raiz)))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modo", required=True, choices=["indice", "tasa"])
    p.add_argument("--capital", required=True, type=Decimal)
    p.add_argument("--desde", required=True, type=date.fromisoformat)
    p.add_argument("--hasta", required=True, type=date.fromisoformat)
    p.add_argument("--serie", default="ipc", help="Nombre de la serie: ipc, ripte, cer")
    p.add_argument("--interes-puro", type=Decimal, default=Decimal("6"),
                   help="Interés puro anual. 'Barrios' fija un TECHO del 6%%, no una tasa fija")
    p.add_argument("--tna", type=Decimal, default=None, help="Tasa nominal anual, modo tasa")
    p.add_argument("--repo", default=None,
                   help="Raiz del repo. Si se omite se resuelve sola (ver configurar.py)")
    a = p.parse_args()

    if a.hasta < a.desde:
        raise SystemExit("La fecha final es anterior a la inicial.")
    dias = (a.hasta - a.desde).days
    marcadores = []

    print("ACTUALIZACIÓN E INTERESES\n")
    print(f"  Capital           {float(q(a.capital)):>18,.2f}")
    print(f"  Periodo           {a.desde.isoformat()} a {a.hasta.isoformat()}  ({dias} dias)")

    if a.modo == "indice":
        serie, ruta = cargar_serie(a.serie, a.repo)
        p0, p1 = a.desde.strftime("%Y-%m"), a.hasta.strftime("%Y-%m")
        if not serie:
            print(f"\n  La serie '{a.serie}' no está cargada. No se estima.\n")
            if datos(a.repo) is None:
                print("    No hay repo configurado en esta máquina: correr configurar.py")
            print(f"    [VERIFICAR MONTO ACTUALIZADO: serie {a.serie.upper()} para el período "
                  f"{p0} a {p1} - cargar derecho/fuentes/datos/serie-{a.serie}.csv desde la "
                  f"fuente oficial antes de liquidar]")
            raise SystemExit(2)
        faltan = [x for x in (p0, p1) if x not in serie]
        if faltan:
            print(f"\n  La serie '{a.serie}' no cubre {', '.join(faltan)}. No se estima.\n")
            print(f"    [VERIFICAR MONTO ACTUALIZADO: serie {a.serie.upper()} - falta el "
                  f"período {', '.join(faltan)} en {ruta}]")
            raise SystemExit(2)
        coef = serie[p1] / serie[p0]
        actualizado = a.capital * coef
        puro = actualizado * a.interes_puro / 100 * Decimal(dias) / Decimal(365)
        print(f"  Serie             {a.serie.upper()}  ({ruta})")
        print(f"  Indice {p0}    {float(serie[p0]):>18,.4f}")
        print(f"  Indice {p1}    {float(serie[p1]):>18,.4f}")
        print(f"  Coeficiente       {float(coef):>18,.6f}")
        print()
        print(f"  Capital actualizado          {float(q(actualizado)):>18,.2f}")
        print(f"  Interes puro {float(a.interes_puro)}% anual      "
              f"{float(q(puro)):>18,.2f}")
        print(f"  TOTAL                        {float(q(actualizado + puro)):>18,.2f}")
        marcadores.append(
            "[VERIFICAR MONTO ACTUALIZADO: valores de la serie utilizada - contrastar contra "
            "la publicación oficial del organismo a la fecha del cálculo]")
        if a.interes_puro > 6:
            marcadores.append(
                "[VERIFICAR CRITERIO DEL FUERO: interés puro superior al 6% anual - "
                '"Barrios" (SCBA, C. 124.096, 17/04/2024) lo fija como techo]')
    else:
        if a.tna is None:
            raise SystemExit("--tna es obligatorio en modo tasa")
        interes = a.capital * a.tna / 100 * Decimal(dias) / Decimal(365)
        print(f"  TNA               {float(a.tna):>18,.2f} %")
        print(f"  Base de calculo   dias/365, sobre capital nominal, sin capitalizacion")
        print()
        print(f"  Interes                      {float(q(interes)):>18,.2f}")
        print(f"  TOTAL                        {float(q(a.capital + interes)):>18,.2f}")
        marcadores.append(
            "[VERIFICAR TASA VIGENTE: fuero - instrumento que fija la tasa y su valor para "
            "cada tramo del período; este cálculo usa una tasa única y sin capitalización]")

    marcadores.append(
        "[VERIFICAR TASA VIGENTE: fuero laboral PBA - determinar si el crédito cae bajo el "
        "art. 12 LRT texto Ley 27.348 (\"Galarza\", SCBA L. 132.729, 30/03/2026), bajo el "
        "art. 55 de la Ley 27.802, o bajo la doctrina \"Barrios\"]")

    print("\n  MARCADORES")
    for m in marcadores:
        print(f"    {m}")
    print("\n  Este script calcula un tramo unico. Si el crédito tiene tramos con criterios "
          "distintos\n  (por ejemplo, hasta la cuantificación y desde ahí al pago), correrlo "
          "una vez por tramo.")


if __name__ == "__main__":
    main()
