#!/usr/bin/env python3
"""Descarga los textos normativos del manifiesto y los deja en texto plano con procedencia.

Cada archivo queda en `argentina/fuentes/normas/<slug>.txt` con un encabezado que dice de
donde salió, cuando y con que hash. El hash es lo que después permite detectar que la norma
cambió (ver `verificar_normas.py`).

    python3 descargar_normas.py                  # todo el manifiesto
    python3 descargar_normas.py --prioridad 1    # solo lo imprescindible
    python3 descargar_normas.py --slug pba-ley-11653 --slug lct-20744
    python3 descargar_normas.py --forzar         # vuelve a bajar lo ya descargado

Los PDF se guardan tal cual, sin extraer texto.

ADVERTENCIA. Los textos que publican estas bases pueden estar truncados o con la acentuación
degradada. Antes de transcribir un artículo a un escrito, cotejar contra el PDF del Boletín
Oficial de la fecha de publicación. Lo bajado por este script es material de trabajo
verificable, no fe publica.
"""
from __future__ import annotations

import argparse
import sys
import urllib.parse
from datetime import date, datetime, timezone

from _comun import (NORMAS, bajar, cargar_manifiesto, cargar_procedencia,
                    cargar_revisiones, decodificar, guardar_procedencia, revisar_texto,
                    sha256, sha256_texto, ATexto)

# Todo lo que no sea un marcador de format() va en ASCII, y no por descuido: este encabezado
# ya esta escrito en los .txt bajados, asi que la plantilla y el corpus son el mismo texto en
# dos lugares. Acentuar una palabra de aca no corrige nada -- parte el corpus en dos, los
# viejos con una forma y los nuevos con otra --, y volver a alinearlo exige bajar las normas
# de nuevo, que es algo que InfoLEG y normas.gba solo le permiten al usuario. Vale para las
# etiquetas y para la prosa: `TestPlantillaDelEncabezado` compara las dos contra los .txt.
# Los marcadores, ademas, son identificadores de format(): `{jurisdicción}` levanta KeyError
# recien al bajar la primera norma.
ENCABEZADO = """{titulo}
{raya}
Jurisdiccion:     {jurisdiccion}
Fuente:           {url}
Descargado:       {fecha}
SHA-256 (crudo):  {hash}
Charset:          {charset}

Texto consolidado automaticamente desde la fuente oficial. Reproduccion de norma juridica.
NO es publicacion oficial: para transcribir un articulo en un escrito, cotejar contra el
Boletin Oficial. Si el texto aparece truncado o con acentuacion degradada, esta anotado en
el manifiesto `normas.json`.
{raya}

"""


def es_pdf_real(ctype: str | None, declarado: bool) -> bool:
    """Decide si lo bajado es un PDF por lo que DICE EL SERVIDOR, no por la extensión.

    Acá hubo un bug: la extensión y el campo `formato` del manifiesto son una suposición, y
    un digesto provincial que sirve el PDF desde una URL sin `.pdf` -con query string, por
    ejemplo- hacía que el script tratara los bytes como HTML, los pasara por el parser y
    escribiera un .txt binario de 240 KB. El archivo quedaba ilegible y el unico sintoma era
    que revisar_texto no encontraba ni un artículo, que parece un problema de la fuente.
    """
    if declarado:
        return True
    return bool(ctype) and "pdf" in ctype.lower()


def ya_registrada(proc: dict, slug: str) -> bool:
    """True si la norma ya tiene procedencia registrada.

    Existe como función propia porque acá hubo un bug que vivio varias versiones: el chequeo
    era `slug in proc`, y `cargar_procedencia()` devuelve el documento entero, cuyo primer
    nivel son `_descripcion` y `normas`. Nunca había un slug ahí, con lo que la condición
    daba False siempre: el script rebajaba las 59 normas en cada corrida, la rama YA ESTA era
    código muerto y `--forzar` no se distinguia de no pasarlo. Se ve solo si uno cuenta los
    pedidos a los sitios oficiales.
    """
    return slug in proc.get("normas", {})


