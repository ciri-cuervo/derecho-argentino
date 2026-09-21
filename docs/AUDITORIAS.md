# 📋 Auditorías contra fuente primaria

Registro de las auditorías que este fork corre contra `derecho/fuentes/`: qué se leyó, contra
qué texto, y qué se encontró. Es **capa 3a, CC BY-SA 4.0** — ver [`LICENCIAS.md`](../LICENCIAS.md).

**Una auditoría vale por su fecha**, así que cada entrada la lleva: dice **contra qué texto se
cotejó y cuándo**. Varias anotan además dónde se corrigió lo que encontraron, y se quedan como
están: es parte de lo que se hizo ese día. Lo que no va acá es el cambio sin el cotejo — para eso
están `references/changelog-normativo.md` y `derecho/kb/CHANGELOG.md` —este último es el
historial de la base heredada, capa 2, y la frontera de licencia es la ruta—.

**El orden es de la más nueva a la más vieja, y una entrada no se reescribe.** Si un hallazgo
posterior la supera, se anota **debajo de la entrada**, con su fecha, y la original queda: lo que
se registró es lo que se verificó ese día. Las tres entradas de septiembre entraron en el mismo
commit, así que su orden relativo no sale de una fecha sino de sus referencias internas —la de la
Ley 15.057 cita a la normativa cruzada como anterior—; la de fuentes doctrinarias no tiene ninguna
que la ubique y quedó al final.

Lo que va en cada lugar:

| Qué | Dónde |
| --- | --- |
| Una auditoría de este fork contra fuente primaria | **Este archivo** |
| El estado de verificación por bloque, con fecha y volatilidad | `references/changelog-normativo.md` |
| Un cambio en la base heredada | `derecho/kb/CHANGELOG.md`, y sólo si se tocó `kb/` |
| La versión del plugin | [`CHANGELOG.md`](../CHANGELOG.md), sólo al publicar |

---

## 19/09/2026 - Diez hallazgos de una evaluación del plugin en runtime, verificados uno por uno

La evaluación vino de afuera: otra corrida leyó el plugin instalado y reportó diez problemas.
**Ninguno se tomó por bueno.** Cada uno se midió con un comando, y **tres no se sostienen como
estaban dichos**: `verificar_respuesta.py` no aparece «una sola vez» sino seis —lo que sí es
cierto es que ningún comando lo corre—; de las «tres cifras mal» en `/derecho:verificar` hay
**una** —el `--help` no dice ninguna, y el «ciento cuarenta y siete» es un docstring que narra
otra cosa—; y la corrección del conteo de `evals/README.md` **no se puede hacer**: es una de las
cinco excepciones de capa 2 que declara `LICENCIAS.md`, y ahí no se corrige ni el contenido ni la
ortografía. La discrepancia se nombra afuera, como cualquier otra de esa frontera.

**Lo que sí estaba, y es lo que más costaba en uso real: la skill se negaba a regular en la
justicia nacional teniendo el dato.** `uma_csjn.py --fecha 2026-09-01` devuelve el valor y la
resolución que lo fijó, con la serie cargada desde el 01/10/2024 — y **cuatro** textos decían que
`uma-csjn.csv` estaba vacío: el párrafo y el marcador enlatado de `/derecho:honorarios`, y dos
lugares de `honorarios-nacional.md`, uno de ellos cinco renglones arriba de un marcador que ya
decía lo correcto. **El marcador enlatado es lo peor de los cuatro**: afirmaba un estado falso de
la propia base, y un marcador que miente sobre la base es peor que no emitirlo. El defecto tenía
un día: la serie se cargó el 18/09 y la prosa quedó atrás.

**De ahí el guardarraíl, porque la clase se repite:** decir que una serie está vacía es una
afirmación sobre el disco, y vence sola cuando la serie se carga.
`TestLoQueLaProsaAfirmaDeLaSerie` cruza `references/` y `commands/` contra los csv de
`fuentes/datos/` y falla nombrando el archivo y las filas que tiene. No confunde la condicional
—«si la serie está vacía el script se planta» describe al script, no al disco—, y ese límite lo
ejercita un test propio.

**`/derecho:estado` informaba verde sin haber medido.** El comando corre la suite con `tail -3`, y
desde la copia instalada las seis suites se plantan a propósito —falta
`.claude-plugin/marketplace.json`—. El motivo va en el **primer** renglón de la salida y el
recorte se lo llevaba: lo único que quedaba a la vista era `OK (skipped=1)`. Comprobado copiando
el plugin afuera del repo y corriéndolo. Es la alarma que no suena nunca, adentro del comando que
existe para diagnosticar. Quedó en `tail -6`, con la instrucción de decir *no se midió*, y el test
no fija el número: corre la suite como la corre el usuario instalado y exige que el motivo
sobreviva al recorte que el comando escriba.

**Y el censo de cifras estaba apagado justo donde envejeció la cifra.** `cifras.json` excluía
`derecho/commands/` con el motivo *"describen qué hacer, no cuánto hay"*, y `/derecho:verificar`
decía «son 55 normas» cuando las normas con URL del manifiesto ya eran varios cientos: la
exclusión afirmaba algo sobre el contenido y era falso. Entrados los ocho comandos al alcance, el
censo levantó **exactamente esa** cifra y ninguna otra. Es la misma forma que tuvo `references/`
cuando entró tarde, y la regla es la de entonces: **una exclusión es una afirmación, y se mide
como cualquier otra.**

**Los cuatro frentes que abrió esta auditoría, cerrados el mismo día:**

- **La clave de respuestas era legible para el agente evaluado.** `rubrica.md`, `graders/` y
  `resultado.md` viven al lado del caso, en el repositorio contra el que corre. En las dos trazas
  que sobrevivían no había ninguna lectura de `evals/`, pero **de la corrida del 18/09 no quedaba
  ninguna de las seis**: el sandbox se borra y con él la prueba. `herramientas/traza_eval.py` lee
  el `tracePath` de cada brazo, rompe si se abrió una rúbrica, un `graders/` o el propio caso,
  avisa si se abrió el `resultado.md` de otro —que 23.8 declara— y **se planta con rc=2 cuando la
  traza ya no está**: no hay verde por ausencia de instrumento.
- **`modelos.md` 23.8 afirmaba que el contenido normativo de los evals estaba verificado.** No
  puede estarlo: un `resultado.md` no tiene fila en `references/changelog-normativo.md` ni en
  `docs/REVALIDAR.md`, así que ninguna reforma lo va a marcar. Quedó dicho lo que sí son —**la
  forma**: qué se resuelve antes del fondo, qué marcador va en cada hueco— y que lo normativo sale
  del módulo y de `fuentes/`. `DESARROLLO.md` decía además que *"ningún módulo rutea a `evals/`"*,
  que era falso desde que 23.8 existe.
- **La `description` pasó de 1.463 a 1.016 caracteres**, que es el tope de la API de Skills, no el
  1.536 de la truncación de Claude Code. Cada carácter que salió es un disparador que salió, así
  que el recorte se hizo contra el control que exige una activación por rama — y ese control
  comparaba por **subcadena**: `ART` daba por activado a `laboral-riesgos.md` desde adentro de la
  palabra «parte». Ahora compara por palabra completa, y fue lo que atrapó la rama de servicios
  públicos que el recorte había dejado sin «luz».
- **Las cinco licencias viajan adentro del paquete.** `plugin.json` declaraba `SEE LICENCIAS.md`
  y el archivo se quedaba en la raíz del repositorio: el plugin distribuye capa 2 y quien lo
  instala tiene que poder leer bajo qué términos. Son copias byte a byte y un test exige que no se
  separen — lo comprobó el mismo día, cuando `cifras.py --sellar` reescribió la de la raíz y dejó
  la copia atrás.

**Lo que sigue abierto:** `evals/README.md` dice que **un** caso está migrado y son siete, y no se
corrige porque es capa 2; el conteo de `verificar_respuesta.py` sigue sin comando propio ni paso de
cierre en `escritos.md` 11 —se agregó sólo como paso del procedimiento de evals—; y la herramienta
de la traza sólo puede medir **pegada** a la corrida, así que la disciplina de correrla es parte
del procedimiento y no algo que el repositorio pueda comprobar solo.

---

## 15/09/2026 - Seis normas citadas sin texto, y cómo se cierra ese frente

Entrada trasladada: el registro estaba en el cuerpo de `references/changelog-normativo.md`, que la
skill carga en cada consulta. **Es contabilidad de deuda del repositorio, no derecho**, y por eso
pasa acá.

**Qué se bajó.** Seis leyes que los módulos citaban con articulado y sin texto: la **Ley 27.798**
—Presupuesto 2026, por su art. 62—, las **Leyes 25.390, 26.200 y 26.023** —Estatuto de Roma, su
implementación y la Convención Interamericana contra el Terrorismo, que delimitan el ámbito del
juicio en ausencia— y las **Leyes 23.857 y 25.358**, los dos convenios de restitución
internacional.

**Dos resultados que corrigieron contenido**, y son la razón por la que bajar la norma no es sólo
completar el catálogo: el art. 62 de la 27.798 resultó ser **sólo de deuda pública provincial** y
no toca el crédito laboral; y el **art. 8 bis del Estatuto de Roma no está en el anexo de la Ley
25.390** —es de las enmiendas de 2010—, así que hay que verificar por qué instrumento entró al
derecho argentino. Lo mismo había pasado con la Ley 25.323, de cuyo texto salieron dos reglas que
ningún módulo traía: la **no acumulación** del art. 1 con los arts. 8, 9, 10 y 15 de la Ley 24.013
y la **facultad judicial de reducir hasta eximir** el recargo del art. 2. Están escritas en
`laboral.md` 5.3 y `concursos.md` 29.

**Cómo se mantiene cerrado el frente.** `herramientas/cobertura_normativa.py` cruza las leyes que
los módulos citan con articulado contra las declaradas en `normas.json`, y **la medición viva la
da el comando**. Toda ley citada sin estar declarada tiene veredicto en
`herramientas/cobertura-revisada.json` con su motivo; los que más se repiten son que la norma es
una reforma ya incorporada al consolidado de otra que sí está bajada, que es una mención histórica
de una norma derogada, o que es una cita bibliográfica del índice doctrinario. El script vuelve a
reclamar cualquier ley sin veredicto, así que la cuenta se mantiene sola y no se escribe en ningún
lado. Las declaradas sin URL oficial identificada quedan visibles en el catálogo, con su detalle en
`derecho/fuentes/MANIFIESTO.md`.

**Es una lista para revisar, no para aplicar**: la detección mira una ventana de texto y se
equivoca en los dos sentidos, así que antes de agregar una norma hay que abrir el módulo y ver
cómo se usa.

---

## 18/09/2026 - La Justicia de Paz bonaerense, que era lo último del catálogo sin escribir

**Y el texto ya estaba bajado.** `PENDIENTES.md` la daba por la única materia sin nada escrito, y
al ir a buscar qué faltaba apareció que la **Ley 5.827, orgánica del Poder Judicial de PBA**, ya
estaba en `fuentes/` desde antes — con el fuero entero adentro. Lo que faltaba era la prosa y una
norma: el **Código de Faltas**, que se bajó ese día contra `normas.gba.gob.ar`
—`pba-decreto-ley-8031-1973.txt`, texto ordenado por Decreto 181/87 y consolidado hasta la Ley
15.406—. Se verificó antes de bajarlo que está **vigente con modificaciones**: la Ley 15.041
derogó varios artículos, no el cuerpo.

**Lo que decide el fuero, y no se parece a ningún otro módulo: la competencia depende del
partido.** El **art. 61, texto de la Ley 13.645**, parte los Juzgados de Paz en dos grupos y
enumera **veinte partidos del conurbano** por su nombre; ésos **no tienen familia**. El inciso II
dice *"los restantes"*, y a ésos les suma alimentos, tenencia y régimen de visitas, suspensión de
la patria potestad, internaciones de urgencia con aviso en veinticuatro horas y **hábeas corpus**.
De ahí sale el nodo bloqueante del módulo: **antes de contestar se pregunta el partido**.

**Dos remisiones a normas derogadas, y las dos definen competencia o recurso.**

- El **art. 61 inc. II a)** da competencia en *"separación personal, divorcio vincular y
  conversión"* **en los términos de los arts. 205, 215, 216 y 238 del Código Civil**, y el inc. 2
  a) en el asentimiento conyugal del **art. 1277**. Cotejado contra `ccycn-26994.txt`: la
  separación personal ya no se decreta —hay divorcio único del art. 437—, el asentimiento es hoy
  el art. 470, **y la conversión sobrevive por texto expreso**: la norma complementaria Primera
  del art. 8 de la Ley 26.994 la mantiene para las decretadas antes de la vigencia del Código, con
  competencia propia y resolución **sin trámite alguno**. Esa es la porción del inciso que todavía
  tiene objeto.
- El **art. 144 del Código de Faltas** manda la apelación a la *"Cámara de Apelaciones en lo
  Criminal y Correccional"* y al *"Capítulo III del Libro IV del Código de Procedimiento Penal
  (t.o. Decreto 1174/86)"*. Los dos nombres son de estructuras que ya no existen: el rito penal
  bonaerense es la **Ley 11.922** y la alzada la nombra el **art. 51 de la Ley 5.827**, que además
  trae la regla que más se pasa por alto — **la alzada cambia con la materia dentro del mismo
  juzgado**: Cámara Civil y Comercial, salvo faltas, donde es la de Apelación y Garantías en lo
  Penal.

**Lo que el fuero tiene de propio en materia contravencional**, cotejado artículo por artículo:
prescripción de la acción y de la pena en **un año** (art. 33, texto Ley 10.580), con tres causales
de interrupción y ninguna más; parte general del Código Penal y CPP provincial **supletorios**
(art. 3); cinco penas (art. 5); detención preventiva de **doce horas**; declaración dentro de
**veinticuatro**, con notificación del derecho a defensor; sentencia en **diez días** desde la
planilla de antecedentes; y el recurso, que **suspende la ejecución** salvo para el detenido.

**Entró como fuero y no como sección**, que es la barra alta: módulo con fuente primaria a la
vista, norma bajada por el descargador, disparador propio y caso de prueba —
`justicia-de-paz-pba-competencia-y-faltas`, con el partido como dato que falta a propósito—.
**Lo que queda pendiente es jurisprudencia: no hay un solo fallo bajado de este fuero**, y las dos
remisiones a normas derogadas no las resuelve ningún precedente cargado.

---

## 18/09/2026 - Barrido por el defecto del art. 245 sobre todos los módulos: cuatro enseñaban el texto nuevo sin decir desde cuándo

