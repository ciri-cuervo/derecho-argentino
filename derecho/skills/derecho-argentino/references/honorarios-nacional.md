# Honorarios en la justicia nacional y federal · Ley 27.423

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

**Esto no es PBA.** En la Provincia de Buenos Aires rige la **Ley 14.967** y la unidad es el
**jus**; acá rige la **Ley 27.423** y la unidad es la **UMA**. Son dos regímenes distintos con dos
unidades distintas, así que aplicar uno donde rige el otro **no da un error de redondeo: da un
número con cara de correcto**. Los honorarios de PBA están en
`honorarios-pba.md` 1.6.6, y la calculadora `honorarios_pba.py` es de
esa ley y sólo de esa.

**Primero se resuelve qué justicia interviene, y eso no lo dice la ciudad.** Si es nacional o
federal, este módulo — **incluidos los juzgados nacionales con asiento en CABA**. Si es la
justicia local de la Ciudad o la de una provincia, rige su propia ley arancelaria, y **ninguna
está cargada salvo la de PBA**.

## 37 · Arancel nacional y federal — Ley 27.423

### 37.1 Alcance, y la ley que derogó

Rige los honorarios de **abogados, procuradores y auxiliares de la Justicia** por su actividad
judicial, extrajudicial y administrativa en asuntos de competencia de la justicia nacional y
federal (art. 1). **Derogó la Ley 21.839 y su modificatoria** (art. 65). A las provincias y a CABA
las **invita a adherir** sólo en lo referente al límite de embargabilidad del art. 3 (art. 66): la
invitación no extiende el arancel.

> **El Decreto 1077/2017 (B.O. 21/12/2017) observó SIETE tramos de esta ley al promulgarla**, y el
> texto consolidado los trae anotados uno por uno. **Ninguno se cita como vigente:**
>
> | Qué se observó | Por qué importa |
> | --- | --- |
> | Un párrafo del **art. 5** | Toca la nulidad de la renuncia de honorarios |
> | Un párrafo del **art. 11** | Sobre el cobro contra la condenada en costas |
> | Texto de la tabla del **art. 19** | La parte relativa a mediación o conciliación |
> | Un inciso del **art. 25** | Sobre el perito que no intervino |
> | El **art. 47** entero | Regulaba incidentes y tercerías entre el 8% y el 25%, con un piso de cinco UMA |
> | El **art. 63** entero | **Sustituía los arts. 254 y 257 de la Ley 24.522**, o sea el régimen de honorarios del síndico concursal: esa reforma NO rige. Ver `concursos.md` 29 |
> | El **art. 64** entero | **La vigencia y la aplicación a procesos en curso** |
>
> **El último es el que más pesa:** decía que la ley se aplicaba a los procesos en curso sin
> regulación firme, así que **la regla de transición no surge del texto** y no se da por sabida.

`[REVISIÓN NORMATIVA REQUERIDA: el art. 64 de la Ley 27.423 está observado por el Decreto 1077/2017, así que la aplicación temporal del arancel a procesos iniciados bajo la Ley 21.839 no surge del texto. Verificar el criterio del fuero interviniente antes de afirmar qué ley rige un proceso en curso]`

### 37.2 La UMA — qué es y quién la publica

**Unidad de Medida Arancelaria**, instituida por el **art. 19**. Equivale al **tres por ciento
(3%) de la remuneración básica asignada al cargo de juez federal de primera instancia**. La
**Corte Suprema la suministra y publica mensualmente**, elimina las fracciones decimales e informa
su valor a las cámaras.

> **Hay otra UMA, se llama igual y la publica otro organismo.** El art. 20 de la **Ley 5.134 de
> CABA** instituye una unidad homónima para la **justicia local de la Ciudad**, cotejado contra
> `fuentes/normas/caba-ley-5134.txt`. Difieren en tres cosas:
>
> | | Nacional y federal, art. 19 Ley 27.423 | Local de CABA, art. 20 Ley 5.134 |
> | --- | --- | --- |
> | Porcentaje | **3%** | **1,5%** |
> | Base | remuneración **básica** de un juez **federal** de 1ª instancia | remuneración **total** de un juez de 1ª instancia **de la Ciudad**, o sea *"la suma de todos aquellos rubros, sea cual fuere su denominación, incluida la bonificación por antigüedad de cinco años"* |
> | Quién la publica | **la CSJN**, mensualmente | **el Consejo de la Magistratura de CABA**, mensualmente; el **CPACF** informa el valor a las Cámaras |
>
> **La tercera fila es la que más se paga:** buscar el valor de la UMA porteña en la página de la
> Corte devuelve un número que existe, es oficial y es de otra ley. El resultado sale expresado en
> «UMA» de todos modos y nada en él delata el error. Antes de convertir, resolver qué justicia
> interviene — 37.9 de este módulo y la puerta de `/derecho:honorarios`.

