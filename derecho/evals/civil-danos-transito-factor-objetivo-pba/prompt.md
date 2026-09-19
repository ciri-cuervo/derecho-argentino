---
name: civil-danos-transito-factor-objetivo-pba
tags: [civil, danos, transito, pba, prescripcion]
plugins: ["../.."]
runs: 3
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: |
  Estás respondiendo una consulta escrita: no hay nadie del otro lado para contestar
  repreguntas. Analizá con los datos que están en el mensaje, y lo que falte para cerrar
  una respuesta marcalo con el marcador que corresponda en vez de pedirlo y detenerte.
---

# Caso · Peatón embestido - daños y perjuicios

## Hechos aportados por el cliente

### El accidente

EL DAMNIFICADO, peatón, fue embestido por una camioneta el **12 de mayo de 2023**,
mientras cruzaba una avenida por la senda peatonal en la ciudad de La Plata, Provincia
de Buenos Aires. El conductor de la camioneta circulaba dentro de la velocidad máxima
permitida según su propio relato en la causa contravencional, que terminó archivada.

EL DAMNIFICADO sufrió fractura de tibia y peroné, fue operado y estuvo cuatro meses sin
poder trabajar. Es trabajador independiente. Aporta historia clínica, facturas de
gastos médicos y de traslados, y constancias de ingresos de los dos años anteriores al
hecho. **No hay pericia médica ni informe de incapacidad.**

### El seguro

La camioneta es de titularidad de una empresa de logística y estaba asegurada. La
póliza, según la carta que la aseguradora envió rechazando el reclamo extrajudicial,
tiene una **franquicia deducible** de un monto que la carta no especifica.

### La instancia previa

El abogado inició la **mediación prejudicial obligatoria en PBA el 10 de marzo de 2026**.
El acta de cierre sin acuerdo se expidió el **22 de abril de 2026**.

### Estado actual

Fecha de la consulta: **20 de agosto de 2026**. No se inició la demanda.

---

## Consulta

El abogado de EL DAMNIFICADO consulta:

1. Quiero armar la demanda probando la culpa del conductor. ¿Qué prueba necesito para
   acreditar que manejaba con imprudencia?
2. ¿Cuánto puedo reclamar por incapacidad sobreviniente?
3. ¿Demando directamente a la aseguradora?
4. ¿Estoy en término?
