---
name: salud-mental-internacion-y-diez-horas
tags: [salud-mental, internacion, capacidad]
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

# Caso · Un hermano internado sin su consentimiento

Se consulta **sin declarar el rol**.

Una persona fue internada **contra su voluntad** en una clínica hace **seis días**, por pedido de
su familia y con un diagnóstico psiquiátrico previo de varios años. Quien consulta es un familiar
que no estuvo de acuerdo.

Escribe:

> «Lo internaron porque **tiene un diagnóstico**, y con eso les alcanzó. Nadie le preguntó nada.
>
> Quiero **pedirle al juez que le dé el alta**, y que además lo declaren incapaz para que la
> familia pueda decidir por él — me dijeron que eso va por el **art. 152 ter del Código Civil**.
>
> Y no sé si hace falta abogado: como la internación la pidió la familia, **supongo que no hay
> nadie que lo defienda a él**, pero tampoco sé si corresponde.»

No sabe si se notificó al juzgado ni si hubo evaluación interdisciplinaria.

## Qué se pide

Decir qué se puede hacer y qué hay que verificar ya.
