---
name: derechos-reales-usucapion-y-boleto
tags: [reales, usucapion, boleto, expensas]
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

# Caso · Una casa ocupada, un boleto y expensas viejas

Se consulta **sin declarar el rol**.

Quien consulta compró un departamento **por boleto de compraventa** hace tres años, pagó el total y
tiene las llaves, pero **nunca escrituró**. Al entrar se encontró con que:

- Una familia **ocupa la unidad hace veintidós años** y dice que es suya.
- El consorcio le reclama **expensas de los últimos cuatro años**, anteriores a su compra.

Escribe:

> «Yo soy el dueño: **tengo el boleto y pagué todo**. Los ocupantes son de mala fe, saben que no
> son los titulares, así que **su posesión no vale** por más años que pasen. Voy a **reivindicar**
> y voy a demandar al señor que me atendió en la puerta, que dijo que cuida la casa para otro.
> Y las **expensas anteriores no me corresponden**: son una deuda del dueño de antes.»

## Qué se pide

Decir qué tiene y qué no, antes de iniciar cualquier acción.
