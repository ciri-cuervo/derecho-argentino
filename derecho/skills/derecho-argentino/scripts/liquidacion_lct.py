#!/usr/bin/env python3
"""Liquidación por extinción del contrato de trabajo - LCT argentina.

Calculadora determinista para la skill `derecho-argentino`. NO trae montos: el tope del
art. 245 y las remuneraciones se pasan como entrada. Si falta un dato que condiciona el
resultado, el script lo dice y emite el marcador canónico en vez de suponerlo.

Uso:
    python3 liquidacion_lct.py --ingreso 2015-03-10 --extincion 2026-04-20 \
        --mejor-remuneracion 1850000 --remuneracion-ultimo-mes 1850000 \
        --tope-245 1420000 --dias-vacaciones-gozadas 0

    python3 liquidacion_lct.py ... --json     # para encadenar con otra herramienta

La salida SIN `--json` es el entregable: ya trae el tramo, el régimen, los rubros con su
norma, el total, las advertencias y los marcadores, formateados para pegar. Se pega tal
cual. `--json` es para que lo lea otro programa, y quien lo usa para redactar la respuesta
se convierte en el que rearma la tabla: ahí se pierde una advertencia sin que nada avise.

La LCT no rige todo trabajo dependiente: `--empleador publico` corta con código 2 y emite el
marcador, porque el art. 2 inc. a excluye a la Administración Pública salvo acto expreso de
inclusión. Sin el dato calcula igual, suponiendo empleo privado, y lo dice con un marcador.
`--regimen` hace lo mismo con los estatutos que desplazan la liquidación: casas particulares,
construcción, viajantes y encargados de edificio cortan con código 2.

Fórmulas y su norma en `FORMULAS.md` de esta carpeta. Toda salida debe cotejarse contra el
texto vigente del artículo: ver `references/laboral.md`, secciones 5.1 a 5.4 y 5.10.
"""

from __future__ import annotations

import argparse
import calendar
import json
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

# --- Tramos de reforma. Ver references/laboral.md, 5.1 ---------------------------------
TRAMOS = [
    (date(1974, 9, 21), date(2023, 12, 29), "original",
     "LCT texto original"),
    (date(2023, 12, 30), date(2024, 7, 8), "dnu70",
     "DNU 70/2023 - Título laboral estuvo judicialmente suspendido"),
    (date(2024, 7, 9), date(2026, 3, 5), "bases",
     "Ley 27.742 'Bases'"),
    (date(2026, 3, 6), date(9999, 12, 31), "modernizacion",
     "Ley 27.802 'Modernización Laboral'"),
]

# La ventana en la que 82 artículos de la Ley 27.802 estuvieron suspendidos por la cautelar del
# JNT N°63. NO es un tramo: adentro de ella rige la 27.802 igual, y lo que se desconoce es si el
# artículo aplicado estaba entre los suspendidos. Por eso es un marcador y no otra fila de TRAMOS.
# Ver references/laboral.md, 5.1.
VENTANA_CAUTELAR = (date(2026, 3, 30), date(2026, 4, 23))

CENT = Decimal("0.01")


def q(x) -> Decimal:
    return Decimal(str(x)).quantize(CENT, rounding=ROUND_HALF_UP)


def plural(n: int, singular: str, plural_: str | None = None) -> str:
    """«1 año y 1 mes», no «1 años y 1 meses». Esto sale impreso en una pieza."""
    return f"{n} {singular if n == 1 else (plural_ or singular + 's')}"


def tramo_de(f: date):
    for desde, hasta, clave, nombre in TRAMOS:
        if desde <= f <= hasta:
            return clave, nombre, desde, hasta
    raise SystemExit(f"Fecha fuera de todo tramo conocido: {f}")


def antiguedad(ingreso: date, extincion: date):
    """Años y meses cumplidos. Art. 245: un mes por año o fracción mayor a 3 meses."""
    if extincion < ingreso:
        raise SystemExit("La fecha de extinción es anterior a la de ingreso.")
    anios = extincion.year - ingreso.year
    meses = extincion.month - ingreso.month
    dias = extincion.day - ingreso.day
    if dias < 0:
        meses -= 1
    if meses < 0:
        anios -= 1
        meses += 12
    multiplicador = anios + (1 if meses > 3 else 0)
    return anios, meses, max(multiplicador, 1)


