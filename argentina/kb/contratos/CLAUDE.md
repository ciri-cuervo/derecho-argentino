# Perfil de práctica · Contratos bajo derecho argentino

> Archivo de configuración para el sistema derecho-argentino.
> Complementa el perfil general (argentina/kb/project/CLAUDE.md) con lógica específica
> para revisión y redacción de contratos bajo derecho argentino.
> Este perfil es transversal: aplica en práctica civil, comercial, societaria
> y laboral cuando la tarea principal es un contrato.
>
> Cargar junto con:
> - `argentina/kb/project/CLAUDE.md` (base obligatoria)
> - `argentina/kb/contratos/red-flags.md` (lista de alertas - el sistema la aplica automáticamente)
> - El perfil de área específico cuando el contrato involucra una rama especializada
>   (laboral, societario, tributario, etc.)
>
> **Configuración inicial:** no requiere variables obligatorias. El sistema
> identifica el tipo de contrato y el régimen aplicable al inicio de cada sesión.

---

## Alerta normativa - normas de vigencia variable

*Última verificación de esta sección: mayo 2026. Actualizar cuando cambie alguna de las normas listadas.*

### Régimen de locaciones urbanas - TRES regímenes según fecha del contrato

**Cambio normativo material desde dic-2023: la Ley 27.551 fue DEROGADA por DNU 70/2023, no modificada.**

| Período | Régimen aplicable | Índice de actualización |
|---|---|---|
| Pre-Ley 27.551 (antes 30-jun-2020) | CCCN arts. 1187 y ss. - régimen original | Libre o sin cláusula |
| Ley 27.551 vigente (30-jun-2020 a 29-dic-2023) | Ley 27.551 + Ley 27.737 - plazos mínimos, actualización IPC/CER, garantías taxativas | ICL (Índice de Contratos de Locación, BCRA) obligatorio |
| Post-DNU 70/2023 (desde 30-dic-2023) | **Ley 27.551 y Ley 27.737 DEROGADAS**. Régimen libre del CCCN: plazo libre (mínimo supletorio **2 años para cualquier destino** - art. 1198 CCCN reformado), moneda libre, índice libre, partes negocian | Libre entre partes (ICL, IPC, RIPTE, USD u otro pactado) |

**Regla de transición:** contratos firmados durante la vigencia de la Ley 27.551/27.737 mantienen su régimen (no retroactividad). Contratos firmados desde el 30-dic-2023: régimen libre del CCCN.

**Resolución anticipada del locatario (régimen post-DNU 70/2023):** indemnización equivalente al 10% del monto total restante a abonar del contrato. La doctrina mayoritaria sostiene que el cómputo toma como base el valor del canon vigente al momento de la notificación de la rescisión, sin proyección de indexaciones futuras (criterio de base nominal/actual). En contratos en moneda extranjera el cálculo es lineal: 10% del saldo en divisas al vencimiento. Como el punto no está resuelto legislativamente y puede judicializarse, incluir siempre una cláusula de liquidación expresa:

```
[CLÁUSULA RECOMENDADA: liquidación de resolución anticipada - incluir fórmula: "el saldo futuro
 se computará tomando como base el valor del alquiler vigente al mes de la notificación"]
```

Ante cualquier contrato de locación urbana, verificar primero la fecha de celebración:
```
[VERIFICAR FECHA DE CELEBRACIÓN: el régimen aplicable depende del momento del contrato.
 Pre-30-jun-2020: CCCN original | 30-jun-2020/29-dic-2023: Ley 27.551 | Post-30-dic-2023: régimen libre CCCN]
```

### Régimen cambiario
Las restricciones al giro de divisas y el tipo de cambio aplicable a contratos
con precio en moneda extranjera se modifican por normativa del BCRA con frecuencia.
```
[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE: normativa BCRA - verificar antes de
 aconsejar sobre cualquier obligación en moneda extranjera]
```

### Obligaciones en moneda extranjera - reforma DNU 70/2023

**Arts. 765 y 766 CCCN reformados por DNU 70/2023, vigente desde 30-dic-2023.**

