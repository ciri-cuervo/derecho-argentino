#!/usr/bin/env python3
"""El sobre común de los archivos de veredicto del repositorio.

Un archivo de veredicto guarda lo que alguien LEYÓ sobre los candidatos que reporta un
detector. Todos los detectores de este repo reportan candidatos y no culpables --texto
compartido con kb/, leyes citadas sin fuente, capas de OCR, marcas del descargador-- y el
valor de la herramienta se pierde el dia en que su salida deja de mirarse. El archivo de
veredicto es lo que hace que la lista baje en vez de crecer.

Son seis archivos y cada uno se había inventado su propia forma. La fecha del último
repaso llegó a llamarse de tres maneras --`revisado`, `_revisado`, `fijado`-- en tres archivos
que dicen lo mismo. Eso no rompe nada, pero son varias formas de leer mal un mismo concepto, y
el patrón va a seguir apareciendo.

EL SOBRE, igual en los seis. `kb-procedencia.json` ya lo tenía y sirvió de modelo:

    _descripcion   que es y quien lo consume. Obligatorio.
    _criterio      por que existe y como se decide un veredicto. Opcional.
    _vocabulario   los valores válidos del veredicto, con su significado. Opcional.
    fijado         fecha del último repaso, ISO. Obligatorio.
    nota           por que quedo en este estado. Opcional, pero se completa al fijar.
    <carga>        el contenido, con la forma que le sirva a su consumidor.

LA CARGA NO se unifica, y es deliberado. Son tres formas honestas y distintas: un conjunto de
pertenencia (`secuencias`, sin veredicto individual), un mapa de veredictos (`leyes`,
`lecturas`) y un mapa de listas (`revisiones`, porque una norma puede volver con más de un
defecto). Forzar las tres a `ítems: {clave: {veredicto, fecha}}` inflaria la primera cientos de
veces y registraria un veredicto por secuencia que nadie tomo. Un formato unico que miente
sobre el contenido es peor que tres formatos que lo dicen.

`derecho/fuentes/normas/revisiones.json` usa el mismo sobre pero NO pasa por acá: vive dentro
del plugin, que tiene que ser autocontenido para poder instalarse, y no puede importar de
`herramientas/`. Lo carga `derecho/fuentes/scripts/_comun.py`. Lo que los mantiene juntos es
el test del sobre, que los lee a los seis.
"""
import datetime
import json
import pathlib

OBLIGATORIAS = ("_descripcion", "fijado")
OPCIONALES = ("_criterio", "_vocabulario", "nota")
DEL_SOBRE = OBLIGATORIAS + OPCIONALES


class SobreInvalido(ValueError):
    """El archivo no trae el sobre común: se dice cual falta, no se adivina un default."""


def cargar(ruta: pathlib.Path, carga: str, vacio=None):
    """Devuelve (sobre, contenido). Si el archivo no esta, contenido es `vacío`.

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


def guardar(ruta: pathlib.Path, sobre: dict, carga: str, contenido, nota: str = "") -> None:
    """Reescribe el archivo poniendo la fecha de hoy. `nota` reemplaza a la anterior si viene."""
    d = {k: sobre[k] for k in DEL_SOBRE if k in sobre and k != "fijado"}
    d["fijado"] = datetime.date.today().isoformat()
    if nota:
        d["nota"] = nota
    d[carga] = contenido
    orden = {k: d[k] for k in DEL_SOBRE if k in d}
    orden[carga] = d[carga]
    ruta.write_text(json.dumps(orden, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
