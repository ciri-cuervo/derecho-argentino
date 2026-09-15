#!/usr/bin/env python3
"""Tests de las herramientas de auditoría de jurisprudencia. Sin dependencias externas.

    python3 herramientas/test_auditoria.py
"""
import json
import pathlib
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))

import auditar_fechas_fallos as auditor


class TestFechaImpresa(unittest.TestCase):
    """Los tomos de los 80 no tienen firma digital: la fecha está impresa en el cuerpo."""

    FIORENTINO = """
    Por todo lo cual, opino que corresponde anular el fallo dictado. Buenos
    Aires, 21 de mayo de 1984. Juan Octavio Gauna.

    FALLO DE LA CORTE SUPREMA
    Buenos Aires, 27 de noviembre de 1984.

    Vistos los autos: "Recurso de hecho deducido por el abogado defensor".
    """

    def test_toma_la_fecha_del_fallo_y_no_la_del_dictamen(self):
        # El dictamen del Procurador lleva otra fecha y va ANTES en el documento.
        self.assertEqual(auditor.fecha_impresa(self.FIORENTINO), "1984-11-27")

    def test_sin_el_titulo_del_fallo_no_adivina(self):
        sin_titulo = self.FIORENTINO.replace("FALLO DE LA CORTE SUPREMA", "")
        self.assertIsNone(auditor.fecha_impresa(sin_titulo))

    def test_dia_de_un_digito(self):
        texto = "FALLO DE LA CORTE SUPREMA\nBuenos Aires, 5 de agosto de 1986,"
        self.assertEqual(auditor.fecha_impresa(texto), "1986-08-05")

    def test_tolera_setiembre_sin_p(self):
        texto = "FALLO DE LA CORTE SUPREMA\nBuenos Aires, 9 de setiembre de 1987."
        self.assertEqual(auditor.fecha_impresa(texto), "1987-09-09")

    def test_un_mes_ilegible_no_inventa_fecha(self):
        texto = "FALLO DE LA CORTE SUPREMA\nBuenos Aires, 9 de agoslo de 1987."
        self.assertIsNone(auditor.fecha_impresa(texto))

    def test_no_mira_mas_alla_del_titulo(self):
        # Una fecha que aparece mucho despues no es la del fallo.
        texto = "FALLO DE LA CORTE SUPREMA\n" + "x" * 500 + "\nBuenos Aires, 1 de marzo de 1990."
        self.assertIsNone(auditor.fecha_impresa(texto))


class TestManifiestoDeFallos(unittest.TestCase):
    def test_ninguna_fecha_es_el_1_de_enero(self):
        # Un 1 de enero en este manifiesto es relleno de una fecha que no se pudo leer, no una
        # fecha: los tres que quedaban se recuperaron del tomo el 14/09/2026.
        fallos = json.loads(
            (RAIZ / "argentina" / "fuentes" / "jurisprudencia" / "fallos.json")
            .read_text(encoding="utf-8"))["fallos"]
        rellenos = [f["slug"] for f in fallos if str(f.get("fecha", "")).endswith("-01-01")]
        self.assertEqual(rellenos, [], "fecha sin confirmar: correr auditar_fechas_fallos.py")


class TestDependenciasExternas(unittest.TestCase):
    """Sin `pdftotext`, el auditor metía el FileNotFoundError en el mismo `except` que usa
    para un PDF roto y seguía: el resumen decía `0 A REVISAR` con el auditor apagado y salía
    con código 0. En una máquina sin poppler —lo normal en Windows— los 64 fallos pasaban sin
    mirarse. Si la herramienta no puede medir, lo dice y se planta."""

    def test_nombra_que_instalar_y_para_que_plataforma(self):
        import _externos
        texto = _externos.instruccion("pdftotext")
        self.assertIn("pdftotext", texto)
        self.assertIn("poppler", texto)
        esperado = {"darwin": "brew", "win32": "choco", "linux": "apt"}[
            "darwin" if sys.platform == "darwin"
            else "win32" if sys.platform.startswith("win") else "linux"]
        self.assertIn(esperado, texto)

    def test_exigir_corta_en_vez_de_dejar_seguir(self):
        import _externos
        with self.assertRaises(SystemExit) as cm:
            _externos.exigir("binario-que-no-existe-en-ninguna-plataforma")
        self.assertIn("falta", str(cm.exception))

    def test_exigir_no_molesta_cuando_el_binario_esta(self):
        import _externos
        _externos.exigir(pathlib.Path(sys.executable).name)

    def test_el_auditor_exige_pdftotext_antes_de_contar(self):
        """MUTACIÓN del modo de fallar: que la exigencia esté ANTES de armar el resumen, no
        después. Si se cuela debajo, vuelve el verde con el instrumento apagado."""
        fuente = (RAIZ / "herramientas" / "auditar_fechas_fallos.py").read_text(
            encoding="utf-8")
        cuerpo = fuente.split("def main()", 1)[1]
        exige = cuerpo.index('_externos.exigir("pdftotext")')
        resume = cuerpo.index("A REVISAR")
        self.assertLess(exige, resume)


if __name__ == "__main__":
    unittest.main()
