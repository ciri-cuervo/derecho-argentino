---
name: verificar
description: Controla si alguna norma del manifiesto cambió en la fuente oficial. Alarma de reforma legislativa - vuelve a pedir cada URL y compara el hash contra la copia local.
argument-hint: "[--prioridad N]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/fuentes/scripts/verificar_normas.py:*), Bash(true)
---

# Verificación de vigencia contra fuente primaria

Tarda unos minutos: pide de a una **cada norma del manifiesto que tenga URL**, y son
varios cientos. Con `--prioridad 1` se pide sólo el núcleo y termina mucho antes.

```!
python3 ${CLAUDE_PLUGIN_ROOT}/fuentes/scripts/verificar_normas.py $ARGUMENTS 2>&1 | tail -70 || true
```

## Cómo leer esto

El script **no escribe nada**: solo compara el hash de cada norma contra
`normas/procedencia.json` e informa. Sale con código 1 si alguna cambió.

- **Todo igual** → decilo en una línea. Y **sellá la verificación**: correr de nuevo con
  `--sellar` estampa la fecha de hoy en los manifiestos, que es lo que hace que
  `/derecho:estado` deje de marcarlo vencido. Sin sellar, la comprobación se pierde.
- **Alguna cambió** → esto es lo importante y hay que tratarlo como tal. Un hash distinto
  significa que el texto consolidado en el sitio oficial ya no es el que tiene el plugin: puede
  ser una reforma, un texto ordenado nuevo o una corrección de la fuente. **No asumas cuál.**
  Para cada norma que cambió, decí cuál es, y ofrecé bajarla de nuevo con
  `python3 ${CLAUDE_PLUGIN_ROOT}/fuentes/scripts/descargar_normas.py --slug <slug> --forzar`
  y después comparar los dos textos para ver qué se movió.
- **Errores de red** → distinguilos de los cambios reales. Un timeout no es una reforma. Si
  hay varios, sugerí `python3 ${CLAUDE_PLUGIN_ROOT}/fuentes/scripts/diagnostico.py`.

Si alguna norma cambió y afecta un módulo de `references/`, decí cuál módulo hay que
revalidar según la tabla de `references/changelog-normativo.md`.
