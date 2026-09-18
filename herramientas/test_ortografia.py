#!/usr/bin/env python3
"""Tests de `ortografia.py`. Sin LanguageTool: no baja nada y no necesita Java.

    python3 herramientas/test_ortografia.py

La herramienta se corre a mano y está fuera del checklist; lo que decide QUÉ se mide corre
siempre, y es esto. Un extractor que se deja afuera medio archivo no da error: da menos
hallazgos, y menos hallazgos se lee como que el repositorio está mejor.
"""
import importlib.util
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "ortografia.py"


def cargar():
    spec = importlib.util.spec_from_file_location("ortografia", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class Aviso:
    """Lo mínimo de un `Match` de LanguageTool: la regla y las sugerencias."""

    def __init__(self, rule_id, replacements):
        self.rule_id = rule_id
        self.replacements = replacements


class TestQueSeMide(unittest.TestCase):
    def setUp(self):
        self.o = cargar()

    def test_la_fila_de_tabla_se_mide_y_no_se_descarta(self):
        """Era el 85% de `changelog-normativo.md`, descartado por venir entre pipes."""
        piezas = dict(self.o.prosa_de_md(
            "# Titulo\n\n| Bloque | Cómo revalidar |\n| --- | --- |\n"
            "| **Previsional** | el texto traia otra cosa |\n"))
        self.assertIn("el texto traia otra cosa", piezas.get(5, ""))
        self.assertNotIn("|", piezas.get(5, ""))

    def test_la_fila_delimitadora_no_es_texto(self):
        piezas = dict(self.o.prosa_de_md("| a | b |\n| --- | --- |\n| c | d |\n"))
        self.assertNotIn(2, piezas)

    def test_cada_pieza_lleva_la_linea_donde_arranca(self):
        """Todos los hallazgos de los `.md` salían en la línea 1, que es no tener línea."""
        texto = "# Uno\n\nparrafo uno\n\n```\ncodigo\nmas codigo\n```\n\nparrafo dos\n"
        lineas = [n for n, _ in self.o.prosa_de_md(texto)]
        self.assertEqual(lineas, [1, 3, 10])

    def test_el_bloque_cercado_se_vacia_sin_correr_las_lineas(self):
        """Borrarlo en vez de vaciarlo corre todo lo que sigue y la línea vuelve a mentir."""
        piezas = dict(self.o.prosa_de_md("```\nuno\ndos\n```\n\ndespues\n"))
        self.assertEqual(list(piezas), [6])

    def test_en_el_frontmatter_se_mide_el_valor_y_no_la_clave(self):
        """`titulo:` y `area:` son contrato; su valor es prosa. Eran 73 avisos falsos."""
        piezas = dict(self.o.prosa_de_md(
            "---\ntitulo: Restitución del nino\narea: familia\nname: un-slug\n---\n\ncuerpo\n"))
        self.assertIn("Restitución del nino", piezas.get(2, ""))
        self.assertNotIn("titulo", piezas.get(2, ""))
        self.assertNotIn(4, piezas, "`name:` es un valor que el usuario tipea")

    def test_el_bloque_con_sangria_es_codigo(self):
        piezas = dict(self.o.prosa_de_md("texto\n\n    comando --con opcion\n\notro\n"))
        self.assertEqual(sorted(piezas), [1, 5])


class TestLimpiar(unittest.TestCase):
    def setUp(self):
        self.o = cargar()

    def test_saca_el_slug_que_es_identificador(self):
        self.assertEqual(self.o.limpiar("el eval civil-danos-transito-pba anda").split(),
                         ["el", "eval", "anda"])

    def test_no_se_lleva_una_palabra_con_un_solo_guion(self):
        """Dos tramos pueden ser prosa --«teórico-práctico»--; tres ya son un slug."""
        self.assertIn("teorico-practico", self.o.limpiar("un examen teorico-practico"))

    def test_junta_los_espacios_que_deja_el_recorte(self):
        """Cada hueco delante de un signo disparaba `INCORRECT_SPACES`: 725 avisos propios."""
        self.assertEqual(self.o.limpiar("la copia de `x` tiene precedencia"),
                         "la copia de tiene precedencia")


class TestDosMitadesDeMorfologik(unittest.TestCase):
    """Separar la falta de acento del vocabulario que el diccionario no tiene."""

    def setUp(self):
        self.o = cargar()

    def test_una_falta_de_acento_es_candidato(self):
        aviso = Aviso("MORFOLOGIK_RULE_ES", ["unión", "unió", "anión"])
        self.assertFalse(self.o.palabra_desconocida(aviso, "union"))

    def test_una_sigla_es_vocabulario(self):
        aviso = Aviso("MORFOLOGIK_RULE_ES", ["IBA", "PBI", "PÚA"])
        self.assertTrue(self.o.palabra_desconocida(aviso, "PBA"))

    def test_lo_que_no_es_morfologik_siempre_es_candidato(self):
        self.assertFalse(self.o.palabra_desconocida(Aviso("ESTA_TILDE", ["está"]), "esta"))

    def test_una_letra_suelta_no_tiene_ortografia(self):
        """Vienen de `inc. b` y de `n° 1`."""
        self.assertTrue(self.o.es_propio("b"))
        self.assertTrue(self.o.es_propio("(n)"))
        self.assertFalse(self.o.es_propio("union"))


class TestVocabularioDeVeredictos(unittest.TestCase):
    """Un valor de veredicto es una clave, va en ASCII, y no puede salir como falta.

    Encabeza cada motivo --«locucion — la cifra es parte de una expresión»--, así que el
    diccionario lo lee como prosa mal escrita y lo reclama una vez por motivo. Acentuarlo
    para callarlo rompería el archivo. Se leen del `_vocabulario` de cada archivo de
    veredicto y no de una lista copiada acá: una copia se separa del original y entonces o
    se reclama un valor legítimo o se deja de reclamar una falta.
    """

    def setUp(self):
        self.o = cargar()

    def test_los_valores_declarados_no_se_reclaman(self):
        valores = self.o.vocabulario_de_veredictos()
        self.assertGreater(len(valores), 10, "no se leyó ningún `_vocabulario`")
        for v in ("locucion", "congelada", "de-terceros", "no-hace-falta"):
            with self.subTest(v):
                self.assertIn(v, valores)
                self.assertTrue(self.o.es_propio(v))

    def test_una_falta_de_verdad_sigue_saliendo(self):
        """Instrumento encendido: la exención alcanza a los valores, no a la prosa de al lado."""
        self.assertFalse(self.o.es_propio("union"))
        self.assertFalse(self.o.es_propio("credito"))

    def test_el_cotejo_del_ocr_no_se_mide(self):
        """`de` y `a` son el texto que el OCR devolvió y el que dice la página: se comparan
        byte a byte, y corregirles la ortografía es justamente lo que no hay que hacer."""
        self.assertIn("de", self.o.SALTAR_CAMPO)
        self.assertIn("a", self.o.SALTAR_CAMPO)


class TestGiroPropio(unittest.TestCase):
    """`el fuente` y `el checklist` son la voz del repositorio, no discordancias.

    Y la excepción es de giros, no de la regla: `AGREEMENT_DET_NOUN` atrapó un «un cita» de
    verdad, así que apagarla entera costaba más de lo que ahorraba. Lo que se exceptúa está
    medido: `el fuente` son 18 apariciones y todas hablan del código --frente a 64 `la
    fuente`, todas fuente del derecho--, y `checklist` va en masculino 26 veces y en
    femenino ninguna.
    """

    def setUp(self):
        self.o = cargar()

    def test_el_giro_propio_no_se_reclama(self):
        for giro in ("el fuente", "del fuente", "el checklist", "los checklists"):
            with self.subTest(giro):
                self.assertIn(giro, self.o.FRASES_PROPIAS)

    def test_una_discordancia_de_verdad_no_queda_exenta(self):
        for giro in ("un cita", "un tilde", "el suite", "la fuente"):
            with self.subTest(giro):
                self.assertNotIn(giro, self.o.FRASES_PROPIAS)

    def test_la_distincion_de_fuente_sigue_en_pie(self):
        """Si `el fuente` se usara para la fuente del derecho, la excepción taparía el error.

        No se puede medir con un regex —los dos giros son gramaticales— así que lo que se
        fija es el reparto: el masculino tiene que seguir siendo la minoría clara. El día que
        se empareje, la distinción dejó de existir y esta excepción hay que volver a pensarla.
        """
        import re
        masc = fem = 0
        for p in list(RAIZ.rglob("*.md")) + list(RAIZ.rglob("*.py")):
            if "derecho/kb" in p.as_posix() or ".git" in p.parts:
                continue
            t = p.read_text(encoding="utf-8", errors="replace")
            masc += len(re.findall(r"\b(?:el|del|un|este|ese) fuente\b", t, re.I))
            fem += len(re.findall(r"\b(?:la|de la|una|esta|esa) fuente\b", t, re.I))
        self.assertGreater(fem, masc * 2,
                           f"«el fuente» pasó a ser {masc} contra {fem} femeninos: o se está "
                           f"usando para la fuente del derecho, o la distinción se perdió")


class TestCapa2(unittest.TestCase):
    """El material de otro autor no se corrige, así que tampoco se reclama."""

    def setUp(self):
        self.o = cargar()

    def test_kb_y_las_cinco_excepciones_quedan_afuera(self):
        for ruta in ("derecho/kb/CHANGELOG.md",
                     "derecho/evals/README.md",
                     "derecho/evals/consumidor-prepaga-aumento-dnu70/rubrica.md",
                     "derecho/evals/administrativo-caba-recursos-agotamiento-via/rubrica.md"):
            with self.subTest(ruta):
                self.assertTrue(self.o.es_de_otro_autor(RAIZ / ruta))

    def test_lo_propio_si_se_mide(self):
        for ruta in ("AGENTS.md",
                     "derecho/evals/consumidor-dano-punitivo-gratuidad-pba/rubrica.md",
                     "derecho/skills/derecho-argentino/references/laboral.md"):
            with self.subTest(ruta):
                self.assertFalse(self.o.es_de_otro_autor(RAIZ / ruta))

    def test_las_excepciones_estan_nombradas_en_los_dos_documentos(self):
        """Las cinco están escritas en tres lugares: `CAPA_2`, que es la que exime archivos de
        verdad; `LICENCIAS.md`, que es el mapa de licencia con el commit de origen; y
        `AGENTS.md`, que las nombra como regla de trabajo. Si una entra a una lista y no a las
        otras, la herramienta le corrige a otro autor o reclama sobre material intocable.

        MUTACIÓN que lo comprueba: agregar a `CAPA_2` un eval propio —uno que no esté en los dos
        documentos— deja este test en rojo por cada documento que no lo nombra.
        """
        docs = {d: (RAIZ / d).read_text(encoding="utf-8")
                for d in ("LICENCIAS.md", "AGENTS.md")}
        for c in self.o.CAPA_2:
            if c == "derecho/kb":
                continue
            slug = c.rsplit("/", 1)[-1]
            for doc, texto in docs.items():
                with self.subTest(f"{doc} · {slug}"):
                    self.assertIn(slug, texto, f"esta excepción no figura en {doc}")

    def test_toda_excepcion_existe_en_el_arbol(self):
        """Una ruta que ya no está exime un archivo que no hay y esconde uno que sí."""
        for c in self.o.CAPA_2:
            with self.subTest(c):
                self.assertTrue((RAIZ / c).exists(), f"{c} no está en el árbol")


if __name__ == "__main__":
    unittest.main(verbosity=1)
