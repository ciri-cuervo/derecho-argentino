#!/usr/bin/env python3
"""Tests del medidor de deuda. Sin dependencias externas.

    python3 herramientas/test_pendientes.py
"""
import re
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))

import pendientes


class TestMarcadoresDeInstituto(unittest.TestCase):
    """Distingue el hueco de contenido de la definición del marcador y de la prosa que lo cita."""

    def test_encuentra_huecos_reales(self):
        hallados = pendientes.institutos_sin_precedente()
        self.assertGreater(len(hallados), 0, "dejó de leer los marcadores de los módulos")
        for archivo, _, payload in hallados:
            with self.subTest(f"{archivo}: {payload[:40]}"):
                self.assertNotEqual(payload, "...")
                self.assertFalse(payload.startswith("doctrina requerida"))

    def test_no_cuenta_la_definicion_del_marcador(self):
        # marcadores.md define B1: si entrara al corpus, el módulo del vocabulario figuraría
        # como si le faltara doctrina.
        self.assertNotIn("marcadores.md", {a for a, _, _ in pendientes.institutos_sin_precedente()})


class TestDeudaPorBloque(unittest.TestCase):
    def test_la_frase_no_se_corta_en_una_abreviatura(self):
        # "Falta fallo cargado sobre la escala del art. 44" se cortaba en "del art".
        frases = [t for _, _, t in pendientes.deuda_por_bloque()]
        self.assertTrue(frases, "dejó de leer la tabla de estado de verificación")
        for frase in frases:
            with self.subTest(frase[:50]):
                self.assertFalse(frase.rstrip().endswith(("art", "Ley", "Leyes", "Decreto")),
                                 f"frase cortada en una abreviatura: {frase!r}")


class TestVerificacionVencida(unittest.TestCase):
    def test_aplica_la_regla_de_seis_meses_de_la_propia_tabla(self):
        self.assertEqual(pendientes.DIAS_DE_GRACIA, 180)
        lejano = date(2030, 1, 1)
        self.assertGreater(len(pendientes.verificacion_vencida(lejano)), 0,
                           "con una fecha lejana todos los bloques tienen que estar vencidos")

    def test_ordena_del_mas_vencido_al_menos(self):
        vencidos = pendientes.verificacion_vencida(date(2030, 1, 1))
        dias = [d for _, _, d in vencidos]
        self.assertEqual(dias, sorted(dias, reverse=True))


