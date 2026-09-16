#!/usr/bin/env python3
"""Descarga las sentencias verificadas de jurisprudencia/fallos.json.

    python3 descargar_jurisprudencia.py
    python3 descargar_jurisprudencia.py --slug scba-galarza-l132729-2026-03-30 --forzar

Guarda cada sentencia como `jurisprudencia/<slug>.pdf` y registra procedencia y hash en
`jurisprudencia/procedencia.json`. Un fallo descargado deja de estar alcanzado por la
prohibición de la sección 2 de la skill: pasa a ser material verificado. Que este verificado
no significa que siga siendo buen derecho: eso lo dice `[VERIFICAR PRECEDENTE: ...]`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from _comun import RAIZ, ATexto, bajar, decodificar, fragmento_div, sha256_archivo
from descargar_normas import es_pdf_real

def _clave(texto: str) -> str:
    """Normaliza para comparar carátulas: minúsculas, sin acentos ni puntuación."""
    import unicodedata
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def confirmar_identidad(cuerpo: str, caratula: str) -> str | None:
    """Comprueba que lo bajado sea EL fallo declarado. Devuelve el problema, o None.

    Por que existe: en los repositorios de la CSJN el documento se pide por un identificador
    interno -idAnalisis, idDocumento- que NO se deriva de la cita de Fallos y hay que curar a
    mano. Un id tomado de un buscador web puede corresponder a otro fallo: buscando "Acosta"
    331:858 aparece indexado idAnalisis=584107, que baja "Llerena, Horacio Luis s/ abuso de
    armas". Sin este control se cita un fallo por otro, que es el peor error posible acá.

    El criterio es deliberadamente laxo: alcanza con que el apellido principal de la carátula
    aparezca en el cuerpo. No se pide coincidencia exacta porque las carátulas oficiales traen
    "s/ recurso de hecho", numeros de causa y abreviaturas que varían entre repositorios.
    """
    if not cuerpo or not caratula:
        return None
    cuerpo_k = _clave(cuerpo)
    # el apellido es lo primero de la carátula, antes de la coma o del " c/ "
    cabeza = re.split(r"[,]| c/ | vs\. | contra ", caratula)[0]
    apellido = _clave(cabeza)
    if len(apellido) < 4:
        return None
    if apellido not in cuerpo_k:
        return (f"el documento bajado no menciona \"{cabeza.strip()}\": puede ser OTRO fallo. "
                f"Verificar el identificador contra la caratula antes de aceptarlo")
    return None


JURIS = RAIZ / "jurisprudencia"
MANIFIESTO = JURIS / "fallos.json"
PROCEDENCIA = JURIS / "procedencia.json"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slug", action="append", default=[])
    p.add_argument("--forzar", action="store_true")
    p.add_argument("--timeout", type=int, default=180,
                   help="Segundos por intento (default 180). Subirlo si el sitio es lento")
    p.add_argument("--reintentos", type=int, default=3)
    p.add_argument("--verboso", action="store_true",
                   help="Muestra tamanio y tiempo de cada intento")
    a = p.parse_args()

    fallos = json.loads(MANIFIESTO.read_text(encoding="utf-8"))["fallos"]
    if a.slug:
        fallos = [f for f in fallos if f["slug"] in a.slug]
    proc = (json.loads(PROCEDENCIA.read_text(encoding="utf-8"))
            if PROCEDENCIA.exists() else {"fallos": {}})

    ok = fallo_n = salteados = avisados = 0
    for f in fallos:
        destino = JURIS / f"{f['slug']}.pdf"
        alterno = JURIS / f"{f['slug']}.html"
        if (destino.exists() or alterno.exists()) and not a.forzar \
                and f["slug"] in proc.get("fallos", {}):
            print(f"  YA ESTA   {f['slug']}")
            salteados += 1
            continue
        try:
            crudo, _, ctype = bajar(f["url"], timeout=a.timeout,
                                    reintentos=a.reintentos, verboso=a.verboso)
        except Exception as e:
            print(f"  ERROR     {f['slug']:42} {type(e).__name__}: {e}")
            fallo_n += 1
            continue
        # La extensión sale del Content-Type, no de la esperanza. Un fallo tomado de JUBA o
        # de una ficha devuelve HTML, y guardarlo como .pdf hace que después no se pueda leer
        # ni auditar: es el mismo error que ya había en el descargador de normas.
        aviso = None
        guardado = crudo
        if not es_pdf_real(ctype, crudo[:5] == b"%PDF-"):
            destino = alterno
            avisados += 1
            print(f"  AVISO     {f['slug']:42} no es PDF ({ctype or 'sin content-type'}): "
                  f"se guarda como .html")
            # De la página se guarda sólo la sentencia. El resto -menú, scripts, pie- es más de
            # la mitad del archivo y se mueve cuando el portal se rediseña, sin que cambie una
            # línea del fallo. Si el div no está se guarda entera y se dice: guardar menos en
            # silencio es peor que guardar maqueta.
            fragmento = fragmento_div(crudo, "contenido")
            if fragmento:
                guardado = fragmento
                print(f"              -> solo <div class=\"contenido\">: "
                      f"{len(fragmento):,} de {len(crudo):,} bytes")
            else:
                print(f"              -> AVISO: no encontré <div class=\"contenido\">, "
                      f"se guarda la página entera")
            # Solo se puede cotejar la identidad cuando hay texto legible. Un PDF escaneado
            # no la permite, y ahí el control queda en el ojo de quien lo lea. Se coteja sobre
            # lo GUARDADO: que la carátula aparezca en el menú no probaría nada.
            parser = ATexto()
            parser.feed(decodificar(guardado, None))
            aviso = confirmar_identidad(parser.texto(), f.get("caratula", ""))
        destino.write_bytes(guardado)
        proc["fallos"][f["slug"]] = {
            "archivo": destino.name,
            "caratula": f["caratula"], "tribunal": f["tribunal"], "causa": f["causa"],
            "fecha": f["fecha"], "url": f["url"], "content_type": ctype,
            "descargado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        # Se registra el hash de lo GUARDADO y nada más: de la página entera no conservamos
        # los bytes, así que un hash suyo no se podría volver a cotejar contra nada. El
        # contrato está escrito una sola vez, en `_comun.py`.
        proc["fallos"][f["slug"]]["sha256_archivo"] = sha256_archivo(destino)
        if aviso:
            proc["fallos"][f["slug"]]["revisar"] = [aviso]
            print(f"  REVISAR   {f['slug']:42} {len(crudo):>9,} bytes")
            print(f"              -> {aviso}")
        else:
            print(f"  OK        {f['slug']:42} {len(crudo):>9,} bytes")
        PROCEDENCIA.write_text(json.dumps(proc, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
        ok += 1

    PROCEDENCIA.write_text(json.dumps(proc, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"\n  {ok} bajados, {salteados} ya estaban, {fallo_n} con error"
          + (f", {avisados} guardados como .html por no ser PDF." if avisados else "."))
    print("  Al citar cualquiera de estos fallos, acompaniar igual con "
          "[VERIFICAR PRECEDENTE: ...].")
    return 1 if fallo_n else 0


if __name__ == "__main__":
    sys.exit(main())
