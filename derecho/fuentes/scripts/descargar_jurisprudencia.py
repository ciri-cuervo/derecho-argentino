#!/usr/bin/env python3
"""Descarga las sentencias verificadas de jurisprudencia/fallos.json.

    python3 descargar_jurisprudencia.py
    python3 descargar_jurisprudencia.py --slug scba-galarza-l132729-2026-03-30 --forzar

Guarda cada sentencia como `jurisprudencia/<slug>.pdf` y registra procedencia y hash en
`jurisprudencia/procedencia.json`. Un fallo descargado deja de estar alcanzado por la
prohibición de la sección 2 de la skill: pasa a ser material verificado. Que esté verificado
no significa que siga siendo buen derecho: eso lo dice `[VERIFICAR PRECEDENTE: ...]`.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from _comun import (RAIZ, ATexto, ahora, bajar, decodificar, exigir_slugs_conocidos,
                    fragmento_div, sha256_archivo)
from descargar_normas import avisar_intento, es_pdf_real, limpiar_aviso

# Los separadores que parten una carátula argentina. `s/` es el más común de todos -"Fulano
# s/ recurso de hecho"- y faltaba: sin él, `cabeza` se queda con la carátula ENTERA cuando no
# hay coma antes, y una cadena de noventa caracteres con el objeto del proceso y el número de
# causa no aparece nunca en el cuerpo. Medido sobre el corpus: seis fallos daban "puede ser
# OTRO fallo" estando perfectos, entre ellos "Simón", "Casal" y "Arancibia Clavel". Es la
# alarma que suena mal, que es como se apaga un control.
SEPARADORES = re.compile(r",|\s+s/|\s+c/|\s+vs\.|\s+contra\s|\s+y\s+otros?\b", re.I)


def _clave(texto: str) -> str:
    """Normaliza para comparar carátulas: minúsculas, sin acentos ni puntuación."""
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def cabeza_de_caratula(caratula: str) -> str:
    """La parte de la carátula que nombra a la parte, antes del objeto del proceso."""
    return SEPARADORES.split(caratula)[0]


def es_cotejable(caratula: str) -> bool:
    """False cuando la carátula no tiene apellido contra el que cotejar.

    Son las anonimizadas —«E., M. R. c/ L., M. F. s/ Acción de compensación económica»—, que en
    familia y minoridad son la regla y no la excepción, y en el corpus son diez de setenta. Por
    el apellido no hay medida: una inicial aparece en cualquier documento.

    **Pero que no haya apellido no es que no haya nada que cotejar.** Queda el expediente, y de
    eso se ocupa `expediente_en_el_cuerpo()`. Esta función contesta sólo por el apellido; quien
    llama decide con las dos respuestas.
    """
    return len(_clave(cabeza_de_caratula(caratula))) >= 4


def texto_de_pdf(ruta: Path) -> str | None:
    """El texto del PDF, o None si no se pudo extraer por falta de la herramienta.

    None y `""` son cosas distintas y quien llama tiene que poder separarlas: None es "no pude
    medir" —falta poppler— y `""` es "el PDF no trae capa de texto". Confundirlas deja pasar un
    fallo sin cotejar como si estuviera cotejado.

    Con -layout, que es como hay que extraer siempre: sin esa opción el extractor reordena las
    palabras de los PDF a dos columnas.
    """
    try:
        hecho = subprocess.run(["pdftotext", "-q", "-layout", str(ruta), "-"],
                               capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return hecho.stdout if hecho.returncode == 0 else None


def confirmar_identidad(cuerpo: str, caratula: str) -> str | None:
    """Comprueba que lo bajado sea EL fallo declarado. Devuelve el problema, o None.

    Por qué existe: en los repositorios de la CSJN el documento se pide por un identificador
    interno -idAnalisis, idDocumento- que NO se deriva de la cita de Fallos y hay que curar a
    mano. Un id tomado de un buscador web puede corresponder a otro fallo: buscando "Acosta"
    331:858 aparece indexado idAnalisis=584107, que baja "Llerena, Horacio Luis s/ abuso de
    armas". Sin este control se cita un fallo por otro, que es el peor error posible acá.

    Y corre sobre los PDF, que es donde vive ese peligro. Durante varias versiones el cotejo
    estaba metido en la rama del HTML, así que de setenta fallos se cotejaban tres: los únicos
    que NO vienen de la CSJN. El control existía, daba verde y no medía nada.

    El criterio es deliberadamente laxo: alcanza con que el apellido principal de la carátula
    aparezca en el cuerpo. No se pide coincidencia exacta porque las carátulas oficiales traen
    "s/ recurso de hecho", números de causa y abreviaturas que varían entre repositorios.
    """
    if not cuerpo or not es_cotejable(caratula):
        return None
    cabeza = cabeza_de_caratula(caratula)
    if _clave(cabeza) not in _clave(cuerpo):
        return (f"el documento bajado no menciona \"{cabeza.strip()}\": puede ser OTRO fallo. "
                "Verificar el identificador contra la carátula antes de aceptarlo")
    return None


def expediente_en_el_cuerpo(causa: str, cuerpo: str) -> str | None:
    """El número de expediente de `causa` si aparece en el documento, o None.

    Para una carátula anonimizada no hay apellido, pero sí suele haber expediente, y ése el
    documento lo trae impreso: «C. 122.501», «CIV 86767/2015», «LM-1573-2024». Cotejarlo
    convierte en control lo que antes era una afirmación escrita en el mensaje —«la identidad
    se confirma por la cita»— que NADIE comprobaba.

    No sirve cuando la causa declarada es la cita de Fallos: «Fallos 346:287» se asigna al
    publicar y no está impresa en la sentencia. Ahí devuelve None y el estado sigue siendo
    `no aplica`, que es la verdad.

    Se comparan sin puntos ni espacios porque el registro escribe «C. 122.501» y el documento
    «122501», y sin eso el cotejo fallaría por la tipografía y no por la identidad.
    """
    if not causa or causa.strip().lower().startswith("fallos"):
        return None
    plano = re.sub(r"[.\s]", "", cuerpo)
    for numero in re.findall(r"\d[\d.]{3,}", causa):
        if re.sub(r"[.\s]", "", numero) in plano:
            return numero
    return None


def texto_recuperado(destino: Path) -> str | None:
    """El texto que `reocr_jurisprudencia.py` dejó para este PDF, si lo dejó.

    Vive al lado, en `ocr/<slug>.txt`, y es una DERIVACIÓN del mismo archivo: no es otra
    fuente. Por eso sirve para cotejar identidad y por eso el detalle del cotejo dice que se
    hizo por ahí, en vez de dejar creer que el PDF era legible.
    """
    recuperado = destino.parent / "ocr" / f"{destino.stem}.txt"
    if not recuperado.is_file():
        return None
    return recuperado.read_text(encoding="utf-8", errors="replace")


def _por_ocr(via_ocr: bool) -> str:
    return " (leído de la recuperación por OCR de `ocr/`, no del PDF)" if via_ocr else ""


def cotejar_identidad(destino: Path, guardado: bytes, charset: str | None, es_pdf: bool,
                      caratula: str, causa: str = "") -> tuple[str, str]:
    """Coteja lo guardado contra la carátula declarada. Devuelve (estado, detalle).

    Tres estados y no dos, porque "no se pudo cotejar" no es "está bien":

      cotejado    el apellido de la carátula aparece en el documento; o, si la carátula está
                  anonimizada, el número de expediente de la causa declarada aparece en él.
      no aplica   la carátula está anonimizada Y su causa declarada tampoco sirve de cotejo,
                  porque es la cita de Fallos, que se asigna al publicar y no está impresa en
                  la sentencia. Es permanente y legítimo, así que se REGISTRA y no se marca
                  como pendiente: convertirlo en alarma la haría sonar en cada corrida y se
                  dejaría de mirar. Lo que sí dice el mensaje es que ese documento no tiene
                  control mecánico de identidad, en vez de sugerir que la cita lo confirma.
      revisar     o el apellido no aparece -puede ser otro fallo- o faltó el instrumento. Las
                  dos cosas van a `revisar` y hacen salir con código 1.

    Va aparte de `main()` para poder ejercitarla sin red, que es lo que faltaba: la rama del PDF
    -la única que importa, porque los PDF son los de la CSJN- no la cubría ningún test.

    Se coteja sobre lo GUARDADO y después de escribirlo: que la carátula aparezca en el menú de
    un portal no probaría nada, y del PDF hay que leer el archivo. Del HTML se decodifica con el
    charset que declaró el servidor, que antes se descartaba; no era un defecto —la cascada de
    `decodificar()` prueba utf-8, cp1252 y latin-1 y recupera igual— pero adivinar lo que el
    servidor ya dijo deja el resultado a merced del orden de esa cascada.
    """
    anonima = not es_cotejable(caratula)
    via_ocr = False
    if es_pdf:
        cuerpo = texto_de_pdf(destino)
        if cuerpo is None:
            return ("revisar", "no se pudo cotejar la carátula: falta `pdftotext` (poppler). "
                               "Instalarlo y volver a correr con --forzar, o cotejar a mano")
        if not cuerpo.strip():
            # Sin capa de texto no hay nada que cotejar en el PDF, pero puede haber una
            # recuperación por OCR del MISMO documento, con su procedencia en `ocr/`. Es la
            # única salida: sin esto la marca queda encendida para siempre -el reOCR no toca
            # el PDF- y una alarma que no se puede apagar se deja de mirar.
            cuerpo = texto_recuperado(destino) or ""
            if not cuerpo.strip():
                return ("revisar", "el PDF no trae capa de texto y no hay recuperación en "
                                   "`ocr/`, así que la carátula no se pudo cotejar: correr "
                                   "`reocr_jurisprudencia.py` sobre este slug y repetir")
            via_ocr = True
    else:
        parser = ATexto()
        parser.feed(decodificar(guardado, charset))
        cuerpo = parser.texto()
    if anonima:
        # Sin apellido queda el expediente, que el documento sí trae impreso.
        numero = expediente_en_el_cuerpo(causa, cuerpo)
        if numero:
            return ("cotejado", f"carátula anonimizada, sin apellido que cotejar; el número de "
                                f"causa {numero} aparece en el documento{_por_ocr(via_ocr)}")
        return ("no aplica", "carátula anonimizada y la causa declarada no es un expediente "
                             "cotejable —la cita de Fallos se asigna al publicar y no está "
                             "impresa en la sentencia—: este documento no tiene control "
                             "mecánico de identidad y se coteja leyéndolo")
    problema = confirmar_identidad(cuerpo, caratula)
    if problema:
        return ("revisar", problema)
    return ("cotejado", "el apellido de la carátula aparece en el texto del "
                        f"documento{_por_ocr(via_ocr)}")


JURIS = RAIZ / "jurisprudencia"
MANIFIESTO = JURIS / "fallos.json"
PROCEDENCIA = JURIS / "procedencia.json"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slug", action="append", default=[])
    p.add_argument("--forzar", action="store_true")
    p.add_argument("--timeout", type=int, default=180, help="Segundos por intento (default 180). Subirlo si el sitio es lento")
    p.add_argument("--reintentos", type=int, default=3)
    p.add_argument("--verboso", action="store_true", help="Muestra tamaño y tiempo de cada intento")
    a = p.parse_args()

    fallos = json.loads(MANIFIESTO.read_text(encoding="utf-8"))["fallos"]
    exigir_slugs_conocidos(a.slug, fallos)
    if a.slug:
        fallos = [f for f in fallos if f["slug"] in a.slug]
    proc = (json.loads(PROCEDENCIA.read_text(encoding="utf-8"))
            if PROCEDENCIA.exists() else {})
    # `setdefault` y no `proc["fallos"]`: un archivo que exista sin esa clave hacía morir el
    # script con KeyError después de haber bajado. Es la misma clase de error que `ya_registrada`
    # documenta en el descargador de normas, con el primer nivel del documento confundido con
    # sus entradas.
    proc.setdefault("_descripcion",
                    "Procedencia de las sentencias bajadas: de dónde salió cada una, cuándo, y "
                    "el hash del archivo tal como quedó en disco. `revisar` marca lo que no se "
                    "pudo dar por cotejado y hay que mirar a mano.")
    proc.setdefault("fallos", {})

    ok = fallo_n = salteados = avisados = dudosos = 0
    for f in fallos:
        destino = JURIS / f"{f['slug']}.pdf"
        alterno = JURIS / f"{f['slug']}.html"
        if (destino.exists() or alterno.exists()) and not a.forzar \
                and f["slug"] in proc["fallos"]:
            print(f"  YA ESTÁ   {f['slug']}")
            salteados += 1
            continue
        avisar_intento(f["slug"], f["url"])
        try:
            crudo, charset, ctype = bajar(f["url"], timeout=a.timeout,
                                          reintentos=a.reintentos, verboso=a.verboso)
        except Exception as e:
            limpiar_aviso()
            print(f"  ERROR     {f['slug']:42} {type(e).__name__}: {e}")
            fallo_n += 1
            continue
        limpiar_aviso()
        # La extensión sale del Content-Type, no de la esperanza. Un fallo tomado de JUBA o
        # de una ficha devuelve HTML, y guardarlo como .pdf hace que después no se pueda leer
        # ni auditar: es el mismo error que ya había en el descargador de normas.
        guardado = crudo
        es_pdf = es_pdf_real(ctype, crudo[:5] == b"%PDF-")
        if not es_pdf:
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
                print("              -> AVISO: no encontré <div class=\"contenido\">, "
                      "se guarda la página entera")
        destino.write_bytes(guardado)
        estado, detalle = cotejar_identidad(destino, guardado, charset, es_pdf, f["caratula"],
                                            f.get("causa", ""))
        proc["fallos"][f["slug"]] = {
            "archivo": destino.name,
            "caratula": f["caratula"], "tribunal": f["tribunal"], "causa": f["causa"],
            "fecha": f["fecha"], "url": f["url"], "content_type": ctype,
            "descargado": ahora(),
        }
        # Se registra el hash de lo GUARDADO y nada más: de la página entera no conservamos
        # los bytes, así que un hash suyo no se podría volver a cotejar contra nada. El
        # contrato está escrito una sola vez, en `_comun.py`.
        proc["fallos"][f["slug"]]["sha256_archivo"] = sha256_archivo(destino)
        # El resultado del cotejo se registra SIEMPRE, incluso cuando salió bien. Que la entrada
        # no diga nada es lo que hacía indistinguible "se cotejó y pasó" de "no se cotejó nunca",
        # y eso último era el caso de los sesenta y siete PDF.
        proc["fallos"][f["slug"]]["cotejo"] = f"{estado}: {detalle}"
        if estado == "revisar":
            proc["fallos"][f["slug"]]["revisar"] = [detalle]
            dudosos += 1
            print(f"  REVISAR   {f['slug']:42} {len(crudo):>9,} bytes")
            print(f"              -> {detalle}")
        else:
            proc["fallos"][f["slug"]].pop("revisar", None)
            marca = "OK" if estado == "cotejado" else "SIN COTEJO"
            print(f"  {marca:9} {f['slug']:42} {len(crudo):>9,} bytes")
            if estado != "cotejado":
                print(f"              -> {detalle}")
        PROCEDENCIA.write_text(json.dumps(proc, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
        ok += 1

    PROCEDENCIA.write_text(json.dumps(proc, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"\n  {ok} bajados, {salteados} ya estaban, {fallo_n} con error"
          + (f", {avisados} guardados como .html por no ser PDF." if avisados else "."))
    if dudosos:
        print(f"\n  {dudosos} quedaron marcados en 'revisar' de procedencia.json: la carátula no "
              f"se pudo\n  dar por cotejada. Citar un fallo por otro es el peor error posible "
              f"acá, así que\n  esto se mira antes de usarlos.")
    print("  Al citar cualquiera de estos fallos, acompañar igual con "
          "[VERIFICAR PRECEDENTE: ...].")
    return 1 if fallo_n or dudosos else 0


if __name__ == "__main__":
    sys.exit(main())
