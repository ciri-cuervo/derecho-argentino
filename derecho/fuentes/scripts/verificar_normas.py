#!/usr/bin/env python3
"""Controla si alguna de las normas descargadas cambió en la fuente oficial.

Vuelve a pedir cada URL, calcula el hash y lo compara contra `normas/procedencia.json`. No
escribe nada: solo informa. Sirve como alarma de reforma legislativa.

    python3 verificar_normas.py
    python3 verificar_normas.py --prioridad 1
    python3 verificar_normas.py --slug lct-20744

Los códigos de salida son tres, y la diferencia importa si esto cuelga de una tarea programada:

    0   se verificaron todas y ninguna cambió
    1   alguna cambió
    2   alguna NO SE PUDO verificar -- el sitio no respondió, o no hay con qué contrastar

El 2 existe porque "no pude mirar" no es "está bien". Que el hash cambie tampoco significa
siempre que cambió la ley: las bases oficiales tocan la maquetación de sus páginas. Lo que el
resultado dice es "hay que mirar esta", no "esta norma se reformó".
"""
from __future__ import annotations

import argparse
import json
import sys

from _comun import (RAIZ, ATexto, bajar, cargar_manifiesto, cargar_procedencia,
                    decodificar, exigir_slugs_conocidos, hoy, sha256, sha256_texto)


def comparar(registro: dict, crudo: bytes, charset: str | None) -> tuple[str, str]:
    """Compara lo que devolvió el sitio contra lo guardado. Devuelve (estado, detalle).

    Tres estados y no dos, y la diferencia es el valor de la alarma:

      sin cambios  el hash coincide.
      cambio       no coincide: hay que mirar esa norma.
      sin medir    NO SE PUDO comparar. Decir "cambio" acá manda a alguien a buscar una reforma
                   que no existe, y una alarma que hace eso seguido se aprende a ignorar.

    Se compara contra LO QUE GUARDAMOS, que es lo único de lo que tenemos hash. De un PDF
    guardamos la descarga entera, así que va byte a byte. De una página guardamos el texto ya
    extraído, y ahí el byte a byte no sirve: hay bases -argentina.gob.ar, juristeca- que
    reescriben su HTML en cada request con tokens y nonces sin que cambie una coma de la norma.
    Compararlas por bytes las dejaría en rojo permanente, que es la forma más segura de que nadie
    mire la alarma cuando de verdad suene.

    Va aparte de `main()` porque es la decisión entera del script y no se podía ejercitar sin
    salir a la red.
    """
    es_pdf = registro.get("archivo", "").lower().endswith(".pdf")
    if es_pdf:
        esperado, actual, motivo = registro.get("sha256_archivo"), sha256(crudo), "cambió el PDF"
    else:
        esperado, motivo = registro.get("sha256_texto"), "cambió el texto de la norma"
        try:
            parser = ATexto()
            parser.feed(decodificar(crudo, charset))
            actual = sha256_texto(parser.texto() + "\n")
        except Exception as e:
            return ("sin medir", f"no se pudo extraer el texto de lo que devolvió el sitio "
                                 f"({type(e).__name__}): no dice que la norma cambió")
    if esperado is None:
        return ("sin medir", "no hay hash de lo guardado con qué contrastar: rebajarla con "
                             "descargar_normas.py --forzar para registrarlo")
    if actual == esperado:
        return ("sin cambios", "")
    return ("cambio", motivo)


