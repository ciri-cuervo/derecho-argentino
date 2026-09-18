# 🔧 Desarrollar el plugin

Acá está lo operativo: cómo probar, qué correr antes de cerrar un cambio y las convenciones de
código. Las reglas de criterio —la frontera de licencia, la disciplina de verificación, qué no
se asume del derecho argentino y cómo se escribe acá— están en [`AGENTS.md`](../AGENTS.md), en
la raíz del repositorio.

## Probar sin instalar

Para trabajar sobre el plugin sin reinstalarlo en cada cambio, se carga el directorio
directamente:

```sh
claude --plugin-dir /ruta/al/repo/argentina
```

Ya dentro de la sesión, después de editar cualquier archivo:

```text
/reload-plugins
```

Los cambios se toman sin reiniciar. Si el plugin además está instalado desde un marketplace, **la
copia de `--plugin-dir` tiene precedencia** en esa sesión, así que no hace falta desinstalarlo
para probar.

Para probar el marketplace completo antes de publicarlo, se lo puede agregar por ruta local:

```sh
claude plugin marketplace add /ruta/al/repo
claude plugin install derecho@derecho-argentino
```

Ojo con esto último: instalar hace una copia, así que los cambios posteriores en el repo **no** se
ven hasta reinstalar. Para iterar, `--plugin-dir`.

Otros comandos útiles: `/plugin list`, `/plugin marketplace list`,
`/plugin uninstall derecho@derecho-argentino`, y `/help` → *Custom commands* para confirmar que
los ocho comandos slash quedaron registrados.

## En qué máquinas corre

Windows, Linux y macOS. **Python 3 y nada más** para la skill, los descargadores y la mayoría
de las herramientas: no hay `requirements.txt` ni entorno virtual que armar.

Tres herramientas necesitan binarios que no son de Python, y **ninguna de ellas hace falta
para usar la skill** — son de auditoría del repositorio:

| Herramienta | Necesita | macOS | Linux | Windows |
| --- | --- | --- | --- | --- |
| `auditar_fechas_fallos.py` · `calidad_ocr.py` | `pdftotext` | `brew install poppler` | `apt install poppler-utils` | `choco install poppler` |
| `reocr_jurisprudencia.py` | `pdfinfo`, `pdftoppm`, `tesseract` con español | `brew install poppler tesseract tesseract-lang` | `apt install poppler-utils tesseract-ocr tesseract-ocr-spa` | `choco install poppler tesseract` |

Si falta el binario, la herramienta **se planta con un mensaje que dice qué instalar**
(`herramientas/_externos.py`). El modo de falla que eso evita es el peor: un `FileNotFoundError`
atrapado junto con el de un PDF roto imprime cero hallazgos y sale con código 0, así que en una
máquina sin poppler la auditoría entera pasa sin mirarse. La regla —**no hay verde por ausencia de
instrumento**— está en `.claude/rules/herramientas.md`.

### Fines de línea

`.gitattributes` fija `eol=lf` para todo el repositorio. **No es cosmética tampoco.**
`frontera_kb.py` es el guardarraíl de la frontera de licencia: fija el sha256 de los 109
archivos de `derecho/kb/`, que son capa 2 y de otro autor. Medido: con un checkout CRLF
**cambian todos los hashes** sin que cambie una letra, y con las claves en formato nativo
**dejan de matchear todos menos tres**. El script reportaría la capa 2 entera como alterada, y
una alarma que suena entera se calla con `--fijar` — que acepta a ciegas el estado de `kb/`,
justo lo que el guardarraíl existe para impedir.

Por eso hay dos defensas y no una: `.gitattributes` normaliza en el checkout, y `huella()`
hashea el **texto con los saltos normalizados** y arma las claves con `as_posix()`, por si el
clon llegó de otra forma. Un cambio real de contenido sigue moviendo el hash: hay tests de
mutación que lo comprueban en las dos direcciones.

## Antes de dar por terminado un cambio

```sh
claude plugin validate ./derecho --strict
python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
python3 -m unittest discover -s herramientas -p "test_*.py"
python3 derecho/skills/derecho-argentino/scripts/estado.py
python3 herramientas/fuga_textual.py derecho/skills/derecho-argentino/SKILL.md \
    derecho/skills/derecho-argentino/references/*.md derecho/evals/*/*.md docs/AUDITORIAS.md
python3 herramientas/frontera_kb.py
python3 herramientas/deuda_vencida.py
```

En orden: que el plugin sea válido; que corran **los dos árboles de suites**, el de la skill y el
de `herramientas/`; que los nueve bloques de datos estén al día; que no se haya filtrado prosa de
`kb/` a un módulo de la capa 3; que `kb/` —que es de otro autor— no haya cambiado sin que nadie lo
decida; y que ningún reclamo de faltante haya quedado desmentido por `fuentes/`.

**Los dos árboles se descubren, no se enumeran, y esa es la razón.** Un test que no está en el
checklist es un test apagado, y uno apagado es peor que uno que no existe: figura en el conteo y
nadie lo corre. Con `unittest discover` **no hay lista de la que caerse**: un archivo nuevo que
empiece con `test_` entra solo, acá y en CI.

> **Antes se enumeraban, y divergieron.** El checklist llegó a nombrar seis suites mientras
> `tests.yml` corría cinco, y para sostenerlo hubo que escribir sendos tests que cruzaban una
> lista contra la otra. Esos tests existían **por** la enumeración: al sacarla, se fueron con
> ella. Es
> el caso donde una propiedad estructural reemplaza a un guardarraíl, que es la única forma de
> sacar un control sin perder lo que cuidaba.

**Los dos árboles no comparten `discover`** porque no comparten raíz: `scripts/` cuelga de la
skill y `herramientas/` de la del repo. Por eso el checklist trae un comando por árbol, y no por olvido.

### Que no dependa de acordarse

El checklist de arriba es un procedimiento, y un procedimiento se olvida. Las mismas suites
corren solos en dos lugares:

```sh
git config core.hooksPath herramientas/hooks
```

Eso instala `herramientas/hooks/pre-commit`, que antes de cada commit que toque un `.md` corre el
verificador de documentación —un segundo— y frena el commit si encuentra algo. **Hace falta el
`git config` porque `.git/hooks/` no se versiona**: un hook suelto ahí adentro no viaja a un clon.
Se saltea con `--no-verify`, a propósito: es una ayuda, no una aduana.

La aduana es `.github/workflows/tests.yml`, que corre las mismas suites en cada push y en cada pull
request. Eso no se saltea y no hay que instalarlo. El hook es apenas el eco local y rápido de lo
mismo, para enterarse antes de pushear y no después.

## Cada cosa se explica en un solo lugar

Un porqué escrito dos veces se separa: alguien corrige una copia y la otra queda afirmando lo
contrario, sin que nada avise. Por eso hay un lugar por tema, y el resto remite:

