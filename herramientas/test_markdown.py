#!/usr/bin/env python3
"""Verificador de los .md del repositorio. Sin dependencias externas.

    python3 herramientas/test_markdown.py

Revisa lo que se rompe en silencio: un link que apunta a un archivo renombrado, un ancla que
dejo de existir, una tabla con una celda de mas, un bloque de codigo sin cerrar. La
documentacion de este repo es parte del producto -- la lee quien instala el plugin, en GitHub --
y esos cuatro defectos no se ven al escribir, solo al renderizar.

**No opina de estilo.** El ancho de linea, el orden de las secciones y el uso de enfasis son
decisiones de quien escribe. Un verificador que las discute termina apagado, y uno apagado es
peor que uno que no existe. Para dimensionarlo: con las reglas de ancho de un linter generico
este repo devuelve mas de veinte mil avisos, casi todos deliberados.

**Ambito: todo el repositorio menos `argentina/kb/`.** Esa capa es material heredado de otro
autor, no sigue estas convenciones y no se toca sin decision previa; su deuda esta anotada en
`docs/DESARROLLO.md`. Todo lo demas -- README, docs/, la skill, los evals, las herramientas --
entra.
"""
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUERA = ("argentina/kb", "argentina/fuentes/_local", "node_modules")
ALERTAS = ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION")


def archivos():
    """Los .md del ambito, en orden estable."""
    out = []
    for p in sorted(RAIZ.rglob("*.md")):
        rel = p.relative_to(RAIZ).as_posix()
        if ".git" in p.parts or rel.startswith(FUERA):
            continue
        out.append(p)
    return out


def prosa(p):
    """(numero, linea) de las lineas que NO estan dentro de un bloque de codigo.

    Lo de adentro del bloque es texto literal -- comandos, JSON, salidas de consola -- y
    cualquier regla que se le aplique esta discutiendo con el ejemplo, no con el documento.
    """
    dentro = False
    for i, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if l.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            yield i, l


TAG_HTML = re.compile(r"<[^>]+>")


def ancla(titulo):
    """El slug con el que GitHub ancla un encabezado.

    Los tres detalles se midieron contra encabezados renderizados por GitHub, no se dedujeron:

        Derecho argentino · skill para agentes de IA   ->  #derecho-argentino--skill-para-agentes-de-ia
        <img ...> En la app de Claude                  ->  #-en-la-app-de-claude
        🎊 2026 edition is here!                       ->  #-2026-edition-is-here

    1. Los elementos HTML **no aportan texto**: se sacan antes de armar el slug. Si no, el
       `<img>` de un encabezado deja adentro sus atributos.
    2. Lo que se quita -emoji, `·`, `/`, `!`- **deja su espacio**, y el slug NO se recorta: de
       ahi el guion inicial de un encabezado que arranca con emoji o con imagen.
    3. Cada espacio es UN guion: dos espacios seguidos dan `--`. No se colapsan.
    """
    # El recorte va ANTES de sacar los tags: GitHub recorta el encabezado crudo, y el espacio
    # que queda al eliminar un `<img>` inicial es el que se convierte en el guion de adelante.
    t = titulo.replace("`", "").strip().lower()
    t = TAG_HTML.sub("", t)
    t = re.sub(r"[^\w\s-]", "", t)
    return "#" + re.sub(r"\s", "-", t)


def anclas_de(p):
    return {ancla(m.group(1)) for _, l in prosa(p)
            for m in [re.match(r"#{1,6}\s+(.*)", l)] if m}


ARCHIVOS = archivos()
ANCLAS = {p: anclas_de(p) for p in ARCHIVOS}


class TestAmbito(unittest.TestCase):
    def test_hay_archivos_que_revisar(self):
        """Si un cambio de rutas deja la lista vacia, todo lo de abajo pasa sin mirar nada."""
        self.assertGreater(len(ARCHIVOS), 50, "el ambito quedo vacio o casi")

    def test_kb_queda_afuera(self):
        for p in ARCHIVOS:
            self.assertNotIn("argentina/kb/", p.as_posix())


class TestAncla(unittest.TestCase):
    """`ancla()` tiene que reproducir a GitHub, y GitHub tiene tres rarezas.

    Los valores de abajo **se midieron** contra encabezados ya renderizados —los del README de
    este repo y uno ajeno con emoji—, no se dedujeron leyendo la documentación. Sin este test,
    `ancla()` opina y el verificador de anclas valida contra su propia opinión: aprobaría un
    link roto y rechazaría uno bueno.
    """

    MEDIDOS = {
        # de github.com/ciri-cuervo/derecho-argentino
        "Instalar": "#instalar",
        "Derecho argentino · skill para agentes de IA":
            "#derecho-argentino--skill-para-agentes-de-ia",
        '<img src="assets/logos/claude.svg" height="20" alt=""> En la app de Claude':
            "#-en-la-app-de-claude",
        # de github.com/goldbergyoni/nodebestpractices
        "🎊 2026 edition is here!": "#-2026-edition-is-here",
    }

    def test_reproduce_las_anclas_medidas_en_github(self):
        for titulo, esperado in self.MEDIDOS.items():
            with self.subTest(titulo[:40]):
                self.assertEqual(ancla(titulo), esperado)

    def test_lo_que_se_quita_deja_su_guion(self):
        """Emoji o imagen al principio ⇒ guion inicial. Es lo que más se cita mal."""
        self.assertEqual(ancla("📦 Instalar"), "#-instalar")
        self.assertEqual(ancla("Instalar"), "#instalar")

    def test_dos_espacios_dan_dos_guiones(self):
        """GitHub no colapsa los espacios: `a · b` deja `a--b`."""
        self.assertEqual(ancla("uno · dos"), "#uno--dos")


