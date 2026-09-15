# 🔧 Desarrollar el plugin

Acá está lo operativo: cómo probar, qué correr antes de cerrar un cambio y las convenciones de
código. Las reglas de criterio —la frontera de licencia, la disciplina de verificación, qué no
se asume del derecho argentino y cómo se escribe acá— están en [`CLAUDE.md`](../CLAUDE.md), en
la raíz del repositorio.

## Probar sin instalar

Para trabajar sobre el plugin sin reinstalarlo en cada cambio, se carga el directorio
directamente:

```sh
claude --plugin-dir /ruta/al/repo/argentina
```

Ya dentro de la sesión, después de editar cualquier archivo:

```
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
(`herramientas/_externos.py`). Eso no es cosmética: `auditar_fechas_fallos.py` metía el
`FileNotFoundError` en el mismo `except` que usa para un PDF roto, así que en una máquina sin
poppler imprimía `0 A REVISAR` y salía con código 0 — los 64 fallos pasaban sin mirarse. **Si la
herramienta no puede medir, lo dice y se planta**; no hay verde por ausencia de instrumento.

### Fines de línea

`.gitattributes` fija `eol=lf` para todo el repositorio. **No es cosmética tampoco.**
`frontera_kb.py` es el guardarraíl de la frontera de licencia: fija el sha256 de los 109
archivos de `argentina/kb/`, que son capa 2 y de otro autor. Medido: con un checkout CRLF
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
claude plugin validate ./argentina --strict
python3 argentina/skills/derecho-argentino/scripts/test_scripts.py
python3 herramientas/test_frontera.py
python3 herramientas/test_auditoria.py
python3 herramientas/test_pendientes.py
python3 herramientas/test_reformas.py
python3 herramientas/test_markdown.py
python3 herramientas/test_cifras.py
python3 herramientas/test_fuga.py
python3 herramientas/test_cobertura.py
python3 argentina/skills/derecho-argentino/scripts/estado.py
python3 herramientas/fuga_textual.py argentina/skills/derecho-argentino/SKILL.md \
    argentina/skills/derecho-argentino/references/*.md argentina/evals/*/*.md
python3 herramientas/frontera_kb.py
```

En orden: que el plugin sea válido; que las calculadoras sigan dando lo mismo; que la
frontera de licencia, las herramientas de auditoría y el medidor de deuda sigan haciendo lo que
dicen; que la documentación no tenga links, anclas, tablas ni bloques rotos; que los nueve
bloques de datos estén al día; que no se haya filtrado prosa de `kb/` a un
módulo de la capa 3; y que `kb/` —que es de otro autor— no haya cambiado sin que nadie lo decida.

**El checklist va entero.** Un test que no está en el checklist es un test apagado, y uno
apagado es peor que uno que no existe: figura en el conteo y nadie lo corre. `test_scripts.py`
comprueba dos cosas para que eso no dependa de acordarse: que **cada `herramientas/test_*.py` esté
nombrado en este bloque**, y que **`.github/workflows/tests.yml` corra los mismos**. Un suite nuevo
rompe los tests hasta que entre a los dos lugares.

### Que no dependa de acordarse

El checklist de arriba es un procedimiento, y un procedimiento se olvida. Los mismos suites
corren solos en dos lugares:

```sh
git config core.hooksPath herramientas/hooks
```

Eso instala `herramientas/hooks/pre-commit`, que antes de cada commit que toque un `.md` corre el
verificador de documentación —un segundo— y frena el commit si encuentra algo. **Hace falta el
`git config` porque `.git/hooks/` no se versiona**: un hook suelto ahí adentro no viaja a un clon.
Se saltea con `--no-verify`, a propósito: es una ayuda, no una aduana.

La aduana es `.github/workflows/tests.yml`, que corre los mismos suites en cada push y en cada pull
request. Eso no se saltea y no hay que instalarlo. El hook es apenas el eco local y rápido de lo
mismo, para enterarse antes de pushear y no después.

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
| `argentina/fuentes/normas/revisiones.json` | `revisiones` | `descargar_normas.py` |

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

**En el fuente** —comentarios y docstrings— la costumbre es escribir sin acentos, y conviene seguirla
por consistencia. Eso es estilo y no tiene test.

