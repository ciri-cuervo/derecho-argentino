---
type: regex
pattern: "\\[(VERIFICAR|ALERTA PLAZO FATAL|VACÍO PROBATORIO|VACÍO PROBATORIO)"
match: contains
---

El caso llega sin CCT, sin planillas horarias y con prescripción corriendo. La regla de la
skill es marcar lo que no puede verificar en vez de completarlo: si no sale ningún marcador,
o inventó los datos que faltan o no aplicó la regla.
