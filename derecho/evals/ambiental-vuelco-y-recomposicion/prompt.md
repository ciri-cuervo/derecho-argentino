---
name: ambiental-vuelco-y-recomposicion
tags: [ambiental, danos, competencia, prueba]
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

# Caso · La fábrica, el arroyo y los vecinos

Se consulta **sin declarar el rol**.

Una fábrica vuelca efluentes en el arroyo que cruza un barrio. Hay olor, mortandad de peces y
varios vecinos con problemas de salud. **La empresa dice que cumple con la ordenanza municipal**,
que fija parámetros de vuelco más permisivos que la normativa nacional. Un informe del organismo
provincial de ambiente **ya constató la contaminación**.

Escriben vecinos organizados:

> «Queremos **demandar para que les paguen a los vecinos** por el daño ambiental: que la plata se
> reparta entre las familias del barrio.
>
> La empresa dice que **cumple la ordenanza**, así que por ahí no hay nada que hacer.
>
> Vamos al **juzgado penal provincial** para que investiguen, porque hay residuos peligrosos.
>
> Y vamos a pedir una **pericia** desde cero, porque el informe del organismo **es sólo un papel
> administrativo**.»

## Qué se pide

Decir qué acción hay, contra quién y ante qué fuero.