**La pregunta era si el hueco de `laboral.md` 5.2 estaba en otros módulos.** El defecto tiene
firma: el módulo desarrolla un artículo **sustituido hace poco**, describe el texto vigente y no
dice qué rige para los hechos anteriores. Nada lo medía: `reformas_no_leidas.py` comprueba que el
módulo **nombre** la reforma, no que diga desde cuándo se aplica.

**Cómo se barrió.** Para cada `.txt` de `fuentes/normas/` se extrajo, artículo por artículo, la
nota de sustitución con fecha de B.O. —75 normas la traen, **36 con alguna posterior al
01/01/2024**— y se cruzó contra los artículos que cada módulo cita en la misma unidad de texto.

**Cuatro hallazgos sobre las referencias principales.** El barrido se corrió sobre todos los
módulos y después se leyó módulo por módulo, porque el cruce automático confunde el `art. N` de una
ley con el de otra nombrada en el mismo párrafo.

**Primero, y es un plazo fatal.** El **art. 46 de la Ley 18.345**, texto del art. 82 de
la Ley 27.802, incorporó la **caducidad de instancia sin intimación previa** al proceso laboral
nacional. El consolidado remite a la regla de aplicación, y ahí está lo que faltaba: el **art. 93
de la Ley 27.802** aplica las modificaciones de ese Título **a todos los procesos EN TRÁMITE**
desde el día siguiente a la publicación, el 07/03/2026, salvo los arts. 79 y 80. **Una causa
laboral iniciada antes de la reforma puede caducar**, que es lo contrario de lo que se supone por
inercia. `laboral.md` 5.9 y la tabla de `plazos.md` enunciaban la caducidad sin esa frase.

Con el mismo cotejo entraron dos cosas más: el **art. 94**, que a los arts. 79 y 80 —competencia
por materia y territorial— los aplica en los procesos en trámite **sólo donde la competencia
estuviere pendiente de resolución**; y la nota del **art. 217**, que registra la prórroga del
**art. 27 del Decreto 408/2026** al **01/11/2026** para el Título II, Fondo de Asistencia Laboral.

**Segundo: `empleo-publico.md` desarrollaba la cesantía sin decir que era texto nuevo.** La Ley
27.742 sustituyó **diez artículos de la Ley 25.164** —11, 12, 14, 18, 20, 24, 31, 32, 33 y 37, con
vigencia desde el 09/07/2024—, y entre ellos el **art. 32, causales de cesantía**, que es el
corazón del módulo. Toda doctrina anterior a julio de 2024 sobre el régimen disciplinario se
escribió sobre otro articulado.

**Tercero: el texto de la Ley 25.871 que enseña `administrativo-nacional.md` es el de un DNU que el
módulo no nombraba.** El **Decreto 366/2025**, B.O. **29/05/2025**, sustituyó por su art. 34
**treinta y un artículos** —entre ellos los arts. 8, 29, 61, 62, 70 y 86 que el bloque desarrolla—
y derogó otros tres. El módulo tenía un aviso genérico sobre "decretos de necesidad y urgencia
sucesivos"; ahora nombra cuál, con su fecha, y dice lo que eso implica: **es un DNU reformando una
ley del Congreso**, con la validez discutible por sí misma y el trámite ante la Comisión Bicameral
sin verificar, igual que el Decreto 941/2025 en inteligencia. El decreto se bajó.

**Y cuarto, el de los arts. 17 y 18 de la LNPA**, que está en la entrada de más abajo.

**Lo que quedó limpio, que también se mide.** `laboral-colectivo.md` nombra el texto artículo por
artículo, con la fecha y **diciendo cuáles conservan el anterior**; `laboral-licencias.md` hace lo
mismo con los arts. 209 y 210; el bloque de trabajo agrario de `laboral.md` acierta 8 de 8;
`tributario.md` lo dice en el título de la sección —*"el art. 56 cambió en enero de 2026"*—;
`salud-discapacidad.md` etiqueta cada artículo con su *"texto Ley 27.793"*. Y los candidatos de los
cuatro módulos penales eran todos colisiones de numeración entre los cuatro códigos procesales: el
art. 290 que el cruce marcaba es la reposición del **CPP de la Ciudad**, no la rebeldía de la Ley
23.984 ni la dirección del debate del CPPF.

**El barrido NO queda como herramienta, y el motivo es el mismo que el repositorio le aplica a
cualquier alarma.** Atribuir un `art. N` suelto a una de las leyes nombradas en el párrafo no se
puede hacer con un regex: da **26 candidatos** sobre el árbol de hoy y, leídos, casi todos son
colisiones de número entre leyes distintas —el `art. 7` de la Ley 26.682 contado como art. 7 de la
Ley 24.901, el `art. 17` de la Ley 25.164 como art. 17 de la LNPA—. Una alarma que suena
veintiséis veces para acertar una se apaga sola. Queda escrito acá **cómo se corre**, para
repetirlo a mano después de una reforma grande, que es cuando sirve.

---

## 18/09/2026 - El eval de despido, corrido dos veces: bajaron los turnos y tres rúbricas medían mal

**Qué se comparó.** El caso `laboral-despido-tramos-reforma-pba`, misma forma las dos veces
—`with-without`, tres corridas por brazo, concurrencia 2— para que los números se pudieran leer de
frente. Las dos el 18/09/2026, la primera antes de escribir la disciplina de lectura en la sección 16
del `SKILL.md` y la segunda después — los directorios de `evals/results/` las fechan en UTC y por
eso la segunda figura como del 19.

| | Antes | Después |
| --- | --- | --- |
| Turnos con la skill | 20 · 25 · 18 → **21,0** | 11 · 18 · 9 → **12,7** |
| Costo por corrida | **US$ 2,30** | **US$ 2,07** |
| Score con la skill | 0,583 | 0,633 |
| Score sin la skill | 0,583 | 0,500 |

**Lo único que se mueve más allá del ruido son los turnos: −40%.** El costo baja apenas un 10%
porque los turnos que se ahorraron eran los baratos —greps de rescate, relecturas parciales—: lo
caro es cargar `SKILL.md` y `laboral.md` la primera vez, que no se evita. **El score no se puede
leer:** el brazo sin skill se movió 0,083 sin que nada cambiara ahí, así que un movimiento de 0,05
en el otro no dice nada. Tres corridas por brazo y ningún modelo fijado.

**Y el eval destapó lo que no se estaba buscando: tres rúbricas medían mal.** Se vio leyendo las
respuestas, no el score.

- **`base-del-245` afirmaba el derecho equivocado.** Pedía que la base *"excluya el SAC"*, que es
  el párrafo de la remuneración *"devengada y pagada en cada mes calendario"* incorporado por el
  **art. 51 de la Ley 27.802** (B.O. 06/03/2026). El despido del caso es del **15/10/2025**.
  Cotejado contra `lct-20744.txt` —la única nota de sustitución del art. 245 es la de la 27.802— y
  contra `ley-27742.txt`, que no lo tocó. Reprobó 3 de 3 respuestas que decían bien que regía el
  texto anterior.
- **`no-liquida-multas-derogadas` medía la maqueta.** Exigía los agravantes derogados *"en el
  cuadro de rubros"*; reprobó respuestas que los resolvían en un bloque aparte y advertían sobre
  pluspetición, con un cuadro de rubros que —con razón— no lista lo que no existe. Es su segunda
  reescritura por la misma causa.
- **`antiguedad-multiplicador` castigaba la comparación.** Pedía *"no dejar la elección abierta"*
  entre la fecha real y la registrada, y reprobó una respuesta que liquidaba con la real y además
  cuantificaba la diferencia con la registrada, que es lo que se le pide a un análisis de parte.

Las tres se reescribieron alrededor del hecho y en positivo, con la medición al lado. **`no-cita-la-11653`
se dejó como está**: ahí el ruido es del juez —dos respuestas equivalentes votadas distinto— y
mover la vara para que apruebe el caso conocido es calibrar, no corregir.

**Lo que el módulo no tenía, y es el hallazgo de fondo.** `laboral.md` 5.2 desarrollaba **sólo** el
régimen vigente. Para un acto extintivo entre el 09/07/2024 y el 05/03/2026 —hoy, el que más
llega— el módulo no decía cuál era la base, y el análisis tenía que deducirlo. Se escribió
**5.2.1** con lo único afirmable: que rige el texto anterior, que `fuentes/` trae el consolidado y
por lo tanto no lo incluye, que el mínimo es de **dos meses** y el piso del 67% es **doctrina
"Vizzoti"** y no texto legal —las dos cosas ya estaban decididas dentro de `liquidacion_lct.py`—,
que la **exclusividad reparatoria** de los tres últimos párrafos **no existe** en ese tramo, y que
la incidencia del SAC en la base es criterio discutido, con marcador.

**Las reescrituras de las rúbricas no están medidas contra una corrida**: la próxima dirá si el
0 de 3 era la vara o el módulo.

---

## 18/09/2026 - Dos citas que no tenían texto detrás: los arts. 17 y 18 de la LNPA y una disposición de consumo

Las dos salieron de cruzar **las 158 citas entrecomilladas verificables** de los módulos contra
`fuentes/` y `kb/` —incluidos los `.html` y los `.pdf` reextraídos—. Resolvieron 147.

**La LNPA: el módulo enseñaba la numeración anterior a la Ley 27.742.** `administrativo-nacional.md`
46.3.1 explica «Talleres Navales Dársena Norte», Fallos 341:1679, **del 21/11/2018**, y decía en
presente que el recaudo de *"no causar perjuicio a terceros"* es del **art. 18**. Cotejado contra
`fuentes/normas/lnpa-19549.txt`: el **art. 36 de la Ley 27.742** (B.O. 08/07/2024) refundió los dos
regímenes dentro del **art. 17** —el acto regular es su párrafo tercero y el recaudo su párrafo
cuarto, junto con el dolo del administrado y el título precario— y el **art. 37** dejó el art. 18
para la derogación de **actos de alcance general**. La cita tampoco era la cita: el texto dice
*"sin causar perjuicio a terceros"*.

**Y los rótulos del consolidado quedaron cruzados**, que es la trampa que hace caer: InfoLEG titula
al art. 17 *"Revocación del acto nulo"* cuando ya trae también el regular, y al art. 18
*"Revocación del acto regular"* cuando habla de alcance general. **El rótulo no es el articulado.**
El bloque quedó con la traducción escrita, con la salvedad de que para un acto anterior al
09/07/2024 rige el texto viejo, y con marcador sobre si la distinción del fallo sobrevive a la
refundición.

**Consumo: se citaba textual una norma que no estaba bajada.** `consumidor.md` 17.2 citaba la
**Disposición SSDCyLC 890/2025** entre comillas sin texto en `fuentes/`, y **ninguna herramienta
podía verlo**: `cobertura_normativa.py` cruza números de ley y de decreto, no disposiciones de
subsecretaría. Bajada —`disposicion-890-2025.txt`, InfoLEG— y cotejada. La cita era correcta, y el
texto agregó dos cosas que el módulo no tenía: el **art. 2 inc. a** le manda *analizar, asignar y
derivar* según el art. 41 LDC, lo que confirma que es mesa de entrada y no instancia previa; y el
**art. 4 invita a adherir a las provincias que faltan**, así que el *"único medio formal"* rige
donde hubo adhesión y **la norma no trae la lista**. Deroga la Resolución 274/2021.

**Lo que queda medido como punto ciego:** una cita entrecomillada a una disposición, resolución o
acordada no la cruza ningún detector. Se sigue leyendo.

---

## 18/09/2026 - Penal se parte en tres: el Código Penal por un lado y el proceso por el otro

**No es una auditoría normativa: es una partición**, y queda registrada acá por lo mismo que las
de `laboral.md`: movió contenido ya cotejado y el corte dejó algo a la vista.

**El corte es por materia, y la materia estaba escrita en el título del módulo sin cumplirse.**
El título de `penal.md` prometía régimen aplicable, proceso y ejecución, y dos de sus bloques no
eran ninguna de las tres cosas: 24.4 —extinción de la acción, prescripción, probation— y 24.7 —imputabilidad,
tentativa, participación, concurso, reincidencia, condena condicional— son **Código Penal**, que
rige igual cualquiera sea el código procesal. Salieron juntos a `penal-parte-general.md`. Nulidades
(24.5) y recursos (24.6) salieron a `penal-impugnacion.md`: son las dos formas de atacar —la
nulidad ataca un acto, el recurso ataca una decisión—, las dos con el plazo encima y las dos
terminando en la misma pregunta, qué solución se pretende.

**Lo que NO salió, y es la decisión que importa.** Por tamaño, 24.3 —coerción y libertad durante
el proceso— era el candidato: 213 renglones y una consulta acotadísima, la excarcelación. Se
queda, y el motivo se lee en su índice: 24.3.1 es el CPPF, 24.3.2 la Ley 23.984, 24.3.3 el CPP PBA
y 24.3.4 el de la Ciudad. Está organizado **por el mismo eje que 24.1**, que es qué código rige, y
quien pregunta por una preventiva necesita las dos cosas en la misma lectura. Sacarlo habría
partido la elección del código de su aplicación.

Lo que carga una consulta penal, medido en KB sobre `SKILL.md` más `intake.md`, `marcadores.md` y
el módulo o los módulos que la fila de ruteo indica:

| Consulta | Antes | Ahora |
| --- | --- | --- |
| Prescripción, probation o parte general | 165 KB | **108 KB** |
| Excarcelación, preventiva o extradición | 165 KB | **108 KB** |
| Nulidad o recurso | 165 KB | **139 KB** |

La última fila es el costo del corte y estaba previsto: cuál código rige define el nombre del
recurso, su plazo y sus motivos, así que esa consulta abre `penal-impugnacion.md` **y** `penal.md`
24.1. La fila de ruteo lo dice, y la cabecera del módulo nuevo también.

**Lo que el corte destapó, y era lo contrario de lo que se buscaba.** Después de partir, la pieza
más pesada de una consulta penal ya no es el módulo sino el **núcleo: 72 KB** entre `SKILL.md`,
`intake.md` y `marcadores.md`, contra 35 KB del módulo más grande de los tres. El próximo
rendimiento no está en seguir partiendo módulos.

**Y destapó dos números repetidos.** `penal.md` tenía dos secciones `24.6.5` y dos `24.10`, con
las filas de `changelog-normativo.md` y `REVALIDAR.md` apuntando a una de las dos. El control que
debía verlo juntaba los módulos en un `set` y los fundía en una entrada: la alarma que no suena
nunca. Hoy hay un test que cuenta por archivo, y su mutación está nombrada en el docstring.

---

## 18/09/2026 - Los seis frentes de derecho internacional, y dos códigos que no dicen lo mismo

**Uno de los seis no necesitaba descargar nada.** El exequátur estaba sin cubrir no por falta de
fuente sino por falta de dueño: es **procesal**, así que no entró con el Título IV del CCyCN, y
`proceso-nacional.md`, `proceso-pba.md` y `ejecucion.md` tampoco lo tomaron. Los dos códigos ya
estaban bajados desde antes.