| Qué se explica | Dónde vive |
| --- | --- |
| Una convención del repositorio, y por qué | **`docs/DESARROLLO.md`** |
| Una regla que hay que tener en la cabeza antes de tocar algo | **`AGENTS.md`** |
| Lo que sólo vale para Claude Code | **`CLAUDE.md`**, que es un `@AGENTS.md` y tres líneas más |
| La capa offline: qué hay, de dónde salió, cómo se verifica | **`derecho/fuentes/MANIFIESTO.md`** |
| El mapa de licencias por ruta | **`LICENCIAS.md`** |
| Qué hace un script y cómo se corre | Su **docstring** |
| **Qué herramientas de estado hay y cómo se corren** | La salida de **`herramientas/pendientes.py`**, que las nombra al cierre. `AGENTS.md` remite ahí en vez de copiar la lista |
| Por qué existe un guardarraíl y qué error atrapa | El **docstring de su test**, que es lo que se lee cuando se pone en rojo |

**La remisión nombra el archivo —entre acentos graves o como link— y después el título de la
sección entre comillas angulares**, y `TestPunterosDeSeccion` comprueba que ese encabezado
exista, en cualquiera de las dos formas. Sin ese control la remisión se
pudre en silencio —se renombra la sección y el puntero deja de llevar a ningún lado—, que es
peor que la copia que vino a reemplazar.

Lo que **sí** se repite a propósito, y por qué:

- **El encabezado de cada módulo de `references/`.** Un módulo se lee solo, así que lo
  que no diga ahí no está dicho. Va idéntico y lo fija `TestEncabezadoDeLosModulos`.
- **La invocación en cada archivo de `commands/`.** Claude Code los carga de a uno.
- **La declaración de la zona horaria, tres veces.** Los tres árboles de scripts no comparten
  módulo por diseño; lo sostiene `TestUnaSolaZonaHoraria`.
- **La terna de un eval y su `prompt.md`.** Formatos distintos del mismo caso, mientras dure
  la migración.

### Los cuatro destinos de una regla

| Si la regla… | va en | y no pasa de |
| --- | --- | --- |
| rige **siempre**, o errar es irreversible | `AGENTS.md`, o `.claude/rules/<tema>.md` declarada siempre-activa | 200 / 120 renglones |
| rige **al tocar** cierto árbol | `.claude/rules/<tema>.md`, con `paths:` | 120 renglones |
| es orientación para leer, no instrucción | `docs/` | sin tope |
| explica por qué existe un guardarraíl | el docstring de su test | sin tope |

Las tres reglas de hoy —`prosa.md`, `derecho-argentino.md` y `herramientas.md`— son las tres
siempre-activas, y **ninguna usa la segunda fila**. Una regla con `paths:` sólo sube cuando
Claude lee un archivo de esa ruta con la herramienta `Read`; leer con `cat`, `sed` o `grep` por
Bash no la carga, y eso es lo que hace el modo auto. Una regla cuya vigencia depende de con qué
herramienta se leyó un archivo no rige, así que la segunda fila queda para el día en que el
alcance sea tan angosto que cargarla siempre no se justifique.

**Lo que decide entre `AGENTS.md` y una regla siempre-activa no es el contenido, es el tope POR
ARCHIVO.** El umbral de adherencia que da la documentación de Claude Code es por archivo, no por
sesión, así que repartir deja cada uno bajo el suyo y el conjunto se lee mejor que un archivo
único que nadie termina.

Lo que no puede pasar es que una regla no esté en ninguna de las dos partes —ni `paths:` ni la
declaración de siempre-activa—, porque ahí nadie decidió que cargue siempre. Lo exige
`TestDondeVaCadaRegla`, que además falla si un archivo pasa su tope, si aparece una regla que
esta tabla no nombra o si `AGENTS.md` no la nombra por su ruta: `.claude/rules/` es un mecanismo
de Claude Code, y quien trabaja en Codex las abre a mano o no las tiene.

## Los archivos de veredicto

Todos los detectores de este repo reportan **candidatos, no culpables**: texto compartido con
`kb/`, leyes citadas sin fuente en `fuentes/`, capas de OCR, marcas del descargador. El valor de
un detector se pierde el día en que su salida deja de mirarse, y eso pasa cuando la lista crece
en vez de bajar. El archivo de veredicto es lo que la hace bajar: guarda **lo que alguien leyó**,
con fecha.

Todos comparten un sobre. `kb-procedencia.json` ya lo tenía y sirvió de modelo:

```json
{
  "_descripcion": "qué es y quién lo consume",
  "_criterio":    "por qué existe y cómo se decide un veredicto",
  "_vocabulario": {"valor": "qué significa"},
  "fijado":       "2026-09-14",
  "nota":         "por qué quedó en este estado",
  "<carga>":      "el contenido"
}
```

| Archivo | Carga | Lo consume |
| --- | --- | --- |
| `herramientas/fuga-revisada.json` | `secuencias` | `fuga_textual.py` |
| `herramientas/cobertura-revisada.json` | `leyes` | `cobertura_normativa.py` |
| `herramientas/lecturas-ocr.json` | `lecturas` | `calidad_ocr.py`, `reocr_jurisprudencia.py` |
| `herramientas/kb-procedencia.json` | `archivos` | `frontera_kb.py` |
| `herramientas/reformas-revisadas.json` | `reformas` | `reformas_no_leidas.py` |
| `herramientas/cifras-revisadas.json` | `cifras` | `cifras.py` |
| `herramientas/deuda-revisada.json` | `reclamos` | `deuda_vencida.py` |
| `herramientas/ramas-revisadas.json` | `ramas` | `ramas_sin_disparador.py` |
| `derecho/fuentes/normas/revisiones.json` | `revisiones` | `descargar_normas.py` |

**La carga no se unifica, y es a propósito.** Son tres formas honestas y distintas: un conjunto
de pertenencia (`secuencias`, sin veredicto individual), un mapa de veredictos
(`leyes`, `lecturas`) y un mapa de listas (`revisiones`, porque una norma puede volver con más
de un defecto). Forzar las tres a `items: {clave: {veredicto, fecha}}` inflaría la primera cientos
de veces y registraría un veredicto por secuencia que nadie tomó. **Un formato único que miente
sobre el contenido es peor que tres formatos que lo dicen.**

**Tampoco hay un loader único**, y por una razón de arquitectura: `revisiones.json` vive dentro
del plugin, que tiene que ser autocontenido para poder instalarse y no puede importar de
`herramientas/`. Los demás pasan por `herramientas/_veredictos.py`; ése carga su sobre en
`_comun.py`. Lo que los mantiene alineados es `TestSobreDeLosVeredictos`, que los lee a todos — y
que además falla si aparece uno nuevo sin declarar.

## Lo que un script imprime tiene que entrar en cp1252

En Windows la consola suele estar en **cp1252**, y un `print()` de un carácter que no entra en esa
página de códigos termina en `UnicodeEncodeError`. El script muere **después** de haber hecho el
trabajo, y quien lo corre cree que falló la medición. Peor todavía si ya escribió: `cifras.py
--sellar` reescribe archivos y **después** informa qué selló.

**Los acentos no son el problema.** `á é í ó ú ñ ü · —` están todos en cp1252, y `pendientes.py`
los imprime sin inconveniente. Lo que rompe es otra cosa:

| Carácter | Entra en cp1252 |
| --- | --- |
| `á` `é` `í` `ó` `ú` `ñ` `ü` `·` `—` `«` `»` `¿` `¡` | **Sí.** Se pueden imprimir |
| `→` `✔` `≥` `│` `─` y el resto de flechas, tildes y caracteres de dibujo | **No.** Rompen la corrida |

