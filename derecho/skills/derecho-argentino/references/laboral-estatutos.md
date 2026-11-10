# Laboral · los estatutos que desplazan la liquidación de la LCT

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

**Salió de `laboral.md` y conserva su numeración** —5.17 quater, 5.17 quinquies y 5.17 sexies—,
que es global y estable: quien viene de una remisión llega igual.

**El corte es por materia.** Acá van los regímenes con estatuto propio —trabajo agrario, personal
de casas particulares, construcción, viajantes de comercio y encargados de edificio—, que traen
otro preaviso, otra indemnización o un fondo en su lugar, y que `liquidacion_lct.py` no liquida.
Lo común a todo contrato —régimen por fecha del acto extintivo, art. 245, intereses, prescripción,
jornada— sigue en `laboral.md`, y la LCT entra a cada estatuto por la puerta que él mismo abre.

## 5 · Laboral — estatutos especiales

### 5.17 quater Trabajo agrario — Ley 26.727, y por qué no se resuelve con la LCT sola

Cotejada contra `fuentes/normas/ley-26727.txt`. **Es un estatuto especial, no una exclusión.**
Ahí está la diferencia con el empleo público de `laboral.md` 5.1: el art. 2 inc. b manda aplicar la **Ley
20.744** *"en todo lo que resulte compatible y no se oponga al régimen jurídico específico"*. O
sea que la LCT **sí rige**, supletoriamente, y lo que hay que verificar en cada instituto es si la
26.727 dispuso otra cosa.

**A quién alcanza y a quién no.** Hay contrato de trabajo agrario cuando se prestan servicios **en
el ámbito rural** para tareas propias de la actividad agraria (art. 11). El **art. 3** excluye al
personal afectado *"exclusiva o principalmente a actividades industriales, comerciales, turísticas,
de transporte o servicios"* **aunque trabaje en un establecimiento mixto agrario-industrial**, y a
quien fue contratado para tareas ajenas a la actividad agraria. **La discusión de encuadre es
fáctica**: qué hacía la persona, no qué figura el establecimiento.

**Dos modalidades, y la segunda tiene una indemnización propia.**

| | **Permanente de prestación continua (art. 16)** | **Temporario (art. 17)** |
| --- | --- | --- |
| Cuándo | **Es la regla**: se presume, salvo los casos que la ley prevé expresamente | Necesidades **cíclicas o estacionales**, procesos temporales, **ferias y remates de hacienda**, y tareas ocasionales, accidentales o supletorias |
| Extinción | Por el **Título XII de la LCT** | Concluye con la tarea |

**El art. 20 es el que más se pasa por alto.** Al concluir la relación, el trabajador temporario
debe percibir, **además del SAC proporcional**, una **indemnización sustitutiva de vacaciones
equivalente al diez por ciento (10%) del total de las remuneraciones devengadas**. No es el
régimen de vacaciones de la LCT: es un porcentaje sobre lo devengado, y se liquida siempre.

**Solidaridad (art. 12, texto Ley 27.802).** Los trabajadores son **empleados directos de quien
registre la relación**, y **la empresa usuaria responde solidariamente** por las obligaciones
laborales y de la seguridad social. Es la vía para el trabajo provisto por terceros, frecuente en
cosecha.

> **El régimen se movió dos veces y es lo primero que hay que mirar.** De la **Ley 26.727**, la
> **Ley 27.802 (B.O. 06/03/2026)** derogó el **art. 13**, el **art. 18** y el **art. 21**, y dio
> texto nuevo al **art. 12**, al **art. 16**, al **art. 17**, al **art. 32** y al **art. 34**; la
> **Ley 27.742 (B.O. 08/07/2024)** derogó el **art. 15** y sustituyó el **art. 69**. **Toda
> doctrina anterior a marzo de 2026 sobre este régimen se escribió sobre otros artículos**, y un
> escrito que cite un artículo derogado se cae solo. Las notas de cada uno están en el consolidado
> bajado.

**La remuneración no sale de un mínimo legal (art. 32, texto Ley 27.802):** se acuerda por
negociación colectiva conforme las Leyes 14.250 y 23.546, **con homologación posterior**. Sin
acuerdo vigente para la actividad, se aplican las generales.

