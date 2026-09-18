---
titulo: Consultas de ruteo · qué módulo abre el sistema
---

# Consultas de ruteo

> Eval de una sola pregunta: **¿abrió el módulo que correspondía?** No se juzga la respuesta.

## Por qué es un eval aparte

Los casos de `evals/` traen una pieza procesal y una rúbrica de contenido. Miden bien lo que
pasa una vez que el sistema está leyendo el módulo correcto. Con el catálogo de módulos que hay,
la falla que crece no es esa: es abrir el que no era, o ninguno y contestar de memoria. Y una
respuesta de memoria que acierta aprueba cualquier rúbrica de contenido, así que esa falla no
deja rastro hasta el día que la memoria se equivoca.

Por eso acá la consulta es corta a propósito y **no se puntúa el análisis**. Sólo se anota qué
abrió. Una consulta de una línea es además el peor caso para el ruteo, que es justo lo que se
quiere medir.

## Cómo se corre

1. Sesión nueva por consulta. El ruteo se mide en frío: un módulo ya abierto en el contexto
   contesta la siguiente consulta sin que nadie rutee nada.
2. Pegar la consulta tal cual, sin agregar el área ni el fuero.
3. Anotar **qué archivos abrió**, en orden, antes de contestar.
4. Aprueba si abrió todos los esperados. Abrir de más no reprueba; abrir de menos sí.
5. Si no abrió ninguno y contestó igual, **reprueba aunque la respuesta sea correcta**: eso es
   exactamente lo que el eval busca.

Los módulos que se listan como esperados son los que la consulta exige. `intake.md` y
`marcadores.md` se leen en casi toda consulta de fondo y no se anotan salvo que la consulta
gire sobre ellos.

## El mapa, aparte

Que desde el ruteo se **pueda** llegar a cada módulo es una propiedad del repositorio y se mide
sola:

```sh
python3 herramientas/ruteo.py
```

Informa a qué distancia del router quedó cada módulo y cuál no se alcanza por ningún camino.
Un módulo a distancia tres existe, está escrito y nadie lo va a abrir. Esa herramienta mide el
mapa; estas consultas miden el manejo.

---

### R61 · Mi cliente tiene condena firme y quiere pedir salidas transitorias. Está alojado en una unidad de PBA. ¿Qué pido y ante quién?

esperado: `ejecucion-penal.md`

Rutear a `penal.md` sería el error de esta fila: allá está el proceso hasta la sentencia. Y dentro
de este módulo lo que decide es la ley del establecimiento: la **Ley 24.660** organiza la ejecución
por **períodos sucesivos** y la **Ley 12.256 de PBA** por **regímenes de utilización alternativa y
no necesariamente secuencial**, así que "el ingreso al período de prueba" no existe ante un juez
bonaerense.

### R60 · AGIP me determinó de oficio Ingresos Brutos y me intiman a pagar antes de poder discutir. ¿Es así?

esperado: `tributario-caba.md`

Vigila la confusión entre tres jurisdicciones. Rutear a `tributario.md` sería contestar con la Ley
11.683, y rutear a `tributario-pba.md` sería peor: **allá el pago previo es requisito de
admisibilidad de la demanda y acá lo decide el juez con criterio cautelar**, por el art. 9 de la
Ley 189.

### R59 · Me labraron un acta en la Ciudad por tener las mesas del bar sobre la vereda. ¿Qué es esto y qué hago?

esperado: `contravencional-caba.md`

Vigila la frontera que ordena el módulo: **falta de la Ley 451 o contravención de la Ley 1.472**,
que no se resuelve por el nombre del acta sino por la norma que imputa. Rutear a `transito.md`
sería el error de esta fila —ahí están las infracciones del régimen nacional y de PBA— y rutear a
`penal.md` también: el fuero es el mismo, el régimen no.

### R58 · Soy docente de la Provincia, me jubilé por el IPS y me liquidaron el haber sobre un cargo inferior al que tenía. ¿Qué reclamo?

esperado: `previsional-pba.md`

Rutear a `previsional.md` sería el error de esta fila: allá está el SIPA, con PBU, compensatoria y
adicional por permanencia. Acá el haber es el **70% de la remuneración del cargo** (art. 41 del
Decreto-Ley 9650/80) y lo que decide cuál cargo se toma son los **36 meses consecutivos o 60
alternados** en él.

