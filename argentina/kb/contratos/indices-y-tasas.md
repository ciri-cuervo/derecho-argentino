# Índices y tasas de referencia · Derecho argentino

> Archivo de configuración para el sistema derecho-argentino.
> Parámetros de referencia para evaluar actualización de créditos, abusividad
> de intereses y cláusulas de ajuste en contratos y escritos judiciales.
>
> Cargar junto con el perfil de área correspondiente cuando la tarea involucre:
> - Liquidación de créditos con intereses
> - Evaluación de cláusulas de actualización o de intereses en contratos
> - Detección de anatocismo o tasas usurarias
> - Redacción de liquidaciones en escritos judiciales
>
> **Regla general:** los valores numéricos de este archivo son de referencia.
> Los índices y tasas cambian periódicamente. Ante cualquier liquidación concreta,
> verificar el valor vigente en la fuente oficial antes de calcular.

---

## Alerta normativa - vigencia variable

*Última verificación de esta sección: mayo 2026.*
*Las tasas del BCRA, los índices del INDEC y las tasas judiciales se actualizan
con frecuencia. Este archivo provee la lógica de evaluación, no los valores exactos.*

---

## Índices de actualización - referencia por tipo de obligación

### Contratos civiles y comerciales

| Índice | Fuente | Uso habitual |
|---|---|---|
| IPC (Índice de Precios al Consumidor) | INDEC | Actualización general de obligaciones civiles y comerciales |
| ICL (Índice de Contratos de Locación) | BCRA | Locaciones bajo régimen Ley 27.551 (contratos 2020-2023); opcional en contratos post-DNU |
| RIPTE (Remuneración Imponible Promedio de los Trabajadores Estables) | Secretaría de Seguridad Social | Obligaciones laborales; también usado en contratos de servicios con componente salarial |
| UVA (Unidad de Valor Adquisitivo) | BCRA | Créditos hipotecarios UVA; contratos con cláusula de ajuste UVA |
| CVS (Coeficiente de Variación Salarial) | INDEC | Actualización de créditos laborales en algunos fueros |

**Regla operativa para contratos post-DNU 70/2023:** las partes tienen libertad para pactar cualquier índice. Si el contrato no especifica índice: marcar como `[RED FLAG - RIESGO ALTO: ausencia de mecanismo de actualización]`. Si el índice pactado es el dólar u otra divisa: agregar `[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE: normativa BCRA]`.

### Obligaciones laborales - índices aplicables

| Concepto | Índice / Tasa |
|---|---|
| Actualización de créditos laborales (general) | RIPTE o índice que fije el CCT aplicable |
| Indemnización por despido - base de cálculo | Mejor remuneración mensual normal y habitual (art. 245 LCT) |
| Intereses sobre créditos laborales (CNAT) | Tasa activa del Banco Nación (criterio plenario "Recurso de hecho Gómez, Carla c/ Witcel" y sus antecedentes) - verificar plenario vigente |
| Intereses sobre créditos laborales (SCBA) | Tasa pasiva del BCRA más un adicional - verificar acuerdo de la SCBA vigente |

```
[VERIFICAR TASA JUDICIAL VIGENTE: las tasas de interés aplicables a créditos
 laborales se fijan por acuerdo o plenario del fuero. Verificar el criterio
 vigente en la Cámara competente antes de liquidar]
```

---

## Intereses - evaluación de abusividad y anatocismo

### Marco normativo

**Art. 767 CCCN [VERIFICAR VIGENCIA]:** los intereses compensatorios pueden ser convenidos libremente. Si no se convienen o resultan nulos, se aplica la tasa que fijen las leyes especiales o, en subsidio, la tasa pasiva promedio del BCRA.

**Art. 768 CCCN [VERIFICAR VIGENCIA]:** intereses moratorios. A falta de acuerdo, se aplica la tasa que fijen las leyes especiales; en subsidio, la tasa activa del BCRA.

