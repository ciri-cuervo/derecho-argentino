#!/usr/bin/env python3
"""Detector de fuga textual desde `argentina/kb/` hacia el resto del repositorio.

La frontera de licencia de este repo es la ruta: lo que está bajo `kb/` es obra de
Cristian Aboitiz -capa 2, uso comercial con autorización previa- y lo que está afuera
es MIT. Llevar un instituto de un perfil heredado a `references/` exige REESCRIBIRLO
contra fuente primaria, no copiarlo. Este script mide si eso se cumplió.

Método: normaliza a minúsculas sin puntuación y compara secuencias contiguas de nueve
palabras. Una coincidencia de nueve palabras seguidas no es casualidad.

El filtro que importa: una coincidencia que TAMBIÉN aparece en `fuentes/normas/` es
texto legal citado, de libre reproducción, y no es fuga. Solo se reportan como PROSA
las que coinciden con kb/ y no con la fuente primaria. Esas son las que hay que
reescribir.

Uso, desde la raíz del repositorio:

    python3 herramientas/fuga_textual.py argentina/skills/derecho-argentino/references/*.md

Sale con código 1 si encontró prosa, para poder encadenarlo.

No se instala con el plugin: vive fuera de `argentina/`.
"""

import re
import sys
import pathlib

N = 9
RAIZ_KB = pathlib.Path("argentina/kb")
RAIZ_FUENTES = pathlib.Path("argentina/fuentes/normas")


CODIGO = re.compile(r"`[^`\n]*`")
RUTA = re.compile(r"[\w./-]+\.(?:md|txt|json|py|pdf)\b")
# Cita del perfil heredado para nombrar su error: *"..."*. Los bloques de contradicciones
# nominadas la usan, y test_scripts.py exige que sea VERBATIM contra kb/. Sin esta exclusión
# los dos guardarrailes se pisan: uno obliga a copiar la frase y el otro la reporta como fuga.
CITA_DEL_PERFIL = re.compile(r'\*"[^"\n]{15,}"\*')