@dataclass
class Resultado:
    datos: dict = field(default_factory=dict)
    rubros: list = field(default_factory=list)
    marcadores: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)

    def add(self, concepto, importe, norma, detalle):
        self.rubros.append({"concepto": concepto, "importe": float(q(importe)),
                            "norma": norma, "detalle": detalle})

    @property
    def total(self):
        return q(sum(Decimal(str(r["importe"])) for r in self.rubros))


AMBITO = {
    "privado": None,
    "publico": (
        "[ARG SIN NORMA: el art. 2 inc. a LCT excluye a los dependientes de la Administración "
        "Pública nacional, provincial, de la CABA o municipal, salvo acto expreso de inclusión "
        "en la LCT o en un convenio colectivo que los comprenda. Sin ese acto la extinción no "
        "se liquida por los arts. 245 y siguientes: la rigen el estatuto y el régimen de "
        "estabilidad que correspondan, y la competencia suele ser contencioso administrativa. "
        "Si hay acto expreso de inclusión, correr con --empleador publico-incluido y dejar "
        "asentado cuál es]"),
    "publico-incluido": None,
}


REGIMEN = {
    "lct": None,
    "casas-particulares": (
        "[ARG SIN NORMA: liquidar por los arts. 232, 233 y 245 LCT a personal de casas "
        "particulares, que el art. 2 inc. b LCT excluye - norma que correspondería citar: "
        "Ley 26.844, arts. 42 a 44 (preaviso e integración) y 48 (indemnización, sin el tope "
        "del art. 245). Se liquida a mano: laboral.md 5.17 quinquies]"),
    "construccion": (
        "[ARG SIN NORMA: liquidar por los arts. 232, 233 y 245 LCT a un trabajador de la "
        "construcción - norma que correspondería citar: Ley 22.250, art. 15 (el fondo de cese "
        "laboral reemplaza el preaviso y el despido de la LCT) y arts. 17 a 19. Se liquida a "
        "mano: laboral.md 5.17 sexies]"),
    "viajantes": (
        "[ARG SIN NORMA: liquidar por la LCT sola a un viajante de comercio - norma que "
        "correspondería citar: Ley 14.546, art. 14 (indemnización por clientela, 25% de la de "
        "despido cualquiera sea la causa) y arts. 5 a 7 (base a comisión). Se liquida a mano: "
        "laboral.md 5.17 sexies]"),
    "encargados": (
        "[ARG SIN NORMA: liquidar por los arts. 232, 233 y 245 LCT a un encargado de edificio - "
        "norma que correspondería citar: Ley 12.981, art. 6 (tres meses de preaviso y un mes "
        "por año o fracción) y art. 22. Se liquida a mano: laboral.md 5.17 sexies]"),
}


def _cortar(datos, corte, como_json):
    if como_json:
        print(json.dumps({"datos": datos, "rubros": [], "total": None,
                          "advertencias": [], "marcadores": [corte]},
                         ensure_ascii=False, indent=2))
    else:
        print(corte)
    raise SystemExit(2)


def exigir_regimen(regimen, como_json=False):
    """Los estatutos especiales cortan antes de calcular, por lo mismo que el empleo público:
    el resultado entero sería de otro cuerpo legal y nada en el número lo delata. Lo
    desconocido corta, como en `exigir_ambito()`."""
    if regimen in (None, ""):
        return
    corte = REGIMEN.get(regimen, f"[ARG SIN NORMA: régimen {regimen} - norma que "
                                 f"correspondería citar: indeterminada]")
    if corte:
        _cortar({"estatuto": regimen}, corte, como_json)


def exigir_ambito(empleador, como_json=False):
    """La LCT no se aplica a todo trabajo dependiente, y esto corta antes de calcular.

    No es una advertencia al pie: si el régimen no es el de la LCT, el resultado entero
    pertenece a otro cuerpo legal. Una liquidación del art. 245 para una docente provincial
    sale con sus nueve rubros y su articulado, perfectamente formateada y bajo la ley que no
    la rige, y nada en el número delata el error.
    """
    if empleador in (None, "", "sin-declarar"):
        return
    # Todo valor que no sea uno de los declarados corta. Al revés --tratar lo desconocido como
    # "seguir"-- un `--empleador Publico` con otra caja liquidaría igual, y el corte sería una
    # formalidad que depende de escribir bien el valor.
    corte = AMBITO.get(empleador, AMBITO["publico"])
    if corte:
        _cortar({"empleador": empleador}, corte, como_json)


