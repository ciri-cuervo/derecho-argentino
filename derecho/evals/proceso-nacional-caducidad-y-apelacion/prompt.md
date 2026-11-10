---
name: proceso-nacional-caducidad-y-apelacion
tags: [proceso, nacional, caducidad, honorarios, plazos]
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

# Caso · Un expediente dormido y una regulación que se quiere apelar

Se consulta **sin declarar el rol**.

Un juicio ordinario por daños tramita en la **Justicia Nacional en lo Civil**. Se dictó sentencia,
la actora apeló y el expediente está **en la Cámara desde hace cuatro meses sin movimiento**. En el
medio, el juzgado reguló honorarios y la parte quiere discutirlos.

Escribe quien consulta:

> «Me dijeron que la caducidad de instancia es de **seis meses**, así que todavía tengo margen de
> sobra. Igual, con mi colega de la contraria **acordamos suspender los plazos hasta fin de año**
> y quedó por escrito entre nosotros, así que no corre nada. Sobre los honorarios: como la
> regulación no me causa un gravamen irreparable, **entiendo que es inapelable** y habrá que
> discutirlo al final. Y el plazo para apelar lo cuento **desde que salió la resolución**, que es
> cuando la vi en el sistema.»

No acompaña constancias de notificación ni el acuerdo de suspensión.

## Qué se pide

Decir si el expediente está en riesgo y qué hay que hacer, antes de que algún plazo se cumpla.
