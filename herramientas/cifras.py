#!/usr/bin/env python3
"""Genera las cifras de inventario de la documentación y controla que ninguna quede suelta.

    python3 herramientas/cifras.py             # verifica y censa: sale 1 si algo esta mal
    python3 herramientas/cifras.py --sellar    # reescribe cada cifra con lo que hay en disco
    python3 herramientas/cifras.py --censo     # solo el censo

La documentación afirma cuántos módulos, normas, fallos, comandos y casos de prueba hay. Escritas
a mano, esas cifras envejecen en silencio: el repositorio se contradice solo y el primero en
notarlo es quien lo lee. Ya paso --`LICENCIAS.md` declaraba dos documentos en `docs/` cuando había
cuatro-- y no lo atrapo nada, porque hasta ahora la cobertura era opt-in: cada cifra necesitaba que
alguien se acordara de escribirle un test, y el que no se acuerda no rompe nada.

TRES PIEZAS, y la tercera es la que importa.

    --sellar     reescribe la cifra en su lugar. El ancla es el patrón de texto que la rodea, no
                 un marcador en el archivo: los .md no cambian en nada. Es a propósito, porque la
                 mitad de estos archivos viajan dentro del plugin y los lee el modelo, y un
                 <!--#normas-->132<!--/--> ahí no es invisible: es ruido en las instrucciones.

    --verificar  no escribe y sale con 1. Es lo que corre CI.

    --censo      busca CUALQUIER cifra pegada a un sustantivo de inventario y exige que este
                 declarada: en el registro de anclas, en la lista de cubiertas por otro test, o
                 en `cifras-revisadas.json` con motivo. Lo que no este en ninguna, rompe. Eso
                 invierte el default: una cifra nueva sin declarar ya no pasa desapercibida.

Sale con código 1 si algo esta desfasado, suelto o no engancha. Cero dependencias externas.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import _veredictos

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = Path(__file__).resolve().parent / "cifras.json"
VEREDICTOS = Path(__file__).resolve().parent / "cifras-revisadas.json"

# Hasta veinte alcanza para todo lo que hoy se escribe con letras. Arriba de eso el script se
# niega en vez de inventar "treinta y uno": preferimos un control que se plante antes que uno
# que escriba mal castellano. El 1 tampoco esta: "un módulos" no existe, y pasar al singular
# obliga a reescribir la frase, que es trabajo de una persona.
PALABRAS = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho",
            9: "nueve", 10: "diez", 11: "once", 12: "doce", 13: "trece", 14: "catorce",
            15: "quince", 16: "dieciséis", 17: "diecisiete", 18: "dieciocho",
            19: "diecinueve", 20: "veinte"}
NUMEROS = {v: k for k, v in PALABRAS.items()}


class RegistroInvalido(ValueError):
    """El registro pide algo imposible. Se dice cual, no se sigue de largo."""


def _alternancia(palabras) -> str:
    # Las más largas primero: si "dieciseis" va después de "seis", la alternancia matchea el
    # final de la palabra y el número sale mal.
    return "|".join(sorted(palabras, key=len, reverse=True))


def cargar():
    reg = json.loads(REGISTRO.read_text(encoding="utf-8"))
    # La capa 2 se sale por la ruta y por cinco excepciones que la ruta NO dice. Comprobar sólo
    # `argentina/kb/` dejaba en el alcance a `argentina/evals/README.md`, que es una de ellas.
    # Es el error que este repositorio comete sin querer: se cruza la frontera corrigiendo.
    for archivo in list(reg["anclas"]) + list(reg["alcance"]):
        for ruta in reg["capa_2"]["rutas"]:
            if archivo == ruta or archivo.startswith(ruta):
                raise RegistroInvalido(
                    f"{archivo}: es capa 2, de otro autor. Este script no le escribe ni lo censa: "
                    f"lo vigila `frontera_kb.py`. Ver LICENCIAS.md sección 2.")
    return reg


# ---------------------------------------------------------------- medir

def medir(nombre: str, definicion: dict) -> int:
    """Cinco tipos y nada más. El límite es deliberado: son cinco formas de contar, no un
    lenguaje. Si una metrica nueva no entra en ninguna, es una senal de que la cifra que
    pretende sellar tampoco esta bien definida en la prosa."""
    tipo = definicion["tipo"]
    # `glob` y `glob_excluye` cuentan ARCHIVOS. Sin ese filtro, un patrón recursivo como
    # `kb/**/*` suma los directorios y la cifra sale inflada sin que se note.
    if tipo == "glob":
        return len([f for f in RAIZ.glob(definicion["patron"]) if f.is_file()])
    if tipo == "carpetas":
        return len([d for d in RAIZ.glob(definicion["patron"]) if d.is_dir()])
    if tipo == "glob_excluye":
        return len([f for f in RAIZ.glob(definicion["patron"]) if f.is_file()
                    and not any(f.match(x) for x in definicion["excluye"])])
    if tipo == "json_largo":
        d = json.loads((RAIZ / definicion["archivo"]).read_text(encoding="utf-8"))
        return len(d[definicion["clave"]])
    if tipo == "renglones":
        texto = (RAIZ / definicion["archivo"]).read_text(encoding="utf-8")
        return len(re.findall(definicion["patron"], texto, re.M))
    raise RegistroInvalido(f"{nombre}: tipo de metrica desconocido `{tipo}`")


def metricas(reg: dict) -> dict:
    return {n: medir(n, d) for n, d in reg["metricas"].items()}


# ---------------------------------------------------------------- anclas

def compilar(ancla: str, formato: str) -> re.Pattern:
    """El espacio del ancla matchea cualquier espacio, incluido un salto de renglon.

    La prosa se envuelve: `los 109\\narchivos de kb/` es la misma frase que `los 109 archivos`,
    y un ancla que no lo tolera se despega cada vez que alguien reacomoda un párrafo. El
    reemplazo no se ve afectado, porque solo se reescribe el grupo del número.
    """
    if ancla.count("{n}") != 1:
        raise RegistroInvalido(f"«{ancla}»: el ancla lleva un solo {{n}}")
    antes, despues = (re.escape(p).replace(r"\ ", r"\s+") for p in ancla.split("{n}"))
    grupo = r"(\d{1,4})" if formato == "digito" else f"(?i:({_alternancia(NUMEROS)}))"
    return re.compile(antes + grupo + despues)


def escribir(valor: int, formato: str, tal_como_estaba: str, ancla: str) -> str:
    if formato == "digito":
        return str(valor)
    if valor not in PALABRAS:
        raise RegistroInvalido(
            f"«{ancla}»: la metrica vale {valor} y se pide en palabras. "
            f"{'El singular obliga a reescribir la frase' if valor < 2 else 'La tabla llega a veinte'}"
            f": cambiar ese ancla a digitos o arreglar la prosa a mano.")
    palabra = PALABRAS[valor]
    return palabra.capitalize() if tal_como_estaba[:1].isupper() else palabra


def leer(texto: str, formato: str) -> int:
    return int(texto) if formato == "digito" else NUMEROS[texto.lower()]


def revisar_anclas(reg: dict, medidas: dict, sellar: bool):
    """Devuelve (problemas, sellados). Un ancla que no engancha exactamente una vez es un
    problema y no un aviso: si la frase se reescribió, corresponde un rojo y no un sellado a
    ciegas sobre la ocurrencia que quedo."""
    problemas, sellados = [], []
    for archivo, anclas in reg["anclas"].items():
        ruta = RAIZ / archivo
        texto = ruta.read_text(encoding="utf-8")
        for entrada in anclas:
            ancla, metrica = entrada["ancla"], entrada["metrica"]
            formato = entrada.get("formato", "digito")
            patron = compilar(ancla, formato)
            hallados = list(patron.finditer(texto))
            if len(hallados) != 1:
                problemas.append(f"{archivo}: «{ancla}» engancha {len(hallados)} veces, "
                                 f"tiene que enganchar una")
                continue
            m = hallados[0]
            esperado = medidas[metrica]
            nuevo = escribir(esperado, formato, m.group(1), ancla)
            if leer(m.group(1), formato) == esperado:
                continue
            if not sellar:
                problemas.append(f"{archivo}: «{ancla}» dice {m.group(1)} y {metrica} vale "
                                 f"{esperado}")
                continue
            texto = texto[:m.start(1)] + nuevo + texto[m.end(1):]
            # `->` y no `→`: la flecha U+2192 no entra en cp1252 y rompe la consola de Windows
            # justo después de haber reescrito los archivos. Ver docs/DESARROLLO.md.
            sellados.append(f"{archivo}: {m.group(1)} -> {nuevo}  ({metrica})")
        if sellar:
            ruta.write_text(texto, encoding="utf-8")
    return problemas, sellados


# ---------------------------------------------------------------- censo

def patron_del_censo(reg: dict) -> re.Pattern:
    # El lookbehind es lo que evita que `python3 herramientas/test_frontera.py` parezca decir
    # "3 herramientas". NO se saltean los bloques de código: el árbol de directorios de
    # ARQUITECTURA.md esta dentro de uno y contiene anclas de verdad.
    nombres = _alternancia(reg["sustantivos"])
    return re.compile(r"(?<![\w/.\-])(?i:(\d{1,4}|" + _alternancia(NUMEROS) + r"))"
                      r"\s+\*{0,2}(?i:(" + nombres + r"))\b")


def cubiertos(reg: dict, archivo: str, texto: str) -> list:
    """Los tramos ya declarados: lo que matchea un ancla y lo que mide otro test."""
    tramos = []
    for entrada in reg["anclas"].get(archivo, []):
        patron = compilar(entrada["ancla"], entrada.get("formato", "digito"))
        tramos += [m.span() for m in patron.finditer(texto)]
    for entrada in reg["cubiertas"]:
        if entrada["archivo"] == archivo:
            tramos += [m.span() for m in re.finditer(entrada["patron"], texto)]
    return tramos


def censar(reg: dict, veredictos: dict):
    patron = patron_del_censo(reg)
    huerfanas, usados = [], set()
    for archivo in reg["alcance"]:
        texto = (RAIZ / archivo).read_text(encoding="utf-8")
        tramos = cubiertos(reg, archivo, texto)
        for m in patron.finditer(texto):
            if any(ini <= m.start() and m.end() <= fin for ini, fin in tramos):
                continue
            # La clave va con el espacio aplanado. La prosa se envuelve, así que "dos módulos"
            # puede quedar partido en dos renglones: sin aplanar, el veredicto se despegaria
            # cada vez que alguien reacomoda un párrafo.
            clave = f"{archivo} | {re.sub(r'[ \t]*\n[ \t]*', ' ', m.group(0))}"
            if clave in veredictos:
                usados.add(clave)
                continue
            renglon = texto[:m.start()].count("\n") + 1
            huerfanas.append(f"{archivo}:{renglon}  «{clave.split(' | ', 1)[1]}»  SIN DECLARAR")
    return huerfanas, sorted(set(veredictos) - usados)


# ---------------------------------------------------------------- cli

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sellar", action="store_true", help="reescribe las cifras")
    ap.add_argument("--censo", action="store_true", help="solo el censo")
    args = ap.parse_args()

    reg = cargar()
    _, veredictos = _veredictos.cargar(VEREDICTOS, "cifras", vacio={})
    medidas = metricas(reg)

    if not args.censo:
        problemas, sellados = revisar_anclas(reg, medidas, args.sellar)
        for linea in sellados:
            print(f"SELLADA  {linea}")
        for linea in problemas:
            print(f"DESFASADA  {linea}")
        if problemas:
            print(f"\n{len(problemas)} "
                  f"{'cifra que no coincide' if len(problemas) == 1 else 'cifras que no coinciden'}"
                  f" con el disco. Para arreglarlas: python3 herramientas/cifras.py --sellar")
            return 1
        if args.sellar:
            print(f"{len(sellados)} cifras selladas sobre {sum(len(v) for v in reg['anclas'].values())} anclas")
            return 0
        print(f"cifras al dia: {sum(len(v) for v in reg['anclas'].values())} anclas "
              f"sobre {len(medidas)} metricas")

    huerfanas, sin_usar = censar(reg, veredictos)
    for linea in huerfanas:
        print(linea)
    for clave in sin_usar:
        print(f"VEREDICTO MUERTO  {clave}  (la cifra ya no está en el archivo)")
    if huerfanas or sin_usar:
        print(f"\ncenso: {len(huerfanas)} "
              f"{'cifra sin declarar' if len(huerfanas) == 1 else 'cifras sin declarar'}, "
              f"{len(sin_usar)} {'veredicto muerto' if len(sin_usar) == 1 else 'veredictos muertos'}"
              f". Una cifra nueva se declara en cifras.json --si la mide el repo-- o en "
              f"cifras-revisadas.json con motivo --si no es inventario--.")
        return 1
    print(f"censo: sin cifras sueltas en {len(reg['alcance'])} archivos "
          f"({len(veredictos)} declaradas como no-inventario)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