### R57 · ARBA me determinó de oficio Ingresos Brutos por cuatro años y me llegó la resolución. ¿Qué presento y ante quién?

esperado: `tributario-pba.md`

Rutear a `tributario.md` sería el error de esta fila: allá está el procedimiento ante ARCA, con
los recursos del art. 76 de la Ley 11.683 y sus plazos. Acá el plazo es de quince días, la opción
entre reconsideración y Tribunal Fiscal es **excluyente** y la decide el monto, y el silencio opta
por el Tribunal.

### R56 · Tengo un cliente detenido hace tres días y el juzgado no le tomó declaración. ¿Qué presento?

esperado: `penal-leyes-especiales.md`

Hábeas corpus de la Ley 23.098, en 24.9.1. Rutear a `penal.md` sería el error de esta fila: allá
está el proceso —coerción, nulidades, recursos— y acá las leyes que están fuera del Código.

### R55 · El convenio de mi actividad venció hace dos años y la empresa dice que ya no me cubre. ¿Es así?

esperado: `laboral-colectivo.md`

Ultraactividad del art. 6 de la Ley 14.250, texto Ley 27.802: vencido el término subsisten
**solamente** las cláusulas normativas, hasta que entre en vigencia una nueva convención. Rutear a `laboral.md` sería el error de esta fila — allá está la
liquidación individual, acá el convenio.

### R47 · Me cortaron el gas por una deuda que no reconozco y la distribuidora dice que tengo que reclamar primero ante el ente. ¿Es así?

esperado: `consumidor.md`

Vigila la rama que entró como sección: 17.11.5 bis. El art. 53 de la Ley 24.076 sí impone
instancia previa, pero el art. 25 LDC deja al usuario elegir dónde reclamar, y los dos conviven.

### R48 · Misma pregunta pero con la luz: ¿tengo que ir al ente antes de demandar?

esperado: `consumidor.md`

La respuesta es la contraria a la de R47 y por eso la consulta está separada: el art. 58 de la
Ley 24.065 hace **facultativa** la instancia previa para el usuario. Si las dos rutean igual y se
contestan igual, el ruteo funcionó y el contenido no.

### R49 · La aerolínea me perdió la valija en un vuelo a Salta. ¿Qué me tienen que pagar?

esperado: `consumidor.md`

El art. 63 LDC manda al Código Aeronáutico y la LDC queda supletoria: 17.11.5 ter. Abrir el módulo civil por la
palabra «daños» sería el error.

### R50 · Soy socio de una cooperativa de trabajo y quiero cobrar mi parte de los excedentes.

esperado: `societario.md`

No es una sociedad de la Ley 19.550 y no hay dividendos: 31.3 bis. El riesgo es contestar con
societario común sin abrir la sección.

### R51 · Trabajo en una finca levantando cosecha. Me echaron sin preaviso. ¿Corre la LCT?

esperado: `laboral.md`

Es el estatuto de la Ley 26.727: 5.17 quater. No es una exclusión de la LCT sino un estatuto
especial, y su art. 2 inc. b manda aplicar la 20.744 en lo compatible.

### R52 · Pedí información a un ministerio hace tres meses y no me contestaron nada.

esperado: `administrativo-nacional.md`

Ley 27.275, 46.5 bis. El silencio habilita la vía, y hay dos caminos optativos entre sí.

### R53 · Soy abogado y un cliente me quiere pagar los honorarios en efectivo, en dólares. ¿Tengo que informar algo?

esperado: `penal.md`

El art. 20 inc. 17 de la Ley 25.246 pone al abogado como sujeto obligado en ciertos supuestos:
24.9.6. Es la consulta que más se contesta de memoria y peor.

### R54 · No fui a votar en las últimas elecciones y ahora no puedo hacer un trámite en el municipio.

esperado: `penal.md`

Es el art. 126 del Código Electoral, en 24.9.7: la consecuencia de no pagar la multa no es la
multa. Abrir el módulo de procedimiento administrativo por la palabra «trámite» sería el error.

---

### R01 · Me despidieron en julio y quiero saber cuánto me corresponde.

esperado: `laboral.md`

### R02 · ¿Cuándo vence el traslado si me notificaron por cédula electrónica un viernes?

esperado: `plazos.md`, `notificaciones-pba.md`

### R03 · Choqué con un auto que estaba mal estacionado y el seguro no quiere pagar.

esperado: `civil.md`, `transito.md`

### R04 · La prepaga me aumentó un 40% de un mes para el otro.

