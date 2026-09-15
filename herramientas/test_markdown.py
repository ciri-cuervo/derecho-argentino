#!/usr/bin/env python3
"""Verificador de los .md del repositorio. Sin dependencias externas.

    python3 herramientas/test_markdown.py

Revisa lo que se rompe en silencio: un link que apunta a un archivo renombrado, un ancla que
dejo de existir, una tabla con una celda de más, un bloque de código sin cerrar. La
documentación de este repo es parte del producto -- la lee quien instala el plugin, en GitHub --
y esos cuatro defectos no se ven al escribir, solo al renderizar.

**No opina de estilo.** El ancho de línea, el orden de las secciones y el uso de énfasis son
decisiones de quien escribe. Un verificador que las discute termina apagado, y uno apagado es
peor que uno que no existe. Para dimensionarlo: con las reglas de ancho de un linter genérico
este repo devuelve más de veinte mil avisos, casi todos deliberados.

**Ámbito: todo el repositorio menos `argentina/kb/`.** Esa capa es material heredado de otro
autor, no sigue estas convenciones y no se toca sin decisión previa; su deuda está anotada en
`docs/DESARROLLO.md`. Todo lo demas -- README, docs/, la skill, los evals, las herramientas --
entra.
"""
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUERA = ("argentina/kb", "argentina/fuentes/_local")
ALERTAS = ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION")


def archivos():
    """Los .md del ámbito, en orden estable."""
    out = []
    for p in sorted(RAIZ.rglob("*.md")):
        rel = p.relative_to(RAIZ).as_posix()
        if ".git" in p.parts or rel.startswith(FUERA):
            continue
        out.append(p)
    return out


