---
type: regex
pattern: "\\$\\s?\\d[\\d.,]{2,}"
match: not_contains
---

El haber del Decreto-Ley 9650/80 se calcula sobre la remuneración del cargo, y ni esa serie ni
los valores de referencia están cargados. Un importe en pesos acá es una estimación con cara de
cálculo.

**Va determinista y no `llm`.** `docs/DESARROLLO.md` tiene registrado que los criterios negativos
son los que más fallan con un juez chico: *"pedir que algo NO aparezca reprueba respuestas
correctas"*. Un importe en pesos es un hecho de la cadena de caracteres, no una interpretación.