esperado: `consumidor.md`, `salud-discapacidad.md`

### R05 · Quiero pedir alimentos para mi hija y el padre vive en otra provincia.

esperado: `familia.md`

### R06 · Necesito redactar una demanda y ver si ya tienen un modelo armado.

esperado: `escritos.md`, `modelos.md`

### R07 · Soy el juez y tengo que dictar el veredicto en un juicio laboral bonaerense.

esperado: `sede-judicial.md`, `sede-judicial-pba.md`

Son dos: el modo de trabajo no tiene fuero y la pieza sí. Abrir sólo el segundo saltea qué se
controla de oficio y qué deja de hacerse; abrir sólo el primero deja la sentencia sin estructura.


### R08 · La empresa que me debe la indemnización se presentó en concurso.

esperado: `concursos.md`, `laboral.md`

### R09 · El banco me informó como moroso en el Veraz por una deuda que ya pagué.

esperado: `datos-personales.md`, `consumidor.md`

### R10 · Quiero impugnar la pericia contable porque el perito no explicó el método.

esperado: `prueba-pericial.md`

### R11 · Mandé el telegrama de intimación y no me contestaron en 48 horas.

esperado: `telegramas.md`, `laboral.md`

### R12 · El municipio me rechazó el recurso y quiero ir a la justicia.

esperado: `contencioso-pba.md`

### R13 · Firmé un contrato de locación con una cláusula que me obliga a pagar en dólares.

esperado: `contratos.md`, `civil.md`

### R14 · ARBA me determinó de oficio y quiero discutir la prescripción.

esperado: `tributario.md`

### R15 · El deudor es una SRL vaciada y quiero ir contra los socios.

esperado: `societario.md`

### R16 · Me rechazaron el retiro por invalidez de ANSES.

esperado: `previsional.md`

### R17 · El contrato con el proveedor dice que se juzga en Montevideo.

esperado: `dipr.md`

### R18 · Me imputaron tenencia de estupefacientes para consumo personal.

esperado: `penal.md`

### R19 · Tengo sentencia firme y el demandado no paga.

esperado: `ejecucion.md`

### R20 · ¿Qué dijo la Corte en "Aquino"?

esperado: `fallos-csjn.md`

### R21 · ¿La reforma laboral cambió algo desde que se armó este repositorio?

esperado: `changelog-normativo.md`

### R22 · ¿De dónde sacaron el texto de la ley que me están citando?

esperado: `fuentes.md`

### R23 · Represento a la parte actora y tengo que preparar la audiencia preliminar.

esperado: `parte.md`

### R24 · Necesito cuantificar la incapacidad sobreviniente en un juicio de daños.

esperado: `civil.md`, `danos-indice-doctrinario.md`

### R25 · Me mordió el perro del vecino y quiero saber qué reclamo.

esperado: `civil.md`, `perfiles-heredados.md`

### R26 · ¿Qué datos te tengo que dar antes de que analices el caso?

esperado: `intake.md`

### R27 · ¿Qué significan los corchetes en mayúscula que ponés en los escritos?

esperado: `marcadores.md`

### R28 · A mi hijo de 16 lo detuvieron en La Plata por un robo. ¿Qué pasa ahora?

esperado: `penal-juvenil-pba.md`, `penal.md`

### R29 · Me regularon honorarios en un juicio en Comodoro Py y quiero saber si está bien hecho.

esperado: `honorarios-nacional.md`

### R46 · Tres empresas del rubro se pusieron de acuerdo para subir los precios y mi negocio se fundió. ¿Tengo que denunciar primero?

esperado: `competencia.md`, `civil.md`

El art. 62 habilita la acción de daños por derecho común ante el juez civil sin esperar a la autoridad, y el acuerdo entre competidores del art. 2 presume el perjuicio al interés económico general. Contestar que primero hay que agotar la vía administrativa es el error que esta fila vigila.

### R45 · Quiero acompañar como prueba unos mails y un PDF firmado con una imagen de mi firma.

esperado: `firma-digital.md`, `prueba-pericial.md`

Una imagen de firma escaneada no es firma digital: es firma electrónica del art. 5, y ahí no hay presunción de autoría — la carga de probarla es de quien la invoca. Tratarla como firma digital es el error que esta fila vigila.

### R44 · Internaron a mi hermano contra su voluntad en una clínica. ¿Puedo hacer algo?

esperado: `salud-mental.md`

