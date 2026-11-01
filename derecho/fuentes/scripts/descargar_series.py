#!/usr/bin/env python3
"""Descarga las series de índices que usan las calculadoras de la skill.

Fuentes: el CSV del INDEC para el IPC y la API de estadísticas del BCRA para el CER, que son las
de los organismos que los publican —las copias de datos.gob.ar dejaron de actualizarse—, y la API
de Series de Tiempo del Estado (https://apis.datos.gob.ar/series/api/) para el RIPTE, completada
con la página del organismo. Las dos son públicas y sin token. Deja
cada serie en `derecho/fuentes/datos/serie-<nombre>.csv` con el formato
`periodo,indice` que consume `scripts/intereses.py`, y un encabezado con la procedencia.

    python3 descargar_series.py                 # las tres
    python3 descargar_series.py --serie ipc
    python3 descargar_series.py --serie cer --desde 2020-01

Cuidado con los serie_id parecidos: `145.3_INGNACNAL_DICI_M_15` es el ÍNDICE del IPC y
`145.3_INGNACUAL_DICI_M_38` es la VARIACIÓN mensual. Difieren en un carácter, y bajar la
equivocada da un archivo con el formato correcto y los números de otra cosa.

Contra eso hay dos controles, y ninguno se escribe al archivo si falla:

  el ancla        el valor de un período que la serie tiene por DEFINICIÓN, como el IPC de
                  diciembre de 2016 = 100 por ser su base. Sólo existe si la serie declara una
                  base dentro del rango que pedimos, así que no todas pueden tenerla; las que
                  no, lo dicen en su entrada.
  la continuidad  que no falte ni se repita un mes. Vale para las tres y no depende de conocer
                  ningún valor. Un hueco no rompe nada visible: `intereses.py` actualiza entre
                  dos períodos y un mes faltante le cambia el resultado en silencio.
"""
from __future__ import annotations

import argparse
import calendar
import csv
import io
import json
import re
import sys
import textwrap

from _comun import RAIZ, bajar, decodificar, hoy

DATOS = RAIZ / "datos"
API = "https://apis.datos.gob.ar/series/api/series/"
API_BCRA = "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/"

SERIES = {
    "ipc": {
        "id": "serie_ipc_divisiones.csv, `Codigo` 0, `Region` Nacional",
        "api": "indec",
        "titulo": "IPC INDEC - Nivel General Nacional, índice, base diciembre 2016 = 100",
        "organismo": "INDEC, serie de divisiones",
        "frecuencia": "mensual",
        "desde": "2016-12",
        "control": ("2016-12", 100.0),
        "nota": ("Sale del CSV que publica el INDEC: la copia de datos.gob.ar "
                 "(145.3_INGNACNAL_DICI_M_15) dejó de traer los meses nuevos. En ese CSV la "
                 "columna `Indice_IPC` es el índice y `v_m_IPC` la variación mensual: se toma "
                 "la primera, del `Codigo` 0 y la `Region` Nacional."),
    },
    "ripte": {
        "id": "158.1_REPTE_0_0_5",
        "titulo": "RIPTE - Remuneración imponible promedio de los trabajadores estables",
        "organismo": "Secretaría de Trabajo, Empleo y Seguridad Social",
        "frecuencia": "mensual",
        "desde": "1994-07",
        # Sin ancla posible: el RIPTE son pesos corrientes y no declara base, así que no hay un
        # valor que la serie tenga por definición. Lo que la cubre es la continuidad.
        "control": None,
        "complemento": "ripte",
        "nota": "Pesos corrientes. Es la serie que usa el art. 12 LRT texto Ley 27.348.",
    },
    "cer": {
        "id": "30",
        "api": "bcra",
        "titulo": "CER - Coeficiente de Estabilización de Referencia (base 02/02/2002 = 1)",
        "organismo": "BCRA, API de estadísticas v4.0, variable 30",
        "frecuencia": "diaria, colapsada al último día de cada mes completo",
        "desde": "2016-12",
        # El CER sí tiene base -02/02/2002 = 1- pero cae FUERA del rango que pedimos, así que no
        # sirve de ancla mientras arranquemos en 2016-12. Se cubre con la continuidad.
        "control": None,
        "nota": ("Un mes entra sólo si la API trae su último día: el mes en curso queda afuera "
                 "hasta cerrarse. Para el CER de un día puntual, la misma API con desde y "
                 "hasta: https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/30 (sin token; "
                 "la v3.0 devuelve HTTP 410)."),
    },
}


