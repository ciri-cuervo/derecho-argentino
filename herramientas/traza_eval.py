#!/usr/bin/env python3
"""Si el agente evaluado abrió la clave de respuestas, leído de la traza de la corrida.

    python3 herramientas/traza_eval.py
    python3 herramientas/traza_eval.py --resultados derecho/evals/results/<sello>

**La clave de respuestas está al lado del caso.** `claude plugin eval` corre el agente contra el
repositorio vivo, y ahí mismo, en `evals/<caso>/`, están la `rubrica.md`, el `resultado.md`
esperado y los `graders/` que dicen textualmente qué puntúa el juez. Nada impide leerlos. Un
puntaje sacado así mide la lectura, no el razonamiento, y no se distingue de uno bueno.

**Y no se puede comprobar después.** La traza vive en el sandbox de la corrida —el `tracePath`
que anota `aggregate-result.json`, bajo `/tmp`— y se borra con él. Por eso esto se corre
**pegado** al eval, y por eso se planta (rc=2) cuando la traza ya no está: no hay verde por
ausencia de instrumento.

**Dos niveles, porque no todo lo que está bajo `evals/` es clave de respuestas.** `modelos.md`
23.8 manda al runtime a los `resultado.md` como ejemplos trabajados, así que abrir el de OTRO
caso es comportamiento declarado y acá se avisa, no se rompe. Lo que rompe es lo que ningún uso
legítimo explica: un `graders/` o una `rubrica.md` de cualquier caso —eso es el criterio con que
lo van a puntuar— y cualquier ruta del caso que se está corriendo, que es su propio enunciado
resuelto.

**Mide lo que el agente PIDIÓ, no lo que vio.** Un `Glob` sobre la raíz del repositorio devuelve
rutas de `evals/` en el resultado sin que ninguna herramienta las abra: eso no lo cuenta esta
medida. Lo que cuenta es la ruta que el agente puso en la entrada de una herramienta.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "derecho" / "evals" / "results"

#: Una ruta de eval en la entrada de una herramienta. `results/` es la salida de la corrida, no
#: material del caso: sale por el grupo negativo.
RUTA = re.compile(r"(?:derecho/)?evals/(?!results/)(?P<caso>[\w.-]+)/(?P<resto>[\w./-]*)")


def ultima_corrida(directorio: pathlib.Path | None = None) -> pathlib.Path:
    if directorio is not None:
        return directorio / "aggregate-result.json"
    sellos = sorted(p for p in RESULTADOS.glob("*/aggregate-result.json"))
    if not sellos:
        raise SystemExit(f"no hay ninguna corrida en {RESULTADOS.relative_to(RAIZ)}: "
                         f"esto se corre pegado a `claude plugin eval`")
    return sellos[-1]


def entradas(traza: pathlib.Path):
    """Las entradas de cada `tool_use` de la traza, ya serializadas."""
    for renglon in traza.read_text(encoding="utf-8").splitlines():
        try:
            registro = json.loads(renglon)
        except json.JSONDecodeError:
            continue
        mensaje = registro.get("message")
        if not isinstance(mensaje, dict):
            continue
        for bloque in mensaje.get("content", []):
            if isinstance(bloque, dict) and bloque.get("type") == "tool_use":
                yield bloque.get("name", "?"), json.dumps(bloque.get("input"), ensure_ascii=False)


def clasificar(caso_corrido: str, texto: str) -> list:
    """`(gravedad, ruta)` por cada ruta de eval que aparezca en una entrada."""
    hallazgos = []
    for m in RUTA.finditer(texto):
        caso, resto = m.group("caso"), m.group("resto")
        ruta = f"evals/{caso}/{resto}".rstrip("/")
        if resto.startswith("graders") or resto.startswith("rubrica") or caso == caso_corrido:
            hallazgos.append(("ROMPE", ruta))
        else:
            hallazgos.append(("avisa", ruta))
    return hallazgos


def revisar(agregado: pathlib.Path) -> tuple[list, list, list]:
    datos = json.loads(agregado.read_text(encoding="utf-8"))
    rompen, avisan, sin_traza = [], [], []
    for caso in datos.get("cases", []):
        nombre = caso.get("name", "?")
        for brazo, corridas in (caso.get("arms") or {}).items():
            for i, corrida in enumerate(corridas, 1):
                ruta = corrida.get("tracePath")
                quien = f"{nombre} [{brazo} {i}]"
                if not ruta or not pathlib.Path(ruta).is_file():
                    sin_traza.append(f"{quien}: {ruta or 'sin tracePath'}")
                    continue
                for herramienta, texto in entradas(pathlib.Path(ruta)):
                    for gravedad, hallada in clasificar(nombre, texto):
                        (rompen if gravedad == "ROMPE" else avisan).append(
                            f"{quien}  {herramienta}  {hallada}")
    return rompen, avisan, sin_traza


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resultados", type=pathlib.Path,
                    help="carpeta de una corrida; por defecto, la última")
    args = ap.parse_args()

    agregado = ultima_corrida(args.resultados)
    if not agregado.is_file():
        raise SystemExit(f"no existe {agregado}")
    rompen, avisan, sin_traza = revisar(agregado)

    print(f"corrida: {agregado.parent.name}")
    for linea in avisan:
        print(f"  avisa  {linea}")
    for linea in rompen:
        print(f"  ROMPE  {linea}")

    if sin_traza:
        for linea in sin_traza:
            print(f"  SIN TRAZA  {linea}")
        print(f"\n{len(sin_traza)} corridas sin traza en disco: el sandbox de `claude plugin "
              f"eval` se borra, así que esto se corre PEGADO al eval. No se puede decir que la "
              f"corrida estuvo limpia; se puede decir que no se midió.")
        return 2
    if rompen:
        print(f"\n{len(rompen)} lecturas de la clave de respuestas. El puntaje de esas corridas "
              f"mide la lectura, no el razonamiento: se descartan.")
        return 1
    print(f"traza limpia: ninguna corrida abrió rúbricas, graders ni su propio caso "
          f"({len(avisan)} lecturas de otro caso, que 23.8 declara)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