def normalizar(texto: str) -> list[str]:
    """Minúsculas, sin puntuación ni marcado, colapsando espacios.

    Antes de normalizar se sacan los tramos entre backticks, las rutas de archivo y las citas
    entrecomilladas del perfil: una tabla de ruteo que apunta a `kb/...` comparte cadenas
    largas con kb/ por construcción, y eso es la referencia funcionando, no prosa copiada.
    """
    texto = CITA_DEL_PERFIL.sub(" ", texto)
    texto = CODIGO.sub(" ", texto)
    texto = RUTA.sub(" ", texto)
    texto = texto.lower()
    texto = re.sub(r"[^a-zaeiounu\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00fc0-9 ]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip().split()


def secuencias(palabras: list[str], n: int = N) -> set[str]:
    return {" ".join(palabras[i:i + n]) for i in range(len(palabras) - n + 1)}


# Vocabulario de cita: numeros de norma, fechas, artículos, incisos, boletines. Una secuencia
# hecha mayormente de esto es un DATO -que norma, de que fecha, que artículo-, no prosa de nadie.
# El proyecto ya lo tiene dicho: el articulado, los plazos y las carátulas de fallos se mueven
# libres; lo que no se mueve es la redacción.
CITA = {
    "art", "arts", "articulo", "articulos", "inc", "incs", "inciso", "incisos", "ley", "leyes",
    "decreto", "decretos", "dec", "dnu", "res", "resolucion", "resoluciones", "rg", "acordada",
    "ac", "bo", "cn", "ccycn", "ccyc", "lct", "ldc", "cpccba", "cpccn", "cpp", "cppf", "srt",
    "arca", "afip", "scba", "csjn", "sancionada", "sustituido", "incorporado", "derogado",
    "vigencia", "texto", "segun", "según", "resolución", "bis", "ter", "quater",
    "quinquies", "y", "de", "del", "la",
    "el", "los", "las", "al", "a", "en", "por", "o", "un", "una", "no",
    # Unidades y adjetivos de plazo. Una fila de tabla que dice materia, numero y norma es
    # el dato "cuanto tiempo da esa norma", y el proyecto ya lo declara de movimiento libre.
    "dia", "dias", "mes", "meses", "anio", "anios", "ano", "anos", "hora", "horas", "plazo",
    "plazos", "habil", "habiles", "corrido", "corridos", "judicial", "judiciales",
    "administrativo", "administrativos", "primeras", "despacho", "siguiente", "inmediato",
    "vence", "vencimiento", "computo", "nacional", "federal", "provincial", "pba", "caba",
}


def es_cita(secuencia: str) -> bool:
    """True si la secuencia es mayormente numeros y vocabulario de cita, no redacción."""
    palabras = secuencia.split()
    datos = sum(1 for p in palabras if p.isdigit() or p in CITA)
    return datos >= len(palabras) - 2


def corpus(raiz: pathlib.Path, patrones: tuple[str, ...],
           excluir: set[pathlib.Path] | None = None) -> set[str]:
    excluir = {p.resolve() for p in (excluir or set())}
    acumulado: set[str] = set()
    for patron in patrones:
        for archivo in raiz.rglob(patron):
            if archivo.resolve() in excluir:
                continue
            texto = archivo.read_text(encoding="utf-8", errors="ignore")
            acumulado |= secuencias(normalizar(texto))
    return acumulado


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _veredictos

BASE = pathlib.Path("herramientas/fuga-revisada.json")


def cargar_base():
    """Línea de base: las coincidencias ya revisadas a mano y su veredicto.

    El detector marca candidatos, no culpables. Decidir si una coincidencia es cita legal,
    dato o prosa copiada es una lectura, no una heurística, y esa lectura hay que poder
    registrarla. Lo que este archivo guarda es el resultado de haberla hecho: si una secuencia
    figura acá, ya se miro y se decidió que puede quedar.

    La consecuencia útil: la corrida diaria no reporta el total histórico sino lo NUEVO, que
    es lo unico sobre lo que hay que decidir algo.

    El sobre del archivo es el común a los cinco: ver `_veredictos.py`.
    """
    return _veredictos.cargar(BASE, "secuencias", vacio=[])


# Excepción declarada en LICENCIAS.md: los textos canónicos de los marcadores vienen de
# kb/marcadores-GLOSARIO.md y se transcriben exactos a propósito, porque son vocabulario
# controlado del que dependen los scripts. Coincidir ahí es lo correcto, no una fuga.
EXCEPCIONES = {"marcadores.md"}

# La frontera es la ruta, pero hay dos archivos bajo kb/ que NO son de la capa 2: los dos
# README, escritos por nosotros para explicar que es ese directorio, con que licencia entra
# y en que contradice a la skill. Son capa 3a viviendo bajo una ruta que declara capa 2. Si
# se los deja en el corpus, el detector compara nuestro texto contra si mismo y reporta como
# fuga la regla del CCT o la advertencia sobre la Ley 11.653, que son nuestras. Registrado en
# LICENCIAS.md, sección 2.
NO_SON_CAPA_2 = {pathlib.Path("argentina/kb/project/README.md"),
                 pathlib.Path("argentina/kb/README.md")}


def main(argv: list[str]) -> int:
    aceptar = "--aceptar" in argv
    argv = [a for a in argv if a != "--aceptar"]
    if not argv:
        print("uso: fuga_textual.py [--aceptar] <archivo.md> [...]", file=sys.stderr)
        return 2
    if not RAIZ_KB.is_dir():
        print(f"no encuentro {RAIZ_KB}: corre el script desde la raiz del repo", file=sys.stderr)
        return 2

    kb = corpus(RAIZ_KB, ("*.md", "*.template"), excluir=NO_SON_CAPA_2)
    legal = corpus(RAIZ_FUENTES, ("*.txt",)) if RAIZ_FUENTES.is_dir() else set()
    sobre, revisadas_base = cargar_base()
    revisadas = set(revisadas_base)
    if revisadas:
        print(f"línea de base: {len(revisadas)} secuencias revisadas el "
              f"{sobre['fijado']}\n")

    total_prosa = 0
    nuevas: set[str] = set()
    for ruta in argv:
        archivo = pathlib.Path(ruta)
        if archivo.name in EXCEPCIONES:
            print(f"{archivo}: excepcion declarada en LICENCIAS.md, no se mide")
            continue
        propias = secuencias(normalizar(archivo.read_text(encoding="utf-8")))
        coincidencias = propias & kb
        prosa = sorted(
            s for s in coincidencias
            if s not in legal and not es_cita(s) and s not in revisadas
        )
        total_prosa += len(prosa)
        nuevas |= set(prosa)
        libres = len(coincidencias) - len(prosa)
        print(f"{archivo}: {len(coincidencias)} coincidencias con kb/, "
              f"{libres} texto legal o cita, {len(prosa)} PROSA")
        for secuencia in prosa:
            print(f"  PROSA: {secuencia}")

    if aceptar and nuevas:
        _veredictos.guardar(BASE, sobre, "secuencias", sorted(revisadas | nuevas))
        print(f"\nlinea de base actualizada: +{len(nuevas)} secuencias revisadas")
        return 0

    if total_prosa:
        print(f"\nfuga textual: {total_prosa} secuencias NUEVAS, sin revisar")
        print("Leerlas una por una y decidir: si es texto legal o dato, va a la línea de base")
        print("con --aceptar; si es prosa de kb/, se reescribe el módulo.")
        return 1
    print("\nfuga textual: 0 secuencias nuevas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
