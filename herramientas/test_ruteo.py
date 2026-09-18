#!/usr/bin/env python3
"""Tests de `ruteo.py`, el medidor del mapa de módulos.

Ancla en `Path(__file__)`, no en `_raiz.raiz_repo()`: esa función consulta primero
`~/.config/derecho-argentino/config.json`, así que quien tenga la ruta fijada y trabaje en
un clon distinto correría los tests contra OTRO repositorio y los vería en verde.

Lo que se fija: que el propio medidor no se apague. Un medidor de alcanzabilidad que deja de
encontrar la tabla de ruteo, o que empieza a contar como alcanzado lo que no lo está, informa
verde sobre un repositorio roto, y esa es la peor forma de alarma: la que no suena.
"""

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "ruteo.py"


def cargar():
    spec = importlib.util.spec_from_file_location("ruteo", HERRAMIENTA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestElMapa(unittest.TestCase):
    def setUp(self):
        self.r = cargar()

    def test_hay_modulos_y_hay_tabla_de_ruteo(self):
        """Instrumento encendido: sin esto, «cero inalcanzables» también es cero módulos."""
        self.assertGreater(len(self.r.modulos()), 20)
        self.assertIn("## 16 ·", self.r.seccion_de_ruteo())

    def test_ningun_modulo_queda_fuera_del_ruteo(self):
        """Un módulo que el ruteo no nombra no falla: se vuelve invisible y el análisis lo
        suple con lo que el modelo ya cree saber, que es de donde salen las citas inventadas."""
        dist = self.r.distancias()
        comandos = self.r.desde_comandos()
        huerfanos = sorted(m for m in self.r.modulos()
                           if m not in dist and m not in comandos)
        self.assertEqual(huerfanos, [],
                         "estos módulos existen y ningún camino de ruteo los nombra: "
                         + ", ".join(huerfanos))

    def test_ningun_modulo_queda_a_distancia_tres(self):
        """A distancia tres un módulo existe y nadie lo abre: para llegar hay que haber leído
        antes otros dos que no venían al caso."""
        dist = self.r.distancias()
        lejos = sorted(f"{m} ({d})" for m, d in dist.items() if d >= 3)
        self.assertEqual(lejos, [], "modulos demasiado lejos del router: " + ", ".join(lejos))

    def test_nombrados_solo_devuelve_modulos_que_existen(self):
        universo = {"laboral.md", "civil.md"}
        texto = "ver `references/laboral.md` y `inventado.md` y references/civil.md"
        self.assertEqual(self.r.nombrados(texto, universo), {"laboral.md", "civil.md"})


class TestLasConsultas(unittest.TestCase):
    def setUp(self):
        self.r = cargar()
        self.casos, self.encabezados = self.r.consultas()

    def test_hay_consultas_y_se_parsean(self):
        # Y que haya módulos: sin esto, `modulos()` devolviendo vacío deja pasar en verde los
        # dos tests de abajo, porque las diferencias de conjuntos quedan vacías. El guard vivía
        # en OTRA clase, que es lo mismo que no tenerlo.
        self.assertGreater(len(self.r.modulos()), 20, "sin modulos no se compara nada")
        self.assertGreater(len(self.casos), 10)
        # Toda consulta escrita tiene que poder leerse entera. Una con el separador roto
        # desaparecía sin bajar de este umbral y sin que nada avisara.
        self.assertEqual(self.encabezados, len(self.casos),
                         "hay consultas que el parser no pudo leer enteras")
        identificadores = [c[0] for c in self.casos]
        self.assertEqual(len(identificadores), len(set(identificadores)),
                         "hay identificadores de consulta repetidos")

    def test_todo_modulo_esperado_existe(self):
        universo = self.r.modulos()
        rotas = [f"{i} espera {m}" for i, _, esperados in self.casos
                 for m in esperados if m not in universo]
        self.assertEqual(rotas, [], "; ".join(rotas))

    def test_cada_modulo_lo_ejercita_alguna_consulta(self):
        """Es el guardarraíl que se rompe solo cuando entra un módulo nuevo: si nadie escribe
        la consulta que lo abre, el módulo entra al repositorio sin que nada mida su ruteo."""
        ejercitados = {m for _, _, esperados in self.casos for m in esperados}
        sin_consulta = sorted(self.r.modulos() - ejercitados)
        self.assertEqual(sin_consulta, [],
                         "estos modulos no los ejercita ninguna consulta de ruteo: "
                         + ", ".join(sin_consulta))


class TestCLI(unittest.TestCase):
    def _correr(self, *argumentos):
        return subprocess.run([sys.executable, str(HERRAMIENTA), *argumentos],
                              capture_output=True, text=True, encoding="utf-8", cwd=str(RAIZ))

    def test_el_repo_de_hoy_pasa(self):
        r = self._correr()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_todo_lista_los_modulos(self):
        r = self._correr("--todo")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("laboral.md", r.stdout)

    def test_una_consulta_que_espera_un_modulo_inexistente_se_reclama(self):
        r = cargar()
        with tempfile.TemporaryDirectory() as d:
            falso = pathlib.Path(d) / "consultas.md"
            falso.write_text("### R99 · consulta\n\nesperado: no-existe.md\n", encoding="utf-8")
            casos, encabezados = r.consultas(falso)
            self.assertEqual(casos, [("R99", "consulta", ["no-existe.md"])])
            self.assertEqual(encabezados, 1)
            self.assertNotIn("no-existe.md", r.modulos())


if __name__ == "__main__":
    unittest.main(verbosity=2)