Así que la regla es una sola y se verifica corriendo los scripts de verdad: **toda la salida tiene
que poder codificarse en cp1252.** El test lo comprueba sobre las herramientas que no necesitan
binarios externos ni red.

**Pero la salida sí va acentuada.** Lo que un script imprime es texto que alguien lee, y en el caso
de las calculadoras es texto que **se copia a un escrito**: un rubro que dijera
`Indemnizacion por antiguedad` entra así a una demanda. Eso está en el mismo cajón que las carátulas de los fallos, no
en el de las convenciones.

**En el fuente** —comentarios y docstrings— también va acentuado: es prosa que alguien lee, y
varios docstrings se imprimen enteros en `--help` porque el script hace `description=__doc__`.
Lo sostienen `TestProsaAcentuadaEnElFuente` y `TestSalidaAcentuadaEnTodoElRepo`.

**El corrector de verdad se corre a mano**, porque necesita Java y baja LanguageTool:

```sh
uv run --with language-tool-python --with jdk4py python3 herramientas/ortografia.py
```

Los tests de la suite son reglas —`-ción`, la ñ transliterada, determinante más sustantivo, `se`
más pretérito— y cubren lo que una regla decide; son el piso, corren siempre y sin red.
`ortografia.py` es el techo: tiene diccionario y gramática, y encuentra lo que ninguna regla
puede —`Boletin`, `dieciseis`, `polizas`, `conyuge`, `transito`—. No entra al checklist a
propósito: un candado que tarda minutos y depende de la red se termina salteando.

**Lo que decide QUÉ mide el techo sí corre siempre**, en `herramientas/test_ortografia.py`, y
está en el checklist. Es la parte que falla en silencio: un extractor que se deja afuera medio
archivo no da error, da menos hallazgos, y menos hallazgos se lee como que el repositorio está
mejor. Pasó dos veces —las filas de tabla descartadas enteras, que eran el 85% de
`changelog-normativo.md`, y todos los `.md` reportados en la línea 1—.

**La coma delante de `pero` va cuando une dos oraciones, no cuando coordina dos predicados
del mismo sujeto.** «el Senado lo rechazó, pero Diputados nunca lo trató» lleva coma; «mueve
el cursor pero no borra» y «daño cierto pero futuro» no, y la RAE lo admite para el segundo
elemento breve. `ortografia.py` reclama las dos por igual —unos treinta avisos—: la regla
queda encendida porque la primera clase es un error de verdad, y la segunda se saltea leyendo.

### Qué mide `ortografia.py`, y qué reglas están apagadas

El criterio está tomado, y cada regla apagada lleva su medición al lado. Vive acá y no en
`PENDIENTES.md` porque no es una decisión por tomar.

**La ortografía está cerrada; queda gramática, y menos de la que parece.** `ortografia.py`
recorre los `.md`, los comentarios, docstrings y cadenas de los `.py` y los campos de prosa de
los `.json`. **Los candidatos de acento están leídos uno por uno y no queda ninguno sin
resolver:** los que siguen apareciendo son verbos homógrafos de un sustantivo acentuado
—`valida`, `publica`, `prorroga`, `tramite`—, demostrativos, apellidos que salen del documento
y defectos de OCR citados entre comillas. Son la lista que la sección de ortografía declara no
automatizable, funcionando.
**La gramática también quedó decidida, leyendo los avisos de una corrida completa**: 8.799
piezas de prosa, 328 candidatos. La coma delante de `pero` ya estaba resuelta —va cuando une
dos oraciones, no cuando coordina dos predicados del mismo sujeto; el criterio está en
`docs/DESARROLLO.md`— y quedan unos treinta avisos que se saltean leyendo. De las cuatro que
faltaban, **dos se apagaron y dos quedaron encendidas porque aciertan**:

| Regla | Veredicto | Medición |
| --- | --- | --- |
| `COMMA_SINO` | apagada | 16 avisos, ninguno real: reclama la coma en el correlativo simple |
| `AGREEMENT_PARTICIPLE_NOUN` | apagada | 11 avisos, 11 falsos: dispara con `palabra por palabra` |
| `COMMA_MARCADOR_DISCURSIVO` | **encendida** | 14 avisos, **4 reales** ya corregidos; los falsos son `Además de` |
| `AGREEMENT_ADJ_NOUN` | **encendida** | 12 avisos, **2 reales**: `los mismos suites` en el archivo que declara que `suite` va en femenino |

El guion de `contencioso administrativo` también quedó decidido —sin guion en prosa propia, con
el de la fuente en una cita—, y su regla se apagó por reclamar lo ya decidido: 15 avisos, 15
contra una forma elegida. **Lo que sigue abierto de este punto es sólo correr la herramienta**,
que pide dependencias externas por `uv` y por eso está fuera del checklist, no del trabajo.
**Las reglas apagadas llevan su motivo y su medición al lado**, casi todas por la misma causa:
este repositorio está hecho de citas legales y de texto recortado, y ahí `art. 441 texto Ley
13.818` o `número de causa` no son concordancias rotas. Antes de apagar una novena, medirla:
si se equivoca sobre todos los casos conocidos no sirve, y si acierta sobre alguno se arregla
ese caso. En los `.json` la mitad del archivo es contrato, así que la revisión va campo por
campo: una clave o un valor que se compara no se toca.

**`contencioso administrativo` va SIN guion en nuestra prosa, y con el que traiga la fuente
cuando se cita.** La RAE pediría el guion para dos adjetivos independientes, y el articulado no
la respalda ni la contradice: **usa los dos**. Medido sobre `fuentes/normas/`, 124 sin guion y
44 con — las constituciones de Catamarca, Misiones y Santa Cruz lo llevan; las de Santa Fe y PBA
no. Pero acotado a lo que este repositorio cubre —las normas de PBA y las nacionales— son **101
sin guion contra 15**, y ahí entran la Constitución de la Provincia, la Ley 15.057 y el Acuerdo
4013 de la SCBA. Nuestra prosa ya venía escribiéndolo así en sus 27 apariciones, sin una sola
excepción, así que la decisión **fija lo que ya se hacía** en vez de cambiar nada.
**Una cita textual conserva el guion si la fuente lo trae**, por la misma regla que el resto de
las citas, y `TestContenciosoAdministrativoSinGuion` exime la línea entrecomillada o citada con
`>`. Si alguna vez hace falta el guion fuera de una cita, el test salta: es un aviso para
decidir, no una prohibición.

**Tres palabras llevan un género fijado, y una de ellas distingue dos cosas.** `la fuente`
es la fuente del derecho —primaria, oficial— y **`el fuente` es el código**, por elipsis de
«el [código] fuente». La distinción se usa todo el tiempo en este repositorio y conviene
sostenerla: medido, los 18 masculinos hablan de código y los 64 femeninos de derecho.
`el checklist` va en masculino —26 veces, ninguna en femenino— y `la suite` y `la tilde`, en
femenino, que es lo que dice la RAE. `ortografia.py` exime los dos primeros por giro, no
apagando la regla, y `TestGiroPropio` avisa si el reparto de `fuente` se empareja: ese día la
distinción dejó de existir.

