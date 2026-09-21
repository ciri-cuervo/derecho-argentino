---
name: configurar
description: Entrevista corta para guardar cómo trabajás - modo, jurisdicción y fueros - de modo que la skill ordene sus preguntas de apertura en vez de repetirlas enteras.
argument-hint: "[lo que ya quieras adelantar]"
allowed-tools: Read, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/perfil.py:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/configurar.py:*), Bash(true)
---

Lo que el usuario adelantó: `$ARGUMENTS`

Perfil actual y catálogo de valores válidos:

```!
python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/perfil.py 2>&1 || true
echo "----- OPCIONES -----"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/perfil.py --opciones 2>&1 || true
```

## Cómo llevar la entrevista

Conversada, no un formulario. **Cuatro preguntas, en una sola tanda**, con las opciones a la
vista para que se conteste de corrido. Si el usuario ya adelantó algo arriba, no lo vuelvas a
preguntar.

1. **¿Desde dónde trabajás habitualmente?** Es el campo `modo` y es el que más cambia la
   respuesta: desde el órgano se verifica y se controla de oficio; para una parte se produce
   la pieza y se cuidan las decisiones irreversibles; en estudio se explica el razonamiento.
2. **¿Qué jurisdicciones?** Nacional y federal, CABA, PBA, otra provincia.
3. **¿Qué fueros?** Los que aparezcan seguido. Se pueden marcar varios.
4. **Si es PBA y trabajás en un órgano: ¿qué departamento judicial?** Hay criterios que varían
   por departamento y sirve para advertirlo.

Y una quinta **solo si el usuario la trae**: si dice que le molesta que le pregunten el rol en
cada conversación, ofrecé `rol` + `rol-fijo=si`. **No la ofrezcas de motu proprio.**

Guardá con `perfil.py --set clave=valor`, un `--set` por campo, todo en una sola corrida.

## Lo que hay que decirle, y no es relleno

**El perfil ordena las preguntas; no las contesta.** La skill va a seguir preguntando el rol y
el fuero al abrir, porque la misma persona consulta como tribunal un día y como particular al
otro, y equivocarse de rol cambia el trabajo entero. Lo que se ahorra es tipear las mismas
opciones cada vez.

**El perfil no guarda el CCT**, ni datos de expedientes, ni montos, ni topes. El CCT no es dato
de cartera: surge de lo que las partes invocan y prueban en cada causa. Si el usuario lo
ofrece, explicá por qué no se guarda.

Se cambia cuando quiera con este mismo comando, y se borra con `perfil.py --borrar`.
