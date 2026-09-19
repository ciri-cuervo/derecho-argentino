---
type: regex
pattern: "\\$\\s?\\d[\\d.,]{2,}"
match: not_contains
---

El art. 84 de la Ley 24.449 está bajado y define la UF como **el menor precio de venta al público
de un litro de nafta especial**. Lo que ninguna norma puede dar es ese precio: es un dato de
mercado del día del pago, así que **no hay serie que cargar** y cualquier importe en pesos que
aparezca acá salió de la memoria del modelo.

**Va determinista y no `llm`.** `docs/DESARROLLO.md` tiene registrado que los criterios negativos
son los que más fallan con un juez chico: *"pedir que algo NO aparezca reprueba respuestas
correctas"*. Un importe en pesos es un hecho de la cadena de caracteres, no una interpretación.

El enunciado de este caso no trae ningún importe en pesos, así que no hay nada legítimo que citar
de vuelta.
