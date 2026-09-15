#!/usr/bin/env python3
"""Tests del medidor de deuda. Sin dependencias externas.

    python3 herramientas/test_pendientes.py
"""
import sys
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))

import pendientes


class TestMarcadoresDeInstituto(unittest.TestCase):
    """Distingue el hueco de contenido de la definición del marcador y de la prosa que lo cita."""

    def test_encuentra_huecos_reales(self):
        hallados = pendientes.institutos_sin_precedente()
        self.assertGreater(len(hallados), 0, "dejó de leer los marcadores de los módulos")
        for archivo, _, payload in hallados:
            with self.subTest(f"{archivo}: {payload[:40]}"):
                self.assertNotEqual(payload, "...")
                self.assertFalse(payload.startswith("doctrina requerida"))

    def test_no_cuenta_la_definicion_del_marcador(self):
        # marcadores.md define B1: si entrara al corpus, el módulo del vocabulario figuraría
        # como si le faltara doctrina.
        self.assertNotIn("marcadores.md", {a for a, _, _ in pendientes.institutos_sin_precedente()})


class TestDeudaPorBloque(unittest.TestCase):
    def test_la_frase_no_se_corta_en_una_abreviatura(self):
        # "Falta fallo cargado sobre la escala del art. 44" se cortaba en "del art".
        frases = [t for _, _, t in pendientes.deuda_por_bloque()]
        self.assertTrue(frases, "dejó de leer la tabla de estado de verificación")
        for frase in frases:
            with self.subTest(frase[:50]):
                self.assertFalse(frase.rstrip().endswith(("art", "Ley", "Leyes", "Decreto")),
                                 f"frase cortada en una abreviatura: {frase!r}")


class TestVerificacionVencida(unittest.TestCase):
    def test_aplica_la_regla_de_seis_meses_de_la_propia_tabla(self):
        self.assertEqual(pendientes.DIAS_DE_GRACIA, 180)
        lejano = date(2030, 1, 1)
        self.assertGreater(len(pendientes.verificacion_vencida(lejano)), 0,
                           "con una fecha lejana todos los bloques tienen que estar vencidos")

    def test_ordena_del_mas_vencido_al_menos(self):
        vencidos = pendientes.verificacion_vencida(date(2030, 1, 1))
        dias = [d for _, _, d in vencidos]
        self.assertEqual(dias, sorted(dias, reverse=True))


class TestCruceConEvals(unittest.TestCase):
    def test_reconoce_el_modulo_por_el_slug_del_caso(self):
        # `civil-danos-transito-...` ejercita civil.md sin nombrar el archivo.
        self.assertNotIn("civil.md", pendientes.modulos_sin_eval())

    def test_los_modulos_de_rama_sin_eval_se_reportan(self):
        sin_eval = pendientes.modulos_sin_eval()
        for esperado in ("transito.md", "previsional.md", "tributario.md"):
            self.assertIn(esperado, sin_eval)


if __name__ == "__main__":
    unittest.main()