**Y los identificadores nunca se acentúan.** Aprendido a fuerza de romperlo diez veces: el nombre del
tramo `modernizacion` que el código compara, las claves de `inhabiles.json`, los valores de `--tipo`,
las claves del JSON del perfil, un componente de ruta y las variables dentro de las llaves de una
f-string. Son ASCII a propósito, y acentuarlos rompe la interfaz o la lectura del dato — a veces con
un `KeyError` y a veces en silencio. La línea es: **si se muestra, se acentúa; si se compara, no.**

**Y no alcanza a los datos.** Una carátula de fallo lleva sus acentos porque es texto que se cita,
y hay un test que lo exige — ver `TestCaratulasAcentuadas`.

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

## markdownlint sirve para prospectar, no para bloquear

El verificador del repositorio es `herramientas/test_markdown.py`: no tiene dependencias, corre en
el CI y comprueba lo que se rompe **en silencio** —links, anclas, cercas, imágenes que dejaron de
renderizar, acentos, cifras, marcadores partidos—. `markdownlint` es lo otro: un tercero que mira el
árbol con otros ojos y encuentra lo que nuestro verificador no busca.

```sh
npx --yes markdownlint-cli2          # avisa
npx --yes markdownlint-cli2 --fix    # arregla lo mecánico
```

No está en el checklist de cierre ni en el CI, y es deliberado: agregar Node al camino de un
repositorio que hoy corre con Python de fábrica es un costo que el usuario del plugin no debería
pagar. **Lo que valga la pena de una corrida se implementa en `test_markdown.py`**, que sí corre
siempre. Así llegó el control de marcadores partidos: de los 9.868 avisos de la primera corrida, ése
fue el único defecto real, y es un invariante nuestro que ningún linter tiene.

La configuración está en `.markdownlint-cli2.jsonc` con el motivo de cada regla apagada al lado.
Dos cosas que conviene tener presentes:

- **`--fix` reescribe archivos**, así que su `ignores` tiene que dejar afuera la capa 2: `kb/` y las
  cinco excepciones de [`LICENCIAS.md`](../LICENCIAS.md). Un test lo controla, porque es la única
  herramienta del repositorio capaz de editarle a otro autor sin que nadie se lo pida.
- **El estilo de tabla va dicho, no inferido.** MD060 con el default `any` elige por tabla el estilo
  más cercano, y en las de celda larga elegía `aligned`, que exige alinear los pipes en columna: una
  celda de 1.545 caracteres no se alinea. Fijado en `compact` —un espacio de cada lado en toda
  celda, delimitador incluido— el `--fix` normaliza el árbol entero.

Un cambio de estilo de tabla no es cosmético: lo primero que hay que revisar es **quién parsea
tablas**. `pendientes.py` buscaba la fila delimitadora con `startswith("|--")`, que reconoce
`|---|---|` y no `| --- | --- |`, y el modo de falla era mudo: la fila pasaba como dato, `"---"` se
leía como nombre de bloque y el script no reportaba nada.

## Si escribís contenido

**Bajo qué licencia entra lo que escribas.** La frontera es la ruta y ahora tiene cuatro capas, con
el mapa completo en [`LICENCIAS.md`](../LICENCIAS.md):

| Lo que escribís | Licencia |
| --- | --- |
| Un módulo de `references/`, un comando, un eval, documentación | **CC BY-SA 4.0**: atribución y **CompartirIgual** |
| Un script, una herramienta, un manifiesto `.json` | **MIT** |
| Cualquier cosa bajo `argentina/kb/` | **No se escribe ahí.** Es capa 2, de Cristian Aboitiz |

Que el contenido sea CompartirIgual tiene una consecuencia si aceptás aportes: **el autor puede
relicenciar su propia obra, pero lo que aporte un tercero bajo CC BY-SA no**, salvo cesión expresa.

La regla que más se viola sin querer es la frontera con la capa 2, y es la ruta: bajo
`argentina/kb/` es capa 2 —Cristian Aboitiz, uso comercial con autorización previa—, fuera es de
este fork. **Se cruza en los dos sentidos y los dos importan.**

**Sentido uno: prosa de `kb/` que entra a un módulo.** Nunca se copia. Para llevar un instituto de
un perfil heredado a `references/`, se reescribe verificado contra fuente primaria. Las citas de
articulado, los plazos y las carátulas de fallos no son obra de nadie y se mueven libres; la prosa
no. `herramientas/fuga_textual.py` compara los módulos contra `kb/` y reporta secuencias de nueve
palabras compartidas, con una línea de base de lo ya revisado en `fuga-revisada.json`. Reporta
**candidatos, no culpables**: hay que leerlos. Si es texto legal o un dato, va a la base con
`--aceptar`; si es prosa de `kb/`, se reescribe el módulo.

