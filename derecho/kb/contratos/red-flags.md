# Red flags para revisión de contratos · Derecho argentino

Lista de alertas prioritarias para análisis automatizado de contratos bajo derecho argentino continental. Ordenadas por nivel de riesgo.

---

## Nulidad absoluta

Estas situaciones invalidan la cláusula de pleno derecho. Marcar siempre, sin excepción.

### 1. Renuncia anticipada a derechos irrenunciables

**Normas:** Art. 12 LCT (laboral) / Art. 37 LDC (consumo) / Arts. 944-954 CCCN (general)

Cualquier cláusula que intente hacer renunciar al trabajador o al consumidor a derechos de orden público es nula. El contrato subsiste sin la cláusula.

Formas habituales:
- "El trabajador renuncia a cualquier diferencia salarial futura"
- "El consumidor acepta renunciar a cualquier acción por daños derivados del servicio"
- "Las partes acuerdan que el presente contrato satisface íntegramente cualquier crédito laboral"

### 2. Prórroga de jurisdicción al extranjero en contratos de consumo

**Norma:** Art. 2654 CCCN - prohibición expresa

Contexto habitual: contratos de plataformas digitales, servicios SaaS, e-commerce internacional, términos y condiciones de servicios con sede en EE.UU. o Europa.

Forma habitual: "Any dispute arising from this agreement shall be submitted to the exclusive jurisdiction of the courts of [estado extranjero]"

### 3. Limitación de responsabilidad por dolo o culpa grave

**Norma:** Art. 1743 CCCN - nulidad sin excepción

Cualquier cláusula que limite o excluya la responsabilidad del predisponente por su propio dolo o culpa grave es inválida, independientemente de la forma en que esté redactada.

Formas habituales:
- "En ningún caso la parte X será responsable por daños directos o indirectos..."
- "La responsabilidad total de X no excederá el monto pagado por el servicio..."
- "X no será responsable por fallas en la prestación causadas por cualquier motivo..."

### 4. Cláusulas abusivas en contratos de adhesión

**Normas:** Arts. 985-989 CCCN / Arts. 37-38 LDC

Contrastar cada cláusula limitativa o excluyente contra el estándar de desequilibrio significativo entre derechos y obligaciones. La lista del art. 37 LDC es enunciativa, no taxativa.

Tipos más frecuentes:
- Modificación unilateral de precio o condiciones sin causa objetiva
- Exclusión o limitación de responsabilidad por vicios o defectos
- Inversión de la carga probatoria en perjuicio del consumidor
- Renuncia anticipada a derechos procesales (fuero, recurso)

---

## Riesgo alto

Marcar y desarrollar en el informe. Requieren análisis específico o propuesta de redacción alternativa.

### 5. Ausencia de mecanismo de actualización en contratos de largo plazo

**Contexto:** En Argentina, un contrato de tracto sucesivo (locación de servicios, suministro, mantenimiento, licencia de uso) sin cláusula de actualización es un pasivo potencial para la parte acreedora de dinero.

Verificar si el plazo supera seis meses. Si supera: alertar y proponer alguna de estas opciones:
- Cláusula de ajuste por índice (ICL, IPC, RIPTE según el tipo de contrato)
- Precio en moneda extranjera con indicación de tipo de cambio aplicable
- Revisión periódica pactada con mecanismo de negociación

### 6. Pacto comisorio sin notificación previa

**Normas:** Arts. 1083-1089 CCCN

Verificar que el mecanismo de resolución contractual sea compatible con el régimen legal: intimación previa con plazo razonable (art. 1088 CCCN) o resolución de pleno derecho cuando el incumplimiento hace imposible la finalidad del contrato (art. 1089 CCCN).

Formas problemáticas:
- "El incumplimiento de cualquier obligación dará derecho a resolver el contrato de pleno derecho y de manera inmediata"
- Ausencia total de cláusula resolutoria cuando el contrato es de larga duración

### 7. Confidencialidad sin plazo determinado

**Riesgo:** Nulidad parcial por indeterminación del objeto o plazo irrazonable según fuero y circunstancias.

Verificar: si la obligación de confidencialidad no tiene plazo o tiene un plazo irrazonablemente extenso (más de 5 años para información no constitutiva de secreto comercial), alertar.

Proponer: plazo máximo razonable según el tipo de información protegida, con indicación de las excepciones estándar (información pública, obtenida de tercero, requerida judicialmente).

