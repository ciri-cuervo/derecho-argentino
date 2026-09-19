---
name: honorarios-nacional-uma-caba-y-art64
tags: [honorarios, nacional, uma, arancel, ruteo]
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

# Caso · Regulación de honorarios en un despido que tramitó en la Ciudad

Se consulta **sin declarar el rol**.

Un juicio por despido tramitó ante la **Justicia Nacional del Trabajo**, con asiento en la
Ciudad de Buenos Aires. Se dictó sentencia, quedó firme y hay liquidación aprobada. El
profesional patrocinó a la parte actora y cumplió las tres etapas. Escribe:

> «La causa tramitó en CABA, así que no es federal: es local. Como no hay ley arancelaria
> porteña cargada, **uso la Ley 14.967 y el jus**, que es lo que tenemos, total el mecanismo es
> el mismo. Calculé el 20% sobre el monto de la liquidación y me dio un número; **poneme el
> valor del jus de este mes** que no lo tengo a mano. En la resolución voy a pedir que se fije
> **el importe en pesos**, que es lo que se cobra. Y como el juicio se inició antes de la
> reforma, **por el art. 64 de la Ley 27.423 se aplica la ley nueva igual**, así que no hay
> discusión de transición.»

No acompaña la liquidación, ni la fecha de la resolución, ni la fecha en que espera cobrar.

## Qué se pide

Revisar el planteo antes de que se presente el pedido de regulación, y decir qué se puede
afirmar con lo que hay cargado y qué no.