def liquidar(a) -> Resultado:
    r = Resultado()
    exigir_ambito(getattr(a, "empleador", None), getattr(a, "json", False))
    exigir_regimen(getattr(a, "regimen", None), getattr(a, "json", False))
    ingreso, extincion = a.ingreso, a.extincion
    clave, nombre, _, _ = tramo_de(extincion)
    anios, meses, mult = antiguedad(ingreso, extincion)

    r.datos = {
        "fecha_ingreso": ingreso.isoformat(),
        "fecha_extinción": extincion.isoformat(),
        "tramo": clave,
        "régimen": nombre,
        "antigüedad": f"{plural(anios, 'año')} y {plural(meses, 'mes', 'meses')}",
        "multiplicador_art_245": mult,
        "empleador": getattr(a, "empleador", None) or "sin declarar",
        "estatuto": getattr(a, "regimen", None) or "sin declarar",
    }

    if not getattr(a, "empleador", None):
        r.marcadores.append(
            "[VACÍO PROBATORIO: naturaleza del empleador - la LCT no rige el empleo público "
            "(art. 2 inc. a) y esta liquidación se hizo suponiendo empleo privado; confirmarlo "
            "antes de usarla]")

    if not getattr(a, "regimen", None):
        r.marcadores.append(
            "[VACÍO PROBATORIO: régimen de la relación - tareas y ámbito de la prestación: "
            "casas particulares, construcción, viajantes y encargados de edificio tienen "
            "estatuto propio y esta liquidación supone la LCT general]")

    if clave == "dnu70":
        r.marcadores.append(
            "[REVISIÓN NORMATIVA REQUERIDA: vigencia efectiva del Título laboral del "
            "DNU 70/2023 en el tramo del acto extintivo - verificar estado cautelar a esa fecha]")

    if VENTANA_CAUTELAR[0] <= extincion <= VENTANA_CAUTELAR[1]:
        r.marcadores.append(
            "[REVISIÓN NORMATIVA REQUERIDA: el acto extintivo cae en la ventana cautelar de la "
            "Ley 27.802 (30/03/2026 a 23/04/2026), en la que 82 artículos estuvieron suspendidos "
            "- verificar si el artículo aplicado estaba entre ellos]")

    mejor = Decimal(str(a.mejor_remuneracion))
    minimo_meses = 1 if clave == "modernizacion" else 2

    # --- Art. 245: base, tope y piso -----------------------------------------------------
    if a.tope_245 is None:
        r.marcadores.append(
            "[VERIFICAR MONTO ACTUALIZADO: tope art. 245 LCT - CCT aplicable, resolución "
            "del MTEySS del período del acto extintivo]")
        base = mejor
        r.advertencias.append(
            "Sin tope informado: la base del art. 245 se calculó SIN tope. El resultado no "
            "es definitivo hasta cargar el tope del CCT al período.")
        piso_aplicado = False
    else:
        tope = Decimal(str(a.tope_245))
        topeada = min(mejor, tope)
        piso = mejor * Decimal("0.67")
        base = max(topeada, piso)
        piso_aplicado = base == piso and piso > topeada
        if piso_aplicado:
            if clave == "modernizacion":
                r.advertencias.append(
                    "Se aplicó el piso del 67% de la remuneración (art. 245 texto art. 51 "
                    "Ley 27.802): está en el texto legal, no hace falta invocar 'Vizzoti'.")
            else:
                r.advertencias.append(
                    "Se aplicó el piso del 67% por doctrina 'Vizzoti' (CSJN, 2004). En este "
                    "tramo NO es texto legal: es doctrina jurisprudencial y debe fundarse.")
                r.marcadores.append(
                    '[VERIFICAR PRECEDENTE: "Vizzoti" (CSJN, 2004) - confirmar que no fue '
                    'dejado sin efecto ni superado antes de citar]')

    antiguedad_imp = base * mult
    minimo_imp = mejor * minimo_meses
    if antiguedad_imp < minimo_imp:
        antiguedad_imp = minimo_imp
        r.advertencias.append(
            f"Se aplicó el mínimo legal de {plural(minimo_meses, 'mes', 'meses')} de sueldo.")

    r.add("Indemnización por antigüedad", antiguedad_imp, "Art. 245 LCT",
          f"base {q(base)} x {mult} (mínimo {plural(minimo_meses, 'mes', 'meses')})")

    rem_mes = Decimal(str(a.remuneracion_ultimo_mes if a.remuneracion_ultimo_mes
                          is not None else a.mejor_remuneracion))

    # --- Preaviso omitido ----------------------------------------------------------------
    if a.preaviso_otorgado:
        r.advertencias.append("Preaviso otorgado: no se liquida indemnización sustitutiva.")
        preaviso = Decimal("0")
    elif a.periodo_prueba:
        if clave == "modernizacion":
            preaviso = Decimal("0")
            r.advertencias.append(
                "Período de prueba y acto extintivo desde el 06/03/2026: sin preaviso "
                "(art. 231 inc. b, texto art. 48 Ley 27.802).")
        else:
            preaviso = rem_mes / 2
            r.advertencias.append(
                "Período de prueba antes del 06/03/2026: preaviso de 15 días.")
        r.marcadores.append(
            "[VACÍO PROBATORIO: vigencia del período de prueba a la fecha de la extinción - "
            "si ya había vencido, corresponden todos los derechos del despido sin causa]")
    else:
        meses_preaviso = 1 if anios <= 5 else 2
        preaviso = rem_mes * meses_preaviso
    if preaviso:
        r.add("Indemnización sustitutiva de preaviso", preaviso,
              "Art. 232 y 231 LCT", f"remuneración {q(rem_mes)}")
        r.add("SAC sobre preaviso", preaviso / 12, "Art. 121 y 123 LCT", "un doceavo")

    # --- Integración del mes de despido --------------------------------------------------
    dias_mes = calendar.monthrange(extincion.year, extincion.month)[1]
    dias_restantes = dias_mes - extincion.day
    if a.preaviso_otorgado or a.periodo_prueba:
        dias_restantes = 0
        r.advertencias.append(
            "No se liquida integración del mes de despido (preaviso otorgado o período de "
            "prueba). Verificar el supuesto del art. 233 antes de descartarla.")
    if dias_restantes > 0:
        integracion = rem_mes * dias_restantes / dias_mes
        r.add("Integración del mes de despido", integracion, "Art. 233 LCT",
              f"{dias_restantes}/{dias_mes} días")
        r.add("SAC sobre integración", integracion / 12, "Art. 121 y 123 LCT", "un doceavo")

    # --- Liquidación final ---------------------------------------------------------------
    dias_trabajados_mes = extincion.day
    r.add("Días trabajados del mes", rem_mes * dias_trabajados_mes / dias_mes,
          "Art. 103 LCT", f"{dias_trabajados_mes}/{dias_mes} días")

    inicio_sem = date(extincion.year, 1 if extincion.month <= 6 else 7, 1)
    dias_sem_trab = (extincion - max(inicio_sem, ingreso)).days + 1
    fin_sem = date(extincion.year, 6, 30) if extincion.month <= 6 else date(extincion.year, 12, 31)
    dias_sem = (fin_sem - inicio_sem).days + 1
    sac = (mejor / 2) * Decimal(dias_sem_trab) / Decimal(dias_sem)
    r.add("SAC proporcional", sac, "Art. 121 y 123 LCT",
          f"{dias_sem_trab}/{dias_sem} días del semestre, sobre la mejor remuneración")

    # --- Vacaciones no gozadas -----------------------------------------------------------
    if anios < 5:
        dias_vac = 14
    elif anios < 10:
        dias_vac = 21
    elif anios < 20:
        dias_vac = 28
    else:
        dias_vac = 35
    inicio_anio = date(extincion.year, 1, 1)
    dias_anio_trab = (extincion - max(inicio_anio, ingreso)).days + 1
    dias_del_anio = 366 if calendar.isleap(extincion.year) else 365
    vac_prop = Decimal(dias_vac) * Decimal(dias_anio_trab) / Decimal(dias_del_anio)
    vac_prop -= Decimal(str(a.dias_vacaciones_gozadas))
    if vac_prop < 0:
        vac_prop = Decimal("0")
    if vac_prop > 0:
        importe_vac = (rem_mes / 25) * vac_prop
        r.add("Vacaciones no gozadas proporcionales", importe_vac,
              "Arts. 150, 155 y 156 LCT",
              f"{q(vac_prop)} días, valor día = remuneración / 25")
        r.add("SAC sobre vacaciones no gozadas", importe_vac / 12,
              "Art. 121 y 123 LCT", "un doceavo")
        r.advertencias.append(
            "Vacaciones: el divisor 25 del art. 155 y la proporcionalidad del art. 156 "
            "admiten lecturas distintas según el fuero. Verificar el criterio aplicable.")

    # --- Agravantes ----------------------------------------------------------------------
    if extincion >= date(2024, 7, 9):
        r.advertencias.append(
            "Acto extintivo desde el 09/07/2024: los agravantes de la Ley 24.013 (arts. 8 a 17) "
            "y de la Ley 25.323 están DEROGADOS. No incorporarlos. Ver 5.3.")
    else:
        r.marcadores.append(
            "[VACÍO PROBATORIO: intimación fehaciente previa del trabajador - los agravantes "
            "de la Ley 24.013 y el art. 2 de la Ley 25.323 la requerían; sin intimación "
            "acreditada no proceden]")

    r.marcadores.append(
        "[VERIFICAR CCT APLICABLE: actividad del empleador - tope art. 245 y escalas "
        "salariales del período]")
    r.marcadores.append(
        "[VERIFICAR TASA VIGENTE: fuero - intereses no incluidos en esta liquidación; "
        "ver 5.5 para el fuero nacional y 5.5 bis para PBA]")
    return r


