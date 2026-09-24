# 🔧 Desarrollar el plugin

Acá está lo operativo: cómo probar, qué correr antes de cerrar un cambio, las convenciones y
dónde se anota cada cosa. Las reglas de criterio —la frontera de licencia, la disciplina de
verificación, qué no se asume del derecho argentino y cómo se escribe— están en
[`AGENTS.md`](../AGENTS.md). El porqué de cada guardarraíl está en el docstring del test que lo
sostiene, que es lo que se lee cuando se pone en rojo; lo que se decidió con fecha, en
[`BITACORA.md`](BITACORA.md).

## Probar sin instalar

```sh
claude --plugin-dir /ruta/al/repo/derecho
```

Dentro de la sesión, `/reload-plugins` toma los cambios sin reiniciar. Si el plugin además está
instalado desde el marketplace, la copia de `--plugin-dir` tiene precedencia en esa sesión.

Para probar el marketplace completo se lo agrega por ruta local:

```sh
claude plugin marketplace add /ruta/al/repo
claude plugin install derecho@derecho-argentino
```

Instalar hace una copia: los cambios posteriores no se ven hasta reinstalar. Para iterar,
`--plugin-dir`. `/help` → *Custom commands* confirma que los ocho comandos slash quedaron
registrados.

## En qué máquinas corre

Windows, Linux y macOS, con **Python 3 y nada más** para la skill, los descargadores y casi todas
las herramientas. Tres herramientas de auditoría del repositorio necesitan binarios, y ninguna
hace falta para usar la skill:

| Herramienta | Necesita | macOS | Linux | Windows |
| --- | --- | --- | --- | --- |
| `auditar_fechas_fallos.py` · `calidad_ocr.py` | `pdftotext` | `brew install poppler` | `apt install poppler-utils` | `choco install poppler` |
| `reocr_jurisprudencia.py` | `pdfinfo`, `pdftoppm`, `tesseract` con español | `brew install poppler tesseract tesseract-lang` | `apt install poppler-utils tesseract-ocr tesseract-ocr-spa` | `choco install poppler tesseract` |

Si falta el binario, la herramienta **se planta y dice qué instalar** (`herramientas/_externos.py`).
No hay verde por ausencia de instrumento: la regla está en `.claude/rules/herramientas.md`.

**Fines de línea.** `.gitattributes` fija `eol=lf` para todo el repositorio, y `frontera_kb.py`
hashea el texto con los saltos normalizados y arma las claves con `as_posix()`. Las dos defensas
existen porque un checkout CRLF cambia el hash de los 109 archivos de `kb/` sin cambiar una letra, y una
alarma que suena entera se calla con `--fijar`, que es lo que el guardarraíl existe para impedir.

## Antes de dar por terminado un cambio

```sh
claude plugin validate ./derecho --strict
python3 -m unittest discover -s derecho/skills/derecho-argentino/scripts -p "test_*.py"
python3 -m unittest discover -s herramientas -p "test_*.py"
python3 derecho/skills/derecho-argentino/scripts/estado.py
python3 herramientas/fuga_textual.py derecho/skills/derecho-argentino/SKILL.md \
    derecho/skills/derecho-argentino/references/*.md derecho/evals/*/*.md docs/AUDITORIAS.md docs/BITACORA.md
python3 herramientas/frontera_kb.py
python3 herramientas/deuda_vencida.py
```

En orden: que el plugin sea válido; que corran **los dos árboles de suites** —no comparten
`discover` porque no comparten raíz—; que los datos estén al día; que no se haya filtrado prosa de
`kb/` a la capa 3; que `kb/` no haya cambiado sin que nadie lo decida; y que ningún reclamo de
faltante haya quedado desmentido por `fuentes/`.

**Las suites se descubren, no se enumeran.** Un archivo nuevo que empiece con `test_` entra solo,
acá y en CI. Un test que no está en el checklist es un test apagado, y una lista enumerada a mano
es la forma de que aparezca uno.

**Y que no dependa de acordarse:** `git config core.hooksPath herramientas/hooks` instala el
`pre-commit`, que corre el verificador de documentación antes de cada commit que toque un `.md`.
Hace falta el `git config` porque `.git/hooks/` no se versiona, y se saltea con `--no-verify`: es
una ayuda. La aduana es `.github/workflows/tests.yml`, que corre las mismas suites en cada push y
en cada pull request.

## Cada cosa se explica en un solo lugar

Un porqué escrito dos veces se separa. Hay un lugar por tema, y el resto remite:

