# Empleo público nacional · Ley 25.164

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

Cotejado contra `fuentes/normas/ley-25164.txt`.

**Este módulo existe porque el repositorio declaraba el hueco.** `scripts/liquidacion_lct.py` se
planta y emite `[ARG SIN NORMA]` cuando el empleador es público: el **art. 2 inc. a de la LCT**
excluye a los dependientes de la Administración salvo acto expreso de inclusión, **así que la
extinción no se liquida por los arts. 245 y siguientes**. Lo que sigue es adónde va entonces.

## 49 · Empleo público nacional

### 49.1 Lo primero: la LCT no se aplica, y la competencia suele ser otra

**Sin acto expreso de inclusión en la LCT o en un convenio colectivo que los comprenda**, al
empleado público lo rigen **su estatuto y su régimen de estabilidad**, y el conflicto suele
tramitar ante el fuero **contencioso administrativo**, no ante el laboral.

**Consecuencia directa:** no hay indemnización del art. 245, no hay preaviso de la LCT y no
corren las multas de la Ley 24.013 ni del art. 2 de la Ley 25.323. Liquidar un cese público con la
calculadora laboral da un número que no existe. Ver `laboral.md` 5 para el lado del que se viene, y
`administrativo-nacional.md` 46 para la impugnación del acto.

### 49.2 Qué alcanza esta ley, y qué queda para la negociación

**Sus disposiciones tienen carácter general** (art. 3) y **se adecuan por negociación colectiva
sectorial de la Ley 24.185**, salvo lo que el propio artículo excluye. Antes de aplicar un
artículo de la 25.164 a un organismo concreto hay que ver si un convenio sectorial lo desplazó.

`[VERIFICAR CCT APLICABLE: el régimen del empleado público nacional se adecua por negociación colectiva sectorial conforme el art. 3 de la Ley 25.164. Verificar qué convenio rige en el organismo antes de aplicar el texto general]`

### 49.3 Estabilidad: quién la tiene y cuándo se adquiere

**Art. 8:** el régimen de estabilidad comprende al personal que **ingresa por los mecanismos de
selección** a cargos del régimen de carrera, con financiación prevista en la Ley de Presupuesto.

**Art. 17:** el personal con estabilidad tiene derecho a **conservar el empleo, el nivel y el grado
alcanzado**, y la ley enumera las condiciones que deben cumplirse para adquirirla. **La estabilidad
en la función es materia convencional**, y no se confunde con la estabilidad en el empleo.

**Y hay una categoría que no la tiene (art. 9):** el personal contratado **por tiempo determinado**,
que comprende exclusivamente servicios **transitorios o estacionales** no incluidos en las
funciones del régimen de carrera y que no puedan cubrirse con planta permanente. Es la figura que
se usa de hecho para relaciones prolongadas, y de ahí sale buena parte de la litigiosidad.

**Reestructuración (art. 11):** el personal con estabilidad afectado por supresión de órganos o
funciones, o por reducción de dotación, entra en el régimen que ese artículo prevé. No es un
despido y no se indemniza como tal.

### 49.3.1 El contratado en relaciones prolongadas — "Ramos", y hasta dónde llega

**CSJN, "Ramos, José Luis c/ Estado Nacional (Min. de Defensa - A.R.A.) s/ indemnización por
despido", Fallos 333:311, R. 354. XLIV, 06/04/2010.** Leído contra el documento. Veintiún años de
renovaciones bajo el decreto 4381/73, rescindidas por restricciones presupuestarias. **Revoca** el
rechazo de la demanda.

**Lo que se prueba no es el paso del tiempo, sino el fraude al plazo del régimen.** El decreto
limitaba la renovación a **cinco años**, y la administración contrató veintiuno *"en abierta
violación al plazo máximo previsto por la norma"*. Sobre eso la Corte concluye que usó figuras de
excepción **"con una evidente desviación de poder que tuvo como objetivo encubrir una designación
permanente bajo la apariencia de un contrato por tiempo determinado"**.