**Y al leerlos aparecieron diferencias de fondo entre Nación y Provincia.** El CPCCN pide **cinco**
requisitos y el CPCCBA **seis**. Dos son decisivos: el bonaerense exige además *"que la obligación
que haya constituido el objeto del juicio sea válida según nuestras leyes"* —el CPCCN no tiene
equivalente—, y habla de *"orden público **interno**"* donde el nacional dice *"principios de orden
público del derecho argentino"*. **Una sentencia ejecutable en la Nación puede no serlo en PBA**, y
leer «orden público interno» como si fuera el internacional de 35.3.1 amplía el control mucho más de
lo que el DIPr admite.

**Lo que se bajó para los otros cinco frentes:** Ley 24.488 (inmunidad), Ley 27.449 (arbitraje
comercial internacional), Ley 24.767 (cooperación penal y extradición), Ley 22.765 (Convención de
Viena) y Ley 24.578 (Protocolo de Las Leñas).

**Cinco cosas que el texto desmiente y que se citan mal:**

- **El art. 3 de la Ley 24.488 está OBSERVADO** por el art. 1 del Decreto 849/95. Lo dice el propio
  texto bajado.
- **El art. 519 bis del CPCCN fue derogado** por el art. 107 de la Ley 27.449: los laudos
  extranjeros ya no van por el Código procesal.
- **La declaración argentina de los arts. 12 y 96 de Viena** desactiva la libertad de forma del art.
  11, y el art. 12 dice que las partes **no pueden apartarse de él**. Dar por supuesta la libertad
  de forma es el error de esa materia.
- **Entre Estados del Mercosur el trámite es otro**: por exhorto y Autoridad Central, con el orden
  público **atenuado** —*"no contraríen manifiestamente"*— y **sin legalización ni apostilla**.
- **La opción del nacional argentino del art. 12 de la Ley 24.767 cede ante el tratado**, y ejercida
  la opción el juzgamiento local sólo se monta si el Estado requirente presta conformidad, renuncia
  a su jurisdicción y remite las pruebas.

**Una rama que el detector encontró y tenía razón.** `ramas_sin_disparador.py` marcó `penal.md`
24.10: quien consulta por un pedido de extradición no se reconoce en «código procesal, coerción,
probation, nulidades y recursos», que era lo que decía la fila. Se resolvió **agregando filas a la
tabla de ruteo de la sección 16 y no comprando espacio en el `description`**, que está a dos
caracteres del límite: la tabla de ruteo cuenta como disparador para el control, y no cuesta nada.
Entraron cinco filas —exequátur, inmunidad, arbitraje internacional, Viena y extradición—.

**Lo que NO se hizo, y por qué.** El arbitraje internacional da para módulo propio y quedó como
sección: partirlo hoy costaría un disparador nuevo en un `description` sin lugar, y la materia
todavía entra por «elemento extranjero». La **parte especial del Título IV** sigue sin escribir. Y
el **estado de ratificaciones y reservas** —qué Estados están vinculados por cada tratado, si la
República retiró la declaración de Viena— no está cargado y lleva marcador en cada lugar donde
importa.

---

## 18/09/2026 - DIPr: el módulo mandaba mirar el tratado y el repositorio no tenía los tratados

**El hueco, dicho como era.** `dipr.md` 35.1 enseña que el art. 2594 **no es negociable** —primero
el tratado, el Código es subsidiario— y que empezar por el art. 2650 sin descartarlo es *el error
de método de esta materia*. Pero el catálogo tenía tres convenios de DIPr: los dos de restitución
de niños y la Convención de Nueva York. **La regla estaba bien enunciada y la capa offline no podía
cumplirla.**

**Lo que entró.** El **Decreto-Ley 7.771/56**, que ratifica los cinco instrumentos de Montevideo
del 19/03/1940 y **trae su articulado completo** —Civil, Comercial Terrestre, Navegación, Procesal
y el Protocolo Adicional—, y la **Ley 24.669**, el Protocolo de Buenos Aires del Mercosur con sus
dieciocho artículos. De ahí salió la sección **35.1 bis**.

**Las tres colisiones que justifican la sección**, cotejadas contra el texto:

- **Autonomía de la voluntad.** El art. 5 del Protocolo Adicional dice que la jurisdicción y la ley
  aplicable *"no pueden ser modificadas por voluntad de las partes, salvo en la medida en que lo
  autorice dicha ley"*. Es lo inverso del art. 2651 del Código.
- **Ley del contrato.** El art. 37 del Tratado de Derecho Civil somete a la ley del lugar de
  cumplimiento *"todo cuanto concierne a los contratos"*, y el art. 38 califica ese lugar según el
  objeto.
- **Prórroga de jurisdicción, que es la más cara.** El art. 56 la admite **sólo después de promovida
  la acción**, y *"la voluntad del demandado debe expresarse en forma positiva y no ficta"*. Bajo el
  Código, no contestar la demanda prorroga; bajo Montevideo, el silencio no prorroga nada. Y el
  Protocolo de Buenos Aires resuelve distinto que los dos: acuerdo escrito en cualquier momento,
  no obtenido en forma abusiva, con el derecho **más favorable a la validez del acuerdo**.

**Una alarma que sonó y era falsa, y el veredicto que la apaga.** El descargador marcó la Ley
24.669 como *"parece la ley APROBATORIA y no su contenido"*. Se leyeron los dieciocho artículos: el
anexo **está transcripto**, y los diecinueve que el detector contó son el artículo de la ley más los
dieciocho del Protocolo. El veredicto quedó en `normas/revisiones.json` **y se apagó la marca
bajando con `--forzar`**, que es como el repositorio exige que viajen las dos cosas: un veredicto
escrito que no apaga la marca da impresión de resuelto y la alarma vuelve a sonar igual.

**Dos defectos propios corregidos de paso.** El módulo decía que propiedad industrial *"el repo
todavía no cubre"* y `propiedad-industrial.md` existe; al corregirlo se escribió «sección 57» de
memoria cuando es la **40**. Y los títulos y notas de las dos normas nuevas se cargaron sin
acentos para esquivar el quoting del shell —el vicio exacto que la regla de prosa nombra—: lo
atraparon `TestTitulosDeNormas` y `TestProsaAcentuadaEnLosJSON`.

**Lo que sigue faltando, y es lo grande.** La **parte especial** del Título IV, arts. 2613 a 2671,
dieciséis secciones, sigue sin escribir y así está declarado en 35.9. Y el **estado de
ratificaciones** de cada tratado no está cargado: qué Estados están hoy vinculados con Argentina
lleva marcador y no se asume.

---

## 18/09/2026 - Una búsqueda que no corría, y una sentencia de la SCBA que apareció por el costado

**Lo que hay que saber del buscador de JUBA antes de volver a usarlo.** `form_input` escribe el
valor en el DOM pero **la página no lo registra**: el botón queda inhabilitado y la consulta se
envía vacía, con el cartel *"Debe ingresar algún valor para realizar la búsqueda"*. **Hay que
tipear con el teclado**, haciendo clic en el campo **por referencia de elemento y no por
coordenada** —la ventana cambia de tamaño y la página conserva el scroll, así que un clic por
coordenada cae al vacío—, y verificar con una captura que el texto esté en el campo antes de
buscar. Tres consultas se dieron por «cero resultados» cuando en realidad **no habían corrido**.

**Un caso de lo que este repositorio llama concluir el proceso desde el producto.** La pantalla
mostraba el formulario otra vez y de eso se concluyó que la búsqueda había dado cero. El producto
—formulario en blanco— era compatible con dos procesos distintos, y el que valía era el otro.

**Lo que sí quedó medido sobre el art. 2255.** JUBA tiene **un solo sumario** de legitimación
pasiva en reivindicación y es de **2010**, resuelto bajo los arts. 2758, 2783 y 2465 del **Código
Civil derogado**. **No cierra el marcador**, por la misma razón que el módulo ya advierte para el
art. 1185 bis: la doctrina del código anterior no se traslada.

**Y apareció, por el costado, SCBA C. 125.685.** Buscando compensación económica —79 sumarios— uno
de los resultados enlazaba una sentencia de la **Suprema Corte** del **22/05/2025** que no es de esa
materia: es **prescripción adquisitiva entre ex cónyuges sobre un bien ganancial**. Entró a
`derechos-reales.md` 45.3 bis. Su holding: la interversión del título exige **conformidad del
propietario o actos exteriores suficientes de contradicción**, con criterio estricto, **pero ese
rigor se relaja en el contexto intrafamiliar** cuando el titular registral *"abdicó de tal
condición, voluntariamente"*.

**Se escribieron sus dos límites en el mismo bloque**, porque sin ellos el precedente se cita mal:
el voto de **Soria llega al mismo rechazo por otra vía** —hubo conformidad del titular registral—,
así que el relajamiento es el voto de Kogan y no toda la Corte; y el propio fallo separa el caso
intrafamiliar del caso entre extraños.

**Una cifra que puse yo y no estaba en la sentencia.** Al escribir el holding cité *"art. 24 inc. c
de la Ley 14.159"* cuando el fallo dice sólo *"el inc. c) de la ley 14159"*. El número lo había
completado de memoria. Se reemplazó por un marcador, se bajó la ley y se verificó contra el texto:
el art. 24 existe, y de paso entraron sus incisos a y b —**juicio contencioso con certificación
registral acompañada a la demanda, y plano de mensura**—, que el módulo no tenía y son recaudos de
admisibilidad.

---

## 18/09/2026 - Dos módulos sin ningún precedente, y el navegador donde el fetcher no llega

**Por qué estos dos.** De los **39 institutos sin precedente propio**, `derechos-reales.md` y
`firma-digital.md` eran los únicos cuyo marcador no pedía un matiz sino que decía *"no hay
precedente bajado sobre …"*. El instrumento estaba sano antes de empezar —**0 documentos sin leer,
0 sin medir, 0 a revisar en la auditoría de fechas**—, así que no había deuda que saldar: esto es
cobertura nueva.

**«Simonet» — arts. 1170 y 1171 CCyCN.** Cámara Segunda de Apelación Civil y Comercial de La Plata,
Sala Segunda, causa 133134-2, registrada el 05/12/2023. Enuncia textualmente los cuatro requisitos
del art. 1170 y **separa su régimen del art. 1171**: el 1171 no exige publicidad en su letra, y el
tribunal sostiene que *"una interpretación sistemática de la norma requiere la exigencia de
publicidad posesoria"*. Confirma además la advertencia que el módulo ya traía: la doctrina
provincial anterior es del art. 1185 bis del código derogado y **no se traslada**, porque el 1170
agregó el eslabonamiento y la publicidad.

**«Beltrame» — contratación por canal electrónico.** Cámara Segunda de La Plata, Sala Primera,
causa 135587, 19/12/2023, voto de Sosa Aubone. Revoca la sentencia que negaba valor a préstamos por
home banking y cajero porque pulsar *"aceptar"* no sería firma. **Y se escribió su límite en el
mismo párrafo**, que es lo que evita citarlo mal: el tribunal razona sobre contratos no negados y
sobre una firma electrónica **cuya autoría e integridad no se cuestionaron**, así que no resuelve
el caso del desconocimiento, que es donde el art. 5 pone la carga.

**Lo que sí se aprendió sobre las fuentes, y vale para la próxima.** WebFetch **no sirve** para
esto: SAIJ y JUBA son aplicaciones JavaScript y devuelven la cáscara, y los PDF comprimidos de los
buscadores judiciales vuelven ilegibles. **Lo que funciona es el navegador**: JUBA, operado como
página, entrega sumarios por voces y el texto completo del fallo. Un intento previo por buscador
web sólo produjo texto sintetizado sin sentencia identificada, y **eso no se escribe**: un holding
sale de abrir el documento.

**Los dos marcadores no se cerraron: se achicaron, y por eso el conteo sigue en 39.** Queda abierta
la legitimación pasiva del art. 2255, y queda abierto el caso de la firma electrónica desconocida
—JUBA publica sumarios en punto, «Afluenta c/ Celentano Acevedo» y «Banco de Galicia c/ Zamora»,
pero **sin texto completo**, y el marcador lo dice para que nadie lo cierre con un resumen—.

**Y un guardarraíl acertó sobre una decisión mía.** El primer registro de «Simonet» declaraba el
campo `origen`, que significa *"no viene del registro del tribunal"*. `scba.gov.ar` **sí** está en
la tabla de fuentes, y el test exigió sacarlo: si se declara origen sobre una fuente sancionada, el
campo deja de querer decir algo. El matiz —que es un blog departamental y no el buscador— pasó a
la nota, que es donde corresponde.

---

## 18/09/2026 - Medicina legal no era un módulo: eran cinco huecos en módulos que ya existían

**Qué se midió antes de escribir.** El perfil heredado `kb/especialidades/medicina-legal-CLAUDE.md`
—464 líneas— cita dieciséis leyes. Trece ya las nombraba algún módulo nuestro y doce ya estaban en
el catálogo. **La especialidad no era la unidad correcta:** su columna vertebral es cómo **redactar**
el informe médico-legal, que es trabajo del perito, y la skill actúa desde una parte o desde el
órgano. Lo que el perfil aportaba de verdad era señalar cinco huecos, y cada uno tenía dueño.

**Dos contradicciones del perfil, y en las dos el módulo propio estaba mejor.** Dice que el Decreto
549/2025 *"reemplazó al Decreto 659/1996"*, cuando lo sustituido es su **Anexo I** y el decreto
sigue vigente —`laboral-riesgos.md` 5.8.3, con B.O. y vigencia—. Y da el estado de implementación
del CPPF en prosa, sin la regla de transición del art. 5 de la Ley 27.063, que `penal.md` sí trae
con tabla por jurisdicción.

**Lo que entró, y contra qué se cotejó.** Cinco leyes bajadas con el descargador: 26.529, 17.132,
24.655, 27.260 y 24.463.

- **`salud-discapacidad.md` 27.4 bis** — historia clínica, consentimiento informado y deberes del
  profesional. Lo que decide el caso: el titular es el paciente y la copia se entrega **en 48
  horas** a simple requerimiento (art. 14); la guarda es de **diez años desde la última actuación
  registrada** (art. 18); y **la negativa tiene acción propia, que es habeas data y no amparo**
  (art. 20), exenta de gastos en jurisdicción nacional. El puente con la Ley 17.132 es expreso: el
  art. 21 manda sus sanciones al Título VIII de aquélla.
- **`previsional.md` 32.4 bis** — PUAM. Vitalicia, no contributiva, desde los 65, y **no genera
  derecho a pensión** (art. 15), que es lo que cambia qué se le dice a la familia.
