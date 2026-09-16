---
name: actualizar
description: Vuelve a bajar normas, fallos y series de índices de las fuentes oficiales. Mantenimiento de la capa offline de fuente primaria.
argument-hint: "[normas|fallos|series]"
---

# Actualizar la capa de fuente primaria

Argumento recibido: `$ARGUMENTS` (vacío = las tres cosas).

Series de índices (IPC, RIPTE, CER) — es la que más rápido se desactualiza:

```!
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/fuentes/scripts/descargar_series.py 2>&1 | tail -20 || true
```

Normas y jurisprudencia faltantes (no re-baja lo que ya está, salvo `--forzar`):

```!
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/fuentes/scripts/descargar_normas.py 2>&1 | tail -30 || true
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/fuentes/scripts/descargar_jurisprudencia.py 2>&1 | tail -20 || true
```

## Qué informar

1. **Qué se bajó nuevo y qué ya estaba.** No repitas la lista entera: los totales y las
   novedades.
2. **Todo lo que diga REVISAR o ERROR.** Los descargadores hacen controles de sanidad —cuentan
   artículos, detectan fichas de InfoLEG en vez del texto, detectan leyes aprobatorias sin su
   anexo—. Un REVISAR quiere decir que el archivo se bajó pero **puede no ser el texto que
   corresponde**: hay que abrirlo antes de citarlo.
3. **Si algo falló por red**, sugerí `python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/fuentes/scripts/diagnostico.py` antes de reintentar. No
   reintentes la misma descarga más de una vez.

**Lo que este comando no hace:** no cambia ningún módulo de `references/`. Bajar el texto
nuevo de una norma no actualiza lo que la skill dice sobre ella. Si una norma cambió de fondo,
decilo y señalá qué módulo hay que revisar.
