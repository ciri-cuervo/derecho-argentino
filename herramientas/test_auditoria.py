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
        # Una fecha que aparece mucho después no es la del fallo.
        texto = "FALLO DE LA CORTE SUPREMA\n" + "x" * 500 + "\nBuenos Aires, 1 de marzo de 1990."
        self.assertIsNone(auditor.fecha_impresa(texto))


class TestManifiestoDeFallos(unittest.TestCase):
    def test_ninguna_fecha_es_el_1_de_enero(self):
        # Un 1 de enero en este manifiesto es relleno de una fecha que no se pudo leer, no una
        # fecha: los tres que quedaban se recuperaron del tomo el 14/09/2026.
        fallos = json.loads(
            (RAIZ / "derecho" / "fuentes" / "jurisprudencia" / "fallos.json")
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


class TestMedidaDeBasura(unittest.TestCase):
    """La medida de basura de OCR, que decide si un documento se puede transcribir.

    Se ejercita sobre texto y no sobre PDF a propósito: la regla que hay que fijar es que CERO
    PALABRAS no es cero basura, y eso no depende de como se extrajo el texto. Un escaneo sin
    capa de texto devuelve vacío, y la versión anterior lo informaba como 0% -- la lectura de
    un documento impecable -- porque dividía por `max(len(tokens), 1)`. Pasaba por el mejor del
    corpus justamente el que no se puede leer.
    """

    def setUp(self):
        import calidad_ocr
        self.ocr = calidad_ocr

    def test_sin_palabras_no_hay_medida(self):
        for vacio in ("", "   \n\t ", "123 456", "--- *** ---"):
            with self.subTest(repr(vacio)):
                self.assertIsNone(self.ocr.proporcion_sucia(vacio),
                                  "sin palabras devolvió un número: se lee como documento limpio")

    def test_texto_sano_mide_cero(self):
        sano = ("Vistos los autos: Recurso de hecho deducido por la defensa. "
                "Considerando que la cámara resolvió con arreglo al artículo 14.")
        self.assertEqual(self.ocr.proporcion_sucia(sano), 0.0)

    def test_basura_de_caracteres_se_mide_alto(self):
        # Como se ve un tomo con la capa de texto arruinada: caracteres que no son del idioma.
        roto = r"&n,n+`7n4NK\W.nG.nZ7K\7K4A.n57nG.n-.G. Considerando"
        medido = self.ocr.proporcion_sucia(roto)
        self.assertGreater(medido, self.ocr.UMBRAL_BASURA,
                           f"midió {medido:.0%} sobre texto destruido")

    def test_la_medida_es_de_CARACTERES_y_por_eso_no_alcanza(self):
        """El límite de la medida, fijado a propósito para que nadie la "arregle" aflojándola.

        `basura()` cuenta caracteres que no son del castellano. Una capa de OCR puede estar
        destruida usando SÓLO caracteres válidos, y entonces mide 0%: este texto es de un tomo
        que `lecturas-ocr.json` tiene registrado como `destruido`, y por acá pasa impecable.

        No es un defecto a corregir: es la razón por la que el veredicto de los otros dos
        defectos -- columnas y sustituciones -- se LEE y se registra, y no se estima. Cuatro
        medidas se probaron y las cuatro fallaron sobre casos conocidos. Si algún día esta
        aserción molesta, lo que hay que revisar es la medida nueva contra el corpus entero,
        no este número.
        """
        destruido_pero_legible_al_regex = "Considerando: 1*) i BEi Que vei segtin vi surge Xi"
        self.assertEqual(self.ocr.proporcion_sucia(destruido_pero_legible_al_regex), 0.0)

    def test_las_letras_del_castellano_no_son_basura(self):
        # Si la clase de letras pierde una, un documento sano se mide como roto y se manda a
        # reocr sin necesidad. Ya pasó en otro control con la Ü.
        limpio = "El cónyuge alegó antigüedad y daños en años anteriores según la ley"
        self.assertEqual(self.ocr.proporcion_sucia(limpio), 0.0)

    def test_la_puntuacion_del_castellano_tampoco(self):
        limpio = '¿Corresponde? ¡Sí! —dijo— «con arreglo al art. 14», 3º párrafo.'
        self.assertEqual(self.ocr.proporcion_sucia(limpio), 0.0)

    def test_un_pdf_ilegible_no_se_informa_como_limpio(self):
        """`basura()` sobre algo que `pdftotext` no puede leer devuelve None, no 0.0."""
        import _externos
        if _externos.falta("pdftotext"):
            self.skipTest("sin poppler: la regla pura la fija test_sin_palabras_no_hay_medida")
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            falso = pathlib.Path(d) / "no-es-un-pdf.pdf"
            falso.write_text("esto no es un PDF\n", encoding="utf-8")
            self.assertIsNone(self.ocr.basura(falso))


if __name__ == "__main__":
    unittest.main()
