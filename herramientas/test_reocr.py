#!/usr/bin/env python3
"""Tests del cotejo declarado del OCR. Sin dependencias externas: no corre tesseract.

    python3 herramientas/test_reocr.py

El cotejo del OCR se declara como dato y lo aplica el script; el porqué está en
`derecho/fuentes/MANIFIESTO.md`, sección «El cotejo se declara, no se edita».

Lo que se prueba acá es la parte que decide si eso es confiable o si es una edición a mano con
otro nombre: que una corrección que ya no coincide con lo que el OCR devuelve PLANTE el script en
vez de trasladarse a ciegas. Sin eso, una versión nueva de tesseract convertiría el cotejo en un
generador de texto que nadie leyó, que es el peor error posible en un fallo.
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "reocr_jurisprudencia.py"
COTEJOS = RAIZ / "derecho" / "fuentes" / "jurisprudencia" / "ocr" / "correcciones"


def cargar():
    spec = importlib.util.spec_from_file_location("reocr_jurisprudencia", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class TestAplicarCotejo(unittest.TestCase):
    """Aplicar una corrección declarada, y negarse cuando ya no corresponde."""

    def setUp(self):
        self.r = cargar()

    def _cotejo(self, *pares):
        return {"cotejado_el": "2026-09-16", "base": "páginas del PDF leídas una por una",
                "correcciones": [{"pagina": 1, "impresa": 1, "de": d, "a": a,
                                  "motivo": "el OCR leyó mal el volado del ordinal"}
                                 for d, a in pares]}

    def test_corrige_lo_declarado_y_deja_el_resto_intacto(self):
        cuerpo = "19) Que según surge\notra linea con regisiro\n"
        salida = self.r.aplicar_cotejo(cuerpo, self._cotejo(("19) Que", "1°) Que")), "x")
        self.assertIn("1°) Que según surge", salida)
        # Lo que el cotejo no declara NO se toca, aunque sea un error evidente del OCR: el
        # cotejo es lo que alguien leyó, no lo que se podría deducir.
        self.assertIn("regisiro", salida)

    def test_aplica_en_orden_y_no_se_pisan(self):
        cuerpo = "primero 19) y despues 29)\n"
        salida = self.r.aplicar_cotejo(
            cuerpo, self._cotejo(("19)", "1°)"), ("29)", "2°)")), "x")
        self.assertEqual(salida, "primero 1°) y despues 2°)\n")

    def test_se_planta_si_la_correccion_ya_no_coincide(self):
        # El caso real: tesseract cambia de versión y deja de devolver el error que el cotejo
        # arregla. Trasladar la corrección igual sería escribir en el fallo algo que nadie leyó.
        with self.assertRaises(SystemExit) as caso:
            self.r.aplicar_cotejo("el texto ya salió bien\n",
                                  self._cotejo(("19) Que", "1°) Que")), "fiorentino")
        self.assertIn("coincide 0 veces", str(caso.exception))
        self.assertIn("volver a leer", str(caso.exception).lower())

    def test_se_planta_si_la_correccion_coincide_dos_veces(self):
        # No es un detalle: `39) Que en primera instancia` aparece en el voto de la mayoría y en
        # el de Petracchi. Una sustitución sin contexto corregiría el renglón equivocado y el
        # otro quedaría mal, las dos cosas en silencio.
        cuerpo = "39) Que en primera instancia\n...\n39) Que en primera instancia\n"
        with self.assertRaises(SystemExit) as caso:
            self.r.aplicar_cotejo(cuerpo, self._cotejo(("39) Que en primera instancia",
                                                        "3°) Que en primera instancia")), "x")
        self.assertIn("coincide 2 veces", str(caso.exception))

    def test_el_mensaje_dice_cual_correccion_y_en_que_pagina(self):
        cotejo = self._cotejo(("presente", "presente"), ("ausente", "corregido"))
        cotejo["correcciones"][1]["pagina"] = 17
        with self.assertRaises(SystemExit) as caso:
            self.r.aplicar_cotejo("presente\n", cotejo, "x")
        self.assertIn("corrección 2", str(caso.exception))
        self.assertIn("17", str(caso.exception))


class TestCargarCotejo(unittest.TestCase):
    """Un cotejo incompleto no se acepta a medias: sin fecha ni base no se sabe qué se leyó."""

    def setUp(self):
        self.r = cargar()

    def test_sin_archivo_no_hay_cotejo(self):
        self.assertIsNone(self.r.cargar_cotejo("un-fallo-que-nadie-leyo"))

    def test_falta_un_campo_y_se_planta_diciendo_cual(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.r.COTEJOS = Path(tmp)
            (Path(tmp) / "x.json").write_text(
                json.dumps({"correcciones": []}), encoding="utf-8")
            with self.assertRaises(SystemExit) as caso:
                self.r.cargar_cotejo("x")
            self.assertIn("base", str(caso.exception))
            self.assertIn("cotejado_el", str(caso.exception))


class TestEncabezadoDelCotejo(unittest.TestCase):
    """El encabezado tiene que decir que hay renglones corregidos, y que el resto no lo está."""

    FICHA = {"slug": "x", "caratula": "Fulano, Mengano.", "tribunal": "CSJN",
             "causa": "Fallos 1:1", "fecha": "1984-11-27", "url": "https://ejemplo/x"}

    def setUp(self):
        self.r = cargar()

    def _cabecera(self, cotejo):
        return self.r.encabezado(self.FICHA, Path("x.pdf"), "abc123", 9, "spa",
                                 "tesseract 5.5.3", cotejo)

    def test_sin_cotejo_no_anuncia_ninguno(self):
        cabecera = self._cabecera(None)
        self.assertIn("RECUPERADO POR OCR LOCAL", cabecera)
        self.assertNotIn("Cotejado:", cabecera)
        self.assertNotIn("ATENCIÓN", cabecera)

    def test_con_cotejo_lo_anuncia_y_avisa_que_el_resto_no_se_reviso(self):
        cotejo = {"cotejado_el": "2026-09-16", "base": "páginas del PDF leídas una por una",
                  "correcciones": [{"de": "a", "a": "b"}, {"de": "c", "a": "d"}]}
        cabecera = self._cabecera(cotejo)
        self.assertIn("Cotejado:         2026-09-16", cabecera)
        self.assertIn("páginas del PDF leídas una por una", cabecera)
        self.assertIn("2 declaradas en ocr/correcciones/x.json", cabecera)
        # Lo que más importa del aviso: un archivo medio cotejado que no lo dice invita a
        # confiar en el renglón de al lado, que sigue siendo salida cruda del OCR.
        self.assertIn("TODO EL RESTO es salida de máquina sin revisar", cabecera)


class TestCotejosDelRepositorio(unittest.TestCase):
    """Los cotejos que hay declarados tienen que ser aplicables, no sólo estar bien formados."""

    def setUp(self):
        self.r = cargar()
        if not COTEJOS.is_dir() or not any(COTEJOS.glob("*.json")):
            self.skipTest("todavía no hay ningún cotejo declarado")

    def test_ningun_cotejo_declara_dos_correcciones_con_el_mismo_origen(self):
        # Dos correcciones con el mismo `de` son un error de armado: la primera consume la
        # coincidencia y la segunda se planta, así que el cotejo entero queda inaplicable.
        for ruta in sorted(COTEJOS.glob("*.json")):
            cotejo = json.loads(ruta.read_text(encoding="utf-8"))
            origenes = [c["de"] for c in cotejo["correcciones"]]
            with self.subTest(ruta.stem):
                repetidos = {o for o in origenes if origenes.count(o) > 1}
                self.assertEqual(repetidos, set(), "hay correcciones con el mismo origen")

    def test_ninguna_correccion_deshace_a_otra(self):
        # Si el `a` de una es el `de` de otra, el orden decide el resultado y el cotejo deja de
        # ser una lista de hechos leídos para pasar a ser un programa.
        for ruta in sorted(COTEJOS.glob("*.json")):
            cotejo = json.loads(ruta.read_text(encoding="utf-8"))
            llegadas = {c["a"] for c in cotejo["correcciones"]}
            with self.subTest(ruta.stem):
                for c in cotejo["correcciones"]:
                    self.assertNotIn(c["de"], llegadas,
                                     f"la corrección de la página {c.get('pagina')} deshace a "
                                     f"otra: el resultado depende del orden")


class TestLoQueSeDecidioNoCorregir(unittest.TestCase):
    """Lo que el cotejo declara en `no_corregidas` tiene que SEGUIR en el texto.

    Son erratas del tomo impreso que parecen defectos de OCR; el caso y el porqué están en
    `derecho/fuentes/MANIFIESTO.md`. Este test es el candado: sin él, la lectura siguiente
    las vuelve a encontrar y las «arregla».
    """

    def setUp(self):
        if not COTEJOS.is_dir() or not any(COTEJOS.glob("*.json")):
            self.skipTest("todavía no hay ningún cotejo declarado")

    def test_lo_declarado_como_errata_del_tomo_sigue_textual(self):
        mirados = 0
        for ruta in sorted(COTEJOS.glob("*.json")):
            cotejo = json.loads(ruta.read_text(encoding="utf-8"))
            recuperado = (RAIZ / "derecho" / "fuentes" / "jurisprudencia" / "ocr"
                          / f"{ruta.stem}.txt")
            if not recuperado.is_file():
                continue
            texto = recuperado.read_text(encoding="utf-8")
            for e in cotejo.get("no_corregidas", []):
                mirados += 1
                with self.subTest(f"{ruta.stem}:{e['pagina']}"):
                    self.assertIn(e["texto"], texto,
                                  f"«{e['texto']}» se declaró errata del tomo impreso y ya no "
                                  f"está en el texto: alguien la corrigió, y eso hace que el "
                                  f"archivo diga algo que la página no dice. Motivo escrito: "
                                  f"{e['motivo'][:90]}")
        self.assertGreater(mirados, 0, "ningún cotejo declara `no_corregidas`: si de verdad no "
                                       "hay ninguna, sacar este test en vez de dejarlo en verde "
                                       "sin mirar nada")

    def test_ninguna_correccion_borra_una_errata_declarada(self):
        """Una corrección PUEDE tocar el renglón de una errata; lo que no puede es pisarla.

        Pasa de verdad: el renglón de «inpugnó» arranca con un ordinal que el OCR leyó mal,
        así que hay una corrección sobre esa misma línea. Está bien. Lo que el control mira
        es el resultado: si la errata entra en el `de` de una corrección, tiene que seguir
        entera en su `a`.
        """
        for ruta in sorted(COTEJOS.glob("*.json")):
            cotejo = json.loads(ruta.read_text(encoding="utf-8"))
            for e in cotejo.get("no_corregidas", []):
                for c in cotejo["correcciones"]:
                    if e["texto"] not in c["de"]:
                        continue
                    with self.subTest(f"{ruta.stem}:{e['pagina']}"):
                        self.assertIn(e["texto"], c["a"],
                                      f"la corrección de la página {c.get('pagina')} se lleva "
                                      f"puesta «{e['texto']}», que está declarada errata del "
                                      f"tomo impreso")


class TestDescripcionDeLaProcedencia(unittest.TestCase):
    """El `_descripcion` en disco tiene que ser el que el script escribe hoy.

    Lo escribe un `setdefault`, y ahí está la trampa: una vez que la clave existe no se
    vuelve a tocar nunca, por más corridas que se hagan. Así quedó un `_descripcion` con
    `Derivacion`, `publicacion` y `salio` sin tilde meses después de que el fuente dijera
    `Derivación`, `publicación` y `salió`. El archivo se lee y el fuente no, así que la
    versión vieja es la que alguien termina leyendo.
    """

    PROCEDENCIA = (RAIZ / "derecho" / "fuentes" / "jurisprudencia" / "ocr"
                   / "procedencia.json")

    def test_el_descripcion_en_disco_es_el_que_escribe_el_script(self):
        if not self.PROCEDENCIA.is_file():
            self.skipTest("todavía no hay OCR recuperado")
        en_disco = json.loads(self.PROCEDENCIA.read_text(encoding="utf-8"))["_descripcion"]
        fuente = HERRAMIENTA.read_text(encoding="utf-8")
        # Se comprueban las frases, no la cadena entera: en el fuente viene partida en
        # literales concatenados y unirlos acá sería reimplementar el parser.
        for frase in ("Texto recuperado por OCR local de PDF con la capa de texto arruinada.",
                      "Derivación, no descarga: no es publicación oficial.",
                      "sha256_pdf es el del PDF del que salió"):
            with self.subTest(frase[:40]):
                self.assertIn(frase.split(". ")[0][:60], en_disco,
                              "el `_descripcion` en disco quedó viejo: `setdefault` no lo "
                              "reescribe. Corregirlo en el .json, no sólo en el script")
                self.assertIn(frase[:60], fuente.replace('"\n                        "', ""))


if __name__ == "__main__":
    unittest.main(verbosity=1)
