#!/usr/bin/env python3
"""Dice, documento por documento, si el texto extraído sirve para transcribir.

POR QUE EXISTE

fallos-csjn.md afirmaba que los fallos con la capa de texto arruinada eran
"los cuatro anteriores a 1994", por escaneo. La regla por época es FALSA:
"Góngora" es de 2013 y su texto esta mezclado igual que los de los ochenta, y
"Rodriguez Pereyra" (2012) trae sustituciones. La Corte publico escaneos en
muchos años. La propiedad es del documento.

QUE SE PUEDE MEDIR Y QUE NO

Hay tres defectos y no se detectan igual:

  BASURA       el OCR devolvió caracteres que no son letras:
               `Considerando: 1*) i BE`i Que >`vei segtin`.
               SE MIDE BIEN. Es lo unico que este script calcula.

  LAYOUT       NO es un defecto del documento sino de como se lo extrae, y se
               tardo en verlo. Cinco fallos -"Góngora", "Buffoni", "Duarte",
               el de reintegro de hijo y "Villamil"- parecian tener las
               columnas intercaladas y se los había dado por intranscribibles.
               Con `pdftotext -layout` se leen enteros: "Buffoni" se leyó así
               y su holding está escrito. La categoría "mezclado" no existía.
               REGLA: extraer siempre con -layout, y no declarar roto un
               documento sin haberlo probado con esa opción.

  SUSTITUCIÓN  el OCR cambió letras y dejó palabras válidas pero equivocadas:
               "apelanie remiten al andlisis de evestiones de hecho" en
               "Santa Coloma". -layout NO lo arregla, porque el problema no
               está en el orden sino en las letras.

Para los dos últimos se probaron cuatro medidas y las cuatro fallaron contra
un caso conocido, así que NO están en el script. Tres de las cuatro buscaban
detectar una "mezcla" que después resultó no existir -era la extracción-, lo
que explica por que ninguna daba: estaban midiendo un fenomeno inventado.

  - contar fórmulas jurídicas contiguas ordenaba por largo del archivo:
    "Montalvo", destruido, salía mejor que "Mosca", que se lee bien;
  - exigir la formula de encabezado marcaba los veintidós fallos de la SCBA,
    que abren distinto que la Corte y están sanos;
  - agregar una formula por tribunal seguia marcando los que vienen firmados
    digitalmente, que no traen acuerdo;
  - contar tokens cortos raros no separaba "Quaranta" (limpio, 2,4%) de
    "reintegro de hijo" (mezclado, 2,4%).

Una medida que se equivoca sobre un fallo conocido no sirve para decidir sobre
los desconocidos. Entonces el veredicto de esos dos defectos NO se estima: se
LEE, y queda registrado en lecturas-ocr.json con la fecha y lo que se vio. El
script informa lo medido y lo leído por separado, y marca como "sin leer" lo
que todavía nadie miro.

Uso:
  python3 herramientas/calidad_ocr.py            informe
  python3 herramientas/calidad_ocr.py --pendientes   solo lo que falta leer
"""
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _externos
import _veredictos

LETRAS = set("abcdefghijklmnopqrstuvwxyzáéíóúüñ")
PUNTUACION = set(".,;:()[]-–—«»\"'“”‘’/°ºª¿?¡!%$&*+=@#_|\\~^")
UMBRAL_BASURA = 0.06

RAIZ = pathlib.Path(__file__).resolve().parent
LECTURAS = RAIZ / "lecturas-ocr.json"
CORPUS = RAIZ.parent / "derecho" / "fuentes" / "jurisprudencia"


def proporcion_sucia(texto: str) -> float | None:
    """Proporción de tokens con algún carácter que no es del espaniol.

    None cuando no hay ni una palabra: no hay medida. Antes esto daba 0.0,
    porque el cociente se hacía contra `max(len(tokens), 1)`, y 0.0 es la
    lectura de un documento impecable -- un escaneo sin capa de texto pasaba
    por el mejor del corpus. Es el mismo modo de fallar que `_externos` existe
    para tapar, verde con el instrumento apagado, un nivel mas abajo: por
    documento en vez de por corrida. Quien llama tiene que poder distinguir
    "medi y esta limpio" de "no pude medir".

    Va aparte de `basura()` para que se pueda ejercitar sin poppler: la regla
    de que cero palabras no es cero basura es lo que hay que fijar, y no
    depende de como se extrajo el texto.
    """
    texto = re.sub(r"\s+", " ", texto.lower())
    tokens = [t for t in texto.split() if any(c.isalpha() for c in t)]
    if not tokens:
        return None
    sucios = sum(1 for t in tokens
                 if any(c not in LETRAS and not c.isdigit() and c not in PUNTUACION
                        for c in t))
    return sucios / len(tokens)


def basura(ruta: pathlib.Path) -> float | None:
    """Lo mismo, sobre el texto que extrae `pdftotext`. None si no se pudo medir.

    Con -layout, que es como hay que extraer siempre: sin esa opción el
    extractor reordena las palabras de los PDF a dos columnas y un documento
    sano parece roto.
    """
    hecho = subprocess.run(["pdftotext", "-q", "-layout", str(ruta), "-"],
                           capture_output=True, text=True)
    if hecho.returncode != 0:
        return None
    return proporcion_sucia(hecho.stdout)


def main(argv: list[str]) -> int:
    _externos.exigir("pdftotext")
    solo_pendientes = "--pendientes" in argv
    leidas = _veredictos.cargar(LECTURAS, "lecturas", vacio={})[1]

    pdfs = sorted(CORPUS.glob("*.pdf"))
    if not pdfs:
        print(f"sin PDF en {CORPUS}")
        return 1

    filas, pendientes, sin_medir = [], [], []
    for p in pdfs:
        b = basura(p)
        leido = leidas.get(p.stem)
        if leido is None:
            pendientes.append(p.stem)
        estado = leido["estado"] if leido else "sin leer"
        if b is None:
            # No se pudo extraer: no hay medida, y eso NO es un documento limpio.
            # Entra como defecto siempre, porque lo que no se extrae no se transcribe.
            sin_medir.append(p.stem)
            filas.append((estado, b, p.stem, (leido or {}).get("nota", "")))
        elif b > UMBRAL_BASURA or estado not in ("limpio", "sin leer"):
            filas.append((estado, b, p.stem, (leido or {}).get("nota", "")))

    if not solo_pendientes:
        print("  Documentos con defecto, medido o leído:\n")
        for estado, b, slug, nota in sorted(filas, key=lambda f: (f[0], f[1] is not None,
                                                                 f[1] or 0, f[2])):
            if b is None:
                med = "SIN MEDIR"
            elif b > UMBRAL_BASURA:
                med = f"basura {b:.0%}"
            else:
                med = "  --  "
            print(f"  {estado:12} {med:12}  {slug}")
            if nota:
                print(f"               {nota}")
        print()

    print(f"  {len(pdfs)} documentos | {len(filas)} con defecto | "
          f"{len(pendientes)} sin leer | {len(sin_medir)} sin medir")
    if sin_medir:
        print("\n  SIN MEDIR: `pdftotext` no devolvió palabras. Puede ser un escaneo sin capa")
        print("  de texto -- va a reocr_jurisprudencia.py -- o un archivo que no es el PDF que")
        print("  dice ser. No se cuenta como limpio:")
        for s in sin_medir:
            print(f"    {s}")
    if pendientes:
        print("\n  SIN LEER: que no figuren arriba no prueba que su texto este bien,")
        print("  solo que nadie lo miro. Leer y registrar en lecturas-ocr.json:")
        for s in pendientes:
            print(f"    {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
