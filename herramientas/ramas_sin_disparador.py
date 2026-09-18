#!/usr/bin/env python3
"""Secciones que traen una rama nueva al módulo y no tienen con qué activarse.

    python3 herramientas/ramas_sin_disparador.py
    python3 herramientas/ramas_sin_disparador.py --secciones

Una rama puede entrar de dos maneras: como **módulo** propio, o como **sección** de un módulo
que ya existe. La segunda es más barata y se usó dieciséis veces, pero deja un agujero que el
repositorio no medía: **una sección no se rutea sola**. La tabla de ruteo de la sección 16 del
SKILL.md manda a un módulo, y el `description` activa la skill por materia; si la materia nueva
no figura en ninguno de los dos, el texto está escrito y nadie lo va a abrir.

**Los controles que había miran módulos.** `ruteo.py` mide a qué distancia del router queda cada
módulo, y `TestElDescriptionDeLaSkillActivaTodasLasRamas` exige que el `description` active a cada
uno. Los siete módulos que contienen las secciones estaban alcanzados, así que los dos daban verde
mientras quince ramas eran inalcanzables. Es la alarma que no suena.

**Reporta CANDIDATOS, no culpables**, igual que `fuga_textual.py` o `deuda_vencida.py`: el
veredicto de cada uno se lee y se anota en `ramas-revisadas.json`, y lo que queda después es lo
nuevo. Un candidato puede ser legítimamente `no-es-rama`: una subdivisión interna de una materia
que la fila del módulo ya alcanza, como el salario mínimo dentro de laboral.

**Cómo se detecta, y por qué así.** Se probaron tres reglas contra las dieciséis ramas conocidas:

  - **el encabezado nombra una ley** — acierta 10 de 16;
  - **una ley declarada que aparece sólo en esa sección del módulo** — 104 candidatos, dispara
    en casi toda sección y no discrimina nada;
  - **sólo las secciones `bis`/`ter`/`quater`/…** — 12 de 16, y ciega a las que numeran `24.9.6`.

Ninguna sirve sola. La que quedó es la **conjunción de las dos primeras** —el encabezado nombra
una norma **y** esa norma no aparece en ningún otro lugar del módulo—, que da 23 candidatos y
alcanza las dos formas de numerar.

**LO QUE ESTA MEDIDA NO VE, y por eso es un piso.** Una sección cuyo encabezado **no** nombra su
ley no entra como candidato: hoy quedan afuera *Navegación por agua*, *Cooperativas* y *Transporte
aéreo*, que son ramas y están declaradas a mano en el archivo de veredictos. Escribir el número de
la ley en el encabezado es lo que hace que la próxima se detecte sola.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
REFERENCIAS = RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"
SKILL = RAIZ / "derecho" / "skills" / "derecho-argentino" / "SKILL.md"
NORMAS = RAIZ / "derecho" / "fuentes" / "normas" / "normas.json"
VEREDICTOS = Path(__file__).resolve().parent / "ramas-revisadas.json"

# Índices y catálogos: no son módulos de rama y nombran normas de todas las materias, así que
# cada sección suya sería un candidato falso.
FUERA = {"changelog-normativo.md", "marcadores.md", "danos-indice-doctrinario.md",
         "fuentes.md", "modelos.md", "fallos-csjn.md", "perfiles-heredados.md"}

ENCABEZADO = re.compile(r"^### (.+)$", re.M)
NOMBRA_NORMA = re.compile(r"(?:Ley|Código|Decreto|Acuerdo)\s*\w*\s*N?°?\s*\d[\d.]*", re.I)


def formas(slug: str) -> list[str]:
    """Cómo puede aparecer esa norma escrita en la prosa. Igual que en `normas_huerfanas.py`."""
    nums = re.findall(r"\d+", slug)
    if not nums:
        return []
    if len(nums) >= 2 and len(nums[1]) == 4:
        return [f"{nums[0]}/{nums[1]}", f"{nums[0]}/{nums[1][2:]}"]
    n = nums[0]
    return [f"{n[:-3]}.{n[-3:]}", n] if len(n) >= 4 else [n]


def aparece(forma: str, texto: str) -> bool:
    """Con bordes, porque `6716` está adentro de `26716` y daría un uso que no existe."""
    return re.search(rf"(?<![\d.]){re.escape(forma)}(?!\d)", texto) is not None


def secciones(texto: str) -> list[tuple[str, str]]:
    """Parte un módulo en (encabezado, cuerpo) por sus `###`, más lo que va antes del primero."""
    cortes = [(m.start(), m.group(1).strip()) for m in ENCABEZADO.finditer(texto)]
    if not cortes:
        return []
    tramos = []
    for i, (pos, nombre) in enumerate(cortes):
        fin = cortes[i + 1][0] if i + 1 < len(cortes) else len(texto)
        tramos.append((nombre, texto[pos:fin]))
    return tramos


def candidatos() -> list[tuple[str, str, list[str]]]:
    """(módulo, encabezado, normas propias) de cada sección que trae una norma al módulo."""
    catalogo = json.loads(NORMAS.read_text(encoding="utf-8"))["normas"]
    fuera = []
    for md in sorted(REFERENCIAS.glob("*.md")):
        if md.name in FUERA:
            continue
        t = md.read_text(encoding="utf-8")
        tramos = secciones(t)
        if not tramos:
            continue
        cabecera = t[: t.index(f"### {tramos[0][0]}")]
        for nombre, cuerpo in tramos:
            if not NOMBRA_NORMA.search(nombre):
                continue
            resto = "".join(c for n, c in tramos if n != nombre) + cabecera
            propias = [e["slug"] for e in catalogo
                       if (fs := formas(e["slug"]))
                       and any(aparece(f, cuerpo) for f in fs)
                       and not any(aparece(f, resto) for f in fs)]
            if propias:
                fuera.append((md.name, nombre, sorted(propias)))
    return fuera


def disparadores() -> str:
    """El texto donde una materia tiene que figurar para ser alcanzable: ruteo y description."""
    t = SKILL.read_text(encoding="utf-8")
    fin = t.index("\n## 17") if "\n## 17" in t else len(t)
    tabla = t[t.index("\n## 16"):fin] if "\n## 16" in t else ""
    m = re.search(r"^description:\s*(.*?)(?=\n[a-z_]+:|\n---)", t, re.S | re.M)
    return tabla + "\n" + (m.group(1) if m else "")


ORDINAL = re.compile(r"^(\S+(?:\s+(?:bis|ter|quater|quinquies|sexies))?)", re.I)


def clave(modulo: str, encabezado: str) -> str:
    """`consumidor.md :: 17.11.5 bis` — el número de sección, sin el título, que sí se reescribe.

    El ordinal es parte del número y no del título: sin él, `17.11.5 bis` y `17.11.5 ter` son
    la misma clave y dos ramas distintas quedan tapadas por un veredicto solo.
    """
    return f"{modulo} :: {ORDINAL.match(encabezado).group(1)}"


def revisar() -> tuple[list, list, list]:
    """Devuelve (sin_disparador, sin_veredicto, alcanzadas)."""
    sobre, veredictos = _veredictos.cargar(VEREDICTOS, "ramas", vacio={})
    texto = disparadores()
    declaradas = {k: v for k, v in veredictos.items() if v.get("veredicto") == "rama"}

    sin_disparador, sin_veredicto, alcanzadas = [], [], []
    detectados = {clave(m, e): (m, e, n) for m, e, n in candidatos()}

    for k in sorted(set(detectados) | set(declaradas)):
        v = veredictos.get(k)
        if v is None:
            sin_veredicto.append(k)
            continue
        if v.get("veredicto") != "rama":
            continue
        falta = [d for d in v.get("disparadores", []) if d.lower() not in texto.lower()]
        (sin_disparador if falta else alcanzadas).append((k, falta or v.get("disparadores", [])))
    return sin_disparador, sin_veredicto, alcanzadas


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--secciones", action="store_true", help="sólo los candidatos detectados")
    args = p.parse_args()

    if args.secciones:
        for m, e, n in candidatos():
            print(f"{clave(m, e)}\t{','.join(n)}")
        return 0

    sin_disparador, sin_veredicto, alcanzadas = revisar()

    print(f"\nRAMAS QUE ENTRARON COMO SECCIÓN — {len(alcanzadas) + len(sin_disparador)} declaradas")
    print("  Una sección no se rutea sola: si su materia no está en la tabla de ruteo de la")
    print("  sección 16 ni en el `description`, el texto está escrito y nadie lo va a abrir.")

    if sin_disparador:
        print(f"\n  SIN DISPARADOR — {len(sin_disparador)}. Inalcanzables:")
        for k, falta in sin_disparador:
            print(f"    {k}")
            print(f"        falta: {', '.join(falta)}")
    else:
        print("\n  Todas alcanzables: cada rama declarada tiene su disparador.")

    if sin_veredicto:
        print(f"\n  SIN VEREDICTO — {len(sin_veredicto)}. Abrir la sección y decidir si es una rama")
        print("  nueva o una subdivisión que la fila del módulo ya alcanza:")
        for k in sin_veredicto:
            print(f"    {k}")

    return 1 if (sin_disparador or sin_veredicto) else 0


if __name__ == "__main__":
    raise SystemExit(main())