**Dos grafías tradicionales se conservan a propósito:** `sólo` con tilde y los demostrativos
`éste`, `ésa`, `aquéllas` cuando son pronombres. La RAE les sacó la tilde en 2010; acá se
mantiene porque es la ortografía del foro y la de los escritos que la skill produce. Es una
decisión, no un descuido: `ortografia.py` apaga las dos reglas con ese motivo escrito al lado.
El repositorio no las mezcla —medido: 32 demostrativos acentuados y ninguno sin acentuar—, y si
alguna vez se revierte, se revierte entero y desde acá.

**Un pase automático sobre comentarios toca sólo el texto del comentario, nunca la línea.** Media
línea de código y media de comentario —`RAIZ = Path(...)  # derecho/fuentes`— es el caso que
rompe: tratarla entera como prosa renombra la constante y acentúa cadenas que están fijadas por
hash.

**Qué se acentúa y qué es contrato no se decide acá**: la regla y sus nueve excepciones están en
`.claude/rules/prosa.md`, que carga al abrir la sesión. Lo que sí es de este archivo es el caso de
borde de arriba —el pase sobre comentarios y la línea mixta—, que es una convención de cómo se
edita, no de qué se escribe. Y que una carátula de fallo lleva sus acentos porque es un
dato que se cita: lo exige `TestCaratulasAcentuadas`.

## Las cifras de la documentación no se escriben a mano

Cada vez que un documento dice cuántos módulos, normas, fallos o casos de prueba hay, está
afirmando algo que envejece solo. `LICENCIAS.md` declaraba **2 documentos** en `docs/` cuando ya
había cuatro, y no lo atrapó nada: la cobertura era opt-in, así que cada cifra necesitaba que
alguien se acordara de escribirle un test, y el que no se acuerda no rompe nada.

```sh
python3 herramientas/cifras.py            # verifica y censa
python3 herramientas/cifras.py --sellar   # reescribe cada cifra con lo que hay en disco
```

**El ancla es el patrón de texto que rodea la cifra, no un marcador en el archivo.** Los `.md` no
llevan nada raro adentro: la cifra se escribe como se escribiría igual. Es a propósito, porque la
mitad de estos archivos viajan dentro del plugin y los lee el modelo, y un
`<!--#normas-->132<!--/-->` ahí no es invisible: es ruido en las instrucciones. El registro está en
`herramientas/cifras.json`.

**Y el censo es la parte que importa.** Busca *cualquier* cifra pegada a un sustantivo de inventario
y exige que esté declarada en uno de tres lugares: el registro de anclas, la lista de las que ya
mide otro test, o `cifras-revisadas.json` con motivo si no es inventario. Lo que no esté en ninguno,
rompe. Eso invierte el default: **una cifra nueva sin declarar ya no pasa desapercibida.**

Tres reglas que salieron de armarlo, y que conviene saber antes de tocar una cifra:

- **Un ancla tiene que enganchar exactamente una vez.** Si engancha dos, la cifra está escrita dos
  veces en el mismo archivo. La salida no es alargar el ancla hasta que sea única —eso la apoya en
  una coma o en un nombre de archivo que no tienen nada que ver con la cuenta— sino **sacar la
  repetida**. Así se fue el segundo *"seis tomos"* de `MANIFIESTO.md`.
- **Toda cifra sellada necesita una definición ejecutable.** `LICENCIAS.md` decía *"los 9 scripts
  de la skill"* y hay ocho sin contar la suite, nueve contándola: no estaba vencida, estaba
  indefinida. Una cifra que no se puede definir no se puede verificar con ningún mecanismo, así que
  **se saca de la prosa**.
- **Si la cifra no informa, mejor que no esté.** Es lo más barato de mantener y no hay que
  declararlo en ninguna parte.


### Una cifra que cambia según dónde se mide no es una cifra

`mb_instalados` —lo que pesa el plugin— pasó el suite local y **rompió el pipeline dos veces**.
La primera sumaba la carpeta `derecho/` entera y sobraban 0,77 MB de `__pycache__` y `.DS_Store`.
Se filtraron por patrón, y a la corrida siguiente sobraba **1,19 MB de `derecho/evals/results/`**,
que deja `claude plugin eval` y que `.gitignore` ya excluía.

**El segundo rojo es el que enseña.** Agregar `results` a la lista de patrones habría sido
calibrar contra el caso conocido, y la lista siempre va a ir atrás de la próxima herramienta que
escriba algo en el árbol. Lo que estaba mal era la definición: la cifra dice cuánto **descarga**
quien instala, y eso es lo que el repositorio **versiona**, no lo que hay en la carpeta de quien
mide. Git ya sabe qué ignora, así que la métrica le pregunta — `git ls-files` — y eso es una
regla en vez de una lista. Si no hay git, **se planta**: no hay verde por ausencia de instrumento.

El filtro por patrón además se equivocaba al revés: salteaba todo tramo con punto, de modo que
`derecho/.claude-plugin/plugin.json`, que sí viaja, no contaba.

Lo sostiene `TestElPesoSeMideIgualEnCualquierMaquina`, que arma un repo de prueba con un archivo
versionado y otro ignorado y exige que sólo pese el primero.

**Y antes de pushear algo que cuente archivos, se mide contra un clon, no contra una copia.** Una
copia del árbol arrastra lo que git ignora, que es justamente lo que hace divergir la cifra:

```sh
git clone . /tmp/runner && git diff HEAD > /tmp/wip.patch
git -C /tmp/runner apply /tmp/wip.patch
cd /tmp/runner && python3 -m unittest discover -s herramientas -p "test_*.py"
```

### Qué entra al censo, y por qué los módulos entraron tarde

`references/` estuvo **excluido** con este motivo: *"ahí las cifras son derecho —48 artículos,
tres etapas del art. 28 inc. h— y el censo se ahogaría en falsos positivos"*. Medido, el motivo
era falso sobre sus propios ejemplos: el censo no busca números, busca **número + sustantivo de
inventario**, y ni «artículos» ni «etapas» están en esa lista. Ninguno de los dos casos podía
disparar.

Al entrar los módulos aparecieron 52 candidatos, y ahí estaban **dos contradicciones que
llevaban tiempo**: `escritos.md` decía treinta y cinco modelos y `modelos.md` treinta y cuatro
—el disco dice 34—, y `marcadores.md` decía 24 marcadores mientras el `SKILL.md` decía veintidós
—son 26—. Las dos son la forma exacta que `prosa.md` describe: *repetir una cifra en dos archivos
garantiza que uno de los dos mienta*. Las dos pasaron a métrica.

**La lección no es que el motivo estuviera mal, sino de qué tipo era.** Decía lo que el control
iba a hacer sin haberlo corrido: es «del producto no se concluye el proceso» aplicado a una
exclusión. Una exclusión se escribe después de mirar qué reporta, no antes.

## Dos agentes, un solo archivo de reglas

**Que el contenido viva en `AGENTS.md`, y que `CLAUDE.md` sea apenas un `@AGENTS.md`, lo dice
cada uno de ellos.** Acá va el porqué y cómo se rompe.

