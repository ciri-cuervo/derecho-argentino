#!/usr/bin/env python3
"""Controla si alguna de las normas descargadas cambió en la fuente oficial.

Vuelve a pedir cada URL, calcula el hash y lo compara contra `normas/procedencia.json`. No
escribe nada: solo informa. Sirve como alarma de reforma legislativa.

    python3 verificar_normas.py
    python3 verificar_normas.py --prioridad 1

Sale con código 1 si alguna norma cambió, de modo que se puede colgar de una tarea
programada o de un workflow. Que el hash cambie no significa siempre que cambió la ley: las
bases oficiales tocan la maquetación de sus páginas. Lo que el resultado dice es "hay que
mirar esta", no "esta norma se reformó".
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
                   help="Si nada cambió, actualiza la fecha `verificado` de los manifiestos")
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
        # Se compara contra LO QUE GUARDAMOS, que es lo único de lo que tenemos hash.
        #
        # De un PDF guardamos la descarga entera, así que la comparación es byte a byte. De
        # una página guardamos el texto ya extraído, y ahí el byte a byte no sirve: hay bases
        # -argentina.gob.ar, juristeca- que reescriben su HTML en cada request con tokens y
        # nonces, sin que cambie una coma de la norma. Compararlas por bytes las dejaria en
        # rojo permanente, que es la forma más segura de que nadie mire la alarma cuando de
        # verdad suene. Se reextrae el texto y se compara eso.
        es_pdf = proc[slug].get("archivo", "").lower().endswith(".pdf")
        if es_pdf:
            esperado, actual = proc[slug].get("sha256_archivo"), sha256(crudo)
            motivo = "cambió el PDF"
        else:
            esperado, actual = proc[slug].get("sha256_texto"), None
            motivo = "cambió el texto de la norma"
            try:
                parser = ATexto()
                parser.feed(decodificar(crudo, charset))
                actual = sha256_texto(parser.texto() + "\n")
            except Exception:
                actual = None
        if esperado is None:
            cambiadas.append(slug)
            print(f"  CAMBIO      {slug:28} REVISAR - no hay hash de lo guardado para "
                  f"contrastar")
        elif actual == esperado:
            print(f"  SIN CAMBIOS {slug:28} (bajada el {bajada})")
        else:
            cambiadas.append(slug)
            print(f"  CAMBIO      {slug:28} REVISAR - {motivo}")

    print(f"\n  {len(cambiadas)} cambiadas, {len(sin_bajar)} sin bajar, {len(errores)} con error.")
    if sin_bajar:
        print("\n  Sin registro de procedencia. Si el archivo existe igual, se bajó en una "
              "corrida\n  interrumpida: correr `python3 descargar_normas.py` y el script lo "
              "rebaja para\n  registrar hash y fecha.")
    if cambiadas:
        print("\n  Para actualizar y ver qué cambió:")
        print("    python3 descargar_normas.py --forzar " +
              " ".join(f"--slug {s}" for s in cambiadas))
        print("    git diff derecho/fuentes/normas/")
        print("\n  Si el cambio es de fondo, anotarlo en "
              "derecho/skills/derecho-argentino/references/changelog-normativo.md")
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
