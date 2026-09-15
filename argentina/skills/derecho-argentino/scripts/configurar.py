#!/usr/bin/env python3
"""Deja configurada, una sola vez por maquina, la ruta al repo de conocimiento juridico.

    python3 configurar.py --repo ~/develop/derecho-argentino
    python3 configurar.py                 # busca solo y muestra que encontro
    python3 configurar.py --mostrar       # solo informa, no escribe

La skill se instala a nivel de cuenta y corre en cualquier maquina; el repo puede estar en
cualquier ruta. Esto lo resuelve sin que ninguna ruta quede escrita en la skill.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from _raiz import (ENV, MARCADOR, archivo_config, base, es_repo, guardar_raiz,
                   resolver)


def estado(p: Path):
    B = base(p)
    d = B / "fuentes" / "datos"
    piezas = {
        "valor del jus": d / "jus-scba.csv",
        "inhabiles": d / "inhabiles.json",
        "serie IPC": d / "serie-ipc.csv",
        "serie RIPTE": d / "serie-ripte.csv",
        "serie CER": d / "serie-cer.csv",
        "normas": B / "fuentes" / "normas",
        "jurisprudencia": B / "fuentes" / "jurisprudencia",
    }
    print("\n  Contenido:")
    for nombre, f in piezas.items():
        if f.is_dir():
            n = len(list(f.glob("*.txt"))) + len(list(f.glob("*.pdf")))
            print(f"    {nombre:16} {n} archivos")
        elif f.is_file():
            filas = sum(1 for l in f.read_text(encoding='utf-8', errors='replace').splitlines()
                        if l.strip() and not l.lstrip().startswith("#"))
            print(f"    {nombre:16} {'cargado' if filas > 1 else 'VACIO'} ({filas} filas)")
        else:
            print(f"    {nombre:16} FALTA")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", default=None, help="Ruta a la raiz del repo")
    p.add_argument("--mostrar", action="store_true", help="Informa sin escribir configuracion")
    a = p.parse_args()

    if a.repo and not a.mostrar:
        ruta = Path(a.repo).expanduser()
        if not es_repo(ruta):
            raise SystemExit(
                f"  {ruta} no parece el repo: falta {MARCADOR}\n"
                f"  Indicar la RAIZ del repo, no una subcarpeta.")
        destino = guardar_raiz(ruta)
        print(f"  Configurado: {ruta.resolve()}")
        print(f"  Guardado en: {destino}")
        estado(ruta.resolve())
        print("\n  Los scripts de la skill ya lo van a encontrar solos en esta maquina.")
        return

    encontrado, origen = resolver(a.repo, fijar=not a.mostrar, avisar=False)
    if encontrado:
        print(f"  Repo encontrado: {encontrado}")
        print(f"  Por: {origen}")
        estado(encontrado)
        if origen.endswith("(queda fijada)"):
            print(f"\n  Se dejo anotado en {archivo_config()}: los proximos usos lo toman "
                  f"de ahi.")
        elif a.mostrar and origen.startswith(("ubicacion habitual", "la skill")):
            print("\n  Todavia no esta escrito en la configuracion (--mostrar no escribe).")
    else:
        print("  No se encontro el repo en esta maquina.")
        print(f"  Config esperada en: {archivo_config()}")
        print(f"  Variable de entorno alternativa: {ENV}")
        print("\n  Para configurarlo:")
        print("    python3 configurar.py --repo /ruta/al/repo")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
