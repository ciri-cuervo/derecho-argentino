#!/usr/bin/env python3
"""Normas bajadas que ningún módulo, script ni eval nombra.

    python3 herramientas/normas_huerfanas.py
    python3 herramientas/normas_huerfanas.py --slugs

`cobertura_normativa.py` mira una sola dirección: la norma que un módulo **cita** y no está
bajada. La inversa no la miraba nadie, y por eso una norma podía estar meses en `fuentes/` sin
que ninguna prosa la usara, invisible para todo control.

**No es una alarma: es una lista de trabajo.** Una huérfana no está mal bajada ni sobra; está
esperando el módulo que la use, y eso no se apaga con un veredicto sino escribiendo. Por eso acá
no hay archivo de veredictos ni línea de base: la lista se achica sola cuando la prosa la nombra,
y mientras tanto tiene que seguir viéndose entera.

**Lo que mide es MENCIÓN, no cobertura.** Que un módulo nombre la ley no prueba que la desarrolle;
prueba que alguien la miró. Es el piso, no el techo: lo que sigue después es leer el módulo.

**Y sólo mide lo que se cita por NÚMERO.** Una constitución provincial se nombra, no se cita, y una
medida por nombre se probó y se descartó: buscar el token del slug en el mismo renglón que
«constitución» daba por usadas a Misiones —dentro de «comisiones»—, a CABA —por un renglón que
habla de inconstitucionalidad— y a Catamarca, por una línea que documenta un DEFECTO del texto
bajado y no un uso. Con bordes de palabra seguía fallando en dos de los tres. Una medida que se
equivoca sobre casos conocidos no sirve para los desconocidos, así que esas normas salen aparte,
como SIN MEDIDA, y saber si están usadas es leer.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = RAIZ / "derecho" / "fuentes" / "normas"
SKILL = RAIZ / "derecho" / "skills" / "derecho-argentino"

# Los dos JSON del propio catálogo nombran todos los slugs por definición: contarlos como uso
# convertiría a cada norma en usada y el detector reportaría cero para siempre.
EXCLUIDOS = {"normas.json", "procedencia.json", "revisiones.json"}


def prosa_del_repo() -> str:
    """Todo lo que puede nombrar una norma: los módulos, los scripts de la skill y los evals."""
    partes = []
    for patron in (SKILL / "references", SKILL / "scripts", RAIZ / "derecho" / "evals"):
        for f in patron.rglob("*"):
            if f.suffix in (".md", ".py", ".json") and f.name not in EXCLUIDOS:
                partes.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(partes)


def formas(slug: str) -> list[str]:
    """Cómo puede aparecer esa norma escrita en la prosa.

    Un decreto se declara `decreto-84-2026` y se escribe `84/2026` o `84/26`; una ley se declara
    `ley-27499` y se escribe `27.499` o `27499`. Se devuelven todas, y alcanza con que UNA
    aparezca: el detector busca menciones, no una forma canónica.
    """
    nums = re.findall(r"\d+", slug)
    if not nums:
        return []
    if len(nums) >= 2 and len(nums[1]) == 4:          # decreto/acuerdo N-AAAA
        n, anio = nums[0], nums[1]
        return [f"{n}/{anio}", f"{n}/{anio[2:]}"]
    n = nums[0]
    if len(n) >= 4:
        return [f"{n[:-3]}.{n[-3:]}", n]
    return [n]


def aparece(forma: str, texto: str) -> bool:
    """Con bordes, porque `6716` está adentro de `26716` y daría un uso que no existe."""
    return re.search(rf"(?<![\d.]){re.escape(forma)}(?!\d)", texto) is not None


def bajada(slug: str) -> bool:
    return (NORMAS / f"{slug}.txt").is_file() or (NORMAS / f"{slug}.pdf").is_file()


def huerfanas() -> tuple[list[tuple[str, str]], list[tuple[str, str]], int]:
    """Devuelve (huérfanas, sin_medida, usadas).

    `sin_medida` son las que no se citan por número —las constituciones—: acá no se adivina.
    """
    texto = prosa_del_repo()
    entradas = json.loads((NORMAS / "normas.json").read_text(encoding="utf-8"))["normas"]
    sueltas, sin_medida, usadas = [], [], 0
    for e in entradas:
        slug = e["slug"]
        if not bajada(slug):
            continue                                  # declarada y sin bajar: eso lo mide otro
        titulo = e.get("titulo", "")
        if slug in texto or any(aparece(f, texto) for f in formas(slug)):
            usadas += 1
        elif not formas(slug):
            sin_medida.append((slug, titulo))
        else:
            sueltas.append((slug, titulo))
    return sueltas, sin_medida, usadas


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slugs", action="store_true", help="sólo los slugs, uno por línea")
    args = p.parse_args()

    sueltas, sin_medida, usadas = huerfanas()
    if args.slugs:
        for slug, _ in sueltas:
            print(slug)
        return 0

    total = usadas + len(sueltas) + len(sin_medida)
    print(f"\nNORMAS BAJADAS QUE NINGÚN MÓDULO NOMBRA — {len(sueltas)} de {total}")
    if sueltas:
        print("  Texto verificado esperando el módulo que lo use. No es un defecto: es trabajo")
        print("  pendiente, y por eso no se apaga con un veredicto sino escribiendo la prosa.")
        for slug, titulo in sueltas:
            print(f"  · {slug}")
            print(f"      {titulo}")
        print("\n  Que un módulo la nombre es el PISO, no el techo: nombrarla la saca de esta")
        print("  lista y no prueba que la desarrolle. Eso se mira leyendo el módulo.")
    else:
        print("  Ninguna. Todo lo que se cita por número lo usa algún módulo, script o eval.")

    if sin_medida:
        print(f"\n  SIN MEDIDA — {len(sin_medida)}. No se citan por número sino por nombre, y acá")
        print("  no se adivina: saber si un módulo las usa es leer, no contar.")
        for slug, _ in sin_medida:
            print(f"    {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
