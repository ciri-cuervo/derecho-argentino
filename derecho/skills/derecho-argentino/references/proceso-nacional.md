# Proceso civil y comercial de la Nación · CPCCN

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

Cotejado contra `fuentes/normas/cpccn-17454.txt`.

**Esto no es PBA.** El proceso bonaerense va por el CPCC de la Provincia y tiene sus módulos
propios: `sede-judicial-pba.md`, `notificaciones-pba.md`
y `parte.md`. **Los plazos y los recursos no se transpolan de una jurisdicción a la
otra**, y el error no avisa: el escrito entra igual y el plazo ya venció.

## 44 · Proceso nacional y federal

### 44.1 Los plazos son perentorios, y eso cambia todo lo demás

**Art. 155:** los plazos legales o judiciales **son perentorios**. Se pueden prorrogar sólo por
acuerdo de partes y respecto de actos determinados; cuando el Código no fija plazo, lo señala el
juez.

**Cómputo (art. 156):** corren **desde la notificación** y, si son comunes, **desde la última**.
**No se cuenta el día de la diligencia ni los días inhábiles.**

**Suspensión convencional (art. 157):** los apoderados **no pueden acordar una suspensión mayor de
veinte días** sin acreditar la conformidad de sus mandantes. La abreviación sí puede pactarse por
escrito.

El cómputo se hace con `scripts/plazos.py`, que conoce las ferias y los feriados trasladables — ver
`plazos.md` 8.

### 44.2 Los plazos que deciden un expediente

| Acto | Plazo | Artículo |
| --- | --- | --- |
| Contestar la demanda, proceso ordinario | **15 días** | art. 338 |
| Contestar cuando la demandada es la Nación, una provincia o una municipalidad | **plazo ampliado** por el mismo artículo | art. 338 |
| **Apelar** | **5 días**, y el recurso **puede fundarse al interponerlo** | art. 244 |
| Caducidad de instancia, primera o única | **6 meses** | art. 310 inc. 1 |
| Caducidad en segunda o tercera instancia, sumarísimo, ejecutivo, ejecuciones especiales e incidentes | **3 meses** | art. 310 inc. 2 |

**Dos cosas del art. 244 que se pasan por alto:** *"Toda regulación de honorarios será apelable"* —
no hace falta discutir si causa gravamen irreparable —, y el recurso **puede ir fundado desde el
mismo escrito**, lo que en la práctica conviene cuando el plazo para expresar agravios es incierto.

**Y la caducidad del art. 310 es el riesgo silencioso del expediente dormido.** Seis meses en
primera instancia, y sólo tres en las instancias superiores y en los procesos abreviados: el plazo
se acorta justo donde el expediente suele quedar quieto.

**Acá se declara de oficio y sin trámite previo.** El art. 316 la declara *"sin otro trámite que
la comprobación del vencimiento"*, y el art. 315 sustancia el pedido *"únicamente con un traslado
a la parte contraria"*. **En PBA no es así**: el art. 315 del CPCCBA exige intimación previa por
única vez y cinco días para manifestar la intención de continuar, y el 316 condiciona la
declaración de oficio a esa misma intimación — `proceso-pba.md` 58.4. Dar por perdida una
instancia bonaerense con este régimen es el error que ese módulo vigila.

### 44.3 Qué se puede apelar

**Art. 242:** sólo la sentencia definitiva, las interlocutorias y **las providencias simples que
causen un gravamen que no pueda repararse en la sentencia definitiva**. El artículo fija además un
límite por monto para la inapelabilidad, que hay que leer en el texto antes de invocarlo.

`[VERIFICAR MONTO ACTUALIZADO: el límite de inapelabilidad por monto del art. 242 CPCCN está expresado en pesos y se actualiza por acordada de la CSJN. No se transcribe el número del texto consolidado sin cotejar la acordada vigente]`

### 44.4 Excepciones previas: la lista es cerrada

**Art. 347:** *"Sólo se admitirán como previas las siguientes excepciones"* — incompetencia, falta
de personería, **falta de legitimación cuando fuere manifiesta**, y las demás que el artículo
enumera. **Que la lista sea cerrada es el dato operativo**: una defensa que no esté ahí va en la
contestación, no como previa.

**Y la legitimación sólo va como previa si es manifiesta.** Si no lo es, el planteo se difiere para
la sentencia — el propio inciso lo dice.