**Los indicios que el fallo pondera, y que hay que ofrecer como prueba:** que las tareas *"carecían
de la transitoriedad que supone el mencionado régimen de excepción"*, que el agente era
**calificado y evaluado en forma anual**, que **se le reconocía la antigüedad** y que **gozaba de
los servicios sociales** del empleador.

**La consecuencia es la legítima expectativa, y su protección es indemnizatoria.** El
comportamiento estatal *"tuvo aptitud para generar [...] una legítima expectativa de permanencia
laboral que merece la protección que el artículo 14 bis de la Constitución Nacional otorga al
trabajador contra el 'despido arbitrario'"*.

**Pero no hay reincorporación, y esto es lo que más se cita al revés.** El actor *"no podría
solicitar su reincorporación al empleo ni la aplicación de un régimen laboral específico para el
cálculo de la indemnización"*. Atribuir estabilidad a quien no ingresó por los mecanismos de
selección **trastocaría el art. 8 de la Ley 25.164** y alteraría el monto que el Congreso autoriza
por separado para personal contratado y permanente (arts. 75 inc. 8 CN y 29 de la Ley 24.156). Ese
art. 29, cotejado contra `fuentes/normas/ley-24156.txt`, dice que los créditos del presupuesto
**"constituyen el límite máximo de las autorizaciones disponibles para gastar"**: es el pilar
presupuestario del argumento, y no admite excepción judicial. Por
eso el caso **se distingue de `"Madorrán"`** (Fallos 330:1989), donde el agente era de planta
permanente y sí tenía estabilidad.

**La cuantía sale del derecho público, por analogía.** Las partes *"no tuvieron la intención de
someter el vínculo a un régimen de derecho privado"*, así que **no se aplica el art. 245 LCT**: a
falta de previsión específica, la Corte toma **la indemnización del art. 11 de la Ley 25.164** como
*"una medida equitativa"*. Es la misma norma de 49.3, usada acá **por analogía** y no por su
supuesto de hecho.

**Y el sometimiento voluntario al régimen no cierra el reclamo.** `"Gil"` (Fallos 312:245) no
obsta, porque lo que se cuestiona no es el régimen sino **el incumplimiento de sus límites
temporales**.

*Cómo se usa.* Es la base de cualquier reclamo de un contratado con antigüedad. **Pide
indemnización, no reincorporación**, y su eje probatorio es el plazo máximo del régimen invocado
más los indicios de no transitoriedad. Las costas se impusieron por su orden *"atento a la
ausencia de un criterio claramente uniforme en los precedentes de esta Corte"*, y Fayt, Maqueda y
Zaffaroni concurrieron **según su voto**.

### 49.4 Cómo termina la relación

**Art. 42** enumera las causales: cancelación de la designación del personal **sin** estabilidad,
renuncia aceptada o vencimiento del plazo, y las demás que el artículo detalla.

**La renuncia tiene una regla propia (art. 22):** produce **la baja automática a los treinta días
corridos** de presentada si antes no fue aceptada. Y su aceptación **puede dejarse en suspenso** en
los supuestos que el artículo contempla — típicamente si hay sumario en trámite.

**Cesantía (art. 32):** entre sus causales, **inasistencias injustificadas que excedan de cinco
días discontinuos en los doce meses anteriores** y **abandono de servicio**, que se considera
consumado con **más de tres inasistencias continuas** sin causa y previa intimación en los términos
del artículo.

### 49.5 La impugnación de la sanción: hay opción, y el plazo es de noventa días

**Art. 39 — el agente con estabilidad puede optar:**

1. **Impugnar por la vía administrativa común** y, agotada ésta, ir a sede judicial; **o**
2. **Recurrir directamente** ante el tribunal que el artículo indica.

**Art. 40:** el **recurso judicial directo se interpone dentro de los noventa días de notificada la
sanción**, y la autoridad debe remitir el expediente con el legajo **dentro de los diez días** de
requerido.

**Elegir una vía cierra la otra**, y el plazo de noventa días no se suspende por intentar después
la administrativa. Es la decisión que hay que tomar temprano y con la fecha de notificación a la
vista.

**El procedimiento disciplinario debe garantizar la defensa en juicio** y establecer **plazos
perentorios e improrrogables** para resolver (art. 38), pero su detalle sale de la reglamentación.

