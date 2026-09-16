# Ejecución de sentencia · liquidación, embargo y excepciones

> Módulo de referencia de la skill `derecho-argentino`. La numeración de secciones es global y
> se mantiene igual que en el SKILL.md original: las remisiones cruzadas entre módulos siguen siendo
> válidas. Las reglas de integridad de la sección 2 rigen acá también.

---

## 21 · Ejecución de sentencia

Etapa donde se pierde en horas lo que se ganó en años. Tres errores concentran casi todo el
daño: liquidar con una tasa que ya no rige, dejar vencer el plazo de observación, y oponer
—o admitir— una excepción que no está en la enumeración taxativa.

### 21.1 Qué régimen rige

| Proceso | Norma de la ejecución |
| --- | --- |
| Laboral PBA, causa **con** vista celebrada antes de la Res. SC 1840/2024 | **Arts. 48 a 53 bis Ley 11.653**, con remisión al CPCCBA |
| Laboral PBA, causa **sin** vista celebrada | **Arts. 59 a 66 Ley 15.057** |
| Civil, comercial, familia y consumo en sede judicial PBA | **Arts. 497 a 510 CPCCBA** |
| Laboral nacional | Arts. 132 a 139 Ley 18.345, con supletoriedad del CPCCN |
| Civil y comercial nacional | Arts. 499 a 516 CPCCN |

Los dos textos laborales bonaerenses **no dicen lo mismo** en los tres puntos que más importan:
la tasa, el plazo para pedir el embargo y la recurribilidad de la desestimación del incidente
parcial. Determinar el régimen antes de calcular.

### 21.2 La liquidación — quién la practica y en qué plazo

**Laboral PBA.** Es una particularidad del fuero: **la practica el Secretario, de oficio**, no
la parte vencedora.

- **Art. 48 Ley 11.653** (texto Ley 14.399): "Dictada la sentencia el Secretario del Tribunal
  practicará liquidación de capital, intereses y costas, notificando a las partes en la forma
  ordenada en el artículo 16, bajo apercibimiento de tenerla por consentida si dentro del
  quinto día no se formularen observaciones, cuyo trámite no interrumpirá el plazo para
  deducir los recursos correspondientes."
- **Art. 59 Ley 15.057**: idéntico en la parte transcripta, con la remisión al art. 16 y al
  quinto día. **Suprime el segundo párrafo** del art. 48.

Dos consecuencias que se olvidan:

1. **El trámite de la observación no interrumpe el plazo recursivo.** Observar la liquidación
   y esperar su resolución para recurrir la sentencia es perder el recurso. Los dos plazos
   corren en paralelo. Es una de las trampas más caras del fuero.
2. **La liquidación se notifica junto con la sentencia definitiva** (art. 16 inc. h Ley 11.653;
   art. 16 inc. g Ley 15.057, que remite al art. 59) y por cédula, no por ministerio de la ley.
   Ver `notificaciones-pba.md` sección 22.

> **El segundo párrafo del art. 48 no se aplica.** El texto según Ley 14.399 manda adicionar
> intereses "al promedio de la Tasa Activa" del Banco Provincia. **La SCBA declaró
> inconstitucional la Ley 14.399 en "Abraham" (L. 108.164, 13/11/2013).** Una liquidación que
> hoy invoque ese párrafo está aplicando una norma inconstitucional. La tasa se determina por
> la doctrina legal vigente de la SCBA, no por el art. 48. Ver `laboral.md` sección 5.5 bis
> para la cadena completa de precedentes y `scripts/intereses.py` para el cálculo.

**Civil y comercial PBA — art. 501 CPCCBA.** Lógica inversa: la liquidación **la presenta el
vencedor**; si no lo hace dentro de **diez días** desde que la sentencia es ejecutable, puede
hacerlo el vencido. Presentada, se da **vista por cinco días** a la otra parte. Expresada la
conformidad o vencido el plazo sin contestar, se ejecuta por la suma resultante (art. 502).
Si hay impugnación, tramita como incidente (arts. 178 y ss.).

Nunca transcribir una liquidación sin haber verificado la tasa, el período y el capital base.
Si falta cualquiera de los tres, `[VACÍO PROBATORIO: criterio de cuantificación pendiente - tasa, período o capital base de la liquidación]` y no se cierra el número.

### 21.3 El embargo — el plazo de diez días es exclusivo de la Ley 15.057

