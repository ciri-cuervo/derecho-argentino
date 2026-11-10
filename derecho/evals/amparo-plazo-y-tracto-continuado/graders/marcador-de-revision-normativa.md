---
type: regex
pattern: "\\[(?:REVISIÓN NORMATIVA REQUERIDA|VERIFICAR VIGENCIA|NORMA DESACTUALIZADA)"
match: contains
---

La rúbrica pide el marcador sobre el desplazamiento de la Ley 16.986 por el art. 43 CN.

La rúbrica pide «el marcador de revisión normativa». El patrón acepta los tres de la familia A
de `references/marcadores.md` que dicen que el texto citado puede no ser el vigente
—`REVISIÓN NORMATIVA REQUERIDA`, `VERIFICAR VIGENCIA` y `NORMA DESACTUALIZADA`—, porque exigir
uno solo reprobaría una respuesta que eligió otro igual de correcto: exigir de más falla igual
que prohibir de más.