| Qué se explica | Dónde vive |
| --- | --- |
| Una convención del repositorio, y por qué | **`docs/DESARROLLO.md`** |
| Una regla que hay que tener en la cabeza antes de tocar algo | **`AGENTS.md`** |
| Lo que sólo vale para Claude Code | **`CLAUDE.md`**, que es un `@AGENTS.md` y tres líneas más |
| La capa offline: qué hay, de dónde salió, cómo se verifica | **`derecho/fuentes/MANIFIESTO.md`** |
| El mapa de licencias por ruta | **`LICENCIAS.md`** |
| Qué hace un script y cómo se corre | Su **docstring** |
| Qué herramientas de estado hay y cómo se corren | La salida de **`herramientas/pendientes.py`**, que las nombra al cierre |
| Por qué existe un guardarraíl y qué error atrapa | El **docstring de su test** |

**La remisión nombra el archivo y después el título de la sección entre comillas angulares**, y
`TestPunterosDeSeccion` comprueba que ese encabezado exista. Lo que sí se repite a propósito: el
encabezado de cada módulo de `references/` (un módulo se lee solo), la invocación en cada archivo
de `commands/`, la declaración de la zona horaria en los tres árboles de scripts
(`TestUnaSolaZonaHoraria`) y la terna de un eval junto a su `prompt.md`, mientras dure la
migración.

### Los cuatro destinos de una regla

| Si la regla… | va en | y no pasa de |
| --- | --- | --- |
| rige **siempre**, o errar es irreversible | `AGENTS.md`, o `.claude/rules/<tema>.md` declarada siempre-activa | 200 / 120 renglones |
| rige **al tocar** cierto árbol | `.claude/rules/<tema>.md`, con `paths:` | 120 renglones |
| es orientación para leer, no instrucción | `docs/` | sin tope |
| explica por qué existe un guardarraíl | el docstring de su test | sin tope |

Las tres reglas de hoy —`prosa.md`, `derecho-argentino.md` y `herramientas.md`— son
siempre-activas, y **ninguna usa la segunda fila**: una regla con `paths:` carga sólo cuando Claude
lee un archivo de esa ruta con `Read`, y leer con `cat` o `grep` por Bash no la carga. Una regla
cuya vigencia depende de con qué herramienta se leyó un archivo no rige.

Entre `AGENTS.md` y una regla siempre-activa decide **el tope por archivo**, no el contenido: el
umbral de adherencia es por archivo, así que repartir deja cada uno bajo el suyo. Lo exige
`TestDondeVaCadaRegla`, que falla si un archivo pasa su tope, si aparece una regla que esta tabla
no nombra o si `AGENTS.md` no la nombra por su ruta: `.claude/rules/` es un mecanismo de Claude
Code, y quien trabaja en Codex las abre a mano.

## Los archivos de veredicto

Todos los detectores reportan **candidatos, no culpables**. El archivo de veredicto guarda lo que
alguien leyó, con fecha, y es lo que hace que la lista baje en vez de crecer. Todos comparten un
sobre:

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

| Archivo | Carga | Lo consume | Reporta muertos |
| --- | --- | --- | --- |
| `herramientas/fuga-revisada.json` | `secuencias` | `fuga_textual.py` | no: recibe los archivos por argumento |
| `herramientas/cobertura-revisada.json` | `leyes` | `cobertura_normativa.py` | sí, con `--purgar` |
| `herramientas/lecturas-ocr.json` | `lecturas` | `calidad_ocr.py`, `reocr_jurisprudencia.py` | sí, sin purga: una lectura vale por su fecha |
| `herramientas/kb-procedencia.json` | `archivos` | `frontera_kb.py` | — |
| `herramientas/reformas-revisadas.json` | `reformas` | `reformas_no_leidas.py` | sí, con `--purgar` |
| `herramientas/cifras-revisadas.json` | `cifras` | `cifras.py` | sí, y se sacan a mano |
| `herramientas/deuda-revisada.json` | `reclamos` | `deuda_vencida.py` | sí, con `--purgar` |
| `herramientas/ramas-revisadas.json` | `ramas` | `ramas_sin_disparador.py` | no: un veredicto `rama` es una declaración y sobrevive al detector |
| `derecho/fuentes/normas/revisiones.json` | `revisiones` | `descargar_normas.py` | — |

**Una clave muere cuando el texto que la produjo cambió de redacción o se mudó de archivo.** No
esconde nada, pero infla el archivo, y una lista inflada se deja de leer. `_veredictos.muertos()`
las reporta igual en todas; **no se purgan solas**, porque una clave muerta guarda que ese texto
exacto ya se leyó, y perder esa memoria es una decisión de quien corre `--purgar`. Lo sostiene
`TestLosVeredictosNoSeLlenanDeMuertos`.

