---
name: documento-electronico-firma-notificacion-y-pericia
tags: [firma-digital, notificaciones, pericia, pba, proceso]
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

# Caso · Tres problemas del expediente digital, todos el mismo día

Se consulta **sin declarar el rol**.

En un juicio civil en la Provincia de Buenos Aires:

> «**Uno.** Acompañé como prueba un contrato en PDF **firmado con una imagen escaneada de la firma**
> del demandado. Él lo desconoció. Yo digo que es **firma digital** y que se presume que es de él,
> así que **la carga de probar que no firmó es suya**.
>
> **Dos.** Me llegó una notificación electrónica **un viernes a las 20:30**. Yo cuento el plazo
> **desde ese mismo viernes**.
>
> **Tres.** El perito presentó el dictamen, me corrieron traslado y **dejé pasar el plazo** porque
> quería consultarlo con un especialista. Ahora quiero **impugnarlo y designar un consultor
> técnico** que revise el trabajo.»

## Qué se pide

Decir qué se sostiene y qué ya se perdió.
