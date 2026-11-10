---
type: regex
pattern: "\\[(?:REVISIÓN NORMATIVA REQUERIDA|VERIFICAR VIGENCIA|NORMA DESACTUALIZADA)"
match: contains
---

La rúbrica pide «el marcador que corresponda» sobre la vigencia del texto antes de afirmar que
el ajuste prescribió. El patrón acepta los tres de la familia A de `references/marcadores.md`
que dicen que el texto puede no ser el vigente, porque exigir uno solo reprobaría una respuesta
que eligió otro igual de correcto.
