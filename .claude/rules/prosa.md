# Cómo se escribe, y qué lleva acento

Rige siempre: carga al abrir la sesión, no al tocar un `.md`, `.py` o `.json`.

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
`no está` puede ser el verbo o el demostrativo: *"pero no esta otra"* está bien escrito. Para esas
palabras **el control es la lectura, no el test**.

**Un barrido da candidatos, no culpables.** Buscar las palabras que el repo escribe de las dos
formas encuentra el problema entero de una vez, pero la decisión sigue siendo una lectura: `quater`
y `quantum` son voces latinas y el articulado las escribe sin tilde, así que ahí la fuente falló
en contra del barrido.

**Las fechas van en tres clases** y sólo una se ablanda: la del derecho —B.O., vigencia, fecha de
un fallo— es **exacta siempre**; la que lee una máquina —la columna de `changelog-normativo.md`, un
`fijado`, un `descargado`— es **exacta** o el medidor queda ciego; y la de nuestro propio trabajo va
**por mes**, porque una fecha al día invita a leer el repositorio como vencido el día 181.

**Las que escribimos nosotros van en hora argentina, con offset fijo `-03:00`.** Se lee como el
día en que lo hicimos, así que en UTC un trabajo de las nueve de la noche queda fechado al día
siguiente. Y el offset es fijo y no la zona del sistema porque el workflow de CI corre en UTC: con
`astimezone()` la misma corrida fecharía distinto según dónde se corra. Ningún script llama a
`date.today()` ni a `datetime.now(timezone.utc)` por su cuenta; usan el `hoy()` o el `ahora()` de
su árbol, y `TestUnaSolaZonaHoraria` sostiene que las tres declaraciones no se separen y que no
aparezca un cuarto reloj.