- **`previsional.md` 32.4 ter** — el fuero de la Ley 24.655 y la regla que sorprende: el art. 15 de
  la Ley 24.463, texto del art. 3 de la 24.655, dice que **no hace falta recurso administrativo
  alguno** para habilitar la instancia. No se transpola el agotamiento de la vía.
- **`prueba-pericial.md` 20.1** — la tabla de regímenes no tenía la seguridad social federal.
- **`civil.md`** — la línea de mala praxis médica ahora manda al piso normativo, que antes no
  existía en ningún módulo.

**Dos veredictos que murieron al bajar las leyes, y lo que eso deja escrito.** La línea de base de
`cobertura_normativa.py` tenía decidido que las Leyes 17.132 y 26.529 *"sólo aparecen en
`danos-indice-doctrinario.md`... mención bibliográfica, no uso de la norma como fuente de una
regla"*. Era cierto y dejó de serlo en el mismo acto: ahora son fuente. La medición del perfil
sirvió exactamente para eso, y no para escribir un módulo nuevo.

**Y una alarma que sonó por algo.** `reformas_no_leidas.py` marcó que `previsional.md` citaba los
arts. 25 y 28 de la LNPA sin nombrar la **Ley 27.742** (B.O. 08/07/2024), que sustituyó los dos.
Cotejado contra `fuentes/normas/lnpa-19549.txt`: el plazo del art. 25 es hoy de **ciento ochenta
días hábiles judiciales** y el art. 28 tiene procedimiento y régimen de apelación nuevos. **Un
cómputo hecho con el texto anterior da otro resultado**, y la remisión estaba escrita sin eso. Los
cuatro veredictos que se anotaron quedaron muertos enseguida y se purgaron: la reforma nombrada
dentro del módulo es mejor lugar que un archivo de veredictos.

**Lo que NO se hizo, y por qué.** No se escribió `medicina-legal.md`. Un módulo así repetiría
`prueba-pericial.md` 20 y `laboral-riesgos.md`, y lo que le quedaría de propio es criterio médico,
que es lo que este repositorio no puede afirmar contra fuente primaria. El perfil queda declarado
en `perfiles-heredados.md` como lo que es, y su fila dejó de decir que notarial tampoco tiene
módulo, porque ahora lo tiene.

---

## 18/09/2026 - Notarial: el fondo del CCyCN y dos leyes locales que no se trasladan

**Contra qué se cotejó.** `fuentes/normas/ccycn-26994.txt`, arts. 285 a 312; `fuentes/normas/caba-ley-404.txt`
y `fuentes/normas/pba-decreto-ley-9020-1978.txt`, las dos bajadas con el descargador en esta misma
auditoría; y `fuentes/normas/ley-12990.txt`, bajada después, por lo que se cuenta más abajo.

**Lo que decidió la forma del módulo.** El notariado se parte en dos y la partición no es de
grado: el **CCyCN** dice qué es un instrumento público y qué hace plena fe, y eso rige en las tres
jurisdicciones; **la organización de la función es local** y no se traslada. Escribir un módulo
que mezclara las dos capas habría producido reglas que se aplican donde no rigen, que es el error
que la sección 60.2 está construida para evitar.

**El art. 296 parte la plena fe en dos y se cita mal.** Que el oficial enuncie un hecho cumplido
por él o ante él cae *"hasta que sea declarado falso en juicio civil o criminal"*; el contenido de
las declaraciones sobre convenciones, pagos y reconocimientos cede *"hasta que se produzca prueba
en contrario"*. Es la distinción que decide si hace falta redargüir de falsedad, y el eval
`notarial-escritura-fe-publica-y-segunda-copia` la mide de frente.

**Un contraste que sólo aparece leyendo las dos leyes locales.** El acceso a la titularidad es por
concurso en las dos, pero PBA lo llama **cada dos años** con **90 días** de antelación y lo
califica un **Tribunal Calificador presidido por el Presidente de la Cámara civil y comercial en
turno**, rotando por Departamento Judicial e integrado por el **Juez Notarial** (arts. 8 y 9 del
Decreto-Ley 9.020); la Ciudad lo llama **una vez al año desde abril**, ante un jurado presidido por
un miembro del **Tribunal de Superintendencia**, cuyos miembros *"no podrán ser recusados"* y cuya
calificación *"será inapelable"* (arts. 34 y 35 de la Ley 404). **El Juez Notarial no tiene
equivalente porteño** y es la diferencia institucional que más se nota.

**Una inferencia propia que resultó falsa, y cómo se cayó.** El módulo se escribió diciendo que el
texto de la **Ley 12.990** no estaba cargado, y se apoyó en que el manifiesto ya declara que
InfoLEG no publica normas de 1948 —el caso de la Ley 13.478—. Eso es concluir el proceso desde el
producto: la ausencia de una norma de esa época no dice nada de otra. `cobertura_normativa.py` la
reportó SIN DECIDIR, se buscó, **InfoLEG la publica con texto consolidado** y se bajó con el
descargador. La regla que queda: la época de una norma no es un veredicto sobre su disponibilidad,
y cuando comprobarlo cuesta un comando no se opina.

**Y lo que la 12.990 bajada permitió afirmar.** Su propio articulado limita el ámbito a los
escribanos *"de la Capital Federal y territorios nacionales"* —arts. 2, 27, 36, 43 y 48—: **nunca
rigió el notariado de las provincias.** El art. 180 de la Ley 404 la deja sin efecto *"en el
ámbito de la Ciudad Autónoma de Buenos Aires"*, y dejar sin efecto en un ámbito no es derogar. El
marcador que el módulo conserva se achicó en consecuencia: ya no pregunta qué queda de la ley, sino
lo único que sigue abierto, si subsiste algún territorio nacional al que pueda aplicarse.

**Lo que el módulo declara que NO hace.** Las demás provincias —ninguna otra ley notarial está
cargada—, la forma exigida para cada contrato en particular, el documento electrónico y los
aranceles notariales, que son locales. Quedan además dos marcadores: el **Decreto 3.887/1998**,
reglamento notarial de PBA, y la falta de precedente bajado sobre la frontera del art. 296.

---

## 18/09/2026 - Violencia digital sale de `kb/` y pasa a módulo propio

**Contra qué se cotejó.** `fuentes/normas/ley-26485.txt` —texto actualizado— y
`fuentes/normas/ley-27736.txt`, artículo por artículo. Todas las incorporaciones y sustituciones
de la Ley Olimpia llevan **B.O. 23/10/2023**.

**Por qué esta materia y no otra.** De las tres que sólo tenían perfil heredado —medicina legal,
violencia digital y notarial—, es la única cuyo articulado **ya estaba bajado entero**. Notarial
tiene base en el CCyCN pero le falta la ley local, que es materia provincial. Medicina legal no es
una rama del derecho sino técnica pericial: no tiene articulado que cotejar, y lo suyo ya está
repartido entre `prueba-pericial.md` 20 y `laboral-riesgos.md` 5.8.3.

**El hallazgo que ordena el módulo.** *La Ley 27.736 no creó ningún delito.* Sus trece artículos
modifican la Ley 26.485 y nada más, que es una ley de protección integral. Es el error más caro
posible acá, porque el consultante llega hablando de algo que suena penal.

**Lo que el cotejo puso a la vista, y que se pierde parafraseando:**

- El **art. 6 inc. i** dice *"real o editado"*, así que la definición alcanza al material
  fabricado.
- El **art. 26 ap. a.9** exige *"identificarse en la orden la URL específica del contenido cuya
  remoción se ordena"*: una orden que describe el contenido sin la dirección no cumple el artículo.
- El mismo apartado **manda** —*"deberá solicitar"*— el aseguramiento de tráfico, abonado y
  contenido por noventa días renovables una vez, en secreto. **Pedir la baja sin el aseguramiento
  borra la prueba de la acción de fondo**, y el articulado lo dice en la misma oración.
- Asegurar y revelar son dos pasos: el acceso es facultativo, a pedido de parte y sólo para la
  acción de fondo.
- La notificación a la plataforma puede hacerse por el **art. 122 de la Ley 19.550**, que es el
  emplazamiento a sociedades del exterior.

**Un veredicto viejo que estaba mal, y se descubrió acá.** `cobertura-revisada.json` decía de la
Ley 14.407 de PBA que era la *"adhesión de PBA a la Ley 27.736 Olimpia"*. Leída: declara la
**emergencia pública en materia social por violencia de género** y adhiere a la **Ley 26.485**, y
no es permanente. `familia.md` 18.6 ya lo tenía bien; el error vivía sólo en el veredicto, que
había sido purgado el mismo día por otra razón. El módulo lo dice y emite marcador de vigencia
sobre el alcance provincial de los apartados nuevos, en vez de afirmarlo.

**Y se cerró un puntero a `kb/`.** `familia.md` declaraba que la cautelar digital *"está
desarrollada en `kb/perfiles/familia-CLAUDE.md`; 18.6 solo la roza"*. Ahora está escrita contra
fuente primaria, y el mapa de perfiles heredados baja de tres materias sin módulo a dos.

---

## 18/09/2026 - La frontera de licencia estaba sin cruzar sobre la mitad de los módulos

**Contra qué se cotejó.** `fuentes/normas/caba-ley-1217.txt`, `caba-ley-451.txt`,
`ley-27799.txt` y `ley-27801.txt`.

**Cómo apareció.** `fuga_textual.py` se corre a mano, con la lista de archivos como argumento, así
que su cobertura es la de ese día. Su línea de base decía en la nota *"SKILL.md y los 30 módulos
de `references/`"* cuando ya hay **63**: los 33 que entraron después **nunca se habían cruzado
contra `kb/`**, y nada lo avisaba —el suite probaba el detector con un corpus de mentira, no el
árbol real—. Corrido entero: **cinco pasajes** sin revisar.

**Dos eran defecto propio.**

1. **`contravencional-caba.md` tenía una fila repetida con la condición mal escrita.** La tabla
   del régimen de pago de faltas decía, en dos renglones distintos, *"pide la UACF dentro de los
   40 días y es condenado → 25% de bonificación"* y *"no paga ni pide la UACF dentro de los 40
   días → 75% de la multa"*. Son **el mismo supuesto en dos unidades** —25% de bonificación es
   pagar el 75%—, y la segunda condición además contradecía a la cuarta fila. El **art. 13 de la
   Ley 1.217** lo separa por el plazo y no por qué se pidió: inc. b), quien dentro de los 40 días
   *"no se acoge al pago voluntario y/o requiere la intervención"* paga **75%** si se confirma;
   inc. c), quien deja vencer el plazo paga **100%**. Reescrita en tres filas, con la norma de
   cada una, y transcribiendo el *"y/o"* del inciso en vez de parafrasearlo: es ambiguo en la
   fuente y resolverlo por nuestra cuenta habría sido inventar.

2. **Dos pasajes de `penal-leyes-especiales.md` condensaban articulado.** Ahora se citan textual,
   y la cita corrigió una imprecisión: la extinción por pago del régimen penal tributario corre
   *"hasta dentro de los treinta (30) días hábiles posteriores al acto procesal por el cual se
   notifique fehacientemente la imputación penal"* —desde **el acto procesal**, no desde una
   notificación cualquiera—. El otro es el art. 20 de la Ley 27.801, con sus tres recaudos previos.

**Los tres restantes no son fuga.** Son dos resúmenes de la misma ley que convergen —arts. 41 a 43
de la Ley 27.801, cotejados: la oposición del fiscal **sí** es vinculante por el art. 42— y una
frase de sintaxis legal común que engancha con un modelo de descargo de tránsito. Aceptados a la
línea de base con el motivo escrito.

**El guardarraíl que faltaba.** `TestElArbolRealEntero` corre el detector sobre `SKILL.md` y los
63 módulos y exige cero secuencias nuevas. Sin él, la cobertura del control dependía de qué
archivos le pasaran a mano.

---

## 18/09/2026 - Licencias, enfermedades inculpables y suspensiones salen con riesgos

Segunda partición de `laboral.md` el mismo día, con el mismo criterio. Acá el eje es **el contrato
que sigue vivo y la prestación que se interrumpe**: maternidad y excedencia (5.13), enfermedad
inculpable con reserva del puesto (5.14) y suspensión con poder disciplinario (5.15). En
`laboral.md` el eje es el otro, cómo termina el contrato y cuánto se paga.

**Lo que NO salió, y es la decisión que importa.** Por tamaño, 5.16 —principios y orden público
laboral— era el candidato obvio: 8,2 KB. Se queda, y el motivo se lee abriéndolo: el **art. 15**
decide si un acuerdo libera y el **art. 12** si un derecho es renunciable, y las dos cosas pesan
en un despido. Sacarlas habría ahorrado bytes a costa de que la consulta más frecuente perdiera lo
que necesita. **Se parte por materia, no por tamaño** — y esto es lo que esa regla significa
cuando el tamaño empuja para el otro lado.

| Consulta | Antes | Ahora |
| --- | --- | --- |
| Accidente de trabajo | ~54k tokens | **~26k** |
| Suspensión o licencia | ~54k tokens | **~29k** |
| Despido sin causa | ~54k tokens | ~45k |
| Despido estando de licencia | ~54k tokens | ~52k |

La última fila es el costo del corte y estaba previsto: quien cruza las dos materias abre los dos
módulos y no ahorra casi nada. El módulo nuevo lo dice en su cabecera, para que ese caso no se
resuelva con uno solo.

---

## 18/09/2026 - Riesgos del trabajo sale a módulo propio, y dos cosas que el corte destapó

**No es una auditoría normativa: es una partición.** Queda registrada acá porque movió contenido
cotejado y porque el corte dejó a la vista dos cosas que estaban tapadas.

**El criterio del corte, medido y no estimado.** `laboral.md` eran 117 KB y una consulta laboral
cargaba 199 con el núcleo y los módulos de infraestructura. Medido por sección, **riesgos del
trabajo era el 11%** y lo abre sólo quien tiene un accidente. Salió con su numeración —5.8 y sus
subsecciones, que la numeración global hace estables—, igual que el derecho colectivo salió a
`laboral-colectivo.md`: **por materia, no por tamaño**. Es otra ley, la 24.557, con instancia
administrativa previa, baremo propio y su propia jurisprudencia, y el eje es la reparación de un
daño y no la extinción del contrato.

| Consulta | Antes | Ahora |
| --- | --- | --- |
| Accidente de trabajo | ~54k tokens | **~26k** |
| Despido sin causa | ~54k tokens | ~51k |

