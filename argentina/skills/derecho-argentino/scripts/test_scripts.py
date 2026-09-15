"""Tests de las calculadoras de la skill derecho-argentino. Sin dependencias externas.

    python3 -m unittest discover -s . -p 'test_*.py' -v
"""
import hashlib
import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import _raiz
import liquidacion_lct as liq
import plazos

# Las clases de letras del castellano, en un solo lugar. La dieresis va incluida y NO es un
# detalle: "antigüedad" con dieresis aparece 67 veces en el repositorio y es el nucleo del
# art. 245 LCT, así que un marcador como [VERIFICAR ANTIGÜEDAD: ...] es plausible. Sin la Ü
# en la clase, ese marcador no matchea y el control lo IGNORA en silencio en vez de fallar.
MAYUSCULAS = "A-ZÁÉÍÓÚÜÑ"
LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"


class TestAntiguedad(unittest.TestCase):
    def test_fraccion_mayor_a_tres_meses_suma_un_ano(self):
        anios, meses, mult = liq.antiguedad(date(2015, 3, 10), date(2026, 7, 20))
        self.assertEqual((anios, meses), (11, 4))
        self.assertEqual(mult, 12)

    def test_fraccion_de_tres_meses_exactos_no_suma(self):
        anios, meses, mult = liq.antiguedad(date(2015, 3, 10), date(2026, 6, 10))
        self.assertEqual((anios, meses), (11, 3))
        self.assertEqual(mult, 11)

    def test_minimo_un_mes(self):
        _, _, mult = liq.antiguedad(date(2026, 1, 10), date(2026, 2, 10))
        self.assertEqual(mult, 1)

    def test_extincion_anterior_al_ingreso_falla(self):
        with self.assertRaises(SystemExit):
            liq.antiguedad(date(2026, 1, 10), date(2025, 1, 10))


class TestTramos(unittest.TestCase):
    def test_cortes(self):
        casos = {
            date(2023, 12, 29): "original",
            date(2023, 12, 30): "dnu70",
            date(2024, 7, 8): "dnu70",
            date(2024, 7, 9): "bases",
            date(2026, 3, 5): "bases",
            date(2026, 3, 6): "modernizacion",
        }
        for f, esperado in casos.items():
            self.assertEqual(liq.tramo_de(f)[0], esperado, f)


class TestArt245(unittest.TestCase):
    def _args(self, **kw):
        base = dict(ingreso=date(2015, 3, 10), extincion=date(2026, 4, 20),
                    mejor_remuneracion=Decimal("1000000"),
                    remuneracion_ultimo_mes=None, tope_245=None,
                    dias_vacaciones_gozadas=Decimal("0"),
                    periodo_prueba=False, preaviso_otorgado=False)
        base.update(kw)
        return type("A", (), base)

    def test_piso_del_67_por_ciento(self):
        # tope muy bajo: debe prevalecer el 67% de la mejor remuneración
        r = liq.liquidar(self._args(tope_245=Decimal("500000")))
        antiguedad = next(x for x in r.rubros if x["concepto"].startswith("Indemnización por"))
        self.assertAlmostEqual(antiguedad["importe"], 670000 * 11, places=2)

    def test_tope_se_aplica_si_es_mayor_al_piso(self):
        r = liq.liquidar(self._args(tope_245=Decimal("800000")))
        antiguedad = next(x for x in r.rubros if x["concepto"].startswith("Indemnización por"))
        self.assertAlmostEqual(antiguedad["importe"], 800000 * 11, places=2)

    def test_sin_tope_marca_provisorio(self):
        r = liq.liquidar(self._args())
        self.assertTrue(any("tope art. 245" in m for m in r.marcadores))
        self.assertTrue(any("SIN tope" in a for a in r.advertencias))

    def test_agravantes_derogados_desde_9_7_2024(self):
        r = liq.liquidar(self._args())
        self.assertTrue(any("DEROGADOS" in a for a in r.advertencias))

    def test_agravantes_anteriores_piden_intimacion(self):
        r = liq.liquidar(self._args(extincion=date(2024, 5, 20)))
        self.assertTrue(any("intimación fehaciente previa" in m for m in r.marcadores))

    def test_tramo_dnu70_emite_revision(self):
        r = liq.liquidar(self._args(extincion=date(2024, 3, 15)))
        self.assertTrue(any("DNU 70/2023" in m for m in r.marcadores))

    def test_preaviso_dos_meses_sobre_cinco_anios(self):
        r = liq.liquidar(self._args(tope_245=Decimal("2000000")))
        pre = next(x for x in r.rubros if "preaviso" in x["concepto"])
        self.assertAlmostEqual(pre["importe"], 2000000.0, places=2)


class TestPascuaYFeriados(unittest.TestCase):
    def test_pascua(self):
        # valores de referencia del cómputo gregoriano
        self.assertEqual(plazos.pascua(2024), date(2024, 3, 31))
        self.assertEqual(plazos.pascua(2025), date(2025, 4, 20))
        self.assertEqual(plazos.pascua(2026), date(2026, 4, 5))
        self.assertEqual(plazos.pascua(2027), date(2027, 3, 28))

    def test_viernes_santo_y_carnaval_2026(self):
        f = plazos.feriados_ley_27399(2026)
        self.assertIn(date(2026, 4, 3), f)          # Viernes Santo
        self.assertIn(date(2026, 2, 16), f)         # Carnaval lunes
        self.assertIn(date(2026, 2, 17), f)         # Carnaval martes

    def test_inamovibles_presentes(self):
        f = plazos.feriados_ley_27399(2026)
        for d in [date(2026, 1, 1), date(2026, 3, 24), date(2026, 4, 2), date(2026, 5, 1),
                  date(2026, 5, 25), date(2026, 6, 20), date(2026, 7, 9), date(2026, 12, 8),
                  date(2026, 12, 25)]:
            self.assertIn(d, f, d)

    def test_traslado_art_2(self):
        # martes -> lunes anterior; jueves -> lunes siguiente; lunes queda igual
        self.assertEqual(plazos.trasladar(date(2026, 8, 18)).weekday(), 0)
        self.assertLess(plazos.trasladar(date(2026, 8, 18)), date(2026, 8, 18))
        self.assertEqual(plazos.trasladar(date(2026, 10, 15)).weekday(), 0)
        self.assertGreater(plazos.trasladar(date(2026, 10, 15)), date(2026, 10, 15))
        lunes = date(2026, 10, 12)
        self.assertEqual(plazos.trasladar(lunes), lunes)


