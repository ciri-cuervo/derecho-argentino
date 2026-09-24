#!/usr/bin/env python3
"""La capa offline: manifiesto, procedencia, OCR, series y la identidad de cada documento.

Salió de `test_scripts.py` al partirlo: el original llegó a 6149 renglones, tres veces el corte de
`Read`. Lo compartido está en `_comun_tests.py`, y el porqué del corte también.

    python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _comun_tests import RAIZ_DEL_CHECKOUT, load_tests


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
# Una serie declarada vacía: el nombre del csv y, después, la afirmación. Se cuenta sólo si
# NO está subordinada a una condición — «si la serie está vacía el script se planta» describe
# qué hace el script, no el estado del disco. Ese es el límite conocido de la medida y lo
# ejercita `test_no_confunde_una_condicional_con_una_afirmacion`.
VACIO = re.compile(r"(?P<archivo>[\w-]+\.csv)(?P<medio>[^.\n]{0,120}?)"
                   r"est[áa] (?:vací[oa]|sin valores)")
CONDICION = re.compile(r"(?:^|[\s(«—-])(?i:si|mientras|cuando|en cuanto|hasta que)\s")


def _series_declaradas_vacias(texto: str) -> set:
    vacias = set()
    for m in VACIO.finditer(texto):
        oracion = texto[max(0, texto.rfind(".", 0, m.start()) + 1):m.end()]
        if not CONDICION.search(oracion):
            vacias.add(m.group("archivo"))
    return vacias


class TestLoQueLaProsaAfirmaDeLaSerie(unittest.TestCase):
    """Decir que una serie está vacía es una afirmación sobre el disco, y se vence sola: la
    serie se carga y el texto se queda. Es peor que una cifra vieja, porque no informa de menos
    sino que **niega el dato que hay**: con veintidós vigencias cargadas, `honorarios-nacional.md`
    y `/derecho:honorarios` decían en cuatro lugares que `uma-csjn.csv` estaba vacío, el marcador
    enlatado del comando lo afirmaba también, y la skill se negaba a regular en la justicia
    nacional teniendo el valor a un comando de distancia. Un marcador que miente sobre la propia
    base es peor que no emitirlo.

    Mide los dos archivos que viajan en el plugin y que el runtime lee: `references/` y
    `commands/`.

    MUTACIÓN que lo comprueba: devolverle a cualquiera de esos textos «uma-csjn.csv está sin
    valores» y este test falla nombrando el archivo y las filas que tiene.
    """

    def test_ninguna_prosa_declara_vacia_una_serie_cargada(self):
        import estado
        raiz = RAIZ_DEL_CHECKOUT
        datos = raiz / "derecho" / "fuentes" / "datos"
        carpetas = (raiz / "derecho" / "skills" / "derecho-argentino" / "references",
                    raiz / "derecho" / "commands")
        for carpeta in carpetas:
            for md in sorted(carpeta.glob("*.md")):
                for nombre in _series_declaradas_vacias(md.read_text(encoding="utf-8")):
                    serie = datos / nombre
                    if not serie.is_file():
                        continue
                    with self.subTest(f"{md.name} -> {nombre}"):
                        _, filas = estado._ultima_fila_csv(serie)
                        self.assertEqual(filas, 0,
                                         f"{md.name} dice que {nombre} está vacío y tiene "
                                         f"{filas} filas cargadas")

    def test_no_confunde_una_condicional_con_una_afirmacion(self):
        """El caso conocido que la medida no puede errar: el texto que describe qué hace el
        script cuando la serie está vacía no afirma que lo esté."""
        self.assertEqual(_series_declaradas_vacias(
            "Si la serie de uma-csjn.csv está vacía el script se planta."), set())
        self.assertEqual(_series_declaradas_vacias(
            "El archivo uma-csjn.csv está sin valores."), {"uma-csjn.csv"})


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
