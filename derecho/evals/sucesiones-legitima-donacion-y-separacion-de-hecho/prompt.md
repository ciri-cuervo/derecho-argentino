---
name: sucesiones-legitima-donacion-y-separacion-de-hecho
tags: [sucesiones, legitima, donacion, conyuge]
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

# Caso · Murió el padre y aparecen una donación y una esposa de la que nadie hablaba

Se consulta **sin declarar el rol**.

Murió una persona dejando **tres hijos**. Está casada, pero **vive separada de hecho de su cónyuge
desde hace ocho años**, sin divorcio ni sentencia de ningún tipo. En el patrimonio quedan un
departamento y algo de dinero.

Y hay un dato que sale después: **hace quince años el causante le donó un campo a uno de los
hijos**, que lo posee desde entonces.

Escriben los otros dos hijos:

> «Queremos que la herencia se reparta bien. Entendemos que **la legítima se calcula sobre lo que
> quedó**, o sea el departamento y la plata, y que el campo **ya no entra porque fue hace quince
> años y está prescripto**.
>
> Y suponemos que **la esposa hereda igual**, porque nunca se divorciaron, así que le toca su
> parte de todo, incluidos los gananciales.»

## Qué se pide

Decir cómo se reparte y qué acciones hay.