PAGINA = 1000
IPC_INDEC = "https://www.indec.gob.ar/ftp/cuadros/economia/serie_ipc_divisiones.csv"
RIPTE_PAGINA = "https://www.argentina.gob.ar/trabajo/seguridadsocial/ripte"
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
         "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11,
         "diciembre": 12}
PAGINA_BCRA = 3000


def pedir(cfg: dict, desde: str, timeout: int = 180, reintentos: int = 3,
          verboso: bool = False) -> list:
    """Todas las páginas de la serie. La condición de corte mira la página CRUDA.

    Comparar el largo del cuerpo YA FILTRADO contra el límite trunca la serie en silencio: basta
    una fila con el período vacío en una página completa para que el filtro deje 999, el bucle
    corte y falten todos los períodos siguientes. El archivo sale bien formado y con menos datos,
    que es la peor forma de estar mal.
    """
    filas, offset = [], 0
    while True:
        url = (f"{API}?ids={cfg['id']}&format=csv&start_date={desde}&limit={PAGINA}"
               f"&offset={offset}")
        crudo, charset, _ = bajar(url, timeout=timeout, reintentos=reintentos,
                                  verboso=verboso)
        texto = decodificar(crudo, charset)
        lote = list(csv.reader(io.StringIO(texto)))
        if not lote:
            break
        crudas = lote[1:]                       # sin el encabezado que trae cada página
        filas += [f for f in crudas if f and f[0]]
        if len(crudas) < PAGINA:
            break
        offset += PAGINA
    return filas


def pedir_bcra(cfg: dict, desde: str, timeout: int = 180, reintentos: int = 3,
               verboso: bool = False, hasta=None) -> list:
    """La variable diaria del BCRA, colapsada al último día de cada mes.

    Devuelve filas `[fecha, valor]` como `pedir()`, para que el resto del flujo —ancla,
    continuidad, no perder períodos— sea el mismo. Un mes sin su último día no entra: el valor
    de otro día no es el de fin de mes, y un mes salteado lo atrapa después la continuidad.
    """
    hasta = hasta or hoy()
    diarios, offset = {}, 0
    while True:
        url = (f"{API_BCRA}{cfg['id']}?desde={desde}-01&hasta={hasta}"
               f"&limit={PAGINA_BCRA}&offset={offset}")
        crudo, charset, _ = bajar(url, timeout=timeout, reintentos=reintentos,
                                  verboso=verboso)
        cuerpo = json.loads(decodificar(crudo, charset))
        resultados = cuerpo.get("results") or []
        detalle = resultados[0].get("detalle", []) if resultados else []
        for d in detalle:
            diarios[d["fecha"]] = d["valor"]
        if len(detalle) < PAGINA_BCRA:
            break
        offset += PAGINA_BCRA
    filas = []
    for fecha in sorted(diarios):
        anio, mes, dia = int(fecha[:4]), int(fecha[5:7]), int(fecha[8:10])
        if dia == calendar.monthrange(anio, mes)[1]:
            filas.append([fecha, repr(float(diarios[fecha]))])
    return filas