### 8. Arbitraje con sede en el extranjero

Verificar antes de dar el visto bueno:
- Ley aplicable al fondo del asunto
- Validez del acuerdo arbitral bajo Ley 27.449 (Arbitraje Comercial Internacional, basada en Ley Modelo CNUDMI): requisitos de forma escrita, arbitrabilidad del objeto, capacidad de las partes
- Ejecutabilidad del laudo en Argentina: Convención de Nueva York (Ley 23.619) para reconocimiento y ejecución de laudos extranjeros
- Compatibilidad con orden público argentino
- En contratos de consumo: la prórroga a arbitraje extranjero puede ser inválida (ver red flag 2)

Marcar como pendiente de análisis específico si el contrato no aporta suficiente información sobre el tipo de arbitraje (ad hoc o institucional) y las reglas aplicables.

### 9. Relación laboral encubierta en contratos de servicios civiles o comerciales

**Normas:** Arts. 22, 23 y 26 LCT / Art. 12 LCT / Arts. 97 y ss. Ley 27.742

La presunción del art. 23 LCT sigue vigente: opera ante cualquier prestación de servicios con independencia de la denominación contractual. La Ley 27.742 no modificó el texto del art. 23 ni introdujo una exclusión por emisión de facturas. Lo que creó es el régimen de **trabajador independiente con colaboradores** (arts. 97 y ss. Ley 27.742): una figura alternativa que compite con la relación de dependencia cuando el prestador encuadra en sus requisitos específicos (hasta 3 colaboradores, inscripción en el registro correspondiente, actividad autónoma real, sin subordinación).

**Flujo de análisis:**

1. Verificar si el prestador podría encuadrar en el régimen de trabajador independiente con colaboradores (Ley 27.742). Si encuadra y cumple los requisitos formales: la presunción del art. 23 no opera de forma automática; continuar el análisis civil con nota de precaución.
2. Si no encuadra en ese régimen, o si hay señales de subordinación real: aplicar presunción del art. 23 y emitir el marcador.

**Señales de alerta que activan la presunción independientemente del régimen invocado:**
- Exclusividad: el prestador no puede trabajar para otros clientes o debe pedir autorización
- Horario: el contrato fija horarios de inicio, fin o disponibilidad
- Subordinación directa: el prestador recibe instrucciones operativas del contratante
- Elementos del comitente: el prestador usa equipos, sistemas o lugar de trabajo del contratante

Si se verifica una o más señales: emitir el siguiente marcador y no continuar el análisis como contrato civil sin intervención del abogado:

```
[VACÍO PROBATORIO: existencia probable de relación de dependencia encubierta -
 verificar con el abogado antes de continuar el análisis bajo régimen civil.
 Evaluar si aplica régimen de trabajador independiente (arts. 97 y ss. Ley 27.742).
 Activar perfil laboral (laboral/CLAUDE.md) si se confirma la relación]
```

---

## Riesgo medio

Consignar en el informe. No bloquean el avance pero requieren atención del abogado.

### 10. Ausencia de domicilio especial constituido en Argentina

Relevancia para: notificaciones fehacientes, notificaciones procesales, eventual ejecución judicial.

En contratos con personas jurídicas extranjeras: verificar si tienen sucursal inscripta en Argentina (art. 118 LGS) y si el domicilio contractual coincide con el registral.

### 11. Moneda de pago en divisas - verificación de régimen aplicable

Verificar dos aspectos antes de dar el visto bueno:

**a) Régimen cambiario vigente**
Las restricciones al giro de divisas varían con frecuencia por normativa del BCRA.
```
[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE: normativa BCRA - verificar antes de firmar]
```

**b) Régimen aplicable a la obligación según fecha del contrato**
- Obligaciones nacidas post-30-dic-2023 (DNU 70/2023): el deudor NO puede liberarse pagando en moneda distinta a la pactada, salvo aceptación del acreedor (arts. 765-766 CCCN reformados).
- Obligaciones nacidas pre-30-dic-2023: régimen original del art. 765 CCCN; el deudor podía cancelar en moneda nacional al tipo de cambio oficial del día del pago.
```
[VERIFICAR RÉGIMEN APLICABLE: obligación en moneda extranjera - fecha de origen determina
 si aplica art. 765 CCCN original o reformado por DNU 70/2023]
```

Si el contrato no incluye cláusula de opción de pago en pesos para obligaciones pre-30-dic-2023 todavía vigentes: alertar sobre el cambio de régimen y la necesidad de adecuación.

