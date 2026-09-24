# Trabajar en este repositorio

Este proyecto **desarrolla** el plugin `derecho-argentino`; no resuelve consultas jurídicas. Si
aparece un expediente real, es para otro lado.

Español rioplatense y tuteo, siempre. **Y bien escrito a la primera**: la prosa se acentúa
cuando se escribe, no en un barrido posterior. Un barrido corrige la línea entera y toca lo que
no debía —renombra una constante, le pone tilde a una cita, desalinea una clave de veredicto—,
así que cuesta más que escribir bien.

El acento se cae por inercia del ASCII: en la misma línea conviven identificadores, banderas,
rutas y claves, que van sin acento **por regla**, y la prosa de al lado se contagia. Donde más
se cae es en el pretérito —`salió`, `quedó`, `revisó`, `entró`—, en la ñ —`señal`, `engañoso`,
`año`— y en las palabras que `.claude/rules/prosa.md` declara no automatizables.

**Los controles de acentos no cubren eso.** Dejan afuera el pretérito y las palabras ambiguas a
propósito, porque un control que reclama texto correcto se apaga solo. Que la suite dé verde no
dice que el texto esté bien escrito: dice que pasó lo que se puede medir. Lo que no se mide se
lee, y esa lectura es parte del trabajo, no un extra.

