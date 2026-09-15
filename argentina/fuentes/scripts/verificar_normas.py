#!/usr/bin/env python3
"""Controla si alguna de las normas descargadas cambio en la fuente oficial.

Vuelve a pedir cada URL, calcula el hash y lo compara contra `normas/procedencia.json`. No
escribe nada: solo informa. Sirve como alarma de reforma legislativa.

    python3 verificar_normas.py
    python3 verificar_normas.py --prioridad 1

Sale con codigo 1 si alguna norma cambio, de modo que se puede colgar de una tarea
programada o de un workflow. Que el hash cambie no significa siempre que cambio la ley: las
bases oficiales tocan la maquetacion de sus paginas. Lo que el resultado dice es "hay que
mirar esta", no "esta norma se reformo".
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

from _comun import (RAIZ, ATexto, bajar, cargar_manifiesto, cargar_procedencia,
                    decodificar, sha256, sha256_texto)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prioridad", type=int, default=None)
    p.add_argument("--timeout", type=int, default=180,
                   help="Segundos por intento (default 180). Subirlo si el sitio es lento")
    p.add_argument("--reintentos", type=int, default=3)
    p.add_argument("--verboso", action="store_true",
                   help="Muestra tamanio y tiempo de cada intento")
    p.add_argument("--sellar", action="store_true",
                   help="Si nada cambio, actualiza la fecha `verificado` de los manifiestos")
    a = p.parse_args()

    proc = cargar_procedencia()["normas"]
    normas = cargar_manifiesto()
    if a.prioridad:
        normas = [n for n in normas if n.get("prioridad", 9) <= a.prioridad]

    cambiadas, sin_bajar, errores = [], [], []
    for n in normas:
        slug, url = n["slug"], n.get("url")
        if not url:
            continue
        if slug not in proc:
            sin_bajar.append(slug)
            print(f"  SIN BAJAR   {slug}")
            continue
        try:
            crudo, charset, _ = bajar(url, timeout=a.timeout, reintentos=a.reintentos,
                                      verboso=a.verboso)
        except Exception as e:
            errores.append(slug)
            print(f"  ERROR       {slug:28} {type(e).__name__}: {e}")
            continue
        bajada = proc[slug]["descargado"][:10]
        if sha256(crudo) == proc[slug]["sha256"]:
            print(f"  SIN CAMBIOS {slug:28} (bajada el {bajada})")
            continue
        # El hash crudo no coincide. Antes de dar la alarma, comparar el CUERPO: hay bases
        # que reescriben su HTML en cada request -tokens, nonces, hashes de assets- sin que
        # cambie una coma de la norma. Sin este segundo control esas quedan en rojo siempre,
        # que es la forma mas segura de que nadie mire la alarma cuando de verdad suene.
        esperado = proc[slug].get("sha256_texto")
        actual = None
        if esperado and not url.lower().endswith(".pdf"):
            try:
                parser = ATexto()
                parser.feed(decodificar(crudo, charset))
                actual = sha256_texto(parser.texto() + "\n")
            except Exception:
                actual = None
        if esperado and actual == esperado:
            print(f"  SIN CAMBIOS {slug:28} (bajada el {bajada}; la fuente reescribe el HTML)")
        elif esperado is None:
            cambiadas.append(slug)
            print(f"  CAMBIO      {slug:28} REVISAR - cambio el hash crudo y no hay hash de "
                  f"texto para contrastar")
        else:
            cambiadas.append(slug)
            print(f"  CAMBIO      {slug:28} REVISAR - cambio el texto de la norma")

    print(f"\n  {len(cambiadas)} cambiadas, {len(sin_bajar)} sin bajar, {len(errores)} con error.")
    if sin_bajar:
        print("\n  Sin registro de procedencia. Si el archivo existe igual, se bajo en una "
              "corrida\n  interrumpida: correr `python3 descargar_normas.py` y el script lo "
              "rebaja para\n  registrar hash y fecha.")
    if cambiadas:
        print("\n  Para actualizar y ver que cambio:")
        print("    python3 descargar_normas.py --forzar " +
              " ".join(f"--slug {s}" for s in cambiadas))
        print("    git diff argentina/fuentes/normas/")
        print("\n  Si el cambio es de fondo, anotarlo en "
              "argentina/skills/derecho-argentino/references/changelog-normativo.md")
    if a.sellar:
        if cambiadas or errores:
            print("\n  NO se sella. Sellar significa 'esto se comprobo contra la fuente oficial "
                  "y\n  coincide', y eso hoy no es cierto para todas. Resolver lo de arriba "
                  "primero.")
        else:
            hoy = datetime.now().strftime("%Y-%m-%d")
            for ruta in (RAIZ / "normas" / "normas.json",
                         RAIZ / "jurisprudencia" / "fallos.json"):
                try:
                    m = json.loads(ruta.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    print(f"  no se pudo sellar {ruta.name}")
                    continue
                m["verificado"] = hoy
                ruta.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
                print(f"  sellado {ruta.name}: verificado = {hoy}")
            print("\n  estado.py deja de marcarlo vencido.")

    return 1 if cambiadas else 0


if __name__ == "__main__":
    sys.exit(main())
