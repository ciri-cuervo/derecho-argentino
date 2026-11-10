---
name: tributario-prescripcion-y-opcion-del-art-76
tags: [tributario, nacional, arca, recursos, prescripcion]
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

# Caso · Una determinación de oficio y dos recursos en el aire

Se consulta **sin declarar el rol**.

Una empresa recibió una **determinación de oficio de ARCA** con intereses y multa. La notificación
fue hace **doce días hábiles**.

Escribe quien consulta:

> «Vamos a presentar el **recurso de reconsideración** ante el propio organismo, y **al mismo
> tiempo** vamos al **Tribunal Fiscal**, para no perder ninguna de las dos vías y que decida el
> que primero se expida.
>
> Sobre el fondo: parte del ajuste es de hace más de cinco años, así que **está prescripto** — el
> art. 56 de la Ley 11.683 da cinco años y eso no cambió nunca.
>
> Y como vamos a recurrir, **mientras tanto no hay que pagar nada**, el trámite suspende todo.»

## Qué se pide

Decir qué se puede hacer y qué hay que decidir hoy.
