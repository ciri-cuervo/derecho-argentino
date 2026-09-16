#!/usr/bin/env python3
"""Detecta reformas que están en el texto bajado y ningún modulo leyó.

    python3 herramientas/reformas_no_leidas.py
    python3 herramientas/reformas_no_leidas.py --desde 2024

La capa de fuente primaria se actualiza sola: `descargar_normas.py` vuelve a traer el texto
consolidado de InfoLEG, que YA incorpora la última reforma. Los módulos no. Entre las dos cosas
se abre una ventana en la que el repositorio tiene el artículo nuevo y la skill sigue explicando
el viejo, sin que nada avise.

Método: cada consolidado trae al pie de sus artículos una nota del tipo "(Artículo sustituido
por art. X de la Ley N° NN.NNN B.O. DD/MM/AAAA)". El script extrae esas notas, se queda con la
reforma más reciente de cada norma, y pregunta si algún módulo nombra esa ley.

Reporta CANDIDATOS, no culpables. Una reforma puede tocar un artículo que el módulo no cubre, y
entonces es correcto que no la nombre. Lo que decide es abrir el módulo. Los veredictos se
anotan en `reformas-revisadas.json` para que el reporte no repita lo ya visto.

Sale con código 1 si hay candidatos sin veredicto. Cero dependencias externas.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = RAIZ / "derecho" / "fuentes" / "normas"
SKILL = RAIZ / "derecho" / "skills" / "derecho-argentino"
REGISTRO = Path(__file__).resolve().parent / "reformas-revisadas.json"

# "(Artículo sustituido por art. 7° de la Ley N° 27.786 B.O. 10/03/2025 ...)". La ventana entre
# el número de ley y el B.O. es corta a propósito: si se agranda, empareja leyes con fechas de
# otra nota.
NOTA = re.compile(r"Ley N[°º\.]? ?(\d{2}\.\d{3})[^)]{0,80}?B\.?O\.? ?(\d{1,2})/(\d{1,2})/((?:19|20)\d{2})")


def texto_de_los_modulos() -> str:
    partes = [(SKILL / "SKILL.md").read_text(encoding="utf-8")]
    partes += [p.read_text(encoding="utf-8") for p in sorted((SKILL / "references").glob("*.md"))]
    return "\n".join(partes)


def ultima_reforma_por_norma(desde: int) -> list[tuple[date, str, str]]:
    """(fecha, slug de la norma bajada, ley reformadora) para la reforma más reciente de cada una."""
    hallados = []
    for archivo in sorted(NORMAS.glob("*.txt")):
        por_fecha: dict[date, set[str]] = {}
        for ley, dia, mes, anio in NOTA.findall(
                archivo.read_text(encoding="utf-8", errors="replace")):
            try:
                cuando = date(int(anio), int(mes), int(dia))
            except ValueError:
                continue                      # fecha imposible en la nota: no se adivina
            por_fecha.setdefault(cuando, set()).add(ley)
        if not por_fecha:
            continue
        ultima = max(por_fecha)
        if ultima.year < desde:
            continue
        for ley in sorted(por_fecha[ultima]):
            hallados.append((ultima, archivo.stem, ley))
    return sorted(hallados, reverse=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--desde", type=int, default=0,
                    help="ignorar normas cuya última reforma sea anterior a ese año")
    args = ap.parse_args()

    modulos = texto_de_los_modulos()
    _, revisadas = _veredictos.cargar(REGISTRO, "reformas", vacio={})

    sin_veredicto, conocidas, decididas = [], 0, 0
    for cuando, slug, ley in ultima_reforma_por_norma(args.desde):
        if f"Ley {ley}" in modulos or ley in modulos:
            conocidas += 1
            continue
        clave = f"{slug}:{ley}"
        if clave in revisadas:
            decididas += 1
            continue
        sin_veredicto.append((cuando, slug, ley))

    print(f"\n  Normas con notas de reforma: la última de cada una se compara contra los modulos.")
    print(f"  Reformas que los módulos nombran: {conocidas}. Con veredicto escrito: {decididas}.")

    if not sin_veredicto:
        print("\n  Sin pendientes: no hay reforma reciente que los módulos no nombren.\n")
        return 0

    print(f"\n  SIN DECIDIR ({len(sin_veredicto)}) — abrir el modulo y ver si la reforma lo toca:\n")
    for cuando, slug, ley in sin_veredicto:
        print(f"  {cuando.strftime('%d/%m/%Y')}  {slug:<24} Ley {ley}")
    print("\n  Un veredicto se anota en reformas-revisadas.json con su motivo, con la clave")
    print("  'slug:ley'. Reporta candidatos: una reforma puede tocar un artículo que el módulo")
    print("  no cubre, y entonces es correcto que no la nombre.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