def leer_tabla_ripte(html: str) -> list:
    """(período, valor) de la tabla de la página oficial del RIPTE.

    La página escribe el mes de dos formas en la misma tabla —`Agosto2026` y `Febrero/2025`— y el
    monto como `$ 1.982.518,19`. Una fila que no se lee así se descarta: la que importa la
    controla después `completar()` contra el archivo."""
    filas = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        celdas = [re.sub(r"<[^>]+>", " ", c).strip()
                  for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S | re.I)]
        if len(celdas) < 2:
            continue
        m = re.fullmatch(r"([a-záéíóúüñ]+)\s*/?\s*(\d{4})", celdas[0].lower().replace("&nbsp;", ""))
        monto = re.fullmatch(r"\$\s*([\d.]+,\d+)", celdas[1].replace("&nbsp;", " ").strip())
        if not m or not monto or m.group(1) not in MESES:
            continue
        filas.append((f"{m.group(2)}-{MESES[m.group(1)]:02d}",
                      float(monto.group(1).replace(".", "").replace(",", "."))))
    return sorted(filas)


def completar(en_disco: list, nuevos: list):
    """La serie del archivo más los meses nuevos de otra fuente, o (None, motivo).

    Sólo se acepta si las dos fuentes se solapan y coinciden al centavo en cada mes común: es lo
    que prueba que miden lo mismo. Sin solapamiento no hay contra qué cotejar, y no se agrega."""
    previos = dict(en_disco)
    comunes = [p for p, _ in nuevos if p in previos]
    if not comunes:
        return None, "la página oficial no comparte ningún mes con el archivo: no hay cotejo"
    for p, v in nuevos:
        if p in previos and abs(previos[p] - v) > 0.005:
            return None, f"{p}: el archivo dice {previos[p]} y la página {v}"
    return sorted({**previos, **dict(nuevos)}.items()), None


def serie_en_disco(destino) -> list:
    if not destino.is_file():
        return []
    out = []
    for linea in destino.read_text(encoding="utf-8").splitlines():
        if linea.startswith("#") or linea.startswith("periodo") or not linea.strip():
            continue
        per, val = linea.split(",")[:2]
        out.append((per, float(val)))
    return out


def leer_ipc_indec(texto: str, desde: str) -> list:
    """Filas `[AAAA-MM-01, valor]` del nivel general nacional del CSV del INDEC.

    El CSV trae todas las regiones y divisiones en la misma tabla, separadas por `;` y con coma
    decimal. Equivocar el filtro da una serie con formato correcto y números de otra región."""
    filas = []
    for r in csv.DictReader(io.StringIO(texto), delimiter=";"):
        if (r.get("Codigo") or "").strip() != "0" or (r.get("Region") or "").strip() != "Nacional":
            continue
        periodo = (r.get("Periodo") or "").strip()
        if not re.fullmatch(r"\d{6}", periodo):
            continue
        per = f"{periodo[:4]}-{periodo[4:]}"
        if per >= desde:
            filas.append([f"{per}-01", (r.get("Indice_IPC") or "").replace(",", ".")])
    return sorted(filas)


def pedir_indec(cfg: dict, desde: str, timeout: int = 180, reintentos: int = 3,
                verboso: bool = False) -> list:
    crudo, charset, _ = bajar(IPC_INDEC, timeout=timeout, reintentos=reintentos,
                              verboso=verboso)
    return leer_ipc_indec(decodificar(crudo, charset), desde)


def url_de_fuente(cfg: dict, desde: str) -> str:
    if cfg.get("api") == "indec":
        return IPC_INDEC
    if cfg.get("api") == "bcra":
        return f"{API_BCRA}{cfg['id']}?desde={desde}-01"
    return f"{API}?ids={cfg['id']}&format=csv&start_date={desde}"


