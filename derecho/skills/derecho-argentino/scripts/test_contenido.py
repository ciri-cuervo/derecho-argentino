#!/usr/bin/env python3
"""El contenido de la skill: SKILL.md, los módulos, los marcadores, las remisiones y el ruteo.

Salió de `test_scripts.py` al partirlo: el original llegó a 6149 renglones, tres veces el corte de
`Read`. Lo compartido está en `_comun_tests.py`, y el porqué del corte también.

    python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
"""
import collections
import json
import os
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _comun_tests import RAIZ_DEL_CHECKOUT, LETRAS, MAYUSCULAS, load_tests


class TestLaSkillNoNombraLoQueNoSeInstala(unittest.TestCase):
    """Lo que el plugin distribuye es `derecho/`: `herramientas/`, `docs/`, `AGENTS.md`,
    `LICENCIAS.md` y `.github/` se quedan en el repositorio.

    Un módulo que nombra uno de esos manda al lector a una ruta que en su copia **no existe**, y
    el lector es el modelo: no se topa con un 404, completa el hueco. Pero el costo mayor no es
    ese. Esa prosa es el **diario del trabajo** —con qué comando se regenera un OCR, qué
    veredicto quedó anotado dónde, cuántas medidas se descartaron—, y vive adentro de archivos
    que se cargan en cada consulta. El lector de la skill paga contexto por leer cómo se
    mantiene el repositorio.

    **La regla es de destino, no de estilo:** la regla operativa se queda en el módulo, el cómo
    se llegó a ella va a `docs/AUDITORIAS.md`, que además está excluido del censo de cifras
    justamente por ser un registro fechado.

    Los `scripts/` quedan afuera del control: son código, y un comentario que nombra a sus dos
    hermanos —las tres declaraciones de zona horaria— explica un invariante que se lee al tocarlo.

    MUTACIÓN que lo comprueba: devolverle a `marcadores.md` el «el cotejo de
    `herramientas/verificar_respuesta.py` compara el nombre en forma plana» —hoy el script está
    adentro del plugin, pero la frase nombraba una ruta del repositorio—, que es de donde
    salió este control, lo deja en rojo.
    """

    #: Lo que existe en el repo y no en la copia instalada del plugin.
    FUERA = re.compile(r"herramientas/|docs/[A-Z]+\.md|\bAGENTS\.md\b|\bLICENCIAS\.md\b"
                       r"|\.github/|\.claude/rules/")

    def test_ningun_modulo_manda_a_una_ruta_del_repositorio(self):
        skill = RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
        archivos = [skill / "SKILL.md"] + sorted((skill / "references").glob("*.md"))
        rotas = []
        for a in archivos:
            for n, linea in enumerate(a.read_text(encoding="utf-8").splitlines(), 1):
                hallado = self.FUERA.search(linea)
                if hallado:
                    rotas.append(f"{a.name}:{n} nombra «{hallado.group(0)}»")
        self.assertGreater(len(archivos), 50, "no leyó los módulos: el control está apagado")
        self.assertEqual(rotas, [],
                         "la skill nombra rutas que el plugin instalado no trae:\n    "
                         + "\n    ".join(rotas))

    def test_el_patron_reconoce_lo_que_tiene_que_reconocer(self):
        """Instrumento encendido: si el patrón dejara de enganchar, la lista vacía de arriba
        significaría «no hay» cuando significa «no miré»."""
        for ejemplo in ("corre `herramientas/cifras.py`", "ver `docs/DESARROLLO.md`",
                        "lo dice AGENTS.md", "la licencia está en LICENCIAS.md",
                        "el workflow de .github/workflows/tests.yml",
                        "la regla de .claude/rules/prosa.md"):
            with self.subTest(ejemplo):
                self.assertIsNotNone(self.FUERA.search(ejemplo))
        for sano in ("ver `fuentes/normas/ley-27802.txt`", "`scripts/estado.py`",
                     "`references/laboral.md` 5.3", "en `kb/perfiles/laboral-CLAUDE.md`"):
            with self.subTest(sano):
                self.assertIsNone(self.FUERA.search(sano), "engancha una ruta que SÍ se instala")
class TestVocabularioDeMarcadores(unittest.TestCase):
    """Todo marcador que un módulo emita tiene que existir en `references/marcadores.md`.

    El marcador es la salida que el abogado copia al escrito, así que un nombre inventado no
    falla ruidosamente: sale igual y nadie lo reconoce. `marcadores.md` declara las dos listas
    —los canónicos en sus encabezados y los contraejemplos en la tabla "No usar"— y acá se
    acepta sólo lo que figure en una de las dos.
    """

    NOMBRE = re.compile(r"\[([" + MAYUSCULAS + "][" + MAYUSCULAS + r" \-]{3,})(?::|\])")
    # El mismo patrón pero tolerante a la caja: es el que detecta un marcador mal
    # capitalizado, y también necesita la diéresis o `[Verificar Antigüedad: ...]` pasa.
    CUALQUIERA = re.compile(r"\[([" + LETRAS + "][" + LETRAS + r" \-]{3,})(?::|\])")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.skill = raiz / "derecho" / "skills" / "derecho-argentino"
        vocabulario = (self.skill / "references" / "marcadores.md").read_text(encoding="utf-8")
        self.canonicos = set(re.findall(r"^### [A-D]\d+ · (.+)$", vocabulario, re.M))
        # Los contraejemplos que el propio vocabulario declara, para poder NOMBRARLOS al
        # explicar qué no usar sin que el test los tome por invención. Nombrar no es emitir:
        # ver `test_un_marcador_prohibido_no_se_puede_emitir`.
        self.declarados = set(re.findall(r"`\[([" + MAYUSCULAS + "][" + MAYUSCULAS + r" \-]{3,})[\]:]", vocabulario))

    def test_el_vocabulario_tiene_las_cuatro_series_completas(self):
        vocabulario = (self.skill / "references" / "marcadores.md").read_text(encoding="utf-8")
        series = re.findall(r"^### ([A-D])(\d+) ·", vocabulario, re.M)
        cuenta = {serie: max(int(n) for s, n in series if s == serie) for serie, _ in series}
        self.assertEqual(cuenta, {"A": 11, "B": 5, "C": 4, "D": 6})
        self.assertEqual(len(self.canonicos), 26)

    def _archivos(self):
        """SKILL.md, los módulos y TAMBIÉN los evals.

        Los evals quedaban afuera, y son justo donde vive la salida esperada: un marcador roto
        en un `resultado.md` no falla, ensenia la forma equivocada.
        """
        archivos = [self.skill / "SKILL.md"]
        archivos += [p for p in sorted((self.skill / "references").glob("*.md"))
                     if p.name != "marcadores.md"]
        archivos += sorted(self.skill.parent.parent.glob("evals/**/*.md"))
        return archivos

    def test_un_marcador_con_dieresis_no_escapa_al_control(self):
        """MUTACIÓN del alcance del propio control, y no de un archivo del repo.

        Las clases de letras estaban escritas tres veces a mano y a las tres les faltaba la Ü.
        Consecuencia: `[VERIFICAR ANTIGÜEDAD: ...]` no matcheaba el patrón, así que el marcador
        no era ni candidato y el control lo IGNORABA en silencio en vez de reclamarlo. No es
        hipotético: "antigüedad" con diéresis aparece 67 veces en el repositorio y es el núcleo
        del art. 245 LCT.

        Hoy las tres clases salen de MAYÚSCULAS y LETRAS, definidas una sola vez arriba.
        """
        inventado = "[VERIFICAR ANTIGÜEDAD: cómputo del art. 245 - aportar fecha de ingreso]"
        self.assertEqual(self.NOMBRE.findall(inventado), ["VERIFICAR ANTIGÜEDAD"],
                         "el patrón no ve un marcador con diéresis: se le escapa al control")
        self.assertNotIn("VERIFICAR ANTIGÜEDAD", self.canonicos | self.declarados,
                         "si algún día se declara, este fixture hay que cambiarlo")
        # Y la Ñ, que es el otro carácter que ya estaba y conviene fijar de paso.
        self.assertEqual(self.NOMBRE.findall("[VERIFICAR DISEÑO: x]"), ["VERIFICAR DISEÑO"])
        # Y el patrón tolerante a la caja, que usa LETRAS y no MAYÚSCULAS.
        self.assertEqual(self.CUALQUIERA.findall("[Verificar Antigüedad: x]"),
                         ["Verificar Antigüedad"])

    def test_ningun_marcador_perdio_las_mayusculas(self):
        """MUTACIÓN vivida: una corrección de acentos en masa convirtió
        `[VERIFICAR CRITERIO DEL FUERO:` en `[VERIFICAR Criterio DEL FUERO:` en dos evals, y
        esta suite no lo vio porque su regex solo aceptaba candidatos ya en mayúsculas: el
        marcador roto no era ni candidato. Ahora se mira cualquier nombre y, si en mayúsculas
        resulta ser un marcador canónico, tiene que estar escrito exactamente así.
        """
        for archivo in self._archivos():
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for nombre in self.CUALQUIERA.findall(linea):
                    nombre = nombre.strip()
                    if nombre.upper() not in self.canonicos or nombre == nombre.upper():
                        continue
                    with self.subTest(f"{archivo.name}:{numero} {nombre}"):
                        self.fail(f"{archivo.name}:{numero} escribe «{nombre}» y el marcador "
                                  f"canónico es «{nombre.upper()}»")

    #: Un marcador EMITIDO lleva su carga: `[NOMBRE: motivo]`. Nombrado va desnudo, `[NOMBRE]`.
    EMITIDO = re.compile(r"\[([" + MAYUSCULAS + "][" + MAYUSCULAS + r" \-]{3,}):")

    def test_un_marcador_prohibido_no_se_puede_emitir(self):
        """La tabla «No usar» de `marcadores.md` declara formas **prohibidas**, y el control las
        aceptaba en cualquier archivo: estaban en el mismo conjunto que los canónicos, así que
        servían de salvoconducto. La alarma sonaba por un nombre inventado y era sorda a los
        nueve nombres que el vocabulario prohíbe por su nombre — la falla peor, porque da verde.

        Lo que separa nombrar de emitir es la carga: `SKILL.md` y `marcadores.md` los nombran
        desnudos, entre backticks, para decir qué no usar; un módulo que lo emite le pone los dos
        puntos y el motivo. Esa es la forma que se prohíbe, y no hace falta lista de excepciones.

        MUTACIÓN que lo comprueba: devolver a `penal-leyes-especiales.md` su
        `[VERIFICAR RÉGIMEN APLICABLE: fecha del hecho contra el 05/09/2026 - ...]`, que es de
        donde salió este control, lo deja en rojo.
        """
        prohibidos = self.declarados - self.canonicos
        self.assertGreaterEqual(len(prohibidos), 5,
                                "no se leyó la tabla «No usar»: el control está apagado")
        self.assertIn("VERIFICAR RÉGIMEN APLICABLE", prohibidos,
                      "el fixture perdió su caso conocido: revisar la tabla «No usar»")
        emitidos = []
        for archivo in self._archivos():
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for nombre in self.EMITIDO.findall(linea):
                    if nombre.strip() in prohibidos:
                        emitidos.append(f"{archivo.name}:{numero} [{nombre.strip()}: ...]")
        self.assertEqual(emitidos, [],
                         "emiten un marcador que la tabla «No usar» de marcadores.md prohíbe:\n    "
                         + "\n    ".join(emitidos))

    def test_ningun_modulo_emite_un_marcador_inventado(self):
        archivos = self._archivos()
        for archivo in archivos:
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for nombre in self.NOMBRE.findall(linea):
                    nombre = nombre.strip()
                    with self.subTest(f"{archivo.name}:{numero} {nombre}"):
                        self.assertTrue(nombre in self.canonicos or nombre in self.declarados,
                                        f"{archivo.name}:{numero} emite un marcador que no está "
                                        f"en marcadores.md: [{nombre}]")