**Las multas por no registrar al trabajador rural (art. 15 de la Ley 25.191, texto art. 14 de la
Ley 27.826).** No inscribirse en el RENATRE y la falta u omisión de registración del contrato se
sancionan por trabajador afectado, o por establecimiento si no se lo puede individualizar, en tres
escalas: declaración **inconsistente**, de $120.000 a $187.500; declaración **falsa**, de $375.000 a
$1.500.000; **omisión total**, de $1.500.000 a $7.500.000. La reincidencia en cinco años puede
subir el tope de las muy graves hasta un 50%. Esos montos rigen para las infracciones **constatadas
desde el 09/10/2026** (art. 16 de la Ley 27.826). Desde el 01/01/2027 se ajustan cada año por UVA y
el RENATRE publica la tabla; **para cancelar se toma el monto vigente al cancelar** (art. 15 bis).
Cotejado contra `fuentes/normas/ley-25191.txt`.

`[VERIFICAR MONTO ACTUALIZADO: escalas del art. 15 de la Ley 25.191 para actas labradas desde el 01/01/2027 - el art. 15 bis las ajusta por UVA y el RENATRE publica la tabla de cada año]`

`[REVISIÓN NORMATIVA REQUERIDA: este módulo recorre el Título I -ámbito y fuentes-, el III -modalidades- y los arts. 12, 20 y 32. Los Títulos IV a XIII -vivienda y alimentación, jornada, licencias, trabajo adolescente, seguridad social y los órganos tripartitos, incluido el RENATRE- NO están recorridos, y ahí viven obligaciones propias del empleador rural. De la Ley 25.191 —libreta y RENATRE— este módulo recorre sólo los arts. 15 y 15 bis]`

### 5.17 quinquies Personal de casas particulares — Ley 26.844, y por qué `liquidacion_lct.py` no sirve acá

Cotejada contra `fuentes/normas/ley-26844.txt`, texto actualizado con la **Ley 27.802**. **Es un
estatuto especial, como el agrario de 5.17 quater, y la LCT entra sólo por la puerta que el
propio estatuto abre**: el art. 72 inc. a reescribió el **art. 2 inc. b LCT**, que hoy excluye al
personal de casas particulares *"sin perjuicio que las disposiciones de la presente ley serán de
aplicación en todo lo que resulte compatible y no se oponga a la naturaleza y modalidades propias
del régimen específico o cuando así se lo disponga expresamente"*. Y el estatuto lo dispone
expresamente en tres lugares: jubilación (arts. 252 y 253 LCT, por el art. 46 inc. d),
incapacidad sobreviniente (art. 212 LCT, por el art. 46 inc. j) e intereses (art. 276 LCT, por el
art. 70).

**A quién alcanza (arts. 1 y 2).** Al trabajo en casas particulares o en el ámbito de la vida
familiar que **no importe lucro o beneficio económico directo para el empleador, cualquiera fuere
la cantidad de horas diarias o de jornadas semanales**: limpieza, mantenimiento, tareas típicas
del hogar, asistencia y acompañamiento, y **cuidado no terapéutico** de personas enfermas o con
discapacidad. Tres modalidades: **sin retiro**, **con retiro para un único empleador** y **con
retiro para distintos empleadores**. No hay mínimo de horas para entrar: la trabajadora de una
vez por semana está adentro.

**A quién no (art. 3).** Contratadas por **personas jurídicas**; parientes del dueño de casa; el
cuidado **exclusivamente terapéutico** o que exija habilitación profesional; el chofer; quien
conviva con el personal sin prestar servicios; el personal de **consorcios, clubes de campo y
barrios privados** para tareas en las unidades. Y la exclusión que decide encuadres: quien además
de las tareas domésticas presta **otros servicios en actividades o empresas del empleador**, con
cualquier periodicidad, donde **se presume una única relación laboral ajena a este régimen**
(inc. f): esa persona es un trabajador de la LCT.

**Lo que no se aplica, y es lo que más se reclama mal (art. 72 inc. d, texto Decreto 90/2023).**
*"No serán aplicables al presente régimen las disposiciones de la Ley Nº 24.013, salvo su TÍTULO
IV"*, ni las **Leyes 25.323 y 25.345**. Las multas por falta o deficiencia de registro de esos
cuerpos **no proceden** en casas particulares. El recargo propio del régimen era el **art. 50**
—la duplicación por relación no registrada— y **está derogado**: por el art. 58 del DNU 70/2023
primero, y por el **art. 99 de la Ley 27.742** (B.O. 08/07/2024, vigente desde el 09/07/2024)
después, según el consolidado. Para un despido posterior a esa fecha no hay agravamiento por falta
de registro, y el art. 73, que le daba 180 días al empleador para regularizar, quedó sin objeto.
Para el tramo del DNU rige la advertencia de `laboral.md` 5.1.

