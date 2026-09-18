#!/usr/bin/env python3
"""Tests del control de cifras de la documentación. Sin dependencias externas.

    python3 herramientas/test_cifras.py
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AQUI = Path(__file__).resolve().parent
HERRAMIENTA = AQUI / "cifras.py"


def _modulo():
    sys.path.insert(0, str(AQUI))
    spec = importlib.util.spec_from_file_location("cifras", HERRAMIENTA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestCifrasDelRepo(unittest.TestCase):
    """Las cifras que la documentación afirma tienen que ser las que hay en disco.

    Antes de esto la cobertura era opt-in y una cifra sin test no rompía nada. El caso que lo
    motivó y el diseño del censo están en `docs/DESARROLLO.md`, sección «Las cifras de la
    documentación no se escriben a mano».
    """

    @classmethod
    def setUpClass(cls):
        cls.mod = _modulo()
        cls.reg = cls.mod.cargar()
        cls.medidas = cls.mod.metricas(cls.reg)

    def test_las_cifras_estan_al_dia_y_el_censo_esta_limpio(self):
        hecho = subprocess.run([sys.executable, str(HERRAMIENTA)],
                               capture_output=True, text=True)
        self.assertEqual(hecho.returncode, 0,
                         "hay cifras desfasadas o sin declarar:\n" + hecho.stdout)

    def test_cada_metrica_tiene_definicion_y_mide_algo(self):
        """Una métrica que mide cero está apuntando a un glob que no existe, y sellaría un 0."""
        for nombre, valor in self.medidas.items():
            with self.subTest(nombre):
                self.assertGreater(valor, 0, f"`{nombre}` mide 0: la definición no apunta a nada")

    def test_ningun_archivo_de_capa_2_entra_al_alcance(self):
        """La frontera de licencia es la ruta, más cinco excepciones que la ruta no dice, y una
        de ellas -`derecho/evals/README.md`- estuvo en el alcance de este script. No tuvo
        consecuencia porque ninguna ancla apuntaba ahí, pero `--sellar` reescribe el archivo del
        ancla: era una puerta, no un incidente.
        """
        for archivo in list(self.reg["anclas"]) + list(self.reg["alcance"]):
            for ruta in self.reg["capa_2"]["rutas"]:
                with self.subTest(archivo):
                    self.assertFalse(archivo == ruta or archivo.startswith(ruta),
                                     f"{archivo} es capa 2 y este script le escribiría")

    def test_cargar_rechaza_un_registro_que_mete_capa_2_en_el_alcance(self):
        """La mutación del test anterior: sin esto, el control vive sólo en el registro y una
        ancla nueva pasa igual."""
        reg = json.loads((AQUI / "cifras.json").read_text(encoding="utf-8"))
        reg["alcance"].append("derecho/evals/consumidor-dano-punitivo-prescripcion/caso.md")
        with tempfile.TemporaryDirectory() as tmp:
            falso = Path(tmp) / "cifras.json"
            falso.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
            mod, original = _modulo(), None
            original, mod.REGISTRO = mod.REGISTRO, falso
            try:
                with self.assertRaises(mod.RegistroInvalido):
                    mod.cargar()
            finally:
                mod.REGISTRO = original

    def test_las_rutas_de_capa_2_son_las_que_declara_licencias(self):
        """Si la lista se acorta acá y no en LICENCIAS.md, deja de ser una excepción declarada."""
        licencias = (RAIZ / "LICENCIAS.md").read_text(encoding="utf-8")
        rutas = self.reg["capa_2"]["rutas"]
        self.assertEqual(len(rutas), 6, "son `kb/` y las cinco excepciones, ni una más")
        for ruta in rutas:
            with self.subTest(ruta):
                self.assertIn(ruta.rstrip("/").rsplit("/", 1)[-1], licencias,
                              "LICENCIAS.md no declara esta ruta como capa 2")

    def test_toda_ancla_nombra_una_metrica_declarada(self):
        for archivo, anclas in self.reg["anclas"].items():
            for entrada in anclas:
                with self.subTest(f"{archivo} {entrada['ancla']}"):
                    self.assertIn(entrada["metrica"], self.reg["metricas"])

    def test_toda_ancla_engancha_exactamente_una_vez(self):
        """Cero o dos no es un aviso: es un rojo. Si la frase se reescribió, corresponde mirarla
        y no sellar a ciegas la ocurrencia que quedó."""
        for archivo, anclas in self.reg["anclas"].items():
            texto = (RAIZ / archivo).read_text(encoding="utf-8")
            for entrada in anclas:
                patron = self.mod.compilar(entrada["ancla"], entrada.get("formato", "digito"))
                with self.subTest(f"{archivo} {entrada['ancla']}"):
                    self.assertEqual(len(patron.findall(texto)), 1)

    def test_todo_veredicto_trae_motivo_y_habla_el_vocabulario(self):
        _, veredictos = self.mod._veredictos.cargar(self.mod.VEREDICTOS, "cifras", vacio={})
        vocabulario = json.loads(
            self.mod.VEREDICTOS.read_text(encoding="utf-8"))["_vocabulario"]
        self.assertTrue(veredictos, "no hay veredictos cargados")
        for clave, motivo in veredictos.items():
            with self.subTest(clave):
                self.assertGreater(len(motivo), 40, "el motivo no explica nada")
                self.assertIn(motivo.split(" ")[0], vocabulario,
                              "el motivo no arranca con un término del vocabulario")
                self.assertIn(" | ", clave, "la clave es `archivo | cifra`")
                archivo = clave.split(" | ", 1)[0]
                self.assertIn(archivo, self.reg["alcance"],
                              "hay un veredicto sobre un archivo que no se censa")

    def test_las_cubiertas_por_otro_test_estan_cubiertas_de_verdad(self):
        """Declarar que otro test mide una cifra es la única forma de sacarla del censo sin
        sellarla. Si ese test no existe, la cifra quedó sin control y nadie se enteró."""
        for entrada in self.reg["cubiertas"]:
            with self.subTest(f"{entrada['archivo']} {entrada['test']}"):
                suite = RAIZ / entrada["suite"]
                self.assertTrue(suite.is_file(), f"no existe {entrada['suite']}")
                # Con re.M y sin pasar el texto al mensaje: el fuente de la suite son 1.800
                # renglones y assertRegex los vuelca enteros cuando falla.
                declarado = re.search(r"^class " + entrada["test"] + r"\b",
                                      suite.read_text(encoding="utf-8"), re.M)
                self.assertIsNotNone(
                    declarado, f"{entrada['suite']} no define {entrada['test']}")
                texto = (RAIZ / entrada["archivo"]).read_text(encoding="utf-8")
                self.assertIsNotNone(
                    re.search(entrada["patron"], texto),
                    f"«{entrada['patron']}» ya no está en {entrada['archivo']}")

    def test_todo_md_esta_en_el_alcance_o_excluido_con_motivo(self):
        """Sin esto, un documento nuevo escapa al censo entero, que es la misma forma del
        agujero que este control viene a tapar."""
        saltar = {".git", "__pycache__", "_local", "node_modules", ".playwright-mcp", ".venv"}
        alcance, excluidos = set(self.reg["alcance"]), self.reg["excluidos"]
        for f in sorted(RAIZ.rglob("*.md")):
            if set(f.relative_to(RAIZ).parts) & saltar:
                continue
            ruta = f.relative_to(RAIZ).as_posix()
            if ruta in alcance:
                continue
            with self.subTest(ruta):
                cubre = [k for k in excluidos if ruta == k or ruta.startswith(k)]
                self.assertTrue(cubre, f"{ruta} no está en el alcance ni excluido en cifras.json")
                self.assertGreater(len(excluidos[cubre[0]]), 40,
                                   "la exclusión no dice por qué")


class TestMecanicaDelSellado(unittest.TestCase):
    """El sellado escribe números en la prosa, así que sus bordes se prueban aparte.

    Se corre sobre un árbol de juguete y no sobre el repo: un test que reescribe `README.md`
    para comprobar que sabe reescribirlo deja el repo sucio si falla en el medio.
    """

    @classmethod
    def setUpClass(cls):
        cls.mod = _modulo()

    def test_el_ancla_en_palabras_conserva_la_mayuscula(self):
        for valor, tal_como_estaba, esperado in [(6, "seis", "seis"), (6, "Seis", "Seis"),
                                                 (8, "ocho", "ocho"), (20, "Dos", "Veinte")]:
            with self.subTest(f"{valor} sobre «{tal_como_estaba}»"):
                self.assertEqual(
                    self.mod.escribir(valor, "palabra", tal_como_estaba, "{n} tomos"), esperado)

    def test_se_niega_a_escribir_una_palabra_que_no_existe(self):
        """MUTACIÓN: preferimos un control que se plante antes que uno que escriba «un módulos»
        o invente «treinta y uno». Los dos casos piden que una persona toque la frase.

        **La frontera es 29 y no 20 porque es la del idioma**, no la del uso: hasta veintinueve el
        número se escribe con UNA palabra y a partir de treinta y uno son tres. Estaba en veinte
        hasta que aparecieron los veintiséis marcadores, y veinte no era una regla: era hasta
        dónde se había necesitado."""
        for valor in (0, 1, 30, 31, 138):
            with self.subTest(valor):
                with self.assertRaises(self.mod.RegistroInvalido):
                    self.mod.escribir(valor, "palabra", "seis", "{n} tomos")

    def test_la_alternancia_pone_las_palabras_largas_primero(self):
        """Si «seis» va antes que «dieciséis», el ancla matchea el final de la palabra larga y
        el número se lee como 6 en vez de 16."""
        patron = self.mod.compilar("{n} tomos", "palabra")
        m = patron.search("son dieciséis tomos")
        self.assertEqual(self.mod.leer(m.group(1), "palabra"), 16)

    def test_el_ancla_exige_un_solo_marcador(self):
        for ancla in ("{n} de {n} normas", "sin marcador"):
            with self.subTest(ancla):
                with self.assertRaises(self.mod.RegistroInvalido):
                    self.mod.compilar(ancla, "digito")

    def test_el_registro_no_puede_apuntar_a_kb(self):
        """MUTACIÓN: `derecho/kb/` es capa 2 y de otro autor. Un script que le escriba rompe
        la frontera de licencia, y el que la vigila es `frontera_kb.py`, no este."""
        with tempfile.TemporaryDirectory() as d:
            falso = Path(d) / "cifras.json"
            reg = json.loads((AQUI / "cifras.json").read_text(encoding="utf-8"))
            reg["anclas"]["derecho/kb/laboral-CLAUDE.md"] = [
                {"ancla": "**{n} módulos**", "metrica": "modulos"}]
            falso.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
            verdadero = self.mod.REGISTRO
            try:
                self.mod.REGISTRO = falso
                with self.assertRaises(self.mod.RegistroInvalido) as caso:
                    self.mod.cargar()
                self.assertIn("capa 2", str(caso.exception))
            finally:
                self.mod.REGISTRO = verdadero


class TestMecanicaDelCenso(unittest.TestCase):
    """El censo es lo que convierte el olvido en un rojo, así que sus falsos positivos y sus
    falsos negativos se prueban sobre fixtures y no sobre el repo."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _modulo()
        cls.reg = cls.mod.cargar()
        cls.patron = cls.mod.patron_del_censo(cls.reg)

    def test_encuentra_la_cifra_en_digitos_y_en_palabras(self):
        for texto in ("guarda **132 normas** y", "son seis tomos con índice",
                      "Cuatro calculadoras deterministas", "los **8 comandos slash**"):
            with self.subTest(texto):
                self.assertTrue(self.patron.search(texto), "el censo no vio la cifra")

    def test_cruza_el_salto_de_renglon(self):
        """REGRESIÓN: la primera versión censaba renglón por renglón y no veía «Son dos
        módulos espejo» cuando la frase quedaba partida. La prosa se envuelve."""
        m = self.patron.search("y ver `references/parte.md`. Son dos\nmódulos espejo: el mismo")
        self.assertIsNotNone(m)
        self.assertEqual(re.sub(r"\s+", " ", m.group(0)), "dos módulos")

    def test_un_digito_pegado_a_una_palabra_no_es_una_cifra(self):
        """Un `python3 herramientas/...` parece decir «3 herramientas», y la documentación
        está llena de invocaciones así. Lo que los descarta es exigir que el número no venga
        pegado a una letra, a una barra, a un punto ni a un guion — eso último por los slugs,
        que terminan en número."""
        for texto in ("    python3 herramientas/test_frontera.py",
                      "correr python3 herramientas/cifras.py --sellar",
                      "el texto de `ley-27798.txt` normas",
                      "el índice de `csjn-casal-fallos-328-3399` fallos"):
            with self.subTest(texto):
                self.assertIsNone(self.patron.search(texto), f"falso positivo en «{texto}»")

    def test_pero_el_mismo_numero_suelto_si_lo_es(self):
        """MUTACIÓN del descarte de arriba: si el lookbehind se pasa de largo, el censo se
        vuelve ciego y deja de ser un control."""
        self.assertIsNotNone(self.patron.search("son 3 herramientas de control"))
        self.assertIsNotNone(self.patron.search("hay 3399 fallos"))

    def test_una_cifra_nueva_sin_declarar_rompe_el_censo(self):
        """MUTACIÓN: es la propiedad entera de este control. Se prueba sobre una copia del
        alcance en un directorio temporal, para no ensuciar el repo."""
        with tempfile.TemporaryDirectory() as d:
            raiz_falsa = Path(d)
            (raiz_falsa / "docs").mkdir()
            (raiz_falsa / "docs" / "TERMINAL.md").write_text(
                "Instalar desde la terminal. Sin cifras acá.\n", encoding="utf-8")
            reg = {**self.reg, "alcance": ["docs/TERMINAL.md"], "anclas": {}, "cubiertas": []}
            verdadera = self.mod.RAIZ
            try:
                self.mod.RAIZ = raiz_falsa
                huerfanas, _ = self.mod.censar(reg, {})
                self.assertEqual(huerfanas, [], "el fixture limpio no debería tener hallazgos")

                (raiz_falsa / "docs" / "TERMINAL.md").write_text(
                    "Ahora hay **41 módulos** auditados.\n", encoding="utf-8")
                huerfanas, _ = self.mod.censar(reg, {})
                self.assertEqual(len(huerfanas), 1, "una cifra nueva pasó sin declararse")
                self.assertIn("41 módulos", huerfanas[0])

                # Y con el veredicto puesto, deja de ser huérfana.
                huerfanas, sin_usar = self.mod.censar(
                    reg, {"docs/TERMINAL.md | 41 módulos": "locucion — motivo largo de prueba "
                                                           "que pasa los cuarenta caracteres"})
                self.assertEqual((huerfanas, sin_usar), ([], []))
            finally:
                self.mod.RAIZ = verdadera

    def test_un_veredicto_que_ya_no_aplica_tambien_rompe(self):
        """Si la cifra se fue del archivo, el veredicto quedó colgado: el archivo de lecturas
        tiene que bajar cuando el problema baja, no acumular entradas muertas."""
        with tempfile.TemporaryDirectory() as d:
            raiz_falsa = Path(d)
            (raiz_falsa / "docs").mkdir()
            (raiz_falsa / "docs" / "TERMINAL.md").write_text("Sin cifras.\n", encoding="utf-8")
            reg = {**self.reg, "alcance": ["docs/TERMINAL.md"], "anclas": {}, "cubiertas": []}
            verdadera = self.mod.RAIZ
            try:
                self.mod.RAIZ = raiz_falsa
                _, sin_usar = self.mod.censar(
                    reg, {"docs/TERMINAL.md | 41 módulos": "locucion — motivo largo de prueba "
                                                           "que pasa los cuarenta caracteres"})
                self.assertEqual(sin_usar, ["docs/TERMINAL.md | 41 módulos"])
            finally:
                self.mod.RAIZ = verdadera


