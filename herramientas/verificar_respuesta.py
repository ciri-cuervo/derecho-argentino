#!/usr/bin/env python3
"""Revisa una respuesta ya producida: que sus marcadores sean del vocabulario y estén verbatim.

POR QUÉ EXISTE

Las rúbricas de `evals/` puntúan el CONTENIDO del análisis. Ninguna puede detectar lo que
pasa después de razonar bien: que el marcador se reescriba, que se le cambie una tilde, que
aparezca uno que nadie declaró. Eso no falla ruidosamente -sale igual, con forma de marcador-
y lo copia al escrito quien confía en la herramienta.

`marcadores.md` declara el vocabulario canónico en sus encabezados y los contraejemplos en su
tabla de "No usar". Acá se acepta solo lo que figure en alguna de las dos listas, y se reclama
por separado el caso más engañoso: el nombre que existe pero escrito distinto -sin tilde, en
minúscula, con un espacio de más-, que a ojo pasa por bueno.

QUÉ MIDE Y QUÉ NO

Mide la FORMA del marcador, no si correspondía emitirlo. Que el análisis haya puesto
`[VERIFICAR PLAZO: ...]` donde hacía falta un `[ALERTA PLAZO FATAL: ...]` es un error de
fondo y lo juzga la rúbrica; acá se contesta la pregunta previa, que es mecánica.

No se instala con el plugin: vive fuera de `derecho/`.

Uso, desde la raíz del repositorio:

    python3 herramientas/verificar_respuesta.py respuesta.md [...]
    python3 herramientas/verificar_respuesta.py --vocabulario     # imprime la lista canónica

Sale con código 1 si encontró un marcador que no pertenece al vocabulario.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
VOCABULARIO = RAIZ / "derecho" / "skills" / "derecho-argentino" / "references" / "marcadores.md"

# Las clases de letras se escriben una sola vez: una Ü o una Ñ olvidada no hace fallar el
# control, lo hace IGNORAR el marcador en silencio, que es peor. Ya pasó en el repo.
MAYUSCULAS = "A-ZÁÉÍÓÚÜÑ"
LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
# El cuerpo del nombre admite también dígito y barra: sin ellos, `[MARCADOR 2: ...]` y
# `[FALTA DATO/PRUEBA: ...]` no eran ni candidatos y el control los IGNORABA en silencio, que
# es el mismo modo de falla que la Ü.
#
# El punto NO entra, y eso se probó: con él, `[Verificar el plazo vigente del art. 11.]` --prosa
# entre corchetes, que aparece en un resultado de eval-- pasaba a ser candidato y salía como
# marcador desconocido. Un control que reclama texto correcto se apaga solo. El costo es que un
# `[ART. SIN NORMA: ...]` mal escrito no se detecta; se prefiere eso a la falsa alarma.
CUERPO = r"0-9/"

NOMBRE = re.compile(r"\[([" + MAYUSCULAS + "][" + MAYUSCULAS + CUERPO + r" \-]{3,})(?::|\])")
CUALQUIERA = re.compile(r"\[([" + LETRAS + "][" + LETRAS + CUERPO + r" \-]{3,})(?::|\])")


def plano(s: str) -> str:
    """Minúsculas, sin tildes y con los espacios colapsados: la forma para COMPARAR."""
    sin = unicodedata.normalize("NFD", s)
    sin = "".join(c for c in sin if unicodedata.category(c) != "Mn")
    return " ".join(sin.lower().split())


def vocabulario(ruta: pathlib.Path = VOCABULARIO) -> tuple[set[str], set[str]]:
    """Devuelve (canónicos, declarados-como-contraejemplo)."""
    texto = ruta.read_text(encoding="utf-8")
    canonicos = set(re.findall(r"^### [A-D]\d+ · (.+)$", texto, re.M))
    contraejemplos = set(re.findall(
        r"`\[([" + MAYUSCULAS + "][" + MAYUSCULAS + r" \-]{3,})[\]:]", texto))
    return canonicos, contraejemplos


def revisar(texto: str, canonicos: set[str], contraejemplos: set[str]) -> list[tuple[str, str]]:
    """Devuelve [(clase, nombre)] con clase en {'desconocido', 'mal escrito', 'no usar'}."""
    equivalentes = {plano(c): c for c in canonicos}
    hallazgos = []
    for nombre in dict.fromkeys(CUALQUIERA.findall(texto)):
        if nombre in canonicos:
            continue
        if nombre in contraejemplos:
            hallazgos.append(("no usar", nombre))
        elif plano(nombre) in equivalentes:
            hallazgos.append(("mal escrito", f"{nombre} -> {equivalentes[plano(nombre)]}"))
        else:
            hallazgos.append(("desconocido", nombre))
    return hallazgos


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--vocabulario", action="store_true",
                   help="imprimir la lista canónica y salir")
    p.add_argument("archivos", nargs="*", metavar="respuesta.md")
    a = p.parse_args(argv)

    if not VOCABULARIO.is_file():
        print(f"no encuentro {VOCABULARIO}: corré el script desde la raíz del repo",
              file=sys.stderr)
        return 2
    canonicos, contraejemplos = vocabulario()

    if a.vocabulario:
        for nombre in sorted(canonicos):
            print(f"  [{nombre}: ...]")
        print(f"\n  {len(canonicos)} marcadores canónicos en {VOCABULARIO.name}")
        return 0

    if not a.archivos:
        print("uso: verificar_respuesta.py <respuesta.md> [...]", file=sys.stderr)
        return 2

    roto = 0
    for ruta in a.archivos:
        archivo = pathlib.Path(ruta)
        if not archivo.is_file():
            print(f"{archivo}: no existe", file=sys.stderr)
            return 2
        texto = archivo.read_text(encoding="utf-8")
        usados = [n for n in dict.fromkeys(NOMBRE.findall(texto)) if n in canonicos]
        hallazgos = revisar(texto, canonicos, contraejemplos)
        print(f"{archivo}: {len(usados)} marcadores del vocabulario, {len(hallazgos)} a revisar")
        for clase, nombre in hallazgos:
            print(f"  {clase.upper():12} [{nombre}]")
        roto += len(hallazgos)

    if roto:
        print(f"\n{roto} marcadores fuera del vocabulario. Un marcador se copia tal cual: el")
        print("nombre no se adapta al caso, y si falta uno se agrega a marcadores.md primero.")
        return 1
    total = sum(len([n for n in dict.fromkeys(NOMBRE.findall(
        pathlib.Path(r).read_text(encoding="utf-8"))) if n in canonicos])
        for r in a.archivos)
    if not total:
        print("\nno hay ningún marcador que revisar: esto NO dice que la respuesta esté bien,\ndice que no emitió ninguno")
        return 0
    print("\nmarcadores: todos del vocabulario y escritos como corresponde")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
