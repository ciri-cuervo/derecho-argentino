#!/usr/bin/env python3
"""Tests de la frontera de licencia con la capa 2. Sin dependencias externas.

    python3 herramientas/test_frontera.py
"""
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
KB = RAIZ / "derecho" / "kb"
HERRAMIENTA = RAIZ / "herramientas" / "frontera_kb.py"
REGISTRO = RAIZ / "herramientas" / "kb-procedencia.json"


class TestFronteraKB(unittest.TestCase):
    """`derecho/kb/` es de otro autor: cualquier cambio tiene que ser deliberado.

    La frontera se cruza corrigiendo: el perfil heredado dice algo mal y la tentación es
    arreglarlo donde se lee. El registro de huellas hace visible esa deriva, y obliga a que
    tocar `kb/` sea una decisión y no un descuido.
    """

    def test_el_registro_esta_al_dia(self):
        hecho = subprocess.run([sys.executable, str(HERRAMIENTA)], capture_output=True, text=True)
        self.assertEqual(hecho.returncode, 0,
                         "kb/ cambió sin actualizar el registro:\n" + hecho.stdout)

    def test_el_registro_cubre_todo_kb(self):
        registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
        enDisco = {p.relative_to(KB).as_posix() for p in KB.rglob("*")
                   if p.is_file() and not p.name.startswith(".")}
        self.assertEqual(set(registro["archivos"]), enDisco)
        self.assertTrue(registro["nota"], "el registro no dice por qué quedó en este estado")

    def test_ningun_archivo_de_kb_declara_una_licencia_del_fork(self):
        # Salvo los dos README, que son del titular del fork y lo dicen (ver LICENCIAS.md 2).
        propios = {"README.md", "project/README.md"}
        for p in sorted(KB.rglob("*.md")):
            if p.relative_to(KB).as_posix() in propios:
                continue
            with self.subTest(p.relative_to(KB).as_posix()):
                texto = p.read_text(encoding="utf-8", errors="replace")
                for licencia in ("CC BY-SA", "LICENSE-MIT", "LICENSE-CC-BY-SA"):
                    self.assertNotIn(licencia, texto,
                                     "un archivo de capa 2 no declara licencias del fork")


class TestFronteraPortatil(unittest.TestCase):
    """El guardarraíl tiene que decir la verdad en Windows, Linux y macOS.

    Medido sobre los 109 archivos de `kb/`: con las claves en formato nativo, 106 dejan de
    matchear en Windows; con un checkout CRLF, los 109 cambian de hash sin que cambie una
    letra. Una alarma que suena entera invita a callarla con `--fijar`, y eso acepta a ciegas
    el estado de la capa 2, que es justo lo que este guardarraíl existe para impedir.
    """

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("frontera_kb", HERRAMIENTA)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_el_hash_no_se_mueve_por_el_fin_de_linea(self):
        with tempfile.TemporaryDirectory() as d:
            lf = Path(d) / "lf.md"
            crlf = Path(d) / "crlf.md"
            cuerpo = "# Perfil\n\nArt. 245 LCT: indemnización por antigüedad.\n"
            lf.write_bytes(cuerpo.encode("utf-8"))
            crlf.write_bytes(cuerpo.replace("\n", "\r\n").encode("utf-8"))
            self.assertEqual(self.mod.huella(lf), self.mod.huella(crlf))

    def test_pero_un_cambio_de_contenido_si_lo_mueve(self):
        """MUTACIÓN: si esto pasa, normalizar los saltos se comió un cambio real."""
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.md", Path(d) / "b.md"
            a.write_text("Art. 245 LCT: indemnización por antigüedad.\n", encoding="utf-8")
            b.write_text("Art. 246 LCT: indemnización por antigüedad.\n", encoding="utf-8")
            self.assertNotEqual(self.mod.huella(a), self.mod.huella(b))
            # Y un renglón de más tampoco puede pasar desapercibido.
            c = Path(d) / "c.md"
            c.write_text("Art. 245 LCT: indemnización por antigüedad.\n\nY algo más.\n",
                         encoding="utf-8")
            self.assertNotEqual(self.mod.huella(a), self.mod.huella(c))

    def test_fijar_no_se_come_el_sobre(self):
        """REGRESIÓN: `--fijar` escribía el registro de cero y borraba `_descripcion` y
        `_criterio`, que son lo que explica qué es ese archivo. El test que exige el sobre
        completo vive en otra suite, así que el repo quedaba roto recién después de fijar,
        que es la única vez que nadie mira. Acá se fija contra una copia, no contra el
        registro de verdad."""
        with tempfile.TemporaryDirectory() as d:
            copia = Path(d) / "kb-procedencia.json"
            copia.write_text(REGISTRO.read_text(encoding="utf-8"), encoding="utf-8")
            antes = json.loads(copia.read_text(encoding="utf-8"))
            sobre = {k: v for k, v in antes.items() if k.startswith("_")}
            self.assertTrue(sobre, "el registro de verdad ya perdió el sobre")

            registro_real, argv = self.mod.REGISTRO, sys.argv
            try:
                self.mod.REGISTRO = copia
                sys.argv = ["frontera_kb.py", "--fijar", "--nota", "prueba"]
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(self.mod.main(), 0)
            finally:
                self.mod.REGISTRO, sys.argv = registro_real, argv

            despues = json.loads(copia.read_text(encoding="utf-8"))
            for clave, valor in sobre.items():
                with self.subTest(clave):
                    self.assertEqual(despues.get(clave), valor, f"--fijar se comió `{clave}`")
            self.assertEqual(despues["nota"], "prueba")
            self.assertTrue(despues["archivos"])

    def test_las_claves_del_registro_son_posix(self):
        """Una clave con separador nativo hace que el registro no matchee en Windows."""
        registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
        for clave in registro["archivos"]:
            with self.subTest(clave):
                self.assertNotIn("\\", clave)

    def test_el_repo_declara_normalizacion_de_fin_de_linea(self):
        """Sin .gitattributes, un clone en Windows puede traer CRLF y el .txt de fuentes/
        deja de ser el mismo archivo en las tres plataformas."""
        atributos = RAIZ / ".gitattributes"
        self.assertTrue(atributos.is_file(), "falta .gitattributes en la raíz")
        self.assertIn("eol=lf", atributos.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
