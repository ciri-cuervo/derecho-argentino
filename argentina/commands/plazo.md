---
name: plazo
description: Cómputo de un plazo procesal o administrativo argentino, con ferias, feriados trasladables y plazo de gracia. En PBA verifica primero cuándo se perfeccionó la notificación.
argument-hint: "[ej: 5 días hábiles desde el 10/09/2026, PBA]"
allowed-tools: Read, Bash(python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/plazos.py:*)
---

Consulta: `$ARGUMENTS`

**Leé `${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/plazos.md` antes de calcular.** Y si el plazo es bonaerense, leé también
`${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/notificaciones-pba.md` sección 22: **el error más caro acá no es la aritmética, es
arrancar el cómputo el día equivocado.**

## Orden

1. **Fuero y tipo de plazo.** Hábiles judiciales, hábiles administrativos, corridos, horas,
   meses o años. No son lo mismo y el traslado por vencimiento en inhábil tampoco.
2. **Desde cuándo corre.** En los plazos judiciales `--desde` es la fecha de **notificación**,
   no la de la providencia. En PBA, si la notificación fue por cédula electrónica, se
   perfecciona **el martes o viernes inmediato posterior a que quedó disponible** en el
   sistema, salvo urgencia justificada en la propia providencia (sección 22.3). Si no sabés
   la fecha de disponibilidad, **no calcules el vencimiento**: emitilo con marcador.
3. **Corré el script:**

   ```
   python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/plazos.py --tipo {habiles|corridos|meses|anios} --desde AAAA-MM-DD \
     [--dias N | --cantidad N] [--fuero {nacional|pba}] [--traza]
   ```

   Usá `--traza` cuando el usuario quiera ver el conteo día por día.
4. **Si el script dice que falta el año en `inhabiles.json`, no estimes.** Las ferias, los
   asuetos y los puentes turísticos no se calculan: se cargan. El script emite el marcador.
5. **Plazo de gracia.** Cuatro horas en PBA (art. 124 CPCCBA), dos en el orden nacional. No
   declares un plazo vencido mientras corra. En el expediente digital bonaerense su aplicación
   está discutida: ver 22.5.
6. **Si el plazo es fatal o de caducidad, decilo con el marcador `[ALERTA PLAZO FATAL: ...]`**,
   con norma, plazo, fecha de inicio y vencimiento.