# Secciones del repositorio que GitHub resuelve por ruta relativa y no existen en el disco.
# `../../issues` desde un archivo de la raiz es la forma que RECOMIENDA GitHub, porque sobrevive
# a un fork y a un rename del repositorio, cosa que una URL absoluta no hace. No son links
# rotos: son links que solo resuelven renderizados.
SECCIONES_DE_GITHUB = ("issues", "discussions", "pulls", "wiki", "releases", "security")


def es_seccion_de_github(destino: str) -> bool:
    partes = destino.split("/")
    return partes[:2] == ["..", ".."] and len(partes) > 2 and partes[2] in SECCIONES_DE_GITHUB


class TestLinks(unittest.TestCase):
    """Un link roto en el README es la primera impresion del repositorio."""

    @staticmethod
    def _destinos(l):
        sin_codigo = re.sub(r"`[^`]*`", "", l)
        for m in re.finditer(r"\]\(([^)\s]+)\)", sin_codigo):
            yield m.group(1)

    def test_los_links_relativos_apuntan_a_algo_que_existe(self):
        for p in ARCHIVOS:
            for i, l in prosa(p):
                for d in self._destinos(l):
                    if d.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    if es_seccion_de_github(d):
                        continue
                    ruta = d.partition("#")[0]
                    if not ruta:
                        continue
                    with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                        self.assertTrue((p.parent / ruta).exists(),
                                        f"link a {d}, que no existe")

    def test_solo_las_secciones_conocidas_de_github_se_saltean(self):
        """La excepcion es una lista corta, no una puerta para cualquier `../../`."""
        self.assertTrue(es_seccion_de_github("../../issues"))
        self.assertTrue(es_seccion_de_github("../../security/advisories/new"))
        self.assertFalse(es_seccion_de_github("../../docs/ARQUITECTURA.md"))
        self.assertFalse(es_seccion_de_github("../issues"))
        self.assertFalse(es_seccion_de_github("../../"))

    def test_las_anclas_apuntan_a_un_encabezado_real(self):
        for p in ARCHIVOS:
            for i, l in prosa(p):
                for d in self._destinos(l):
                    if d.startswith(("http://", "https://", "mailto:")):
                        continue
                    ruta, _, frag = d.partition("#")
                    if not frag:
                        continue
                    destino = p if not ruta else (p.parent / ruta).resolve()
                    if destino not in ANCLAS:
                        continue          # no es .md del ambito: no hay que comprobar
                    with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                        self.assertIn("#" + frag.lower(), ANCLAS[destino],
                                      f"ancla {d}, que no es ningun encabezado")


class TestTablas(unittest.TestCase):
    """Una fila con una celda de mas no avisa: GitHub la renderiza corrida y se lee mal."""

    def test_todas_las_filas_tienen_las_mismas_celdas(self):
        for p in ARCHIVOS:
            bloque = []
            for i, l in list(prosa(p)) + [(0, "")]:
                if l.strip().startswith("|"):
                    bloque.append((i, l.count("|")))
                    continue
                if len(bloque) > 1:
                    anchos = {n for _, n in bloque}
                    with self.subTest(f"{p.relative_to(RAIZ)}:{bloque[0][0]}"):
                        self.assertEqual(len(anchos), 1,
                                         f"filas con distinta cantidad de celdas: {sorted(anchos)}")
                bloque = []


class TestHigiene(unittest.TestCase):
    def test_no_quedan_espacios_al_final_de_linea(self):
        """Dos espacios al final son un salto de linea forzado que nadie escribe a proposito:
        entran solos al editar y ensucian el diff de quien toque esa linea despues."""
        for p in ARCHIVOS:
            for i, l in prosa(p):
                with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                    self.assertEqual(l, l.rstrip(), "la linea termina en espacios")

    def test_los_bloques_de_codigo_estan_cerrados(self):
        """Un fence sin cerrar se come el resto del documento al renderizar."""
        for p in ARCHIVOS:
            abiertos = sum(1 for l in p.read_text(encoding="utf-8").splitlines()
                           if l.lstrip().startswith("```"))
            with self.subTest(str(p.relative_to(RAIZ))):
                self.assertEqual(abiertos % 2, 0, "quedo un bloque de codigo sin cerrar")

    def test_las_alertas_son_de_los_tipos_que_github_renderiza(self):
        """`> [!AVISO]` no falla: se dibuja como una cita comun y el enfasis se pierde."""
        for p in ARCHIVOS:
            for i, l in prosa(p):
                m = re.match(r">\s*\[!(\w+)\]", l)
                if not m:
                    continue
                with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                    self.assertIn(m.group(1), ALERTAS, "tipo de alerta que GitHub no conoce")


if __name__ == "__main__":
    unittest.main()
