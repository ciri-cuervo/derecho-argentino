---
name: locacion-desalojo-e-intimacion-previa
tags: [locacion, desalojo, vivienda, dnu-70]
plugins: ["../.."]
runs: 1
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: |
  Estás respondiendo una consulta escrita: no hay nadie del otro lado para contestar
  repreguntas. Analizá con los datos que están en el mensaje, y lo que falte para cerrar
  una respuesta marcalo con el marcador que corresponda en vez de pedirlo y detenerte.
---

# Caso · Un alquiler firmado en 2022 y un desalojo apurado

Se consulta **sin declarar el rol**.

Un contrato de locación **con destino de vivienda**, firmado en **marzo de 2022**, sigue vigente.
El locatario **adeuda dos meses** y hubo discusiones por el ajuste y por unas expensas.

Escribe quien consulta:

> «Debe dos meses, así que **mando la demanda de desalojo el lunes**. Le avisé por WhatsApp que
> estaba atrasado, con eso alcanza. Además le estoy cobrando **las expensas extraordinarias** del
> edificio, que las tiene que pagar él porque usa el departamento. El ajuste se lo apliqué **por
> el índice que yo elijo**, porque el Código ahora deja pactarlo libremente. Y si se quiere ir
> antes, que **pague el 10% del saldo**, que es lo que dice la ley.»

No acompaña el contrato ni constancia de intimación.

## Qué se pide

Revisar el plan antes de presentar la demanda.