**La carga no se unifica.** Un conjunto de pertenencia (`secuencias`), un mapa de veredictos
(`leyes`, `lecturas`) y un mapa de listas (`revisiones`, porque una norma puede volver con más de
un defecto) son tres formas honestas; forzarlas a una registraría veredictos que nadie tomó.
**Tampoco hay un loader único**: `revisiones.json` vive dentro del plugin, que no puede importar
de `herramientas/`. Los demás pasan por `herramientas/_veredictos.py`; ése carga su sobre en
`_comun.py`. `TestSobreDeLosVeredictos` los lee a todos y falla si aparece uno sin declarar.

## Lo que un script imprime tiene que entrar en cp1252

En Windows la consola suele estar en cp1252, y un `print()` de un carácter que no entra termina en
`UnicodeEncodeError` **después** de haber hecho el trabajo. **Los acentos no son el problema:**

| Carácter | Entra en cp1252 |
| --- | --- |
| `á` `é` `í` `ó` `ú` `ñ` `ü` `·` `—` `«` `»` `¿` `¡` | **Sí.** Se pueden imprimir |
| `→` `✔` `≥` `│` `─` y el resto de flechas, tildes y caracteres de dibujo | **No.** Rompen la corrida |

Se verifica corriendo los scripts de verdad, sobre las herramientas que no necesitan binarios ni
red. **Y la salida va acentuada**: lo que una calculadora imprime se copia a un escrito, y un
rubro que dijera `Indemnizacion por antiguedad` entra así a una demanda. En el fuente —comentarios
y docstrings— también, porque varios docstrings se imprimen enteros en `--help`. Lo sostienen
`TestProsaAcentuadaEnElFuente` y `TestSalidaAcentuadaEnTodoElRepo`.

### Ortografía: el piso corre siempre, el techo a mano

Los tests de la suite son reglas —`-ción`, la ñ transliterada, determinante más sustantivo, `se`
más pretérito— y corren sin red. El corrector con diccionario y gramática necesita Java y baja
LanguageTool, así que **no entra al checklist**: un candado que tarda minutos se termina salteando.

```sh
uv run --with language-tool-python --with jdk4py python3 herramientas/ortografia.py
```

Mide lo que el repositorio **versiona**, que se lo pregunta a git. Cada regla apagada lleva su
motivo y su medición al lado, en el propio script; antes de apagar otra, medirla: si se equivoca
sobre todos los casos conocidos no sirve, y si acierta sobre alguno se arregla ese caso. Qué se
acentúa y qué es contrato no se decide acá sino en `.claude/rules/prosa.md`; lo que sí es de este
archivo son cinco decisiones de estilo que el corrector exime a propósito:

- **`sólo` con tilde y los demostrativos pronominales** —`éste`, `ésa`, `aquéllas`— se conservan:
  es la ortografía del foro y de los escritos que la skill produce. Si alguna vez se revierte, se
  revierte entero.
- **`contencioso administrativo` va sin guion en prosa propia**, y con el que traiga la fuente
  dentro de una cita. Es lo que hacen las normas de PBA y las nacionales, y
  `TestContenciosoAdministrativoSinGuion` exime la línea entrecomillada o citada con `>`.
- **`la fuente` es la fuente del derecho y `el fuente` es el código**; `el checklist`, `la suite`
  y `la tilde` llevan ese género. `TestGiroPropio` avisa si el reparto de `fuente` se empareja.
- **La coma delante de `pero`** va cuando une dos oraciones, no cuando coordina dos predicados
  del mismo sujeto. El corrector reclama las dos; la segunda se saltea leyendo.
- **Un pase automático sobre comentarios toca sólo el texto del comentario, nunca la línea**: la
  línea mixta —código y comentario— renombra constantes si se trata entera como prosa.

## Las cifras de la documentación no se escriben a mano

Cada vez que un documento dice cuántos módulos, normas, fallos o casos hay, afirma algo que
envejece solo:

```sh
python3 herramientas/cifras.py            # verifica y censa
python3 herramientas/cifras.py --sellar   # reescribe cada cifra con lo que hay en disco
```

**El ancla es el patrón de texto que rodea la cifra**, registrado en `herramientas/cifras.json`;
los `.md` no llevan marcas adentro porque la mitad viajan dentro del plugin y los lee el modelo.
**El censo** busca cualquier cifra pegada a un sustantivo de inventario y exige que esté declarada:
en las anclas, en la lista de las que ya mide otro test, o en `cifras-revisadas.json` con motivo.
Lo que no esté en ninguno rompe. Tres reglas para tocar una cifra:

