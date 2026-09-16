---
name: honorarios
description: Regulación de honorarios y aportes en Provincia de Buenos Aires (Ley 14.967), con el valor del jus leído de la serie y no de memoria.
argument-hint: "[monto del proceso, porcentaje]"
allowed-tools: Read, Bash(python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/honorarios_pba.py:*)
---

Consulta: `$ARGUMENTS`

**Leé `${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/sede-judicial-pba.md` sección 1.6.6 antes de regular.** Ahí están las cuatro cosas
que hacen nula o mal hecha una regulación bonaerense.

## Lo que hay que tener resuelto

1. **La cuantía** (art. 23): el total reclamado en demanda o reconvención, no lo que prosperó.
2. **Las etapas.** En procesos orales ante tribunales colegiados el **art. 28 inc. h** cuenta
   **tres** etapas, no las del proceso escrito. Pasalas con `--etapas-cumplidas` y
   `--etapas-totales`.
3. **El monto en jus es requisito de validez** — art. 15 inc. d, bajo pena de nulidad. Y el
   valor definitivo del jus es **el del momento del pago**, no el de la regulación.
4. **Diferimiento del art. 51**: si hay intereses pendientes de determinación, corresponde
   diferir. Verificá si es el caso antes de dar un número cerrado.

## Después

```
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/honorarios_pba.py --monto N --porcentaje N \
  [--valor-jus N] [--etapas-cumplidas N] [--etapas-totales N] \
  [--con-intereses] [--tipo {contradictorio|voluntario}] [--tasa-justicia N]
```

**No pases `--valor-jus` de memoria.** Sin ese flag el script lo lee de
`fuentes/datos/jus-scba.csv` e informa a qué fecha corresponde el valor usado. Si la serie
está vieja, el script lo dice: transcribí esa advertencia, no la borres. Si sale con código 2,
el marcador es la respuesta.

Informá siempre **el monto en jus y el valor del jus con su fecha**, más los aportes de la Ley
6.716 art. 12 si corresponden.
