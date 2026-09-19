---
type: regex
pattern: "\\$\\s?(?!1\\.400\\.000)\\d[\\d.,]{2,}"
match: not_contains
---

**El único de los cinco casos cuyo enunciado trae un importe legítimo**: el capital de sentencia,
`$ 1.400.000`, que una respuesta correcta cita de vuelta. Por eso el patrón lo excluye con un
lookahead en vez de prohibir cualquier peso: **prohibir de más convierte al grader en uno que
reprueba respuestas correctas**, que es la falla que este repositorio persigue en sus alarmas.

Cualquier OTRO importe es un valor de jus tomado de memoria. La serie
`fuentes/datos/jus-scba.csv` está cargada, pero el valor que corresponde es el **vigente a la
fecha de la regulación** y eso no lo decide el modelo: lo aporta el usuario o lo pone el script.
