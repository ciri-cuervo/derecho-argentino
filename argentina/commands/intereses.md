---
name: intereses
description: Actualización e intereses sobre un crédito. Elegir entre índice más interés puro o tasa nominal no es una decisión técnica - depende de qué doctrina rige.
argument-hint: "[capital, desde, hasta, fuero]"
allowed-tools: Read, Bash(python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/intereses.py:*)
---

Consulta: `$ARGUMENTS`

**Leé antes de calcular:** `${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/laboral.md` sección 5.5 para el fuero nacional y **5.5 bis**
para PBA, que traen la cadena de precedentes completa. Si actuás desde el órgano,
`${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/sede-judicial-pba.md` 1.6.8.

## Lo que hay que resolver antes de tocar el script

**Elegir el modo no es una decisión técnica: es determinar qué norma o doctrina rige el
crédito.** El script tiene dos modos y aplicar el equivocado da un número defendible y mal.

- `--modo indice` — actualización por índice oficial más interés puro. Es el esquema de
  **"Barrios"** (SCBA, C. 124.096, 17/04/2024) y el del art. 276 LCT.
- `--modo tasa` — tasa nominal anual sobre capital nominal.

Tres cosas que se equivocan seguido y están en 5.5 bis:

1. **No trasladar el criterio de la CNAT a PBA.** Son cadenas de precedentes distintas.
2. **"Barrios" no alcanza a las prestaciones de la LRT** — "Galarza", L. 132.729, 30/03/2026.
3. **El segundo párrafo del art. 48 de la Ley 11.653** (tasa activa, texto Ley 14.399) está
   declarado inconstitucional desde "Abraham", L. 108.164. Una liquidación que lo invoque
   aplica una norma muerta. Ver `${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/ejecucion.md` 21.2.

## Después

```
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/intereses.py --modo indice --capital N --desde AAAA-MM-DD --hasta AAAA-MM-DD \
  --serie {ipc|ripte|cer} --interes-puro N
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/intereses.py --modo tasa --capital N --desde AAAA-MM-DD --hasta AAAA-MM-DD --tna N
```

Si la serie no está cargada el script **no estima**: emite el marcador y corta. No lo
completes. Si le falta el último período, decí hasta qué fecha llega la serie y ofrecé
`/derecho:actualizar`.

Decí siempre **qué modo usaste, con qué fundamento y con qué serie**, y que el resultado se
coteja contra el criterio del departamento judicial.