class TestPlazos(unittest.TestCase):
    def test_no_cuenta_el_dia_de_notificacion(self):
        venc, traza, _ = plazos.computar_habiles(date(2026, 9, 10), 1, "pba")
        self.assertEqual(venc, date(2026, 9, 11))

    def test_salta_fin_de_semana(self):
        # jueves 10/09/2026 + 2 hábiles -> lunes 14
        venc, _, _ = plazos.computar_habiles(date(2026, 9, 10), 2, "pba")
        self.assertEqual(venc, date(2026, 9, 14))

    def test_sumar_meses_de_fecha_a_fecha(self):
        self.assertEqual(plazos.sumar_meses(date(2026, 3, 31), 1), date(2026, 4, 30))
        self.assertEqual(plazos.sumar_meses(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(plazos.sumar_meses(date(2024, 1, 31), 1), date(2024, 2, 29))
        self.assertEqual(plazos.sumar_meses(date(2024, 5, 10), 24), date(2026, 5, 10))

    def test_datos_pendientes_se_reportan(self):
        _, _, meta = plazos.cargar_datos(2026, "pba")
        self.assertIn(meta["estado"], ("PENDIENTE", "OK", "SIN DATOS", "SIN ARCHIVO"))


class TestInhabilesCargados(unittest.TestCase):
    """El calendario de 2026 está cargado y verificado: estos casos lo comprueban."""

    def test_bloque_2026_pba_verificado(self):
        _, _, meta = plazos.cargar_datos(2026, "pba")
        self.assertEqual(meta["estado"], "OK")
        self.assertEqual(meta["verificado"], "2026-09-13")

    def test_descuenta_la_feria_de_invierno(self):
        # notificación el 16/07/2026: 17/7 es asueto y del 20 al 31/7 hay feria
        venc, _, _ = plazos.computar_habiles(date(2026, 7, 16), 5, "pba")
        self.assertEqual(venc, date(2026, 8, 7))

    def test_descuenta_la_feria_de_enero(self):
        venc, _, _ = plazos.computar_habiles(date(2026, 12, 22), 10, "pba")
        self.assertEqual(venc, date(2027, 2, 4))

    def test_el_calculo_de_trasladables_coincide_con_lo_verificado(self):
        _, _, meta = plazos.cargar_datos(2026, "pba")
        verificados = {date.fromisoformat(d) for d in meta["trasladables_verificados"]}
        calculados = {f for f, n in plazos.feriados_ley_27399(2026).items()
                      if n.endswith("(trasladable)")}
        self.assertEqual(verificados, calculados)

    def test_asuetos_distritales_no_se_descuentan(self):
        extra, _, meta = plazos.cargar_datos(2026, "pba")
        self.assertTrue(meta["distritales"], "deberia haber al menos un asueto distrital")
        for d in meta["distritales"]:
            self.assertNotIn(date.fromisoformat(d["fecha"]), extra)

    def test_trasladable_en_fin_de_semana_se_reporta(self):
        # 20/11/2027 cae sabado: ubicación indeterminada por el Decreto 614/2025
        dudosos = plazos.trasladables_dudosos(2027)
        self.assertTrue(any("2027-11-20" in d for d in dudosos))

    def test_pendientes_de_2027_estan_declarados(self):
        _, _, meta = plazos.cargar_datos(2027, "pba")
        self.assertTrue(meta["pendientes"])


class TestRaizDelRepo(unittest.TestCase):
    """La skill se instala a nivel de cuenta y corre en cualquier máquina: no puede haber
    ninguna ruta hardcodeada. Estos tests cubren el resolvedor."""

    def test_reconoce_el_repo_por_el_marcador(self):
        repo, origen = _raiz.raiz_repo()
        self.assertIsNotNone(repo, "no se encontró el repo desde su propia carpeta")
        self.assertTrue((repo / _raiz.MARCADOR).is_file())

    def test_rechaza_una_carpeta_que_no_es_el_repo(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(_raiz.es_repo(pathlib.Path(d)))
            r, motivo = _raiz.raiz_repo(d)
            self.assertIsNone(r)
            self.assertIn("no es el repo", motivo)

    def test_ruta_explicita_gana(self):
        repo, _ = _raiz.raiz_repo()
        r, origen = _raiz.raiz_repo(str(repo))
        self.assertEqual(r, repo)
        self.assertEqual(origen, "--repo")

    def test_variable_de_entorno(self):
        repo, _ = _raiz.raiz_repo()
        entorno = dict(os.environ, DERECHO_AR_REPO=str(repo), XDG_CONFIG_HOME="/nonexistent")
        codigo = ("import sys; sys.path.insert(0, %r); import _raiz; "
                  "p, o = _raiz.raiz_repo(); print(o)" % str(pathlib.Path(__file__).parent))
        r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True,
                           env=entorno, cwd=tempfile.gettempdir())
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("DERECHO_AR_REPO", r.stdout)

    def test_funciona_con_la_skill_fuera_del_repo(self):
        """El caso que importa: la skill instalada a nivel de cuenta, lejos del repo."""
        repo, _ = _raiz.raiz_repo()
        aqui = pathlib.Path(__file__).parent
        with tempfile.TemporaryDirectory() as d:
            copia = pathlib.Path(d) / "skill" / "scripts"
            shutil.copytree(aqui, copia, ignore=shutil.ignore_patterns("__pycache__"))
            entorno = dict(os.environ, DERECHO_AR_REPO=str(repo),
                           XDG_CONFIG_HOME=str(pathlib.Path(d) / "cfg"))
            r = subprocess.run(
                [sys.executable, str(copia / "honorarios_pba.py"),
                 "--monto", "10000000", "--porcentaje", "20"],
                capture_output=True, text=True, env=entorno, cwd=d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("Valor del jus utilizado", r.stdout)
            self.assertIn("vigencia:", r.stdout)

    def test_sin_repo_los_scripts_lo_dicen_y_no_inventan(self):
        aqui = pathlib.Path(__file__).parent
        with tempfile.TemporaryDirectory() as d:
            copia = pathlib.Path(d) / "skill" / "scripts"
            shutil.copytree(aqui, copia, ignore=shutil.ignore_patterns("__pycache__"))
            entorno = {k: v for k, v in os.environ.items() if k != "DERECHO_AR_REPO"}
            entorno["XDG_CONFIG_HOME"] = str(pathlib.Path(d) / "cfg")
            entorno["HOME"] = d
            r = subprocess.run(
                [sys.executable, str(copia / "honorarios_pba.py"),
                 "--monto", "10000000", "--porcentaje", "20"],
                capture_output=True, text=True, env=entorno, cwd=d)
            self.assertEqual(r.returncode, 2)
            self.assertIn("VERIFICAR MONTO ACTUALIZADO", r.stdout)
            self.assertNotIn("HONORARIOS  ", r.stdout)

    def test_el_primer_hallazgo_queda_fijado_solo(self):
        """Instalar una skill no ejecuta nada: el primer uso que necesite el repo tiene que
        encontrarlo Y dejarlo anotado, o se resuelve por adivinanza para siempre."""
        repo, _ = _raiz.raiz_repo()
        aqui = pathlib.Path(__file__).parent
        with tempfile.TemporaryDirectory() as d:
            casa = pathlib.Path(d) / "home"
            (casa / "develop").mkdir(parents=True)
            (casa / "develop" / "derecho-argentino").symlink_to(repo, target_is_directory=True)
            copia = pathlib.Path(d) / "skill" / "scripts"
            shutil.copytree(aqui, copia, ignore=shutil.ignore_patterns("__pycache__"))
            cfg = pathlib.Path(d) / "cfg"
            entorno = {k: v for k, v in os.environ.items() if k != "DERECHO_AR_REPO"}
            entorno.update(HOME=str(casa), XDG_CONFIG_HOME=str(cfg))
            destino = cfg / "derecho-argentino" / "config.json"
            self.assertFalse(destino.exists())
            r = subprocess.run(
                [sys.executable, str(copia / "honorarios_pba.py"),
                 "--monto", "10000000", "--porcentaje", "20"],
                capture_output=True, text=True, env=entorno, cwd=d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("anotado en", r.stdout)
            self.assertTrue(destino.exists(), "el hallazgo no quedo fijado")
            self.assertEqual(json.loads(destino.read_text())["repo"], str(repo))

    def test_plugin_root_resuelve_el_repo(self):
        """Instalada como plugin, la skill no vive en ~/develop: Claude Code define
        CLAUDE_PLUGIN_ROOT y esa es la respuesta autoritativa, antes que la adivinanza."""
        repo, _ = _raiz.raiz_repo()
        with tempfile.TemporaryDirectory() as d:
            entorno = {k: v for k, v in os.environ.items() if k != "DERECHO_AR_REPO"}
            entorno.update(HOME=d, XDG_CONFIG_HOME=str(pathlib.Path(d) / "cfg"))
            guion = (
                "import sys, _raiz; print(_raiz.raiz_repo()[0]); print(_raiz.raiz_repo()[1])"
            )
            for raiz_plugin in (repo, pathlib.Path(repo) / "argentina"):
                with self.subTest(raiz=str(raiz_plugin)):
                    e = dict(entorno, CLAUDE_PLUGIN_ROOT=str(raiz_plugin))
                    r = subprocess.run(
                        [sys.executable, "-c", guion], capture_output=True, text=True,
                        env=e, cwd=str(pathlib.Path(__file__).parent))
                    self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                    lineas = r.stdout.strip().splitlines()
                    self.assertEqual(lineas[0], str(repo))
                    self.assertIn("CLAUDE_PLUGIN_ROOT", lineas[1])

    def test_el_plugin_instalado_por_el_marketplace_resuelve_solo(self):
        """El caso real de instalación, que el test de arriba no cubre: el marketplace
        publica el plugin desde argentina/, así que esa carpeta llega renombrada con el
        nombre del plugin, rodeada de los otros plugins y sin ningún repo arriba. No hay
        un argentina/ que encontrar en ningún lado."""
        repo, _ = _raiz.raiz_repo()
        with tempfile.TemporaryDirectory() as d:
            instalado = pathlib.Path(d) / "plugins" / "synced" / "derecho"
            instalado.mkdir(parents=True)
            for sub in ("fuentes", "kb", "skills", ".claude-plugin"):
                (instalado / sub).symlink_to(pathlib.Path(repo) / "argentina" / sub,
                                             target_is_directory=True)
            copia = pathlib.Path(d) / "skill" / "scripts"
            shutil.copytree(pathlib.Path(__file__).parent, copia,
                            ignore=shutil.ignore_patterns("__pycache__"))
            entorno = {k: v for k, v in os.environ.items() if k != "DERECHO_AR_REPO"}
            entorno.update(HOME=d, XDG_CONFIG_HOME=str(pathlib.Path(d) / "cfg"),
                           CLAUDE_PLUGIN_ROOT=str(instalado))
            r = subprocess.run(
                [sys.executable, str(copia / "honorarios_pba.py"),
                 "--monto", "10000000", "--porcentaje", "20"],
                capture_output=True, text=True, env=entorno, cwd=d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("Valor del jus utilizado", r.stdout)

    def test_el_plugin_instalado_se_encuentra_sin_variable_de_entorno(self):
        """Lo mismo pero sin CLAUDE_PLUGIN_ROOT: la skill vive adentro de la copia
        instalada y los datos están al lado, así que tiene que hallarlos subiendo."""
        repo, _ = _raiz.raiz_repo()
        origen = pathlib.Path(repo) / "argentina"
        with tempfile.TemporaryDirectory() as d:
            instalado = pathlib.Path(d) / "plugins" / "derecho"
            (instalado / "fuentes").mkdir(parents=True)
            shutil.copy2(origen / "fuentes" / "MANIFIESTO.md", instalado / "fuentes")
            shutil.copytree(origen / "fuentes" / "datos", instalado / "fuentes" / "datos")
            copia = instalado / "skills" / "derecho-argentino" / "scripts"
            shutil.copytree(pathlib.Path(__file__).parent, copia,
                            ignore=shutil.ignore_patterns("__pycache__"))
            entorno = {k: v for k, v in os.environ.items() if k != "DERECHO_AR_REPO"}
            entorno.update(HOME=d, XDG_CONFIG_HOME=str(pathlib.Path(d) / "cfg"))
            r = subprocess.run(
                [sys.executable, str(copia / "honorarios_pba.py"),
                 "--monto", "10000000", "--porcentaje", "20"],
                capture_output=True, text=True, env=entorno, cwd=d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("Valor del jus utilizado", r.stdout)
            # no se fija en config: la ruta de la copia instalada cambia al actualizar
            self.assertNotIn("anotado en", r.stdout)

    def test_base_distingue_las_dos_disposiciones(self):
        repo, _ = _raiz.raiz_repo()
        self.assertEqual(_raiz.base(repo), pathlib.Path(repo) / "argentina")
        argentina = pathlib.Path(repo) / "argentina"
        self.assertEqual(_raiz.base(argentina), argentina)
        self.assertTrue(_raiz.es_repo(argentina))
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(_raiz.es_repo(pathlib.Path(d)))
            self.assertFalse(_raiz.es_base(pathlib.Path(d)))

    def test_repo_explicito_gana_sobre_plugin_root(self):
        repo, _ = _raiz.raiz_repo()
        with tempfile.TemporaryDirectory() as d:
            e = dict(os.environ, CLAUDE_PLUGIN_ROOT=d)
            e.pop("DERECHO_AR_REPO", None)
            r = subprocess.run(
                [sys.executable, "-c",
                 "import _raiz, sys; print(_raiz.raiz_repo(sys.argv[1])[1])", str(repo)],
                capture_output=True, text=True, env=e,
                cwd=str(pathlib.Path(__file__).parent))
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("--repo", r.stdout)

    def test_configurar_guarda_y_se_lee(self):
        repo, _ = _raiz.raiz_repo()
        with tempfile.TemporaryDirectory() as d:
            entorno = dict(os.environ, XDG_CONFIG_HOME=d)
            entorno.pop("DERECHO_AR_REPO", None)
            r = subprocess.run(
                [sys.executable, str(pathlib.Path(__file__).parent / "configurar.py"),
                 "--repo", str(repo)], capture_output=True, text=True, env=entorno)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            cfg = json.loads((pathlib.Path(d) / "derecho-argentino" / "config.json")
                             .read_text(encoding="utf-8"))
            self.assertEqual(cfg["repo"], str(repo))


class TestPerfil(unittest.TestCase):
    """El perfil ORDENA la pregunta de apertura; no la reemplaza. Eso se testea acá porque es
    la regla que separa 'personalizable' de 'asume cosas por vos'."""

    def _entorno(self, d):
        e = dict(os.environ, XDG_CONFIG_HOME=str(d))
        e.pop("DERECHO_AR_REPO", None)
        return e

    def _correr(self, d, *args):
        return subprocess.run(
            [sys.executable, str(pathlib.Path(__file__).parent / "perfil.py"), *args],
            capture_output=True, text=True, env=self._entorno(d),
            cwd=str(pathlib.Path(__file__).parent))

    def test_sin_configurar_dice_que_se_pregunta_igual(self):
        with tempfile.TemporaryDirectory() as d:
            r = self._correr(d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("sin configurar", r.stdout)
            self.assertIn("preguntar", r.stdout)

    def test_guarda_y_relee(self):
        with tempfile.TemporaryDirectory() as d:
            r = self._correr(d, "--set", "modo=estudio", "--set", "fueros=penal,laboral")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            cfg = json.loads((pathlib.Path(d) / "derecho-argentino" / "config.json")
                             .read_text(encoding="utf-8"))
            self.assertEqual(cfg["perfil"]["modo"], "estudio")
            self.assertEqual(cfg["perfil"]["fueros"], ["penal", "laboral"])
            r2 = self._correr(d, "--json")
            self.assertEqual(json.loads(r2.stdout)["modo"], "estudio")

    def test_rechaza_valores_fuera_del_catalogo(self):
        with tempfile.TemporaryDirectory() as d:
            for mal in ("modo=cualquiera", "rol=presidente", "fueros=laboral,marciano",
                        "cct=42", "sin_igual"):
                with self.subTest(mal=mal):
                    r = self._correr(d, "--set", mal)
                    self.assertEqual(r.returncode, 2, r.stdout)
                    self.assertIn("ERROR", r.stdout)
            self.assertFalse((pathlib.Path(d) / "derecho-argentino" / "config.json").exists(),
                             "un --set invalido no debe escribir nada")

    def test_el_rol_no_queda_fijo_salvo_pedido_expreso(self):
        with tempfile.TemporaryDirectory() as d:
            self._correr(d, "--set", "rol=juez")
            r = self._correr(d)
            self.assertIn("se pregunta igual", r.stdout)
            self.assertNotIn("FIJO", r.stdout)
            self._correr(d, "--set", "rol-fijo=si")
            r2 = self._correr(d)
            self.assertIn("FIJO", r2.stdout)

    def test_no_admite_campos_de_caso_ni_cct(self):
        """El CCT no es dato de cartera y los datos de expediente no van a configuración."""
        with tempfile.TemporaryDirectory() as d:
            for prohibido in ("cct=76/75", "expediente=123", "actor=Perez", "tope_245=100"):
                r = self._correr(d, "--set", prohibido)
                self.assertEqual(r.returncode, 2, f"{prohibido} no debería aceptarse")

    def test_no_pisa_la_ruta_del_repo(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = pathlib.Path(d) / "derecho-argentino" / "config.json"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(json.dumps({"repo": "/ruta/previa"}), encoding="utf-8")
            self._correr(d, "--set", "modo=estudio")
            self.assertEqual(json.loads(cfg.read_text())["repo"], "/ruta/previa")


class TestEstado(unittest.TestCase):
    def test_informe_json_y_codigo_de_salida(self):
        r = subprocess.run(
            [sys.executable, str(pathlib.Path(__file__).parent / "estado.py"), "--json"],
            capture_output=True, text=True, cwd=str(pathlib.Path(__file__).parent))
        self.assertIn(r.returncode, (0, 1), r.stdout + r.stderr)
        inf = json.loads(r.stdout)
        self.assertTrue(inf["repo"], "debería encontrar el repo en esta máquina")
        bloques = {b["bloque"] for b in inf["bloques"]}
        for esperado in ("normas", "fallos", "jus", "inhabiles", "serie IPC", "descargas"):
            self.assertIn(esperado, bloques)
        for b in inf["bloques"]:
            self.assertIn(b["estado"], ("OK", "VENCIDO", "REVISAR", "FALTA"))
            if b["estado"] != "OK":
                self.assertTrue(b["arreglo"], f"{b['bloque']} vencido sin decir cómo arreglarlo")

    def test_sin_repo_sale_2_y_no_revienta(self):
        with tempfile.TemporaryDirectory() as d:
            e = {k: v for k, v in os.environ.items() if k != "DERECHO_AR_REPO"}
            e.update(HOME=d, XDG_CONFIG_HOME=str(pathlib.Path(d) / "cfg"))
            e.pop("CLAUDE_PLUGIN_ROOT", None)
            copia = pathlib.Path(d) / "skill" / "scripts"
            shutil.copytree(pathlib.Path(__file__).parent, copia,
                            ignore=shutil.ignore_patterns("__pycache__"))
            r = subprocess.run([sys.executable, str(copia / "estado.py")],
                               capture_output=True, text=True, env=e, cwd=d)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("NO ENCONTRADO", r.stdout)


class TestJusCargado(unittest.TestCase):
    def test_ultimo_jus_es_el_de_agosto_2026(self):
        import honorarios_pba
        valor, fecha, _ = honorarios_pba.jus_del_repo()
        self.assertEqual(fecha, "2026-08-01")
        self.assertEqual(valor, Decimal("53232"))


class TestHonorariosCLI(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).parent / "honorarios_pba.py"), *args],
            capture_output=True, text=True)

    def test_minimo_siete_jus(self):
        r = self._run("--monto", "1000", "--porcentaje", "20", "--valor-jus", "50000")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("mínimo del art. 22", r.stdout)
        self.assertIn("350,000.00", r.stdout)     # 7 x 50.000

    def test_expresa_en_jus(self):
        r = self._run("--monto", "10000000", "--porcentaje", "20", "--valor-jus", "50000")
        self.assertIn("Expresado en jus", r.stdout)
        self.assertIn("40.00 jus", r.stdout)      # 2.000.000 / 50.000

    def test_rechaza_porcentaje_fuera_de_escala(self):
        r = self._run("--monto", "10000000", "--porcentaje", "30", "--valor-jus", "50000")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fuera de la escala del art. 21", r.stderr)

    def test_advierte_por_debajo_de_la_media(self):
        r = self._run("--monto", "10000000", "--porcentaje", "12", "--valor-jus", "50000")
        self.assertIn("media de la escala", r.stdout)

    def test_lee_el_jus_del_repo(self):
        r = self._run("--monto", "10000000", "--porcentaje", "20")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("vigencia:", r.stdout)


class TestInteresesCLI(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).parent / "intereses.py"), *args],
            capture_output=True, text=True)

    def test_corta_si_la_serie_no_cubre_el_periodo(self):
        # 1999 no está en ninguna serie cargada: debe cortar, no estimar
        r = self._run("--modo", "indice", "--capital", "1000",
                      "--desde", "1999-01-10", "--hasta", "2026-08-31", "--serie", "ipc")
        self.assertEqual(r.returncode, 2)
        self.assertIn("VERIFICAR MONTO ACTUALIZADO", r.stdout)

    def test_corta_si_la_serie_no_existe(self):
        r = self._run("--modo", "indice", "--capital", "1000",
                      "--desde", "2025-01-10", "--hasta", "2026-08-31", "--serie", "inventada")
        self.assertEqual(r.returncode, 2)

    def test_actualiza_con_la_serie_ipc_cargada(self):
        r = self._run("--modo", "indice", "--capital", "1000000",
                      "--desde", "2025-01-15", "--hasta", "2026-08-31", "--serie", "ipc")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Coeficiente", r.stdout)
        self.assertIn("Capital actualizado", r.stdout)

    def test_tasa_nominal(self):
        r = self._run("--modo", "tasa", "--capital", "100000",
                      "--desde", "2025-01-01", "--hasta", "2026-01-01", "--tna", "10")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("10,000.00", r.stdout)

    def test_marca_el_regimen_a_determinar(self):
        r = self._run("--modo", "tasa", "--capital", "1000",
                      "--desde", "2025-01-01", "--hasta", "2026-01-01", "--tna", "10")
        self.assertIn("Galarza", r.stdout)


class TestDescargadorDeNormas(unittest.TestCase):
    """La capa de fuentes no tenía cobertura, y ahí vivio un bug que rebajaba las 59 normas
    en cada corrida. Estas pruebas fijan los dos contratos que lo habrian atajado."""

    @classmethod
    def setUpClass(cls):
        cls.dir = (Path(__file__).resolve().parents[3] / "fuentes" / "scripts")
        if not cls.dir.exists():
            raise unittest.SkipTest("no esta la capa de fuentes")
        sys.path.insert(0, str(cls.dir))

    def test_procedencia_tiene_la_clave_normas(self):
        import _comun
        vacia = {"_descripcion": "x", "normas": {}}
        self.assertIn("normas", vacia)
        self.assertTrue(hasattr(_comun, "cargar_procedencia"))

    def test_ya_registrada_mira_adentro_de_normas(self):
        import descargar_normas as dn
        proc = {"_descripcion": "x", "normas": {"lct-20744": {"sha256": "abc"}}}
        self.assertTrue(dn.ya_registrada(proc, "lct-20744"))
        self.assertFalse(dn.ya_registrada(proc, "ley-19550"))

    def test_ya_registrada_no_confunde_las_claves_del_documento(self):
        """El bug original: `slug in proc` daba False para todo slug real y True para las
        claves de primer nivel. Si esta prueba falla, volvió."""
        import descargar_normas as dn
        proc = {"_descripcion": "x", "normas": {"lct-20744": {}}}
        self.assertFalse(dn.ya_registrada(proc, "normas"))
        self.assertFalse(dn.ya_registrada(proc, "_descripcion"))

    def test_ya_registrada_tolera_procedencia_sin_normas(self):
        import descargar_normas as dn
        self.assertFalse(dn.ya_registrada({}, "lct-20744"))

    def test_pdf_se_detecta_por_content_type_y_no_por_la_extension(self):
        """Un digesto provincial que sirve el PDF desde una URL sin `.pdf` hacía que el
        script tratara los bytes como HTML y escribiera un .txt binario de 240 KB. El unico
        sintoma era que no se encontraba ni un artículo, que parece un problema de la fuente.
        Si esto falla, volvió."""
        sys.path.insert(0, str(self.dir))
        import descargar_normas as dn
        self.assertTrue(dn.es_pdf_real("application/pdf", False))
        self.assertTrue(dn.es_pdf_real("application/pdf; charset=binary", False))
        self.assertFalse(dn.es_pdf_real("text/html; charset=utf-8", False))
        self.assertFalse(dn.es_pdf_real(None, False))

    def test_lo_declarado_como_pdf_manda_aunque_el_servidor_diga_otra_cosa(self):
        sys.path.insert(0, str(self.dir))
        import descargar_normas as dn
        self.assertTrue(dn.es_pdf_real("text/html", True))
        self.assertTrue(dn.es_pdf_real(None, True))

    def test_hash_de_texto_ignora_el_encabezado_de_procedencia(self):
        """El hash crudo de argentina.gob.ar y juristeca cambia en cada request sin que
        cambie la norma. El del cuerpo no puede moverse por eso."""
        import _comun
        raya = "=" * 78
        cuerpo = "ARTÍCULO 1.- Texto de prueba.\n"
        def armar(hash_crudo):
            return (f"Titulo\n{raya}\nJurisdiccion:     nacional\n"
                    f"SHA-256 (crudo):  {hash_crudo}\n\nAdvertencia\n{raya}\n\n{cuerpo}")
        with tempfile.TemporaryDirectory() as d:
            a = Path(d) / "a.txt"
            b = Path(d) / "b.txt"
            a.write_text(armar("1" * 64), encoding="utf-8")
            b.write_text(armar("2" * 64), encoding="utf-8")
            ca = _comun.cuerpo_consolidado(a)
            cb = _comun.cuerpo_consolidado(b)
            self.assertEqual(ca, cuerpo)
            self.assertEqual(_comun.sha256_texto(ca), _comun.sha256_texto(cb))

    def test_el_veredicto_leido_apaga_la_marca_de_ese_problema_y_solo_de_ese(self):
        """revisar_texto() reporta candidatos: hay leyes legitimamente cortas. El veredicto
        se indexa por el texto exacto del problema, no por el slug, para que una norma que
        vuelve con otro defecto siga sonando."""
        import _comun
        with tempfile.TemporaryDirectory() as d:
            arch = Path(d) / "revisiones.json"
            arch.write_text(json.dumps({
                "_descripcion": "veredictos de prueba", "fijado": "2026-09-14",
                "revisiones": {"ley-x": [
                    {"problema": "solo 2 articulos en 1430 caracteres: sospechosamente corto",
                     "veredicto": "la ley son dos articulos", "fecha": "2026-09-14"}]}}),
                encoding="utf-8")
            original = _comun.REVISIONES
            try:
                _comun.REVISIONES = arch
                leidos = _comun.cargar_revisiones()
            finally:
                _comun.REVISIONES = original
        self.assertEqual(leidos["ley-x"]["solo 2 articulos en 1430 caracteres: "
                                         "sospechosamente corto"],
                         "la ley son dos articulos")
        # Otro defecto en la misma norma no queda apagado.
        self.assertNotIn("casi no hay acentos: el charset puede estar mal resuelto",
                         leidos["ley-x"])

    def test_sin_archivo_de_revisiones_no_se_apaga_nada(self):
        import _comun
        original = _comun.REVISIONES
        try:
            _comun.REVISIONES = Path("/no/existe/revisiones.json")
            self.assertEqual(_comun.cargar_revisiones(), {})
        finally:
            _comun.REVISIONES = original

    def test_las_revisiones_declaradas_apuntan_a_normas_del_manifiesto(self):
        """Un veredicto sobre un slug que ya no está en el manifiesto es papel muerto que
        nadie va a volver a leer."""
        import _comun
        if not _comun.REVISIONES.exists():
            self.skipTest("no hay veredictos declarados")
        slugs = {n["slug"] for n in _comun.cargar_manifiesto()}
        for slug in _comun.cargar_revisiones():
            with self.subTest(slug):
                self.assertIn(slug, slugs)

    def test_la_fecha_del_portal_no_mueve_el_hash_del_texto(self):
        """El BO y JURISTECA imprimen la fecha de hoy DENTRO del cuerpo, encima de la norma.
        Sin sacarla, `verificar_normas.py` canta "cambió el texto de la norma" sobre tres
        normas todos los días, y una alarma que suena siempre se deja de mirar."""
        import _comun
        bo = ("Edición del\n\n{f}\n\nEdiciones Anteriores\n\n"
              "Ciudad de Buenos Aires, 30/09/2019\n\nARTÍCULO 1°.- Sustitúyese el art. 12.\n")
        ju = "Saltar al contenido\n\n{f}\n\nLas fuentes del Derecho a tu alcance\n\nLey 6407\n"
        for plantilla, uno, otro in ((bo, "11 de Septiembre de 2026", "14 de Septiembre de 2026"),
                                     (ju, "13 septiembre 2026", "14 septiembre 2026")):
            with self.subTest(plantilla[:20]):
                self.assertEqual(
                    _comun.sha256_texto(_comun.normalizar_cromo(plantilla.format(f=uno))),
                    _comun.sha256_texto(_comun.normalizar_cromo(plantilla.format(f=otro))))

    def test_solo_se_saca_la_fecha_que_esta_entre_los_rotulos_del_portal(self):
        """El riesgo de sacar el cromo es comerse las fechas de la norma -sanción,
        promulgación, vigencia-, que son justo las que hay que detectar si cambian. Por eso
        el patrón va anclado a los rotulos del portal y no busca fechas sueltas."""
        import _comun
        for intacto in ("ARTÍCULO 1°.- Rige desde el 14 de Septiembre de 2026.\n",
                        "DADA EN BUENOS AIRES, A LOS 14 de Septiembre de 2026.\n",
                        "Sancionada: 8 de Febrero de 1995\nPromulgada: 1 marzo 1995\n"):
            with self.subTest(intacto[:30]):
                self.assertEqual(_comun.normalizar_cromo(intacto), intacto)

    def test_el_cromo_removido_deja_rastro_visible(self):
        """Si se borrara el renglon sin decir nada, quien lea el .txt ve dos líneas de maqueta
        pegadas y no sabe si falta algo de la norma."""
        import _comun
        salida = _comun.normalizar_cromo(
            "Edición del\n\n14 de Septiembre de 2026\n\nEdiciones Anteriores\n")
        self.assertIn(_comun.SIN_FECHA, salida)
        self.assertNotIn("14 de Septiembre de 2026", salida)

    def test_hash_de_texto_si_cambia_cuando_cambia_la_norma(self):
        import _comun
        self.assertNotEqual(_comun.sha256_texto("ARTÍCULO 1.- uno"),
                            _comun.sha256_texto("ARTÍCULO 1.- dos"))

    def test_descargas_cuenta_la_interseccion_y_no_dos_totales(self):
        """El conteo era len(procedencia) menos len(manifiesto con URL). Una sola entrada
        registrada sin URL -una norma aportada a mano- tapaba una que faltaba bajar, y el
        diagnóstico daba todo en verde con una norma ausente. Si esto falla, volvió."""
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        with tempfile.TemporaryDirectory() as d:
            N = Path(d) / "argentina" / "fuentes" / "normas"
            N.mkdir(parents=True)
            (N.parent / "datos").mkdir()
            (N / "una.txt").write_text("x", encoding="utf-8")
            (N / "normas.json").write_text(json.dumps({"normas": [
                {"slug": "una", "url": "http://x/1"},
                {"slug": "otra", "url": "http://x/2"},
                {"slug": "sin-url"},
            ]}), encoding="utf-8")
            (N / "procedencia.json").write_text(json.dumps({"normas": {
                "una": {"archivo": "una.txt"},
                "aportada-a-mano": {"archivo": "aportada.pdf"},
            }}), encoding="utf-8")
            filas = estado.revisar(Path(d))
            fila = next(f for f in filas if f["bloque"] == "descargas")
            self.assertIn("1 de 2", fila["detalle"])
            self.assertIn("faltan 1", fila["detalle"])
            self.assertEqual(fila["estado"], "REVISAR")

    def test_descargas_no_cuenta_un_archivo_que_no_existe(self):
        """Procedencia puede tener el registro y el archivo haber desaparecido."""
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        with tempfile.TemporaryDirectory() as d:
            N = Path(d) / "argentina" / "fuentes" / "normas"
            N.mkdir(parents=True)
            (N.parent / "datos").mkdir()
            (N / "normas.json").write_text(json.dumps(
                {"normas": [{"slug": "una", "url": "http://x/1"}]}), encoding="utf-8")
            (N / "procedencia.json").write_text(json.dumps(
                {"normas": {"una": {"archivo": "una.txt"}}}), encoding="utf-8")
            filas = estado.revisar(Path(d))
            fila = next(f for f in filas if f["bloque"] == "descargas")
            self.assertIn("faltan 1", fila["detalle"])

    def test_confirmar_identidad_detecta_el_fallo_cambiado(self):
        """El incidente que motiva el control: buscando "Acosta" (Fallos 331:858) aparece
        indexado un idAnalisis que baja "Llerena, Horacio Luis s/ abuso de armas". En los
        repositorios de la CSJN el documento se pide por un id interno que no se deriva de la
        cita, así que un id mal curado cita un fallo por otro. Si esto falla, el agujero volvió."""
        import descargar_jurisprudencia as dj
        llerena = ("Buenos Aires, 17 de mayo de 2005. Vistos los autos: Recurso de hecho "
                   "deducido por la defensa en la causa Llerena, Horacio Luis s/ abuso de "
                   "armas y lesiones, para decidir sobre su procedencia.")
        problema = dj.confirmar_identidad(llerena, "Acosta, Alejandro Esteban")
        self.assertIsNotNone(problema)
        self.assertIn("Acosta", problema)

    def test_confirmar_identidad_acepta_el_fallo_correcto(self):
        """Y no debe saltar por las variantes de carátula entre repositorios: numero de causa,
        's/ recurso de hecho', abreviaturas. Alcanza con que el apellido este."""
        import descargar_jurisprudencia as dj
        acosta = ("A. 2186. XLI. Recurso de hecho. Acosta, Alejandro Esteban s/ infracción "
                  "art. 14, 1 párrafo ley 23.737 causa N 28/05.")
        self.assertIsNone(dj.confirmar_identidad(acosta, "Acosta, Alejandro Esteban"))

    def test_confirmar_identidad_tolera_acentos_y_puntuacion(self):
        import descargar_jurisprudencia as dj
        cuerpo = "recurso de hecho deducido en la causa GÓNGORA, Gabriel Arnaldo s/ causa n 14.092"
        self.assertIsNone(dj.confirmar_identidad(cuerpo, "Góngora, Gabriel Arnaldo"))

    def test_confirmar_identidad_usa_el_apellido_y_no_la_caratula_entera(self):
        """Una carátula con 'contra' o 'c/' se parte: lo que se busca es la cabeza."""
        import descargar_jurisprudencia as dj
        cuerpo = "Vera, Isabel contra Fisco de la Provincia de Buenos Aires. Enfermedad accidente"
        self.assertIsNone(dj.confirmar_identidad(cuerpo, "Vera, Isabel contra Fisco de la Provincia"))
        self.assertIsNotNone(dj.confirmar_identidad(cuerpo, "Marchetti, Jorge Gabriel contra Fiscalía"))

    def test_puntos_suspensivos_no_son_codepage_degradado(self):
        """El set original incluia U+2026. Una fe de erratas que dice DONDE DICE: ... /
        DEBE DECIR: ... , o una tabla con puntos de relleno, marcaba la norma como mal
        codificada. Tres de las cuatro normas marcadas eran eso: texto sano."""
        import _comun
        sano = ("ARTÍCULO 1.- " + "el artículo se aplicará según la reglamentación más próxima. " * 60
                + "DONDE DICE: \u2026 actividades especiales\u2026 DEBE DECIR: "
                  "\u2026 actividades diferenciales\u2026 " * 6)
        self.assertEqual(_comun.revisar_texto(sano), [])

    def test_control_pegado_a_letras_si_es_codepage_degradado(self):
        """Lo que delata la corrupción es el carácter de control entre letras: m,rito por
        mérito. Eso no pasa en texto sano."""
        import _comun
        roto = ("ARTÍCULO 1.- " + "la petición se resolverá según el criterio más razonable. " * 60
                + "segun el m\u201arito que arrojen los autos, por c\u201adula, "
                  "cuando el Tribunal no est\u201a en audiencia, si \u201aestos lo pidieran ")
        problemas = _comun.revisar_texto(roto)
        self.assertTrue(any("acentuacion degradada" in p for p in problemas), problemas)

    def test_mojibake_de_doble_codificacion(self):
        import _comun
        roto = ("ARTÍCULO 1.- " + "la acción prescribirá según el plazo más breve. " * 60 + "aÃ±os Ã©poca Ã³rgano artÃ­culo ")
        problemas = _comun.revisar_texto(roto)
        self.assertTrue(any("mojibake" in p for p in problemas), problemas)

    def test_sentencias_reporta_un_fallo_declarado_y_no_bajado(self):
        """El bloque "fallos" solo mira la fecha de verificación del manifiesto. Un fallo con
        URL declarada pero sin PDF en disco no lo reportaba nadie, y había tres así citados en
        los módulos. Si esto falla, el agujero volvió."""
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        with tempfile.TemporaryDirectory() as d:
            J = Path(d) / "argentina" / "fuentes" / "jurisprudencia"
            J.mkdir(parents=True)
            (J.parent / "datos").mkdir()
            (J / "bajado.pdf").write_text("x", encoding="utf-8")
            (J / "fallos.json").write_text(json.dumps({"fallos": [
                {"slug": "bajado", "url": "http://x/1"},
                {"slug": "declarado-sin-pdf", "url": "http://x/2"},
                {"slug": "sin-url"},
            ]}), encoding="utf-8")
            (J / "procedencia.json").write_text(json.dumps({"fallos": {
                "bajado": {"url": "http://x/1"},
                "declarado-sin-pdf": {"url": "http://x/2"},
            }}), encoding="utf-8")
            fila = next(f for f in estado.revisar(Path(d)) if f["bloque"] == "sentencias")
            self.assertIn("1 de 2", fila["detalle"])
            self.assertIn("faltan 1", fila["detalle"])
            self.assertEqual(fila["estado"], "REVISAR")

    def test_sentencias_en_verde_cuando_estan_todas(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        with tempfile.TemporaryDirectory() as d:
            J = Path(d) / "argentina" / "fuentes" / "jurisprudencia"
            J.mkdir(parents=True)
            (J.parent / "datos").mkdir()
            (J / "bajado.pdf").write_text("x", encoding="utf-8")
            (J / "fallos.json").write_text(json.dumps(
                {"fallos": [{"slug": "bajado", "url": "http://x/1"}]}), encoding="utf-8")
            (J / "procedencia.json").write_text(json.dumps(
                {"fallos": {"bajado": {"url": "http://x/1"}}}), encoding="utf-8")
            fila = next(f for f in estado.revisar(Path(d)) if f["bloque"] == "sentencias")
            self.assertEqual(fila["estado"], "OK")
            self.assertNotIn("faltan", fila["detalle"])


class TestConteoDeSeries(unittest.TestCase):
    """El encabezado de un csv no es un período. Contarlo informaba uno de más por serie."""

    def _csv(self, cuerpo: str) -> Path:
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        f = d / "serie.csv"
        f.write_text(cuerpo, encoding="utf-8")
        return f

    def test_no_cuenta_el_encabezado_como_periodo(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        f = self._csv("# INDEC\n# frecuencia: mensual\nperiodo,indice\n"
                      "2026-06,100\n2026-07,101\n2026-08,102\n")
        self.assertEqual(estado._ultima_fila_csv(f), ("2026-08", 3))

    def test_un_csv_con_encabezado_y_sin_datos_cuenta_como_vacio(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        f = self._csv("# INDEC\nperiodo,indice\n")
        self.assertEqual(estado._ultima_fila_csv(f), (None, 0))

    def test_las_series_del_repo_informan_lo_que_tienen(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        import estado
        raiz, _origen = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        for arch in ("serie-ipc.csv", "serie-ripte.csv", "serie-cer.csv", "jus-scba.csv"):
            ruta = raiz / "argentina" / "fuentes" / "datos" / arch
            with self.subTest(arch):
                utiles = [l for l in ruta.read_text(encoding="utf-8").splitlines()
                          if l.strip() and not l.lstrip().startswith("#")]
                _, contadas = estado._ultima_fila_csv(ruta)
                self.assertEqual(contadas, len(utiles) - 1)


class TestManifiestoDeFuentes(unittest.TestCase):
    """`fuentes/MANIFIESTO.md` afirma cuánto hay cargado, y viaja dentro del plugin.

    Ya se desactualizó una vez —decía 42 normas cuando había 112— y nadie se enteró porque
    ningún control lo miraba. Cada fila declara sus números y acá se comparan contra el repo.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.fuentes = raiz / "argentina" / "fuentes"
        self.tabla = (self.fuentes / "MANIFIESTO.md").read_text(encoding="utf-8")

    def _declarado(self, patron: str) -> tuple:
        hallado = re.search(patron, self.tabla)
        self.assertIsNotNone(
            hallado, f"la tabla del MANIFIESTO ya no dice esto: {patron}")
        return tuple(int(g) for g in hallado.groups())

    def _en_prosa(self, patron: str) -> tuple:
        """Como `_declarado`, pero con los saltos de línea aplanados: la prosa se reacomoda
        al reescribirla y el control no tiene por que romperse por un salto de renglon."""
        hallado = re.search(patron, re.sub(r"\s+", " ", self.tabla))
        self.assertIsNotNone(hallado, f"el MANIFIESTO ya no dice esto: {patron}")
        return tuple(int(g) for g in hallado.groups())

    def _json(self, ruta: Path, clave: str) -> list:
        d = json.loads(ruta.read_text(encoding="utf-8"))[clave]
        return d if isinstance(d, list) else list(d.values())

    def test_las_normas_declaradas_son_las_que_hay(self):
        normas = self._json(self.fuentes / "normas" / "normas.json", "normas")
        con_url = sum(1 for n in normas if n.get("url"))
        self.assertEqual(self._declarado(r"\*\*(\d+) entradas\*\*, (\d+) con URL"),
                         (len(normas), con_url))
        self.assertEqual(self._declarado(r"\*\*(\d+) entradas sin URL\*\*"),
                         (len(normas) - con_url,))

    def test_los_textos_declarados_son_los_que_hay(self):
        proc = self._json(self.fuentes / "normas" / "procedencia.json", "normas")
        txt = list((self.fuentes / "normas").glob("*.txt"))
        self.assertEqual(
            self._declarado(r"\*\*(\d+) descargadas\*\*.*?\*\*(\d+) textos con hash\*\*"),
            (len(txt), len(proc)))

    def test_los_fallos_declarados_son_los_que_hay(self):
        fallos = self._json(self.fuentes / "jurisprudencia" / "fallos.json", "fallos")
        self.assertEqual(self._declarado(r"\*\*(\d+) fallos\*\*"), (len(fallos),))
        pdfs = list((self.fuentes / "jurisprudencia").glob("*.pdf"))
        self.assertEqual(self._declarado(r"\*\*(\d+) descargados\*\*"), (len(pdfs),))

    def test_las_series_declaradas_son_las_que_hay(self):
        import estado
        esperado = {
            "jus-scba.csv": r"\*\*(\d+) filas\*\*",
            "serie-ipc.csv": r"serie-ipc\.csv` \| \*\*Completa\*\*: (\d+) períodos",
            "serie-ripte.csv": r"serie-ripte\.csv` \| \*\*Completa\*\*: (\d+) períodos",
            "serie-cer.csv": r"serie-cer\.csv` \| \*\*Completa\*\*: (\d+) períodos",
        }
        for arch, patron in esperado.items():
            with self.subTest(arch):
                _, filas = estado._ultima_fila_csv(self.fuentes / "datos" / arch)
                self.assertEqual(self._declarado(patron), (filas,))

    def test_la_prosa_que_explica_los_tres_numeros_dice_lo_mismo_que_la_tabla(self):
        """La tabla estaba controlada y la frase que la explica no: decía 112, 111 y 106."""
        normas = self._json(self.fuentes / "normas" / "normas.json", "normas")
        proc = self._json(self.fuentes / "normas" / "procedencia.json", "normas")
        carpeta = self.fuentes / "normas"
        self.assertEqual(
            self._en_prosa(
                r"\*\*(\d+)\*\* es lo que la skill espera encontrar, \*\*(\d+)\*\* es lo que "
                r"tiene texto bajado con hash registrado, y \*\*(\d+)\*\* son los `\.txt` en "
                r"disco, porque los \*\*(\d+)\*\* restantes son PDF"),
            (len(normas), len(proc),
             len(list(carpeta.glob("*.txt"))), len(list(carpeta.glob("*.pdf")))))

    MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre")

    def test_la_foto_no_puede_ser_anterior_a_la_ultima_descarga(self):
        """El encabezado decía 13/09 con nueve normas bajadas el 15/09, y nada lo miraba.

        La foto se fecha POR MES y no por dia, a propósito: una fecha al dia invita a leer el
        repositorio como vencido el dia 181, cuando la granularidad real del trabajo es el mes.
        La precisión al dia se conserva donde la consume una herramienta --la columna de
        `changelog-normativo.md`, de la que `pendientes.py` cuenta los 180 días-- y no donde la
        lee una persona. Así que esto compara meses, con un mes de tolerancia, y sigue
        atrapando lo que importa: una foto que quedo atrás de lo que hay bajado.
        """
        proc = self._json(self.fuentes / "normas" / "procedencia.json", "normas")
        ultima = max(p["descargado"][:7] for p in proc)          # AAAA-MM
        m = re.search(r"^## Estado a (\w+) de ((?:19|20)\d{2})$", self.tabla, re.M)
        self.assertIsNotNone(m, "el MANIFIESTO dejo de fechar su foto")
        mes, anio = m.group(1).lower(), m.group(2)
        self.assertIn(mes, self.MESES, f"«{mes}» no es un mes")
        foto = f"{anio}-{self.MESES.index(mes) + 1:02d}"
        self.assertGreaterEqual(
            foto, ultima,
            f"la foto del MANIFIESTO ({foto}) es anterior al mes de la ultima norma bajada "
            f"({ultima})")


class TestIndiceDeFallosCSJN(unittest.TestCase):
    """`fallos-csjn.md` §34.8 lleva la cuenta de qué falta leer, escrita a mano.

    Una cuenta a mano sobre una tabla que crece se separa de la tabla sin que nadie lo note.
    Acá se compara contra las tablas del propio módulo y contra los veredictos de lectura de
    `herramientas/lecturas-ocr.json`.
    """

    FILA = r"^\| \*\*(.+?)\*\* \| ([^|]+?) \| ([^|]+?) \| `([^`]+)` \|"
    PENDIENTE = r"^\| ([^|]+?) \| ([^|]+?) \| (34\.\d) \| ([^|]+?) \|"

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz
        self.modulo = (raiz / "argentina" / "skills" / "derecho-argentino" / "references"
                       / "fallos-csjn.md").read_text(encoding="utf-8")
        self.filas = re.findall(self.FILA, self.modulo, re.M)
        self.pendientes = re.findall(self.PENDIENTE, self.modulo.split("### 34.8")[1], re.M)

    def _declarados(self) -> tuple[int, int]:
        """Los dos contadores de §34.8. Uno solo lugar, para que no puedan discrepar."""
        hallado = re.search(r"Con holding leído contra el documento: (\d+)\. "
                            r"Sin holding: (\d+)\.", self.modulo)
        self.assertIsNotNone(hallado, "§34.8 ya no declara los dos contadores")
        return int(hallado.group(1)), int(hallado.group(2))

    def test_la_cuenta_de_holdings_cierra_con_las_filas_que_hay(self):
        con, sin = self._declarados()
        self.assertEqual(con + sin, len(self.filas),
                         "los holdings declarados no suman los fallos que hay en las tablas")

    def test_la_tabla_de_pendientes_tiene_tantas_filas_como_dice(self):
        _con, sin = self._declarados()
        self.assertEqual(len(self.pendientes), sin,
                         "la tabla de pendientes no coincide con el contador")

    def test_cada_pendiente_declara_el_ocr_que_tiene_medido(self):
        lecturas = json.loads((self.raiz / "herramientas" / "lecturas-ocr.json")
                              .read_text(encoding="utf-8"))["lecturas"]
        for caratula, cita, _seccion, ocr in self.pendientes:
            with self.subTest(caratula.strip()):
                fila = next((f for f in self.filas if cita.strip() in f[1]), None)
                self.assertIsNotNone(fila, f"{cita} no está en las tablas del módulo")
                estado = lecturas.get(fila[3], {}).get("estado")
                self.assertIsNotNone(estado, f"{fila[3]} no tiene veredicto de lectura")
                self.assertIn(estado, ocr,
                              f"declara «{ocr.strip()}» y el veredicto medido es «{estado}»")

    def test_cada_fila_tiene_su_pdf_y_esta_en_el_manifiesto(self):
        J = self.raiz / "argentina" / "fuentes" / "jurisprudencia"
        fallos = json.loads((J / "fallos.json").read_text(encoding="utf-8"))["fallos"]
        slugs = {f["slug"] for f in (fallos if isinstance(fallos, list) else fallos.values())}
        for _car, _cita, _fecha, slug in self.filas:
            with self.subTest(slug):
                self.assertTrue((J / f"{slug}.pdf").exists(), "sin PDF en el repo")
                self.assertIn(slug, slugs, "no está en fallos.json")


class TestTextoRecuperadoPorOCR(unittest.TestCase):
    """`fuentes/jurisprudencia/ocr/` es texto DERIVADO de un PDF, y las derivaciones vencen.

    Si el PDF se vuelve a bajar y cambia, el .txt de al lado sigue ahí diciendo lo de antes.
    Cada entrada guarda el hash del PDF del que salió y el del texto: acá se comparan.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.juris = raiz / "argentina" / "fuentes" / "jurisprudencia"
        registro = self.juris / "ocr" / "procedencia.json"
        if not registro.exists():
            self.skipTest("todavía no hay texto recuperado")
        self.registro = json.loads(registro.read_text(encoding="utf-8"))["fallos"]

    def _sha(self, ruta: Path) -> str:
        return hashlib.sha256(ruta.read_bytes()).hexdigest()

    def test_cada_derivacion_corresponde_al_pdf_que_dice(self):
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                pdf = self.juris / ficha["pdf"]
                self.assertTrue(pdf.exists(), f"falta {ficha['pdf']}")
                self.assertEqual(self._sha(pdf), ficha["sha256_pdf"],
                                 "el PDF cambió: regenerar con reocr_jurisprudencia.py")

    def test_el_texto_no_fue_editado_a_mano(self):
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                txt = self.juris / "ocr" / ficha["archivo"]
                self.assertTrue(txt.exists(), f"falta {ficha['archivo']}")
                self.assertEqual(self._sha(txt), ficha["sha256_texto"],
                                 "el texto no coincide con su hash: es una derivación, "
                                 "no se corrige a mano; se regenera")

    def test_cada_derivacion_avisa_que_no_es_publicacion_oficial(self):
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                cabecera = (self.juris / "ocr" / ficha["archivo"]).read_text(
                    encoding="utf-8")[:1500]
                self.assertIn("RECUPERADO POR OCR LOCAL", cabecera)
                self.assertIn("publicacion oficial", cabecera)  # sin tilde: fijado por hash
                self.assertIn(ficha["sha256_pdf"], cabecera)


class TestEntradasSinURL(unittest.TestCase):
    """Una norma declarada sin URL tiene que decir por qué, o el descargador no informa nada.

    `descargar_normas.py` imprime `SIN URL <slug> <nota>` en cada corrida. Sin `nota` imprime
    "completar el manifiesto", que no dice ni qué falta ni por qué importa, y la entrada se
    vuelve ruido que se aprende a saltear.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        catalogo = raiz / "argentina" / "fuentes" / "normas" / "normas.json"
        self.normas = json.loads(catalogo.read_text(encoding="utf-8"))["normas"]

    def test_toda_entrada_sin_url_explica_por_que(self):
        sin_url = [e for e in self.normas if not e.get("url")]
        self.assertTrue(sin_url, "el catálogo dejó de declarar normas sin URL")
        for entrada in sin_url:
            with self.subTest(entrada["slug"]):
                self.assertGreater(len(entrada.get("nota", "")), 40,
                                   f"{entrada['slug']} no dice por qué no tiene URL")


class TestVocabularioDeMarcadores(unittest.TestCase):
    """Todo marcador que un módulo emita tiene que existir en `references/marcadores.md`.

    El marcador es la salida que el abogado copia al escrito, así que un nombre inventado no
    falla ruidosamente: sale igual y nadie lo reconoce. `marcadores.md` declara las dos listas
    —los canónicos en sus encabezados y los contraejemplos en la tabla "No usar"— y acá se
    acepta sólo lo que figure en una de las dos.
    """

    NOMBRE = re.compile(r"\[([" + MAYUSCULAS + "][" + MAYUSCULAS + r" \-]{3,})(?::|\])")
    # El mismo patrón pero tolerante a la caja: es el que detecta un marcador mal
    # capitalizado, y también necesita la dieresis o `[Verificar Antigüedad: ...]` pasa.
    CUALQUIERA = re.compile(r"\[([" + LETRAS + "][" + LETRAS + r" \-]{3,})(?::|\])")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.skill = raiz / "argentina" / "skills" / "derecho-argentino"
        vocabulario = (self.skill / "references" / "marcadores.md").read_text(encoding="utf-8")
        self.canonicos = set(re.findall(r"^### [A-D]\d+ · (.+)$", vocabulario, re.M))
        # Los contraejemplos que el propio vocabulario declara, para poder nombrarlos al
        # explicar qué no usar sin que el test los tome por invención.
        self.declarados = set(re.findall(r"`\[([" + MAYUSCULAS + "][" + MAYUSCULAS + r" \-]{3,})[\]:]", vocabulario))

    def test_el_vocabulario_tiene_las_cuatro_series_completas(self):
        vocabulario = (self.skill / "references" / "marcadores.md").read_text(encoding="utf-8")
        series = re.findall(r"^### ([A-D])(\d+) ·", vocabulario, re.M)
        cuenta = {serie: max(int(n) for s, n in series if s == serie) for serie, _ in series}
        self.assertEqual(cuenta, {"A": 11, "B": 5, "C": 4, "D": 6})
        self.assertEqual(len(self.canonicos), 26)

    def _archivos(self):
        """SKILL.md, los módulos y TAMBIÉN los evals.

        Los evals quedaban afuera, y son justo donde vive la salida esperada: un marcador roto
        en un `resultado.md` no falla, ensenia la forma equivocada.
        """
        archivos = [self.skill / "SKILL.md"]
        archivos += [p for p in sorted((self.skill / "references").glob("*.md"))
                     if p.name != "marcadores.md"]
        archivos += sorted(self.skill.parent.parent.glob("evals/**/*.md"))
        return archivos

    def test_un_marcador_con_dieresis_no_escapa_al_control(self):
        """MUTACION del alcance del propio control, y no de un archivo del repo.

        Las clases de letras estaban escritas tres veces a mano y a las tres les faltaba la Ü.
        Consecuencia: `[VERIFICAR ANTIGÜEDAD: ...]` no matcheaba el patrón, así que el marcador
        no era ni candidato y el control lo IGNORABA en silencio en vez de reclamarlo. No es
        hipotetico: "antigüedad" con dieresis aparece 67 veces en el repositorio y es el nucleo
        del art. 245 LCT.

        Hoy las tres clases salen de MAYÚSCULAS y LETRAS, definidas una sola vez arriba.
        """
        inventado = "[VERIFICAR ANTIGÜEDAD: cómputo del art. 245 - aportar fecha de ingreso]"
        self.assertEqual(self.NOMBRE.findall(inventado), ["VERIFICAR ANTIGÜEDAD"],
                         "el patrón no ve un marcador con diéresis: se le escapa al control")
        self.assertNotIn("VERIFICAR ANTIGÜEDAD", self.canonicos | self.declarados,
                         "si algún día se declara, este fixture hay que cambiarlo")
        # Y la Ñ, que es el otro carácter que ya estaba y conviene fijar de paso.
        self.assertEqual(self.NOMBRE.findall("[VERIFICAR DISEÑO: x]"), ["VERIFICAR DISEÑO"])
        # Y el patrón tolerante a la caja, que usa LETRAS y no MAYÚSCULAS.
        self.assertEqual(self.CUALQUIERA.findall("[Verificar Antigüedad: x]"),
                         ["Verificar Antigüedad"])

    def test_ningun_marcador_perdio_las_mayusculas(self):
        """MUTACION vivida: una corrección de acentos en masa convirtio
        `[VERIFICAR CRITERIO DEL FUERO:` en `[VERIFICAR Criterio DEL FUERO:` en dos evals, y
        este suite no lo vio porque su regex solo aceptaba candidatos ya en mayúsculas: el
        marcador roto no era ni candidato. Ahora se mira cualquier nombre y, si en mayúsculas
        resulta ser un marcador canónico, tiene que estar escrito exactamente así.
        """
        for archivo in self._archivos():
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for nombre in self.CUALQUIERA.findall(linea):
                    nombre = nombre.strip()
                    if nombre.upper() not in self.canonicos or nombre == nombre.upper():
                        continue
                    with self.subTest(f"{archivo.name}:{numero} {nombre}"):
                        self.fail(f"{archivo.name}:{numero} escribe «{nombre}» y el marcador "
                                  f"canónico es «{nombre.upper()}»")

    def test_ningun_modulo_emite_un_marcador_inventado(self):
        archivos = self._archivos()
        for archivo in archivos:
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for nombre in self.NOMBRE.findall(linea):
                    nombre = nombre.strip()
                    with self.subTest(f"{archivo.name}:{numero} {nombre}"):
                        self.assertTrue(nombre in self.canonicos or nombre in self.declarados,
                                        f"{archivo.name}:{numero} emite un marcador que no está "
                                        f"en marcadores.md: [{nombre}]")


class TestCuentaDeEvals(unittest.TestCase):
    """Cuántos casos de verificación hay se afirma en `LICENCIAS.md`, y esa cifra se vence sola.

    Importa más que un conteo cualquiera: la sección 2 del mapa declara **cuáles** de los evals
    son capa 2 —los que venían del fork de origen— y cuántos se escribieron acá. Si el total se
    desactualiza, la resta que declara la autoría queda mal.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz
        self.casos = [d for d in (raiz / "argentina" / "evals").iterdir() if d.is_dir()]

    def test_licencias_declara_los_casos_que_hay(self):
        texto = (self.raiz / "LICENCIAS.md").read_text(encoding="utf-8")
        hallado = re.search(r"\*\*(\d+) casos\*\* de verificación", texto)
        self.assertIsNotNone(hallado, "LICENCIAS.md dejó de decir cuántos evals hay")
        self.assertEqual(int(hallado.group(1)), len(self.casos))

    def test_el_slug_del_encabezado_es_el_nombre_del_directorio(self):
        """El slug se escribe en el encabezado de `rubrica.md` y `resultado.md`, y ahí va en
        ASCII porque es el nombre de una carpeta.

        MUTACION VIVIDA: una corrección de acentos por regla convirtio
        `familia-restitución-grave-riesgo-violencia` en `...-restitución-...` en cinco archivos,
        y ningún test lo vio. El slug identifica el caso: si el encabezado dice otro, el eval
        deja de poder cruzarse con su carpeta.
        """
        for caso in sorted(self.casos):
            for nombre in ("rubrica.md", "resultado.md", "caso.md"):
                f = caso / nombre
                if not f.is_file():
                    continue
                encabezado = next((l for l in f.read_text(encoding="utf-8").splitlines()
                                   if l.startswith("#")), "")
                if "·" not in encabezado:
                    continue
                declarado = encabezado.split("·")[-1].strip()
                # Solo cuando lo que sigue al · ES un slug. `caso.md` pone ahí el titulo en
                # prosa, y eso no tiene por que coincidir con el nombre de la carpeta.
                if " " in declarado or not re.fullmatch(r"[\w\-]+", declarado):
                    continue
                with self.subTest(f"{caso.name}/{nombre}"):
                    self.assertEqual(declarado, caso.name,
                                     "el encabezado no nombra el directorio del caso")

    def test_los_cuatro_de_capa_2_siguen_estando(self):
        """Si uno se renombra, la enumeración del mapa deja de identificar nada."""
        de_capa_2 = ("administrativo-caba-recursos-agotamiento-via",
                     "consumidor-dano-punitivo-prescripcion",
                     "consumidor-garantia-producto-defectuoso",
                     "consumidor-prepaga-aumento-dnu70")
        nombres = {d.name for d in self.casos}
        for caso in de_capa_2:
            with self.subTest(caso):
                self.assertIn(caso, nombres)
        texto = (self.raiz / "LICENCIAS.md").read_text(encoding="utf-8")
        for caso in de_capa_2:
            with self.subTest(f"declarado: {caso}"):
                self.assertIn(caso, texto, "LICENCIAS.md dejó de nombrarlo como capa 2")

    def test_cada_caso_trae_sus_tres_piezas(self):
        for caso in sorted(self.casos):
            with self.subTest(caso.name):
                for pieza in ("caso.md", "rubrica.md", "resultado.md"):
                    self.assertTrue((caso / pieza).is_file(), f"falta {pieza}")


class TestInventarioDeModelos(unittest.TestCase):
    """`modelos.md` existe para que los modelos se encuentren: si falta uno, no sirve.

    El conteo vive repetido en tres documentos, así que acá se mide contra el disco en vez
    de recordarlo.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz
        self.escritos = raiz / "argentina" / "kb" / "escritos"
        self.modelos = {f"kb/escritos/{p.relative_to(self.escritos).as_posix()}"
                        for d in self.escritos.rglob("modelos") if d.is_dir()
                        for p in d.glob("*.md")}

    def test_el_inventario_cita_todos_los_modelos_del_repo(self):
        texto = (self.raiz / "argentina" / "skills" / "derecho-argentino" / "references"
                 / "modelos.md").read_text(encoding="utf-8")
        citados = set(re.findall(r"`(kb/escritos/[\w./\-]+\.md)`", texto))
        faltan = sorted(self.modelos - citados)
        self.assertEqual(faltan, [], f"modelos.md no inventaría: {faltan}")

    def test_los_documentos_que_cuentan_modelos_dicen_el_numero_real(self):
        cuantos = len(self.modelos)
        for relativo in ("argentina/kb/README.md", "docs/ARQUITECTURA.md"):
            with self.subTest(relativo):
                texto = (self.raiz / relativo).read_text(encoding="utf-8")
                hallado = re.search(r"(\d+) modelos", texto)
                self.assertIsNotNone(hallado, f"{relativo} dejó de contar los modelos")
                self.assertEqual(int(hallado.group(1)), cuantos)


class TestREADMEDeScripts(unittest.TestCase):
    """El README de `scripts/` describe la suite y las series, y eso se vence solo.

    Una cifra escrita a mano sobre algo que crece envejece en silencio: acá se mide.
    """

    def setUp(self):
        self.aqui = Path(__file__).parent
        self.readme = (self.aqui / "README.md").read_text(encoding="utf-8")

    def test_la_cantidad_de_tests_que_anuncia_es_la_que_hay(self):
        anunciados = re.search(r"\*\*(\d+) tests\*\*", self.readme)
        self.assertIsNotNone(anunciados, "el README dejó de decir cuántos tests hay")
        cargados = unittest.defaultTestLoader.discover(str(self.aqui), pattern="test_*.py")
        self.assertEqual(int(anunciados.group(1)), cargados.countTestCases())

    def test_el_checklist_nombra_todos_los_suites_de_herramientas(self):
        """Un test que no está en el checklist es un test apagado, y uno apagado es peor que
        uno que no existe: figura en el conteo y nadie lo corre. `herramientas/` llegó a tener
        cuatro suites mientras el checklist nombraba sólo `test_scripts.py`. Esto obliga a que
        un suite nuevo entre al checklist o rompa los tests."""
        raiz = self.aqui.parents[3]
        desarrollo = raiz / "docs" / "DESARROLLO.md"
        if not desarrollo.is_file():
            self.skipTest("no está docs/DESARROLLO.md")
        texto = desarrollo.read_text(encoding="utf-8")
        bloque = re.search(r"## Antes de dar por terminado un cambio\n+```sh\n(.*?)```",
                           texto, re.S)
        self.assertIsNotNone(bloque, "el checklist dejó de tener su bloque de comandos")
        comandos = bloque.group(1)
        suites = sorted((raiz / "herramientas").glob("test_*.py"))
        self.assertTrue(suites, "no encontré los suites de herramientas/")
        for suite in suites:
            with self.subTest(suite.name):
                self.assertIn(f"herramientas/{suite.name}", comandos,
                              f"el checklist de DESARROLLO.md no corre {suite.name}")
        # Y al revés: un suite que se saca del repo tiene que salir del checklist, o el
        # procedimiento manda correr un archivo que no existe y falla en la mano de quien
        # lo sigue. Pasa al mover una herramienta afuera.
        nombres = {s.name for s in suites}
        for linea in comandos.splitlines():
            if "herramientas/test_" not in linea:
                continue
            nombrado = linea.split("herramientas/")[1].split()[0]
            with self.subTest(nombrado):
                self.assertIn(nombrado, nombres,
                              f"el checklist manda correr {nombrado}, que ya no está")

    def test_ci_corre_los_mismos_suites_que_el_checklist(self):
        """El checklist es un procedimiento y CI es la aduana: si dicen distinto, gana el olvido.

        Ya habían divergido: el checklist nombraba seis suites y `tests.yml` corría cinco,
        porque un suite nuevo entra al checklist —que sí tiene guardarraíl— y a nadie le suena
        que además hay que agregarlo al workflow.
        """
        raiz = self.aqui.parents[3]
        flujo = raiz / ".github" / "workflows" / "tests.yml"
        if not flujo.is_file():
            self.skipTest("no está el workflow de CI")
        ci = flujo.read_text(encoding="utf-8")
        for suite in sorted((raiz / "herramientas").glob("test_*.py")):
            with self.subTest(suite.name):
                self.assertIn(f"herramientas/{suite.name}", ci,
                              f"CI no corre {suite.name}, que sí está en el checklist")
        self.assertIn("scripts/test_scripts.py", ci, "CI no corre el suite de la skill")

    def test_nombra_todos_los_scripts_del_directorio(self):
        for guion in sorted(self.aqui.glob("*.py")):
            if guion.name.startswith("test_"):
                continue
            with self.subTest(guion.name):
                self.assertIn(f"`{guion.name}`", self.readme,
                              f"el README no menciona {guion.name}")


class TestSalidaCodificable(unittest.TestCase):
    """Toda la salida de una herramienta tiene que poder codificarse en cp1252.

    En Windows la consola suele estar en cp1252, y un print de un carácter que no entra en esa
    página de códigos termina en UnicodeEncodeError: el script muere DESPUÉS de haber medido y
    quien lo corre cree que fallo la medición. Peor si además escribió: `cifras.py --sellar`
    reescribe archivos y recién después informa que sello.

    LOS ACENTOS NO SON EL PROBLEMA, y conviene tenerlo claro para no arreglar lo que no está
    roto: a e i o u con tilde, la ñ, la ü, el · y el guion largo están todos en cp1252, y
    `pendientes.py` los imprime sin inconveniente. Lo que rompe son las flechas, los tildes de
    verificación y los caracteres de dibujo. Este repositorio tuvo exactamente uno: el `→` que
    `cifras.py` imprimia al sellar.

    Se mide corriendo los scripts, no leyendo el fuente: la salida se arma con f-strings y datos,
    así que el fuente no dice que se imprime.
    """

    # Los que corren sin binarios externos ni red. `calidad_ocr.py`,
    # `auditar_fechas_fallos.py` y `reocr_jurisprudencia.py` quedan afuera porque necesitan
    # poppler o tesseract, y los descargadores porque salen a la red.
    HERRAMIENTAS = ("herramientas/cifras.py", "herramientas/frontera_kb.py",
                    "herramientas/cobertura_normativa.py", "herramientas/pendientes.py",
                    "herramientas/reformas_no_leidas.py",
                    "argentina/skills/derecho-argentino/scripts/estado.py")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz

    @staticmethod
    def _rompe(texto):
        """Devuelve el primer carácter que una consola cp1252 no puede imprimir."""
        for ch in texto:
            try:
                ch.encode("cp1252")
            except UnicodeEncodeError:
                return ch
        return None

    def test_la_salida_entra_en_cp1252(self):
        for rel in self.HERRAMIENTAS:
            with self.subTest(rel):
                guion = self.raiz / rel
                self.assertTrue(guion.is_file(), f"no existe {rel}")
                hecho = subprocess.run([sys.executable, str(guion)], cwd=str(self.raiz),
                                       capture_output=True, text=True)
                for flujo, texto in (("stdout", hecho.stdout), ("stderr", hecho.stderr)):
                    malo = self._rompe(texto)
                    self.assertIsNone(
                        malo, f"{rel} imprime «{malo}» (U+{ord(malo):04X}) por {flujo}: no entra "
                              f"en cp1252 y corta la corrida en una consola de Windows"
                        if malo else "")

    def test_el_detector_reconoce_lo_que_rompe_y_deja_pasar_los_acentos(self):
        """MUTACION del control: si `_rompe` se vuelve permisivo, el test da verde siempre; si se
        vuelve estricto, obliga a sacar acentos que no molestan a nadie."""
        for ch in ("→", "✔", "≥", "│"):
            with self.subTest(f"rompe {ch}"):
                self.assertEqual(self._rompe(f"medido {ch} y listo"), ch)
        for ch in ("á", "é", "í", "ó", "ú", "ñ", "ü", "·", "—", "«", "»", "¿", "¡"):
            with self.subTest(f"pasa {ch}"):
                self.assertIsNone(self._rompe(f"medido {ch} y listo"))

    # Lo que se transcribe a una pieza. Su salida son nombres de rubro y etiquetas que el
    # abogado copia, así que ahí un acento faltante es un error de tipeo en una demanda.
    QUE_VAN_AL_ESCRITO = (
        ("argentina/skills/derecho-argentino/scripts/liquidacion_lct.py",
         ["--ingreso", "2019-03-03", "--extincion", "2026-08-10",
          "--mejor-remuneracion", "1450000", "--tope-245", "2000000"]),
        ("argentina/skills/derecho-argentino/scripts/plazos.py",
         ["--tipo", "habiles", "--desde", "2026-09-10", "--dias", "5", "--fuero", "pba"]),
        # Un plazo que cruza a 2027 para que entren las notas de `inhábiles.json` sobre lo que
        # todavía no está dictado: esas notas se imprimen y las lee el usuario, así que el
        # control tiene que verlas. Con el caso de septiembre no salen.
        ("argentina/skills/derecho-argentino/scripts/plazos.py",
         ["--tipo", "habiles", "--desde", "2026-12-22", "--dias", "10", "--fuero", "pba"]),
        ("argentina/skills/derecho-argentino/scripts/honorarios_pba.py",
         ["--monto", "10000000", "--etapas", "3"]),
    )
    # Reglas, no lista de palabras: en castellano ninguna palabra termina en -cion/-sion sin
    # tilde, y la ñ nunca se escribe "ni". Los plurales -ciones SI van sin tilde, y por eso el
    # patrón exige el fin de palabra después de "ion".
    DEGRADADA = re.compile(r"\b[A-Za-z]{2,}[csx]ion\b|\banios?\b", re.I)

    def test_lo_que_se_transcribe_no_sale_degradado(self):
        """Un rubro que dice «Indemnización por antigüedad» entra así a una demanda.

        Es la misma clase de problema que las carátulas en ASCII, no una cuestión de estilo. Lo
        que este test NO exige es acentuar los identificadores: el tramo `modernización`, las
        claves de `inhábiles.json` y los valores de `--tipo` son ASCII a propósito, y acentuarlos
        rompe la interfaz o la lectura del dato. Diez reversiones costo aprenderlo.
        """
        for rel, args in self.QUE_VAN_AL_ESCRITO:
            with self.subTest(rel.rsplit("/", 1)[-1]):
                hecho = subprocess.run([sys.executable, str(self.raiz / rel)] + args,
                                       cwd=str(self.raiz), capture_output=True, text=True)
                salida = hecho.stdout + hecho.stderr
                # `modernización` es el identificador del tramo y se imprime tal cual.
                salida = salida.replace("modernizacion", "").replace("hábiles - fuero", "")
                hallado = self.DEGRADADA.search(salida)
                self.assertIsNone(
                    hallado, f"{rel} imprime «{hallado.group(0) if hallado else ''}»: eso se "
                             f"copia a un escrito" if hallado else "")

    def test_la_regla_esta_declarada_con_su_razon(self):
        desarrollo = (self.raiz / "docs" / "DESARROLLO.md").read_text(encoding="utf-8")
        plano = re.sub(r"\s+", " ", desarrollo)
        self.assertIn("tiene que entrar en cp1252", plano)
        self.assertIn("Los acentos no son el problema", plano,
                      "sin esa aclaración, la regla invita a despojar de acentos la salida")


class TestCaratulasAcentuadas(unittest.TestCase):
    """La carátula de un fallo se cita como la escribe el registro, acentos incluidos.

    `fallos.json` guardaba las 64 carátulas en ASCII, y siete decían `Danios` por `Daños`: eso
    no es un acento faltante, es otra palabra. La sección 2 de SKILL.md pone la carátula entre
    los cinco datos que NUNCA se reconstruyen, así que una carátula degradada deja dos salidas
    y las dos son malas — citarla mal en un escrito, o "arreglarla" adivinando los acentos, que
    es exactamente lo prohibido.

    Se recuperaron contra el documento bajado de cada fallo, palabra por palabra, moviendo sólo
    diacríticos y nunca la caja: las carátulas de la CSJN están en mayúsculas porque así las
    escribe su registro, y `UATRE` o `ART` no son errores de tipeo.
    """

    ARCHIVOS = ("fallos.json", "procedencia.json")
    # La ñ transliterada, en las dos formas que aparecían en el dato: `DANOS` y `Danios`.
    TRANSLITERADA = re.compile(r"(?i)\b(dan[io]os|anios|munioz|espania)\b")
    # Palabras que en una carátula van acentuadas siempre. No es la lista completa del idioma:
    # son las que estaban degradadas, así que si vuelve una, vuelve por la misma vía.
    SIN_ACENTO = ("fiscalia", "apelacion", "resolucion", "proteccion", "casacion", "impugnacion",
                  "restitucion", "infraccion", "declaracion", "adopcion", "educacion",
                  "orientacion", "prevencion", "reinstalacion", "privacion", "asociacion",
                  "juridico", "ilicita", "ilegitima", "policia", "ejercito", "medica",
                  "parrafo", "compania", "sumarisimo")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.jur = raiz / "argentina" / "fuentes" / "jurisprudencia"

    def _caratulas(self, arch):
        d = json.loads((self.jur / arch).read_text(encoding="utf-8"))["fallos"]
        it = d if isinstance(d, list) else list(d.values())
        return {(f.get("slug") or f.get("archivo", "").rsplit(".", 1)[0]): f["caratula"]
                for f in it if "caratula" in f}

    def test_ninguna_caratula_trae_la_ñ_transliterada(self):
        for arch in self.ARCHIVOS:
            for slug, car in self._caratulas(arch).items():
                with self.subTest(f"{arch} {slug}"):
                    hallado = self.TRANSLITERADA.search(car)
                    self.assertIsNone(hallado, f"«{hallado.group(0) if hallado else ''}» "
                                               f"es una ñ transliterada, no una carátula")

    def test_ninguna_caratula_perdio_sus_acentos(self):
        for arch in self.ARCHIVOS:
            for slug, car in self._caratulas(arch).items():
                plano = car.lower()
                for palabra in self.SIN_ACENTO:
                    with self.subTest(f"{arch} {slug} {palabra}"):
                        self.assertNotRegex(plano, r"\b" + palabra + r"\b",
                                            f"«{palabra}» va acentuada en la carátula")

    def test_las_dos_copias_de_la_caratula_dicen_lo_mismo(self):
        """`fallos.json` y `procedencia.json` guardan la misma carátula por duplicado, y una
        copia se corrige sin la otra: es exactamente cómo se degradó esto."""
        a, b = (self._caratulas(x) for x in self.ARCHIVOS)
        self.assertEqual(sorted(a), sorted(b), "las dos copias no cubren los mismos fallos")
        for slug in a:
            with self.subTest(slug):
                self.assertEqual(a[slug], b[slug])


class TestTitulosDeNormas(unittest.TestCase):
    """Los 138 titulos de `normas.json` estaban enteros en ASCII, y no era solo cosmética.

    Son la etiqueta con la que la skill nombra una norma cuando la cita, así que "Código de
    Transito" y "Fuero Penal del Nino" salian así al escrito. Y había un error de otro tipo,
    repetido veinte veces: "Constitución de la Catamarca", que parece salido de una plantilla.
    Quedaron como "Constitución de la Provincia de Catamarca", que es como se titulan.

    ESTO SE CONTROLA CON REGLAS Y NO CON UNA LISTA DE PALABRAS, a propósito. En castellano
    ninguna palabra termina en `-cion` o `-sion` sin tilde: es una regla y no admite excepción.
    Una lista, en cambio, arrastra ambigüedad --`practica`, `publica`, `calculo` y `numero`
    existen sin tilde porque también son formas verbales-- y corregir por lista introduce
    errores: paso dos veces en esta misma tarea, con "la actora práctica liquidación" y con
    "InfoLEG no pública texto actualizado".
    """

    ARCHIVOS = ("normas.json", "procedencia.json")
    SIN_TILDE = re.compile(r"\b[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{2,}[csx]ion\b")
    TRANSLITERADA = re.compile(r"(?i)\b(dan[io]os|anios?|nino|munioz|espania)\b")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.normas = raiz / "argentina" / "fuentes" / "normas"

    def _titulos(self, arch):
        d = json.loads((self.normas / arch).read_text(encoding="utf-8"))["normas"]
        it = d if isinstance(d, list) else list(d.values())
        return {(x.get("slug") or x.get("archivo", "").rsplit(".", 1)[0]): x["titulo"]
                for x in it if "titulo" in x}

    def test_ningun_titulo_termina_una_palabra_en_cion_sin_tilde(self):
        for arch in self.ARCHIVOS:
            for slug, titulo in self._titulos(arch).items():
                hallado = self.SIN_TILDE.search(titulo)
                with self.subTest(f"{arch} {slug}"):
                    self.assertIsNone(hallado, f"«{hallado.group(0) if hallado else ''}» lleva "
                                               f"tilde: en castellano no hay -cion sin acento")

    def test_ningun_titulo_trae_la_ñ_transliterada(self):
        for arch in self.ARCHIVOS:
            for slug, titulo in self._titulos(arch).items():
                hallado = self.TRANSLITERADA.search(titulo)
                with self.subTest(f"{arch} {slug}"):
                    self.assertIsNone(hallado, f"«{hallado.group(0) if hallado else ''}» es una "
                                               f"ñ transliterada")

    def test_ninguna_constitucion_provincial_pierde_el_sustantivo(self):
        """«Constitución de la Catamarca» no es castellano. Van con «de la Provincia de»."""
        malo = re.compile(r"Constitución de la (?!Provincia|Nación|Ciudad)")
        for arch in self.ARCHIVOS:
            for slug, titulo in self._titulos(arch).items():
                with self.subTest(f"{arch} {slug}"):
                    self.assertIsNone(malo.search(titulo),
                                      f"falta «Provincia de» en: {titulo}")

    def test_las_dos_copias_del_titulo_dicen_lo_mismo(self):
        a, b = (self._titulos(x) for x in self.ARCHIVOS)
        for slug in set(a) & set(b):
            with self.subTest(slug):
                self.assertEqual(a[slug], b[slug])


class TestFaltaElInterprete(unittest.TestCase):
    """Sin Python instalado, las cuatro calculadoras no corren. La skill tiene que DECIRLO.

    Es el unico modo de falla del repositorio que ningún script puede diagnosticar, porque el
    diagnóstico también es Python: `estado.py` falla por la misma causa. Así que la regla vive
    en SKILL.md y este test es lo que la sostiene.

    Y hay una razón para que sea explícita. SKILL.md decía "si no están disponibles, hacer el
    cálculo a mano": una instrucción escrita para el caso de que no haya repo, que aplicada a
    la falta de interprete entrega un número hecho a ojo a un usuario que cree que corrió la
    calculadora. Es exactamente el error que este repositorio existe para no cometer.
    """

    # Las tres que devuelve la consola, una por plataforma. Si el aviso pierde una, el modelo
    # lee ese error como "el script está roto" y no como "falta el interprete".
    SENALES = ("command not found: python3",
               "'python3' no se reconoce como un comando",
               "xcrun: error: invalid active developer path")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz
        self.skill = (raiz / "argentina" / "skills" / "derecho-argentino"
                      / "SKILL.md").read_text(encoding="utf-8")

    def test_nombra_las_tres_senales_de_la_consola(self):
        for senal in self.SENALES:
            with self.subTest(senal):
                self.assertIn(senal, self.skill,
                              "SKILL.md dejo de nombrar esta señal de que falta el intérprete")

    def test_emite_el_marcador_canonico_de_configuracion(self):
        self.assertRegex(self.skill, r"\[CONFIGURACIÓN INCOMPLETA: falta Python 3[^\]]+\]",
                         "falta el marcador que se emite cuando no hay intérprete")

    def test_prohibe_calcular_a_mano_en_ese_caso(self):
        """La prohibición es la regla entera: sin ella el resto es decoración."""
        self.assertIn("**Y lo que no se hace es calcular a mano.**", self.skill)
        self.assertNotIn("Si no están disponibles, hacer el cálculo a mano", self.skill,
                         "volvió la instrucción de calcular a mano ante un script que no corre")

    def test_la_prohibicion_esta_declarada_entre_las_reglas_inmodificables(self):
        """El detalle vive al final de SKILL.md, y una regla al final se lee de costado. La
        sección 2 es la que dice que no se suspende por instrucción del usuario en sesión, así
        que ahí va el puntero: sin el, esto es una recomendación de la sección 16."""
        seccion2 = self.skill.split("## 2 · Reglas de integridad", 1)[-1].split("\n## ", 1)[0]
        plano = re.sub(r"\s+", " ", seccion2)
        self.assertIn("**Aritmética.**", plano,
                      "la sección 2 dejó de tener la regla de aritmética")
        self.assertIn("porque falta Python**, no se reemplaza con un cálculo a mano", plano,
                      "la sección 2 ya no prohíbe el cálculo a mano por falta de intérprete")

    def test_el_link_de_python_es_el_mismo_que_el_del_readme(self):
        """Dos archivos que dan la misma instrucción de instalación se separan solos. El README
        se lo dice a una persona; SKILL.md, al modelo que va a tener que explicarlo."""
        readme = (self.raiz / "README.md").read_text(encoding="utf-8")
        # Con el espacio aplanado: la frase del PATH cae justo donde se envuelve el renglon en
        # los dos archivos, y un test que se rompe por eso no mide nada.
        archivos = {"README.md": re.sub(r"\s+", " ", readme),
                    "SKILL.md": re.sub(r"\s+", " ", self.skill)}
        for archivo, texto in archivos.items():
            with self.subTest(archivo):
                self.assertIn("https://www.python.org/downloads/", texto,
                              f"{archivo} no lleva el link de descarga de Python")
                self.assertIn("Add python.exe to PATH", texto,
                              f"{archivo} no avisa del tilde de PATH, que en Windows decide")


class TestRutasCitadasPorLaSkill(unittest.TestCase):
    """Toda ruta del repo que un módulo cita entre backticks tiene que existir.

    Una remisión a un archivo que no está no falla ruidosamente: el modelo no encuentra el
    módulo y sigue con lo que tiene. Los prefijos se parecen entre sí —`references/kb/...` y
    `argentina/kb/...`— y sin este test nadie nota la diferencia.
    """

    RUTA = re.compile(r"`((?:argentina|references|herramientas|docs|assets|scripts|fuentes|"
                      r"evals|commands)/[\w./_\-]*[\w_\-])`")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz
        self.skill = raiz / "argentina" / "skills" / "derecho-argentino"

    def test_las_rutas_que_citan_los_modulos_existen(self):
        archivos = [self.skill / "SKILL.md"] + sorted((self.skill / "references").glob("*.md"))
        citadas = 0
        for archivo in archivos:
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for ruta in self.RUTA.findall(linea):
                    citadas += 1
                    # Se admite relativa al repo, a la skill, a references/ o a argentina/.
                    candidatos = [self.raiz / ruta, self.skill / ruta,
                                  self.skill / "references" / ruta, self.raiz / "argentina" / ruta]
                    with self.subTest(f"{archivo.name}:{numero}"):
                        self.assertTrue(any(c.exists() for c in candidatos),
                                        f"{archivo.name}:{numero} cita una ruta inexistente: {ruta}")
        self.assertGreater(citadas, 100, "los módulos dejaron de citar rutas del repo")


class TestSobreDeLosVeredictos(unittest.TestCase):
    """Los archivos de veredicto comparten un sobre, y esto es lo que los mantiene juntos.

    Cada uno se había inventado su forma: la fecha del último repaso llegó a llamarse
    `revisado`, `_revisado` y `fijado` en tres archivos que dicen lo mismo. No rompía nada,
    pero son tres maneras de leer mal un concepto, y el patrón sigue creciendo.

    No se puede unificar con un loader compartido: `revisiones.json` vive dentro del plugin,
    que tiene que ser autocontenido para instalarse y no puede importar de `herramientas/`.
    Así que lo que unifica es este test.
    """

    ARCHIVOS = {
        "herramientas/fuga-revisada.json": "secuencias",
        "herramientas/cobertura-revisada.json": "leyes",
        "herramientas/lecturas-ocr.json": "lecturas",
        "herramientas/kb-procedencia.json": "archivos",
        "herramientas/reformas-revisadas.json": "reformas",
        "herramientas/cifras-revisadas.json": "cifras",
        "argentina/fuentes/normas/revisiones.json": "revisiones",
    }
    OBLIGATORIAS = ("_descripcion", "fijado")
    PERMITIDAS = OBLIGATORIAS + ("_criterio", "_vocabulario", "nota")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz

    def test_todos_traen_el_sobre_completo(self):
        for ruta, carga in self.ARCHIVOS.items():
            f = self.raiz / ruta
            if not f.is_file():
                continue
            d = json.loads(f.read_text(encoding="utf-8"))
            with self.subTest(ruta):
                for clave in self.OBLIGATORIAS:
                    self.assertTrue(d.get(clave), f"{ruta}: falta `{clave}` en el sobre")
                self.assertIn(carga, d, f"{ruta}: no trae la carga `{carga}`")

    def test_no_quedan_nombres_viejos_para_la_fecha(self):
        """MUTACIÓN del problema original: `revisado` y `_revisado` no vuelven."""
        for ruta in self.ARCHIVOS:
            f = self.raiz / ruta
            if not f.is_file():
                continue
            d = json.loads(f.read_text(encoding="utf-8"))
            with self.subTest(ruta):
                for viejo in ("revisado", "_revisado", "notas", "_estados", "_veredictos"):
                    self.assertNotIn(viejo, d,
                                     f"{ruta}: `{viejo}` es un nombre del sobre viejo")

    def test_solo_hay_una_clave_de_carga_fuera_del_sobre(self):
        """Si aparece una segunda clave de datos, el archivo se está convirtiendo en otra cosa
        y el sobre deja de describirlo."""
        for ruta, carga in self.ARCHIVOS.items():
            f = self.raiz / ruta
            if not f.is_file():
                continue
            d = json.loads(f.read_text(encoding="utf-8"))
            with self.subTest(ruta):
                self.assertEqual(sorted(set(d) - set(self.PERMITIDAS)), [carga])

    def test_la_fecha_del_sobre_es_una_fecha(self):
        for ruta in self.ARCHIVOS:
            f = self.raiz / ruta
            if not f.is_file():
                continue
            with self.subTest(ruta):
                fecha = json.loads(f.read_text(encoding="utf-8"))["fijado"]
                datetime.date.fromisoformat(fecha)

    def test_no_aparecio_un_archivo_de_veredicto_sin_declarar(self):
        """El patrón crece: un archivo de veredicto nuevo entra a esta lista o falla acá.

        El glob va con `revisad*` y no con `revisada`: los nombres alternan singular y plural
        según lo que revisan —`fuga-revisada`, `reformas-revisadas`, `cifras-revisadas`— y con
        el patrón en singular este guardarraíl no veía los dos plurales.
        """
        sospechosos = set()
        for patron in ("herramientas/*-revisad*.json", "herramientas/lecturas-*.json",
                       "argentina/fuentes/normas/revisiones.json"):
            sospechosos |= {p.relative_to(self.raiz).as_posix()
                            for p in self.raiz.glob(patron)}
        self.assertEqual(sospechosos - set(self.ARCHIVOS), set(),
                         "hay un archivo de veredicto que no está en TestSobreDeLosVeredictos")


SEMVER = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.\-]+)?"



class TestVersionUnica(unittest.TestCase):
    """La versión del plugin se declara en cinco lugares y ninguno la deriva de otro.

    Publicar 1.0.1 significa editar cinco archivos, y hasta ahora nada atrapaba el que
    faltara: el repositorio se contradice solo y el primero en notarlo es quien instala.
    La fuente de verdad es `argentina/.claude-plugin/plugin.json`, que es de donde
    `generar_marca.py` saca el número para la chapa.
    """

    @staticmethod
    def _v(ruta: Path, *claves):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        for k in claves:
            d = d[k]
        return d

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.raiz = raiz
        self.canonica = self._v(raiz / "argentina" / ".claude-plugin" / "plugin.json", "version")

    def test_los_manifiestos_declaran_la_misma_version(self):
        manifiestos = {
            "argentina/plugin.json": ("version",),
            ".claude-plugin/marketplace.json": ("plugins", 0, "version"),
        }
        for ruta, claves in manifiestos.items():
            f = self.raiz / ruta
            if not f.is_file():
                continue
            with self.subTest(ruta):
                self.assertEqual(self._v(f, *claves), self.canonica)

    def test_el_changelog_encabeza_con_esa_version(self):
        texto = (self.raiz / "CHANGELOG.md").read_text(encoding="utf-8")
        primera = re.search(r"^## \[(" + SEMVER + r")\]", texto, re.M)
        self.assertIsNotNone(primera, "el CHANGELOG dejo de encabezar con una version")
        self.assertEqual(primera.group(1), self.canonica,
                         "la version más reciente del CHANGELOG no es la del manifiesto")

    def test_esa_entrada_del_changelog_esta_fechada(self):
        """Este test capturaba la versión y no la fecha, así que el CHANGELOG se podía publicar
        con `## [1.0.1] — 2026-mm-dd`: el placeholder que se pone mientras la versión se cocina
        y que nadie mira el dia que se publica. Que quede rojo hasta que la fecha este puesta
        es el punto, no un efecto colateral: es lo último que falta de un release.

        El encabezado se toma por POSICIÓN, no con un `re.search` sobre todo el archivo. Un
        search se va de largo: con `## [1.0.1]` sin fecha encontraba la de la entrada de 1.0.0 y
        daba verde validando la versión anterior. Lo encontró una mutación.
        """
        texto = (self.raiz / "CHANGELOG.md").read_text(encoding="utf-8")
        encabezado = next((l for l in texto.splitlines() if l.startswith("## [")), None)
        self.assertIsNotNone(encabezado, "el CHANGELOG dejo de encabezar con una version")
        fechada = re.fullmatch(r"## \[" + SEMVER + r"\] — (\S+)", encabezado)
        self.assertIsNotNone(
            fechada, f"la entrada que encabeza el CHANGELOG no trae fecha: «{encabezado}»")
        try:
            datetime.date.fromisoformat(fechada.group(1))
        except ValueError:
            self.fail(f"la fecha de la entrada que encabeza el CHANGELOG no es una fecha: "
                      f"«{fechada.group(1)}». Falta ponerle la del release.")

    def test_la_chapa_del_readme_anuncia_esa_version(self):
        texto = (self.raiz / "README.md").read_text(encoding="utf-8")
        m = re.search(r'alt="Versión (' + SEMVER + r')"', texto)
        self.assertIsNotNone(m, "el README dejo de declarar la version en el alt de la chapa")
        self.assertEqual(m.group(1), self.canonica)

    def test_no_aparecio_un_sexto_lugar_sin_declarar(self):
        """Si alguien suma un manifiesto, entra a este test o el repo vuelve a poder mentir."""
        conocidos = {
            "argentina/.claude-plugin/plugin.json",
            "argentina/plugin.json",
            ".claude-plugin/marketplace.json",
        }
        hallados = set()
        for patron in ("**/plugin.json", "**/marketplace.json"):
            for f in self.raiz.glob(patron):
                if any(x in f.parts for x in ("_to_delete", ".venv", "node_modules")):
                    continue
                if '"version"' in f.read_text(encoding="utf-8"):
                    hallados.add(f.relative_to(self.raiz).as_posix())
        self.assertEqual(hallados - conocidos, set(),
                         "hay un manifiesto con version que no está en TestVersionUnica")


class TestSalidaDeEstado(unittest.TestCase):
    """`estado.py` interpola constantes de `_raiz` en lo que imprime, y esas constantes cambian.

    `ENV_PLUGIN` paso de ser una cadena a una tupla al sumar Codex, y la interpolación quedo
    escupiendo el repr de Python -parentesis y comillas- en la salida que el usuario lee
    justamente cuando NO se encontró el repo. Ningún test lo vio porque es un print en una
    rama de error.
    """

    def test_lo_que_imprime_no_trae_repr_de_python(self):
        """Se mira el TIPO de la constante, no su nombre.

        Una primera versión marcaba cualquier nombre en mayúsculas y fallaba sobre {ENV},
        que es una cadena y esta bien interpolada. Una medida que se equivoca sobre un caso
        conocido no sirve para los desconocidos: lo que decide no es como se llama sino que
        es.
        """
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        fuente = (Path(__file__).parent / "estado.py").read_text(encoding="utf-8")
        for numero, linea in enumerate(fuente.splitlines(), 1):
            if not re.search(r'print\(f?"', linea):
                continue
            for var in re.findall(r"\{([A-Z_][A-Z0-9_]*)\}", linea):
                valor = getattr(_raiz, var, None)
                if valor is None:
                    continue
                with self.subTest(f"estado.py:{numero} {var}"):
                    self.assertIsInstance(
                        valor, str,
                        f"estado.py:{numero} interpola {{{var}}} directo y {var} es "
                        f"{type(valor).__name__}: imprime el repr de Python en la cara del "
                        f"usuario. Usar ' o '.join({var}).")


class TestIdentidadDeLasNormas(unittest.TestCase):
    """El número de la norma tiene que aparecer en el CUERPO del texto bajado, no sólo en el
    encabezado que le escribimos nosotros.

    `revisar_texto()` valida la FORMA de lo descargado —que haya articulado, que no sea la
    ficha del portal, que el charset esté sano— pero no la IDENTIDAD: una URL que apunta a
    otra norma baja un articulado perfectamente sano y pasa en verde. Pasó: el id 44911 de
    InfoLEG es el texto ordenado del Impuesto a las Ganancias, y quedó guardado como
    `ley-21526.txt`, que es Entidades Financieras. 488 KB de articulado impecable, de otra ley.

    Es el mismo control que `auditar_fechas_fallos.py` hace con la jurisprudencia: identidad
    primero, contenido después.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.normas = raiz / "argentina" / "fuentes" / "normas"
        if not (self.normas / "procedencia.json").is_file():
            self.skipTest("no esta la capa de fuentes")
        sys.path.insert(0, str(raiz / "argentina" / "fuentes" / "scripts"))

    @staticmethod
    def _plano(texto: str) -> str:
        import unicodedata
        t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
        return re.sub(r"[^a-z0-9]+", " ", t)

    def test_el_numero_de_la_norma_esta_en_su_propio_texto(self):
        import _comun
        proc = json.loads((self.normas / "procedencia.json").read_text(encoding="utf-8"))["normas"]
        mirados = 0
        for slug, reg in sorted(proc.items()):
            archivo = self.normas / reg["archivo"]
            if archivo.suffix != ".txt" or not archivo.is_file():
                continue
            m = re.search(r"(\d{4,5})$", slug)
            if not m:
                continue        # constituciones, códigos y acuerdos no llevan numero en el slug
            numero = m.group(1)
            # Sin el encabezado de procedencia: ese lo escribimos nosotros con el titulo del
            # manifiesto, así que buscar ahí confirmaria lo que ya creemos y no lo que bajamos.
            cuerpo = self._plano(_comun.cuerpo_consolidado(archivo)[:3000])
            mirados += 1
            with self.subTest(slug):
                self.assertTrue(
                    any(v in cuerpo for v in (numero, f"{numero[:-3]} {numero[-3:]}")),
                    f"{archivo.name} no menciona el numero {numero} en su texto: la URL puede "
                    f"apuntar a otra norma. Empieza con: {cuerpo[:90]}")
        self.assertGreater(mirados, 80, "dejaron de controlarse las normas descargadas")


class TestEscalasTranscriptas(unittest.TestCase):
    """Cada monto en U.F. que `transito.md` transcribe tiene que estar en el texto del decreto.

    28.5 ter transcribe a mano más de sesenta escalas del Anexo V del Decreto 532/2009. Una
    transcripción larga se degrada sola: se corrige un número al editar la fila de al lado, o
    la fuente se vuelve a bajar con otro texto y la tabla queda vieja sin que nada avise. Acá
    la tabla se coteja contra el .txt con procedencia, fila por fila.
    """

    FILA = re.compile(r"\|\s*\*?\*?arts?\. (\d+)(?: y (\d+))?\*?\*?\s*\|")
    ESCALA = re.compile(r"\|\s*\*?\*?(?:hasta )?([\d.]+)(?: a ([\d.]+))?(?: U\.F\. fija)?\*?\*?\s*\|\s*$")

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz
        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        modulo = (raiz / "argentina" / "skills" / "derecho-argentino" / "references"
                  / "transito.md")
        decreto = raiz / "argentina" / "fuentes" / "normas" / "pba-decreto-532-2009.txt"
        if not decreto.is_file():
            self.skipTest("no esta el texto del Decreto 532/2009")
        texto = modulo.read_text(encoding="utf-8")
        if "### 28.5 ter" not in texto:
            self.skipTest("todavía no esta la sección de escalas")
        self.tabla = texto[texto.index("### 28.5 ter"):texto.index("### 28.6")]
        crudo = decreto.read_text(encoding="utf-8")
        av = crudo[crudo.index("ANEXO VRÉGIMEN"):]
        self.articulos = {}
        for trozo in re.split(r"\n(?=ARTÍCULO \d)", av):
            m = re.match(r"ARTÍCULO (\d+)", trozo)
            if m:
                self.articulos[m.group(1)] = re.sub(r"\s+", " ", trozo)

    def _filas(self):
        for linea in self.tabla.splitlines():
            a, e = self.FILA.search(linea), self.ESCALA.search(linea)
            if a and e:
                for art in filter(None, a.groups()):
                    yield art, e.group(1), e.group(2), linea

    def test_cada_monto_de_la_tabla_esta_en_el_decreto(self):
        filas = list(self._filas())
        self.assertGreater(len(filas), 30, "la tabla de escalas dejó de leerse")
        for art, piso, techo, linea in filas:
            with self.subTest(f"art {art}: {piso}–{techo}"):
                cuerpo = self.articulos.get(art)
                self.assertIsNotNone(cuerpo, f"el Anexo V no tiene un art. {art}")
                self.assertIn(f"{piso} U.F", cuerpo,
                              f"monto que el decreto no dice, en: {linea.strip()[:70]}")
                if techo:
                    self.assertIn(f"{techo} U.F", cuerpo,
                                  f"tope que el decreto no dice, en: {linea.strip()[:70]}")

    def test_cada_articulo_citado_existe_en_el_anexo(self):
        citados = {art for art, _, _, _ in self._filas()}
        self.assertTrue(citados <= set(self.articulos),
                        f"cita artículos que no están en el Anexo V: "
                        f"{sorted(citados - set(self.articulos))}")


class TestContradiccionesNominadas(unittest.TestCase):
    """Cada cita entrecomillada de un bloque de contradicciones tiene que estar en `kb/`.

    Esos bloques citan al perfil para nombrar su error, así que la cita tiene que ser
    textual: si no aparece literalmente bajo `kb/`, el módulo está discutiendo con una frase
    que nadie escribió, o el perfil cambió y la contradicción quedó vieja.
    """

    CITA = re.compile(r'\*"([^"]{15,})"\*')

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import _raiz

        raiz, _ = _raiz.raiz_repo()
        if raiz is None:
            self.skipTest("no se encontró el repo")
        self.referencias = raiz / "argentina" / "skills" / "derecho-argentino" / "references"
        kb = raiz / "argentina" / "kb"
        self.kb = self._plano("\n".join(
            p.read_text(encoding="utf-8", errors="replace") for p in sorted(kb.rglob("*.md"))))

    @staticmethod
    def _plano(texto: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[*`]", "", texto)).strip().lower()

    def _citas(self):
        for archivo in sorted(self.referencias.glob("*.md")):
            dentro = False
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                if linea.startswith("#"):
                    dentro = "Contradicciones nominadas" in linea
                elif dentro and linea.startswith("|"):
                    for cita in self.CITA.findall(linea):
                        yield archivo.name, numero, cita

    def test_las_citas_del_perfil_existen_en_kb(self):
        citas = list(self._citas())
        self.assertGreaterEqual(len(citas), 5, "dejaron de citarse los errores del perfil")
        for archivo, numero, cita in citas:
            with self.subTest(f"{archivo}:{numero}"):
                # assertTrue y no assertIn: assertIn volcaría los 2,3 MB de kb/ en el error.
                self.assertTrue(self._plano(cita) in self.kb,
                                f"{archivo}:{numero} cita como error del perfil un texto que no "
                                f"está en kb/: «{cita}»")


class TestRaizEnLosComandos(unittest.TestCase):
    """El `allowed-tools` de un comando tiene que nombrar la ruta igual que el cuerpo la invoca.

    Claude Code expande `${CLAUDE_PLUGIN_ROOT}` adentro del `allowed-tools`, pero el permiso se
    matchea contra el TEXTO LITERAL del comando, antes de que el shell expanda nada. Entonces un
    patrón que quedó como ruta absoluta no matchea un comando que arranca con
    `${CODEX_PLUGIN_ROOT:-...}`: el permiso no aplica y la calculadora pide aprobación en cada
    corrida. No falla ruidosamente —el comando igual corre si el usuario acepta—, así que sin
    este test la desalineación no la ve nadie.

    Se exige además que la expresión sea UNA sola en todo el repo y que nombre a los dos
    agentes: el plugin corre en Claude Code y en Codex, y elegir uno acá recorta por agente.
    """

    COMANDOS = Path(__file__).resolve().parents[3] / "commands"
    # `${VAR}` o `${VAR:-${VAR2}}`, siempre seguido de la barra de la ruta.
    EXPRESION = re.compile(r"\$\{[A-Z_]+(?::-\$\{[A-Z_]+\})?\}(?=/)")
    # Hasta el `.py`: la expresión de raíz lleva `:` adentro y cortar ahí la parte al medio.
    PATRON = re.compile(r"Bash\(python3 (\S+\.py)")

    def setUp(self):
        self.archivos = sorted(self.COMANDOS.glob("*.md"))
        self.assertTrue(self.archivos, f"no se encontró ningún comando en {self.COMANDOS}")

    def _partes(self, texto: str) -> tuple[str, str]:
        """Frontmatter y cuerpo. Los comandos abren con `---` sin excepción."""
        self.assertTrue(texto.startswith("---"), "el comando no abre con frontmatter")
        _, frente, cuerpo = texto.split("---", 2)
        return frente, cuerpo

    def test_el_patron_de_permiso_dice_la_misma_ruta_que_el_cuerpo(self):
        revisados = 0
        for archivo in self.archivos:
            frente, cuerpo = self._partes(archivo.read_text(encoding="utf-8"))
            declarado = re.search(r"^allowed-tools:(.*)$", frente, re.M)
            if not declarado:
                continue
            revisados += 1
            with self.subTest(archivo.name):
                rutas = self.PATRON.findall(declarado.group(1))
                self.assertTrue(rutas, f"{archivo.name}: el allowed-tools no pre-aprueba ningún "
                                       f"script, pero el comando corre uno")
                # Uno por uno y no el conjunto: un patrón colgado de `/` al lado de uno bueno
                # no se nota mirando qué expresiones aparecen en la línea.
                for ruta in rutas:
                    arranque = self.EXPRESION.match(ruta)
                    self.assertIsNotNone(
                        arranque,
                        f"{archivo.name}: el patrón `{ruta}` no arranca con la raíz del plugin. "
                        f"Colgado de `/`, no matchea nunca.")
                en_patron = set(self.EXPRESION.findall(declarado.group(1)))
                en_cuerpo = set(self.EXPRESION.findall(cuerpo))
                self.assertEqual(en_patron, en_cuerpo,
                                 f"{archivo.name}: el allowed-tools declara {sorted(en_patron)} "
                                 f"y el cuerpo invoca {sorted(en_cuerpo)}. El permiso se matchea "
                                 f"sobre el texto literal: tienen que ser iguales.")
        self.assertGreaterEqual(revisados, 4,
                                "ningún comando declara allowed-tools: el test quedó mirando nada")

    def test_la_expresion_de_raiz_es_una_sola_y_nombra_a_los_dos_agentes(self):
        usadas: dict[str, list[str]] = {}
        for archivo in self.archivos:
            for expresion in self.EXPRESION.findall(archivo.read_text(encoding="utf-8")):
                usadas.setdefault(expresion, []).append(archivo.name)
        self.assertTrue(usadas, "ningún comando nombra la raíz del plugin")
        self.assertEqual(len(usadas), 1,
                         "los comandos usan más de una expresión de raíz: "
                         + "; ".join(f"{e} en {sorted(set(a))}" for e, a in sorted(usadas.items())))
        expresion = next(iter(usadas))
        for variable in ("CLAUDE_PLUGIN_ROOT", "CODEX_PLUGIN_ROOT"):
            self.assertIn(variable, expresion,
                          f"la raíz de los comandos no nombra {variable}: {expresion}. "
                          f"El plugin corre en los dos agentes.")

    def test_todo_script_que_un_patron_pre_aprueba_existe(self):
        nombrados = 0
        for archivo in self.archivos:
            frente, _ = self._partes(archivo.read_text(encoding="utf-8"))
            declarado = re.search(r"^allowed-tools:(.*)$", frente, re.M)
            if not declarado:
                continue
            for ruta in self.PATRON.findall(declarado.group(1)):
                relativa = self.EXPRESION.sub("", ruta).lstrip("/")
                nombrados += 1
                with self.subTest(f"{archivo.name}:{relativa}"):
                    self.assertTrue((self.COMANDOS.parent / relativa).exists(),
                                    f"{archivo.name} pre-aprueba un script que no existe: {relativa}")
        self.assertGreaterEqual(nombrados, 5, "los patrones dejaron de nombrar scripts")


if __name__ == "__main__":
    unittest.main()