| | Ley 11.653 art. 49 | Ley 15.057 art. 60 |
| --- | --- | --- |
| Presupuesto | Sentencia pasada en autoridad de cosa juzgada | Sentencia firme **y** transcurridos **diez días sin que el condenado deposite**, en todo o en parte |
| Quién lo decreta | El Tribunal, a instancia de parte | El Juez, a pedido de parte |
| Citación al deudor | Cinco días para oponer excepción de pago documentado posterior a la sentencia | Igual: cinco días |
| Si prospera la excepción | Se rechaza la ejecución **levantando el embargo** | Se rechaza la ejecución y **se ordena el levantamiento de todas las medidas dispuestas** |
| Si se desestima | Se manda llevar adelante, con el trámite de la sentencia de remate del **Libro III, Título II, Capítulo III CPCCBA** | Igual, con remisión genérica al CPCCBA |

**La ventana de diez días de la 15.057 es nueva y es un requisito de procedencia**: pedir el
embargo antes de que venza, en una causa regida por la 15.057, es prematuro. En la 11.653 no
existe esa espera: firme la sentencia, procede a instancia de parte.

**Excepción de pago documentado — el rigor del art. 49.** La 11.653 lo dice expresamente: si
la prueba documental del pago no surge de la causa o no se agrega en el mismo acto de oponer
la excepción, **se desestima sin más trámite**. En caso contrario, traslado por tres días al
ejecutante y resolución sumaria. La 15.057 no reproduce esa frase, pero la carga documental
surge igual del propio texto ("excepción de pago documentado").

**Art. 61 Ley 15.057** — sin equivalente en la 11.653: declara aplicables al proceso de
ejecución los arts. 18, 19, 20 y 21 de la ley "en cuanto resulte compatible".

### 21.4 Incidente de ejecución parcial

Herramienta subutilizada: permite cobrar lo firme sin esperar el resultado de los recursos
sobre el resto.

**Dos supuestos, en los dos textos** (art. 50 Ley 11.653; art. 62 Ley 15.057):

1. El empleador **reconoce**, en cualquier estado del juicio, adeudar un crédito líquido y
   exigible de origen laboral.
2. Quedó **firme la condena** al pago de alguna suma, aunque respecto de otros rubros se haya
   interpuesto un recurso.

En el segundo supuesto la parte debe pedir, para encabezar el incidente, **copia autenticada o
testimonio con certificación** de que el rubro que se pretende ejecutar no está comprendido en
el recurso y de que la sentencia quedó firme respecto de él. Si hay duda sobre esos extremos,
se deniega la formación del incidente.

**La diferencia decisiva:**

| Ley 11.653 art. 50 | Ley 15.057 art. 62 |
| --- | --- |
| "Si hubiere alguna duda acerca de estos extremos, el Tribunal denegará la formación del incidente." Nada dice sobre recurso. | "Si hubiere alguna duda [...] el Juez **podrá** denegar la formación del incidente. **La desestimación será apelable.**" |

La 15.057 convierte una facultad denegatoria sin control en una decisión revisable. En una
causa regida por la 11.653 no corresponde afirmar que la denegatoria es apelable.

Recursos en la 11.653 remiten al régimen extraordinario; en la 15.057, a "los recursos
previstos en esta ley", que incluyen la apelación ante la Cámara de Apelación del Trabajo.
Ver `sede-judicial-pba.md` y `parte.md` sección 1.7.6.

### 21.5 Vía ejecutiva por créditos reconocidos — excepciones taxativas

**Art. 51 Ley 11.653 / art. 63 Ley 15.057.** Cuando en **instrumento público** el empleador
reconoce créditos líquidos, exigibles y provenientes de una relación laboral a favor de un
trabajador, éste tiene acción ejecutiva. Si el documento no trae aparejada ejecución por sí
solo, puede prepararse la vía ejecutiva conforme al CPCCBA (la 11.653 remite expresamente al
art. 523 y concordantes).

**Art. 52 Ley 11.653 / art. 64 Ley 15.057 — las siete excepciones, idénticas en ambos textos y
taxativas** ("sólo se admitirán como excepciones las siguientes"):

1. Incompetencia.
2. Falta de capacidad de las partes o de personería de sus representantes.
3. Litispendencia.
4. Prescripción.
5. Pago total o parcial acreditado mediante documento que **debe acompañarse al oponer la
   excepción, bajo apercibimiento de ser rechazada sin más trámite**.
6. Conciliación o transacción homologadas.
7. Cosa juzgada.

No están: inhabilidad de título, falsedad, nulidad de la ejecución, quita o espera. Oponerlas
es oponer una excepción inadmisible. Admitirlas es ampliar por vía interpretativa una
enumeración que la ley cerró.

**Contraste con la ejecución de sentencia del CPCCBA — art. 504.** Ahí las excepciones son
**cuatro**, también taxativas: falsedad de la ejecutoria, prescripción de la ejecutoria, pago,
y quita, espera o remisión. Y el art. 505 agrega el rigor probatorio: deben fundarse en
**hechos posteriores a la sentencia o laudo**, probarse por constancias del juicio o por
documentos emanados del ejecutante acompañados al deducirlas, **con exclusión de todo otro
medio probatorio**; sin los documentos, el juez rechaza la excepción sin sustanciarla y **la
resolución es irrecurrible**.

