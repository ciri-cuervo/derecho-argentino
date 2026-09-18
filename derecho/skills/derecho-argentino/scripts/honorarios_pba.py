#!/usr/bin/env python3
"""Regulación de honorarios y aportes - Provincia de Buenos Aires (Ley 14.967).

Calculadora determinista para la skill `derecho-argentino`. El valor del jus NO se toma de
memoria: se pasa con --valor-jus o se lee de `derecho/fuentes/datos/jus-scba.csv`, y el
script informa siempre a qué fecha corresponde el valor usado.

Uso:
    python3 honorarios_pba.py --monto 22768351.81 --porcentaje 17.5
    python3 honorarios_pba.py --monto 22768351.81 --porcentaje 20 --valor-jus 53232 \
        --etapas-cumplidas 3 --etapas-totales 3 --tipo contradictorio

Base normativa: art. 9 (jus), art. 15 (forma, bajo pena de nulidad; el inc. d exige el monto
en jus), art. 16 (pautas), art. 21 (escala 10-25% en primera instancia y en Tribunales
Colegiados de Instancia Única), art. 22 (mínimo 7 jus), art. 23 (cuantía = total reclamado),
art. 28 inc. h (tres etapas en procesos orales ante tribunales colegiados), art. 43 (causas
laborales), art. 51 (regulación de oficio y diferimiento si hay intereses). Aportes: Ley
6.716, art. 12. Ver `references/sede-judicial-pba.md`, 1.6.6.
"""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP

from _raiz import datos

CENT = Decimal("0.01")
MINIMO_JUS = Decimal("7")      # art. 22
ESCALA_MIN = Decimal("10")     # art. 21
ESCALA_MAX = Decimal("25")     # art. 21
MEDIA_ESCALA = (ESCALA_MIN + ESCALA_MAX) / 2


def q(x) -> Decimal:
    return Decimal(str(x)).quantize(CENT, rounding=ROUND_HALF_UP)


