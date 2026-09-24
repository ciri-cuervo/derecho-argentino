#!/usr/bin/env python3
"""Ortografía y codificación: lo que se muestra se acentúa, y lo que se compara no.

Salió de `test_scripts.py` al partirlo: el original llegó a 6149 renglones, tres veces el corte de
`Read`. Lo compartido está en `_comun_tests.py`, y el porqué del corte también.

    python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
"""
import ast
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _comun_tests import RAIZ_DEL_CHECKOUT, load_tests, sin_color as _sin_color


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
        if not re.search(r"[a-záéíóúüñ] [a-záéíóúüñ]", s, re.I):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
