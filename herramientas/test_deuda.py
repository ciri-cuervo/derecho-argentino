#!/usr/bin/env python3
"""Tests del detector de reclamos de faltante vencidos. Sin dependencias externas.

    python3 herramientas/test_deuda.py

El detector cruza los renglones que reclaman un faltante contra el catálogo de `normas.json`,
y reporta el que nombra una norma que SÍ está bajada. Lo que se vigila acá es lo que puede
fallar en silencio:

- que el árbol real no tenga reclamos nuevos sin revisar, que es para lo que existe;
- que NO infiera el número de la prosa, que es el camino ya medido y descartado en
  `docs/PENDIENTES.md`: acá el número sale del catálogo;
- que una norma bajada dispare y una sin bajar no;
- que el cruce llegue al párrafo y no muera en el renglón, que es por donde se escapó un
  reclamo falso de verdad;
- que un fallo bajado dispare por su carátula, que es la segunda colección que el repositorio
  cataloga y contra la que el reclamo no se cruzaba.

La prosa de prueba es INVENTADA y el catálogo se arma en un directorio temporal.
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTA = RAIZ / "herramientas" / "deuda_vencida.py"


def cargar():
    spec = importlib.util.spec_from_file_location("deuda_vencida", HERRAMIENTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class TestElArbolReal(unittest.TestCase):
    def test_no_hay_reclamos_nuevos_sin_revisar(self):
        """Lo que el detector existe para impedir: un reclamo que la carpeta ya desmiente.

        Mutación que lo comprueba: escribir en cualquier `.md` alcanzado un renglón que diga
        que una norma bajada «no está cargada» lo deja en rojo.
        """
        dv = cargar()
        sobre, revisados = dv._veredictos.cargar(dv.BASE, "reclamos", vacio=[])
        nuevos = [c for c in dv.candidatos() if c not in set(revisados)]
        self.assertEqual(nuevos, [], "reclamos de faltante sin revisar: " + ", ".join(nuevos[:6]))


class TestComoDecideUnCandidato(unittest.TestCase):
    """El número sale del CATÁLOGO, no de la prosa. Inferirlo está medido y descartado."""

    def _arbol(self, titulo: str, bajada: bool, renglon: str):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, d, True)
        normas = d / "derecho" / "fuentes" / "normas"
        normas.mkdir(parents=True)
        (normas / "normas.json").write_text(
            json.dumps({"verificado": "2026-09-17",
                        "normas": [{"slug": "ley-99999", "titulo": titulo}]}, ensure_ascii=False),
            encoding="utf-8")
        if bajada:
            (normas / "ley-99999.txt").write_text("texto\n", encoding="utf-8")
        (d / "modulo.md").write_text(renglon + "\n", encoding="utf-8")
        dv = cargar()
        dv.RAIZ, dv.NORMAS = d, normas
        return dv

    def test_una_norma_bajada_dispara(self):
        dv = self._arbol("Ley 99.999 - de prueba", True,
                         "La Ley 99.999 no está cargada en `fuentes/`.")
        self.assertEqual([c.rsplit(":", 2)[1] for c in dv.candidatos()], ["ley-99999"])

    def test_una_norma_SIN_bajar_no_dispara(self):
        """El reclamo es cierto: no hay nada que corregir y no debe aparecer."""
        dv = self._arbol("Ley 99.999 - de prueba", False,
                         "La Ley 99.999 no está cargada en `fuentes/`.")
        self.assertEqual(dv.candidatos(), [])

    def test_sin_reclamo_no_dispara(self):
        """Nombrar una norma bajada no es reclamar que falte."""
        dv = self._arbol("Ley 99.999 - de prueba", True,
                         "La Ley 99.999 rige el caso y está bajada.")
        self.assertEqual(dv.candidatos(), [])

    def test_un_numero_que_el_catalogo_no_declara_se_ignora(self):
        """La medida no adivina: si el número no está en normas.json, no hay candidato.

        Inferir el número de la prosa saca «155» de «1558/2001»; acá sale del catálogo.
        """
        dv = self._arbol("Ley 99.999 - de prueba", True,
                         "El Decreto 1558/2001 no está cargado en `fuentes/`.")
        self.assertEqual(dv.candidatos(), [])


class TestLaClaveNoDependeDeLaPosicion(unittest.TestCase):
    """Un reclamo se identifica por lo que DICE, no por en qué renglón está.

    Con el número de renglón en la clave, agregar una fila más arriba reabre todo lo ya leído y
    la línea de base se vuelve ruido — la alarma que suena siempre, por edición ajena.

    Mutación que lo comprueba: volver a meter el número de renglón en la clave de `candidatos()`
    deja en rojo a `test_mover_el_reclamo_de_renglon_no_lo_reabre`.
    """

    def test_la_huella_ignora_el_espaciado_pero_no_el_texto(self):
        dv = cargar()
        self.assertEqual(dv.huella("La Ley 99.999  no   está"), dv.huella("La Ley 99.999 no está"))
        self.assertNotEqual(dv.huella("La Ley 99.999 no está"), dv.huella("La Ley 99.998 no está"))

    def test_mover_el_reclamo_de_renglon_no_lo_reabre(self):
        import json, shutil, tempfile
        from pathlib import Path as P
        d = P(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        normas = d / "derecho" / "fuentes" / "normas"
        normas.mkdir(parents=True)
        (normas / "normas.json").write_text(json.dumps(
            {"verificado": "2026-09-17", "normas": [{"slug": "ley-99999", "titulo": "Ley 99.999 - de prueba"}]},
            ensure_ascii=False), encoding="utf-8")
        (normas / "ley-99999.txt").write_text("texto\n", encoding="utf-8")
        reclamo = "La Ley 99.999 no está cargada en `fuentes/`.\n"
        modulo = d / "modulo.md"
        dv = cargar()
        dv.RAIZ, dv.NORMAS = d, normas
        modulo.write_text(reclamo, encoding="utf-8")
        antes = dv.candidatos()
        modulo.write_text("Una línea nueva arriba.\n\n" + reclamo, encoding="utf-8")
        self.assertEqual(dv.candidatos(), antes,
                         "el reclamo se reabrió por haberse corrido de renglón")


class TestElAlcanceDelCruce(unittest.TestCase):
    """El reclamo y el número de su norma se separan al cortar el renglón, y ahí se escapaba.

    Mutación que lo comprueba, y que ya ocurrió sola en el árbol: la rúbrica de
    `penal-juvenil-pba-preventiva-y-organo` decía que la Ley 13.298 «no está cargada» con el
    número en el renglón de arriba, y `pba-ley-13298.txt` estaba bajada. Reponer ese renglón
    deja en rojo a `TestElArbolReal`; con el cruce acotado al renglón, no lo dejaba.
    """

    def _arbol(self, texto: str):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, d, True)
        normas = d / "derecho" / "fuentes" / "normas"
        normas.mkdir(parents=True)
        (normas / "normas.json").write_text(
            json.dumps({"verificado": "2026-09-17",
                        "normas": [{"slug": "ley-99999", "titulo": "Ley 99.999 - de prueba"}]},
                       ensure_ascii=False), encoding="utf-8")
        (normas / "ley-99999.txt").write_text("texto\n", encoding="utf-8")
        (d / "modulo.md").write_text(texto, encoding="utf-8")
        dv = cargar()
        dv.RAIZ, dv.NORMAS = d, normas
        return dv

    def test_el_numero_en_el_renglon_de_arriba_dispara(self):
        dv = self._arbol("El sistema se apoya en la Ley 99.999, que\nno está cargada en `fuentes/`.\n")
        self.assertEqual([c.rsplit(":", 2)[1] for c in dv.candidatos()], ["ley-99999"])

    def test_un_blanco_en_el_medio_separa(self):
        """Dos párrafos no se leen juntos: si no, el cruce alcanza a media página."""
        dv = self._arbol("Rige la Ley 99.999.\n\nLa ley arancelaria local no está cargada.\n")
        self.assertEqual(dv.candidatos(), [])

    def test_dos_filas_de_tabla_no_se_mezclan(self):
        """Unida entera, un número de una fila se cruzaría contra el reclamo de otra."""
        dv = self._arbol("| a | Ley 99.999 bajada |\n| b | la serie no está cargada |\n")
        self.assertEqual(dv.candidatos(), [])

    def test_dos_items_de_lista_no_se_mezclan(self):
        dv = self._arbol("- Rige la Ley 99.999.\n- La ley local no está cargada.\n")
        self.assertEqual(dv.candidatos(), [])

    def test_la_huella_es_del_renglon_y_no_de_la_unidad(self):
        """Con la unidad en la huella, editar el renglón de al lado reabre un reclamo intacto."""
        dv = self._arbol("Se apoya en la Ley 99.999, que\nno está cargada en `fuentes/`.\n")
        antes = dv.candidatos()
        (dv.RAIZ / "modulo.md").write_text(
            "Se apoya en la Ley 99.999 -sancionada en 1999-, que\nno está cargada en `fuentes/`.\n",
            encoding="utf-8")
        self.assertEqual(dv.candidatos(), antes,
                         "el reclamo se reabrió por una edición del renglón vecino")


class TestLoQueElControlNoMira(unittest.TestCase):
    """Una medida que saltea en silencio reporta verde con el instrumento apagado.

    Mutación que lo comprueba: hacer que `sin_cruzar()` devuelva siempre `[]` deja en rojo a
    `test_un_reclamo_sin_norma_se_informa`.
    """

    def _arbol(self, texto: str):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, d, True)
        normas = d / "derecho" / "fuentes" / "normas"
        normas.mkdir(parents=True)
        (normas / "normas.json").write_text(
            json.dumps({"verificado": "2026-09-17", "normas": []}, ensure_ascii=False),
            encoding="utf-8")
        (d / "modulo.md").write_text(texto, encoding="utf-8")
        dv = cargar()
        dv.RAIZ, dv.NORMAS = d, normas
        return dv

    def test_un_reclamo_sin_norma_se_informa(self):
        dv = self._arbol("Su ley arancelaria local no está cargada.\n")
        self.assertEqual(dv.sin_cruzar(), ["modulo.md:1"])

    def test_un_reclamo_con_norma_no_se_informa_como_ciego(self):
        dv = self._arbol("La Ley 99.999 no está cargada.\n")
        self.assertEqual(dv.sin_cruzar(), [])

    def test_la_frase_dice_el_numero_y_no_lo_esconde(self):
        dv = cargar()
        self.assertIn("2", dv.ciego_dice(["a.md:1", "b.md:2"]))
        self.assertIn("ningún", dv.ciego_dice([]))

    def test_el_arbol_real_informa_su_punto_ciego(self):
        """No fija una cifra -baja cuando se cruza más-: exige que la salida lo diga."""
        dv = cargar()
        self.assertNotIn("--sin-cruzar", dv.ciego_dice([]))
        if dv.sin_cruzar():
            self.assertIn("--sin-cruzar", dv.ciego_dice(dv.sin_cruzar()))


class TestElCruceContraLosFallos(unittest.TestCase):
    """La segunda colección catalogada. Un reclamo dice «X no está bajado» y X se bajó.

    Mutación que lo comprueba: `test_un_fallo_que_se_baja_reabre_el_reclamo` simula el día en
    que alguien baja "Rayford" -hoy ausente, y `penal.md` dice que falta- y exige que aparezca
    un candidato nuevo. Sacar el cruce de `_reclamos()` lo deja en rojo.

    Y hay un límite que **no** se calibra y por eso se declara: dos fallos con el mismo
    apellido no se separan. En `fallos-csjn.md` hay dos "Bianchi", el penal bajado y el de
    peaje no, y el cruce los ve iguales.
    """

    def _arbol(self, texto: str, bajados: list[str], catalogo: list[tuple[str, str]]):
        import shutil
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        normas = d / "derecho" / "fuentes" / "normas"
        juris = d / "derecho" / "fuentes" / "jurisprudencia"
        normas.mkdir(parents=True)
        juris.mkdir(parents=True)
        (normas / "normas.json").write_text(
            json.dumps({"verificado": "2026-09-17", "normas": []}, ensure_ascii=False),
            encoding="utf-8")
        (juris / "fallos.json").write_text(json.dumps(
            {"fallos": [{"slug": s, "caratula": c} for s, c in catalogo]}, ensure_ascii=False),
            encoding="utf-8")
        for s in bajados:
            (juris / f"{s}.pdf").write_text("pdf\n", encoding="utf-8")
        (d / "modulo.md").write_text(texto, encoding="utf-8")
        dv = cargar()
        dv.RAIZ, dv.NORMAS, dv.JURIS = d, normas, juris
        return dv

    CATALOGO = [("csjn-rayford", "RAYFORD REGINALD Y OTROS s/ROBO"),
                ("csjn-quaranta", "QUARANTA JOSÉ CARLOS s/INF. LEY 23.737")]
    RECLAMO = '**"Rayford" no está bajado**; se cita porque "Quaranta" lo transcribe.\n'

    def test_un_fallo_bajado_dispara_por_su_caratula(self):
        dv = self._arbol(self.RECLAMO, ["csjn-quaranta"], self.CATALOGO)
        self.assertEqual([c.rsplit(":", 2)[1] for c in dv.candidatos()], ["csjn-quaranta"])

    def test_un_fallo_SIN_bajar_no_dispara(self):
        """El reclamo es cierto mientras el documento no esté: no hay nada que corregir."""
        dv = self._arbol('**"Rayford" no está bajado**.\n', [], self.CATALOGO)
        self.assertEqual(dv.candidatos(), [])

    def test_un_fallo_que_se_baja_reabre_el_reclamo(self):
        """El día que alguien baja "Rayford", el renglón que dice que falta tiene que saltar."""
        dv = self._arbol(self.RECLAMO, ["csjn-quaranta"], self.CATALOGO)
        antes = dv.candidatos()
        (dv.JURIS / "csjn-rayford.pdf").write_text("pdf\n", encoding="utf-8")
        nuevos = set(dv.candidatos()) - set(antes)
        self.assertEqual([c.rsplit(":", 2)[1] for c in nuevos], ["csjn-rayford"])

    def test_estar_en_el_catalogo_no_alcanza_si_el_documento_no_esta(self):
        """Un fallo declarado y sin documento es lo que el reclamo dice: sigue faltando."""
        dv = self._arbol(self.RECLAMO, [], self.CATALOGO)
        self.assertEqual(dv.candidatos(), [])

    def test_un_apellido_sin_comillas_no_dispara(self):
        """El repositorio cita los fallos entrecomillados; sin comillas es prosa cualquiera."""
        dv = self._arbol("El caso Quaranta no está bajado.\n", ["csjn-quaranta"], self.CATALOGO)
        self.assertEqual(dv.candidatos(), [])

    def test_una_caratula_anonimizada_no_se_indexa(self):
        """Punto ciego declarado: sin apellido no hay clave, y tampoco se las cita así."""
        dv = self._arbol('"E." no está bajado.\n', ["scba-e-m-r"],
                         [("scba-e-m-r", "E., M. R. c/ L., M. F. s/ compensación")])
        self.assertEqual(dv.jurisprudencia(), {})

    def test_los_diacriticos_los_resuelve_pelado_y_no_la_clase_de_letras(self):
        """La `Ü` del regex fue un error de este repositorio. Acá el acento se pela antes.

        Mutación que lo comprueba: sacar `pelado()` de `jurisprudencia()` o de `nombrados()`
        deja en rojo este test, porque los dos lados dejan de encontrarse.
        """
        dv = cargar()
        for nombre, clave in [("AGÜERO", "AGUERO"), ("GÖTTE", "GOTTE"),
                              ("ÁLVAREZ", "ALVAREZ"), ("PEÑA", "PENA")]:
            self.assertEqual(dv.APELLIDO.match(dv.pelado(nombre)).group(0), clave)
            self.assertEqual(dv.nombrados(f'"{nombre.title()}" no está bajado'), [clave])

    def test_un_acento_en_la_caratula_encuentra_la_cita_sin_acento(self):
        """Los dos lados se pelan, así que da igual cómo esté escrito cada uno."""
        dv = self._arbol('"Aguero" no está bajado.\n', ["csjn-aguero"],
                         [("csjn-aguero", "AGÜERO, JUAN s/ recurso")])
        self.assertEqual([c.rsplit(":", 2)[1] for c in dv.candidatos()], ["csjn-aguero"])

    def test_un_apellido_compuesto_con_particula_corta_no_se_indexa(self):
        """Punto ciego declarado, no calibrado: el apellido es el primer token.

        Bajar el mínimo indexaría «DE» y «LA», que colisionan con media biblioteca. Hoy no hay
        ninguna carátula así en el catálogo, y este test fija que si aparece, no se cruza.
        """
        dv = self._arbol('"San Martín" no está bajado.\n', ["csjn-sanmartin"],
                         [("csjn-sanmartin", "SAN MARTÍN, PEDRO c/ ANSES")])
        self.assertEqual(dv.jurisprudencia(), {})

    def test_el_arbol_real_indexa_los_fallos_que_tiene(self):
        """Del producto no se concluye el proceso: que el índice exista no prueba que mire."""
        dv = cargar()
        idx = dv.jurisprudencia()
        self.assertIn("FLORES", idx)
        self.assertNotIn("RAYFORD", idx, "«Rayford» figura como bajado y el módulo dice que no")


if __name__ == "__main__":
    unittest.main()
