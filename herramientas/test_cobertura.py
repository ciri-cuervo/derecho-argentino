#!/usr/bin/env python3
"""Tests del control de cobertura normativa. Sin dependencias externas.

    python3 herramientas/test_cobertura.py

`cobertura_normativa.py` contesta la pregunta previa a todos los descargadores: QUE norma
debería estar en el catálogo. Lo que decide si su lista sirve o si nadie la mira es una sola
regla -- separar la ley que es FUENTE de una regla de la que sólo REFORMÓ a otra ya bajada --,
y esa regla no tenía un test.
"""
import importlib.util
import json
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "cobertura_normativa.py"
NORMAS = RAIZ / "argentina" / "fuentes" / "normas" / "normas.json"


def cargar():
    spec = importlib.util.spec_from_file_location("cobertura_normativa", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class TestClaseDeCita(unittest.TestCase):
    """Una ley se nombra por dos motivos y sólo uno pide bajar su texto."""

    def setUp(self):
        self.c = cargar()

    def test_fuente_de_una_regla_pide_el_texto(self):
        for ventana in ("el art. 2 de la Ley 25.323 duplica la indemnización",
                        "según los artículos 1 y 2 de la Ley 25.323",
                        "la Ley 23.661 en su art. 22 y el inc. b) del mismo"):
            with self.subTest(ventana[:40]):
                self.assertEqual(self.c.clase_de_cita(ventana), "regla")

    def test_una_reforma_no_pide_bajar_nada(self):
        # El articulado es del código o de la ley base, que ya está en el catálogo.
        for ventana in ("el art. 245, texto Ley 27.802, fija la base",
                        "el art. 163 según la Ley 15.232 del CPP",
                        "los arts. 8 a 17 derogados por la Ley 27.742",
                        "el art. 11 bis incorporado por la Ley 27.802",
                        "el art. 12 sustituido por la Ley 27.348"):
            with self.subTest(ventana[:40]):
                self.assertEqual(self.c.clase_de_cita(ventana), "reforma")

    def test_sin_articulado_alrededor_es_solo_un_nombre(self):
        self.assertEqual(self.c.clase_de_cita("la Ley 27.742 cambió el régimen laboral"),
                         "solo_nombre")

    def test_la_ventana_es_finita(self):
        """El articulado tiene que estar CERCA. Si se mira todo el módulo, cualquier cita
        queda pegada a algún `art.` y la clasificación deja de decir nada."""
        lejos = "la Ley 25.323 " + ("relleno " * 40) + "art. 9"
        self.assertGreater(len(lejos), self.c.VENTANA)
        self.assertEqual(self.c.clase_de_cita(lejos[:self.c.VENTANA]), "solo_nombre")


class TestCitaYDeclaradas(unittest.TestCase):
    def setUp(self):
        self.c = cargar()

    def test_la_cita_matchea_con_punto_sin_punto_y_con_numeral(self):
        for texto, esperado in (("la Ley 25.323", "25.323"), ("la ley 25323", "25323"),
                                ("Ley N° 25.323", "25.323"), ("Leyes 25.323", "25.323")):
            with self.subTest(texto):
                hallado = self.c.CITA.search(texto)
                self.assertIsNotNone(hallado, f"no reconoció «{texto}»")
                self.assertEqual(hallado.group(1), esperado)

    def test_declaradas_sale_del_slug_y_no_del_titulo(self):
        """MUTACION VIVIDA: los números salían de `titulo` + `slug`.

        El título es prosa y nombra otras leyes -- "Reglamentación de la Ley 25.326",
        "abrogado por la Ley 27.063" --, así que cada una de esas quedaba declarada por
        aparecer en la entrada de OTRA, y el control dejaba de reclamarla. El caso vivo era la
        Ley 24.430, que no tiene entrada propia y sólo figura en el título de `cn-1994`.
        """
        declaradas = self.c.declaradas()
        entradas = json.loads(NORMAS.read_text(encoding="utf-8"))["normas"]
        slugs = " ".join(e.get("slug", "") for e in entradas)
        for numero in declaradas:
            with self.subTest(numero):
                self.assertRegex(slugs, re.escape(numero),
                                 f"{numero} se declara sin estar en ningún slug: salió de "
                                 f"la prosa de un título")

    def test_ninguna_entrada_esconde_su_numero_solo_en_el_titulo(self):
        """La contracara: leer sólo el slug no puede perder una declaración real.

        Si el título arranca nombrando su propia norma con número, ese número tiene que estar
        en el slug. Así el día que entre una entrada con el número sólo en el título, esto lo
        dice, en vez de que la norma quede reportada como faltante sin serlo.
        """
        arranque = re.compile(r"^(?:Ley|Leyes|Decreto|Decreto-Ley)\s+(?:N[°º]\s*)?(\d{2}\.?\d{3})")
        for e in json.loads(NORMAS.read_text(encoding="utf-8"))["normas"]:
            hallado = arranque.match(e.get("titulo", ""))
            if not hallado:
                continue
            numero = hallado.group(1).replace(".", "")
            with self.subTest(e.get("slug", "")):
                self.assertIn(numero, e.get("slug", "").replace(".", ""),
                              "el número propio no está en el slug: declaradas() no lo va a ver")


class TestCorridaCompleta(unittest.TestCase):
    def test_no_hay_pendientes_sin_veredicto(self):
        """Toda ley citada como fuente de una regla y no declarada tiene que tener veredicto
        escrito. Lo que ninguna de las dos medidas admite es el silencio."""
        c = cargar()
        tengo, ya = c.declaradas(), c.decisiones()
        sin_veredicto = []
        for archivo in sorted(c.REFS.glob("*.md")):
            texto = archivo.read_text(encoding="utf-8")
            for m in c.CITA.finditer(texto):
                numero = m.group(1).replace(".", "")
                if numero in tengo or numero in ya:
                    continue
                ventana = texto[max(0, m.start() - c.VENTANA):m.end() + c.VENTANA]
                if c.clase_de_cita(ventana) == "regla":
                    sin_veredicto.append(f"{numero} ({archivo.name})")
        self.assertEqual(sorted(set(sin_veredicto)), [],
                         "hay leyes usadas con articulado, sin declarar y sin veredicto en "
                         "cobertura-revisada.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
