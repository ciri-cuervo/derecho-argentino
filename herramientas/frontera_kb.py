#!/usr/bin/env python3
"""Fija el estado de `argentina/kb/`, que es capa 2 y de otro autor.

    python3 herramientas/frontera_kb.py            # informa lo que cambio
    python3 herramientas/frontera_kb.py --fijar    # acepta el estado actual

`argentina/kb/` es la contribucion de Cristian Aboitiz. La frontera de licencia es la ruta,
asi que un texto propio guardado ahi queda clasificado como obra de otro autor. Este script
guarda el sha256 de cada archivo en `kb-procedencia.json` y avisa cuando alguno cambia: no
prohibe editar, obliga a que el cambio sea deliberado y quede registrado.

Sale con codigo 1 si algo cambio. Cero dependencias externas.
"""
import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
KB = RAIZ / "argentina" / "kb"
REGISTRO = Path(__file__).resolve().parent / "kb-procedencia.json"


# Dos decisiones que existen para que esto no de 109 falsos positivos en Windows. Una alarma
# que suena entera invita a callarla con --fijar, y eso acepta a ciegas el estado de kb/, que
# es justo lo que este script existe para impedir.
#
#   La CLAVE va en forma POSIX. `str(Path)` da "perfiles\laboral-CLAUDE.md" en Windows y
#   "perfiles/laboral-CLAUDE.md" en el resto: el registro no matchearia en 106 de 109.
#
#   El HASH va sobre el texto con los saltos normalizados, no sobre los bytes crudos. Un
#   checkout con CRLF cambia los 109 bytes sin que cambie una letra. Los 109 archivos de kb/
#   son texto -108 .md y un .template-, asi que normalizar no deja nada afuera. Un cambio
#   real de contenido sigue moviendo el hash; lo unico que deja de moverlo es el fin de linea.
def huella(p: Path) -> str:
    texto = p.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def huellas() -> dict[str, str]:
    return {
        p.relative_to(KB).as_posix(): huella(p)
        for p in sorted(KB.rglob("*"))
        if p.is_file() and not p.name.startswith(".")
    }


def comparar(actual: dict[str, str], fijado: dict[str, str]):
    return (sorted(set(actual) - set(fijado)),
            sorted(set(fijado) - set(actual)),
            sorted(n for n in set(actual) & set(fijado) if actual[n] != fijado[n]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fijar", action="store_true", help="acepta el estado actual de kb/")
    ap.add_argument("--nota", default="", help="por que cambio, para el registro")
    args = ap.parse_args()

    actual = huellas()
    if args.fijar:
        # El sobre -las claves que empiezan con guion bajo- describe QUE es este archivo y
        # con que criterio se llena, y no depende del estado que se este fijando: se conserva
        # tal cual estaba. Escribirlo de cero lo borraba, y el test que exige el sobre
        # completo solo fallaba despues de un --fijar, que es justo cuando nadie mira.
        sobre = {}
        if REGISTRO.exists():
            try:
                previo = json.loads(REGISTRO.read_text(encoding="utf-8"))
                sobre = {k: v for k, v in previo.items() if k.startswith("_")}
            except (OSError, ValueError):
                sobre = {}
        REGISTRO.write_text(json.dumps({
            **sobre,
            "fijado": date.today().isoformat(),
            "nota": args.nota,
            "archivos": actual,
        }, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        print(f"kb-procedencia.json: {len(actual)} archivos fijados")
        return 0

    if not REGISTRO.exists():
        print("falta kb-procedencia.json: correr con --fijar", file=sys.stderr)
        return 1

    registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
    nuevos, faltantes, cambiados = comparar(actual, registro["archivos"])
    for etiqueta, lista in (("NUEVO", nuevos), ("FALTA", faltantes), ("CAMBIO", cambiados)):
        for nombre in lista:
            print(f"{etiqueta}  kb/{nombre}")
    total = len(nuevos) + len(faltantes) + len(cambiados)
    if total:
        print(f"\ncapa 2 alterada: {total} archivos. Si el cambio es querido, correr con "
              f"--fijar --nota '...' y anotarlo en argentina/kb/CHANGELOG.md.")
        return 1
    print(f"capa 2 sin cambios: {len(actual)} archivos, fijados el {registro['fijado']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
