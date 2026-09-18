#!/usr/bin/env python3
"""El sobre común de los archivos de veredicto del repositorio.

Un archivo de veredicto guarda lo que alguien LEYÓ sobre los candidatos que reporta un
detector, con fecha. **El porqué, la tabla de los nueve archivos y el motivo de que la carga
NO se unifique están en `docs/DESARROLLO.md`, sección «Los archivos de veredicto».** Acá va
sólo lo que hace falta para usar el módulo.

EL SOBRE, igual en los nueve:

    _descripcion   qué es y quién lo consume. Obligatorio.
    _criterio      por qué existe y cómo se decide un veredicto. Opcional.
    _vocabulario   los valores válidos del veredicto, con su significado. Opcional.
    fijado         fecha del último repaso, ISO. Obligatorio.
    nota           por qué quedó en este estado. Opcional, pero se completa al fijar.
    <carga>        el contenido, con la forma que le sirva a su consumidor.

`derecho/fuentes/normas/revisiones.json` usa el mismo sobre y NO pasa por acá: vive dentro
del plugin, que tiene que ser autocontenido, y lo carga `derecho/fuentes/scripts/_comun.py`.
Lo que mantiene alineados a los nueve es `TestSobreDeLosVeredictos`.
"""
import json
import pathlib
from datetime import datetime, timedelta, timezone

OBLIGATORIAS = ("_descripcion", "fijado")
OPCIONALES = ("_criterio", "_vocabulario", "nota")
DEL_SOBRE = OBLIGATORIAS + OPCIONALES


class SobreInvalido(ValueError):
    """El archivo no trae el sobre común: se dice cuál falta, no se adivina un default."""


def cargar(ruta: pathlib.Path, carga: str, vacio=None):
    """Devuelve (sobre, contenido). Si el archivo no está, contenido es `vacío`.

    No se tolera un sobre incompleto en un archivo que SI existe: un veredicto sin fecha no
    se puede envejecer, y uno sin descripción no se sabe quien lo consume.
    """
    if not ruta.exists():
        return ({"_descripcion": "", "fijado": None}, vacio)
    d = json.loads(ruta.read_text(encoding="utf-8"))
    faltan = [k for k in OBLIGATORIAS if not d.get(k)]
    if faltan:
        raise SobreInvalido(f"{ruta.name}: falta {', '.join(faltan)} en el sobre")
    if carga not in d:
        raise SobreInvalido(f"{ruta.name}: no trae la carga `{carga}`")
    return ({k: d[k] for k in DEL_SOBRE if k in d}, d[carga])


# La misma zona que `derecho/fuentes/scripts/_comun.py` y que la skill, y por los mismos dos
# motivos: una fecha de este repositorio se lee como "el día en que lo hicimos", y el offset va
# FIJO porque el workflow de CI corre en UTC y `astimezone()` haría fechar distinto según dónde
# se corra. Está en tres lugares porque los tres árboles de scripts no comparten módulo, a
# propósito; que no se separen lo sostiene `TestUnaSolaZonaHoraria`.
ARGENTINA = timezone(timedelta(hours=-3))


def hoy() -> str:
    """La fecha de hoy en hora argentina, ISO."""
    return datetime.now(ARGENTINA).date().isoformat()


def guardar(ruta: pathlib.Path, sobre: dict, carga: str, contenido, nota: str = "") -> None:
    """Reescribe el archivo poniendo la fecha de hoy. `nota` reemplaza a la anterior si viene."""
    d = {k: sobre[k] for k in DEL_SOBRE if k in sobre and k != "fijado"}
    d["fijado"] = hoy()
    if nota:
        d["nota"] = nota
    d[carga] = contenido
    orden = {k: d[k] for k in DEL_SOBRE if k in d}
    orden[carga] = d[carga]
    ruta.write_text(json.dumps(orden, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
