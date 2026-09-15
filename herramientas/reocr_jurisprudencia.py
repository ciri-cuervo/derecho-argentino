#!/usr/bin/env python3
"""Recupera por OCR el texto de los fallos cuyo PDF trae la capa de texto arruinada.

    python3 herramientas/reocr_jurisprudencia.py --listar
    python3 herramientas/reocr_jurisprudencia.py                 # los defectuosos del veredicto
    python3 herramientas/reocr_jurisprudencia.py csjn-bazterrica-fallos-308-1392

La basura de esos documentos no esta en el papel sino en una capa de texto vieja que
`pdftotext` se limita a copiar: en "Bazterrica" devolvia `El] \\^<+]Ky puede P^+*+y un ^Fy dia`
donde la pagina dice "El sujeto puede un dia probar la droga". Esto vuelve a leer las
imagenes con tesseract y deja el resultado en `argentina/fuentes/jurisprudencia/ocr/`.

Lo que sale de aca NO es publicacion oficial ni reemplaza al PDF: es una relectura local, y
cada cita literal se coteja contra la pagina antes de ir a un escrito. Por eso vive en su
propia carpeta, con la procedencia y el hash del PDF del que salio.

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
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _externos
import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
JURIS = RAIZ / "argentina" / "fuentes" / "jurisprudencia"
SALIDA = JURIS / "ocr"
MANIFIESTO = JURIS / "fallos.json"
VEREDICTOS = RAIZ / "herramientas" / "lecturas-ocr.json"

# Un veredicto `layout` se arregla con `pdftotext -layout` y no necesita esto.
RECUPERABLES = ("destruido", "sustituciones")

RESOLUCION = 300
SEPARADOR = "=" * 78


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
        raise SystemExit(f"no pude contar las paginas de {pdf.name}")
    return int(hallado.group(1))


def sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def leer_pagina(pdf: Path, n: int, idioma: str, taller: Path) -> str:
    """Una pagina: se rasteriza a PNG y se OCRea.

    Va por archivo y no por tuberia porque la salida a stdout de pdftoppm devuelve cero bytes
    en la build de poppler de Homebrew, sin error: el PNG intermedio es mas predecible.
    """
    prefijo = taller / "pagina"
    png = prefijo.with_suffix(".png")
    png.unlink(missing_ok=True)
    _correr(["pdftoppm", "-png", "-r", str(RESOLUCION), "-f", str(n), "-l", str(n),
             "-singlefile", str(pdf), str(prefijo)])
    if not png.exists():
        raise SystemExit(f"pdftoppm no dejo el PNG de la pagina {n} de {pdf.name}")
    txt = _correr(["tesseract", str(png), "stdout", "-l", idioma, "--psm", "6"])
    png.unlink(missing_ok=True)
    return txt.decode("utf-8", errors="replace").rstrip()


def encabezado(ficha: dict, pdf: Path, hash_pdf: str, total: int, idioma: str,
               herramienta: str) -> str:
    fecha = ficha.get("fecha", "")
    dudosa = fecha.endswith("-01-01")
    return "\n".join([
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
        f"Generado:         {date.today().isoformat()}",
        f"Herramienta:      {herramienta}, -l {idioma} --psm 6, pdftoppm -r {RESOLUCION}",
        "",
        "TEXTO RECUPERADO POR OCR LOCAL. No se bajo de la fuente: la capa de texto que traia el",
        "PDF estaba arruinada y esto es una relectura de las imagenes de la pagina. NO es",
        "publicacion oficial y no reemplaza al PDF. Para transcribir un considerando a un escrito,",
        "cotejar contra la pagina del PDF: el numero de pagina esta marcado abajo.",
        "",
        "Regenerar: python3 herramientas/reocr_jurisprudencia.py " + ficha["slug"],
        SEPARADOR,
        "",
    ])


def recuperar(ficha: dict, idioma: str, herramienta: str, verboso: bool = True) -> dict:
    slug = ficha["slug"]
    pdf = JURIS / f"{slug}.pdf"
    if not pdf.exists():
        raise SystemExit(f"no esta el PDF de {slug}")
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
                print(f"    {slug}: {n}/{total} paginas", flush=True)
    texto = encabezado(ficha, pdf, hash_pdf, total, idioma, herramienta) + "\n\n".join(cuerpo) + "\n"

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / f"{slug}.txt"
    destino.write_text(texto, encoding="utf-8")
    if verboso:
        print(f"    {slug}: {total} paginas en {time.time() - arranque:.0f} s "
              f"-> ocr/{destino.name} ({len(texto):,} caracteres)")
    return {
        "archivo": destino.name,
        "pdf": pdf.name,
        "sha256_pdf": hash_pdf,
        "sha256_texto": sha256(texto.encode("utf-8")),
        "paginas": total,
        "generado": date.today().isoformat(),
        "herramienta": f"{herramienta}, -l {idioma} --psm 6, pdftoppm -r {RESOLUCION}",
    }


def fichas() -> dict[str, dict]:
    datos = json.loads(MANIFIESTO.read_text(encoding="utf-8"))["fallos"]
    lista = datos if isinstance(datos, list) else list(datos.values())
    return {f["slug"]: f for f in lista}


def defectuosos() -> list[str]:
    if not VEREDICTOS.exists():
        raise SystemExit(f"no encontre {VEREDICTOS.name}: pasa los slugs a mano")
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
                        "Derivacion, no descarga: no es publicacion oficial. "
                        "sha256_pdf es el del PDF del que salio; si el PDF cambia, hay que "
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