### 49.5.1 Un deber que llega desde afuera de la Ley 25.164: la Ley Micaela

**La Ley 27.499** —cotejada contra `fuentes/normas/ley-27499.txt`— impone **capacitación
obligatoria en género y violencia contra las mujeres a todas las personas que se desempeñen en la
función pública, en los tres poderes de la Nación** (art. 1). No está en el estatuto, pero **pega
en el régimen disciplinario de 49.5**, y por eso aparece acá.

**Lo que decide un caso es el art. 8, y conviene leerlo entero.** La secuencia tiene tres pasos y
la sanción cuelga del tercero, no del primero:

1. La persona **se niega sin justa causa** a realizar la capacitación.
2. La autoridad de aplicación la **intima en forma fehaciente**, a través del organismo de que se
   trate.
3. **"El incumplimiento de dicha intimación será considerado falta grave dando lugar a la sanción
   disciplinaria pertinente"** — y además *"siendo posible hacer pública la negativa a participar
   en la capacitación"*.

> **La falta grave es el incumplimiento de la INTIMACIÓN, no la negativa.** Sin intimación
> fehaciente previa no se llega al encuadre, y ésa es la primera defensa en un sumario que se
> apoye en este artículo. La otra es la **justa causa**, que la ley admite sin definir.

**Quién responde por la implementación.** No es sólo la persona: el art. 4 pone a **las máximas
autoridades de cada organismo** —con sus áreas de género y las organizaciones sindicales— como
responsables de garantizar las capacitaciones. Y el art. 7 obliga al organismo de aplicación a
publicar el **grado de cumplimiento por organismo**, con el porcentaje de personas capacitadas
**desagregado por jerarquía** y un informe anual.

#### 49.5.1 bis En PBA rige otra ley, y las diferencias deciden casos

El art. 10 de la nacional **invita a adherir**, y la Provincia lo hizo con la **Ley 15.134**
—cotejada contra `fuentes/normas/pba-ley-15134.txt`—, que **no es una adhesión de un artículo:
tiene trece propios**. Cuatro diferencias, y ninguna es de matiz:

| | **Ley 27.499 (nacional)** | **Ley 15.134 (PBA)** |
| --- | --- | --- |
| A quién alcanza | Quienes se desempeñen en la función pública, sin más (art. 1) | Lo mismo **más** *"en forma permanente o transitoria, ya sea por cargo electivo, designación directa, por concurso o por cualquier otro medio legal"* (art. 1) |
| Efecto sobre la carrera | **No tiene norma** | La capacitación permanente es **"requisito obligatorio para la promoción a niveles superiores por concurso o progresión"** (art. 3) |
| Quién intima | La **autoridad de aplicación** (art. 8) | Los **órganos de implementación** de cada poder (arts. 5 y 8) |
| Justa causa | *"se negaren **sin justa causa**"* (art. 8) | *"se negaren"* — **la fórmula no está** (art. 8) |

**Las dos últimas son las que hay que tener a la vista en un sumario bonaerense.** El art. 8
provincial **no condiciona el encuadre a que la negativa sea sin justa causa**, así que la defensa
que sirve en el orden nacional no tiene el mismo anclaje textual acá; y quien debe intimar no es la
autoridad de aplicación sino el **órgano de implementación del poder respectivo**, designado por el
art. 5. Una intimación cursada por quien no corresponde es atacable.

**Y la sanción provincial es doble.** El incumplimiento *"será considerado falta grave y dará lugar
a las sanciones que prevean la Constitución, leyes, estatutos y reglamentos respectivos"* —o sea
que remite al estatuto aplicable y no fija ella la sanción— ***"sin perjuicio de la no
efectivización de la promoción"*** del art. 3, y de publicar la negativa. **El bloqueo de la
carrera es autónomo de la sanción disciplinaria**, y es lo que la nacional no tiene.

**Dos capas más que la nacional no arma.** La Ley 15.134 separa la **autoridad de aplicación**
(art. 4) de los **órganos de implementación** por poder (art. 5), y su art. 11 **invita a adherir a
los municipios** — así que en un caso municipal hay que preguntar si esa comuna adhirió.