La internación involuntaria se notifica al juez en diez horas y la persona tiene derecho a un abogado desde el momento de la internación, que el Estado debe proporcionar si no lo designa. Contestar que hay que esperar a que el juez resuelva, sin nombrar esos dos recaudos, es el error que esta fila vigila.

### R43 · Tengo un cheque que me rechazaron hace once meses. ¿Todavía lo puedo ejecutar?

esperado: `titulos-ejecutivos.md`

El año del art. 61 se cuenta desde la expiración del plazo de presentación si es común, y desde el rechazo si es de pago diferido. Contestar con una sola regla, sin preguntar qué clase de cheque es, es el error que esta fila vigila.

### R42 · Trabajé doce años en un organismo del Estado con contratos renovados y me dejaron afuera. ¿Cuánto me corresponde por el art. 245?

esperado: `empleo-publico.md`, `laboral.md`

La pregunta trae adentro la respuesta equivocada: el art. 2 inc. a LCT excluye al empleado público sin acto expreso de inclusión, así que no hay art. 245. Liquidar con la calculadora laboral es el error que esta fila vigila, y `liquidacion_lct.py` ya se planta con [ARG SIN NORMA] cuando se lo intenta.

### R41 · Mi inquilino debe dos meses. ¿Puedo iniciar el desalojo ya?

esperado: `locacion.md`

Dos períodos consecutivos habilitan la resolución por el art. 1219 inc. c, pero si el destino es habitacional el art. 1222 exige intimación fehaciente previa con un plazo no menor a diez días corridos. Contestar que sí sin preguntar el destino ni la intimación es el error que esta fila vigila.

### R40 · El contrato con la empresa dice que cualquier juicio va a los tribunales de otra provincia. Soy consumidor en CABA.

esperado: `consumo-caba.md`, `consumidor.md`

El art. 3 del Código porteño hace la competencia improrrogable PARA EL PROVEEDOR, así que la cláusula no le sirve a él. Tratarla como una prórroga válida, o rutear sólo al derecho de fondo sin ver el fuero, es el error que esta fila vigila.

### R39 · Me rechazaron un recurso en un organismo nacional hace cuatro meses. ¿Ya perdí la chance de ir a juicio?

esperado: `administrativo-nacional.md`

El plazo del art. 25 es de ciento ochenta días hábiles judiciales desde la notificación, así que cuatro meses no lo agotan; pero antes hay que ver si la vía quedó agotada. Contestar con el plazo anterior a la reforma de la Ley 27.742, o dar por perdida la acción sin contar hábiles judiciales, es el error que esta fila vigila.

### R38 · Ocupo una casa hace veintidós años sin papeles. El dueño anterior dice que mi posesión es de mala fe.

esperado: `derechos-reales.md`

A los veinte años la mala fe deja de ser oponible: el art. 1899 lo dice expresamente, y también que no se puede invocar la falta o nulidad del título. Discutir la buena fe cuando se invocan veintidós años es el error que esta fila vigila.

### R37 · Mi juicio en Tribunales está parado hace siete meses. ¿Me pueden pedir la caducidad?

esperado: `proceso-nacional.md`

Seis meses en primera instancia por el art. 310 inc. 1, pero tres si está en cámara o si es ejecutivo o sumarísimo. Contestar con el plazo bonaerense, o con el de primera instancia sin preguntar en qué instancia está, es el error que esta fila vigila.

### R36 · La prepaga me negó la cobertura hace veinte días. ¿Puedo hacer un amparo?

esperado: `amparo.md`, `salud-discapacidad.md`

Los quince días del art. 2 inc. e parecen vencidos, y ahí está la trampa: si la negativa se
renueva mes a mes la lesión es de tracto continuado y el cómputo es otro. Contestar «ya venció»
sin preguntar si el acto se agotó es el error que esta fila vigila.

### R35 · Gané un amparo en el fuero contencioso administrativo de la Ciudad. ¿Cuánto son mis honorarios en UMA?

esperado: `honorarios-caba.md`

Trae la unidad correcta y el fuero correcto, y aun así se puede fallar: la UMA de la Ley 5.134 no
es la de la Ley 27.423, y la publica el Consejo de la Magistratura de CABA y no la CSJN. Rutear a
`honorarios-nacional.md` por la palabra «UMA» es el error que esta fila vigila.

### R34 · Una fábrica vuelca residuos al arroyo del barrio. Queremos que paguen a los vecinos.

