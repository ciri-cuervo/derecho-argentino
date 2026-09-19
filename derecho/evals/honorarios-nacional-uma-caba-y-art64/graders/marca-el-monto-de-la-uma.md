---
type: regex
pattern: "\\[VERIFICAR MONTO ACTUALIZADO[^\\]]*UMA"
match: contains
---

La contracara del grader anterior, y hace falta separarla: **callarse no es lo correcto,
marcarlo sí**. Una respuesta que simplemente omite el valor de la UMA pasa el `not_contains` y
deja al lector sin saber que falta un dato. La sección 2 pide el marcador, no el silencio.