**Lo primero que destapó: una reforma que parecía leída.** `reformas_no_leidas.py` reclamó el
art. 4 de la Ley 27.348 contra la Ley 27.802, que antes no reclamaba nada porque el módulo grande
nombraba la 27.802 por otro motivo. Leído contra `fuentes/normas/ley-27348.txt`: el **art. 154 de
la Ley 27.802 no sustituye ese artículo**, incorpora uno nuevo al Título I que faculta a la SRT a
suspender asistencia técnica y financiamiento a la jurisdicción incumplidora, y de paso nombra el
art. 4 segundo párrafo. Es apalancamiento federal sobre las provincias, no una regla que cambie lo
que hace el trabajador. Veredicto escrito.

**Lo segundo: un hueco de cobertura que nadie había declarado.** Al escribir el borde del módulo
quedó claro que **la homologación del acuerdo ante la Comisión Médica no está cubierta** —art. 4
de la Ley 27.348, que le da autoridad de cosa juzgada administrativa en los términos del art. 15
LCT y manda poner las prestaciones a disposición en cinco días—. Declarado en el borde con su
marcador, en vez de suplirlo.

---

## 18/09/2026 - La serie de la UMA, cargada, y un hueco del jus que no era un hueco

**Contra qué se cotejó.** La consulta oficial de la CSJN —`csjn.gov.ar/transparencia/uma`— y la
tabla del jus de la SCBA —`scba.gov.ar/paginas.asp?id=41320`—, abiertas **con navegador** el
18/09/2026. Es el camino que *Los registros judiciales no se pueden buscar* describe: con un
cliente HTTP la página de la UMA no entrega nada útil; con navegador, lista sus resoluciones.

**La UMA: 22 vigencias, del 01/10/2024 al 01/07/2026.** La página lista las resoluciones con
fecha y número, y **el valor está adentro de cada PDF**. Se bajaron veinte resoluciones y se
extrajo el texto de cada una con `pdftotext -layout`; el valor y la vigencia salen de la oración
dispositiva, no del resumen de la página. Tres puntos que el cotejo obligó a mirar:

- **La vigencia no es la fecha de la resolución.** La SGA 1930/2026, dictada el 20/08/2026, fija
  el valor *"a partir del primero de julio de 2026"*. Tomar la fecha de la resolución habría
  corrido toda la serie.
- **Una resolución puede fijar varios períodos.** La SGA 3495/2024 fija tres de una vez —octubre,
  noviembre y diciembre de 2024—, así que leer un valor por documento perdía dos.
- **Dos resoluciones parten «Unidad de Medida / Arancelaria» en dos renglones**, y el primer
  extractor las descartó por buscar la frase entera en el texto con saltos. Se veían como huecos
  de enero y marzo de 2025; eran un defecto del lector. Corregido y verificados los 22 períodos
  contra el articulado en letras, que confirma los dígitos.

**El jus: los meses que faltaban no faltan.** `estado.py` venía señalando mayo y junio de 2026
como salteados. **La tabla oficial también salta de abril a julio**: la SCBA publica un período
sólo cuando el valor cambia, así que un mes ausente hereda el anterior. Las seis filas que había
coinciden una por una con la fuente y eran **todas** las de 2026. La serie se extendió con lo que
la tabla trae —23 períodos, 01/01/2024 a 01/08/2026, con las dos unidades— y **el detector de
huecos se descartó**: se equivocaba sobre un caso conocido.

**La UMA porteña, que es otra unidad.** El art. 20 de la Ley 5.134 instituye una UMA propia
—1,5% de la remuneración **total** de un juez de primera instancia de la Ciudad, contra el 3% de
la **básica** de un juez federal— y la fija el **Consejo de la Magistratura de CABA**. Su consulta
oficial —`consejo.jusbaires.gob.ar/servicios/uma/`— publica **un solo valor, el vigente**: no hay
tabla ni buscador de resoluciones anteriores, así que **la serie histórica no se reconstruye desde
el organismo que la fija**. Cargado el único que publica: **$175.791 desde el 01/08/2026,
Res. SAGyP 500/2026**.

**Y la conversión existe acá por otro motivo, medido contra el texto.** El art. 51 de la Ley
27.423 obliga a expresar la regulación nacional en pesos Y en UMA bajo pena de nulidad; la Ley
5.134 **no tiene esa regla** —sus dos *"bajo pena de nulidad"* son el art. 16, fundar la
regulación citando la norma, y la integración de intereses a la base—. La UMA porteña hace falta
para contrastar los **mínimos**, que los arts. 21 y 60 escriben en UMA. Por eso `uma_caba.py` es
un script aparte y no una bandera de `uma_csjn.py`: nombrar la jurisdicción queda obligatorio por
construcción, que es lo que impide traer *"un número oficial, vigente y de otra ley"*.

**Qué cambia para quien usa la skill.** En la justicia nacional y federal el art. 51 de la Ley
27.423 exige expresar la regulación en pesos **y** en UMA, y hasta hoy la skill explicaba el
régimen sin poder dar ninguno de los dos números. Ahora `uma_csjn.py --fecha` los da desde el
01/10/2024. Antes de esa fecha **sigue plantándose**: no se extrapola hacia atrás. Y la **UMA
porteña** de la Ley 5.134, que es otra unidad y la publica el Consejo de la Magistratura de CABA,
sigue sin cargar.

---

## 18/09/2026 - Una rúbrica premiaba el fuero equivocado en lo previsional de PBA

**Contra qué se cotejó.** `fuentes/normas/pba-ley-12008.txt`, art. 5º texto según Ley 13.101.

**Qué se encontró.** La rúbrica de `evals/previsional-compensacion-de-edad-y-pba` daba por
correcto que en PBA lo previsional *"va por el **fuero laboral**"*, y lo respaldaba diciendo que
lo señalan el módulo y `docs/COBERTURA.md`. **Los tres extremos son falsos.** El art. 5º de la Ley
12.008 fija la competencia territorial **dentro del contencioso administrativo**, y su **inciso b**
le da regla propia a las *"pretensiones deducidas por reclamantes o beneficiarios de prestaciones
previsionales"* —domicilio del interesado o de la demandada, a elección del demandante—.
`previsional-pba.md` 55 ya lo decía bien y `docs/COBERTURA.md` también.

**Por qué importa más que un error en prosa.** Una rúbrica es el criterio con el que se puntea una
respuesta: escrita así, **reprobaba a quien contestaba bien**. Un eval sin correr no lo delata, y
éste es uno de los veintiún casos que nadie pasó todavía por el sistema. Corregida contra el
texto, con la remisión a `previsional-pba.md` 55 y `contencioso-pba.md` 26.2.

---

## 18/09/2026 - El reparto de OCR y las tres fechas, que estaban escritos adentro de la skill

**No es una auditoría nueva: es la misma, movida de lugar.** El registro de cómo se estableció qué
documentos de `fuentes/jurisprudencia/` se transcriben y cuáles no vivía en el cuerpo de
`references/fallos-csjn.md`, que es un módulo que la skill carga en cada consulta de
jurisprudencia. Ahí el lector pagaba por el diario del trabajo. Lo que queda allá es la **regla**
—la fecha sale del registro de la Secretaría de Jurisprudencia y nunca del encabezado del PDF, y
una cita literal se coteja contra la página—; el cómo se llegó a ella queda acá.

**Las tres fechas.** Los tomos viejos tienen la fecha **impresa en el cuerpo**, en la línea que
sigue al título "FALLO DE LA CORTE SUPREMA", que no es la del dictamen del Procurador —en
"Fiorentino" el dictamen es del 21/05/1984 y el fallo del 27/11/1984—.
`herramientas/auditar_fechas_fallos.py` la lee de ahí y la compara contra el manifiesto. Así se
corrigieron tres que estaban rellenadas con un 1 de enero porque la capa de texto no se podía leer:

| Fallo | Decía | Es |
| --- | --- | --- |
| "Fiorentino" 306:1752 | 1984-01-01 | **27/11/1984** |
| "Santa Coloma" 308:1160 | 1986-01-01 | **05/08/1986** |
| "Bazterrica" 308:1392 | 1986-01-01 | **29/08/1986** |

**Cómo se estableció el reparto.** No por regla ni por estimación: se midió lo que se puede medir
y se leyó el resto. `herramientas/calidad_ocr.py` calcula la basura de caracteres, que es el único
defecto que una medida detecta bien; los veredictos de lectura quedan en
`herramientas/lecturas-ocr.json` con la fecha y lo que se vio. Se descartaron **cuatro** medidas
automáticas que fallaban contra un caso conocido, y tres de ellas buscaban detectar la "mezcla"
que después resultó no existir: estaban midiendo un fenómeno inventado.

**Cada documento se lee uno por uno**, cabecera y una franja del medio —el medio importa: "Santa
Coloma" tiene la cabecera impecable y las sustituciones aparecen en el cuerpo—. El repaso del
**14/09/2026** cerró sobre 63 documentos: **53 se transcribían sin más**, **4 pedían `-layout`** y
**6 tenían defecto real** —tres destruidos y tres con sustituciones—. Los seis quedaron con su
copia recuperada en `ocr/`, así que había texto legible de los 63: 57 directo del PDF y 6 por
relectura, éstos con cotejo obligatorio.

Ese reparto cambió dos veces y las dos por leer, no por estimar. Primero, cinco documentos que
parecían intranscribibles se leían con `-layout`. Después, "S., D." 336:849 estaba clasificado
`layout` y en realidad tenía sustituciones —se descubrió al leerlo para escribir su holding—, así
que pasó de 5 a 4 los que sólo piden `-layout` y de 5 a 6 los que tienen defecto real.

**La medición viva la da `calidad_ocr.py`**, y las cifras de arriba valen por su fecha: son el
estado del 14/09/2026 sobre el corpus de ese día.

---

## 18/09/2026 - La base del art. 245 y las horas extras: el perfil heredado dice lo contrario

**Contra qué se cotejó.** `fuentes/normas/ley-27802.txt`, art. 51 —el que sustituye el art. 245
LCT—, párrafo por párrafo contra `references/laboral.md` 5.2.

**Qué dice el texto.** Define "normal" *"en el caso de conceptos variables como ser premios
mensuales, **horas extra**, comisiones, el promedio de los últimos seis (6) meses, o del último
año si fuera más favorable al trabajador"*. Y las únicas exclusiones que enuncia son las del
párrafo anterior: *"los conceptos de pago no mensuales como el Sueldo Anual Complementario,
vacaciones, premios que no sean de pago mensual"*. **Las horas extra habituales integran la
base**, por la definición de "normal" y no por excepción.

**Qué se encontró.** El módulo estaba bien y lo decía desde el principio —*"No decir que la base
excluye horas extras"*—. El que está mal es el perfil heredado `kb/perfiles/laboral-CLAUDE.md`,
que afirma lo contrario y lo sella con *"Verificado en Infoleg"*. La corrección **no va allá**:
va al módulo, como contradicción nominada con la cita textual del perfil, y quedó como quinta
fila del bloque de 5.11. El perfil no se toca — es capa 2 y la frontera es la ruta.

**Y una segunda, sobre la misma sección.** La cronología de la ventana cautelar de la Ley 27.802
abría diciendo *"Vigencia plena desde el 23/04/2026"* al lado de un cuadro que aplica la ley desde
el 06/03/2026. No eran dos reglas sino una mal enunciada: la ley **rige desde el 06/03/2026**, y
lo que va del 30/03/2026 al 23/04/2026 es la ventana en la que 82 de sus artículos estuvieron
suspendidos. Escrito así, y con el marcador que lo dice cuando el acto extintivo cae adentro —que
`liquidacion_lct.py` no emitía aunque el módulo lo instruyera, teniendo ya el mecanismo escrito
para el tramo simétrico del DNU 70/2023—. La cronología en sí **sigue sin fuente primaria del
expediente** y así está declarado.

---

## 18/09/2026 - El CPCCBA, que se citaba en catorce módulos y no tenía dueño

**Contra qué se cotejó.** `fuentes/normas/pba-cpccba-7425.txt` y `fuentes/normas/cpccn-17454.txt`,
enfrentados artículo por artículo. **No se citó jurisprudencia.**

**Por qué se leyó.** Medido: el CPCCBA aparece en catorce módulos y `proceso-nacional.md` existía
para el CPCCN sin espejo bonaerense. Excepciones previas y caducidad de instancia en PBA no
estaban en ningún módulo.

**Qué salió.**

- **La caducidad no funciona igual, y decide expedientes.** El **art. 315 CPCCBA** (texto según
  Ley 13.986) sustancia el pedido *"previa intimación por única vez a las partes para que en el
  término de cinco (5) días manifiesten su intención de continuar"*, y el **art. 316** condiciona
  la declaración de oficio a esa misma intimación. El **art. 315 CPCCN** sustancia *"únicamente
  con un traslado"* y el **316** declara de oficio *"sin otro trámite que la comprobación del
  vencimiento"*. **En PBA hay un acto que salva la instancia y en la Nación no.**
- **El art. 310 tampoco coincide.** El bonaerense pone en los tres meses la **Justicia de Paz** y
  los procesos **sumarios**; el nacional pone las **ejecuciones especiales y los incidentes**, que
  el provincial no enumera.
- **Las excepciones previas son el art. 345 y no el 347.** El art. 347 del CPCCBA es otra cosa: el
  requisito de admisión. Es el número el que engaña, no el instituto.
- **El deber de fundar sí coincide**: art. 34 inc. 4 en los dos códigos, mismo número y mismo
  texto. Junto con el art. 29 inc. 4 de la Ley 189 —mismo texto, otro número— completa el mapa de
  dónde se cita bien y dónde se cita mal.

**Y el arancel de PBA salió de donde no correspondía.** La Ley 14.967 vivía como sección 1.6.6 de
`sede-judicial-pba.md`, que es del fuero laboral, cuando es la ley arancelaria de **toda** la
justicia bonaerense y sus hermanas —Leyes 27.423 y 5.134— ya tenían módulo. Pasó a
`honorarios-pba.md`, **conservando el número 1.6.6**: la numeración de este repositorio es global
y no se renumera.

---

## 18/09/2026 - La sentencia en la justicia nacional y en el fuero CAyT porteño

**Contra qué se cotejó.** `fuentes/normas/cpccn-17454.txt`, `fuentes/normas/ley-18345.txt` y
`fuentes/normas/caba-ley-189.txt`, artículo por artículo, leídos del texto consolidado. **No se
citó jurisprudencia**: lo que necesita precedente quedó marcado en los módulos.

**Qué se leyó y qué salió.**

- **El art. 155 de la Ley 18.345 lista al art. 163 del CPCCN.** La pregunta que abrió la lectura
  era si el contenido de la sentencia laboral nacional sale de la Ley 18.345 o del CPCCN, y la
  respuesta no es "por analogía" ni "por supletoriedad genérica": el art. 155 enumera los
  artículos aplicables uno por uno, y adentro están los **arts. 160, 161, 163, 164 y 165** y el
  **art. 34 incs. 2, 4, 5 y 6**. De ahí que el civil y el laboral nacionales compartan pieza, y
  que `sede-judicial-nacional.md` sea **uno solo** y no dos.