**Los valores están cargados:** `fuentes/datos/uma-csjn.csv` trae las vigencias desde el
01/10/2024, leídas de las resoluciones de la SGA. Se cargan **a mano** porque la consulta
oficial es un formulario y no una tabla, y por eso no hay descargador: la serie avanza cuando
alguien la carga, y `/derecho:estado` avisa cuando se quedó atrás. `uma_csjn.py --fecha` devuelve
el valor **y la resolución que lo fijó**; para una fecha anterior al arranque de la serie no
extrapola hacia atrás: emite `[CONFIGURACIÓN INCOMPLETA: ...]` y el valor se pide o se marca.
Hacia adelante aplica la última vigencia cargada, que es como rige una UMA: hasta que otra
resolución la cambie.

`[VERIFICAR MONTO ACTUALIZADO: valor de la UMA - lo publica la CSJN por resolución de su Secretaría General de Administración, art. 19 Ley 27.423, y se consulta en csjn.gov.ar/transparencia/uma. El archivo fuentes/datos/uma-csjn.csv trae las vigencias desde el 01/10/2024, leídas de las resoluciones de la SGA: el valor sale de correr scripts/uma_csjn.py --fecha, nunca de memoria. Para una fecha anterior a esa, el script se planta y el valor se pide o se marca]`

### 37.3 La regla que anula una regulación mal hecha (art. 51)

El art. 51, textual:

> *"La regulación de honorarios deberá contener, bajo pena de nulidad, el monto expresado en
> moneda de curso legal y la cantidad de UMA que éste representa a la fecha de la resolución."*

**Un solo número no alcanza: van los dos, y la omisión anula.**

**Y el pago cancela por la UMA, no por los pesos.** El art. 51 lo dice sin rodeos: el pago es
definitivo y cancelatorio **únicamente** si se abona la cantidad de pesos equivalente a las UMA de
la resolución **según su valor vigente al momento del pago**. En un contexto de precios móviles,
la diferencia entre el valor de la regulación y el del pago es el grueso del importe, y **es un
cálculo que se rehace, no se hereda del expediente**.

Es el mismo mecanismo que el art. 15 inc. d de la Ley 14.967 en PBA con el jus, y conviene tenerlo
presente al cruzar de un fuero al otro: **cambia la unidad, no la lógica**.

### 37.4 La escala del art. 21, y el piso que se olvida

En procesos **susceptibles de apreciación pecuniaria**, los honorarios por la defensa de cada
parte se fijan según la cuantía:

| Cuantía | Porcentaje |
| --- | --- |
| Hasta 15 UMA | 22% a 33% |
| De 16 a 45 UMA | 20% a 26% |
| De 46 a 90 UMA | 18% a 24% |
| De 91 a 150 UMA | 17% a 22% |
| De 151 a 450 UMA | 15% a 20% |
| De 451 a 750 UMA | 13% a 17% |
| De 751 UMA en adelante | 12% a 15% |

**El párrafo que se pasa por alto:** *"En ningún caso los honorarios podrán ser inferiores al
máximo del grado inmediato anterior de la escala, con más el incremento por aplicación al
excedente de la alícuota que corresponde al grado siguiente."* Aplicar el porcentaje del tramo
sobre el total, sin ese piso, da de menos en el borde de cada escalón.

**Litisconsorcio:** la regulación se hace **con relación al interés de cada litisconsorte**. En
jurisdicción voluntaria se considera que hay **una sola parte**.

**Auxiliares de la Justicia:** no menos del **5%** ni más del **10%** del monto del proceso, con
la salvedad de labores altamente complejas o extensas, que por auto fundado admiten un porcentaje
mayor. Los **peritos de parte y consultores técnicos** se rigen igual que los peritos de oficio,
salvo lo del art. 478 CPCCN.

