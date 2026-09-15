#!/usr/bin/env python3
"""Binarios que no son Python y que algunas herramientas necesitan.

Existe por un modo de fallar específico: cuando falta `pdftotext`, el auditor de fechas
metia el `FileNotFoundError` en el mismo `except` que usa para un PDF roto y seguia. El
resumen final decía `0 A REVISAR` con el auditor apagado -- en una máquina sin poppler, los
64 fallos pasaban sin mirarse y el código de salida era 0.

La regla es la misma que para una medida que se equivoca: si la herramienta no puede medir,
lo dice y se planta. No hay veredicto verde por ausencia de instrumento.
"""
import shutil
import sys

# Que instalar, por plataforma. Se nombra el proyecto además del paquete porque los nombres
# de paquete cambian y el proyecto no.
PROVEEDOR = {
    "pdftotext": "poppler",
    "pdftoppm": "poppler",
    "pdfinfo": "poppler",
    "tesseract": "tesseract",
}
COMO = {
    "poppler": {
        "darwin": "brew install poppler",
        "linux": "apt install poppler-utils   (o el equivalente de tu distribución)",
        "win32": "choco install poppler   o   scoop install poppler",
    },
    "tesseract": {
        "darwin": "brew install tesseract tesseract-lang",
        "linux": "apt install tesseract-ocr tesseract-ocr-spa",
        "win32": "choco install tesseract   (agregar el idioma spa)",
    },
}


def falta(binario: str) -> bool:
    """True si el binario no está en el PATH. En Windows shutil.which respeta PATHEXT."""
    return shutil.which(binario) is None


def instruccion(binario: str) -> str:
    proyecto = PROVEEDOR.get(binario, binario)
    receta = COMO.get(proyecto, {})
    plataforma = ("darwin" if sys.platform == "darwin"
                  else "win32" if sys.platform.startswith("win") else "linux")
    orden = receta.get(plataforma, f"instalar {proyecto}")
    return (f"falta `{binario}`, que viene con {proyecto} y no es un paquete de Python.\n"
            f"  Instalarlo con:  {orden}\n"
            f"  Y volver a correr esto.")


def exigir(*binarios: str) -> None:
    """Corta con un mensaje legible si falta alguno. Nunca deja seguir a medias."""
    ausentes = [b for b in binarios if falta(b)]
    if ausentes:
        raise SystemExit("\n".join(instruccion(b) for b in ausentes))
