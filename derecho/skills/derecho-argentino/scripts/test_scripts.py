"""Tests de las calculadoras de la skill derecho-argentino. Sin dependencias externas.

    python3 -m unittest discover -s . -p 'test_*.py' -v
"""
import ast
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
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import _raiz
import liquidacion_lct as liq
import plazos

# La raíz del checkout DONDE VIVE este archivo. No se usa `_raiz.raiz_repo()`, que consulta
# `~/.config/derecho-argentino/config.json` antes de subir desde `__file__`: con la ruta fijada
# y un clon distinto, la suite corría contra OTRO repositorio y daba verde. Un test valida el
# checkout en el que está, no el que diga una configuración de la máquina.
RAIZ_DEL_CHECKOUT = Path(__file__).resolve().parents[4]

# Las clases de letras del castellano, en un solo lugar. La diéresis va incluida y NO es un
# detalle: "antigüedad" con diéresis aparece 67 veces en el repositorio y es el núcleo del
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
        # 20/11/2027 cae sábado: ubicación indeterminada por el Decreto 614/2025
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
            for raiz_plugin in (repo, pathlib.Path(repo) / "derecho"):
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
        publica el plugin desde derecho/, así que esa carpeta llega renombrada con el
        nombre del plugin, rodeada de los otros plugins y sin ningún repo arriba. No hay
        un derecho/ que encontrar en ningún lado."""
        repo, _ = _raiz.raiz_repo()
        with tempfile.TemporaryDirectory() as d:
            instalado = pathlib.Path(d) / "plugins" / "synced" / "derecho"
            instalado.mkdir(parents=True)
            for sub in ("fuentes", "kb", "skills", ".claude-plugin"):
                (instalado / sub).symlink_to(pathlib.Path(repo) / "derecho" / sub,
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
        origen = pathlib.Path(repo) / "derecho"
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
        self.assertEqual(_raiz.base(repo), pathlib.Path(repo) / "derecho")
        argentina = pathlib.Path(repo) / "derecho"
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
    """La capa de fuentes no tenía cobertura, y ahí vivió un bug que rebajaba las 59 normas
    en cada corrida. Estas pruebas fijan los dos contratos que lo habrían atajado."""

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
        proc = {"_descripcion": "x", "normas": {"lct-20744": {"sha256_archivo": "abc"}}}
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
        script tratara los bytes como HTML y escribiera un .txt binario de 240 KB. El único
        síntoma era que no se encontraba ni un artículo, que parece un problema de la fuente.
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

    def test_cuerpo_consolidado_contesta_None_y_no_revienta_con_lo_que_no_es_texto(self):
        """Promete `str | None`, así que con un archivo ilegible tiene que devolver `None`.

        No es hipotético: en `normas/` hay cinco entradas que son PDF -la Res. SC 1840/2024,
        dos acuerdos de la SCBA, los tratados del art. 75 inc. 22 y la Constitución de Río
        Negro- y con cualquiera de ellas esto tiraba `UnicodeDecodeError`, porque el `except`
        atrapaba sólo `OSError`. Hoy los llamadores filtran por sufijo y por eso no se veía;
        el que olvide el filtro se lleva una excepción en vez de un `None`.
        """
        import _comun
        with tempfile.TemporaryDirectory() as d:
            pdf = Path(d) / "x.pdf"
            pdf.write_bytes(b"%PDF-1.4\n\xa1\xe2\x9c binario que no es UTF-8")
            self.assertIsNone(_comun.cuerpo_consolidado(pdf))
            self.assertIsNone(_comun.cuerpo_consolidado(Path(d) / "no-existe.txt"))
            sin_encabezado = Path(d) / "y.txt"
            sin_encabezado.write_text("ARTÍCULO 1.- sin las dos rayas\n", encoding="utf-8")
            self.assertIsNone(_comun.cuerpo_consolidado(sin_encabezado))

    def test_el_veredicto_leido_apaga_la_marca_de_ese_problema_y_solo_de_ese(self):
        """revisar_texto() reporta candidatos: hay leyes legítimamente cortas. El veredicto
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

    def test_un_acento_en_el_texto_del_problema_no_apaga_el_veredicto(self):
        """El problema es mensaje y clave a la vez, así que se compara en forma plana.

        PASÓ, y en silencio: `revisar_texto()` decía `articulos` cuando se escribió el
        veredicto de `ley-24754` y después pasó a decir `artículos`. La clave dejó de
        encontrarse, la marca volvió a sonar sobre una norma que nadie había tocado, y quedó
        sentada en la lista de pendientes como si fuera un defecto nuevo. Comparar por el
        texto exacto convierte cualquier corrección de ortografía en una falsa alarma.
        """
        import _comun
        self.assertEqual(_comun.plano("Solo 2 artículos  en 1.430 CARACTERES"),
                         "solo 2 articulos en 1.430 caracteres")
        with tempfile.TemporaryDirectory() as d:
            arch = Path(d) / "revisiones.json"
            arch.write_text(json.dumps({
                "_descripcion": "veredictos de prueba", "fijado": "2026-09-14",
                "revisiones": {"ley-x": [
                    {"problema": "solo 2 articulos en 1430 caracteres: sospechosamente corto",
                     "veredicto": "leido", "fecha": "2026-09-14"}]}}), encoding="utf-8")
            original = _comun.REVISIONES
            try:
                _comun.REVISIONES = arch
                leidos = _comun.cargar_revisiones()
            finally:
                _comun.REVISIONES = original
        acentuado = "solo 2 artículos en 1430 caracteres: sospechosamente corto"
        self.assertIn(_comun.plano(acentuado), leidos["ley-x"])

    def test_los_veredictos_del_repositorio_apagan_las_marcas_que_dicen_apagar(self):
        """Un veredicto escrito que ya no matchea es peor que no tenerlo: la marca vuelve.

        Se comprueba contra lo que `revisar_texto()` redacta HOY, no contra una copia. Si
        alguien reescribe un mensaje de `revisar_texto()`, este test dice cuál veredicto
        quedó huérfano en vez de dejar que la marca reaparezca en la próxima descarga.
        """
        import _comun
        raiz = RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "normas"
        if not (raiz / "revisiones.json").is_file():
            self.skipTest("no esta la capa de fuentes")
        crudo = json.loads((raiz / "revisiones.json").read_text(encoding="utf-8"))
        proc = json.loads((raiz / "procedencia.json").read_text(encoding="utf-8"))["normas"]
        leidos = _comun.cargar_revisiones()
        huerfanos = []
        for slug, entradas in crudo.get("revisiones", {}).items():
            marcadas = proc.get(slug, {}).get("revisar", [])
            for e in entradas:
                if any(_comun.plano(m) == _comun.plano(e["problema"]) for m in marcadas):
                    huerfanos.append(f"{slug}: «{e['problema'][:60]}» tiene veredicto y sigue "
                                     f"marcada en procedencia.json")
            self.assertIn(slug, leidos)
        self.assertEqual(huerfanos, [], "\n  ".join(huerfanos))

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
        el patrón va anclado a los rótulos del portal y no busca fechas sueltas."""
        import _comun
        for intacto in ("ARTÍCULO 1°.- Rige desde el 14 de Septiembre de 2026.\n",
                        "DADA EN BUENOS AIRES, A LOS 14 de Septiembre de 2026.\n",
                        "Sancionada: 8 de Febrero de 1995\nPromulgada: 1 marzo 1995\n"):
            with self.subTest(intacto[:30]):
                self.assertEqual(_comun.normalizar_cromo(intacto), intacto)

    def test_el_cromo_removido_deja_rastro_visible(self):
        """Si se borrara el renglón sin decir nada, quien lea el .txt ve dos líneas de maqueta
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
            N = Path(d) / "derecho" / "fuentes" / "normas"
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
            N = Path(d) / "derecho" / "fuentes" / "normas"
            N.mkdir(parents=True)
            (N.parent / "datos").mkdir()
            (N / "normas.json").write_text(json.dumps(
                {"normas": [{"slug": "una", "url": "http://x/1"}]}), encoding="utf-8")
            (N / "procedencia.json").write_text(json.dumps(
                {"normas": {"una": {"archivo": "una.txt"}}}), encoding="utf-8")
            filas = estado.revisar(Path(d))
            fila = next(f for f in filas if f["bloque"] == "descargas")
            self.assertIn("faltan 1", fila["detalle"])

    def test_la_linea_de_progreso_se_borra_antes_del_resultado(self):
        """`\\r` mueve el cursor pero NO borra, y la línea de aviso es más larga que el resultado.

        Se veía en pantalla como `28,551 bytesjn.gov.ar`: los bytes del fallo y, pegado sin
        separación, el resto del host que se estaba pidiendo. Parecía un archivo con el nombre
        corrompido, y a un corpus de setenta fallos eso manda a revisar procedencias que están
        perfectas. Lo que se fija acá es que la limpieza cubra TODO el ancho del aviso.
        """
        import descargar_normas as dn
        import urllib.parse
        # La invariante NO es que el resultado sea corto: uno más largo que el aviso lo tapa
        # entero y no deja nada. Lo que hay que sostener es que el AVISO no exceda lo que la
        # limpieza borra, porque `ljust` rellena pero no recorta: un slug largo con un host largo
        # pasa de ANCHO_AVISO y la cola vuelve a quedar visible.
        fuentes = RAIZ_DEL_CHECKOUT / "derecho" / "fuentes"
        entradas = json.loads((fuentes / "normas" / "normas.json").read_text(
            encoding="utf-8"))["normas"]
        entradas += json.loads((fuentes / "jurisprudencia" / "fallos.json").read_text(
            encoding="utf-8"))["fallos"]
        medidos, mas_largo = 0, ("", 0)
        for e in entradas:
            if not e.get("url"):
                continue
            medidos += 1
            host = urllib.parse.urlsplit(e["url"]).netloc
            aviso = f"  bajando     {e['slug']:28} {host[:40]}".ljust(dn.ANCHO_AVISO)
            if len(aviso) > mas_largo[1]:
                mas_largo = (e["slug"], len(aviso))
            with self.subTest(e["slug"]):
                self.assertLessEqual(len(aviso), dn.ANCHO_AVISO,
                                     f"el aviso de este slug mide {len(aviso)} y la limpieza "
                                     f"borra {dn.ANCHO_AVISO}: subir ANCHO_AVISO")
        self.assertGreater(medidos, 100, "no se midió casi ningún slug real")
        self.assertEqual(mas_largo[1], dn.ANCHO_AVISO,
                         f"el aviso más largo ({mas_largo[0]}) mide {mas_largo[1]}: si quedó por "
                         f"debajo de ANCHO_AVISO, el relleno dejó de aplicarse")

    def test_el_arrastre_no_cuenta_lo_de_esta_corrida(self):
        """Un recuento que suma dos veces lo mismo se deja de leer.

        Con `--forzar` sobre el manifiesto entero, el aviso de arrastre decía "6 de corridas
        anteriores" cuando cinco de esas seis acababan de imprimirse tres renglones más arriba.
        El número útil es el de las que la corrida NO tocó.
        """
        marcadas = ["decreto-659-1996", "ley-24754", "pba-ley-11653"]
        registro = {s: {"revisar": ["x"]} for s in marcadas}
        registro["cn-tratados-ddhh"] = {"revisar": ["sin URL oficial"]}
        registro["lct-20744"] = {"sha256_texto": "abc"}
        arrastre = sorted(s for s, r in registro.items()
                          if r.get("revisar") and s not in marcadas)
        self.assertEqual(arrastre, ["cn-tratados-ddhh"])
        # Y la fuente tiene que restar de verdad, no sólo este cálculo de juguete.
        fuente = (RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "scripts"
                  / "descargar_normas.py").read_text(encoding="utf-8")
        self.assertIn("s not in marcadas", fuente,
                      "el arrastre volvió a contar las marcadas en esta misma corrida")

    def test_no_poder_comparar_no_se_informa_como_cambio(self):
        """La alarma de reforma tiene tres estados, y confundir dos vale un falso positivo.

        Cuando la extracción del texto falla, o cuando no hay hash guardado con qué contrastar,
        antes se informaba CAMBIO: eso manda a alguien a buscar una reforma que no existe. Una
        alarma que hace eso seguido se aprende a ignorar, y ahí se pierde el cambio real.
        """
        import verificar_normas as vn
        pagina = b"<html><body><p>ARTICULO 1 - texto</p></body></html>"
        from _comun import ATexto, sha256_texto
        parser = ATexto()
        parser.feed(pagina.decode())
        propio = sha256_texto(parser.texto() + "\n")

        estado, _ = vn.comparar({"archivo": "x.txt", "sha256_texto": propio}, pagina, "utf-8")
        self.assertEqual(estado, "sin cambios")
        estado, detalle = vn.comparar({"archivo": "x.txt", "sha256_texto": "otro"}, pagina, "utf-8")
        self.assertEqual(estado, "cambio")
        self.assertIn("texto de la norma", detalle)
        # Sin hash guardado no se sabe: NO es cambio.
        estado, detalle = vn.comparar({"archivo": "x.txt"}, pagina, "utf-8")
        self.assertEqual(estado, "sin medir")
        self.assertIn("con qué contrastar", detalle)
        # Un PDF se compara byte a byte y por su propio campo.
        crudo = b"%PDF-1.4 lo que sea"
        from _comun import sha256
        self.assertEqual(vn.comparar({"archivo": "x.pdf", "sha256_archivo": sha256(crudo)},
                                     crudo, None)[0], "sin cambios")
        self.assertEqual(vn.comparar({"archivo": "x.pdf", "sha256_archivo": "otro"},
                                     crudo, None)[0], "cambio")

    def test_verificar_normas_no_sella_la_jurisprudencia(self):
        """`--sellar` no puede tocar `fallos.json`: este script no verifica ni un fallo.

        Lo hacía, y el sello significa "esto se comprobó contra la fuente oficial y coincide".
        O sea que afirmaba eso sobre setenta sentencias que nadie miró, y `estado.py` lo mostraba
        como `[ok] fallos ... verificados hace N días`. La jurisprudencia no tiene verificador;
        mientras no lo tenga, su fecha no se escribe desde acá.
        """
        fuente = (RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "scripts"
                  / "verificar_normas.py").read_text(encoding="utf-8")
        # Se busca la construcción de la RUTA, no la palabra: el script nombra `fallos.json` a
        # propósito, en la línea que aclara que no lo sella. Prohibir la mención dejaría el test
        # rojo por decir la verdad.
        self.assertNotRegex(fuente, r'RAIZ\s*/\s*"jurisprudencia"',
                            "verificar_normas.py volvió a armar la ruta del manifiesto de "
                            "jurisprudencia: si es para sellarlo, está afirmando una "
                            "verificación que no hace")

    def test_la_jurisprudencia_no_guarda_una_fecha_que_nadie_escribe(self):
        """Ni `fallos.json` ni su procedencia llevan fecha de verificación, y es a propósito.

        Las dos estuvieron: `fallos.json` con `verificado` y `procedencia.json` con `cotejado`
        en el primer nivel. Ningún script escribía ninguna de las dos --el único que podría,
        `verificar_normas.py`, se excluye a sí mismo porque no verifica fallos-- así que eran
        fechas tipeadas a mano que envejecían solas. La de `fallos.json` encima salía por
        `estado.py` como `[ok] fallos ... verificados hace N días`: una verificación que nadie
        hizo, presentada en verde. Es la alarma que no suena nunca.

        Lo que sí se mide de un fallo va sin fecha, porque no vence: la identidad contra la
        carátula, que el descargador escribe en `cotejo` en cada bajada, y el hash, que el
        suite controla en cada corrida. Una sentencia firme no cambia.
        """
        J = RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "jurisprudencia"
        if not (J / "fallos.json").is_file():
            self.skipTest("no esta la capa de fuentes")
        for nombre in ("fallos.json", "procedencia.json"):
            datos = json.loads((J / nombre).read_text(encoding="utf-8"))
            sueltas = [k for k, v in datos.items()
                       if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", v)]
            self.assertEqual(sueltas, [],
                             f"jurisprudencia/{nombre} volvió a llevar una fecha en el primer "
                             f"nivel ({', '.join(sueltas)}). Ningún script la escribe, así que "
                             f"envejece sola y se lee como una medición que nadie hizo. Lo que "
                             f"se mide de un fallo -identidad y hash- no lleva fecha.")

    def test_estado_reporta_el_cotejo_de_identidad_de_los_fallos(self):
        """El bloque `fallos` de `estado.py` censa el cotejo, y un fallo sin cotejar no pasa.

        Los tres estados se cuentan distinto y el tercero es el que importa: `no aplica` es
        permanente y legítimo -carátula anonimizada- así que no puede pintar de rojo; `revisar`
        y "no figura el cotejo" sí, porque los dos significan que nadie confirmó que el archivo
        sea el fallo declarado, que es el peor error posible acá.
        """
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        with tempfile.TemporaryDirectory() as d:
            J = Path(d) / "derecho" / "fuentes" / "jurisprudencia"
            J.mkdir(parents=True)
            (J.parent / "datos").mkdir()
            (J / "fallos.json").write_text(json.dumps({"fallos": [
                {"slug": "a"}, {"slug": "b"}, {"slug": "c"}]}), encoding="utf-8")

            def fila(proc):
                (J / "procedencia.json").write_text(json.dumps({"fallos": proc}),
                                                    encoding="utf-8")
                return next(f for f in estado.revisar(Path(d)) if f["bloque"] == "fallos")

            f = fila({"a": {"cotejo": "cotejado: x"}, "b": {"cotejo": "no aplica: y"},
                      "c": {"cotejo": "cotejado: z"}})
            self.assertEqual(f["estado"], "OK")
            self.assertIn("2 cotejados", f["detalle"])
            self.assertIn("1 sin apellido que cotejar", f["detalle"])
            self.assertNotIn("días", f["detalle"], "volvió la fecha de verificación")

            f = fila({"a": {"cotejo": "cotejado: x"}, "b": {"cotejo": "no aplica: y"},
                      "c": {"cotejo": "revisar: no menciona el apellido"}})
            self.assertEqual(f["estado"], "REVISAR")
            self.assertIn("1 a revisar", f["detalle"])

            # El que no figura en procedencia no se cotejó nunca, y eso no es "está bien".
            f = fila({"a": {"cotejo": "cotejado: x"}, "b": {"cotejo": "no aplica: y"}})
            self.assertEqual(f["estado"], "REVISAR")
            self.assertIn("1 sin cotejar", f["detalle"])

    def test_el_comando_que_sugiere_verificar_normas_es_ejecutable(self):
        """Es salida que alguien copia y pega, y se rompió sin que nada avisara.

        La concatenación quedó como `"...--forzar ".join(slugs)`: con un slug imprime el slug sin
        comando, y con dos mete el comando ENTRE los dos slugs. Una sugerencia mal armada no falla
        ruidosamente, se pega en la terminal y ahí se ve.
        """
        import verificar_normas as vn
        uno = vn.comando_para_rebajar(["lct-20744"])
        self.assertIn("python3 descargar_normas.py --forzar --slug lct-20744", uno)
        dos = vn.comando_para_rebajar(["lct-20744", "pba-ley-11653"])
        self.assertIn("--forzar --slug lct-20744 --slug pba-ley-11653", dos)
        self.assertEqual(dos.count("python3"), 1, "el comando aparece más de una vez")

    def test_los_sitios_del_diagnostico_siguen_siendo_los_del_manifiesto(self):
        """Las URLs de `diagnostico.py` duplican las de `normas.json`, y una copia se vence.

        Si el manifiesto cambia una URL, el diagnóstico sigue probando la vieja e informa que el
        sitio anda sobre una dirección que nadie usa. La excepción es la API de series, que no es
        una norma y por eso no está en ese catálogo.
        """
        import diagnostico
        catalogo = json.loads((RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "normas"
                               / "normas.json").read_text(encoding="utf-8"))["normas"]
        urls = {n.get("url") for n in catalogo}
        for nombre, url in diagnostico.SITIOS:
            with self.subTest(nombre):
                if "apis.datos.gob.ar" in url:
                    continue
                self.assertIn(url, urls,
                              f"{nombre} prueba una URL que ya no está en normas.json")

    def test_la_continuidad_de_una_serie_detecta_hueco_y_repetido(self):
        """Un mes faltante o repetido no rompe nada visible, y cambia el resultado.

        `intereses.py` actualiza entre dos períodos y toma lo que encuentra: el CSV queda bien
        formado, el cálculo sale distinto y no hay síntoma. Era el defecto que ningún control
        miraba, porque el único que había —el ancla del IPC— comprueba un valor y no la forma de
        la serie, y encima sólo existe para una de las tres.
        """
        import descargar_series as ds
        limpia = [("2026-01", 1.0), ("2026-02", 2.0), ("2026-03", 3.0)]
        self.assertIsNone(ds.continuidad(limpia))
        # El salto de año no es un hueco: diciembre a enero son meses consecutivos.
        self.assertIsNone(ds.continuidad([("2025-12", 1.0), ("2026-01", 2.0)]))
        hueco = ds.continuidad([("2026-01", 1.0), ("2026-03", 3.0)])
        self.assertIsNotNone(hueco)
        self.assertIn("2026-01", hueco)
        repetido = ds.continuidad([("2026-01", 1.0), ("2026-01", 1.5), ("2026-02", 2.0)])
        self.assertIsNotNone(repetido)
        self.assertIn("repetidos", repetido)

    def test_no_se_sobreescribe_una_serie_con_menos_periodos(self):
        """`--desde` posterior reescribía el archivo con menos datos y nada avisaba.

        Acá no hay historial de git al que volver: lo que se borra se borra. Y la pérdida es
        invisible en el archivo resultante, que sigue estando bien formado.
        """
        import descargar_series as ds
        with tempfile.TemporaryDirectory() as d:
            csv = Path(d) / "serie-x.csv"
            self.assertIsNone(ds.periodos_en_disco(csv), "un archivo que no existe no tiene nada")
            csv.write_text("# comentario\n# otro\nperiodo,indice\n2026-01,1.0\n2026-02,2.0\n",
                           encoding="utf-8")
            self.assertEqual(ds.periodos_en_disco(csv), 2,
                             "cuenta comentarios o el encabezado como datos")

    def test_la_nota_de_una_serie_llega_entera_al_csv(self):
        """Se compara contra los CSV EN DISCO, que es lo que el script escribió de verdad.

        Comprobar el `textwrap` que el test calcula por su cuenta no mide nada: si alguien vuelve
        a partir la nota por oraciones, el test seguiría verde y el archivo saldría roto. Y era un
        defecto real: partir en ". " se come las abreviaturas del castellano jurídico, y la nota
        del RIPTE quedó escrita como "usa el art." y "12 LRT texto Ley 27.348" en dos renglones,
        o sea una cita quebrada dentro de un archivo de datos que alguien lee para saber qué serie
        tiene.
        """
        import descargar_series as ds
        datos = RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "datos"
        mirados = 0
        for nombre, cfg in ds.SERIES.items():
            csv = datos / f"serie-{nombre}.csv"
            if not csv.is_file():
                continue
            mirados += 1
            with self.subTest(nombre):
                comentarios = [l[1:].strip() for l in csv.read_text(encoding="utf-8").splitlines()
                               if l.startswith("#")]
                for renglon in comentarios:
                    self.assertFalse(re.search(r"\b(art|inc|arts|cf|conf|ss)\.$", renglon),
                                     f"un renglón del encabezado corta una cita: «{renglon}»")
                # Y la nota tiene que estar completa, no sólo sin cortes: se busca su texto
                # normalizado dentro del bloque de comentarios.
                self.assertIn(" ".join(cfg["nota"].split()), " ".join(" ".join(comentarios).split()),
                              "la nota de la serie no llegó completa al archivo")
        self.assertGreater(mirados, 0, "no había ningún CSV contra el que comparar")

    def test_la_paginacion_no_corta_por_una_fila_vacia(self):
        """La condición de corte mira la página CRUDA, no la filtrada.

        Con el largo del cuerpo ya filtrado, basta una fila con el período vacío en una página
        completa para que queden 999, el bucle corte y falten TODOS los períodos siguientes. El
        archivo sale bien formado y con menos datos.
        """
        import descargar_series as ds
        paginas, pedidos = [], []

        def falso_bajar(url, **kw):
            pedidos.append(url)
            return paginas.pop(0).encode("utf-8"), "utf-8", "text/csv"

        # Primera página: 1000 filas crudas, una de ellas sin período. Segunda: el resto.
        filas = ["indice_tiempo,valor"]
        filas += [""] + [f"2000-{i % 12 + 1:02d}-01,{i}" for i in range(ds.PAGINA - 1)]
        paginas.append("\n".join(filas))
        paginas.append("indice_tiempo,valor\n2026-01-01,9\n")
        original = ds.bajar
        ds.bajar = falso_bajar
        try:
            devueltas = ds.pedir({"id": "x"}, "2000-01")
        finally:
            ds.bajar = original
        self.assertEqual(len(pedidos), 2,
                         "cortó en la primera página: la fila vacía volvió a truncar la serie")
        self.assertEqual(len(devueltas), ds.PAGINA - 1 + 1,
                         "no juntó las dos páginas sin la fila vacía")

    def test_un_slug_inexistente_corta_antes_de_bajar(self):
        """Un dedazo en `--slug` no puede terminar en "0 bajadas" y código 0.

        Es el peor no-op posible: el pedido no se cumplió, nada lo dijo, y quien lo corrió cree
        que la norma está bajada. `reocr_jurisprudencia.py` ya se plantaba; los dos descargadores
        -que además son los que salen a la red- seguían de largo.
        """
        import descargar_normas as dn
        catalogo = [{"slug": "lct-20744", "prioridad": 1}, {"slug": "pba-ley-11653",
                                                            "prioridad": 2}]
        with self.assertRaises(SystemExit) as caso:
            dn.seleccionar(catalogo, ["lct-20744", "lct-2074"], None)
        self.assertIn("lct-2074", str(caso.exception))
        self.assertNotIn("lct-20744,", str(caso.exception), "acusó al slug que sí existe")
        # Y sin slugs no molesta, que es el caso normal.
        self.assertEqual(len(dn.seleccionar(catalogo, [], None)), 2)

    def test_prioridad_cero_no_se_confunde_con_no_haber_pedido_prioridad(self):
        """`if a.prioridad:` daba falso con 0 y bajaba el manifiesto ENTERO.

        O sea: se pedía el subconjunto más chico posible y se disparaban ciento cuarenta y siete
        pedidos a InfoLEG y normas.gba. Un filtro numérico se compara contra None, nunca por su
        verdad, porque el cero es un valor y no una ausencia.
        """
        import descargar_normas as dn
        catalogo = [{"slug": "a", "prioridad": 1}, {"slug": "b", "prioridad": 2},
                    {"slug": "c", "prioridad": 3}]
        self.assertEqual([n["slug"] for n in dn.seleccionar(catalogo, [], 0)], [])
        self.assertEqual([n["slug"] for n in dn.seleccionar(catalogo, [], 1)], ["a"])
        self.assertEqual(len(dn.seleccionar(catalogo, [], None)), 3,
                         "sin --prioridad se baja todo")

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
        """Y no debe saltar por las variantes de carátula entre repositorios: número de causa,
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

    def test_confirmar_identidad_parte_la_caratula_por_la_s_de_sobre(self):
        """`s/` es el separador más común de una carátula argentina y faltaba en el corte.

        Sin él, una carátula sin coma antes del `s/` -las de la CSJN en mayúsculas- dejaba
        `cabeza` con la carátula ENTERA, objeto del proceso y número de causa incluidos, y esa
        cadena de noventa caracteres no aparece nunca en el cuerpo. Medido sobre el corpus: seis
        fallos correctos daban "puede ser OTRO fallo", entre ellos "Simón", "Casal" y "Arancibia
        Clavel". Es la alarma que suena mal, que es como se termina apagando un control.
        """
        import descargar_jurisprudencia as dj
        casos = (
            ("SIMÓN JULIO HÉCTOR Y OTROS s/PRIVACIÓN ILEGÍTIMA DE LA LIBERTAD ETC. "
             "-CAUSA N 17.768-", "en la causa Simón, Julio Héctor y otros, para decidir"),
            ("CASAL MATÍAS EUGENIO Y OTRO s/ROBO SIMPLE EN GRADO DE TENTATIVA -CAUSA N 1681-",
             "recurso de hecho deducido en la causa Casal, Matías Eugenio"),
            ("QUARANTA JOSÉ CARLOS s/INF. LEY 23.737 -CAUSA N 763-",
             "autos: Quaranta, José Carlos s/ infracción ley 23.737"),
        )
        for caratula, cuerpo in casos:
            with self.subTest(caratula[:28]):
                self.assertIsNone(dj.confirmar_identidad(cuerpo, caratula),
                                  "un fallo correcto quedó marcado como si fuera otro")
        # Y no se vuelve permisivo: partido por `s/`, sigue detectando el fallo cambiado.
        self.assertIsNotNone(dj.confirmar_identidad(
            "en la causa Llerena, Horacio Luis s/ abuso de armas",
            "ACOSTA ALEJANDRO ESTEBAN s/INFRACCIÓN ART. 14 LEY 23.737 -CAUSA N 28/05-"))

    def test_una_caratula_anonimizada_no_pasa_por_cotejada(self):
        """En familia y minoridad la carátula viene anonimizada y no hay apellido que cotejar.

        Ahí no hay medida posible: una inicial aparece en cualquier documento. Lo que no puede
        pasar es que salga indistinguible de un fallo que sí pasó el control -en el corpus son
        diez de setenta-, así que el estado es «no aplica» y queda registrado. Tampoco puede ir a
        `revisar`: sería una alarma que suena en cada corrida y se dejaría de mirar.
        """
        import descargar_jurisprudencia as dj
        for caratula in ("E., M. R. c/ L., M. F. s/ Acción de compensación económica",
                         "P., S. M. y otro s/ homicidio simple",
                         "R., V. S. contra D., G. J. Tenencia de hijo"):
            with self.subTest(caratula[:26]):
                self.assertFalse(dj.es_cotejable(caratula))
                estado, detalle = dj.cotejar_identidad(Path("no-se-usa"), b"", None, False,
                                                       caratula)
                self.assertEqual(estado, "no aplica")
                self.assertIn("anonimizada", detalle)
        self.assertTrue(dj.es_cotejable("Fiorentino, Diego Enrique."))

    def test_sin_apellido_todavia_queda_el_expediente(self):
        """Que no haya apellido no es que no haya nada que cotejar.

        El mensaje de `no aplica` decía que «la identidad del documento se confirma por la
        cita», y NADIE comprobaba la cita: era una afirmación en un string, no un control. Sin
        apellido queda el expediente, que el documento sí trae impreso —«C. 122.501», «CIV
        86767/2015»—, y ése se coteja. En el corpus de hoy eso convierte cinco de diez
        anonimizados en cotejados de verdad.

        Los otros cinco son de la CSJN y su causa declarada es la cita de Fallos, que se asigna
        al PUBLICAR y no está impresa en la sentencia: ahí sigue sin haber control mecánico, y
        el mensaje ahora lo dice en vez de sugerir lo contrario.

        MUTACIÓN que lo demuestra: cambiar el número de causa por otro tiene que devolver
        `no aplica` en vez de `cotejado`.
        """
        import descargar_jurisprudencia as dj
        cuerpo = b"<html><body>Causa N 122.501. Sentencia. R., V. S. contra D., G. J.</body></html>"
        anonima = "R., V. S. contra D., G. J. s/ Tenencia de hijo"

        estado, detalle = dj.cotejar_identidad(Path("x"), cuerpo, None, False, anonima,
                                               "C. 122.501")
        self.assertEqual(estado, "cotejado", "el expediente está en el documento")
        self.assertIn("122", detalle)

        estado, detalle = dj.cotejar_identidad(Path("x"), cuerpo, None, False, anonima,
                                               "C. 999.999")
        self.assertEqual(estado, "no aplica", "el expediente NO está: no se da por cotejado")

        # La cita de Fallos no es un expediente y no se coteja contra el cuerpo.
        estado, detalle = dj.cotejar_identidad(Path("x"), cuerpo, None, False, anonima,
                                               "Fallos 346:287")
        self.assertEqual(estado, "no aplica")
        self.assertIn("Fallos", detalle, "el mensaje tiene que decir POR QUÉ no se pudo")

        # Y sin causa declarada, tampoco.
        estado, _ = dj.cotejar_identidad(Path("x"), cuerpo, None, False, anonima, "")
        self.assertEqual(estado, "no aplica")

    def test_el_cotejo_de_un_pdf_ilegible_no_pasa_por_cotejado(self):
        """No hay verde por ausencia de instrumento.

        Un PDF del que no se puede extraer texto -o para el que falta `pdftotext`- tiene que
        quedar distinguible de uno cotejado y aprobado, o el registro afirma un cotejo que nunca
        ocurrió. Y va a `revisar`, no a «no aplica»: acá el cotejo SÍ se puede hacer, lo que falta
        es la herramienta, y eso se arregla.
        """
        import descargar_jurisprudencia as dj
        with tempfile.TemporaryDirectory() as d:
            falso = Path(d) / "no-es-un-pdf.pdf"
            falso.write_bytes(b"esto no es un PDF")
            estado, detalle = dj.cotejar_identidad(falso, b"", None, True,
                                                   "Acosta, Alejandro Esteban")
            self.assertEqual(estado, "revisar", "un PDF ilegible pasó por cotejado")
            self.assertIn("cotejar", detalle)

    def test_un_pdf_sin_capa_de_texto_coteja_contra_la_recuperacion_por_ocr(self):
        """Un escaneo puro no tiene capa de texto, y su recuperación en `ocr/` sí sirve de cotejo.

        Es el caso de los fallos anteriores al corte de 1994, que el visor de la Corte devuelve
        como imagen del tomo impreso. Sin esta rama la marca de `revisar` no se puede apagar
        NUNCA: `reocr_jurisprudencia.py` escribe en `ocr/` y no toca el PDF, así que volver a
        bajar da el mismo resultado. Una alarma que no se puede apagar se deja de mirar, y con
        ella las que sí importan.

        MUTACIÓN QUE LO RESPALDA: sacar `ocr/<slug>.txt` y volver a cotejar. Sin el archivo
        vuelve «revisar» y el detalle manda correr el reOCR; con él, «cotejado» diciendo que se
        leyó de la recuperación. Las dos mitades importan: si el detalle no dijera por dónde se
        cotejó, el registro haría creer que el PDF era legible.
        """
        import descargar_jurisprudencia as dj
        sys.path.insert(0, str(RAIZ_DEL_CHECKOUT / "herramientas"))
        import _externos
        if _externos.falta("pdftotext"):
            # Sin poppler, `texto_de_pdf` devuelve vacío por FALTA DE HERRAMIENTA y no por
            # falta de capa de texto, así que `cotejar_identidad` toma la rama de «falta
            # pdftotext» —que es lo correcto— y este test mediría otra cosa. El fixture no
            # puede distinguir los dos vacíos: por eso se declara acá y no se adivina.
            self.skipTest("sin poppler: el cotejo contra `ocr/` no se puede ejercitar")
        with tempfile.TemporaryDirectory() as d:
            escaneo = Path(d) / "csjn-ejemplo-fallos-310-380.pdf"
            # PDF válido de una página vacía: `pdftotext` corre y devuelve sólo el salto de
            # página. Es la diferencia con un archivo roto, que no se parsea y cae en la rama
            # de «falta pdftotext»: acá la herramienta está y el documento no tiene texto.
            escaneo.write_bytes(
                b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
                b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
                b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
                b"trailer<</Root 1 0 R>>\n%%EOF\n")
            self.assertFalse((dj.texto_de_pdf(escaneo) or "").strip(),
                             "el fixture tiene que quedar SIN capa de texto")
            (Path(d) / "ocr").mkdir()

            estado, detalle = dj.cotejar_identidad(escaneo, b"", None, True, "Bodegas y Viñedos Giol")
            self.assertEqual(estado, "revisar", "sin recuperación tiene que quedar marcado")
            self.assertIn("reocr", detalle)

            (Path(d) / "ocr" / "csjn-ejemplo-fallos-310-380.txt").write_text(
                "Vistos los autos: Bodegas y Viñedos Giol E.E.I. y C. c/ Dirección General",
                encoding="utf-8")
            estado, detalle = dj.cotejar_identidad(escaneo, b"", None, True, "Bodegas y Viñedos Giol")
            self.assertEqual(estado, "cotejado", "con recuperación tiene que cotejar")
            self.assertIn("OCR", detalle,
                          "el detalle tiene que decir que se leyó de la recuperación y no del PDF")

    def test_el_cotejo_de_un_html_lee_el_apellido_pese_a_la_codificacion(self):
        """La rama del HTML —los fallos que no vienen de la CSJN— también tiene que cotejar.

        Y el apellido acentuado tiene que sobrevivir a la codificación. El charset declarado se
        pasa en lugar de descartarse, aunque no sea lo que salva el caso: la cascada de
        `decodificar()` prueba utf-8, cp1252 y latin-1, así que una página en windows-1252 se lee
        bien de las dos formas. Se comprobó: pasar «utf-8» a propósito sobre bytes cp1252 igual
        coteja. Lo que este test sostiene es el resultado, no el camino.
        """
        import descargar_jurisprudencia as dj
        html = "<html><body><p>en la causa Góngora, Gabriel Arnaldo s/ causa n 14.092</p></body></html>"
        for charset in ("windows-1252", None):
            with self.subTest(charset=charset):
                estado, _ = dj.cotejar_identidad(Path("no-se-usa"),
                                                 html.encode("windows-1252"), charset, False,
                                                 "Góngora, Gabriel Arnaldo")
                self.assertEqual(estado, "cotejado")

    def test_puntos_suspensivos_no_son_codepage_degradado(self):
        """El set original incluía U+2026. Una fe de erratas que dice DONDE DICE: ... /
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
        self.assertTrue(any("acentuación degradada" in p for p in problemas), problemas)

    def test_mojibake_de_doble_codificacion(self):
        import _comun
        roto = ("ARTÍCULO 1.- " + "la acción prescribirá según el plazo más breve. " * 60 + "aÃ±os Ã©poca Ã³rgano artÃ­culo ")
        problemas = _comun.revisar_texto(roto)
        self.assertTrue(any("mojibake" in p for p in problemas), problemas)

    def test_sentencias_reporta_un_fallo_declarado_y_no_bajado(self):
        """El bloque "fallos" mira el cotejo de identidad, no si el archivo está. Un fallo con
        URL declarada pero sin PDF en disco no lo reportaba nadie, y había tres así citados en
        los módulos. Si esto falla, el agujero volvió."""
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        with tempfile.TemporaryDirectory() as d:
            J = Path(d) / "derecho" / "fuentes" / "jurisprudencia"
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
            J = Path(d) / "derecho" / "fuentes" / "jurisprudencia"
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


class TestUmbralesDeVencimiento(unittest.TestCase):
    """Ningún umbral de serie puede sonar por el calendario en vez de por el dato.

    Las tres series son MENSUALES y `_periodo_a_fecha()` ancla el período al día 1, así que
    la más fresca posible ya tiene 31 días el primero del mes siguiente y 46 el día 16. Un
    umbral por debajo de eso pone la serie en rojo todos los meses pasado el 15, con el dato
    completo hasta el último mes cerrado y sin nada que bajar. Estaba pasando con el CER, en
    45. Para que el umbral signifique «se saltó un mes» tiene que pasar de 62 —dos meses de
    31—, y ahí sí un rojo es una serie atrasada de verdad.
    """

    def test_ninguna_serie_mensual_se_vence_dentro_del_mes_siguiente(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        for serie, dias in estado.UMBRAL_SERIE.items():
            with self.subTest(serie):
                self.assertGreater(dias, 62,
                                   f"{serie} se marca vencida a los {dias} días, y una serie "
                                   f"mensual anclada al día 1 llega sola a 62 sin que falte "
                                   f"nada: la alarma sonaría por el almanaque")

    def test_el_jus_si_puede_vencer_dentro_del_mes(self):
        """No es lo mismo: lo que el umbral del jus mide es hace cuánto que nadie mira la
        tabla oficial, y mirarla todos los meses es lo que se pide."""
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        self.assertLess(estado.UMBRALES["jus"], 62)


class TestElJusMideLaMiradaYNoElValor(unittest.TestCase):
    """La SCBA publica el jus con rezago, así que el valor envejece sin que falte cargarlo.

    Medir la antigüedad del último período ponía el bloque en rojo todos los meses con el
    dato completo, y el arreglo que sugería -«cargar el jus del mes»- era consejo falso: no
    hay nada que cargar. Lo que vence es la mirada, y por eso el csv lleva
    `# verificado: AAAA-MM-DD` y `estado.py` mide eso, igual que las normas miden su
    `verificado` y no la antigüedad de las leyes.

    La forma de esa línea es contrato. Si alguien reescribe el comentario a mano y le cambia
    el prefijo, `_verificado_csv()` devuelve None y el bloque sale REVISAR: la alarma falsa
    no vuelve en silencio.

    MUTACIÓN que lo demuestra: envejecer la línea `# verificado:` tiene que poner el bloque
    en rojo, y envejecer sólo el valor NO.
    """

    def _csv(self, verificado: str, periodo: str) -> Path:
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        f = d / "jus-scba.csv"
        f.write_text(f"# Valor del jus\n{verificado}\n"
                     f"vigencia_desde,jus_ley_14967\n{periodo},53232\n", encoding="utf-8")
        return f

    def _estado(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import estado
        return estado

    def test_el_csv_del_repositorio_declara_su_verificado(self):
        e = self._estado()
        csv = RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "scripts"
        csv = (csv / ".." / ".." / ".." / "fuentes" / "datos" / "jus-scba.csv").resolve()
        self.assertTrue(csv.is_file(), f"no está {csv}")
        self.assertIsNotNone(
            e._verificado_csv(csv),
            "jus-scba.csv no declara `# verificado: AAAA-MM-DD`: sin esa línea el bloque "
            "vuelve a medir la antigüedad del valor y a pedir que se cargue lo que no falta")

    def test_un_valor_viejo_con_mirada_fresca_no_vence(self):
        e = self._estado()
        hoy = e._hoy().isoformat()
        f = self._csv(f"# verificado: {hoy}", "2020-01-01")
        self.assertEqual(e._verificado_csv(f), 0)

    def test_una_mirada_vieja_si_vence(self):
        e = self._estado()
        viejo = (e._hoy() - timedelta(days=e.UMBRALES["jus"] + 1)).isoformat()
        f = self._csv(f"# verificado: {viejo}", "2020-01-01")
        self.assertGreater(e._verificado_csv(f), e.UMBRALES["jus"])

    def test_un_prefijo_roto_no_pasa_por_fresco(self):
        """Si el contrato se rompe, REVISAR. Nunca volver a la alarma falsa en silencio."""
        e = self._estado()
        hoy = e._hoy().isoformat()
        for roto in (f"# verificada: {hoy}", f"# verificado {hoy}", f"#verificado: {hoy}x",
                     f"# verificado: {hoy} y algo más"):
            with self.subTest(roto):
                self.assertIsNone(e._verificado_csv(self._csv(roto, "2020-01-01")))

    def test_el_verificado_no_se_busca_despues_del_encabezado(self):
        """Una fila de datos que parezca el marcador no cuenta: el contrato es del encabezado."""
        e = self._estado()
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        f = d / "jus-scba.csv"
        f.write_text("# Valor del jus\nvigencia_desde,jus_ley_14967\n2020-01-01,1\n"
                     f"# verificado: {e._hoy().isoformat()}\n", encoding="utf-8")
        self.assertIsNone(e._verificado_csv(f))


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
        import estado
        raiz = RAIZ_DEL_CHECKOUT
        for arch in ("serie-ipc.csv", "serie-ripte.csv", "serie-cer.csv", "jus-scba.csv"):
            ruta = raiz / "derecho" / "fuentes" / "datos" / arch
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
        raiz = RAIZ_DEL_CHECKOUT
        self.fuentes = raiz / "derecho" / "fuentes"
        self.tabla = (self.fuentes / "MANIFIESTO.md").read_text(encoding="utf-8")

    def _declarado(self, patron: str) -> tuple:
        hallado = re.search(patron, self.tabla)
        self.assertIsNotNone(
            hallado, f"la tabla del MANIFIESTO ya no dice esto: {patron}")
        return tuple(int(g) for g in hallado.groups())

    def _en_prosa(self, patron: str) -> tuple:
        """Como `_declarado`, pero con los saltos de línea aplanados: la prosa se reacomoda
        al reescribirla y el control no tiene por que romperse por un salto de renglón."""
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

        La foto se fecha POR MES y no por día, a propósito: una fecha al día invita a leer el
        repositorio como vencido el día 181, cuando la granularidad real del trabajo es el mes.
        La precisión al día se conserva donde la consume una herramienta --la columna de
        `changelog-normativo.md`, de la que `pendientes.py` cuenta los 180 días-- y no donde la
        lee una persona. Así que esto compara meses, con un mes de tolerancia, y sigue
        atrapando lo que importa: una foto que quedó atrás de lo que hay bajado.
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
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.modulo = (raiz / "derecho" / "skills" / "derecho-argentino" / "references"
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
        J = self.raiz / "derecho" / "fuentes" / "jurisprudencia"
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

    Lo otro que sostienen es el cotejo declarado: que lo que `ocr/correcciones/<slug>.json`
    dice esté efectivamente aplicado en el `.txt` y que el encabezado lo anuncie. El porqué de
    declararlo en vez de editar el archivo está en `fuentes/MANIFIESTO.md`.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.juris = raiz / "derecho" / "fuentes" / "jurisprudencia"
        registro = self.juris / "ocr" / "procedencia.json"
        if not registro.exists():
            self.skipTest("todavía no hay texto recuperado")
        self.registro = json.loads(registro.read_text(encoding="utf-8"))["fallos"]

    def _sha(self, ruta: Path) -> str:
        return hashlib.sha256(ruta.read_bytes()).hexdigest()

    def _cotejo(self, slug: str) -> dict | None:
        ficha = self.juris / "ocr" / "correcciones" / f"{slug}.json"
        return json.loads(ficha.read_text(encoding="utf-8")) if ficha.exists() else None

    def test_cada_derivacion_corresponde_al_pdf_que_dice(self):
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                pdf = self.juris / ficha["pdf"]
                self.assertTrue(pdf.exists(), f"falta {ficha['pdf']}")
                self.assertEqual(self._sha(pdf), ficha["sha256_pdf"],
                                 "el PDF cambió: regenerar con reocr_jurisprudencia.py")

    def test_el_texto_coincide_con_su_hash(self):
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                txt = self.juris / "ocr" / ficha["archivo"]
                self.assertTrue(txt.exists(), f"falta {ficha['archivo']}")
                self.assertEqual(self._sha(txt), ficha["sha256_texto"],
                                 "el texto no coincide con su hash. Si se lo corrigió a mano, "
                                 "la corrección va declarada en ocr/correcciones/ y se aplica "
                                 "regenerando; recalcular el hash acá apaga este control")

    def test_cada_derivacion_avisa_que_no_es_publicacion_oficial(self):
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                cabecera = (self.juris / "ocr" / ficha["archivo"]).read_text(
                    encoding="utf-8")[:2000]
                self.assertIn("RECUPERADO POR OCR LOCAL", cabecera)
                self.assertIn("publicación oficial", cabecera)
                self.assertIn(ficha["sha256_pdf"], cabecera)

    def test_todo_cotejo_declarado_esta_aplicado(self):
        # El punto es que el archivo y su cotejo no se separen. Si alguien regenera sin el
        # cotejo, o lo edita después, el hash ya lo caza; esto caza lo que el hash no ve: un
        # cotejo que declara una corrección que no está en el texto, o al revés.
        cotejados = 0
        for slug, ficha in self.registro.items():
            cotejo = self._cotejo(slug)
            if not cotejo:
                continue
            cotejados += 1
            texto = (self.juris / "ocr" / ficha["archivo"]).read_text(encoding="utf-8")
            for n, c in enumerate(cotejo["correcciones"], 1):
                with self.subTest(slug=slug, correccion=n):
                    # Se exige presencia, no unicidad: dos correcciones distintas pueden dar el
                    # mismo renglón —`4°) Que contra el referido pronunciamiento` sale igual en
                    # el voto de la mayoría y en el de Petracchi— y una puede ser prefijo de la
                    # otra. La unicidad se exige donde importa, sobre el texto SIN corregir, y la
                    # exige el script al aplicar.
                    self.assertIn(c["a"], texto,
                                  f"la corrección {n} (página {c.get('pagina')}) declara un "
                                  f"resultado que no está en el texto")
                    self.assertNotIn(c["de"], texto,
                                     f"la corrección {n} (página {c.get('pagina')}) está "
                                     f"declarada pero el texto sigue con el error del OCR: "
                                     f"regenerar con reocr_jurisprudencia.py")
        if not cotejados:
            self.skipTest("todavía no hay ningún cotejo declarado")

    def test_todo_cotejo_dice_en_que_se_baso_y_por_que(self):
        # Un cotejo sin motivo es indistinguible de una edición de gusto, y es lo que hay que
        # poder auditar renglón por renglón: qué decía el OCR, qué dice la página, y por dónde
        # se verifica. `impresa` es el número que lleva el volumen de Fallos, que no coincide
        # con el del PDF.
        for slug in self.registro:
            cotejo = self._cotejo(slug)
            if not cotejo:
                continue
            with self.subTest(slug):
                self.assertRegex(cotejo.get("cotejado_el", ""), r"^\d{4}-\d{2}-\d{2}$",
                                 "el cotejo no dice cuándo se leyó")
                self.assertGreater(len(cotejo.get("base", "")), 20,
                                   "el cotejo no dice contra qué se leyó")
                self.assertTrue(cotejo["correcciones"], "el cotejo no declara ninguna")
            for n, c in enumerate(cotejo["correcciones"], 1):
                with self.subTest(slug=slug, correccion=n):
                    self.assertGreater(len(c.get("motivo", "")), 20,
                                       "no dice por qué el OCR se equivocó")
                    self.assertIsInstance(c.get("pagina"), int, "no dice en qué página del PDF")
                    self.assertIsInstance(c.get("impresa"), int,
                                          "no dice qué página lleva impresa: sin eso el cotejo "
                                          "no se puede volver a verificar")
                    self.assertNotEqual(c["de"], c["a"], "no corrige nada")

    def test_la_ficha_declara_el_cotejo_que_el_archivo_tiene(self):
        # Las dos direcciones. Una ficha que no declara su cotejo lo vuelve invisible para
        # cualquiera que lea sólo la procedencia; una que declara uno inexistente hace creer
        # que el texto se leyó contra el PDF cuando nadie lo miró.
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                cotejo = self._cotejo(slug)
                if cotejo:
                    self.assertEqual(ficha.get("correcciones"), len(cotejo["correcciones"]),
                                     "la procedencia no cuenta las correcciones que hay")
                    self.assertEqual(ficha.get("cotejado"), cotejo["cotejado_el"],
                                     "la procedencia y el cotejo no coinciden en la fecha")
                else:
                    self.assertIsNone(ficha.get("cotejado"),
                                      "la procedencia declara un cotejo que no existe")
                    self.assertIsNone(ficha.get("correcciones"),
                                      "la procedencia cuenta correcciones que no existen")

    def test_el_encabezado_anuncia_el_cotejo(self):
        # Quien abre el .txt tiene que ver en la cabecera que hay renglones corregidos a mano y,
        # sobre todo, que el resto NO se revisó. Un archivo medio cotejado que no lo dice es
        # peor que uno sin cotejar: invita a confiar en el renglón de al lado.
        for slug, ficha in self.registro.items():
            with self.subTest(slug):
                cabecera = (self.juris / "ocr" / ficha["archivo"]).read_text(
                    encoding="utf-8")[:2000]
                cotejo = self._cotejo(slug)
                if cotejo:
                    self.assertIn("Cotejado:", cabecera)
                    self.assertIn(f"{len(cotejo['correcciones'])} declaradas", cabecera)
                    self.assertIn(f"correcciones/{slug}.json", cabecera)
                    self.assertIn("TODO EL RESTO es salida de máquina sin revisar", cabecera)
                else:
                    self.assertNotIn("Cotejado:", cabecera,
                                     "el encabezado anuncia un cotejo que no existe")


class TestPlantillaDelEncabezadoOCR(unittest.TestCase):
    """La prosa que `reocr_jurisprudencia.py` escribe en el encabezado y la del corpus son una.

    El .txt entero está fijado por hash en `ocr/procedencia.json`, así que la plantilla y los
    archivos generados son el mismo texto en dos lugares: cambiar una palabra en una sola punta
    parte el corpus en dos. Se arregla regenerando, que acá es correr tesseract y son minutos.

    Ya se bifurcó una vez, y en silencio, en la dirección contraria a la que uno esperaría: la
    plantilla acentuó `imágenes`, `página` y `publicación` mientras los seis .txt seguían en
    ASCII, y nadie regeneró. Ningún test lo veía, porque el único que mira la cabecera buscaba
    `publicacion oficial` sin tilde y eso lo daba el corpus, no la plantilla: el control medía un
    lado y daba verde sobre los dos. La primera regeneración lo habría puesto en rojo sin decir
    por qué.
    """

    RUTA = Path(__file__).resolve().parents[4] / "herramientas" / "reocr_jurisprudencia.py"

    def setUp(self):
        if not self.RUTA.exists():
            self.skipTest(f"no está {self.RUTA.name}")
        self.fuente = self.RUTA.read_text(encoding="utf-8")
        self.ocr = RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "jurisprudencia" / "ocr"

    def _constante(self, nombre: str) -> list:
        """Los renglones de una constante del script, leídos del fuente.

        Por AST y no por regex: es una tupla de literales, y un regex sobre el texto arrastra
        también el docstring del módulo, que es prosa nuestra y no va escrita en ningún .txt.
        """
        arbol = ast.parse(self.fuente)
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, ast.Assign):
                continue
            if any(isinstance(d, ast.Name) and d.id == nombre for d in nodo.targets):
                return [n.value for n in ast.walk(nodo.value)
                        if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.fail(f"no se encontró la constante {nombre}: el test quedó mirando nada")

    def test_la_prosa_de_la_plantilla_no_se_bifurca_del_corpus(self):
        recuperados = sorted(self.ocr.glob("*.txt"))
        if not recuperados:
            self.skipTest("no hay texto recuperado contra el que comparar")
        # El aviso va en todos; el del cotejo, sólo en los que tienen uno declarado. Compararlo
        # contra todos lo dejaría rojo para siempre, que es la alarma que se aprende a ignorar.
        cotejados = [p for p in recuperados
                     if (self.ocr / "correcciones" / f"{p.stem}.json").exists()]
        planes = [("AVISO", recuperados), ("AVISO_COTEJO", cotejados)]
        mirados = 0
        for nombre, alcance in planes:
            renglones = self._constante(nombre)
            self.assertGreater(len(renglones), 2,
                               f"{nombre} se leyó con muy pocos renglones: el test quedó "
                               f"mirando casi nada")
            if not alcance:
                continue
            textos = [(p.name, p.read_text(encoding="utf-8")) for p in alcance]
            for renglon in renglones:
                mirados += 1
                with self.subTest(renglon[:40]):
                    distintos = [n for n, t in textos if renglon not in t]
                    self.assertEqual(distintos[:3], [],
                                     f"la plantilla escribe «{renglon[:55]}» y {len(distintos)} "
                                     f"de {len(textos)} archivos usan otra forma: o se revierte "
                                     f"la plantilla, o se corre el OCR de nuevo sobre todos")
        self.assertGreater(mirados, 3, "no se comparó casi nada")

    # La ortografía de estos renglones NO se controla acá. Al sacar `AVISO` de las constantes
    # exceptuadas, `TestSalidaAcentuadaEnTodoElRepo` pasó a medirlos con la regla del -ción y las
    # listas, que es el control de verdad. Un test propio que pidiera «al menos un acento» sería
    # la alarma que suena siempre: se pone roja el día que un renglón correcto no lleve ninguno.


class TestUnaSolaZonaHoraria(unittest.TestCase):
    """Las fechas del repositorio se escriben en hora argentina, y en UNA sola zona.

    Está declarada tres veces porque los tres árboles de scripts no comparten módulo a propósito
    —`fuentes/scripts/_comun.py`, `herramientas/_veredictos.py` y `perfil.py` en la skill—, así
    que lo que hay que sostener es que no se separen. Es el mismo trato que la versión del plugin.

    Dos cosas más que este test fija, y las dos tienen consecuencia:

    Que el offset sea FIJO y no la zona del sistema. El workflow de CI corre en UTC: con
    `astimezone()` la misma corrida fecharía distinto según dónde se corra, y una fecha que lee
    una máquina no puede depender de eso. Argentina no usa horario de verano desde 2009.

    Y que no quede ningún reloj suelto. Un `date.today()` o un `datetime.now(timezone.utc)` en
    cualquier script vuelve a meter una segunda zona sin que nada proteste: pasó con `descargado`
    en UTC y el `Descargado:` del encabezado en hora local, con lo que el mismo archivo podía
    decir dos días distintos.
    """

    RAIZ = Path(__file__).resolve().parents[4]
    DECLARACIONES = (
        Path("derecho") / "fuentes" / "scripts" / "_comun.py",
        Path("herramientas") / "_veredictos.py",
        Path("derecho") / "skills" / "derecho-argentino" / "scripts" / "perfil.py",
    )
    # Los que miden tiempo de verdad. Un script que sólo parsea fechas de un archivo no cuenta.
    ARBOLES = (Path("derecho") / "fuentes" / "scripts", Path("herramientas"),
               Path("derecho") / "skills" / "derecho-argentino" / "scripts")
    RELOJ = re.compile(r"date\.today\(\)|datetime\.now\((?!ARGENTINA\))|utcnow\(")

    def test_las_tres_declaraciones_dicen_lo_mismo(self):
        hallados = {}
        for relativa in self.DECLARACIONES:
            ruta = self.RAIZ / relativa
            self.assertTrue(ruta.is_file(), f"falta {relativa}")
            hallada = re.search(r"ARGENTINA\s*=\s*timezone\(timedelta\(hours=(-?\d+)\)\)",
                                ruta.read_text(encoding="utf-8"))
            self.assertIsNotNone(hallada, f"{relativa} no declara ARGENTINA: o se movió de "
                                          f"lugar, o este test quedó mirando nada")
            hallados[relativa.as_posix()] = int(hallada.group(1))
        self.assertEqual(set(hallados.values()), {-3},
                         f"las zonas se separaron: {hallados}")

    def test_ningun_script_usa_otro_reloj(self):
        sueltos = []
        for arbol in self.ARBOLES:
            for guion in sorted((self.RAIZ / arbol).glob("*.py")):
                if guion.name.startswith("test_"):
                    continue
                for numero, linea in enumerate(
                        guion.read_text(encoding="utf-8").splitlines(), 1):
                    if linea.lstrip().startswith("#"):
                        continue
                    if self.RELOJ.search(linea):
                        sueltos.append(f"{arbol.as_posix()}/{guion.name}:{numero} {linea.strip()}")
        self.assertEqual(sueltos, [],
                         "hay relojes que no pasan por ARGENTINA: usar hoy() o ahora()")


class TestEntradasSinURL(unittest.TestCase):
    """Una norma declarada sin URL tiene que decir por qué, o el descargador no informa nada.

    `descargar_normas.py` imprime `SIN URL <slug> <nota>` en cada corrida. Sin `nota` imprime
    "completar el manifiesto", que no dice ni qué falta ni por qué importa, y la entrada se
    vuelve ruido que se aprende a saltear.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        catalogo = raiz / "derecho" / "fuentes" / "normas" / "normas.json"
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
    # capitalizado, y también necesita la diéresis o `[Verificar Antigüedad: ...]` pasa.
    CUALQUIERA = re.compile(r"\[([" + LETRAS + "][" + LETRAS + r" \-]{3,})(?::|\])")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.skill = raiz / "derecho" / "skills" / "derecho-argentino"
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
        """MUTACIÓN del alcance del propio control, y no de un archivo del repo.

        Las clases de letras estaban escritas tres veces a mano y a las tres les faltaba la Ü.
        Consecuencia: `[VERIFICAR ANTIGÜEDAD: ...]` no matcheaba el patrón, así que el marcador
        no era ni candidato y el control lo IGNORABA en silencio en vez de reclamarlo. No es
        hipotético: "antigüedad" con diéresis aparece 67 veces en el repositorio y es el núcleo
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
        """MUTACIÓN vivida: una corrección de acentos en masa convirtió
        `[VERIFICAR CRITERIO DEL FUERO:` en `[VERIFICAR Criterio DEL FUERO:` en dos evals, y
        esta suite no lo vio porque su regex solo aceptaba candidatos ya en mayúsculas: el
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
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        # Un caso es una carpeta CON `caso.md`. `claude plugin eval` deja su salida en
        # `evals/results/`, que es una carpeta y no un caso: contarla corrompía la resta
        # de autoría de LICENCIAS.md con cada corrida.
        self.casos = [d for d in (raiz / "derecho" / "evals").iterdir()
                      if d.is_dir() and (d / "caso.md").is_file()]

    def test_licencias_declara_los_casos_que_hay(self):
        texto = (self.raiz / "LICENCIAS.md").read_text(encoding="utf-8")
        hallado = re.search(r"\*\*(\d+) casos\*\* de verificación", texto)
        self.assertIsNotNone(hallado, "LICENCIAS.md dejó de decir cuántos evals hay")
        self.assertEqual(int(hallado.group(1)), len(self.casos))

    def test_el_slug_del_encabezado_es_el_nombre_del_directorio(self):
        """El slug se escribe en el encabezado de `rubrica.md` y `resultado.md`, y ahí va en
        ASCII porque es el nombre de una carpeta.

        MUTACIÓN VIVIDA: una corrección de acentos por regla convirtió
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
                # Solo cuando lo que sigue al · ES un slug. `caso.md` pone ahí el título en
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
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.escritos = raiz / "derecho" / "kb" / "escritos"
        self.modelos = {f"kb/escritos/{p.relative_to(self.escritos).as_posix()}"
                        for d in self.escritos.rglob("modelos") if d.is_dir()
                        for p in d.glob("*.md")}

    def test_el_inventario_cita_todos_los_modelos_del_repo(self):
        texto = (self.raiz / "derecho" / "skills" / "derecho-argentino" / "references"
                 / "modelos.md").read_text(encoding="utf-8")
        citados = set(re.findall(r"`(kb/escritos/[\w./\-]+\.md)`", texto))
        faltan = sorted(self.modelos - citados)
        self.assertEqual(faltan, [], f"modelos.md no inventaría: {faltan}")

    def test_los_documentos_que_cuentan_modelos_dicen_el_numero_real(self):
        cuantos = len(self.modelos)
        for relativo in ("derecho/kb/README.md", "docs/ARQUITECTURA.md"):
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

    # `test_el_checklist_nombra_todos_los_suites_de_herramientas` y
    # `test_ci_corre_los_mismos_suites_que_el_checklist` vivían acá y se fueron con lo que
    # cuidaban. Existían porque el checklist de `docs/DESARROLLO.md` y `.github/workflows/
    # tests.yml` enumeraban las suites a mano, y habían llegado a divergir —seis en uno, cinco
    # en el otro—. Los dos lugares corren ahora `unittest discover`: no hay lista de la que
    # caerse, así que no hay nada que cruzar. Reponer una enumeración obliga a reponer los dos.

    def test_nombra_todos_los_scripts_del_directorio(self):
        for guion in sorted(self.aqui.glob("*.py")):
            if guion.name.startswith("test_"):
                continue
            with self.subTest(guion.name):
                self.assertIn(f"`{guion.name}`", self.readme,
                              f"el README no menciona {guion.name}")


class TestSalidaCodificable(unittest.TestCase):
    """Toda la salida de una herramienta tiene que poder codificarse en cp1252.

    El porqué y la tabla de qué entra y qué no están en `docs/DESARROLLO.md`, sección «Lo que
    un script imprime tiene que entrar en cp1252». En una línea: los acentos NO son el
    problema; lo que rompe son las flechas, los tildes de verificación y los caracteres de
    dibujo.

    Se mide corriendo los scripts, no leyendo el fuente: la salida se arma con f-strings y datos,
    así que el fuente no dice qué se imprime.
    """

    # Los que corren sin binarios externos ni red. `calidad_ocr.py`,
    # `auditar_fechas_fallos.py` y `reocr_jurisprudencia.py` quedan afuera porque necesitan
    # poppler o tesseract, y los descargadores porque salen a la red.
    HERRAMIENTAS = ("herramientas/cifras.py", "herramientas/frontera_kb.py",
                    "herramientas/cobertura_normativa.py", "herramientas/pendientes.py",
                    "herramientas/reformas_no_leidas.py",
                    "derecho/skills/derecho-argentino/scripts/estado.py")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
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
        """MUTACIÓN del control: si `_rompe` se vuelve permisivo, el test da verde siempre; si se
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
        ("derecho/skills/derecho-argentino/scripts/liquidacion_lct.py",
         ["--ingreso", "2019-03-03", "--extincion", "2026-08-10",
          "--mejor-remuneracion", "1450000", "--tope-245", "2000000"]),
        ("derecho/skills/derecho-argentino/scripts/plazos.py",
         ["--tipo", "habiles", "--desde", "2026-09-10", "--dias", "5", "--fuero", "pba"]),
        # Un plazo que cruza a 2027 para que entren las notas de `inhábiles.json` sobre lo que
        # todavía no está dictado: esas notas se imprimen y las lee el usuario, así que el
        # control tiene que verlas. Con el caso de septiembre no salen.
        ("derecho/skills/derecho-argentino/scripts/plazos.py",
         ["--tipo", "habiles", "--desde", "2026-12-22", "--dias", "10", "--fuero", "pba"]),
        ("derecho/skills/derecho-argentino/scripts/honorarios_pba.py",
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
        raiz = RAIZ_DEL_CHECKOUT
        self.jur = raiz / "derecho" / "fuentes" / "jurisprudencia"

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

    def test_ninguna_caratula_pierde_un_acento_por_regla(self):
        """La misma regla que `TestTitulosDeNormas`: ninguna palabra termina en -cion o -sion
        sin tilde. No necesita lista y no envejece.

        La lista `SIN_ACENTO` de abajo no tenía `escarcelacion`, así que la carátula de
        "Estévez" pasó limpia — y encima no era un acento faltante sino otra palabra: el
        documento dice **ex**carcelación. Se recuperó del PDF, que es la única vía permitida.

        Se aplica SÓLO a la carátula. El campo `tribunal` queda afuera a propósito: la fuente
        de "ccsm3" escribe "CAMARA DE APELACION" sin tildes y en caja alta, y una carátula o un
        tribunal se citan como los escribe el registro, no como los querría el idioma.
        """
        for arch in self.ARCHIVOS:
            for slug, car in self._caratulas(arch).items():
                hallado = re.search(r"(?<![\w-])[a-záéíóúüñ]+[cs]ion(?![\w-])", car, re.I)
                with self.subTest(f"{arch} {slug}"):
                    self.assertIsNone(hallado,
                                      f"«{hallado.group(0) if hallado else ''}» va acentuada; "
                                      "recuperarla del documento bajado, no adivinarla")

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
    """Los 138 títulos de `normas.json` estaban enteros en ASCII, y no era solo cosmética.

    Son la etiqueta con la que la skill nombra una norma cuando la cita, así que "Código de
    Transito" y "Fuero Penal del Nino" salían así al escrito. Y había un error de otro tipo,
    repetido veinte veces: "Constitución de la Catamarca", que parece salido de una plantilla.
    Quedaron como "Constitución de la Provincia de Catamarca", que es como se titulan.

    ESTO SE CONTROLA CON REGLAS Y NO CON UNA LISTA DE PALABRAS, a propósito. En castellano
    ninguna palabra termina en `-cion` o `-sion` sin tilde: es una regla y no admite excepción.
    Una lista, en cambio, arrastra ambigüedad --`practica`, `publica`, `calculo` y `numero`
    existen sin tilde porque también son formas verbales-- y corregir por lista introduce
    errores: pasó dos veces en esta misma tarea, con "la actora práctica liquidación" y con
    "InfoLEG no pública texto actualizado".
    """

    ARCHIVOS = ("normas.json", "procedencia.json")
    SIN_TILDE = re.compile(r"\b[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{2,}[csx]ion\b")
    TRANSLITERADA = re.compile(r"(?i)\b(dan[io]os|anios?|nino|munioz|espania)\b")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.normas = raiz / "derecho" / "fuentes" / "normas"

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

    Es el único modo de falla del repositorio que ningún script puede diagnosticar, porque el
    diagnóstico también es Python: `estado.py` falla por la misma causa. Así que la regla vive
    en SKILL.md y este test es lo que la sostiene.

    Y hay una razón para que sea explícita. SKILL.md decía "si no están disponibles, hacer el
    cálculo a mano": una instrucción escrita para el caso de que no haya repo, que aplicada a
    la falta de intérprete entrega un número hecho a ojo a un usuario que cree que corrió la
    calculadora. Es exactamente el error que este repositorio existe para no cometer.
    """

    # Las tres que devuelve la consola, una por plataforma. Si el aviso pierde una, el modelo
    # lee ese error como "el script está roto" y no como "falta el intérprete".
    SENALES = ("command not found: python3",
               "'python3' no se reconoce como un comando",
               "xcrun: error: invalid active developer path")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.skill = (raiz / "derecho" / "skills" / "derecho-argentino"
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
        # Con el espacio aplanado: la frase del PATH cae justo donde se envuelve el renglón en
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
    `derecho/kb/...`— y sin este test nadie nota la diferencia.
    """

    RUTA = re.compile(r"`((?:argentina|references|herramientas|docs|assets|scripts|fuentes|"
                      r"evals|commands)/[\w./_\-]*[\w_\-])`")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.skill = raiz / "derecho" / "skills" / "derecho-argentino"

    def test_las_rutas_que_citan_los_modulos_existen(self):
        archivos = [self.skill / "SKILL.md"] + sorted((self.skill / "references").glob("*.md"))
        citadas = 0
        for archivo in archivos:
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for ruta in self.RUTA.findall(linea):
                    citadas += 1
                    # Se admite relativa al repo, a la skill, a references/ o a derecho/.
                    candidatos = [self.raiz / ruta, self.skill / ruta,
                                  self.skill / "references" / ruta, self.raiz / "derecho" / ruta]
                    with self.subTest(f"{archivo.name}:{numero}"):
                        self.assertTrue(any(c.exists() for c in candidatos),
                                        f"{archivo.name}:{numero} cita una ruta inexistente: {ruta}")
        self.assertGreater(citadas, 100, "los módulos dejaron de citar rutas del repo")


class TestElPresupuestoDeSKILL(unittest.TestCase):
    """`SKILL.md` se carga entero en cada conversación, y nada de eso es bajo demanda.

    La documentación de Claude Code lo dice sin vueltas: *"Keep `SKILL.md` under 500 lines. Move
    detailed reference material to separate files"*
    (<https://code.claude.com/docs/en/skills.md>, consultado el 18/09/2026). El cuerpo entra
    completo al activarse la skill; los `references/` sólo cuando el modelo decide abrirlos. De
    modo que un renglón acá lo paga toda conversación y un renglón allá lo paga la que lo usa.

    **Se miden dos cosas distintas y por eso hay dos topes.** Los 500 documentados se aplican a la
    **prosa**, que es lo que se infla: explicaciones que ya están en un módulo, estados anteriores,
    la misma regla dicha dos veces. Las **filas de tabla** son otra cosa —el ruteo de la sección 16
    y el vocabulario de marcadores de la sección 3—, y son justamente lo que la documentación manda
    dejar acá: navegación, y un vocabulario que el modelo transcribe **exacto** en cada respuesta y
    no va a abrir un módulo para copiar un corchete. Un módulo nuevo agrega una fila y eso es
    cobertura, no deuda.

    **Contarlas juntas rompía el control en la dirección equivocada:** un módulo nuevo ponía el
    suite en rojo y lo que se aprendía era a subir el número. Separadas, la prosa tiene el tope
    documentado y las tablas un trinquete que impide que exploten.

    MUTACIÓN que lo comprueba: agregarle diez renglones de prosa a `SKILL.md` lo deja en rojo por
    `test_la_prosa_entra_en_los_500`; agregarle veinte filas de tabla, por `test_las_tablas_no_explotan`.
    """

    PROSA = 500        # el tope documentado por Claude Code
    TABLA = 145        # trinquete: las filas de hoy con margen para módulos nuevos

    def setUp(self):
        self.archivo = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                        / "SKILL.md")
        ls = self.archivo.read_text(encoding="utf-8").splitlines()
        self.filas = [l for l in ls if l.startswith("| ")]
        self.prosa = len(ls) - len(self.filas)

    def test_la_prosa_entra_en_los_500(self):
        self.assertLessEqual(
            self.prosa, self.PROSA,
            f"la prosa del SKILL.md son {self.prosa} renglones y el tope documentado es "
            f"{self.PROSA}. Lo que entra tiene que sacar algo, y lo primero que se busca es la "
            f"explicación que ya está en un módulo: se reemplaza por el puntero.")

    def test_las_tablas_no_explotan(self):
        self.assertLessEqual(
            len(self.filas), self.TABLA,
            f"{len(self.filas)} filas de tabla contra un trinquete de {self.TABLA}. Una fila por "
            f"módulo nuevo es esperable; veinte de golpe es una tabla que se copió de un módulo.")

    def test_el_control_mira_el_archivo_que_cree(self):
        """Instrumento encendido: si la ruta o el formato cambiaran, los topes no medirían nada."""
        self.assertGreater(self.prosa, 300, "midió menos prosa de la posible: ¿está leyendo el archivo?")
        self.assertGreater(len(self.filas), 80, "no encontró las tablas de ruteo y de marcadores")


class TestLaCoberturaNoRepiteElRuteo(unittest.TestCase):
    """0.1 bis dice **hasta dónde llega** cada materia; la sección 16 dice **qué módulo abrir**.

    Las dos son tablas de materia contra módulo y por eso convergen solas: cada módulo nuevo
    entraba a las dos, y 0.1 bis terminó con treinta y tres filas que describían el contenido de
    un módulo —«Salud y discapacidad: CUD, quién debe cubrir…»— doce renglones más arriba de la
    fila de la 16 que lo enruta. Eso se paga en cada conversación y no orienta a nadie: para
    rutear sirve la situación de quien consulta, que es lo que dice la 16, no el temario del
    archivo.

    Lo que sostiene la separación son dos reglas:

    - **Una fila por materia, no una por módulo.** Los módulos son decenas; las materias con
      veredicto propio, poco más de diez. Una tabla que crece con los módulos se pasa del tope.
    - **Una fila tiene que decir algo además de a dónde ir.** Si sacándole las rutas y los
      nombres de archivo no queda texto, esa fila es ruteo y su lugar es la 16.

    MUTACIÓN que lo comprueba: copiar a 0.1 bis una fila de la sección 16 —de las que dicen
    «`references/<modulo>.md`» y nada más— deja en rojo `test_ninguna_fila_es_solo_un_destino`.
    """

    TOPE_DE_FILAS = 20

    def setUp(self):
        t = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
             / "SKILL.md").read_text(encoding="utf-8")
        bis = t[t.index("### 0.1 bis"):t.index("### 0.2 ·")]
        self.filas = [l for l in bis.splitlines()
                      if l.startswith("| ") and "---" not in l and not l.startswith("| Materia")]

    @staticmethod
    def _pelado(celda):
        """La celda sin rutas ni nombres de archivo, y sin puntuación: lo que de verdad dice."""
        return re.sub(r"[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", "", re.sub(r"`[^`]+`", "", celda))

    def test_hay_tabla(self):
        """Instrumento encendido: sin filas, las dos reglas de abajo pasan sin mirar nada."""
        self.assertGreater(len(self.filas), 8, "no encontró la tabla de cobertura de 0.1 bis")

    def test_una_fila_por_materia_y_no_una_por_modulo(self):
        self.assertLessEqual(
            len(self.filas), self.TOPE_DE_FILAS,
            f"0.1 bis tiene {len(self.filas)} filas: está creciendo con los módulos en vez de "
            f"con las materias. El mapa de módulos es la tabla de ruteo de la sección 16.")

    def test_ninguna_fila_es_solo_un_destino(self):
        solo_ruta = [f for f in self.filas if not self._pelado(f.strip("| ").split(" | ")[-1])]
        self.assertEqual(
            [], [f[:80] for f in solo_ruta],
            "hay filas de 0.1 bis cuya cobertura es sólo un módulo: eso es ruteo y va a la "
            "sección 16. Acá va el veredicto — profunda, cubierta, nada cargado, sin perfil.")


class TestElModuloDeRolDiceDeQueFueroEs(unittest.TestCase):
    """`sede-judicial-pba.md` y `parte.md` son del **fuero laboral de PBA**, y hay que decirlo
    donde se rutea, no una sola vez al pie de una tabla.

    El módulo de sede judicial trae la estructura del veredicto y de la sentencia, los recaudos
    de los arts. 168 y 171 de la Constitución provincial y el régimen recursivo bonaerense. Nada
    de eso rige en un juzgado nacional del trabajo, en uno civil de la Nación ni en un tribunal
    penal, y su única mención al orden nacional es una advertencia de **no** transpolar el art.
    46 de la Ley 18.345. De eso la skill no tiene módulo.

    El riesgo no es que el módulo sea de PBA: es **dónde** se entera el modelo. La 0.1 pregunta
    el rol en el primer turno y rutea ahí mismo, así que un juez del fuero nacional queda
    encaminado a un módulo provincial antes de que se haya leído nada más. Por eso el límite se
    exige en las dos secciones que deciden —la que pregunta y la que explica el modo— y no
    alcanza con que esté en la 0.1 bis.

    MUTACIÓN que lo comprueba: sacar «del **fuero laboral bonaerense**» del párrafo de la 0.1
    deja este test en rojo por esa sección.
    """

    #: Cada tramo va del encabezado que lo abre al que lo cierra.
    SECCIONES = {"0.1 · el rol se pregunta y se rutea": ("### 0.1 · Desde dónde se actúa",
                                                         "#### El perfil guardado"),
                 "1.6 · el modo órgano": ("### 1.6 · Si se actúa desde el órgano", "\n---\n")}

    def setUp(self):
        self.skill = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                      / "SKILL.md").read_text(encoding="utf-8")

    def _tramo(self, arranca, corta):
        i = self.skill.index(arranca)
        resto = self.skill[i:]
        j = resto.index(corta, len(arranca))
        return re.sub(r"\s+", " ", resto[:j])

    def test_las_dos_secciones_que_rutean_nombran_el_fuero(self):
        for nombre, (arranca, corta) in self.SECCIONES.items():
            with self.subTest(nombre):
                tramo = self._tramo(arranca, corta)
                self.assertIn("sede-judicial-pba.md", tramo,
                              "esta sección dejó de rutear al módulo: revisar el tramo")
                self.assertTrue(
                    "bonaerense" in tramo or "de la PBA" in tramo,
                    f"«{nombre}» rutea a `sede-judicial-pba.md` sin decir que es de PBA: un "
                    f"órgano del fuero nacional queda encaminado a un módulo provincial")
                self.assertIn("laboral", tramo,
                              f"«{nombre}» no dice que el módulo es del fuero laboral")

    def test_el_modulo_sigue_siendo_de_un_solo_fuero(self):
        """Instrumento encendido al revés: el día que el módulo cubra otro fuero, estas
        advertencias pasan a ser falsas y hay que sacarlas. Lo que se mide es que el título del
        módulo siga declarando su alcance, que es de donde sale la advertencia."""
        titulo = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "sede-judicial-pba.md").read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("fuero laboral PBA", titulo,
                      "el módulo cambió de alcance: revisar las advertencias del SKILL.md")


class TestLosModulosDeclaranSuBorde(unittest.TestCase):
    """Un módulo que no dice dónde termina se lee como si no terminara.

    El modelo abre el módulo de la rama, no encuentra el punto, y **completa con conocimiento
    general** en vez de decir que ahí la skill no llega. Es el mismo modo de falla que el de un
    monto citado de memoria, y es más difícil de ver porque la respuesta sale bien redactada.

    Lo declara una sección **«Lo que este módulo NO hace»**, con el destino de cada cosa que
    queda afuera. La practican los módulos que nacieron angostos; los que hay que vigilar son los
    grandes y viejos —`laboral.md`, `civil.md`, `consumidor.md`— porque son los que el modelo
    abre primero y con los que más confianza trabaja.

    **Es un trinquete sobre el reparto, no un mínimo por archivo.** Exigirlo en los 57 dejaría el
    suite en rojo hasta escribir 31 bordes de memoria, que es exactamente lo que no hay que
    hacer: cada uno sale de leer el módulo. Lo que se fija es que la práctica no retroceda.

    MUTACIÓN que lo comprueba: borrar la sección de `laboral.md` deja este test en rojo.
    """

    # La forma del encabezado es exacta a propósito: contar con un regex laxo enganchaba una
    # minúscula y contaba de más, y un control que cuenta de más es el que no suena nunca.
    #
    # **El piso se sube cuando se agrega un borde, y eso es parte de agregarlo.** Un trinquete que
    # no se mueve queda atrás de la práctica y deja de atrapar: con el piso en 26 y treinta bordes
    # escritos, borrar uno no lo hacía fallar. La mutación lo destapó.
    PISO = 30   # los que lo declaran hoy

    def setUp(self):
        self.refs = sorted((RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                            / "references").glob("*.md"))
        self.con_borde = [p.name for p in self.refs
                          if "Lo que este módulo NO hace" in p.read_text(encoding="utf-8")
                          or "Qué NO cubre" in p.read_text(encoding="utf-8")]

    def test_el_control_mira_todos_los_modulos(self):
        """Instrumento encendido: sin módulos, «no retrocedió» no mide nada."""
        self.assertGreater(len(self.refs), 40, "no encontró los módulos de referencia")

    def test_la_practica_no_retrocede(self):
        self.assertGreaterEqual(
            len(self.con_borde), self.PISO,
            f"{len(self.con_borde)} módulos declaran su borde y antes eran {self.PISO}. Un borde "
            f"no se saca: si el módulo creció y ahora cubre lo que decía no cubrir, se reescribe "
            f"la sección, no se borra.")


class TestLasRemisionesApuntanAUnaSeccionQueExiste(unittest.TestCase):
    """Una remisión a `modulo.md 42` es una promesa: ahí está lo que hace falta.

    Si esa sección no existe, **nada falla ruidosamente**. El modelo abre el módulo, no encuentra
    la sección, y sigue con lo que tiene — que es el modo de falla que este repositorio persigue.
    `TestRutasCitadasPorLaSkill` ya exige que el ARCHIVO exista; esto exige que exista la SECCIÓN.

    **Es la novena cosa que arrastra una partición**, la que `docs/DESARROLLO.md` decía que
    ninguna suite reclamaba: cuando el derecho colectivo salió a `laboral-colectivo.md`, la tabla
    de absorbidos de `laboral.md` siguió diciendo *"5.17 de este módulo"* sobre una sección que ya
    no estaba ahí. También atrapó una remisión a `ejecucion.md` 20 —es la 21; la 20 es
    `prueba-pericial.md`— escrita justamente en la frase que decía «no confundir».

    **El ordinal es parte del número.** `5.17 bis` y `5.17 ter` existen y `5.17` no, así que el
    control lee el ordinal: sin eso reclamaba cuatro remisiones correctas y el instrumento se
    apagaba solo.

    MUTACIÓN que lo comprueba: cambiar una remisión de `ejecucion.md` 21 por `ejecucion.md` 20 lo
    deja en rojo.
    """

    ORDINAL = "bis|ter|quater|quinquies|sexies"
    ENCABEZADO = re.compile(rf"^#{{2,4}} (\d+(?:\.\d+)*(?:\s+(?:{ORDINAL}))?)\b", re.M)
    CITA = re.compile(rf"`(?:references/)?([\w\-]+\.md)`,?\s+(\d+(?:\.\d+)*(?:\s+(?:{ORDINAL}))?)\b")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        skill = raiz / "derecho" / "skills" / "derecho-argentino"
        self.refs = skill / "references"
        self.secciones = {
            p.name: {" ".join(m.group(1).split())
                     for m in self.ENCABEZADO.finditer(p.read_text(encoding="utf-8"))}
            for p in sorted(self.refs.glob("*.md"))}
        self.archivos = ([skill / "SKILL.md"] + sorted(self.refs.glob("*.md"))
                         + sorted((raiz / "docs").glob("*.md"))
                         + [raiz / "AGENTS.md", raiz / "README.md", raiz / "LICENCIAS.md"])

    def _cubre(self, modulo, numero):
        """Una remisión a 24.9 vale si el módulo declara 24.9 o cualquier 24.9.x."""
        return any(s == numero or s.startswith(numero + ".") or s.startswith(numero + " ")
                   for s in self.secciones[modulo])

    def test_toda_remision_numerada_existe(self):
        rotas, miradas = [], 0
        for a in self.archivos:
            if not a.is_file():
                continue
            for n, linea in enumerate(a.read_text(encoding="utf-8").splitlines(), 1):
                for modulo, numero in self.CITA.findall(linea):
                    if modulo not in self.secciones:
                        continue
                    miradas += 1
                    numero = " ".join(numero.split())
                    if not self._cubre(modulo, numero):
                        rotas.append(f"{a.name}:{n} → {modulo} {numero}")
        self.assertGreater(miradas, 100, "casi no se miró ninguna remisión: el control está apagado")
        self.assertEqual(rotas, [],
                         "remisiones a una sección que el módulo no declara:\n    "
                         + "\n    ".join(rotas))

    def test_los_modulos_declaran_secciones(self):
        """Instrumento encendido: si el regex del encabezado dejara de enganchar, todo pasaría."""
        con = [m for m, s in self.secciones.items() if s]
        self.assertGreater(len(con), 40, "casi ningún módulo declara secciones numeradas")
        self.assertIn("5.17 bis", self.secciones["laboral.md"],
                      "el control perdió el ordinal y volvería a reclamar remisiones correctas")


class TestNingunNumeroDeSeccionEstaEnDosModulos(unittest.TestCase):
    """La numeración es **global**, así que un número es una dirección y tiene un solo destino.

    Si dos módulos declaran `5.18`, una remisión a 5.18 apunta a dos lugares y el lector llega al
    que abrió primero. Pasó al agregar los bordes: la sección «Lo que este módulo NO hace» de
    `laboral.md` se numeró 5.18, que es **Asociaciones sindicales** en `laboral-colectivo.md`
    desde la partición. Nada falló: simplemente había dos 5.18.

    **Dos repeticiones son legítimas, y las dos se reconocen por su forma, no por una lista.**

    - **El número raíz se comparte tras una partición.** `laboral.md` y `laboral-colectivo.md`
      declaran los dos `## 5`, porque 5.1 a 5.17 quedaron en uno y 5.17 a 5.18 se fueron al otro.
      El padre es el árbol; lo que tiene que ser único es la **hoja**, así que el control mira los
      números con punto.
    - **El stub que reenvía lo dice en su encabezado**, con esta forma exacta:
      `## 24.8 · Ejecución de la pena — está en ` seguido del módulo entre backticks. Es lo que
      hace que una remisión vieja siga llegando después de una mudanza, así que el número **tiene**
      que repetirse — y exigir la forma obliga al stub a decir a dónde manda, que es lo que el
      lector necesita. Una primera versión de este control adivinaba el stub por si el texto
      nombraba otro módulo, y **la mutación no la hizo fallar**: el borde de `laboral.md` nombra
      cuatro módulos en sus viñetas y pasaba por stub. Se descartó en vez de calibrarla.

    **`danos-indice-doctrinario.md` queda afuera**: sus §1 a §38 son los capítulos de una obra
    comercial, otro espacio de nombres que no colisiona con este árbol aunque los números coincidan.

    MUTACIÓN que lo comprueba: renumerar el borde de `laboral.md` como 5.18 lo deja en rojo.
    """

    OTRO_ESPACIO = {"danos-indice-doctrinario.md"}
    H = re.compile(r"^#{2,4} (\d+(?:\.\d+)*(?:\s+(?:bis|ter|quater|quinquies|sexies))?)\b([^\n]*)",
                   re.M)
    #: La forma que declara un stub de reenvío, y de paso dice a dónde manda.
    STUB = re.compile(r"—\s*est[áa]\s+en\s+`[\w\-]+\.md`")

    def setUp(self):
        self.refs = sorted((RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                            / "references").glob("*.md"))
        self.dueno, self.stubs = {}, 0
        for p in self.refs:
            if p.name in self.OTRO_ESPACIO:
                continue
            for m in self.H.finditer(p.read_text(encoding="utf-8")):
                num = " ".join(m.group(1).split())
                if self.STUB.search(m.group(2)):
                    self.stubs += 1
                    continue
                self.dueno.setdefault(num, set()).add(p.name)

    def test_el_control_ve_los_numeros_y_los_stubs(self):
        """Instrumento encendido por los dos lados: si no viera números no mediría nada, y si no
        reconociera ningún stub estaría reclamando las mudanzas legítimas."""
        self.assertGreater(len(self.dueno), 300, "casi no encontró secciones numeradas")
        self.assertGreater(self.stubs, 0, "no reconoció ningún stub de reenvío: revisar la forma")

    def test_una_hoja_un_modulo(self):
        choques = [f"{num}: {sorted(m)}" for num, m in sorted(self.dueno.items())
                   if "." in num and len(m) > 1]
        self.assertEqual(choques, [],
                         "el mismo número de sección en dos módulos, y ninguno declara ser un "
                         "stub de reenvío:\n    " + "\n    ".join(choques))


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
        "herramientas/deuda-revisada.json": "reclamos",
        "herramientas/ramas-revisadas.json": "ramas",
        "derecho/fuentes/normas/revisiones.json": "revisiones",
    }
    OBLIGATORIAS = ("_descripcion", "fijado")
    PERMITIDAS = OBLIGATORIAS + ("_criterio", "_vocabulario", "nota")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
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
                       "derecho/fuentes/normas/revisiones.json"):
            sospechosos |= {p.relative_to(self.raiz).as_posix()
                            for p in self.raiz.glob(patron)}
        self.assertEqual(sospechosos - set(self.ARCHIVOS), set(),
                         "hay un archivo de veredicto que no está en TestSobreDeLosVeredictos")


SEMVER = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.\-]+)?"



class TestVersionUnica(unittest.TestCase):
    """La versión del plugin se declara en cinco lugares y ninguno la deriva de otro.

    Publicar 1.0.1 significa editar cinco archivos, y hasta ahora nada atrapaba el que
    faltara: el repositorio se contradice solo y el primero en notarlo es quien instala.
    La fuente de verdad es `derecho/.claude-plugin/plugin.json`, que es de donde
    `generar_marca.py` saca el número para la chapa.
    """

    @staticmethod
    def _v(ruta: Path, *claves):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        for k in claves:
            d = d[k]
        return d

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.canonica = self._v(raiz / "derecho" / ".claude-plugin" / "plugin.json", "version")

    def test_los_manifiestos_declaran_la_misma_version(self):
        manifiestos = {
            "derecho/plugin.json": ("version",),
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
        y que nadie mira el día que se publica. Que quede rojo hasta que la fecha este puesta
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
            "derecho/.claude-plugin/plugin.json",
            "derecho/plugin.json",
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


class TestLosDosManifiestosDicenLoMismo(unittest.TestCase):
    """Los TRES manifiestos repiten la ficha del plugin, y nada la mantenía alineada.

    La versión ya tenía control —`TestVersionUnica`—, pero la **descripción** y las **keywords**
    estaban duplicadas a mano en dos archivos y sólo coincidían porque alguien se acordaba. Es el
    mismo molde que este repositorio ya persiguió con las cifras de la documentación: un dato
    escrito dos veces se separa, y el que lee uno de los dos no se entera.

    Las keywords importan más de lo que parece: son lo que los disparadores del `description` son
    para la skill, y por ahí se la encuentra en el marketplace.

    MUTACIÓN QUE LO RESPALDA: cambiarle una keyword a `plugin.json` y no a `marketplace.json`.
    Corrida el 17/09/2026: `test_las_keywords_son_las_mismas` falla y nombra la que sobra en cada
    lado. Con la descripción, lo mismo.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.plugin = json.loads(
            (raiz / "derecho" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.mercado = json.loads(
            (raiz / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"][0]

    def test_la_descripcion_es_la_misma(self):
        self.assertEqual(self.plugin["description"], self.mercado["description"],
                         "la descripción del plugin y la del marketplace se separaron")

    def test_las_keywords_son_las_mismas(self):
        a, b = self.plugin["keywords"], self.mercado["keywords"]
        self.assertEqual(sorted(set(a) - set(b)), [], "keywords que sólo están en plugin.json")
        self.assertEqual(sorted(set(b) - set(a)), [], "keywords que sólo están en marketplace.json")
        self.assertEqual(a, b, "las keywords coinciden pero en distinto orden")

    def test_el_portable_es_un_subconjunto_declarado(self):
        """El manifiesto de Codex lleva una ficha más corta a propósito, y eso se declara acá.

        Su `description` es un resumen y sus keywords son un núcleo: **no puede traer ninguna que
        los de Claude no tengan**, porque entonces se estaría anunciando en un lado algo que en el
        otro no figura, y nadie lo vería. Lo que sí puede es traer menos.

        MUTACIÓN QUE LO RESPALDA: agregarle al portable una keyword que los otros dos no tengan.
        """
        portable = json.loads((RAIZ_DEL_CHECKOUT / "derecho" / "plugin.json")
                              .read_text(encoding="utf-8"))
        sobrantes = sorted(set(portable["keywords"]) - set(self.plugin["keywords"]))
        self.assertEqual(sobrantes, [],
                         "el portable anuncia keywords que los manifiestos de Claude no tienen")
        self.assertTrue(portable["description"].startswith(
            "Análisis, redacción y revisión jurídica bajo derecho argentino"),
            "las tres fichas dejaron de abrir con la misma frase")

    def test_las_keywords_no_llevan_acento(self):
        """Se comparan y se tipean: van en ASCII, como cualquier identificador."""
        for k in self.plugin["keywords"]:
            with self.subTest(k):
                self.assertEqual(k, k.encode("ascii", "ignore").decode(),
                                 "una keyword con acento no se puede tipear igual en dos lados")
                self.assertEqual(k, k.lower())

    def test_instrumento_encendido(self):
        """Sin esto, «no hay diferencias» también sería «no hay keywords»."""
        self.assertGreater(len(self.plugin["keywords"]), 10)
        self.assertGreater(len(self.plugin["description"]), 100)


class TestSalidaDeEstado(unittest.TestCase):
    """`estado.py` interpola constantes de `_raiz` en lo que imprime, y esas constantes cambian.

    `ENV_PLUGIN` pasó de ser una cadena a una tupla al sumar Codex, y la interpolación quedó
    escupiendo el repr de Python -paréntesis y comillas- en la salida que el usuario lee
    justamente cuando NO se encontró el repo. Ningún test lo vio porque es un print en una
    rama de error.
    """

    def test_lo_que_imprime_no_trae_repr_de_python(self):
        """Se mira el TIPO de la constante, no su nombre.

        Una primera versión marcaba cualquier nombre en mayúsculas y fallaba sobre {ENV},
        que es una cadena y está bien interpolada. Una medida que se equivoca sobre un caso
        conocido no sirve para los desconocidos: lo que decide no es como se llama sino que
        es.
        """
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
    otra norma baja un articulado perfectamente sano y pasa en verde. Pasó, con 488 KB de
    articulado impecable de otra ley; el caso está fechado en `docs/AUDITORIAS.md`.

    Identidad primero, contenido después: es el mismo orden que `auditar_fechas_fallos.py`
    sigue con la jurisprudencia.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.normas = raiz / "derecho" / "fuentes" / "normas"
        if not (self.normas / "procedencia.json").is_file():
            self.skipTest("no esta la capa de fuentes")
        sys.path.insert(0, str(raiz / "derecho" / "fuentes" / "scripts"))

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
                continue        # constituciones, códigos y acuerdos no llevan número en el slug
            numero = m.group(1)
            # Sin el encabezado de procedencia: ese lo escribimos nosotros con el título del
            # manifiesto, así que buscar ahí confirmaría lo que ya creemos y no lo que bajamos.
            cuerpo = self._plano(_comun.cuerpo_consolidado(archivo)[:3000])
            mirados += 1
            with self.subTest(slug):
                self.assertTrue(
                    any(v in cuerpo for v in (numero, f"{numero[:-3]} {numero[-3:]}")),
                    f"{archivo.name} no menciona el numero {numero} en su texto: la URL puede "
                    f"apuntar a otra norma. Empieza con: {cuerpo[:90]}")
        self.assertGreater(mirados, 80, "dejaron de controlarse las normas descargadas")


class TestCuerpoContraProcedencia(unittest.TestCase):
    """El CUERPO del `.txt` tiene que hashear a su `sha256_texto`.

    Es la otra mitad, y mira otra cosa que `TestArchivoContraProcedencia`: `sha256_texto` es el
    hash del texto extraído, y es el que `verificar_normas.py` compara contra una re-extracción
    de la página viva para decidir si cambió la NORMA. Que ese hash describa además el cuerpo
    que publicamos no está garantizado por nada más que esto.

    SE LEE EN BYTES, y ahí está la trampa que costó el diagnóstico. `read_text()` abre con
    saltos universales y colapsa `\\r\\n` en `\\n`, pero el hash se calculó sobre el texto tal
    como salió del parser, con sus `\\r`. Treinta de los `.txt` bajados los traen -son los de
    normas.gba, digesto SCBA y JURISTECA-, así que leerlos como texto da un cuerpo distinto del
    que se hasheó y el control reporta desalineados que no lo están. Medido: leyendo bytes
    coinciden; colapsando los saltos, ninguno. `_comun.cuerpo_consolidado()` lee como texto y
    arrastra lo mismo: sirve para mirar el cuerpo, no para verificarlo.
    """

    RAYA = b"=" * 78

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.normas = raiz / "derecho" / "fuentes" / "normas"
        f = self.normas / "procedencia.json"
        if not f.is_file():
            self.skipTest("no esta la capa de fuentes")
        self.proc = json.loads(f.read_text(encoding="utf-8"))["normas"]

    def _cuerpo(self, archivo: Path):
        """El cuerpo en bytes: lo que sigue a la segunda raya del encabezado."""
        crudo = archivo.read_bytes()
        i = crudo.find(self.RAYA)
        j = crudo.find(self.RAYA, i + len(self.RAYA)) if i >= 0 else -1
        return None if j < 0 else crudo[j + len(self.RAYA):].lstrip(b"\n")

    def test_cada_txt_hashea_a_lo_que_dice_procedencia(self):
        import hashlib
        mirados, distintos = 0, []
        for slug, reg in sorted(self.proc.items()):
            esperado = reg.get("sha256_texto")
            archivo = self.normas / reg["archivo"]
            if not esperado or archivo.suffix != ".txt" or not archivo.is_file():
                continue
            cuerpo = self._cuerpo(archivo)
            if cuerpo is None:
                distintos.append(f"{slug} (sin encabezado reconocible)")
                continue
            mirados += 1
            if hashlib.sha256(cuerpo).hexdigest() != esperado:
                distintos.append(slug)
        self.assertGreater(mirados, 100, "dejaron de controlarse los textos bajados")
        self.assertEqual(distintos, [],
                         f"el cuerpo del .txt no hashea a su sha256_texto en procedencia.json: "
                         f"{', '.join(distintos[:5])}. El texto y su hash se escriben juntos, "
                         f"así que si difieren el archivo se tocó después de bajarse o la "
                         f"corrida no registró: volver a bajar ese slug con --forzar")


class TestFragmentoDelPortal(unittest.TestCase):
    """`fragmento_div()` recorta la sentencia y descarta la maqueta del portal.

    Un fallo de JUBA llega como página entera y la sentencia vive en un solo
    `<div class="contenido">`: más de la mitad del archivo es menú, scripts y pie, que se
    mueven cuando el portal se rediseña sin que cambie una línea del fallo.

    Los dos casos que importan, y los dos estaban en los archivos reales: el div de contenido
    trae divs ANIDADOS, así que cortar en el primer `</div>` trunca la sentencia; y los
    comentarios HTML traen tokens `<div` que no abren nada, así que contarlos corre el cierre.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "fuentes" / "scripts"))
        import _comun
        self.c = _comun

    def test_cierra_balanceado_y_no_en_el_primer_cierre(self):
        html = (b'<p>menu</p><div class="contenido">A<div class="interno">B</div>C</div>'
                b'<footer>pie</footer>')
        frag = self.c.fragmento_div(html, "contenido")
        self.assertEqual(frag, b'<div class="contenido">A<div class="interno">B</div>C</div>')
        self.assertNotIn(b"pie", frag)
        self.assertIn(b"C</div>", frag, "cortó en el cierre del div interno: trunca la sentencia")

    def test_un_div_en_un_comentario_no_corre_el_cierre(self):
        html = b'<div class="contenido">A<!-- <div> roto --></div><footer>pie</footer>'
        self.assertEqual(self.c.fragmento_div(html, "contenido"),
                         b'<div class="contenido">A<!-- <div> roto --></div>')

    def test_un_div_dentro_de_un_script_no_corre_el_cierre(self):
        html = (b'<div class="contenido">A<script>var x="</div>";</script>B</div>'
                b'<footer>pie</footer>')
        frag = self.c.fragmento_div(html, "contenido")
        self.assertTrue(frag.endswith(b"B</div>"), f"cerró adentro del script: {frag[-30:]!r}")

    def test_devuelve_un_tajo_exacto_del_original(self):
        html = b'ruido<div class="contenido">\r\n texto \r\n</div>ruido'
        frag = self.c.fragmento_div(html, "contenido")
        self.assertIn(frag, html, "el fragmento no es un tramo textual del original")
        self.assertEqual(frag.count(b"\r\n"), 2, "se tocaron los fines de línea")

    def test_sin_el_div_devuelve_None_y_no_adivina(self):
        # Quien llama guarda la página entera y lo dice. Guardar menos en silencio es peor.
        self.assertIsNone(self.c.fragmento_div(b"<div class=otra>x</div>", "contenido"))
        self.assertIsNone(self.c.fragmento_div(b'<div class="contenido">sin cierre',
                                               "contenido"))

    def test_la_clase_se_matchea_entera(self):
        # `contenido` no debe matchear `contenidos` ni `subcontenido`.
        self.assertIsNone(self.c.fragmento_div(b'<div class="contenidos">x</div>', "contenido"))
        self.assertIsNone(self.c.fragmento_div(b'<div class="subcontenido">x</div>', "contenido"))

    def test_convive_con_otras_clases_en_el_mismo_atributo(self):
        html = b'<div id="q" class="ancho contenido activo">x</div>'
        self.assertEqual(self.c.fragmento_div(html, "contenido"), html)


class TestCopiaDeIdentidad(unittest.TestCase):
    """El manifiesto y `procedencia.json` guardan la identidad por duplicado, y tiene que decir
    lo mismo en las dos.

    La duplicación es deliberada: `procedencia.json` es una foto del momento de bajar, y si
    hubiera que salir a buscar la carátula al manifiesto dejaría de sostenerse solo -- se
    corrige un título y el registro ya no dice qué se bajó. El precio es que una copia se
    corrige sin la otra, que es exactamente cómo se degradaron las carátulas.

    El cotejo de la carátula ya existe, en `TestCaratulasAcentuadas`. Esto cubre el resto, y el
    que más importa es `fecha`: `auditar_fechas_fallos.py` la lee de PROCEDENCIA y la audita
    contra el documento, así que dos copias distintas hacen que audite la fecha equivocada.
    """

    CORPUS = (("jurisprudencia", "fallos.json", "fallos", ("tribunal", "causa", "fecha")),
              ("normas", "normas.json", "normas", ("titulo", "url")))

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.fuentes = raiz / "derecho" / "fuentes"
        if not (self.fuentes / "normas" / "procedencia.json").is_file():
            self.skipTest("no esta la capa de fuentes")

    def test_las_dos_copias_de_la_identidad_dicen_lo_mismo(self):
        """Salvo cuando la entrada está marcada `revisar`: ahí el desajuste es el pendiente.

        Cambiar la URL de una norma en el manifiesto porque la vieja servía la ficha del
        portal, o un texto con los acentos rotos, deja las dos copias distintas A PROPÓSITO
        hasta que alguien corra el descargador: `procedencia.json` es la foto de lo que se
        bajó, y todavía no se bajó nada nuevo. Sin esta salvedad el control obliga a elegir
        entre dejar la URL mala en el manifiesto o tener la suite en rojo, y las dos son
        peores que decirlo. La salvedad no es una puerta abierta: está atada a `revisar`,
        que es la marca que `pendientes.py` lista y que se levanta al rebajar la norma.
        """
        mirados, pendientes = 0, []
        for carpeta, manifiesto, clave, campos in self.CORPUS:
            base = self.fuentes / carpeta
            man = {e["slug"]: e for e in
                   json.loads((base / manifiesto).read_text(encoding="utf-8"))[clave]}
            proc = json.loads((base / "procedencia.json").read_text(encoding="utf-8"))[clave]
            for slug, registro in sorted(proc.items()):
                if slug not in man:
                    continue
                mirados += 1
                for campo in campos:
                    if campo not in registro or campo not in man[slug]:
                        continue
                    if registro[campo] == man[slug][campo]:
                        continue
                    if campo == "url" and registro.get("revisar"):
                        pendientes.append(slug)
                        continue
                    with self.subTest(f"{slug}/{campo}"):
                        self.fail(f"{campo} difiere entre {manifiesto} y "
                                  f"procedencia.json: se corrigió una copia sola")
        self.assertGreater(mirados, 200, "dejó de cotejarse la identidad de lo bajado")
        self.assertLess(len(pendientes), 10,
                        f"demasiadas URL cambiadas sin rebajar ({', '.join(pendientes)}): "
                        f"la salvedad de `revisar` dejó de ser una excepción")


class TestArchivoContraProcedencia(unittest.TestCase):
    """Todo archivo bajado tiene que hashear a su `sha256_archivo`. Los dos corpus, una regla.

    Es la pregunta "alguien lo tocó después de bajarlo", y no la contestaba nada:
    `verificar_normas.py` compara una descarga fresca contra el registro y nunca abre el
    archivo del disco, y la jurisprudencia no tiene verificador. El contrato de los tres
    hashes está escrito en `fuentes/scripts/_comun.py`.

    SE LEE EN BYTES. `read_text()` abre con saltos universales y colapsa `\\r\\n` en `\\n`, y
    hay .txt que vienen con CRLF -- normas.gba, digesto SCBA, JURISTECA --: leerlos como texto
    da el hash de un archivo que no es el que hay. Es lo que hizo parecer desalineados a
    treinta archivos que estaban perfectos.
    """

    CORPUS = (("normas", "normas"), ("jurisprudencia", "fallos"))

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.fuentes = raiz / "derecho" / "fuentes"
        if not (self.fuentes / "normas" / "procedencia.json").is_file():
            self.skipTest("no esta la capa de fuentes")

    def test_cada_archivo_hashea_a_su_sha256_archivo(self):
        import hashlib
        mirados, mal = 0, []
        for carpeta, clave in self.CORPUS:
            base = self.fuentes / carpeta
            reg = json.loads((base / "procedencia.json").read_text(encoding="utf-8"))[clave]
            for slug, e in sorted(reg.items()):
                archivo = base / e["archivo"]
                if not archivo.is_file():
                    mal.append(f"{slug} (no está {e['archivo']})")
                    continue
                mirados += 1
                esperado = e.get("sha256_archivo")
                if not esperado:
                    mal.append(f"{slug} (falta sha256_archivo)")
                elif hashlib.sha256(archivo.read_bytes()).hexdigest() != esperado:
                    mal.append(slug)
        self.assertGreater(mirados, 200, "dejaron de controlarse los archivos bajados")
        self.assertEqual(mal, [],
                         f"no hashean a su sha256_archivo: {', '.join(mal[:5])}. El archivo y "
                         f"su hash se escriben juntos, así que si difieren se tocó después de "
                         f"bajarse: volver a bajar ese slug con --forzar")


class TestFragmentoGuardado(unittest.TestCase):
    """De un fallo de JUBA se guarda la sentencia, no la página."""

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.juris = raiz / "derecho" / "fuentes" / "jurisprudencia"
        f = self.juris / "procedencia.json"
        if not f.is_file():
            self.skipTest("no esta la capa de fuentes")
        self.proc = json.loads(f.read_text(encoding="utf-8"))["fallos"]

    def test_el_html_empieza_y_termina_en_el_div(self):
        """No se controla la AUSENCIA de etiquetas de página: JUBA emite la sentencia envuelta
        en un `<html>` suelto adentro de un `<p>`, así que eso es carga y no maqueta. Lo que se
        controla son los bordes, que es donde se ve si se guardó el recorte o la página."""
        mirados = 0
        for slug, reg in sorted(self.proc.items()):
            archivo = self.juris / reg["archivo"]
            if not reg["archivo"].endswith(".html") or not archivo.is_file():
                continue
            mirados += 1
            with self.subTest(slug):
                crudo = archivo.read_bytes().strip()
                self.assertTrue(crudo[:60].lower().startswith(b'<div class="contenido"'),
                                f"no arranca en el div de contenido: {crudo[:60]!r}")
                self.assertTrue(crudo.endswith(b"</div>"),
                                f"no termina en el cierre del div: {crudo[-60:]!r}")
        self.assertGreater(mirados, 0, "dejaron de controlarse los .html de jurisprudencia")


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
        raiz = RAIZ_DEL_CHECKOUT
        modulo = (raiz / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "transito.md")
        decreto = raiz / "derecho" / "fuentes" / "normas" / "pba-decreto-532-2009.txt"
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


class TestLosDosAgentesLeenLoMismo(unittest.TestCase):
    """`CLAUDE.md` tiene que importar `AGENTS.md`, y `AGENTS.md` tiene que ser el contenido.

    Los dos agentes leen archivos distintos: Codex lee `AGENTS.md` y Claude Code lee
    `CLAUDE.md`. La única forma de que lean lo mismo sin duplicarlo es la importación
    `@AGENTS.md`, que Claude Code expande al abrir la sesión. Por eso el contenido vive en el
    archivo del agente que NO tiene con qué importar.

    Lo que este control impide son las tres maneras de romperlo, y ninguna avisa sola:

    1. **Que se borre la línea de importación.** Claude Code se queda sin las reglas del
       repositorio y sigue trabajando como si no existieran.
    2. **Que la importación quede adentro de acentos graves.** La documentación es explícita:
       `` `@AGENTS.md` `` entre backticks es texto literal y no importa nada. Se ve igual.
    3. **Que el contenido se copie a `CLAUDE.md`.** Ahí habría dos copias de las reglas y la
       que se corrija va a ser una sola.

    Las reglas del repositorio viven repartidas entre `AGENTS.md` y `.claude/rules/*.md`. Acá
    se miden dos fallas propias: la importación rota (casos 1 y 2 de arriba) y la copia del
    contenido a `CLAUDE.md` (caso 3), con el tope de palabras sobre `CLAUDE.md` -si el
    contenido se duplicara ahí, el archivo crecería por encima de "la importación más lo
    exclusivo de Claude Code". El piso de 2000 palabras sobre `AGENTS.md` más las reglas
    atrapa una falla distinta: que el conjunto se vacíe, borrado en vez de repartido.

    Lo que este piso NO atrapa es CÓMO se reparte: una sección puede mudarse entera de
    `AGENTS.md` a una regla de `.claude/rules/` con `paths:` de alcance angosto -que casi
    nunca carga- sin que la suma baje un solo caracter, porque el volumen sigue estando en
    algún `.md` del repositorio. Eso lo vigila `TestDondeVaCadaRegla`, en
    `herramientas/test_markdown.py`: nombra una por una las secciones de `AGENTS.md` que
    rigen siempre y le pone un piso de palabras a cada región del archivo.

    No se comprueba por symlink porque en Windows hace falta Developer Mode, y este
    repositorio declara que corre en Windows.
    """

    def test_claude_md_importa_agents_md_y_no_lo_duplica(self):
        raiz = RAIZ_DEL_CHECKOUT
        claude, agents = raiz / "CLAUDE.md", raiz / "AGENTS.md"
        reglas = sorted((raiz / ".claude" / "rules").rglob("*.md")) if (raiz / ".claude" / "rules").is_dir() else []
        self.assertTrue(agents.is_file(), "no está AGENTS.md: ahí viven las reglas")
        self.assertTrue(claude.is_file(), "no está CLAUDE.md: Claude Code no lee AGENTS.md")
        texto = claude.read_text(encoding="utf-8")
        sin_codigo = re.sub(r"`[^`]*`", " ", texto)
        # (?m) y no `\s*$`: sin multilínea el ancla es la cadena entera, y `\s` se come los
        # saltos, así que el renglón «suelto» dejaría de estar suelto.
        self.assertRegex(sin_codigo, r"(?m)^@AGENTS\.md[ \t]*$",
                         "CLAUDE.md no importa AGENTS.md fuera de acentos graves: la "
                         "importación tiene que ir sola en su renglón y sin backticks, o "
                         "Claude Code la lee como texto y se queda sin las reglas")
        # Y que no sea una copia: el que lleva el contenido es uno solo.
        self.assertLess(len(texto.split()), 400,
                        "CLAUDE.md creció: las reglas van en AGENTS.md o en .claude/rules/, "
                        "y acá sólo la importación más lo que es exclusivo de Claude Code")
        texto_agents = agents.read_text(encoding="utf-8")
        palabras_reglas = len(texto_agents.split())
        palabras_reglas += sum(len(p.read_text(encoding="utf-8").split()) for p in reglas)
        self.assertGreater(palabras_reglas, 2000,
                           "AGENTS.md más .claude/rules/*.md quedó corto: ¿se movió el "
                           "contenido a CLAUDE.md o se borró en vez de repartirse entre los "
                           "dos destinos?")

    def test_los_claude_md_de_capa_2_estan_excluidos(self):
        """Claude Code carga un `CLAUDE.md` de subdirectorio al leer archivos de esa carpeta.

        Bajo `derecho/kb/` hay dos, y son perfiles de práctica de otro autor escritos para ser
        obedecidos. Sin la exclusión, quien desarrolle el repositorio recibe como instrucción
        el material que la frontera de licencia dice que sólo se cita y se contradice. La
        exclusión va en `.claude/settings.json`, que por eso está versionado.
        """
        raiz = RAIZ_DEL_CHECKOUT
        ajustes = raiz / ".claude" / "settings.json"
        if not (raiz / "derecho" / "kb").is_dir():
            self.skipTest("no esta la capa 2")
        self.assertTrue(ajustes.is_file(),
                        ".claude/settings.json no está: se versiona a propósito, porque "
                        "`claudeMdExcludes` tiene que viajar al clon")
        excluidos = json.loads(ajustes.read_text(encoding="utf-8")).get("claudeMdExcludes", [])
        encontrados = sorted(p.relative_to(raiz).as_posix()
                             for p in (raiz / "derecho" / "kb").rglob("CLAUDE.md"))
        for ruta in encontrados:
            with self.subTest(ruta):
                self.assertTrue(any(ruta in patron for patron in excluidos),
                                f"{ruta} es capa 2 y Claude Code lo cargaría como "
                                f"instrucción: falta en `claudeMdExcludes`")
        self.assertGreater(len(encontrados), 0,
                           "no se encontró ningún CLAUDE.md en kb/: el control quedó vacío")


class TestEncabezadoDeLosModulos(unittest.TestCase):
    """Todos los módulos abren con el MISMO encabezado, palabra por palabra.

    No es prolijidad: un módulo se lee solo. La skill carga `laboral.md` sin cargar los otros
    veintinueve, así que lo que el encabezado no diga ahí, ahí no está dicho. Y lo que tiene
    que decir es que rigen las reglas de integridad de la sección 2 --las que prohíben
    afirmar una norma sin fuente a la vista--.

    Había derivado a **21 redacciones distintas en 30 archivos**, y sólo 13 nombraban esas
    reglas. Los otros 17 no las negaban: no las mencionaban, que para quien lee un archivo
    solo es lo mismo. Una convención que se copia a mano treinta veces diverge; el candado es
    esto.

    Lo que sigue siendo propio de cada módulo --la jurisdicción de lo procesal, qué quedó sin
    cerrar, que es el espejo de otro-- va DESPUÉS, en el mismo bloque. Lo común va primero y
    es idéntico.
    """

    COMUN = ("Módulo de referencia de la skill `derecho-argentino`. Numeración global: las "
             "remisiones cruzadas entre módulos siguen siendo válidas. **Rigen las reglas de "
             "integridad de la sección 2 del SKILL.md.**")

    # `danos-indice-doctrinario.md` no es un módulo de derecho sino el índice de una obra
    # comercial que vive en `_local/`: no lo lee la skill como módulo y no abre con el bloque.
    SIN_ENCABEZADO = {"danos-indice-doctrinario.md"}

    def test_todos_abren_con_el_mismo_encabezado(self):
        base = RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "references"
        if not base.is_dir():
            self.skipTest("no esta la skill")
        modulos = [p for p in sorted(base.glob("*.md")) if p.name not in self.SIN_ENCABEZADO]
        self.assertGreater(len(modulos), 25, "no encontré los módulos: el control está apagado")
        for p in modulos:
            lineas = p.read_text(encoding="utf-8").splitlines()
            bloque = []
            for l in lineas[:20]:
                if l.startswith(">"):
                    bloque.append(l.lstrip(">").strip())
                elif bloque:
                    break
            texto = " ".join(bloque)
            with self.subTest(p.name):
                self.assertTrue(texto.startswith(self.COMUN),
                                f"{p.name} no abre con el encabezado común. Empieza con:\n"
                                f"  {texto[:120]}\nY tiene que empezar con:\n"
                                f"  {self.COMUN[:120]}")


class TestContradiccionesNominadas(unittest.TestCase):
    """Cada cita entrecomillada de un bloque de contradicciones tiene que estar en `kb/`.

    Esos bloques citan al perfil para nombrar su error, así que la cita tiene que ser
    textual: si no aparece literalmente bajo `kb/`, el módulo está discutiendo con una frase
    que nadie escribió, o el perfil cambió y la contradicción quedó vieja.
    """

    CITA = re.compile(r'\*"([^"]{15,})"\*')

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.referencias = raiz / "derecho" / "skills" / "derecho-argentino" / "references"
        kb = raiz / "derecho" / "kb"
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


class TestElDescriptionDeHonorariosNombraLosDosAranceles(unittest.TestCase):
    """Un pin sobre `honorarios`, NO un control de la clase: los otros comandos no lo tienen.

    El `description` es lo que se lee antes de decidir si se invoca el comando, y el cuerpo de
    `honorarios` atiende tres jurisdicciones: PBA calcula por la Ley 14.967, la nacional y federal
    explica la Ley 27.423 sin dar número, y el resto ni se explica. **Anunciar una sola es peor
    que no anunciar ninguna**: quien tiene una causa federal lee "Buenos Aires", no invoca el
    comando y contesta de memoria — el error que la puerta del cuerpo existe para atajar,
    salteado antes de llegar a ella.

    **El control general no existe y está medido:** exigir que toda ley del cuerpo aparezca en el
    `description` es falso hoy en `intereses` —11.653 y 14.399 en el cuerpo, ninguna en su
    descripción, y con razón— y en `liquidacion`. Se descartó en vez de calibrarlo. Por eso esto
    pinta un solo archivo y no pretende cubrir a los nueve.

    Mutación que lo comprueba: sacarle `27.423` al `description` de `derecho/commands/honorarios.md`
    deja el test en rojo. Sacarle `14.967`, también.
    """

    ARANCELES = ("14.967", "27.423")

    def setUp(self):
        self.comando = Path(__file__).resolve().parents[3] / "commands" / "honorarios.md"
        texto = self.comando.read_text(encoding="utf-8")
        _, self.frente, self.cuerpo = texto.split("---", 2)

    def test_el_description_nombra_las_dos_leyes_arancelarias(self):
        declarado = re.search(r"^description:(.*)$", self.frente, re.M)
        self.assertIsNotNone(declarado, "honorarios.md no declara `description`")
        descripcion = declarado.group(1)
        for ley in self.ARANCELES:
            with self.subTest(ley):
                self.assertIn(ley, descripcion,
                              f"el description de honorarios no nombra la Ley {ley}: anuncia un "
                              f"alcance más angosto que la puerta del cuerpo")

    def test_el_cuerpo_sigue_atendiendo_las_dos(self):
        """Si el cuerpo deja de rutear las dos, el pin de arriba pasa a pedir una mentira."""
        for ley in self.ARANCELES:
            with self.subTest(ley):
                self.assertIn(ley, self.cuerpo,
                              f"el cuerpo de honorarios ya no nombra la Ley {ley}: revisar el "
                              f"description antes de tocar este test")


class TestLaSerieDeLaUMA(unittest.TestCase):
    """La UMA se carga a mano y el script se planta si no está: no hay número por ausencia.

    La consulta oficial de la CSJN es un formulario, no una tabla, así que no hay descargador
    —es la pared que `docs/PENDIENTES.md` describe en *Los registros judiciales no se pueden
    buscar*— y `uma-csjn.csv` nace vacío. El riesgo
    de una serie vacía no es que falle: es que devuelva algo. Un cero, el valor más viejo
    extrapolado hacia atrás o una excepción tragada dan un importe con cara de correcto, y el
    art. 51 hace que ese importe termine en una resolución.

    Mutaciones que lo comprueban, las tres corridas:
      · que `uma_a_fecha` devuelva `filas[0]` cuando la fecha es anterior a toda vigencia
        —extrapolar hacia atrás— deja en rojo a `test_no_extrapola_hacia_atras`;
      · que `_filas` acepte filas con la columna `uma` vacía deja en rojo a
        `test_una_fila_sin_valor_no_cuenta`;
      · que el bloque de `estado.py` reporte `OK` en vez de `FALTA` con la serie vacía
        deja en rojo a
        `test_estado_no_da_verde_con_la_serie_vacia`.
    """

    ENCABEZADO = "vigencia_desde,uma,resolucion,fuente"

    def _repo(self, filas: str) -> str:
        """Un repo de mentira con la marca estructural y la serie que le pasemos."""
        d = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        (d / _raiz.MARCADOR).parent.mkdir(parents=True, exist_ok=True)
        (d / _raiz.MARCADOR).write_text("manifiesto de mentira\n", encoding="utf-8")
        datos = d / _raiz.SUB / "fuentes" / "datos"
        datos.mkdir(parents=True, exist_ok=True)
        (datos / "uma-csjn.csv").write_text(
            f"# serie de prueba\n# verificado: 2026-09-17\n{self.ENCABEZADO}\n{filas}",
            encoding="utf-8")
        return str(d)

    def _corre(self, repo: str, *args):
        return subprocess.run(
            [sys.executable, str(pathlib.Path(__file__).parent / "uma_csjn.py"),
             "--repo", repo, *args],
            capture_output=True, text=True, env=_sin_color())

    def test_toma_la_ultima_vigencia_que_no_es_posterior(self):
        repo = self._repo("2026-06-01,80000,,\n2026-08-01,95626,SGA 1076/2026,\n")
        r = self._corre(repo, "--fecha", "2026-07-15")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("80000", r.stdout)
        self.assertNotIn("95626", r.stdout, "tomó una vigencia POSTERIOR a la fecha pedida")

    def test_no_extrapola_hacia_atras(self):
        repo = self._repo("2026-06-01,80000,,\n")
        r = self._corre(repo, "--fecha", "2026-01-10")
        self.assertEqual(r.returncode, 2, "una fecha previa a la serie tiene que plantarse")
        self.assertIn("CONFIGURACIÓN INCOMPLETA", r.stdout)
        self.assertNotIn("80000", r.stdout, "extrapoló el valor más viejo hacia atrás")

    def test_una_fila_sin_valor_no_cuenta(self):
        r = self._corre(self._repo("2026-06-01,,,\n"), "--fecha", "2026-07-01")
        self.assertEqual(r.returncode, 2, "una fila con la columna `uma` vacía no es un valor")
        self.assertIn("CONFIGURACIÓN INCOMPLETA", r.stdout)

    def test_la_serie_vacia_se_planta_y_dice_donde_buscar(self):
        r = self._corre(self._repo(""), "--fecha", "2026-09-01")
        self.assertEqual(r.returncode, 2)
        self.assertIn("CONFIGURACIÓN INCOMPLETA", r.stdout)
        self.assertIn("csjn.gov.ar/transparencia/uma", r.stdout,
                      "el plantón tiene que decir de dónde se saca el dato")

    def test_convierte_en_las_dos_direcciones(self):
        repo = self._repo("2026-08-01,100000,,\n")
        ida = self._corre(repo, "--fecha", "2026-08-10", "--pesos", "4500000")
        self.assertEqual(ida.returncode, 0, ida.stderr)
        self.assertIn("45.000 UMA", ida.stdout)
        vuelta = self._corre(repo, "--fecha", "2026-08-10", "--uma", "45")
        self.assertEqual(vuelta.returncode, 0, vuelta.stderr)
        self.assertIn("4500000.00", vuelta.stdout)

    def test_la_serie_del_repo_declara_su_contrato(self):
        """El archivo real: nace sin valores, pero con la línea que `estado.py` compara."""
        real = pathlib.Path(__file__).resolve().parents[3] / "fuentes" / "datos" / "uma-csjn.csv"
        self.assertTrue(real.is_file(), "falta derecho/fuentes/datos/uma-csjn.csv")
        texto = real.read_text(encoding="utf-8")
        self.assertRegex(texto, r"(?m)^# verificado:",
                         "la serie no declara la línea de contrato `# verificado:`")
        self.assertIn("csjn.gov.ar/transparencia/uma", texto,
                      "la serie no dice de dónde salen sus valores")
        self.assertRegex(texto, r"(?m)^" + re.escape(self.ENCABEZADO) + r"\s*$",
                         "las columnas de la serie cambiaron: uma_csjn.py las lee por nombre")

    def test_estado_no_da_verde_con_la_serie_vacia(self):
        """El instrumento apagado no puede reportar OK: hoy la serie real está sin cargar."""
        import estado
        bloques = {b["bloque"]: b for b in estado.revisar(_raiz.raiz_repo()[0])}
        self.assertIn("UMA", bloques, "estado.py no reporta la serie de la UMA")
        self.assertNotEqual(bloques["UMA"]["estado"], "OK",
                            "la serie está vacía y estado.py la dio por buena")


class TestManifiestoDeCodex(unittest.TestCase):
    """Codex lee este manifiesto con reglas estrechas, y cuando algo no encaja no protesta.

    Tres cosas, todas leídas del código de `openai/codex` y todas silenciosas si fallan:

    1. Elige el `plugin.json` de la raíz del plugin SÓLO si su `$schema` empieza con la URL de
       agent-plugins.org; si no, lo ignora y cae a `.codex-plugin/plugin.json`, que acá no
       existe. Un `$schema` cambiado deja al plugin sin manifiesto.
    2. `interface` lo lee del PRIMER NIVEL. Anidado bajo `extensions` no llega: serde descarta
       la clave que no conoce y el ícono no aparece, sin error.
    3. Las rutas de los assets tienen que empezar literalmente con `./`, no llevar `..` y
       resolver bajo la raíz del plugin. Cualquier otra cosa se descarta con un warning.

    El espejo bajo `extensions` se conserva aparte: la app de escritorio muestra el
    `shortDescription`, que por el camino de arriba no debería ver. Mientras las dos lecturas no
    coincidan se sirven las dos, y este test las mantiene iguales para que no se despeguen.
    """

    RAIZ = Path(__file__).resolve().parents[3]
    ESQUEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"

    def setUp(self):
        manifiesto = self.RAIZ / "plugin.json"
        self.assertTrue(manifiesto.exists(), f"falta {manifiesto}")
        self.datos = json.loads(manifiesto.read_text(encoding="utf-8"))
        self.interface = self.datos.get("interface")

    def test_el_schema_es_el_que_codex_reconoce(self):
        self.assertEqual(self.datos.get("$schema"), self.ESQUEMA,
                         "con otro $schema Codex ignora este archivo y busca .codex-plugin/")

    def test_el_interface_esta_en_el_primer_nivel(self):
        self.assertIsNotNone(self.interface,
                             "`interface` sólo se lee del primer nivel: bajo `extensions` no llega")
        self.assertIn("displayName", self.interface)

    def test_el_espejo_de_extensions_dice_lo_mismo(self):
        espejo = self.datos["extensions"]["com.openai"]["interface"]
        self.assertEqual(self.interface, espejo,
                         "el `interface` de primer nivel y el de `extensions` se despegaron")

    def test_toda_ruta_de_asset_es_relativa_y_existe(self):
        rutas = {c: v for c, v in self.interface.items()
                 if isinstance(v, str) and ("/" in v or v.endswith(".png"))}
        self.assertTrue(rutas, "el interface no declara ninguna ruta: el test mira nada")
        for campo, ruta in sorted(rutas.items()):
            if ruta.startswith("http"):
                continue
            with self.subTest(campo):
                self.assertTrue(ruta.startswith("./"),
                                f"`{campo}` vale {ruta}: Codex exige que empiece con `./`")
                self.assertNotIn("..", ruta, f"`{campo}` sale de la raíz del plugin")
                self.assertTrue((self.RAIZ / ruta[2:]).exists(),
                                f"`{campo}` apunta a {ruta}, que no existe bajo {self.RAIZ.name}/")

    def test_los_iconos_del_plugin_son_identicos_a_los_de_la_marca(self):
        # El generador de la marca no escribe estas copias y `test_marca.py` no sabe que existen:
        # son las que se despegan sin que nadie se entere. Byte a byte, no parecido.
        for nombre in ("icono.png", "icono-oscuro.png"):
            copia = self.RAIZ / "assets" / nombre
            fuente = self.RAIZ.parent / "assets" / "marca" / nombre
            with self.subTest(nombre):
                for ruta in (copia, fuente):
                    self.assertTrue(ruta.exists(), f"falta {ruta}")
                self.assertEqual(copia.read_bytes(), fuente.read_bytes(),
                                 f"{nombre} del plugin se despegó del que genera la marca: "
                                 f"copiá assets/marca/{nombre} a derecho/assets/, no lo edites acá")



class TestNormasDeCambiosRecientes(unittest.TestCase):
    """Toda norma nombrada en «Cambios recientes» está declarada o tiene veredicto escrito.

    Es el hueco que ninguna otra medida tapa. `cobertura_normativa.py` cruza las leyes que un
    módulo cita **con articulado**, así que una resolución nombrada en una lista de cambios
    recientes no cae en su ventana: puede quedar ahí sin que nada la reclame. Y es justamente
    donde el repositorio anota lo más volátil —montos, reglamentaciones del semestre—, que es
    lo primero que envejece.

    La salida es la misma que para el articulado: o la norma está en `normas.json`, o alguien
    escribió por qué no, en `cobertura-revisada.json`. Lo que no se admite es el silencio.
    """

    RAIZ = Path(__file__).resolve().parents[4]
    SECCION = "## 13 ·"
    # Una norma se reconoce por la palabra que la nombra, no por su forma: en `12/12/2024` el
    # `12/2024` no es ninguna norma. La prosa además las enumera —"Decretos 407, 408 y
    # 409/2026"—, y ahí el año del final vale para toda la lista.
    CLAVE = r"(?:Ley(?:es)?|Res\.|Resoluci[oó]n|Decretos?|RG(?:\s+ARCA)?)"
    LISTA = re.compile(
        CLAVE + r"[^\n:;]{0,24}?((?:\d{1,4}(?:\.\d{3})?)(?:\s*(?:,|y)\s*\d{1,4})*\s*/?\s*\d{0,4})")

    @staticmethod
    def _clave(numero: str) -> str:
        """Clave canónica de una norma: `4/2026` -> `4|2026`, `27.802` -> `27802`.

        Se compara por igualdad y NO por subcadena: aplanados a dígitos, `5844/2026` contiene
        a `4/2026`, así que una norma borrada del manifiesto seguía pareciendo declarada
        porque otra, sin relación, la contenía.
        """
        if "/" in numero:
            cuerpo, anio = numero.split("/", 1)
            return f"{cuerpo.strip()}|{anio.strip()}"
        return numero.replace(".", "").strip()

    @classmethod
    def _clave_de_slug(cls, slug: str) -> str:
        """Misma clave, leída del slug: `res-srt-39-2026` -> `39|2026`, `ley-27802` -> `27802`."""
        con_anio = re.search(r"-(\d{1,4})-(\d{4})$", slug)
        if con_anio:
            return f"{con_anio.group(1)}|{con_anio.group(2)}"
        suelto = re.search(r"-(\d{4,5})$", slug)
        return suelto.group(1) if suelto else ""

    @classmethod
    def _normas_de(cls, renglon: str) -> list:
        salida = []
        for tramo in cls.LISTA.findall(renglon):
            tramo = tramo.strip()
            if "/" in tramo:
                cuerpo, anio = tramo.rsplit("/", 1)
                if not (anio.isdigit() and len(anio) == 4):
                    continue
                salida += [f"{numero}/{anio}" for numero in re.findall(r"\d{1,4}", cuerpo)]
            elif "." in tramo:
                salida.append(tramo)
        return salida

    def setUp(self):
        modulo = (self.RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "changelog-normativo.md")
        self.assertTrue(modulo.exists(), f"falta {modulo}")
        texto = modulo.read_text(encoding="utf-8")
        self.assertIn(self.SECCION, texto,
                      f"no está la sección «{self.SECCION}»: el test quedó mirando otra cosa")
        seccion = texto.split(self.SECCION)[1].split("\n---")[0]
        self.renglones = [l for l in seccion.splitlines() if l.startswith("- **")]
        self.vinetas = [l for l in seccion.splitlines()
                        if re.match(r"\s*[-*+]\s|\s*\d+[.)]\s", l)]

        normas = json.loads((self.RAIZ / "derecho" / "fuentes" / "normas" / "normas.json")
                            .read_text(encoding="utf-8"))["normas"]
        self.declarado = {self._clave_de_slug(n["slug"]) for n in normas} - {""}
        revisadas = json.loads((self.RAIZ / "herramientas" / "cobertura-revisada.json")
                               .read_text(encoding="utf-8"))
        crudo = json.dumps(revisadas.get("leyes", {}), ensure_ascii=False)
        self.con_veredicto = {self._clave(n) for n in
                              re.findall(r"\d{1,3}\.\d{3}|\d{1,4}/\d{4}", crudo)}

    def test_el_lector_ve_todos_los_renglones_de_la_seccion(self):
        # Sin umbral: si un renglón de la lista cambia de marcador o de forma, el lector lo
        # pierde y el test de cobertura pasa en verde sin haberlo mirado. Un número mínimo no
        # se entera de eso, porque los otros seis ya lo superan solos.
        self.assertTrue(self.vinetas, "«Cambios recientes» no tiene ningún renglón de lista")
        perdidos = [l for l in self.vinetas if l not in self.renglones]
        self.assertEqual(perdidos, [],
                         "el lector no reconoce estos renglones de «Cambios recientes», así que "
                         "las normas que nombran no las revisa nadie: " + "; ".join(
                             l.strip()[:60] for l in perdidos))

    def test_las_claves_no_se_confunden_entre_si(self):
        # El caso que rompió la versión anterior: por subcadena, `5844/2026` tapaba a `4/2026`.
        self.assertNotEqual(self._clave("4/2026"), self._clave("5844/2026"))
        self.assertEqual(self._clave("39/2026"), self._clave_de_slug("res-srt-39-2026"))
        self.assertEqual(self._clave("27.802"), self._clave_de_slug("ley-27802"))
        self.assertEqual(self._clave("15.563"), self._clave_de_slug("pba-ley-15563"))
        self.assertEqual(self._clave("409/2026"), self._clave_de_slug("decreto-409-2026"))

    def test_el_lector_acierta_en_los_casos_de_control(self):
        # Un lector que se equivoca en un renglón conocido no sirve para los que nadie miró.
        self.assertEqual(
            self._normas_de("Decretos 407, 408 y 409/2026 (BO 01/06/2026): reglamentación de "
                            "la Ley 27.802"),
            ["407/2026", "408/2026", "409/2026", "27.802"],
            "el lector no abre la enumeración de decretos o pierde la ley del final")
        self.assertEqual(self._normas_de("PBA - Ley 15.513 (sancionada 12/12/2024)"), ["15.513"],
                         "el lector confunde una fecha con un número de norma")

    def test_cada_norma_listada_esta_declarada_o_tiene_veredicto(self):
        for renglon in self.renglones:
            corto = re.sub(r"\*\*|\s+", " ", renglon[2:]).strip()[:60]
            with self.subTest(corto):
                numeros = self._normas_de(renglon)
                self.assertTrue(numeros, f"«{corto}» no nombra ninguna norma reconocible")
                for numero in numeros:
                    clave = self._clave(numero)
                    self.assertTrue(clave in self.declarado or clave in self.con_veredicto,
                                    f"«{corto}» nombra la norma {numero}, que no está declarada "
                                    f"en normas.json ni tiene veredicto en "
                                    f"cobertura-revisada.json. No la reclama ninguna herramienta.")


class TestPlantillaDelEncabezado(unittest.TestCase):
    """La plantilla del encabezado tiene que formatear con los nombres que el script le pasa.

    Un marcador de `str.format` es un identificador, no prosa: acentuar `{jurisdicción}` deja la
    plantilla sintácticamente perfecta y rompe la descarga entera con un `KeyError`, en la
    llamada y no al importar. Ningún test lo veía porque nadie formateaba la plantilla sin bajar
    una norma de verdad. Esto la formatea en seco.
    """

    RUTA = (Path(__file__).resolve().parents[3] / "fuentes" / "scripts" / "descargar_normas.py")

    def setUp(self):
        self.assertTrue(self.RUTA.exists(), f"falta {self.RUTA}")
        self.fuente = self.RUTA.read_text(encoding="utf-8")

    def _plantilla(self) -> str:
        hallada = re.search(r'ENCABEZADO = """(.*?)"""', self.fuente, re.S)
        self.assertIsNotNone(hallada, "no se encontró ENCABEZADO: el test quedó mirando nada")
        return hallada.group(1)

    def _llamada(self) -> set:
        """Los nombres que el script le pasa a .format(), leídos de la llamada real."""
        hallada = re.search(r"ENCABEZADO\.format\((.*?)\)\n", self.fuente, re.S)
        self.assertIsNotNone(hallada, "no se encontró la llamada a ENCABEZADO.format()")
        return set(re.findall(r"(\w+)\s*=", hallada.group(1)))

    def test_los_marcadores_son_ascii(self):
        for marcador in re.findall(r"\{(\w+)\}", self._plantilla()):
            with self.subTest(marcador):
                self.assertEqual(marcador, marcador.encode("ascii", "ignore").decode(),
                                 f"`{{{marcador}}}` lleva un carácter no ASCII: es un "
                                 f"identificador de format(), no prosa, y rompe la descarga")

    def test_la_plantilla_formatea_con_lo_que_el_script_le_pasa(self):
        pasados = self._llamada()
        self.assertIn("titulo", pasados, "la llamada no se leyó bien: faltan los nombres")
        pedidos = set(re.findall(r"\{(\w+)\}", self._plantilla()))
        self.assertEqual(pedidos - pasados, set(),
                         "la plantilla pide marcadores que la llamada no pasa: la descarga "
                         "muere con KeyError recién al bajar la primera norma")
        # Y se formatea de verdad, que es lo único que prueba que no hay KeyError.
        self._plantilla().format(**{nombre: "x" for nombre in pasados})

    def _texto_fijo(self) -> list:
        """Los tramos de la plantilla que no son marcadores: etiquetas y prosa.

        Es lo que queda igual en todo `.txt` bajado, así que es lo comparable. Se saca por
        renglón y sacándole los `{marcador}`, que son lo único que varía de archivo a archivo.
        """
        tramos = []
        for renglon in self._plantilla().splitlines():
            fijo = re.sub(r"\{\w+\}", "", renglon).strip()
            if fijo and set(fijo) != {"="}:
                tramos.append(fijo)
        return tramos

    def test_el_texto_fijo_del_encabezado_no_se_bifurca_del_corpus(self):
        # Los .txt ya bajados llevan escrito este mismo encabezado, así que la plantilla y el
        # corpus son el mismo texto en dos lugares: retocar una palabra acá y no más lo parte en
        # dos, los viejos con una forma y los nuevos con otra.
        #
        # Realinearlo NO exige bajar las normas de nuevo, y creer que sí mantuvo la prosa del
        # encabezado en ASCII durante varias versiones. El encabezado queda fuera de
        # `sha256_texto`, que se calcula sobre el cuerpo: se reescribe en los archivos que ya
        # están, en BYTES para no colapsar los CRLF, y se recalcula `sha256_archivo`.
        #
        # Se comparan TODOS los tramos fijos, etiquetas y prosa. Mirar una etiqueta por
        # posición no alcanza: en cuanto el encabezado gana un renglón, el control pasa a medir
        # la etiqueta de al lado -que el corpus también tiene-, se queda verde, y lo que cambió
        # deja de mirarse. Y la prosa quedaba afuera del todo, que es por donde se bifurcó.
        normas = self.RUTA.resolve().parents[1] / "normas"
        bajados = sorted(normas.glob("*.txt"))
        if not bajados:
            self.skipTest("no hay .txt bajados contra los que comparar")
        tramos = self._texto_fijo()
        self.assertGreater(len(tramos), 5,
                           "se leyeron muy pocos tramos fijos: el test quedó mirando casi nada")
        textos = [(p.name, p.read_text(encoding="utf-8")) for p in bajados]
        for fijo in tramos:
            with self.subTest(fijo[:40]):
                distintos = [nombre for nombre, texto in textos if fijo not in texto]
                self.assertEqual(distintos[:5], [],
                                 f"la plantilla escribe «{fijo[:60]}» y {len(distintos)} de "
                                 f"{len(textos)} archivos ya bajados usan otra forma: o se "
                                 f"revierte la plantilla, o se les reescribe el encabezado en "
                                 f"bytes y se recalcula sha256_archivo. Bajar de nuevo no hace "
                                 f"falta: el encabezado no entra en sha256_texto")


class TestTramosDelSMVM(unittest.TestCase):
    """El cuadro de 5.12 bis tiene que decir lo que dice el texto de la Res. 4/2026.

    Es un monto escrito en un módulo, que es la forma más cara de equivocarse que tiene este
    repositorio: nadie lo ve. Entra porque la resolución fija tramos con fecha de comienzo, así
    que cada uno queda acotado por el siguiente y se vence a la vista. Lo que este test sostiene
    es la otra mitad: que lo escrito sea lo transcripto, tramo por tramo y peso por peso, contra
    el consolidado con procedencia y no contra la memoria de nadie.
    """

    RAIZ = Path(__file__).resolve().parents[4]
    SLUG = "res-cnepysmvym-4-2026"
    MESES = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05",
             "junio": "06", "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10",
             "noviembre": "11", "diciembre": "12"}

    def setUp(self):
        fuente = self.RAIZ / "derecho" / "fuentes" / "normas" / f"{self.SLUG}.txt"
        if not fuente.exists():
            self.skipTest(f"no está bajado {self.SLUG}.txt: sin fuente no se mide")
        self.modulo = (self.RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"
                       / "laboral.md").read_text(encoding="utf-8")
        self.texto = fuente.read_text(encoding="utf-8")

    def _de_la_norma(self) -> list:
        cuerpo = self.texto.split("ARTÍCULO 2")[0]
        partes = re.split(r"\n([a-z])\.-\s", cuerpo)[1:]
        filas = []
        for tramo in partes[1::2]:
            fecha = re.search(r"A partir del 1°\s+de\s+(\w+)\s+(?:de\s+)?(\d{4})", tramo)
            montos = re.findall(r"\$\s?([\d.]+)", tramo)
            if not fecha or len(montos) < 2:
                continue
            filas.append((f"01/{self.MESES[fecha.group(1).lower()]}/{fecha.group(2)}",
                          montos[0], montos[1]))
        return filas

    def _del_modulo(self) -> list:
        bloque = self.modulo.split("### 5.12 bis")[1].split("\n### ")[0]
        return [(f, m.strip(), h.strip()) for f, m, h in
                re.findall(r"\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*\$\s*([\d.]+)\s*\|"
                           r"\s*\$\s*([\d.]+)\s*\|", bloque)]

    def test_el_lector_encuentra_las_dos_listas(self):
        # Si cualquiera de los dos lectores se apaga, la comparación de abajo da verde sobre dos
        # listas vacías, que es exactamente igual de verde que sobre dos listas iguales.
        self.assertGreaterEqual(len(self._de_la_norma()), 2, "no se leyeron tramos de la norma")
        self.assertGreaterEqual(len(self._del_modulo()), 2, "no se leyó el cuadro del módulo")

    def test_el_cuadro_dice_lo_mismo_que_la_norma(self):
        self.assertEqual(self._del_modulo(), self._de_la_norma(),
                         "el cuadro de SMVM de `laboral.md` 5.12 bis no coincide con "
                         f"{self.SLUG}.txt: se transcribe del consolidado, no de memoria")

    def test_el_modulo_cita_la_resolucion_que_transcribe(self):
        bloque = self.modulo.split("### 5.12 bis")[1].split("\n### ")[0]
        self.assertIn(self.SLUG, bloque,
                      "el cuadro no dice de qué archivo de fuentes/ sale: sin procedencia a la "
                      "vista, un monto escrito es una afirmación sin respaldo")


class TestOrigenDeLosFallos(unittest.TestCase):
    """Un fallo que no viene del registro del tribunal tiene que decir de dónde viene.

    La tabla de portales de `fuentes.md` 14 no es una lista de sitios confiables: es una regla de
    prelación, su texto prevalece ante discrepancia. Un repositorio que selecciona una parte, o un
    sitio privado, no puede reclamar eso — y sin embargo el documento puede ser el único disponible
    cuando ningún registro judicial publica esa instancia.

    La salida es el campo `origen`: el fallo entra, marcado por lo que es. Lo que no se admite es
    que una URL de cualquier lado se vea igual que una del registro.

    Los dominios permitidos NO están escritos acá: salen de la propia tabla de `fuentes.md`, para
    que agregar un portal sea un solo cambio y no dos que se despegan.
    """

    RAIZ = Path(__file__).resolve().parents[4]

    def setUp(self):
        fuentes = (self.RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"
                   / "fuentes.md").read_text(encoding="utf-8")
        # Anclado al renglón entero: partir por el prefijo hace que `### Portalesx` también
        # matchee, y el lector se queda leyendo otra tabla sin avisar.
        corte = re.search(r"^### Portales[ \t]*$", fuentes, re.M)
        self.assertIsNotNone(corte, "no está la tabla «### Portales» de fuentes.md")
        tabla = fuentes[corte.end():].split("\n###")[0]
        self.primarios = {re.sub(r"^www\.", "", h)
                          for h in re.findall(r"https://([^/\s|]+)", tabla)}
        self.assertGreaterEqual(len(self.primarios), 8,
                                "se leyeron muy pocos portales: el lector quedó apagado y "
                                "entonces cualquier dominio pasaría por no primario o al revés")
        datos = json.loads((self.RAIZ / "derecho" / "fuentes" / "jurisprudencia"
                            / "fallos.json").read_text(encoding="utf-8"))
        self.fallos = datos["fallos"]

    def _es_primario(self, url: str) -> bool:
        host = re.sub(r"^www\.", "", re.match(r"https?://([^/]+)", url).group(1)).lower()
        return any(host == p or host.endswith("." + p) for p in self.primarios)

    def test_el_lector_separa_los_dos_mundos(self):
        # Si diera todo primario o todo ajeno, el test de abajo no revisaría nada real.
        propios = [f for f in self.fallos if self._es_primario(f["url"])]
        ajenos = [f for f in self.fallos if not self._es_primario(f["url"])]
        self.assertTrue(propios, "ningún fallo quedó como de registro: el lector está roto")
        self.assertTrue(ajenos, "ningún fallo quedó fuera de la lista: si es cierto, este test "
                                "sobra; si no, el lector está roto")

    def test_todo_fallo_de_fuera_del_registro_declara_su_origen(self):
        for f in self.fallos:
            if self._es_primario(f["url"]):
                continue
            with self.subTest(f["slug"]):
                origen = f.get("origen", "").strip()
                self.assertTrue(origen,
                                f"{f['slug']} no sale de ningún portal de la tabla de fuentes.md "
                                f"y no declara `origen`: {f['url']}")
                self.assertGreater(len(origen), 40,
                                   f"{f['slug']}: el `origen` tiene que decir de dónde salió y "
                                   f"por qué no está el registro del tribunal")

    def test_nadie_declara_origen_viniendo_del_registro(self):
        # Al revés también importa: un `origen` sobre una URL del registro es ruido que enseña a
        # ignorar el campo, y el campo sólo sirve mientras signifique algo.
        for f in self.fallos:
            if f.get("origen") and self._es_primario(f["url"]):
                self.fail(f"{f['slug']} declara `origen` pero su URL sí es de la tabla de "
                          f"fuentes.md: sacalo, o el campo deja de querer decir algo")


class TestMapaDeCobertura(unittest.TestCase):
    """`docs/COBERTURA.md` nombra módulos, y esa lista se despega sola.

    El documento es un relevamiento fechado: que la taxonomía siga siendo la de las fuentes no lo
    puede verificar nadie, y así está dicho ahí. Lo que sí se puede sostener es la otra mitad —
    que los módulos que nombra existan, y que ningún módulo del repositorio quede sin mencionar.
    Sin esto, agregar un módulo deja el mapa mintiendo por omisión, que es la forma en que un
    documento de cobertura se vuelve inútil sin que nadie lo note.

    No se revisa el contenido de la taxonomía: eso se relee contra las fuentes y se cambia la
    fecha. Un test que pretendiera verificarlo daría verde sobre una opinión.
    """

    RAIZ = Path(__file__).resolve().parents[4]

    def setUp(self):
        self.doc = self.RAIZ / "docs" / "COBERTURA.md"
        self.assertTrue(self.doc.exists(), f"falta {self.doc}")
        self.texto = self.doc.read_text(encoding="utf-8")
        self.modulos = {p.name for p in
                        (self.RAIZ / "derecho" / "skills" / "derecho-argentino"
                         / "references").glob("*.md")}
        self.assertGreater(len(self.modulos), 10, "no se encontraron los módulos")

    def test_lleva_fecha_de_relevamiento(self):
        # Vale por su fecha: sin ella, un mapa viejo se lee como si fuera de hoy.
        self.assertRegex(self.texto, r"[Rr]elevado el \d{2}/\d{2}/\d{4}",
                         "COBERTURA.md no dice cuándo se relevó")

    def test_todo_modulo_que_nombra_existe(self):
        nombrados = set(re.findall(r"`([a-z0-9-]+\.md)`", self.texto)) & {
            n for n in re.findall(r"`([a-z0-9-]+\.md)`", self.texto)}
        nombrados = {n for n in nombrados if n not in ("AGENTS.md", "COBERTURA.md")}
        self.assertTrue(nombrados, "COBERTURA.md no nombra ningún módulo: el lector quedó apagado")
        for nombre in sorted(nombrados):
            with self.subTest(nombre):
                self.assertIn(nombre, self.modulos,
                              f"COBERTURA.md nombra {nombre}, que no está en references/")

    def test_las_ramas_con_modulo_estan_todas_nombradas(self):
        # Sólo los módulos de RAMA: los de infraestructura no son cobertura de materia y
        # nombrarlos en el mapa sería ruido.
        infraestructura = {"changelog-normativo.md", "escritos.md", "fuentes.md", "intake.md",
                           "marcadores.md", "modelos.md", "perfiles-heredados.md", "parte.md",
                           "plazos.md", "fallos-csjn.md", "danos-indice-doctrinario.md",
                           "sede-judicial-pba.md", "notificaciones-pba.md", "prueba-pericial.md",
                           "ejecucion.md", "telegramas.md", "contratos.md", "civil.md"}
        ramas = self.modulos - infraestructura
        # Con backticks y nombre completo, que es como el documento cita un módulo: buscar la
        # subcadena suelta haría que «tránsito» matchee dentro de «transitorio».
        citados = set(re.findall(r"`([a-z0-9-]+\.md)`", self.texto))
        faltan = sorted(r for r in ramas if r not in citados)
        self.assertEqual(faltan, [],
                         "estos módulos de rama existen y COBERTURA.md no los menciona, así que "
                         "el mapa miente por omisión: " + ", ".join(faltan))


def _sin_color(entorno: dict | None = None) -> dict:
    """El entorno del subproceso con el color apagado.

    `argparse` colorea su ayuda, y varios controles la PARSEAN con regex: con los escapes ANSI
    de por medio `--json` deja de encontrarse y `{a,b,c}` deja de matchear. No se posterga el
    problema limpiando la salida: se pide la ayuda sin color, que es el dato que se quiere
    medir. El color es del terminal, no del programa.

    MUTACIÓN que lo demuestra: sacar `NO_COLOR` del entorno pone en rojo
    `test_todo_valor_de_bandera_que_se_documenta_es_uno_de_los_validos` y
    `test_la_ayuda_de_json_dice_para_que_es_y_para_que_no`.
    """
    return {**(entorno if entorno is not None else os.environ), "NO_COLOR": "1"}


class TestBanderasDeLaAyuda(unittest.TestCase):
    """El ejemplo de uso del docstring es lo que un agente copia, y `argparse` lo imprime como
    descripción en `--help`. Si ahí una bandera está escrita distinto de como la declara
    `add_argument`, el primer intento falla con código 2.

    Pasó de verdad: el docstring de `liquidacion_lct.py` decía `--extinción`,
    `--mejor-remuneración` y `--remuneración-ultimo-mes`, con tilde, contra las banderas ASCII
    del parser. Un agente que leyó el archivo copió el ejemplo y el primer llamado se cayó.
    Es la regla de ortografía del proyecto —si se compara, no se acentúa— aplicada donde más
    cuesta verla: la bandera no se muestra, se compara carácter por carácter.
    """

    def setUp(self):
        aqui = Path(__file__).parent
        self.guiones = [g for g in sorted(aqui.glob("*.py"))
                        if not g.name.startswith(("test_", "_"))]
        raiz = RAIZ_DEL_CHECKOUT
        if raiz:
            # `herramientas/` también: no se instala con el plugin, pero `AGENTS.md` manda
            # correr esos comandos y de ahí se copian igual.
            for carpeta in (raiz / "derecho" / "fuentes" / "scripts", raiz / "herramientas"):
                self.guiones += [g for g in sorted(carpeta.glob("*.py"))
                                 if not g.name.startswith(("test_", "_"))]
        self.assertTrue(self.guiones, "no encontré ningún script que revisar")

    @staticmethod
    def _declaradas(texto):
        """Banderas que el script acepta de verdad, venga de `argparse` o de mirar `argv`."""
        decl = set(re.findall(r'add_argument\(\s*"(--[^"]+)"', texto))
        decl |= set(re.findall(r'"(--[a-z0-9-]+)"\s*(?:in|==|!=)\s*a', texto))
        decl |= set(re.findall(r'!=\s*"(--[a-z0-9-]+)"', texto))
        return decl

    @staticmethod
    def _docstring(texto):
        marca = texto.find('"""')
        if marca < 0:
            return ""
        fin = texto.find('"""', marca + 3)
        return texto[marca + 3:fin if fin > 0 else None]

    def test_toda_bandera_del_ejemplo_de_uso_existe_en_el_parser(self):
        con_parser = 0
        for guion in self.guiones:
            texto = guion.read_text(encoding="utf-8")
            declaradas = self._declaradas(texto)
            if not declaradas:
                continue
            con_parser += 1
            usadas = set(re.findall(r"--[0-9A-Za-zÁÉÍÓÚÑáéíóúñ][-0-9A-Za-zÁÉÍÓÚÑáéíóúñ]*",
                                    self._docstring(texto)))
            huerfanas = sorted(usadas - declaradas)
            with self.subTest(guion.name):
                self.assertEqual(huerfanas, [],
                                 f"{guion.name} muestra en su ayuda banderas que el parser no "
                                 f"acepta: {', '.join(huerfanas)}")
        # Si `_declaradas` dejara de matchear —por ejemplo con `add_argument('--x')` en comillas
        # simples— todos caerían en el `continue` y el control quedaría verde sin revisar nada.
        self.assertGreater(con_parser, 10,
                           "casi ningún script declaró banderas: el control está apagado")

    def _opciones(self, guion):
        """{bandera: {valores válidos}} leídos del `--help` real, no del fuente.

        Se saca de la corrida porque `choices` puede venir de una constante -`sorted(AMBITO)`-
        y leerlo del AST obligaría a evaluar el módulo. `argparse` ya lo imprime resuelto.
        """
        r = subprocess.run([sys.executable, str(guion), "--help"],
                           capture_output=True, text=True, encoding="utf-8",
                           env=_sin_color())
        if r.returncode != 0:
            return {}
        return {b: set(v.split(",")) for b, v in
                re.findall(r"(--[\w-]+) \{([^}]+)\}", r.stdout)}

    def test_todo_valor_de_bandera_que_se_documenta_es_uno_de_los_validos(self):
        """El inverso del test de arriba: la bandera existe y el VALOR está mal escrito.

        `--tipo` se compara contra `habiles`, así que `--tipo hábiles` sale con código 2. Y el
        error se copia igual que el de la bandera, porque sale del mismo lugar: el ejemplo de
        uso. Estaban así `--tipo hábiles`, `--tipo años` y `--modo índice`, los tres en el
        docstring que se imprime en `--help`, y un cuarto en un mensaje de error.

        Es la regla del proyecto en el sentido menos intuitivo: el valor de una bandera **se
        compara**, así que va en ASCII aunque se muestre.
        """
        con_opciones = 0
        malos = []
        for guion in self.guiones:
            opciones = self._opciones(guion)
            if not opciones:
                continue
            con_opciones += 1
            # Los comentarios quedan afuera: ahí se nombra a propósito un valor inválido para
            # explicar por qué se rechaza -- «un `--empleador Publico` con otra caja» --, y
            # reclamarlo sería pedir que el código no pueda hablar de sus propios errores.
            lineas = [l for l in guion.read_text(encoding="utf-8").splitlines()
                      if not l.lstrip().startswith("#")]
            texto = "\n".join(lineas)
            for bandera, validos in opciones.items():
                for valor in re.findall(re.escape(bandera) + r" ([^\s`\]]+)", texto):
                    valor = valor.rstrip('")\',.;:')
                    if not valor or valor.startswith("-") or valor.isupper() or "{" in valor:
                        continue          # metavariable de la propia ayuda, no un valor
                    if valor not in validos:
                        malos.append(f"{guion.name}: {bandera} {valor} "
                                     f"(válidos: {', '.join(sorted(validos))})")
        self.assertGreater(con_opciones, 2,
                           "ningún script declaró opciones: el control está apagado")
        self.assertEqual(malos, [],
                         "se documentan valores de bandera que el parser rechaza:\n  "
                         + "\n  ".join(malos))

    def test_toda_bandera_de_la_documentacion_existe_en_el_parser(self):
        """El docstring no es el único lugar de donde se copia un comando: `commands/`,
        `AGENTS.md` y `docs/` traen invocaciones enteras en bloques de código, y ahí también
        una bandera mal escrita se copia tal cual.

        Sólo dentro de una cerca: en prosa un `--fix` puede ser de otra herramienta.
        """
        raiz = RAIZ_DEL_CHECKOUT
        acepta = {}
        for guion in self.guiones:
            decl = self._declaradas(guion.read_text(encoding="utf-8"))
            if decl:
                acepta[guion.name] = decl
        docs = [d for d in raiz.rglob("*.md") if ".git" not in d.parts]
        self.assertTrue(docs, "no encontré documentación que revisar")
        huerfanas = []
        for doc in docs:
            dentro, actual = False, None
            for n, linea in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
                if linea.lstrip().startswith("```"):
                    dentro, actual = not dentro, None
                    continue
                if not dentro:
                    continue
                desde = 0
                for nombre in acepta:
                    if nombre in linea:
                        actual, desde = nombre, linea.index(nombre) + len(nombre)
                if actual is None:
                    continue
                # Sólo lo que viene DESPUÉS del nombre del script: en
                # `uv run --with X python3 ruteo.py`, el `--with` es de `uv`.
                for f in re.findall(r"--[0-9A-Za-zÁÉÍÓÚÑáéíóúñ][-0-9A-Za-zÁÉÍÓÚÑáéíóúñ]*",
                                    linea[desde:] if desde else linea):
                    if f not in acepta[actual] and f != "--help":
                        huerfanas.append(f"{doc.relative_to(raiz)}:{n} {actual} {f}")
        self.assertEqual(huerfanas, [],
                         "la documentación manda correr banderas que el parser no acepta:\n  "
                         + "\n  ".join(huerfanas))


class TestLaSalidaPlanaNoPierdeNada(unittest.TestCase):
    """La salida plana es el entregable; `--json` está para encadenar. El invariante que hace
    verdadera esa frase es que **lo plano no puede traer menos que el JSON**.

    Pasó en un uso real: el agente pidió `--json`, rearmó la tabla a mano y se cayeron la línea
    del tramo y la advertencia del divisor 25 de vacaciones, sin que nada avisara. El remedio no
    es pedirle al modelo que copie mejor, es que el modo que se pega tenga todo y no haya motivo
    para rearmar nada. Si alguien agrega un dato al JSON y se olvida del formateador, esto rompe.
    """

    CASOS = (
        ("--ingreso", "2024-08-15", "--extincion", "2026-08-14",
         "--mejor-remuneracion", "1000000", "--remuneracion-ultimo-mes", "1000000",
         "--tope-245", "800000", "--dias-vacaciones-gozadas", "0"),
        # Sin tope: el resultado es provisorio y aparece un marcador más.
        ("--ingreso", "2015-03-10", "--extincion", "2023-11-30",
         "--mejor-remuneracion", "1850000"),
        # Período de prueba: otro tramo de la lógica, con su propio vacío probatorio.
        ("--ingreso", "2026-01-05", "--extincion", "2026-02-20",
         "--mejor-remuneracion", "900000", "--periodo-prueba"),
    )

    GUION = Path(__file__).parent / "liquidacion_lct.py"

    def _correr(self, argumentos):
        return subprocess.run([sys.executable, str(self.GUION), *argumentos], env=_sin_color(),
                              capture_output=True, text=True, encoding="utf-8")

    def test_todo_lo_que_el_json_dice_esta_en_la_salida_plana(self):
        comparados = 0
        for caso in self.CASOS:
            with self.subTest(caso[1]):
                crudo = self._correr([*caso, "--json"])
                plano = self._correr(list(caso))
                self.assertEqual(crudo.returncode, plano.returncode,
                                 "los dos modos no coinciden ni en el código de salida")
                # Sin esto, un renombre de bandera hace que los dos modos fallen igual, el
                # assertEqual de arriba pasa y el caso se saltea SIN dejar rastro: el test
                # quedaba verde con cero comparaciones hechas.
                self.assertEqual(crudo.returncode, 0,
                                 f"el caso no corrió, así que no comparó nada: {crudo.stderr}")
                comparados += 1
                d = json.loads(crudo.stdout)
                texto = plano.stdout
                falta = []
                for clave in ("tramo", "régimen", "antigüedad"):
                    if str(d["datos"][clave]) not in texto:
                        falta.append(f"datos.{clave} = {d['datos'][clave]}")
                for r in d["rubros"]:
                    if r["concepto"] not in texto:
                        falta.append(f"rubro {r['concepto']}")
                    if r["norma"] not in texto:
                        falta.append(f"norma {r['norma']} de {r['concepto']}")
                    # El importe se formatea con separador de miles: se compara así.
                    if f"{r['importe']:,.2f}" not in texto:
                        falta.append(f"importe {r['importe']} de {r['concepto']}")
                if f"{d['total']:,.2f}" not in texto:
                    falta.append(f"total {d['total']}")
                for a in d["advertencias"]:
                    if a not in texto:
                        falta.append(f"advertencia: {a[:60]}...")
                for m in d["marcadores"]:
                    if m not in texto:
                        falta.append(f"marcador: {m[:60]}...")
                self.assertEqual(falta, [],
                                 "el JSON trae cosas que la salida plana no muestra, así que "
                                 "pegar lo plano pierde información:\n  " + "\n  ".join(falta))
        self.assertEqual(comparados, len(self.CASOS),
                         "no todos los casos llegaron a compararse")

    def test_la_ayuda_de_json_dice_para_que_es_y_para_que_no(self):
        """Sin esto la bandera se lee como «el modo serio» y vuelve el rearmado a mano.

        Se mira el bloque de `--json`, no la ayuda entera: el docstring también dice
        «encadenar» y buscarlo suelto daba verde con la ayuda de la bandera ya borrada.
        """
        ayuda = self._correr(["--help"]).stdout.splitlines()
        arranca = [i for i, l in enumerate(ayuda) if l.startswith("  --json")]
        self.assertEqual(len(arranca), 1, "no encontré la entrada de `--json` en la ayuda")
        bloque = [ayuda[arranca[0]]]
        for linea in ayuda[arranca[0] + 1:]:
            if not linea.strip() or not linea.startswith(" " * 12):
                break
            bloque.append(linea)
        self.assertIn("encadenar", " ".join(bloque),
                      "la ayuda de `--json` no dice que es para encadenar con otra herramienta")


class TestLasCalculadorasDevuelvenSusEntradas(unittest.TestCase):
    """`intake.md` manda abrir con el bloque de datos tomados, copiado de la salida de la
    herramienta. Esa instrucción sólo se puede cumplir si la herramienta devuelve lo que se le
    pasó: si una calculadora deja de imprimir una entrada, la regla queda escrita y sin sostén,
    y el dato vuelve a retipearse de memoria, que es de donde salió el error que la motivó.

    Un dato mal tipeado no produce ningún síntoma: devuelve un resultado plausible, con su
    articulado y su total. Devolverlo impreso es el único lugar donde se lo puede ver.
    """

    AQUI = Path(__file__).parent

    CASOS = (
        ("liquidacion_lct.py",
         ["--ingreso", "2024-08-15", "--extincion", "2026-08-14",
          "--mejor-remuneracion", "1000000", "--tope-245", "800000"],
         ["2024-08-15", "2026-08-14", "1000000", "800000"]),
        ("plazos.py",
         ["--tipo", "habiles", "--desde", "2026-03-10", "--dias", "15", "--fuero", "pba"],
         ["habiles", "2026-03-10", "15", "pba"]),
        ("honorarios_pba.py",
         ["--monto", "22768351.81", "--porcentaje", "17.5", "--valor-jus", "53232"],
         ["22768351.81", "17.5", "53232"]),
        ("intereses.py",
         ["--modo", "indice", "--capital", "1000000", "--desde", "2024-01-15",
          "--hasta", "2025-06-30", "--serie", "ipc"],
         ["1000000", "2024-01-15", "2025-06-30", "ipc"]),
    )

    @staticmethod
    def _formas(valor):
        """Un número se imprime con separador de miles y a veces con decimales."""
        formas = {valor, valor.upper()}
        try:
            n = Decimal(valor)
        except Exception:
            return formas
        formas |= {f"{n:,}", f"{n:,.2f}", f"{float(n):,.2f}", f"{n:f}".rstrip("0").rstrip(".")}
        return formas

    def test_cada_calculadora_imprime_los_datos_con_los_que_calculo(self):
        for guion, argumentos, esperados in self.CASOS:
            with self.subTest(guion):
                r = subprocess.run([sys.executable, str(self.AQUI / guion), *argumentos],
                                   capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                salida = r.stdout
                faltan = [v for v in esperados
                          if not any(f in salida for f in self._formas(v))]
                self.assertEqual(faltan, [],
                                 f"{guion} calculó con estos datos y no los devuelve, así que "
                                 f"no hay contra qué cotejar: {', '.join(faltan)}")


class TestSalidaAcentuada(unittest.TestCase):
    """Lo que una calculadora imprime **se copia a un escrito**, así que va acentuado.

    La regla está escrita en `docs/DESARROLLO.md`: el fuente —comentarios y docstrings— va sin
    acentos por costumbre, los identificadores van en ASCII porque se comparan, y **la salida
    sí va acentuada**, porque es texto que alguien lee y pega. Un rubro que dijera
    `Indemnizacion por antiguedad` entra así a una demanda.

    Estaba escrita y no la sostenía nada: `intereses.py` imprimía «Base de calculo días/365 [...]
    sin capitalización», «Período», «Índice» e «Interes»; `estado.py`, «Versión» y «último
    período»; y `liquidacion_lct.py`, «se calculo SIN tope» y «Período de prueba».

    Se mide corriendo los scripts sobre varias ramas de su lógica, no leyendo el fuente: la
    salida se arma con f-strings y la advertencia que falta acento suele estar en la rama que
    nadie corrió. Por eso cada guion aparece acá con más de un caso.
    """

    AQUI = Path(__file__).parent

    # LA LISTA SOLO LLEVA PALABRAS INEQUÍVOCAS, y eso es la mitad del diseño, igual que en
    # `test_markdown.py`. Quedan afuera a propósito:
    #   - `intereses` y `vencimiento`, que NO llevan tilde y entraron por error en un borrador
    #     de esta misma lista;
    #   - `habiles`, que sale impreso como valor de `--tipo`: es un identificador que se compara
    #     y además el eco literal de lo que se tipeó, que `intake.md` manda devolver tal cual.
    PALABRAS = ("articulo", "articulos", "dias", "codigo", "prescripcion", "indemnizacion",
                "verificacion", "seccion", "caratula", "aplicacion", "resolucion", "informacion",
                "liquidacion", "despues", "modulo", "razon", "notificacion", "ejecucion",
                "accion", "sancion", "peticion", "jurisdiccion", "obligacion", "relacion",
                "extincion", "suspension", "conciliacion", "version", "organo", "reduccion",
                "tambien", "ultimo", "minimo", "maximo", "interes", "parrafo", "impugnacion",
                "capitalizacion", "periodo", "periodos", "indice", "indices", "antiguedad",
                "remuneracion", "regimen", "numero", "computo", "analisis", "credito",
                "actualizacion", "deposito", "formula", "formulas", "dia")

    PATRON = re.compile(r"(?<![\w-])(" + "|".join(PALABRAS) + r")(?![\w-])", re.I)
    DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")

    CASOS = (
        ("liquidacion_lct.py", ["--ingreso", "2024-08-15", "--extincion", "2026-08-14",
                                "--mejor-remuneracion", "1000000", "--tope-245", "800000"]),
        ("liquidacion_lct.py", ["--ingreso", "2015-03-10", "--extincion", "2023-11-30",
                                "--mejor-remuneracion", "1850000", "--preaviso-otorgado"]),
        ("liquidacion_lct.py", ["--ingreso", "2026-01-05", "--extincion", "2026-02-20",
                                "--mejor-remuneracion", "900000", "--periodo-prueba"]),
        ("plazos.py", ["--tipo", "habiles", "--desde", "2026-03-10", "--dias", "15",
                       "--fuero", "pba"]),
        ("plazos.py", ["--tipo", "corridos", "--desde", "2026-03-07", "--dias", "5",
                       "--fuero", "nacional"]),
        ("plazos.py", ["--tipo", "meses", "--desde", "2026-03-07", "--cantidad", "6",
                       "--fuero", "nacional"]),
        ("plazos.py", ["--tipo", "anios", "--desde", "2023-05-12", "--cantidad", "3",
                       "--fuero", "pba"]),
        ("honorarios_pba.py", ["--monto", "22768351.81", "--porcentaje", "17.5"]),
        ("honorarios_pba.py", ["--monto", "22768351.81", "--porcentaje", "20",
                               "--etapas-cumplidas", "2", "--etapas-totales", "3",
                               "--tipo", "voluntario", "--con-intereses"]),
        ("intereses.py", ["--modo", "indice", "--capital", "1000000", "--desde", "2024-01-15",
                          "--hasta", "2025-06-30", "--serie", "ipc"]),
        ("intereses.py", ["--modo", "tasa", "--capital", "1000000", "--desde", "2024-01-15",
                          "--hasta", "2025-06-30", "--tna", "50"]),
        ("estado.py", []),
    )

    def _salida(self, guion, argumentos):
        r = subprocess.run([sys.executable, str(self.AQUI / guion), *argumentos],
                           capture_output=True, text=True, encoding="utf-8")
        # `estado.py` sale con 1 cuando hay un dato vencido, que es su trabajo, no un error.
        # Para el resto se exige 0: aceptar 1 en todos dejaba pasar un script que empezara a
        # fallar imprimiendo su error por stdout, y el control de acentos revisaría ese error
        # en vez de la salida real.
        esperados = (0, 1) if guion == "estado.py" else (0,)
        self.assertIn(r.returncode, esperados, r.stdout + r.stderr)
        self.assertTrue(r.stdout.strip(), f"{guion} no imprimió nada: no hay qué revisar")
        return r.stdout

    @staticmethod
    def _sin_datos(linea):
        """Fuera las URL y los nombres de archivo: son rutas, no prosa."""
        linea = re.sub(r"https?://\S+", " ", linea)
        return re.sub(r"[\w./-]*\.(py|csv|json|md|pdf)\b", " ", linea)

    def test_ninguna_calculadora_imprime_prosa_sin_acentos(self):
        for guion, argumentos in self.CASOS:
            with self.subTest(f"{guion} {' '.join(argumentos[:2])}"):
                crudos = []
                for n, l in enumerate(self._salida(guion, argumentos).splitlines(), 1):
                    hallado = self.PATRON.search(self._sin_datos(l))
                    if hallado:
                        crudos.append(f"linea {n}: «{hallado.group(0)}» en {l.strip()[:60]}")
                self.assertEqual(crudos, [],
                                 f"{guion} imprime prosa sin acentos, y esa salida se copia a "
                                 "un escrito:\n  " + "\n  ".join(crudos))

    def test_el_dia_de_la_semana_sale_en_castellano_y_no_del_locale(self):
        """`strftime("%A")` devuelve «Monday» o «lunes» según el locale de la máquina.

        Una calculadora determinista no puede imprimir un texto distinto según dónde corra, y
        menos el que se pega al escrito. `plazos.py` lo hacía: en CI decía «(Monday)».
        """
        salida = self._salida("plazos.py", ["--tipo", "habiles", "--desde", "2026-03-10",
                                            "--dias", "15", "--fuero", "pba"])
        venc = [l for l in salida.splitlines() if "VENCIMIENTO" in l]
        self.assertTrue(venc, "no encontré la línea de vencimiento")
        self.assertTrue(any(d in venc[0] for d in self.DIAS),
                        f"el día de la semana no salió en castellano: {venc[0].strip()}")
        import plazos
        self.assertEqual(plazos.DIAS_DE_LA_SEMANA, self.DIAS)


class TestSalidaAcentuadaEnTodoElRepo(unittest.TestCase):
    """El mismo control que `TestSalidaAcentuada`, pero LEYENDO el fuente en vez de correrlo.

    Los dos hacen falta. Correr los scripts atrapa lo que se arma con f-strings y datos, pero
    sólo en la rama que el caso recorre: la advertencia sin tilde suele estar justo en la que
    nadie corrió. Leer el fuente las alcanza todas, incluidos los descargadores y los que
    necesitan poppler, que acá no se pueden ejecutar.

    Tres versiones anteriores de este control se quedaron cortas, y cada agujero enseña algo:

    1. Miraba sólo `print` y `SystemExit`. Un mensaje también sale por `raise ErrorDeDescarga`,
       por `problemas.append(...)` y por el `help=` de argparse, que es lo que se ve en
       `--help`. Ahora se miran TODOS los literales que no sean docstring.
    2. Salteaba los archivos que empiezan con `_`. Ahí vive `_comun.py`, que es donde más
       mensajes al usuario hay, y `_raiz.py`, que tiene el texto de «no encuentro el repo».
    3. Dependía de una lista de palabras, y una lista siempre llega tarde: no tenía `comprobo`
       ni `metrica`. Por eso ahora manda la REGLA que `AGENTS.md` ya enunciaba —ninguna palabra
       en castellano termina en `-cion` o `-sion` sin tilde— y la lista quedó de complemento.

    Se miran los literales de PROSA, no los identificadores: un literal cuenta como prosa si
    tiene un espacio entre dos letras. Las claves de diccionario, los valores que se comparan y
    los marcadores de `format()` son una sola palabra y quedan afuera solos.
    """

    # Complemento de la regla, para lo que no termina en -cion. Inequívocas otra vez: las
    # palabras que existen de las dos formas salen de `AGENTS.md` y se restan abajo, así no
    # pueden divergir de lo que ese documento declara.
    PALABRAS = ("articulo", "articulos", "dias", "dia", "codigo", "caratula", "caratulas",
                "despues", "razon", "ultimo", "ultimos", "minimo", "maximo", "parrafo",
                "periodo", "periodos", "indice", "indices", "antiguedad", "regimen",
                "analisis", "credito", "deposito", "metrica", "metricas", "ningun", "aqui",
                "raiz", "pagina", "paginas", "proposito", "sesion", "unico", "unica",
                "automatico", "automatica", "automaticamente", "juridico", "juridica",
                "electronico", "electronica", "basico", "tecnico", "facil", "dificil",
                "comun", "canonico", "canonicos", "canonica", "vacio", "valido", "comprobo",
                "salio", "tambien", "organo", "asi", "segun", "estan")

    # La ñ transliterada no es un acento que falta: es otra palabra, y no hay forma válida sin
    # ella. Misma clase que los `Danios` por `Daños` de las carátulas.
    # La lista se cura a mano y no se deriva del repositorio, aunque sea tentador: generar las
    # formas transliteradas del vocabulario con ñ que el repo escribe bien y descartar las que
    # colisionen con palabras reales -«cañón» da «canon», «peña» da «pena»- se envenena solo,
    # porque las listas de este mismo archivo son parte del repositorio y hacen pasar por
    # legítimas justo a `senal`, `dano` y `nino`. Medido. Así que se agregan de a una, cuando
    # aparecen: `acompaniar` salía impreso en `descargar_jurisprudencia.py`, y `espania`
    # cubría el país pero no el gentilicio, así que `espaniol` pasaba en un docstring de
    # `calidad_ocr.py`. Por eso el sufijo va abierto: la raíz es la que no tiene forma
    # válida sin la ñ.
    TRANSLITERADA = re.compile(
        r"(?<![\w-])(enganios[oa]|senial(?:es)?|senal(?:es)?|disenio|nin[oa]s?|anios?|"
        r"companias?|espani\w*|munioz|minuscula|mayuscula|venian?|acompani\w*)(?![\w-])", re.I)

    # DETERMINANTE + palabra = sustantivo. Es sintaxis, no lista: «yo modulo» no existe después
    # de «el», así que acá `modulo` lleva tilde aunque sea ambigua en abstracto. Esto es lo que
    # alcanza a las palabras que `AGENTS.md` declara no automatizables, sin negar que lo sean.
    DETERMINADO = re.compile(
        r"(?<![\w-])(el|los|la|las|un|una|unos|unas|cada|ese|esa|esos|esas|este|esta|estos|"
        r"estas|del|al|su|sus|otro|otra|otros|otras|mismo|misma|mismos|mismas|algun|algún|"
        r"ningun|ningún|todo|toda|todos|todas)\s+"
        # Un adjetivo en el medio no cambia que lo que sigue sea sustantivo. Era el hueco:
        # «su propio calculo» pasaba limpio porque el determinante no estaba pegado.
        r"(?:(?:propi[oa]s?|mism[oa]s?|primer[oa]?s?|segund[oa]s?|nuev[oa]s?|viej[oa]s?|"
        r"unic[oa]s?|únic[oa]s?|ultim[oa]s?|últim[oa]s?|buen[oa]?s?|gran(?:des)?|"
        r"simple|simples|solo|sola|solos|solas)\s+)?"
        r"(modulos?|lineas?|numeros?|calculos?|titulos?|practicas?|criticas?|rubricas?|"
        r"computos?|terminos?|epocas?|paginas?)(?![\w-])", re.I)

    # `mas` seguido de `de` o `que` es comparativo: lleva tilde. La conjunción `mas` = «pero»
    # nunca va delante de esas dos.
    COMPARATIVO = re.compile(r"(?<![\w-])mas\s+(de|que)(?![\w-])", re.I)

    # `se` + palabra terminada en -o es pretérito de tercera persona: `se revisó`, `se bajó`,
    # `se cotejó`. La primera persona no existe ahí --«se reviso» no es castellano--, así que
    # esto alcanza al pretérito, que es la clase que las listas de palabras dejan afuera por
    # ambigua. La excepción es cerrada y gramatical, no una calibración: los pretéritos
    # irregulares NO llevan tilde.
    IRREGULARES = ("pudo", "hizo", "tuvo", "supo", "dijo", "quiso", "vino", "puso", "vio",
                   "dio", "fue", "produjo", "extrajo", "interpuso", "dedujo", "obtuvo",
                   "anduvo", "estuvo", "condujo", "trajo", "redujo", "repuso", "dispuso",
                   "impuso", "propuso", "expuso", "compuso", "contrajo", "atrajo", "distrajo",
                   "sustrajo", "retrajo", "satisfizo", "deshizo", "rehizo", "cupo", "hubo",
                   # y los sustantivos que de verdad siguen a `se`
                   "daño", "cargo")
    SE_PRETERITO = re.compile(
        r"(?<![\w-])se\s+(?!(?:" + "|".join(IRREGULARES) + r")(?![\w-]))"
        r"([a-záéíóúüñ]{3,}o)(?![\w-])", re.I)

    # Ninguna palabra del castellano termina en -cion/-sion sin tilde. Es una regla y no
    # admite excepción, así que no necesita lista y no envejece. Vale para el SINGULAR: el
    # plural NO lleva tilde --vacaciones, opciones, decisiones, contestaciones-- y una
    # primera versión de esta regexp los reclamaba a todos, que es la forma más rápida de
    # que alguien apague el control entero.
    REGLA = re.compile(r"(?<![\w-])[a-záéíóúüñ]+[cs]ion(?![\w-])", re.I)

    # Excepciones, cada una con su motivo escrito. No se agregan sin uno.
    EXCEPCIONES = {
        # Cabecera HTTP: viaja en un header y va en ASCII.
        "derecho-argentino/fuentes (repositorio de conocimiento juridico)",
        # Valor de `--tipo`, que se compara: se nombra tal cual se tipea.
        "Para --tipo habiles o corridos",
        # Ídem `--modo`: el usuario tiene que poder tipear el valor, así que va sin tilde en
        # el `help=` que lo nombra. Los dos literales de `reformas_no_leidas.py`.
        "Por defecto 2024 con --modo articulo, sin corte con --modo norma. ",
        "Con --modo articulo, la nota se compara contra el artículo que ",
    }

    # No hay ninguna. Hubo una —el `ENCABEZADO` de `descargar_normas.py`— y el motivo escrito era
    # que realinear el corpus exigía volver a bajar las 142 normas, con los 403 de InfoLEG en el
    # medio. Era falso, y por eso la excepción duró: el encabezado queda FUERA de `sha256_texto`,
    # que se calcula sobre el cuerpo, así que se reescribe sobre los archivos que ya están y sólo
    # cambia `sha256_archivo`. Una excepción con un motivo plausible y no comprobado es la peor
    # clase: nadie la vuelve a mirar. Antes de escribir otra, medir el costo real de no ponerla.
    CONSTANTES_EXCEPTUADAS = set()

    @classmethod
    def _exceptuadas(cls, guion, arbol):
        ids = set()
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, ast.Assign):
                continue
            for destino in nodo.targets:
                if (isinstance(destino, ast.Name)
                        and (guion.name, destino.id) in cls.CONSTANTES_EXCEPTUADAS):
                    for sub in ast.walk(nodo.value):
                        if isinstance(sub, ast.Constant):
                            ids.add(id(sub))
        return ids

    @staticmethod
    def _docstrings(arbol, fuente):
        """Los docstrings, MENOS el del módulo cuando el script lo imprime en `--help`.

        `argparse.ArgumentParser(description=__doc__)` manda el docstring entero a la pantalla,
        así que ahí deja de ser documentación del fuente y pasa a ser salida. Saltearlo dejó
        pasar «Que este verificado» en la ayuda de `descargar_jurisprudencia.py`.
        """
        ids = set()
        va_a_la_ayuda = "description=__doc__," in fuente
        for n in ast.walk(arbol):
            if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if isinstance(n, ast.Module) and va_a_la_ayuda:
                    continue
                primero = n.body[0] if n.body else None
                if (isinstance(primero, ast.Expr) and isinstance(primero.value, ast.Constant)
                        and isinstance(primero.value.value, str)):
                    ids.add(id(primero.value))
        return ids

    @staticmethod
    def _es_prosa(s):
        if not re.search(r"[a-záéíóúñ] [a-záéíóúñ]", s, re.I):
            return False
        return not re.search(r"\\[dwsWSb]|\(\?|\[\^|%[sdr]\b", s)

    @staticmethod
    def _sin_rutas(s):
        """Fuera lo que no es prosa: URL, tramos de ruta y lo que va entre backticks.

        `/actualizacion` es parte de una URL oficial, y entre backticks van identificadores
        --el encabezado `periodo,indice` de los csv-- que son ASCII porque se comparan.
        """
        # Entre backticks van identificadores; entre comillas —rectas o angulares— van
        # CITAS. «se calculo» en un docstring es la salida rota que el test documenta:
        # corregirla haría que el texto diga lo contrario de lo que documenta.
        s = re.sub(r"`[^`]*`", " ", s)
        s = re.sub(r'"[^"]*"', " ", s)
        s = re.sub(r"«[^»]*»", " ", s)
        s = re.sub(r"https?://\S+", " ", s)
        # Y los marcadores de `format()`: `{jurisdiccion}` es un identificador y acentuarlo
        # levanta KeyError, así que va en ASCII aunque esté embebido en un renglón de prosa que
        # sí se acentúa. Lo exige `TestPlantillaDelEncabezado.test_los_marcadores_son_ascii`, y
        # sin esta línea los dos controles se contradicen: uno pide la tilde y el otro la prohíbe.
        s = re.sub(r"\{\w+\}", " ", s)
        # Y el valor que sigue a una bandera: `--modo indice` va en ASCII porque se COMPARA,
        # y lo exige `test_todo_valor_de_bandera_que_se_documenta_es_uno_de_los_validos`. Sin
        # esto los dos controles se contradicen y uno de los dos tiene que apagarse.
        s = re.sub(r"--[\w-]+ +\S+(?:(?:,| o ) *[\w-]+)*", " ", s)
        s = re.sub(r"/[\w.-]+", " ", s)
        return re.sub(r"[\w.-]*\.(py|md|json|csv|txt|html|pdf|yml)\b", " ", s)

    def _no_automatizables(self, raiz):
        """La lista que el repositorio declara: existen de las dos formas y las decide el
        contexto.

        Se busca en `AGENTS.md` y en `.claude/rules/**/*.md`, que son los dos lugares donde
        puede vivir una regla, en vez de apuntar a un archivo fijo: un parser apuntado a mano
        se rompe en la mudanza siguiente, y en silencio. Que el bloque esté en uno solo lo
        exige `test_la_lista_no_automatizable_vive_en_un_solo_lugar`.
        """
        candidatos = [raiz / "AGENTS.md"] + sorted((raiz / ".claude" / "rules").rglob("*.md"))
        bloque = None
        for archivo in candidatos:
            if not archivo.is_file():
                continue
            # Sin re.S a propósito: con él, el `.` del grupo matchea saltos de línea y el
            # bloque se traga el resto del documento.
            hallado = re.search(
                r"\*\*Estas no se automatizan nunca\*\*[^\n]*\n\n((?:    [^\n]+\n)+)",
                archivo.read_text(encoding="utf-8"))
            if hallado:
                bloque = hallado
                break
        self.assertIsNotNone(bloque, "ningún archivo de reglas declara las palabras no "
                                     "automatizables")
        palabras = {w.strip() for linea in bloque.group(1).splitlines()
                    for w in linea.split("·") if w.strip()}
        self.assertGreater(len(palabras), 10, "la lista quedó vacía o no se parseó")
        self.assertLess(len(palabras), 40,
                        "el bloque capturó más que la lista: el regex volvió a derramarse")
        for esperada in ("aun", "esta", "practica", "modulo"):
            self.assertIn(esperada, palabras,
                          "la lista dejó de traer las palabras conocidas")
        return palabras

    def test_la_lista_no_automatizable_vive_en_un_solo_lugar(self):
        """El bloque de palabras no automatizables vive en exactamente un archivo de reglas.

        Apuntar el parser a mano en cada mudanza es lo que lo rompe. Se busca en los dos
        lugares donde puede estar una regla, y se exige exactamente uno: si no está en
        ninguno el parser quedó huérfano, y si está en dos hay dos listas que van a divergir.
        """
        raiz = RAIZ_DEL_CHECKOUT
        candidatos = [raiz / "AGENTS.md"] + sorted((raiz / ".claude" / "rules").rglob("*.md"))
        con_bloque = [p for p in candidatos if p.is_file()
                      and "**Estas no se automatizan nunca**" in p.read_text(encoding="utf-8")]
        self.assertEqual(len(con_bloque), 1,
                         f"el bloque de palabras no automatizables está en "
                         f"{[p.name for p in con_bloque]}: tiene que estar en exactamente uno")

    def test_ningun_mensaje_del_repo_sale_sin_acentos(self):
        raiz = RAIZ_DEL_CHECKOUT
        prohibidas = set(self.PALABRAS) - self._no_automatizables(raiz)
        patron = re.compile(r"(?<![\w-])(" + "|".join(sorted(prohibidas)) + r")(?![\w-])", re.I)

        guiones = [g for g in sorted(raiz.rglob("*.py"))
                   if ".git" not in g.parts and not g.name.startswith("test_")]
        self.assertGreater(len(guiones), 15, "no encontré los scripts: el control está apagado")
        crudos = []
        for guion in guiones:
            fuente = guion.read_text(encoding="utf-8")
            arbol = ast.parse(fuente)
            saltar = self._docstrings(arbol, fuente) | self._exceptuadas(guion, arbol)
            for nodo in ast.walk(arbol):
                if not (isinstance(nodo, ast.Constant) and isinstance(nodo.value, str)):
                    continue
                if id(nodo) in saltar or nodo.value in self.EXCEPCIONES:
                    continue
                if not self._es_prosa(nodo.value):
                    continue
                limpio = self._sin_rutas(nodo.value)
                hallado = (self.REGLA.search(limpio) or self.TRANSLITERADA.search(limpio)
                           or self.DETERMINADO.search(limpio)
                           or self.COMPARATIVO.search(limpio)
                           or self.SE_PRETERITO.search(limpio) or patron.search(limpio))
                if hallado:
                    crudos.append(f"{guion.relative_to(raiz)}:{nodo.lineno} "
                                  f"«{hallado.group(0)}» en {nodo.value.strip()[:46]}")
        self.assertEqual(crudos, [],
                         "estos mensajes salen sin acentos, y la salida de una herramienta se "
                         "lee y se copia:\n  " + "\n  ".join(crudos))

    def test_la_regla_de_cion_no_depende_de_ninguna_lista(self):
        """Instrumento encendido: la regla tiene que reclamar una palabra que nadie enumeró."""
        for inventada in ("recategorizacion", "desjudicializacion", "retroversion"):
            with self.subTest(inventada):
                self.assertTrue(self.REGLA.search(f"hubo una {inventada} del caso"))
        self.assertIsNone(self.REGLA.search("hubo una recategorización del caso"))


class TestMarcadoresAcentuados(TestSalidaAcentuadaEnTodoElRepo):
    """El CONTENIDO de un marcador es prosa que se copia a un escrito, y va acentuado.

    Un marcador es `[NOMBRE: contenido]`. El nombre es vocabulario controlado y va exacto como
    figura en `marcadores.md`; el contenido, no: lo lee quien redacta y lo pega en la
    presentación. Es la prosa de más riesgo del repositorio.

    Y era la única que no medía nadie. `TestProsaAcentuada` excluía el marcador entero con el
    motivo de que su acentuación «estaba sin decidir»; y aunque no lo excluyera tampoco lo
    alcanzaría, porque en la mayoría de los módulos el marcador se escribe entre acentos graves
    o dentro de un bloque con sangría, y las dos cosas se descartan por buenos motivos. O sea
    que levantar aquella exclusión no bastaba: hay que ir a buscarlos. Cuando se hizo había 19
    defectos adentro, entre ellos `transito`, `publico`, `dieciseis`, `Boletin`, `Secretaria`,
    `cónyuge` y un `quedo` por `quedó`.

    Acentuar no rompe el cotejo: `verificar_respuesta.py` compara el NOMBRE con `plano()`, que
    baja a minúsculas y saca los diacríticos. Por eso esta decisión no tenía costo y no tenía
    por qué seguir abierta.

    Hereda la batería de `TestSalidaAcentuadaEnTodoElRepo` --la regla del -ción, la ñ
    transliterada, determinante más sustantivo, el comparativo y `se` más pretérito-- en vez de
    llevar lista propia: dos listas iguales en dos lugares divergen.

    Y hereda su alcance, que es la mitad. De los 19 defectos que había, la batería alcanza a
    `estan`, `pagina`, `indice`, `unica`, `regimen`, `parrafos` y `asi`; a los otros --
    `transito`, `Boletin`, `Secretaria`, `dieciseis`, `polizas`, `conyuge`-- no llega ninguna
    regla, porque `transito` y `publico` existen sin tilde como verbo y los demás piden
    diccionario. Esos los encontró `herramientas/ortografia.py`, que es el techo y se corre a
    mano. Este test es el piso: impide que vuelvan los que sí se pueden decidir con una regla.
    """

    MARCADOR = re.compile(r"\[([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9/ \-]{3,}):([^\]]*)\]")

    def _marcadores(self, raiz):
        """(archivo, línea, nombre, contenido) de todo marcador de la skill, esté donde esté.

        Se lee el `.md` CRUDO, sin sacar bloques cercados ni spans de código: acá el marcador
        entre acentos graves es justamente el caso que importa.
        """
        base = raiz / "derecho" / "skills" / "derecho-argentino"
        for p in sorted(base.rglob("*.md")):
            for n, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                for m in self.MARCADOR.finditer(l):
                    yield p.relative_to(raiz), n, m.group(1), m.group(2)

    def test_ningun_marcador_lleva_el_contenido_sin_acentos(self):
        raiz = RAIZ_DEL_CHECKOUT
        if not (raiz / "derecho" / "skills").is_dir():
            self.skipTest("no esta la skill")
        prohibidas = set(self.PALABRAS) - self._no_automatizables(raiz)
        patron = re.compile(r"(?<![\w-])(" + "|".join(sorted(prohibidas)) + r")(?![\w-])", re.I)
        vistos, crudos = 0, []
        for archivo, linea, _nombre, contenido in self._marcadores(raiz):
            vistos += 1
            limpio = self._sin_rutas(contenido)
            hallado = (self.REGLA.search(limpio) or self.TRANSLITERADA.search(limpio)
                       or self.DETERMINADO.search(limpio)
                       or self.COMPARATIVO.search(limpio)
                       or self.SE_PRETERITO.search(limpio) or patron.search(limpio))
            if hallado:
                crudos.append(f"{archivo}:{linea} «{hallado.group(0)}» en {contenido.strip()[:60]}")
        self.assertGreater(vistos, 100, "no encontré los marcadores: el control está apagado")
        self.assertEqual(crudos, [],
                         "el contenido de estos marcadores sale sin acentos, y un marcador se "
                         "copia tal cual al escrito:\n  " + "\n  ".join(crudos))


class TestCabeceraDeLasSeries(unittest.TestCase):
    """La cabecera que `descargar_series.py` escribe en cada csv tiene que decir lo que dice
    el código que la escribe.

    Es el mismo problema que la plantilla de `ENCABEZADO`: el mismo texto vive en dos lugares,
    el fuente y el corpus, y nada los comparaba. Se habían separado sin que nadie lo notara —el
    código decía `Coeficiente de Estabilizacion` y el csv en disco `Estabilización`—, y eso no
    se ve leyendo ninguno de los dos por separado: hay que compararlos.

    Un desfasaje así no rompe nada hoy. Se cobra el día que alguien lee la cabecera del csv para
    saber qué serie tiene entre manos, o que el fuente para saber qué se bajó, y los dos dicen
    cosas distintas sin decir cuál miente.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.datos = raiz / "derecho" / "fuentes" / "datos"
        fuente = (raiz / "derecho" / "fuentes" / "scripts" / "descargar_series.py") \
            .read_text(encoding="utf-8")
        arbol = ast.parse(fuente)
        self.series = None
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Assign) and any(
                    isinstance(d, ast.Name) and d.id == "SERIES" for d in nodo.targets):
                self.series = ast.literal_eval(nodo.value)
        self.assertIsNotNone(self.series, "descargar_series.py dejó de declarar SERIES")
        self.assertTrue(self.series, "SERIES quedó vacío: el control no compara nada")

    def test_cada_csv_declara_el_titulo_que_el_script_escribe(self):
        for nombre, cfg in self.series.items():
            with self.subTest(nombre):
                csv = self.datos / f"serie-{nombre}.csv"
                # Un skipTest DENTRO de un subTest no corta el bucle: se registra y sigue, así
                # que el test entero pasaba "OK (skipped=3)" sin comparar nada. Los tres csv
                # están versionados, así que su ausencia es una rotura, no un caso previsto.
                self.assertTrue(csv.is_file(),
                                f"falta {csv.name}, que está versionado: sin él no hay control")
                lineas = csv.read_text(encoding="utf-8").splitlines()
                self.assertEqual(lineas[0], f"# {cfg['titulo']}",
                                 f"{csv.name} y descargar_series.py dicen cosas distintas sobre "
                                 "la misma serie")
                self.assertEqual(
                    lineas[1],
                    f"# Organismo: {cfg['organismo']} - frecuencia: {cfg['frecuencia']}")
                self.assertEqual(lineas[2], f"# serie_id: {cfg['id']}")


class TestAmbitoDeLaLCT(unittest.TestCase):
    """La LCT no rige todo trabajo dependiente, y el script tiene que negarse antes de calcular.

    El art. 2 inc. a excluye a los dependientes de la Administración Pública salvo acto expreso
    de inclusión. Sin este corte, pedir la liquidación por despido de una docente provincial
    devuelve los nueve rubros con su articulado y su total prolijo, bajo un cuerpo legal que no
    la rige: **nada en el número delata el error**, que es justo la clase de falla que no se
    detecta leyendo el resultado.

    Apareció comparando el script con el liquidador de haberes docentes de SUTEBA, que calcula
    el haber mensual de un cargo bajo la Ley 10.579 — otro régimen, otro momento, otra
    competencia. El repo tenía escrita esa frontera como frontera de COMPETENCIA en
    `perfiles-heredados.md`, y no como frontera del cálculo.
    """

    GUION = Path(__file__).parent / "liquidacion_lct.py"
    BASE = ["--ingreso", "2024-08-15", "--extincion", "2026-08-14",
            "--mejor-remuneracion", "1000000", "--tope-245", "800000"]

    def _correr(self, *extra):
        return subprocess.run([sys.executable, str(self.GUION), *self.BASE, *extra],
                              capture_output=True, text=True, encoding="utf-8")

    def test_el_empleo_publico_corta_y_no_liquida(self):
        r = self._correr("--empleador", "publico")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("[ARG SIN NORMA:", r.stdout)
        self.assertIn("art. 2 inc. a", r.stdout)
        # Y sobre todo: NO liquidó. Un total en pantalla junto al marcador se copia igual.
        self.assertNotIn("TOTAL", r.stdout)
        self.assertNotIn("Art. 245 LCT", r.stdout)

    def test_el_privado_liquida_sin_el_marcador_de_ambito(self):
        r = self._correr("--empleador", "privado")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("TOTAL", r.stdout)
        self.assertNotIn("naturaleza del empleador", r.stdout)

    def test_el_publico_incluido_liquida_porque_hubo_acto_expreso(self):
        """La excepción del art. 2 inc. a existe y tiene que tener camino propio: si no, el
        único modo de liquidar un caso incluido por CCT es mentirle al script diciendo
        `privado`, y ahí se pierde el dato de que hubo acto expreso."""
        r = self._correr("--empleador", "publico-incluido")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("TOTAL", r.stdout)

    def test_sin_el_dato_liquida_pero_lo_dice_con_marcador(self):
        """Suplible, no determinante: la mayoría de los casos son privados, así que cortar
        siempre volvería inútil la herramienta. Lo que no se admite es el silencio."""
        r = self._correr()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[VACÍO PROBATORIO: naturaleza del empleador", r.stdout)
        self.assertIn("sin declarar", r.stdout)

    def test_el_dato_viaja_en_el_json(self):
        r = self._correr("--empleador", "privado", "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["datos"]["empleador"], "privado")

    def test_una_opcion_inventada_se_rechaza(self):
        """Si `--empleador municipal` pasara como desconocido y liquidara, el corte no existe."""
        r = self._correr("--empleador", "municipal")
        self.assertEqual(r.returncode, 2)
        self.assertIn("invalid choice", r.stderr)

    def test_todo_valor_desconocido_corta(self):
        """El corte no puede depender de escribir bien el valor.

        `choices` de argparse tapa esto desde la línea de comandos, pero `liquidar()` también se
        llama desde adentro. Si lo desconocido se tratara como «seguir», un `Publico` con otra
        caja liquidaría igual y el corte sería una formalidad.
        """
        sys.path.insert(0, str(Path(__file__).parent))
        import liquidacion_lct as liq

        def args(**kw):
            base = dict(ingreso=date(2024, 8, 15), extincion=date(2026, 8, 14),
                        mejor_remuneracion=Decimal("1000000"), remuneracion_ultimo_mes=None,
                        tope_245=None, dias_vacaciones_gozadas=Decimal("0"),
                        periodo_prueba=False, preaviso_otorgado=False, json=False)
            base.update(kw)
            return type("A", (), base)

        for valor in ("publico", "Publico", "PUBLICO", "municipal", "provincial", "estatal"):
            with self.subTest(valor):
                with self.assertRaises(SystemExit) as cm:
                    liq.liquidar(args(empleador=valor))
                self.assertEqual(cm.exception.code, 2)
        for valor in ("privado", "publico-incluido"):
            with self.subTest(valor):
                self.assertTrue(liq.liquidar(args(empleador=valor)).rubros)

    def test_el_intake_lo_pide_como_dato_que_bloquea(self):
        """El corte del script y el checklist tienen que decir lo mismo: si `intake.md` no lo
        pide, el dato no llega nunca y el script sólo emite su marcador."""
        raiz = RAIZ_DEL_CHECKOUT
        intake = (raiz / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "intake.md").read_text(encoding="utf-8")
        bloque = re.search(r"## Laboral · liquidación.*?\n(?=## )", intake, re.S)
        self.assertIsNotNone(bloque, "cambió el título de la sección de liquidación en intake.md")
        bloquean = bloque.group(0).split("**Se marcan y no bloquean:**")[0]
        self.assertIn("empleador", bloquean,
                      "intake.md no pide quién era el empleador entre los datos que bloquean")
        self.assertIn("art. 2 inc. a", bloquean, "intake.md no dice por qué bloquea")


class TestVeredictosDeRevisionSiguenVivos(unittest.TestCase):
    """Un veredicto de `revisiones.json` se indexa por el TEXTO EXACTO del problema.

    `descargar_normas.py` hace `[x for x in problemas if x in leidos]`: si el mensaje que
    `revisar_texto()` produce deja de coincidir carácter por carácter con la clave declarada, el
    veredicto humano se vuelve invisible y la norma vuelve a salir como `REVISAR` en la próxima
    descarga, borrando su `revisado` de `procedencia.json`. No falla: reaparece una alarma ya
    contestada, que es la forma de que se dejen de mirar todas.

    Pasó de verdad y por una tilde: al acentuar la salida de `revisar_texto()` —`articulos` ->
    `artículos`, que es correcto porque esa salida se lee— dos veredictos quedaron huérfanos sin
    que nada avisara.

    Se compara el ESQUELETO: sin tildes y sin dígitos. La ortografía y la redacción del mensaje
    son del código y no pueden derivar; los números sí cambian legítimamente cuando el texto
    bajado cambia, y eso es otra cosa —lo vigilan el sha256 y la procedencia— que no se mezcla
    con esta.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.normas = raiz / "derecho" / "fuentes" / "normas"
        archivo = self.normas / "revisiones.json"
        if not archivo.is_file():
            self.skipTest("no está revisiones.json")
        self.declarados = json.loads(archivo.read_text(encoding="utf-8"))["revisiones"]
        sys.path.insert(0, str(raiz / "derecho" / "fuentes" / "scripts"))
        import _comun
        self.revisar = _comun.revisar_texto

    @staticmethod
    def _esqueleto(s):
        import unicodedata
        sin = unicodedata.normalize("NFD", s.lower())
        sin = "".join(c for c in sin if unicodedata.category(c) != "Mn")
        return re.sub(r"\d+", "#", sin)

    def test_cada_problema_declarado_lo_sigue_produciendo_el_detector(self):
        comparados = 0
        huerfanos = []
        for slug, entradas in self.declarados.items():
            archivo = self.normas / f"{slug}.txt"
            if not archivo.is_file():
                huerfanos.append(f"{slug}: hay veredicto y no está el .txt")
                continue
            producidos = {self._esqueleto(x)
                          for x in self.revisar(archivo.read_text(encoding="utf-8"))}
            for e in entradas:
                comparados += 1
                if self._esqueleto(e["problema"]) not in producidos:
                    huerfanos.append(f"{slug}: «{e['problema'][:60]}...»")
        self.assertGreater(comparados, 0,
                           "no se comparó ningún veredicto: el control está apagado")
        self.assertEqual(huerfanos, [],
                         "estos veredictos ya no matchean lo que produce revisar_texto(), así "
                         "que la norma va a volver a salir como REVISAR:\n  "
                         + "\n  ".join(huerfanos))


class TestProsaAcentuadaEnLosJSON(unittest.TestCase):
    """La prosa de los archivos de veredicto también se lee, así que también va acentuada.

    Son las notas, los motivos y los veredictos que explican POR QUÉ una marca no era un
    defecto. Se escriben una vez y se leen cada vez que la alarma vuelve a sonar: es el único
    lugar donde queda el razonamiento, y estaban enteros sin acentos.

    Se aplica la misma regla que a la salida de los scripts —ninguna palabra termina en -cion
    o -sion sin tilde— más la lista corta de inequívocas. Y se salta lo que NO es prosa, cada
    exclusión con su motivo:

    - `problema` es contrato con el mensaje del código: se compara carácter por carácter.
    - `caratula` y `tribunal` son dato que se cita: se recuperan del documento, no del idioma.
      La fuente de un fallo escribe «CAMARA DE APELACION» y así se cita.
    - `secuencias` es la línea de base que `fuga_textual.py` compara contra `kb/`, y
      `normalizar()` conserva los acentos.
    - el token inicial de un motivo de `cifras-revisadas.json`: se compara contra el vocabulario.
    - los nombres de archivo: `INDICE.md` es un archivo del repo, no una palabra.
    """

    SALTAR_CAMPO = {"problema", "caratula", "tribunal", "secuencias"}
    REGLA = re.compile(r"(?<![\w-])[a-zñáéíóúü]+[cs]ion(?![\w-])", re.I)
    PALABRAS = ("recien", "despues", "articulo", "articulos", "dias", "codigo", "caratulas",
                "razon", "ultimo", "ultima", "ultimos", "minimo", "maximo", "parrafo",
                "periodos", "indice", "indices", "antiguedad", "regimen", "analisis",
                "credito", "creditos", "deposito", "metrica", "metricas", "ningun", "aqui",
                "aca", "ahi", "asi", "raiz", "paginas", "proposito", "unico", "unica",
                "juridico", "juridica", "basico", "tecnico", "comun", "canonico", "vacio",
                "valido", "tambien", "organo", "segun", "estan", "mayoria", "leyo", "leida",
                "leido", "leidos", "habia", "via", "epoca", "catalogo", "ambito", "eslabon",
                "patron", "renglon", "transito", "habiles", "busqueda", "prorroga",
                "todavia", "terminos", "mencion", "pension", "rotulo", "rotulos")
    PATRON = re.compile(r"(?<![\w-])(" + "|".join(PALABRAS) + r")(?![\w-])", re.I)
    # Grafías que quedan como están porque documentan cómo lo escribe OTRO: el registro de un
    # tribunal o el encabezado de InfoLEG. Ahí la ortografía es evidencia.
    CITADAS = ("SUMARISIMO", "Articulo", "ARTICULO", "UNICA")
    ARCHIVO = re.compile(r"[\w-]+\.(md|py|json|csv|txt|html|pdf|yml)\b")

    def _crudas(self, texto):
        if any(x in texto for x in self.CITADAS):
            return None
        T = TestSalidaAcentuadaEnTodoElRepo
        # Por `_sin_rutas` como los otros dos controles de acentos, y no por su cuenta: un
        # campo de prosa de un `.json` cita identificadores entre backticks y tramos de ruta
        # igual que un docstring. Sin eso, `/legislacion/legislacion/l-NNNNN.html` dentro de
        # una nota se reclamaba como un `-ción` sin tilde, y los tres controles decían cosas
        # distintas sobre el mismo texto.
        limpio = T._sin_rutas(self.ARCHIVO.sub(" ", re.sub(r"https?://\S+", " ", texto)))
        limpio = re.sub(r"^[a-z-]+ — ", " ", limpio)
        return (self.REGLA.search(limpio) or T.TRANSLITERADA.search(limpio)
                or T.DETERMINADO.search(limpio) or T.COMPARATIVO.search(limpio)
                or T.SE_PRETERITO.search(limpio) or self.PATRON.search(limpio))

    def test_ninguna_nota_de_veredicto_esta_sin_acentos(self):
        raiz = RAIZ_DEL_CHECKOUT
        revisadas = 0
        crudas = []

        def recorrer(nodo, campo, arch):
            nonlocal revisadas
            if isinstance(nodo, dict):
                for k, v in nodo.items():
                    recorrer(v, k, arch)
            elif isinstance(nodo, list):
                for v in nodo:
                    recorrer(v, campo, arch)
            elif isinstance(nodo, str) and " " in nodo and campo not in self.SALTAR_CAMPO:
                revisadas += 1
                hallado = self._crudas(nodo)
                if hallado:
                    crudas.append(f"{arch}:{campo} «{hallado.group(0)}» {nodo[:46]}")

        for archivo in sorted(raiz.rglob("*.json")):
            # `evals/results/` es la salida de `claude plugin eval`: prosa de la herramienta y de
            # los runs, no del repositorio. Es el tercer control que esa carpeta rompió — los
            # otros dos contaban casos— y por eso va nombrada, no ignorada de hecho.
            if (".git" in archivo.parts or archivo.name == "procedencia.json"
                    or "results" in archivo.parts):
                continue
            try:
                d = json.loads(archivo.read_text(encoding="utf-8"))
            except ValueError:
                continue
            recorrer(d, None, str(archivo.relative_to(raiz)))
        self.assertGreater(revisadas, 200,
                           "casi no se revisó prosa: el control está apagado")
        self.assertEqual(crudas, [],
                         "la prosa de los veredictos va acentuada, que es donde queda escrito "
                         "por qué una alarma no era un defecto:\n  " + "\n  ".join(crudas))


class TestProsaAcentuadaEnElFuente(unittest.TestCase):
    """Los comentarios y los docstrings también van acentuados, y esto lo sostiene.

    Se llegó a sostener que en el fuente la costumbre era escribir sin acentos, y era falso:
    medido sobre las líneas de comentario y docstring del repositorio, casi la mitad llevaba
    tilde y ningún archivo era consistente en ninguna de las dos direcciones. No había
    costumbre, había un empate — y el empate sirvió de excusa para dejar sin acentos un
    docstring que se imprime en `--help`.

    Se aplica la misma regla de siempre: nada termina en -cion o -sion sin tilde, más la lista
    corta de inequívocas. Y se salta lo que NO es prosa: lo que va entre backticks, las URL,
    los nombres de archivo y el valor que sigue a una bandera, que va en ASCII porque se
    compara.
    """

    PALABRAS = TestSalidaAcentuadaEnTodoElRepo.PALABRAS
    REGLA = TestSalidaAcentuadaEnTodoElRepo.REGLA
    # Grafías que se dejan como están porque CITAN lo que produjo otro: el registro de un
    # tribunal, o el propio OCR cuando se documenta lo que leyó mal. Corregirlas haría que
    # el texto afirme lo contrario de lo que documenta.
    CITADAS = ("SUMARISIMO", "puede un dia probar la droga",
               # La cita cruza el salto de línea, así que sacar lo entrecomillado no
               # alcanza. Un pase anterior ya le "corrigió" el acento a esta cita y
               # destruyó el ejemplo: el título roto dejó de verse roto.
               'Transito" y "Fuero Penal del Nino"')

    def _prosa(self, guion):
        """Devuelve [(línea, texto)] con SÓLO el texto de comentarios y docstrings.

        El texto del comentario, no la línea que lo contiene: `RAIZ = Path(...)  # derecho/`
        es media línea de código y media de prosa, y tratarla entera como prosa fue lo que
        hizo que un pase automático renombrara la constante y acentuara una cadena que estaba
        fijada por hash.
        """
        src = guion.read_text(encoding="utf-8")
        import io as _io
        import tokenize as _tok
        trozos = []
        for t in _tok.generate_tokens(_io.StringIO(src).readline):
            if t.type == _tok.COMMENT:
                trozos.append((t.start[0], t.string))
        for nodo in ast.walk(ast.parse(src)):
            if isinstance(nodo, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
                c = nodo.body[0] if nodo.body else None
                if (isinstance(c, ast.Expr) and isinstance(c.value, ast.Constant)
                        and isinstance(c.value.value, str)):
                    for i, l in enumerate(c.value.value.splitlines()):
                        trozos.append((c.value.lineno + i, l))
        return trozos

    def test_ningun_comentario_ni_docstring_esta_sin_acentos(self):
        raiz = RAIZ_DEL_CHECKOUT
        prohibidas = (set(self.PALABRAS)
                      - TestSalidaAcentuadaEnTodoElRepo()._no_automatizables(raiz))
        patron = re.compile(r"(?<![\w-])(" + "|".join(sorted(prohibidas)) + r")(?![\w-])", re.I)
        guiones = [g for g in sorted(raiz.rglob("*.py")) if ".git" not in g.parts]
        self.assertGreater(len(guiones), 20, "no encontré los scripts: el control está apagado")
        revisadas = 0
        crudas = []
        for guion in guiones:
            for i, linea in self._prosa(guion):
                if any(x in linea for x in self.CITADAS):
                    continue
                revisadas += 1
                limpio = TestSalidaAcentuadaEnTodoElRepo._sin_rutas(linea)
                T = TestSalidaAcentuadaEnTodoElRepo
                hallado = (self.REGLA.search(limpio) or T.TRANSLITERADA.search(limpio)
                           or T.DETERMINADO.search(limpio) or T.COMPARATIVO.search(limpio)
                           or T.SE_PRETERITO.search(limpio) or patron.search(limpio))
                if hallado:
                    crudas.append(f"{guion.relative_to(raiz)}:{i} «{hallado.group(0)}» "
                                  f"{linea.strip()[:44]}")
        self.assertGreater(revisadas, 500, "casi no se revisó prosa: el control está apagado")
        self.assertEqual(crudas, [],
                         "comentarios y docstrings sin acentos:\n  " + "\n  ".join(crudas))


class TestNadaSeCorrompeAlEditar(unittest.TestCase):
    """Tres roturas que un pase automático sobre texto produce, y que ningún test veía.

    **Un byte nulo en un archivo de texto.** Un pase que protege lo que no debe tocar suele
    hacerlo sustituyendo por un marcador y restaurándolo al final. Si una sustitución posterior
    se come el marcador, la restitución no lo encuentra y queda dentro del archivo. Pasó: se
    comió `` `/derecho:configurar` `` en SKILL.md, `` `fuentes/` `` en AGENTS.md y una ruta en
    AUDITORIAS.md, y el síntoma fue que `git diff` empezó a decir «binary files differ».

    **El frontmatter es identificador, no prosa.** El `name:` de un comando es con lo que se lo
    invoca. Un barrido de ortografía lo dejó como `Liquidación`, con tilde y mayúscula, contra
    los otros que son slugs en ASCII y contra lo que documenta el README.

    **Una palabra en caja alta con la cola en minúscula.** Una regla de acentos aplicada sin
    mirar la caja deja `MUTACION` con la cola en minúscula y acentuada, porque reemplaza el
    final por la forma del diccionario. Salió nueve veces, y dos de ellas eran peor que una falta
    de ortografía —`CAMARA DE APELACION` es cómo escribe el registro de un tribunal, y estaba
    citado—. No hace falta un diccionario para verlo: una palabra que arranca en caja alta y
    termina en minúscula acentuada no la escribe nadie.
    """

    BINARIOS = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".woff", ".woff2", ".zip")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz

    def test_ningun_archivo_de_texto_tiene_un_byte_nulo(self):
        # Sólo lo versionado: `__pycache__`, los `.pyc` y los `.DS_Store` no son del repo, y
        # `git ls-files` es la definición exacta de qué archivos lo son.
        listado = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"],
                                 cwd=str(self.raiz), capture_output=True, text=True)
        if listado.returncode != 0:
            self.skipTest("no es un checkout de git")
        revisados, rotos = 0, []
        for nombre in listado.stdout.split("\0"):
            if not nombre:
                continue
            archivo = self.raiz / nombre
            if not archivo.is_file() or archivo.suffix.lower() in self.BINARIOS:
                continue
            crudo = archivo.read_bytes()
            revisados += 1
            if b"\x00" in crudo:
                linea = crudo[:crudo.index(b"\x00")].count(b"\n") + 1
                rotos.append(f"{archivo.relative_to(self.raiz)}:{linea}")
        self.assertGreater(revisados, 100, "casi no se revisó nada: el control está apagado")
        self.assertEqual(rotos, [],
                         "hay un marcador de edición sin restaurar dentro del archivo: "
                         + ", ".join(rotos))

    # Dos o más mayúsculas seguidas y después una minúscula acentuada. Pide la tilde para que
    # no entre `MiPyMEs` ni `PDFs`, que son caja mezclada legítima y no llevan acento.
    CAJA_ROTA = re.compile(r"(?<![^\W\d_])[A-ZÑ]{2,}[a-zñ]*[áéíóúü][a-zñ]*(?![^\W\d_])")

    def test_ninguna_palabra_mezcla_caja_alta_con_tilde_minuscula(self):
        listado = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"],
                                 cwd=str(self.raiz), capture_output=True, text=True)
        if listado.returncode != 0:
            self.skipTest("no es un checkout de git")
        revisados, rotas = 0, []
        for nombre in listado.stdout.split("\0"):
            if not nombre or nombre.startswith("derecho/kb/"):
                continue          # capa 2: material de otro autor, no se corrige su ortografía
            archivo = self.raiz / nombre
            if not archivo.is_file() or archivo.suffix.lower() in self.BINARIOS:
                continue
            revisados += 1
            texto = archivo.read_text(encoding="utf-8", errors="replace")
            for n, linea in enumerate(texto.splitlines(), 1):
                for m in self.CAJA_ROTA.finditer(linea):
                    rotas.append(f"{nombre}:{n} «{m.group(0)}»")
        self.assertGreater(revisados, 100, "casi no se revisó nada: el control está apagado")
        self.assertEqual(rotas, [], "un pase de acentos le comió la caja a una palabra: "
                                    + ", ".join(rotas[:10]))

    def test_el_nombre_de_cada_comando_es_un_slug_ascii(self):
        """Se compara: es lo que se tipea después de `/derecho:`."""
        comandos = sorted((self.raiz / "derecho" / "commands").glob("*.md"))
        self.assertGreater(len(comandos), 4, "no encontré los comandos")
        for comando in comandos:
            with self.subTest(comando.name):
                declarado = re.search(r"^name:\s*(.+)$",
                                      comando.read_text(encoding="utf-8"), re.M)
                self.assertIsNotNone(declarado, f"{comando.name} no declara `name`")
                nombre = declarado.group(1).strip()
                self.assertRegex(nombre, r"^[a-z0-9-]+$",
                                 f"«{nombre}» no es un slug: el nombre del comando se compara")
                self.assertEqual(nombre, comando.stem,
                                 "el `name` y el archivo tienen que decir lo mismo")


class TestElDescriptionDeLaSkillActivaTodasLasRamas(unittest.TestCase):
    """El `description` del SKILL.md no describe: **enciende**. Un tema que no está ahí no llega.

    Es la diferencia con el `description` de un comando, que el usuario lee y decide. Éste lo
    lee el modelo para saber si la skill aplica, así que un módulo sin disparador es un módulo
    inalcanzable: la consulta se contesta con conocimiento general y el módulo auditado no se
    abre nunca. El daño no se ve, porque la respuesta sale igual.

    **Los disparadores se declaran, no se infieren del nombre del archivo.** «previsional.md»
    se activa con «jubilaciones» y «salud-discapacidad.md» con «prepaga»: nadie consulta usando
    el nombre del módulo. La tabla de abajo es esa declaración, y agregar un módulo de rama sin
    sumarle su disparador deja este test en rojo, que es exactamente lo que tiene que pasar.

    El límite del campo es de 1.536 caracteres contados junto con `when_to_use`, así que hay
    lugar; lo que no hay es margen para olvidarse de una rama.

    Mutación que lo comprueba: sacar «jubilaciones» del `description` del SKILL.md lo deja en
    rojo por `previsional.md`.
    """

    # Un disparador por módulo de rama: una palabra que alguien usaría al consultar.
    DISPARADORES = {
        "amparo.md": ("amparo",),
        "administrativo-nacional.md": ("acto administrativo", "agotamiento de la vía"),
        "ambiental.md": ("ambiental", "contaminación"),
        "civil.md": ("daños", "contratos"),
        "competencia.md": ("defensa de la competencia", "posición dominante"),
        "concursos.md": ("concursos", "quiebras"),
        "consumo-caba.md": ("proceso de consumo de la Ciudad", "conciliación previa"),
        "consumidor.md": ("consumidor", "abusivas"),
        "contencioso-pba.md": ("contencioso administrativa",),
        "contratos.md": ("contratos",),
        "datos-personales.md": ("datos personales", "hábeas data"),
        "derechos-reales.md": ("derechos reales", "usucapión", "propiedad horizontal"),
        "dipr.md": ("elemento extranjero", "jurisdicción internacional"),
        "empleo-publico.md": ("empleo público", "cesantía"),
        "ejecucion.md": ("ejecución de sentencia",),
        "firma-digital.md": ("firma digital", "documento electrónico"),
        "familia.md": ("alimentos", "divorcio"),
        "honorarios-caba.md": ("UMA",),
        "honorarios-nacional.md": ("UMA",),
        "honorarios-pba.md": ("jus",),
        "locacion.md": ("alquileres", "desalojo"),
        "laboral.md": ("despido", "liquidación"),
        "laboral-colectivo.md": ("convenio colectivo",),
        "penal-leyes-especiales.md": ("hábeas corpus", "estupefacientes"),
        "notificaciones-pba.md": ("notificación electrónica",),
        "penal.md": ("penales", "excarcelación"),
        "penal-juvenil-pba.md": ("penal juvenil",),
        "plazos.md": ("plazos", "prescripción"),
        "previsional.md": ("jubilaciones", "pensiones"),
        "propiedad-industrial.md": ("patentes", "marcas"),
        "proceso-nacional.md": ("proceso civil y comercial",),
        "proceso-pba.md": ("caducidad",),
        "prueba-pericial.md": ("prueba pericial",),
        "salud-discapacidad.md": ("prepaga", "discapacidad"),
        "sede-judicial-pba.md": ("veredicto", "sentencia"),
        "sede-judicial.md": ("órgano jurisdiccional",),
        # Los tres de sede comparten disparador a propósito: el `description` ENCIENDE la
        # skill y la tabla de ruteo de la 16 elige el fuero. Darle a cada uno su palabra
        # obligaría a comprar espacio en un `description` que está a siete caracteres del
        # límite, y no compraría precisión: quien consulta dice que es el órgano, no el
        # nombre de su código procesal.
        "sede-judicial-nacional.md": ("órgano jurisdiccional",),
        "sede-judicial-caba.md": ("órgano jurisdiccional",),
        "salud-mental.md": ("salud mental", "internación involuntaria"),
        "seguros.md": ("seguros", "citación en garantía"),
        "societario.md": ("sociedades",),
        "sucesiones.md": ("sucesiones", "legítima"),
        "titulos-ejecutivos.md": ("pagaré", "cheque"),
        "telegramas.md": ("telegramas",),
        "transito.md": ("tránsito",),
        "tributario.md": ("tributario", "Fisco"),
        "tributario-pba.md": ("ARBA",),
        "previsional-pba.md": ("IPS",),
        "contravencional-caba.md": ("contravenciones de CABA",),
        "tributario-caba.md": ("AGIP",),
        "ejecucion-penal.md": ("ejecución de la pena",),
        "changelog-normativo.md": ("prescripción",),
        "fallos-csjn.md": ("penales",),
        "parte.md": ("escritos",),
    }

    def setUp(self):
        skill = Path(__file__).resolve().parents[1] / "SKILL.md"
        self.descripcion = re.search(r"(?m)^description: (.+)$",
                                     skill.read_text(encoding="utf-8")).group(1)
        self.refs = skill.parent / "references"

    def test_cada_modulo_de_rama_tiene_su_disparador(self):
        # La misma partición que usa `herramientas/pendientes.py`: un módulo de rama describe
        # derecho, uno de infraestructura describe cómo trabaja la skill.
        infraestructura = {"danos-indice-doctrinario.md", "escritos.md", "fuentes.md",
                           "intake.md", "marcadores.md", "modelos.md", "perfiles-heredados.md"}
        ramas = [f.name for f in sorted(self.refs.glob("*.md"))
                 if f.name not in infraestructura]
        self.assertGreater(len(ramas), 20, "no se encontraron los módulos de rama")
        sin_disparador = []
        for modulo in ramas:
            palabras = self.DISPARADORES.get(modulo)
            with self.subTest(modulo):
                self.assertIsNotNone(palabras,
                                     f"{modulo} es un módulo de rama y no declara disparador: "
                                     f"agregarlo a DISPARADORES y al description del SKILL.md")
                if palabras and not any(p.lower() in self.descripcion.lower() for p in palabras):
                    sin_disparador.append(f"{modulo} ({'/'.join(palabras)})")
        self.assertEqual(sin_disparador, [],
                         "módulos de rama que el description no activa: " +
                         ", ".join(sin_disparador))

    def test_el_description_entra_en_el_limite(self):
        """1.536 caracteres contados junto con `when_to_use`, que esta skill no usa."""
        self.assertLessEqual(len(self.descripcion), 1536,
                             "el description pasa el límite y se trunca en el listado")


if __name__ == "__main__":
    unittest.main()
