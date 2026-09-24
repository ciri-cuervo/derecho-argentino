#!/usr/bin/env python3
"""Las calculadoras deterministas y sus datos: liquidación, plazos, intereses, honorarios y UMA.

Salió de `test_scripts.py` al partirlo: el original llegó a 6149 renglones, tres veces el corte de
`Read`. Lo compartido está en `_comun_tests.py`, y el porqué del corte también.

    python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
"""
import json
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
from _comun_tests import RAIZ_DEL_CHECKOUT, load_tests, sin_color as _sin_color


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
class TestVentanaCautelarDeLa27802(unittest.TestCase):
    """El aviso que `laboral.md` 5.1 manda emitir cuando el acto extintivo cae entre el
    30/03/2026 y el 23/04/2026, que es la ventana en la que 82 artículos de la Ley 27.802
    estuvieron suspendidos por la cautelar del JNT N°63.

    **Es la fila simétrica de la del DNU 70/2023**, y faltaba: el módulo instruía el marcador y
    el script liquidaba bajo la 27.802 sin decir una palabra del estado cautelar. El mecanismo
    ya estaba escrito para el otro tramo, así que el hueco no se veía leyendo el código — se ve
    corriendo una extinción de abril de 2026 y contando los marcadores que salen.

    La ventana **no es un tramo**: adentro rige la 27.802 igual, y lo que se desconoce es si el
    artículo aplicado estaba entre los suspendidos. Por eso es un marcador y no otra fila de
    `TRAMOS`.

    MUTACIÓN que lo comprueba: borrar el `if VENTANA_CAUTELAR[0] <= extincion` de
    `liquidacion_lct.py` deja en rojo `test_el_acto_dentro_de_la_ventana_lo_dice`.
    """

    def _args(self, extincion):
        return type("A", (), dict(
            ingreso=date(2015, 3, 10), extincion=extincion,
            mejor_remuneracion=Decimal("1000000"), remuneracion_ultimo_mes=None,
            tope_245=Decimal("2000000"), dias_vacaciones_gozadas=Decimal("0"),
            periodo_prueba=False, preaviso_otorgado=False, empleador="privado"))

    def _hay(self, extincion):
        r = liq.liquidar(self._args(extincion))
        return any("ventana cautelar" in m for m in r.marcadores)

    def test_el_acto_dentro_de_la_ventana_lo_dice(self):
        for f in (date(2026, 3, 30), date(2026, 4, 10), date(2026, 4, 23)):
            with self.subTest(f):
                self.assertTrue(self._hay(f), f"{f} cae en la ventana y no emitió el marcador")

    def test_los_bordes_de_afuera_no_lo_emiten(self):
        """Un día antes y un día después. Sin esto, un `>=` mal puesto pasaría igual."""
        for f in (date(2026, 3, 29), date(2026, 4, 24), date(2026, 5, 10)):
            with self.subTest(f):
                self.assertFalse(self._hay(f), f"{f} está fuera de la ventana y la nombró")

    def test_la_ventana_es_la_que_dice_el_modulo(self):
        """Las dos fechas están escritas en dos lados —el script y `laboral.md` 5.1— y esto es
        lo que impide que se separen."""
        modulo = (Path(__file__).resolve().parents[1] / "references" / "laboral.md").read_text(
            encoding="utf-8")
        self.assertIn("del 30/03/2026 al 23/04/2026", modulo)
        self.assertEqual(liq.VENTANA_CAUTELAR, (date(2026, 3, 30), date(2026, 4, 23)))
