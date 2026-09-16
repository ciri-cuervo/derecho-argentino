#!/usr/bin/env python3
"""Tests del detector de fuga textual desde la capa 2. Sin dependencias externas.

    python3 herramientas/test_fuga.py

`fuga_textual.py` era la única herramienta del repositorio sin una sola línea de test, y es
una de las dos mitades de la frontera de licencia: la que vigila la prosa de `kb/` que entra a
un módulo. Se escapó de todas las redes por una razón concreta: la corrida en seco que ejercita
a las demás -`TestSalidaCodificable`- las llama sin argumentos, y ésta necesita rutas.

La prosa de prueba es INVENTADA y el corpus de capa 2 se arma en un directorio temporal. No se
copia texto de `derecho/kb/` a un archivo de este repositorio: eso es exactamente lo que la
herramienta existe para impedir.
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "fuga_textual.py"


def cargar():
    spec = importlib.util.spec_from_file_location("fuga_textual", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# Prosa inventada, con las diez palabras seguidas que hacen falta para que entre una secuencia
# de nueve. No dice nada de ningún expediente: es una oración cualquiera con forma jurídica.
PROSA_DE_CAPA_2 = (
    "La contratista quedó liberada de responder por el desvío del cronograma cuando la "
    "demora provino de una decisión del comitente que nadie discutió en el expediente."
)


class TestFuncionesPuras(unittest.TestCase):
    def setUp(self):
        self.f = cargar()

    def test_la_excepcion_es_la_ruta_y_no_el_nombre(self):
        """MUTACION VIVIDA: la excepción se comparaba por basename.

        `marcadores.md` está exceptuado porque transcribe el glosario de `kb/` a propósito: es
        vocabulario controlado del que dependen los scripts. Comparando por nombre suelto,
        cualquier archivo llamado así en cualquier parte quedaba sin medir, y ya había uno -- el
        grader homónimo de los evals -- que dejó de medirse sin que nadie lo pidiera.
        """
        exceptuada = Path("derecho/skills/derecho-argentino/references/marcadores.md")
        self.assertTrue(self.f.es_excepcion(exceptuada))
        self.assertTrue(self.f.es_excepcion(Path("/abs") / exceptuada))
        self.assertFalse(self.f.es_excepcion(Path("derecho/evals/x/graders/marcadores.md")),
                         "un homónimo en otra carpeta no puede quedar sin medir")
        self.assertFalse(self.f.es_excepcion(Path("marcadores.md")))

    def test_normalizar_saca_lo_que_no_es_prosa(self):
        # Backticks, rutas y la cita entrecomillada del perfil: los tres comparten cadenas con
        # kb/ por construcción, y eso es la referencia funcionando.
        self.assertNotIn("codigo", self.f.normalizar("texto `codigo` texto"))
        self.assertNotIn("json", self.f.normalizar("ver derecho/kb/perfiles/x.json aca"))
        self.assertNotIn("citada", self.f.normalizar('dice *"una frase citada del perfil"* y no'))

    def test_normalizar_conserva_las_letras_del_castellano(self):
        # Si la clase de letras pierde una, la palabra se parte y la secuencia deja de matchear:
        # el control ignora en silencio justo el texto acentuado, que es casi todo.
        for palabra in ("año", "antigüedad", "prórroga", "cónyuge", "días"):
            with self.subTest(palabra):
                self.assertIn(palabra, self.f.normalizar(f"la {palabra} del caso"))

    def test_una_secuencia_de_citas_no_es_prosa(self):
        self.assertTrue(self.f.es_cita("art 245 de la ley 27802 texto segun el art 51"))
        self.assertTrue(self.f.es_cita("30 dias habiles judiciales del plazo de la ley 15057"))

    def test_una_secuencia_redactada_si_es_prosa(self):
        redactada = " ".join(self.f.normalizar(PROSA_DE_CAPA_2)[:9])
        self.assertFalse(self.f.es_cita(redactada),
                         f"«{redactada}» se descarta como cita y es redacción")

    def test_las_secuencias_son_de_nueve_palabras(self):
        palabras = ["p%d" % i for i in range(12)]
        secuencias = self.f.secuencias(palabras)
        self.assertEqual(len(secuencias), 12 - self.f.N + 1)
        self.assertTrue(all(len(s.split()) == self.f.N for s in secuencias))


class TestCorridaCompleta(unittest.TestCase):
    """El detector, de punta a punta, contra un corpus de capa 2 armado a mano."""

    def correr(self, *rutas, cwd):
        return subprocess.run([sys.executable, str(HERRAMIENTA), *rutas],
                              capture_output=True, text=True, cwd=cwd)

    def armar(self, d: Path, prosa_del_modulo: str) -> Path:
        (d / "derecho" / "kb").mkdir(parents=True)
        (d / "derecho" / "kb" / "perfil-CLAUDE.md").write_text(
            "# Perfil heredado\n\n" + PROSA_DE_CAPA_2 + "\n", encoding="utf-8")
        modulo = d / "modulo.md"
        modulo.write_text("# Modulo propio\n\n" + prosa_del_modulo + "\n", encoding="utf-8")
        return modulo

    def test_la_prosa_copiada_se_reporta_y_sale_con_codigo_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            modulo = self.armar(d, PROSA_DE_CAPA_2)
            hecho = self.correr(modulo.name, cwd=d)
            self.assertIn("PROSA:", hecho.stdout, f"no vio la copia:\n{hecho.stdout}")
            self.assertEqual(hecho.returncode, 1, "prosa copiada y salió en verde")

    def test_compartir_articulado_no_es_fuga(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            # Mismo dato, redacción propia: el articulado y los plazos se mueven libres.
            modulo = self.armar(d, "El art. 245 de la LCT segun el art. 51 de la Ley 27.802 "
                                   "fija 30 dias habiles judiciales de plazo en el fuero.")
            hecho = self.correr(modulo.name, cwd=d)
            self.assertNotIn("PROSA:", hecho.stdout, f"marcó articulado:\n{hecho.stdout}")
            self.assertEqual(hecho.returncode, 0)

    def test_sin_capa_2_se_planta_en_vez_de_dar_verde(self):
        # No hay veredicto verde por ausencia de instrumento: sin corpus no hay medida.
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "modulo.md").write_text("# vacio\n", encoding="utf-8")
            hecho = self.correr("modulo.md", cwd=d)
            self.assertEqual(hecho.returncode, 2, "midió sin corpus de capa 2")
            self.assertIn("derecho/kb", hecho.stderr + hecho.stdout)

    def test_el_grader_homonimo_se_mide_y_el_glosario_no(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            self.armar(d, "texto propio cualquiera")
            grader = d / "derecho" / "evals" / "caso" / "graders" / "marcadores.md"
            grader.parent.mkdir(parents=True)
            grader.write_text("# grader\n\n" + PROSA_DE_CAPA_2 + "\n", encoding="utf-8")
            glosario = d / "references" / "marcadores.md"
            glosario.parent.mkdir(parents=True)
            glosario.write_text("# glosario\n\n" + PROSA_DE_CAPA_2 + "\n", encoding="utf-8")
            hecho = self.correr(grader.relative_to(d).as_posix(),
                                glosario.relative_to(d).as_posix(), cwd=d)
            self.assertIn("PROSA:", hecho.stdout, "el grader homónimo quedó sin medir")
            self.assertIn("excepcion declarada", hecho.stdout, "el glosario dejó de exceptuarse")


if __name__ == "__main__":
    unittest.main(verbosity=2)
