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

### R98 · Soy oficial de la Bonaerense, me desafectaron por un sumario y me descuentan la mitad del sueldo. ¿Es legal y cuándo lo recupero?

esperado: `empleo-publico.md`

Vigila que se lea 49.5.5 y no 49.5.4: la Ley 13.982 -arts. 19 a 22- retiene el cincuenta por ciento y lo devuelve de oficio si el sumario termina en amonestación, suspensión de hasta treinta días, sobreseimiento o absolución. Rutear a la Ley 10.430 contestaría con el estatuto equivocado.

### R97 · Una empresa fue sancionada con inhabilitación por un organismo nacional por incumplir una orden de compra. ¿Cómo la impugna?

esperado: `administrativo-nacional.md`

Vigila que se lea 46.5 sexies con 46.5 quater: la sanción del art. 29 del Decreto 1023/2001 se recurre por el Decreto 1759/72 y, agotada la vía, va al fuero contencioso administrativo federal. Rutear a `contencioso-pba.md` sería el error: el organismo es nacional.

### R96 · Le reclamé a un ministerio nacional hace ocho meses y no contestan. ¿Ya puedo demandar? ¿Y una cautelar para que me paguen mientras tanto?

esperado: `administrativo-nacional.md`

Vigila que se lea 46.5 quinquies: seis meses más pronto despacho y otros tres -art. 2 de la Ley 3.952-, y la cautelar de pago choca con el art. 9 de la Ley 26.854 y con los cinco requisitos de la medida positiva del art. 14. Rutear sólo a 46.3 dejaría la cautelar sin su ley.

### R95 · Perdí una licitación del Ministerio de Salud de la Provincia y la adjudicación salió publicada en el sistema de compras el viernes. ¿Cuándo vence el plazo para impugnar?

esperado: `contencioso-pba.md`

Vigila que se lea 26.9 ter: la notificación se tiene por hecha el día hábil siguiente a la publicación -art. 12- y no rige el Capítulo X del Decreto-Ley 7.647/70; la impugnación no suspende, el recurso administrativo sí va por la 7.647. Rutear sólo a 26.4 bis contestaría con la cédula que acá no existe.

### R94 · Me pararon en Ezeiza con tres celulares sin declarar que valen unos ochocientos mil pesos. ¿Es delito o multa?

esperado: `penal-leyes-especiales.md`

Vigila que se lea 24.9.11: por encima de quinientos mil de valor en plaza el hecho es contrabando y no la infracción del art. 947, y las accesorias del art. 876 se aplican en sede judicial o administrativa según el art. 1026. Rutear a `penal.md` a secas contestaría sin el umbral.

### R93 · Alguien entró a mi cuenta de correo, sacó fotos privadas y me amenaza con publicarlas. ¿Qué delitos son y dónde denuncio?

esperado: `penal-leyes-especiales.md`

Vigila que se lea 24.9.10: acceso indebido a una comunicación electrónica -art. 153- o a un sistema -art. 153 bis-, y la amenaza va por el Código. Rutear a `violencia-de-genero.md` puede corresponder además, no en lugar de: la fila mide que se abra el tipo penal.

### R92 · Me llegó un mandamiento de ARBA por ingresos brutos de 2016 con embargo de la cuenta. ¿Tengo cinco días? ¿Puedo decir que está prescripto?

esperado: `tributario-pba.md`

Vigila que se lea 54.5 ter y no `titulos-ejecutivos.md`: cinco días para oponer excepciones, la prescripción está en la lista taxativa del art. 9, y el embargo se dispuso en veinticuatro horas sin caución. El cómputo de la prescripción va al Código Fiscal en 54.3.

### R91 · ARCA me sacó del monotributo por depósitos bancarios que no coinciden con lo que facturo. ¿Cómo lo discuto y cuándo puedo volver?

esperado: `tributario.md`

Vigila que se lea 33.3 bis: la exclusión opera desde la cero hora de la causal, el recurso es el del art. 74 del Decreto 1397/79 y no el del art. 76 de la 11.683, y el reingreso espera tres años calendario. Los montos de las categorías no se citan.

### R90 · Quiero armar una SAS unipersonal con mi hermano como director. ¿Cuánto capital necesito y de qué respondo?

esperado: `societario.md`

Vigila que se lea 31.3 quinquies y no 31.1: dos salarios mínimos de capital, veinticinco por ciento integrado al suscribir, y la garantía solidaria por la integración del art. 43. Rutear sólo a la LGS contestaría con un tipo que no es.

