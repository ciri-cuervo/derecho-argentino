# `normas/` — textos normativos consolidados

Texto plano de las normas de uso diario, con encabezado de procedencia y hash. Es de acá de
donde se transcribe un artículo a un escrito, en lugar de una consulta automática que puede
venir truncada.

- `normas.json` — el manifiesto: qué normas, con qué URL oficial y con qué prioridad.
- `procedencia.json` — qué se bajó, cuándo, desde dónde y con qué hash. Lo escribe el
  descargador.
- `<slug>.txt` / `<slug>.pdf` — los textos.

Poblar y controlar cambios con los scripts de `../scripts/`. Ver `../MANIFIESTO.md`.

**Estos archivos no son publicación oficial.** Son material de trabajo verificable. Para una
transcripción literal que va a un escrito, cotejar contra el Boletín Oficial de la fecha de
publicación. El caso conocido: `normas.gba.gob.ar` devuelve la Ley 11.653 con la acentuación
degradada.