**Contrato y prueba (arts. 6 y 7).** Libertad de formas, presunción de tiempo indeterminado, y
**período de prueba de seis meses** —texto según **art. 107 de la Ley 27.802**, vigente desde el
**06/03/2026**— durante el cual cualquiera extingue sin causa y sin indemnización; un mismo
empleado no puede ser puesto a prueba dos veces.
`[REVISIÓN NORMATIVA REQUERIDA: período de prueba de la Ley 26.844 para ingresos anteriores al 06/03/2026 - el consolidado sólo trae el texto de la Ley 27.802 y el anterior no está cargado]`

**Jornada y descansos (arts. 14, 15 y 25; el art. 14 con texto Ley 27.802).** Ocho horas diarias
o 48 semanales, con distribución desigual que no pase de nueve por día; descanso semanal de **35
horas corridas desde el sábado a las 13**; para el personal con retiro de un mismo empleador,
**pausa de doce horas** entre jornadas. Sin retiro, además: reposo nocturno de **nueve horas**,
descanso de **tres horas** entre las tareas de la mañana y las de la tarde, y habitación amueblada
e higiénica de uso exclusivo. Horas extras con recargo del **50%**, y del **100%** los sábados
después de las 13, domingos y feriados. El art. 14.1 inc. e obliga al empleador a contratar el
**seguro de riesgos del trabajo**: ver el art. 74 más abajo.

**Remuneración, SAC y vacaciones.** El salario mínimo por categoría lo fija la **Comisión
Nacional de Trabajo en Casas Particulares** (art. 18) y no se cita de memoria:
`[VERIFICAR MONTO ACTUALIZADO: salario mínimo por categoría y modalidad fijado por la CNTCP a la fecha del período reclamado - resoluciones de la Comisión, no cargadas]`.
El recibo es **electrónico, emitido por el sistema de ARCA** (art. 20, texto Ley 27.802). SAC: 50%
de la mayor remuneración mensual del semestre (art. 26). Vacaciones de **14, 21, 28 y 35 días
corridos** según la antigüedad supere seis meses, cinco, diez y veinte años (art. 29).

**Enfermedad y maternidad.** Enfermedad inculpable paga hasta **tres meses** al año con antigüedad
menor de cinco años y **seis** si es mayor (art. 34). Licencia por maternidad de **45 y 45 días**,
con opción de reducir la anterior al parto a 30 (art. 39); presunción de despido por embarazo o
maternidad cuando se dispone *"dentro del plazo de siete (7) meses y medio (1/2) anteriores o
posteriores a la fecha del parto"*, con la comunicación cumplida (art. 40); indemnización especial de **un año de remuneraciones**, acumulable a la del
despido, y la misma por matrimonio en los tres meses anteriores o seis posteriores (art. 41).

**Preaviso (arts. 42 a 44).** Lo debe el trabajador con **diez días**; el empleador con **diez**
si la antigüedad es menor de un año y **treinta** si es mayor. Los plazos **corren desde el primer
día del mes siguiente** a la notificación, y el despido sin preaviso en fecha que no es fin de mes
suma la **integración del mes**. Son plazos distintos de los del art. 231 LCT, y por eso la
calculadora de la LCT no sirve.

**Extinción e indemnización (arts. 46 a 49).** El mutuo acuerdo **sólo ante autoridad judicial o
administrativa**; la renuncia por telegrama gratuito o ante la autoridad; el abandono exige
intimación fehaciente por un plazo **nunca inferior a dos días hábiles**; muerte del trabajador y
**muerte del empleador**, 50% de la indemnización del art. 48, y si el servicio sigue para la
familia más de 30 días la relación continúa con su antigüedad. La indemnización del **art. 48** es
un mes de sueldo por año o fracción mayor de tres meses sobre la mejor remuneración mensual,
normal y habitual del último año, con piso de un mes: **el texto no trae tope**, y el del art.
245 LCT es de otro régimen. El despido indirecto (art. 49) da derecho a los arts. 43, 44 y 48. El
personal sin retiro tiene **cinco días** para desocupar la habitación (art. 47).

