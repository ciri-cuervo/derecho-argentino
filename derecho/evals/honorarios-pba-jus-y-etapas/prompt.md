---
name: honorarios-pba-jus-y-etapas
tags: [honorarios, pba, jus, arancel]
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

# Caso · Consulta sobre una regulación practicada

Se consulta **desde la parte actora**. Los datos son inventados.

## Lo que se aporta

Juicio laboral ante un Tribunal del Trabajo bonaerense, causa de monto reducido. La sentencia
hizo lugar parcialmente a la demanda por un capital de **$ 1.400.000** más intereses.

El auto regulatorio dice:

> Regúlanse los honorarios del letrado apoderado de la parte actora en la suma equivalente a
> **cuatro (4) jus arancelarios**, tomando el valor del jus arancelario del decreto-ley 8904/77
> publicado por la Suprema Corte, y aplicando la escala del art. 21 de la Ley 14.967 en su
> mínimo por tratarse de un asunto de escaso contenido económico.

El letrado de la actora pregunta si el auto es correcto.

## Lo que se pregunta

1. ¿La unidad que se tomó es la que corresponde?
2. ¿El número de jus regulado es admisible?
3. ¿Hay que calcular algo, y con qué?