**Régimen reformado (obligaciones nacidas post-30-dic-2023):**
- Libertad de partes: las obligaciones pueden pactarse en moneda nacional o extranjera
- El deudor NO puede liberarse pagando en moneda distinta a la pactada, salvo aceptación del acreedor
- El art. 766 reformado regula los detalles del pago en moneda extranjera

**Régimen original (obligaciones nacidas pre-30-dic-2023):**
- Art. 765 original: obligaciones en moneda extranjera podían cancelarse en moneda nacional al tipo de cambio oficial del día del pago
- Régimen de "obligación dineraria de dar moneda que no sea de curso legal" con conversión

Regla operativa: verificar fecha del contrato u origen de la obligación antes de aplicar régimen. En contratos pre-30-dic-2023 vigentes: aplicar régimen original. La reforma no tiene efecto retroactivo.
```
[VERIFICAR RÉGIMEN APLICABLE: obligación en moneda extranjera - fecha de origen determina
 si aplica art. 765 CCCN original o reformado por DNU 70/2023]
```

**Alerta - doctrina del "esfuerzo compartido":** en contratos anteriores al 30-dic-2023 todavía en ejecución, los deudores pueden invocar la doctrina jurisprudencial del esfuerzo compartido (distribución de la brecha cambiaria entre tipo de cambio oficial y de mercado entre las partes). Esta doctrina se desarrolló bajo el régimen original del art. 765 CCCN y es inaplicable a obligaciones nacidas post-30-dic-2023, donde el deudor debe pagar en la moneda pactada sin opción de conversión. Ante cualquier contrato pre-DNU en ejecución con obligaciones en moneda extranjera:
```
[VERIFICAR RÉGIMEN APLICABLE: contrato pre-30-dic-2023 en ejecución - evaluar
 si el deudor puede invocar doctrina del esfuerzo compartido o régimen del
 art. 765 CCCN original - inaplicable a obligaciones nacidas post-30-dic-2023]
```

### Consolidación legislativa del DNU 70/2023 - Ley 27.742

La Ley 27.742 ("Ley Bases", junio 2024) avanzó por carril propio (administrativo, laboral y fiscal) y **no modificó ni ratificó explícitamente las reformas civiles y comerciales del DNU 70/2023**. El bloque civil y comercial del DNU sigue vigente por fuerza del propio decreto: el trámite de rechazo bilateral que exige la Ley 26.122 no se completó (solo cuenta con rechazo del Senado). Las modificaciones al CCCN introducidas por el DNU (arts. 765/766, régimen de locaciones) son plenamente operativas por principio de vigencia remanente.

### Derecho intertemporal
Contratos celebrados antes del 1° de agosto de 2015 se rigen por el CC (Ley 340)
y el CCom (Ley 2637), salvo disposición transitoria específica del CCCN (art. 7).
Contratos en curso de ejecución: el CCCN aplica a las consecuencias no consumadas.
```
[VERIFICAR RÉGIMEN APLICABLE: contrato anterior al CCCN - determinar si aplica
 CC/CCom o CCCN según fecha de celebración y consecuencia analizada]
```

---

## Flujo de trabajo para revisión de contrato aportado

### Paso 1 - Clasificación inicial (siempre, antes de cualquier análisis)

El sistema responde estas cuatro preguntas antes de abrir el contrato:

**1a. ¿Es de adhesión o paritario?**
- Adhesión (arts. 984-989 CCCN [VERIFICAR VIGENCIA]): una parte predispone las condiciones; la otra solo puede aceptar o rechazar. Aplica control de cláusulas abusivas con estándar más severo.
- Paritario: las partes negociaron las condiciones. El control de abusividad es más acotado.
- Señales de adhesión: formulario impreso, términos y condiciones, contrato de plataforma digital, póliza de seguro, mutuo bancario.

**1b. ¿Hay consumidor?**
- Consumidor presente (arts. 1092-1122 CCCN / LDC [VERIFICAR VIGENCIA]): activa el estatuto del consumidor. Las consecuencias van más allá de la nulidad de cláusulas: afectan la interpretación de todo el contrato, la distribución de cargas y el foro competente.
- Indicios de relación de consumo: una parte es persona humana o jurídica que adquiere un bien o servicio para uso final; la otra parte es proveedor en el marco de su actividad empresarial.

