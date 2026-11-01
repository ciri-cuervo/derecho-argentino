"""Lectura validada de las tablas de `fuentes/datos/` que consumen las calculadoras.

Un renglón mal cargado no puede pasar como dato: una vigencia escrita `2026-9-1` se ordena
como texto antes que `2026-10-01`, un valor en cero termina en una división por cero, y un
período repetido pisa al anterior. Las tres cosas dan un número con cara de correcto, así que
acá cortan con el archivo y el renglón.
"""
from __future__ import annotations

import csv
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

PERIODO = re.compile(r"\d{4}-(0[1-9]|1[0-2])")


class TablaInvalida(ValueError):
    """Un renglón de una tabla de datos que no se puede usar."""


def _clave(texto: str, formato: str) -> str:
    texto = texto.strip()
    if formato == "periodo":
        if not PERIODO.fullmatch(texto):
            raise ValueError(f"período '{texto}' no es AAAA-MM")
        return texto
    return date.fromisoformat(texto).isoformat()


def leer_tabla(ruta, columna_clave: str, columna_valor: str, formato: str = "fecha") -> list:
    """Las filas con valor, ordenadas por la clave, con `valor` ya convertido a Decimal.

    Los renglones vacíos y los comentarios con `#` se saltean, y también las filas con el valor
    vacío: así se cargan las vigencias anunciadas sin monto todavía. `formato` es `fecha`
    (AAAA-MM-DD) o `periodo` (AAAA-MM).
    """
    ruta = Path(ruta)
    renglones = [(n, l) for n, l in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1)
                 if l.strip() and not l.lstrip().startswith("#")]
    if not renglones:
        return []
    lector = csv.DictReader([l for _, l in renglones])
    filas, vistas = [], {}
    for (numero, _), fila in zip(renglones[1:], lector):
        crudo = (fila.get(columna_valor) or "").strip()
        if not crudo:
            continue
        donde = f"{ruta.name}, renglón {numero}"
        try:
            clave = _clave(fila.get(columna_clave) or "", formato)
        except ValueError as e:
            raise TablaInvalida(f"{donde}: {columna_clave} ilegible ({e})") from None
        try:
            valor = Decimal(crudo)
        except InvalidOperation:
            raise TablaInvalida(f"{donde}: {columna_valor} '{crudo}' no es un número") from None
        if not valor.is_finite() or valor <= 0:
            raise TablaInvalida(f"{donde}: {columna_valor} '{crudo}' tiene que ser positivo")
        if clave in vistas:
            raise TablaInvalida(f"{donde}: {columna_clave} {clave} repetido (ya estaba en el "
                                f"renglón {vistas[clave]})")
        vistas[clave] = numero
        fila = dict(fila, **{columna_clave: clave})
        fila["valor"] = valor
        filas.append(fila)
    filas.sort(key=lambda f: f[columna_clave])
    return filas