def prosa(p):
    """(numero, línea) de las líneas que NO están dentro de un bloque de código.

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
       ahí el guion inicial de un encabezado que arranca con emoji o con imagen.
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
        self.assertGreater(len(ARCHIVOS), 50, "el ámbito quedó vacío o casi")

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
# `../../issues` desde un archivo de la raíz es la forma que RECOMIENDA GitHub, porque sobrevive
# a un fork y a un rename del repositorio, cosa que una URL absoluta no hace. No son links
# rotos: son links que solo resuelven renderizados.
SECCIONES_DE_GITHUB = ("issues", "discussions", "pulls", "wiki", "releases", "security")


def es_seccion_de_github(destino: str) -> bool:
    partes = destino.split("/")
    return partes[:2] == ["..", ".."] and len(partes) > 2 and partes[2] in SECCIONES_DE_GITHUB


class TestLinks(unittest.TestCase):
    """Un link roto en el README es la primera impresión del repositorio."""

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
        """La excepción es una lista corta, no una puerta para cualquier `../../`."""
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
                        continue          # no es .md del ámbito: no hay que comprobar
                    with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                        self.assertIn("#" + frag.lower(), ANCLAS[destino],
                                      f"ancla {d}, que no es ningún encabezado")


class TestTablas(unittest.TestCase):
    """Una fila con una celda de más no avisa: GitHub la renderiza corrida y se lee mal."""

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
        """Dos espacios al final son un salto de línea forzado que nadie escribe a propósito:
        entran solos al editar y ensucian el diff de quien toque esa línea después."""
        for p in ARCHIVOS:
            for i, l in prosa(p):
                with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                    self.assertEqual(l, l.rstrip(), "la línea termina en espacios")

    def test_los_bloques_de_codigo_estan_cerrados(self):
        """Un fence sin cerrar se come el resto del documento al renderizar."""
        for p in ARCHIVOS:
            abiertos = sum(1 for l in p.read_text(encoding="utf-8").splitlines()
                           if l.lstrip().startswith("```"))
            with self.subTest(str(p.relative_to(RAIZ))):
                self.assertEqual(abiertos % 2, 0, "quedó un bloque de código sin cerrar")

    def test_las_alertas_son_de_los_tipos_que_github_renderiza(self):
        """`> [!AVISO]` no falla: se dibuja como una cita común y el énfasis se pierde."""
        for p in ARCHIVOS:
            for i, l in prosa(p):
                m = re.match(r">\s*\[!(\w+)\]", l)
                if not m:
                    continue
                with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                    self.assertIn(m.group(1), ALERTAS, "tipo de alerta que GitHub no conoce")


class TestImagenes(unittest.TestCase):
    """Toda imagen tiene que apuntar a un archivo que exista.

    El verificador miraba los links de Markdown y no los `src` de las etiquetas `<img>`, que es
    como el README arma la marca. Costo real: una corrección de acentos convirtio
    `chapa-versión.png` en `chapa-versión.png`, el badge de la versión dejo de renderizar y
    ningún control lo vio. Los nombres de archivo van en ASCII y esto lo fija.
    """

    FUENTE = re.compile(r'(?:src|srcset)="([^":]+?)"')

    def test_toda_imagen_existe(self):
        for p in ARCHIVOS:
            for i, l in prosa(p):
                for ruta in self.FUENTE.findall(l):
                    with self.subTest(f"{p.relative_to(RAIZ)}:{i} {ruta}"):
                        self.assertTrue((p.parent / ruta).is_file(),
                                        f"la imagen {ruta} no existe")

    def test_ninguna_url_lleva_no_ascii_en_su_ruta(self):
        """El path de una URL va en ASCII; lo que no lo sea, percent-encodeado.

        `references/fuentes.md` citaba cuatro veces `.../ley-14250-46379/actualización` mientras
        el manifiesto escribe `/actualización` en las setenta URLs que el descargador baja de
        verdad. Las dos formas resuelven en el servidor, así que no rompia nada visible: lo que
        rompia era el cotejo, porque quien compara la URL de un módulo contra `normas.json` no
        encuentra la misma cadena. El manifiesto ya hace lo correcto y percent-encodea
        --`resoluci%C3%B3n-298-2017`--, así que la regla es la suya.

        Se mira solo hasta el `?`: el valor de un parámetro puede llevar acentos sin problema,
        como el `n=Ver+Resolución+SC1840.pdf` que la SCBA usa de nombre de archivo sugerido.
        """
        URL = re.compile(r"https?://[^\s)`\"|<>]+")
        for p in ARCHIVOS:
            for i, l in prosa(p):
                for u in URL.findall(l):
                    ruta = u.split("?", 1)[0]
                    malo = next((c for c in ruta if ord(c) > 127), None)
                    with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                        self.assertIsNone(malo, f"«{malo}» en el path de {ruta[:60]}: va "
                                                f"percent-encodeado" if malo else "")

    def test_ningun_nombre_de_archivo_lleva_acentos(self):
        """MUTACION del caso vivido: un `.png` o un `.md` con tilde en el nombre no se
        encuentra, y el fallo es silencioso —la imagen no aparece, el link no anda—."""
        CITA = re.compile(r"[\w./-]*[\w-]\.(?:md|py|json|txt|csv|pdf|svg|png|yml)\b")
        for p in ARCHIVOS:
            for i, l in prosa(p):
                for nombre in CITA.findall(l):
                    with self.subTest(f"{p.relative_to(RAIZ)}:{i} {nombre}"):
                        self.assertIsNone(
                            re.search(r"[áéíóúüñÁÉÍÓÚÜÑ]", nombre),
                            f"«{nombre}» lleva acentos: ningún archivo del repo los tiene")


class TestMarcadoresEnteros(unittest.TestCase):
    """Un marcador canónico no puede quedar partido por un renglón que Markdown reinterpreta.

    El marcador es una cadena que el abogado copia al escrito, así que tiene que renderizar como
    una sola cosa. Si se envuelve en dos renglones y el segundo arranca con `- `, Markdown lo lee
    como viñeta y **parte el marcador en dos**: deja de ser copiable y el cierre `]` queda colgando
    en otro bloque.

    Salió de correr `markdownlint` a mano sobre el árbol. De sus 9.868 avisos éste fue el único
    defecto real, y es una regla que markdownlint no tiene: es un invariante de este repositorio,
    no una convención de Markdown. Por eso vive acá y no en una configuración de un linter.

    Dentro de un blockquote, `> ` al principio del renglón siguiente **es** la continuación
    correcta y no rompe nada: ese fue el primer falso positivo del detector.
    """

    ABRE = re.compile(r"\[[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ \-]{3,}:")
    # Lo que Markdown lee como el comienzo de otro bloque.
    REINTERPRETA = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|\||```)")

    # Capa 2 fuera de `kb/`: son de Cristian Aboitiz y no se corrigen, ni el contenido ni la
    # forma. `argentina/evals/administrativo-caba-recursos-agotamiento-via/resultado.md:19`
    # TIENE el defecto -- un [ALERTA PLAZO FATAL: ...] partido por un renglon que arranca con
    # `- ` -- y queda anotado aca en vez de arreglado. Ver LICENCIAS.md seccion 2.
    AJENOS = ("administrativo-caba-recursos-agotamiento-via",
              "consumidor-dano-punitivo-prescripcion",
              "consumidor-garantia-producto-defectuoso",
              "consumidor-prepaga-aumento-dnu70",
              "evals/README.md")

    def test_las_excepciones_de_capa_2_son_las_que_declara_licencias(self):
        """Si esta lista crece sin que crezca la de LICENCIAS.md, deja de ser una excepcion
        declarada y pasa a ser una puerta."""
        licencias = (RAIZ / "LICENCIAS.md").read_text(encoding="utf-8")
        for nombre in self.AJENOS:
            with self.subTest(nombre):
                self.assertIn(nombre.replace("evals/", ""), licencias,
                              "LICENCIAS.md no declara esta excepción de capa 2")

    def test_la_configuracion_de_markdownlint_deja_la_capa_2_afuera(self):
        """`markdownlint-cli2 --fix` REESCRIBE los archivos que mira. Es la única herramienta del
        repositorio que le puede escribir a otro autor sin que nadie lo pida, así que su `ignores`
        tiene que nombrar las cinco excepciones además de `kb/`. Se comprueba por texto: la
        configuración lleva comentarios y no es JSON parseable sin sacarlos."""
        config = (RAIZ / ".markdownlint-cli2.jsonc").read_text(encoding="utf-8")
        ignorados = config.split('"ignores"', 1)[1]
        for nombre in ("argentina/kb/**",) + self.AJENOS:
            with self.subTest(nombre):
                self.assertIn(nombre, ignorados,
                              "markdownlint podría reescribir un archivo de capa 2 con --fix")

    def test_ningun_marcador_queda_partido_por_un_renglon_que_markdown_reinterpreta(self):
        for p in ARCHIVOS:
            if any(x in p.as_posix() for x in self.AJENOS):
                continue
            lineas = p.read_text(encoding="utf-8").splitlines()
            abierto = False
            for numero, linea in enumerate(lineas, 1):
                if abierto and self.REINTERPRETA.match(linea):
                    with self.subTest(f"{p.relative_to(RAIZ)}:{numero}"):
                        self.fail(f"un marcador abierto sigue en «{linea.strip()[:52]}», que "
                                  f"Markdown lee como otro bloque: el marcador se parte en dos")
                m = list(self.ABRE.finditer(linea))
                if m:
                    abierto = "]" not in linea[m[-1].end():]
                elif abierto and "]" in linea:
                    abierto = False


class TestProsaAcentuada(unittest.TestCase):
    """La prosa de los `.md` va en castellano acentuado, y esto lo sostiene.

    Medido: fuera de `kb/`, más del 97% de estas palabras ya estaba acentuado, así que las que
    faltaban eran errores sueltos y no una convención. En los `.py` es al revés y tiene su
    propia regla, en docs/DESARROLLO.md: lo que se imprime a consola tiene que entrar en cp1252.

    LA LISTA SOLO LLEVA PALABRAS INEQUIVOCAS, y eso es la mitad del diseño. `practica`,
    `tramite`, `calculo`, `cómputo` y `numero` existen sin tilde: son formas verbales
    --"quien la practica", "el expediente tramite"-- y una corrección automática sobre ellas
    introduce errores en vez de sacarlos. Paso: un reemplazo en masa escribió "la actora
    práctica liquidación", que es el verbo. Si una palabra puede ser dos cosas, no entra acá.
    """

    # Sustantivos y adjetivos que en castellano no tienen forma valida sin tilde.
    PALABRAS = ("habiles", "habil", "articulo", "articulos", "dias", "codigo", "prescripcion",
                "indemnizacion", "verificacion", "seccion", "caratula", "aplicacion",
                "resolucion", "informacion", "liquidacion", "despues", "modulo", "razon",
                "proteccion", "notificacion", "ejecucion", "accion", "sancion", "peticion",
                "jurisdiccion", "obligacion", "relacion", "extincion", "asociacion", "ilicita",
                "participacion", "suspension", "conciliacion", "huerfano", "dano", "danos",
                "version", "organo", "reduccion", "exencion", "tambien", "ultimo", "minimo",
                "maximo", "interes", "fiscalia", "juridico", "medica", "policia", "ejercito",
                "parrafo", "compania", "sumarisimo", "casacion", "impugnacion", "restitucion",
                "infraccion", "declaracion", "adopcion", "educacion", "orientacion",
                "prevencion", "reinstalacion", "privacion", "ilegitima")

    # Texto de otro autor, conservado palabra por palabra: no se corrige su ortografia.
    AJENOS = ("LICENSE-ABOITIZ.md", "LICENSE-CC-BY-SA-4.0.md")

    PATRON = re.compile(r"(?<![\w-])(" + "|".join(PALABRAS) + r")(?![\w-])", re.I)

    # Un marcador es carga de un vocabulario controlado, no prosa, y su acentuación está sin
    # decidir: medido sobre la skill, 119 marcadores traen acentos en su contenido y 94 no. Esa
    # decisión merece tomarse aparte y no caer de rebote de este test, así que acá se excluyen.
    MARCADOR = re.compile(r"\[[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ \-]{3,}:[^\]]*\]")

    @staticmethod
    def _sin_codigo(linea):
        """Saca lo que no es prosa: bloques indentados, spans de código, URLs, `name:` y
        marcadores.

        Ahí lo no acentuado es correcto o es otra discusión: una ruta, un slug de eval y el
        identificador de un comando son ASCII por definición y acentuarlos los rompe, y un
        renglon con cuatro espacios de sangria es un bloque de código de Markdown --el diagrama
        de linaje de LICENCIAS.md, por ejemplo-- que `prosa()` no descarta porque solo mira los
        bloques cercados con acentos graves.
        """
        if re.match(r"^\s*name:\s", linea) or re.match(r"^\s{4,}\S", linea):
            return ""
        linea = TestProsaAcentuada.MARCADOR.sub(" ", linea)
        linea = re.sub(r"`[^`]*`", " ", linea)
        return re.sub(r"https?://\S+", " ", linea)

    def test_la_prosa_no_pierde_los_acentos(self):
        for p in ARCHIVOS:
            if p.name in self.AJENOS:
                continue
            for i, l in prosa(p):
                hallado = self.PATRON.search(self._sin_codigo(l))
                if not hallado:
                    continue
                with self.subTest(f"{p.relative_to(RAIZ)}:{i}"):
                    self.fail(f"«{hallado.group(0)}» va acentuada: "
                              f"{l.strip()[:70]}")

    def test_ninguna_palabra_de_la_lista_es_ambigua(self):
        """MUTACION del criterio: si entra una forma verbal, el control empieza a pedir errores.

        Las cinco de abajo son las que hay que rechazar, y están como fixture porque son la
        razón por la que la lista no se completa sola con un diccionario.
        """
        for verbal in ("practica", "tramite", "calculo", "computo", "numero", "critica",
                       "publico", "termino"):
            with self.subTest(verbal):
                self.assertNotIn(verbal, self.PALABRAS,
                                 f"«{verbal}» tambien es forma verbal y no puede entrar")


if __name__ == "__main__":
    unittest.main()