**La trampa de este sentido no es copiar, es condensar.** Dos resúmenes de la misma fuente
convergen sin que nadie haya leído al otro: escribiendo el holding de un fallo sale "ni excusa el
incumplimiento" donde la Corte dice "ni resulta decisivo para excusar el incumplimiento", y esa
condensación ya estaba en `kb/doctrina/`. **Citar textual al tribunal, entre comillas, en vez de
resumirlo con palabras propias** evita el problema y además mejora la cita.

**Sentido dos: texto propio que sale hacia `kb/`.** Es el fácil de cruzar sin darse cuenta,
porque se cruza **corrigiendo**: el perfil heredado dice algo mal y la tentación es arreglarlo
donde se lee. No va ahí. Por la regla de la ruta esa corrección queda clasificada como obra de
otro autor, y encima **desactiva el sentido uno**: al reescribir la línea de `kb/` con palabras
propias, la coincidencia que `fuga_textual.py` busca desaparece. **Si el perfil heredado dice algo
mal, la corrección va al módulo de `references/`, y el bloque de contradicciones nominadas es el
que nombra el error, citándolo textual.** `herramientas/frontera_kb.py` avisa cuando `kb/` cambia;
si el cambio es querido, se fija con `--fijar --nota '...'`.

> **Los evals entran al detector, igual que los módulos.** Son capa 3 y se escriben con las
> mismas reglas, así que el comando de arriba los incluye. Los 18 casos dan **cero prosa**: sus
> coincidencias con `kb/` son articulado y carátulas de fallos, que se mueven libres. Un caso
> nuevo que copie prosa rompe el checklist, que es exactamente para lo que está.

> **Deuda conocida: `argentina/kb/` está fuera del verificador de documentación.** Esa capa es
> de otro autor y no sigue estas convenciones: tiene **312 líneas con espacios al final** en 6
> archivos, **2 tablas con filas de distinto ancho** —`administrativo-SALTA` y
> `administrativo-TUCUMAN`— y **un bloque de código sin cerrar** en
> `administrativo-CHACO-CLAUDE.md`, que al renderizar se come el resto del documento. El último
> es un defecto real y visible; los otros dos, cosmética. Se arreglan el día que se toque ese
> material, no antes: `kb/` no se modifica sin decisión previa.

> **Deuda conocida: la migración de los evals a `claude plugin eval` está empezada y parada.**
> `laboral-despido-tramos-reforma-pba` es el caso piloto —tiene `prompt.md` y `graders/` al lado
> de los tres archivos del formato manual— y los otros 16 siguen solo en manual. Lo que se
> verificó corriéndolo de verdad, para no volver a averiguarlo:
>
> - El formato sale de `claude plugin eval init --bare`, no de la documentación. `focus:` en un
>   grader `llm` está **rechazado** por el cargador.
> - `max_turns: 10` no alcanza: la skill se gasta los turnos leyendo sus propios módulos y la
>   corrida muere sin producir respuesta, con todos los graders fallando sobre un mensaje vacío.
>   Con 30 usa 18 y llega.
> - Declarar `Bash` en `allowed_tools` exige además `--allow-tools` **y** un sandbox instalado
>   (bubblewrap y socat), o el harness se niega a correr. Estos evals miden doctrina, no
>   aritmética —que ya tiene tests deterministas—, así que corren **sin shell**.
> - Cuesta entre US$ 0,67 y US$ 1,00 y entre 2 y 6 minutos por corrida. Con `runs: 3`, los 17
>   casos son entre 35 y 50 dólares la pasada: va a mano antes de publicar, no en cada push.
> - **Un hecho por grader.** Un criterio `llm` con cuatro afirmaciones adentro falla por la más
>   débil: dio FAIL con una respuesta correcta, que decía "9 años" donde el criterio pedía "9
>   períodos". Los graders deterministas —fecha, ley citada, marcador, skill disparada— no
>   fallaron nunca.
> - Dos corridas del mismo caso dieron **0.88 y 0.44**, y lo que falló en la segunda falló con
>   razón: describió el fuero como Tribunal del Trabajo colegiado y dejó el multiplicador de
>   antigüedad sin resolver entre la fecha real y la registrada. Esa varianza entre corridas es
>   el argumento más fuerte a favor de los evals, y no se ve leyendo una corrida a ojo.
>
> Antes de migrar los otros 16: ajustar a un hecho cada uno los cinco graders con juez del
> piloto y correrlo con `runs: 3`, para que el puntaje donde se estabilice sea el `--threshold`
> honesto.