def periodos_en_disco(destino) -> int | None:
    """Cuántos períodos tiene el CSV que ya está, o None si no está.

    Sirve para no reescribir una serie con menos datos de los que había. Cuenta las filas que no
    son comentario ni encabezado, que es lo mismo que hace `intereses.py` al leerlas.
    """
    if not destino.is_file():
        return None
    cuenta = 0
    for linea in destino.read_text(encoding="utf-8").splitlines():
        if linea.startswith("#") or linea.startswith("periodo") or not linea.strip():
            continue
        cuenta += 1
    return cuenta


def continuidad(datos: list[tuple[str, float]]) -> str | None:
    """El problema de continuidad de una serie mensual, o None. Vale para las tres.

    Un período repetido o un mes faltante no rompen nada visible: el CSV queda bien formado y
    `intereses.py` sigue calculando. Lo que cambia es el resultado, porque actualiza entre dos
    períodos y toma lo que encuentra. Es la clase de defecto que no se ve leyendo el archivo.

    No se controla que la serie sea creciente, aunque las tres lo sean hoy: un índice puede
    quedar plano o bajar, y una medida que se equivoca sobre un caso legítimo se descarta en vez
    de calibrarse.
    """
    periodos = [p for p, _ in datos]
    repetidos = sorted({p for p in periodos if periodos.count(p) > 1})
    if repetidos:
        return f"períodos repetidos: {', '.join(repetidos[:5])}"
    for a, b in zip(periodos, periodos[1:]):
        meses = (int(b[:4]) * 12 + int(b[5:7])) - (int(a[:4]) * 12 + int(a[5:7]))
        if meses != 1:
            return f"falta al menos un mes entre {a} y {b}"
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--serie", action="append", default=[], choices=list(SERIES))
    p.add_argument("--desde", default=None, help="Período inicial, YYYY-MM")
    p.add_argument("--forzar", action="store_true",
                   help="Escribe el archivo aunque la descarga traiga menos períodos que el "
                        "que ya está")
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
            traer = {"bcra": pedir_bcra, "indec": pedir_indec}.get(cfg.get("api"), pedir)
            filas = traer(cfg, desde, a.timeout, a.reintentos, a.verboso)
        except Exception as e:
            print(f"  ERROR   {nombre:6} {type(e).__name__}: {e}")
            error += 1
            continue
        if not filas and not cfg.get("complemento"):
            print(f"  ERROR   {nombre:6} la API no devolvió datos")
            error += 1
            continue

        datos, descartadas = [], 0
        for f in filas:
            try:
                datos.append((f[0][:7], float(f[1])))
            except (IndexError, ValueError):
                descartadas += 1
        datos.sort()

        complemento = None
        if cfg.get("complemento") == "ripte":
            destino = DATOS / f"serie-{nombre}.csv"
            try:
                crudo, charset, _ = bajar(RIPTE_PAGINA, timeout=a.timeout,
                                          reintentos=a.reintentos, verboso=a.verboso)
                nuevos = leer_tabla_ripte(decodificar(crudo, charset))
            except Exception as e:
                nuevos = []
                print(f"  AVISO   {nombre:6} no se pudo leer la página oficial: "
                      f"{type(e).__name__}: {e}")
            base = datos or serie_en_disco(destino)
            if nuevos and base and nuevos[-1][0] > base[-1][0]:
                unidos, motivo = completar(base, nuevos)
                if unidos is None:
                    print(f"  ERROR   {nombre:6} no se completa con la página oficial: {motivo}. "
                          f"NO se escribió el archivo.")
                    error += 1
                    continue
                datos, complemento = unidos, RIPTE_PAGINA
                if not filas:
                    print(f"  AVISO   {nombre:6} la API no devolvió datos: se completa la serie del "
                          f"archivo con la página oficial")
            elif not filas:
                print(f"  ERROR   {nombre:6} la API no devolvió datos y la página oficial no trae "
                      f"meses nuevos")
                error += 1
                continue

        # Descartar en silencio es lo que hace que un cambio de formato de la API parezca una
        # serie más corta. Se dice cuántas, y si no quedó ninguna se corta acá: sin esto la
        # primera serie con formato nuevo moría en un IndexError al armar el encabezado.
        if descartadas:
            print(f"  AVISO   {nombre:6} {descartadas} filas sin período o sin valor: "
                  f"descartadas")
        if not datos:
            print(f"  ERROR   {nombre:6} ninguna fila tenía período y valor legibles: la API "
                  f"cambió de formato o el serie_id no es una serie")
            error += 1
            continue

        if cfg["control"]:
            per, val = cfg["control"]
            hallado = dict(datos).get(per)
            if hallado is None or abs(hallado - val) > 0.001:
                print(f"  ERROR   {nombre:6} el ancla no coincide: se esperaba {per} = {val} y "
                      f"llegó {hallado}. NO se escribió el archivo.")
                print(f"            Si se pidió --desde posterior a {per}, el ancla queda fuera "
                      f"del rango y este control no puede correr: bajar la serie entera.")
                print("            Si no, revisar el serie_id: hay ids que difieren en un "
                      "carácter y devuelven otra medición.")
                error += 1
                continue

        roto = continuidad(datos)
        if roto:
            print(f"  ERROR   {nombre:6} la serie no es continua: {roto}. NO se escribió el "
                  f"archivo.")
            print("            Un mes faltante le cambia el resultado a intereses.py sin que "
                  "se vea. Revisar\n            en la fuente antes de aceptarlo.")
            error += 1
            continue

        destino = DATOS / f"serie-{nombre}.csv"
        # Bajar una serie no puede PERDER períodos sin decirlo. Con `--desde` posterior al de la
        # entrada, el archivo se reescribía con menos datos y nada avisaba: acá no hay historial
        # de git al que volver, así que lo que se borra se borra.
        tenia = periodos_en_disco(destino)
        if tenia is not None and len(datos) < tenia and not a.forzar:
            print(f"  ERROR   {nombre:6} la descarga trae {len(datos)} períodos y el archivo "
                  f"tiene {tenia}: NO se sobreescribe.")
            print("            Si la intención es acortar la serie, repetir con --forzar.")
            error += 1
            continue
        with destino.open("w", encoding="utf-8", newline="") as fh:
            fh.write(f"# {cfg['titulo']}\n")
            fh.write(f"# Organismo: {cfg['organismo']} - frecuencia: {cfg['frecuencia']}\n")
            fh.write(f"# serie_id: {cfg['id']}\n")
            fh.write(f"# Fuente: {url_de_fuente(cfg, desde)}\n")
            if complemento:
                fh.write(f"# Complemento: {complemento} (meses posteriores al último de la API,\n"
                         f"#   aceptados porque los meses comunes coinciden al centavo)\n")
            fh.write(f"# Descargado: {hoy()}"
                     f"  ({len(datos)} períodos, {datos[0][0]} a {datos[-1][0]})\n")
            # Se envuelve por ancho, NO se parte por oraciones. Partir en ". " se come las
            # abreviaturas del castellano jurídico: la nota del RIPTE salía cortada en "usa el
            # art." / "12 LRT texto Ley 27.348", que es una cita quebrada dentro de un archivo
            # de datos que alguien va a leer para saber qué serie tiene.
            for linea in textwrap.wrap(cfg["nota"], width=94):
                fh.write(f"# {linea}\n")
            fh.write("periodo,indice\n")
            for per, val in datos:
                fh.write(f"{per},{val}\n")
        print(f"  OK      {nombre:6} {len(datos):>5} períodos  {datos[0][0]} a {datos[-1][0]}"
              f"  -> {destino.name}")

    print(f"\n  {len(nombres) - error} series actualizadas, {error} con error.")
    print("  Las consume scripts/intereses.py de la skill. Volver a correr este script "
          "antes de\n  liquidar con un período posterior al último descargado.")
    return 1 if error else 0


if __name__ == "__main__":
    sys.exit(main())
