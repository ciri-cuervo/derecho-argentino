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

**Ámbito: todo el repositorio menos `derecho/kb/`.** Esa capa es material heredado de otro
autor, no sigue estas convenciones y no se toca sin decisión previa; su deuda está anotada en
`docs/DESARROLLO.md`. Todo lo demás -- README, docs/, la skill, los evals, las herramientas --
entra.
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUERA = ("derecho/kb", "derecho/fuentes/_local")
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
    """(número, línea) de las líneas que NO están dentro de un bloque de código.

    Lo de adentro del bloque es texto literal -- comandos, JSON, salidas de consola -- y
    cualquier regla que se le aplique está discutiendo con el ejemplo, no con el documento.
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
        """Si un cambio de rutas deja la lista vacía, todo lo de abajo pasa sin mirar nada."""
        self.assertGreater(len(ARCHIVOS), 50, "el ámbito quedó vacío o casi")

    def test_kb_queda_afuera(self):
        for p in ARCHIVOS:
            self.assertNotIn("derecho/kb/", p.as_posix())


class TestInstalacionAMano(unittest.TestCase):
    """Las instrucciones de copiar la skill a mano nombran una carpeta que existe.

    Es el camino de Codex, donde no hay marketplace que resuelva nada: quien instala copia la
    línea y la pega. Una carpeta renombrada la deja apuntando al vacío, y el error aparece en la
    terminal de otro. Las dos líneas —`cp` y `Copy-Item`— se escriben por separado y con
    separadores distintos, así que se desincronizan sin que se note al leerlas.

    MUTACIÓN que lo comprueba: cambiar `derecho` por `argentina` en cualquiera de las dos líneas
    de `docs/TERMINAL.md` deja este test en rojo.
    """

    #: El operando de origen de una copia, contado desde el nombre con el que se clona el repo.
    COPIA = re.compile(r"^(?:cp -R|Copy-Item -Recurse) +derecho-argentino[/\\](\S+)", re.M)

    def test_toda_ruta_que_se_copia_existe_en_el_repo(self):
        vistas = 0
        for p in ARCHIVOS:
            for m in self.COPIA.finditer(p.read_text(encoding="utf-8")):
                vistas += 1
                relativa = m.group(1).replace("\\", "/")
                with self.subTest(f"{p.relative_to(RAIZ)}: {relativa}"):
                    self.assertTrue((RAIZ / relativa).exists(),
                                    f"{p.relative_to(RAIZ)} manda a copiar `{relativa}`, "
                                    f"que no existe en el repositorio")
        self.assertGreaterEqual(vistas, 2, "no se encontró ninguna instrucción de copia: "
                                           "las dos plataformas llevan una")


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
    como el README arma la marca. Costo real: una corrección de acentos convirtió
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
        verdad. Las dos formas resuelven en el servidor, así que no rompía nada visible: lo que
        rompía era el cotejo, porque quien compara la URL de un módulo contra `normas.json` no
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
        """MUTACIÓN del caso vivido: un `.png` o un `.md` con tilde en el nombre no se
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
    # forma. `derecho/evals/administrativo-caba-recursos-agotamiento-via/resultado.md:19`
    # TIENE el defecto -- un [ALERTA PLAZO FATAL: ...] partido por un renglón que arranca con
    # `- ` -- y queda anotado acá en vez de arreglado. Ver LICENCIAS.md sección 2.
    AJENOS = ("administrativo-caba-recursos-agotamiento-via",
              "consumidor-dano-punitivo-prescripcion",
              "consumidor-garantia-producto-defectuoso",
              "consumidor-prepaga-aumento-dnu70",
              "evals/README.md")

    def test_las_excepciones_de_capa_2_son_las_que_declara_licencias(self):
        """Si esta lista crece sin que crezca la de LICENCIAS.md, deja de ser una excepción
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
        for nombre in ("derecho/kb/**",) + self.AJENOS:
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


class TestPunterosDeSeccion(unittest.TestCase):
    """Un puntero en prosa a la sección de otro archivo tiene que resolver.

    `test_markdown.py` ya verifica los links de Markdown, pero la mitad de las remisiones de
    este repositorio no son links: son prosa, del tipo «ver tal archivo, tal sección». Eso no
    lo mira ningún verificador, y es justo la forma que MÁS se usa al sacar texto repetido:
    donde antes había una copia queda un puntero. Si el título de destino cambia, la copia ya
    no está y el puntero tampoco lleva a ninguna parte, así que el porqué desaparece de los
    dos lados sin que nada avise.

    Se exige que exista un ENCABEZADO que contenga ese título, no un encabezado igual: varios
    llevan numeración o un emoji adelante.
    """

    # El nombre de un .md --entre acentos graves o como destino de un link--, hasta 30
    # caracteres, y el título entre comillas angulares. Las DOS formas, porque el repositorio
    # usa las dos y un control que mira una sola deja pudrir la otra. El hueco de 30 cubre lo
    # que se escribe en el medio: ", sección", ", " y " -- ver".
    REF = re.compile(r"(?:`([A-Za-z0-9_./-]+\.md)`|\]\(([A-Za-z0-9_./-]+\.md)\))"
                     r"[^«\n]{0,30}«([^»\n]{6,90})»")

    @staticmethod
    def _resolver(origen, destino):
        """Los .md que ese puntero puede estar nombrando.

        Dos formas, y las dos se usan: una ruta relativa al archivo que remite -la de un link
        de Markdown, `../README.md`- y un nombre suelto o parcial -`intake.md`,
        `references/intake.md`-, que es como se escribe adentro de un docstring, donde no hay
        ruta relativa que valga.
        """
        relativo = (origen.parent / destino).resolve()
        if relativo.is_file():
            return [relativo]
        return [q for q in RAIZ.rglob("*.md")
                if q.as_posix().endswith(destino) and not q.as_posix().startswith("derecho/kb")]

    def _fuentes(self):
        """Los .md del ámbito y además los .py: un docstring también remite."""
        for p in ARCHIVOS:
            yield p
        for p in sorted(RAIZ.rglob("*.py")):
            if ".git" not in p.parts and "derecho/kb" not in p.as_posix():
                yield p

    def test_todo_puntero_a_una_seccion_encuentra_su_encabezado(self):
        rotos, mirados = [], 0
        for p in self._fuentes():
            for i, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                for m in self.REF.finditer(l):
                    destino, titulo = m.group(1) or m.group(2), m.group(3)
                    candidatos = self._resolver(p, destino)
                    mirados += 1
                    if not candidatos:
                        rotos.append(f"{p.relative_to(RAIZ)}:{i} apunta a {destino}, que no existe")
                        continue
                    if not any(re.search(r"^#{1,6}\s+.*" + re.escape(titulo),
                                         q.read_text(encoding="utf-8"), re.M)
                               for q in candidatos):
                        rotos.append(f"{p.relative_to(RAIZ)}:{i} apunta a «{titulo}» de "
                                     f"{destino}, y ahí no hay ningún encabezado con ese texto")
        self.assertGreater(mirados, 3, "no se miró ningún puntero: el control está apagado")
        self.assertEqual(rotos, [], "punteros de sección que no resuelven:\n  "
                         + "\n  ".join(rotos))


class TestProsaAcentuada(unittest.TestCase):
    """La prosa de los `.md` va en castellano acentuado, y esto lo sostiene.

    Medido: fuera de `kb/`, más del 97% de estas palabras ya estaba acentuado, así que las que
    faltaban eran errores sueltos y no una convención.

    En los `.py` la regla NO es «al revés», como decía acá antes: se parte en tres, y esta nota
    equivocada sirvió de excusa para dejar `Base de calculo dias/365` impreso en `intereses.py`.
    Lo que dice docs/DESARROLLO.md es que el fuente —comentarios y docstrings— va sin acentos
    por costumbre, que los identificadores van en ASCII porque se comparan, y que **la salida sí
    va acentuada**, porque se copia a un escrito. Eso último lo sostiene `TestSalidaAcentuada`
    en la suite de la skill; lo de cp1252 es otra regla distinta y la sostiene
    `TestSalidaCodificable`.

    LA LISTA SOLO LLEVA PALABRAS INEQUÍVOCAS, y eso es la mitad del diseño. `practica`,
    `tramite`, `calculo`, `computo` y `numero` existen sin tilde: son formas verbales
    --"quien la practica", "el expediente tramite"-- y una corrección automática sobre ellas
    introduce errores en vez de sacarlos. Pasó: un reemplazo en masa escribió "la actora
    práctica liquidación", que es el verbo. Si una palabra puede ser dos cosas, no entra acá.
    """

    # Sustantivos y adjetivos que en castellano no tienen forma válida sin tilde.
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

    # Texto de otro autor, conservado palabra por palabra: no se corrige su ortografía.
    AJENOS = ("LICENSE-ABOITIZ.md", "LICENSE-CC-BY-SA-4.0.md")

    PATRON = re.compile(r"(?<![\w-])(" + "|".join(PALABRAS) + r")(?![\w-])", re.I)

    # De un marcador se excluye SÓLO EL NOMBRE, y el contenido se mide como cualquier prosa.
    #
    # El nombre es vocabulario controlado y va exacto como figura en `marcadores.md`; el
    # contenido, después de los dos puntos, es prosa que se copia a un escrito judicial. Es la
    # prosa de más riesgo que hay en el repositorio, y estuvo excluida entera con el motivo de
    # que la acentuación de los marcadores "estaba sin decidir". Decidida: van acentuados, y
    # `verificar_respuesta.py` compara el nombre con `plano()` --minúsculas y sin tildes-- así
    # que acentuar no rompe el cotejo. Cuando se levantó la exclusión había 19 defectos adentro,
    # entre ellos `transito`, `publico`, `dieciseis`, `Boletin` y `Secretaria`.
    NOMBRE_DE_MARCADOR = re.compile(r"\[[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9/ \-]{3,}:")

    @staticmethod
    def _sin_codigo(linea):
        """Saca lo que no es prosa: bloques indentados, spans de código, URLs, `name:` y
        el NOMBRE de los marcadores --no su contenido, que sí es prosa y sí se mide--.

        Ahí lo no acentuado es correcto o es otra discusión: una ruta, un slug de eval y el
        identificador de un comando son ASCII por definición y acentuarlos los rompe, y un
        renglón con cuatro espacios de sangría es un bloque de código de Markdown --el diagrama
        de linaje de LICENCIAS.md, por ejemplo-- que `prosa()` no descarta porque solo mira los
        bloques cercados con acentos graves.

        `tags:` va con `name:` y por el mismo motivo: es la lista con la que se filtra una
        corrida de evals desde la línea de comandos, o sea un valor que el usuario tiene que
        poder tipear. Acentuarlo lo vuelve intipeable; dejarlo en ASCII no es un descuido de
        prosa. Es el único renglón del frontmatter con esa forma: `titulo`, `area` y `problema`
        son prosa y siguen medidos.
        """
        if re.match(r"^\s*(name|tags):\s", linea) or re.match(r"^\s{4,}\S", linea):
            return ""
        linea = TestProsaAcentuada.NOMBRE_DE_MARCADOR.sub(" ", linea)
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
        """MUTACIÓN del criterio: si entra una forma verbal, el control empieza a pedir errores.

        Las de abajo son las que hay que rechazar, y están como fixture porque son la
        razón por la que la lista no se completa sola con un diccionario.
        """
        for verbal in ("practica", "tramite", "calculo", "computo", "numero", "critica",
                       "publico", "termino"):
            with self.subTest(verbal):
                self.assertNotIn(verbal, self.PALABRAS,
                                 f"«{verbal}» también es forma verbal y no puede entrar")


class TestDondeVaCadaRegla(unittest.TestCase):
    """Los cuatro destinos de una regla, y que ninguno se desborde.

    El tope de `AGENTS.md` es el umbral de adherencia que da la documentación de Claude Code.
    Un archivo de reglas que nadie termina de leer es una regla que no se sigue, y eso no
    falla ruidosamente: falla el día que alguien hace lo que la regla prohibía.

    El tope de las reglas es más bajo que el de `AGENTS.md` a propósito. Una regla acotada
    por ruta que crece es una que absorbió algo que no le toca, y lo que absorbe deja de
    cargarse cuando hace falta.

    La invariante inversa -que lo que rige siempre no emigre hacia una regla de `paths:`
    angosto, que casi nunca carga- la miden dos pruebas de acá abajo, por REGIÓN: el preámbulo
    de `AGENTS.md` (desde el título hasta el primer `## `) más sus secciones `## `. El piso de
    palabras de `TestLosDosAgentesLeenLoMismo` no la atrapa, porque es sobre la SUMA de
    `AGENTS.md` y las reglas, y una mudanza no la baja. Las dos pruebas miden cosas distintas
    y ninguna cubre a la otra:

    - `test_agents_md_conserva_sus_secciones_siempre_activas` mide IDENTIDAD, contra
      `SECCIONES_SIEMPRE_ACTIVAS`. Un conteo de secciones no alcanza. MUTACIÓN que lo
      demuestra: se saca «La frontera de licencia» entera a `.claude/rules/`, y se repone el
      conteo partiendo «Disciplina de verificación» en dos con un `## ` nuevo.
    - `test_ninguna_region_de_agents_md_quedo_reducida_a_cascara` mide SUSTANCIA, con un piso
      de palabras por región. La identidad no alcanza: el encabezado puede quedar en pie con
      el cuerpo vaciado, y el preámbulo no tiene ningún `## ` del que colgar un nombre.
      MUTACIÓN: se deja el encabezado en pie y se reemplaza el cuerpo por un puntero de una
      oración.

    **Lo que ninguna de las dos atrapa:** que una región se lime de a poco, palabra por
    palabra, en sucesivas ediciones, sin cruzar nunca el umbral de una sola vez. No
    reemplazan la lectura de lo que cambia en cada edición.
    """

    REGLAS = RAIZ / ".claude" / "rules"
    # Las seis secciones de `AGENTS.md` rigen siempre, así que la válvula hacia
    # `.claude/rules/` está cerrada: cuando el archivo cruce el tope, la prosa se acorta o lo
    # que sea orientación se va a `docs/`. **El tope no se sube.** Subirlo es calibrar la
    # medida contra el caso que la hizo sonar, y una medida así deja de medir.
    TOPE_AGENTS = 200
    TOPE_REGLA = 120

    # Reglas de `.claude/rules/` que cargan siempre, por diseño: sin `paths:` en el
    # frontmatter, pero declaradas acá para que la falta de `paths:` no sea, por sí sola,
    # evidencia de un archivo mal puesto. Lo que las manda a `.claude/rules/` en vez de sumarse
    # a `AGENTS.md` es el tope POR ARCHIVO, no el contenido: 194 + 79 renglones en dos
    # archivos, contra un tope de 200 para un archivo único. MUTACIÓN: una regla sin `paths:`
    # que no está acá tiene que fallar.
    REGLAS_SIEMPRE_ACTIVAS = ("prosa.md", "derecho-argentino.md", "herramientas.md")

    # Las secciones de `AGENTS.md` que rigen SIEMPRE, por prefijo de encabezado y no por el
    # título entero: un retoque de redacción no tiene por qué romper el control. Una sección
    # nueva se agrega acá el día que se escribe; lo que no puede pasar es que una de éstas se
    # mude a un archivo que carga por `paths:`.
    SECCION_DE_LAS_REGLAS = "## Las reglas"

    SECCIONES_SIEMPRE_ACTIVAS = (
        "## Dos nombres",
        SECCION_DE_LAS_REGLAS,
        "## Un commit por versión",
        "## La frontera de licencia",
        "## Disciplina de verificación",
        "## Estado y pendientes",
    )

    # Una región «reducida a cáscara» es un puntero de una oración -«Ver
    # `.claude/rules/lo-que-sea.md`.»- o apenas el título sin desarrollo: entre cinco y quince
    # palabras. Treinta deja margen a una anotación de una o dos oraciones sin llegar a
    # contener una regla con su excepción y su consecuencia -el mínimo real de hoy, la sección
    # «Estado y pendientes», tiene 71, más del doble de este piso-. No se calibró para que
    # ninguna mutación en particular falle: se calibró contra lo que un puntero mide.
    PISO_POR_REGION = 30

    @classmethod
    def _reglas(cls):
        """Los `.md` de `.claude/rules/`, RECURSIVO como los descubre Claude Code.

        Con `glob` en vez de `rglob`, una regla en un subdirectorio queda fuera de todos los
        controles de esta clase -tope, `paths:` y estar nombrada- y ninguno protesta: el
        `mkdir` es la evasión entera. MUTACIÓN: `.claude/rules/anidada/x.md` sin `paths:`, que
        Claude Code carga en toda sesión igual que `AGENTS.md`.
        """
        return sorted(cls.REGLAS.rglob("*.md")) if cls.REGLAS.is_dir() else []

    @staticmethod
    def _paths_declarados(frontmatter):
        """Los patrones de `paths:` de un frontmatter, o `None` si la clave no está.

        Va por regex anclado al principio de renglón y no por `assertIn("paths:", ...)`, que
        es substring y da por declarada la regla que escribe `xpaths:` o que dejó el
        `# paths:` comentado. MUTACIÓN: las dos formas, más `paths: []`.
        """
        hallado = re.search(r"(?m)^paths:[ \t]*(.*)$", frontmatter)
        if hallado is None:
            return None
        en_linea = hallado.group(1).strip()
        if en_linea.startswith("["):
            return re.findall(r"[^\s,\[\]\"\']+", en_linea)
        if en_linea:
            return [en_linea.strip("\"\'")]
        patrones = []
        for linea in frontmatter[hallado.end():].split("\n"):
            if not linea.strip():
                continue
            item = re.match(r"[ \t]+-[ \t]*(.+?)[ \t]*$", linea)
            if item is None:
                break
            patrones.append(item.group(1).strip("\"\'"))
        return patrones

    @staticmethod
    def _seccion(texto, encabezado):
        """El cuerpo de una sección de un `.md`, hasta el encabezado de igual o menor nivel."""
        nivel = len(encabezado.split(" ")[0])
        resto = texto[texto.index(encabezado) + len(encabezado):]
        corte = re.search(r"(?m)^#{1,%d} " % nivel, resto)
        return resto[:corte.start()] if corte else resto

    def test_agents_md_no_pasa_el_umbral_de_adherencia(self):
        n = len((RAIZ / "AGENTS.md").read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(n, self.TOPE_AGENTS,
                             f"AGENTS.md tiene {n} renglones. Lo que rige al tocar cierto "
                             f"árbol va a `.claude/rules/` con `paths:`; lo que es "
                             f"orientación, a `docs/`. La tabla está en DESARROLLO.md")

    def test_cada_regla_declara_paths_o_figura_siempre_activa(self):
        """Una regla sin `paths:` no es, por sí sola, evidencia de que está mal puesta.

        Carga siempre igual que `AGENTS.md`, y eso es legítimo cuando está en
        `REGLAS_SIEMPRE_ACTIVAS`: el motivo de mandarla a `.claude/rules/` en vez de sumarla a
        `AGENTS.md` es el tope POR ARCHIVO, no el contenido. Lo que no puede pasar es que falte
        en las dos partes -ni `paths:` ni la declaración-, porque ahí nadie decidió que cargue
        siempre. MUTACIÓN: una regla sin `paths:` y sin declarar tiene que fallar; una sin
        `paths:` mismo pero declarada, y una con `paths:`, tienen que pasar.
        """
        reglas = self._reglas()
        self.assertGreater(len(reglas), 0, "no hay ninguna regla: el control quedó vacío")
        for p in reglas:
            texto = p.read_text(encoding="utf-8")
            rel = p.relative_to(RAIZ).as_posix()
            with self.subTest(rel):
                # Una regla declarada siempre-activa puede no llevar frontmatter: sin
                # `paths:` no hay nada que declarar, y por eso `prosa.md` no abre con `---`.
                frontmatter = texto.split("---", 2)[1] if texto.startswith("---\n") else ""
                patrones = self._paths_declarados(frontmatter)
                if patrones is None:
                    self.assertIn(p.name, self.REGLAS_SIEMPRE_ACTIVAS,
                                 f"{rel} no declara `paths:` ni figura en "
                                 f"REGLAS_SIEMPRE_ACTIVAS: carga siempre sin que nadie lo "
                                 f"haya decidido")
                else:
                    self.assertGreater(len(patrones), 0,
                                       f"{rel} declara `paths:` vacío: no alcanza ningún "
                                       f"archivo y la regla queda muerta sin que nada avise")
                n = len(texto.splitlines())
                self.assertLessEqual(n, self.TOPE_REGLA,
                                     f"{rel} tiene {n} renglones: absorbió algo que no "
                                     f"le toca")

    def test_cada_regla_esta_nombrada_en_la_tabla_de_destinos(self):
        """Una regla que la tabla no nombra es una que nadie va a encontrar.

        Se recorta la sección antes de buscar. Sobre el archivo entero el control se apaga
        solo: `README.md`, `SKILL.md`, `marcadores.md` y una docena más de nombres aparecen
        en otros párrafos de DESARROLLO.md, así que una regla con cualquiera de esos nombres
        pasa sin estar en la tabla. MUTACIÓN: `.claude/rules/marcadores.md`.
        """
        texto = (RAIZ / "docs" / "DESARROLLO.md").read_text(encoding="utf-8")
        encabezado = "### Los cuatro destinos de una regla"
        self.assertIn(encabezado, texto,
                      f"docs/DESARROLLO.md ya no tiene «{encabezado}»: el control quedó sin "
                      f"dónde buscar, y sobre el archivo entero no mide nada")
        tabla = self._seccion(texto, encabezado)
        for p in self._reglas():
            rel = p.relative_to(RAIZ).as_posix()
            with self.subTest(rel):
                self.assertIn(p.name, tabla,
                              f"{rel} no figura en «Los cuatro destinos de una regla» de "
                              f"docs/DESARROLLO.md")

    def test_agents_md_nombra_cada_regla_por_su_ruta(self):
        """Codex no carga `.claude/rules/`, así que `AGENTS.md` tiene que anunciarlas.

        Una regla que `AGENTS.md` no anuncia es disciplina que ese agente pierde sin
        enterarse, y el silencio es la falla: nada en el repositorio se rompe. Se exige la
        ruta entera y no el basename, y se busca en la SECCIÓN del anuncio y no en el archivo
        entero: sobre el archivo entero, una ruta mencionada al pasar en otro párrafo -el
        preámbulo cita `.claude/rules/prosa.md`- alcanza para dar el anuncio por hecho.
        MUTACIÓN: se borra la fila de `prosa.md` de la tabla dejando la sección en pie.
        """
        agents = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
        encabezado = next((l for l in agents.split("\n")
                           if l.startswith(self.SECCION_DE_LAS_REGLAS)), None)
        self.assertIsNotNone(encabezado,
                             f"AGENTS.md ya no tiene «{self.SECCION_DE_LAS_REGLAS}…»: el "
                             f"control quedó sin dónde buscar")
        anuncio = self._seccion(agents, encabezado)
        reglas = self._reglas()
        self.assertGreater(len(reglas), 0, "no hay ninguna regla: el control quedó vacío")
        for p in reglas:
            ruta = p.relative_to(RAIZ).as_posix()
            with self.subTest(ruta):
                self.assertIn(ruta, anuncio,
                              f"AGENTS.md no nombra `{ruta}`, que es de Claude Code: quien "
                              f"trabaja en Codex se queda sin esa regla y sin saber que "
                              f"existe. Va en «Las reglas por ruta», con qué cubre")

    @staticmethod
    def _regiones_de_agents_md():
        """El preámbulo más cada sección `## ` de `AGENTS.md`, como (nombre, texto)."""
        lineas = (RAIZ / "AGENTS.md").read_text(encoding="utf-8").split("\n")
        idx_h1 = next(i for i, l in enumerate(lineas) if l.startswith("# "))
        idx_secciones = [i for i, l in enumerate(lineas) if l.startswith("## ")]
        limites = idx_secciones + [len(lineas)]
        regiones = [("preámbulo", lineas[idx_h1 + 1:idx_secciones[0]])]
        for k, ini in enumerate(idx_secciones):
            nombre = lineas[ini][3:].strip()
            regiones.append((nombre, lineas[ini:limites[k + 1]]))
        return [(nombre, "\n".join(cuerpo)) for nombre, cuerpo in regiones]

    def test_agents_md_conserva_sus_secciones_siempre_activas(self):
        """Cada sección que rige siempre sigue estando, y se comprueba CUÁL.

        Un conteo se repone partiendo otra sección en dos, y la mudada no deja rastro.
        """
        encabezados = ["## " + nombre for nombre, _ in self._regiones_de_agents_md()[1:]]
        for prefijo in self.SECCIONES_SIEMPRE_ACTIVAS:
            with self.subTest(prefijo):
                self.assertTrue(any(h.startswith(prefijo) for h in encabezados),
                                f"AGENTS.md ya no tiene «{prefijo}…»: lo que rige siempre se "
                                f"mudó a un archivo que no carga siempre. Las secciones de "
                                f"hoy son {encabezados}")

    def test_ninguna_region_de_agents_md_quedo_reducida_a_cascara(self):
        for nombre, cuerpo in self._regiones_de_agents_md():
            n = len(cuerpo.split())
            with self.subTest(nombre[:50]):
                self.assertGreaterEqual(n, self.PISO_POR_REGION,
                                        f"«{nombre[:50]}» de AGENTS.md tiene {n} palabras: "
                                        f"parece un puntero a otro archivo, no la regla "
                                        f"misma. Lo que rige siempre tiene que seguir "
                                        f"estando en el archivo que carga siempre")


class TestContenciosoAdministrativoSinGuion(unittest.TestCase):
    """Nuestra prosa lo escribe sin guion; una cita conserva el que traiga la fuente.

    El articulado no dirime: medido sobre `derecho/fuentes/normas/`, 124 apariciones sin guion y
    44 con —las constituciones de Catamarca, Misiones y Santa Cruz lo llevan—. Acotado a lo que
    este repositorio cubre, PBA y lo nacional, son 101 contra 15. El criterio y su medición están
    en `docs/DESARROLLO.md`.

    **No alcanza `fuentes/` ni `kb/`**: el primero es texto fijado por hash y el segundo es capa 2,
    y en los dos la ortografía ajena no se toca. Y exime la línea citada —entre comillas o con
    `>`— porque ahí el guion es el de la fuente y corregirlo sería falsear la cita.

    Mutación que lo comprueba: escribir `contencioso-administrativo` en un renglón de prosa de
    cualquier `.md` alcanzado lo deja en rojo; ponerlo entre comillas en ese mismo renglón, no.
    """

    CON_GUION = re.compile(r"[Cc]ontencioso-[Aa]dministrativ")
    # Una cita: la línea arranca con `>`, o el término aparece entre comillas en esa línea.
    CITA = re.compile(r'^\s*>|["«»""].*[Cc]ontencioso-[Aa]dministrativ|'
                      r'[Cc]ontencioso-[Aa]dministrativ\w*.*["«»""]')

    def test_la_prosa_propia_no_usa_el_guion(self):
        raiz = Path(__file__).resolve().parent.parent
        rotas, revisados = [], 0
        for f in sorted(raiz.rglob("*.md")):
            rel = f.relative_to(raiz).as_posix()
            if rel.startswith(("derecho/kb/", "derecho/fuentes/")) or "/.git/" in rel:
                continue
            revisados += 1
            for n, linea in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if self.CON_GUION.search(linea) and not self.CITA.search(linea):
                    rotas.append(f"{rel}:{n}")
        self.assertGreater(revisados, 40, "casi no se revisó nada: el control está apagado")
        self.assertEqual(rotas, [], "«contencioso-administrativo» con guion fuera de una cita: "
                                    + ", ".join(rotas[:8]) + " - ver docs/DESARROLLO.md")


class TestNingunModuloSePasaDelCorteDeRead(unittest.TestCase):
    """Un módulo más largo que el corte de `Read` se lee a medias y nadie se entera.

    `Read` trae **2000 renglones por defecto**. Un módulo más largo llega truncado, y el
    truncamiento **no avisa**: el agente cree que lo leyó entero. Si lo que queda del otro lado
    del corte es un agravante derogado o un plazo, se pierde en silencio, que es el modo de falla
    que este repositorio persigue.

    **Medido, no supuesto.** `laboral.md` llegó a 2118 renglones y la traza de una corrida real
    del 17/09/2026 lo muestra tal cual: `Read laboral.md` · `Read parte.md` · `Read laboral.md`
    otra vez · y después **dos `Grep` sobre el mismo archivo** para recuperar lo que faltaba.
    Cuatro accesos al mismo módulo, y un run de esa corrida murió en el límite de 30 turnos.

    **El umbral es 1900 y no 2000 a propósito.** Un control que salta recién al truncarse avisa
    tarde: cuando salta, el daño ya está. A 1900 quedan cien renglones de aviso, que es una
    sección. Y se mide el ARCHIVO, no la sección, porque el corte de `Read` es por archivo.

    Lo que este control **no** hace es decidir dónde cortar. Eso se lee: `laboral.md` se partió
    por materia —el derecho colectivo a `laboral-colectivo.md`— y no por número, porque 5.17 bis,
    ter y quater están numeradas ahí por vecindad y no son derecho colectivo.
    """

    CORTE_DE_READ = 2000
    TOPE = 1900
    AVISO = 1700

    def setUp(self):
        self.modulos = sorted(
            (RAIZ / "derecho" / "skills" / "derecho-argentino" / "references").glob("*.md"))

    def _renglones(self, md):
        return len(md.read_text(encoding="utf-8").split("\n"))

    def test_ninguno_pasa_el_tope(self):
        pasados = [(self._renglones(m), m.name) for m in self.modulos
                   if self._renglones(m) > self.TOPE]
        cerca = sorted(((self._renglones(m), m.name) for m in self.modulos
                        if self.AVISO < self._renglones(m) <= self.TOPE), reverse=True)
        detalle = "".join(f"\n    {n} renglones · {nombre}" for n, nombre in sorted(pasados, reverse=True))
        vecinos = "".join(f"\n    {n} · {nombre}" for n, nombre in cerca)
        self.assertEqual(pasados, [],
                         f"hay módulos arriba de {self.TOPE} renglones, y a {self.CORTE_DE_READ} "
                         f"`Read` los trunca sin avisar:{detalle}\n  "
                         f"Se parten por MATERIA, no por número de sección."
                         f"\n  Los que vienen atrás:{vecinos}")

    def test_el_codigo_tampoco_pasa_el_tope(self):
        """**El corte de `Read` es por archivo, no por extensión**, y este control miraba sólo los
        `.md`. Mientras tanto `test_scripts.py` —el archivo que sostiene buena parte de estas
        reglas— llegó a **6149 renglones, tres veces el tope**, y nadie lo veía.

        Un `.py` truncado se lee peor que un `.md`: el agente cree que vio el archivo entero y
        concluye que un test no existe. Se partió en seis por lo que cada suite afirma, y lo
        compartido quedó en `_comun_tests.py`.

        **El tope es el mismo y el motivo también.** No se exceptúa ningún archivo: si uno crece,
        se parte, que es lo que se le pide a un módulo.

        MUTACIÓN que lo comprueba: concatenar dos de las suites de `scripts/` lo deja en rojo.
        """
        codigo = sorted(p for p in RAIZ.rglob("*.py")
                        if ".git" not in p.parts and "_local" not in p.parts)
        self.assertGreater(len(codigo), 20, "no encontró los .py: el control está apagado")
        pasados = sorted(((self._renglones(p), str(p.relative_to(RAIZ)))
                          for p in codigo if self._renglones(p) > self.TOPE), reverse=True)
        detalle = "".join(f"\n    {n} renglones · {nombre}" for n, nombre in pasados)
        self.assertEqual(pasados, [],
                         f"hay archivos de código arriba de {self.TOPE} renglones, y a "
                         f"{self.CORTE_DE_READ} `Read` los trunca sin avisar:{detalle}\n  "
                         f"Se parten por lo que afirman, no por número de renglón.")

    def test_el_control_mira_todos_los_modulos(self):
        """Instrumento encendido: sin esto, «ninguno se pasa» también sería «no miró ninguno»."""
        self.assertGreater(len(self.modulos), 40, "no encontró los módulos de referencia")
        self.assertGreater(max(self._renglones(m) for m in self.modulos), 1000,
                           "ningún módulo grande: el control estaría midiendo otra cosa")


if __name__ == "__main__":
    unittest.main()