Son tres listas distintas —siete, siete y cuatro— para tres situaciones distintas. No
intercambiarlas.

### 21.6 Ejecución de resoluciones administrativas

**Art. 53 Ley 11.653 / art. 65 Ley 15.057.** Incumplida la resolución de la autoridad del
trabajo, puede ejecutarse ante el órgano laboral competente, **solicitando la remisión del
expediente administrativo**. Se aplican las reglas del CPCCBA para ejecución de sentencias
(la 15.057 agrega "y en esta Ley"), y **además** de las excepciones allí autorizadas pueden
oponerse cuatro:

- a) Incompetencia del órgano judicial y de la autoridad administrativa, **fundada en la
  ausencia de presupuestos que legitimen su actuación**;
- b) falta de capacidad de las partes o personería de sus representantes;
- c) cosa juzgada;
- d) litispendencia.

Prueba: solo documentos adjuntados al deducirlas, o confesión judicial, **con exclusión de
otro medio probatorio**. Si no pueden acompañarse testimonios u otras constancias oficiales,
se manifiesta y se pide el envío de las actuaciones en el plazo que fije el órgano.

Notar que acá las excepciones **se suman** a las del CPCCBA, mientras que en la vía ejecutiva
del art. 52 / art. 64 **la enumeración las reemplaza**. Es la diferencia entre "además de las
que allí se autorizan" y "sólo se admitirán las siguientes".

### 21.7 Preparación de la vía ejecutiva por salarios impagos

**Art. 53 bis Ley 11.653** (incorporado por Ley 13.829) y **art. 66 Ley 15.057**. Salarios,
asignaciones familiares o rubros no remunerativos de una relación individual de trabajo
subordinado, vencidos e impagos, pueden demandarse preparando la vía ejecutiva.

**Diferencia de alcance:** el art. 53 bis lo limita a **un máximo de tres meses** devengados,
vencidos e impagos. **El art. 66 de la Ley 15.057 suprime ese tope.**

Condición esencial de viabilidad en ambos: cursar previamente al deudor una **intimación
extrajudicial fehaciente** (carta documento o telegrama Ley 23.789) por el plazo y con las
modalidades del **art. 57 LCT**, que contenga los datos que la norma enumera —fecha de ingreso
o antigüedad computable, entre otros—. Ver `laboral.md` y los modelos de telegramas del
Project. Sin la intimación previa con ese contenido, la vía no se abre.

La Ley 23.789, cotejada (`fuentes/normas/ley-23789.txt`), establece el servicio de telegrama y carta documento **gratuito para el remitente** en todo el país, para trabajadores dependientes, jubilados y pensionados.

### 21.8 Ejecución en el CPCCBA — lo que hay que tener presente

- **Art. 497**: consentida o ejecutoriada la sentencia y vencido el plazo de cumplimiento, se
  ejecuta **a instancia de parte**.
- **Art. 498**: las mismas reglas se aplican a la ejecución de **transacciones o acuerdos
  homologados**, **multas procesales** y **cobro de honorarios regulados en concepto de
  costas**. Es la vía para ejecutar honorarios; ver `sede-judicial-pba.md` sección 1.6.6.
- **Arts. 501-502**: liquidación y vista, ya vistos en 21.2.
- **Arts. 504-505**: excepciones y su rigor probatorio, ya vistos en 21.5.

### 21.9 Cierre — verificar antes de responder

1. ¿Está identificado el régimen de ejecución aplicable (21.1)?
2. ¿La liquidación la practicó quien correspondía —Secretario en laboral PBA, parte vencedora
   en el CPCCBA—?
3. ¿Se advirtió que el trámite de observación **no interrumpe** el plazo recursivo?
4. ¿La tasa aplicada es la de la doctrina legal vigente, y no la del segundo párrafo del
   art. 48 declarado inconstitucional en "Abraham"?
5. En causa regida por la 15.057, ¿transcurrieron los **diez días** del art. 60 antes de pedir
   el embargo?
6. ¿La excepción opuesta o admitida está en la lista taxativa que corresponde —siete del
   art. 52 / 64, cuatro del art. 504, o las adicionales del art. 53 / 65—?
7. ¿El documento de pago se acompañó **en el mismo acto** de oponer la excepción?
8. En incidente parcial por rubro firme, ¿se acompañó la certificación de que no está
   comprendido en el recurso?
9. Si se afirma que la denegatoria del incidente es apelable, ¿la causa se rige por la 15.057?
10. ¿Cada monto de la liquidación tiene respaldo verificable, o lleva marcador?
