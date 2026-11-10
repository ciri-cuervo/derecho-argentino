---
name: titulos-cheque-rechazado-y-prescripcion
tags: [titulos, cheque, pagare, prescripcion]
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

# Caso · Dos papeles en un cajón

Se consulta **sin declarar el rol**.

Quien consulta tiene dos documentos de un mismo deudor:

> «Primero, un **cheque** que me rechazaron. La fecha de rechazo dice **hace once meses**, así que
> todavía estoy dentro del año y lo puedo ejecutar. El banco me lo devolvió y me quedé con el
> papel, aunque **no tiene ningún sello ni constancia encima** — me avisaron por el homebanking.
>
> Segundo, un **pagaré** que le hice firmar. Dice el monto, la fecha y está firmado, pero **no
> puse el lugar de pago** y tampoco escribí "a la orden". Igual es un pagaré, la firma es lo que
> importa.
>
> Y además le vendí mercadería que nunca me pagó. Como tengo los papeles, **entiendo que la deuda
> por la mercadería ya está absorbida** y sólo puedo reclamar los títulos.»

No acompaña copia de los documentos.

## Qué se pide

Decir qué se puede ejecutar, contra quién y hasta cuándo.
