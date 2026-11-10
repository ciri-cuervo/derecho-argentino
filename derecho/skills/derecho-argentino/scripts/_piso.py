"""El piso de Python de lo que se distribuye, comprobado al arrancar.

Los scripts de la skill se miden desde 3.9 —el Python de las herramientas de Xcode— y por
debajo de ese piso nadie los corrió: un número que salga de ahí no tiene medida detrás. La
sección 16 del `SKILL.md` trata un Python anterior a 3.9 igual que la falta de Python, y para
que esa regla se pueda aplicar tiene que haber una señal en la consola. Ésta es la señal.

Se importa desde `_raiz.py`, que lo trae a casi todos, y directamente desde los dos scripts que
no pasan por la raíz: `liquidacion_lct.py` y `verificar_respuesta.py`.
`TestElPisoDePython`, en `test_scripts.py`, sostiene que ningún script quede afuera.
"""
from __future__ import annotations

import sys

PISO = (3, 9)


def mensaje(version) -> str | None:
    """El aviso para un intérprete debajo del piso, o None si está a la altura."""
    v = tuple(version)
    if v[:2] >= PISO:
        return None
    return (f"Este script necesita Python {PISO[0]}.{PISO[1]} o posterior, y se está corriendo "
            f"con {'.'.join(str(x) for x in v[:3])}. Para la skill es lo mismo que no tener "
            f"Python: no calcula. Se baja de https://www.python.org/downloads/ y después se "
            f"vuelve a abrir la aplicación.")


def exigir(version=None) -> None:
    """Corta con código 2 y el aviso por stderr si el intérprete está debajo del piso."""
    aviso = mensaje(sys.version_info if version is None else version)
    if aviso:
        print(aviso, file=sys.stderr)
        raise SystemExit(2)

exigir()