class TestSingularYPluralEnLaPieza(unittest.TestCase):
    """«1 años y 1 meses» salía impreso en una liquidación, que es una pieza que se entrega.

    MUTACIÓN que lo comprueba: volver `plural()` a `f"{n} {singular}s"` deja en rojo
    `test_un_anio_y_un_mes`.
    """

    def test_un_anio_y_un_mes(self):
        self.assertEqual(liq.plural(1, "año"), "1 año")
        self.assertEqual(liq.plural(1, "mes", "meses"), "1 mes")

    def test_el_plural_sigue_siendo_plural(self):
        self.assertEqual(liq.plural(0, "año"), "0 años")
        self.assertEqual(liq.plural(9, "año"), "9 años")
        self.assertEqual(liq.plural(2, "mes", "meses"), "2 meses")
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
        """El instrumento apagado no puede reportar OK.

        **Se mide contra un árbol de mentira y no contra el repositorio.** La versión anterior
        leía el archivo vivo y se apoyaba en que estuviera sin cargar: cuando la serie se cargó
        —22 vigencias leídas de las resoluciones de la SGA el 18/09/2026— el test se puso rojo
        por una mejora. Un control atado a que el corpus esté sucio se rompe cuando el
        repositorio avanza, y la salida obvia entonces es apagarlo.
        """
        import estado
        vacio = self._repo("")
        bloques = {b["bloque"]: b for b in estado.revisar(pathlib.Path(vacio))}
        self.assertIn("UMA", bloques, "estado.py no reporta la serie de la UMA")
        self.assertEqual(bloques["UMA"]["estado"], "FALTA",
                         "la serie está vacía y estado.py no la reportó FALTA")

    def test_estado_da_verde_cuando_la_serie_esta(self):
        """El otro lado del mismo control: si con valores siguiera diciendo FALTA, el bloque
        estaría clavado y no mediría nada."""
        import estado
        con = self._repo("2026-07-01,104220,Res. SGA 1930/2026,\n")
        bloques = {b["bloque"]: b for b in estado.revisar(pathlib.Path(con))}
        self.assertNotEqual(bloques["UMA"]["estado"], "FALTA",
                            "con la serie cargada sigue reportando FALTA")
class TestLasDosUMANoSeMezclan(unittest.TestCase):
    """Son dos unidades de dos leyes distintas, y confundirlas devuelve un número **oficial,
    vigente y de otra ley** — que es la peor clase de error, porque se verifica y da bien.

    | | Ley 5.134 CABA, art. 20 | Ley 27.423 nacional, art. 19 |
    | --- | --- | --- |
    | Porcentaje | 1,5% | 3% |
    | Base | remuneración TOTAL de un juez de la Ciudad | BÁSICA de un juez federal |
    | La fija | Consejo de la Magistratura de CABA | CSJN |

    Por eso son dos scripts y dos archivos, y no una bandera: **nombrar la jurisdicción es
    obligatorio por construcción**, igual que la skill pregunta el fuero en vez de suponerlo.

    Y hay una asimetría que el diseño respeta: la consulta oficial porteña publica **un solo
    valor**, el vigente, así que la serie histórica no se reconstruye desde el organismo que la
    fija. Plantarse antes de la primera vigencia es acá el caso frecuente, no el raro.

    MUTACIÓN que lo comprueba: apuntar `uma_caba.ARCHIVO` a `uma-csjn.csv` deja en rojo
    `test_cada_script_lee_su_propio_archivo`, que es lo que pasaría al unificarlos por descuido.
    """

    def setUp(self):
        import uma_caba, uma_csjn
        self.caba, self.csjn = uma_caba, uma_csjn

    def test_cada_script_lee_su_propio_archivo(self):
        self.assertEqual(self.caba.ARCHIVO, "uma-caba.csv")
        self.assertEqual(self.csjn.ARCHIVO, "uma-csjn.csv")
        self.assertNotEqual(self.caba.ARCHIVO, self.csjn.ARCHIVO)

    def test_los_dos_valores_del_arbol_real_son_distintos(self):
        """Sobre los archivos vivos: si alguien copiara uno sobre el otro, esto lo ve."""
        raiz = RAIZ_DEL_CHECKOUT
        a, _, m1 = self.caba.uma_del_repo(str(raiz))
        b, _, m2 = self.csjn.uma_del_repo(str(raiz))
        self.assertIsNotNone(a, m1)
        self.assertIsNotNone(b, m2)
        self.assertNotEqual(a, b, "las dos series traen el mismo valor: se cruzaron")

    def test_la_porteña_no_extrapola_hacia_atras(self):
        """El caso frecuente acá, no el raro: sólo hay valor desde la primera vigencia."""
        from datetime import date as _d
        valor, _fila, motivo = self.caba.uma_a_fecha(_d(2020, 1, 1), str(RAIZ_DEL_CHECKOUT))
        self.assertIsNone(valor, "extrapoló hacia atrás sobre un mínimo legal")
        self.assertIn("no se extrapola", motivo)

    def test_la_ley_5134_no_tiene_la_regla_del_art_51(self):
        """El motivo por el que la conversión existe es OTRO, y el docstring lo afirma.

        Medido contra el texto: los dos «bajo pena de nulidad» de la Ley 5.134 son el art. 16
        —fundar la regulación citando la norma— y la integración de intereses a la base. No hay
        obligación de expresar la regulación en pesos Y en UMA, que es lo que manda el art. 51
        nacional. Si algún día la hubiera, este test cae y el docstring hay que reescribirlo.
        """
        ley = (RAIZ_DEL_CHECKOUT / "derecho" / "fuentes" / "normas"
               / "caba-ley-5134.txt").read_text(encoding="utf-8")
        self.assertNotIn("moneda de curso legal", ley)
        self.assertEqual(ley.count("bajo pena de nulidad"), 2,
                         "cambió el texto de la Ley 5.134: revisar el docstring de uma_caba.py")
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