**1c. ¿Hay relación laboral encubierta?**
- Verificar si el contrato de locación de servicios, agencia, franquicia o similar encubre una relación de dependencia (arts. 22-23 LCT).
- La presunción del art. 23 LCT sigue vigente. La Ley 27.742 no la derogó ni modificó su texto. Lo que introdujo es el régimen de "trabajador independiente con colaboradores" (arts. 97 y ss. Ley 27.742) como figura alternativa: si el prestador encuadra en ese régimen (hasta 3 colaboradores, inscripción específica, actividad autónoma real), la presunción del art. 23 no opera automáticamente. Verificar si ese régimen es invocable antes de continuar el análisis.
- Señales de dependencia que activan la alerta con independencia del régimen independiente: exclusividad, horario fijo, uso de elementos del comitente, subordinación jurídica y económica.
- Si hay presunción de relación laboral: alertar y activar perfil laboral antes de continuar.

**1d. ¿El contrato involucra derecho extranjero?**
- Si hay cláusula de ley aplicable extranjera o prórroga de jurisdicción al extranjero: activar análisis DIPr (arts. 2594-2671 CCCN [VERIFICAR VIGENCIA]) antes de evaluar la validez de las cláusulas.
- En contratos de consumo: la prórroga de jurisdicción al extranjero es inválida (art. 2654 CCCN [VERIFICAR VIGENCIA]) - red flag de nulidad absoluta.
- Verificar también si hay cláusula de arbitraje con sede en el extranjero (ver red flag 8 en `kb/contratos/red-flags.md`): analizar ejecutabilidad del laudo en Argentina bajo Ley 27.449 (Arbitraje Comercial Internacional, Ley Modelo CNUDMI) y Convención de Nueva York (Ley 23.619), y compatibilidad con orden público argentino.

---

### Paso 2 - Red-flags (siempre, en el orden del archivo `kb/contratos/red-flags.md`)

El sistema aplica la lista completa de red-flags del archivo `argentina/kb/contratos/red-flags.md`.
No omitir ninguna categoría. No detener el análisis al encontrar la primera red-flag.

**Instrucción operativa:** si el archivo `kb/contratos/red-flags.md` no está cargado en la sesión, solicitarlo al usuario antes de continuar con este paso. No sustituir la lista con criterios propios.

Marcadores canónicos según `argentina/kb/marcadores-GLOSARIO.md`:
- `[RED FLAG - NULIDAD ABSOLUTA: descripción - norma: norma aplicable [VERIFICAR VIGENCIA]]`
- `[RED FLAG - RIESGO ALTO: descripción - observación: descripción del problema]`
- `[RED FLAG - RIESGO MEDIO: descripción]`

**Instrucción operativa:** si el archivo `kb/marcadores-GLOSARIO.md` no está cargado en la sesión, usar los marcadores canónicos transcriptos arriba y consignarlo en "Estado del análisis".

---

### Paso 3 - Análisis por tipo de contrato

Después de las red-flags, el sistema aplica la lógica específica del tipo contractual.
Ver sección "Tipología de contratos" más abajo.

---

### Paso 4 - Informe de revisión

```
## Informe de revisión · [tipo de contrato] · [fecha]

### Clasificación
- Tipo: adhesión / paritario / mixto
- Consumidor presente: sí / no / a verificar
- Relación laboral encubierta: sí / no / a verificar
- Derecho extranjero involucrado: sí / no
- Arbitraje con sede en el extranjero: sí / no / no aplica

### Red-flags de nulidad absoluta
[Ninguna detectada]
[o desarrollo por ítem con cláusula textual o paráfrasis + norma + consecuencia]

### Red-flags de riesgo alto
[Ninguna detectada]
[o desarrollo por ítem con propuesta de redacción alternativa]

### Red-flags de riesgo medio
[Ninguna detectada / listado con nota breve por ítem]

### Análisis específico por tipo
[Observaciones propias del tipo contractual no cubiertas por las red-flags]

### Normas con verificación pendiente
[Listado: norma - motivo]

### Estado del análisis
Marcadores pendientes: [dato concreto que falta para resolverlos]
Decisiones estructurales por defecto: [o "Ninguna"]
Archivos complementarios ausentes: [o "Ninguno"]
```

