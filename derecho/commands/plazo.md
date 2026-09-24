---
name: plazo
description: Cómputo de un plazo procesal o administrativo argentino, con ferias, feriados trasladables y plazo de gracia. En PBA verifica primero cuándo se perfeccionó la notificación.
argument-hint: "[ej: 5 días hábiles desde el 10/09/2026, PBA]"
allowed-tools: Read, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/plazos.py:*), Bash(python ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/plazos.py:*), Bash(py -3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/plazos.py:*)
---

Consulta: `$ARGUMENTS`

**Leé `${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/references/plazos.md` antes de calcular.** Y si el plazo es bonaerense, leé también
`${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/references/notificaciones-pba.md` sección 22: **el error más caro acá no es la aritmética, es
arrancar el cómputo el día equivocado.**

## Orden

**Abrí con el bloque de datos tomados**, copiado de la cabecera de la salida del script y
cotejado contra lo que te dieron. Un dato mal tipeado no rompe nada: devuelve un resultado
plausible. Si alguno no coincide, pará y preguntá. Ver `intake.md`, «Devolver los datos
antes de usarlos».

1. **Fuero y tipo de plazo.** Hábiles judiciales, hábiles administrativos, corridos, horas,
   meses o años. No son lo mismo y el traslado por vencimiento en inhábil tampoco.
2. **Desde cuándo corre.** En los plazos judiciales `--desde` es la fecha de **notificación**,
   no la de la providencia. En PBA, si la notificación fue por cédula electrónica, se
   perfecciona **el martes o viernes inmediato posterior a que quedó disponible** en el
   sistema, salvo urgencia justificada en la propia providencia (sección 22.3). Si no sabés
   la fecha de disponibilidad, **no calcules el vencimiento**: emitilo con marcador.
3. **Corré el script:**

   ```sh
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/plazos.py --tipo {habiles|corridos|meses|anios} --desde AAAA-MM-DD \
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

**Si `python3` no responde** —`command not found`, `no se reconoce` o *Python was not
found*—, el mismo comando se corre con `python` y después con `py -3`, y el que ande se usa
en el resto. Si ninguno anda, falta Python: ver «Si un script no corre» en el `SKILL.md`.
