---
name: notarial-escritura-fe-publica-y-segunda-copia
tags: [notarial, escritura, prueba, caba, pba]
plugins: ["../.."]
runs: 1
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: |
  Estás respondiendo una consulta escrita: no hay nadie del otro lado para contestar
  repreguntas. Analizá con los datos que están en el mensaje, y lo que falte para cerrar
  una respuesta marcalo con el marcador que corresponda en vez de pedirlo y detenerte.
---

# Caso · Una escritura de compraventa y un acta de constatación

## Datos aportados por el consultante

### Los hechos

EL CONSULTANTE compró un inmueble ubicado en el partido de La Plata, Provincia de Buenos Aires.
La escritura se otorgó el **12 de marzo de 2026 en la Ciudad Autónoma de Buenos Aires**, ante un
escribano titular de un registro de la Ciudad, y ambas partes concurrieron y firmaron.

La escritura dice, en cláusula tercera, que **el precio fue recibido por el vendedor con
anterioridad al acto**, y el escribano dejó constancia de que las partes así lo manifestaron. EL
CONSULTANTE sostiene que esa manifestación se firmó para agilizar el trámite y que **una parte
del precio quedó pendiente**, y que hay transferencias bancarias posteriores que lo demuestran.

La misma escritura contiene una cláusula donde **el vendedor se obliga a desocupar y entregar la
unidad dentro de los sesenta días**, cosa que no ocurrió.

EL CONSULTANTE le pidió al escribano **una segunda copia** de la escritura y el escribano se la
negó por escrito.

Además encargó a otro escribano, en La Plata, un **acta de constatación** en la puerta del
inmueble. El acta dice que el encargado del edificio **manifestó que el vendedor sigue viviendo
ahí y que no piensa mudarse**.

### Estado actual

Fecha de la consulta: **10 de septiembre de 2026**. No inició ninguna acción. No aporta tasación
ni monto reclamado: quiere saber qué se puede discutir y con qué.

---

## Consulta

El abogado de EL CONSULTANTE consulta:

1. Para discutir que el precio no se pagó del todo, ¿hay que redargüir de falsedad la escritura?
2. ¿La escritura vale, si el inmueble está en La Plata y se hizo en la Ciudad ante un escribano
   porteño?
3. El escribano niega la segunda copia. ¿Puede?
4. El acta dice que el encargado declaró que el vendedor sigue viviendo ahí. ¿Eso lo prueba?
