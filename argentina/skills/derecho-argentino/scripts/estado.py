#!/usr/bin/env python3
"""Diagnostico del plugin: donde esta el repo, como esta el perfil y que tan vieja es la data.

    python3 estado.py            # informe legible
    python3 estado.py --json     # para consumo programatico

Codigos de salida: 0 todo al dia · 1 hay algo vencido o faltante · 2 no se encontro el repo.

POR QUE EXISTE
--------------
Una base de conocimiento juridico **se pudre en silencio**: nada avisa que una ley cambio ni
que el valor del jus quedo dos meses atras. Los scripts se niegan a inventar y emiten el
marcador, asi que el sistema no miente -- pero el usuario se entera tarde y en medio de una
consulta. Esto lo adelanta: dice que esta vencido, hace cuanto y con que comando se arregla.

Todos los chequeos son **locales**: no toca la red. Para preguntarle a las fuentes oficiales
si una norma cambio hay que correr `fuentes/scripts/verificar_normas.py`, que si sale a
internet y tarda.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path

import perfil as _perfil
from _raiz import ENV, ENV_PLUGIN, archivo_config, base, raiz_repo

# Cada cuantos dias se considera vencido cada bloque. La volatilidad manda: el valor del jus
# cambia todos los meses y las acordadas de feria una vez al anio.
UMBRALES = {"normas": 90, "fallos": 180, "jus": 45, "inhabiles": 300}
# Por serie, porque no se publican con el mismo rezago: el RIPTE sale con unos dos meses de
# demora, asi que medirlo con la vara del IPC lo marca vencido cuando esta al dia.
UMBRAL_SERIE = {"IPC": 60, "CER": 45, "RIPTE": 120}


def _hoy():
    return date.today()


def _dias(iso):
    try:
        return (_hoy() - date.fromisoformat(str(iso)[:10])).days
    except (ValueError, TypeError):
        return None


def _ultima_fila_csv(f: Path):
    """Primer campo de la ultima fila de datos de un csv con comentarios '#', y cuantas hay.

    La primera fila util no es un dato sino el encabezado, y contarla informaba un periodo
    de mas en cada serie: 118 donde hay 117. Un archivo con encabezado y sin datos cuenta
    como vacio, porque devolver "periodo" como ultimo valor no ayuda a nadie.
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
    """'2026-08' o '2026-08-01' -> date. Los periodos mensuales se anclan al dia 1."""
    if not p:
        return None
    try:
        partes = str(p).split("-")
        return date(int(partes[0]), int(partes[1]), int(partes[2]) if len(partes) > 2 else 1)
    except (ValueError, IndexError):
        return None


