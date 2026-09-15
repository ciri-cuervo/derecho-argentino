# Intake · qué datos pedir antes de analizar

> Módulo de referencia de la skill `derecho-argentino`. Se lee en el primer turno de una
> consulta de fondo, junto con la apertura de la sección 0 del SKILL.md.

Un análisis jurídico hecho sobre datos faltantes no es un análisis con un hueco: es un
análisis de otro caso. La fecha del acto extintivo decide qué régimen rige, la fecha de la
audiencia de vista decide qué código procesal se cita, el CCT decide el tope. Cambiá uno y
cambia el resultado entero, no un párrafo.

## El rol va primero y va solo

La pregunta de la sección 0.1 —desde dónde se actúa y en qué fuero— **no forma parte de esta
tanda**. Va antes, sola, y se espera la respuesta: de ella depende cuál de los checklists de
abajo corresponde y qué se hace con los datos una vez que llegan. Mezclarla con doce
preguntas sobre el caso es la forma más segura de que se conteste de paso y mal.

## Cómo preguntar

**Una sola tanda, no un interrogatorio de a uno.** Listar numerado lo que falta, con media
línea de por qué hace falta cada dato. El usuario contesta de una y se trabaja.

**Sólo lo determinante bloquea.** El criterio es duro: un dato bloquea si, cambiándolo,
cambia el resultado. Lo demás se marca y se sigue. Si al terminar la tanda quedan tres
preguntas, están bien; si quedan doce, la mitad no eran determinantes.

**"No surge del expediente" es una respuesta válida y completa**, no una evasiva. Cierra la
pregunta y convierte el dato en marcador. En sede judicial es además una respuesta con
consecuencia propia: el hecho no está acreditado y lo soporta quien tenía la carga (ver
`sede-judicial-pba.md`, 1.6).

**Nunca ofrecer un valor de ejemplo para que lo confirmen.** "¿La remuneración era del orden
de un millón?" contamina la respuesta y termina en una liquidación con un número que nadie
aportó.

**No repreguntar lo que ya está en el material.** Antes de armar la tanda, leer lo aportado.
Preguntar la fecha de ingreso cuando está en el primer párrafo de la demanda quema la
paciencia que hace falta para las preguntas que sí importan.

---

## Laboral · liquidación o verificación de una liquidación

Ver también `laboral.md`, 5.10, que trae la tabla de marcadores por dato.

**Bloquean:**

| Dato | Por qué |
|---|---|
| Fecha de ingreso | Antigüedad y multiplicador del art. 245 |
| **Fecha del acto extintivo** | Decide el tramo de reforma. Es el dato que más veces cambia todo el resultado |
| Modo de extinción y quién lo dispuso | Decide qué rubros proceden |
| Remuneraciones del último año, mes por mes | Base del art. 245 y de preaviso e integración |
| CCT invocado | Tope del art. 245 y escalas. En sede judicial **no es dato del tribunal**: surge de lo que invocan y prueban las partes |
| Tope del art. 245 del CCT al período | Sin esto la liquidación es provisoria |

**Se marcan y no bloquean:** vacaciones gozadas en el año; si el período de prueba estaba
vigente; si hubo intimación fehaciente previa (sólo relevante para actos anteriores al
9/7/2024); categoría; jornada.

## Laboral · régimen procesal y trámite

**Bloquea:** la **fecha de la audiencia de vista de causa**. Decide si la causa sigue bajo la
Ley 11.653 o el rito de la Ley 15.057, y con ello la estructura de la pieza, el régimen de
caducidad y la vía recursiva (`sede-judicial-pba.md`, 1.6.1).

**Bloquean también, según la tarea:** fecha de notificación del acto que se quiere recurrir;
departamento judicial; si la sentencia es condenatoria, para el depósito previo.

## Cómputo de plazos

**Bloquean:** fecha de notificación —sin ella no se calcula, se emite `[VACÍO PROBATORIO]`—;
fuero y jurisdicción; qué acto procesal es, para saber qué norma fija el plazo; y si el plazo
es en días hábiles, corridos, meses u horas.

**Se marca:** si hubo suspensión por mediación o conciliación previa, cuyo régimen no es
equivalente entre Nación y PBA (`plazos.md`, 8.4).

## Intereses y actualización

**Bloquean:** naturaleza del crédito —prestación de la LRT con fórmula legal propia, o
crédito común de la LCT: la respuesta decide entre "Galarza" y el resto—; fecha desde la que
corre cada tramo; si el juicio estaba en trámite al 6/3/2026, para el art. 55 de la Ley
27.802; y si ya hubo cuantificación a valores actuales, que parte el cálculo en dos tramos.

**Se marca:** el índice o tasa concretos, que salen de las series y nunca de la memoria.

## Honorarios