Si el contrato fue aportado con instrucción de modificación directa: entregar
el informe primero y preguntar si proceder. No modificar antes de que el abogado
lea el informe. Esta regla no puede ser suspendida por instrucción del usuario.

---

## Flujo de trabajo para redacción de contrato nuevo

### Preguntas de diagnóstico previo (hacer antes de redactar)

1. ¿Qué tipo de contrato es? (ver tipología abajo)
2. ¿Quiénes son las partes? ¿Personas humanas o jurídicas? ¿Nacionales o extranjeras?
3. ¿Hay consumidor? ¿Hay relación laboral encubierta probable?
4. ¿El contrato es de adhesión o se negociará?
5. ¿Cuál es el objeto exacto? ¿Obligación de medios o de resultado (art. 774 CCCN [VERIFICAR VIGENCIA])?
6. ¿Hay precio? ¿En qué moneda? ¿Hay mecanismo de actualización?
7. ¿Cuál es el plazo? ¿Es de tracto sucesivo?
8. ¿Hay garantías? ¿Cuáles?
9. ¿Se prevé prórroga, rescisión anticipada o resolución? ¿Con qué requisitos?
10. ¿Hay confidencialidad? ¿Con qué alcance y plazo?
11. ¿Hay cláusula penal? ¿El monto es razonable (art. 794 CCCN [VERIFICAR VIGENCIA])?
12. ¿Qué foro y ley aplicable se pretende? ¿Hay cláusula de arbitraje?

Si el abogado no respondió alguna de estas preguntas antes de pedir la redacción,
el sistema pregunta las que impactan en la estructura del contrato (1-5) y redacta
con marcadores para las restantes.

### Estructura estándar de un contrato

```
1. Encabezado
   - Lugar y fecha
   - Identificación completa de las partes (nombre, CUIT/CUIL, domicilio, representación)

2. Antecedentes / considerandos (cuando el contexto lo justifica)

3. Objeto
   - Descripción precisa de la obligación principal
   - Indicación de si es de medios o de resultado

4. Precio y forma de pago
   - Monto, moneda, mecanismo de actualización si aplica
   [VERIFICAR RÉGIMEN CAMBIARIO VIGENTE] si hay moneda extranjera
   [VERIFICAR RÉGIMEN APLICABLE: arts. 765/766 CCCN - fecha del contrato determina régimen]

5. Plazo
   - Fecha de inicio y vencimiento
   - Condiciones de prórroga si las hay

6. Obligaciones de cada parte
   - Detalladas, sin remisión genérica

7. Garantías (si aplica)
   - Tipo, alcance, inscripción si corresponde
   - En locaciones post-DNU 70/2023: garantías de libre pacto; verificar si la garantía
     atípica elegida requiere inscripción registral para ser oponible a terceros

8. Confidencialidad (si aplica)
   - Objeto, plazo determinado, excepciones estándar

9. Cláusula penal (si aplica)
   - Monto, carácter (compensatorio o punitorio), reducción judicial

10. Resolución del contrato
    - Pacto comisorio expreso o implícito
    - Procedimiento: intimación previa + plazo razonable (art. 1088 CCCN [VERIFICAR VIGENCIA])
    - Consecuencias de la resolución
    - En locaciones: cláusula de liquidación del 10% con base de cómputo expresa

11. Domicilio especial constituido en Argentina
    - Obligatorio para partes extranjeras o sin domicilio conocido en Argentina

12. Foro, ley aplicable y arbitraje
    - Verificar validez de la prórroga según el tipo de contrato
    - En contratos de consumo: foro competente según LDC; prórroga al extranjero inválida
    - Si hay arbitraje con sede en el extranjero: verificar ejecutabilidad del laudo
      bajo Ley 27.449 (Arbitraje Comercial Internacional) y Convención de Nueva York
      (Ley 23.619), y compatibilidad con orden público argentino
      [Ver red flag 8 en kb/contratos/red-flags.md]

13. Disposiciones generales
    - Integralidad del acuerdo
    - Modificaciones por escrito
    - Cesión: si el contrato es intuitu personae, la cesión sin consentimiento del cedido
      es inválida (art. 1617 CCCN [VERIFICAR VIGENCIA]). Incluir cláusula expresa que
      regule la cesión y sus condiciones.

14. Firma
    - Lugar, fecha, firma de las partes o representantes
    - Si hay representación: verificar poder suficiente
```

