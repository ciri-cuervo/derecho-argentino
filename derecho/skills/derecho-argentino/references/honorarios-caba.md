# Honorarios en la justicia local de la Ciudad · Ley 5.134

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

Cotejado contra `fuentes/normas/caba-ley-5134.txt`, texto consolidado al 29/02/2024 por la Ley
6.764.

**Rige en el Poder Judicial de la Ciudad, no en los juzgados nacionales con asiento en CABA.** Una
causa laboral o civil que tramita en Capital va por la **Ley 27.423** y su UMA: eso está en
`honorarios-nacional.md` 37. La puerta que decide cuál se aplica es la de
`/derecho:honorarios`, y se resuelve por el fuero, nunca por la ciudad.

## 42 · Arancel de la justicia de la Ciudad Autónoma de Buenos Aires

### 42.1 La UMA porteña no es la UMA nacional

**Se llaman igual y son unidades distintas.** Es el error más caro de la materia, porque el
resultado sale expresado en «UMA» de todos modos.

| | Ley 5.134 CABA, art. 20 | Ley 27.423 nacional, art. 19 |
| --- | --- | --- |
| Porcentaje | **1,5%** | **3%** |
| Base | remuneración **total** de un juez de 1ª instancia **de la Ciudad** | remuneración **básica** de un juez **federal** de 1ª instancia |
| Qué integra la base | *"la suma de todos aquellos rubros, sea cual fuere su denominación, incluida la bonificación por antigüedad de cinco años"* | la básica, sin más |
| Quién publica el valor | **Consejo de la Magistratura de CABA**, mensualmente; el **CPACF** lo informa a las Cámaras | **la CSJN**, mensualmente |

**La última fila es la que se paga más caro:** buscar el valor de la UMA porteña en la página de la
Corte devuelve un número oficial, vigente y de otra ley.

`[VERIFICAR MONTO ACTUALIZADO: valor de la UMA de la Ley 5.134 - lo suministra mensualmente el Consejo de la Magistratura de la Ciudad, art. 20. La serie no está cargada en fuentes/datos/, así que el valor no se toma de memoria ni se estima: se pide o se marca. Y NO se usa el valor que publica la CSJN, que es el de la Ley 27.423]`

### 42.2 La escala y sus dos topes

**Procesos susceptibles de apreciación pecuniaria, primera instancia hasta la sentencia: entre el
11% y el 25% del monto** (art. 23). Dos límites que se olvidan:

- **Litisconsorcio:** la regulación se hace **con relación al interés de cada litisconsorte**.
- **Tope global:** las regulaciones **no superarán en total el cincuenta por ciento** del monto del
  proceso.

**Mínimos cuando el juicio no está previsto en otro artículo** (art. 60): **10 UMA** en procesos de
conocimiento, **6 UMA** en ejecutivos y **2 UMA** en mediación.

### 42.3 Cómo se determina la cuantía

**Cobro de sumas de dinero (art. 24):** el monto de la **liquidación que resulte de la sentencia o
transacción** por capital actualizado si correspondiere **e intereses**. La actualización y los
intereses fijados en la sentencia integran la base.

**Inmuebles sin tasar en autos (art. 25 inc. a):** se toma la **valuación fiscal**.

**Liquidación de la sociedad conyugal (art. 47):** la escala del art. 23 **sobre el activo**.

### 42.4 La regulación tiene que estar fundada, bajo pena de nulidad

**Art. 16:** toda regulación debe fundarse y hacerse **con citación de la disposición legal
aplicada, bajo pena de nulidad**, y **la mera mención del articulado de esta ley no es fundamento
válido**. Es un requisito de forma más exigente que el del art. 51 de la Ley 27.423 y se controla
distinto: no se mira si están las dos expresiones del monto, se mira si el auto explica por qué.

### 42.5 Pago, mora y recurso

- **Pago: diez días** de quedar firme el auto regulatorio; los extrajudiciales, diez días de
  intimado el pago cuando sean exigibles (art. 56). Vencido el plazo, la mora opera **de pleno
  derecho**.
- **Notificación y apelación (art. 58):** el auto se notifica al beneficiario y al obligado al pago
  de modo fehaciente, y es **apelable dentro de los cinco días**, pudiendo fundarse el recurso en
  el acto de deducirlo.

### 42.6 Aplicación temporal

**Art. 62:** la ley se aplica **a todos los procesos en curso en los que no haya regulación firme**
al tiempo de su publicación, y la cláusula transitoria la extiende a los fueros que integren el
Poder Judicial de la Ciudad en el futuro.

**Es la diferencia con el régimen nacional, y conviene tenerla presente:** el art. 64 de la Ley
27.423, que decía algo equivalente, **está observado por el Decreto 1077/2017** y por eso allá la
transición no surge del texto. Acá sí.

### 42.7 Lo que este módulo NO hace

- **No calcula.** Falta la serie de valores de la UMA porteña, así que no hay número. La
  calculadora determinista existe sólo para PBA.
- **No cubre las etapas ni la segunda instancia** más allá de lo nombrado.
- **No trae los aranceles del Consejo de la Magistratura de la Ciudad** ni la reglamentación del
  CPACF.

`[INSERTAR FALLO VERIFICADO: no hay precedente bajado sobre la Ley 5.134 - en particular sobre la nulidad por falta de fundamentación del art. 16 y sobre el tope global del cincuenta por ciento del art. 23 - aportar carátula, sala, expediente, fuero y año]`

### 42.8 Qué preguntar antes de regular

1. **Si el juzgado es de la Ciudad o nacional**, que es la pregunta y no en qué ciudad queda.
2. **El valor de la UMA porteña a la fecha**, y de la fuente correcta: el Consejo de la Magistratura
   de CABA, no la CSJN.
3. **La cuantía por el art. 24**, que es la liquidación con sus intereses y no el monto de demanda.
4. **Si hay litisconsorcio**, por el interés de cada uno y por el tope del cincuenta por ciento.
5. **Si ya hay regulación firme**, por el art. 62.