- **Lo que la Ley 18.345 no cede son los plazos recursivos.** El art. 155 **no** lista el art. 244
  CPCCN. Apelar la definitiva son **seis días con los agravios adentro** (art. 116), la
  interlocutoria **tres días sin fundar** (art. 117), y sin agravios el recurso **se deniega sin
  más trámite** (art. 118). Informar los cinco días del art. 244 en este fuero es error.
- **El deber de fundar cambia de número y no de texto.** Art. 34 inc. 4 CPCCN y **art. 29 inc. 4
  de la Ley 189** dicen lo mismo, palabra por palabra, incluido *"bajo pena de nulidad"*. Es el
  error de cita más difícil de ver leyendo, porque la frase citada es exacta.
- **El art. 147 de la Ley 189 no es el art. 163 del CPCCN con otro número.** Tres diferencias
  salieron del cotejo: el **inc. 5 exige la valoración de la prueba** como contenido escrito,
  donde el CPCCN pide sólo "los fundamentos y la aplicación de la ley"; el mérito de los hechos
  sobrevinientes es **inciso autónomo** (inc. 7) y no un párrafo del de la decisión; y el **inc. 8
  remite al art. 397** para el plazo de cumplimiento cuando la condenada es la autoridad
  administrativa, que no tiene equivalente nacional.
- **El art. 148 condiciona los daños a que hayan sido reclamados.** Es congruencia escrita en el
  código del fuero, y quedó como el nudo del caso de prueba porteño.

**Qué quedó sin cerrar.** El régimen de notificaciones electrónicas de los dos fueros —acordadas
de la CSJN, resoluciones del Consejo de la Magistratura porteño— **no está bajado**, así que
desde cuándo corre un plazo va con marcador y no con fecha. Y ningún estándar de nulidad por falta
de fundamentación se afirmó: sin fallo leído, marcador.

---

## 18/09/2026 - Incorporación de cinco normas nuevas, y dos resultados que contradicen su origen

Segunda tanda de la revisión que abrió la auditoría del régimen penal juvenil. Cinco textos
bajados de InfoLEG y del registro provincial bonaerense, con procedencia y hash, y cotejados
antes de escribir una línea.

**Ley 27.799, Régimen Penal Tributario.** El repo ya razonaba sobre ella en `civil.md` 6.3 sin
tener el texto, y por eso `tributario.md` 33 arrastraba un marcador de monto sobre el umbral del
art. 1. **Ese marcador se cerró contra fuente**: son cien millones de pesos. Los doce umbrales del
Título IX quedaron escritos con su unidad de cómputo, verificados uno por uno contra el
consolidado de `ley-27430.txt`, que ya los trae con la nota de sustitución al pie de cada
artículo. Se incorporó además su reglamentación, el Decreto 93/2026.

**Ley 27.786, organizaciones criminales.** Dos tipos penales nuevos —arts. 210 ter y 210 quáter
CP—, autónomos de la zona especial por su art. 9, y en los dos el texto **desactiva expresamente
los arts. 46 y 47 CP**. Las seis facultades del art. 6 quedaron tabuladas por quién autoriza cada
una, que es donde se juegan las nulidades.

**Ley 25.520 en texto actualizado, con el Decreto 941/2025.** Medido contra el texto: las cinco
prohibiciones del art. 4 siguen, **cuatro tienen excepción nueva y la única que quedó entera es el
inciso 3** —no producir inteligencia por raza, fe, opinión política, pertenencia sindical o
partidaria, ni por actividad lícita—. El art. 10 nonies habilita al personal de inteligencia a
aprehender personas. Queda marcado que es un DNU que reforma una ley del Congreso y que su trámite
ante la Comisión Bicameral no está verificado.

**Ley 27.796, emergencia sanitaria pediátrica.** Nació por insistencia de ambas cámaras con dos
tercios, y el propio texto de InfoLEG trae la comunicación del Senado que lo acredita. Lo
determinante no es su contenido sino su plazo: **se declaró por un año desde el 22/10/2025**.

**Dos resultados que contradicen la hipótesis con la que se empezó.** El informe que motivó la
revisión atribuía a la Ley 15.557 de PBA un efecto sobre el cobro de deudas; leído el texto
completo, **la emergencia que declara no suspende ejecuciones, no declara inembargables los fondos
públicos ni consolida deuda**, y eso se registró como negativo en `contencioso-pba.md` 26.9 bis,
porque la inferencia contraria es automática. Y de las leyes que ese informe presentaba como
novedad, la 27.784 y la 27.785 **ya estaban cotejadas** en `penal.md`. El material sirvió para
elegir dónde mirar; lo que decidió cada punto fue el texto oficial.

## 18/09/2026 - Auditoría contra fuente primaria: la Ley 22.278 está derogada y tres módulos la daban por vigente

**Ley 27.801 de Régimen Penal Juvenil**, bajada de InfoLEG (id 423722) con procedencia y hash en
`fuentes/normas/ley-27801.txt`, y cotejada artículo por artículo. **Su art. 48 deroga la Ley
22.278 y sus modificatorias**; su art. 52 difiere la vigencia a los ciento ochenta días de la
publicación en el Boletín Oficial, que fue el 09/03/2026, de modo que **rige desde el 05/09/2026**.

La sección 24.9.4 de `penal-leyes-especiales.md` describía el régimen de la 22.278 —no punibilidad
por debajo de los dieciséis, punibilidad de dieciséis a dieciocho, los tres requisitos
acumulativos del art. 4 para imponer pena— y se reescribió entera sobre la ley nueva.

**Dos hechos medidos contra el texto, no recordados.** La ley alcanza a los adolescentes **desde
los catorce años**, donde la anterior empezaba en los dieciséis: el universo de punibles se
amplió sin que cambiara una coma del art. 32 de la Ley 13.634, que remite a "la legislación
nacional" sin nombrarla. Y el texto de la 27.801 **no contiene ninguna remisión al art. 44 CP ni
a la escala de la tentativa**, comprobado por búsqueda sobre el archivo: ése era el vehículo legal
del primer holding de *"Maldonado"*, Fallos 328:4343, que `penal-parte-general.md` 24.7.8 citaba sin condición.

**El texto derogado no se da de baja.** El art. 2 CP manda aplicar siempre la ley más benigna, y
para un hecho anterior al 05/09/2026 cometido por alguien de catorce o quince años la 22.278 lo
declaraba no punible. `ley-22278.txt` queda en `fuentes/` porque es lo que permite cotejar de qué
lado cae cada caso, y los tres módulos ahora preguntan primero la fecha del hecho.

**Lo que queda abierto y está marcado**: el decreto reglamentario, que no está cargado; la
adecuación procesal de la Provincia de Buenos Aires, que el art. 49 invita y no impone; y la
suerte de la doctrina de *"Maldonado"* sin la remisión derogada, que no tiene precedente bajado.

**Corrección de origen.** La hipótesis de trabajo que disparó esta auditoría venía de un informe
generado con un modelo de lenguaje, no de una fuente. De su listado, dos leyes que figuraban como
novedad —la 27.784 de juicio en ausencia y la 27.785 de reincidencia y reiterancia— **ya estaban
cotejadas** en `penal.md` 24.2.1 y 24.3.1, y un pasaje suyo sobre el estado cautelar de la Ley
27.802 contradecía lo que `laboral.md` 5.1 tiene verificado con fechas. El informe sirvió para
elegir dónde mirar; lo que decidió cada punto fue el texto oficial.

## 17/09/2026 - Auditoría contra fuente primaria: dos textos ordenados de 2025 y tres números de norma mal atribuidos

Se bajaron y leyeron las normas de dieciséis materias que ningún módulo cubría. Lo que sigue no
es el contenido —eso está en `references/changelog-normativo.md`, fila por fila— sino **lo que la
lectura desmintió**.

1. **Los textos ordenados de 2025 renumeraron el gas y la electricidad, y nadie lo tenía escrito.**
   El **Decreto 451/2025** (B.O. 07/07/2025) aprobó la *"Ley N° 24.076 - T.O. 2025"* y el
   **Decreto 450/2025**, del mismo día, el de la Ley 24.065. La jurisdicción previa del ente pasó
   del **art. 66 al 53** en gas y del **art. 72 al 58** en electricidad.

   Se detectó leyendo *"Y.P.F. S.A. c/ ENARGAS"* (CSJN, 29/09/2015), que cita el art. 66 para el
   texto que el consolidado numera 53. **El corrimiento no es parejo**: los arts. 9 y 14 conservan
   su número, así que no se puede restar. Y **ninguno de los dos decretos publica tabla de
   correspondencia**: el mapeo se establece leyendo. Toda cita anterior a julio de 2025 —incluidas
   las notas de InfoLEG al pie— usa la numeración vieja.

2. **Tres números de norma estaban mal atribuidos, y dos venían de confundir decretos del mismo
   número.**

   - **El baremo es el Decreto 659/96, no el 658/96.** El 658 es el **listado de enfermedades
     profesionales**; el 659 es la **Tabla de Evaluación de Incapacidades**. El perfil heredado
     decía *"baremo del Decreto 658/96"* y la columna de contradicciones de `laboral.md` no
     corregía el número. Corregido, y el 658 bajado: son 187 entradas «AGENTE:».
   - **La reglamentación de la Ley 27.636 es el Decreto 659/2021, no el 721/2020.** El 721 es
     **anterior a la ley** y fijó el cupo del 1% por decreto. Mismo número que el baremo, otro año.
   - **El art. 63 LDC sigue vigente porque su derogación fue vetada.** El art. 32 de la Ley 26.361
     lo derogaba, y el **art. 1° del Decreto 565/2008** —publicado el mismo día— lo observó. La
     **Resolución 344/2009 de Diputados** declaró la validez del decreto. Un texto que liste el
     art. 63 como derogado invierte la prelación del transporte aéreo.

3. **El baremo vigente NO está completo en texto, y la diferencia importa.** El Anexo I del 659/96
   sustituido por el **Decreto 549/2025** está en `fuentes/` en prosa, con los porcentajes que
   enuncia en línea. **Las tablas no**: donde el anexo dice *"deberá determinarse utilizando la
   siguiente tabla"*, la extracción no trae nada, porque son imágenes.

   **No se suplen con OCR**, y está medido: de las **25 correcciones** que dejó el cotejo página
   por página de "Fiorentino", **14 cambian dígitos**, y una convirtió `art. 6°` en `art. 62`. En
   prosa el idioma delata la sustitución; en una tabla de porcentajes no hay nada que la delate.
   Los valores se piden o se marcan.

4. **Ninguna fuente oficial bloquea a los descargadores.** El repositorio documentaba en seis
   lugares que InfoLEG, `normas.gba.gob.ar` y SAIJ devuelven 403 a los agentes. Medido con
   `diagnostico.py` y con `verificar_normas.py`, que no escribe nada: **los seis sitios responden
   HTTP 200**, incluido SAIJ. Lo que sí se confirmó es que el buscador de SAIJ **no se consulta
   por query string** —devuelve *"SIN RESULTADO"* sin rechazar la consulta, que es el peor modo de
   falla—. Corregidos los seis renglones, y lo de JUBA y los sumarios de la CSJN quedó intacto:
   eso no es un 403 sino postback de ASP.NET y estado de sesión.

## 16/09/2026 - Lectura de imagen: las 27 páginas de "Fiorentino" y dos erratas del tomo

El PDF de **"Fiorentino, Diego Enrique"** (Fallos 306:1752) trae la capa de texto arruinada, así
que lo que hay en `fuentes/jurisprudencia/ocr/` es una relectura de las imágenes con tesseract.
Se leyeron **las 27 páginas una por una contra la imagen ampliada**, y el resultado está
declarado como dato en `ocr/correcciones/csjn-fiorentino-fallos-306-1752.json`: **25
correcciones**, que el script vuelve a aplicar en cada regeneración.

**Lo que más importa de esta lectura no son las correcciones, son las dos que NO se hicieron.**

Había seis secuencias que parecían defectos de OCR. Cuatro lo eran: `regisiro` por «registro»,
`setiva` por «sativa» —`cannabis sativa` va en cursiva y el OCR lee la `a` como `e`—,
`consintendo` por «consintiendo», y dos volados de ordinal leídos como dígito, uno de los cuales
convertía el **art. 6° de la ley 20.771 en «art. 62»**: un número de artículo cambiado, que es
la peor clase de error que puede tener una transcripción.

Las otras dos son **erratas del tomo impreso**, y se transcriben como están:

| Página del PDF | Impresa | Lo que dice | Lo correcto sería |
| --- | --- | --- | --- |
| 11 | 1762 | `la defensa inpugnó el aludido` | «impugnó» |
| 13 | 1764 | `donde vvía de modo permanente` | «vivía» |

La de la pág. 11 se confirma con el propio volumen: el mismo pasaje, en el voto del doctor
Petracchi (pág. 15, impresa 1766), imprime «impugnó». O sea que el tomo se contradice a sí mismo
y la errata está en el primer voto, no en nuestra lectura.

**Se anotan porque, si no, la próxima lectura las "arregla".** Una transcripción reproduce el
documento; corregirle la ortografía al tribunal la convierte en otra cosa. Van declaradas en
`no_corregidas` del mismo archivo, con su motivo, y `herramientas/test_reocr.py` exige que
sigan textuales en el `.txt`.

---

## 14/09/2026 - Auditoría contra fuente primaria: la cadena de cobertura de la medicina prepaga

Se bajaron los textos de las **Leyes 23.660, 23.661 y 24.754** y se leyó la cadena que
`salud-discapacidad.md` 27.5 usaba para sostener que la Ley 24.901 alcanza a las prepagas. El
módulo la afirmaba de memoria; ahora los dos eslabones están cotejados y citados textualmente.

1. **El art. 1 de la Ley 24.754 tiene una fe de erratas que cambia el sentido.** El texto
   publicado el 02/01/1997 decía *"prestaciones obligatorias dispuestas **por** las obras
   sociales"*; la fe de erratas lo corrigió a *"dispuestas **para** las obras sociales"*. No es
   lo mismo: "para" son las obligaciones que se les imponen, que es el piso que se traslada a la
   prepaga; "por" sugeriría que cada obra social las fija. Las fuentes secundarias reproducen el
   texto con el error. Anotado en el módulo como advertencia de transcripción.

2. **El art. 28 de la Ley 23.661 dice más de lo que el módulo le atribuía.** El módulo sólo
   decía que "manda actualizar periódicamente" el programa de prestaciones. El texto además
   exige que dentro de las prestaciones obligatorias *"deberán incluirse todas aquéllas que
   requieran la rehabilitación de las personas discapacitadas"*, más los medicamentos que
   requieran. Es el eslabón que cierra el argumento: **la rehabilitación no es una inferencia,
   está en el texto**. Reescrito 27.5 con las dos citas.

