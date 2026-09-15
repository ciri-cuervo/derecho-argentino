# Cómputo de plazos

> Módulo de referencia de la skill `derecho-argentino`. La numeración de secciones es global y
> se mantiene igual que en el SKILL.md original: las remisiones cruzadas entre módulos siguen siendo
> válidas. Las reglas de integridad de la sección 2 rigen acá también.

---

## 8 · Cómputo de plazos

Nunca calcular sin identificar **fuero** y **tipo de plazo**.

> **Antes de contar hay que saber desde cuándo.** En PBA el momento en que una resolución
> queda notificada lo fija el reglamento del expediente digital, no la fecha de la
> providencia ni la de la lectura: la notificación electrónica se perfecciona **el martes o
> viernes inmediato posterior a la disponibilidad** de la cédula en el sistema, salvo urgencia
> justificada en la propia providencia. Ver **`notificaciones-pba.md` sección 22** antes de
> calcular cualquier vencimiento bonaerense — incluido el efecto del art. 124 sobre las
> presentaciones electrónicas (sección 22.5) y las caídas del sistema (22.6). Si falta la fecha de
notificación, emitir `[VACÍO PROBATORIO: ...]` y **no** calcular vencimiento.

### 8.1 Tipos de plazo

- **Hábiles judiciales** — **art. 156 CPCCN** y **art. 156 CPCCBA** (la numeración coincide;
  en el CPCCBA el art. 152 define días y horas hábiles y el art. 153 es la *habilitación* de
  días y horas inhábiles, que es otra cosa). El plazo corre desde la notificación, sin contar
  el día en que se practica ni los días inhábiles. Si el último día es inhábil, se traslada
  al primer hábil siguiente.
- **Hábiles administrativos** (art. 1 inc. e LNPA): son los días en que funciona la
  Administración. **No asumir que coinciden con los judiciales.**
- **Corridos** (art. 6 CCyCN): el cómputo empieza al día siguiente, hábil o no; sin traslado
  por vencimiento en inhábil salvo norma expresa.
- **Horas** (penal): hora a hora desde el momento exacto, incluida la hora de inicio; no se
  descuentan inhábiles; no hay plazo de gracia. Indicar fecha y hora exactas.
- **Meses o años** (arts. 6-7 CCyCN): de fecha a fecha; si el mes de vencimiento no tiene el
  día equivalente, vence el último día de ese mes.

### 8.2 Plazo de gracia — no es igual en los dos fueros

| Fuero | Norma | Plazo |
|---|---|---|
| Nacional | Art. 124 CPCCN | **Dos** primeras horas del despacho del día hábil inmediato |
| PBA | Art. 124 CPCCBA | **Cuatro** primeras horas del despacho del día hábil inmediato |

Son las primeras horas **de atención del tribunal**, no "las 2 de la madrugada". No lo prevén
el amparo federal, los plazos fijados en horas ni los plazos administrativos de la LNPA. En
el fuero laboral PBA la Ley 15.057 no lo regula, pero su art. 89 declara supletorio el
CPCCBA, lo que remite al art. 124. No declarar un plazo vencido mientras corra la gracia.

**En el expediente digital bonaerense su aplicación está discutida** y el reglamento no la
resuelve: ver `notificaciones-pba.md` sección 22.5 antes de darla por operativa o por
inoperante.

### 8.3 Ferias y feriados

Nacionales: acordada CSJN. **PBA: acordadas de la SCBA, que no coinciden necesariamente con
las nacionales.** Verificar las fechas del año en curso. Durante la feria los plazos están
suspendidos; la habilitación no es automática. Feriados trasladables (Ley 27.399): verificar
el día de la semana en el año del cómputo antes de descontarlos.

### 8.4 Suspensión por conciliación o mediación — los regímenes NO son equivalentes