def comando_para_rebajar(cambiadas: list[str]) -> str:
    """El comando que rebaja las normas que cambiaron, para copiar y pegar.

    Va aparte y con test porque es salida que alguien ejecuta, y se rompió sin que nada avisara:
    la concatenación quedó como `"...--forzar ".join(slugs)`, que con un slug imprime el slug sin
    comando y con dos mete el comando ENTRE los dos slugs. Una sugerencia de comando mal armada no
    falla ruidosamente: se pega en la terminal y ahí se ve.
    """
    return ("    python3 descargar_normas.py --forzar "
            + " ".join(f"--slug {s}" for s in cambiadas))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prioridad", type=int, default=None)
    p.add_argument("--slug", action="append", default=[], help="Verificar sólo estas normas. Sin esto se piden las 147 al sitio oficial")
    p.add_argument("--timeout", type=int, default=180, help="Segundos por intento (default 180). Subirlo si el sitio es lento")
    p.add_argument("--reintentos", type=int, default=3)
    p.add_argument("--verboso", action="store_true", help="Muestra tamaño y tiempo de cada intento")
    p.add_argument("--sellar", action="store_true", help="Si nada cambió, actualiza la fecha `verificado` de normas.json")
    a = p.parse_args()

    proc = cargar_procedencia()["normas"]
    normas = cargar_manifiesto()
    exigir_slugs_conocidos(a.slug, normas)
    if a.slug:
        normas = [n for n in normas if n["slug"] in a.slug]
    # `is not None`: `--prioridad 0` es falsy y quedaba ignorado, verificando el manifiesto
    # entero -o sea ciento cuarenta y siete pedidos a sitios oficiales- cuando se pidió el
    # subconjunto más chico posible.
    if a.prioridad is not None:
        normas = [n for n in normas if n.get("prioridad", 9) <= a.prioridad]

    cambiadas, sin_bajar, errores, sin_medir = [], [], [], []
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
        bajada = str(proc[slug].get("descargado", "?"))[:10]
        estado, detalle = comparar(proc[slug], crudo, charset)
        if estado == "sin medir":
            sin_medir.append(slug)
            print(f"  SIN MEDIR   {slug:28} {detalle}")
        elif estado == "sin cambios":
            print(f"  SIN CAMBIOS {slug:28} (bajada el {bajada})")
        else:
            cambiadas.append(slug)
            print(f"  CAMBIO      {slug:28} REVISAR - {detalle}")

    print(f"\n  {len(cambiadas)} cambiadas, {len(sin_medir)} sin medir, {len(sin_bajar)} sin "
          f"bajar, {len(errores)} con error.")
    if sin_medir:
        print("\n  SIN MEDIR no es 'sin cambios': de esas normas no se sabe. Salen con código 2 "
              "para que\n  una tarea programada no las tome por verificadas.")
    if sin_bajar:
        print("\n  Sin registro de procedencia. Si el archivo existe igual, se bajó en una "
              "corrida\n  interrumpida: correr `python3 descargar_normas.py` y el script lo "
              "rebaja para\n  registrar hash y fecha.")
    if cambiadas:
        print("\n  Para actualizar y ver qué cambió:")
        print(comando_para_rebajar(cambiadas))
        print("    git diff derecho/fuentes/normas/")
        print("\n  Si el cambio es de fondo, anotarlo en "
              "derecho/skills/derecho-argentino/references/changelog-normativo.md")
    if a.sellar:
        # Se sella normas.json y NADA MÁS. Durante varias versiones también se sellaba
        # `fallos.json`, y este script no mira ni un fallo: el sello decía "esto se comprobó
        # contra la fuente oficial y coincide" sobre setenta sentencias que nadie verificó, y
        # `estado.py` lo mostraba como `[ok] fallos ... verificados hace N días`. La
        # jurisprudencia no tiene verificador; hasta que lo tenga, su fecha no se toca desde acá.
        if cambiadas or errores or sin_medir:
            print("\n  NO se sella. Sellar significa 'esto se comprobó contra la fuente oficial "
                  "y\n  coincide', y eso hoy no es cierto para todas. Resolver lo de arriba "
                  "primero.")
        elif a.slug or a.prioridad is not None:
            print("\n  NO se sella: se verificó un subconjunto y el sello habla del manifiesto "
                  "entero.\n  Correr sin --slug ni --prioridad para sellar.")
        else:
            fecha = hoy()
            ruta = RAIZ / "normas" / "normas.json"
            try:
                m = json.loads(ruta.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                print(f"  no se pudo sellar {ruta.name}: {type(e).__name__}")
                return 2
            m["verificado"] = fecha
            ruta.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  sellado {ruta.name}: verificado = {fecha}")
            print("  fallos.json NO se sella acá: este script no verifica jurisprudencia.")
            print("\n  estado.py deja de marcar vencidas las normas.")

    if cambiadas:
        return 1
    return 2 if (sin_medir or errores) else 0


if __name__ == "__main__":
    sys.exit(main())