**Sin apreciación pecuniaria** se aplican las pautas de valoración del **art. 16**: monto,
valor/motivo/extensión y calidad jurídica de la labor, complejidad y novedad, responsabilidad,
resultado obtenido, trascendencia de la resolución para futuros casos, y trascendencia económica y
moral para el interesado.

### 37.5 Cómo se determina la cuantía (arts. 22 y 23)

**Juicios por cobro de sumas de dinero** (art. 22): la cuantía es el **monto de la demanda o
reconvención**; si hay sentencia, el de la **liquidación que resulte de ella, actualizada por
intereses** si correspondiere; en transacción, el **monto de la transacción**.

**Si la demanda o reconvención se desestima íntegramente**, el valor del pleito es su importe,
actualizado por intereses al momento de la sentencia si correspondiere, **disminuido en un 30%** —
o, en procesos de monto indeterminado, según la pericia contable si existiere.

**Bienes inmuebles sin tasar en autos** (art. 23 inc. a): la **valuación fiscal al momento de la
regulación, incrementada en un 50%**. El profesional puede estimar otro valor, con traslado al
obligado al pago; si hay oposición, el juez designa perito tasador, y **las costas de esa pericia
las carga quien haya quedado más lejos del valor que fije el juez**.

### 37.6 Etapas (art. 29) y segunda instancia (art. 30)

**Tres etapas, cada una un tercio:**

1. La **demanda y contestación** en toda clase de juicios, y el escrito inicial en sucesiones y
   juicios semejantes.
2. Las **actuaciones de prueba** en juicios ordinarios y especiales, y las realizadas hasta la
   declaratoria de herederos inclusive.
3. Las **demás diligencias y trámites** hasta la terminación del proceso en primera instancia.

**Segunda o ulterior instancia** (art. 30): **30% a 35%** de lo que se fije para la primera. Y si
la sentencia recurrida se revoca o modifica, **el tribunal de alzada adecua de oficio** las
regulaciones de primera instancia según el nuevo resultado.

### 37.7 Procurador, pacto y cuotalitis

**Procurador: 40%** de lo que corresponda al abogado patrocinante (art. 20). **Si el abogado actúa
como apoderado sin patrocinio, percibe la asignación total** de ambos.

**Pacto de cuotalitis** (art. 6): por escrito, con tantos ejemplares como partes, antes o después
de iniciado el juicio, y **no puede exceder del 30% del resultado del pleito** —cualquiera sea el
número de pactos y de profesionales—, salvo que el profesional tome expresamente a su cargo los
gastos.

**La renuncia anticipada de honorarios y todo pacto que tienda a reducirlos son nulos** (art. 5).

### 37.8 Lo que este módulo NO hace

- **No regula.** No trae escala aplicada ni etapas calculadas: eso se hace leyendo los arts. 21
  y 29 de acá. La calculadora determinista de honorarios existe sólo para PBA.
- **Convertir sí convierte**: la cuenta del art. 51 —pesos a UMA a una fecha, y UMA a pesos a la
  del pago— la hace `scripts/uma_csjn.py` con la serie cargada. Fuera del tramo cargado se planta
  con `[CONFIGURACIÓN INCOMPLETA]` y dice dónde buscar el valor.
- **No resuelve la aplicación temporal** a procesos iniciados bajo la Ley 21.839: el art. 64 está
  observado y eso va con marcador.
- **No cubre las leyes arancelarias provinciales** salvo la de PBA, que está en
  `honorarios-pba.md` 1.6.6.

### 37.8.1 Una regulación tiene que decir por qué — "Puebla"

**CSJN, "Puebla, Julio César c/ EN - M Salud de la Nación y otros s/ amparo ley 16.986", Fallos
349:858, 20/08/2026.** Leído contra el documento. La cámara había reducido a **10 UMA en total**
los honorarios de un amparo. La Corte deja sin efecto esa decisión **por arbitrariedad**.

**La pregunta que la cámara no contestó, y que hay que contestar siempre:** si el proceso es o no
**susceptible de apreciación pecuniaria**. Sin eso *"la resolución apelada carece de una
fundamentación suficiente que permita considerarla una sentencia fundada en ley"*, porque de esa
respuesta dependen dos caminos incompatibles.