def revisar(raiz: Path) -> list[dict]:
    """Un dict por bloque de datos: nombre, estado, detalle, dias, arreglo."""
    F = base(raiz) / "fuentes"
    D = F / "datos"
    out = []

    def add(nombre, estado, detalle, dias=None, arreglo=None):
        out.append({"bloque": nombre, "estado": estado, "detalle": detalle,
                    "dias": dias, "arreglo": arreglo})

    # -- manifiestos: cuando se verifico por ultima vez contra fuente primaria
    for nombre, ruta, clave in (("normas", F / "normas" / "normas.json", "normas"),
                                ("fallos", F / "jurisprudencia" / "fallos.json", "fallos")):
        try:
            m = json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            add(nombre, "FALTA", f"no se pudo leer {ruta.name}",
                arreglo="revisar la instalacion del plugin")
            continue
        total = len(m.get(clave, []))
        d = _dias(m.get("verificado"))
        if d is None:
            add(nombre, "REVISAR", f"{total} en el manifiesto, sin fecha de verificacion",
                arreglo="/derecho:verificar")
        else:
            venc = d > UMBRALES[nombre]
            add(nombre, "VENCIDO" if venc else "OK",
                f"{total} en el manifiesto, verificados hace {d} dias",
                d, "/derecho:verificar" if venc else None)

    # -- descargas efectivas contra el manifiesto
    try:
        proc = json.loads((F / "normas" / "procedencia.json").read_text(encoding="utf-8"))
        m = json.loads((F / "normas" / "normas.json").read_text(encoding="utf-8"))
        reg = proc.get("normas", proc)          # el manifiesto anida bajo "normas"
        # Contar la INTERSECCION, no dos totales. Restar el tamanio de procedencia al de
        # normas con URL da cualquier cosa apenas hay una entrada registrada sin URL -una
        # norma aportada a mano, por ejemplo-: cada una de esas tapa una que falta bajar.
        con_url = [n["slug"] for n in m.get("normas", []) if n.get("url")]
        declaradas = len(con_url)
        pendientes = [s for s in con_url
                      if s not in reg or not (F / "normas" / reg[s].get("archivo", "")).exists()]
        bajadas = declaradas - len(pendientes)
        faltan = len(pendientes)
        add("descargas", "REVISAR" if faltan > 0 else "OK",
            f"{bajadas} de {declaradas} normas con URL estan descargadas"
            + (f"; faltan {faltan}" if faltan > 0 else ""),
            arreglo="/derecho:actualizar" if faltan > 0 else None)
    except (OSError, ValueError):
        add("descargas", "FALTA", "no se pudo leer procedencia.json",
            arreglo="/derecho:actualizar")

    # -- lo mismo para jurisprudencia. Faltaba: un fallo declarado en el manifiesto con su URL
    # pero sin PDF bajado no lo reportaba nadie, porque el bloque "fallos" de mas arriba solo
    # mira la fecha de verificacion del manifiesto, no si los archivos estan.
    try:
        procj = json.loads((F / "jurisprudencia" / "procedencia.json").read_text(encoding="utf-8"))
        mj = json.loads((F / "jurisprudencia" / "fallos.json").read_text(encoding="utf-8"))
        regj = procj.get("fallos", procj)
        con_url_j = [f["slug"] for f in mj.get("fallos", []) if f.get("url")]
        pend_j = [s for s in con_url_j
                  if s not in regj
                  or not (F / "jurisprudencia" / regj[s].get("archivo", f"{s}.pdf")).exists()]
        add("sentencias", "REVISAR" if pend_j else "OK",
            f"{len(con_url_j) - len(pend_j)} de {len(con_url_j)} fallos con URL estan descargados"
            + (f"; faltan {len(pend_j)}" if pend_j else ""),
            arreglo="/derecho:actualizar" if pend_j else None)
    except (OSError, ValueError):
        add("sentencias", "FALTA", "no se pudo leer jurisprudencia/procedencia.json",
            arreglo="/derecho:actualizar")

    # -- valor del jus: cambia todos los meses
    ult, filas = _ultima_fila_csv(D / "jus-scba.csv")
    f = _periodo_a_fecha(ult)
    if f is None:
        add("jus", "FALTA", "jus-scba.csv vacio o ilegible", arreglo="/derecho:actualizar")
    else:
        d = (_hoy() - f).days
        venc = d > UMBRALES["jus"]
        add("jus", "VENCIDO" if venc else "OK",
            f"ultimo valor: {ult} ({filas} filas, {d} dias)", d,
            "cargar el jus del mes en fuentes/datos/jus-scba.csv" if venc else None)

    # -- series de indices
    for nombre, arch in (("IPC", "serie-ipc.csv"), ("RIPTE", "serie-ripte.csv"),
                         ("CER", "serie-cer.csv")):
        ult, filas = _ultima_fila_csv(D / arch)
        f = _periodo_a_fecha(ult)
        if f is None:
            add(f"serie {nombre}", "FALTA", f"{arch} vacio o ilegible",
                arreglo="/derecho:actualizar")
            continue
        d = (_hoy() - f).days
        venc = d > UMBRAL_SERIE.get(nombre, 60)
        add(f"serie {nombre}", "VENCIDO" if venc else "OK",
            f"ultimo periodo: {ult} ({filas} periodos)", d,
            "/derecho:actualizar" if venc else None)

    # -- calendario de inhabiles: tiene que cubrir este anio y el que viene
    try:
        inh = json.loads((D / "inhabiles.json").read_text(encoding="utf-8"))
        anios = sorted(inh.get("anios", {}))
        need = {str(_hoy().year), str(_hoy().year + 1)}
        faltan = sorted(need - set(anios))
        add("inhabiles", "VENCIDO" if faltan else "OK",
            f"anios cargados: {', '.join(anios) or 'ninguno'}"
            + (f"; falta cargar {', '.join(faltan)}" if faltan else ""),
            arreglo=("cargar las acordadas de feria en fuentes/datos/inhabiles.json"
                     if faltan else None))
    except (OSError, ValueError):
        add("inhabiles", "FALTA", "no se pudo leer inhabiles.json",
            arreglo="revisar la instalacion del plugin")
    return out


def version_plugin(raiz: Path):
    try:
        return json.loads((base(raiz) / ".claude-plugin" / "plugin.json")
                          .read_text(encoding="utf-8")).get("version")
    except (OSError, ValueError):
        return None


def recolectar():
    raiz, origen = raiz_repo()
    inf = {"fecha": _hoy().isoformat(), "repo": str(raiz) if raiz else None, "origen": origen,
           "config": str(archivo_config()), "perfil": _perfil.leer(),
           "version": version_plugin(raiz) if raiz else None,
           "bloques": revisar(raiz) if raiz else []}
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
        print(f"    python3 configurar.py --repo /ruta/al/repo")
        print(f"    export {ENV}=/ruta/al/repo")
        # ENV_PLUGIN es una tupla: interpolarla directo imprimiria el repr de Python en la
        # cara del usuario, y justo en la salida que lee cuando NO encontro el repo.
        print(f"    (instalado como plugin, {' o '.join(ENV_PLUGIN)} lo resuelve solo)")
        return
    print(f"\n  Repo      {inf['repo']}")
    print(f"  Por       {inf['origen']}")
    print(f"  Version   {inf['version'] or '(sin declarar)'}")
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
        print("\n  Para ponerlo al dia:")
        for a in arreglos:
            print(f"    {a}")
    else:
        print("\n  Todo al dia. Igual, la unica forma de saber si una norma cambio en la")
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
