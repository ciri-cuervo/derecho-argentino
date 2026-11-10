---
name: penal-prescripcion-tope-del-art-62-y-probation
tags: [penal, prescripcion, probation, reincidencia]
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

# Caso · Una causa vieja, una probation pedida y una condena anterior

## Datos aportados por el consultante

### Los hechos

EL CONSULTANTE es **agente de una repartición pública** y está imputado en dos causas distintas.

**Causa A.** El hecho se habría cometido el **12 de marzo de 2017**. La imputación es por un
delito que, según el auto de procesamiento, está **reprimido con prisión de cinco (5) a veinte
(20) años**. En el expediente constan estos actos, y ningún otro:

| Acto | Fecha |
| --- | --- |
| Primer llamado a prestar declaración indagatoria | **18/04/2019** |
| Requerimiento fiscal de elevación a juicio | **05/08/2022** |
| Auto de citación a juicio | **20/03/2024** |
| Última presentación de la defensa | **02/07/2026** |

No hubo sentencia. EL CONSULTANTE no cometió otro delito en el período. Su abogado anterior le
dijo que **"a los veinte años recién prescribe"** y que por eso no había nada que plantear.

**Causa B.** Un hecho del **junio de 2026**, imputado como un delito reprimido con **prisión de
uno (1) a cinco (5) años**, que se le atribuye **en ejercicio de sus funciones** en la
repartición. EL CONSULTANTE quiere pedir la **suspensión del juicio a prueba**: ofrece reparar el
daño y dice que no tiene antecedentes relevantes para esta causa.

**Antecedente.** En 2013 EL CONSULTANTE fue **condenado a pena de prisión de efectivo
cumplimiento**, sentencia **firme**, que terminó de cumplir en 2016.

### Estado actual

Fecha de la consulta: **18 de septiembre de 2026**. No aporta montos ni tasación: quiere saber
qué se puede plantear en cada causa y con qué norma.

---

## Consulta

El abogado de EL CONSULTANTE consulta:

1. En la causa A, ¿la acción prescribió? ¿Desde cuándo se cuenta y contra qué plazo?
2. ¿Los cuatro actos de la tabla interrumpen todos?
3. En la causa B, ¿puede pedir la suspensión del juicio a prueba?
4. Si en alguna de las dos recayera condena, ¿la de 2013 le impide la libertad condicional?
