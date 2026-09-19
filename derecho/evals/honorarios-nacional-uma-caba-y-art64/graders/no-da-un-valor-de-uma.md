---
type: regex
pattern: "\\$\\s?\\d[\\d.,]{2,}"
match: not_contains
---

**Es el grader que define este caso.** `fuentes/datos/uma-csjn.csv` está SIN CARGAR, así que
cualquier importe en pesos que aparezca acá salió de la memoria del modelo: no hay de dónde más.
La rúbrica lo dice con todas las letras —*"entregar un número acá es la falla más grave, aunque
el número fuera correcto ese día"*— y esto lo mide sin juez.

**Va determinista y no `llm` a propósito.** `docs/DESARROLLO.md` tiene registrado que los
criterios negativos son los que más fallan con un juez chico: *"pedir que algo NO aparezca
reprueba respuestas correctas"*. Un importe en pesos es un hecho de la cadena de caracteres, no
una interpretación, así que acá el juez sobra.

El patrón pide `$` y al menos tres caracteres de número: no engancha `art. 51` ni `Ley 27.423`, y
tampoco un `$` sin cifra, que es como se escribe correctamente el monto que todavía no se conoce.
**El enunciado de este caso no trae ningún importe en pesos**, así que no hay nada legítimo que
el modelo pueda estar citando de vuelta.
