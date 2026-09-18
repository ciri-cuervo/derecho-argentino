#!/usr/bin/env python3
"""Tests de `verificar_respuesta.py`.

Lo que se fija acá no es que el script corra: es que NO pase por alto las tres formas en que un
marcador se rompe sin hacer ruido. Un marcador inventado, uno escrito distinto y uno de la lista
de contraejemplos salen los tres con forma de marcador y los tres se copian al escrito.

Ancla en `Path(__file__)`, no en el config del usuario: un test valida el checkout donde
vive, no el que diga una configuración de la máquina.

El caso de la diéresis tiene historia propia en este repositorio: las clases de letras estaban
escritas a mano y les faltaba la Ü, así que `[VERIFICAR ANTIGÜEDAD: ...]` no era ni candidato y
el control lo ignoraba en silencio. Un control que ignora es peor que uno que no existe.
"""

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "verificar_respuesta.py"


def cargar():
    spec = importlib.util.spec_from_file_location("verificar_respuesta", HERRAMIENTA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestVocabulario(unittest.TestCase):
    def setUp(self):
        self.vr = cargar()
        self.canonicos, self.contraejemplos = self.vr.vocabulario()

    def test_lee_las_cuatro_series_del_vocabulario(self):
        self.assertEqual(len(self.canonicos), 26)
        for esperado in ("ALERTA PLAZO FATAL", "VACÍO PROBATORIO", "VERIFICAR VIGENCIA"):
            self.assertIn(esperado, self.canonicos)

    def test_el_canonico_pasa_sin_hallazgos(self):
        texto = ("[ALERTA PLAZO FATAL: art. 2561 CCyCN - 3 años]\n"
                 "[VERIFICAR VIGENCIA: Ley 25.358]\n")
        self.assertEqual(self.vr.revisar(texto, self.canonicos, self.contraejemplos), [])

    def test_el_inventado_se_reclama(self):
        texto = "[VERIFICAR ANTIGÜEDAD: cómputo del art. 245 - aportar fecha de ingreso]"
        self.assertEqual(self.vr.revisar(texto, self.canonicos, self.contraejemplos),
                         [("desconocido", "VERIFICAR ANTIGÜEDAD")])

    def test_el_mal_escrito_se_distingue_del_inventado(self):
        """Es el caso más engañoso: a ojo pasa por bueno, y no es lo mismo que inventar uno.

        Sin tilde, en minúscula o con un espacio de más: las tres son el mismo marcador
        escrito distinto, y el marcador se copia tal cual o no sirve.
        """
        for mal in ("[VACIO PROBATORIO: falta la cédula]",
                    "[Vacío Probatorio: falta la cédula]",
                    "[VACÍO  PROBATORIO: falta la cédula]"):
            with self.subTest(mal):
                hallazgos = self.vr.revisar(mal, self.canonicos, self.contraejemplos)
                self.assertEqual(len(hallazgos), 1, hallazgos)
                self.assertEqual(hallazgos[0][0], "mal escrito", hallazgos)
                self.assertIn("VACÍO PROBATORIO", hallazgos[0][1])

    def test_la_prosa_entre_corchetes_no_se_reclama_como_marcador(self):
        """Control negativo. El punto quedó fuera del patrón justamente por esto: un resultado
        de eval trae `[Verificar el plazo vigente del art. 11.]`, que es prosa, no un marcador.
        Un control que reclama texto correcto deja de mirarse."""
        for prosa in ("[Verificar el plazo vigente del art. 11.]",
                      "[ver la nota al pie del art. 3.]"):
            with self.subTest(prosa):
                self.assertEqual(
                    self.vr.revisar(prosa, self.canonicos, self.contraejemplos), [])

    def test_el_contraejemplo_declarado_se_reclama_como_no_usar(self):
        """La tercera clase de hallazgo que el docstring promete, y la única que no se probaba.

        Dos mutaciones independientes pasaban en verde: que `vocabulario()` dejara de parsear la
        tabla «No usar», y que la rama entera se borrara. Un contraejemplo es un marcador que el
        propio vocabulario declara equivocado, así que dejarlo pasar es peor que no tener lista.
        """
        solo_contraejemplos = sorted(self.contraejemplos - self.canonicos)
        self.assertTrue(solo_contraejemplos,
                        "marcadores.md dejó de declarar contraejemplos: no hay qué probar")
        for nombre in solo_contraejemplos[:5]:
            with self.subTest(nombre):
                hallazgos = self.vr.revisar(f"[{nombre}: algo]", self.canonicos,
                                            self.contraejemplos)
                self.assertEqual(hallazgos, [("no usar", nombre)])

    def test_un_marcador_con_digito_punto_o_barra_no_escapa(self):
        """Mismo modo de falla que la Ü, con puntuación: si el nombre no matchea el patrón, el
        marcador inventado no es ni candidato y el control lo IGNORA en silencio."""
        for inventado in ("[MARCADOR INVENTADO 2: x]", "[FALTA DATO/PRUEBA: x]"):
            with self.subTest(inventado):
                hallazgos = self.vr.revisar(inventado, self.canonicos, self.contraejemplos)
                self.assertEqual(len(hallazgos), 1, f"{inventado} pasó sin ser candidato")
                self.assertEqual(hallazgos[0][0], "desconocido")

    def test_la_dieresis_no_hace_que_el_control_ignore_el_marcador(self):
        """MUTACIÓN del alcance del control, no de un archivo.

        Si la Ü sale de las clases de letras, el marcador deja de matchear y el script informa
        CERO hallazgos sobre un texto roto: verde con el instrumento apagado.
        """
        self.assertIn("Ü", self.vr.MAYUSCULAS)
        self.assertIn("ü", self.vr.LETRAS)
        texto = "[VERIFICAR ANTIGÜEDAD: cómputo del art. 245]"
        self.assertEqual(self.vr.CUALQUIERA.findall(texto), ["VERIFICAR ANTIGÜEDAD"])

    def test_plano_compara_sin_tildes_ni_caja_ni_espacios_de_mas(self):
        self.assertEqual(self.vr.plano("VACÍO  PROBATORIO"), self.vr.plano("vacio probatorio"))
        self.assertNotEqual(self.vr.plano("VERIFICAR PLAZO"), self.vr.plano("VERIFICAR VIGENCIA"))


class TestCLI(unittest.TestCase):
    def _correr(self, *argumentos):
        return subprocess.run([sys.executable, str(HERRAMIENTA), *argumentos],
                              capture_output=True, text=True, encoding="utf-8", cwd=str(RAIZ))

    def _archivo(self, carpeta, texto):
        ruta = pathlib.Path(carpeta) / "respuesta.md"
        ruta.write_text(texto, encoding="utf-8")
        return str(ruta)

    def test_sin_argumentos_corta_con_dos(self):
        self.assertEqual(self._correr().returncode, 2)

    def test_un_archivo_que_no_existe_corta_con_dos(self):
        self.assertEqual(self._correr("no-existe-jamas.md").returncode, 2)

    def test_una_respuesta_limpia_sale_con_cero(self):
        with tempfile.TemporaryDirectory() as d:
            r = self._correr(self._archivo(d, "[VERIFICAR VIGENCIA: Ley 25.358]\n"))
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_una_respuesta_con_marcador_inventado_sale_con_uno(self):
        with tempfile.TemporaryDirectory() as d:
            r = self._correr(self._archivo(d, "[VERIFICAR ANTIGÜEDAD: art. 245]\n"))
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("DESCONOCIDO", r.stdout)

    def test_los_resultados_de_los_evals_estan_limpios(self):
        """La salida esperada de un eval ensenia la forma correcta: si ahí hay un marcador roto,
        se propaga a cada análisis que se compare contra ella."""
        resultados = sorted(str(p) for p in (RAIZ / "derecho" / "evals").glob("*/resultado.md"))
        self.assertTrue(resultados, "no encontré los resultados de los evals")
        r = self._correr(*resultados)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_vocabulario_imprime_la_lista(self):
        r = self._correr("--vocabulario")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[ALERTA PLAZO FATAL: ...]", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