- **Un ancla engancha exactamente una vez.** Si engancha dos, la cifra está escrita dos veces; se
  saca la repetida, no se alarga el ancla.
- **Toda cifra sellada necesita una definición ejecutable.** La que no se puede definir no se
  puede verificar, así que se saca de la prosa.
- **Si la cifra no informa, mejor que no esté.**

**Una cifra que cambia según dónde se mide no es una cifra.** `mb_instalados` es lo que descarga
quien instala, o sea lo que el repositorio **versiona**: la métrica le pregunta a `git ls-files`
y se planta si no hay git. `TestElPesoSeMideIgualEnCualquierMaquina` lo sostiene. Por lo mismo,
antes de pushear algo que cuente archivos se mide contra un clon y no contra una copia:

```sh
git clone . /tmp/runner && git diff HEAD > /tmp/wip.patch
git -C /tmp/runner apply /tmp/wip.patch
git ls-files --others --exclude-standard | tar cf - -T - | (cd /tmp/runner && tar xf -)
cd /tmp/runner && python3 -m unittest discover -s herramientas -p "test_*.py"
```

El tercer renglón no es opcional: `git diff HEAD` no trae los archivos nuevos, y se copian así y
no con `git add -N` porque en este repositorio no se corre `git add`.

**Qué entra al censo.** Todo lo que `cifras.json` declara en `alcance`, incluidos los módulos: el
censo no busca números sino **número más sustantivo de inventario**, así que los artículos y las
etapas de una norma no disparan. Una exclusión se escribe después de mirar qué reporta, no antes.
`AUDITORIAS.md`, `REVALIDAR.md` y `BITACORA.md` quedan afuera porque son registros fechados:
sellarles una cifra convertiría en dato vivo lo que vale por el día en que se midió.

## Dos agentes, un solo archivo de reglas

El contenido va en `AGENTS.md`, que es lo que lee el agente que **no** tiene con qué importar;
`CLAUDE.md` es un `@AGENTS.md` y lo poco que sólo vale para Claude Code. `TestLosDosAgentesLeenLoMismo`
ataja las tres formas de romperlo: que se borre la importación, que quede entre acentos graves
—ahí es texto literal— o que alguien copie el contenido y queden dos copias. **Symlink no**: en
Windows pide permisos y en un clon puede aparecer como un archivo de texto con una ruta adentro.
`.claude/settings.json` está versionado por el `claudeMdExcludes` que evita que los `CLAUDE.md` de
`kb/` entren como instrucciones.

## markdownlint sirve para prospectar, no para bloquear

El verificador del repositorio es `herramientas/test_markdown.py`: sin dependencias, corre en CI y
mira lo que se rompe en silencio —links, anclas, cercas, imágenes, acentos, cifras, marcadores
partidos—. `markdownlint` es un tercero con otros ojos:

```sh
npx --yes markdownlint-cli2          # avisa
npx --yes markdownlint-cli2 --fix    # arregla lo mecánico
```

No está en el checklist ni en CI, para no sumar Node a un repositorio que corre con Python de
fábrica. Lo que valga la pena de una corrida se implementa en `test_markdown.py`. La corrida da
cero, con cada regla arreglada o apagada con motivo en `.markdownlint-cli2.jsonc`; `--fix`
reescribe archivos, así que su `ignores` deja afuera la capa 2, y un test lo controla. El estilo
de tabla está fijado en `compact`. Antes de cambiar la forma de una tabla, buscá quién la parsea.

## Si escribís contenido

| Lo que escribís | Licencia |
| --- | --- |
| Un módulo de `references/`, un comando, un eval, documentación | **CC BY-SA 4.0**: atribución y CompartirIgual |
| Un script, una herramienta, un manifiesto `.json` | **MIT** |
| Cualquier cosa bajo `derecho/kb/` | **No se escribe ahí.** Es capa 2, de Cristian Aboitiz |

CompartirIgual tiene una consecuencia si aceptás aportes: el autor puede relicenciar su obra,
pero lo que aporte un tercero bajo CC BY-SA no, salvo cesión expresa. El mapa completo está en
[`LICENCIAS.md`](../LICENCIAS.md) y la regla de la frontera en [`AGENTS.md`](../AGENTS.md),
sección «La frontera de licencia». Los dos detectores: `fuga_textual.py` compara los módulos
contra `kb/` y reporta secuencias de nueve palabras compartidas —texto legal o dato va a la base
con `--aceptar`; prosa de `kb/` se reescribe—, y `frontera_kb.py` avisa cuando `kb/` cambia, y se
fija con `--fijar --nota '...'` si el cambio es querido. Los evals entran al primero igual que los
módulos: los 54 casos dan cero prosa. `kb/` queda fuera del verificador de documentación porque
es de otro autor y no sigue estas convenciones.