**Bloquean:** monto del proceso (art. 23); etapas cumplidas —en procesos orales ante
tribunales colegiados son tres, art. 28 inc. h—; si la condena incluye intereses, que obliga
a **diferir** el auto regulatorio (art. 51); y el valor del jus a la fecha, que cambia todos
los meses.

**Se marca:** carácter de la intervención; si hubo litisconsorcio, por el tope del 40%.

## Daños civiles

**Bloquean:** fecha del hecho —derecho intertemporal, art. 7 CCyCN, y prescripción—; factor
de atribución, que decide toda la estrategia probatoria y hay que identificar **antes**;
rubros reclamados; si hay relación de consumo, que cambia el plazo de prescripción y habilita
el daño punitivo; y si hay seguro, por la citación en garantía y el límite de cobertura.

**Se marca:** el criterio de cuantificación de la sala, y el valor de la canasta para el tope
del daño punitivo.

## Contratos

**Bloquean:** fecha de celebración —en locación decide entre tres regímenes—; si es de
adhesión o paritario; si hay consumidor; y el texto completo, no un resumen.

El análisis de red-flags se dispara solo, sin instrucción (sección 7). Si el contrato vino con
instrucción de modificarlo, primero el informe y después **preguntar**.

## Consumo

**Bloquean:** si hay **relación de consumo** y quién es el proveedor —el art. 1093 CCyCN exige
actuación organizada, habitual y lucrativa, y sin proveedor profesional no hay estatuto
protectorio—; fecha del hecho o del contrato; si el reclamo es **individual o colectivo**, que
cambia el régimen de gratuidad; y si existe un **plazo especial** aplicable al contrato de que
se trate, por la doctrina de "Toscano".

Para daño punitivo bloquean además: la conducta concreta que se imputa al proveedor, y el
valor de la CBT hogar 3 del mes, que fija el tope.

**Se marca:** la vía administrativa previa, que en PBA no es obligatoria (17.2).

## Familia

**Bloquean:** qué materia del art. 827 CPCCBA es, porque decide competencia y si hay etapa
previa; si ya se cumplió la **etapa previa ante el Consejero**, o si el caso es de urgencia o
se optó por saltearla en alimentos; el **centro de vida** de los niños, niñas o adolescentes
(art. 716 CCyCN), que decide competencia territorial; y si hay **medidas de protección
vigentes** por violencia familiar, que cambian el orden de todo lo demás.

En alimentos bloquean además: edades de los alimentados —la Canasta de Crianza sólo llega
hasta los 12 años—, si hubo interpelación fehaciente y su fecha, por la retroactividad del
art. 641, y los ingresos y capacidad económica del alimentante o los indicios de ella.

**Se marca:** todo lo que dependa del informe del Equipo Técnico Auxiliar.

## Escritos aportados para diagnóstico

**Bloquean:** el texto completo del escrito; tipo de pieza y fuero; y quién lo suscribe.

**Se marca:** todo lo demás. El diagnóstico está para encontrar los huecos, no para exigirlos
por adelantado.

## Sede judicial · proyecto de veredicto, sentencia o interlocutoria

Además de lo anterior:

**Bloquean:** fecha de la audiencia de vista (estructura de la pieza); **qué opuso cada
parte** —determinante para congruencia y para saber si la prescripción fue opuesta, que no se
declara de oficio—; rubros pretendidos, uno por uno; y prueba producida sobre cada hecho, que
es lo que el veredicto tiene que individualizar (art. 47).

**Se marca:** lo que no surja del expediente, con la consecuencia de carga probatoria que
corresponda.

## Modo parte · antes de demandar o contestar

Además de lo que pida la materia:

**Bloquean:** por quién se actúa; **si ya hubo intercambio telegráfico**, con fechas y textos
—condiciona qué se puede reclamar—; si se agotó la instancia conciliatoria previa, que el
art. 31 inc. i de la Ley 15.057 exige acreditar en la demanda; qué prueba está efectivamente
en poder de la parte, porque se ofrece toda en la demanda o contestación y después no entra;
y, si es contestación, la fecha de notificación del traslado.

En reclamos por accidente o enfermedad, bloquea además si ya se optó por la vía de la LRT o
la civil: la opción del art. 4 de la Ley 26.773 es excluyente e **irrevocable**, y preguntarlo
después de encaminar la demanda no sirve de nada.

**Se marca:** todo lo que dependa de prueba a producir.

---

## Lo que no se pregunta

- **Lo que se verifica solo.** Si el repo está disponible, el texto de un artículo, la
  vigencia de una norma o el valor del jus se buscan, no se preguntan.
- **Lo que el usuario no puede saber.** A un tribunal no se le pregunta el CCT de la
  actividad: se le pregunta qué CCT invocaron y probaron las partes.
- **Lo que ya se preguntó.** Si un dato se pidió y la respuesta fue que no consta, no se
  vuelve sobre él: quedó como marcador.