### 44.5 La carga de contestar (art. 356)

El demandado debe **reconocer o negar categóricamente cada hecho**, la autenticidad de los
documentos que se le atribuyen y la recepción de las cartas y telegramas dirigidos a él. **La
negativa genérica no cumple la carga**, y el silencio o la respuesta evasiva pueden valer como
reconocimiento. Es lo que hace que la contestación se escriba hecho por hecho.

Para el telegrama laboral y su cruce, ver `telegramas.md` 25.

### 44.6 Medidas cautelares

**Se piden antes o después de la demanda** (art. 195), y el escrito debe expresar **el derecho que
se pretende asegurar, la medida, la disposición legal en que se funda** y el cumplimiento de los
requisitos de la que se pide.

**Se decretan y cumplen sin audiencia de la otra parte** (art. 198), y **ningún incidente del
destinatario detiene su cumplimiento**. Si no tomó conocimiento al ejecutarse, se le notifica
personalmente.

### 44.7 Ejecución de sentencia

**Art. 499:** consentida o ejecutoriada la sentencia y vencido el plazo de cumplimiento, se ejecuta
**a instancia de parte**, y **puede ejecutarse parcialmente**. El desarrollo del trámite de
ejecución, con su cruce bonaerense, está en `ejecucion.md` 21.

### 44.8 Lo que este módulo NO hace

- **No cubre el proceso de PBA.** Para eso está `proceso-pba.md` 58, que es su espejo, y para el fuero laboral bonaerense `sede-judicial-pba.md` y `notificaciones-pba.md`.
- **No trae el régimen de notificaciones electrónicas de la justicia nacional**, que sale de
  acordadas de la CSJN y no está cargado.
- **No cubre la prueba en detalle** —la pericial tiene módulo propio, `prueba-pericial.md` 20— ni
  el recurso extraordinario federal, que se rige por acordada.
- **No cubre el proceso laboral nacional**, que va por la Ley 18.345.
- **No calcula.** El cómputo de plazos lo hace `scripts/plazos.py`.

### 44.8.1 Qué acto interrumpe la caducidad — el test de la Corte

**CSJN, "Editorial El Atlántico S.A.I.C. s/ concurso preventivo s/ incidente de revisión por
AFIP", Fallos 329:1936, 30/05/2006.** Leído contra el documento. Confirma la caducidad declarada.

**El test, y es el que hay que aplicar acto por acto.** Reviste carácter de actividad procesal
idónea para impulsar el procedimiento **"únicamente la que, cumplida por las partes, el órgano
jurisdiccional o sus auxiliares, resulta adecuada a la etapa procesal en la que se la realice para
hacer avanzar el proceso hasta la sentencia"** (Fallos 308:967 y 313:548). Son tres condiciones
juntas: **quién** lo hace, que sea **adecuada a la etapa** y que **haga avanzar** hacia la
sentencia.

**La aplicación concreta que más se discute.** La presentación de un **nuevo apoderado** y la
constitución de un **nuevo domicilio** *"no configura una actividad procesal idónea"*, porque
*"hace únicamente al interés de la parte y no constituye impulso alguno del curso del proceso"*. Y
**tampoco lo son la providencia que despacha ese escrito ni su notificación**: si el acto no
impulsa, lo que se deriva de él tampoco.

*Cómo se usa.* Contra la caducidad, no alcanza con mostrar movimiento en el expediente: hay que
mostrar un acto que empuje hacia la sentencia en la etapa en que se está. A favor, sirve para
descartar como interruptivos los actos de mera gestión propia y su despacho.

`[INSERTAR FALLO VERIFICADO: el estándar de «legitimación manifiesta» del art. 347 inc. 3 sigue sin precedente bajado - los actos que interrumpen la caducidad del art. 310 los cubre 44.8.1 - aportar carátula, sala, expediente, fuero y año]`

### 44.9 Qué preguntar antes de contestar

1. **En qué jurisdicción tramita**, antes que cualquier plazo: nacional o PBA cambian los números.
2. **Cuándo se notificó**, y si el plazo es común, porque corre desde la última.
3. **En qué instancia está**, por la caducidad de seis o tres meses.
4. **Si la contraria es el Estado nacional, provincial o municipal**, por el plazo ampliado del
   art. 338.
5. **Qué clase de resolución se quiere apelar**, por el art. 242.
6. **Si el expediente estuvo parado**, y desde cuándo.
