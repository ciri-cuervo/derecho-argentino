#!/usr/bin/env python3
"""Tests del detector de ramas que entraron como sección y no se pueden alcanzar.

    python3 herramientas/test_ramas.py

Lo que sostiene no es el número de ramas —crece con el trabajo— sino las tres decisiones que
hacen que la lista sirva: qué cuenta como candidato, dónde se busca el disparador, y que una
rama declarada sin disparador **falle** en vez de pasar inadvertida.
"""
import importlib.util
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "ramas_sin_disparador.py"


def cargar():
    spec = importlib.util.spec_from_file_location("ramas_sin_disparador", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class TestLaClaveDeUnaSeccion(unittest.TestCase):
    """El ordinal es parte del número, no del título.

    MUTACIÓN VIVIDA: `clave()` cortaba en el primer espacio y devolvía `17.11.5` para `bis`,
    `ter`, `quater` y `quinquies`. Corrida el 17/09/2026 sobre el árbol real: las cuatro
    secciones de servicios de red colapsaban en una sola clave, así que **un veredicto tapaba a
    las otras tres** y tres ramas quedaban sin vigilar sin que nada lo dijera.
    """

    def setUp(self):
        self.h = cargar()

    def test_el_ordinal_entra_en_la_clave(self):
        c = self.h.clave
        self.assertEqual(c("consumidor.md", "17.11.5 bis Gas natural — Ley 24.076"),
                         "consumidor.md :: 17.11.5 bis")
        self.assertEqual(c("consumidor.md", "17.11.5 ter Transporte aéreo"),
                         "consumidor.md :: 17.11.5 ter")
        self.assertNotEqual(c("consumidor.md", "17.11.5 bis X"),
                            c("consumidor.md", "17.11.5 ter Y"))

    def test_una_seccion_sin_ordinal_conserva_su_numero(self):
        self.assertEqual(self.h.clave("penal.md", "24.9.6 Prevención del lavado"),
                         "penal.md :: 24.9.6")


class TestDondeSeBuscaElDisparador(unittest.TestCase):
    """Las dos capas: la tabla de ruteo decide qué módulo abrir, el description activa la skill.

    Buscar en una sola dejaría pasar la mitad de los casos, y buscar en todo el SKILL.md haría
    que una mención de paso en cualquier sección contara como disparador.
    """

    def setUp(self):
        self.h = cargar()

    def test_trae_la_tabla_de_ruteo_y_el_description(self):
        t = self.h.disparadores().lower()
        self.assertIn("references/laboral.md", t, "falta la tabla de ruteo de la sección 16")
        self.assertIn("análisis, redacción y revisión jurídica", t, "falta el description")

    def test_no_trae_el_resto_del_skill(self):
        """Si entrara el SKILL.md entero, cualquier mención de paso apagaría la alarma."""
        t = self.h.disparadores()
        self.assertNotIn("no se importan", t, "se coló prosa de otra sección del SKILL.md")


class TestElArbolReal(unittest.TestCase):
    def setUp(self):
        self.h = cargar()

    def test_toda_rama_declarada_tiene_su_disparador(self):
        sin_disparador, _sin_veredicto, _ok = self.h.revisar()
        self.assertEqual([k for k, _ in sin_disparador], [],
                         "hay ramas escritas que ningún disparador alcanza")

    def test_todo_candidato_tiene_veredicto(self):
        """Una sección nueva sin veredicto es lo que el detector existe para mostrar."""
        _sd, sin_veredicto, _ok = self.h.revisar()
        self.assertEqual(sin_veredicto, [],
                         "hay secciones candidatas sin veredicto en ramas-revisadas.json")

    def test_instrumento_encendido(self):
        """Sin esto, «cero sin disparador» también sería cero ramas declaradas."""
        _sd, _sv, alcanzadas = self.h.revisar()
        self.assertGreater(len(alcanzadas), 10, "no leyó el archivo de veredictos")
        self.assertGreater(len(self.h.candidatos()), 10, "no detectó ninguna sección")

    def test_una_rama_declarada_sin_disparador_falla(self):
        """LA MUTACIÓN, hecha en memoria para no tocar el árbol.

        Se le inventa a una rama un disparador que no existe en ninguna de las dos capas. Si
        `revisar()` la diera por alcanzada, el control entero sería decorativo: reportaría cero
        porque no mira, no porque esté todo bien.
        """
        original = self.h.disparadores
        self.h.disparadores = lambda: original() + ""   # sin cambios: el disparador falso no está
        try:
            import json
            sobre, veredictos = __import__("_veredictos").cargar(self.h.VEREDICTOS, "ramas", vacio={})
            clave = next(k for k, v in veredictos.items() if v.get("veredicto") == "rama")
            veredictos[clave] = dict(veredictos[clave], disparadores=["zzz-materia-inexistente"])
            leer = self.h._veredictos.cargar
            self.h._veredictos.cargar = lambda *a, **k: (sobre, veredictos)
            try:
                sin_disparador, _sv, _ok = self.h.revisar()
                self.assertIn(clave, [c for c, _ in sin_disparador],
                              "una rama con un disparador inexistente pasó como alcanzable")
            finally:
                self.h._veredictos.cargar = leer
        finally:
            self.h.disparadores = original


if __name__ == "__main__":
    unittest.main(verbosity=2)
