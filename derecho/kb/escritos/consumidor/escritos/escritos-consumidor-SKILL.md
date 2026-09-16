---
name: escritos-consumidor
description: Redacta escritos de derecho del consumidor argentino (amparo de salud por prepaga, demanda de daños y daño punitivo, demanda por garantía y producto defectuoso, reclamo administrativo ante la Ventanilla Única Federal / OMIC). Activar ante cualquier pedido de redacción de un escrito de consumo, aunque el usuario no nombre el modelo. Trabaja junto con el perfil kb/perfiles/consumidor-CLAUDE.md.
---

# Escritos de consumo

> Parte del repositorio de conocimiento jurídico argentino.
> Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)

---

## Descripción

Redacta escritos de consumo para abogados matriculados. El abogado firma y asume la responsabilidad profesional de cada pieza. Este skill redacta; el abogado revisa y decide. Opera siempre junto con el perfil `kb/perfiles/consumidor-CLAUDE.md`, que aporta la lógica de fondo (fueros, institutos, alertas normativas).

---

## Cuándo usar

Activar cuando el usuario pida redactar o preparar un escrito de consumo: amparo por aumento o baja de prepaga, demanda de daños y daño punitivo, demanda por garantía o producto defectuoso, o reclamo administrativo. No es necesario que nombre el modelo.

No activar para el solo análisis estratégico o de viabilidad sin redacción: para eso alcanza el perfil `kb/perfiles/consumidor-CLAUDE.md`.

---

## Proceso

### Paso 1 - Encuadre y datos

Antes de redactar, definir con el usuario:

- Pretensión: cese/cobertura urgente, resarcimiento (con o sin daño punitivo), cumplimiento de garantía, o reclamo administrativo previo.
- Urgencia: si hay riesgo de baja, exclusión o corte de una prestación de salud en curso, la vía es el amparo, no el reclamo de consumo ni la acción ordinaria.
- Cuantía y jurisdicción: definen el fuero (Justicia de Consumo, Comercial nacional, CCF, CAyTyC porteño, justicia provincial).
- Componente de discapacidad: si se reclama una prestación bajo Ley 24.901, el encuadre principal se deriva al perfil de discapacidad y el escrito de consumo opera como refuerzo.
- Material disponible: contrato, comprobantes, comunicaciones, constancias de reclamos. Sin material, los hechos van con marcador, no se asumen.

### Paso 2 - Verificación normativa (no opcional)

Antes de incluir cualquier cita, leer la sección `## Alerta normativa - normas de vigencia variable` de `kb/perfiles/consumidor-CLAUDE.md` y aplicar sus reglas. Puntos críticos:

- Tope del daño punitivo: 2.100 CBT tipo 3 del INDEC (texto Ley 27.701), nunca el monto fijo derogado de $5.000.000. Recalcular con la CBT del mes de la demanda.
- Prescripción de la acción de daños de consumo contractual: 5 años (art. 2560 CCyC), no el art. 50 LDC (3 años, solo sanciones administrativas).
- DNU 70/2023: vigente; sostener la revisión por abusividad de los aumentos de prepaga pese a la desregulación.
- COPREC: disuelto; no citarlo. La conciliación o mediación prejudicial local (CABA, PBA) sigue siendo recaudo de admisibilidad.
- Garantía legal: distinguir de la comercial; la opción del art. 17 es del consumidor.

### Paso 3 - Elegir el modelo

Leer el modelo que corresponda y redactar sobre su estructura:

| Situación | Modelo |
|---|---|
| Intimación extrajudicial fehaciente previa (carta documento): cumplir oferta, garantía, devolución, cese de cobro, rechazo de aumento de prepaga, revocación, cobranza abusiva, etc. | `modelos/kb/escritos/consumidor/escritos/modelos/cartas-documento-intimaciones.md` (bloque de variantes) |
| Urgencia: aumento abusivo, baja o exclusión de cobertura de prepaga u obra social nacional | `modelos/kb/escritos/consumidor/escritos/modelos/amparo-salud-prepaga.md` |
| Daño ya causado en relación de consumo, con o sin daño punitivo | `modelos/kb/escritos/consumidor/escritos/modelos/demanda-dano-punitivo.md` |
| Producto defectuoso o garantía legal (opción del art. 17) | `modelos/kb/escritos/consumidor/escritos/modelos/demanda-garantia-producto.md` |
| Reclamo administrativo previo / conciliación | `modelos/kb/escritos/consumidor/escritos/modelos/reclamo-ventanilla-omic.md` |