**El contenido va en el archivo del agente que no tiene con qué importar.** Claude Code sí tiene:
`@ruta` se expande y entra al contexto al abrir la sesión. Codex no, así que un `AGENTS.md` que
remitiera a `CLAUDE.md` dependería de que el agente decida ir a buscarlo. Al revés funciona
siempre.

Tres formas de romperlo, ninguna ruidosa, y las tres las ataja `TestLosDosAgentesLeenLoMismo`: que
se borre la importación, que quede **entre acentos graves** —ahí es texto literal y no importa
nada, y se ve igual— o que alguien copie el contenido a `CLAUDE.md` y queden dos copias de las
reglas.

**Symlink no**, aunque la documentación lo admita: en Windows pide Developer Mode o Administrador,
y este repositorio declara que corre en Windows. Un symlink que en un clon aparece como un archivo
de texto con una ruta adentro es peor que no tenerlo.

**Y `.claude/settings.json` está versionado** —el resto de `.claude/` sigue ignorado— porque lleva
el `claudeMdExcludes` que evita que los `CLAUDE.md` de `kb/` entren como instrucciones. El porqué
está en `CLAUDE.md`, que es de donde sale esa exclusión; si aparece un tercero, el test lo reclama.

## markdownlint sirve para prospectar, no para bloquear

El verificador del repositorio es `herramientas/test_markdown.py`: no tiene dependencias, corre en
el CI y comprueba lo que se rompe **en silencio** —links, anclas, cercas, imágenes que dejaron de
renderizar, acentos, cifras, marcadores partidos—. `markdownlint` es lo otro: un tercero que mira
el árbol con otros ojos y encuentra lo que nuestro verificador no busca.

```sh
npx --yes markdownlint-cli2          # avisa
npx --yes markdownlint-cli2 --fix    # arregla lo mecánico
```

**No está en el checklist de cierre ni en el CI, y es deliberado:** agregar Node al camino de un
repositorio que hoy corre con Python de fábrica es un costo que el usuario del plugin no debería
pagar. **Lo que valga la pena de una corrida se implementa en `test_markdown.py`**, que sí corre
siempre — así llegó el control de marcadores partidos, que es un invariante nuestro y ningún
linter tiene.

**La corrida da cero, y recién por eso sirve.** Cada regla está arreglada y encendida, o apagada
con el motivo escrito al lado en `.markdownlint-cli2.jsonc`. Con avisos pendientes el resultado no
significa nada: una alarma que suena siempre es una que nadie mira, y ahí adentro se pierde el
aviso que sí importa. Que dé cero **no la mete en el checklist**: sigue afuera por lo de Node, y
sigue siendo prospección. El valor está en que un aviso nuevo se ve de entrada.

Dos cosas que conviene tener presentes:

- **`--fix` reescribe archivos**, así que su `ignores` tiene que dejar afuera la capa 2: `kb/` y las
  cinco excepciones de [`LICENCIAS.md`](../LICENCIAS.md). Un test lo controla, porque es la única
  herramienta del repositorio capaz de editarle a otro autor sin que nadie se lo pida.
- **El estilo de tabla va dicho, no inferido.** MD060 con el default `any` elige por tabla el estilo
  más cercano, y en las de celda larga elige `aligned`, que exige alinear los pipes en columna: una
  celda de mil y pico de caracteres no se alinea. Fijado en `compact` —un espacio de cada lado en
  toda celda, delimitador incluido— el `--fix` normaliza el árbol entero.

Y antes de cambiar el estilo de una tabla, **buscá quién la parsea**. La regla y el caso que la
enseñó están en `.claude/rules/herramientas.md`.

## Si escribís contenido

**Bajo qué licencia entra lo que escribas.** La frontera es la ruta y ahora tiene cuatro capas, con
el mapa completo en [`LICENCIAS.md`](../LICENCIAS.md):

| Lo que escribís | Licencia |
| --- | --- |
| Un módulo de `references/`, un comando, un eval, documentación | **CC BY-SA 4.0**: atribución y **CompartirIgual** |
| Un script, una herramienta, un manifiesto `.json` | **MIT** |
| Cualquier cosa bajo `derecho/kb/` | **No se escribe ahí.** Es capa 2, de Cristian Aboitiz |

Que el contenido sea CompartirIgual tiene una consecuencia si aceptás aportes: **el autor puede
relicenciar su propia obra, pero lo que aporte un tercero bajo CC BY-SA no**, salvo cesión expresa.

**La frontera con la capa 2 se cruza en los dos sentidos, y la regla está en
[`AGENTS.md`](../AGENTS.md), sección «La frontera de licencia».** Acá va cómo se opera cada
detector.

**Sentido uno: prosa de `kb/` que entra a un módulo.** Lo mide `herramientas/fuga_textual.py`,
que compara los módulos contra `kb/` y reporta secuencias de nueve palabras compartidas, con
la línea de base de lo ya revisado en `fuga-revisada.json`. Reporta **candidatos, no
culpables**: hay que leerlos. Si es texto legal o un dato, va a la base con `--aceptar`; si es
prosa de `kb/`, se reescribe el módulo.

**Sentido dos: texto propio que sale hacia `kb/`.** Lo avisa `herramientas/frontera_kb.py`
cuando `kb/` cambia; si el cambio es querido, se fija con `--fijar --nota '...'`. Ojo con la
interacción entre los dos: reescribir una línea de `kb/` con palabras propias **desactiva al
primero**, porque hace desaparecer la coincidencia que busca.

> **Los evals entran al detector, igual que los módulos.** Son capa 3 y se escriben con las
> mismas reglas, así que el comando de arriba los incluye. Los 49 casos dan **cero prosa**: sus
> coincidencias con `kb/` son articulado y carátulas de fallos, que se mueven libres. Un caso
> nuevo que copie prosa rompe el checklist, que es exactamente para lo que está.

> **`derecho/kb/` está fuera del verificador de documentación, y se queda afuera.** Esa capa es de
> otro autor y no sigue estas convenciones. El único defecto que se ve al renderizar es **un bloque
> de código sin cerrar** en `administrativo-CHACO-CLAUDE.md`, que se come el resto del documento;
> el resto son espacios al final de línea y anchos de tabla. Nada de eso se toca: `kb/` no se
> modifica sin decisión previa, y el día que se toque se arregla entonces.

### Correr los evals con `claude plugin eval`

**El estado de la migración no está acá**, sino en `docs/PENDIENTES.md`, sección «El formato de
los casos de prueba», que es donde vive la decisión abierta. Acá va lo que cuesta averiguar
corriéndolo, para no volver a averiguarlo:

- **El formato sale de `claude plugin eval init --bare`, no de la documentación.** `focus:` en un
  grader `llm` está **rechazado** por el cargador.
- **`max_turns: 10` no alcanza:** la skill se gasta los turnos leyendo sus propios módulos y la
  corrida muere sin producir respuesta, con todos los graders fallando sobre un mensaje vacío. Con
  30 usa 18 y llega.
- **Declarar `Bash` en `allowed_tools` exige además `--allow-tools` y un sandbox instalado**
  —bubblewrap y socat—, o el harness se niega a correr. Estos evals miden doctrina, no aritmética
  —que ya tiene tests deterministas—, así que corren **sin shell**.