### 12. Garantías sin inscripción registral cuando corresponde

- Prenda con registro (Decreto-Ley 15.348/46): verificar inscripción y vigencia
- Hipoteca (arts. 2205-2211 CCCN): verificar inscripción registral y rango
- Anticresis (arts. 2212-2218 CCCN): verificar instrumentación y entrega de la cosa
- Garantías sobre acciones o cuotas sociales: verificar régimen aplicable según tipo societario
- Garantías atípicas en locaciones post-DNU 70/2023: el régimen libre habilita garantías no previstas expresamente por la ley; verificar en cada caso si la garantía pactada requiere inscripción para ser oponible a terceros.

### 13. Plazo de prescripción no contemplado

Verificar que el contrato no intente modificar los plazos de prescripción legales (arts. 2532-2564 CCCN). Las partes pueden acortar o ampliar plazos dentro de los límites legales (art. 2533 CCCN), pero no pueden eliminarlos ni fijar plazos irrazonables.

---

## Contratos laborales - régimen diferenciado

Las cláusulas que siguen se analizan bajo el régimen laboral, no bajo el CCCN. La norma de base es el art. 12 LCT: son nulas las convenciones de partes que supriman o reduzcan los derechos reconocidos al trabajador por la LCT, los estatutos, los CCT o los contratos individuales. La nulidad es parcial: la cláusula inválida se sustituye por la norma que hubiera correspondido; el contrato subsiste.

### Nulidad absoluta en el contrato de trabajo

#### L1. Cláusula de no competencia post-empleo sin contraprestación

**Normas:** Art. 12 LCT / Arts. 953 y 1004 CCCN (objeto ilícito) / Art. 14 bis CN

Las cláusulas de no competencia post-empleo son admisibles con tres requisitos copulativos:
- Limitación temporal razonable (criterio judicial: no más de 1 a 2 años según el caso y el fuero)
- Limitación territorial o de actividad específica y acotada
- Contraprestación económica adecuada al sacrificio impuesto al trabajador

Formas inválidas:
- "El trabajador se obliga a no trabajar en la industria X por el plazo de 5 años sin compensación alguna"
- "La sola percepción de la indemnización por despido compensa la obligación de no competencia"
- Cláusula sin plazo determinado o con plazo indeterminado

Consecuencia: el fuero nacional del trabajo tiende a declarar la nulidad de la cláusula sin compensación o con plazo irrazonable. La nulidad impide al empleador reclamar daños por su violación.

#### L2. Renuncia anticipada a créditos laborales

**Normas:** Arts. 12, 15, 58, 260 y 277 LCT

El trabajador no puede renunciar anticipadamente a ningún crédito derivado de la LCT, un CCT o su contrato. La renuncia a créditos es válida únicamente respecto de créditos ciertos y exigibles al momento de la renuncia, con homologación judicial o ante autoridad administrativa laboral competente (SECLO, Ministerio de Trabajo).

Formas inválidas:
- "El trabajador declara no tener nada más que reclamar por ningún concepto presente o futuro"
- "La firma del presente contrato implica la renuncia a cualquier diferencia salarial anterior"
- Recibos finales con leyenda "nada más a reclamar" no homologados, respecto de diferencias salariales no pagadas

#### L3. Confidencialidad que abarca información sindical o de condiciones de trabajo

**Normas:** Arts. 4, 14 y 62 LCT / Ley 23.551

Una cláusula de confidencialidad que cubra información sobre remuneraciones, condiciones de trabajo o actividad gremial del trabajador es nula en esa extensión. Choca con el derecho a la información sindical y con los principios de la relación laboral.

Formas problemáticas:
- "El trabajador se obliga a no revelar a ningún tercero, incluyendo compañeros de trabajo, su remuneración u otros beneficios"
- Cláusulas de confidencialidad que incluyan como "información confidencial" toda referencia a condiciones laborales

### Riesgo alto en contratos laborales

#### L4. Cláusula de no competencia con contraprestación insuficiente

**Normas:** Arts. 12 y 62 LCT / [INSERTAR FALLO VERIFICADO: doctrina CNAT sobre no competencia y contraprestación]

Si la contraprestación existe pero es simbólica o no guarda relación con el valor de la restricción y el salario del trabajador, el riesgo de nulidad es alto. Proponer revisión del monto y del plazo.