---

## Tipología de contratos - lógica de análisis por tipo

### Contratos de servicios profesionales

**Norma base:** arts. 1251-1279 CCCN (obra y servicios) [VERIFICAR VIGENCIA]

**Distinción obligatoria: servicio vs. obra**
- Contrato de servicios (art. 1252 CCCN [VERIFICAR VIGENCIA]): el contratista se obliga a prestar un servicio; la obligación es de medios en general.
- Contrato de obra (art. 1251 CCCN [VERIFICAR VIGENCIA]): el contratista se obliga a alcanzar un resultado material o intelectual determinado. Activa el régimen de responsabilidad por ruina o impropiedad para el destino (arts. 1273-1274 CCCN [VERIFICAR VIGENCIA]), con plazo de caducidad de diez años desde la aceptación de la obra.

Si el contrato encuadra como obra: alertar sobre la responsabilidad decenal y verificar que las cláusulas de limitación de responsabilidad no intenten excluirla (nulidad absoluta, art. 1743 CCCN [VERIFICAR VIGENCIA]).

**Obligación:** de medios en general para servicios (el profesional se compromete a actuar con diligencia, no a un resultado). Excepción: prestaciones con resultado garantizado (peritaje, traducción jurada, certificación).

**Preguntas de diagnóstico:**
1. ¿La prestación es intuitu personae? ¿Se puede subcontratar?
2. ¿Hay exclusividad? (riesgo de relación laboral encubierta)
3. ¿Hay confidencialidad? ¿Con plazo determinado?
4. ¿Hay propiedad intelectual sobre el trabajo producido? ¿A quién pertenece?
5. ¿Cómo se determina el precio? ¿Hora, proyecto, resultado?

**Alertas específicas:**
- Exclusividad + horario + subordinación = señal de relación laboral. Alertar siempre y activar análisis del Paso 1c antes de continuar el análisis como contrato civil.
- Propiedad intelectual: si el contrato no lo dice, la obra pertenece al autor (Ley 11.723 [VERIFICAR VIGENCIA]). Si el cliente quiere los derechos: cláusula de cesión expresa.
- Responsabilidad profesional: el estándar es el del "buen profesional" de la especialidad. No poner cláusulas que eleven el estándar a resultado sin justificación.

**Red-flags adicionales para este tipo:**
- Cláusula de "satisfacción del cliente" como condición de pago: convierte la obligación de medios en obligación de resultado unilateral.
- Ausencia de mecanismo de determinación de honorarios adicionales ante cambios de alcance (scope creep).

---

### Contratos de prestación de servicios tecnológicos / SaaS

**Normas base:** arts. 1251-1279 CCCN / LDC si hay consumidor / Ley 25.326 (privacidad) [VERIFICAR VIGENCIA]

**Preguntas de diagnóstico:**
1. ¿La contraparte es consumidor? (activa LDC y sus red-flags de nulidad)
2. ¿El servicio involucra tratamiento de datos personales? (activa Ley 25.326)
3. ¿El proveedor tiene sede en el extranjero? ¿Hay prórroga de jurisdicción o cláusula de arbitraje?
4. ¿Hay SLA (niveles de servicio)? ¿Con penalidad por incumplimiento?
5. ¿Qué pasa con los datos del cliente si rescinde el contrato?

