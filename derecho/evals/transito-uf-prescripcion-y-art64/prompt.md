---
name: transito-uf-prescripcion-y-art64
tags: [transito, faltas, pba, prescripcion, danos]
plugins: ["../.."]
runs: 3
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: |
  Estás respondiendo una consulta escrita: no hay nadie del otro lado para contestar
  repreguntas. Analizá con los datos que están en el mensaje, y lo que falte para cerrar
  una respuesta marcalo con el marcador que corresponda en vez de pedirlo y detenerte.
---

# Caso · Descargo por una multa y reclamo civil por el mismo hecho

Se consulta **sin declarar el rol**.

Hace **dos años y tres meses**, en un partido del conurbano bonaerense, dos autos chocaron en
una bocacalle sin semáforo. Quien consulta conducía el que venía **por la izquierda**. La
autoridad labró acta y le retuvo la licencia, entregándole **Boleta de Citación**. Nunca se
presentó.

Ahora le llega una intimación de pago. Escribe:

> «El acta dice **300 UF**. Yo tengo el valor de la UF del día del accidente, que era bastante
> más bajo, así que voy a pagar eso. Además pasaron más de dos años, así que **la multa ya
> prescribió**: el art. 89 da dos años. Y aparte quiero demandar al otro por los daños: como él
> venía por la izquierda y **el art. 64 de la Ley 24.449 establece la responsabilidad objetiva
> del dueño y guardián**, con eso alcanza para que responda por todo. Yo respeté la prioridad de
> paso, así que no tengo nada que discutir.»

No acompaña el acta, ni la Boleta de Citación, ni constancia de qué actos hubo en el expediente
de faltas.

## Qué se pide

Un análisis de la posición en el expediente de faltas y del reclamo civil.
