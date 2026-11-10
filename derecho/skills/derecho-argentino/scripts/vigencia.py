#!/usr/bin/env python3
"""Desde cuándo rige una norma, a partir de la fecha de su publicación oficial.

Una ley que no fija fecha propia rige, por el art. 5 del CCyCN, «después del octavo día de su
publicación oficial»; el art. 6 manda no contar el día de la publicación y contar días corridos.
Es una cuenta de calendario, y una cuenta de calendario hecha a ojo es el error que la sección 2
de la skill no admite. La regla no sale de memoria: los arts. 5 y 6 se leen del consolidado del
CCyCN en `fuentes/normas/` y se imprimen con su procedencia —del 6, las dos oraciones que hacen
la cuenta—. Si falta alguno, el script se planta.

Uso:
    python3 vigencia.py --bo 2026-10-30                          # sin fecha propia
    python3 vigencia.py --bo 2026-10-30 --jurisdiccion pba       # una ley provincial
    python3 vigencia.py --bo 2026-03-09 --desde 2026-09-05       # la norma fija su fecha
    python3 vigencia.py --bo 2026-01-02 --clase otra             # un decreto, una resolución

**Lo que NO resuelve, y por eso emite marcador:**

- Que la norma no fije su propia fecha ni condicione su aplicación a una reglamentación. Eso se
  lee en la norma; con `--desde` se le pasa la fecha que ella fija.
- Que el art. 5 alcance a una ley provincial. Es la regla del Título Preliminar y se aplica a
  falta de otra, pero cada jurisdicción puede tener la suya: con `--jurisdiccion` distinta de
  `nacional`, el marcador lo dice.
- Que alcance a un decreto o a una resolución: el art. 5 habla de leyes, y un reglamento puede
  tener la regla de su propio régimen. Con `--clase otra`, el marcador lo dice.

La fecha que imprime es el primer día en que la norma rige. Para un hecho de ese mismo día o
posterior se aplica la norma nueva; para uno anterior, la que regía, y eso decide el derecho
aplicable antes que cualquier otra cosa.

Códigos de salida: 0 calculó; 2 falta el repo o el texto de los arts. 5 y 6.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import articulo
from perfil import hoy
from plazos import DIAS_DE_LA_SEMANA

PLAZO_SUPLETORIO = 8   # «después del octavo día de su publicación oficial» (art. 5 CCyCN)
FUENTE_REGLA = "ccycn-26994"
# Las dos oraciones del art. 6 que hacen la cuenta: sin la primera se contaría el día de la
# publicación, y sin la segunda se saltearían los inhábiles.
COMPUTO = ("queda éste excluido del cómputo", "días completos y continuos")


def con_dia(f: date) -> str:
    return f"{f.isoformat()} ({DIAS_DE_LA_SEMANA[f.weekday()]})"


def calcular(bo: date, desde: date | None = None) -> dict:
    """Sin `desde`: el octavo día corrido sin contar el de publicación, y el siguiente."""
    if desde is not None:
        return {"rige": desde, "octavo": None, "regla": "fecha propia"}
    octavo = bo + timedelta(days=PLAZO_SUPLETORIO)
    return {"rige": octavo + timedelta(days=1), "octavo": octavo, "regla": "art. 5 CCyCN"}


def _plano(lineas) -> str:
    return " ".join(l.strip() for l in lineas if l.strip())


def leer_regla(repo=None):
    """(procedencia, art. 5, [oraciones del art. 6]) del CCyCN desde fuentes/, o None si falta
    alguno de los dos o el art. 6 no trae las oraciones de `COMPUTO`."""
    normas = articulo.carpeta_normas(repo)
    archivo = None if normas is None else normas / f"{FUENTE_REGLA}.txt"
    if archivo is None or not archivo.is_file():
        return None
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    bloques = articulo.anexos(lineas)
    if len(bloques) < 2 or "5" not in bloques[1] or "6" not in bloques[1]:
        return None
    oraciones = [o.strip() + "." for o in _plano(bloques[1]["6"]).split(". ")]
    computo = [next((o for o in oraciones if clave in o), None) for clave in COMPUTO]
    if None in computo:
        return None
    return articulo.encabezado(lineas), _plano(bloques[1]["5"]), computo


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bo", required=True, type=date.fromisoformat,
                   help="fecha de la publicación oficial, AAAA-MM-DD")
    p.add_argument("--desde", type=date.fromisoformat,
                   help="la fecha que la propia norma fija para su vigencia, si la fija")
    p.add_argument("--jurisdiccion", choices=("nacional", "pba", "caba", "otra"),
                   default="nacional", help="de quién es la norma")
    p.add_argument("--clase", choices=("ley", "otra"), default="ley",
                   help="ley, u otra: decreto, resolución, acordada")
    p.add_argument("--repo", help="ruta al repo, si no está configurada")
    a = p.parse_args(argv)

    print("VIGENCIA DE UNA NORMA")
    print()
    print(f"  Publicación oficial        {con_dia(a.bo)}")
    print(f"  Jurisdicción               {a.jurisdiccion}")
    print(f"  Clase                      {a.clase}")
    print(f"  Fecha propia               {con_dia(a.desde) if a.desde else 'no se informó'}")
    print()

    r = calcular(a.bo, a.desde)
    marcadores = []
    if a.desde is None:
        regla = leer_regla(a.repo)
        if regla is None:
            print("  [CONFIGURACIÓN INCOMPLETA: texto de los arts. 5 y 6 del CCyCN - no están "
                  f"en fuentes/normas/{FUENTE_REGLA}.txt, y la regla no se aplica de memoria]")
            return 2
        cabecera, texto, computo = regla
        print("  Regla, leída de fuentes/:")
        for linea in cabecera:
            print(f"    {linea}")
        print(f"    art. 5, anexo 1 · {texto}")
        for oracion in computo:
            print(f"    art. 6, anexo 1 · «{oracion}»")
        print()
        print(f"  Octavo día                 {con_dia(r['octavo'])}")
        marcadores.append(
            "[VERIFICAR VIGENCIA: fecha de entrada en vigencia - confirmar en el texto que la "
            "norma no fija fecha propia ni condiciona su aplicación a una reglamentación]")
        if a.jurisdiccion != "nacional":
            marcadores.append(
                "[VERIFICAR VIGENCIA: entrada en vigencia de una norma local - el art. 5 CCyCN "
                "rige a falta de regla propia de la jurisdicción; verificar que no la tenga "
                "antes de usar esta fecha]")
        if a.clase != "ley":
            marcadores.append(
                "[VERIFICAR VIGENCIA: entrada en vigencia de un reglamento - el art. 5 CCyCN "
                "habla de leyes; verificar la regla del régimen de la norma antes de usar esta "
                "fecha]")
    else:
        print("  Regla: la que fija la propia norma (art. 5 CCyCN, «o desde el día que ellas")
        print("  determinen»).")
        if a.desde < a.bo:
            marcadores.append(
                "[VERIFICAR VIGENCIA: fecha propia anterior a la publicación - una norma que "
                "se declara vigente antes de publicarse plantea retroactividad; leer la "
                "cláusula antes de usar esta fecha]")
    print(f"  RIGE DESDE                 {con_dia(r['rige'])}")
    hoy_ = hoy()
    print(f"  Hoy, {hoy_.isoformat()}: {'ya rige' if hoy_ >= r['rige'] else 'todavía no rige'}.")
    if marcadores:
        print()
        print("  MARCADORES")
        for m in marcadores:
            print(f"    {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
