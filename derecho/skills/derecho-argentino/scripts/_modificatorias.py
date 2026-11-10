"""Qué norma del catálogo modifica a cuál, y si el texto consolidado ya lo refleja.

`normas.json` declara la relación en la norma que modifica: `"modifica": ["pba-ley-13927"]`.
Va ahí y no en la modificada porque es la que llega después, y quien la agrega al catálogo es
quien sabe qué toca. Sirve a dos lectores:

- `articulo.py`, que cuando no encuentra un artículo en el consolidado lo busca en sus
  modificatorias —el art. 28 quater de la Ley 13.927 vive, por ahora, sólo en la Ley 15.657— y
  cuando sí lo encuentra avisa si el consolidado no menciona una modificatoria declarada;
- `estado.py`, que reporta cada consolidado que todavía no menciona a quien lo modifica.

**Mencionar no es incorporar.** Lo que se mide es si el número de la modificatoria aparece en
el texto de la modificada precedido por su clase —«Ley», «Decreto»—, que es como los
consolidados anotan cada sustitución. Que aparezca no prueba que el artículo que importa esté
al día; que no aparezca sí prueba que el consolidado no la recorrió. Es una alarma de una sola
dirección, y así se la lee.

**Un texto original no se atrasa: no se actualiza nunca.** InfoLEG sirve dos cosas distintas
para la misma norma —`texact.htm`, el consolidado, y `norma.htm`, el texto tal como se publicó—, y
normas.gba ofrece el original en PDF. Un original no va a mencionar a su modificatoria por más
que se lo vuelva a bajar, así que reportarlo como atrasado es una alarma que suena siempre:
`atrasados()` lo deja afuera. `articulo.py` igual avisa, porque leer un original sin saber que
lo modificaron es el mismo error.

Una designación con menos de tres cifras —«Res. SRT 7/2026»— no se mide: el número suelto
aparece en cualquier texto y la medida daría por mencionada una norma que no lo está.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

# La clase y el número con que un título del catálogo designa a su norma: «Ley 15.657 PBA - ...»,
# «Decreto 1253/2026 - ...», «Decreto-Ley 9650/80 ...».
DESIGNACION = re.compile(
    r"^(?P<clase>Ley|Decreto-Ley|Decreto|DNU|Resoluci[oó]n|Res\.)\s+(?:N[°º.]?\s*)?"
    r"(?P<numero>\d{1,3}(?:\.\d{3})+|\d+)")

# Qué palabras pueden preceder al número en el texto que lo menciona, por clase de norma.
CLASES = {
    "Ley": r"Ley(?:es)?",
    "Decreto-Ley": r"Decreto[- ]Ley|Dec(?:reto)?\.?-?Ley",
    "Decreto": r"Decreto|Dec\.|DNU",
    "DNU": r"Decreto|Dec\.|DNU",
    "Resolución": r"Resoluci[oó]n|Res\.",
    "Resolucion": r"Resoluci[oó]n|Res\.",
    "Res.": r"Resoluci[oó]n|Res\.",
}


def catalogo(normas: Path) -> list[dict]:
    return json.loads((normas / "normas.json").read_text(encoding="utf-8"))["normas"]


def modificadoras_de(slug: str, entradas: list[dict]) -> list[dict]:
    return [n for n in entradas if slug in (n.get("modifica") or [])]


def designacion(titulo: str):
    """(«Ley», «15.657») del título, o None si no tiene una designación que se pueda medir."""
    m = DESIGNACION.match(titulo or "")
    if not m or len(re.sub(r"\D", "", m.group("numero"))) < 3:
        return None
    return m.group("clase"), m.group("numero")


def menciona(texto: str, titulo_modificadora: str):
    """True si el texto menciona a la norma del título, False si no, None si no se puede medir."""
    d = designacion(titulo_modificadora)
    if d is None:
        return None
    clase, numero = d
    cifras = re.sub(r"\D", "", numero)
    # Con o sin el punto de los miles: «15.657» y «15657» son la misma ley.
    patron_numero = re.escape(cifras[:-3]) + r"\.?" + re.escape(cifras[-3:]) \
        if len(cifras) > 3 else re.escape(cifras)
    clase_re = re.compile(rf"(?:{CLASES.get(clase, re.escape(clase))})", re.I)
    for m in re.finditer(rf"(?<![\d.]){patron_numero}(?!\d)", texto):
        # La clase tiene que estar cerca y antes: «Leyes 14.879, 15.000 y 15.657» cuenta.
        if clase_re.search(texto[max(0, m.start() - 60):m.start()]):
            return True
    return False


def nombre(entrada: dict) -> str:
    """«Ley 15.657 PBA», la parte del título antes de la raya, para mostrar."""
    return (entrada.get("titulo") or entrada["slug"]).split(" - ")[0].strip()


def es_original(entrada: dict) -> bool:
    """True si la URL de la entrada sirve el texto tal como se publicó, que no se actualiza."""
    url = (entrada.get("url") or "").lower()
    return (("infoleg.gob.ar" in url and url.endswith("/norma.htm"))
            or ("normas.gba.gob.ar" in url and url.endswith(".pdf")))


def sin_reflejar(slug: str, texto: str, entradas: list[dict]) -> list[dict]:
    """Las modificatorias declaradas de `slug` que su texto todavía no menciona."""
    return [m for m in modificadoras_de(slug, entradas)
            if menciona(texto, m.get("titulo", "")) is False]


def atrasados(normas: Path) -> list[tuple[dict, dict]]:
    """Cada par (modificada, modificatoria) con el texto consolidado de la primera en disco y
    sin mención. Los originales no entran: ver `es_original()`."""
    entradas = catalogo(normas)
    por_slug = {n["slug"]: n for n in entradas}
    salida = []
    for mod in entradas:
        for base in mod.get("modifica") or []:
            archivo = normas / f"{base}.txt"
            if base not in por_slug or not archivo.is_file() or es_original(por_slug[base]):
                continue
            if menciona(archivo.read_text(encoding="utf-8"), mod.get("titulo", "")) is False:
                salida.append((por_slug[base], mod))
    return salida