### R89 · Hago doce horas por día en una fábrica, seis días por semana, y me pagan todo como jornal simple. ¿Qué me deben?

esperado: `laboral.md`

Vigila que se lea 5.17 septies junto con 5.4: ocho y cuarenta y ocho son el tope de la Ley 11.544, el recargo es del cincuenta por ciento y del cien en feriados, y las excepciones del art. 3 tienen el texto de la Ley 27.802. La liquidación va al script con el valor hora que aporte el usuario.

### R88 · Trabajo desde casa desde la pandemia y ahora me exigen volver a la oficina de un día para otro. ¿Pueden?

esperado: `laboral-licencias.md`

Vigila que se lea 5.14 bis y no sólo el ius variandi de `laboral.md`: si el contrato empezó presencial y pasó a teletrabajo, la reversión es un derecho del trabajador -art. 8-, y si nació como teletrabajo el cambio va por el convenio. La fecha de inicio es lo primero que hay que preguntar.

### R87 · El Servicio Local se llevó a mi hijo a un hogar hace tres días y no me dijeron por cuánto tiempo. ¿Qué puedo hacer?

esperado: `familia.md`

Vigila que se lea 18.10 quater: la medida excepcional se notifica al juez en veinticuatro horas y éste revisa la legalidad en setenta y dos -art. 40 de la Ley 26.061-, y el plazo de abrigo del art. 35 bis va con marcador. Rutear a `penal-juvenil-pba.md` sería el error: no hay imputado.

### R86 · Una vecina me dio a su bebé para que lo críe y quiero adoptarlo. ¿Cómo se hace?

esperado: `familia.md`

Vigila que se lea 18.10 ter: la entrega directa está prohibida por el art. 611 y la guarda de hecho no se considera para adoptar, salvo parentesco. Una respuesta que explique el trámite sin decir eso primero reprueba aunque cite bien las tres etapas.

### R85 · Conviví seis años con mi pareja sin casarnos, la casa está a su nombre y nos separamos. ¿Tengo derecho a algo?

esperado: `familia.md`

Vigila que se lea 18.10 bis y no 18.9: sin pacto los bienes quedan en el patrimonio de cada uno -art. 528-, la compensación caduca a los seis meses y la vivienda se atribuye por hasta dos años. Rutear al perfil heredado sería el error: la fila está absorbida.

### R84 · Firmé un boleto de compraventa y me dicen que el escribano pidió el certificado el lunes y hay un embargo anotado el miércoles. ¿Quién gana?

esperado: `derechos-reales.md`

Vigila que se lea 45.5 bis: la reserva de prioridad del art. 25 depende de que la escritura se otorgue dentro de la vigencia del certificado y se presente en cuarenta y cinco días. Rutear a `contratos.md` contestaría el boleto donde la pregunta es registral.

### R83 · Soy administrador de un consorcio de Quilmes y un propietario debe ocho meses de expensas. ¿Con qué le inicio la ejecución y qué me puede oponer?

esperado: `derechos-reales.md`

Vigila que se lea 45.4 y no sólo `titulos-ejecutivos.md`: el certificado del art. 2048 con aprobación del consejo es el título, y el art. 2049 cierra las defensas salvo compensación. Rutear sólo a `procesos-especiales.md` sería el error de esta fila.

### R82 · Me llegó el resumen de la tarjeta con dos compras que no hice y vence en cuatro días. ¿Qué hago y hasta cuándo?

esperado: `consumidor.md`

Vigila que se lea 17.11.7 y no sólo la LDC: treinta días para impugnar por nota simple, el emisor no puede bloquear la tarjeta mientras tanto, y pagar el mínimo no es aceptar. Rutear a `titulos-ejecutivos.md` sería el error de esta fila: el saldo de tarjeta no es título ejecutivo.

### R81 · Cobro la AUH por mis dos hijos y me la suspendieron porque el más chico no tiene el control del año. ¿Es así?

esperado: `previsional.md`

Vigila que se lea 32.4 quater: hasta los cuatro años los controles sanitarios condicionan el veinte por ciento reservado, no el ochenta mensual, y los montos no salen de la ley. Rutear a `salud-discapacidad.md` sería contestar cobertura donde la pregunta es la asignación.

### R80 · Un oficial albañil trabajó dos años para una constructora de Berazategui, lo echaron ayer y no le dieron la libreta. ¿Qué le corresponde?

