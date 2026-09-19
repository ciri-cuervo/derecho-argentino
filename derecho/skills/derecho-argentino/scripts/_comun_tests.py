#!/usr/bin/env python3
"""Lo que comparten las seis suites de `scripts/`: la raíz, el plantón y las clases de letras.

**`test_scripts.py` llegó a 6149 renglones**, tres veces el corte de `Read` que este repositorio
le impone a los módulos —`TestNingunModuloSePasaDelCorteDeRead`—, y ese control hacía `glob`
sobre `references/*.md`, así que no lo miraba. Se partió en seis por lo que cada suite afirma:
las calculadoras, el descargador, la capa offline, el contenido de la skill, la ortografía de la
salida, y lo que queda de plomería del plugin.

Acá vive sólo lo que las seis necesitan. Nada de esto se duplica: duplicarlo era el camino por el
que `RAIZ_DEL_CHECKOUT` terminaba apuntando a otro lado en una de las copias.
"""
import os
import unittest
from pathlib import Path

# La raíz del checkout DONDE VIVE este archivo. No se usa `_raiz.raiz_repo()`, que consulta
# `~/.config/derecho-argentino/config.json` antes de subir desde `__file__`: con la ruta fijada
# y un clon distinto, la suite corría contra OTRO repositorio y daba verde. Un test valida el
# checkout en el que está, no el que diga una configuración de la máquina.
RAIZ_DEL_CHECKOUT = Path(__file__).resolve().parents[4]

MAYUSCULAS = "A-ZÁÉÍÓÚÜÑ"
LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
SEMVER = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.\-]+)?"


def load_tests(cargador, suite, patron):
    """El plugin instalado no trae `herramientas/`, `docs/` ni el manifiesto del marketplace, y
    dos tercios de estas suites miden el repositorio entero. Corridas desde la copia instalada
    daban casi cincuenta rojos que no son defectos del plugin sino ausencia de instrumento, y el
    que las corre concluye que el plugin está roto.

    Así que se plantan en vez de dar verde y en vez de dar rojo: dicen que no están en el
    checkout, nombran la marca que buscaron y no miden nada. La marca es la misma que separa las
    dos disposiciones en `_raiz.es_clon()` —sólo el repo trae `.claude-plugin/marketplace.json`—,
    porque el nombre de la carpeta no alcanza: las dos se llaman `derecho`.

    **Se importa en las seis suites**, y por eso vive acá: `unittest` lo busca por nombre en el
    módulo, así que importarlo alcanza.

    MUTACIÓN que lo comprueba: copiar `derecho/` afuera del repo y correr las suites ahí. Sin
    esto salen 29 fallas y 19 errores; con esto, un SkipTest con el motivo.
    """
    if not (RAIZ_DEL_CHECKOUT / ".claude-plugin" / "marketplace.json").is_file():
        raise unittest.SkipTest(
            f"esta suite mide el repositorio y {RAIZ_DEL_CHECKOUT} no lo es: falta "
            f".claude-plugin/marketplace.json. Se corre desde un clon de "
            f"github.com/ciri-cuervo/derecho-argentino, no desde el plugin instalado.")
    return suite


def sin_color(entorno: dict | None = None) -> dict:
    """El entorno con `NO_COLOR`, para leer la ayuda de un script sin secuencias ANSI.

    `argparse` colorea desde Python 3.13 y los códigos de escape metían ruido en la comparación.
    El color es del terminal, no del programa.
    """
    return {**(entorno if entorno is not None else os.environ), "NO_COLOR": "1"}
