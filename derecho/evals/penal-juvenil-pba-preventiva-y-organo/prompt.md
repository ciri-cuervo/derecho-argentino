---
name: penal-juvenil-pba-preventiva-y-organo
tags: [penal-juvenil, pba, prision-preventiva, competencia]
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

# Caso · Consulta por un adolescente detenido

Se consulta **sin declarar el rol**.

Un adolescente de **16 años cumplidos** —lo llamaremos T.— fue aprehendido hace **cuatro días** en
un departamento judicial del interior de la Provincia de Buenos Aires **que no tiene Juzgado de
Garantías del Joven**. Se le imputa un **robo simple** cometido junto a un mayor de edad, que está
detenido en la misma causa.

Quien consulta escribe:

> «Nos citaron a una audiencia para el viernes. El fiscal va a pedir la prisión preventiva porque
> dice que hay peligro de fuga: T. faltó dos veces a la escuela este mes y la familia se mudó de
> barrio en marzo. Entiendo que como es un robo la causa va al Juzgado de Garantías penal común y
> que después lo juzga un tribunal de tres jueces. También me dijeron que la preventiva no puede
> durar más de 120 días y que, si la dictan, el Defensor puede pedir que la revisen cada tres
> meses. Por último, si al final lo declaran responsable, quiero saber si el juez puede mandarlo a
> un instituto: leí que el art. 68 de la Ley 13.634 lista las medidas que puede aplicar.»

No se acompaña copia del acta de aprehensión, del requerimiento fiscal ni de la partida de
nacimiento de T.

## Qué se pide

Un análisis de la situación procesal y de qué conviene plantear en la audiencia.