Si el caso combina urgencia y resarcimiento, separar: amparo para la urgencia (cautelar ex nunc) y acción ordinaria para el daño ya causado.

---

## Reglas de integridad (inmodificables)

- Jurisprudencia: prohibido citar carátula, sala, año o expediente sin material aportado. Usar `[INSERTAR FALLO VERIFICADO: doctrina requerida]`. Los fallos ya verificados en el perfil (Halabi, PADEC, Cainelli, Morsentti, Machinandiarena) pueden citarse, indicando que se verifique el texto íntegro antes de transcribir.
- Hechos: no asumir nada que no figure en el material. Usar `[VACÍO PROBATORIO: descripción]`.
- Normas: en la primera mención, `[VERIFICAR VIGENCIA]`. Si se sabe derogada o modificada, informarlo y proponer la vigente.
- Tope del daño punitivo: solo en CBT del INDEC; el marcador recae sobre el valor de la CBT, no sobre la fórmula.

---

## Restricciones absolutas

- No inventar hechos no aportados por el usuario.
- No citar el COPREC como instancia vigente.
- No cuantificar el daño punitivo con el monto fijo derogado.
- No aplicar el art. 50 LDC como plazo de la acción civil de daños.
- No tramitar una urgencia de salud como reclamo de consumo de baja cuantía.
- No subsumir una cobertura por discapacidad (Ley 24.901) en la lógica de consumo.

---

## Racionalizaciones comunes

| Racionalización | Realidad |
|---|---|
| "Por el DNU 70/23 el aumento de prepaga es inatacable" | La desregulación es comercial; el aumento desproporcionado sigue siendo revisable por abusividad (art. 1122 CCyC) y abuso del derecho (art. 10 CCyC). |
| "La acción de daños del consumidor prescribe a los 3 años (art. 50 LDC)" | El art. 50 rige solo las sanciones administrativas desde la Ley 26.994. La acción de daños contractual prescribe a 5 años (art. 2560 CCyC). |
| "El tope del daño punitivo es $5.000.000" | Derogado. Hoy es 2.100 CBT del INDEC (Ley 27.701); se recalcula con la canasta del mes. |
| "Caído el COPREC, se puede demandar sin instancia previa" | En CABA y PBA la conciliación o mediación prejudicial sigue siendo recaudo de admisibilidad. |
| "La opción del art. 17 la elige el proveedor" | La elección entre sustitución, devolución o quita es del consumidor. |
| "Si el afiliado tiene discapacidad, basta el encuadre de consumo" | La prestación bajo Ley 24.901 se rige por el perfil de discapacidad; consumo es refuerzo. |

---

## Señales de alerta

Indicadores de que el borrador está mal antes de entregarlo:

- Cuantificar el daño punitivo en $5.000.000 o en un monto fijo.
- Afirmar que la acción prescribió a los 3 años por el art. 50 LDC.
- Citar el COPREC como instancia conciliatoria vigente.
- Encuadrar una urgencia de salud como reclamo de baja cuantía.
- Pedir cautelar retroactiva por diferencias ya pagadas.
- Citar un fallo con carátula y sala sin material aportado, fuera de los verificados en el perfil.

---

## Verificación al cierre

Antes de entregar el borrador:

- [ ] Pretensión y vía correctas (amparo / ordinaria / garantía / administrativa)
- [ ] Fuero determinado por cuantía y jurisdicción; mudanza competencial CABA verificada si aplica
- [ ] Sección de alerta normativa de `kb/perfiles/consumidor-CLAUDE.md` consultada (Paso 2)
- [ ] Modelo correspondiente leído (Paso 3)
- [ ] Tope del daño punitivo en CBT, con marcador del valor a la fecha
- [ ] Prescripción quinquenal aplicada; no art. 50 LDC
- [ ] Instancia conciliatoria previa local considerada
- [ ] Marcadores de integridad colocados (fallos, hechos, normas)
- [ ] Cierre con "Estado del escrito"

---

*Última actualización: junio 2026*
*Normativa base: art. 42 CN, Ley 24.240 (texto Ley 27.701 para multas en CBT), CCyC arts. 10 y 1092-1122, Ley 26.682, DNU 274/2019, Ley 26.993; perfil de fondo en kb/perfiles/consumidor-CLAUDE.md*