esperado: `laboral.md`

Vigila que se lea 5.17 sexies y no se liquide con el art. 245: hay fondo de cese y no indemnización, la libreta se entrega en cuarenta y ocho horas, y la intimación de dos días hábiles abre la indemnización de treinta a noventa días. Correr `liquidacion_lct.py` sería el error de esta fila.

### R79 · Soy empleado municipal de Quilmes con ocho años de planta y me dejaron cesante por inasistencias sin sumario. ¿Qué recurso tengo y cuánto plazo?

esperado: `empleo-publico.md`

Vigila que se lea 49.5.4 y no la Ley 25.164: rige la Ley 14.656, la cesantía exige sumario previo, el recurso es revocatoria o jerárquico ante quien sancionó, y la prescripción disciplinaria municipal es de doce meses. Rutear a `laboral.md` sería contestar con la LCT, que el art. 2 inc. a excluye.

### R78 · Me notificaron por TAD que rechazaron mi pedido en un organismo nacional y la notificación no dice qué recurso tengo. ¿Qué hago?

esperado: `administrativo-nacional.md`

Vigila que se lea 46.5 quater: la notificación que no indica el recurso y el plazo es inválida por el art. 40 del reglamento, la reconsideración son veinte días y el jerárquico treinta, y pedir vista suspende los plazos. Rutear sólo a la LNPA de 46.4 deja la pregunta sin contestar.

### R77 · ARBA me rechazó un reclamo por resolución de un director y quiero llegar a la justicia. ¿Tengo que recurrir antes, y en qué plazo?

esperado: `contencioso-pba.md`

Vigila que se lea 26.4 bis además de 26.4: la revocatoria y el jerárquico son de diez días hábiles, el jerárquico contra el acto de un director lo resuelve el Poder Ejecutivo, y el acto dictado con intervención del interesado que deja expedita la acción no necesita jerárquico. Rutear a `tributario-pba.md` solo contesta el fondo y no la vía.


### R76 · Una empleada que trabaja tres veces por semana en una casa de familia de Lanús fue despedida sin causa después de cuatro años, nunca registrada. ¿Qué le corresponde y dónde se reclama?

esperado: `laboral.md`

Vigila que el módulo se lea hasta 5.17 quinquies y no se conteste con el art. 245: el preaviso,
la integración y la indemnización son los de la Ley 26.844, **no hay multas de las Leyes 24.013,
25.323 ni 25.345**, el art. 50 está derogado, y el Tribunal del Título XII es de Capital Federal.
Rutear a `liquidacion_lct.py` sería el error de esta fila.

### R75 · Mi defendido está imputado por homicidio agravado en Lomas de Zamora y el fiscal ya pidió la elevación a juicio. ¿Puedo evitar el jurado?

esperado: `penal.md`

Vigila la ventana del art. 22 bis: la renuncia se hace en el plazo del art. 336 y **firme la
requisitoria ya no se puede**, bajo pena de nulidad. Rutear sólo a `penal-impugnacion.md` sería
contestar sobre el recurso cuando la pregunta es sobre la etapa.

### R74 · Rescataron a una mujer de un departamento donde la obligaban a prostituirse; ella dice que había aceptado venir a trabajar. ¿Qué delito es, quién investiga y qué pasa con lo que ella hizo mientras estaba ahí?

esperado: `penal-leyes-especiales.md`

Vigila tres cosas del mismo módulo: que el tipo se lea en el **Código Penal** con texto de la Ley
26.842 y no en los arts. 10 y 11 de la ley especial; que el **consentimiento no exime**; y que la
víctima **no es punible** por el art. 5. Rutear a `penal.md` sería contestar el proceso sin el
encuadre.


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


### R67 · Tuve un accidente en la obra, la ART me dio el alta y quedé con una limitación en el hombro. ¿Qué hago?

esperado: `laboral-riesgos.md`

**El error que vigila es abrir `laboral.md`** por la palabra «trabajo». El régimen de la Ley
24.557 salió a módulo propio con su numeración —5.8 y sus subsecciones— porque es otra ley, con
instancia administrativa previa ante Comisión Médica, baremo propio y su propia jurisprudencia. Y
el eje no es la extinción del contrato sino la reparación de un daño: acá no hay despido que
liquidar. Si además lo despidieran, se leen los dos.

### R68 · Avisé que estoy embarazada y a los dos meses me suspendieron sin sueldo por quince días. ¿Pueden?

esperado: `laboral-licencias.md`

