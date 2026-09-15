# Trabajar en este repositorio

Este proyecto **desarrolla** el plugin `derecho-argentino`; no resuelve consultas jurídicas. Si
aparece un expediente real, es para otro lado.

Español rioplatense y tuteo, siempre.

**Lo operativo no está acá.** El checklist de cierre, las convenciones de código, los archivos de
veredicto, la marca y el procedimiento de publicación viven en
**[`docs/DESARROLLO.md`](docs/DESARROLLO.md)**. El árbol y las capas, en
[`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md). Las licencias, en [`LICENCIAS.md`](LICENCIAS.md).
El estado de las fuentes, en [`argentina/fuentes/MANIFIESTO.md`](argentina/fuentes/MANIFIESTO.md).
Este archivo tiene lo que hay que **tener en la cabeza antes de tocar algo**.

## Tres nombres que se confunden

El marketplace es `derecho-argentino`, el plugin es `derecho` y la skill es `derecho-argentino`.
De ahí sale `derecho@derecho-argentino`, que es plugin@marketplace. **Quedan así:** el comando ya
está publicado. El directorio del plugin se llama `argentina/` a propósito — renombrarlo tocaría
cientos de rutas para algo que el usuario no ve.

**Corre en Claude y en Codex**, en Windows, Linux y macOS. Los dos leen el mismo `SKILL.md` con
`references/` y `scripts/`; lo que cambia es el envoltorio y que **los comandos `/derecho:...` son
sólo de Claude Code** — en Codex se pide en castellano. Nada del repo debe suponer un solo agente;
si algo funciona en uno solo, se dice cuál.

**El piso es Python 3.13**, que es lo que fija el workflow de `.github/workflows/tests.yml`. No
hay que escribir para versiones anteriores ni evitar sintaxis nueva por las dudas.

## Un solo commit, y el usuario lo hace

Publicado en `github.com/ciri-cuervo/derecho-argentino`, **un solo commit sin padres**: lo que se
ofrece para instalar es el estado revisado, no las etapas. Se trabaja con `--amend`, no se agregan
commits, y cada amend necesita `git push --force`.

**No se commitea hasta que el usuario lo ordene, y lo ordena él.** Nunca corras `git add`,
`git commit` ni `git push` por tu cuenta: ni con todo en verde, ni cuando el cambio parezca
terminado, ni porque te pidieron "cerrar" o "dejar listo" — eso significa exactamente dejar el
árbol listo y decir qué queda pendiente, no commitear. El commit es el acto por el que el
usuario se hace cargo de lo que se publica, y con un solo commit y `--force` no hay a dónde
volver si se equivocó el momento.

Dos consecuencias de no tener historial:

- **Sacar un archivo lo borra para siempre.** Antes de quitar algo, copialo afuera del repo.
- **El porqué de un cambio no queda en ningún mensaje de commit**, así que va en su lugar o el
  registro se vuelve un diario que nadie lee:

| Qué | Dónde |
| --- | --- |
| Versión del plugin | `CHANGELOG.md`, **sólo** al publicar una versión |
| Contenido normativo | `references/changelog-normativo.md`, con fecha y volatilidad |
| Auditoría contra fuente primaria | `docs/AUDITORIAS.md` |
| Estado de la capa offline | `argentina/fuentes/MANIFIESTO.md` |
| Si un fallo se puede transcribir | `herramientas/lecturas-ocr.json` |
| Algo tocado bajo `kb/` | `kb/CHANGELOG.md` **y** `frontera_kb.py --fijar --nota '...'` |

**El repositorio es PÚBLICO.** Nunca subir piezas, liquidaciones, datos de expedientes, partes ni
montos de casos reales. Ni siquiera en un eval: los casos de prueba se inventan.
`argentina/fuentes/_local/` está en `.gitignore` para obras comerciales: no tocarlo.

## La frontera de licencia — la regla que más se viola sin querer

**Bajo `argentina/kb/` es capa 2 —Cristian Aboitiz, uso comercial con autorización previa— y
fuera es de este fork. La frontera es la ruta.** El mapa completo, con el commit de origen para
reconstruir el corte, está en `LICENCIAS.md`.

**Hay excepciones fuera de `kb/`, y son cinco:** los evals
`administrativo-caba-recursos-agotamiento-via`, `consumidor-dano-punitivo-prescripcion`,
`consumidor-garantia-producto-defectuoso`, `consumidor-prepaga-aumento-dnu70` y
`argentina/evals/README.md`. Son capa 2 aunque la ruta no lo diga, y `frontera_kb.py` no las
vigila. No se corrigen: **ni el contenido ni la ortografía.**

`kb/` queda, con atribución y licencia propia. Lo que ordena la convivencia son dos cosas de los
módulos: las filas *"Absorbido: ya no se rutea al perfil"* y los bloques de **contradicciones
nominadas**, que dicen punto por punto dónde el perfil heredado dice lo contrario y con qué norma
se resuelve. Un test exige que la cita del perfil sea **verbatim** contra `kb/`.

Se cruza **en los dos sentidos** y cada uno tiene su herramienta: prosa de `kb/` que entra a un
módulo, `fuga_textual.py`; texto propio que sale hacia `kb/`, `frontera_kb.py`.

El segundo es el fácil de cruzar sin darse cuenta, porque **se cruza corrigiendo**: el perfil dice
algo mal y la tentación es arreglarlo donde se lee. No va ahí. Encima **desactiva al primero**,
porque reescribir una línea de `kb/` con palabras propias hace desaparecer la coincidencia que el
detector busca. La corrección va al módulo, y el bloque de contradicciones nombra el error
citándolo textual.

`fuga_textual.py` reporta **candidatos, no culpables**. **La trampa no es copiar, es condensar:**
dos resúmenes de la misma fuente convergen sin que nadie lea al otro. Citar textual al tribunal,
entre comillas, lo evita y además cita.

## Disciplina de verificación — es el valor del proyecto entero

No se afirma una norma, un plazo ni un fallo **sin fuente primaria a la vista**. Ante la duda,
marcador canónico que diga qué falta; nunca una estimación plausible. El vocabulario válido es el
de `references/marcadores.md`, y tiene dos clases que no se cuentan igual: los que el módulo lleva
**pre-colocados** y los que la skill **emite en tiempo de ejecución** sobre lo que trae el usuario.

**Un fallo bajado no es un fallo leído.** Carátula, cita y fecha salen del registro oficial; el
holding se escribe **después** de abrir el documento. Y la carátula es uno de los cinco datos que
nunca se reconstruyen: si el dato guardado está degradado, se recupera **del documento**, no de la
memoria ni del idioma. Los diacríticos de un nombre propio salen del documento; los de un
sustantivo común pueden salir del idioma, y eso se anota.

Hay tres defectos distintos de OCR —basura de caracteres, columnas mezcladas, y sustituciones que
dejan palabras válidas pero equivocadas— y **sólo el primero se detecta con una medida**. No hay
regla por época. Antes de dar un PDF por ilegible, reextraerlo con `pdftotext -layout`: sin esa
opción las columnas se mezclan y un documento sano parece roto.

Para la web: **WebSearch y WebFetch únicamente.** Nunca `curl`, `wget` ni `requests`, y nunca
desactivar la verificación TLS. InfoLEG y `normas.gba.gob.ar` dan 403 a los agentes: esos
descargadores los corre el usuario en su terminal. El navegador sirve para mirar una ficha, pero
**el texto que termine en `fuentes/` lo baja siempre el script**, que es lo que le pone
encabezado, hash y fecha.

Fuentes primarias: InfoLEG, Boletín Oficial, `normas.gba.gob.ar`, SAIJ, `scba.gov.ar`, JUBA.

## Contexto jurídico que no se puede asumir mal

**Fuero laboral PBA: conviven dos regímenes.** El art. 88 de la Ley 15.057 derogó la Ley 11.653,
pero la Res. SC 1840/2024 la aplicó sólo a las causas **sin audiencia de vista celebrada**; las
anteriores siguen bajo la 11.653 por ultraactividad. Nunca asumir uno de los dos.

**Intereses laborales:** los arts. 54, 55 y 56 son **de la Ley 27.802**, no de la LCT. Se citan
como art. 276 LCT (créditos nuevos), art. 55 de la Ley 27.802 (norma autónoma, juicios en trámite)
y art. 277 LCT (pago en cuotas). El art. 54 LCT está derogado por el art. 207.

**SECLO no aplica en PBA.** La mediación de la Ley 13.951 no suspende la prescripción como la
nacional: tiene efecto de intimación (art. 2541 CCyCN, seis meses, una sola vez).

**El CCT no es dato de cartera:** surge de lo que las partes invocan y prueban.

**La skill no asume el rol de quien consulta ni el fuero:** los pregunta al abrir. El perfil de
usuario ordena las opciones, no las elige. Es deliberado y no se relaja.

## Cómo se escribe acá

**Nada de recorte por área.** No decir que la skill "cubre en profundidad" ciertas materias ni que
tiene "foco" en ciertos fueros: está en desarrollo temprano y va a cubrir todos. El alcance se
enuncia como derecho argentino, y que la cobertura auditada crece. Los temas concretos sí van en
los disparadores del `description` de la skill: eso es lo que la activa.

**Nada de narrativa de antes y ahora.** No documentar problemas resueltos ni estados anteriores.
Se escribe el **estado** y la **regla** que lo sostiene. Cuando la lección viene de un error
propio, queda la regla y el guardarraíl; el error sirve de ejemplo, no de crónica. Un registro de
verificación sí lleva fecha: vale por su fecha.

**No repitas una cifra que un test ya verifica en otro archivo.** Es la forma más común de que el
repo se contradiga solo. Las cifras de inventario las genera `herramientas/cifras.py` desde una
sola medición, y su censo falla si aparece una cifra nueva sin declarar.

Ir al grano. Antes de tocar un archivo, leerlo. Antes de afirmar algo del repo, **medirlo con un
comando en vez de recordarlo** — y ojo con el filesystem case-insensitive de macOS y con los
basenames repetidos al comparar árboles.

Cuando encuentres un error propio, **decilo y arreglalo, no lo minimices**: un error normativo
silencioso es peor que un rechazo. Preferir borrar y reescribir antes que acumular capas de
advertencias sobre algo dudoso.

## Ortografía: la prosa en castellano, los identificadores en ASCII

**La regla es una: si se muestra, se acentúa; si se compara, no.** Vale para los `.md`, para los
comentarios y docstrings de los `.py`, para las cadenas que un script imprime y para los campos de
prosa de los `.json`.

**Y hay nueve cosas que parecen prosa pero son contrato.** Acentuarlas rompe, a veces con un
`KeyError` y a veces en silencio:

| No se acentúa | Por qué |
| --- | --- |
| Una clave de JSON, y todo valor comparado con `==` o usado de clave | El código deja de encontrarlo |
| Un grupo nombrado de regex: `(?P<despues>...)` | Es un identificador de Python |
| Un valor de `choices` del CLI y su mención en un mensaje | El usuario tiene que poder tipearlo |
| Un nombre de archivo, un slug de eval, el `name:` de un comando | La ruta no existe |
| El `src` de una imagen y el **path** de una URL | La imagen no carga; el path va percent-encodeado |
| Texto fijado por hash — el encabezado de los `.txt` de OCR | Cambiarlo exige correr el OCR de nuevo, no editar |
| Los `problema` de `revisar_texto()` | Se comparan contra `revisiones.json` |
| Las listas de palabras de los guardarraíles | Son las formas **sin** acento que detectan |
| Una variable, un atributo, el nombre de un test | Son identificadores |

**Reglas antes que listas.** En castellano ninguna palabra termina en `-cion` o `-sion` sin tilde:
eso es una regla y no admite excepción. Una lista de palabras, en cambio, arrastra ambigüedad y
**corregir por lista introduce errores**.

**Estas no se automatizan nunca**, porque existen de las dos formas y el contexto decide:

    aun · mas · esta · practica · publica · titulo · numero · calculo · computo
    modulo · linea · rubrica · hacia · bajo · cambio · critica · continua · termino

`aun` significa *incluso* y `aún` significa *todavía*; en `aun cuando` y `aun así` va sin tilde.
`no esta` puede ser el verbo o el demostrativo: *"pero no esta otra"* está bien escrito. Para esas
palabras **el control es la lectura, no el test**.

**Un barrido da candidatos, no culpables.** Buscar las palabras que el repo escribe de las dos
formas encuentra el problema entero de una vez, pero la decisión sigue siendo una lectura: `quater`
y `quantum` son voces latinas y el articulado las escribe sin tilde, así que ahí la fuente falló
en contra del barrido.

**Las fechas van en tres clases** y sólo una se ablanda: la del derecho —B.O., vigencia, fecha de
un fallo— es **exacta siempre**; la que lee una máquina —la columna de `changelog-normativo.md`, un
`fijado`, un `descargado`— es **exacta** o el medidor queda ciego; y la de nuestro propio trabajo va
**por mes**, porque una fecha al día invita a leer el repositorio como vencido el día 181.

## Cómo se mide, y cómo fallan las medidas

**Una medida que se equivoca sobre un caso conocido no sirve para los desconocidos: se descarta, no
se calibra.** Cuando no haya medida confiable, se lee y se registra el veredicto, con fecha y con
lo que se vio.

Las alarmas fallan de dos maneras, y las dos se buscan a propósito:

- **La que suena siempre** se calla con `--fijar` o se deja de mirar, y ahí se pierde el cambio real.
- **La que no suena nunca** reporta verde con el instrumento apagado. Es la peor: da confianza.

Si una herramienta no puede medir —falta un binario, falta una fuente— **lo dice y se planta**. No
hay verde por ausencia de instrumento.

**Después de agregar un guardarraíl, comprobalo con una mutación**: reintroducí el error que
debería atrapar y confirmá que falla. Dos cosas que se aprenden rompiéndolas:

- **A veces hay que mutar el alcance del control, no un archivo.** A las clases de letras de los
  regex les faltaba la `Ü`, así que `[VERIFICAR ANTIGÜEDAD: ...]` no era ni candidato: el control
  lo ignoraba en silencio y todo daba verde.
- **Un guardarraíl sólo cubre lo que su fixture ejercita.** Una nota que se imprime únicamente
  cuando el plazo cruza a otro año no está cubierta si el caso de prueba no lo cruza.

**Antes de reformatear en masa, buscá quién parsea eso.** Buena parte de las medidas de este
repositorio salen de leer los `.md` con un regex, así que un cambio de forma que a la vista no dice
nada les cambia la entrada. Y el parser no protesta: sigue, lee otra cosa y **reporta cero**. Pasó
con el relleno de las filas de tabla y `pendientes.py`.

Los archivos que la mutación necesite crear van al scratch de `/tmp`, porque adentro del repo **no
se pueden borrar**. Cuando la mutación tenga que estar adentro para que el guardarraíl la vea,
moverla a `_to_delete/` **en el mismo acto**, y avisar de `rm -rf _to_delete` antes de commitear.

## Estado y pendientes

**No copies cifras acá: las herramientas las miden.**

```sh
python3 herramientas/pendientes.py            # doctrina, evals y verificación vencida
python3 argentina/skills/derecho-argentino/scripts/estado.py   # datos y series
python3 herramientas/cobertura_normativa.py   # normas citadas sin bajar
python3 herramientas/calidad_ocr.py --pendientes   # jurisprudencia sin leer
python3 herramientas/cifras.py                # cifras de la documentación y censo
```

Lo que ninguna herramienta mide todavía:

1. **Las normas declaradas en `normas.json` que no tienen URL oficial son estructurales, y no la
   van a tener.** Una es la Ley 13.478, de 1948, que InfoLEG no publica por época; la otra, la
   publicación de los once instrumentos del art. 75 inc. 22 en un solo documento. Están en el
   catálogo para que se vea que faltan, y el motivo de cada una está escrito en su entrada.
2. **`docs/AUDITORIAS.md` está fuera del checklist de fuga** y tiene secuencias sin revisar, de
   entradas viejas. Se leen una por una, **no** se aceptan en masa.
3. **`reformas_no_leidas.py` compara por norma, no por artículo.** Si un módulo nombra una ley por
   una reforma, el detector la da por absorbida y otra reforma de la misma ley pasa sin mirarse.
   Ya costó una atribución equivocada.
4. **Falta una revisión completa de ortografía y gramática de los documentos internos.** Lo
   automatizable ya está: las reglas de arriba, con sus guardarraíles. Lo que queda es una lectura
   entera de los `.md`, de los comentarios, docstrings y cadenas de los `.py`, y de los campos de
   prosa de los `.json` —carátulas, títulos de norma, `nota`, `motivo`, `_descripcion`—, que ningún
   test reemplaza: las palabras que existen de las dos formas se deciden leyendo, y la gramática no
   se mide con un regex. En los `.json` la mitad del archivo es contrato, así que la revisión va
   campo por campo y no por archivo: una clave o un valor que se compara no se toca. Las cinco
   excepciones de capa 2 quedan afuera: no se les corrige la ortografía.
5. **Los casos de prueba están en un formato propio y `claude plugin eval` lee otro.** El nativo es
   `prompt.md` con `graders/*.md` —o `case.yaml`— y lo corre el comando con arm de ablación sin
   plugin; el nuestro es la terna `caso.md`, `rubrica.md` y `resultado.md`, que se lee a mano. El
   manifiesto ya declara `experimental.evals`, y `laboral-despido-tramos-reforma-pba` ya está
   migrado y sirve de molde. Dos cosas a decidir en la migración: si la terna se reemplaza o
   convive —`rubrica.md` dice en prosa lo que los graders dicen ejecutable, y `resultado.md` es un
   registro fechado de lo que se vio— y qué pasa con los casos heredados de capa 2, que se pueden
   envolver pero no reescribir.
6. **El plugin tiene que contener mucho más derecho del que contiene.** Es el trabajo de fondo, no
   mantenimiento: fueros nuevos, más normas bajadas y auditadas, más jurisprudencia leída. El
   alcance enunciado es el derecho argentino y lo auditado es una fracción — la respuesta es
   agrandar lo cubierto, nunca ablandar la disciplina ni recortar la promesa.
   Un fuero nuevo entra entero o no entra: módulo con fuente primaria a la vista, normas bajadas por
   el descargador, fallos **leídos** y su caso de prueba. Sin el caso, `pendientes.py` lo reporta
   como módulo que ningún eval nombra, y tiene razón.
   Y **ninguna herramienta dice qué falta**, porque todas miden contra lo declarado:
   `cobertura_normativa.py` reporta la norma que un módulo cita y no bajamos, no la que ningún
   módulo cita todavía. El orden en que crece se decide leyendo, y para eso está
   [`docs/COBERTURA.md`](docs/COBERTURA.md): una taxonomía traída de fuentes externas —CONEAU, el
   Tesauro SAIJ, planes de estudio, institutos de los colegios y los fueros de Nación y PBA—
   cruzada contra lo que el repositorio cubre. Es un mapa fechado para decidir el orden, **no un
   enunciado de alcance**: el alcance sigue siendo el derecho argentino.
7. **Las reglas del linter de Markdown quedaron flojas y hay que endurecerlas.** `MD013` con el
   tope alto, y `MD040` —cercas sin lenguaje—, `MD028` —blanco dentro de un blockquote— y `MD001`
   —encabezado que salta un nivel— todavía avisan. **Mientras avise, una corrida limpia no
   significa nada y nadie la mira**, que es la alarma que suena siempre. El objetivo es que cada
   regla esté arreglada y encendida, o apagada con el motivo escrito al lado como las que ya lo
   tienen, y recién entonces discutir si entra al checklist. Ojo con el orden: `--fix` reescribe,
   así que primero se busca quién parsea lo que va a cambiar. Y lo que valga la pena se reimplementa
   en `test_markdown.py`: `MD051` se apagó porque su slugger no reproduce a GitHub, y el nuestro sí.

8. **Nada detecta una deuda escrita que ya se cumplió.** Un módulo dice "falta bajar la Ley X" o
   emite un marcador diciendo que algo "no está cargado en `fuentes/`", se baja, y **el reclamo
   sobrevive al hecho**. Lo peor no es el renglón viejo: es que una lista de deuda con entradas
   falsas se deja de leer entera, y con ella las que sí importan. Es la alarma que suena siempre.
   Se encontraron cuatro de esas leyendo, y hay que buscarlas leyendo cada vez que se baja algo.
   **No se puede automatizar como está.** Se intentó y se descartó: inferir de la prosa *cuál*
   norma se declara faltante acierta en menos de la mitad de los renglones reales, porque el
   sujeto de la frase puede ir después, o no ser una norma sino un fallo, un régimen provincial
   o una lista de leyes de adhesión — y "los umbrales del Título IX de la Ley 27.430 no están cargados" es cierto aunque
   la ley esté bajada, porque lo que falta son los montos. La salida sería que un reclamo de
   faltante **nombre el slug** en vez de la norma en prosa, y ahí el test es exacto y trivial.
   Toca la convención de `references/marcadores.md`: está sin decidir.
9. **Los registros judiciales oficiales no se pueden BUSCAR, sólo abrir.** JUBA opera por postback
   de ASP.NET y no admite consulta por query string; el buscador de sumarios de la CSJN devuelve
   HTTP 500 y el de fallos es POST sin parámetros; SAIJ responde 403 a los agentes. Se puede
   abrir un documento cuyo id ya se conoce —en la CSJN, **sólo** por
   `sjconsulta.csjn.gov.ar/sjconsulta/documentos/verDocumentoById.html?idDocumento=N`, porque el
   otro visor devuelve la ficha— pero **encontrar** el fallo depende de una búsqueda de afuera.
   Eso pesa directo sobre el punto 6, que es donde está el trabajo de fondo: ampliar la
   jurisprudencia leída es más caro de lo que parece, y el cuello no es leer sino ubicar.

Fuera del repo, en `~/develop/derecho-argentino-marca/`, vive el generador de la marca con su
propio README — la única parte con dependencias externas. El detalle, en
`docs/DESARROLLO.md § La marca`.
