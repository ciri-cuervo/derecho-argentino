---
titulo: Le faltan aportes para jubilarse - la compensación de exceso de edad del art. 19 que hay que pedir, y el fuero federal con asiento en la provincia
---
# Resultado · previsional-compensacion-de-edad-y-pba

**Corrido el 01/11/2026** con `claude plugin eval`, Sonnet, una pasada por brazo y la traza
revisada con `herramientas/traza_eval.py`: limpia. La primera corrida dio **0,75 con el plugin y
0,25 sin él**, y lo que reprobó fue el grader y no la respuesta: exigía el contencioso
bonaerense para un beneficio del SIPA. Con la rúbrica corregida contra el art. 15 de la Ley
24.463 —ver `docs/AUDITORIAS.md`—, la segunda dio **1,00 contra 0,50**.

## Qué se anota al correrlo

1. **Si nombró la compensación del art. 19**, y si dijo que hay que pedirla.
2. **Si hizo la cuenta** o prometió sin hacerla.
3. **Si encontró la opción de continuar hasta los 65.**
4. **Si dio algún monto**, que es reprobación directa.

## Lo que se vio el 01/11/2026

1. **Nombró la compensación del art. 19** y dijo que hay que pedirla.
2. **Hizo la cuenta**: tres años de exceso cubren un año y medio, y no alcanza.
3. **Encontró la vía de seguir aportando**, y además la PUAM a los 65.
4. **No dio ningún monto.**

Mandó el reclamo al juzgado federal con asiento en la provincia, y el IPS como alternativa
condicionada. No cotejó el art. 19 contra `fuentes/` y lo dijo.
