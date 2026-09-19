---
type: regex
pattern: "\\[VERIFICAR MONTO ACTUALIZADO[^\\]]*UF"
match: contains
---

Callarse no es lo correcto, marcarlo sí: una respuesta que omite el valor de la UF sin decir que
falta pasa el `not_contains` y deja al lector creyendo que el punto está cerrado.