**Art. 770 CCCN [VERIFICAR VIGENCIA] - anatocismo:** prohibido el anatocismo (interés sobre interés) salvo:
- Acuerdo expreso entre partes posterior al vencimiento de la obligación
- Demanda judicial: desde la notificación, los intereses se capitalizan anualmente
- Obligaciones de ejecución periódica con cuota que comprende capital e intereses

**Art. 771 CCCN [VERIFICAR VIGENCIA] - facultad judicial de morigeración:** los jueces pueden reducir los intereses pactados cuando la tasa excede, sin justificación, el costo medio del dinero para deudores y operaciones similares. El criterio aplicado por la jurisprudencia es la comparación con la tasa activa del Banco Nación o la tasa de mercado para operaciones similares.

**Art. 332 CCCN [VERIFICAR VIGENCIA] - lesión:** una tasa de interés que configure explotación de la necesidad, inexperiencia o ligereza del deudor puede dar lugar a la acción de lesión. El vicio no se presume; debe ser acreditado.

### Criterios judiciales de referencia por fuero

**Fuero Civil y Comercial Nacional (CNCIV / CNACOM)**

```
[INSERTAR FALLO VERIFICADO: tasa de interés moratorio aplicable - verificar
 plenario o acuerdo de cámara vigente en CNCIV/CNACOM - aportar número y fecha]
```

Referencia histórica (verificar si sigue vigente): la CNACOM aplicó la tasa activa del Banco Nación para obligaciones en pesos. La CNCIV tuvo criterios variables. Ante cualquier liquidación, verificar el criterio vigente antes de calcular.

**Fuero Laboral Nacional (CNAT)**

```
[INSERTAR FALLO VERIFICADO: tasa de interés laboral - verificar plenario
 o acuerdo de cámara vigente en CNAT - aportar número y fecha]
```

Referencia histórica: la CNAT aplicó la tasa activa del Banco Nación (criterio "Recurso de hecho Goméz"). Verificar si fue modificado por acuerdo posterior.

**Fuero Civil y Comercial de la Provincia de Buenos Aires (SCBA)**

```
[INSERTAR FALLO VERIFICADO: tasa de interés aplicable - verificar acuerdo
 de la SCBA vigente - aportar número y fecha]
```

Referencia histórica: la SCBA fijó tasas por acuerdo periódico. El criterio varió entre tasa pasiva más adicional y tasa activa según el período. Siempre verificar el acuerdo vigente.

### Alerta de abusividad - regla operativa

Al revisar un contrato, evaluar la tasa de interés pactada contra el siguiente criterio:

```
Tasa pactada > 3 veces la tasa activa del Banco Nación para operaciones similares
→ [RED FLAG - RIESGO ALTO: tasa de interés potencialmente abusiva - verificar
   criterio del fuero competente y posibilidad de morigeración judicial (art. 771 CCCN)]
```

Este umbral es orientativo. La calificación final depende del fuero, el tipo de operación y el perfil del deudor. No aplicar mecánicamente: consignar la alerta y derivar al abogado.

Si el contrato prevé capitalización de intereses sin encuadrar en alguna de las excepciones del art. 770 CCCN:

```
[RED FLAG - NULIDAD ABSOLUTA: cláusula de anatocismo fuera de los supuestos
 del art. 770 CCCN - norma: art. 770 CCCN [VERIFICAR VIGENCIA]]
```

---

## Obligaciones en moneda extranjera - índices y contingencias

### Régimen post-DNU 70/2023 (obligaciones nacidas desde 30-dic-2023)

El deudor debe pagar en la moneda pactada (arts. 765-766 CCCN reformados). Si hay restricciones cambiarias que impidan el acceso a divisas, el deudor no queda automáticamente liberado: la imposibilidad de pago en moneda extranjera por causas regulatorias puede encuadrar en teoría de la imprevisión (art. 1091 CCCN [VERIFICAR VIGENCIA]) o frustración del fin del contrato (art. 1090 CCCN [VERIFICAR VIGENCIA]), pero requiere análisis caso por caso.

