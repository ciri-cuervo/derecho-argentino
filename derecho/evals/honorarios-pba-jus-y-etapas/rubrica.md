---
titulo: Regulación de honorarios en PBA - cuál de los dos jus, el mínimo del art. 22 y el pago con la escala equivocada
---
## Rúbrica · honorarios-pba-jus-y-etapas

Cada punto es binario: el sistema lo identifica o no.

### Obligatorios

- [ ] Identifica que rige la **Ley 14.967** de la Provincia de Buenos Aires, que derogó el
  Decreto-Ley 8904/77 (art. 63). No aplica la Ley 27.423 ni su UMA, que son de la justicia
  nacional y federal.

- [ ] **Señala que la unidad está mal tomada.** En la tabla de la SCBA conviven el **jus del
  art. 9 de la Ley 14.967** y el **"jus arancelario decreto-ley 8904/77"**, que subsiste porque
  leyes arancelarias de otras profesiones remiten a él. En una regulación a abogados va **el de
  la 14.967**, y confundirlos produce una diferencia del orden del 30%.

- [ ] **Señala que cuatro jus está por debajo del mínimo legal.** El **art. 22** fija que, con
  prescindencia del contenido económico del asunto, la regulación de los profesionales de cada
  parte **no puede ser inferior a siete (7) jus**, cualquiera fuese la actividad y el órgano.
  "Escaso contenido económico" no es causal para bajar de ahí.

- [ ] Señala que **no hay escala laboral separada**: el **art. 43** remite a las disposiciones
  arancelarias generales de la ley para las causas ante Tribunales del Trabajo.

- [ ] Ubica la escala en el **art. 21** —entre el **10% y el 25%**— y advierte que, según el
  **art. 16**, la regulación al vencedor **parte de la media de la escala** y sólo puede
  disminuirse **fundadamente**, respetando los mínimos.

- [ ] **No cita un valor de jus de memoria.** Emite el marcador de monto y remite a la
  resolución de la SCBA vigente a la fecha de la regulación.

- [ ] Ofrece correr **`scripts/honorarios_pba.py`** con el valor del jus que aporte el usuario,
  en vez de calcular a mano.

### Marcadores esperados

- [ ] `[VERIFICAR VIGENCIA]` en la primera mención de la Ley 14.967.
- [ ] `[VERIFICAR MONTO ACTUALIZADO: valor del jus del art. 9 de la Ley 14.967 - resolución de la
  SCBA vigente a la fecha de la regulación]`, o su equivalente canónico.

### Errores que anulan el punto

- [ ] Dar por buena la unidad del decreto-ley 8904/77 para una regulación a abogados.
- [ ] Convalidar los cuatro jus.
- [ ] Citar un valor concreto de jus sin material a la vista.
- [ ] Aplicar la **Ley 27.423** o la **UMA** a esta regulación.
