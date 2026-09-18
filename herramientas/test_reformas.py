#!/usr/bin/env python3
"""Tests del detector de reformas no leídas. Sin dependencias externas.

    python3 herramientas/test_reformas.py
"""
import json
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))

import reformas_no_leidas as detector

HERRAMIENTA = RAIZ / "herramientas" / "reformas_no_leidas.py"
REGISTRO = RAIZ / "herramientas" / "reformas-revisadas.json"


class TestExtraccionDeNotas(unittest.TestCase):
    """La nota de reforma vive al pie del artículo y hay que emparejar ley con SU fecha.

    InfoLEG escribe esa fecha de cuatro formas distintas, y no es una hipótesis: medido sobre
    los textos bajados en `derecho/fuentes/normas/`, hay 1.394 notas `dd/mm`, 785 `dd/m`, 704
    `d/m` y 113 `d/mm`. El detector tiene que leer las cuatro, así que las cuatro están acá.

    Ese directorio queda afuera de cualquier normalización de fechas del repositorio, porque es
    texto bajado y se coteja por hash: rellenar un cero ahí cambiaria el archivo respecto de su
    fuente. Estos fixtures lo imitan, así que tampoco se normalizan.
    """

    # (forma, texto del B.O., día y mes tal como los devuelve el regex)
    FORMAS = (("dd/mm", "B.O. 10/03/2025", "10", "03", "2025"),
              ("dd/m", "B.O. 14/4/2020", "14", "4", "2020"),
              ("d/m", "B.O. 3/8/2017", "3", "8", "2017"),
              ("d/mm", "B.O. 6/11/2009", "6", "11", "2009"))

    def test_empareja_la_ley_con_su_propia_fecha_en_las_cuatro_formas(self):
        from datetime import date
        for forma, bo, dia, mes, anio in self.FORMAS:
            nota = (f"(Artículo sustituido por art. 7° de la Ley N° 27.786 {bo}. Vigencia: "
                    f"a partir del día siguiente.)")
            with self.subTest(forma):
                self.assertEqual(detector.reformas_del_texto(nota),
                                 {"27786": date(int(anio), int(mes), int(dia))})

    def test_lee_el_estilo_de_la_provincia_que_no_trae_bo(self):
        """Los textos de PBA anotan «(Texto según Ley 14765)», sin B.O. y sin fecha.

        Exigir el B.O. dejaba afuera un tercio de las notas del corpus, y las dejaba afuera
        callado: las procesales bonaerenses y la LCT son las más anotadas a ese estilo. Una
        reforma que el detector no ve es una reforma que nadie va a leer.

        MUTACIÓN que lo demuestra: volver a exigir `B.O.` en `NOTA` tiene que vaciar este
        resultado.
        """
        self.assertEqual(detector.reformas_del_texto("(Texto según Ley 14765)"), {"14765": None})
        self.assertEqual(detector.reformas_del_texto("(Artículo derogado por Ley 13.634)"),
                         {"13634": None})

    def test_un_parentesis_que_no_nombra_ley_no_es_una_reforma(self):
        """El articulado remite todo el tiempo sin reformar nada."""
        self.assertEqual(detector.reformas_del_texto("(Texto según el criterio del tribunal)"), {})
        self.assertEqual(detector.reformas_del_texto("conforme la Ley 11.922 y modificatorias"), {},
                         "una remisión suelta, fuera de paréntesis, no es una nota de reforma")

    def test_no_cruza_una_ley_con_la_fecha_de_otra_nota(self):
        from datetime import date
        texto = ("(Artículo sustituido por art. 1° de la Ley N° 25.561 B.O. 7/1/2002).\n\n"
                 "(Artículo incorporado por art. 2° de la Ley N° 27.786 B.O. 10/03/2025.)")
        self.assertEqual(detector.reformas_del_texto(texto),
                         {"25561": date(2002, 1, 7), "27786": date(2025, 3, 10)})

    def test_una_fecha_imposible_no_rompe_la_corrida(self):
        # El script no adivina la fecha, pero tampoco pierde la reforma: la deja sin fechar.
        self.assertEqual(
            detector.reformas_del_texto("(Artículo sustituido por Ley N° 27.786 B.O. 31/02/2025)"),
            {"27786": None})

    def test_sin_fecha_ordena_por_numero_de_ley(self):
        """Dentro de una jurisdicción los números son secuenciales, así que el mayor es el más
        nuevo. Es una regla del sistema de numeración, no una estimación, y sólo se usa cuando
        la nota no trae fecha.
        """
        from datetime import date
        leyes = detector.reformas_del_texto(
            "(Texto según Ley 13772) ... (Texto según Ley 14765) ... (Texto según Ley 12061)")
        self.assertEqual(set(leyes), {"13772", "14765", "12061"})
        self.assertEqual(max(leyes, key=lambda l: (leyes[l] or date.min, int(l))), "14765")

    def test_una_fechada_le_gana_a_una_sin_fecha(self):
        """Si un texto mezcla los dos estilos, la que trae fecha manda sobre la que no."""
        from datetime import date
        leyes = detector.reformas_del_texto(
            "(Texto según Ley 15999) (Artículo sustituido por Ley N° 27.786 B.O. 10/03/2025)")
        self.assertEqual(max(leyes, key=lambda l: (leyes[l] or date.min, int(l))), "27786")


