---
name: estado
description: Diagnóstico del plugin - dónde encontró el repo, cómo está el perfil de trabajo, qué datos tiene cargados y cuáles quedaron vencidos.
argument-hint: ""
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/estado.py:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/test_scripts.py:*), Bash(true)
---

# Estado del plugin

```!
python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/estado.py 2>&1 || true
```

Tests de las calculadoras:

```!
python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/test_scripts.py 2>&1 | tail -6 || true
```

## Qué informar

Resumí la salida en pocas líneas. El informe ya viene ordenado por gravedad y cada bloque
vencido dice con qué comando se arregla; **no repitas la tabla entera**, contá lo que importa:

1. **Si el repo se encontró y por qué camino.** Si dice `CODEX_PLUGIN_ROOT` o `CLAUDE_PLUGIN_ROOT`, está instalado
   como plugin y no hay nada que configurar.
2. **Si hay perfil de trabajo.** Si no lo hay, ofrecé `/derecho:configurar` en una línea —
   sin insistir: preguntar en cada conversación es el comportamiento correcto por defecto.
3. **Qué está vencido y qué consecuencia tiene.** Traducilo: una serie sin cargar no es un
   detalle de mantenimiento, es que esa calculadora va a cortar con un marcador en vez de dar
   un número. El calendario de inhábiles sin el año en curso es lo mismo para los plazos.
4. **Si los tests dicen `skipped`, no corrieron: no es verde.** Las seis suites miden el
   repositorio entero y desde la copia instalada se plantan a propósito —falta
   `.claude-plugin/marketplace.json`, la marca que separa el clon del plugin instalado—. Decilo
   así: *no se midió*, y que se corren desde un clon del repo. **Si fallan de verdad**, el
   problema es del plugin y no de los datos.

Cerrá con el comando concreto, uno solo, el más urgente. Si está todo al día, decilo en una
línea y recordá que lo único que no se puede saber sin red es si una norma cambió en la fuente
oficial: eso lo contesta `/derecho:verificar`.