Antes de escribir sobre un instituto: leer el texto en `derecho/fuentes/normas/`, que está
consolidado con URL, fecha y hash, con `scripts/articulo.py` para no cargar el archivo entero. El
vocabulario de marcadores es el de `references/marcadores.md`. Cada bloque nuevo o corregido lleva
su fila en `references/changelog-normativo.md` —fecha y volatilidad— y en `docs/REVALIDAR.md`
—contra qué texto se cotejó—, **en el mismo orden**: `TestLasDosMitadesDeLaVerificacion` exige las
mismas filas por el par bloque y módulo, y una fila que no verifica nada no va, porque reinicia el
reloj de los seis meses sin que nadie haya vuelto a leer la norma.

### Un monto se escribe sólo si la norma le pone ventana

La pregunta no es si el monto es reciente sino **si tiene vencimiento escrito**. Un monto con
cronograma —del tal fecha al tal otra— entra a la tabla con su ventana, y pasada la fecha se ve
vencido solo. Un valor corriente sin fin escrito, como el SMVM, se emite por marcador: guardado
envejecería en silencio pareciendo vigente. Al bajar una norma de montos, leerla para ver si trae
cronograma.

### Dos puertas de entrada, dos detectores

Una norma **citada con articulado** en un módulo la reclama `cobertura_normativa.py`; una
**nombrada en «Cambios recientes»** de `changelog-normativo.md` la reclama
`TestNormasDeCambiosRecientes`. Las dos tienen la misma salida: o la norma está declarada en
`normas.json`, o alguien escribió por qué no en `cobertura-revisada.json`. Al comparar números,
la clave es exacta y no por subcadena. Y el detector de cobertura lee **el slug** para saber qué
está declarado: una norma bajada por partes lleva su número en cada slug, como
`ley-22415-delitos`, o aparece citada y sin bajar teniendo el texto.

### `SKILL.md` se paga en cada conversación, y los módulos no