Cruza las dos materias del módulo y ninguna es la extinción: la **protección del art. 177 y la
presunción del art. 178** por un lado, y por el otro **los tres requisitos de validez del art.
218** —justa causa, plazo fijo y notificación por escrito— con los plazos máximos del art. 220 y
la impugnación del art. 67. **El error que vigila es abrir `laboral.md`** por «suspensión sin
sueldo», buscando allá una liquidación que acá no hay: el contrato sigue vivo. Si además la
despidieran, recién ahí se suman los dos.

### R69 · Mi ex subió fotos íntimas mías a un grupo y las están reenviando. Quiero que las bajen ya.

esperado: `violencia-digital.md`

**El error que vigila es ir directo a `penal.md`.** La Ley 27.736, llamada Olimpia, **no creó
ningún delito**, sus trece artículos modifican la Ley 26.485, que es de protección integral. Lo que hay
es la medida del **art. 26 ap. a.9** —orden de baja por auto fundado, con **la URL específica
identificada**— y el aseguramiento de tráfico y contenido por noventa días que la misma norma
manda pedir. El segundo error que vigila es contestar sólo con `familia.md`: allá está el proceso,
acá lo que la modalidad digital agrega. Si además la conducta configura un delito, recién ahí se
suma el encuadre penal.

### R70 · Compré un departamento y la escritura dice que pagué todo, pero quedó un saldo. ¿Tengo que redargüir de falsedad?

esperado: `notarial.md`

**El error que vigila es mandar a redargüir de falsedad**, que es caro, se plantea por incidente y
acá no corresponde. El **art. 296** parte la plena fe en dos: que las partes **manifestaron** lo
que dice la cláusula es un hecho cumplido ante el escribano y sólo cae *"declarado falso en juicio
civil o criminal"*; **que el precio se haya pagado** es el contenido de esa declaración y cede
*"hasta que se produzca prueba en contrario"*. El segundo error que vigila es resolverlo con
`civil.md`: lo que se discute no es el contrato sino el valor del documento. Si además hay que
ejecutar la obligación de entrega, recién ahí se suma el fuero y su rito.

### R71 · Entraron a mi casa sin orden, encontraron un arma y con eso me imputan. ¿Sirve como prueba?

esperado: `penal-impugnacion.md`, `penal.md`

**El error que vigila es contestar con el art. 18 CN y nada más.** Si hay regla de exclusión
**escrita** o hay que construirla desde la Constitución y la jurisprudencia depende del código
que rija: el **CPPF art. 129** y el **CPP PBA art. 211** la traen en el texto y la **Ley 23.984
no tiene ninguna**, así que el planteo se funda distinto. Por eso la consulta abre dos módulos y
el orden importa: cuál código rige está en `penal.md` 24.1, y la regla, en `penal-impugnacion.md`
24.5.1. El segundo error que vigila es ir a `penal-parte-general.md`: lo que se discute no es el
tipo ni la pena sino si el acto puede valorarse.

### R72 · El hecho fue hace nueve años y recién ahora me citaron a declarar. ¿No prescribió?

esperado: `penal-parte-general.md`

**El error que vigila es abrir `plazos.md`**, que es la prescripción civil y liberatoria: acá el
plazo sale del **art. 62 CP** y se cuenta contra el **máximo de la pena del delito, con tope de
doce años y piso de dos**, así que la respuesta no se puede dar sin saber qué se imputa. El
segundo error que vigila es contestar con el plazo y callar los **cinco actos interruptivos** del
art. 67 y sus cuatro supuestos de suspensión, que son los que explican por qué una causa de nueve
años puede seguir viva.

### R73 · Me llegó una cédula de un Juzgado de Paz de Lobos por un reclamo de alimentos. ¿Es ahí?

esperado: `justicia-de-paz-pba.md`

**El error que vigila es contestar que el Juzgado de Paz no tiene familia**, que es verdad en
veinte partidos del conurbano y falso en todos los demás. El **art. 61 de la Ley 5.827** parte los
juzgados en dos grupos: el inciso I nombra veinte partidos por su nombre —Lobos no está— y el
inciso II dice *"los restantes"*, que suman alimentos, tenencia, régimen de visitas, internaciones
de urgencia y hábeas corpus. El segundo error que vigila es mandar a `familia.md` sin más: allá
está el fondo del reclamo, acá si ese juzgado es competente. **Y el dato que hay que pedir antes de
contestar es el partido**, no el departamento judicial.
