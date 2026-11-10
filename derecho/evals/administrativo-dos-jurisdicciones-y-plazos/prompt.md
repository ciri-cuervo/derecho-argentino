---
name: administrativo-dos-jurisdicciones-y-plazos
tags: [administrativo, nacional, pba, plazos, silencio]
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

# Caso · Dos expedientes administrativos, dos jurisdicciones

Se consulta **sin declarar el rol**.

Un estudio lleva dos casos a la vez:

**Caso A —** Un organismo **nacional** rechazó un recurso. La resolución se notificó hace **cinco
meses**.

**Caso B —** Un municipio **bonaerense** dictó un acto que perjudica a un comerciante. Se presentó
un recurso y **la administración no contestó nunca**; ya pasaron cuatro meses desde la
presentación.

Escribe quien consulta:

> «En los dos casos tengo **noventa días** para ir a juicio, así que el A ya lo perdí y el B está
> por vencer.
>
> En el B, como no me contestaron, **entiendo que eso es un rechazo automático** y puedo demandar
> cuando quiera.
>
> Para el A voy a citar doctrina de 2019 sobre la Ley 19.549, que **es la misma ley de siempre**.»

## Qué se pide

Decir qué plazo rige cada uno y qué hay que hacer.