| Régimen | Norma | Efecto |
|---|---|---|
| Mediación prejudicial nacional | Art. 18 Ley 26.589 | Suspende prescripción y caducidad durante **todo el procedimiento**; se reanuda a los **20 días** del acta de cierre. El dies a quo varía según sea por acuerdo de partes, por sorteo o a propuesta del requirente. |
| **Mediación prejudicial PBA** | **Art. 40 Ley 13.951** | **No suspende como la nacional.** La ley le asigna *carácter de intimación*, con los efectos del segundo párrafo del art. 3986 del Código Civil — norma derogada, hoy reconducida al **art. 2541 CCyCN: suspensión por interpelación fehaciente, por una sola vez y por seis meses**. |
| SECLO (laboral nacional) | Art. 7 Ley 24.635 | La presentación **suspende** *"por el término que establece el art. 257 de la ley de contrato de trabajo"*, que es de **seis meses como máximo**. El art. 257 LCT dice **interrumpirá**, no suspenderá, y la remisión crea el conflicto. **El plazo de 30 días desde la clausura NO está en la Ley 24.635**: ver `laboral.md` 5.6. |

Confundir el régimen bonaerense con el nacional puede dar por viva una acción prescripta.
Ante un cómputo de prescripción en PBA con mediación de por medio, emitir
`[VERIFICAR CRITERIO DEL FUERO: alcance de la suspensión del art. 40 Ley 13.951 - departamento judicial]`.

### 8.5 Plazos frecuentes

| Acto | Plazo | Norma |
|---|---|---|
| Apelación (Nación y PBA) | 5 días hábiles | Art. 244 CPCCN / art. 244 CPCCBA |
| Recurso extraordinario federal | 10 días hábiles | Art. 257 CPCCN |
| Queja por REF denegado | 5 días hábiles | **Art. 285 en función del art. 282** CPCCN |
| Traslado de la demanda, laboral nacional | 10 días hábiles | **Art. 68** Ley 18.345 (el art. 71 regula la *forma* de la contestación) |
| Apelación de interlocutorias, laboral nacional | 3 días hábiles | **Art. 117** Ley 18.345 (el art. 110 es el efecto diferido) |
| Apelación de sentencias definitivas, laboral nacional | 6 días hábiles | Art. 116 Ley 18.345 |
| Caducidad de instancia, laboral nacional | 6 meses (1ª instancia) / 3 meses (2ª) | Art. 46 Ley 18.345, texto art. 82 Ley 27.802 |
| Amparo federal | 15 días hábiles | Art. 2 inc. e Ley 16.986 |

> **Los diez días del REF se cuentan con el calendario del tribunal apelado, no con el de la
> Corte.** Es el error que se paga más caro, porque se descubre cuando ya venció. *"Vallejos,
> Julio César y otro c/ Hospital Interzonal Dr. José Penna y otros s/ daños y perjuicios"*,
> **Fallos 344:1785, 8/7/2021** — leído contra el documento, `fallos-csjn.md` 34.4. La Corte
> **desestimó la queja**: el plazo del art. 257 CPCCN *"se computa teniendo en cuenta los días
> hábiles para actuar ante el tribunal apelado, en cuyo estrado debe cumplirse con la actuación
> de que se trata"* (Fallos 212:85, 227:68, 254:305).
>
> **En la práctica bonaerense eso significa el calendario de la SCBA**: sus ferias, sus asuetos
> y sus suspensiones. En "Vallejos" fue decisivo — con la notificación del 13/3/2020 y el asueto
> por pandemia que suspendió plazos desde el 16/3 hasta el 6/5/2020, la presentación del
> 13/8/2020 llegó tarde, y **no se había invocado incompatibilidad** con las restricciones
> sanitarias.
>
> Y la otra mitad de la regla, que parece contradictoria y no lo es: **el régimen procesal del
> REF lo regulan exclusivamente las normas nacionales** (Fallos 334:896). O sea, el **plazo** es
> el del art. 257, y **los días hábiles** los pone el tribunal ante el que se presenta.

**Contencioso administrativo — art. 25 LNPA:** **180 días hábiles judiciales** para actos
notificados **desde el 9/7/2024** (texto art. 43 Ley 27.742); 90 días para actos anteriores.
No aplicar el plazo federal por analogía a **CABA** (90 días, art. 7 Ley 189) ni a **PBA**
(90 días, art. 18 Ley 12.008, texto Ley 13.101). Para PBA, el cómputo por inciso y todo lo que
lo condiciona están en `contencioso-pba.md` 26.6.

