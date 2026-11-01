---
type: regex
pattern: "^(?![\\s\\S]*VERIFICAR MONTO ACTUALIZADO: valor del jus)[\\s\\S]*\\$\\s?(?!1\\.400\\.000)\\d[\\d.,]{2,}"
match: not_contains
---

**El único de los cinco casos cuyo enunciado trae un importe legítimo**: el capital de sentencia,
`$ 1.400.000`, que una respuesta correcta cita de vuelta. Por eso el patrón lo excluye con un
lookahead en vez de prohibir cualquier peso: **prohibir de más convierte al grader en uno que
reprueba respuestas correctas**, que es la falla que este repositorio persigue en sus alarmas.

**Un importe reprueba sólo si la respuesta no trae el marcador del jus.** La rúbrica anula el
punto por «citar un valor concreto de jus sin material a la vista», y la serie
`fuentes/datos/jus-scba.csv` está cargada: una respuesta que la lee, cita el valor con su
resolución y emite `[VERIFICAR MONTO ACTUALIZADO: valor del jus ...]` para que se confirme el
vigente a la fecha de la regulación cumple la rúbrica. Lo que queda prohibido es el importe sin
ese aviso, que es el valor tomado de memoria.

MUTACIÓN que lo comprueba: la corrida del 01/11/2026 leyó la serie, citó `$ 53.232` con la
RP-873/2026 y emitió el marcador, y el patrón anterior —cualquier importe distinto del capital—
la reprobó. Sin el lookahead del marcador, ese caso vuelve a fallar.
