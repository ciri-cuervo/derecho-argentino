#!/usr/bin/env python3
"""Descarga las series de indices que usan las calculadoras de la skill.

Fuente: API de Series de Tiempo del Estado (https://apis.datos.gob.ar/series/api/), publica,
sin token. Deja cada serie en `argentina/fuentes/datos/serie-<nombre>.csv` con el formato
`periodo,indice` que consume `scripts/intereses.py`, y un encabezado con la procedencia.

    python3 descargar_series.py                 # las tres
    python3 descargar_series.py --serie ipc
    python3 descargar_series.py --serie cer --desde 2020-01

Cuidado con los serie_id parecidos: `145.3_INGNACNAL_DICI_M_15` es el INDICE del IPC y
`145.3_INGNACUAL_DICI_M_38` es la VARIACION mensual. Difieren en un caracter. Por eso cada
serie declara un control de sanidad que el script verifica antes de escribir el archivo.
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
from datetime import date, datetime, timezone

from _comun import RAIZ, bajar, decodificar

DATOS = RAIZ / "datos"
API = "https://apis.datos.gob.ar/series/api/series/"

SERIES = {
    "ipc": {
        "id": "145.3_INGNACNAL_DICI_M_15",
        "titulo": "IPC INDEC - Nivel General Nacional, indice, base diciembre 2016 = 100",
        "organismo": "INDEC",
        "frecuencia": "mensual",
        "desde": "2016-12",
        "control": ("2016-12", 100.0),
        "nota": ("NO confundir con 145.3_INGNACUAL_DICI_M_38, que es la variacion mensual "
                 "y no el indice."),
    },
    "ripte": {
        "id": "158.1_REPTE_0_0_5",
        "titulo": "RIPTE - Remuneracion imponible promedio de los trabajadores estables",
        "organismo": "Secretaria de Trabajo, Empleo y Seguridad Social",
        "frecuencia": "mensual",
        "desde": "1994-07",
        "control": None,
        "nota": "Pesos corrientes. Es la serie que usa el art. 12 LRT texto Ley 27.348.",
    },
    "cer": {
        "id": "94.2_CD_D_0_0_10",
        "titulo": "CER - Coeficiente de Estabilizacion de Referencia (base 2/2/2002 = 1)",
        "organismo": "BCRA, via datos.gob.ar",
        "frecuencia": "diaria, colapsada a fin de mes",
        "desde": "2016-12",
        "control": None,
        "colapsar": True,
        "nota": ("La serie de datos.gob.ar suele atrasar unas dos semanas respecto del BCRA. "
                 "Para el CER del dia, ir a la API del BCRA: "
                 "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/30 (variable 30, sin "
                 "token; la v3.0 devuelve HTTP 410)."),
    },
}


def pedir(cfg: dict, desde: str, timeout: int = 180, reintentos: int = 3,
          verboso: bool = False) -> list:
    filas, offset = [], 0
    while True:
        url = (f"{API}?ids={cfg['id']}&format=csv&start_date={desde}&limit=1000"
               f"&offset={offset}")
        if cfg.get("colapsar"):
            url += "&collapse=month&collapse_aggregation=end_of_period"
        crudo, charset, _ = bajar(url, timeout=timeout, reintentos=reintentos,
                                  verboso=verboso)
        texto = decodificar(crudo, charset)
        lote = list(csv.reader(io.StringIO(texto)))
        if not lote:
            break
        cab, cuerpo = lote[0], [f for f in lote[1:] if f and f[0]]
        filas += cuerpo
        if len(cuerpo) < 1000:
            break
        offset += 1000
    return filas


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--serie", action="append", default=[], choices=list(SERIES))
    p.add_argument("--desde", default=None, help="Periodo inicial, YYYY-MM")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--reintentos", type=int, default=3)
    p.add_argument("--verboso", action="store_true")
    a = p.parse_args()

    nombres = a.serie or list(SERIES)
    error = 0
    for nombre in nombres:
        cfg = SERIES[nombre]
        desde = a.desde or cfg["desde"]
        try:
            filas = pedir(cfg, desde, a.timeout, a.reintentos, a.verboso)
        except Exception as e:
            print(f"  ERROR   {nombre:6} {type(e).__name__}: {e}")
            error += 1
            continue
        if not filas:
            print(f"  ERROR   {nombre:6} la API no devolvio datos")
            error += 1
            continue

        datos = []
        for f in filas:
            try:
                datos.append((f[0][:7], float(f[1])))
            except (IndexError, ValueError):
                continue
        datos.sort()

        if cfg["control"]:
            per, val = cfg["control"]
            hallado = dict(datos).get(per)
            if hallado is None or abs(hallado - val) > 0.001:
                print(f"  ERROR   {nombre:6} control de sanidad fallido: se esperaba "
                      f"{per} = {val} y llego {hallado}. NO se escribio el archivo: "
                      f"revisar el serie_id.")
                error += 1
                continue

        destino = DATOS / f"serie-{nombre}.csv"
        with destino.open("w", encoding="utf-8", newline="") as fh:
            fh.write(f"# {cfg['titulo']}\n")
            fh.write(f"# Organismo: {cfg['organismo']} - frecuencia: {cfg['frecuencia']}\n")
            fh.write(f"# serie_id: {cfg['id']}\n")
            fh.write(f"# Fuente: {API}?ids={cfg['id']}&format=csv&start_date={desde}\n")
            fh.write(f"# Descargado: {datetime.now(timezone.utc).date().isoformat()}"
                     f"  ({len(datos)} periodos, {datos[0][0]} a {datos[-1][0]})\n")
            for linea in cfg["nota"].split(". "):
                if linea.strip():
                    fh.write(f"# {linea.strip().rstrip('.')}.\n")
            fh.write("periodo,indice\n")
            for per, val in datos:
                fh.write(f"{per},{val}\n")
        print(f"  OK      {nombre:6} {len(datos):>5} periodos  {datos[0][0]} a {datos[-1][0]}"
              f"  -> {destino.name}")

    print(f"\n  {len(nombres) - error} series actualizadas, {error} con error.")
    print("  Las consume scripts/intereses.py de la skill. Volver a correr este script "
          "antes de\n  liquidar con un periodo posterior al ultimo descargado.")
    return 1 if error else 0


if __name__ == "__main__":
    sys.exit(main())