**Recomendación de redacción para contratos en moneda extranjera:**
Incluir cláusula de contingencia cambiaria que prevea un mecanismo alternativo de pago ante restricciones del BCRA. Opciones habituales en la práctica contractual argentina 2024-2026:
- Pago al tipo de cambio MEP o CCL publicado por una entidad de referencia pactada
- Pago en pesos al tipo de cambio libre publicado por [fuente pactada] al día del vencimiento
- Depósito en cuenta en el exterior del acreedor

```
[CLÁUSULA RECOMENDADA: contingencia cambiaria - el contrato en moneda extranjera
 debería prever un mecanismo alternativo ante restricciones del BCRA para evitar
 controversias sobre imposibilidad de pago]
```

### Conversión histórica para liquidaciones

Para contratos anteriores al 30-dic-2023 que todavía están en ejecución y donde el deudor invoque el régimen original del art. 765 CCCN (pago en moneda nacional al tipo de cambio oficial):

```
[VERIFICAR RÉGIMEN APLICABLE: obligación en moneda extranjera pre-30-dic-2023 -
 verificar si el deudor puede cancelar en pesos al tipo de cambio oficial del BCRA
 según art. 765 CCCN original - contrastar con fecha de origen de la obligación]
```

**Alerta - doctrina del "esfuerzo compartido":** bajo el régimen original del art. 765 CCCN, la jurisprudencia desarrolló la doctrina del esfuerzo compartido: ante la brecha entre el tipo de cambio oficial y el de mercado, algunos tribunales distribuyeron esa diferencia entre las partes en lugar de aplicar mecánicamente el tipo oficial. Esta doctrina es inaplicable a obligaciones nacidas post-30-dic-2023 (régimen reformado: el deudor debe pagar en la moneda pactada). Para contratos pre-DNU en ejecución donde el deudor la invoque:

```
[INSERTAR FALLO VERIFICADO: doctrina del esfuerzo compartido - verificar
 criterio vigente en el fuero competente - aportar sala, número y año]
```

---

## Índices para actualización de indemnizaciones - referencia

### Accidentes de tránsito y daños (fuero civil)

La actualización del valor del daño desde la fecha del hecho hasta la sentencia o liquidación se practica habitualmente con IPC. El fuero civil nacional y provincial admite la actualización por vía de intereses o por indexación directa según el criterio del tribunal.

```
[INSERTAR FALLO VERIFICADO: criterio de actualización del valor del daño
 aplicable en el fuero y jurisdicción competente - aportar sala, número y año]
```

### Honorarios profesionales

Los honorarios regulados judicialmente se actualizan por las reglas de la ley de honorarios aplicable al fuero. Para honorarios contractuales: aplicar el índice pactado; a falta de pacto, IPC desde la fecha de la obligación.

```
[VERIFICAR LEY DE HONORARIOS APLICABLE: la ley de honorarios del fuero
 puede prever un índice específico de actualización - verificar antes de liquidar]
```

---

## Instrucciones operativas

- Ante cualquier liquidación de intereses en un escrito judicial: verificar la tasa vigente en el fuero antes de calcular. No usar tasas de referencia históricas sin confirmación.
- Ante una cláusula de intereses en un contrato: correr la regla de abusividad (umbral 3x tasa activa BNA) y, si supera el umbral, consignar la alerta.
- Ante cláusula de anatocismo: verificar si encuadra en alguna excepción del art. 770 CCCN antes de marcar como nulidad absoluta.
- Ante contrato en moneda extranjera post-DNU: verificar si incluye cláusula de contingencia cambiaria. Si no incluye: consignar `[CLÁUSULA RECOMENDADA]`.
- Los `[INSERTAR FALLO VERIFICADO]` de este archivo no pueden ser resueltos por el sistema sin material aportado por el abogado. Consignarlos en "Estado del análisis" como marcadores pendientes.

---

*Última actualización: mayo 2026*
*Normativa base: CCCN (Ley 26.994) arts. 332, 767, 768, 770, 771, 1090, 1091; arts. 765-766 reformados por DNU 70/2023; LCT (Ley 20.744) art. 245*
*Fuentes de tasas: BCRA, INDEC, Secretaría de Seguridad Social*
*Las tasas judiciales de referencia requieren verificación en el fuero competente antes de cualquier liquidación*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
