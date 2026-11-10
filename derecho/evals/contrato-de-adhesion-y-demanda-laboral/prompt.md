---
name: contrato-de-adhesion-y-demanda-laboral
tags: [contratos, adhesion, laboral, pba, riesgos-del-trabajo]
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

# Caso · Un contrato firmado y un juicio laboral que empieza

Se consulta **sin declarar el rol**.

Un trabajador firmó, al ingresar, un **contrato de adhesión** con la empresa que incluye:

- **Prórroga de jurisdicción** a los tribunales de otra provincia.
- Un **plazo de prescripción pactado** de un año para cualquier reclamo.
- **Renuncia anticipada** a las defensas que pudiera oponer en juicio.

Tuvo un accidente de trabajo. **Ya cobró la prestación dineraria de la ART.** Ahora quiere
demandar.

Escribe quien consulta:

> «Las tres cláusulas son **abusivas**, así que las vamos a atacar en el mismo escrito y pedimos
> que el juez **integre el contrato** como corresponde.
>
> Sobre el accidente: **como ya cobré de la ART**, ahora **voy también por la acción civil** para
> completar.
>
> Y la demanda laboral la presento **la semana que viene** en el juzgado de La Plata.»

## Qué se pide

Revisar el planteo antes de presentar nada.
