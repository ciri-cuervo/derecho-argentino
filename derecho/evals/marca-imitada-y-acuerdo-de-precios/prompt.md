---
name: marca-imitada-y-acuerdo-de-precios
tags: [marcas, competencia, transferencia-de-tecnologia, dipr]
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

# Caso · La marca que no se usaba y el acuerdo del que todos hablaban

Se consulta **sin declarar el rol**.

Una empresa argentina tiene una **marca registrada hace doce años** que **no usa desde hace siete**.
Descubre que un competidor está usando una muy parecida. Además:

- Está por firmar una **licencia de tecnología con una empresa de Alemania** que la controla.
- Sospecha que **tres competidores acordaron precios** y que por eso su negocio cayó.

Escribe quien consulta:

> «La marca es mía, está registrada, **usarla o no es asunto mío**. Voy a intimar al competidor.
>
> La licencia con los alemanes **la firmamos y listo**, es un contrato entre privados.
>
> Y por el acuerdo de precios voy a pedir **daño punitivo** como en consumo, pero **primero tengo
> que denunciar** ante la autoridad de competencia y esperar que resuelva.
>
> Ah, y en el contrato de licencia pusimos que **cualquier conflicto se resuelve en tribunales
> alemanes**, incluida la validez de la marca.»

## Qué se pide

Revisar las cuatro decisiones.
