#!/usr/bin/env python3
"""Mide la deuda declarada de la skill. No la recuerda: la lee de los archivos.

    python3 herramientas/pendientes.py

Un archivo de pendientes escrito a mano se vence igual que cualquier otra cifra escrita a
mano, y encima duplica lo que ya está anotado en su lugar. Este script no guarda nada: junta
lo que los propios módulos declaran como faltante y lo ordena.

De dónde sale cada bloque:

  institutos sin precedente   marcadores [INSERTAR FALLO VERIFICADO: ...] en references/
  deuda por bloque            columna "Cómo revalidar" de references/changelog-normativo.md
  verificación vencida        columna de fecha de esa misma tabla, con la regla de 6 meses
  módulos sin eval            ningún caso de evals/ los menciona
  evals sin correr            el resultado del caso se declara a sí mismo sin medición
  fuentes marcadas            campo `revisar` de las dos procedencias de fuentes/

Lo que miden otras herramientas se referencia al final en vez de repetirse. Cero dependencias.

Esta salida **es el inventario de herramientas del repositorio**: `AGENTS.md` ya no copia la
lista, remite acá. Una herramienta nueva que mida algo del estado se agrega al cierre de
`main()`, o queda sin puerta de entrada.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "derecho" / "skills" / "derecho-argentino"
REFERENCIAS = SKILL / "references"
EVALS = RAIZ / "derecho" / "evals"

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
# Un hueco real dice de qué instituto se trata.
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


def _tabla(archivo, titulo: str, columnas: int) -> list[list[str]]:
    """Las filas de una tabla markdown que arranca después de `titulo`.

    **Se exige el ancho.** La verificación vive en dos tablas —la fecha adentro de la skill, el
    cotejo en `docs/REVALIDAR.md`— y si una cambia de forma, un parser laxo sigue leyendo, lee
    otra cosa y REPORTA CERO. Cero acá se lee como «no hay deuda».
    """
    if not archivo.is_file():
        return []
    partes = archivo.read_text(encoding="utf-8").split(titulo, 1)
    if len(partes) < 2:
        return []
    filas = []
    for linea in partes[1].splitlines():
        if not linea.startswith("|") or DELIMITADOR.fullmatch(linea.strip()):
            continue
        campos = [c.strip() for c in linea.strip("|").split("|")]
        if len(campos) == columnas and campos[0] != "Bloque":
            filas.append(campos)
    return filas


def _filas_de_verificacion() -> list[list[str]]:
    """Bloque, módulo, fecha y volatilidad. Vive en la skill: contesta desde cuándo rige."""
    return _tabla(REFERENCIAS / "changelog-normativo.md",
                  "## Estado de verificación por bloque", 4)


def _filas_de_revalidacion() -> list[list[str]]:
    """Bloque, módulo y con qué se cotejó. Vive en `docs/`: es del que revalida."""
    return _tabla(RAIZ / "docs" / "REVALIDAR.md", "## Cómo revalidar", 3)


def deuda_por_bloque() -> list[tuple[str, str, str]]:
    hallados = []
    for campos in _filas_de_revalidacion():
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


# Módulos que no son de rama: no describen derecho, describen cómo trabaja la skill. Un eval
# los ejercita de costado en cada caso -todo caso pasa por `intake.md` y emite marcadores de
# `marcadores.md`- y escribirles un caso propio no mediría cobertura de derecho. Se listan acá y
# no se infieren del nombre: la inferencia se equivocaría con `perfiles-heredados.md`, que suena a rama
# y es un índice. Contarlos como deuda infla el número y una lista inflada se deja de leer.
DE_INFRAESTRUCTURA = frozenset({
    "danos-indice-doctrinario.md",  # índice de doctrina, no una rama
    "escritos.md",
    "fuentes.md",
    "intake.md",
    "marcadores.md",
    "modelos.md",
    "perfiles-heredados.md",
})


def modulos_sin_eval() -> list[str]:
    """Un módulo está ejercitado si algún eval lo nombra, o si es de rama y el slug de un caso
    arranca con su nombre.

    Lo segundo hace falta porque varios casos identifican la rama en el nombre del directorio
    -`civil-danos-transito-...`- y después citan la sección sin repetir el nombre del archivo.

    **Y por eso el prefijo sólo vale para un módulo de nombre simple.** `civil.md` es la rama
    entera y un caso `civil-...` la ejercita; `penal-juvenil-pba.md` es un fuero acotado y un
    caso `penal-estupefacientes-...` no lo toca, aunque compartan la primera palabra. Un módulo
    de nombre compuesto tiene que estar NOMBRADO por algún archivo del caso: la coincidencia de
    prefijo lo daba por testeado sin que nadie hubiera escrito una consulta que lo abra, que es
    deuda invisible en la medida que existe para hacerla visible.

    MUTACIÓN que lo demuestra: quitar del eval de un módulo compuesto la mención a su archivo
    -dejando el directorio con el mismo prefijo- tiene que hacerlo aparecer en esta lista.
    """
    if not EVALS.is_dir():
        return []
    mencionados, prefijos = set(), set()
    # Sólo los CASOS: una carpeta con `caso.md`. `RUTEO.md` nombra todos los módulos por
    # definición y `PROCEDIMIENTO.md` cita varios, así que contarlos daba cero deuda sobre un
    # repositorio con la misma deuda de antes: verde con el instrumento apagado.
    casos = sorted(p for p in EVALS.iterdir() if p.is_dir() and (p / "caso.md").is_file())
    for carpeta in casos:
        for pieza in sorted(carpeta.glob("*.md")):
            mencionados |= set(re.findall(r"([a-z][a-z0-9-]*\.md)",
                                          pieza.read_text(encoding="utf-8")))
        prefijos.add(carpeta.name.strip().split("-")[0])
    faltan = []
    for modulo in sorted(REFERENCIAS.glob("*.md")):
        # El nombre compuesto no hereda el prefijo de su primera palabra: ver el docstring.
        por_prefijo = "-" not in modulo.stem and modulo.stem in prefijos
        if modulo.name not in mencionados and not por_prefijo:
            faltan.append(modulo.name)
    return faltan


def evals_sin_correr() -> list[str]:
    """Los casos cuyo `resultado.md` declara que nadie los pasó por el sistema.

    Un eval escrito y no corrido es una promesa, no una medición: el módulo tiene consulta que lo
    ejercita y nadie sabe qué contesta. `modulos_sin_eval()` mide lo de al lado —qué rama no tiene
    ningún caso— y da cero con todos los casos sin correr, que es verde con el instrumento apagado
    sobre la pregunta que importa.

    La marca es la que escriben los propios archivos: **Sin correr** en negrita al abrir el
    cuerpo. Se lee así y no por ausencia de archivo porque el repositorio no deja el resultado
    vacío: lo escribe diciendo qué falta y desde cuándo.

    MUTACIÓN que lo demuestra: sacarle el «Sin correr» a un `resultado.md` lo baja de esta lista.
    """
    if not EVALS.is_dir():
        return []
    sin = []
    for carpeta in sorted(p for p in EVALS.iterdir()
                          if p.is_dir() and (p / "caso.md").is_file()):
        r = carpeta / "resultado.md"
        if r.is_file() and "**Sin correr" in r.read_text(encoding="utf-8"):
            sin.append(carpeta.name)
    return sin


def fuentes_marcadas_para_revisar() -> list[tuple[str, str, str]]:
    """Lo que los descargadores marcaron como dudoso y nadie resolvió.

    Por qué existe: `descargar_normas.py` y `descargar_jurisprudencia.py` escriben `revisar` en
    su procedencia cuando el texto bajado no es lo que dice ser -la URL devolvió la ficha, el
    articulado no aparece, la carátula no coincide con el documento-, y hasta acá NADIE leía ese
    campo. Se escribía y se olvidaba. El único modo de verlo era volver a bajar, que con los 403
    de InfoLEG y normas.gba sólo puede hacer el usuario, o abrir el JSON a mano.

    Es texto offline que ya sabemos defectuoso y que la skill sigue usando, así que el lugar de
    esa deuda es la lista de deuda. Una marca se resuelve arreglando la fuente, o se apaga con un
    veredicto de lectura en `normas/revisiones.json`, que es lo que la mueve a `revisado`.

    **El veredicto y el apagado viajan juntos, y esta función sólo ve el segundo.** Acá se lee
    el campo `revisar` de la procedencia y nada más: quien compara el problema contra
    `revisiones.json` -por `plano()`, que aplana acentos y mayúsculas- y lo mueve a `revisado`
    es `descargar_normas.py`, al bajar la norma. Escribir el veredicto y dejar la marca arriba
    es un estado prohibido, y lo sostiene
    `test_los_veredictos_del_repositorio_apagan_las_marcas_que_dicen_apagar`: un veredicto que
    no apaga nada es peor que no tenerlo, porque la marca vuelve a sonar igual y el veredicto
    da la impresión de estar resuelto. Así que el veredicto se escribe **y** se apaga la marca,
    sea volviendo a bajar la norma -con `--forzar`, porque el archivo ya está- o moviendo la
    entrada a `revisado` con esa misma comparación.
    """
    import json
    fuentes = RAIZ / "derecho" / "fuentes"
    corpus = (("normas", fuentes / "normas" / "procedencia.json", "normas"),
              ("jurisprudencia", fuentes / "jurisprudencia" / "procedencia.json", "fallos"))
    marcadas = []
    for etiqueta, ruta, clave in corpus:
        if not ruta.is_file():
            continue
        entradas = json.loads(ruta.read_text(encoding="utf-8")).get(clave, {})
        for slug, reg in sorted(entradas.items()):
            for problema in reg.get("revisar", []):
                marcadas.append((etiqueta, slug, problema))
    return marcadas


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    hoy = date.fromisoformat(_veredictos.hoy())

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
    print(f"\nVERIFICACIÓN VENCIDA (más de {DIAS_DE_GRACIA} días) — {len(vencidos)}")
    if not vencidos:
        print("  Ninguna. Todos los bloques están dentro de los seis meses.")
    for bloque, modulo, dias in vencidos:
        print(f"  · {bloque} ({modulo}): {dias} días")

    sin_eval = modulos_sin_eval()
    de_rama = [m for m in sin_eval if m not in DE_INFRAESTRUCTURA]
    infra = [m for m in sin_eval if m in DE_INFRAESTRUCTURA]
    total = len(list(REFERENCIAS.glob("*.md")))
    print(f"\nMÓDULOS DE RAMA QUE NINGÚN EVAL NOMBRA — {len(de_rama)} de {total}")
    print("  Esto es deuda de cobertura: la rama existe y ninguna consulta la ejercita.")
    for nombre in de_rama:
        print(f"  · {nombre}")
    if infra:
        print(f"\n  Y {len(infra)} de infraestructura, que NO son deuda: no describen derecho "
              f"sino cómo")
        print("  trabaja la skill, y cada caso los ejercita de costado.")
        print("  " + ", ".join(infra))

    casos = [p for p in sorted(EVALS.iterdir())
             if p.is_dir() and (p / "caso.md").is_file()] if EVALS.is_dir() else []
    sin_correr = evals_sin_correr()
    print(f"\nEVALS ESCRITOS Y SIN CORRER — {len(sin_correr)} de {len(casos)}")
    if not sin_correr:
        print("  Ninguno. Todos los casos tienen una medición anotada.")
    else:
        print("  El caso existe y nadie lo pasó por el sistema: hay consulta, no hay medición.")
        print("  Lo declara cada `resultado.md`, que se escribe igual y no vacío.")
        for nombre in sin_correr:
            print(f"  · {nombre}")

    marcadas = fuentes_marcadas_para_revisar()
    print(f"\nFUENTES BAJADAS Y MARCADAS PARA REVISAR — {len(marcadas)}")
    if not marcadas:
        print("  Ninguna. Todo lo bajado pasó el control de su descargador.")
    else:
        print("  Lo escribió el descargador en su procedencia y sigue sin resolver. Es texto")
        print("  offline que ya sabemos defectuoso, y la skill lo usa igual.")
    for corpus, slug, problema in marcadas:
        print(f"  · {corpus}/{slug}")
        print(f"      {problema[:110]}")

    print("\nLO QUE MIDEN OTRAS HERRAMIENTAS")
    print("  reformas que están en el texto bajado y ningún módulo leyó")
    print("    python3 herramientas/reformas_no_leidas.py")
    print("  normas citadas con articulado y sin bajar")
    print("    python3 herramientas/cobertura_normativa.py")
    print("  normas bajadas que ningún módulo, script ni eval nombra")
    print("    python3 herramientas/normas_huerfanas.py")
    print("  ramas que entraron como sección y no tienen disparador")
    print("    python3 herramientas/ramas_sin_disparador.py")
    print("  documentos de jurisprudencia sin leer o con defecto de OCR")
    print("    python3 herramientas/calidad_ocr.py --pendientes")
    print("  prosa candidata contra kb/, para leerla antes de que el candado la reclame")
    print("    python3 herramientas/fuga_textual.py derecho/evals/*/*.md")
    print("  reclamos de faltante que la propia carpeta fuentes/ ya desmiente")
    print("    python3 herramientas/deuda_vencida.py")
    print("  cifras de la documentación desfasadas, y el censo de las sueltas")
    print("    python3 herramientas/cifras.py")
    print("  datos y series de la capa offline")
    print("    python3 derecho/skills/derecho-argentino/scripts/estado.py")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