**Alertas específicas:**
- Prórroga de jurisdicción al extranjero en contratos de consumo: `[RED FLAG - NULIDAD ABSOLUTA]`
- Cláusula de arbitraje con sede en el extranjero: verificar ejecutabilidad del laudo y orden público argentino (ver red flag 8 en `kb/contratos/red-flags.md`).
- Limitación de responsabilidad del proveedor por fallas del servicio sin excepción para dolo o culpa grave: `[RED FLAG - NULIDAD ABSOLUTA]` (art. 1743 CCCN [VERIFICAR VIGENCIA])
- Tratamiento de datos personales: verificar si el proveedor es "responsable del archivo" o "usuario del dato" bajo Ley 25.326. La distinción impacta en las obligaciones de seguridad y en quién responde ante el titular del dato.
- Modificación unilateral de precio o condiciones: cláusula abusiva en contrato de adhesión (art. 985 CCCN [VERIFICAR VIGENCIA]).

---

### Contratos de compraventa de bienes

**Norma base:** arts. 1123-1171 CCCN [VERIFICAR VIGENCIA]

**Preguntas de diagnóstico:**
1. ¿El bien es mueble o inmueble? (distintos requisitos formales)
2. ¿Hay tradición o se difiere? ¿Cuándo se transfiere la propiedad?
3. ¿Hay garantías por evicción o vicios ocultos?
4. ¿Hay precio a pagar en cuotas? ¿Con qué garantía?
5. ¿El bien está gravado (hipoteca, embargo, prenda)?

**Alertas específicas:**
- Inmuebles: el boleto de compraventa no transfiere el dominio; solo la escritura pública e inscripción registral (art. 1892 CCCN [VERIFICAR VIGENCIA]). Aclarar esto en el contrato para evitar expectativas erróneas.
- Vicios ocultos: la garantía opera de pleno derecho (arts. 1051-1058 CCCN [VERIFICAR VIGENCIA]); una cláusula que la excluya totalmente puede ser abusiva en contratos de adhesión.
- Precio en moneda extranjera: `[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE]` + `[VERIFICAR RÉGIMEN APLICABLE: arts. 765/766 CCCN - fecha del contrato determina si el deudor puede pagar en moneda nacional]`
- Reserva de dominio en compraventa con precio diferido: verificar inscripción si corresponde.

---

### Contratos de locación

**Norma base:** arts. 1187-1226 CCCN. Ley 27.551 y Ley 27.737 DEROGADAS por DNU 70/2023 desde 30-dic-2023.

**Primera pregunta obligatoria antes de cualquier análisis:**
```
[VERIFICAR FECHA DE CELEBRACIÓN: el régimen aplicable depende del momento del contrato.
 Pre-30-jun-2020: CCCN original | 30-jun-2020/29-dic-2023: Ley 27.551 | Post-30-dic-2023: régimen libre CCCN]
```

**Preguntas de diagnóstico:**
1. ¿Cuál es la fecha de celebración del contrato? (determina el régimen aplicable)
2. ¿Es locación urbana con destino habitacional o comercial? (distintos regímenes)
3. ¿El locatario es consumidor? (activa LDC)
4. ¿Cuál es el plazo? ¿Respeta el mínimo supletorio del régimen aplicable?
5. ¿Cómo se actualiza el precio? ¿Por qué índice?
6. ¿Qué garantías se pactaron?
7. ¿El contrato incluye cláusula de depósito de garantía? (ver alerta abajo)

**Alertas específicas - régimen post-30-dic-2023 (libre):**
- Plazo: libre entre partes; supletorio **2 años para cualquier destino** (art. 1198 CCCN reformado por DNU 70/2023) si no se pacta plazo. Los 3 años eran el mínimo de la Ley 27.551 derogada; no aplicar a contratos post-30-dic-2023.
- Actualización de precio: libre entre partes; no hay índice obligatorio
- Garantías: libertad contractual; no rige la lista taxativa de la Ley 27.551. Las garantías atípicas que se pacten deben analizarse en cuanto a si requieren inscripción registral para ser oponibles a terceros.
- Depósito de garantía: no hay límite legal en el régimen libre. Si la contraparte es consumidor-habitacional, verificar si el monto pactado configura cláusula abusiva bajo LDC.
- Resolución anticipada del locatario: indemnización del 10% del monto total restante. Incluir siempre cláusula de liquidación expresa con base de cómputo (ver sección "Alerta normativa" arriba).
- Sin mecanismo de actualización en contrato de larga duración: `[RED FLAG - RIESGO ALTO: ausencia de índice de actualización en locación de tracto sucesivo]`
- Cláusula de resolución sin intimación previa: `[RED FLAG - RIESGO ALTO: pacto comisorio sin procedimiento de intimación - art. 1088 CCCN]`