class TestCruceConEvals(unittest.TestCase):
    def test_reconoce_el_modulo_por_el_slug_del_caso(self):
        # `civil-danos-transito-...` ejercita civil.md sin nombrar el archivo.
        self.assertNotIn("civil.md", pendientes.modulos_sin_eval())

    def test_los_modulos_de_rama_sin_eval_se_reportan(self):
        """Lo reportado tiene que ser cierto, y tiene que quedar algo por reportar.

        No se fijan nombres: un test que nombra `transito.md` como deuda se rompe el día que
        alguien le escribe el eval, o sea que castiga justo el trabajo que la medida pide. Lo
        que no decae es la invariante: todo lo que la lista reporta no está nombrado por ningún
        caso, y la lista no está vacía —si lo estuviera sin que la deuda se hubiera saldado,
        el instrumento se apagó—.
        """
        sin_eval = pendientes.modulos_sin_eval()
        self.assertGreater(len(sin_eval), 0,
                           "la lista quedó vacía: o se saldó toda la deuda, o el cruce con "
                           "evals/ dejó de leer")
        nombrados = set()
        for carpeta in pendientes.EVALS.iterdir():
            if carpeta.is_dir() and (carpeta / "caso.md").is_file():
                for pieza in carpeta.glob("*.md"):
                    nombrados |= set(re.findall(r"([a-z][a-z0-9-]*\.md)",
                                                pieza.read_text(encoding="utf-8")))
        for modulo in sin_eval:
            with self.subTest(modulo):
                self.assertNotIn(modulo, nombrados,
                                 f"{modulo} se reporta como sin eval y hay un caso que lo "
                                 f"nombra: la medida está reportando deuda que no existe")

    def test_el_nombre_compuesto_no_hereda_el_prefijo_de_su_primera_palabra(self):
        """Un módulo acotado no queda testeado porque otro caso comparta su primera palabra.

        `penal-juvenil-pba.md` es el Fuero de la Responsabilidad Penal Juvenil y
        `penal-estupefacientes-arriola-nulidad` es un caso de tenencia: comparten «penal» y nada
        más. Contar el prefijo lo daba por ejercitado sin que existiera una consulta que lo
        abriera: deuda invisible dentro de la medida que existe para hacerla visible. El prefijo
        sigue valiendo para un módulo de rama entera, cuyo nombre es una sola palabra.

        El árbol se arma acá y no se cruza el repositorio real, porque hoy todos los módulos
        compuestos están nombrados por su eval y la comparación pasaría igual con el criterio
        viejo: un guardarraíl sólo cubre lo que su fixture ejercita.

        MUTACIÓN que lo demuestra: volver el criterio a `stem.split("-")[0] in prefijos` tiene
        que poner este test en rojo.
        """
        raiz = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, raiz, True)
        refs, evals = raiz / "references", raiz / "evals"
        refs.mkdir()
        for nombre in ("civil.md", "penal.md", "penal-juvenil-pba.md", "salud-x.md"):
            (refs / nombre).write_text("# módulo\n", encoding="utf-8")
        # Dos casos. Ninguno NOMBRA un archivo: los dos sólo aportan su prefijo.
        for caso in ("civil-danos-transito-pba", "penal-estupefacientes-arriola"):
            d = evals / caso
            d.mkdir(parents=True)
            (d / "caso.md").write_text("# caso sin citar ningún archivo\n", encoding="utf-8")

        original = (pendientes.REFERENCIAS, pendientes.EVALS)
        pendientes.REFERENCIAS, pendientes.EVALS = refs, evals
        try:
            sin_eval = pendientes.modulos_sin_eval()
        finally:
            pendientes.REFERENCIAS, pendientes.EVALS = original

        self.assertNotIn("civil.md", sin_eval,
                         "el prefijo tiene que seguir valiendo para un módulo de rama entera")
        self.assertNotIn("penal.md", sin_eval, "ídem: nombre simple, caso con su prefijo")
        self.assertIn("penal-juvenil-pba.md", sin_eval,
                      "un módulo de nombre compuesto no queda ejercitado por compartir la "
                      "primera palabra con un caso que no lo nombra")
        self.assertIn("salud-x.md", sin_eval,
                      "y menos todavía uno cuyo prefijo no aparece en ningún caso")


    def test_la_lista_de_infraestructura_nombra_modulos_que_existen(self):
        """Una lista de exenciones se pudre cuando nombra archivos que ya no están.

        Cada nombre que sobra baja la deuda reportada sin que nadie lo decida: el módulo se
        renombró o se borró, y su exención sigue descontando. Y al revés, un módulo de rama que
        entre a la lista por error desaparece de la medida.

        MUTACIÓN que lo demuestra: agregar un nombre inventado a `DE_INFRAESTRUCTURA` tiene que
        poner este test en rojo.
        """
        existen = {m.name for m in pendientes.REFERENCIAS.glob("*.md")}
        sobran = sorted(pendientes.DE_INFRAESTRUCTURA - existen)
        self.assertEqual(sobran, [],
                         f"DE_INFRAESTRUCTURA exime módulos que no existen: {sobran}. Cada uno "
                         f"descuenta deuda que nadie decidió descontar")

    def test_ningun_modulo_de_rama_esta_exento(self):
        """La exención es para lo que describe cómo trabaja la skill, no para una rama.

        El criterio no se puede inferir del nombre —`perfiles-heredados.md` suena a rama y es un
        índice— así que se comprueba contra la tabla de cobertura, que declara qué ramas tienen
        módulo. Si una de ésas apareciera exenta, la deuda de cobertura se estaría escondiendo
        en la lista que la mide.
        """
        cobertura = (pendientes.RAIZ / "docs" / "COBERTURA.md").read_text(encoding="utf-8")
        tabla = cobertura.split("## Materias con módulo que no son un fuero", 1)
        self.assertGreater(len(tabla), 1, "cambió la sección de COBERTURA.md que se cruza acá")
        for exento in sorted(pendientes.DE_INFRAESTRUCTURA):
            with self.subTest(exento):
                self.assertNotIn(f"`{exento}`", tabla[1].split("##")[0],
                                 f"{exento} figura como módulo de una materia en COBERTURA.md, "
                                 f"así que su deuda de eval es real y no se exime")