esperado: `ambiental.md`, `civil.md`

El daño colectivo se recompone y su indemnización sustitutiva va al Fondo de Compensación, no a
los vecinos: eso es el art. 28. El daño individual de cada uno corre aparte. Prometer que «paguen
a los vecinos» por la vía colectiva es el error que esta fila vigila, y si hay residuos peligrosos
la competencia penal es federal.

### R33 · Una empresa de España nos quiere licenciar su marca. ¿Alcanza con firmar el contrato?

esperado: `propiedad-industrial.md`

La Ley 22.426 parte el régimen en dos: si hay vínculo de control con la licenciante, el acto va a
APROBACIÓN de la autoridad; si no, a registro informativo. Contestar que alcanza con firmar, o
rutear a `contratos.md` y quedarse ahí, es el error que esta fila vigila.

### R32 · Choqué, denuncié al otro día y la aseguradora me contestó recién a los dos meses que no cubre. ¿Puede?

esperado: `seguros.md`, `transito.md`

El art. 56 da treinta días para pronunciarse y el silencio importa aceptación, así que la
cronología decide antes que el fondo. Contestar sobre la cobertura sin reconstruir las fechas es
el error que esta fila vigila.

### R31 · Murió mi papá y a mi hermano le había donado un departamento hace quince años. ¿Eso se cuenta?

esperado: `sucesiones.md`

Cruza dos cosas que se confunden: la donación entra a la base de cálculo de la legítima por el
art. 2445 aunque no esté en el acervo, y a los quince años de posesión el art. 2459 —texto Ley
27.587— ya impide la reducción contra el donatario. Rutear sólo a `civil.md` es el error.

### R30 · Gané un despido en el fuero laboral de Capital. ¿Cuánto son mis honorarios en jus?

esperado: `honorarios-nacional.md`

La pregunta trae la unidad equivocada adentro: el fuero laboral de Capital es la Justicia
Nacional del Trabajo y ahí rige la UMA, no el jus. Rutear a `sede-judicial-pba.md` por la
palabra «jus» es el error que esta fila vigila.

### R62 · Soy juez civil de la Nación y tengo que dictar sentencia en un juicio de daños.

esperado: `sede-judicial.md`, `sede-judicial-nacional.md`, `civil.md`

**`sede-judicial-pba.md` es la respuesta equivocada**, y es la que el nombre del módulo invita a
dar: sus recaudos son de la Constitución bonaerense y su pieza doble es del rito laboral
provincial. Acá la sentencia sale del art. 163 CPCCN y el deber de fundar del art. 34 inc. 4.

### R63 · Soy juez del fuero contencioso administrativo y tributario de la Ciudad y tengo que dictar sentencia.

esperado: `sede-judicial.md`, `sede-judicial-caba.md`

El error que vigila es citar el **art. 34 inc. 4** del CPCCN por el deber de fundar: en el CCAyT
es el **art. 29 inc. 4**, con el mismo texto y otro número. Y la sentencia es el art. 147, que
exige la valoración de la prueba como inciso propio y no como parte de los fundamentos.

### R64 · Soy juez nacional del trabajo y quiero saber qué plazo tiene la parte para apelar mi sentencia.

esperado: `sede-judicial-nacional.md`

Son **seis días y con los agravios adentro** (art. 116 Ley 18.345), no los cinco del art. 244
CPCCN: el fuero tiene plazo propio aunque el contenido de la sentencia lo tome del CPCCN por la
remisión del art. 155.

### R65 · Me contestaron un pedido de caducidad en un juicio civil en La Plata. ¿Perdí la instancia?

esperado: `proceso-pba.md`

El error que vigila es contestar con el CPCCN, donde la caducidad se declara de oficio sin más
trámite (art. 316). En PBA el art. 315 exige **intimación previa por única vez, y cinco días para
manifestar la intención de continuar**: hay un acto entre el vencimiento y la pérdida.

### R66 · Me regularon cuatro jus en un juicio laboral en Provincia. ¿Está bien?

esperado: `honorarios-pba.md`

Dos errores de una: el **mínimo del art. 22 de la Ley 14.967 son siete jus** con prescindencia del
contenido económico, y en la tabla de la SCBA conviven el jus del art. 9 y el **jus arancelario
del decreto-ley 8904/77**, que no es el de los abogados. Rutear a `honorarios-nacional.md` por la
palabra «honorarios» es el otro error que esta fila vigila.

