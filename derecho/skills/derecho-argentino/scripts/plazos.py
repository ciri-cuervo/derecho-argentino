#!/usr/bin/env python3
"""Cómputo de plazos procesales - derecho argentino.

Calculadora determinista para la skill `derecho-argentino`. Los feriados móviles (Carnaval y
Viernes Santo) se calculan con el cómputo de Pascua; los inamovibles y trasladables salen de
la Ley 27.399. Los **puentes turísticos**, los **asuetos** y las **ferias judiciales** NO se
pueden calcular: se leen de `derecho/fuentes/datos/inhabiles.json` y, si ese archivo no
tiene cargado el año del cómputo, el script lo dice y emite el marcador.

Uso:
    python3 plazos.py --tipo hábiles --dias 5 --desde 2026-09-10 --fuero pba
    python3 plazos.py --tipo corridos --dias 30 --desde 2026-09-10
    python3 plazos.py --tipo meses --cantidad 6 --desde 2026-03-31
    python3 plazos.py --tipo años --cantidad 2 --desde 2024-05-10

`--desde` es la fecha de NOTIFICACIÓN en los plazos judiciales: el cómputo arranca al dia
siguiente y no cuenta el dia de la notificación (art. 156 CPCCN / art. 156 CPCCBA).
Ver `references/plazos.md`.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from _raiz import datos

FUEROS = {
    "nacional": {"gracia_horas": 2, "norma_gracia": "art. 124 CPCCN"},
    "pba": {"gracia_horas": 4, "norma_gracia": "art. 124 CPCCBA"},
}


def pascua(anio: int) -> date:
    """Cómputo de Pascua (algoritmo de Meeus/Jones/Butcher, calendario gregoriano)."""
    a = anio % 19
    b, c = divmod(anio, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return date(anio, mes, dia + 1)


def trasladar(f: date) -> date:
    """Art. 6 Ley 27.399: los feriados trasladables del art. 1 inc. b que caen martes o
    miercoles pasan al lunes anterior; los que caen jueves o viernes, al lunes siguiente.

    Sabado y domingo quedan sin mover por esta función: el Decreto 614/2025 habilita a la
    Jefatura de Gabinete a llevarlos al viernes anterior o al lunes posterior, y esa opción
    no es calculable. Esos casos se informan aparte (ver `trasladables_dudosos`)."""
    if f.weekday() in (1, 2):
        return f - timedelta(days=f.weekday())
    if f.weekday() in (3, 4):
        return f + timedelta(days=7 - f.weekday())
    return f


def trasladables_dudosos(anio: int) -> list:
    """Trasladables que caen sabado o domingo: ubicación indeterminada hasta que la
    Jefatura de Gabinete ejerza la opción del Decreto 614/2025."""
    base = {date(anio, 6, 17): "Güemes", date(anio, 8, 17): "San Martín",
            date(anio, 10, 12): "Diversidad Cultural", date(anio, 11, 20): "Soberanía Nacional"}
    return [f"{f.isoformat()} ({n}) cae {'sabado' if f.weekday() == 5 else 'domingo'}"
            for f, n in base.items() if f.weekday() >= 5]


def feriados_ley_27399(anio: int) -> dict:
    p = pascua(anio)
    inamovibles = {
        date(anio, 1, 1): "Año nuevo",
        p - timedelta(days=48): "Carnaval (lunes)",
        p - timedelta(days=47): "Carnaval (martes)",
        date(anio, 3, 24): "Día de la Memoria",
        p - timedelta(days=2): "Viernes Santo",
        date(anio, 4, 2): "Malvinas",
        date(anio, 5, 1): "Día del Trabajador",
        date(anio, 5, 25): "Revolución de Mayo",
        date(anio, 6, 20): "Paso a la Inmortalidad de Belgrano",
        date(anio, 7, 9): "Día de la Independencia",
        date(anio, 12, 8): "Inmaculada Concepción",
        date(anio, 12, 25): "Navidad",
    }
    trasladables = {}
    for f, n in {date(anio, 6, 17): "Güemes", date(anio, 8, 17): "San Martín",
                 date(anio, 10, 12): "Diversidad Cultural",
                 date(anio, 11, 20): "Soberanía Nacional"}.items():
        trasladables[trasladar(f)] = n + " (trasladable)"
    return {**inamovibles, **trasladables}


def cargar_datos(anio: int, jurisdiccion: str, repo=None):
    """Lee puentes, asuetos y ferias del repo. Devuelve (inhábiles_extra, ferias, meta).

    Los asuetos distritales NO se descuentan: alcanzan a un partido o dependencia y no a
    toda la jurisdicción. Se informan para que quien computa decida si aplican a la causa."""
    d = datos(repo)
    cand = None if d is None else d / "inhabiles.json"
    if cand is None or not cand.is_file():
        return set(), [], {
            "estado": "SIN ARCHIVO",
            "detalle": ("no hay repo configurado en esta máquina: correr configurar.py"
                        if d is None else f"falta {cand}"),
            "pendientes": [], "distritales": [], "trasladables_verificados": []}
    crudo = json.loads(cand.read_text(encoding="utf-8"))
    bloque = crudo.get("anios", {}).get(str(anio), {}).get(jurisdiccion)
    if not bloque:
        return set(), [], {"estado": "SIN DATOS",
                           "detalle": f"inhabiles.json no tiene {jurisdiccion} para {anio}",
                           "verificado": crudo.get("verificado"),
                           "pendientes": [], "distritales": [],
                           "trasladables_verificados": []}
    extra = {date.fromisoformat(d) for d in bloque.get("puentes_y_asuetos", [])}
    ferias = [(date.fromisoformat(f["desde"]), date.fromisoformat(f["hasta"]))
              for f in bloque.get("ferias", [])]
    comun = {"pendientes": bloque.get("pendientes", []),
             "distritales": bloque.get("asuetos_distritales", []),
             "trasladables_verificados": bloque.get("trasladables_verificados", [])}
    if not bloque.get("verificado"):
        return extra, ferias, {
            "estado": "PENDIENTE",
            "detalle": (f"el bloque {jurisdiccion}/{anio} de inhabiles.json está sin verificar "
                        "(campo 'verificado' vacío): faltan cargar ferias, puentes y asuetos"),
            "verificado": None, **comun}
    return extra, ferias, {"estado": "OK", "verificado": bloque.get("verificado"),
                           "fuente": bloque.get("fuente"), **comun}


def es_habil(f: date, feriados: dict, extra: set, ferias: list) -> tuple:
    if f.weekday() >= 5:
        return False, "fin de semana"
    if f in feriados:
        return False, feriados[f]
    if f in extra:
        return False, "puente o asueto"
    for desde, hasta in ferias:
        if desde <= f <= hasta:
            return False, "feria judicial"
    return True, ""


def computar_habiles(desde: date, dias: int, jurisdiccion: str, repo=None):
    feriados, extra, ferias, metas = {}, set(), [], []
    for anio in {desde.year, desde.year + 1}:
        feriados.update(feriados_ley_27399(anio))
        e, fr, meta = cargar_datos(anio, jurisdiccion, repo)
        extra |= e
        ferias += fr
        metas.append({"anio": anio, **meta})
    # Control cruzado: el cálculo del art. 6 contra la ubicación verificada del año.
    for m in metas:
        verificados = {date.fromisoformat(d) for d in m.get("trasladables_verificados", [])}
        if not verificados:
            continue
        calculados = {f for f, n in feriados_ley_27399(m["anio"]).items()
                      if n.endswith("(trasladable)")}
        if verificados != calculados:
            m["divergencia_trasladables"] = (
                f"calculado {sorted(d.isoformat() for d in calculados)} vs verificado "
                f"{sorted(d.isoformat() for d in verificados)}")
        for f in verificados:
            feriados[f] = "Feriado trasladable (verificado)"

    cur, contados, traza = desde, 0, []
    while contados < dias:
        cur += timedelta(days=1)
        habil, motivo = es_habil(cur, feriados, extra, ferias)
        if habil:
            contados += 1
            traza.append(f"{cur.isoformat()}  habil  ({contados}/{dias})")
        else:
            traza.append(f"{cur.isoformat()}  INHABIL  {motivo}")
        if (cur - desde).days > 3000:
            raise SystemExit("Cómputo desbordado: revisar los datos de inhábiles.")
    return cur, traza, metas


def sumar_meses(f: date, cantidad: int) -> date:
    """Arts. 6 y 7 CCyCN: de fecha a fecha; si el mes de vencimiento no tiene el dia
    equivalente, vence el último dia de ese mes."""
    import calendar
    mes = f.month - 1 + cantidad
    anio = f.year + mes // 12
    mes = mes % 12 + 1
    dia = min(f.day, calendar.monthrange(anio, mes)[1])
    return date(anio, mes, dia)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tipo", required=True,
                   choices=["habiles", "corridos", "meses", "anios"])
    p.add_argument("--desde", required=True, type=date.fromisoformat,
                   help="Fecha de notificación o de inicio del cómputo")
    p.add_argument("--dias", type=int, help="Para --tipo habiles o corridos")
    p.add_argument("--cantidad", type=int, help="Para --tipo meses o anios")
    p.add_argument("--fuero", default="pba", choices=list(FUEROS))
    p.add_argument("--traza", action="store_true", help="Imprime el detalle dia por dia")
    p.add_argument("--repo", default=None,
                   help="Raiz del repo. Si se omite se resuelve sola (ver configurar.py)")
    a = p.parse_args()

    print(f"CÓMPUTO DE PLAZO - tipo: {a.tipo} - fuero: {a.fuero}")
    print(f"  Fecha de inicio (no se cuenta): {a.desde.isoformat()}")
    marcadores = []

    if a.tipo == "habiles":
        if not a.dias:
            raise SystemExit("--dias es obligatorio para --tipo hábiles")
        venc, traza, metas = computar_habiles(a.desde, a.dias, a.fuero, a.repo)
        atravesados = set(range(a.desde.year, venc.year + 1))
        metas = [m for m in metas if m["anio"] in atravesados]
        print(f"  Plazo: {a.dias} días hábiles judiciales")
        print(f"  VENCIMIENTO: {venc.isoformat()} ({venc.strftime('%A')})")
        g = FUEROS[a.fuero]
        print(f"  Plazo de gracia: primeras {g['gracia_horas']} horas de despacho del día "
              f"hábil siguiente ({g['norma_gracia']}) -> {(venc + timedelta(days=1)).isoformat()} o el hábil posterior")
        for m in metas:
            if m.get("divergencia_trasladables"):
                marcadores.append(
                    f"[VERIFICAR PLAZO: ubicación de los feriados trasladables de {m['anio']} - "
                    f"{m['divergencia_trasladables']}; se usó la lista verificada]")
            for d in trasladables_dudosos(m["anio"]):
                marcadores.append(
                    f"[VERIFICAR PLAZO: feriado trasladable de ubicación indeterminada - {d}; "
                    "el Decreto 614/2025 deja la opción a la Jefatura de Gabinete y el cómputo "
                    "NO lo descuenta]")
            for x in m.get("pendientes", []):
                marcadores.append(f"[VERIFICAR PLAZO: {a.fuero} {m['anio']} - {x}]")
            for d in m.get("distritales", []):
                print(f"  Asueto distrital {m['anio']}: {d['fecha']} - {d['alcance']} "
                      f"({d.get('norma','')}). NO descontado: verificar si alcanza a la causa.")
            if m["estado"] != "OK":
                marcadores.append(
                    f"[VERIFICAR PLAZO: ferias, puentes y asuetos de {m['anio']} para "
                    f"{a.fuero} - {m['detalle']}; el vencimiento calculado NO los descuenta]")
            else:
                print(f"  Inhábiles {m['anio']}: cargados, verificados al {m.get('verificado')} "
                      f"({m.get('fuente')})")
        if a.traza:
            print("\n  TRAZA")
            for t in traza:
                print(f"    {t}")
    elif a.tipo == "corridos":
        if not a.dias:
            raise SystemExit("--dias es obligatorio para --tipo corridos")
        venc = a.desde + timedelta(days=a.dias)
        print(f"  Plazo: {a.dias} dias corridos (art. 6 CCyCN)")
        print(f"  VENCIMIENTO: {venc.isoformat()} ({venc.strftime('%A')})")
        print("  Sin traslado por vencimiento en inhábil, salvo norma expresa.")
    else:
        if not a.cantidad:
            raise SystemExit("--cantidad es obligatorio para --tipo meses o anios")
        n = a.cantidad * (12 if a.tipo == "anios" else 1)
        venc = sumar_meses(a.desde, n)
        print(f"  Plazo: {a.cantidad} {a.tipo} (arts. 6 y 7 CCyCN, de fecha a fecha)")
        print(f"  VENCIMIENTO: {venc.isoformat()} ({venc.strftime('%A')})")

    marcadores.append(
        "[VERIFICAR PLAZO: acto procesal - confirmar la norma de la jurisdicción que fija "
        "este plazo antes de usar el resultado]")
    print("\n  MARCADORES")
    for m in marcadores:
        print(f"    {m}")
    print("\n  Feriados: inamovibles y trasladables del art. 1 de la Ley 27.399; los "
          "trasladables se\n  ubicaron por la regla del art. 6 y, cuando el año está cargado en "
          "inhábiles.json, se\n  usa la ubicación verificada. Los puentes los fija cada año la "
          "Jefatura de Gabinete\n  (art. 7): sin ese dato cargado, el cómputo no los descuenta.")


if __name__ == "__main__":
    main()
