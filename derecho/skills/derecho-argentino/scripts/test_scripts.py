#!/usr/bin/env python3
"""Plomería del plugin: dónde está la raíz, el perfil, los manifiestos y los comandos.

Salió de `test_scripts.py` al partirlo: el original llegó a 6149 renglones, tres veces el corte de
`Read`. Lo compartido está en `_comun_tests.py`, y el porqué del corte también.

    python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
"""
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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import _raiz
from _comun_tests import RAIZ_DEL_CHECKOUT, SEMVER, load_tests, sin_color as _sin_color


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


class TestElBloqueDeImportsNoSeCopia(unittest.TestCase):
    """Las seis suites salieron de partir un archivo de 6149 renglones, y cada una se llevó el
    bloque de imports ENTERO. Quedaron **95 nombres importados y no usados**: `hashlib` en la que
    no hashea, `Decimal` en la que no calcula, `plazos` en la que no computa plazos.

    No rompe nada, y por eso se queda: un import de más es gratis hasta que alguien lee el
    encabezado para saber de qué depende el archivo y le contesta la copia, no el uso. La partición
    se hizo para que cada suite diga qué afirma; el encabezado tiene que decir lo mismo.

    **`load_tests` es la excepción y no se toca.** `unittest` lo busca **por nombre** en el módulo:
    importarlo ES usarlo, aunque ninguna línea lo nombre. Sacarlo no da error — deja de plantarse
    fuera del checkout y la suite pasa a dar cincuenta rojos que no son defectos.

    MUTACIÓN que lo comprueba: agregar `import hashlib` a `test_scripts.py` lo deja en rojo con el
    archivo y el nombre.
    """

    #: `load_tests` se importa para que `unittest` lo encuentre por nombre y `annotations` es una
    #: directiva del compilador: los dos son imports que por definición nadie escribe después.
    POR_PROTOCOLO = {"load_tests", "annotations"}

    def test_cada_suite_importa_solo_lo_que_usa(self):
        import ast
        base = Path(__file__).resolve().parent
        archivos = sorted(base.glob("*.py"))
        self.assertGreater(len(archivos), 8, "no encontró los scripts: el control está apagado")
        sobrantes = []
        for f in archivos:
            arbol = ast.parse(f.read_text(encoding="utf-8"))
            atados = {}
            for nodo in ast.walk(arbol):
                if isinstance(nodo, (ast.Import, ast.ImportFrom)):
                    for a in nodo.names:
                        atados[a.asname or a.name.split(".")[0]] = nodo.lineno
            usados = {n.id for n in ast.walk(arbol) if isinstance(n, ast.Name)}
            usados |= {n.attr for n in ast.walk(arbol) if isinstance(n, ast.Attribute)}
            for nombre, linea in sorted(atados.items()):
                if nombre in usados or nombre in self.POR_PROTOCOLO:
                    continue
                sobrantes.append(f"{f.name}:{linea} importa `{nombre}` y no lo usa")
        self.assertEqual(sobrantes, [],
                         "imports que sobraron al partir el archivo:\n    "
                         + "\n    ".join(sobrantes))


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
