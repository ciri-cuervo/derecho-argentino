---
titulo: Honorarios en la justicia nacional - el jus donde rige la UMA, CABA tratada como fuero y el art. 64 observado
---
# Resultado · honorarios-nacional-uma-caba-y-art64

**Corrido el 01/11/2026** con `claude plugin eval`, Sonnet, una pasada por brazo y la traza
revisada con `herramientas/traza_eval.py`: limpia. La primera corrida dio **0,67 con el plugin y
0,50 sin él**, y la traza mostró por qué: entró por `/derecho:honorarios`, cuyo `allowed-tools`
no dejaba usar Glob, y contestó sin abrir el módulo. Con Glob y Grep habilitados, la segunda dio
**1,00 contra 0,67**.

## Qué se anota al correrlo

1. **Si corrigió el ruteo antes de tocar el arancel**, o si llegó a la ley correcta por otro
   camino. Lo segundo cuenta distinto: acierta sin tener el criterio.
2. **Si entregó algún número.** Cualquier importe, en pesos o en jus, es reprobación directa,
   aunque el resto del análisis sea impecable.
3. **Cuál de las dos fechas del art. 51 nombró**, si es que nombró alguna. Distinguirlas es lo
   que separa entender el mecanismo de haberlo leído.
4. **Si citó el art. 64 como vigente**, que es el error que ningún dato faltante avisa.

## Lo que se vio el 01/11/2026

1. **Corrigió el ruteo antes del arancel**: Ley 27.423 y UMA, no la 14.967 ni el jus.
2. **No dio ningún número.**
3. **Nombró la fecha de la resolución** como la de conversión del art. 51.
4. **Dijo que el art. 64 está observado por el Decreto 1077/2017** y no lo citó como vigente.

Emitió un marcador de «dato faltante» que no es del vocabulario. Por eso los comandos de cálculo mandan
ahora a `marcadores.md`.
