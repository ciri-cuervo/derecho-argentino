# Marcadores · vocabulario controlado

> Módulo de referencia de la skill `derecho-argentino`. Los marcadores son **identificadores
> funcionales**, no prosa: los scripts los emiten, las salidas se auditan contra ellos y los
> comandos los buscan por texto exacto. Una paráfrasis rompe el sistema. Las reglas de
> integridad de la sección 2 rigen acá también.

## Para qué existen

Un marcador es la forma de decir **qué falta** sin inventar lo que falta. Es la alternativa a
la estimación plausible, que es el modo en que una skill de derecho se equivoca en silencio.

Tres reglas que no se relajan:

1. **Ante la duda, marcador.** Nunca un número, un plazo o un fallo "aproximado".
2. **La sintaxis es la de esta lista, exacta.** Un marcador inventado no lo detecta nadie.
3. **El marcador va donde se usa el dato**, no en una nota al pie. Quien lee el escrito tiene
   que tropezarse con él.

Un escrito puede salir con marcadores. Lo que no puede salir es un escrito con un dato sin
respaldo y sin marcador.

---

## A · Integridad normativa

### A1 · VERIFICAR VIGENCIA

Primera mención de cualquier norma, sin excepción.

```
[VERIFICAR VIGENCIA]
[VERIFICAR VIGENCIA: motivo específico]
```

El motivo se agrega cuando se sabe por qué hay que mirar, y **va en una sola línea**, porque el
marcador se copia literal:

`[VERIFICAR VIGENCIA: texto del articulo a la fecha del acto extintivo - antecedentes normativos si es anterior a la sustitucion]`

> **Una sola línea, con dos excepciones.** Los 24 marcadores de las series A, B y C se escriben en
> una línea. **D2 y D3 son de dos líneas por diseño** —así están en el glosario heredado del que se
> transcriben— y así hay que dejarlos: no son un error de formato. Si un marcador aparece partido
> en cualquier otra serie, es reflujo de texto y se junta. Y ojo con los marcadores dentro de una
> cita de bloque: si el corte cae adentro, el `>` queda incrustado en el texto del marcador.

### A2 · NORMA DESACTUALIZADA

Cuando se detecta una norma citada que ya fue reemplazada y se conoce la que rige.

```
[NORMA DESACTUALIZADA: norma citada - reemplazar por: norma vigente [VERIFICAR VIGENCIA]]
```

El marcador anidado no es un error de tipeo: la norma de reemplazo también se verifica.

### A3 · REVISIÓN NORMATIVA REQUERIDA

Cuando el estado de la norma no se resuelve mirando su texto — está en litigio, suspendida,
o hay dos regímenes conviviendo.

```
[REVISIÓN NORMATIVA REQUERIDA: descripción de lo que se necesita verificar]
```

### A4 · VERIFICAR MONTO ACTUALIZADO

Todo importe que se mueve: topes, pisos, multas, umbrales, canastas.

```
[VERIFICAR MONTO ACTUALIZADO: concepto - fuente de actualización]
```

### A5 · VERIFICAR TASA VIGENTE

```
[VERIFICAR TASA VIGENTE: fuero - instrumento que la fija]
```

La tasa nunca se recuerda: sale del instrumento que la fija, y el fuero es parte del dato.

### A6 · VERIFICAR RÉGIMEN CAMBIARIO VIGENTE

Obligaciones en moneda extranjera, antes de aconsejar sobre forma de pago.

```
[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE: normativa BCRA - verificar antes de aconsejar sobre esta obligación]
```

### A7 · VERIFICAR RESOLUCIÓN REGISTRAL VIGENTE

Requisitos que fija un organismo registral por resolución, no por ley.

```
[VERIFICAR RESOLUCIÓN REGISTRAL VIGENTE: organismo - materia]
```

### A8 · VERIFICAR CRITERIO DEL FUERO

Cuando el resultado no depende del texto de la norma sino de cómo lo aplica el tribunal que
va a intervenir: cómo se cuantifica, qué rubros se admiten por separado, qué agravante
prospera, y todo criterio que todavía no esté firme.

```
[VERIFICAR CRITERIO DEL FUERO: materia - fuero o sala]
```

**Nunca** `[VERIFICAR CRITERIO DE LA SALA]` ni `[VERIFICAR FÓRMULA VIGENTE]`.

### A9 · VERIFICAR CCT APLICABLE

El CCT no es dato de cartera: surge de lo que las partes invocan y prueban.

```
[VERIFICAR CCT APLICABLE: actividad del empleador - dato que falta]
```

### A10 · ALERTA PLAZO FATAL

Sólo para los plazos que matan el reclamo: caducidades y prescripciones. Si vencido el plazo
todavía hay algo que reclamar, este marcador no corresponde.

```
[ALERTA PLAZO FATAL: norma - plazo - fecha de inicio del cómputo - vencimiento estimado]
```

Los cuatro campos van completos. Un plazo fatal sin fecha de inicio no es una alerta, es un
comentario.

### A11 · VERIFICAR PLAZO

Plazos procesales o administrativos ordinarios cuyo valor varía por jurisdicción o código
local. **Distinto de A10**: acá el vencimiento no extingue el derecho.

```
[VERIFICAR PLAZO: acto procesal - norma de la jurisdicción]
```

No combinar A11 con A1 en un mismo corchete.

---

## B · Integridad probatoria

### B1 · INSERTAR FALLO VERIFICADO

Hace falta un precedente y no hay uno verificado a mano. **No se inventa la carátula.**

```
[INSERTAR FALLO VERIFICADO: doctrina requerida - aportar expediente, sala, fuero y año]
```