**Lo operativo no está acá.** El checklist de cierre, las convenciones de código, los archivos de
veredicto, la marca y el procedimiento de publicación viven en
**[`docs/DESARROLLO.md`](docs/DESARROLLO.md)**. El árbol y las capas, en
[`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md). Las licencias, en [`LICENCIAS.md`](LICENCIAS.md).
El estado de las fuentes, en [`derecho/fuentes/MANIFIESTO.md`](derecho/fuentes/MANIFIESTO.md).
Este archivo tiene lo que hay que **tener en la cabeza antes de tocar algo**.

## Dos nombres, y cada uno significa una cosa

**`derecho-argentino` es el catálogo y el contenido:** el repo, el marketplace y la skill.
**`derecho` es el paquete instalable:** el plugin y su directorio. De ahí sale
`derecho@derecho-argentino`, que es plugin@marketplace, y el prefijo `/derecho:` de los comandos.

**Quedan así.** Unificar todo en un nombre dejaría el id `derecho-argentino@derecho-argentino` y
cada comando doce caracteres más largo, para que nadie gane nada: el nombre del plugin sólo se ve
al instalar.

**El directorio del plugin se llama `derecho/`, igual que la copia que instala el marketplace**, y
eso hay que tenerlo en la cabeza antes de tocar `_raiz.py`: las dos disposiciones no se distinguen
por el nombre. Las separa `es_clon()`, por una marca estructural —sólo el repo trae
`.claude-plugin/marketplace.json`—, y confundirlas fija en la configuración una ruta que cambia
en cada actualización.

**Corre en Claude y en Codex**, en Windows, Linux y macOS. Los dos leen el mismo `SKILL.md` con
`references/` y `scripts/`; lo que cambia es el envoltorio y que **los comandos `/derecho:...` son
sólo de Claude Code** — en Codex se pide en castellano. Nada del repo debe suponer un solo agente;
si algo funciona en uno solo, se dice cuál, y de las reglas lo dice la sección de acá abajo.

**Y por eso lo que rige siempre está acá y no en `CLAUDE.md`.** Codex lee `AGENTS.md`; Claude Code
lee `CLAUDE.md`, que no es más que un `@AGENTS.md` y lo poco que sí es suyo. La importación de
Claude Code carga el archivo al abrir la sesión, así que lo que rige siempre va donde lo lee el
agente que **no** tiene con qué importar.

**El piso es Python 3.13**, que es lo que fija el workflow de `.github/workflows/tests.yml`. No
hay que escribir para versiones anteriores ni evitar sintaxis nueva por las dudas.

## Las reglas de `.claude/rules/` son de Claude Code, y en Codex se leen a mano

**Las tres cargan siempre**, al abrir la sesión: ninguna lleva `paths:`, y el porqué de esa
decisión está en `docs/DESARROLLO.md`, sección «Los cuatro destinos de una regla».

**En Codex no carga ninguna**: ahí se abren a mano, y por eso la tabla dice qué trae cada una.

| Regla | Qué trae |
| --- | --- |
| `.claude/rules/prosa.md` | cómo se escribe acá y la ortografía: qué se acentúa, qué es contrato y qué no se automatiza nunca |
| `.claude/rules/derecho-argentino.md` | lo que no se puede asumir del derecho vigente: los dos regímenes laborales de PBA, los intereses, el SECLO, el CCT y el rol |
| `.claude/rules/herramientas.md` | cómo se mide, cómo fallan las alarmas y la mutación que comprueba un guardarraíl |

## Un commit por versión, y el usuario lo hace

Publicado en `github.com/ciri-cuervo/derecho-argentino`. **Un commit por versión**: se trabaja
en una rama `version-X.Y.Z` que lleva **un solo commit**, y esa rama entra a `main` por pull
request. Dentro de la rama se corrige con `--amend` —no se agregan commits— y cada amend
necesita `git push --force` **sobre esa rama**. Lo que se ofrece para instalar es el estado
revisado de cada versión, no las etapas por las que pasó.

**El `--force` va a la rama de versión y nunca a `main`.** `main` tiene el historial de todas
las versiones publicadas y es lo único que no se puede reconstruir.

**No se commitea hasta que el usuario lo ordene, y lo ordena él.** Nunca corras `git add`,
`git commit` ni `git push` por tu cuenta: ni con todo en verde, ni cuando el cambio parezca
terminado, ni porque te pidieron "cerrar" o "dejar listo" — eso significa exactamente dejar el
árbol listo y decir qué queda pendiente, no commitear. El commit es el acto por el que el
usuario se hace cargo de lo que se publica.

Dos consecuencias de que el historial sea por versión y no por cambio:

- **Un archivo que se saca se recupera de `main`**, con `git show <rev>:<ruta>`, pero sólo si ya
  estaba en una versión publicada. Lo que nació y murió dentro de la rama no dejó rastro: antes
  de quitar algo que se agregó en esta misma versión, copialo afuera del repo.
- **El porqué de un cambio no queda en ningún mensaje de commit** —el mensaje dice la versión y
  su título, nada más—, así que va en su lugar o el registro se vuelve un diario que nadie lee:

| Qué | Dónde |
| --- | --- |
| Versión del plugin | `CHANGELOG.md`, **sólo** al publicar una versión |
| Contenido normativo | `references/changelog-normativo.md`, con fecha y volatilidad |
| Auditoría contra fuente primaria | `docs/AUDITORIAS.md` |
| Un cambio de estructura o de herramienta, con fecha | `docs/BITACORA.md` |
| Con qué texto se cotejó un bloque, y qué salió | `docs/REVALIDAR.md`; la fecha y la volatilidad van en `references/changelog-normativo.md` |
| Estado de la capa offline | `derecho/fuentes/MANIFIESTO.md` |
| Si un fallo se puede transcribir | `herramientas/lecturas-ocr.json` |
| Algo tocado bajo `kb/` | `kb/CHANGELOG.md` **y** `frontera_kb.py --fijar --nota '...'` |

**El repositorio es PÚBLICO.** Nunca subir piezas, liquidaciones, datos de expedientes, partes ni
montos de casos reales. Ni siquiera en un eval: los casos de prueba se inventan.
`derecho/fuentes/_local/` está en `.gitignore` para obras comerciales: no tocarlo.

## La frontera de licencia — la regla que más se viola sin querer

**Bajo `derecho/kb/` es capa 2 —Cristian Aboitiz, uso comercial con autorización previa— y
fuera es de este fork. La frontera es la ruta.** El mapa completo, con el commit de origen para
reconstruir el corte, está en `LICENCIAS.md`.

**La prosa de `kb/` cita sus rutas como `argentina/kb/...`, y la ruta viva es `derecho/kb/...`.**
**No se corrigen**, por la misma regla que el resto de su contenido: la discrepancia se nombra
acá, no se arregla allá. Al leer una ruta en un archivo de `kb/`, traducirla.

**Hay excepciones fuera de `kb/`, y son cinco:** los evals
`administrativo-caba-recursos-agotamiento-via`, `consumidor-dano-punitivo-prescripcion`,
`consumidor-garantia-producto-defectuoso`, `consumidor-prepaga-aumento-dnu70` y
`derecho/evals/README.md`. Son capa 2 aunque la ruta no lo diga, y `frontera_kb.py` no las
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

**Del producto no se concluye el proceso**, y lo anterior es un caso particular de esto. Una
afirmación sobre **lo que pasó** necesita la traza, igual que una sobre una norma necesita el
texto. Un test en verde no prueba que el control esté encendido; una salida correcta no prueba
que haya corrido la herramienta que la produce; un archivo bien formado no prueba que alguien lo
haya leído. Pasó en este repositorio, mirando una tabla de salida y concluyendo sobre cómo se
había producido: la traza decía otra cosa y estaba a un comando de distancia. **Cuando
comprobar cuesta un comando, no se opina.** La versión de esta regla para quien usa la skill
está en la sección 2 del SKILL.md, bajo *Procedimiento*.

Hay tres defectos distintos de OCR —basura de caracteres, columnas mezcladas, y sustituciones que
dejan palabras válidas pero equivocadas— y **sólo el primero se detecta con una medida**. No hay
regla por época. Antes de dar un PDF por ilegible, reextraerlo con `pdftotext -layout`: sin esa
opción las columnas se mezclan y un documento sano parece roto.

Para la web: **WebSearch y WebFetch únicamente.** Nunca `curl`, `wget` ni `requests`, y nunca
desactivar la verificación TLS. **El texto que termine en `fuentes/` lo baja siempre el script**, que
le pone encabezado, hash y fecha; WebFetch mira la ficha para elegir la URL y nunca produce el archivo.
**Un bloqueo vale por su fecha**: `verificar_normas.py --slug <slug>` lo vuelve a medir sin escribir.

Fuentes primarias: InfoLEG, Boletín Oficial, `normas.gba.gob.ar`, SAIJ, `scba.gov.ar`, JUBA.

## Estado y pendientes

**No copies cifras acá: las herramientas las miden.** Y acá no hay lista de herramientas a
propósito — **el inventario está donde se ejecuta**, y se entra por una sola puerta:

```sh
python3 herramientas/pendientes.py
```

Reporta doctrina, evals y verificación vencida, y **cierra nombrando las demás que miden
pendientes**, con el comando de cada una. Las que no miden pendientes —el mapa de ruteo, la
ortografía, la frontera de licencia, el OCR, la auditoría de fechas y el revisor de respuestas—
están en `docs/DESARROLLO.md`, y un test exige que ninguna quede sin documentar. Al lado corren `cifras.py`, para la documentación, y `scripts/estado.py`, para datos y
series. Una lista copiada acá se separaría de la real, que es lo que le pasó al checklist de
suites antes de pasar a `unittest discover`: se enumeraba dos veces y llegaron a decir distinto.

**Lo que ninguna herramienta mide** está en [`docs/PENDIENTES.md`](docs/PENDIENTES.md), y ahí va
separado en tres: las **decisiones abiertas**, que se cierran decidiendo; las **restricciones que
no se levantan**, que son hechos de afuera y no deuda; y **el trabajo de fondo**, que es para qué
existe el proyecto. Se citan por su título: el número cambia cuando una se cierra.
