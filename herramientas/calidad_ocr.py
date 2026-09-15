#!/usr/bin/env python3
"""Dice, documento por documento, si el texto extraido sirve para transcribir.

POR QUE EXISTE

fallos-csjn.md afirmaba que los fallos con la capa de texto arruinada eran
"los cuatro anteriores a 1994", por escaneo. La regla por epoca es FALSA:
"Gongora" es de 2013 y su texto esta mezclado igual que los de los ochenta, y
"Rodriguez Pereyra" (2012) trae sustituciones. La Corte publico escaneos en
muchos anios. La propiedad es del documento.

QUE SE PUEDE MEDIR Y QUE NO

Hay tres defectos y no se detectan igual:

  BASURA       el OCR devolvio caracteres que no son letras:
               `Considerando: 1*) i BE`i Que >`vei segtin`.
               SE MIDE BIEN. Es lo unico que este script calcula.

  LAYOUT       NO es un defecto del documento sino de como se lo extrae, y se
               tardo en verlo. Cinco fallos -"Gongora", "Buffoni", "Duarte",
               el de reintegro de hijo y "Villamil"- parecian tener las
               columnas intercaladas y se los habia dado por intranscribibles.
               Con `pdftotext -layout` se leen enteros: "Buffoni" se leyo asi
               y su holding esta escrito. La categoria "mezclado" no existia.
               REGLA: extraer siempre con -layout, y no declarar roto un
               documento sin haberlo probado con esa opcion.

  SUSTITUCION  el OCR cambio letras y dejo palabras validas pero equivocadas:
               "apelanie remiten al andlisis de evestiones de hecho" en
               "Santa Coloma". -layout NO lo arregla, porque el problema no
               esta en el orden sino en las letras.

Para los dos ultimos se probaron cuatro medidas y las cuatro fallaron contra
un caso conocido, asi que NO estan en el script. Tres de las cuatro buscaban
detectar una "mezcla" que despues resulto no existir -era la extraccion-, lo
que explica por que ninguna daba: estaban midiendo un fenomeno inventado.

  - contar formulas juridicas contiguas ordenaba por largo del archivo:
    "Montalvo", destruido, salia mejor que "Mosca", que se lee bien;
  - exigir la formula de encabezado marcaba los veintidos fallos de la SCBA,
    que abren distinto que la Corte y estan sanos;
  - agregar una formula por tribunal seguia marcando los que vienen firmados
    digitalmente, que no traen acuerdo;
  - contar tokens cortos raros no separaba "Quaranta" (limpio, 2,4%) de
    "reintegro de hijo" (mezclado, 2,4%).

Una medida que se equivoca sobre un fallo conocido no sirve para decidir sobre
los desconocidos. Entonces el veredicto de esos dos defectos NO se estima: se
LEE, y queda registrado en lecturas-ocr.json con la fecha y lo que se vio. El
script informa lo medido y lo leido por separado, y marca como "sin leer" lo
que todavia nadie miro.

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
CORPUS = RAIZ.parent / "argentina" / "fuentes" / "jurisprudencia"


def basura(ruta: pathlib.Path) -> float:
    """Proporcion de tokens con algun caracter que no es del espaniol.

    Con -layout, que es como hay que extraer siempre: sin esa opcion el
    extractor reordena las palabras de los PDF a dos columnas y un documento
    sano parece roto.
    """
    crudo = subprocess.run(["pdftotext", "-q", "-layout", str(ruta), "-"],
                           capture_output=True, text=True).stdout.lower()
    texto = re.sub(r"\s+", " ", crudo)
    tokens = [t for t in texto.split() if any(c.isalpha() for c in t)]
    sucios = sum(1 for t in tokens
                 if any(c not in LETRAS and not c.isdigit() and c not in PUNTUACION
                        for c in t))
    return sucios / max(len(tokens), 1)


def main(argv: list[str]) -> int:
    _externos.exigir("pdftotext")
    solo_pendientes = "--pendientes" in argv
    leidas = _veredictos.cargar(LECTURAS, "lecturas", vacio={})[1]

    pdfs = sorted(CORPUS.glob("*.pdf"))
    if not pdfs:
        print(f"sin PDF en {CORPUS}")
        return 1

    filas, pendientes = [], []
    for p in pdfs:
        b = basura(p)
        leido = leidas.get(p.stem)
        if leido is None:
            pendientes.append(p.stem)
        estado = leido["estado"] if leido else "sin leer"
        if b > UMBRAL_BASURA or estado not in ("limpio", "sin leer"):
            filas.append((estado, b, p.stem, (leido or {}).get("nota", "")))

    if not solo_pendientes:
        print("  Documentos con defecto, medido o leido:\n")
        for estado, b, slug, nota in sorted(filas):
            med = f"basura {b:.0%}" if b > UMBRAL_BASURA else "  --  "
            print(f"  {estado:12} {med:12}  {slug}")
            if nota:
                print(f"               {nota}")
        print()

    print(f"  {len(pdfs)} documentos | {len(filas)} con defecto | "
          f"{len(pendientes)} sin leer")
    if pendientes:
        print("\n  SIN LEER: que no figuren arriba no prueba que su texto este bien,")
        print("  solo que nadie lo miro. Leer y registrar en lecturas-ocr.json:")
        for s in pendientes:
            print(f"    {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