`[VERIFICAR VIGENCIA]` La autoridad de aplicación nacional que la ley nombra es el **Instituto
Nacional de las Mujeres** (arts. 3, 5, 6 y 7), y ese organismo fue reestructurado después de 2018:
antes de afirmar quién certifica o publica hoy, verificar qué organismo lo sucedió. En PBA el art.
4 **delega la designación en el Poder Ejecutivo** dentro de los treinta días de la promulgación y
no la nombra: hay que verificar en qué organismo recayó.

`[CONFIGURACIÓN INCOMPLETA: si el agente es municipal, la Ley 15.134 rige sólo si esa comuna adhirió por su art. 11 - el listado de municipios adherentes no está en fuentes/ y hay que pedirlo o verificarlo]`

### 49.5.2 El cupo del uno por ciento — Ley 27.636

Cotejada contra `fuentes/normas/ley-27636.txt`. Su **art. 5** obliga al **Estado nacional** —los
tres poderes, los Ministerios Públicos, los organismos descentralizados o autárquicos, **los entes
públicos no estatales**, y las empresas y sociedades del Estado— a ocupar **no menos del uno por
ciento (1%)** de su personal con personas travestis, transexuales y transgénero, **en todas las
modalidades de contratación vigentes**.

**Tres precisiones que cambian a quién se le reclama.** El cupo no se mide sobre la planta
permanente sino sobre **la totalidad del personal** y **todas las modalidades**, así que alcanza a
los contratados de 49.3; alcanza a **entes públicos no estatales**, que suelen quedar fuera de la
Ley 25.164; y el **art. 8** exige que la inclusión se refleje en **todos los organismos obligados**
y con **distribución federal** de los puestos, no concentrada.

**Y hay una regla de contrataciones (art. 10):** el Estado nacional debe dar **prioridad en sus
contrataciones** a quienes cumplan con la ley — un incentivo que opera sobre proveedores privados.

**Dónde está la definición de «ente público no estatal», que es la que decide el alcance.** No en
la ley: la da el **art. 5 del Decreto 659/2021**, la reglamentación, por remisión al **inc. c del
art. 8 de la Ley 24.156**. Las dos normas están bajadas.

**Y el cupo existía antes de la ley.** El **Decreto 721/2020** lo había fijado en el 1% para el
Sector Público Nacional, con **reserva de puestos** y de las vacantes que dejen quienes ingresaron
por ese régimen, y con la aclaración de que cumplirlo **nunca implica el cese de relaciones
laborales existentes**. Sigue siendo la norma a citar para el período anterior a la Ley 27.636.

El resto del régimen —terminalidad educativa, antecedentes contravencionales y el detalle de la
reglamentación— está en `laboral.md` 5.17 ter, porque rige el ingreso en general y no sólo el
empleo público.

### 49.5.3 Ética pública — Ley 25.188

Cotejada contra `fuentes/normas/ley-25188.txt`. **Es un régimen paralelo al estatuto**: se aplica
*"sin excepción, a todas las personas que se desempeñen en la función pública en todos sus niveles
y jerarquías, en forma permanente o transitoria, por elección popular, designación directa, por
concurso o por cualquier otro"* medio legal (art. 1) — la misma fórmula que el art. 1 de la Ley
15.134 de PBA que está en 49.5.1 bis, y por eso alcanza a quien no tiene estabilidad.

**Las incompatibilidades que se alegan (arts. 13 a 15).** Es incompatible *"dirigir, administrar,
representar, patrocinar, asesorar, o, de cualquier otra forma, prestar servicios"* a quien gestione
o tenga una concesión, sea proveedor del Estado o realice actividades reguladas por él, **siempre
que el cargo tenga competencia funcional directa** sobre eso. Quien ya está alcanzado al ser
designado debe **renunciar a esa actividad como condición previa** a asumir, o **abstenerse**
durante la gestión (art. 15). Y el **art. 14** veda por **tres años** actuar en el ente regulador
de una empresa o servicio en cuya privatización o concesión se tuvo intervención decisoria.

