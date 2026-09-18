#!/usr/bin/env python3
"""Tests del detector de normas bajadas que nadie usa. Sin dependencias externas.

    python3 herramientas/test_huerfanas.py

Lo que sostiene no es el número de huérfanas —crece y baja con el trabajo— sino las dos
decisiones que hacen que la lista sirva: cómo se reconoce que una norma está nombrada, y qué
queda deliberadamente fuera de la medida.
"""
import importlib.util
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "normas_huerfanas.py"


def cargar():
    spec = importlib.util.spec_from_file_location("normas_huerfanas", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class TestFormasDeCita(unittest.TestCase):
    """Una norma se nombra de varias maneras y el slug no es ninguna de ellas."""

    def setUp(self):
        self.h = cargar()

    def test_una_ley_se_cita_con_punto_y_sin_punto(self):
        self.assertEqual(sorted(self.h.formas("ley-27499")), sorted(["27.499", "27499"]))
        self.assertEqual(sorted(self.h.formas("pba-ley-15134")), sorted(["15.134", "15134"]))

    def test_un_decreto_se_cita_con_barra_y_con_dos_digitos_de_ano(self):
        self.assertEqual(sorted(self.h.formas("decreto-659-1996")),
                         sorted(["659/1996", "659/96"]))

    def test_una_constitucion_no_tiene_forma_de_cita(self):
        """No lleva número, y de eso depende que caiga en SIN MEDIDA y no en huérfana."""
        self.assertEqual(self.h.formas("constitucion-salta"), [])
        self.assertEqual(self.h.formas("cn-tratados-ddhh"), [])


class TestElBordeDeLaCoincidencia(unittest.TestCase):
    """El control que impide contar un uso que no existe.

    MUTACIÓN QUE LO RESPALDA: reemplazar el `re.search` con bordes de `aparece()` por un
    `forma in texto`. Corrida el 17/09/2026: el test falla, y **el conteo del árbol real no
    cambia**. O sea que hoy el guardarraíl no está sosteniendo ningún caso: es preventivo, y
    eso se dice en vez de insinuar que atrapa algo que todavía no pasó. Lo que evita es
    concreto: que `6716` se dé por usada por aparecer dentro de `26716`, que es cuestión de
    que entre una ley más al catálogo.
    """

    def setUp(self):
        self.h = cargar()

    def test_un_numero_adentro_de_otro_no_cuenta_como_uso(self):
        self.assertFalse(self.h.aparece("6716", "la Ley 26716 dice otra cosa"))
        self.assertFalse(self.h.aparece("27.499", "según la Ley 127.499 del Reino"))

    def test_la_mencion_real_si_cuenta(self):
        self.assertTrue(self.h.aparece("27.499", "la Ley 27.499 impone la capacitación"))
        self.assertTrue(self.h.aparece("659/1996", "el Decreto 659/1996 trae el baremo"))

    def test_las_dos_formas_de_una_ley_se_buscan_juntas(self):
        """Por eso `formas()` devuelve las dos: la prosa escribe «6.716» y el slug trae «6716».

        Buscar sólo la forma sin punto daría huérfana a una ley que el módulo nombra en todas
        sus menciones, que es el falso positivo más caro de esta lista: manda a escribir algo
        que ya está escrito.
        """
        texto = "el art. 12 de la Ley 6.716 fija el aporte"
        self.assertFalse(self.h.aparece("6716", texto), "sin punto no aparece, y está bien")
        self.assertTrue(any(self.h.aparece(f, texto) for f in self.h.formas("pba-ley-6716")),
                        "con las dos formas tiene que encontrarla")


class TestElArbolReal(unittest.TestCase):
    def setUp(self):
        self.h = cargar()

    def test_no_reporta_una_norma_que_no_esta_bajada(self):
        """Declarada y sin bajar es otra deuda, y la mide `descargar_normas.py`.

        Mezclarlas haría que esta lista creciera con cada declaración nueva, que es justo el
        momento en que todavía no hay nada que escribir.
        """
        sueltas, sin_medida, _ = self.h.huerfanas()
        for slug, _titulo in sueltas + sin_medida:
            with self.subTest(slug):
                self.assertTrue(self.h.bajada(slug), "reportó una norma que no está en fuentes/")

    def test_las_constituciones_van_a_sin_medida_y_no_a_huerfanas(self):
        """La medida por nombre se probó y se descartó: el detector no adivina.

        Si alguna constitución apareciera como huérfana significaría que volvió a intentarse
        inferir el uso desde el nombre, que es lo que daba por usadas a Misiones dentro de
        «comisiones» y a Catamarca por un renglón que habla de un defecto del texto.
        """
        sueltas, _sin_medida, _ = self.h.huerfanas()
        for slug, _titulo in sueltas:
            with self.subTest(slug):
                self.assertTrue(self.h.formas(slug),
                                "una norma sin forma de cita entró como huérfana: el detector "
                                "está infiriendo el uso desde el nombre")

    def test_el_catalogo_propio_no_cuenta_como_uso(self):
        """`normas.json` nombra todos los slugs: si contara, no habría huérfana posible."""
        self.assertIn("normas.json", self.h.EXCLUIDOS)
        self.assertIn("procedencia.json", self.h.EXCLUIDOS)
        sueltas, _sin_medida, usadas = self.h.huerfanas()
        self.assertGreater(len(sueltas) + usadas, 0, "no leyó el catálogo")


if __name__ == "__main__":
    unittest.main(verbosity=2)