**No hay calculadora para este régimen.** `liquidacion_lct.py` liquida la LCT, con su preaviso,
su integración y su base; acá los tres son otros. La liquidación se arma a mano con los arts. 42
a 44 y 48, con el bloque de datos tomados por delante y la verificación aritmética de cierre de
`plazos.md` 8.6, y se dice que salió sin script.

**Prescripción e intereses (arts. 69 y 70).** Dos años, de orden público; el reclamo ante la
autoridad administrativa **interrumpe** mientras dure, y la conciliación del art. 53 **suspende**
por el plazo del conciliador. Los intereses van por el **art. 276 LCT** y los arts. 277 y 278,
más el **art. 55 de la Ley 27.802** (art. 70, texto Ley 27.802): rige lo de `laboral.md` 5.5 tal cual.

**Dónde se litiga, y acá la jurisdicción decide todo (arts. 51 a 61 y 68).** El Título XII crea
el **Tribunal de Trabajo para el Personal de Casas Particulares**, organismo del Ministerio de
Trabajo, **competente sólo para las relaciones desenvueltas en la Capital Federal** (art. 51), y
el art. 68 lo excluye del alcance nacional de la ley *"salvo para aquellas provincias que decidan
adherir"*. En esa sede la instancia previa es la **audiencia del art. 53** ante un conciliador
del propio servicio, con diez días hábiles para lograr acuerdo, y no la de la Ley 24.635, cuyo
art. 1 alcanza los reclamos de competencia de la Justicia Nacional del Trabajo; la resolución del
Tribunal se apela en **seis días, con recurso fundado**, ante el Juzgado Nacional de Primera
Instancia del Trabajo que sortee la Cámara (art. 56), y ahí se ejecuta (art. 59). Patrocinio
letrado obligatorio (art. 54), gratuidad en sede administrativa (art. 61), y si la relación no
estaba registrada el expediente va a ARCA para la determinación de la deuda previsional (art.
58). **En la Provincia de Buenos Aires el Título XII no rige por sí**: el conflicto es una
controversia individual de trabajo del art. 2 inc. a de la Ley 11.653 o de la Ley 15.057, según
cuál gobierne la causa por 1.6.1.
`[VERIFICAR VIGENCIA: si la Provincia de Buenos Aires adhirió al régimen procesal del Título XII de la Ley 26.844 -art. 68-; sin adhesión, la vía es el tribunal del trabajo de la Ley 11.653 o el juzgado de la Ley 15.057, y la instancia previa es la de esa ley]`

**Riesgos del trabajo y seguridad social (arts. 72 inc. e y 74).** La incorporación al régimen
de las Leyes 24.557 y 26.773 es *"en el modo y condiciones que se establezcan por vía
reglamentaria"*, gradual, y el aporte es el del **Título XVIII de la Ley 25.239**: el régimen
sustantivo está en `laboral-riesgos.md` 5.8, y lo que falta cargar es la reglamentación.
`[REVISIÓN NORMATIVA REQUERIDA: reglamentación de la Ley 26.844 -Decreto 467/2014- y las resoluciones de la SRT sobre cobertura de riesgos del personal de casas particulares, sin descargar]`

`[REVISIÓN NORMATIVA REQUERIDA: este bloque recorre los Títulos I, III, V a XII y XIV de la Ley 26.844 -ámbito, deberes, jornada, remuneración, licencias, preaviso, extinción, indemnización, tribunal y disposiciones finales-. El Título II -trabajo adolescente-, el IV -libreta y registro-, el XIII -la CNTCP- y las resoluciones de la Comisión sobre categorías y salarios NO están recorridos]`

### 5.17 sexies Tres estatutos que desplazan la liquidación de la LCT — construcción, viajantes y encargados de edificio

Cotejados contra `fuentes/normas/ley-22250.txt`, `fuentes/normas/ley-14546.txt` y
`fuentes/normas/ley-12981.txt`. Como el agrario y el de casas particulares, son regímenes
especiales: **la LCT entra en lo compatible, y en lo que cada estatuto regula manda el estatuto.**
Los tres cambian lo que `liquidacion_lct.py` calcula, así que **no se corre**: se liquida a mano
con el bloque de datos por delante y la verificación aritmética de cierre de `plazos.md` 8.6.