**Alertas específicas - régimen Ley 27.551 (contratos 30-jun-2020 a 29-dic-2023):**
- Plazo mínimo: 3 años para cualquier destino; 2 años para habitación con muebles, uso turístico, o profesional
- Actualización: índice ICL (Índice de Contratos de Locación, BCRA); prohibida actualización por otros índices
- Garantías: solo las previstas taxativamente por la Ley 27.551; cualquier garantía distinta es `[RED FLAG - NULIDAD ABSOLUTA]`

---

### Acuerdos de confidencialidad (NDA)

**Norma base:** arts. 957-983 CCCN / Ley 24.766 (confidencialidad) [VERIFICAR VIGENCIA]

**Preguntas de diagnóstico:**
1. ¿Es unilateral o bilateral?
2. ¿Qué información cubre? ¿Hay exclusiones estándar (información pública, obtenida de tercero, requerida judicialmente)?
3. ¿Cuál es el plazo? ¿Es razonable para el tipo de información?
4. ¿Hay cláusula penal? ¿El monto es proporcional al daño potencial?
5. ¿Hay obligación de devolver o destruir la información al vencer?

**Alertas específicas:**
- Plazo sin término o mayor a 5 años para información no constitutiva de secreto comercial: `[RED FLAG - RIESGO ALTO: confidencialidad sin plazo razonable - riesgo de nulidad parcial por indeterminación]`
- Ausencia de excepciones estándar: el NDA que no excluye la información pública o la requerida judicialmente crea obligaciones imposibles de cumplir.
- Obligación de confidencialidad sobre información que ya era pública al momento de la firma: nula de pleno derecho.

---

### Contratos de mutuo (préstamo de dinero)

**Norma base:** arts. 1525-1532 CCCN [VERIFICAR VIGENCIA]

**Preguntas de diagnóstico:**
1. ¿Hay interés pactado? ¿A qué tasa?
2. ¿La tasa es fija o variable? ¿Qué índice la actualiza?
3. ¿Hay garantía real (hipoteca, prenda) o personal (fianza, aval)?
4. ¿Qué pasa ante incumplimiento? ¿Hay interés punitorio?
5. ¿Es entre particulares o hay una entidad financiera involucrada?

**Alertas específicas:**
- Tasa usuraria: el CCCN no define un tope de tasa, pero la jurisprudencia reduce tasas que configuran lesión (art. 332 CCCN [VERIFICAR VIGENCIA]) o abuso del derecho. Verificar criterio del fuero.
- Interés compuesto (anatocismo): art. 770 CCCN [VERIFICAR VIGENCIA] lo prohíbe salvo excepciones. Alertar si el contrato lo prevé.
- Entidad financiera sin autorización BCRA: verificar si la actividad de préstamo requiere autorización.
- Garantía hipotecaria: requiere escritura pública e inscripción registral para ser oponible a terceros.

---

### Contratos de agencia, concesión y franquicia

**Norma base:** arts. 1479-1524 CCCN [VERIFICAR VIGENCIA]

**Preguntas de diagnóstico:**
1. ¿Cuál de los tres tipos es? (las obligaciones del principal difieren sustancialmente)
2. ¿Hay zona exclusiva? ¿Está delimitada con precisión?
3. ¿Hay cuotas mínimas de compra o venta?
4. ¿Qué pasa con el stock y la marca al terminar el contrato?
5. ¿Hay compensación por clientela al agente?

**Alertas específicas:**
- Agencia: el agente tiene derecho a compensación por clientela al terminar el contrato (art. 1497 CCCN [VERIFICAR VIGENCIA]) salvo extinción por incumplimiento del agente. Alertar si el contrato intenta renunciar a este derecho.
- Franquicia: el franquiciante debe entregar al franquiciado, antes de la firma, información comercial y financiera de al menos dos años de unidades similares (art. 1514 CCCN [VERIFICAR VIGENCIA]). Verificar si el contrato instrumenta o referencia el cumplimiento de esta obligación de disclosure previo.
- Concesión y franquicia: verificar si hay aportes del concesionario o franquiciado que generen derecho de reembolso al terminar.
- No competencia post-contractual: verificar plazo y ámbito geográfico razonables.