class TestParserDeTabla(unittest.TestCase):
    """La fila delimitadora se reconoce con y sin espacios alrededor del guion.

    Buscarla con `startswith("|--")` andaba con `|---|---|` y fallaba EN SILENCIO con
    `| --- | --- |`: la fila pasaba como dato, se leía "---" como nombre de bloque y el reporte
    quedaba con una entrada fantasma que no dice nada. Un parser de tablas no puede depender de
    si el que escribió la tabla puso espacios.
    """

    def test_reconoce_los_dos_estilos(self):
        for fila in ("|---|---|", "| --- | --- |", "|---|---|---|---|---|",
                     "| --- | --- | --- |", "|:--|--:|", "| :-- | --: |"):
            with self.subTest(fila):
                self.assertIsNotNone(pendientes.DELIMITADOR.fullmatch(fila),
                                     "no reconoce esta fila delimitadora")

    def test_no_confunde_una_fila_de_datos(self):
        """MUTACIÓN del patrón: si se vuelve permisivo, se come filas con contenido."""
        for fila in ("| Bloque | Modulo | Fecha |", "| **Transito** | `transito.md` | 14/09/2026 |",
                     "| - | - fila con guiones de verdad | x |"):
            with self.subTest(fila):
                self.assertIsNone(pendientes.DELIMITADOR.fullmatch(fila),
                                  "toma por delimitadora una fila con datos")

    def test_la_tabla_de_verificacion_no_trae_filas_fantasma(self):
        for campos in pendientes._filas_de_verificacion():
            with self.subTest(campos[0][:30]):
                self.assertNotRegex(campos[0], r"^[-:\s]*$",
                                    "una fila delimitadora entro como dato")


class TestLasDosMitadesDeLaVerificacion(unittest.TestCase):
    """La verificación por bloque vive en dos tablas y **la clave es el par bloque + módulo**.

    `references/changelog-normativo.md` lleva la fecha y la volatilidad, que es lo que contesta
    «¿desde cuándo rige?» y es lo único que el lector de la skill necesita. `docs/REVALIDAR.md`
    lleva con qué texto se cotejó y qué salió, que es lo que necesita el que revalida — y pesaba
    seis veces más que las otras cuatro columnas juntas adentro de un módulo que se carga en cada
    consulta sobre vigencia.

    **Partir una tabla en dos crea la posibilidad de que se desincronicen**, y eso no falla
    ruidosamente: una fila que quedó sola sigue leyéndose bien de su lado. Esto es lo que lo
    impide, y por eso el orden también se exige — las dos se leen de arriba abajo.

    MUTACIÓN que lo comprueba: sacarle una fila a cualquiera de las dos, o cambiarle el módulo a
    una fila de una sola, deja en rojo `test_las_dos_tablas_tienen_las_mismas_filas`.
    """

    def _pares(self, filas):
        return [(f[0].replace("**", ""), f[1]) for f in filas]

    def test_las_dos_tablas_tienen_las_mismas_filas(self):
        skill = self._pares(pendientes._filas_de_verificacion())
        docs = self._pares(pendientes._filas_de_revalidacion())
        self.assertGreater(len(skill), 100, "no leyó la tabla de la skill: el control está apagado")
        faltan_en_docs = [p for p in skill if p not in docs]
        faltan_en_skill = [p for p in docs if p not in skill]
        self.assertEqual(faltan_en_docs, [],
                         "bloques con fecha y sin cotejo escrito en docs/REVALIDAR.md")
        self.assertEqual(faltan_en_skill, [],
                         "bloques con cotejo en docs/REVALIDAR.md y sin fecha en la skill")
        self.assertEqual(skill, docs, "las dos tablas tienen las mismas filas en otro orden")

    def test_ninguna_fila_esta_dos_veces(self):
        """Dos filas del mismo par son dos relojes para un solo bloque, y el de la fecha vieja no
        sirve para nada. Pasó con «Ejecución de la pena», donde la segunda fila no registraba una
        verificación sino una mudanza de módulo: **reiniciaba los seis meses sin que nadie hubiera
        vuelto a leer la norma**, que es justo el modo de falla que la tabla existe para evitar.
        """
        pares = self._pares(pendientes._filas_de_verificacion())
        repetidos = sorted({p for p in pares if pares.count(p) > 1})
        self.assertEqual(repetidos, [],
                         "el mismo bloque con dos fechas de verificación: "
                         + ", ".join(f"{b} ({m})" for b, m in repetidos))

    def test_el_ancho_de_cada_tabla_es_el_que_se_espera(self):
        """Instrumento encendido. El parser exige el ancho justo porque, si una tabla cambia de
        forma, uno laxo sigue leyendo, lee otra cosa y **reporta cero** — y cero acá se lee como
        que no hay deuda."""
        self.assertTrue(all(len(f) == 4 for f in pendientes._filas_de_verificacion()))
        self.assertTrue(all(len(f) == 3 for f in pendientes._filas_de_revalidacion()))
        self.assertGreater(len(pendientes.deuda_por_bloque()), 0,
                           "la deuda por bloque dio cero: el parser dejó de enganchar")


