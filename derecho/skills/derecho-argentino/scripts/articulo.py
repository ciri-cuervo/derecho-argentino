#!/usr/bin/env python3
"""Devuelve un artículo de una norma bajada, con su procedencia, sin abrir el archivo entero.

**Existe por una medida y no por comodidad.** `Read` trae 2.000 renglones y trunca sin avisar;
el CCyCN consolidado tiene más de 27.000 y la LCT casi 5.000. Para transcribir el art. 245 el
modelo abría el archivo, leía la primera parte, volvía con `Grep` y cargaba miles de renglones que
no iba a usar, o daba por leído un texto cortado. Acá entra al contexto sólo el artículo pedido,
y arriba va lo que la sección 2 de la skill exige para citarlo: título de la norma, URL oficial,
fecha de descarga y hash.

Uso:
    python3 articulo.py lct-20744 245
    python3 articulo.py lct-20744 245 245bis 232       # varios de una vez
    python3 articulo.py cp-11179 "145 bis"
    python3 articulo.py ccycn-26994 --listar           # qué artículos reconoce el corte
    python3 articulo.py ley-24669 6 --anexo 1          # el art. 6 del tratado que aprueba

Reconoce los encabezados con que las fuentes oficiales abren un artículo —`ARTICULO 1° —`,
`ARTÍCULO 22 BIS:`, `Art. 245. —`, `Artículo 1° —`, `ARTÍCULO 1º Las...`— y **sólo al principio
del renglón**. Un
`Artículo 145 bis:` citado dentro del cuerpo de otro artículo no corta: viene después de un
renglón que termina en dos puntos anunciando la transcripción, y un encabezado real no.

No corrige nada del texto: lo que sale es lo que está en el `.txt`, con las notas de InfoLEG
sobre sustituciones y derogaciones, que son parte de lo que hay que leer antes de citar. Y no
sabe si el artículo está vigente: eso lo dice la nota que trae, o `changelog-normativo.md`.

**Una ley aprobatoria trae dos numeraciones**: la suya —«Apruébase el Protocolo...»— y la del
texto anexo, que vuelve a empezar en 1. Sin `--anexo`, el corte de siempre: los números que
se repiten se quedan con su primera aparición, así que en `ccycn-26994` los arts. 1 a 8 son los
de la Ley 26.994 y del 9 en adelante los del Código, y en `ley-24669` no hay art. 6 que pedir.
Con `--anexo N` sale sólo la numeración N, contada desde cada vez que el texto vuelve al art. 1,
y ahí también cuenta el encabezado que es el número solo en su renglón —`Artículo 6`—, que es
como vienen los tratados en InfoLEG.

Códigos de salida: 0 encontró todo lo pedido; 2 no hay repo, no existe la norma o falta un
artículo, y en los tres casos dice cuál.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _raiz import datos

# El encabezado de un artículo, tal como lo escriben InfoLEG, normas.gba y los digestos
# porteños: `ARTICULO 1° —`, `Art. 245. —`, `ARTÍCULO 22 BIS:` y también `Artículo 1° —`, que
# es la grafía de más de cien textos del repositorio. El sufijo latino admite las dos mayúsculas
# que conviven en el mismo cuerpo (`bis`, `BIS`, `quáter`, `QUÁTER`).
ENCABEZADO = re.compile(
    r"^(?:ART[IÍ]CULO|Art\.|Artículo)\s*(?P<numero>\d+)\s*[°º]?\s*"
    r"(?:(?P<sufijo>(?i:bis|ter|qu[aá]ter|quinquies|sexies|septies|octies|nonies|decies))\b)?"
    r"\s*(?:[.:\-—–]|(?=\s+[A-ZÁÉÍÓÚÜÑ¿(«\"]))")

# Una ley que incorpora un artículo a otra lo transcribe: `Incorpórase como artículo 145 bis
# del Código Penal, el siguiente:` y en el renglón de abajo `Artículo 145 bis: El que...`. Ese
# renglón tiene forma de encabezado y no lo es. Lo delata el renglón anterior, que anuncia la
# transcripción —«el siguiente:», «redactado de la siguiente manera:»— y termina en dos puntos.
# Que termine en dos puntos no alcanza: «sancionan con fuerza de Ley:» precede al art. 1 de
# toda ley de InfoLEG, y con esa sola señal el art. 1 desaparecía de todas.
ANUNCIA_TRANSCRIPCION = re.compile(
    r"(siguiente|redactad[oa]|sustit[uú]|incorp[oó]r|reempl[aá]z|modif[ií]c)[^\n]*:\s*$", re.I)

PROCEDENCIA = ("Fuente:", "Descargado:", "SHA-256")

# Sólo para los anexos: además, el número solo en su renglón. No entra al corte principal porque
# en él ese renglón partía artículos de más de cuarenta normas que hoy se citan bien.
ENCABEZADO_ANEXO = re.compile(ENCABEZADO.pattern[:-1] + r"|\s*$)")


def clave(numero: str, sufijo: str | None) -> str:
    s = (sufijo or "").lower().replace("á", "a")
    return f"{int(numero)}{' ' + s if s else ''}"


def pedido(texto: str) -> str:
    """Normaliza lo que tipea el usuario: `245bis`, `245 BIS` y `245 bis` son el mismo."""
    m = re.fullmatch(r"\s*(\d+)\s*([A-Za-zÁá]+)?\s*", texto)
    if not m:
        raise ValueError(f"no entiendo el artículo «{texto}»: se espera un número y, si hace "
                         f"falta, bis/ter/quater")
    return clave(m.group(1), m.group(2))


# Respaldo para los textos donde el corte principal no encuentra ningún artículo: el número solo
# con su raya —`2º —`, el Reglamento para la Justicia Nacional—, el ordinal escrito con la letra
# o —`Artículo 1o:`— y el encabezado partido en dos renglones —`ARTICULO` y abajo `1º.- La`—.
# Corre únicamente si el principal devuelve vacío, así que no toca ningún texto que ya se lea.
ENCABEZADO_RESPALDO = re.compile(
    r"^(?:(?:ART[IÍ]CULO|Art\.|Artículo)\s*)?(?P<numero>\d+)\s*(?:[°º]|o(?=\s*[.:\-—–]))?\s*"
    r"(?:(?P<sufijo>(?i:bis|ter|qu[aá]ter|quinquies|sexies|septies|octies|nonies|decies))\b)?"
    r"\s*[.:\-—–]+\s")


def _unir_encabezados_partidos(cuerpo: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(cuerpo):
        if (re.fullmatch(r"\s*ART[IÍ]CULO\s*", cuerpo[i], re.I) and i + 1 < len(cuerpo)
                and re.match(r"\s*\d", cuerpo[i + 1])):
            out.append(cuerpo[i].strip() + " " + cuerpo[i + 1].strip())
            i += 2
            continue
        out.append(cuerpo[i])
        i += 1
    return out


def partir(cuerpo: list[str]) -> dict[str, list[str]]:
    """Cada artículo con sus renglones, en orden de aparición. Lo anterior al primero se descarta."""
    articulos = _partir(cuerpo, ENCABEZADO)
    if not articulos:
        articulos = _partir(_unir_encabezados_partidos(cuerpo), ENCABEZADO_RESPALDO)
    return articulos


def _partir(cuerpo: list[str], encabezado_re) -> dict[str, list[str]]:
    articulos: dict[str, list[str]] = {}
    actual = None
    anterior = ""
    for linea in cuerpo:
        m = encabezado_re.match(linea)
        if m and ANUNCIA_TRANSCRIPCION.search(anterior):
            m = None
        if linea.strip():
            anterior = linea
        if m:
            actual = clave(m.group("numero"), m.group("sufijo"))
            # Un mismo número dos veces es el consolidado intercalando texto viejo: se queda
            # el primero, que es el vigente en las fuentes que hacen eso.
            if actual in articulos:
                actual = None
                continue
            articulos[actual] = [linea]
        elif actual is not None:
            articulos[actual].append(linea)
    for k, ls in articulos.items():
        while ls and not ls[-1].strip():
            ls.pop()
    return articulos


def anexos(cuerpo: list[str]) -> list[dict[str, list[str]]]:
    """Cada numeración del texto por separado: la 0 es la de la norma y la N, la del anexo N.

    Una numeración nueva empieza cuando vuelve el art. 1 ya visto; otro número repetido es el
    consolidado intercalando texto viejo, y se queda el primero."""
    bloques: list[dict[str, list[str]]] = [{}]
    actual = None
    anterior = ""
    for linea in cuerpo:
        m = ENCABEZADO_ANEXO.match(linea)
        if m and ANUNCIA_TRANSCRIPCION.search(anterior):
            m = None
        if linea.strip():
            anterior = linea
        if m:
            actual = clave(m.group("numero"), m.group("sufijo"))
            if actual in bloques[-1]:
                if actual != "1":
                    actual = None
                    continue
                bloques.append({})
            bloques[-1][actual] = [linea]
        elif actual is not None:
            bloques[-1][actual].append(linea)
    for articulos in bloques:
        for ls in articulos.values():
            while ls and not ls[-1].strip():
                ls.pop()
    return bloques


def encabezado(lineas: list[str]) -> list[str]:
    """Título y procedencia, que son las primeras líneas del `.txt` que escribe el descargador."""
    salida = [lineas[0].rstrip()] if lineas else []
    for l in lineas[1:20]:
        if l.startswith(PROCEDENCIA):
            salida.append(l.rstrip())
    return salida


def carpeta_normas(repo=None) -> Path | None:
    d = datos(repo)
    return None if d is None else d.parent / "normas"


def main(argv=None) -> int:
    # Hay textos bajados con caracteres que cp1252 no tiene (■, ✓, №). Escaparlos deja la cita
    # visiblemente marcada; sin esto la consola de Windows corta con UnicodeEncodeError.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("norma", help="slug del texto en fuentes/normas/, sin .txt: lct-20744")
    p.add_argument("articulo", nargs="*", help="245, 245bis, «145 bis»")
    p.add_argument("--listar", action="store_true",
                   help="lista los artículos que reconoce en vez de imprimir uno")
    p.add_argument("--anexo", type=int, default=0,
                   help="numeración del texto anexo: 1 es el tratado o el código que la ley "
                        "aprueba")
    p.add_argument("--repo", help="ruta al repo, si no está configurada")
    a = p.parse_args(argv)

    normas = carpeta_normas(a.repo)
    if normas is None:
        print("No hay repo configurado: correr configurar.py --repo <ruta>, o pasar --repo.")
        return 2
    archivo = normas / f"{a.norma}.txt"
    if not archivo.is_file():
        print(f"No existe {archivo}. El slug es el del manifiesto normas.json; los bajados "
              f"están en {normas}.")
        return 2
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    if a.anexo:
        bloques = anexos(lineas)
        if not 0 < a.anexo < len(bloques):
            print(f"{archivo.name} no tiene anexo {a.anexo}: tiene {len(bloques) - 1} con "
                  f"numeración propia.")
            return 2
        articulos = bloques[a.anexo]
        donde = f"{a.norma}, anexo {a.anexo}"
    else:
        articulos = partir(lineas)
        donde = a.norma
        bloques = anexos(lineas)

    for l in encabezado(lineas):
        print(l)
    print()

    if a.listar:
        print(f"{len(articulos)} artículos reconocidos en {donde}:")
        print("  " + ", ".join(articulos))
        otros = len(anexos(lineas)) - 1
        if otros and not a.anexo:
            print(f"\nTiene {otros} anexo(s) con numeración propia: ver --anexo 1.")
        return 0
    if not a.articulo:
        print("Falta decir qué artículo: por ejemplo 245, o --listar para ver cuáles hay.")
        return 2

    faltan = []
    for pedido_ in a.articulo:
        try:
            k = pedido(pedido_)
        except ValueError as e:
            print(f"  {e}")
            faltan.append(pedido_)
            continue
        if k not in articulos:
            print(f"  No se encontró el art. {k} en {archivo.name}: puede estar numerado de "
                  f"otra forma, o el corte no lo reconoce. Ver --listar.")
            faltan.append(pedido_)
            continue
        print(f"--- art. {k} · {donde}")
        print("\n".join(articulos[k]))
        print()
        if not a.anexo and articulos[k] == bloques[0].get(k):
            con_el_mismo = [str(n) for n, b in enumerate(bloques[1:], 1) if k in b]
            if con_el_mismo:
                lista = " y ".join(con_el_mismo)
                print(f"  OJO: este es el art. {k} de la norma. También hay un art. {k} en "
                      f"{'el anexo' if len(con_el_mismo) == 1 else 'los anexos'} {lista}: si se "
                      f"busca el del texto aprobado —el código o el tratado—, repetir con "
                      f"--anexo {con_el_mismo[0]}.")
                print()
    if faltan:
        print(f"Sin encontrar: {', '.join(faltan)}. Lo que no salió de acá no se cita de memoria.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
