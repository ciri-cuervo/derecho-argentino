#!/usr/bin/env python3
"""Diagnóstico del plugin: dónde está el repo, cómo está el perfil y qué tan vieja es la data.

    python3 estado.py            # informe legible
    python3 estado.py --json     # para consumo programático

Códigos de salida: 0 todo al día · 1 hay algo vencido o faltante · 2 no se encontró el repo.

POR QUÉ EXISTE
--------------
Una base de conocimiento jurídico **se pudre en silencio**: nada avisa que una ley cambió ni
que el valor del jus quedó dos meses atrás. Los scripts se niegan a inventar y emiten el
marcador, así que el sistema no miente -- pero el usuario se entera tarde y en medio de una
consulta. Esto lo adelanta: dice que está vencido, hace cuánto y con qué comando se arregla.

Todos los chequeos son **locales**: no toca la red. Para preguntarle a las fuentes oficiales
si una norma cambió hay que correr `fuentes/scripts/verificar_normas.py`, que si sale a
internet y tarda.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import perfil as _perfil
from _raiz import ENV, ENV_PLUGIN, archivo_config, base, raiz_repo

# Cada cuántos días se considera vencido cada bloque. La volatilidad manda: el valor del jus
# cambia todos los meses y las acordadas de feria una vez al año.
UMBRALES = {"normas": 90, "jus": 45, "uma": 45, "inhabiles": 300}
# Por serie, porque no se publican con el mismo rezago: el RIPTE sale con unos dos meses de
# demora, así que medirlo con la vara del IPC lo marca vencido cuando está al día.
#
# Y ninguna baja de 60, porque las tres son MENSUALES y el período se ancla al día 1. Con eso,
# la serie más fresca posible ya tiene 31 días el primero del mes siguiente y 46 el día 16: el
# CER estaba en 45 y se ponía en rojo todos los meses pasado el 15, con la serie completa hasta
# el último mes cerrado y sin nada que bajar. Medido contra la API: no había período nuevo. Una
# alarma que suena por el calendario y no por el dato es de las que se dejan de mirar. El piso
# tiene que decir «se saltó un mes», y para eso hace falta pasar de 62 MÁS el rezago
# con que publica cada organismo: el BCRA cierra el CER con el mes, el INDEC saca el
# IPC cerca del 13 del mes siguiente, y el RIPTE llega con unos dos meses.
UMBRAL_SERIE = {"IPC": 80, "CER": 70, "RIPTE": 120}


def _hoy():
    return _perfil.hoy()


def _dias(iso):
    try:
        return (_hoy() - date.fromisoformat(str(iso)[:10])).days
    except (ValueError, TypeError):
        return None


def _verificado_csv(f: Path):
    """Días desde la línea `# verificado: AAAA-MM-DD` del encabezado, o None si no está.

    Su forma es contrato: si alguien reescribe el comentario a mano y le cambia el prefijo,
    esto devuelve None y el bloque sale REVISAR en vez de volver en silencio a la alarma
    falsa. Lo exige `TestElJusMideLaMiradaYNoElValor`.
    """
    try:
        for linea in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not linea.startswith("#"):
                break
            hallado = re.match(r"#\s*verificado:\s*(\d{4}-\d{2}-\d{2})\s*$", linea)
            if hallado:
                return _dias(hallado.group(1))
    except OSError:
        pass
    return None


def _ultima_fila_csv(f: Path):
    """Primer campo de la última fila de datos de un csv con comentarios '#', y cuántas hay.

    La primera fila útil no es un dato sino el encabezado, y contarla informaba un período
    de más en cada serie: 118 donde hay 117. Un archivo con encabezado y sin datos cuenta
    como vacío, porque devolver "período" como último valor no ayuda a nadie.
    """
    try:
        filas = [l.strip() for l in f.read_text(encoding="utf-8", errors="replace").splitlines()
                 if l.strip() and not l.lstrip().startswith("#")]
    except OSError:
        return None, 0
    datos = filas[1:]
    if not datos:
        return None, 0
    return datos[-1].split(",")[0], len(datos)


def _periodo_a_fecha(p):
    """'2026-08' o '2026-08-01' -> date. Los períodos mensuales se anclan al día 1."""
    if not p:
        return None
    try:
        partes = str(p).split("-")
        return date(int(partes[0]), int(partes[1]), int(partes[2]) if len(partes) > 2 else 1)
    except (ValueError, IndexError):
        return None


def revisar(raiz: Path) -> list[dict]:
    """Un dict por bloque de datos: nombre, estado, detalle, días, arreglo."""
    F = base(raiz) / "fuentes"
    D = F / "datos"
    out = []

    def add(nombre, estado, detalle, dias=None, arreglo=None):
        out.append({"bloque": nombre, "estado": estado, "detalle": detalle,
                    "dias": dias, "arreglo": arreglo})

    # -- normas: cuándo se le preguntó a la fuente oficial si el texto cambió. La fecha la
    # sella `verificar_normas.py --sellar`, y sólo después de haber comparado de verdad.
    ruta = F / "normas" / "normas.json"
    try:
        m = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        add("normas", "FALTA", f"no se pudo leer {ruta.name}",
            arreglo="revisar la instalación del plugin")
    else:
        total = len(m.get("normas", []))
        d = _dias(m.get("verificado"))
        if d is None:
            add("normas", "REVISAR", f"{total} en el manifiesto, sin fecha de verificación",
                arreglo="/derecho:verificar")
        else:
            venc = d > UMBRALES["normas"]
            add("normas", "VENCIDO" if venc else "OK",
                f"{total} en el manifiesto, verificados hace {d} días",
                d, "/derecho:verificar" if venc else None)

    # -- fallos: acá NO va una fecha de verificación, y es lo que arregla este bloque.
    #
    # Una sentencia firme no cambia, así que la pregunta de las normas -"¿sigue vigente el
    # texto?"- no tiene con qué contestarse acá. Lo que sí se puede perder es otra cosa: que
    # el archivo sea OTRO documento, o que alguien lo haya tocado. Las dos se miden, y sin
    # fecha: el cotejo de identidad contra la carátula lo escribe el descargador en cada
    # bajada, y el hash lo controla la suite en cada corrida.
    #
    # Antes había un `verificado` en `fallos.json` que NINGÚN script escribía ni renovaba
    # -- `verificar_normas.py` lo excluye a propósito porque la jurisprudencia no tiene
    # verificador -- y esto lo mostraba como `[ok] fallos ... verificados hace N días`. Una
    # fecha tipeada a mano que envejece sola y se lee como una medición es peor que no tener
    # ninguna: es la alarma que no suena nunca.
    try:
        mj = json.loads((F / "jurisprudencia" / "fallos.json").read_text(encoding="utf-8"))
        pj = json.loads((F / "jurisprudencia" / "procedencia.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        add("fallos", "FALTA", "no se pudo leer fallos.json o su procedencia",
            arreglo="revisar la instalación del plugin")
    else:
        regj = pj.get("fallos", {})
        censo = {"cotejado": 0, "no aplica": 0, "revisar": 0, "sin cotejo": 0}
        for f in mj.get("fallos", []):
            estado = str(regj.get(f["slug"], {}).get("cotejo", "")).split(":")[0].strip()
            censo[estado if estado in censo else "sin cotejo"] += 1
        total = sum(censo.values())
        pendiente = censo["revisar"] + censo["sin cotejo"]
        add("fallos", "REVISAR" if pendiente else "OK",
            f"{total} en el manifiesto; identidad: {censo['cotejado']} cotejados, "
            f"{censo['no aplica']} sin apellido que cotejar, {censo['revisar']} a revisar"
            + (f", {censo['sin cotejo']} sin cotejar" if censo["sin cotejo"] else ""),
            arreglo="/derecho:actualizar" if pendiente else None)

    # -- descargas efectivas contra el manifiesto
    try:
        proc = json.loads((F / "normas" / "procedencia.json").read_text(encoding="utf-8"))
        m = json.loads((F / "normas" / "normas.json").read_text(encoding="utf-8"))
        reg = proc.get("normas", proc)          # el manifiesto anida bajo "normas"
        # Contar la INTERSECCIÓN, no dos totales. Restar el tamaño de procedencia al de
        # normas con URL da cualquier cosa apenas hay una entrada registrada sin URL -una
        # norma aportada a mano, por ejemplo-: cada una de esas tapa una que falta bajar.
        con_url = [n["slug"] for n in m.get("normas", []) if n.get("url")]
        declaradas = len(con_url)
        pendientes = [s for s in con_url
                      if s not in reg or not (F / "normas" / reg[s].get("archivo", "")).exists()]
        bajadas = declaradas - len(pendientes)
        faltan = len(pendientes)
        add("descargas", "REVISAR" if faltan > 0 else "OK",
            f"{bajadas} de {declaradas} normas con URL están descargadas"
            + (f"; faltan {faltan}" if faltan > 0 else ""),
            arreglo="/derecho:actualizar" if faltan > 0 else None)
    except (OSError, ValueError):
        add("descargas", "FALTA", "no se pudo leer procedencia.json",
            arreglo="/derecho:actualizar")

    # -- lo mismo para jurisprudencia. Faltaba: un fallo declarado en el manifiesto con su URL
    # pero sin PDF bajado no lo reportaba nadie, porque el bloque "fallos" de más arriba solo
    # mira la fecha de verificación del manifiesto, no si los archivos están.
    try:
        procj = json.loads((F / "jurisprudencia" / "procedencia.json").read_text(encoding="utf-8"))
        mj = json.loads((F / "jurisprudencia" / "fallos.json").read_text(encoding="utf-8"))
        regj = procj.get("fallos", procj)
        con_url_j = [f["slug"] for f in mj.get("fallos", []) if f.get("url")]
        pend_j = [s for s in con_url_j
                  if s not in regj
                  or not (F / "jurisprudencia" / regj[s].get("archivo", f"{s}.pdf")).exists()]
        add("sentencias", "REVISAR" if pend_j else "OK",
            f"{len(con_url_j) - len(pend_j)} de {len(con_url_j)} fallos con URL están descargados"
            + (f"; faltan {len(pend_j)}" if pend_j else ""),
            arreglo="/derecho:actualizar" if pend_j else None)
    except (OSError, ValueError):
        add("sentencias", "FALTA", "no se pudo leer jurisprudencia/procedencia.json",
            arreglo="/derecho:actualizar")

    # -- valor del jus
    #
    # Lo que vence acá NO es el valor, es la mirada. La SCBA publica con rezago de semanas,
    # así que medir la antigüedad del último período pone el bloque en rojo todos los meses
    # con el dato completo y nada que cargar, y encima el arreglo que sugería -"cargar el jus
    # del mes"- era consejo falso. Se mide la fecha en que alguien abrió la tabla oficial,
    # igual que las normas miden su `verificado` y no la antigüedad de las leyes.
    ruta_jus = D / "jus-scba.csv"
    ult, filas = _ultima_fila_csv(ruta_jus)
    f = _periodo_a_fecha(ult)
    if f is None:
        add("jus", "FALTA", "jus-scba.csv vacío o ilegible", arreglo="/derecho:actualizar")
    else:
        dv = _verificado_csv(ruta_jus)
        d = (_hoy() - f).days
        if dv is None:
            add("jus", "REVISAR",
                f"último valor: {ult} ({filas} filas), sin línea `# verificado:`", d,
                "mirar la tabla oficial y anotar `# verificado: AAAA-MM-DD` en jus-scba.csv")
        elif dv > UMBRALES["jus"]:
            add("jus", "VENCIDO",
                f"último valor: {ult} ({filas} filas); nadie mira la tabla hace {dv} días", dv,
                "abrir scba.gov.ar/paginas.asp?id=41320 y actualizar `# verificado:`")
        else:
            add("jus", "OK",
                f"último valor: {ult} ({filas} filas, {d} días); "
                f"la tabla oficial no publica posterior, mirada hace {dv} días", dv)

    # -- valor de la UMA
    #
    # Mide la mirada y no el valor, igual que el jus. La diferencia es que acá el archivo nace
    # vacío: no hay descargador porque la consulta oficial de la CSJN es un formulario y no una
    # tabla, así que los valores se cargan a mano. Ese vacío se reporta FALTA y no OK -el
    # vocabulario de estados es cerrado y FALTA es el que ya usa el jus para un csv sin datos-,
    # porque un verde por ausencia de dato es verde con el instrumento apagado.
    ruta_uma = D / "uma-csjn.csv"
    ult, filas = _ultima_fila_csv(ruta_uma)
    f = _periodo_a_fecha(ult)
    if not ruta_uma.is_file():
        add("UMA", "FALTA", "uma-csjn.csv no existe", arreglo="revisar la instalación")
    elif f is None:
        add("UMA", "FALTA",
            "uma-csjn.csv está sin valores: la justicia nacional y federal no se regula",
            arreglo="abrir csjn.gov.ar/transparencia/uma, cargar los valores y sellar "
                    "`# verificado:`")
    else:
        dv = _verificado_csv(ruta_uma)
        d = (_hoy() - f).days
        if dv is None:
            add("UMA", "REVISAR",
                f"último valor: {ult} ({filas} filas), sin línea `# verificado:`", d,
                "mirar la consulta oficial y anotar `# verificado: AAAA-MM-DD` en uma-csjn.csv")
        elif dv > UMBRALES["uma"]:
            add("UMA", "VENCIDO",
                f"último valor: {ult} ({filas} filas); nadie mira la consulta hace {dv} días",
                dv, "abrir csjn.gov.ar/transparencia/uma y actualizar `# verificado:`")
        else:
            add("UMA", "OK",
                f"último valor: {ult} ({filas} filas, {d} días); mirada hace {dv} días", dv)

    # -- valor de la UMA de la CIUDAD
    #
    # Bloque aparte y no una fila más del de arriba: son dos unidades de dos leyes distintas, y
    # confundirlas devuelve un número oficial, vigente y de otra ley. El diagnóstico las separa
    # por la misma razón por la que las separan los scripts.
    #
    # Y hay una diferencia que cambia lo que significa "al día": la consulta oficial del Consejo
    # publica UN SOLO valor, el vigente, y se sobreescribe. Acá la mirada es lo único que se
    # puede medir -no hay serie contra la cual comparar- y por eso el umbral es el mismo que el
    # de la UMA nacional pero el detalle no promete completitud.
    ruta_caba = D / "uma-caba.csv"
    ult, filas = _ultima_fila_csv(ruta_caba)
    f = _periodo_a_fecha(ult)
    if not ruta_caba.is_file():
        add("UMA CABA", "FALTA", "uma-caba.csv no existe", arreglo="revisar la instalación")
    elif f is None:
        add("UMA CABA", "FALTA",
            "uma-caba.csv está sin valores: los mínimos en UMA de la Ley 5.134 no se contrastan",
            arreglo="abrir consejo.jusbaires.gob.ar/servicios/uma, cargar el valor y sellar "
                    "`# verificado:`")
    else:
        dv = _verificado_csv(ruta_caba)
        d = (_hoy() - f).days
        if dv is None:
            add("UMA CABA", "REVISAR",
                f"último valor: {ult} ({filas} filas), sin línea `# verificado:`", d,
                "mirar la consulta oficial y anotar `# verificado: AAAA-MM-DD` en uma-caba.csv")
        elif dv > UMBRALES["uma"]:
            add("UMA CABA", "VENCIDO",
                f"último valor: {ult} ({filas} filas); nadie mira la consulta hace {dv} días",
                dv, "abrir consejo.jusbaires.gob.ar/servicios/uma y actualizar `# verificado:`")
        else:
            add("UMA CABA", "OK",
                f"último valor: {ult} ({filas} filas, {d} días); mirada hace {dv} días", dv)

    # -- series de índices
    for nombre, arch in (("IPC", "serie-ipc.csv"), ("RIPTE", "serie-ripte.csv"),
                         ("CER", "serie-cer.csv")):
        ult, filas = _ultima_fila_csv(D / arch)
        f = _periodo_a_fecha(ult)
        if f is None:
            add(f"serie {nombre}", "FALTA", f"{arch} vacío o ilegible",
                arreglo="/derecho:actualizar")
            continue
        d = (_hoy() - f).days
        venc = d > UMBRAL_SERIE.get(nombre, 60)
        add(f"serie {nombre}", "VENCIDO" if venc else "OK",
            f"último período: {ult} ({filas} períodos)", d,
            "/derecho:actualizar" if venc else None)

    # -- calendario de inhábiles: tiene que cubrir este año y el que viene
    try:
        inh = json.loads((D / "inhabiles.json").read_text(encoding="utf-8"))
        anios = sorted(inh.get("anios", {}))
        need = {str(_hoy().year), str(_hoy().year + 1)}
        faltan = sorted(need - set(anios))
        add("inhabiles", "VENCIDO" if faltan else "OK",
            f"años cargados: {', '.join(anios) or 'ninguno'}"
            + (f"; falta cargar {', '.join(faltan)}" if faltan else ""),
            arreglo=("cargar las acordadas de feria en fuentes/datos/inhabiles.json"
                     if faltan else None))
    except (OSError, ValueError):
        add("inhabiles", "FALTA", "no se pudo leer inhábiles.json",
            arreglo="revisar la instalación del plugin")
    return out


def version_plugin(raiz: Path):
    try:
        return json.loads((base(raiz) / ".claude-plugin" / "plugin.json")
                          .read_text(encoding="utf-8")).get("version")
    except (OSError, ValueError):
        return None


def arreglo_plugin(origen: str, propia: str) -> str:
    """El remedio depende de por dónde se resolvió la raíz: reinstalar no borra un config ni
    desarma una variable, y mandar a hacerlo deja el problema donde estaba."""
    if origen.startswith("config"):
        return (f"correr configurar.py --repo con la ruta que corresponde, o borrar "
                f"{archivo_config()}")
    if origen.startswith(f"variable {ENV}"):
        return f"apuntar {ENV} a la carpeta del plugin de la {propia}, o sacarla del entorno"
    return f"reinstalar el plugin: la carpeta de la {propia} no es la que se está leyendo"


def bloque_plugin(raiz: Path, version_datos, origen: str):
    """Compara la versión de los datos con la de los scripts que están corriendo.

    Al actualizar, la versión anterior puede quedar al lado de la nueva: si la raíz se resolvió
    en esa, los scripts nuevos leen datos viejos y nada más lo delata.
    """
    propia = version_plugin(Path(__file__).resolve().parents[3])
    if propia is None:
        return None
    if propia == version_datos:
        return {"bloque": "plugin", "estado": "OK", "detalle": f"scripts y datos de la {propia}",
                "dias": None, "arreglo": None}
    return {"bloque": "plugin", "estado": "REVISAR",
            "detalle": f"los scripts son de la {propia} y los datos de "
                       f"{base(raiz)} son de la {version_datos or '(sin declarar)'}",
            "dias": None,
            "arreglo": arreglo_plugin(origen, propia)}


def recolectar():
    raiz, origen = raiz_repo()
    version = version_plugin(raiz) if raiz else None
    bloques = revisar(raiz) if raiz else []
    if raiz and (b := bloque_plugin(raiz, version, origen)):
        bloques.insert(0, b)
    inf = {"fecha": _hoy().isoformat(), "repo": str(raiz) if raiz else None, "origen": origen,
           "config": str(archivo_config()), "perfil": _perfil.leer(),
           "version": version, "bloques": bloques}
    estados = {b["estado"] for b in inf["bloques"]}
    inf["salida"] = 2 if raiz is None else (1 if estados & {"VENCIDO", "FALTA", "REVISAR"} else 0)
    return inf


def imprimir(inf):
    print(f"\n  ESTADO DEL PLUGIN derecho-argentino    {inf['fecha']}")
    print("  " + "-" * 66)
    if not inf["repo"]:
        print("\n  Repo: NO ENCONTRADO\n")
        print("  Sin el repo no hay datos, y sin datos las calculadoras no calculan:")
        print("  emiten el marcador y cortan, que es lo correcto pero no resuelve.\n")
        print("    python3 configurar.py --repo /ruta/al/repo")
        print(f"    export {ENV}=/ruta/al/repo")
        # ENV_PLUGIN es una tupla: interpolarla directo imprimiría el repr de Python en la
        # cara del usuario, y justo en la salida que lee cuando NO encontró el repo.
        print(f"    (instalado como plugin, {' o '.join(ENV_PLUGIN)} lo resuelve solo)")
        return
    print(f"\n  Repo      {inf['repo']}")
    print(f"  Por       {inf['origen']}")
    print(f"  Versión   {inf['version'] or '(sin declarar)'}")
    print(f"\n{_perfil.describir(inf['perfil'])}")
    print("\n  Datos:")
    orden = {"FALTA": 0, "VENCIDO": 1, "REVISAR": 2, "OK": 3}
    for b in sorted(inf["bloques"], key=lambda x: (orden.get(x["estado"], 9), x["bloque"])):
        marca = {"OK": "  ok  ", "VENCIDO": " VENC ", "REVISAR": " REV  ", "FALTA": " FALTA"}
        print(f"   [{marca.get(b['estado'], '  ?   ')}] {b['bloque']:14} {b['detalle']}")
    arreglos = []
    for b in inf["bloques"]:
        if b["arreglo"] and b["arreglo"] not in arreglos:
            arreglos.append(b["arreglo"])
    if arreglos:
        print("\n  Para ponerlo al día:")
        for a in arreglos:
            print(f"    {a}")
    else:
        print("\n  Todo al día. Igual, la única forma de saber si una norma cambió en la")
        print("  fuente oficial es preguntarle: /derecho:verificar")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    inf = recolectar()
    if a.json:
        print(json.dumps(inf, ensure_ascii=False, indent=2))
    else:
        imprimir(inf)
    raise SystemExit(inf["salida"])


if __name__ == "__main__":
    main()