Y antes de escribir sobre un instituto: leer el texto en `argentina/fuentes/normas/`, que está
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

## Qué queda pendiente

**No hay archivo de pendientes, y es a propósito.** Una lista escrita a mano se vence igual que
cualquier otra cifra escrita a mano, y además duplica lo que ya está anotado en su lugar: el
marcador vive en el módulo, la deuda normativa en la tabla de `references/changelog-normativo.md`,
el veredicto de lectura en `herramientas/lecturas-ocr.json`. Lo que faltaba era una vista, no un
registro nuevo:

```sh
python3 herramientas/pendientes.py
```

Lee los archivos y ordena cuatro cosas: los institutos con `[INSERTAR FALLO VERIFICADO]` —donde
hoy la skill entrega doctrina de `kb/` sin auditar, avisando que falta—, la deuda que la propia
tabla de verificación declara, los bloques que pasaron los seis meses de la regla de esa tabla, y
los módulos que ningún eval nombra. Al final remite a las herramientas que miden el resto:
`cobertura_normativa.py`, `calidad_ocr.py --pendientes` y `fuga_textual.py` sobre `evals/`.

No está en el checklist de cierre: informa, no bloquea.

## Mantenimiento

Desde Claude Code alcanza con `/derecho:verificar` y `/derecho:actualizar`; desde la app de
escritorio, pedírselo en castellano. A mano:

```sh
# ¿cambió alguna norma del manifiesto?
python3 argentina/fuentes/scripts/verificar_normas.py

# tests de los scripts de la skill
python3 argentina/skills/derecho-argentino/scripts/test_scripts.py

# diagnóstico de conectividad de los descargadores
python3 argentina/fuentes/scripts/diagnostico.py
```

`references/changelog-normativo.md` lleva la tabla de **estado de verificación por bloque**, con
la fecha de la última validación contra fuente primaria y una columna de volatilidad. Lo de
volatilidad alta —valor del jus, canasta de crianza, montos de la SRT, acordadas de feria— se
revisa antes de usarlo, no cada seis meses.

InfoLEG y `normas.gba.gob.ar` devuelven 403 a los agentes: esos descargadores se corren desde una
terminal propia.

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

El repositorio tiene **un solo commit sin padres**: se publicó sin historial a propósito, porque
lo que se ofrece para instalar es el estado revisado, no las etapas por las que pasó. Se sigue
trabajando con `--amend` sobre ese commit, lo que obliga a `git push --force`.

La consecuencia hay que tenerla presente: sin historial, el porqué de un cambio no queda en ningún
mensaje de commit. Hay que anotarlo, **pero cada cosa en su lugar**, o el registro se vuelve un
diario de trabajo que nadie lee:

| Qué cambió | Dónde se anota |
| --- | --- |
| La versión del plugin | [`CHANGELOG.md`](../CHANGELOG.md), **sólo al publicar una versión** |
| Contenido normativo o jurisprudencial | La tabla de estado de verificación de `references/changelog-normativo.md`, con fecha y volatilidad |
| Una auditoría contra fuente primaria, con lo que se leyó y lo que se encontró | [`AUDITORIAS.md`](AUDITORIAS.md) |
| Algo que se tocó bajo `argentina/kb/` | `argentina/kb/CHANGELOG.md`, y además `python3 herramientas/frontera_kb.py --fijar --nota '...'` |
| La doctrina de un fallo | El módulo que la usa, leída contra el documento |
| El estado de la capa offline | `argentina/fuentes/MANIFIESTO.md`, que además tiene guardarraíl en los tests |
| Que un documento se puede o no transcribir | `herramientas/lecturas-ocr.json`, con la fecha y lo que se vio |

`CHANGELOG.md` **no se toca en cada sesión**: lleva versiones, no avances. Si un cambio no cambia la
versión, su lugar es una de las otras filas.

---

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) ·
[Auditorías](AUDITORIAS.md)