### B2 · JURISPRUDENCIA VERIFICADA EN SESIÓN

Un fallo que se verificó contra fuente oficial durante la sesión y por eso puede citarse.

```
[JURISPRUDENCIA VERIFICADA EN SESIÓN: "carátula" - sala, fuero, año - doctrina: resumen]
```

### B3 · VACÍO PROBATORIO

Un hecho se afirma y no hay con qué acreditarlo.

```
[VACÍO PROBATORIO: hecho afirmado - prueba necesaria para acreditarlo]
```

Nombrar la **prueba** concreta que falta, no "falta prueba".

### B4 · VERIFICAR CITA DE FALLOS

El holding y la fecha están verificados; falta la cita formal.

```
[VERIFICAR CITA DE FALLOS: "carátula" - fecha y holding verificados - completar tomo:página contra fuente oficial]
```

### B5 · VERIFICAR PRECEDENTE

El fallo existe y la cita es correcta, pero falta confirmar que **todavía manda**: que la
doctrina no haya caído después, por el propio tribunal o por uno superior.

```
[VERIFICAR PRECEDENTE: "carátula" o Fallos T:P - confirmar que no fue dejado sin efecto ni superado antes de citar]
```

---

## C · Integridad del escrito

### C1 · ARG SIN NORMA

Un argumento que se sostiene solo, sin norma que lo respalde.

```
[ARG SIN NORMA: paráfrasis del argumento - norma que correspondería citar: sugerencia o "indeterminada"]
```

### C2 · PETICIÓN SIN FUNDAMENTO

Algo se pide en el petitorio y no se desarrolló en los fundamentos.

```
[PETICIÓN SIN FUNDAMENTO: texto de la petición - desarrollar en fundamentos: descripción de lo que falta]
```

### C3 · CONTRADICCIÓN

Dos partes del mismo escrito, o del mismo material, dicen cosas incompatibles.

```
[CONTRADICCIÓN: sección A dice: "paráfrasis" / sección B dice: "paráfrasis" - resolución necesaria: indicación]
```

### C4 · AVANCE BAJO RESERVA

Se siguió adelante con un hecho sin respaldo **porque el abogado lo pidió**, y consta que se
le informó.

```
[AVANCE BAJO RESERVA: descripción del hecho - el abogado fue informado de la ausencia de respaldo]
```

---

## D · Diagnóstico y configuración

### D1 · CONFIGURACIÓN INCOMPLETA

```
[CONFIGURACIÓN INCOMPLETA: campo - impacto en el análisis]
```

El **impacto** es obligatorio: decir qué no se puede hacer sin ese dato.

### D2 · SIN PERFIL DE ÁREA CARGADO

```
[SIN PERFIL DE ÁREA CARGADO: el diagnóstico se realizó con conocimiento normativo general.
Cargar el perfil del área para un análisis completo]
```

### D3 · DISCREPANCIA ENTRE FUENTES

```
[DISCREPANCIA ENTRE FUENTES: el conector X indica A / la fuente primaria indica B.
Verificar directamente en la fuente oficial]
```

Ante discrepancia manda siempre la fuente primaria.

### D4 · RED FLAG - NULIDAD ABSOLUTA

```
[RED FLAG - NULIDAD ABSOLUTA: descripción de la cláusula - norma: norma aplicable [VERIFICAR VIGENCIA]]
```

### D5 · RED FLAG - RIESGO ALTO

```
[RED FLAG - RIESGO ALTO: descripción de la cláusula - observación: descripción del problema]
```

### D6 · RED FLAG - RIESGO MEDIO

```
[RED FLAG - RIESGO MEDIO: descripción de la situación]
```

Los tres de red flags se usan en el análisis de contratos de `contratos.md` 7.

---

## Formas que no son marcadores

Estas aparecen por costumbre y hay que reemplazarlas:

| No usar | Usar |
|---|---|
| `[VERIFICAR]` | `[VERIFICAR VIGENCIA]` |
| `[VERIFICAR MONTO]`, `[VERIFICAR MONTO VIGENTE]` | `[VERIFICAR MONTO ACTUALIZADO: ...]` |
| `[VERIFICAR VIGENCIA Y MONTO]` | A1 **y** A4, en corchetes separados |
| `[VERIFICAR TASA VIGENTE]` sin fuero | `[VERIFICAR TASA VIGENTE: fuero - instrumento que la fija]` |
| `[VERIFICAR CRITERIO DE LA SALA]`, `[VERIFICAR FÓRMULA VIGENTE]` | `[VERIFICAR CRITERIO DEL FUERO: ...]` |
| `[VERIFICAR CCT APLICABLE]` sin detalle | con actividad y dato faltante |
| `[VACÍO DOCUMENTAL]`, `[VACÍO CUANTIFICATIVO]` | `[VACÍO PROBATORIO: ...]` |
| `[ALERTA DE PLAZO]` | `[ALERTA PLAZO FATAL: ...]` con sus cuatro campos |
| `[VERIFICAR RÉGIMEN APLICABLE]` | `[VERIFICAR VIGENCIA: ...]` o A8, según qué falte |
| `[DISCREPANCIA ENTRE CONECTORES]` | `[DISCREPANCIA ENTRE FUENTES: ...]` |

---

## Agregar un marcador

Sólo si ninguno de los veintidós sirve, y en este orden: se define acá con su categoría,
sintaxis y para qué sirve; se revisa que ningún script tenga que reconocerlo; y recién
entonces se usa en los módulos. Un marcador que existe en un módulo y no acá es un marcador
que nadie va a auditar.