class TestUltimaReforma(unittest.TestCase):
    def test_se_queda_con_la_mas_reciente_de_cada_norma(self):
        hallados = detector.ultima_reforma_por_norma(desde=0)
        self.assertGreater(len(hallados), 20, "dejó de leer las notas de los consolidados")
        por_norma = {}
        for cuando, slug, _, _n in hallados:
            por_norma.setdefault(slug, set()).add(cuando)
        for slug, fechas in por_norma.items():
            with self.subTest(slug):
                self.assertEqual(len(fechas), 1, f"{slug} quedó con más de una fecha")

    def test_el_codigo_penal_llega_hasta_la_ley_27786(self):
        # Si el consolidado se rebaja a una versión anterior, esto lo dice.
        cp = [(c, l) for c, s, l, _ in detector.ultima_reforma_por_norma(desde=0)
              if s == "cp-11179"]
        self.assertEqual(cp, [(date(2025, 3, 10), "27786")],
                         "la clave va sin puntos: los dos estilos de nota la escriben "
                         "distinto y compararlas con punto perdía la mitad")

    def test_desde_filtra_por_anio(self):
        todas = detector.ultima_reforma_por_norma(desde=0)
        recientes = detector.ultima_reforma_por_norma(desde=2025)
        self.assertLess(len(recientes), len(todas))
        self.assertTrue(all(c and c.year >= 2025 for c, _, _, _ in recientes),
                        "`--desde` filtra por año, así que una reforma sin fecha "
                        "no puede colarse cuando se pide un año")


class TestRegistroDeVeredictos(unittest.TestCase):
    def test_no_quedan_candidatos_sin_veredicto(self):
        hecho = subprocess.run([sys.executable, str(HERRAMIENTA)], capture_output=True, text=True)
        self.assertEqual(hecho.returncode, 0,
                         "hay reformas recientes que ningún módulo nombra:\n" + hecho.stdout)

    def test_cada_veredicto_tiene_motivo_escrito(self):
        registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
        self.assertTrue(registro["reformas"])
        for clave, ficha in registro["reformas"].items():
            with self.subTest(clave):
                self.assertIn(":", clave, "la clave es 'slug:ley'")
                self.assertIn(ficha["veredicto"], ("no-toca-el-modulo", "absorbida"))
                self.assertGreater(len(ficha["motivo"]), 40,
                                   "un veredicto sin motivo es un silencio, no una decisión")


