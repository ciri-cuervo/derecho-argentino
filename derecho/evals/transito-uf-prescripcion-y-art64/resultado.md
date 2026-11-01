---
titulo: Multa de tránsito en PBA - valor de la UF, prescripción del art. 89 y el art. 64 usado como factor de atribución
---
# Resultado · transito-uf-prescripcion-y-art64

**Corrido el 01/11/2026** con `claude plugin eval`, Sonnet, una pasada por brazo y la traza
revisada con `herramientas/traza_eval.py`: limpia. **1,00 con el plugin y 0,60 sin él.**

## Qué se anota al correrlo

1. **Qué archivos abrió**, en orden, antes de contestar. El caso cruza faltas y civil: si sólo
   abrió uno, se anota cuál.
2. **Cuántas de las cinco afirmaciones corrigió**, y cuáles dejó pasar. Es el dato que dice si el
   módulo está bien escrito o si el error está en cómo lo dice.
3. **Si dio un número en pesos.** Cualquier importe sin el marcador de la UF es una falla, aunque
   el número fuera correcto ese día.
4. **Si levantó el plazo del art. 72 bis sin que se lo preguntaran.** Es un plazo fatal y el caso
   lo esconde en un dato de contexto —la Boleta de Citación— en vez de nombrarlo.

## Lo que se vio el 01/11/2026

1. **Abrió `transito.md` y después `civil.md`**, en ese orden, y buscó en el texto de la Ley 24.449.
2. **Las cinco afirmaciones quedaron corregidas**: los cinco graders aprobaron.
3. **No dio ningún importe en pesos.**
4. **Levantó el art. 72 bis sin que se lo preguntaran**, con `[ALERTA PLAZO FATAL: ...]` desde la
   Boleta de Citación.