3. **Ley 24.455 sin declarar, y con más adentro de lo que se le atribuía.** El art. 1 de la
   24.754 remite a las Leyes 23.660, 23.661 **y 24.455**, y esta última no estaba en el
   manifiesto. Declarada y bajada. Leída, **son siete artículos**, no los tres del resumen que
   circula, y dos no se deducen de la cadena:

   - **Art. 1**: el piso que se traslada a la prepaga incluye, nominadas, la cobertura de
     tratamientos *"médicos, psicológicos y farmacológicos"* de sida —con las enfermedades
     intercurrentes— y de dependencia de estupefacientes, más los programas de prevención.
     Agregado como tercer eslabón en 27.5.
   - **Art. 2**: los tratamientos de los **arts. 16 a 19 de la Ley 23.737** los cubre la obra
     social del beneficiario y **es el juez de la causa quien debe dirigirse a ella**. `penal.md`
     24.9.2 tenía la tabla de esas tres salidas curativas y el art. 19, pero no decía quién paga.
     Agregado ahí, con reenvío a 27.5 para el caso de la prepaga.
   - **Art. 5**: condiciona la ejecutoriedad de la ley a que haya partida presupuestaria
     específica. Es una defensa disponible para el obligado y el repositorio no tiene precedente
     propio sobre su oponibilidad: queda con `[VERIFICAR CRITERIO DEL FUERO]`, sin afirmar que
     está descartada.

   **No existe texact.htm para la 24.455**: la ficha de InfoLEG (id 14919) ofrece sólo "Texto
   completo de la norma", y las diez normas vinculadas son reglamentarias o complementarias
   —Decreto 580/1995, la propia 24.754, la Ley 25.543— sin reforma del articulado. La URL
   declarada es `norma.htm`.

4. **Un defecto de fuente que ninguna medida detecta.** El texto de InfoLEG titula el art. 1 de
   la 24.455 como *"ARTCULO 1°"*, sin la I. `contar_articulos()` no lo cuenta, y el ojo lo
   completa solo al leer. No es un problema del articulado —es el mismo artículo— pero quien
   transcriba desde el repo copia el error. Anotado como advertencia de transcripción en 27.5,
   con la referencia al BO del 08/03/1995, nro. 28.098, p. 1. Es el tercer defecto de OCR/fuente,
   el de las sustituciones que dejan texto plausible, y se registra leyendo, no midiendo.

**Veredictos de lectura sobre las marcas del descargador.** `revisar_texto()` marcó la Ley
24.754 como "sospechosamente corta": son dos artículos en 1.430 caracteres. Leído el texto, es
la ley entera - el 1 sustantivo y el 2 de forma. Para que un falso positivo así no vuelva a
sonar en cada descarga hasta que nadie lo mire, los veredictos se anotan en
`fuentes/normas/revisiones.json`, indexados por el **texto exacto del problema**: si la norma
vuelve con otro defecto, o si cambia cómo el detector lo redacta, la marca vuelve a sonar. Un
veredicto vale para lo que se leyó, no para el archivo.

## 14/09/2026 - Auditoría contra fuente primaria: las trece normas citadas sin texto

Trece normas estaban citadas **con articulado** en los módulos y no tenían su texto en
`fuentes/`. Se completaron doce URLs oficiales, se bajaron y **se leyeron una por una contra lo
que el módulo afirmaba**. Dos afirmaciones no resistieron la lectura.

**1. La prescripción del SECLO estaba mal, en dos módulos y con la cita equivocada.**
`laboral.md` 5.6 y `plazos.md` decían que el art. 7 de la Ley 24.635 suspende *"hasta 30 días
después de notificada la clausura"*. El art. 7 dice otra cosa: *"Esta presentación suspenderá el
curso de la prescripción **por el término que establece el art. 257 de la ley de contrato de
trabajo**"*, y el art. 257 LCT fija **seis meses como máximo**. Recorrida la ley completa, **el
plazo de treinta días no aparece**: la única mención de "treinta" es el tope del 30% de
honorarios del conciliador.

Una entrada anterior de este documento había "unificado" dos versiones contradictorias del
perfil heredado *al criterio del texto legal*, citando ese art. 7. Eligió una de las dos sin
leer el artículo. Corregido en los dos módulos, con dos marcadores: dónde localizar el plazo de
treinta días si rige, y el conflicto que crea la propia ley al decir **suspenderá** y remitir a
un artículo que dice **interrumpirá**.

**2. El "secreto financiero" del art. 39 de la Ley 21.526 es más angosto de lo que decía
`datos-personales.md`.** El módulo listaba entre las excepciones al consentimiento del art. 5
LPDP "las operaciones de entidades financieras". El art. 39 dice: *"Las entidades comprendidas
en esta ley no podrán revelar las **operaciones pasivas** que realicen"*. **Pasivas**: depósitos.
Las **activas** —los préstamos, y con ellos el historial crediticio— no están alcanzadas, y por
lo tanto tampoco lo está la excepción que la LPDP construye remitiendo a él. Es la distinción
que decide un habeas data contra un informe crediticio. Reescrito, con los cuatro supuestos en
que sí hay que informar aun tratándose de operaciones pasivas.

**3. La adhesión de PBA a la Ley 26.485 no sostiene lo que `familia.md` apoyaba en ella.** El
módulo afirmaba *"PBA adhirió por la Ley 14.407"* y de ahí derivaba que el art. 26 de la 26.485
—con la supresión de contenidos digitales que agregó la Ley Olimpia— rige en la provincia. La
cadena, cotejada: el **art. 1 de la 26.485** exceptúa de su orden público *"las disposiciones de
carácter procesal establecidas en el Capítulo II del Título III"*; **el art. 26 está exactamente
ahí**; el **art. 19** da a las jurisdicciones locales la opción de *"dictar sus normas de
procedimiento o adherir"*, y **PBA dictó las suyas**, la 12.569. Y la **Ley 14.407** no es una
adhesión permanente: declara una **emergencia de dos años** desde el 18/10/2012 y el adherir es
el inciso a) de sus bases. La vía firme en PBA es el **inc. n) del art. 7 de la 12.569**, la
medida urgente residual, con su plazo de 48 horas; en toda la 12.569 no aparece la palabra
"digital".

**4. Dos entradas del manifiesto estaban mal descriptas.** La **Ley 14.407** figuraba como
"Adhesión a la Ley 27.736", y es de 2012: no puede adherir a una ley de 2023. Y la **Ley 15.170**
se declaraba para verificar el alcance de la remisión del art. 32 de la Ley 13.927: leída, es la
**ley impositiva 2020** y su art. 72 es un cuadro de tasas —incluida la **tasa de justicia
administrativa de infracciones de tránsito**—, no una regla de competencia. Los dos marcadores
quedaron cerrados con lo que dice el texto.

**5. La Ley 13.478 no es un pendiente: es un límite.** Es de 1948 e InfoLEG no publica normas de
esa época. Buscada en InfoLEG, argentina.gob.ar y SAIJ. Su marcador ahora dice **por qué** falta
y contra qué cotejar —el Boletín Oficial de 1948 o el texto transcripto en el propio fallo—, en
vez de dejar un pendiente que invite a volver a buscarla.

**Un guardarraíl que faltaba: identidad de lo descargado.** Una de las doce URLs apuntaba a otra
norma. El id 44911 de InfoLEG es el texto ordenado del **Impuesto a las Ganancias**, y quedó
guardado como `ley-21526.txt`, que es Entidades Financieras: 488 KB de articulado impecable, de
otra ley. El descargador no lo marcó porque `revisar_texto()` valida la **forma** —que haya
articulado, que no sea la ficha del portal, que el charset esté sano— y no la **identidad**.
`TestIdentidadDeLasNormas` exige ahora que **el número de la norma aparezca en el cuerpo** del
texto bajado, descontando el encabezado de procedencia, que lo escribimos nosotros con el título
del manifiesto: buscar ahí confirmaría lo que ya creemos y no lo que se bajó. Corre sobre las 127
y es el mismo control que `auditar_fechas_fallos.py` hace con la jurisprudencia — identidad
primero, contenido después.

---

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) · [Desarrollar](DESARROLLO.md)

## Septiembre 2026 - Auditoría contra fuente primaria: Ley 15.057, mediación PBA, intereses y art. 245

Auditoría de verificación externa contra **InfoLEG**, el **Boletín Oficial** y
**normas.gba.gob.ar**. A diferencia de la auditoría anterior -que resolvió contradicciones
internas entre archivos-, esta contrastó el contenido del repositorio con el texto de las
normas. Los hallazgos se agrupan por gravedad.

**Reversión de un parche anterior (Ley 27.737).** La entrada previa de septiembre de 2026
había alineado `kb/contratos/CLAUDE.md` a la fórmula "la Ley 27.737 subsiste solo en lo no
derogado". La verificación en InfoLEG confirma lo contrario: el **DNU 70/2023 derogó tanto
la Ley 27.551 como la Ley 27.737**. Se revierte ese parche en sus tres puntos de
`kb/contratos/CLAUDE.md`, y se corrige `kb/perfiles/civil-CLAUDE.md` y `skills/derecho-argentino/SKILL.md`
en el mismo sentido.

**Críticos (afectan la validez del consejo):**

1. **La Ley 11.653 está DEROGADA.** El **art. 88 de la Ley 15.057** derogó la Ley 11.653 y
   sus modificatorias. El código procesal laboral vigente de PBA es la **Ley 15.057**
   (modificada por la **Ley 15.557**), cuya operatividad dispuso la **Res. SC 1840/2024**
   (03/07/2024), con aplicación inmediata a las causas en trámite en las que no se hubiera
   celebrado la audiencia de vista de causa. La 11.653 conserva ultraactividad **solo en
   materia de recusación**. La estructura es de **Juzgados del Trabajo unipersonales** y
   **Cámaras de Apelación del Trabajo**, no de Tribunales del Trabajo colegiados. Art. 17:
   plazos por días hábiles, perentorios e improrrogables; art. 89: CPCCBA supletorio.
   Corregido en `kb/perfiles/laboral-CLAUDE.md`, `kb/transversales/plazos-SKILL.md`, `skills/derecho-argentino/SKILL.md`,
   `setup-interview.md` y los tres archivos del eval laboral, con nota en cada lugar para
   que la 11.653 no se reintroduzca.

   > **Superado el 18/09/2026, y la entrada queda como registro de lo que se verificó ese día.**
   > Decir que la 11.653 conserva ultraactividad *"solo en materia de recusación"* no es lo que
   > rige: en las causas **con audiencia de vista ya celebrada** sigue aplicándose **entera**, y
   > por eso **conviven dos regímenes**. Está así en `.claude/rules/derecho-argentino.md`, que
   > carga siempre, y en la tabla de `sede-judicial-pba.md` 1.6. Lo que esta entrada sí fijó y
   > sigue en pie es que el art. 88 de la Ley 15.057 derogó la 11.653 y que el corte lo hace la
   > Res. SC 1840/2024 por la audiencia de vista.

2. **Mediación PBA (Ley 13.951): no suspende como la nacional.** El **art. 40** le asigna
   **carácter de intimación**, con los efectos del segundo párrafo del **art. 3986 del
   Código Civil** (derogado), hoy reconducidos al **art. 2541 CCyCN**: suspensión por
   interpelación fehaciente, **por una sola vez y por seis meses**. No es el régimen del
   **art. 18 de la Ley 26.589** (suspensión durante todo el procedimiento, con reanudación
   a los 20 días del acta de cierre). Corregido en `kb/transversales/plazos-SKILL.md`, `kb/perfiles/civil-CLAUDE.md`,
   `kb/escritos/civil/escritos/escritos-civil-SKILL.md`, `skills/derecho-argentino/SKILL.md` y el eval
   civil.

3. **Intereses laborales: numeración equivocada.** Los artículos del régimen son **de la
   Ley 27.802**, no de la LCT. **Art. 276 LCT** (texto art. 54 Ley 27.802): créditos nuevos,
   IPC Nivel General INDEC + 3% anual. **Art. 55 de la Ley 27.802** (norma autónoma):
   juicios en trámite al 06/03/2026, tasa pasiva BCRA con piso del 67% y tope IPC+3%,
   instrumentada por **Res. Directorio BCRA 45/2026**. **Art. 277 LCT** (texto art. 56
   Ley 27.802): depósito en cuenta sueldo, tope de costas y honorarios y pago en cuotas.
   Además: el **art. 54 LCT fue derogado por el art. 207 de la Ley 27.802**, y los **arts.
   55 y 57 LCT conservan su materia clásica** (presunciones procesales). Corregido en
   `kb/perfiles/laboral-CLAUDE.md`, `kb/escritos/laboral/telegrama/reglas-normativas.md`, `kb/ejemplos/ejemplos-laboral.md` y
   `skills/derecho-argentino/SKILL.md`.

4. **Base del art. 245 LCT.** El texto vigente (art. 51 Ley 27.802) excluye **SAC,
   vacaciones y premios que no sean de pago mensual**, y **no menciona las horas extras**.
   Define **habitual** (devengado durante al menos seis meses) y **normal** (para conceptos
   variables, promedio de los últimos seis meses). Tope: tres veces el importe del **salario
   mensual promedio** del CCT, **excluida la antigüedad**. Incorpora un **piso del 67% de la
   remuneración calculada** (el estándar de "Vizzoti" quedó en el texto legal para este
   tramo) y un **mínimo de un mes** -los regímenes anteriores tenían mínimo de dos-. Se
   eliminó "horas extras" de la exclusión y el pasaje que contraponía la base del preaviso a
   la del art. 245 sobre esa premisa. Se agregó la advertencia de que el **Título laboral del
   DNU 70/2023 estuvo judicialmente suspendido**, de modo que la exclusión de SAC en el tramo
   30/12/2023 a 08/07/2024 **no está confirmada**, con marcador
   `[REVISIÓN NORMATIVA REQUERIDA: vigencia efectiva del Título laboral del DNU 70/2023 en el
   tramo del acto extintivo - verificar estado cautelar a esa fecha]`.

5. **Art. 64 de la Ley 24.449.** No consagra responsabilidad objetiva: se titula
   **"Presunciones"** y fija presunciones **iuris tantum** (se presume responsable a quien
   carecía de prioridad de paso o cometió una infracción relacionada con la causa; beneficio
   de la duda a favor del peatón). La responsabilidad objetiva surge de los **arts. 1757-1758
   CCyCN**. Corregido en `kb/perfiles/civil-CLAUDE.md`, `kb/escritos/civil/escritos/escritos-civil-SKILL.md`,
   `kb/escritos/civil/escritos/modelos/demanda-danos-accidente-transito.md`,
   `skills/derecho-argentino/SKILL.md` y el eval civil.

