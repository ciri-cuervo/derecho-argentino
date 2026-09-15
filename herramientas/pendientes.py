#!/usr/bin/env python3
"""Mide la deuda declarada de la skill. No la recuerda: la lee de los archivos.

    python3 herramientas/pendientes.py

Un archivo de pendientes escrito a mano se vence igual que cualquier otra cifra escrita a
mano, y encima duplica lo que ya está anotado en su lugar. Este script no guarda nada: junta
lo que los propios módulos declaran como faltante y lo ordena.

De donde sale cada bloque:

  institutos sin precedente   marcadores [INSERTAR FALLO VERIFICADO: ...] en references/
  deuda por bloque            columna "Como revalidar" de references/changelog-normativo.md
  verificación vencida        columna de fecha de esa misma tabla, con la regla de 6 meses
  módulos sin eval            ningún caso de evals/ los menciona

Lo que miden otras herramientas se referencia al final en vez de repetirse. Cero dependencias.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "argentina" / "skills" / "derecho-argentino"
REFERENCIAS = SKILL / "references"
EVALS = RAIZ / "argentina" / "evals"

# La tabla de verificación fija su propia regla: pasados los seis meses, el bloque se usa con
# [VERIFICAR VIGENCIA] reforzado hasta revalidarlo.
DIAS_DE_GRACIA = 180

# La fila delimitadora de una tabla, en los dos estilos: `|---|---|` y `| --- | --- |`.
# Buscarla con startswith("|--") funcionaba con el compacto y fallaba EN SILENCIO con el
# otro: la fila pasaba como dato, se parseaba "---" como nombre de bloque y no reportaba
# nada. Un parser de tablas no puede depender de si hay espacios alrededor del guion.
DELIMITADOR = re.compile(r"\|[\s:|-]+\|")

# El marcador también aparece definido en marcadores.md y explicado en prosa. Se los distingue
# por el payload: la definición lleva el texto plantilla y la prosa lleva puntos suspensivos.
# Un hueco real dice de que instituto se trata.
PAYLOAD_GENERICO = re.compile(r"^(doctrina requerida\b|\.\.\.)")
MARCADOR = re.compile(r"\[INSERTAR FALLO VERIFICADO: ([^\]]+)\]")

ARRANQUE_DEUDA = re.compile(
    r"Falta[n]?\s|PENDIENTE\s|[Ss]in fallo[s]?\s+cargado|no est[aá]\s+cargad[oa]"
    r"|NO est[aá]\s+bajad[oa]|Queda abierto")
# Fin de oración: un punto seguido de mayúscula. Así "art. 44" y "Ley 23.551" no la cortan.
FIN_DE_ORACION = re.compile(r"\.\s+(?=[A-ZÁÉÍÓÚÜÑ])|$")


def institutos_sin_precedente() -> list[tuple[str, int, str]]:
    hallados = []
    for archivo in sorted(REFERENCIAS.glob("*.md")):
        for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
            for payload in MARCADOR.findall(linea):
                if PAYLOAD_GENERICO.match(payload.strip()):
                    continue
                hallados.append((archivo.name, numero, payload.strip()))
    return hallados


def _filas_de_verificacion() -> list[list[str]]:
    texto = (REFERENCIAS / "changelog-normativo.md").read_text(encoding="utf-8")
    tabla = texto.split("## Estado de verificación por bloque", 1)
    if len(tabla) < 2:
        return []
    filas = []
    for linea in tabla[1].splitlines():
        if not linea.startswith("|") or DELIMITADOR.fullmatch(linea.strip()):
            continue
        campos = [c.strip() for c in linea.strip("|").split("|")]
        if len(campos) >= 5 and campos[0] != "Bloque":
            filas.append(campos)
    return filas


def deuda_por_bloque() -> list[tuple[str, str, str]]:
    hallados = []
    for campos in _filas_de_verificacion():
        bloque, modulo, revalidar = campos[0].replace("**", ""), campos[1], campos[-1]
        for arranque in ARRANQUE_DEUDA.finditer(revalidar):
            corte = FIN_DE_ORACION.search(revalidar, arranque.start())
            frase = revalidar[arranque.start():corte.start() if corte else None]
            hallados.append((bloque, modulo, " ".join(frase.replace("*", "").split())))
    return hallados


def verificacion_vencida(hoy: date) -> list[tuple[str, str, int]]:
    vencidos = []
    for campos in _filas_de_verificacion():
        fecha = re.search(r"(\d{2})/(\d{2})/(\d{4})", campos[2])
        if not fecha:
            continue
        dia, mes, anio = (int(g) for g in fecha.groups())
        dias = (hoy - date(anio, mes, dia)).days
        if dias > DIAS_DE_GRACIA:
            vencidos.append((campos[0].replace("**", ""), campos[1], dias))
    return sorted(vencidos, key=lambda v: -v[2])


def modulos_sin_eval() -> list[str]:
    """Un módulo esta ejercitado si algún eval lo nombra o si el slug del caso arranca con el.

    Lo segundo hace falta porque varios casos identifican la rama en el nombre del directorio
    -`civil-danos-transito-...`- y después citan la sección sin repetir el nombre del archivo.
    """
    if not EVALS.is_dir():
        return []
    mencionados, prefijos = set(), set()
    for caso in sorted(EVALS.rglob("*.md")):
        mencionados |= set(re.findall(r"([a-z][a-z0-9-]*\.md)", caso.read_text(encoding="utf-8")))
    for directorio in sorted(p for p in EVALS.iterdir() if p.is_dir()):
        prefijos.add(directorio.name.strip().split("-")[0])
    faltan = []
    for modulo in sorted(REFERENCIAS.glob("*.md")):
        raiz = modulo.stem.split("-")[0]
        if modulo.name not in mencionados and raiz not in prefijos:
            faltan.append(modulo.name)
    return faltan


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    hoy = date.today()

    institutos = institutos_sin_precedente()
    print(f"\nINSTITUTOS SIN PRECEDENTE PROPIO — {len(institutos)}")
    print("  Hoy la skill entrega ahí doctrina de kb/ sin auditar, avisando que falta.")
    for archivo, numero, payload in institutos:
        print(f"  · {archivo}:{numero}")
        print(f"      {payload[:110]}")

    deudas = deuda_por_bloque()
    print(f"\nDEUDA DECLARADA POR BLOQUE — {len(deudas)}")
    print("  Lo que la propia tabla de verificación dice que le falta.")
    for bloque, modulo, texto in deudas:
        print(f"  · {bloque} ({modulo})")
        print(f"      {texto[:110]}")

    vencidos = verificacion_vencida(hoy)
    print(f"\nVERIFICACIÓN VENCIDA (más de {DIAS_DE_GRACIA} dias) — {len(vencidos)}")
    if not vencidos:
        print("  Ninguna. Todos los bloques están dentro de los seis meses.")
    for bloque, modulo, dias in vencidos:
        print(f"  · {bloque} ({modulo}): {dias} dias")

    sin_eval = modulos_sin_eval()
    print(f"\nMODULOS QUE NINGUN EVAL NOMBRA — {len(sin_eval)} de "
          f"{len(list(REFERENCIAS.glob('*.md')))}")
    print("  Sin filtrar: varios son de infraestructura -marcadores, intake, fuentes, modelos,")
    print("  otras-ramas- y no se ejercitan por nombre. Los de rama si son deuda de cobertura.")
    for nombre in sin_eval:
        print(f"  · {nombre}")

    print("\nLO QUE MIDEN OTRAS HERRAMIENTAS")
    print("  reformas que están en el texto bajado y ningún módulo leyó")
    print("    python3 herramientas/reformas_no_leidas.py")
    print("  normas citadas con articulado y sin bajar")
    print("    python3 herramientas/cobertura_normativa.py")
    print("  documentos de jurisprudencia sin leer o con defecto de OCR")
    print("    python3 herramientas/calidad_ocr.py --pendientes")
    print("  prosa candidata en los evals, que están fuera del checklist")
    print("    python3 herramientas/fuga_textual.py argentina/evals/*/*.md")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