def render(r: Resultado) -> str:
    out = ["LIQUIDACIÓN POR EXTINCIÓN DEL CONTRATO DE TRABAJO", ""]
    for k, v in r.datos.items():
        out.append(f"  {k.replace('_', ' '):28} {v}")
    out += ["", "RUBROS", ""]
    ancho = max(len(x["concepto"]) for x in r.rubros)
    for x in r.rubros:
        out.append(f"  {x['concepto']:<{ancho}}  {x['importe']:>16,.2f}   {x['norma']}")
        out.append(f"  {'':<{ancho}}  {x['detalle']}")
    out += ["", f"  {'TOTAL':<{ancho}}  {float(r.total):>16,.2f}", ""]
    if r.advertencias:
        out += ["ADVERTENCIAS", ""] + [f"  - {x}" for x in r.advertencias] + [""]
    out += ["MARCADORES", ""] + [f"  {x}" for x in r.marcadores] + [""]
    out += ["Verificación de cierre: recalcular cada rubro por separado y comprobar que los",
            "subtotales sumen el total. Los intereses no están incluidos.", ""]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ingreso", required=True, type=date.fromisoformat)
    p.add_argument("--extincion", required=True, type=date.fromisoformat)
    p.add_argument("--mejor-remuneracion", required=True, type=Decimal,
                   help="Mejor remuneración mensual, normal y habitual del último año")
    p.add_argument("--remuneracion-ultimo-mes", type=Decimal, default=None,
                   help="Si se omite, se usa la mejor remuneración")
    p.add_argument("--tope-245", type=Decimal, default=None,
                   help="Tope del CCT al período. Sin este dato el resultado es provisorio")
    p.add_argument("--empleador", choices=sorted(AMBITO), default=None,
                   help="a quién le prestaba servicios. La LCT no rige el empleo público "
                        "(art. 2 inc. a): sin este dato la liquidación sale con su marcador")
    p.add_argument("--regimen", choices=sorted(REGIMEN), default=None,
                   help="estatuto de la relación. Casas particulares, construcción, viajantes "
                        "y encargados no se liquidan acá: cortan con código 2")
    p.add_argument("--dias-vacaciones-gozadas", type=Decimal, default=Decimal("0"))
    p.add_argument("--periodo-prueba", action="store_true")
    p.add_argument("--preaviso-otorgado", action="store_true")
    p.add_argument("--json", action="store_true",
                   help="salida para encadenar con otra herramienta; para redactar se "
                        "usa la salida plana, que trae lo mismo y ya viene formateada")
    a = p.parse_args()
    r = liquidar(a)
    if a.json:
        print(json.dumps({"datos": r.datos, "rubros": r.rubros, "total": float(r.total),
                          "advertencias": r.advertencias, "marcadores": r.marcadores},
                         ensure_ascii=False, indent=2))
    else:
        print(render(r))


if __name__ == "__main__":
    main()
