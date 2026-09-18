---
titulo: Despido con registración deficiente - tramo Ley 27.742 y agravantes derogados
---
# Resultado esperado · laboral-despido-tramos-reforma-pba

Criterios mínimos de aprobación. No es un análisis de referencia cerrado: cualquier
análisis que cumpla estos criterios se considera válido.

## 1. Nodos bloqueantes, antes del fondo

El análisis debe abrir con dos cosas, no con la liquidación:

- **Fuero y código.** Juzgado del Trabajo del departamento judicial de Morón, PBA.
  Código procesal: **Ley 15.057** (modificada por la Ley 15.557; operativa por Res. SC
  1840/2024 del 03/07/2024, con aplicación inmediata a las causas en trámite en las que no
  se hubiera celebrado la audiencia de vista de causa). **Cuidado con la estructura: la
  Res. SC 1840/24 difirió la operatividad de los arts. 7, 22, 71 a 81, 87 y 90 a 102**, de
  modo que los Juzgados del Trabajo unipersonales y las Cámaras de Apelación del Trabajo
  **no están en funcionamiento** y **no hay recurso de apelación**: sigue actuando el
  Tribunal del Trabajo colegiado, aplicando el rito de la 15.057, y contra su sentencia
  proceden los recursos extraordinarios directos ante la SCBA. Proceso oral; plazos por
  días hábiles, perentorios e improrrogables (art. 17); CPCCBA supletorio (art. 89). **La Ley 11.653 está derogada** por el art. 88 de la Ley 15.057 y
  solo conserva ultraactividad en materia de recusación: citarla como código vigente es un
  error que hace fallar el caso. **SECLO no aplica**: es un instituto del fuero nacional
  (Ley 24.635). Si el sistema pregunta por el SECLO o lo exige como recaudo, el caso falla.
- **Prescripción.** `[ALERTA PLAZO FATAL: art. 256 LCT - 2 años - desde que cada crédito
  fue exigible - vencimiento: calcular por rubro]`, con el desdoblamiento entre los
  créditos indemnizatorios de la extinción y las diferencias salariales de tracto
  sucesivo, que prescriben cuota por cuota.

## 2. El punto que decide el caso: el tramo temporal

El acto extintivo es del **15 de octubre de 2025**. Cae en el tramo **09/07/2024 a
05/03/2026**. De ahí se derivan las dos respuestas que el caso pone a prueba:

- **Base del art. 245:** excluye SAC y conceptos de pago semestral o anual. **Incluye**
  las vacaciones no gozadas, porque esa exclusión la introdujo la Ley 27.802 recién para
  actos extintivos desde el 06/03/2026. Las **horas extras** integran la base en este tramo
  y tampoco están excluidas en el tramo vigente: el texto del art. 245 según el art. 51 de
  la Ley 27.802 excluye SAC, vacaciones y premios que no sean de pago mensual, y **no
  menciona las horas extras**.
- **Agravantes:** ninguno procede. El art. 99 de la Ley 27.742 derogó el bloque completo
  de los **arts. 8 a 17 de la Ley 24.013** (incluidos 8, 9, 10, 11 y 15) y los **arts. 43 a
  48 de la Ley 25.345** (entre ellos el art. 45); el art. 100 derogó los arts. 1 y 2 de la
  Ley 25.323. Todo desde el 09/07/2024.

El caso está construido para tentar al sistema con lo contrario: hay registración
tardía, hay pago parcial en negro y hay una intimación previa en regla. Bajo el régimen
anterior al 09/07/2024 ese cuadro habilitaba los tres agravantes de la Ley 24.013 más la
duplicación del art. 1 de la Ley 25.323. Hoy no habilita ninguno. Un análisis que los
liquide reproduce el error más caro de la práctica post-reforma.

Lo que sí subsiste del reclamo de registración: la antigüedad real (03/02/2017) y la
remuneración real integran la base de cálculo de las indemnizaciones, y la vía de
registración es la de los arts. 7 y ss. de la Ley 24.013 en su texto vigente, incluida
la denuncia directa ante ARCA del art. 7 ter.

## 3. Certificados de trabajo

Sin multa. La obligación del art. 80 LCT subsiste con tres vías de cumplimiento, y el
incumplimiento se persigue por acción de cumplimiento de obligación de hacer con
astreintes (art. 804 CCyCN). Antes de intimar, verificación obligatoria en el servicio
"Trabajo en Blanco" de arca.gob.ar.

## 4. Marcadores que deben aparecer

- `[VERIFICAR CCT APLICABLE: actividad del empleador - dato que falta]`
- `[VERIFICAR MONTO ACTUALIZADO: tope art. 245 LCT - CCT aplicable, promedio INDEC]`
- `[VACÍO PROBATORIO: remuneración real superior a la registrada - aportar recibos reales
  o bancarios]`
- `[VACÍO PROBATORIO: horas extras trabajadas - aportar planillas horarias o testigos]`
- `[ALERTA PLAZO FATAL: art. 256 LCT - ...]`
- `[VERIFICAR TASA VIGENTE: <fuero> - <instrumento>]`

Un análisis que produzca un monto cerrado de indemnización sin el CCT, o que no emita el
marcador de prescripción antes del fondo, no aprueba aunque acierte el tramo temporal.

## 5. Lo que costó correrlo, y qué se aprendió

**Corrido con `claude plugin eval` el 17/09/2026.** Dos corridas, **$16 en total**, y el resultado
no fue el que se esperaba. Va acá para que nadie lo repita a ciegas.

| Qué | Medido |
| --- | --- |
| Un run con plugin | ~$2,10 · 338 s |
| Un run sin plugin (arm de ablación) | ~$0,58 |
| Caso completo: 2 arms × 3 runs | **$8,71 · 992 s** |
| Los 39 casos, si se migraran todos | **del orden de $470 por pasada** |

**El Δ de ablación dio 0,00** —`with` 0,58, `without` 0,58—, pero eso **no medía a la skill**: la
varianza entre runs del mismo arm (0,88 · 0,50 · 0,38) fue mayor que la diferencia entre arms.

**Y tres de los cuatro graders LLM estaban mal.** Leída la traza, la respuesta cumplía los tres
criterios que el juez reprobaba: nombra los agravantes con la leyenda *"Derogados por el art. 99
Ley 27.742"*, no cita la Ley 11.653 ni una vez, y dice *"Tramo de reforma aplicado: Ley 27.742, por
acto extintivo del 15/10/2025"*. **Los tres eran criterios negativos o con varios hechos
encadenados**, que es lo que un juez chico da vuelta. Los seis de regex acertaron el 100%.

**Reescritos en positivo y partidos en un hecho cada uno**, que es la regla que este caso ya
enunciaba en `antiguedad-multiplicador` y que los otros no seguían.

**Dos defectos de la skill que la traza sí mostró**, y que no necesitan otra corrida: un run murió
en el límite de **30 turnos**, y otro no emitió **ningún marcador** pese a que la consulta tiene
datos faltantes de sobra. Se persiguen leyendo, no pagando.
