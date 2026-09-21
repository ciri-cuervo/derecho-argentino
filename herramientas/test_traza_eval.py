#!/usr/bin/env python3
"""Tests del control de contaminación de una corrida de evals. Sin dependencias externas.

    python3 herramientas/test_traza_eval.py
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AQUI = Path(__file__).resolve().parent
HERRAMIENTA = AQUI / "traza_eval.py"


def _modulo():
    spec = importlib.util.spec_from_file_location("traza_eval", HERRAMIENTA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _ConCorrida(unittest.TestCase):
    """Arma una corrida de mentira: el agregado, y las trazas que él nombra."""

    CASO = "laboral-despido-tramos-reforma-pba"

    def setUp(self):
        self.mod = _modulo()
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)

    def _traza(self, nombre: str, llamadas: list) -> Path:
        f = self.d / nombre
        f.write_text("\n".join(json.dumps(
            {"message": {"content": [{"type": "tool_use", "name": h, "input": e}]}})
            for h, e in llamadas) + "\n", encoding="utf-8")
        return f

    def _corrida(self, trazas: list) -> Path:
        agregado = self.d / "aggregate-result.json"
        agregado.write_text(json.dumps({"cases": [{
            "name": self.CASO,
            "arms": {"with": [{"tracePath": str(t)} for t in trazas]}}]}), encoding="utf-8")
        return agregado

    def _revisar(self, llamadas):
        return self.mod.revisar(self._corrida([self._traza("t.jsonl", llamadas)]))


class TestLoQueRompeYLoQueAvisa(_ConCorrida):
    """La clave de respuestas vive al lado del caso y el agente evaluado corre contra el
    repositorio vivo: `graders/` dice textualmente qué puntúa el juez y `resultado.md` es el
    caso resuelto. Leerlos no está impedido por nada, y un puntaje sacado así no se distingue
    de uno bueno.

    La frontera no es «cualquier ruta de evals/», porque `modelos.md` 23.8 manda al runtime a
    los `resultado.md` de OTROS casos como ejemplos trabajados: eso es comportamiento declarado
    y se avisa.

    MUTACIÓN que lo comprueba: cambiar la clasificación de `graders/` a «avisa» deja
    `test_leer_los_graders_del_caso_que_se_corre_rompe` en rojo.
    """

    def test_leer_los_graders_del_caso_que_se_corre_rompe(self):
        rompen, avisan, _ = self._revisar([
            ("Read", {"file_path": f"/x/derecho/evals/{self.CASO}/graders/base-del-245.md"})])
        self.assertEqual(len(rompen), 1, rompen)
        self.assertIn("graders/base-del-245.md", rompen[0])
        self.assertEqual(avisan, [])

    def test_leer_la_rubrica_de_cualquier_caso_rompe(self):
        rompen, _, _ = self._revisar([
            ("Read", {"file_path": "/x/derecho/evals/tributario-pba/rubrica.md"})])
        self.assertEqual(len(rompen), 1, rompen)

    def test_leer_el_resultado_del_propio_caso_rompe(self):
        rompen, _, _ = self._revisar([
            ("Read", {"file_path": f"/x/derecho/evals/{self.CASO}/resultado.md"})])
        self.assertEqual(len(rompen), 1, rompen)

    def test_leer_el_resultado_de_otro_caso_avisa_y_no_rompe(self):
        rompen, avisan, _ = self._revisar([
            ("Read", {"file_path": "/x/derecho/evals/familia-alimentos/resultado.md"})])
        self.assertEqual(rompen, [])
        self.assertEqual(len(avisan), 1, avisan)

    def test_la_salida_de_la_propia_corrida_no_cuenta(self):
        """`evals/results/` es lo que escribe el harness, no material del caso."""
        rompen, avisan, _ = self._revisar([
            ("Read", {"file_path": "/x/derecho/evals/results/2026-01-01/aggregate-result.json"})])
        self.assertEqual((rompen, avisan), ([], []))

    def test_instrumento_encendido(self):
        """Sin esto, «traza limpia» también sería «no supe leer la traza»."""
        llamadas = [("Read", {"file_path": "/x/derecho/skills/derecho-argentino/"
                                           "references/laboral.md"})]
        traza = self._traza("t.jsonl", llamadas)
        self.assertEqual(len(list(self.mod.entradas(traza))), 1,
                         "el parser no encontró la llamada: mediría cero sobre cualquier traza")
        self.assertEqual(self.mod.revisar(self._corrida([traza])), ([], [], []))


class TestSePlantaSinTraza(_ConCorrida):
    """El sandbox de `claude plugin eval` se borra y con él la traza, así que la pregunta
    «¿estuvo limpia?» tiene fecha de vencimiento. Decir que sí porque no se encontró nada sería
    dar verde con el instrumento apagado: se planta con rc=2 y se dice que no se midió.

    MUTACIÓN que lo comprueba: devolver 0 cuando la traza falta deja este test en rojo.
    """

    def test_una_traza_que_ya_no_existe_se_reporta_y_no_se_da_por_limpia(self):
        agregado = self._corrida([self.d / "se-borro.jsonl"])
        rompen, avisan, sin_traza = self.mod.revisar(agregado)
        self.assertEqual((rompen, avisan), ([], []))
        self.assertEqual(len(sin_traza), 1)

    def test_el_codigo_de_salida_distingue_los_tres_estados(self):
        casos = {
            2: [self.d / "se-borro.jsonl"],
            1: [self._traza("sucia.jsonl", [
                ("Read", {"file_path": f"/x/evals/{self.CASO}/rubrica.md"})])],
            0: [self._traza("limpia.jsonl", [("Read", {"file_path": "/x/references/laboral.md"})])],
        }
        for esperado, trazas in casos.items():
            with self.subTest(rc=esperado):
                agregado = self._corrida(trazas)
                hecho = subprocess.run(
                    [sys.executable, str(HERRAMIENTA), "--resultados", str(agregado.parent)],
                    capture_output=True, text=True)
                self.assertEqual(hecho.returncode, esperado, hecho.stdout)


if __name__ == "__main__":
    unittest.main()
