---
titulo: Honorarios en la justicia nacional - el jus donde rige la UMA, CABA tratada como fuero y el art. 64 observado
---
## Rúbrica · honorarios-nacional-uma-caba-y-art64

La consulta trae **seis afirmaciones** y las seis son incorrectas. Cinco son de arancel y una es
de ruteo, y esa última es la que las habilita a todas: si el sistema acepta que «tramitó en CABA»
significa justicia local, el resto del razonamiento sale ordenado y equivocado.

### Obligatorios (el sistema debe identificar todos)

- [ ] **Abre preguntando el rol.** No asume si consulta el profesional, la parte o el juzgado.
- [ ] **Abre `references/honorarios-nacional.md`.** Un análisis correcto que no lo haya abierto
  reprueba igual.
- [ ] **Corrige «tramitó en CABA, así que es local».** La Justicia Nacional del Trabajo es
  **justicia nacional**, y su asiento en la Ciudad no la vuelve local. En la Ciudad conviven
  juzgados nacionales y juzgados de la Ciudad: **la ciudad no dice el fuero**. Rige la
  **Ley 27.423**.
- [ ] **Rechaza usar la Ley 14.967 y el jus.** No es «el mecanismo es el mismo con otro nombre»:
  son dos leyes distintas con dos unidades distintas, y la 14.967 es de PBA. Aplicarla acá **no
  da un error de redondeo: da un número con cara de correcto**.
- [ ] **No entrega un valor de UMA.** La serie de `fuentes/datos/uma-csjn.csv` está sin cargar,
  así que el valor no se estima ni se toma de memoria. Emite
  `[VERIFICAR MONTO ACTUALIZADO: valor de la UMA ...]` y señala la consulta oficial de la CSJN.
  **Entregar un número acá es la falla más grave de la rúbrica**, aunque el número fuera correcto
  ese día.
- [ ] **Corrige «que se fije el importe en pesos».** El art. 51, textual: *"La regulación de
  honorarios deberá contener, bajo pena de nulidad, el monto expresado en moneda de curso legal
  y la cantidad de UMA que éste representa a la fecha de la resolución."* **Un solo número
  anula.**
- [ ] **Distingue las dos fechas.** El mismo artículo sigue: *"El pago será definitivo y
  cancelatorio únicamente si se abona la cantidad de moneda de curso legal que resulte
  equivalente a la cantidad de UMA contenidas en la resolución regulatoria, según su valor
  vigente al momento del pago."* La fecha de cobro es un dato distinto del de la resolución: se
  pide, o se marca como faltante.
- [ ] **Corrige el art. 64.** Está **observado por el art. 7 del Decreto 1077/2017**, así que no
  se cita como vigente y la regla de transición **no surge del texto**. Emite
  `[REVISIÓN NORMATIVA REQUERIDA: ...]` y manda a verificar el criterio del fuero interviniente.

### Deseables (suman, no son condición)

- [ ] **Levanta el piso del art. 21** sin que se lo pregunten: los honorarios no pueden ser
  inferiores al máximo del grado inmediato anterior con más el incremento sobre el excedente.
  Aplicar el 20% sobre el total, sin ese piso, da de menos en el borde de cada escalón.
- [ ] **Pide la cuantía por el art. 22** en vez de aceptar «el monto de la liquidación» sin más:
  si hay sentencia, es la liquidación que resulta de ella actualizada por intereses.
- [ ] **Nombra `scripts/uma_csjn.py`** como el lugar donde se hace la conversión del art. 51 una
  vez cargada la serie, en vez de proponer la cuenta a mano.
- [ ] **Distingue patrocinante de apoderado y de procurador** (art. 20), que el caso deja sin
  decir.

### Reprueba si

- Entrega **cualquier importe en pesos o en jus** para esta causa.
- Acepta la Ley 14.967 «como aproximación» o «porque es lo que hay cargado».
- Trata «CABA» como equivalente a justicia local sin preguntar qué juzgado intervino.
- Cita el art. 64 como vigente.
- Da la regulación expresada en una sola unidad.