class TestCubreElArticulo(unittest.TestCase):
    """Lo que separa `art. 32 de la ley de tránsito` de `art. 32 del Código Fiscal`.

    El primer filtro -qué módulos nombran la norma- no alcanza: nombrar una ley una vez vuelve
    al módulo dueño de sus trescientos artículos. El que decide es éste.

    Mutaciones que lo comprueban, las dos corridas:
      · dejar que el bloque sea el párrafo entero sin separar las filas de tabla deja en rojo a
        `test_una_fila_de_tabla_no_contagia_a_la_de_al_lado`;
      · comparar contra el documento entero en vez del bloque deja en rojo a
        `test_la_ley_tiene_que_estar_en_el_mismo_bloque`.
    """

    def setUp(self):
        self.r = detector

    def test_la_ley_tiene_que_estar_en_el_mismo_bloque(self):
        cuerpo = ("La Ley 13.927 rige el tránsito en la Provincia.\n"
                  "\n"
                  "El art. 48 exige casco homologado.\n")
        self.assertFalse(self.r.cubre_el_articulo(cuerpo, "13927", "48"),
                         "la ley y el artículo están en bloques distintos: no cuenta")

    def test_en_el_mismo_bloque_cuenta(self):
        cuerpo = "El art. 48 de la Ley 13.927 exige casco homologado.\n"
        self.assertTrue(self.r.cubre_el_articulo(cuerpo, "13927", "48"))

    def test_una_fila_de_tabla_no_contagia_a_la_de_al_lado(self):
        """Una tabla no lleva líneas en blanco, así que sin separar filas se lee como un bloque.

        Es el caso real: `transito.md` figuraba cubriendo el art. 43 de la Ley 13.927 -que es
        una cuenta bancaria- por una fila que dice «Giros y rotondas».
        """
        cuerpo = ("| Falta | Ley | Sanción |\n"
                  "| --- | --- | --- |\n"
                  "| Casco | art. 16 Ley 13.927 | 300 a 1.000 |\n"
                  "| Giros y rotondas | art. 21 | art. 43 |\n")
        self.assertFalse(self.r.cubre_el_articulo(cuerpo, "13927", "43"),
                         "el art. 43 está en otra fila que la mención de la ley")
        self.assertTrue(self.r.cubre_el_articulo(cuerpo, "13927", "16"),
                        "el art. 16 y la ley están en la MISMA fila: sí cuenta")


class TestPisoPorJurisdiccion(unittest.TestCase):
    """Las dos numeraciones corren en paralelo y un piso único no filtra.

    Mutación: unificar el piso en 15.000 deja en rojo a `test_una_ley_nacional_vieja_no_pasa`,
    porque la Ley 23.890 es de 1990 y su número supera ese piso.
    """

    def setUp(self):
        self.r = detector

    def test_el_piso_bonaerense_es_mas_bajo_que_el_nacional(self):
        self.assertLess(self.r.PISO_SIN_FECHA["pba"], self.r.PISO_SIN_FECHA["nacional"])

    def test_una_ley_nacional_vieja_no_pasa(self):
        self.assertLess(23890, self.r.PISO_SIN_FECHA["nacional"],
                        "la Ley 23.890 es de 1990 y no puede contar como reforma reciente")

    def test_una_ley_bonaerense_reciente_si_pasa(self):
        self.assertGreaterEqual(15143, self.r.PISO_SIN_FECHA["pba"])


class TestElArbolRealPorArticulo(unittest.TestCase):
    def test_no_hay_articulo_cubierto_con_reforma_sin_leer(self):
        """Mutación: borrar un veredicto de `reformas-revisadas.json` lo deja en rojo."""
        r = detector
        _, revisadas = r._veredictos.cargar(r.REGISTRO, "reformas", vacio={})
        sin = [f"{c[0]}:{c[1]}:{c[2]}" for c in r.reformas_por_articulo(2024)
               if f"{c[0]}:{c[1]}:{c[2]}" not in revisadas]
        self.assertEqual(sin, [], "reformas por artículo sin veredicto: " + ", ".join(sin[:5]))


if __name__ == "__main__":
    unittest.main()
