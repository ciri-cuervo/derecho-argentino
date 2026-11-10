---
type: regex
pattern: "8\\.?031"
match: contains
---

El código de faltas bonaerense. Escrito en positivo: el criterio de fondo de la rúbrica es que
no se aplique a la falta provincial el régimen contravencional de la Ciudad —Leyes 1.472 y 451—,
pero una respuesta correcta puede nombrarlas para descartarlas, así que un `not_contains` sobre
ellas reprobaría la respuesta buena.