- **Cuesta dinero y tiempo:** del orden de un dólar y de dos a seis minutos por corrida, y con
  `runs: 3` una pasada completa son decenas de dólares. Va a mano antes de publicar, no en cada
  push.
- **Un hecho por grader.** Un criterio `llm` con varias afirmaciones adentro falla por la más
  débil: dio FAIL con una respuesta correcta que decía "9 años" donde el criterio pedía "9
  períodos". **Y los criterios negativos son los que más fallan**: pedir que algo NO aparezca
  reprueba respuestas correctas. Los graders deterministas —fecha, ley citada, marcador, skill
  disparada— no fallaron nunca.
- **Dos corridas del mismo caso dieron puntajes muy distintos**, y lo que falló en la segunda
  falló con razón. Esa varianza entre corridas es el argumento más fuerte a favor de los evals, y
  **no se ve leyendo una corrida a ojo**.
- **Correr siempre con `--keep-temp`.** Sin eso no queda la traza y no se puede diagnosticar por
  qué falló un grader; se paga la corrida dos veces.

Y antes de escribir sobre un instituto: leer el texto en `derecho/fuentes/normas/`, que está
consolidado con URL, fecha y hash. El vocabulario de marcadores válido es el de
`references/marcadores.md`. Cuando se agrega o corrige contenido normativo, actualizar la tabla de
estado de verificación de `references/changelog-normativo.md` con la fecha y la volatilidad.

### Un monto se escribe sólo si la norma le pone ventana

La pregunta no es si el monto es reciente, es **si tiene vencimiento escrito**. Los montos de la
Res. SRT 39/2026 están en la tabla de `laboral.md` porque la resolución dice del 01/09/2026 al
28/02/2027: pasada esa fecha el número se ve vencido solo, y el que lo lea sabe que dejó de regir.
El SMVM, en cambio, se emite por marcador —`concursos.md` lo pide para el tope del pronto pago—
porque ahí el número es un valor corriente sin fin escrito, y guardado envejecería en silencio
pareciendo vigente.

De ahí sale qué hacer al bajar una norma de montos: **leerla para ver si trae cronograma.** Si
fija tramos con fechas, el monto entra a la tabla con su ventana y el marcador se retira. Si es un
valor abierto, el marcador se queda y el veredicto se escribe. Un número sin ventana en un módulo
es la forma más cara de equivocarse que tiene este repositorio, porque no se ve.

### Dos puertas de entrada, dos detectores

Una norma entra al repositorio por dos lados, y cada uno tiene su propia medida. **Citada con
articulado** en un módulo: la reclama `cobertura_normativa.py`. **Nombrada en «Cambios recientes»**
de `changelog-normativo.md`: la reclama `TestNormasDeCambiosRecientes`, en `test_scripts.py`.

Hacían falta las dos porque la primera mira una ventana de texto alrededor de un articulado
citado, y una resolución anotada en una lista de cambios recientes no cae ahí. Es justo donde el
repositorio guarda lo más volátil —montos del semestre, reglamentaciones—, o sea lo que primero
envejece: sin la segunda medida, esa sección podía quedar vieja sin que sonara nada.

Las dos tienen la misma salida y la misma disciplina: **o la norma está declarada en
`normas.json`, o alguien escribió por qué no** en `cobertura-revisada.json`. Lo que ninguna de las
dos admite es el silencio.

Al comparar números de norma, **la clave es exacta y no por subcadena.** Aplanados a dígitos,
`5844/2026` contiene a `4/2026`: con subcadena, una norma borrada del manifiesto sigue pareciendo
declarada porque otra sin relación la contiene. Un test de la clase fija ese caso.

### `SKILL.md` se paga en cada conversación, y los módulos no