**Construcción — Ley 22.250.** Alcanza al empleador que ejecuta obras de ingeniería o
arquitectura y a las industrias complementarias por el personal afectado a obra, y al trabajador
de obra, talleres y depósitos, cualquiera sea la forma de contratación (art. 1); **excluye** al
personal de dirección, administrativo, técnico, profesional, jerárquico y de supervisión, al
propietario que construye su propia vivienda y a la Administración pública (art. 2). El empleador
y el trabajador se inscriben en el **Registro Nacional de la Industria de la Construcción** dentro
de los quince días hábiles (art. 3), y la **Libreta de Aportes** se entrega en cinco días hábiles
desde el ingreso (art. 13). El corazón es el **Fondo de Cese Laboral** (art. 15): aporte mensual
del empleador, **doce por ciento** de la remuneración el primer año y **ocho por ciento** después,
depositado en cuenta bancaria a nombre del trabajador, **inembargable e irrenunciable**, que
*"reemplaza al régimen de preaviso y despido contemplados por la Ley de Contrato de Trabajo"*:
**no hay art. 245 ni art. 232**, cualquiera sea la causa del cese. Al cesar, la parte que rescinde
lo comunica fehacientemente y el empleador entrega la libreta con los depósitos acreditados
**dentro de las cuarenta y ocho horas** (art. 17); si no lo hace hay **mora automática**, y con
intimación por **dos días hábiles** nace una indemnización judicial de **treinta a noventa días de
retribución**, más **treinta días** si además no lo había inscripto (art. 18). Salario atrasado o
insuficiente: intimación en **diez días hábiles** desde que debió pagarse y, si no regulariza en
**tres**, **el doble** de lo adeudado, haya o no rescisión (art. 19). Enfermedad inculpable, tres o
seis meses según la antigüedad supere cinco años (art. 21). Quien contrata subcontratistas **no
inscriptos** responde **solidariamente** por esa sola omisión (art. 32). Es de orden público y
**excluye a la LCT en lo que regula**, que se aplica en lo demás (art. 35).
`[VERIFICAR MONTO ACTUALIZADO: escala salarial de la UOCRA para la categoría, zona y período - las retribuciones del art. 19 salen del convenio, no de la ley]`

**Viajantes de comercio — Ley 14.546.** Es viajante quien, exclusivo o no, hace de ello su
actividad habitual y concierta negocios para uno o más comerciantes o industriales por una
remuneración (art. 1); la ley enumera los nombres que se les da y **presume la dependencia** con
acreditar alguno de seis indicios: vende a nombre del principal, a sus precios, cobra sueldo,
viático o comisión, actúa personal y habitualmente, en zona determinable, y **el riesgo de las
operaciones es del empleador** (art. 2). La remuneración es **en todo o en parte a comisión**
sobre las ventas, y los viáticos y gastos de movilidad la integran (art. 7), salvo los viáticos
con comprobante que el art. 105 LCT excluye. La comisión se devenga sobre toda nota de venta
**aceptada**, y **se tiene por aceptada la que no se rechaza por escrito en quince días** —treinta
si el viajante opera fuera de la plaza del empleador—; la inejecución por voluntad del cliente no
la hace perder, y las comisiones se liquidan mensualmente (art. 5). **Comisión indirecta**: la
operación concertada sin el viajante con un cliente de su zona o de su nómina le devenga la misma
tasa (art. 6). El cambio o la reducción de zona exige **conformidad expresa** y garantía del
volumen de remuneraciones (art. 9). El empleador lleva un **libro especial rubricado** con
ingreso, remuneración, zona, notas de venta y comisiones (art. 10), y **la carga de la prueba se
invierte**: contra la declaración jurada del viajante sobre lo que debió constar en el libro, y en
toda controversia sobre remuneraciones, prueba el empleador (art. 11). Descanso de **un día y medio
por cada semana de gira** fuera de la plaza (art. 13). Y la que decide la liquidación:
**indemnización por clientela**, después de un año de contrato, del **veinticinco por ciento de lo
que hubiera correspondido por despido injustificado**, *"cualquiera sea el motivo determinante de
la disolución"*, acumulable a las indemnizaciones del despido (art. 14). Orden público, y el art. 4
fija la **prescripción en cinco años**:
`[VERIFICAR CRITERIO DEL FUERO: si la prescripción quinquenal del art. 4 de la Ley 14.546 subsiste frente a los dos años del art. 256 LCT, posterior y general - sin fallo cargado]`.
Las remisiones del texto al Código de Comercio y a las Leyes 9.688, 11.719 y 14.455 están
**derogadas**, y el consolidado lo anota artículo por artículo.