def jus_del_repo(repo=None):
    d = datos(repo)
    if d is None:
        return None, None, ("no hay repo configurado: correr configurar.py, o pasar "
                            "--valor-jus")
    cand = d / "jus-scba.csv"
    if not cand.is_file():
        return None, None, f"no existe {cand}"
    lineas = [l for l in cand.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.lstrip().startswith("#")]
    filas = [f for f in csv.DictReader(lineas) if f.get("jus_ley_14967")]
    if not filas:
        return None, None, f"{cand} está vacío"
    filas.sort(key=lambda f: f["vigencia_desde"])
    u = filas[-1]
    return Decimal(u["jus_ley_14967"]), u["vigencia_desde"], u.get("fuente") or ""


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--monto", required=True, type=Decimal,
                   help="Monto del proceso (art. 23: total reclamado en demanda o reconvención)")
    p.add_argument("--porcentaje", required=True, type=Decimal,
                   help="Porcentaje de la escala del art. 21 (entre 10 y 25)")
    p.add_argument("--valor-jus", type=Decimal, default=None)
    p.add_argument("--repo", default=None,
                   help="Raíz del repo. Si se omite se resuelve sola (ver configurar.py)")
    p.add_argument("--etapas-cumplidas", type=int, default=None)
    p.add_argument("--etapas-totales", type=int, default=None,
                   help="En procesos orales ante tribunales colegiados son 3 (art. 28 inc. h)")
    p.add_argument("--con-intereses", action="store_true",
                   help="La condena incluye intereses u otros accesorios (art. 51, 2do párrafo)")
    p.add_argument("--tipo", choices=["contradictorio", "voluntario"],
                   default="contradictorio")
    p.add_argument("--tasa-justicia", type=Decimal, default=None,
                   help="Importe de la tasa de justicia, para la contribución del art. 12 inc. g")
    a = p.parse_args()

    marcadores, advertencias = [], []

    valor_jus, jus_fecha, jus_fuente = a.valor_jus, "informado por el usuario", ""
    if valor_jus is None:
        valor_jus, jus_fecha, jus_fuente = jus_del_repo(a.repo)
    if valor_jus is None:
        marcadores.append(
            "[VERIFICAR MONTO ACTUALIZADO: valor del jus del art. 9 de la Ley 14.967 - "
            f"resolución de la SCBA vigente a la fecha de la regulación; {jus_fuente}]")
        print("No hay valor del jus disponible: no se puede regular.\n")
        print("  " + marcadores[0])
        print("\n  Tabla oficial: https://www.scba.gov.ar/paginas.asp?id=41320")
        raise SystemExit(2)

    if not (ESCALA_MIN <= a.porcentaje <= ESCALA_MAX):
        raise SystemExit(
            f"El porcentaje {a.porcentaje} está fuera de la escala del art. 21 "
            f"({ESCALA_MIN}% a {ESCALA_MAX}%).")
    if a.porcentaje < MEDIA_ESCALA:
        advertencias.append(
            f"El porcentaje esta por debajo de la media de la escala ({MEDIA_ESCALA}%). "
            "El art. 16 manda partir de la media para el vencedor y permite disminuir "
            "fundadamente: la resolución debe expresar el fundamento.")

    bruto = a.monto * a.porcentaje / 100
    detalle_etapas = "sin proporción por etapas"
    if a.etapas_cumplidas and a.etapas_totales:
        if a.etapas_cumplidas > a.etapas_totales:
            raise SystemExit("Las etapas cumplidas no pueden superar las totales.")
        bruto = bruto * a.etapas_cumplidas / a.etapas_totales
        detalle_etapas = f"{a.etapas_cumplidas}/{a.etapas_totales} etapas (art. 28)"
        if a.etapas_totales == 3:
            detalle_etapas += (" inc. h: 1) demanda, contestaciones y segundos traslados; "
                               "2) prueba anterior a la vista; 3) audiencia de vista")
        else:
            advertencias.append(
                f"Se dividió en {a.etapas_totales} etapas. En procesos orales ante tribunales "
                "colegiados el art. 28 inc. h prevé TRES: demanda y contestaciones, prueba "
                "anterior a la vista, y audiencia de vista de la causa.")

    minimo = MINIMO_JUS * valor_jus
    aplico_minimo = bruto < minimo
    honorarios = minimo if aplico_minimo else bruto
    en_jus = (honorarios / valor_jus).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    aporte_afiliado = honorarios * Decimal("0.10")          # art. 12 inc. a, a cargo del profesional
    pct_obligado = Decimal("0.10") if a.tipo == "contradictorio" else Decimal("0.05")
    aporte_obligado = honorarios * pct_obligado

    print("REGULACIÓN DE HONORARIOS - Ley 14.967 (PBA)\n")
    print(f"  Monto del proceso (art. 23)      {float(q(a.monto)):>18,.2f}")
    print(f"  Porcentaje aplicado (art. 21)    {float(a.porcentaje):>18,.2f} %")
    print(f"  {detalle_etapas}")
    print(f"  Valor del jus utilizado          {float(q(valor_jus)):>18,.2f}   "
          f"(vigencia: {jus_fecha})")
    if jus_fuente:
        print(f"  Fuente del jus                   {jus_fuente}")
    print(f"  Mínimo del art. 22 (7 jus)       {float(q(minimo)):>18,.2f}")
    print()
    print(f"  HONORARIOS                       {float(q(honorarios)):>18,.2f}")
    print(f"  Expresado en jus (art. 15)       {float(en_jus):>18,.2f} jus")
    if aplico_minimo:
        print("  -> se aplicó el mínimo del art. 22; la escala arrojaba "
              f"{float(q(bruto)):,.2f}")
    print()
    print("  APORTES Y CONTRIBUCIONES - Ley 6.716, art. 12")
    print(f"  inc. a) 10% a cargo del profesional        {float(q(aporte_afiliado)):>14,.2f}")
    print(f"  inc. a) {int(pct_obligado*100)}% a cargo del obligado al pago  "
          f"{float(q(aporte_obligado)):>14,.2f}   ({a.tipo})")
    if a.tasa_justicia is not None:
        contrib = a.tasa_justicia * Decimal("0.05")
        print(f"  inc. g) 5% sobre la tasa de justicia       {float(q(contrib)):>14,.2f}")
        print("          (era 10% hasta la Ley 15.563, B.O. 23/12/2025)")
    else:
        marcadores.append(
            "[VERIFICAR MONTO ACTUALIZADO: alícuota de la tasa de justicia - ley impositiva "
            "de la PBA del ejercicio en curso; la contribución del art. 12 inc. g de la "
            "Ley 6.716 es el 5% de su importe]")

    marcadores.append(
        "[VERIFICAR MONTO ACTUALIZADO: valor del jus a la fecha de la regulación - "
        "https://www.scba.gov.ar/paginas.asp?id=41320]")

    if advertencias:
        print("\n  ADVERTENCIAS")
        for x in advertencias:
            print(f"    - {x}")
    print("\n  MARCADORES")
    for m in marcadores:
        print(f"    {m}")
    if a.con_intereses:
        print("\n  ART. 51, SEGUNDO PÁRRAFO - DIFERIMIENTO")
        print("  La condena incluye intereses u otros accesorios: corresponde DIFERIR el auto")
        print("  regulatorio y dejar constancia en la sentencia definitiva, hasta que quede")
        print("  firme la liquidación. Este cálculo sirve de referencia, no para regular hoy.")

    print("\n  Art. 15: la regulación debe ser fundada, indicar el monto del juicio, "
          "referenciar los\n  antecedentes, precisar las pautas del art. 16 y detallar cada "
          "tarea; y su inc. d exige\n  que el monto esté expresado en jus, cuyo valor "
          "definitivo se establece AL PAGO, no a la\n  regulación. Todo bajo pena de nulidad."
          "\n  Art. 51: la regulación se hace de oficio al dictar sentencia, aun sin petición "
          "de parte.")
    print("  Los honorarios periciales NO los regula la Ley 14.967: rige la ley de cada "
          "profesión.")


if __name__ == "__main__":
    main()
