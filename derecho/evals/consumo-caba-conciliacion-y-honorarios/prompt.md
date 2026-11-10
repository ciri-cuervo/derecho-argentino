---
name: consumo-caba-conciliacion-y-honorarios
tags: [consumo, caba, honorarios, uma, conciliacion]
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

# Caso · Un reclamo chico en el fuero de consumo porteño

Se consulta **sin declarar el rol**.

Un consumidor domiciliado en CABA compró un electrodoméstico que nunca funcionó. El contrato de
adhesión dice que **cualquier conflicto se somete a los tribunales de otra provincia**. Además, la
autoridad administrativa le aplicó una multa a la empresa y el consumidor quiere que se mantenga.

Escribe quien consulta:

> «Presento la demanda **el lunes** ante el fuero de consumo de la Ciudad. Sé que existe una
> instancia de conciliación pero **la hago después**, si el juez la pide.
>
> Me preocupa la cláusula del contrato: **como la firmé, me van a mandar a la otra provincia**.
>
> Para el tema de la multa, cuando la empresa apele **contesto los agravios** como en cualquier
> apelación.
>
> Y para mis honorarios uso **la UMA que publica la Corte**, que es la que todos usan.»

## Qué se pide

Revisar el plan antes del lunes.