def _avisar_intento(slug: str, url: str) -> None:
    """Deja en pantalla que hay una descarga en curso, para que un sitio lento no parezca
    un cuelgue. Un host que no responde se come timeout x reintentos sin imprimir nada, y
    con el default eso es casi diez minutos de silencio. La línea se sobreescribe con el
    resultado, así que no ensucia la salida; si no hay terminal, no se imprime."""
    if not sys.stdout.isatty():
        return
    host = urllib.parse.urlsplit(url).netloc
    print(f"  bajando     {slug:28} {host[:40]}".ljust(100), end="\r", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prioridad", type=int, default=None,
                   help="Baja solo las normas con prioridad menor o igual a este valor")
    p.add_argument("--slug", action="append", default=[])
    p.add_argument("--forzar", action="store_true")
    p.add_argument("--timeout", type=int, default=180,
                   help="Segundos por intento (default 180). Subirlo si el sitio es lento")
    p.add_argument("--reintentos", type=int, default=3)
    p.add_argument("--verboso", action="store_true",
                   help="Muestra tamanio y tiempo de cada intento")
    a = p.parse_args()

    NORMAS.mkdir(parents=True, exist_ok=True)
    proc = cargar_procedencia()
    revisiones = cargar_revisiones()
    normas = cargar_manifiesto()
    if a.slug:
        normas = [n for n in normas if n["slug"] in a.slug]
    if a.prioridad:
        normas = [n for n in normas if n.get("prioridad", 9) <= a.prioridad]

    ok = fallo = salteadas = sin_url = revisar = 0
    for n in normas:
        slug, url = n["slug"], n.get("url")
        if not url:
            print(f"  SIN URL     {slug:28} {n.get('nota', 'completar el manifiesto')}")
            sin_url += 1
            continue
        es_pdf = n.get("formato") == "pdf" or url.lower().endswith(".pdf")
        destino = NORMAS / (f"{slug}.pdf" if es_pdf else f"{slug}.txt")
        # Si ya hay procedencia, el nombre real es el registrado: el adivinado puede diferir
        # cuando el servidor devolvió un PDF desde una URL sin extensión.
        registrado = proc.get("normas", {}).get(slug, {}).get("archivo")
        if registrado:
            destino = NORMAS / registrado
        if destino.exists() and not a.forzar:
            if ya_registrada(proc, slug):
                print(f"  YA ESTA     {slug:28} {destino.name}")
                salteadas += 1
                continue
            # El archivo esta pero no hay procedencia: sin hash ni fecha no sirve como
            # fuente verificable ni se le puede detectar un cambio. Se vuelve a bajar.
            print(f"  SIN REGISTRO {slug:27} {destino.name} - se rebaja para registrar "
                  f"procedencia")
        _avisar_intento(slug, url)
        try:
            crudo, charset, ctype = bajar(url, timeout=a.timeout, reintentos=a.reintentos,
                                          verboso=a.verboso)
        except Exception as e:
            print(f"  ERROR       {slug:28} {type(e).__name__}: {e}")
            fallo += 1
            continue
        h = sha256(crudo)
        h_texto = None
        problemas = []
        if es_pdf_real(ctype, es_pdf) and not es_pdf:
            es_pdf = True
            destino = NORMAS / f"{slug}.pdf"
            problemas.append(
                f"el servidor devolvio {ctype}: se guarda como PDF. Agregar "
                f'"formato": "pdf" a la entrada del manifiesto')
        elif es_pdf_real(ctype, es_pdf):
            es_pdf = True
        if es_pdf:
            destino.write_bytes(crudo)
            if len(crudo) < 20000:
                problemas.append(f"PDF de solo {len(crudo)} bytes: revisar")
        else:
            parser = ATexto()
            parser.feed(decodificar(crudo, charset))
            cuerpo = parser.texto()
            cab = ENCABEZADO.format(titulo=n["titulo"], raya="=" * 78,
                                    jurisdiccion=n["jurisdiccion"], url=url,
                                    fecha=date.today().isoformat(), hash=h,
                                    charset=charset or "no declarado")
            destino.write_text(cab + cuerpo + "\n", encoding="utf-8")
            h_texto = sha256_texto(cuerpo + "\n")
            problemas += revisar_texto(cuerpo)
        proc["normas"][slug] = {
            "titulo": n["titulo"], "url": url, "archivo": destino.name,
            "sha256": h, "sha256_texto": h_texto, "bytes": len(crudo), "content_type": ctype,
            "descargado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        leidos = revisiones.get(slug, {})
        resueltos = [(x, leidos[x]) for x in problemas if x in leidos]
        pendientes = [x for x in problemas if x not in leidos]
        if resueltos:
            proc["normas"][slug]["revisado"] = [
                {"problema": x, "veredicto": v} for x, v in resueltos]
        else:
            proc["normas"][slug].pop("revisado", None)
        if pendientes:
            proc["normas"][slug]["revisar"] = pendientes
            print(f"  REVISAR     {slug:28} {len(crudo):>9,} bytes  -> {destino.name}")
            for x in pendientes:
                print(f"              -> {x}")
            guardar_procedencia(proc)
            revisar += 1
        else:
            proc["normas"][slug].pop("revisar", None)
            estado = "REVISADO" if resueltos else "OK"
            print(f"  {estado:11} {slug:28} {len(crudo):>9,} bytes  -> {destino.name}")
            for x, v in resueltos:
                print(f"              -> {x}")
                print(f"                 leido: {v}")
        guardar_procedencia(proc)   # incremental: un Ctrl-C no debe perder el registro
        ok += 1

    guardar_procedencia(proc)
    print(f"\n  {ok} bajadas ({revisar} marcadas para revisar), {salteadas} ya estaban, "
          f"{sin_url} sin URL en el manifiesto, {fallo} con error.")
    if revisar:
        print("  Las marcadas para revisar quedaron anotadas en procedencia.json bajo "
              "'revisar'.\n  Casi siempre significa que la URL apunta a la ficha y no al "
              "texto de la norma.")
    print(f"  Procedencia actualizada en normas/procedencia.json")
    if sin_url:
        print("\n  Las entradas sin URL quedan pendientes: completar `normas.json` con la "
              "URL oficial\n  del texto actualizado antes de contar con esas normas offline.")
    return 1 if fallo else 0


if __name__ == "__main__":
    sys.exit(main())