> **La Ley 14.546 entera se deroga el 01/01/2027.** Art. 198 de la Ley 27.802: *"Derógase la ley
> 14.546 y sus modificatorias, a partir del 1º de enero de 2027."* Hasta el 31/12/2026 rige todo lo
> de arriba. La Ley 27.802 no trae un régimen que la reemplace, y el consolidado de InfoLEG,
> vuelto a bajar el 10/11/2026, todavía no anota la derogación: leer la 14.546 sola no lo avisa.

`[VERIFICAR VIGENCIA: régimen del viajante de comercio desde el 01/01/2027 - el art. 198 de la Ley 27.802 deroga la Ley 14.546 sin régimen sustituto; para una relación vigente a esa fecha, determinar qué rige la comisión, la indemnización por clientela del art. 14 y la prescripción, y si hay derechos ya devengados]`

**Encargados de casas de renta — Ley 12.981.** Rige a los empleados y obreros de edificios
destinados a producir renta y, por la Ley 14.095, a los de **propiedad horizontal** (art. 1); es
encargado quien cuida y vigila el inmueble habitual y exclusivamente por cuenta del propietario, y
se asimilan ayudantes, ascensoristas y peones permanentes (art. 2). Los beneficios del art. 3
(texto Ley 21.239) tienen medidas propias: descanso de **doce horas** entre jornadas y **cuatro
horas** intermedio, semanal de **treinta y cinco horas desde el sábado a las 13**, y vacaciones
**en días hábiles** —doce, veinte, veinticuatro y veintiocho según la antigüedad supere cinco,
diez y veinte años— entre el 1 de octubre y el 30 de abril, con **suplente pago por el empleador**
durante el descanso y las vacaciones, y el Título V de la LCT supletorio. El trabajador **preavisa
su renuncia con treinta días** (art. 4), y **la renuncia es nula si no se formula personalmente
ante la autoridad de aplicación** (art. 5 in fine). Las **causas de cesantía son taxativas** (art.
5): condena por delito, abandono o desobediencias reiteradas en los últimos seis meses, enfermedad
contagiosa crónica con indemnización, daño por dolo o culpa grave. Con más de **sesenta días** de
antigüedad hay **estabilidad** (art. 6), y el despido sin esas causas —o por demolición o
expropiación— paga **tres meses de sueldo de preaviso**, comunicado por telegrama colacionado,
**más un mes por cada año o fracción** de antigüedad; la venta del edificio o la muerte del
propietario no extinguen la relación. Enfermedad inculpable paga tres o seis meses con derecho a
seguir en la vivienda, y el suplente que reemplaza al titular más de un año después de esos plazos
**queda confirmado como efectivo** (art. 9). Vivienda higiénica o complemento salarial (art. 13),
libreta de trabajo (arts. 14 a 18), orden público (art. 20), y **multa al empleador** por despido
fuera de las causales, que aplica el juez en la sentencia (art. 22). Los sueldos del art. 7 y los
montos en moneda nacional son de 1948: hoy salen del convenio.
`[VERIFICAR CCT APLICABLE: convenio colectivo de los trabajadores de edificios -SUTERH- vigente para el período: categorías, salarios y adicionales, no cargados]`

`[REVISIÓN NORMATIVA REQUERIDA: este bloque recorre de la Ley 22.250 los arts. 1 a 3, 12, 13, 15 a 21, 32 y 35; de la Ley 14.546 los arts. 1 a 14; y de la Ley 12.981 los arts. 1 a 6, 9, 13, 20 y 22. Las infracciones y los recursos del Registro -Ley 22.250, arts. 22 a 34-, la Comisión Paritaria de Viajantes y las paritarias de encargados NO están recorridos. Ninguno de los tres tiene fallo cargado, y la relación de cada estatuto con las reformas de las Leyes 27.742 y 27.802 a la LCT -en especial el fondo de cese que la 27.742 habilitó por convenio- va con marcador]`