class TestLosVeredictosNoSeLlenanDeMuertos(unittest.TestCase):
    """Cuatro de los siete archivos de veredicto reportan sus entradas muertas, y no acumulan.

    La línea de base de un detector **sólo crece**: una clave muere cuando el texto que la produjo
    cambió o se mudó, y entonces no esconde nada pero infla la lista — y una lista inflada se deja
    de leer, que es el modo en que este repositorio pierde una alarma. Medido el 18/09/2026:
    `cobertura-revisada.json` escribía 98 veredictos y usaba 56.

    **Tres no tienen noción de muerto y eso está declarado en `_veredictos.muertos`:**
    `fuga-revisada` porque su detector recibe los archivos por argumento, `ramas-revisadas` porque
    ahí un veredicto es una declaración que sobrevive al detector a propósito —medido, daba 7
    falsos—, y `lecturas-ocr` sí lo reporta pero no se purga: una lectura vale por su fecha.

    MUTACIÓN que lo comprueba: agregarle una clave inventada a `cobertura-revisada.json` la hace
    aparecer en la salida de `cobertura_normativa.py` como muerta.
    """

    #: herramienta -> cuántas entradas muertas se toleran
    PUERTAS = {"cobertura_normativa.py": 0, "reformas_no_leidas.py": 0}

    def test_ninguna_herramienta_arrastra_veredictos_muertos(self):
        import subprocess, sys
        for h in self.PUERTAS:
            with self.subTest(h):
                r = subprocess.run([sys.executable, str(RAIZ / "herramientas" / h)],
                                   capture_output=True, text=True, cwd=str(RAIZ))
                self.assertNotIn("están MUERTAS", r.stdout,
                                 f"{h} arrastra veredictos muertos; se purgan con --purgar\n"
                                 + r.stdout[-400:])

    def test_el_aviso_existe_y_dice_el_comando(self):
        """Instrumento encendido: si `aviso_de_muertos` devolviera siempre vacío, el test de
        arriba pasaría sin medir nada."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_veredictos", RAIZ / "herramientas" / "_veredictos.py")
        v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
        self.assertEqual(v.muertos(["a", "b"], {"a"}), ["b"])
        self.assertEqual(v.aviso_de_muertos(0, 9, "x"), [])
        aviso = v.aviso_de_muertos(2, 9, "correr --purgar")
        self.assertTrue(any("MUERTAS" in l for l in aviso))
        self.assertTrue(any("correr --purgar" in l for l in aviso))


class TestEvalsSinCorrer(unittest.TestCase):
    """Un eval escrito y no corrido es una promesa, no una medición, y hasta ahora no lo medía
    nadie: `modulos_sin_eval()` contesta qué rama no tiene caso, y da cero con **todos** los
    casos sin correr. Es verde con el instrumento apagado sobre la pregunta que importa.

    La marca la escriben los propios `resultado.md`, que no se dejan vacíos: dicen «Sin correr»
    y desde cuándo.

    **La mutación es sobre el detector, no sobre un archivo**: estos tests cuentan contra los
    archivos vivos, así que tocar un `resultado.md` mueve la cifra y los dos lados a la vez —lo
    cual está bien, porque miden, no fijan—. Lo que hay que romper es la lectura.

    MUTACIÓN que lo comprueba: hacer que `evals_sin_correr()` no encuentre la marca deja en rojo
    `test_lo_que_reporta_es_lo_que_declaran_los_archivos` y
    `test_un_resultado_con_medicion_no_entra`, que arma su propio árbol y no depende del corpus.
    """

    def test_lo_que_reporta_es_lo_que_declaran_los_archivos(self):
        evals = pendientes.EVALS
        esperado = sorted(
            c.name for c in evals.iterdir()
            if c.is_dir() and (c / "caso.md").is_file() and (c / "resultado.md").is_file()
            and "**Sin correr" in (c / "resultado.md").read_text(encoding="utf-8"))
        self.assertEqual(pendientes.evals_sin_correr(), esperado)

    def test_el_control_mira_algo(self):
        """Si dejara de encontrar casos no mediría nada y su lista vacía se leería como «todos
        corridos». Lo que se fija acá es que haya casos, no cuántos están sin correr."""
        casos = [c for c in pendientes.EVALS.iterdir()
                 if c.is_dir() and (c / "caso.md").is_file()]
        self.assertGreater(len(casos), 20, "no encontró los casos: el control está apagado")

    def test_un_resultado_con_medicion_no_entra(self):
        """Contra un árbol de mentira, para no depender del estado del corpus."""
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            for nombre, cuerpo in (("corrido", "Corrió el 01/01/2026 y acertó."),
                                   ("pendiente", "**Sin correr.** Nadie lo pasó.")):
                (raiz / nombre).mkdir()
                (raiz / nombre / "caso.md").write_text("caso", encoding="utf-8")
                (raiz / nombre / "resultado.md").write_text(cuerpo, encoding="utf-8")
            viejo = pendientes.EVALS
            try:
                pendientes.EVALS = raiz
                self.assertEqual(pendientes.evals_sin_correr(), ["pendiente"])
            finally:
                pendientes.EVALS = viejo


class TestFuentesMarcadasParaRevisar(unittest.TestCase):
    """El campo `revisar` de las procedencias tiene que llegar a la lista de deuda.

    Lo escriben los dos descargadores cuando el texto bajado no es lo que dice ser -la URL
    devolvió la ficha, no aparece el articulado, la carátula no coincide con el documento- y
    durante varias versiones no lo leyó NADIE. Se escribía y se olvidaba, y la única forma de
    verlo era volver a bajar, que con los 403 de InfoLEG sólo puede hacer el usuario. Es texto
    offline que ya sabemos defectuoso y que la skill usa igual.
    """

    def test_lee_las_dos_procedencias_y_nombra_el_corpus(self):
        marcadas = pendientes.fuentes_marcadas_para_revisar()
        for corpus, slug, problema in marcadas:
            with self.subTest(slug):
                self.assertIn(corpus, ("normas", "jurisprudencia"))
                self.assertTrue(slug and problema, "una marca sin slug o sin problema")
                self.assertGreater(len(problema), 20,
                                   "el problema no dice qué hay que revisar")

    def test_lo_que_reporta_es_lo_que_esta_en_los_archivos(self):
        """Contra los archivos vivos: lo que el corpus tenga marcado tiene que salir listado.

        No exige que haya alguna. Lo exigía, con el motivo de que una lista vacía es
        indistinguible de un campo que se dejó de leer, y eso es cierto -- pero atar el
        control a que el corpus esté sucio lo convierte en un test que se rompe cuando el
        repositorio mejora, y la salida obvia entonces es apagarlo. El instrumento se prueba
        con el árbol armado a mano de acá abajo, que no depende del estado del corpus.
        """
        import json
        fuentes = pendientes.RAIZ / "derecho" / "fuentes"
        esperado = 0
        for ruta, clave in ((fuentes / "normas" / "procedencia.json", "normas"),
                            (fuentes / "jurisprudencia" / "procedencia.json", "fallos")):
            if ruta.is_file():
                entradas = json.loads(ruta.read_text(encoding="utf-8")).get(clave, {})
                esperado += sum(len(r.get("revisar", [])) for r in entradas.values())
        self.assertEqual(len(pendientes.fuentes_marcadas_para_revisar()), esperado)

    def test_sobre_un_arbol_armado_a_mano_encuentra_las_marcas(self):
        """El instrumento encendido, y sin depender de que el corpus tenga deuda.

        El modo de fallar de este bloque es devolver lista vacía y parecer que no hay nada
        que revisar. Acá hay tres marcas puestas a propósito, en los dos corpus y con una
        entrada que lleva dos: si alguna no sale, el campo se dejó de leer.
        """
        import json, tempfile
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            normas = raiz / "derecho" / "fuentes" / "normas"
            juris = raiz / "derecho" / "fuentes" / "jurisprudencia"
            normas.mkdir(parents=True)
            juris.mkdir(parents=True)
            (normas / "procedencia.json").write_text(json.dumps({"normas": {
                "ley-x": {"revisar": ["no se encontró ni un artículo: esto no es un articulado"]},
                "ley-y": {"revisar": ["hay acentuación degradada: la fuente sirve mal el texto",
                                      "solo 2 artículos en 300 caracteres: sospechosamente corto"]},
                "ley-sana": {"archivo": "ley-sana.txt"},
            }}), encoding="utf-8")
            (juris / "procedencia.json").write_text(json.dumps({"fallos": {
                "un-fallo": {"revisar": ["el documento bajado no menciona la carátula declarada"]},
            }}), encoding="utf-8")
            original = pendientes.RAIZ
            try:
                pendientes.RAIZ = raiz
                marcadas = pendientes.fuentes_marcadas_para_revisar()
            finally:
                pendientes.RAIZ = original
        self.assertEqual(len(marcadas), 4, marcadas)
        self.assertEqual({c for c, _, _ in marcadas}, {"normas", "jurisprudencia"})
        self.assertEqual(sorted(s for _, s, _ in marcadas),
                         ["ley-x", "ley-y", "ley-y", "un-fallo"])
        self.assertNotIn("ley-sana", [s for _, s, _ in marcadas])


class TestNingunaHerramientaQuedaSinDocumentar(unittest.TestCase):
    """Una herramienta que no está nombrada en ningún documento es una que nadie va a correr.

    No falla: simplemente no se usa, y lo que medía deja de medirse sin que nada lo diga. Pasó con
    dos que existían, tenían test y no estaban escritas en ninguna parte: `descargar_series.py`,
    que baja el IPC, el CER y el RIPTE que consumen las calculadoras, y el verificador de
    marcadores de una respuesta, que **desde entonces se mudó adentro del plugin** —es el único
    control que corre en tiempo de ejecución— y hoy lo cubre `scripts/README.md`.

    **Documentada quiere decir alcanzable desde una puerta.** `herramientas/pendientes.py` es la
    puerta de las que miden pendientes y las nombra con su comando; el resto —mapas, reparaciones,
    auditorías— vive en `docs/DESARROLLO.md`. `AGENTS.md` dice exactamente eso, y este test es lo
    que lo sostiene.

    MUTACIÓN que lo comprueba: sacar de `docs/DESARROLLO.md` la mención a `descargar_series.py`
    deja este test en rojo.
    """

    #: Las dos puertas. Una herramienta vale por estar en cualquiera.
    PUERTAS = ("herramientas/pendientes.py", "docs/DESARROLLO.md")

    def setUp(self):
        raiz = RAIZ
        self.raiz = raiz
        self.herramientas = [p for d in ("herramientas", "derecho/fuentes/scripts")
                             for p in sorted((raiz / d).glob("*.py"))
                             if not p.name.startswith(("test_", "_"))]
        self.docs = "\n".join((raiz / d).read_text(encoding="utf-8") for d in self.PUERTAS)

    def test_el_control_encuentra_las_herramientas(self):
        """Instrumento encendido: sin herramientas, «todas documentadas» no dice nada."""
        self.assertGreater(len(self.herramientas), 12,
                           "no encontró los ejecutables de herramientas/ ni de fuentes/scripts/")

    def test_todas_estan_nombradas_en_alguna_puerta(self):
        sueltas = [p.name for p in self.herramientas if p.name not in self.docs]
        self.assertEqual(
            sueltas, [],
            "herramientas que ningún documento nombra, así que nadie las va a correr: "
            + ", ".join(sueltas) + f". Van a {self.PUERTAS[0]} si miden un pendiente, y a "
            f"{self.PUERTAS[1]} si no.")



if __name__ == "__main__":
    unittest.main()
