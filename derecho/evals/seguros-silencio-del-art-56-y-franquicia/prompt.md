---
name: seguros-silencio-del-art-56-y-franquicia
tags: [seguros, siniestro, citacion-en-garantia]
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

# Caso · Un choque, una declinación tardía y un reclamo que incluye todo

Se consulta **sin declarar el rol**.

Hubo un choque en la Provincia de Buenos Aires. El asegurado **denunció el siniestro al día
siguiente**. La aseguradora le pidió información complementaria, que él entregó, y **recién dos
meses después le contestó por carta documento que declinaba la cobertura** invocando reticencia en
la declaración del riesgo.

Mientras tanto, el damnificado inició demanda civil. **El expediente ya tiene auto de apertura a
prueba.**

Escribe quien consulta:

> «Voy a discutir la reticencia, porque yo declaré todo de buena fe. Y como estoy en juicio, ahora
> **cito en garantía a la aseguradora**, que todavía estoy a tiempo.
>
> En el reclamo voy a incluir el auto, los gastos y también **el lucro cesante** por los meses que
> no pude trabajar, que la póliza lo tiene que cubrir.
>
> De paso: como la culpa fue del otro, **le reconocí al damnificado que yo no tenía nada que ver y
> firmamos un papel** arreglando entre nosotros.»

## Qué se pide

Revisar la estrategia antes de presentar nada.