### 8.5 bis Caducidades y prescripciones de familia — se pierden solas

Cotejadas contra `fuentes/normas/ccycn-26994.txt`. Van acá y no en `familia.md` porque el
problema de estos plazos no es de fondo sino de cómputo: **son caducidades**, no
prescripciones, así que **no se suspenden ni se interrumpen** y no las alcanza la mediación de
8.4. El cliente que consulta tarde no tiene acción, y eso hay que decírselo en la primera
entrevista.

| Acción | Plazo | Desde | Norma |
|---|---|---|---|
| **Compensación económica · divorcio** | 6 meses, **caducidad** | la **sentencia de divorcio** | Art. 442, último párrafo |
| **Compensación económica · unión convivencial** | 6 meses, **caducidad** | **cualquiera de las causas de cese** del art. 523 | Art. 525, último párrafo |
| Atribución del uso de la vivienda · unión convivencial | tope de **2 años** de duración | el **cese de la convivencia** (art. 523) | Art. 526 |
| Impugnación de la filiación presumida por ley | **1 año**, caducidad | la **inscripción del nacimiento** o desde que se supo que el niño podría no ser hijo de quien la ley presume | Art. 590 |
| — la misma, ejercida **por el hijo** | **sin plazo** | — | Art. 590 |
| Negación de filiación presumida | **1 año**, caducidad | inscripción del nacimiento o conocimiento | Art. 591 |
| Impugnación del reconocimiento | **1 año** | haber **conocido el acto de reconocimiento** o desde que se supo | Art. 593 |
| — la misma, ejercida **por el hijo** | **sin plazo** | — | Art. 593 |
| Alimentos ya devengados | **2 años**, prescripción | cada período devengado | Art. 2562 inc. c |

**Los dos plazos de compensación económica no arrancan igual, y es el error más caro.** En el
matrimonio corre desde la **sentencia** de divorcio; en la unión convivencial, desde el **hecho
del cese**. Una pareja conviviente que se separó en marzo y consulta en noviembre ya no tiene
acción, aunque nadie haya dictado nada. Conviene fechar el cese por escrito en la primera
entrevista.

**El art. 2562 inc. c no dice "alimentos".** Dice "todo lo que se devenga por años o plazos
periódicos más cortos, excepto el reintegro de un capital en cuotas". Los alimentos entran por
ahí: **cada cuota prescribe a los dos años**, de modo que un reclamo por retroactivos recupera
sólo los dos últimos. El derecho a pedir alimentos no prescribe; lo que prescribe son las
cuotas ya devengadas.

**Las acciones de filiación del hijo no tienen plazo.** El art. 590 y el art. 593 lo dicen
expresamente: el hijo puede accionar **en cualquier tiempo**. Sólo caducan para los demás
legitimados. Antes de decirle a alguien que llegó tarde, hay que ver de qué lado está.

**Herederos (art. 590).** Si el legitimado activo fallece antes de vencer el plazo, sus
herederos pueden impugnar; para ellos la acción caduca **una vez cumplido el plazo que ya había
empezado a correr**, no uno nuevo.

Ninguno de estos plazos se suspende por la mediación previa: ver 8.4, y tener presente que en
PBA la Ley 13.951 no suspende la prescripción sino que produce el efecto de intimación del art.
2541 CCyCN — y sobre una **caducidad** no produce ni eso.

### 8.6 Verificación aritmética de cierre

Todo vencimiento que resulte de sumar días a una fecha se recorre sobre el calendario antes de
darlo: mes por mes, contando los días de cada uno, en vez de resolverlo como una cuenta. Los
meses de 28, 30 y 31 días y los años bisiestos son donde aparece la diferencia. **Al usuario le
llega el número ya recorrido, nunca el de la primera pasada**, y cuando el cómputo lo hizo
`scripts/plazos.py` se transcribe su salida, que ya trae la traza.