El cuerpo del `SKILL.md` entra completo al activarse la skill; los `references/` entran cuando el
modelo los abre. La documentación de Claude Code fija el objetivo en
[menos de 500 renglones](https://code.claude.com/docs/en/skills.md). `TestElPresupuestoDeSKILL`
mide la prosa contra ese objetivo y las filas de tabla contra un **trinquete**: lo que se queda
arriba son las dos tablas que no pueden mudarse, el ruteo de la sección 16 y el vocabulario de
marcadores que el modelo transcribe exacto. Todo lo demás va a `references/`, y la duplicación
entre el `SKILL.md` y un módulo se busca antes de escribir: cuando aparece, la copia del
`SKILL.md` es la que nadie actualiza.

**0.1 bis dice hasta dónde llega; la sección 16 dice qué abrir.** Son dos tablas de materia
contra módulo, y `TestLaCoberturaNoRepiteElRuteo` las separa con dos reglas: una fila por materia
y no por módulo, y una fila tiene que decir algo además de a dónde ir.

### Cuándo se parte un módulo

**Un módulo no pasa de 1900 renglones** —`Read` trae 2000 y trunca sin avisar— y el tope vale
igual para el código: `TestNingunModuloSePasaDelCorteDeRead` y `test_el_codigo_tampoco_pasa_el_tope`.
Cuando salta, **se parte por materia y no por número**, y la numeración no se renumera: es global
y las remisiones apuntan a esos números. El módulo nuevo lleva su encabezado de nivel 2.

Pero el tope es el piso, no el motivo. Lo que se paga antes es el contexto: **se parte cuando el
bloque que sale no lo necesita el que se queda**. Si el que se queda lo va a abrir igual, el corte
no ahorró nada y sumó un lugar donde perderse; toda consulta carga además `SKILL.md`, `intake.md`,
`marcadores.md` y `plazos.md`, y cuando el módulo pesa menos que eso, partirlo no rinde.
`penal.md` queda entero por eso: la sección que dice qué código rige está en el mismo archivo que
cada instituto.

Por jurisdicción se parte mirando **dónde está la norma, no dónde tramita el expediente**:

| El derecho que se aplica es | Entonces | Ejemplos |
| --- | --- | --- |
| **Nacional y común** — CCyCN, LCT, LDC, Código Penal | Un solo módulo, y lo procesal se rutea aparte | `civil.md`, `laboral.md`, `consumidor.md` |
| **Local** — código procesal, código fiscal, ley arancelaria, régimen previsional | Un módulo por jurisdicción, con la jurisdicción en el nombre | `tributario` / `-pba` / `-caba`; `honorarios-nacional` / `-pba` / `-caba` |
| **Local, pero la skill sólo tiene una jurisdicción** | Un módulo, y el título dice cuál | `notificaciones-pba.md`, `contencioso-pba.md` |

No se parte por fuero dentro de una jurisdicción: un fuero nuevo entra como sección mientras
quepa. Y el título del módulo declara hasta dónde llega, porque el nombre del archivo no puede:
cuando no dicen lo mismo, manda el título. La sede judicial es el molde: **el modo** —qué se
controla de oficio, qué significa cada marcador— no tiene fuero y vive en `sede-judicial.md` 1.6;
**la pieza que firma** es de cada fuero y va en el suyo, 1.8 y 1.9 y no subsecciones de 1.6
porque 1.6.1 a 1.6.10 ya eran de PBA. Qué fuero hereda el código de otro se lee, no se deduce.

**Partir arrastra nueve cosas**, y la suite reclama ocho: la fila de ruteo, `DISPARADORES` en el
test de activación, el `description` del `SKILL.md`, una consulta en `evals/RUTEO.md`, el veredicto
de `ramas-revisadas.json`, las filas de la tabla de verificación, `docs/COBERTURA.md` y las cifras
de módulos. La novena son las remisiones cruzadas desde otros módulos, y se busca a mano:

```sh
grep -rn '`penal\.md` 24\.9' derecho/skills/derecho-argentino/references/
```

### Lo que un módulo declara

- **Dónde termina.** Cada módulo de rama cierra con «Lo que este módulo NO hace», con el
  encabezado exacto: un módulo que no dice dónde termina se lee como si no terminara, y el modelo
  completa el hueco. `TestLosModulosDeclaranSuBorde` es un trinquete sobre el reparto.
- **Su número, si se lo cita por número.** `civil.md 42`, `civil.md, 42` y `civil.md sección
  42` son la misma dirección, y `TestLasRemisionesApuntanAUnaSeccionQueExiste` las mira todas. Una
  remisión que sale del módulo nombra el archivo.
- **Un marcador prohibido se nombra, pero no se emite.** Entre acentos graves y desnudo,
  `` `[VERIFICAR RÉGIMEN APLICABLE]` `` lo nombra para decir que no se use; con dos puntos y
  motivo lo emite, y eso falla: `test_un_marcador_prohibido_no_se_puede_emitir`.

### La skill no nombra lo que no se instala

Lo que el plugin distribuye es `derecho/`. `herramientas/`, `docs/`, `AGENTS.md`, `LICENCIAS.md` y
`.github/` se quedan en el repositorio, así que un módulo que los nombra manda al lector a una ruta
que en su copia no existe, y el lector es el modelo: completa el hueco. Y el que usa la skill no
tiene que pagar contexto por leer cómo se mantiene el repositorio:

| Qué | Dónde |
| --- | --- |
| La regla operativa —de dónde sale la fecha de un fallo, que una cita literal se coteja— | El módulo |
| Cómo se llegó a ella, con qué se midió y qué se descartó | `docs/AUDITORIAS.md`, con su fecha |
| Con qué texto se cotejó un bloque de la tabla de verificación | `docs/REVALIDAR.md` |
| Qué comando lo regenera o lo vuelve a medir | Acá, o el `--help` de la herramienta |

Lo sostiene `TestLaSkillNoNombraLoQueNoSeInstala`, que mira `SKILL.md` y `references/` y no baja a
`evals/`: el lector de un `PROCEDIMIENTO.md` es quien escribe evals, que trabaja en el checkout. Y
la suite de `scripts/` **se planta fuera del checkout**: dos tercios de sus tests miden el
repositorio, y el `load_tests` levanta `SkipTest` con el motivo escrito cuando no encuentra
`.claude-plugin/marketplace.json`.

### Una rama entra por módulo o por sección, y la sección necesita disparador

**Un fuero nuevo entra entero o no entra**: módulo con fuente primaria a la vista, normas bajadas
por el descargador, fallos leídos y su caso de prueba. **Una materia** —gas, cooperativas,
propiedad horizontal— no es un fuero: es un cuerpo normativo que cae dentro de un módulo que ya
existe, y entra como sección:

| | Fuero, como módulo | Materia, como sección |
| --- | --- | --- |
| Norma bajada y cotejada | sí | sí |
| Marcador de lo que no recorrió | sí | sí |
| Fila en `changelog-normativo.md` y en `REVALIDAR.md` | sí | sí |
| **Disparador de ruteo** | sí | **sí, y es lo que se olvida** |
| Caso de prueba propio | sí | no |
| Fila en la tabla de ruteo con nombre de rama | sí | no: la comparte con su módulo |

Una sección no se rutea sola: la tabla de la sección 16 manda a un módulo y el `description` activa
la skill por materia. Lo mide `ramas_sin_disparador.py`, con veredicto en `ramas-revisadas.json`
—`rama` o `no-es-rama`—, y es un piso: una sección cuyo encabezado no nombra su ley no se detecta.
Escribir el número de la ley en el encabezado es lo que hace que la próxima sí.

### Correr los evals con `claude plugin eval`

El estado de la migración está en `docs/PENDIENTES.md`, sección «El formato de los casos de
prueba». Lo que cuesta averiguar corriéndolo:

- **Los casos viven abajo del plugin** y se instalan con él: `--eval-dir` es un directorio bajo el
  plugin y el manifiesto no tiene campo de exclusión. Es una restricción de afuera.
- **El runtime sí los lee**: `modelos.md` 23.8 manda a los `resultado.md` para la forma, no para
  el contenido, porque un `resultado.md` no tiene fila de verificación y no puede vencer.
- **El formato sale de `claude plugin eval init --bare`**. `focus:` en un grader `llm` está
  rechazado. `max_turns: 10` no alcanza; con 30 llega. `Bash` en `allowed_tools` exige
  `--allow-tools` y un sandbox, y estos evals miden doctrina, así que corren sin shell.
- **Un hecho por grader**, y los negativos deterministas: un criterio `llm` con varias
  afirmaciones falla por la más débil, y pedir que algo no aparezca reprueba respuestas correctas.
- **Cuesta**: del orden de un dólar y varios minutos por corrida. Va a mano antes de publicar,
  siempre con `--keep-temp`, y la traza se revisa apenas termina con `herramientas/traza_eval.py`:
  el agente evaluado corre contra el repositorio vivo y nada le impide abrir la rúbrica o los
  graders del caso que resuelve. La traza vive en `/tmp` y se pierde; la herramienta se planta con
  rc=2 cuando ya no está.

### Una serie que publica por cambio no tiene huecos

El jus de la SCBA y la UMA de la CSJN publican cuando el valor cambia: un período ausente no
falta, significa que el anterior sigue rigiendo, y los lectores toman la última vigencia que no
es posterior a la fecha pedida. Lo que sí se mide es cuándo alguien abrió la tabla oficial por
última vez, que es la línea `# verificado:` de cada csv.

## Qué queda pendiente

La deuda medible se lee de donde está anotada —el marcador en el módulo, la tabla de verificación,
el veredicto de lectura— y la vista es `herramientas/pendientes.py`, que además es el inventario
de herramientas: informa, no bloquea. Lo que ninguna herramienta puede medir está en
[`docs/PENDIENTES.md`](PENDIENTES.md): decisiones abiertas, restricciones que no se levantan y
trabajo de fondo.

## Mantenimiento

Desde Claude Code, `/derecho:verificar` y `/derecho:actualizar`; desde la app de escritorio, en
castellano. A mano:

```sh
python3 derecho/fuentes/scripts/verificar_normas.py            # ¿cambió alguna norma del manifiesto?
python3 derecho/fuentes/scripts/verificar_normas.py --slug <slug> --verboso   # una sola, sin escribir
python3 derecho/fuentes/scripts/descargar_normas.py --slug <slug>             # bajar o rebajar un texto
python3 derecho/fuentes/scripts/descargar_jurisprudencia.py    # los fallos del catálogo
python3 derecho/fuentes/scripts/descargar_series.py            # IPC, CER y RIPTE
python3 derecho/fuentes/scripts/diagnostico.py                 # conectividad de los descargadores
```

`verificar_normas.py` vuelve a pedir cada URL, compara el hash contra `procedencia.json` y no
escribe nada sin `--sellar`. Sus códigos de salida separan lo que importa: `0` verificó y no
cambió, `1` cambió, `2` **no se pudo verificar**, que no es estar bien. **Corre sola los lunes** en
`.github/workflows/verificar.yml`, que abre un issue con la salida entera si sale 1 o 2: avisar
sólo cuando algo cambió sería verde con el instrumento apagado. Un hash que cambió se mira con
`--slug --verboso` antes de decidir si es reforma o maquetación, y lo que resulte va a
`changelog-normativo.md`. **Un bloqueo de una fuente vale por su fecha**: anotarlo sin volver a
medirlo convierte una restricción de un día en una regla permanente.

Las series se bajan aparte porque vienen de otra fuente y vencen a otra velocidad; `estado.py`
dice cuáles quedaron viejas. Los `serie_id` del índice y de la variación del IPC difieren en un
carácter, así que bajar el equivocado deja un archivo con el formato correcto y los números de
otra cosa.

**Las herramientas que no miden pendientes**, y por eso no las nombra `pendientes.py`:

| Herramienta | Qué hace |
| --- | --- |
| `herramientas/ruteo.py` | mide el mapa: que desde el router se pueda llegar a cada módulo |
| `herramientas/frontera_kb.py` | fija y compara el hash de la capa 2 |
| `herramientas/ortografia.py` | el corrector con diccionario, a mano |
| `herramientas/auditar_fechas_fallos.py` | coteja la fecha de cada fallo contra su PDF |
| `herramientas/reocr_jurisprudencia.py` | vuelve a extraer un PDF con tesseract y deja la copia en `ocr/` |
| `herramientas/traza_eval.py` | revisa la traza de una corrida de evals |
| `scripts/verificar_respuesta.py` | el revisor de marcadores de una respuesta, dentro del plugin |

**`verificar_respuesta.py` es el único control que corre en tiempo de ejecución, y por eso se
instala.** Todo lo demás corre sobre el repositorio, antes de publicar; sobre lo que el modelo
escribe en la conversación de un usuario no corre nada, y ahí un modelo chico rompe escribiendo
`[Verificar Vigencia]` donde el vocabulario dice `[VERIFICAR VIGENCIA]`. Acepta sólo lo que
`references/marcadores.md` declara y no importa nada de `herramientas/`. Un verde suyo mide la
forma del marcador: no ve el que faltó emitir.

## La marca

<img src="../assets/marca/icono-128.png" width="72" align="right"
     alt="Ícono: sello cuadrado con la sigla AR">

El sello, el ícono, las chapitas y el separador están commiteados en `assets/marca/`, en SVG y en
PNG. **El generador no vive en este repo**: es la única parte con dependencias externas —Pillow y
fontTools— para algo que se corre una o dos veces por año, y está en `derecho-argentino-marca/`,
al lado, con su README. Regenerar pide las tipografías exactas: el texto se pasa a curvas y el
script no cae en una alternativa parecida. El detalle está en
[`assets/marca/README.md`](../assets/marca/README.md); `social-preview.png` se sube a mano en
*Settings → General → Social preview*.

## Publicar

Un commit por versión, y ninguna versión muestra sus etapas:

1. Rama `version-X.Y.Z` desde `main`, con **un solo commit** encima.
2. Mientras se trabaja, ese commit se corrige con `git commit --amend` y se sube con
   `git push --force` **sobre esa rama**. Nunca sobre `main`, que es lo único irreconstruible.
3. Cuando la versión cierra, entra a `main` por pull request. El mensaje es
   `versión X.Y.Z - <título de la versión>`, el mismo que encabeza su entrada del changelog.

El mensaje de commit no lleva el porqué de ningún cambio. Cada cosa se anota en su lugar:

| Qué cambió | Dónde se anota |
| --- | --- |
| La versión del plugin | [`CHANGELOG.md`](../CHANGELOG.md), **sólo al publicar una versión**, y corta: una línea de encuadre y un renglón por cambio |
| Contenido normativo o jurisprudencial | La tabla de estado de verificación de `references/changelog-normativo.md`, con fecha y volatilidad |
| Una auditoría contra fuente primaria, con lo que se leyó y lo que se encontró | [`AUDITORIAS.md`](AUDITORIAS.md) |
| Una partición, un eval corrido, un registro que se mudó: estructura, no derecho | [`BITACORA.md`](BITACORA.md) |
| Algo que se tocó bajo `derecho/kb/` | `derecho/kb/CHANGELOG.md`, y además `python3 herramientas/frontera_kb.py --fijar --nota '...'` |
| La doctrina de un fallo | El módulo que la usa, leída contra el documento |
| El estado de la capa offline | `derecho/fuentes/MANIFIESTO.md`, con guardarraíl en los tests |
| Que un documento se puede o no transcribir | `herramientas/lecturas-ocr.json`, con la fecha y lo que se vio |

---

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) ·
[Auditorías](AUDITORIAS.md)
