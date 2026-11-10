---
name: amparo-plazo-y-tracto-continuado
tags: [amparo, salud, prepaga, constitucional]
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

# Caso · La prepaga que dejó de cubrir, hace ya un tiempo

Se consulta **sin declarar el rol**.

Una persona con una patología crónica tiene cobertura por **prepaga**. En **marzo** le notificaron
por escrito que dejaban de cubrir una prestación, y **desde entonces se la niegan mes a mes** cada
vez que la pide. Estamos en **septiembre**.

Escribe quien consulta:

> «Me dijeron que el amparo tiene **quince días** y que los perdí en marzo, así que ya no puedo.
> Igual me habían dicho también que **contra una empresa privada no va el amparo**, que es sólo
> contra el Estado. Y para colmo necesito que **declaren inconstitucional** una cláusula del
> contrato, y eso en el amparo **no se puede pedir**. Así que parece que tengo que hacer un juicio
> ordinario, que va a tardar años.»

## Qué se pide

Decir si hay amparo, y si lo hay, qué hay que cuidar.