class TestLosEstatutosNoSeLiquidanComoLCT(unittest.TestCase):
    """Casas particulares, construcción, viajantes y encargados de edificio tienen estatuto
    propio (`laboral.md` 5.17 quinquies y sexies), y el script liquida la LCT: sin el corte,
    devuelve preaviso, integración y art. 245 con aspecto de correctos para una relación que
    no los tiene. Es la misma falla que `TestAmbitoDeLaLCT` y el mismo remedio.

    MUTACIÓN que lo comprueba: dejar `REGIMEN` con todos los valores en `None` pone en rojo a
    `test_cada_estatuto_corta_y_no_liquida`.
    """

    GUION = Path(__file__).parent / "liquidacion_lct.py"
    BASE = ["--ingreso", "2024-08-15", "--extincion", "2026-08-14",
            "--mejor-remuneracion", "1000000", "--tope-245", "800000", "--empleador", "privado"]
    NORMA = {"casas-particulares": "Ley 26.844", "construccion": "Ley 22.250",
             "viajantes": "Ley 14.546", "encargados": "Ley 12.981"}

    def _correr(self, *extra):
        return subprocess.run([sys.executable, str(self.GUION), *self.BASE, *extra],
                              capture_output=True, text=True, encoding="utf-8")

    def test_cada_estatuto_corta_y_no_liquida(self):
        sys.path.insert(0, str(Path(__file__).parent))
        import liquidacion_lct as liq
        self.assertEqual(set(self.NORMA), {k for k, v in liq.REGIMEN.items() if v},
                         "los estatutos que cortan no son los de laboral.md 5.17")
        for regimen, norma in self.NORMA.items():
            with self.subTest(regimen):
                r = self._correr("--regimen", regimen)
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertIn("[ARG SIN NORMA:", r.stdout)
                self.assertIn(norma, r.stdout)
                self.assertNotIn("TOTAL", r.stdout)
                j = self._correr("--regimen", regimen, "--json")
                self.assertEqual(j.returncode, 2)
                self.assertIsNone(json.loads(j.stdout)["total"])

    def test_la_lct_liquida_sin_el_marcador_de_regimen(self):
        r = self._correr("--regimen", "lct")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("TOTAL", r.stdout)
        self.assertNotIn("régimen de la relación", r.stdout)

    def test_sin_el_dato_liquida_pero_lo_dice_con_marcador(self):
        r = self._correr()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[VACÍO PROBATORIO: régimen de la relación", r.stdout)

    def test_el_intake_lo_pide_como_dato_que_bloquea(self):
        intake = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "intake.md").read_text(encoding="utf-8")
        bloque = re.search(r"## Laboral · liquidación.*?\n(?=## )", intake, re.S)
        bloquean = bloque.group(0).split("**Se marcan y no bloquean:**")[0]
        for norma in self.NORMA.values():
            self.assertIn(norma, bloquean, f"intake.md no pide el dato que decide la {norma}")
        self.assertIn("--regimen", bloquean)


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