El cuerpo del `SKILL.md` entra **completo** al activarse la skill; los `references/` entran sólo
cuando el modelo decide abrirlos. La documentación de Claude Code fija el objetivo en
[**menos de 500 renglones**](https://code.claude.com/docs/en/skills.md), con el detalle en
archivos de apoyo. Lo mide `TestElPresupuestoDeSKILL`, en `test_scripts.py`, y **su tope es un
trinquete y no el objetivo**: hoy el archivo mide más, y una alarma que suena siempre se apaga
sola. Lo que fija es que no crezca, con los 500 a la vista en el mensaje de falla.

**Lo que se queda arriba de 500 son las dos tablas que no pueden mudarse.** El ruteo de la
sección 16 es la navegación que la documentación manda dejar ahí; el vocabulario de marcadores
de la sección 3 lo transcribe el modelo **exacto** en cada respuesta, y nadie va a abrir un
módulo para copiar un corchete. Todo lo demás que no se lee en toda conversación va a
`references/`.

**Y la duplicación entre el `SKILL.md` y un módulo se busca antes de escribir.** Es la forma más
cara de crecer, porque se paga siempre y no agrega nada. Cada cosa vive en un solo lugar y el
`SKILL.md` remite: la resolución de la ruta al repo, en `scripts/README.md`; el inventario de
`fuentes/`, en `fuentes.md` 14.0; los tres planos de la Ley 15.057, en `sede-judicial-pba.md`
1.6.1. Cuando la copia igual aparece, **la del `SKILL.md` es la más pobre**, porque es la que
nadie va a actualizar: el que corrige el punto lo corrige en el módulo.

### 0.1 bis dice hasta dónde llega; la sección 16 dice qué abrir

Las dos son tablas de materia contra módulo, así que **convergen solas**: cada módulo nuevo entra
a las dos y la de cobertura termina describiendo el contenido de cada uno, doce renglones más
arriba de la fila que lo enruta. Para rutear sirve la **situación de quien consulta** —«hay una
internación por salud mental»—, no el temario del archivo.

Lo sostiene `TestLaCoberturaNoRepiteElRuteo` con dos reglas: **una fila por materia y no una por
módulo** —los módulos son decenas, las materias con veredicto propio poco más de diez—, y **una
fila tiene que decir algo además de a dónde ir**: si sacándole las rutas no queda texto, esa fila
es ruteo y su lugar es la 16.

### Cuándo un módulo se parte por jurisdicción, y cuándo no

La pregunta se contesta mirando **dónde está la norma, no dónde tramita el expediente**:

| El derecho que se aplica es | Entonces | Ejemplos |
| --- | --- | --- |
| **Nacional y común** — CCyCN, LCT, LDC, Código Penal | **Un solo módulo**, y lo procesal se rutea aparte | `civil.md`, `laboral.md`, `consumidor.md` |
| **Local** — código procesal, código fiscal, ley arancelaria, régimen previsional provincial | **Un módulo por jurisdicción**, con la jurisdicción en el nombre | `tributario` / `-pba` / `-caba`; `honorarios-nacional` / `-pba` / `-caba`; `proceso-nacional` / `proceso-pba` |
| **Local pero la skill sólo tiene una jurisdicción** | Un módulo, y **el título dice cuál** | `notificaciones-pba.md`, `contencioso-pba.md` |

**Lo que no se hace es partir por fuero dentro de una jurisdicción.** Un fuero nuevo entra como
sección del módulo de su jurisdicción mientras quepa; el módulo se parte recién cuando pasa el
tope de renglones, y ahí se parte **por materia**.

**Y el título del módulo declara hasta dónde llega**, porque el nombre del archivo no puede: la
jurisdicción es estable y la cobertura por fuero crece. `sede-judicial-pba.md` se llama así y su
título dice *"en el fuero laboral PBA"*; `sede-judicial-nacional.md` cubre el civil, el comercial
y el laboral nacionales porque **el art. 155 de la Ley 18.345 remite al CPCCN**, y eso se leyó
antes de escribirlo. Cuando el título y el nombre no dicen lo mismo, manda el título, y el borde
del módulo lo repite.

### El modo no tiene fuero y la pieza sí

Es la partición de la sede judicial y sirve de molde para lo que venga. **El modo** —qué deja de
hacerse, qué se controla de oficio, qué pasa a significar cada marcador— sale del CCyCN y de la
posición del órgano, no de un código procesal, así que vive en `sede-judicial.md` 1.6 y le sirve a
cualquier juez. **La pieza que firma** —estructura de la sentencia, recaudos, costas,
admisibilidad recursiva— es de cada fuero y va en el suyo: `sede-judicial-pba.md`,
`sede-judicial-nacional.md` 1.8 y `sede-judicial-caba.md` 1.9.

**Los números son 1.8 y 1.9 y no subsecciones de 1.6 a propósito**, porque 1.6.1 a 1.6.10 ya eran
de PBA y la numeración de este repositorio es global: renumerarlas rompería las remisiones. La
irregularidad está escrita en cada uno de esos módulos para que nadie la "arregle".

**Lo que hace falta antes de escribir uno nuevo** es la puerta de siempre: el código del fuero
bajado por el descargador y cotejado artículo por artículo, y su caso de prueba. Lo que **no** se
puede dar por hecho es que un fuero herede el código de otro — el art. 155 de la Ley 18.345 lista
uno por uno los artículos del CPCCN que aplica, y de ahí sale que el laboral nacional comparta la
pieza con el civil; el art. 29 inc. 4 de la Ley 189 dice lo mismo que el art. 34 inc. 4 del CPCCN
con otro número. Eso se lee, no se deduce.

### Un módulo dice dónde termina

Cada módulo de rama cierra con **«Lo que este módulo NO hace»**, que nombra lo que queda afuera y
a qué módulo va. No es cortesía: un módulo que no dice dónde termina se lee como si no terminara,
y el modelo completa el hueco con conocimiento general en vez de decir que ahí la skill no llega.

Lo sostiene `TestLosModulosDeclaranSuBorde` como **trinquete sobre el reparto**, no como mínimo
por archivo: exigirlo en todos dejaría el suite en rojo hasta escribir de memoria los que faltan,
y cada borde sale de leer el módulo. **El encabezado va exacto** —`Lo que este módulo NO hace`—
porque contar con un regex laxo engancha una minúscula y da de más, y un control que cuenta de más
es el que no suena nunca.

### Un módulo no pasa de 1900 renglones

`Read` trae **2000 renglones por defecto** y el truncamiento **no avisa**: el agente cree que leyó
el módulo entero, vuelve a leerlo y lo completa con `Grep`, y una corrida se come turnos en cuatro
accesos al mismo archivo. Lo mide `TestNingunModuloSePasaDelCorteDeRead`, en `test_markdown.py`,
con tope en **1900** —cien renglones de aviso, que es una sección— y sobre el **archivo**, no la
sección, porque el corte de `Read` es por archivo.

**Cuando el control salta, se parte por MATERIA y no por número.** Cortar por número arrastra las
secciones que están ahí por vecindad: el derecho colectivo sale entero a `laboral-colectivo.md`, y
5.17 bis, ter y quater —RIFL, inclusión laboral trans, trabajo agrario— se quedan donde están. **La
numeración no se renumera**: en este repositorio es global y las remisiones apuntan a esos números.

**Partir un módulo arrastra ocho cosas**, y casi todas las reclama la suite: la fila de ruteo
—pueden ser varias—, `DISPARADORES` en el test de activación, el `description` del `SKILL.md`, una
consulta en `evals/RUTEO.md`, el veredicto de `ramas-revisadas.json`, las filas de la tabla de
verificación que apunten al módulo viejo, `docs/COBERTURA.md`, y las cifras de módulos en README,
LICENCIAS y ARQUITECTURA.

**La novena no la reclama ninguna suite: las remisiones cruzadas desde otros módulos.** Se buscan
así, y conviene correrlo después de cualquier partición:

```sh
grep -rn '`penal\.md` 24\.9' derecho/skills/derecho-argentino/references/
```

Y el módulo nuevo lleva su **encabezado de nivel 2**. Ningún test lo exige, y un módulo que salta
del título a `### 5.17` rompe el índice sin que nada avise.

### Una rama entra por módulo o por sección, y la sección necesita disparador

**Un fuero nuevo entra entero o no entra**: módulo con fuente primaria a la vista, normas bajadas
por el descargador, fallos leídos y su caso de prueba. Esa regla se escribió para **fueros** y
sigue rigiendo para ellos.

**Una materia es otra cosa y tiene su propia puerta.** Gas, cooperativas o navegación no son
fueros: son cuerpos normativos que caen dentro de un módulo que ya existe. Entran como **sección**,
y lo que se les exige es menos y distinto:

| | Fuero, como módulo | Materia, como sección |
| --- | --- | --- |
| Norma bajada y cotejada | sí | sí |
| Marcador de lo que no recorrió | sí | sí |
| **Disparador de ruteo** | sí | **sí, y es lo que se olvida** |
| Caso de prueba propio | sí | no |
| Fila en la tabla de ruteo con nombre de rama | sí | no: la comparte con su módulo |

**El disparador es la parte que no se puede saltear**, y es la que se salteó dieciséis veces
seguidas. Una sección no se rutea sola: la tabla de la sección 16 del `SKILL.md` manda a un
**módulo**, y el `description` activa la skill por **materia**. Si la materia nueva no figura en
ninguno de los dos, el texto está escrito y nadie lo va a abrir.

**Y los controles que había no lo veían**, porque miran módulos: `ruteo.py` mide la distancia de
cada módulo al router, y `TestElDescriptionDeLaSkillActivaTodasLasRamas` exige que el `description`
active a cada uno. Los módulos que contienen las secciones estaban alcanzados, así que los dos
daban verde mientras las ramas de adentro no se podían abrir.

Lo mide `ramas_sin_disparador.py`, con el mismo idiom que los otros detectores: reporta candidatos,
cada uno recibe su veredicto en `ramas-revisadas.json` —`rama` o `no-es-rama`— y lo que queda
después es lo nuevo. **Es un piso, no un techo**, y el motivo está en su docstring: una sección
cuyo encabezado no nombra su ley no se detecta sola. Escribir el número de la ley en el encabezado
es lo que hace que la próxima sí.

## Qué queda pendiente

**La deuda medible no se escribe: se lee de donde ya está anotada.** El marcador vive en el
módulo, la deuda normativa en la tabla de `references/changelog-normativo.md`, el veredicto de
lectura en `herramientas/lecturas-ocr.json`. Lo que hacía falta era una vista, no un registro
nuevo, y es `herramientas/pendientes.py` — que además **es el inventario de herramientas**, como
dice la tabla de más arriba. No está en el checklist de cierre: informa, no bloquea.

**Lo que ninguna herramienta puede medir sí tiene archivo**, y es
[`docs/PENDIENTES.md`](PENDIENTES.md): decisiones abiertas, restricciones que no se levantan y
trabajo de fondo. La diferencia entre los dos no es de formato sino de naturaleza — una lista de
deuda escrita a mano se vence como cualquier cifra escrita a mano, pero una **decisión** no la
mide ningún script.

## Mantenimiento

Desde Claude Code alcanza con `/derecho:verificar` y `/derecho:actualizar`; desde la app de
escritorio, pedírselo en castellano. A mano:

```sh
# ¿cambió alguna norma del manifiesto?
python3 derecho/fuentes/scripts/verificar_normas.py

# tests de los scripts de la skill
python3 derecho/skills/derecho-argentino/scripts/test_scripts.py

# diagnóstico de conectividad de los descargadores
python3 derecho/fuentes/scripts/diagnostico.py

# las series de índices que consumen las calculadoras: IPC, CER y RIPTE
python3 derecho/fuentes/scripts/descargar_series.py
```

**Las series se bajan aparte de las normas** porque vienen de otra fuente —la API de Series de
Tiempo del Estado, pública y sin token— y se pudren a otra velocidad: un índice mensual vence
todos los meses y una ley puede no cambiar en años. `estado.py` dice cuáles quedaron viejas. Y
hay una trampa escrita en el propio script: los `serie_id` del **índice** y de la **variación**
del IPC difieren en un carácter, así que bajar el equivocado deja un archivo con el formato
correcto y los números de otra cosa.

**Y para revisar una respuesta ya producida está `herramientas/verificar_respuesta.py`.** Las
rúbricas de `evals/` puntúan el contenido del análisis; ninguna ve lo que pasa después de razonar
bien: que un marcador se reescriba, que pierda una tilde, que aparezca uno que nadie declaró. Eso
no falla ruidosamente —sale con forma de marcador— y lo copia al escrito quien confía en la
herramienta. El script acepta sólo lo que `references/marcadores.md` declara, y reclama aparte el
caso engañoso: el nombre que existe pero escrito distinto.

`references/changelog-normativo.md` lleva la tabla de **estado de verificación por bloque**, con
la fecha de la última validación contra fuente primaria y una columna de volatilidad. Lo de
volatilidad alta —valor del jus, canasta de crianza, montos de la SRT, acordadas de feria— se
revisa antes de usarlo, no cada seis meses.

### Cuando un descargador no puede bajar

Se corre desde una terminal propia, y cuál fuente está bloqueada **se comprueba antes de
suponerlo**. La medición cuesta un comando y no toca el árbol:

```sh
python3 derecho/fuentes/scripts/verificar_normas.py --slug <slug> --verboso
```

Vuelve a pedir la URL del manifiesto, compara el hash contra `procedencia.json` y **no escribe
nada** sin `--sellar`. Sus tres códigos de salida separan lo que importa: `0` verificó y no cambió,
`1` cambió, `2` **no se pudo verificar**, que no es lo mismo que estar bien.

**Un bloqueo de una fuente oficial vale por su fecha, como cualquier registro de verificación.**
Anotarlo sin volver a medirlo convierte una restricción de un día en una regla permanente, y ahí el
costo no es el renglón: es que nadie vuelve a intentar lo que ya se puede hacer.

## La marca

<img src="../assets/marca/icono-128.png" width="72" align="right"
     alt="Ícono: sello cuadrado con la sigla AR">

El sello del banner, el ícono, las chapitas y el separador están **commiteados** en
`assets/marca/`, en SVG y en PNG. Para usarlos no hace falta nada: se referencian y listo.

**El generador no vive en este repo.** `generar_marca.py` y `test_marca.py` sumaban el 16% de
todo el Python de acá y eran la única dependencia externa del proyecto —Pillow y fontTools—
para algo que se corre una o dos veces por año. El plugin es una herramienta jurídica; el
generador de su logo es una herramienta de autor, y quien instala el plugin no tiene por qué
llevarse mil líneas de dibujo vectorial. Están en `derecho-argentino-marca/`, al lado de este
repo, con su propio README.

Regenerar la marca **pide las tipografías exactas y no hay sustituto**: el texto se pasa a
curvas, así que con otra fuente sale otro archivo y el script no cae en una alternativa
parecida — dice cuál falta y no escribe nada.

El detalle de cada archivo, la paleta y las tipografías está en
[`assets/marca/README.md`](../assets/marca/README.md). Dos cosas que no se resuelven solas:
`social-preview.png` hay que subirlo a mano en *Settings → General → Social preview*, y el ícono
sirve de avatar de la organización.

## Publicar

El historial es **un commit por versión**, y ninguna versión muestra sus etapas: lo que se
ofrece para instalar es el estado revisado. El circuito de una versión es siempre el mismo:

1. Rama `version-X.Y.Z` desde `main`, con **un solo commit** encima.
2. Mientras se trabaja, ese commit se corrige con `git commit --amend` y se sube con
   `git push --force` **sobre esa rama**. Nunca sobre `main`.
3. Cuando la versión cierra, entra a `main` por pull request. El mensaje es
   `versión X.Y.Z - <título de la versión>`, el mismo que encabeza su entrada del changelog.

Dos cosas se siguen de ahí. La primera: **`main` es lo único irreconstruible**, así que el
`--force` no lo toca nunca. La segunda: el mensaje de commit dice la versión y su título y
nada más, de modo que **el porqué de un cambio no queda en ningún mensaje**. Hay que anotarlo,
**pero cada cosa en su lugar**, o el registro se vuelve un diario de trabajo que nadie lee:

| Qué cambió | Dónde se anota |
| --- | --- |
| La versión del plugin | [`CHANGELOG.md`](../CHANGELOG.md), **sólo al publicar una versión** |
| Contenido normativo o jurisprudencial | La tabla de estado de verificación de `references/changelog-normativo.md`, con fecha y volatilidad |
| Una auditoría contra fuente primaria, con lo que se leyó y lo que se encontró | [`AUDITORIAS.md`](AUDITORIAS.md) |
| Algo que se tocó bajo `derecho/kb/` | `derecho/kb/CHANGELOG.md`, y además `python3 herramientas/frontera_kb.py --fijar --nota '...'` |
| La doctrina de un fallo | El módulo que la usa, leída contra el documento |
| El estado de la capa offline | `derecho/fuentes/MANIFIESTO.md`, que además tiene guardarraíl en los tests |
| Que un documento se puede o no transcribir | `herramientas/lecturas-ocr.json`, con la fecha y lo que se vio |

`CHANGELOG.md` **no se toca en cada sesión**: lleva versiones, no avances. Si un cambio no cambia la
versión, su lugar es una de las otras filas. Y **la entrada va corta**: una línea de encuadre y un
renglón por cambio. Lo que hay que explicar se explica donde se puede verificar, que es de lo que
habla la tabla de arriba; una entrada larga duplica ese texto y las dos copias se separan.

---

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) ·
[Auditorías](AUDITORIAS.md)
