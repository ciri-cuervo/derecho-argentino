#!/usr/bin/env python3
"""Tests del detector de reformas no leidas. Sin dependencias externas.

    python3 herramientas/test_reformas.py
"""
import json
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))

import reformas_no_leidas as detector

HERRAMIENTA = RAIZ / "herramientas" / "reformas_no_leidas.py"
REGISTRO = RAIZ / "herramientas" / "reformas-revisadas.json"


class TestExtraccionDeNotas(unittest.TestCase):
    """La nota de reforma vive al pie del artículo y hay que emparejar ley con SU fecha.

    InfoLEG escribe esa fecha de cuatro formas distintas, y no es una hipotesis: medido sobre
    los textos bajados en `argentina/fuentes/normas/`, hay 1.394 notas `dd/mm`, 785 `dd/m`, 704
    `d/m` y 113 `d/mm`. El detector tiene que leer las cuatro, así que las cuatro están acá.

    Ese directorio queda afuera de cualquier normalización de fechas del repositorio, porque es
    texto bajado y se coteja por hash: rellenar un cero ahí cambiaria el archivo respecto de su
    fuente. Estos fixtures lo imitan, así que tampoco se normalizan.
    """

    # (forma, texto del B.O., dia y mes tal como los devuelve el regex)
    FORMAS = (("dd/mm", "B.O. 10/03/2025", "10", "03", "2025"),
              ("dd/m", "B.O. 14/4/2020", "14", "4", "2020"),
              ("d/m", "B.O. 3/8/2017", "3", "8", "2017"),
              ("d/mm", "B.O. 6/11/2009", "6", "11", "2009"))

    def test_empareja_la_ley_con_su_propia_fecha_en_las_cuatro_formas(self):
        for forma, bo, dia, mes, anio in self.FORMAS:
            nota = (f"(Artículo sustituido por art. 7° de la Ley N° 27.786 {bo}. Vigencia: "
                    f"a partir del día siguiente.)")
            with self.subTest(forma):
                self.assertEqual(detector.NOTA.findall(nota), [("27.786", dia, mes, anio)])

    def test_no_cruza_una_ley_con_la_fecha_de_otra_nota(self):
        # Dos notas seguidas, y de formas distintas: cada ley tiene que quedar con la suya, no
        # con la del vecino.
        texto = ("(Artículo sustituido por art. 1° de la Ley N° 25.561 B.O. 7/1/2002).\n\n"
                 "(Artículo incorporado por art. 2° de la Ley N° 27.786 B.O. 10/03/2025.)")
        self.assertEqual(detector.NOTA.findall(texto),
                         [("25.561", "7", "1", "2002"), ("27.786", "10", "03", "2025")])

    def test_una_fecha_imposible_no_rompe_la_corrida(self):
        # El script no adivina: descarta la nota y sigue.
        self.assertEqual(detector.NOTA.findall("Ley N° 27.786 B.O. 31/02/2025"),
                         [("27.786", "31", "02", "2025")])
        self.assertEqual(detector.ultima_reforma_por_norma(desde=9999), [])


class TestUltimaReforma(unittest.TestCase):
    def test_se_queda_con_la_mas_reciente_de_cada_norma(self):
        hallados = detector.ultima_reforma_por_norma(desde=0)
        self.assertGreater(len(hallados), 20, "dejó de leer las notas de los consolidados")
        por_norma = {}
        for cuando, slug, _ in hallados:
            por_norma.setdefault(slug, set()).add(cuando)
        for slug, fechas in por_norma.items():
            with self.subTest(slug):
                self.assertEqual(len(fechas), 1, f"{slug} quedó con más de una fecha")

    def test_el_codigo_penal_llega_hasta_la_ley_27786(self):
        # Si el consolidado se rebaja a una versión anterior, esto lo dice.
        cp = [(c, l) for c, s, l in detector.ultima_reforma_por_norma(desde=0) if s == "cp-11179"]
        self.assertEqual(cp, [(date(2025, 3, 10), "27.786")])

    def test_desde_filtra_por_anio(self):
        todas = detector.ultima_reforma_por_norma(desde=0)
        recientes = detector.ultima_reforma_por_norma(desde=2025)
        self.assertLess(len(recientes), len(todas))
        self.assertTrue(all(c.year >= 2025 for c, _, _ in recientes))


class TestRegistroDeVeredictos(unittest.TestCase):
    def test_no_quedan_candidatos_sin_veredicto(self):
        hecho = subprocess.run([sys.executable, str(HERRAMIENTA)], capture_output=True, text=True)
        self.assertEqual(hecho.returncode, 0,
                         "hay reformas recientes que ningún módulo nombra:\n" + hecho.stdout)

    def test_cada_veredicto_tiene_motivo_escrito(self):
        registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
        self.assertTrue(registro["reformas"])
        for clave, ficha in registro["reformas"].items():
            with self.subTest(clave):
                self.assertIn(":", clave, "la clave es 'slug:ley'")
                self.assertIn(ficha["veredicto"], ("no-toca-el-modulo", "absorbida"))
                self.assertGreater(len(ficha["motivo"]), 40,
                                   "un veredicto sin motivo es un silencio, no una decisión")


if __name__ == "__main__":
    unittest.main()
