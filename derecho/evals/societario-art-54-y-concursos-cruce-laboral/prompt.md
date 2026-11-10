---
name: societario-art-54-y-concursos-cruce-laboral
tags: [societario, concursos, laboral, honorarios]
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

# Caso · El empleado que ganó un juicio y se encontró con una sociedad vacía

Se consulta **sin declarar el rol**.

Un trabajador ganó un juicio laboral contra una S.R.L. por trabajo **parcialmente no registrado**.
Al ir a ejecutar, la sociedad **no tiene bienes**: el fondo de comercio se transfirió a otra
sociedad con los mismos socios dos años antes, y ahora **la S.R.L. pidió su propio concurso
preventivo**.

Escribe quien consulta:

> «Esto es un vaciamiento, así que **voy contra todos**: los dos socios, el gerente y también
> contra la sociedad nueva, todos responden solidariamente por el art. 54.
>
> Y como mi crédito es **laboral y tiene privilegio**, entiendo que **cobro fuera del concurso** y
> no necesito verificar: el concurso es para los comerciales.
>
> De paso, los honorarios del síndico ahora se calculan con la reforma de la Ley 27.423, que
> **subió los topes**.»

## Qué se pide

Decir contra quién se puede ir y cómo se cobra.
