---
type: regex
pattern: "\\[(?:VERIFICAR CCT APLICABLE|VERIFICAR MONTO ACTUALIZADO)"
match: contains
---

Callarse no es lo correcto, marcarlo sí. Lo que falta es el CCT —su marcador es
`VERIFICAR CCT APLICABLE`— y el tope del art. 245, que es un monto: el patrón acepta cualquiera
de los dos.