class TestElPesoSeMideIgualEnCualquierMaquina(unittest.TestCase):
    """`mb_instalados` tiene que dar lo mismo acá y en el runner de CI. No daba, dos veces.

    La primera versión sumaba la carpeta `derecho/` entera: decía **85** en una máquina de trabajo
    y **84** en CI, y la diferencia eran 0,77 MB de `__pycache__` y `.DS_Store`. Se filtraron por
    patrón y el pipeline volvió a romper, ahora por **1,19 MB** de `derecho/evals/results/`, que
    deja `claude plugin eval` y `.gitignore` ya excluía.

    **Agregar `results` a la lista habría sido calibrar contra el caso conocido**, y la lista
    siempre va a ir atrás de la próxima herramienta que escriba algo en el árbol. Lo que se
    cambió fue la definición: la cifra dice cuánto descarga quien instala, y eso es **lo que el
    repositorio versiona**, no lo que hay en la carpeta de quien mide. Git ya sabe qué ignora, y
    preguntarle es una regla en vez de una lista.

    El filtro por patrón además se equivocaba al revés: salteaba todo tramo con punto, de modo que
    `derecho/.claude-plugin/plugin.json` —que sí viaja— no contaba.

    MUTACIÓN que lo comprueba: es este test. Arma un repo de prueba con un archivo versionado y
    otro ignorado, y exige que sólo pese el primero. Volver a `rglob` sobre la carpeta lo deja en
    rojo.
    """

    @classmethod
    def setUpClass(cls):
        cls.mod = _modulo()
        if subprocess.run(["git", "--version"], capture_output=True).returncode != 0:
            raise unittest.SkipTest("sin git no se puede armar el repo de prueba")

    def _medir(self, raiz, excluye=()):
        original, self.mod.RAIZ = self.mod.RAIZ, raiz
        try:
            return self.mod.medir("mb_instalados", {"tipo": "megabytes", "carpeta": "plugin",
                                                    "excluye": list(excluye)})
        finally:
            self.mod.RAIZ = original

    @staticmethod
    def _repo(raiz):
        """Un repo mínimo: `results/` ignorado, y un archivo versionado de 5 MB."""
        correr = lambda *a: subprocess.run(["git", "-C", str(raiz), *a],
                                           capture_output=True, check=True)
        correr("init", "-q")
        correr("config", "user.email", "t@t"); correr("config", "user.name", "t")
        (raiz / ".gitignore").write_text(
            "plugin/results/\n__pycache__/\n", encoding="utf-8")
        plugin = raiz / "plugin"
        (plugin / "fuentes").mkdir(parents=True)
        (plugin / "fuentes" / "norma.txt").write_bytes(b"\0" * 5_000_000)
        correr("add", "-A"); correr("commit", "-qm", "x")

    def test_solo_pesa_lo_que_el_repositorio_versiona(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            self._repo(raiz)
            limpio = self._medir(raiz)
            self.assertEqual(limpio, 5, "no midió el archivo versionado, que es lo que viaja")

            plugin = raiz / "plugin"
            (plugin / "results" / "corrida").mkdir(parents=True)
            (plugin / "results" / "corrida" / "report.html").write_bytes(b"\0" * 4_000_000)
            (plugin / "scripts" / "__pycache__").mkdir(parents=True)
            (plugin / "scripts" / "__pycache__" / "x.pyc").write_bytes(b"\0" * 4_000_000)
            (plugin / "fuentes" / ".DS_Store").write_bytes(b"\0" * 4_000_000)

            self.assertEqual(
                self._medir(raiz), limpio,
                "la cifra se movió con archivos que git ignora: volvió a medir la carpeta en vez "
                "de lo versionado, y va a decir una cosa acá y otra en CI")

    def test_un_archivo_oculto_versionado_si_pesa(self):
        """El filtro por patrón salteaba todo tramo con punto y dejaba afuera
        `.claude-plugin/plugin.json`, que viaja con el plugin. Medir lo versionado lo arregla
        solo, y esto lo fija para que no vuelva."""
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            self._repo(raiz)
            oculta = raiz / "plugin" / ".claude-plugin"
            oculta.mkdir()
            (oculta / "plugin.json").write_bytes(b"\0" * 2_000_000)
            subprocess.run(["git", "-C", str(raiz), "add", "-A"], capture_output=True, check=True)
            subprocess.run(["git", "-C", str(raiz), "commit", "-qm", "y"],
                           capture_output=True, check=True)
            self.assertEqual(self._medir(raiz), 7,
                             "un archivo versionado dentro de una carpeta oculta tiene que pesar")

    def test_se_planta_si_no_puede_medir(self):
        """No hay verde por ausencia de instrumento: fuera de un repo, `git ls-files` falla y la
        métrica corta en vez de estimar desde el disco."""
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / "plugin").mkdir()
            (raiz / "plugin" / "x.txt").write_bytes(b"\0" * 5_000_000)
            with self.assertRaises(self.mod.RegistroInvalido):
                self._medir(raiz)


if __name__ == "__main__":
    unittest.main()
