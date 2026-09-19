#!/usr/bin/env python3
"""El descargador de normas y su procedencia. Vive aparte porque es una sola clase grande.

Salió de `test_scripts.py` al partirlo: el original llegó a 6149 renglones, tres veces el corte de
`Read`. Lo compartido está en `_comun_tests.py`, y el porqué del corte también.

    python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _comun_tests import RAIZ_DEL_CHECKOUT, load_tests


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