**El art. 17 es la consecuencia que más rinde, y no es disciplinaria.** Los actos alcanzados por
los arts. 13, 14 y 15 son **nulos de nulidad absoluta**, *"sin perjuicio de los derechos de
terceros de buena fe"*. Si se trata de un acto administrativo, queda viciado de nulidad absoluta —
y ahí se conecta con `administrativo-nacional.md` 46.3.1: un acto irregular **debe** revocarse en
sede administrativa, con el límite del art. 17 de la Ley 19.549 leído como lo lee `"Talleres
Navales"`.

**Declaraciones juradas (arts. 4, 5 y 8).** Se presentan **dentro de los treinta días hábiles** de
asumir, se actualizan **anualmente** y se presenta una última al cesar. El **art. 8 repite la
estructura del art. 8 de la Ley 27.499** de 49.5.1, y conviene verla como un patrón: quien no
presenta es **intimado en forma fehaciente** a hacerlo en **quince días**, y **el incumplimiento de
esa intimación** —no la omisión inicial— *"será considerado falta grave y dará lugar a la sanción
disciplinaria"*. La defensa vuelve a ser la misma: sin intimación previa no hay encuadre.

**Y una prohibición que se olvida (art. 18):** no se pueden recibir **regalos, obsequios o
donaciones** —cosas, servicios o bienes— con motivo o en ocasión de la función. Los de cortesía o
costumbre diplomática los reglamenta la autoridad de aplicación.

> **El régimen de declaraciones juradas se reescribió en 2013.** La **Ley 26.857 (B.O.
> 23/05/2013)** sustituyó el **art. 5** y derogó tres artículos; el **Decreto 862/2001** había
> sustituido otros dos. Toda doctrina anterior a 2013 sobre el alcance subjetivo de la declaración
> jurada se escribió sobre otro texto. Las notas están en el consolidado bajado.

`[REVISIÓN NORMATIVA REQUERIDA: este módulo recorre los arts. 1, 2, 4, 5, 8, 13 a 15, 17 y 18 de la Ley 25.188. El régimen de la Comisión Nacional de Ética Pública, los antecedentes penales y el resto del articulado NO están recorridos, y la reglamentación no está bajada]`

### 49.6 Lo que este módulo NO hace

- **No trae el estatuto de PBA ni los municipales.** El empleo público bonaerense tiene su propio
  régimen y **no está bajado**: no se le transpolan los plazos de esta ley.
- **No trae la reglamentación** de la Ley 25.164 ni el SINEP, de donde salen el escalafón, las
  categorías y el procedimiento sumarial concreto.
- **No cubre la negociación colectiva del sector público.** El texto de la Ley 24.185 **está
  bajado** en `fuentes/normas/ley-24185.txt`, pero este módulo no lo recorre, aunque el art. 3
  de la Ley 25.164 mande adecuar el régimen por esa vía.
- **No calcula.** No hay calculadora de empleo público, y la de LCT no se usa acá.

`[CONFIGURACIÓN INCOMPLETA: el empleado es público provincial o municipal y su estatuto no está en fuentes/ - sin ese texto no se resuelve la estabilidad ni la extinción: la Ley 25.164 es NACIONAL y no rige en las provincias]`

`[INSERTAR FALLO VERIFICADO: el efecto de la opción del art. 39 sigue sin precedente bajado - el contratado por tiempo determinado en relaciones prolongadas lo cubre 49.3.1 - aportar carátula, sala, expediente, fuero y año]`

### 49.7 Qué preguntar antes de contestar

1. **Si el empleador es nacional, provincial o municipal**, porque esta ley es sólo nacional.
2. **Si hay acto expreso de inclusión en la LCT**, que es lo único que devuelve el caso al régimen
   laboral común.
3. **Si el agente tiene estabilidad**, y cómo ingresó: por selección o por contrato del art. 9.
4. **Qué convenio sectorial rige** en el organismo, por el art. 3.
5. **Cuándo se notificó la sanción**, por los noventa días del art. 40.
6. **Si ya se optó por una vía**, porque la opción del art. 39 se ejerce una sola vez.
