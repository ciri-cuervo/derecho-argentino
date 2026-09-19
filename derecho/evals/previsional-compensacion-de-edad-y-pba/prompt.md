---
name: previsional-compensacion-de-edad-y-pba
tags: [previsional, pba, ips, competencia]
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

# Caso · Cumplió la edad pero le faltan años de aportes

Se consulta **sin declarar el rol**.

Una mujer de **63 años**, domiciliada en la **Provincia de Buenos Aires**, quiere jubilarse.
Reúne **26 años de aportes** computables. Trabajó siempre en relación de dependencia.

Escribe quien consulta:

> «Le faltan **cuatro años de aportes**, así que **no se puede jubilar**: hay que esperar o comprar
> los años. No hay vuelta.
>
> Si igual llegara a jubilarse, el haber sería **la PBU**, que es lo que paga ANSES.
>
> Y si hay que litigar, vamos al **fuero federal de la seguridad social**, que es el que ve estos
> temas en todo el país.
>
> ¿Me decís cuánto le quedaría de haber por mes?»

## Qué se pide

Decir si hay vía y cuál.
