#!/usr/bin/env python3
"""Mide el mapa de ruteo: a qué distancia del router queda cada módulo, y cuál no se alcanza.

POR QUÉ EXISTE

Con más de treinta módulos, el error dominante deja de ser equivocarse DENTRO de un módulo y
pasa a ser abrir el que no era, o ninguno. Nada medía eso. Las rúbricas de `evals/` juzgan la
respuesta, que puede salir bien de memoria: un módulo al que el ruteo no llega no falla
ruidosamente, se vuelve invisible y el análisis lo suple con lo que el modelo ya cree saber.

QUÉ MIDE

La tabla de ruteo de la sección 16 del SKILL.md es la raíz. Un módulo está a distancia 1 si esa
tabla lo nombra; a distancia n+1 si lo nombra un módulo a distancia n. La distancia importa:
un módulo a distancia 3 existe, está escrito y nadie lo va a abrir, porque para llegar hay que
haber leído antes otros dos que no venían al caso.

También cruza las consultas de `derecho/evals/RUTEO.md`: que cada módulo esperado
exista, y qué módulos no ejercita ninguna consulta.

QUÉ NO MIDE

**Que el agente rutee bien.** Esto mide el MAPA, no el manejo: que desde el router se pueda
llegar a cada módulo, no que se llegue. Lo segundo lo contesta correr las consultas contra el
sistema y anotar qué abrió, que es trabajo de quien las corre.

No se instala con el plugin: vive fuera de `derecho/`.

Uso, desde la raíz del repositorio:

    python3 herramientas/ruteo.py
    python3 herramientas/ruteo.py --todo     # imprime también los módulos alcanzados

Sale con código 1 si hay un módulo inalcanzable o una consulta que espera uno que no existe.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SKILL = RAIZ / "derecho" / "skills" / "derecho-argentino"
REFS = SKILL / "references"
COMANDOS = RAIZ / "derecho" / "commands"
CONSULTAS = RAIZ / "derecho" / "evals" / "RUTEO.md"

# Un módulo se nombra con backticks: `references/laboral.md` o `laboral.md` desde otro módulo.
CITA = re.compile(r"`(?:references/)?([a-z0-9-]+\.md)`")
# Y a veces sin backticks dentro de una tabla de ruteo.
SUELTO = re.compile(r"\breferences/([a-z0-9-]+\.md)")


def modulos() -> set[str]:
    return {p.name for p in REFS.glob("*.md")}


def seccion_de_ruteo() -> str:
    texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    arranca = re.search(r"^## 16 ·", texto, re.M)
    if not arranca:
        raise SystemExit("no encuentro la sección 16 de ruteo en SKILL.md")
    resto = texto[arranca.start():]
    corta = re.search(r"^## 17 ", resto, re.M)
    return resto[:corta.start()] if corta else resto


def nombrados(texto: str, universo: set[str]) -> set[str]:
    return (set(CITA.findall(texto)) | set(SUELTO.findall(texto))) & universo


def distancias() -> dict[str, int]:
    """Distancia de cada módulo a la tabla de ruteo. Ausente = inalcanzable."""
    universo = modulos()
    frontera = nombrados(seccion_de_ruteo(), universo)
    dist = {m: 1 for m in frontera}
    paso = 1
    while frontera:
        paso += 1
        siguiente = set()
        for m in frontera:
            for vecino in nombrados((REFS / m).read_text(encoding="utf-8"), universo):
                if vecino not in dist:
                    dist[vecino] = paso
                    siguiente.add(vecino)
        frontera = siguiente
    return dist


def desde_comandos() -> dict[str, set[str]]:
    universo = modulos()
    salida: dict[str, set[str]] = {}
    for comando in sorted(COMANDOS.glob("*.md")):
        for m in nombrados(comando.read_text(encoding="utf-8"), universo):
            salida.setdefault(m, set()).add(comando.name)
    return salida


def consultas(ruta: pathlib.Path = CONSULTAS):
    """Devuelve ([(id, consulta, [módulos esperados])], cuántos encabezados hay en el archivo)."""
    if not ruta.is_file():
        return [], 0
    texto = ruta.read_text(encoding="utf-8")
    salida = []
    for bloque in re.finditer(
            r"^### (R\d+) · (.+?)$\n+esperado: (.+?)$", texto, re.M):
        esperados = [x.strip().strip("`") for x in bloque.group(3).split(",")]
        salida.append((bloque.group(1), bloque.group(2).strip(), esperados))
    # Cuántos encabezados hay, contra cuántos se pudieron leer enteros. Sin esto, una consulta
    # con el separador mal escrito o sin su línea `esperado:` desaparecía en silencio: el conteo
    # bajaba de 27 a 26 y ningún control lo notaba, porque todos miran lo que SI se leyó.
    encabezados = len(re.findall(r"^### R\d+", texto, re.M))
    return salida, encabezados


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--todo", action="store_true",
                   help="listar también los módulos alcanzados, por distancia")
    a = p.parse_args(argv)

    if not REFS.is_dir():
        print(f"no encuentro {REFS}: corré el script desde la raíz del repo", file=sys.stderr)
        return 2

    universo = modulos()
    dist = distancias()
    comandos = desde_comandos()
    lejos = sorted(m for m in universo if dist.get(m, 99) >= 3)
    inalcanzables = sorted(m for m in universo if m not in dist and m not in comandos)
    solo_comando = sorted(m for m in universo if m not in dist and m in comandos)

    por_distancia: dict[int, list[str]] = {}
    for m, d in dist.items():
        por_distancia.setdefault(d, []).append(m)
    print(f"\n  Módulos: {len(universo)}. Desde la tabla de ruteo de la sección 16:")
    for d in sorted(por_distancia):
        print(f"    distancia {d}: {len(por_distancia[d])}")
        if a.todo:
            for m in sorted(por_distancia[d]):
                print(f"      {m}")

    if solo_comando:
        print(f"\n  SOLO DESDE UN COMANDO ({len(solo_comando)}) — no están en el ruteo, así que")
        print("  fuera de su comando no se abren:")
        for m in solo_comando:
            print(f"    {m}  <- {', '.join(sorted(comandos[m]))}")

    if lejos:
        print(f"\n  A DISTANCIA 3 O MÁS ({len(lejos)}) — existen y prácticamente no se abren:")
        for m in lejos:
            print(f"    {m}  (distancia {dist[m]})")

    if inalcanzables:
        print(f"\n  INALCANZABLES ({len(inalcanzables)}) — ningún camino los nombra:")
        for m in inalcanzables:
            print(f"    {m}")

    casos, encabezados = consultas()
    rotas = []
    if encabezados != len(casos):
        rotas.append(f"{CONSULTAS.name} tiene {encabezados} consultas y sólo {len(casos)} se "
                     "pudieron leer enteras: revisar el separador y la línea `esperado:`")
    ejercitados: set[str] = set()
    if casos:
        for ident, _, esperados in casos:
            ejercitados |= set(esperados)
            for m in esperados:
                if m not in universo:
                    rotas.append(f"{ident} espera {m}, que no existe")
        sin_consulta = sorted(universo - ejercitados)
        print(f"\n  Consultas de ruteo: {len(casos)}. Módulos que ejercitan: {len(ejercitados)}.")
        if sin_consulta:
            print(f"  Sin ninguna consulta que los ejercite ({len(sin_consulta)}):")
            for m in sin_consulta:
                print(f"    {m}")
        for r in rotas:
            print(f"    ROTA: {r}")
    elif not CONSULTAS.is_file():
        print(f"\n  No encontré {CONSULTAS.relative_to(RAIZ)}.")
        rotas.append(f"falta {CONSULTAS.name}")
    else:
        # El archivo está y no se pudo leer ninguna consulta: el formato derivó. Devolver 0
        # acá dejaba el chequeo de módulos esperados sin correr y el CLI en verde.
        print(f"\n  {CONSULTAS.name} está pero no pude leer ninguna consulta: cambió el "
              "formato de los encabezados.")
        rotas.append(f"{CONSULTAS.name} sin consultas legibles")

    print("\n  Esto mide el MAPA, no el manejo: que desde el router se pueda llegar a cada")
    print("  módulo, no que se llegue. Lo segundo se contesta corriendo las consultas contra")
    print("  el sistema y anotando qué abrió.")
    return 1 if (inalcanzables or rotas) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
