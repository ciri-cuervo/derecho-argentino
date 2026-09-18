#!/usr/bin/env python3
"""Recupera por OCR el texto de los fallos cuyo PDF trae la capa de texto arruinada.

    python3 herramientas/reocr_jurisprudencia.py --listar
    python3 herramientas/reocr_jurisprudencia.py                 # los defectuosos del veredicto
    python3 herramientas/reocr_jurisprudencia.py csjn-bazterrica-fallos-308-1392

La basura de esos documentos no está en el papel sino en una capa de texto vieja que
`pdftotext` se limita a copiar: en "Bazterrica" devolvía `El] \\^<+]Ky puede P^+*+y un ^Fy dia`
donde la página dice "El sujeto puede un dia probar la droga". Esto vuelve a leer las
imágenes con tesseract y deja el resultado en `derecho/fuentes/jurisprudencia/ocr/`.

Lo que sale de acá NO es publicación oficial ni reemplaza al PDF: es una relectura local, y
cada cita literal se coteja contra la página antes de ir a un escrito. Por eso vive en su
propia carpeta, con la procedencia y el hash del PDF del que salió.

EL COTEJO SE DECLARA, NO SE EDITA. Las correcciones leídas contra la página van en
`ocr/correcciones/<slug>.json` y este script las aplica al generar, así que sobreviven a la
regeneración. Cada una tiene que coincidir exactamente una vez o el script se planta. **El
porqué —y qué va en `no_corregidas`— está en `derecho/fuentes/MANIFIESTO.md`, sección «El
cotejo se declara, no se edita».**

Requiere `pdftoppm` (poppler) y `tesseract` con el idioma español: `brew install tesseract-lang`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _externos
import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
JURIS = RAIZ / "derecho" / "fuentes" / "jurisprudencia"
SALIDA = JURIS / "ocr"
COTEJOS = SALIDA / "correcciones"
MANIFIESTO = JURIS / "fallos.json"
VEREDICTOS = RAIZ / "herramientas" / "lecturas-ocr.json"

# Un veredicto `layout` se arregla con `pdftotext -layout` y no necesita esto.
RECUPERABLES = ("destruido", "sustituciones")

RESOLUCION = 300
SEPARADOR = "=" * 78

# Estas dos quedan escritas dentro de cada .txt recuperado, y `ocr/procedencia.json` guarda el
# sha256 del archivo entero: la plantilla y el corpus son el mismo texto en dos lugares, así que
# tocar una palabra acá parte el corpus en dos y realinearlo exige correr tesseract sobre todos
# los PDF de nuevo. Se puede: son minutos en esta máquina. Lo que NO se puede es tocarlas y no
# regenerar, y eso lo caza `TestPlantillaDelEncabezadoOCR` comparándolas contra el corpus.
#
# Van acentuadas, que es la regla general del repositorio: esto es lo primero que lee quien abre
# el archivo. El encabezado de las normas es la excepción, y no por el hash sino porque
# realinearlo depende de que InfoLEG deje bajar.
AVISO = (
    "TEXTO RECUPERADO POR OCR LOCAL. No se bajó de la fuente: la capa de texto que traía el",
    "PDF estaba arruinada y esto es una relectura de las imágenes de la página. NO es",
    "publicación oficial y no reemplaza al PDF. Para transcribir un considerando a un escrito,",
    "cotejar contra la página del PDF: el número de página está marcado abajo.",
)
AVISO_COTEJO = (
    "ATENCIÓN: los renglones que lista el archivo de correcciones fueron leídos contra la",
    "página del PDF y corregidos. TODO EL RESTO es salida de máquina sin revisar y conserva",
    "los errores del OCR: que un renglón esté corregido no dice nada del de al lado.",
)


def _correr(cmd: list[str], entrada: bytes | None = None) -> bytes:
    hecho = subprocess.run(cmd, input=entrada, capture_output=True)
    if hecho.returncode != 0:
        raise SystemExit(f"fallo `{' '.join(cmd[:3])}...`: "
                         f"{hecho.stderr.decode(errors='replace')[:300]}")
    return hecho.stdout


def version_tesseract() -> str:
    linea = _correr(["tesseract", "--version"]).decode(errors="replace").splitlines()[0]
    return linea.strip()


def idiomas_tesseract() -> set[str]:
    salida = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True)
    return {l.strip() for l in salida.stdout.splitlines()[1:] if l.strip()}


def paginas(pdf: Path) -> int:
    info = _correr(["pdfinfo", str(pdf)]).decode(errors="replace")
    hallado = re.search(r"^Pages:\s+(\d+)", info, re.M)
    if not hallado:
        raise SystemExit(f"no pude contar las páginas de {pdf.name}")
    return int(hallado.group(1))


def sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def leer_pagina(pdf: Path, n: int, idioma: str, taller: Path) -> str:
    """Una página: se rasteriza a PNG y se OCRea.

    Va por archivo y no por tubería porque la salida a stdout de pdftoppm devuelve cero bytes
    en la build de poppler de Homebrew, sin error: el PNG intermedio es más predecible.
    """
    prefijo = taller / "pagina"
    png = prefijo.with_suffix(".png")
    png.unlink(missing_ok=True)
    _correr(["pdftoppm", "-png", "-r", str(RESOLUCION), "-f", str(n), "-l", str(n),
             "-singlefile", str(pdf), str(prefijo)])
    if not png.exists():
        raise SystemExit(f"pdftoppm no dejó el PNG de la página {n} de {pdf.name}")
    txt = _correr(["tesseract", str(png), "stdout", "-l", idioma, "--psm", "6"])
    png.unlink(missing_ok=True)
    return txt.decode("utf-8", errors="replace").rstrip()


def encabezado(ficha: dict, pdf: Path, hash_pdf: str, total: int, idioma: str,
               herramienta: str, cotejo: dict | None = None) -> str:
    fecha = ficha.get("fecha", "")
    dudosa = fecha.endswith("-01-01")
    lineas = [
        ficha.get("caratula", ficha["slug"]).rstrip("."),
        SEPARADOR,
        f"Tribunal:         {ficha.get('tribunal', '')}",
        f"Cita:             {ficha.get('causa', '')}",
        f"Fecha declarada:  {fecha}" + ("  <- 1 de enero: fecha sin confirmar en el manifiesto"
                                        if dudosa else ""),
        f"Fuente del PDF:   {ficha.get('url', '')}",
        f"Derivado de:      jurisprudencia/{pdf.name}",
        f"SHA-256 del PDF:  {hash_pdf}",
        f"Paginas:          {total}",
        f"Generado:         {_veredictos.hoy()}",
        f"Herramienta:      {herramienta}, -l {idioma} --psm 6, pdftoppm -r {RESOLUCION}",
    ]
    if cotejo:
        lineas += [
            f"Cotejado:         {cotejo['cotejado_el']}, {cotejo['base']}",
            f"Correcciones:     {len(cotejo['correcciones'])} declaradas en "
            f"ocr/correcciones/{ficha['slug']}.json",
        ]
    lineas += ["", *AVISO]
    if cotejo:
        lineas += ["", *AVISO_COTEJO]
    lineas += [
        "",
        "Regenerar: python3 herramientas/reocr_jurisprudencia.py " + ficha["slug"],
        SEPARADOR,
        "",
    ]
    return "\n".join(lineas)


def cargar_cotejo(slug: str) -> dict | None:
    """El cotejo declarado de un fallo, o None si nadie leyó sus páginas todavía."""
    ficha = COTEJOS / f"{slug}.json"
    if not ficha.exists():
        return None
    cotejo = json.loads(ficha.read_text(encoding="utf-8"))
    faltan = {"cotejado_el", "base", "correcciones"} - set(cotejo)
    if faltan:
        raise SystemExit(f"el cotejo de {slug} no declara {', '.join(sorted(faltan))}: sin eso "
                         f"no se sabe cuándo se leyó ni contra qué")
    return cotejo


def aplicar_cotejo(cuerpo: str, cotejo: dict, slug: str) -> str:
    """Aplica las correcciones leídas contra el PDF. Cada una tiene que coincidir UNA vez.

    Plantarse cuando no coincide es el punto del control, no un estorbo: significa que el OCR ya
    no devuelve el texto que la corrección arregla —otra versión de tesseract, otro PDF— y ahí
    trasladarla a ciegas sería escribir en el fallo algo que nadie leyó. Y coincidir DOS veces es
    igual de grave: `39) Que en primera instancia` aparece en el voto de la mayoría y en el de
    Petracchi, así que una sustitución sin contexto corregiría el renglón equivocado.
    """
    for n, c in enumerate(cotejo["correcciones"], 1):
        veces = cuerpo.count(c["de"])
        if veces != 1:
            raise SystemExit(
                f"{slug}: la corrección {n} (página {c.get('pagina')}) coincide {veces} veces y "
                f"tiene que coincidir una:\n    {c['de'][:70]!r}\n"
                f"  El OCR dejó de devolver lo que esa corrección arregla. Hay que volver a leer "
                f"esa página del PDF y rehacer ocr/correcciones/{slug}.json.")
        cuerpo = cuerpo.replace(c["de"], c["a"], 1)
    return cuerpo


def recuperar(ficha: dict, idioma: str, herramienta: str, verboso: bool = True) -> dict:
    slug = ficha["slug"]
    pdf = JURIS / f"{slug}.pdf"
    if not pdf.exists():
        raise SystemExit(f"no está el PDF de {slug}")
    hash_pdf = sha256(pdf.read_bytes())
    total = paginas(pdf)

    arranque = time.time()
    cuerpo = []
    with tempfile.TemporaryDirectory(prefix="reocr-") as tmp:
        taller = Path(tmp)
        for n in range(1, total + 1):
            cuerpo.append(f"--- pagina {n} de {total} ---\n\n"
                          f"{leer_pagina(pdf, n, idioma, taller)}")
            if verboso and n % 10 == 0:
                print(f"    {slug}: {n}/{total} páginas", flush=True)

    # El cotejo se aplica al CUERPO y nunca al encabezado: el encabezado lo escribe este script
    # y corregirlo sería corregir el generador, no la lectura de la página.
    cotejo = cargar_cotejo(slug)
    leido = "\n\n".join(cuerpo)
    if cotejo:
        leido = aplicar_cotejo(leido, cotejo, slug)
    texto = encabezado(ficha, pdf, hash_pdf, total, idioma, herramienta, cotejo) + leido + "\n"

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / f"{slug}.txt"
    destino.write_text(texto, encoding="utf-8")
    if verboso:
        print(f"    {slug}: {total} páginas en {time.time() - arranque:.0f} s "
              f"-> ocr/{destino.name} ({len(texto):,} caracteres)"
              + (f", {len(cotejo['correcciones'])} correcciones aplicadas" if cotejo else ""))
    ficha_proc = {
        "archivo": destino.name,
        "pdf": pdf.name,
        "sha256_pdf": hash_pdf,
        # El hash es del archivo COMO QUEDA, cotejo incluido: es el único que se puede volver a
        # contrastar contra algo que exista. Del texto previo al cotejo no se guarda hash porque
        # no se guarda el texto, y un hash de lo que no está describe un archivo fantasma.
        "sha256_texto": sha256(texto.encode("utf-8")),
        "paginas": total,
        "generado": _veredictos.hoy(),
        "herramienta": f"{herramienta}, -l {idioma} --psm 6, pdftoppm -r {RESOLUCION}",
    }
    if cotejo:
        ficha_proc["cotejado"] = cotejo["cotejado_el"]
        ficha_proc["correcciones"] = len(cotejo["correcciones"])
    return ficha_proc


def fichas() -> dict[str, dict]:
    datos = json.loads(MANIFIESTO.read_text(encoding="utf-8"))["fallos"]
    lista = datos if isinstance(datos, list) else list(datos.values())
    return {f["slug"]: f for f in lista}


def defectuosos() -> list[str]:
    if not VEREDICTOS.exists():
        raise SystemExit(f"no encontré {VEREDICTOS.name}: pasa los slugs a mano")
    lecturas = _veredictos.cargar(VEREDICTOS, "lecturas", vacio={})[1]
    return sorted(s for s, v in lecturas.items() if v.get("estado") in RECUPERABLES)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("slugs", nargs="*", help="por defecto, los defectuosos del veredicto")
    ap.add_argument("--idioma", default="spa", help="idioma de tesseract (spa)")
    ap.add_argument("--listar", action="store_true", help="decir qué haría y salir")
    args = ap.parse_args()

    if not args.listar:
        _externos.exigir("pdfinfo", "pdftoppm", "tesseract")

    catalogo = fichas()
    elegidos = args.slugs or defectuosos()
    desconocidos = [s for s in elegidos if s not in catalogo]
    if desconocidos:
        raise SystemExit(f"no están en fallos.json: {', '.join(desconocidos)}")

    if args.listar:
        for s in elegidos:
            pdf = JURIS / f"{s}.pdf"
            print(f"  {s}  ({paginas(pdf) if pdf.exists() else '?'} páginas)")
        return 0

    if args.idioma not in idiomas_tesseract():
        raise SystemExit(f"tesseract no tiene el idioma '{args.idioma}'. "
                         "Para español: brew install tesseract-lang")
    herramienta = version_tesseract()
    print(f"{herramienta} · idioma {args.idioma} · {len(elegidos)} documentos")

    registro = {}
    if (SALIDA / "procedencia.json").exists():
        registro = json.loads((SALIDA / "procedencia.json").read_text(encoding="utf-8"))
    registro.setdefault("_descripcion",
                        "Texto recuperado por OCR local de PDF con la capa de texto arruinada. "
                        "Derivación, no descarga: no es publicación oficial. "
                        "sha256_pdf es el del PDF del que salió; si el PDF cambia, hay que "
                        "regenerar.")
    registro.setdefault("fallos", {})
    for s in elegidos:
        registro["fallos"][s] = recuperar(catalogo[s], args.idioma, herramienta)
    (SALIDA / "procedencia.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"procedencia: ocr/procedencia.json ({len(registro['fallos'])} documentos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