- **Si no tiene contenido patrimonial**, rige el **art. 48**: por amparo se aplican las pautas del
  art. 16 **"con un mínimo de veinte (20) UMA"**. Regular por debajo exige **declarar la
  inconstitucionalidad de la norma** o dar una argumentación plausible; no hacerlo es apartarse de
  la ley sin decirlo.
- **Si es susceptible de apreciación pecuniaria**, había que **indicarlo, enunciar la base
  regulatoria y aplicar la escala del art. 21** — *"lo que resultaba imprescindible para justificar
  el importe finalmente regulado [...] de modo tal que ello no se sustente exclusivamente en la
  mera voluntad de los magistrados"*.

**Y los mínimos son de orden público.** El art. 16 cierra diciendo que *"los jueces no podrán
apartarse de los mínimos establecidos en la presente ley, los cuales revisten carácter de orden
público"*.

**La nulidad del art. 15 tiene contenido propio.** La regulación debe fundarse y practicarse con
cita de la disposición aplicada **bajo pena de nulidad**, y *"la mera mención del articulado de
esta ley no será considerada fundamento válido"*. Enumerar las pautas del art. 16 sin explicar
cuáles pesaron es **fundamentación aparente**.

**Confirmado dos semanas después, y con un caso casi idéntico.** *"Martinuzzi, Luisa Raquel María
c/ OMINT S.A. de Servicios s/ amparo"*, CSJN, **CCF 009469/2018/3/RH002, 03/09/2026**, leído contra
el documento: la cámara había reducido a **14 UMA en total** los honorarios de un amparo, y la Corte
**dejó sin efecto con costas**. Agrega tres cosas al mismo estándar:

- **El incumplimiento se imputa al art. 15.** La cámara *"no explicó cuáles fueron los motivos
  relacionados con la ponderación de los trabajos"* que la llevaron a reducir, *"lo que, tal como
  prescribe inequívocamente la ley, de ningún modo puede considerarse suplido por la mera invocación
  de la norma"*.
- **El art. 48 se invocó y se citó en la resolución, y aun así se lo dejó de lado**: la cámara
  omitió explicitar el fundamento por el cual prescindió de aplicarlo, *"sin declarar su
  inconstitucionalidad ni elaborar argumentación plausible alguna"*.
- **Por qué la Corte entra en una cuestión de honorarios.** Son ajenas a la apelación extraordinaria
  y la arbitrariedad es de carácter **particularmente restringido**, *"ello reconoce excepción
  cuando la decisión carece de fundamentación válida que la sustente por basarse en afirmaciones
  dogmáticas"* (Fallos 325:1691; 327:1491; 328:3067; 330:1529, 1722 y 4207; 347:632), con afectación
  de los arts. 17 y 18 CN.

Viene **firmado digitalmente**, sin defecto de OCR: lo firman **Rosatti y Rosenkrantz**, y
**Lorenzetti** por su voto, con idéntico dispositivo.

*Cómo se usan los dos.* Son el precedente para apelar una regulación que baja del mínimo o que no
explica de dónde sale el número, y **"Martinuzzi" es el más reciente**: si hay que citar uno solo,
ése. **Ninguno resuelve el art. 51**: nada dicen del efecto cancelatorio por UMA al momento del pago.

`[INSERTAR FALLO VERIFICADO: el alcance del efecto cancelatorio por UMA al momento del pago -art. 51- sigue sin precedente bajado; la exigencia de fundar la regulación y el piso del art. 48 los cubre 37.8.1 - aportar carátula, sala, expediente, fuero y año]`

### 37.9 Qué preguntar antes de regular

1. **Si el juzgado es nacional o local**, que es la pregunta y no en qué ciudad queda. Nacional
   o federal manda a este módulo; PBA, a `honorarios-pba.md` 1.6.6; la justicia de la Ciudad o
   la de otra provincia, a su ley arancelaria, que no está cargada.
2. **Si hay regulación firme anterior**, por el art. 64 observado.
3. **La cuantía y cómo se determina** — arts. 22 y 23, que no siempre es el monto de la demanda.
4. **Qué etapas se cumplieron**, por el art. 29.
5. **Si hay litisconsorcio**, porque se regula por el interés de cada uno.
6. **Si el profesional fue patrocinante, apoderado o procurador**, por el art. 20.
7. **El valor de la UMA a las DOS fechas** —la de la resolución y la del pago—, que no se toman
   de memoria: las da `scripts/uma_csjn.py --fecha AAAA-MM-DD`, o no las da nadie.