#### L5. Clasificación del trabajador como "socio" o "contratista independiente" para eludir la relación laboral

**Normas:** Arts. 22, 23 y 26 LCT

La presunción del art. 23 LCT opera ante cualquier prestación de servicios, con independencia de la forma elegida. Las cláusulas que caracterizan al trabajador como socio o contratista autónomo no desvirtúan la relación laboral si en los hechos existe subordinación.

Marcar cuando el contrato:
- Constituye una sociedad entre "socio capitalista" (empleador) y "socio industrial" (trabajador) con aporte de trabajo como única contribución del segundo
- Contrata como "freelancer" o "monotributista" a quien presta servicios exclusivos, con horario y bajo supervisión del contratante
- Aplica retención de honorarios en lugar de remuneración sin justificación real en la autonomía del prestador

#### L6. Cláusula penal por renuncia anticipada del trabajador

**Normas:** Arts. 12, 62 y 240 LCT [VERIFICAR VIGENCIA post-Ley 27.742]

El trabajador tiene derecho a renunciar con preaviso o con pago de la indemnización sustitutiva. Una cláusula penal que le imponga el pago de una suma en caso de renuncia antes de un plazo determinado no tiene respaldo legal y es de validez dudosa o nula según el fuero.

#### L7. Prórroga de jurisdicción al extranjero

**Normas:** Art. 12 LCT / Art. 2654 CCCN / Principio de territorialidad laboral

En el contrato de trabajo ejecutado en Argentina, la prórroga de jurisdicción a tribunales extranjeros para resolver conflictos derivados de la relación laboral es inválida. El fuero del trabajo tiene competencia imperativa.

### Riesgo medio en contratos laborales

#### L8. Ausencia de cláusula de actualización salarial en contratos de plazo determinado

En contratos de plazo determinado que superan los 6 meses, la falta de mecanismo de actualización perjudica al trabajador en contexto inflacionario. El empleador también asume riesgo si el CCT aplicable fija incrementos obligatorios no contemplados en el contrato.

Proponer: referencia expresa al CCT aplicable y a los acuerdos salariales que resulten de la negociación colectiva de la actividad.

#### L9. Jornada y modalidad no documentadas

Si el contrato no especifica jornada, modalidad (presencial, híbrida, remota) o lugar de trabajo, puede generar conflictos sobre horas extras (art. 201 LCT), régimen de teletrabajo (Ley 27.555) si el trabajo remoto no está pactado por escrito, y disponibilidad fuera del horario laboral.

#### L10. Período de prueba mal configurado

**Norma:** Art. 92 bis LCT reformado por Ley 27.742

Plazos vigentes desde la reforma:
- Empresas de más de 10 trabajadores: **6 meses**
- Empresas de 6 a 10 trabajadores: **8 meses**
- Empresas de hasta 5 trabajadores (PyMES): **12 meses**

Solo puede aplicarse una vez entre el mismo empleador y el mismo trabajador. Si el contrato fija un período superior al que corresponde según el tamaño de la empresa, el exceso es inválido y el trabajador adquiere estabilidad desde el inicio de la relación. Verificar el tamaño del empleador antes de evaluar si el período pactado es válido.

---

*Nota de uso de este módulo: se aplica a contratos individuales de trabajo, acuerdos de confidencialidad en el empleo y pactos de no competencia. Para CCT, conflictos colectivos o análisis de despidos, ver laboral/CLAUDE.md.*

---

## Notas de uso

Esta lista es un punto de partida para el análisis automatizado, no un checklist exhaustivo. No reemplaza la revisión del abogado sobre el contrato específico, el contexto de la negociación y la relación entre las partes.

Los red flags marcan situaciones que requieren atención. La evaluación final sobre si una cláusula es o no válida, y sobre qué hacer al respecto, es siempre responsabilidad del abogado.

---

*Última actualización: mayo 2026*
*Normativa base: CCCN (Ley 26.994) con arts. 765/766 y 1198 reformados por DNU 70/2023, LDC (Ley 24.240), LCT (Ley 20.744) con art. 92 bis reformado por Ley 27.742, Ley 25.326, Ley 27.449 (Arbitraje Comercial Internacional), Ley 23.619 (Convención de Nueva York)*
*Ley 27.742 ("Ley Bases"): no modificó el bloque civil/comercial del DNU 70/2023. Sí reformó art. 92 bis LCT e introdujo régimen de trabajador independiente con colaboradores (arts. 97 y ss.)*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