class TestCuentaDeEvals(unittest.TestCase):
    """Cuántos casos de verificación hay se afirma en `LICENCIAS.md`, y esa cifra se vence sola.

    Importa más que un conteo cualquiera: la sección 2 del mapa declara **cuáles** de los evals
    son capa 2 —los que venían del fork de origen— y cuántos se escribieron acá. Si el total se
    desactualiza, la resta que declara la autoría queda mal.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        # Un caso es una carpeta CON `caso.md`. `claude plugin eval` deja su salida en
        # `evals/results/`, que es una carpeta y no un caso: contarla corrompía la resta
        # de autoría de LICENCIAS.md con cada corrida.
        self.casos = [d for d in (raiz / "derecho" / "evals").iterdir()
                      if d.is_dir() and (d / "caso.md").is_file()]

    def test_licencias_declara_los_casos_que_hay(self):
        texto = (self.raiz / "LICENCIAS.md").read_text(encoding="utf-8")
        hallado = re.search(r"\*\*(\d+) casos\*\* de verificación", texto)
        self.assertIsNotNone(hallado, "LICENCIAS.md dejó de decir cuántos evals hay")
        self.assertEqual(int(hallado.group(1)), len(self.casos))

    def test_el_slug_del_encabezado_es_el_nombre_del_directorio(self):
        """El slug se escribe en el encabezado de `rubrica.md` y `resultado.md`, y ahí va en
        ASCII porque es el nombre de una carpeta.

        MUTACIÓN VIVIDA: una corrección de acentos por regla convirtió
        `familia-restitución-grave-riesgo-violencia` en `...-restitución-...` en cinco archivos,
        y ningún test lo vio. El slug identifica el caso: si el encabezado dice otro, el eval
        deja de poder cruzarse con su carpeta.
        """
        for caso in sorted(self.casos):
            for nombre in ("rubrica.md", "resultado.md", "caso.md"):
                f = caso / nombre
                if not f.is_file():
                    continue
                encabezado = next((l for l in f.read_text(encoding="utf-8").splitlines()
                                   if l.startswith("#")), "")
                if "·" not in encabezado:
                    continue
                declarado = encabezado.split("·")[-1].strip()
                # Solo cuando lo que sigue al · ES un slug. `caso.md` pone ahí el título en
                # prosa, y eso no tiene por que coincidir con el nombre de la carpeta.
                if " " in declarado or not re.fullmatch(r"[\w\-]+", declarado):
                    continue
                with self.subTest(f"{caso.name}/{nombre}"):
                    self.assertEqual(declarado, caso.name,
                                     "el encabezado no nombra el directorio del caso")

    def test_los_cuatro_de_capa_2_siguen_estando(self):
        """Si uno se renombra, la enumeración del mapa deja de identificar nada."""
        de_capa_2 = ("administrativo-caba-recursos-agotamiento-via",
                     "consumidor-dano-punitivo-prescripcion",
                     "consumidor-garantia-producto-defectuoso",
                     "consumidor-prepaga-aumento-dnu70")
        nombres = {d.name for d in self.casos}
        for caso in de_capa_2:
            with self.subTest(caso):
                self.assertIn(caso, nombres)
        texto = (self.raiz / "LICENCIAS.md").read_text(encoding="utf-8")
        for caso in de_capa_2:
            with self.subTest(f"declarado: {caso}"):
                self.assertIn(caso, texto, "LICENCIAS.md dejó de nombrarlo como capa 2")

    def test_cada_caso_trae_sus_tres_piezas(self):
        for caso in sorted(self.casos):
            with self.subTest(caso.name):
                for pieza in ("caso.md", "rubrica.md", "resultado.md"):
                    self.assertTrue((caso / pieza).is_file(), f"falta {pieza}")
class TestInventarioDeModelos(unittest.TestCase):
    """`modelos.md` existe para que los modelos se encuentren: si falta uno, no sirve.

    El conteo vive repetido en tres documentos, así que acá se mide contra el disco en vez
    de recordarlo.
    """

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.escritos = raiz / "derecho" / "kb" / "escritos"
        self.modelos = {f"kb/escritos/{p.relative_to(self.escritos).as_posix()}"
                        for d in self.escritos.rglob("modelos") if d.is_dir()
                        for p in d.glob("*.md")}

    def test_el_inventario_cita_todos_los_modelos_del_repo(self):
        texto = (self.raiz / "derecho" / "skills" / "derecho-argentino" / "references"
                 / "modelos.md").read_text(encoding="utf-8")
        citados = set(re.findall(r"`(kb/escritos/[\w./\-]+\.md)`", texto))
        faltan = sorted(self.modelos - citados)
        self.assertEqual(faltan, [], f"modelos.md no inventaría: {faltan}")

    def test_los_documentos_que_cuentan_modelos_dicen_el_numero_real(self):
        cuantos = len(self.modelos)
        for relativo in ("derecho/kb/README.md", "docs/ARQUITECTURA.md"):
            with self.subTest(relativo):
                texto = (self.raiz / relativo).read_text(encoding="utf-8")
                hallado = re.search(r"(\d+) modelos", texto)
                self.assertIsNotNone(hallado, f"{relativo} dejó de contar los modelos")
                self.assertEqual(int(hallado.group(1)), cuantos)
class TestRutasCitadasPorLaSkill(unittest.TestCase):
    """Toda ruta del repo que un módulo cita entre backticks tiene que existir.

    Una remisión a un archivo que no está no falla ruidosamente: el modelo no encuentra el
    módulo y sigue con lo que tiene. Los prefijos se parecen entre sí —`references/kb/...` y
    `derecho/kb/...`— y sin este test nadie nota la diferencia.
    """

    RUTA = re.compile(r"`((?:argentina|references|herramientas|docs|assets|scripts|fuentes|"
                      r"evals|commands)/[\w./_\-]*[\w_\-])`")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.raiz = raiz
        self.skill = raiz / "derecho" / "skills" / "derecho-argentino"

    def test_las_rutas_que_citan_los_modulos_existen(self):
        archivos = [self.skill / "SKILL.md"] + sorted((self.skill / "references").glob("*.md"))
        citadas = 0
        for archivo in archivos:
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                for ruta in self.RUTA.findall(linea):
                    citadas += 1
                    # Se admite relativa al repo, a la skill, a references/ o a derecho/.
                    candidatos = [self.raiz / ruta, self.skill / ruta,
                                  self.skill / "references" / ruta, self.raiz / "derecho" / ruta]
                    with self.subTest(f"{archivo.name}:{numero}"):
                        self.assertTrue(any(c.exists() for c in candidatos),
                                        f"{archivo.name}:{numero} cita una ruta inexistente: {ruta}")
        self.assertGreater(citadas, 100, "los módulos dejaron de citar rutas del repo")
class TestLaDisciplinaDeLectura(unittest.TestCase):
    """Lo que hace que una consulta cueste: **releer**, no leer.

    El costo de una sesión no es el tamaño del módulo sino el tamaño por la cantidad de turnos:
    lo que entra al contexto se reenvía en cada turno que queda. La traza de una corrida real
    —la misma que cita `TestElTamañoDeLosModulos`— muestra `Read laboral.md`, `Read parte.md`,
    `Read laboral.md` **otra vez** y dos `Grep` sobre el mismo archivo. Cuatro accesos, 24k
    tokens de módulo, por algo que ya estaba a la vista.

    **La regla vive en la sección 16 y es lo primero que alguien corta** cuando `SKILL.md` toca el
    tope de 500 renglones de prosa, porque parece prosa. No lo es: es la única parte del archivo
    que habla de cuánto cuesta lo que se hace con él.

    **El trinquete de las secciones va en el mismo lado.** Una fila que nombra la sección deja
    volver sobre un punto ya leído sin abrir nada; sacarlas no rompe nada visible, así que nada
    las defendería. Subir el número cuando entren más filas con sección es la dirección correcta.

    MUTACIÓN que lo comprueba: borrar de la sección 16 el renglón que dice que el módulo se lee
    una vez y entero deja en rojo a `test_la_regla_de_leer_una_vez_esta_escrita`; sacarle la
    sección a una fila de ruteo, a `test_las_filas_que_nombran_seccion_no_bajan`.
    """

    #: Las filas de la sección 16 que hoy nombran la sección del módulo al que rutean.
    CON_SECCION = 11

    def setUp(self):
        skill = Path(__file__).resolve().parents[1] / "SKILL.md"
        self.texto = skill.read_text(encoding="utf-8")
        self.ruteo = self.texto.split("## 16 · Ruteo")[1]

    def test_la_regla_de_leer_una_vez_esta_escrita(self):
        for pieza in ("se lee UNA vez y ENTERO",
                      "está en lo ya leído",
                      "se decide antes"):
            with self.subTest(pieza):
                # `assertTrue` y no `assertIn`: el pajar son 15 KB y un mensaje que los imprime
                # no se lee, que es la misma falla que este control persigue.
                self.assertTrue(pieza in self.ruteo,
                                f"la sección 16 perdió «{pieza}»: sin la disciplina de lectura el "
                                f"modelo vuelve a leer el módulo que ya tiene, y eso se paga en "
                                f"cada turno que queda")

    def test_las_filas_que_nombran_seccion_no_bajan(self):
        filas = [l for l in self.ruteo.split("\n") if l.startswith("| ") and "---" not in l]
        self.assertGreater(len(filas), 50, "no encontró la tabla de ruteo: el control está apagado")
        con = [l for l in filas
               if re.search(r"`(?:references/)?[a-z0-9-]+\.md`\s+\d", l)]
        self.assertGreaterEqual(
            len(con), self.CON_SECCION,
            f"{len(con)} filas de ruteo nombran la sección y el trinquete es {self.CON_SECCION}. "
            f"Que la fila diga la sección es lo que evita el `Grep` de rescate sobre un módulo "
            f"que ya está leído. Si se sacó a propósito, bajar el número acá y decir por qué.")


class TestElPresupuestoDeSKILL(unittest.TestCase):
    """`SKILL.md` se carga entero en cada conversación, y nada de eso es bajo demanda.

    La documentación de Claude Code lo dice sin vueltas: *"Keep `SKILL.md` under 500 lines. Move
    detailed reference material to separate files"*
    (<https://code.claude.com/docs/en/skills.md>, consultado el 18/09/2026). El cuerpo entra
    completo al activarse la skill; los `references/` sólo cuando el modelo decide abrirlos. De
    modo que un renglón acá lo paga toda conversación y un renglón allá lo paga la que lo usa.

    **Se miden dos cosas distintas y por eso hay dos topes.** Los 500 documentados se aplican a la
    **prosa**, que es lo que se infla: explicaciones que ya están en un módulo, estados anteriores,
    la misma regla dicha dos veces. Las **filas de tabla** son otra cosa —el ruteo de la sección 16
    y el vocabulario de marcadores de la sección 3—, y son justamente lo que la documentación manda
    dejar acá: navegación, y un vocabulario que el modelo transcribe **exacto** en cada respuesta y
    no va a abrir un módulo para copiar un corchete. Un módulo nuevo agrega una fila y eso es
    cobertura, no deuda.

    **Contarlas juntas rompía el control en la dirección equivocada:** un módulo nuevo ponía el
    suite en rojo y lo que se aprendía era a subir el número. Separadas, la prosa tiene el tope
    documentado y las tablas un trinquete que impide que exploten.

    MUTACIÓN que lo comprueba: agregarle diez renglones de prosa a `SKILL.md` lo deja en rojo por
    `test_la_prosa_entra_en_los_500`; agregarle veinte filas de tabla, por `test_las_tablas_no_explotan`.
    """

    PROSA = 500        # el tope documentado por Claude Code
    TABLA = 145        # trinquete: las filas de hoy con margen para módulos nuevos

    def setUp(self):
        self.archivo = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                        / "SKILL.md")
        ls = self.archivo.read_text(encoding="utf-8").splitlines()
        self.filas = [l for l in ls if l.startswith("| ")]
        self.prosa = len(ls) - len(self.filas)

    def test_la_prosa_entra_en_los_500(self):
        self.assertLessEqual(
            self.prosa, self.PROSA,
            f"la prosa del SKILL.md son {self.prosa} renglones y el tope documentado es "
            f"{self.PROSA}. Lo que entra tiene que sacar algo, y lo primero que se busca es la "
            f"explicación que ya está en un módulo: se reemplaza por el puntero.")

    def test_las_tablas_no_explotan(self):
        self.assertLessEqual(
            len(self.filas), self.TABLA,
            f"{len(self.filas)} filas de tabla contra un trinquete de {self.TABLA}. Una fila por "
            f"módulo nuevo es esperable; veinte de golpe es una tabla que se copió de un módulo.")

    def test_el_control_mira_el_archivo_que_cree(self):
        """Instrumento encendido: si la ruta o el formato cambiaran, los topes no medirían nada."""
        self.assertGreater(self.prosa, 300, "midió menos prosa de la posible: ¿está leyendo el archivo?")
        self.assertGreater(len(self.filas), 80, "no encontró las tablas de ruteo y de marcadores")
class TestLaCoberturaNoRepiteElRuteo(unittest.TestCase):
    """0.1 bis dice **hasta dónde llega** cada materia; la sección 16 dice **qué módulo abrir**.

    Las dos son tablas de materia contra módulo y por eso convergen solas: cada módulo nuevo
    entraba a las dos, y 0.1 bis terminó con treinta y tres filas que describían el contenido de
    un módulo —«Salud y discapacidad: CUD, quién debe cubrir…»— doce renglones más arriba de la
    fila de la 16 que lo enruta. Eso se paga en cada conversación y no orienta a nadie: para
    rutear sirve la situación de quien consulta, que es lo que dice la 16, no el temario del
    archivo.

    Lo que sostiene la separación son dos reglas:

    - **Una fila por materia, no una por módulo.** Los módulos son decenas; las materias con
      veredicto propio, poco más de diez. Una tabla que crece con los módulos se pasa del tope.
    - **Una fila tiene que decir algo además de a dónde ir.** Si sacándole las rutas y los
      nombres de archivo no queda texto, esa fila es ruteo y su lugar es la 16.

    MUTACIÓN que lo comprueba: copiar a 0.1 bis una fila de la sección 16 —de las que dicen
    «`references/<modulo>.md`» y nada más— deja en rojo `test_ninguna_fila_es_solo_un_destino`.
    """

    TOPE_DE_FILAS = 20

    def setUp(self):
        t = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
             / "SKILL.md").read_text(encoding="utf-8")
        bis = t[t.index("### 0.1 bis"):t.index("### 0.2 ·")]
        self.filas = [l for l in bis.splitlines()
                      if l.startswith("| ") and "---" not in l and not l.startswith("| Materia")]

    @staticmethod
    def _pelado(celda):
        """La celda sin rutas ni nombres de archivo, y sin puntuación: lo que de verdad dice."""
        return re.sub(r"[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", "", re.sub(r"`[^`]+`", "", celda))

    def test_hay_tabla(self):
        """Instrumento encendido: sin filas, las dos reglas de abajo pasan sin mirar nada."""
        self.assertGreater(len(self.filas), 8, "no encontró la tabla de cobertura de 0.1 bis")

    def test_una_fila_por_materia_y_no_una_por_modulo(self):
        self.assertLessEqual(
            len(self.filas), self.TOPE_DE_FILAS,
            f"0.1 bis tiene {len(self.filas)} filas: está creciendo con los módulos en vez de "
            f"con las materias. El mapa de módulos es la tabla de ruteo de la sección 16.")

    def test_ninguna_fila_es_solo_un_destino(self):
        solo_ruta = [f for f in self.filas if not self._pelado(f.strip("| ").split(" | ")[-1])]
        self.assertEqual(
            [], [f[:80] for f in solo_ruta],
            "hay filas de 0.1 bis cuya cobertura es sólo un módulo: eso es ruteo y va a la "
            "sección 16. Acá va el veredicto — profunda, cubierta, nada cargado, sin perfil.")
class TestElModuloDeRolDiceDeQueFueroEs(unittest.TestCase):
    """`sede-judicial-pba.md` y `parte.md` son del **fuero laboral de PBA**, y hay que decirlo
    donde se rutea, no una sola vez al pie de una tabla.

    El módulo de sede judicial trae la estructura del veredicto y de la sentencia, los recaudos
    de los arts. 168 y 171 de la Constitución provincial y el régimen recursivo bonaerense. Nada
    de eso rige en un juzgado nacional del trabajo, en uno civil de la Nación ni en un tribunal
    penal, y su única mención al orden nacional es una advertencia de **no** transpolar el art.
    46 de la Ley 18.345. De eso la skill no tiene módulo.

    El riesgo no es que el módulo sea de PBA: es **dónde** se entera el modelo. La 0.1 pregunta
    el rol en el primer turno y rutea ahí mismo, así que un juez del fuero nacional queda
    encaminado a un módulo provincial antes de que se haya leído nada más. Por eso el límite se
    exige en las dos secciones que deciden —la que pregunta y la que explica el modo— y no
    alcanza con que esté en la 0.1 bis.

    MUTACIÓN que lo comprueba: sacar «del **fuero laboral bonaerense**» del párrafo de la 0.1
    deja este test en rojo por esa sección.
    """

    #: Cada tramo va del encabezado que lo abre al que lo cierra.
    SECCIONES = {"0.1 · el rol se pregunta y se rutea": ("### 0.1 · Desde dónde se actúa",
                                                         "#### El perfil guardado"),
                 "1.6 · el modo órgano": ("### 1.6 · Si se actúa desde el órgano", "\n---\n")}

    def setUp(self):
        self.skill = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                      / "SKILL.md").read_text(encoding="utf-8")

    def _tramo(self, arranca, corta):
        i = self.skill.index(arranca)
        resto = self.skill[i:]
        j = resto.index(corta, len(arranca))
        return re.sub(r"\s+", " ", resto[:j])

    def test_las_dos_secciones_que_rutean_nombran_el_fuero(self):
        for nombre, (arranca, corta) in self.SECCIONES.items():
            with self.subTest(nombre):
                tramo = self._tramo(arranca, corta)
                self.assertIn("sede-judicial-pba.md", tramo,
                              "esta sección dejó de rutear al módulo: revisar el tramo")
                self.assertTrue(
                    "bonaerense" in tramo or "de la PBA" in tramo,
                    f"«{nombre}» rutea a `sede-judicial-pba.md` sin decir que es de PBA: un "
                    f"órgano del fuero nacional queda encaminado a un módulo provincial")
                self.assertIn("laboral", tramo,
                              f"«{nombre}» no dice que el módulo es del fuero laboral")

    def test_el_modulo_sigue_siendo_de_un_solo_fuero(self):
        """Instrumento encendido al revés: el día que el módulo cubra otro fuero, estas
        advertencias pasan a ser falsas y hay que sacarlas. Lo que se mide es que el título del
        módulo siga declarando su alcance, que es de donde sale la advertencia."""
        titulo = (RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "sede-judicial-pba.md").read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("fuero laboral PBA", titulo,
                      "el módulo cambió de alcance: revisar las advertencias del SKILL.md")
class TestLosModulosDeclaranSuBorde(unittest.TestCase):
    """Un módulo que no dice dónde termina se lee como si no terminara.

    El modelo abre el módulo de la rama, no encuentra el punto, y **completa con conocimiento
    general** en vez de decir que ahí la skill no llega. Es el mismo modo de falla que el de un
    monto citado de memoria, y es más difícil de ver porque la respuesta sale bien redactada.

    Lo declara una sección **«Lo que este módulo NO hace»**, con el destino de cada cosa que
    queda afuera. La practican los módulos que nacieron angostos; los que hay que vigilar son los
    grandes y viejos —`laboral.md`, `civil.md`, `consumidor.md`— porque son los que el modelo
    abre primero y con los que más confianza trabaja.

    **Es un trinquete sobre el reparto, no un mínimo por archivo.** Exigirlo en los 57 dejaría el
    suite en rojo hasta escribir 31 bordes de memoria, que es exactamente lo que no hay que
    hacer: cada uno sale de leer el módulo. Lo que se fija es que la práctica no retroceda.

    MUTACIÓN que lo comprueba: borrar la sección de `laboral.md` deja este test en rojo.
    """

    # La forma del encabezado es exacta a propósito: contar con un regex laxo enganchaba una
    # minúscula y contaba de más, y un control que cuenta de más es el que no suena nunca.
    #
    # **El piso se sube cuando se agrega un borde, y eso es parte de agregarlo.** Un trinquete que
    # no se mueve queda atrás de la práctica y deja de atrapar: con el piso en 26 y treinta bordes
    # escritos, borrar uno no lo hacía fallar. La mutación lo destapó.
    PISO = 30   # los que lo declaran hoy

    def setUp(self):
        self.refs = sorted((RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                            / "references").glob("*.md"))
        self.con_borde = [p.name for p in self.refs
                          if "Lo que este módulo NO hace" in p.read_text(encoding="utf-8")
                          or "Qué NO cubre" in p.read_text(encoding="utf-8")]

    def test_el_control_mira_todos_los_modulos(self):
        """Instrumento encendido: sin módulos, «no retrocedió» no mide nada."""
        self.assertGreater(len(self.refs), 40, "no encontró los módulos de referencia")

    def test_la_practica_no_retrocede(self):
        self.assertGreaterEqual(
            len(self.con_borde), self.PISO,
            f"{len(self.con_borde)} módulos declaran su borde y antes eran {self.PISO}. Un borde "
            f"no se saca: si el módulo creció y ahora cubre lo que decía no cubrir, se reescribe "
            f"la sección, no se borra.")
class TestLasRemisionesApuntanAUnaSeccionQueExiste(unittest.TestCase):
    """Una remisión a `modulo.md 42` es una promesa: ahí está lo que hace falta.

    Si esa sección no existe, **nada falla ruidosamente**. El modelo abre el módulo, no encuentra
    la sección, y sigue con lo que tiene — que es el modo de falla que este repositorio persigue.
    `TestRutasCitadasPorLaSkill` ya exige que el ARCHIVO exista; esto exige que exista la SECCIÓN.

    **Es la novena cosa que arrastra una partición**, la que `docs/DESARROLLO.md` decía que
    ninguna suite reclamaba: cuando el derecho colectivo salió a `laboral-colectivo.md`, la tabla
    de absorbidos de `laboral.md` siguió diciendo *"5.17 de este módulo"* sobre una sección que ya
    no estaba ahí. También atrapó una remisión a `ejecucion.md` 20 —es la 21; la 20 es
    `prueba-pericial.md`— escrita justamente en la frase que decía «no confundir».

    **El ordinal es parte del número.** `5.17 bis` y `5.17 ter` existen y `5.17` no, así que el
    control lee el ordinal: sin eso reclamaba cuatro remisiones correctas y el instrumento se
    apagaba solo.

    MUTACIÓN que lo comprueba: cambiar una remisión de `ejecucion.md` 21 por `ejecucion.md` 20 lo
    deja en rojo.
    """

    ORDINAL = "bis|ter|quater|quinquies|sexies"
    ENCABEZADO = re.compile(rf"^#{{2,4}} (\d+(?:\.\d+)*(?:\s+(?:{ORDINAL}))?)\b", re.M)
    #: `modulo.md 42`, `modulo.md, 42` y `modulo.md sección 42` son la misma remisión. La palabra
    #: intermedia estaba afuera del patrón y con ella se colaban diez remisiones a una sección que
    #: no existía: ver `test_la_palabra_seccion_no_esconde_la_remision`.
    CITA = re.compile(rf"`(?:references/)?([\w\-]+\.md)`[,)]?\s+\(?(?:secci[óo]n\s+)?"
                      rf"(\d+(?:\.\d+)*(?:\s+(?:{ORDINAL}))?)\b")

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        skill = raiz / "derecho" / "skills" / "derecho-argentino"
        self.refs = skill / "references"
        self.secciones = {
            p.name: {" ".join(m.group(1).split())
                     for m in self.ENCABEZADO.finditer(p.read_text(encoding="utf-8"))}
            for p in sorted(self.refs.glob("*.md"))}
        self.archivos = ([skill / "SKILL.md"] + sorted(self.refs.glob("*.md"))
                         + sorted((raiz / "docs").glob("*.md"))
                         + [raiz / "AGENTS.md", raiz / "README.md", raiz / "LICENCIAS.md"])

    def _cubre(self, modulo, numero):
        """Una remisión a 24.9 vale si el módulo declara 24.9 o cualquier 24.9.x."""
        return any(s == numero or s.startswith(numero + ".") or s.startswith(numero + " ")
                   for s in self.secciones[modulo])

    def test_toda_remision_numerada_existe(self):
        rotas, miradas = [], 0
        for a in self.archivos:
            if not a.is_file():
                continue
            for n, linea in enumerate(a.read_text(encoding="utf-8").splitlines(), 1):
                for modulo, numero in self.CITA.findall(linea):
                    if modulo not in self.secciones:
                        continue
                    miradas += 1
                    numero = " ".join(numero.split())
                    if not self._cubre(modulo, numero):
                        rotas.append(f"{a.name}:{n} → {modulo} {numero}")
        self.assertGreater(miradas, 100, "casi no se miró ninguna remisión: el control está apagado")
        self.assertEqual(rotas, [],
                         "remisiones a una sección que el módulo no declara:\n    "
                         + "\n    ".join(rotas))

    def test_la_palabra_seccion_no_esconde_la_remision(self):
        """La forma larga —"modulo.md sección 42"— es la que escriben los módulos cuando la
        remisión va en medio de una frase, y el patrón sólo enganchaba la corta. Mientras tanto
        diez módulos mandaban a `perfiles-heredados.md` sección 19 y ese módulo no declaraba
        ninguna sección numerada: el fallback de cobertura —el que se abre justo cuando el módulo
        de la rama no llega— apuntaba a la nada, y el control decía verde porque ni las miraba.

        MUTACIÓN que lo comprueba: sacar `(?:secci[óo]n\\s+)?` del patrón deja de ver estas
        remisiones; si además se quita el `## 19` de `perfiles-heredados.md`, el test de arriba
        vuelve al rojo que tenía que haber dado siempre.
        """
        self.assertEqual(self.CITA.findall("ver `perfiles-heredados.md` sección 19, con su nota"),
                         [("perfiles-heredados.md", "19")])
        self.assertEqual(self.CITA.findall("ver `modelos.md` (sección 23.7)"),
                         [("modelos.md", "23.7")])
        self.assertIn("19", self.secciones["perfiles-heredados.md"],
                      "el módulo al que mandan diez remisiones no declara su número")

    #: «ver 5.9» sin nombrar el archivo. La raíz dice a qué módulo va, pero sólo si se conoce el
    #: mapa número→archivo, que no está escrito en ninguna parte y no tiene por qué estarlo.
    DESNUDA = re.compile(r"[Vv]er (?:la )?(?:secci[óo]n )?(\d{1,2})\.\d+")

    def test_una_remision_que_sale_del_modulo_nombra_el_archivo(self):
        """Adentro del módulo «ver 5.9» se entiende: la raíz es la suya. Afuera obliga a saber
        que 5 es `laboral.md`, y ese mapa no está escrito en ningún lado —lo reconstruye este
        suite leyendo los encabezados—. Así que la remisión que cruza de módulo nombra el archivo,
        y de paso entra al control de arriba, que sólo mira las que lo nombran.

        La línea que EXPLICA la convención queda afuera por su forma: cita el ejemplo entre
        comillas. `SKILL.md` la usa para enseñar que la numeración es global.

        MUTACIÓN que lo comprueba: en `SKILL.md`, sacarle el nombre del archivo a la remisión
        al 8.4 y dejar sólo el número lo deja en rojo.
        """
        archivos = [RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "SKILL.md"]
        archivos += sorted(self.refs.glob("*.md"))
        desnudas, miradas = [], 0
        for a in archivos:
            texto = a.read_text(encoding="utf-8")
            propias = {" ".join(m.group(1).split()).split(".")[0]
                       for m in self.ENCABEZADO.finditer(texto)}
            for n, linea in enumerate(texto.splitlines(), 1):
                if ".md" in linea:
                    continue
                for raiz in self.DESNUDA.findall(linea):
                    miradas += 1
                    if raiz in propias or f'"ver {raiz}.' in linea.lower():
                        continue
                    desnudas.append(f"{a.name}:{n} → {raiz}.x")
        self.assertGreater(miradas, 20, "casi no vio remisiones desnudas: el control está apagado")
        self.assertEqual(desnudas, [],
                         "remisiones a otro módulo sin nombrar el archivo:\n    "
                         + "\n    ".join(desnudas))

    def test_los_modulos_declaran_secciones(self):
        """Instrumento encendido: si el regex del encabezado dejara de enganchar, todo pasaría."""
        con = [m for m, s in self.secciones.items() if s]
        self.assertGreater(len(con), 40, "casi ningún módulo declara secciones numeradas")
        self.assertIn("5.17 bis", self.secciones["laboral.md"],
                      "el control perdió el ordinal y volvería a reclamar remisiones correctas")
class TestNingunNumeroDeSeccionEstaEnDosModulos(unittest.TestCase):
    """La numeración es **global**, así que un número es una dirección y tiene un solo destino.

    Si dos módulos declaran `5.18`, una remisión a 5.18 apunta a dos lugares y el lector llega al
    que abrió primero. Pasó al agregar los bordes: la sección «Lo que este módulo NO hace» de
    `laboral.md` se numeró 5.18, que es **Asociaciones sindicales** en `laboral-colectivo.md`
    desde la partición. Nada falló: simplemente había dos 5.18.

    **Dos repeticiones son legítimas, y las dos se reconocen por su forma, no por una lista.**

    - **El número raíz se comparte tras una partición.** `laboral.md` y `laboral-colectivo.md`
      declaran los dos `## 5`, porque 5.1 a 5.17 quedaron en uno y 5.17 a 5.18 se fueron al otro.
      El padre es el árbol; lo que tiene que ser único es la **hoja**, así que el control mira los
      números con punto.
    - **El stub que reenvía lo dice en su encabezado**, con esta forma exacta:
      `## 24.8 · Ejecución de la pena — está en ` seguido del módulo entre backticks. Es lo que
      hace que una remisión vieja siga llegando después de una mudanza, así que el número **tiene**
      que repetirse — y exigir la forma obliga al stub a decir a dónde manda, que es lo que el
      lector necesita. Una primera versión de este control adivinaba el stub por si el texto
      nombraba otro módulo, y **la mutación no la hizo fallar**: el borde de `laboral.md` nombra
      cuatro módulos en sus viñetas y pasaba por stub. Se descartó en vez de calibrarla.

    **`danos-indice-doctrinario.md` queda afuera**: sus §1 a §38 son los capítulos de una obra
    comercial, otro espacio de nombres que no colisiona con este árbol aunque los números coincidan.

    MUTACIÓN que lo comprueba: renumerar el borde de `laboral.md` como 5.18 lo deja en rojo.
    """

    OTRO_ESPACIO = {"danos-indice-doctrinario.md"}
    #: El ordinal puede llevar subsecciones detrás —`5.2 bis.1`—, y sin el tramo final el regex
    #: cortaba en «5.2 bis» y daba por repetido lo que es la sección y su hija.
    H = re.compile(r"^#{2,4} (\d+(?:\.\d+)*(?:\s+(?:bis|ter|quater|quinquies|sexies))?"
                   r"(?:\.\d+)*)\b([^\n]*)", re.M)
    #: La forma que declara un stub de reenvío, y de paso dice a dónde manda.
    STUB = re.compile(r"—\s*est[áa]\s+en\s+`[\w\-]+\.md`")

    def setUp(self):
        self.refs = sorted((RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino"
                            / "references").glob("*.md"))
        self.dueno, self.stubs = {}, 0
        self.veces = collections.Counter()
        for p in self.refs:
            if p.name in self.OTRO_ESPACIO:
                continue
            for m in self.H.finditer(p.read_text(encoding="utf-8")):
                num = " ".join(m.group(1).split())
                self.veces[(p.name, num)] += 1
                if self.STUB.search(m.group(2)):
                    self.stubs += 1
                    continue
                self.dueno.setdefault(num, set()).add(p.name)

    def test_el_control_ve_los_numeros_y_los_stubs(self):
        """Instrumento encendido por los dos lados: si no viera números no mediría nada, y si no
        reconociera ningún stub estaría reclamando las mudanzas legítimas."""
        self.assertGreater(len(self.dueno), 300, "casi no encontró secciones numeradas")
        self.assertGreater(self.stubs, 0, "no reconoció ningún stub de reenvío: revisar la forma")

    def test_una_hoja_una_sola_vez_en_su_modulo(self):
        """Y el mismo número tampoco se repite **adentro** de un módulo.

        El control de arriba junta los módulos en un `set`, así que dos encabezados con el mismo
        número en el MISMO archivo se funden en una sola entrada y no se ven. Es la alarma que no
        suena nunca: `penal.md` llegó a tener dos `24.6.5` —la checklist de recurrir y el CPP de la
        Ciudad, hoy en `penal-impugnacion.md`— y
        dos `24.10`, con la fila de `changelog-normativo.md` y la de `REVALIDAR.md` apuntando a
        uno de los dos. Una remisión no elige: el lector llega al que aparece primero.

        Acá se cuentan los stubs también: un módulo que reenvía un número no puede además
        declararlo suyo.

        MUTACIÓN que lo comprueba: renumerar «24.6.6 Antes de recurrir» de
        `penal-impugnacion.md` como 24.6.5 lo deja en rojo, y el mensaje nombra el archivo y el
        número.
        """
        repetidos = [f"{nombre} :: {num} ({n} veces)"
                     for (nombre, num), n in sorted(self.veces.items()) if n > 1]
        self.assertEqual(repetidos, [],
                         "el mismo número de sección dos veces en el mismo módulo, y una remisión "
                         "no elige a cuál llega:\n    " + "\n    ".join(repetidos))

    def test_una_hoja_un_modulo(self):
        choques = [f"{num}: {sorted(m)}" for num, m in sorted(self.dueno.items())
                   if "." in num and len(m) > 1]
        self.assertEqual(choques, [],
                         "el mismo número de sección en dos módulos, y ninguno declara ser un "
                         "stub de reenvío:\n    " + "\n    ".join(choques))
class TestEncabezadoDeLosModulos(unittest.TestCase):
    """Todos los módulos abren con el MISMO encabezado, palabra por palabra.

    No es prolijidad: un módulo se lee solo. La skill carga `laboral.md` sin cargar los otros
    veintinueve, así que lo que el encabezado no diga ahí, ahí no está dicho. Y lo que tiene
    que decir es que rigen las reglas de integridad de la sección 2 --las que prohíben
    afirmar una norma sin fuente a la vista--.

    Había derivado a **21 redacciones distintas en 30 archivos**, y sólo 13 nombraban esas
    reglas. Los otros 17 no las negaban: no las mencionaban, que para quien lee un archivo
    solo es lo mismo. Una convención que se copia a mano treinta veces diverge; el candado es
    esto.

    Lo que sigue siendo propio de cada módulo --la jurisdicción de lo procesal, qué quedó sin
    cerrar, que es el espejo de otro-- va DESPUÉS, en el mismo bloque. Lo común va primero y
    es idéntico.
    """

    COMUN = ("Módulo de referencia de la skill `derecho-argentino`. Numeración global: las "
             "remisiones cruzadas entre módulos siguen siendo válidas. **Rigen las reglas de "
             "integridad de la sección 2 del SKILL.md.**")

    # `danos-indice-doctrinario.md` no es un módulo de derecho sino el índice de una obra
    # comercial que vive en `_local/`: no lo lee la skill como módulo y no abre con el bloque.
    SIN_ENCABEZADO = {"danos-indice-doctrinario.md"}

    def test_todos_abren_con_el_mismo_encabezado(self):
        base = RAIZ_DEL_CHECKOUT / "derecho" / "skills" / "derecho-argentino" / "references"
        if not base.is_dir():
            self.skipTest("no esta la skill")
        modulos = [p for p in sorted(base.glob("*.md")) if p.name not in self.SIN_ENCABEZADO]
        self.assertGreater(len(modulos), 25, "no encontré los módulos: el control está apagado")
        for p in modulos:
            lineas = p.read_text(encoding="utf-8").splitlines()
            bloque = []
            for l in lineas[:20]:
                if l.startswith(">"):
                    bloque.append(l.lstrip(">").strip())
                elif bloque:
                    break
            texto = " ".join(bloque)
            with self.subTest(p.name):
                self.assertTrue(texto.startswith(self.COMUN),
                                f"{p.name} no abre con el encabezado común. Empieza con:\n"
                                f"  {texto[:120]}\nY tiene que empezar con:\n"
                                f"  {self.COMUN[:120]}")
class TestContradiccionesNominadas(unittest.TestCase):
    """Cada cita entrecomillada de un bloque de contradicciones tiene que estar en `kb/`.

    Esos bloques citan al perfil para nombrar su error, así que la cita tiene que ser
    textual: si no aparece literalmente bajo `kb/`, el módulo está discutiendo con una frase
    que nadie escribió, o el perfil cambió y la contradicción quedó vieja.
    """

    CITA = re.compile(r'\*"([^"]{15,})"\*')

    def setUp(self):
        raiz = RAIZ_DEL_CHECKOUT
        self.referencias = raiz / "derecho" / "skills" / "derecho-argentino" / "references"
        kb = raiz / "derecho" / "kb"
        self.kb = self._plano("\n".join(
            p.read_text(encoding="utf-8", errors="replace") for p in sorted(kb.rglob("*.md"))))

    @staticmethod
    def _plano(texto: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[*`]", "", texto)).strip().lower()

    def _citas(self):
        for archivo in sorted(self.referencias.glob("*.md")):
            dentro = False
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                if linea.startswith("#"):
                    dentro = "Contradicciones nominadas" in linea
                elif dentro and linea.startswith("|"):
                    for cita in self.CITA.findall(linea):
                        yield archivo.name, numero, cita

    def test_las_citas_del_perfil_existen_en_kb(self):
        citas = list(self._citas())
        self.assertGreaterEqual(len(citas), 5, "dejaron de citarse los errores del perfil")
        for archivo, numero, cita in citas:
            with self.subTest(f"{archivo}:{numero}"):
                # assertTrue y no assertIn: assertIn volcaría los 2,3 MB de kb/ en el error.
                self.assertTrue(self._plano(cita) in self.kb,
                                f"{archivo}:{numero} cita como error del perfil un texto que no "
                                f"está en kb/: «{cita}»")
class TestMapaDeCobertura(unittest.TestCase):
    """`docs/COBERTURA.md` nombra módulos, y esa lista se despega sola.

    El documento es un relevamiento fechado: que la taxonomía siga siendo la de las fuentes no lo
    puede verificar nadie, y así está dicho ahí. Lo que sí se puede sostener es la otra mitad —
    que los módulos que nombra existan, y que ningún módulo del repositorio quede sin mencionar.
    Sin esto, agregar un módulo deja el mapa mintiendo por omisión, que es la forma en que un
    documento de cobertura se vuelve inútil sin que nadie lo note.

    No se revisa el contenido de la taxonomía: eso se relee contra las fuentes y se cambia la
    fecha. Un test que pretendiera verificarlo daría verde sobre una opinión.
    """

    RAIZ = Path(__file__).resolve().parents[4]

    def setUp(self):
        self.doc = self.RAIZ / "docs" / "COBERTURA.md"
        self.assertTrue(self.doc.exists(), f"falta {self.doc}")
        self.texto = self.doc.read_text(encoding="utf-8")
        self.modulos = {p.name for p in
                        (self.RAIZ / "derecho" / "skills" / "derecho-argentino"
                         / "references").glob("*.md")}
        self.assertGreater(len(self.modulos), 10, "no se encontraron los módulos")

    def test_lleva_fecha_de_relevamiento(self):
        # Vale por su fecha: sin ella, un mapa viejo se lee como si fuera de hoy.
        self.assertRegex(self.texto, r"[Rr]elevado el \d{2}/\d{2}/\d{4}",
                         "COBERTURA.md no dice cuándo se relevó")

    def test_todo_modulo_que_nombra_existe(self):
        nombrados = set(re.findall(r"`([a-z0-9-]+\.md)`", self.texto)) & {
            n for n in re.findall(r"`([a-z0-9-]+\.md)`", self.texto)}
        nombrados = {n for n in nombrados if n not in ("AGENTS.md", "COBERTURA.md")}
        self.assertTrue(nombrados, "COBERTURA.md no nombra ningún módulo: el lector quedó apagado")
        for nombre in sorted(nombrados):
            with self.subTest(nombre):
                self.assertIn(nombre, self.modulos,
                              f"COBERTURA.md nombra {nombre}, que no está en references/")

    def test_las_ramas_con_modulo_estan_todas_nombradas(self):
        # Sólo los módulos de RAMA: los de infraestructura no son cobertura de materia y
        # nombrarlos en el mapa sería ruido.
        infraestructura = {"changelog-normativo.md", "escritos.md", "fuentes.md", "intake.md",
                           "marcadores.md", "modelos.md", "perfiles-heredados.md", "parte.md",
                           "plazos.md", "fallos-csjn.md", "danos-indice-doctrinario.md",
                           "sede-judicial-pba.md", "notificaciones-pba.md", "prueba-pericial.md",
                           "ejecucion.md", "telegramas.md", "contratos.md", "civil.md"}
        ramas = self.modulos - infraestructura
        # Con backticks y nombre completo, que es como el documento cita un módulo: buscar la
        # subcadena suelta haría que «tránsito» matchee dentro de «transitorio».
        citados = set(re.findall(r"`([a-z0-9-]+\.md)`", self.texto))
        faltan = sorted(r for r in ramas if r not in citados)
        self.assertEqual(faltan, [],
                         "estos módulos de rama existen y COBERTURA.md no los menciona, así que "
                         "el mapa miente por omisión: " + ", ".join(faltan))

    def test_la_columna_de_modulo_no_lleva_numero_de_seccion(self):
        """En la tabla de materias sin fuero, la referencia es el módulo y nada más.

        Este documento contesta una sola pregunta —si la materia tiene módulo—, y el número de
        sección no la contesta: vive adentro del módulo y en la tabla de ruteo de la sección 16
        del SKILL.md, que es donde alguien lo busca. Acá sólo agrega números escritos a mano que
        se desactualizan cuando un módulo se parte, y **la tabla ya llegó a estar dispareja**:
        siete referencias con número y treinta y una sin él.

        Que el número esté MAL es peor que que falte, y pasa: en esta misma sesión se escribió
        «propiedad-industrial.md 57» cuando es la 40, de memoria y sin cotejar. Prohibirlo acá
        cierra esa puerta en vez de vigilarla.

        MUTACIÓN QUE LO COMPRUEBA: agregar « 1.9» a la referencia de `sede-judicial-caba.md` en
        esa tabla lo deja en rojo, y el mensaje dice qué sección es en realidad.
        """
        refs = self.RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"
        encabezado = re.compile(r"(?m)^#{2,3} (\d[\d.]*)")

        renglones, dentro = [], False
        for linea in self.texto.splitlines():
            if linea.startswith("## "):
                dentro = "Materias con módulo que no son un fuero" in linea
            elif dentro and linea.startswith("| ") and "---" not in linea:
                renglones.append(linea)
        self.assertGreater(len(renglones), 10, "cambió la tabla de COBERTURA.md que se cruza acá")

        con_numero = []
        for linea in renglones[1:]:
            celda = linea.strip("|").split("|")[1]
            for modulo, numero in re.findall(r"`([a-z0-9-]+\.md)`( \d[\d.]*)", celda):
                if modulo not in self.modulos:
                    continue
                hallado = encabezado.search((refs / modulo).read_text(encoding="utf-8"))
                real = hallado.group(1).rstrip(".") if hallado else "sin numerar"
                con_numero.append(f"{modulo} dice {numero.strip()} (es la {real})")
        self.assertEqual(con_numero, [],
                         "la columna de módulo lleva número de sección, y acá va sólo el módulo: "
                         + ", ".join(con_numero))

def _sin_color(entorno: dict | None = None) -> dict:
    """El entorno del subproceso con el color apagado.

    `argparse` colorea su ayuda, y varios controles la PARSEAN con regex: con los escapes ANSI
    de por medio `--json` deja de encontrarse y `{a,b,c}` deja de matchear. No se posterga el
    problema limpiando la salida: se pide la ayuda sin color, que es el dato que se quiere
    medir. El color es del terminal, no del programa.

    MUTACIÓN que lo demuestra: sacar `NO_COLOR` del entorno pone en rojo
    `test_todo_valor_de_bandera_que_se_documenta_es_uno_de_los_validos` y
    `test_la_ayuda_de_json_dice_para_que_es_y_para_que_no`.
    """
    return {**(entorno if entorno is not None else os.environ), "NO_COLOR": "1"}
class TestNormasDeCambiosRecientes(unittest.TestCase):
    """Toda norma nombrada en «Cambios recientes» está declarada o tiene veredicto escrito.

    Es el hueco que ninguna otra medida tapa. `cobertura_normativa.py` cruza las leyes que un
    módulo cita **con articulado**, así que una resolución nombrada en una lista de cambios
    recientes no cae en su ventana: puede quedar ahí sin que nada la reclame. Y es justamente
    donde el repositorio anota lo más volátil —montos, reglamentaciones del semestre—, que es
    lo primero que envejece.

    La salida es la misma que para el articulado: o la norma está en `normas.json`, o alguien
    escribió por qué no, en `cobertura-revisada.json`. Lo que no se admite es el silencio.
    """

    RAIZ = Path(__file__).resolve().parents[4]
    SECCION = "## 13 ·"
    # Una norma se reconoce por la palabra que la nombra, no por su forma: en `12/12/2024` el
    # `12/2024` no es ninguna norma. La prosa además las enumera —"Decretos 407, 408 y
    # 409/2026"—, y ahí el año del final vale para toda la lista.
    CLAVE = r"(?:Ley(?:es)?|Res\.|Resoluci[oó]n|Decretos?|RG(?:\s+ARCA)?)"
    LISTA = re.compile(
        CLAVE + r"[^\n:;]{0,24}?((?:\d{1,4}(?:\.\d{3})?)(?:\s*(?:,|y)\s*\d{1,4})*\s*/?\s*\d{0,4})")

    @staticmethod
    def _clave(numero: str) -> str:
        """Clave canónica de una norma: `4/2026` -> `4|2026`, `27.802` -> `27802`.

        Se compara por igualdad y NO por subcadena: aplanados a dígitos, `5844/2026` contiene
        a `4/2026`, así que una norma borrada del manifiesto seguía pareciendo declarada
        porque otra, sin relación, la contenía.
        """
        if "/" in numero:
            cuerpo, anio = numero.split("/", 1)
            return f"{cuerpo.strip()}|{anio.strip()}"
        return numero.replace(".", "").strip()

    @classmethod
    def _clave_de_slug(cls, slug: str) -> str:
        """Misma clave, leída del slug: `res-srt-39-2026` -> `39|2026`, `ley-27802` -> `27802`."""
        con_anio = re.search(r"-(\d{1,4})-(\d{4})$", slug)
        if con_anio:
            return f"{con_anio.group(1)}|{con_anio.group(2)}"
        suelto = re.search(r"-(\d{4,5})$", slug)
        return suelto.group(1) if suelto else ""

    @classmethod
    def _normas_de(cls, renglon: str) -> list:
        salida = []
        for tramo in cls.LISTA.findall(renglon):
            tramo = tramo.strip()
            if "/" in tramo:
                cuerpo, anio = tramo.rsplit("/", 1)
                if not (anio.isdigit() and len(anio) == 4):
                    continue
                salida += [f"{numero}/{anio}" for numero in re.findall(r"\d{1,4}", cuerpo)]
            elif "." in tramo:
                salida.append(tramo)
        return salida

    def setUp(self):
        modulo = (self.RAIZ / "derecho" / "skills" / "derecho-argentino" / "references"
                  / "changelog-normativo.md")
        self.assertTrue(modulo.exists(), f"falta {modulo}")
        texto = modulo.read_text(encoding="utf-8")
        self.assertIn(self.SECCION, texto,
                      f"no está la sección «{self.SECCION}»: el test quedó mirando otra cosa")
        seccion = texto.split(self.SECCION)[1].split("\n---")[0]
        self.renglones = [l for l in seccion.splitlines() if l.startswith("- **")]
        self.vinetas = [l for l in seccion.splitlines()
                        if re.match(r"\s*[-*+]\s|\s*\d+[.)]\s", l)]

        normas = json.loads((self.RAIZ / "derecho" / "fuentes" / "normas" / "normas.json")
                            .read_text(encoding="utf-8"))["normas"]
        self.declarado = {self._clave_de_slug(n["slug"]) for n in normas} - {""}
        revisadas = json.loads((self.RAIZ / "herramientas" / "cobertura-revisada.json")
                               .read_text(encoding="utf-8"))
        crudo = json.dumps(revisadas.get("leyes", {}), ensure_ascii=False)
        self.con_veredicto = {self._clave(n) for n in
                              re.findall(r"\d{1,3}\.\d{3}|\d{1,4}/\d{4}", crudo)}

    def test_el_lector_ve_todos_los_renglones_de_la_seccion(self):
        # Sin umbral: si un renglón de la lista cambia de marcador o de forma, el lector lo
        # pierde y el test de cobertura pasa en verde sin haberlo mirado. Un número mínimo no
        # se entera de eso, porque los otros seis ya lo superan solos.
        self.assertTrue(self.vinetas, "«Cambios recientes» no tiene ningún renglón de lista")
        perdidos = [l for l in self.vinetas if l not in self.renglones]
        self.assertEqual(perdidos, [],
                         "el lector no reconoce estos renglones de «Cambios recientes», así que "
                         "las normas que nombran no las revisa nadie: " + "; ".join(
                             l.strip()[:60] for l in perdidos))

    def test_las_claves_no_se_confunden_entre_si(self):
        # El caso que rompió la versión anterior: por subcadena, `5844/2026` tapaba a `4/2026`.
        self.assertNotEqual(self._clave("4/2026"), self._clave("5844/2026"))
        self.assertEqual(self._clave("39/2026"), self._clave_de_slug("res-srt-39-2026"))
        self.assertEqual(self._clave("27.802"), self._clave_de_slug("ley-27802"))
        self.assertEqual(self._clave("15.563"), self._clave_de_slug("pba-ley-15563"))
        self.assertEqual(self._clave("409/2026"), self._clave_de_slug("decreto-409-2026"))

    def test_el_lector_acierta_en_los_casos_de_control(self):
        # Un lector que se equivoca en un renglón conocido no sirve para los que nadie miró.
        self.assertEqual(
            self._normas_de("Decretos 407, 408 y 409/2026 (BO 01/06/2026): reglamentación de "
                            "la Ley 27.802"),
            ["407/2026", "408/2026", "409/2026", "27.802"],
            "el lector no abre la enumeración de decretos o pierde la ley del final")
        self.assertEqual(self._normas_de("PBA - Ley 15.513 (sancionada 12/12/2024)"), ["15.513"],
                         "el lector confunde una fecha con un número de norma")

    def test_cada_norma_listada_esta_declarada_o_tiene_veredicto(self):
        for renglon in self.renglones:
            corto = re.sub(r"\*\*|\s+", " ", renglon[2:]).strip()[:60]
            with self.subTest(corto):
                numeros = self._normas_de(renglon)
                self.assertTrue(numeros, f"«{corto}» no nombra ninguna norma reconocible")
                for numero in numeros:
                    clave = self._clave(numero)
                    self.assertTrue(clave in self.declarado or clave in self.con_veredicto,
                                    f"«{corto}» nombra la norma {numero}, que no está declarada "
                                    f"en normas.json ni tiene veredicto en "
                                    f"cobertura-revisada.json. No la reclama ninguna herramienta.")
class TestElDescriptionDeLaSkillActivaTodasLasRamas(unittest.TestCase):
    """El `description` del SKILL.md no describe: **enciende**. Un tema que no está ahí no llega.

    Es la diferencia con el `description` de un comando, que el usuario lee y decide. Éste lo
    lee el modelo para saber si la skill aplica, así que un módulo sin disparador es un módulo
    inalcanzable: la consulta se contesta con conocimiento general y el módulo auditado no se
    abre nunca. El daño no se ve, porque la respuesta sale igual.

    **Los disparadores se declaran, no se infieren del nombre del archivo.** «previsional.md»
    se activa con «jubilaciones» y «salud-discapacidad.md» con «prepaga»: nadie consulta usando
    el nombre del módulo. La tabla de abajo es esa declaración, y agregar un módulo de rama sin
    sumarle su disparador deja este test en rojo, que es exactamente lo que tiene que pasar.

    El límite del campo es de 1.536 caracteres contados junto con `when_to_use`, así que hay
    lugar; lo que no hay es margen para olvidarse de una rama.

    Mutación que lo comprueba: sacar «jubilaciones» del `description` del SKILL.md lo deja en
    rojo por `previsional.md`.
    """

    # Un disparador por módulo de rama: una palabra que alguien usaría al consultar.
    DISPARADORES = {
        "amparo.md": ("amparo",),
        "administrativo-nacional.md": ("acto administrativo", "agotamiento de la vía"),
        "ambiental.md": ("ambiental", "contaminación"),
        "civil.md": ("daños", "contratos"),
        "competencia.md": ("defensa de la competencia", "posición dominante"),
        "concursos.md": ("concursos", "quiebras"),
        "consumo-caba.md": ("proceso de consumo de la Ciudad", "conciliación previa"),
        "consumidor.md": ("consumidor", "abusivas"),
        "contencioso-pba.md": ("contencioso administrativa",),
        "contratos.md": ("contratos",),
        "datos-personales.md": ("datos personales", "hábeas data"),
        "derechos-reales.md": ("derechos reales", "usucapión", "propiedad horizontal"),
        "dipr.md": ("elemento extranjero", "jurisdicción internacional"),
        "empleo-publico.md": ("empleo público", "cesantía"),
        "ejecucion.md": ("ejecución de sentencia",),
        "firma-digital.md": ("firma digital", "documento electrónico"),
        "familia.md": ("alimentos", "divorcio"),
        "honorarios-caba.md": ("UMA",),
        "honorarios-nacional.md": ("UMA",),
        "honorarios-pba.md": ("jus",),
        "locacion.md": ("alquileres", "desalojo"),
        "laboral-riesgos.md": ("accidente de trabajo", "ART"),
        "violencia-digital.md": ("violencia digital", "difusión de material íntimo"),
        "laboral-licencias.md": ("licencia por maternidad", "suspensión disciplinaria"),
        "laboral.md": ("despido", "liquidación"),
        "laboral-colectivo.md": ("convenio colectivo",),
        "penal-leyes-especiales.md": ("hábeas corpus", "estupefacientes"),
        "notificaciones-pba.md": ("notificación electrónica",),
        "notarial.md": ("escribano",),
        "penal.md": ("penales", "excarcelación"),
        "penal-impugnacion.md": ("nulidad", "casación"),
        "penal-parte-general.md": ("probation", "prescripción"),
        "penal-juvenil-pba.md": ("penal juvenil",),
        "justicia-de-paz-pba.md": ("juzgado de paz",),
        "plazos.md": ("plazos", "prescripción"),
        "previsional.md": ("jubilaciones", "pensiones"),
        "propiedad-industrial.md": ("patentes", "marcas"),
        "proceso-nacional.md": ("proceso civil y comercial",),
        "proceso-pba.md": ("caducidad",),
        "prueba-pericial.md": ("prueba pericial",),
        "salud-discapacidad.md": ("prepaga", "discapacidad"),
        "sede-judicial-pba.md": ("veredicto", "sentencia"),
        "sede-judicial.md": ("órgano jurisdiccional",),
        # Los tres de sede comparten disparador a propósito: el `description` ENCIENDE la
        # skill y la tabla de ruteo de la 16 elige el fuero. Darle a cada uno su palabra no
        # compraría precisión: quien consulta dice que es el órgano, no el nombre de su
        # código procesal. Que hoy haya margen en el campo no cambia el criterio.
        "sede-judicial-nacional.md": ("órgano jurisdiccional",),
        "sede-judicial-caba.md": ("órgano jurisdiccional",),
        "salud-mental.md": ("salud mental", "internación involuntaria"),
        "seguros.md": ("seguros", "citación en garantía"),
        "societario.md": ("sociedades",),
        "sucesiones.md": ("sucesiones", "legítima"),
        "titulos-ejecutivos.md": ("pagaré", "cheque"),
        "telegramas.md": ("telegramas",),
        "transito.md": ("tránsito",),
        "tributario.md": ("tributario", "Fisco"),
        "tributario-pba.md": ("ARBA",),
        "previsional-pba.md": ("IPS",),
        "contravencional-caba.md": ("contravenciones de CABA",),
        "tributario-caba.md": ("AGIP",),
        "ejecucion-penal.md": ("ejecución de la pena",),
        "changelog-normativo.md": ("prescripción",),
        "fallos-csjn.md": ("penales",),
        "parte.md": ("escritos",),
    }

    def setUp(self):
        skill = Path(__file__).resolve().parents[1] / "SKILL.md"
        self.descripcion = re.search(r"(?m)^description: (.+)$",
                                     skill.read_text(encoding="utf-8")).group(1)
        self.refs = skill.parent / "references"

    def _activa(self, palabra: str) -> bool:
        """Por palabra completa, no por subcadena: `ART` está adentro de «parte» y daba por
        activado a `laboral-riesgos.md` sin que el término figurara. Con el tope en 1.024 eso
        deja de ser teórico — el recorte saca términos, y una rama apagada tiene que verse.

        MUTACIÓN que lo comprueba: sacar `ART` del `description` y este test falla; con la
        comparación por subcadena, pasaba.
        """
        return re.search(r"(?<!\w)" + re.escape(palabra) + r"(?!\w)",
                         self.descripcion, re.I) is not None

    def test_cada_modulo_de_rama_tiene_su_disparador(self):
        # La misma partición que usa `herramientas/pendientes.py`: un módulo de rama describe
        # derecho, uno de infraestructura describe cómo trabaja la skill.
        infraestructura = {"danos-indice-doctrinario.md", "escritos.md", "fuentes.md",
                           "intake.md", "marcadores.md", "modelos.md", "perfiles-heredados.md"}
        ramas = [f.name for f in sorted(self.refs.glob("*.md"))
                 if f.name not in infraestructura]
        self.assertGreater(len(ramas), 20, "no se encontraron los módulos de rama")
        sin_disparador = []
        for modulo in ramas:
            palabras = self.DISPARADORES.get(modulo)
            with self.subTest(modulo):
                self.assertIsNotNone(palabras,
                                     f"{modulo} es un módulo de rama y no declara disparador: "
                                     f"agregarlo a DISPARADORES y al description del SKILL.md")
                if palabras and not any(self._activa(p) for p in palabras):
                    sin_disparador.append(f"{modulo} ({'/'.join(palabras)})")
        self.assertEqual(sin_disparador, [],
                         "módulos de rama que el description no activa: " +
                         ", ".join(sin_disparador))

    def test_el_description_entra_en_el_limite(self):
        """**Son dos límites distintos y manda el más chico.** Claude Code trunca en 1.536 el
        `description` junto con `when_to_use` —que esta skill no usa— para ahorrar contexto: ahí
        pasarse cuesta disparadores. La API de Skills es otra cosa: pide *"description: Maximum
        1024 characters"* y por esa puerta la skill **no carga**, así que el tope es 1.024 y el
        1.536 queda como lo que es, una truncación de listado. Medido contra
        platform.claude.com/docs/en/api/skills-guide el 19/09/2026.

        Es el tope más caro del repositorio: cada carácter que entra es un disparador que no
        entra, y `test_cada_modulo_de_rama_tiene_su_disparador` es lo que impide que el
        recorte deje una rama apagada.
        """
        self.assertLessEqual(len(self.descripcion), 1024,
                             "el description pasa el límite de la API de Skills: ahí no carga")


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