**Citas y numeración corregidas:**

- **Ley 24.013:** el art. 99 de la Ley 27.742 derogó los **arts. 8 a 17** en bloque (incluye
  8, 9, 10, 11 y 15) y los **arts. 43 a 48 de la Ley 25.345**. El repositorio enumeraba solo
  "8, 9, 10 y 15".
- **CPCCBA:** el cómputo por días hábiles es el **art. 156**, no el 153. El art. 152 define
  días y horas hábiles; el art. 153 es la *habilitación* de días y horas inhábiles.
- **Plazo de gracia:** Nación, art. 124 CPCCN, **dos** primeras horas del despacho; PBA,
  art. 124 CPCCBA, **cuatro** primeras horas del despacho. Son horas de atención del
  tribunal, no "las 2:00 hs": se corrigieron también los ejemplos de output.
- **Ley 18.345:** traslado de la demanda por 10 días, **art. 68** (el art. 71 regula la
  *forma* de la contestación); apelación de interlocutorias por 3 días, **art. 117** (el
  art. 110 es el efecto diferido, sustituido por el art. 87 de la Ley 27.802); sentencias
  definitivas, 6 días, **art. 116**; caducidad de instancia del **art. 46** (texto art. 82
  Ley 27.802): **6 meses** en primera o única instancia y **3 meses** en segunda.
- **CPCCN:** el plazo de 5 días de la queja lo fija el **art. 282**; se cita "art. 285 en
  función del art. 282".
- **Art. 1198 CCyCN** (texto art. 256 DNU 70/2023): **no hay plazo mínimo imperativo**. A
  falta de plazo pactado: locación **temporal**, usos y costumbres del lugar; **vivienda
  permanente**, dos años; **restantes destinos**, tres años. El repositorio traía "2 años
  para cualquier destino".
- **Art. 47 inc. b LDC** (texto art. 119 Ley 27.701): la denominación legal es "de cero coma
  cinco (0,5) a dos mil cien (2.100) **canastas básicas total para el hogar 3**". "CBT tipo
  3" no es la expresión de la ley.

**Matices incorporados:**

- **Art. 9 LCT** (texto art. 3 Ley 27.802): el texto legal adopta el "criterio de
  **agrupamiento por instituciones**, es decir, el conjunto de normas que rige cada una de
  las instituciones en el derecho del trabajo" (conglobamiento por instituciones). Se
  eliminó la fórmula "instituto por instituto".
- **Ley 14.250:** la derogación de los arts. 10, 16 y 21 por el art. 211 de la Ley 27.802 es
  correcta, pero el **art. 6 sigue previendo la subsistencia de las cláusulas normativas**
  hasta que entre en vigencia un nuevo convenio.
- **Ley 26.944:** su art. 11 **invita a las provincias a adherir** y **PBA no adhirió**; en
  el fuero contencioso administrativo bonaerense el plazo de 3 años del art. 7 no se toma
  automáticamente. Incorporado en `kb/perfiles/civil-CLAUDE.md` y
  `kb/jurisdicciones/administrativo/administrativo-PBA-CLAUDE.md`.
- **Arts. 2537, 2560 y 2561 CCyCN:** modificados por la **Ley 27.586** (BO 16/12/2020), que
  incorporó al art. 2560 la **imprescriptibilidad de las acciones civiles derivadas de
  delitos de lesa humanidad**.
- **Art. 1275 CCyCN:** no es un plazo para demandar - exige que **el daño se produzca**
  dentro de los diez años de aceptada la obra. Explicitado en `kb/perfiles/civil-CLAUDE.md`.

**Estado judicial de la Ley 27.802 - hitos agregados a la cronología:**

- **07/05/2026:** la CSJN rechazó el per saltum del Gobierno.
- **08/07/2026:** la Sala IV de la Cámara Contencioso Administrativo Federal confirmó el
  rechazo de una nueva cautelar de la CGT sobre 81 artículos.
- El fondo sigue pendiente ante el **JCAF N°12 sin cautelar activa**.
- **Advertencia:** esta cronología **se sostiene solo en fuentes secundarias**, sin fuente
  primaria pública del expediente. Por eso va acompañada de marcador de verificación y no
  debe citarse como dato firme en un escrito.

**Normas nuevas incorporadas a las alertas normativas:**

- **Res. 4/2026 del Consejo Nacional del Empleo** (BO 02/09/2026): nuevo SMVM y prestación por
  desempleo.
- **Res. SRT 39/2026** (BO 02/09/2026): montos RIPTE de las prestaciones de la LRT.
- **RG ARCA 5844/2026** (RIFL) y **RG ARCA 5862/2026** (PER); **Resolución 1276/2026** (Fondo
  de Asistencia Laboral, 12/08/2026).
- **PBA - Ley 15.563** (BO 26/12/2025): redujo del 10% al 5% el aporte adicional sobre la
  tasa de justicia (art. 12 inc. g Ley 6.716).
- **PBA - Ley 15.513** (sancionada 12/12/2024): reforma del proceso de alimentos en el CPCCBA
  (arts. 635 bis notificación por apps, 636 bis alimentos provisorios, 641 Canasta de Crianza
  INDEC).
- **Decreto 409/2026:** según el listado oficial es el **Régimen de Promoción del Empleo
  Registrado**. `kb/perfiles/laboral-CLAUDE.md` lo describía como "moratoria laboral": se marcó con
  `[VERIFICAR VIGENCIA: contenido y denominación del Decreto 409/2026]` en lugar de
  reescribirlo a ciegas.

**Evals corregidos:**

- `evals/laboral-despido-tramos-reforma-pba/` - Ley 11.653 reemplazada por la **Ley 15.057**
  en `caso.md`, `rubrica.md` y `resultado.md` (fuero del encabezado: "Juzgado del Trabajo PBA
  (Ley 15.057)"). El obligatorio sobre el código procesal ahora exige identificar la 15.057 y
  **detectar como error** citar la 11.653. Agregado a los ausentes esperados: no debe citar
  la Ley 11.653 como vigente, ni excluir las horas extras de la base del art. 245.
- `evals/civil-danos-transito-factor-objetivo-pba/` - reescrita la premisa de la
  prescripción. El obligatorio pasa a ser que el sistema advierta que la mediación de la
  Ley 13.951 **no suspende como la nacional**, sino que opera como interpelación del
  art. 2541 CCyCN (seis meses, una sola vez), y que compute sobre esa base: accidente del
  12/05/2023, prescripción del art. 2561 al 12/05/2026, mediación iniciada el 10/03/2026,
  vencimiento corrido a alrededor del **12/11/2026**, de modo que a la fecha de la consulta
  (20/08/2026) **la acción sigue viva pero por poco**. Agregado a los ausentes esperados: no
  debe aplicar el régimen del art. 18 de la Ley 26.589 a una mediación bonaerense. Corregido
  además el obligatorio sobre el art. 64 de la Ley 24.449 (presunciones, no responsabilidad
  objetiva).

**Fuentes de verificación:** InfoLEG, Boletín Oficial de la República Argentina y
normas.gba.gob.ar.

---

## Septiembre 2026 - Auditoría normativa cruzada: art. 25 LNPA, art. 256 LCT, SECLO y locaciones

Auditoría de consistencia interna entre perfiles, skills transversales y glosario. Seis
divergencias corregidas, todas por contradicción entre archivos del propio repositorio:

1. **Art. 25 LNPA - plazo de caducidad.** `kb/transversales/plazos-SKILL.md`, `kb/marcadores-GLOSARIO.md` y
   `kb/transversales/bucles-SKILL.md` citaban 90 días hábiles judiciales. `kb/perfiles/administrativo-CLAUDE.md` ya
   tenía documentada la reforma de la Ley 27.742 (BO 09/07/2024), que duplicó el plazo a
   **180 días hábiles judiciales** para actos notificados desde esa fecha. Corregidos los
   tres archivos, con el deslinde de los plazos locales (CABA 90 días art. 7 Ley 189;
   PBA 90 días art. 18 Ley 12.008) para evitar la aplicación analógica del plazo federal.
   El ejemplo de output completo de `kb/transversales/plazos-SKILL.md` quedó marcado: su aritmética
   corresponde a 90 días sobre un acto de 2025, que hoy tiene 180; se conserva como
   ilustración del método con `[REVISIÓN NORMATIVA REQUERIDA]` para recomputarlo.

2. **Prescripción laboral - art. 256, no art. 258.** El ejemplo canónico del marcador A10
   en `kb/marcadores-GLOSARIO.md`, y su reproducción en `kb/transversales/diagnostico-SKILL.md` y
   `kb/transversales/bucles-SKILL.md`, citaban el art. 258 LCT. El art. 256 es la prescripción bienal de
   los créditos laborales; el art. 258 rige las acciones por accidente de trabajo y
   enfermedad profesional. `kb/perfiles/laboral-CLAUDE.md`, `kb/transversales/plazos-SKILL.md` y `kb/ejemplos/ejemplos-laboral.md`
   ya usaban el art. 256. Unificado al art. 256 con la aclaración del deslinde.

3. **SECLO - dies a quo de la reanudación.** `kb/perfiles/laboral-CLAUDE.md` decía "30 días después de
   la audiencia" en dos puntos; `kb/transversales/plazos-SKILL.md` decía "30 días desde la notificación de
   la clausura" (art. 7 Ley 24.635). Unificado al segundo criterio, que es el del texto
   legal, con cita del artículo.

4. **Corte temporal de la Ley 27.742.** La tabla de transición de `kb/perfiles/laboral-CLAUDE.md`
   ubicaba el corte el 10/07/2024, mientras que todas las reglas sustantivas del mismo
   archivo operan desde el 09/07/2024. Unificado al 09/07/2024.

5. **Actas CNAT 2764/2022 y 2788/2024.** Aparecían en `kb/perfiles/laboral-CLAUDE.md` sin relación
   explícita, lo que se leía como contradicción. Aclarado: son actas distintas - la
   2788/2024 derogó la 2783/2024 y dejó sin efecto la recomendación unificada; la
   2764/2022 (tasa activa con capitalización) fue dejada sin efecto por la CSJN en "Oliva".

6. **Ley 27.737 en locaciones.** `kb/contratos/CLAUDE.md` la daba por derogada en bloque;
   `kb/perfiles/civil-CLAUDE.md` decía que subsiste en lo no derogado. Alineado `kb/contratos/CLAUDE.md`
   a la fórmula conservadora, en tres puntos.

**Casos de verificación agregados:**

- `evals/laboral-despido-tramos-reforma-pba/` - despido sin causa del 15/10/2025 con
  registración deficiente e intimación previa, ante Tribunal del Trabajo PBA. Pone a
  prueba el tramo temporal del art. 245, la derogación de los agravantes de la Ley 24.013
  y de la Ley 25.323, la inaplicabilidad del SECLO en PBA y el cómputo de la prescripción
  crédito por crédito.
- `evals/civil-danos-transito-factor-objetivo-pba/` - peatón embestido, prescripción
  trienal vencida salvo suspensión por mediación prejudicial de la Ley 13.951 PBA. Pone a
  prueba el factor de atribución objetivo frente a un planteo del abogado basado en la
  culpa, la citación en garantía del art. 118 Ley 17.418 y la negativa a cuantificar
  incapacidad sin pericia.

**Agregado:** `skills/derecho-argentino/SKILL.md` - skill destilada de laboral y
civil/comercial PBA, autosuficiente, con las reglas de integridad, los marcadores
canónicos y los anclajes normativos de ambas ramas.

## Septiembre 2026 - Incorporación de fuentes doctrinarias: CCyC Comentado y derecho de daños

Dos obras de referencia sumadas al repositorio, con tratamiento distinto según su licencia.

**Código Civil y Comercial de la Nación Comentado (SAIJ-INFOJUS, 2ª ed. actualizada 2022).**
Directores: Marisa Herrera, Gustavo Caramelo y Sebastián Picasso. Publicación de distribución
gratuita del Ministerio de Justicia y Derechos Humanos, de libre reproducción total o parcial
citando la fuente. Los seis tomos se incorporan completos en `derecho/fuentes/ccyc-comentado/`
(~18 MB), junto con `INDICE.md`, que:

- mapea cada tomo a su rango de artículos y al archivo PDF correspondiente;
- detalla la estructura interna de cada tomo (Libro / Título / Capítulo) con la página del PDF
  donde arranca cada sección, verificada contra el cuerpo de la obra y no calculada;
- consigna el desfasaje entre página impresa y página PDF, constante dentro de cada tomo
  (T1 +39, T2 +23, T3 +27, T4 +29, T5 +25, T6 +25);
- incluye una tabla de ruteo rápido por instituto, pensada para ir directo al comentario de un
  artículo mientras se redacta;
- señala que "contratos en particular" queda partido entre los tomos 3 y 4, que es el error de
  navegación más probable;
- registra una discrepancia de la fuente sin corregirla: los tomos 1 a 5 imprimen como ISBN de
  obra completa 978-987-8338-31-6 y el tomo 6 imprime 978-987-8338-37-8.

**Manual de Derecho de Daños, 2ª ed. (Weingarten -dir.-, La Ley, 2015).** Obra comercial con
todos los derechos reservados: el editor prohíbe expresamente su reproducción total o parcial.
Como este repositorio es público, **el PDF no se incorpora y no debe incorporarse**. En su lugar
se agrega `derecho/kb/doctrina/civil-DOCTRINA-danos.md`, un índice doctrinario con 38 entradas por
instituto, cada una con síntesis propia, artículos del CCCN y del Código derogado, fallos
citados y remisión a capítulo y página. No contiene transcripción de la obra: el texto
entrecomillado corresponde a carátulas de fallos y a expresiones de la ley.

El archivo consigna además qué institutos la obra **no** trata de forma autónoma -antijuridicidad,
relación de causalidad, eximentes y prescripción no tienen capítulo propio; el daño punitivo solo
tres menciones breves- y una sección de advertencias de vigencia, porque la obra es de 2015 y
comenta el CCCN recién sancionado: DNU 70/2023 en locaciones y obligaciones en moneda extranjera,
art. 1764 CCCN y adhesión provincial a la Ley 26.944, tope del daño punitivo hoy en canastas
básicas por la Ley 27.701, y las fórmulas de cuantificación, que no tienen consagración legal.
Se deja señalado que la obra atribuye el art. 52 bis LDC a la "ley 26.367" cuando corresponde a
la Ley 26.361.

**Regla nueva de higiene del repositorio.** Se agrega `derecho/fuentes/_local/` al `.gitignore`:
es la carpeta donde el abogado guarda su ejemplar de obras comerciales, que nunca se commitean.
El criterio: una obra entra al repositorio solo si su propia licencia lo permite. Las que no,
entran como doctrina destilada con remisión, nunca como texto.

---