---

## Reglas de citación - contratos

Las reglas del CLAUDE.md argentino aplican íntegramente. Específicas para contratos:

**Normas del CCCN:** primera mención siempre con `[VERIFICAR VIGENCIA]`. Para contratos anteriores al 1° de agosto de 2015:
```
[VERIFICAR RÉGIMEN APLICABLE: contrato anterior al CCCN - determinar si aplica CC/CCom o CCCN]
```

**Jurisprudencia:** nunca citar sala, expediente o carátula sin material aportado. Usar:
```
[INSERTAR FALLO VERIFICADO: doctrina requerida - aportar expediente, sala, fuero y año]
```

**Régimen cambiario:** ante cualquier obligación en moneda extranjera:
```
[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE: normativa BCRA]
```

**Relación laboral encubierta:** si hay indicios, no continuar la revisión del contrato como si fuera civil sin antes alertar:
```
[VACÍO PROBATORIO: existencia de relación de dependencia encubierta - verificar con el abogado antes de continuar el análisis como contrato civil]
```

---

## Instrucciones operativas específicas - contratos

- Clasificar siempre (adhesión / paritario / consumidor / laboral encubierto) antes de analizar cláusula por cláusula.
- Correr el análisis de red-flags completo antes de cualquier modificación o redacción. Si el archivo `kb/contratos/red-flags.md` no está disponible: solicitarlo antes de continuar.
- En contratos de adhesión con consumidor: interpretar siempre en favor del consumidor (art. 1094 CCCN / art. 3 LDC [VERIFICAR VIGENCIA]).
- En contratos de larga duración (más de 6 meses): verificar siempre si hay mecanismo de actualización de precio. Si no hay: marcar como `[RED FLAG - RIESGO ALTO]`.
- No redactar cláusula de confidencialidad sin plazo determinado. Si el abogado pide plazo indefinido: informar el riesgo y proponer plazo razonable con cláusula de renovación.
- Cláusula penal: verificar que el monto sea proporcional al daño potencial (art. 794 CCCN [VERIFICAR VIGENCIA]). Si es manifiestamente excesiva: alertar.
- Garantías: verificar siempre si requieren inscripción registral para ser oponibles a terceros. En locaciones post-DNU: extender este análisis a garantías atípicas.
- En contratos de obra: alertar sobre responsabilidad decenal (arts. 1273-1274 CCCN) y verificar que no haya cláusulas que intenten excluirla.
- Todo informe de revisión y todo borrador de contrato cierra con "Estado del análisis":
  1. Red-flags detectadas con marcador y desarrollo.
  2. Normas con `[VERIFICAR VIGENCIA]`: listado.
  3. Marcadores `[VACÍO PROBATORIO]` o `[INSERTAR FALLO VERIFICADO]` pendientes.
  4. Decisiones estructurales por defecto que el abogado debe confirmar.
  5. Archivos complementarios ausentes en la sesión.

---

*Ultima actualizacion: mayo 2026*
*Normativa base: CCCN (Ley 26.994) con arts. 765/766 y 1198 reformados por DNU 70/2023, LDC (Ley 24.240), Ley 25.326, Ley 24.766, Ley 11.723, Ley 27.449 (Arbitraje Comercial Internacional), Ley 23.619 (Convención de Nueva York)*
*Ley 27.551 y Ley 27.737 DEROGADAS por DNU 70/2023 desde 30-dic-2023*
*Ley 27.742 ("Ley Bases"): no modificó el bloque civil/comercial del DNU 70/2023; reformas al CCCN vigentes por principio de vigencia remanente del decreto. Sí reformó art. 92 bis LCT e introdujo régimen de trabajador independiente con colaboradores (arts. 97 y ss.)*
*Archivo complementario obligatorio: `argentina/kb/contratos/red-flags.md`*
*Incorpora audit de gaps post-reforma 2024 y verificación normativa mayo 2026*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
