# Perfil de práctica · Derecho notarial · [PROVINCIA]

> Archivo de configuración para el sistema derecho-argentino.
> Complementa `kb/especialidades/notarial/notarial-CLAUDE.md` y `kb/especialidades/notarial/notarial-clausulas.md` con normativa específica del notariado de [PROVINCIA].
> Cargar junto con `kb/especialidades/notarial/notarial-CLAUDE.md` y `kb/especialidades/notarial/notarial-clausulas.md` en el Project. Este archivo no reemplaza al nacional - lo extiende con las particularidades del colegio, del registro y del fisco provincial.
> **Configuración inicial obligatoria:** completar las variables del Bloque 0 antes de usar.
>
> **Estado del perfil:** [COMPLETAR al entregar. Ej: "operativo - todos los campos completados y verificados contra texto legal" / "operativo con campos pendientes (ver etiquetas [PENDIENTE] en el texto)" / "borrador - requiere revisión antes de usar en caso concreto".]

---

## Sistema de etiquetas

- **[CONFIRMADO]** Dato extraído directamente del texto legal citado; sin reformas conocidas al corte de la fecha de actualización del perfil.
- **[A VERIFICAR]** Dato probable o histórico que debe confirmarse en el Boletín Oficial provincial o en el portal del colegio antes de aplicar al caso concreto.
- **[PENDIENTE]** Dato no disponible en este perfil; requiere investigación activa antes de operar.

Cuando una sección mezcle niveles, el etiquetado aparece en la regla específica, no en el título de la sección.

---

## Changelog

| Versión | Fecha | Cambios principales |
|---------|-------|---------------------|
| 1.0 | [COMPLETAR] | Versión inicial |

---

## Bloque 0 - Configuración inicial

**PROVINCIA:** [COMPLETAR: nombre de la provincia]

**COLEGIO_NOTARIAL:** [COMPLETAR: denominación exacta del colegio de escribanos provincial. Ej: "Colegio de Escribanos de la Provincia de Córdoba" / "Colegio de Escribanos de la Provincia de Santa Fe - 1° Circunscripción".]

**REGISTRO_PROPIEDAD:** [COMPLETAR: denominación exacta del registro de la propiedad inmueble provincial y organización territorial (circunscripciones, departamentos, partidos, etc.). Ej: "Registro General de la Provincia de Córdoba - organizado por secciones departamentales".]

**AREAS_PRACTICA_NOTARIAL:** [COMPLETAR: áreas de mayor volumen en la jurisdicción. Ej: "Compraventas inmobiliarias, donaciones, poderes, hipotecas".]

**SISTEMA_DIGITAL:** [COMPLETAR: plataforma digital del colegio para trámites y certificados. Ej: "GEDONO" / "sistema propio del colegio - denominación y URL".]

---

## Bloque 1 - Identidad y alcance

Este perfil cubre práctica notarial en la provincia de [PROVINCIA]: escrituras traslativas de dominio, donaciones, poderes, actas, sucesiones extrajudiciales, estructuras societarias, hipotecas y compliance UIF, bajo la ley orgánica notarial provincial y las disposiciones técnico-registrales del Colegio de Escribanos de [PROVINCIA] y del Registro de la Propiedad provincial.

**Articulación con el perfil nacional:** el régimen de fondo (CCCN, Ley 17.801, Res. UIF 242/2023, Ley 27.739) opera íntegramente - ver `kb/especialidades/notarial/notarial-CLAUDE.md`. Este perfil extiende ese régimen con las particularidades locales: ley orgánica, estructura registral, disposiciones técnico-registrales del colegio, plataforma digital, Impuesto de Sellos provincial y alertas específicas. No transpolar disposiciones técnico-registrales de otra jurisdicción sin advertencia.

**Regla de jurisdicción:** las disposiciones del Colegio de Escribanos de [PROVINCIA] y del Registro de la Propiedad de [PROVINCIA] aplican exclusivamente a actos autorizados en esta jurisdicción. Si el inmueble está en otra provincia, aplica el registro y las disposiciones técnico-registrales de esa provincia, no las de [PROVINCIA].

**Primer paso obligatorio en toda consulta:** identificar la ubicación del inmueble (o el lugar de otorgamiento del acto) antes de aplicar este perfil. Si el inmueble está en [PROVINCIA] pero el escribano actúa en otra jurisdicción: verificar competencia registral y disposiciones aplicables del registro receptor.

---

## Bloque 2 - Ley orgánica notarial

### 2.1 Norma principal

- **Ley orgánica:** [COMPLETAR: número, denominación oficial y año. Ej: "Ley 4183 (Ley Orgánica del Notariado, Córdoba)" / "Decreto-Ley 9020/78 (PBA)".]
- **Reglamento:** [COMPLETAR: decreto reglamentario si existe, con número y año. Si no hay reglamento específico, consignarlo.]
- **Texto vigente:** [COMPLETAR: indicar si hubo reformas recientes y dónde consultar el texto actualizado. URL del digesto o boletín oficial provincial.]
- **Articulado clave:** [COMPLETAR: artículos sobre habilitación, protocolo, forma de las escrituras, registros, responsabilidad notarial, sanciones disciplinarias. Ej: "arts. X-Y (protocolo y forma), arts. Z-W (registros), art. N (responsabilidad)".]

```
[VERIFICAR VIGENCIA: ley orgánica notarial [PROVINCIA] - verificar modificaciones posteriores a la fecha de este perfil en el digesto o boletín oficial provincial]
```

### 2.2 Protocolo y forma

- **Tipo de protocolo:** [COMPLETAR: ¿protocolo único por registro? ¿Foliación por año? ¿Libro de requerimientos separado? Precisar la práctica local.]
- **Certificación de firmas:** [COMPLETAR: ¿hay libro de certificaciones separado del protocolo? Alícuota arancelaria si corresponde.]
- **Actas notariales:** [COMPLETAR: ¿se asientan en el protocolo o en registro separado según la ley orgánica provincial?]
- **Conservación del protocolo:** [COMPLETAR: plazo de conservación obligatoria según la ley orgánica.]

### 2.3 Registros notariales

- **Estructura de registros:** [COMPLETAR: ¿los registros son individuales o pueden ser compartidos? ¿Hay categorías de registro (1°, 2°)? Precisar la denominación local.]
- **Habilitación:** [COMPLETAR: requisitos de habilitación de nuevo registro - concurso, antigüedad, examen, etc.]
- **Adscripción:** [COMPLETAR: ¿el colegio provincial prevé la figura del adscripto? Condiciones y plazo máximo.]
- **Sustitución y reemplazo:** [COMPLETAR: mecanismo de reemplazo por ausencia o incapacidad del titular.]

### 2.4 Arancel notarial

- **Norma arancelaria:** [COMPLETAR: ley o decreto que fija el arancel. Número y año.]
- **Base de cálculo:** [COMPLETAR: ¿sobre valor fiscal, valor de mercado, precio de escritura o el mayor de ellos?]
- **Alícuota general compraventa:** [COMPLETAR: porcentaje o escala aplicable al acto traslativo de dominio más frecuente.]
- **Alícuotas diferenciadas:** [COMPLETAR: hipotecas, donaciones, poderes, actas. Si hay escala progresiva, indicar tramos.]
- **Actualización:** [COMPLETAR: ¿el arancel se actualiza automáticamente o requiere resolución del colegio? Frecuencia habitual.]

```
[VERIFICAR VIGENCIA: arancel notarial [PROVINCIA] - verificar valores vigentes en el portal del colegio antes de presupuestar]
```

---

## Bloque 3 - Registro de la Propiedad Inmueble provincial

### 3.1 Organización territorial

- **Organismo:** [COMPLETAR: denominación exacta. Ej: "Registro General de la Provincia de Córdoba" / "Dirección Provincial del Registro de la Propiedad (Santa Fe)".]
- **Dependencia:** [COMPLETAR: ministerio u organismo del cual depende. Ej: "Ministerio de Justicia provincial" / "organismo autárquico".]
- **Organización territorial:** [COMPLETAR: ¿se organiza por circunscripciones, departamentos, partidos, secciones? Enumerar las principales circunscripciones o delegaciones si corresponde.]
- **Sistema de folio:** [COMPLETAR: ¿folio real, folio personal o mixto? Si es folio real: ¿por matrícula o por nomenclatura catastral?]

### 3.2 Plazos de vigencia de certificados registrales

Los plazos del art. 24 Ley 17.801 (15/25/30 días hábiles) son los mínimos nacionales. La provincia puede establecer plazos distintos o idénticos mediante disposiciones técnico-registrales propias.

- **Escribano de la misma circunscripción:** [COMPLETAR: días hábiles - fuente (disposición técnico-registral o ley)]
- **Escribano de otra circunscripción de la misma provincia:** [COMPLETAR: días hábiles - fuente]
- **Escribano de otra provincia:** [COMPLETAR: días hábiles - fuente]
- **Régimen especial (si existe):** [COMPLETAR: ¿hay plazos diferenciados por tipo de acto (hipoteca, donación, etc.)?]

```
[VERIFICAR VIGENCIA: plazos de vigencia de certificados registrales [PROVINCIA] - verificar en disposiciones técnico-registrales vigentes del registro provincial]
```

### 3.3 Trámites registrales

- **Inscripción de escrituras:** [COMPLETAR: plazo para presentar a inscripción desde la autorización. ¿Hay plazo de caducidad de la inscripción provisoria?]
- **Certificado de dominio:** [COMPLETAR: forma de solicitud (digital/presencial), plazo de entrega, costo.]
- **Certificado de inhibiciones:** [COMPLETAR: forma de solicitud, plazo de entrega. Alerta de homonimia si corresponde.]
- **Anotaciones personales:** [COMPLETAR: ¿se gestionan por el mismo registro o por organismo separado?]
- **Medidas cautelares:** [COMPLETAR: ¿las medidas se inscriben en el mismo registro o en el archivo de anotaciones personales? Plazo de vigencia de la traba.]
- **Tracto abreviado:** [COMPLETAR: ¿el registro provincial admite tracto abreviado conforme art. 16 Ley 17.801? ¿Hay disposición técnico-registral propia sobre los datos que debe contener la escritura?]

```
[VERIFICAR JURISDICCIÓN: tracto abreviado [PROVINCIA] - verificar requisitos específicos del registro provincial antes de estructurar el acápite "Corresponde"]
```

### 3.4 Observaciones registrales frecuentes

[COMPLETAR: listar las causales de observación más frecuentes en este registro según práctica local. Ej: falta de concordancia entre nomenclatura catastral del título y del certificado; superposición de matrículas en zonas urbanas con subdivisiones antiguas; etcétera. Si no hay información disponible, usar [PENDIENTE].]

```
[PENDIENTE: observaciones registrales frecuentes [PROVINCIA] - aportar práctica local del registro para completar esta sección]
```

---

## Bloque 4 - Colegio de Escribanos provincial

### 4.1 Datos institucionales

- **Denominación:** [COMPLETAR: nombre oficial del colegio.]
- **Portal web:** [COMPLETAR: URL del portal del colegio.]
- **Portal de trámites/plataforma digital:** [COMPLETAR: nombre y URL de la plataforma digital para certificados y trámites registrales. Ej: "GEDONO - gedono.com.ar" / sistema propio con URL.]
- **Correo/Mesa de entradas:** [COMPLETAR: si corresponde.]

### 4.2 Plataforma digital

- **Sistema:** [COMPLETAR: ¿GEDONO u otro sistema propio? Indicar nombre comercial y URL.]
- **Trámites disponibles en línea:** [COMPLETAR: certificados de dominio, inhibiciones, anotaciones personales, informes de dominio. Indicar cuáles están digitalizados y cuáles requieren trámite presencial.]
- **Acceso:** [COMPLETAR: ¿requiere token o firma digital del escribano? ¿Qué certificado digital utiliza?]
- **Alertas operativas:** [COMPLETAR: caídas del sistema frecuentes, horarios de atención, contingencias conocidas. Si no hay datos: [PENDIENTE].]

```
[PENDIENTE: alertas operativas plataforma digital [PROVINCIA] - verificar en el portal del colegio o circular interna antes de operar]
```

### 4.3 Disposiciones técnico-registrales

[COMPLETAR: disposiciones del colegio que regulan la forma de los instrumentos, los requisitos de las escrituras y certificados, y las instrucciones al registro. Listar las disposiciones vigentes más relevantes con número, año y materia. Si no se dispone de la lista completa: [PENDIENTE].]

```
[PENDIENTE: disposiciones técnico-registrales vigentes [PROVINCIA] - verificar en el portal del colegio la lista actualizada de disposiciones antes de operar]
```

### 4.4 Circulares e instrucciones vigentes

[COMPLETAR: circulares o instrucciones del colegio con impacto operativo inmediato (formularios, requisitos de identificación, cambios de procedimiento). Si no se dispone de información actualizada: [PENDIENTE].]

```
[PENDIENTE: circulares vigentes Colegio de Escribanos [PROVINCIA] - verificar en el portal del colegio]
```

---

## Bloque 5 - Impuesto de Sellos provincial

### 5.1 Norma aplicable

- **Ley:** [COMPLETAR: número y año del Código Fiscal provincial o ley de Sellos. Ej: "Código Tributario Provincial Ley N° [X], Título [Y]" / "Ley de Sellos N° [X]".]
- **Ley impositiva anual:** [COMPLETAR: número y año de la ley impositiva vigente al cierre de este perfil que fija las alícuotas del ejercicio.]
- **Texto vigente:** [COMPLETAR: URL del código fiscal provincial o digesto tributario oficial.]

```
[VERIFICAR VIGENCIA: Impuesto de Sellos [PROVINCIA] - alícuotas y exenciones según ley impositiva del año en curso - verificar antes de cada operación]
```

### 5.2 Base imponible

- **Regla general:** [COMPLETAR: ¿la base es el valor de escritura, el valor fiscal (valuación fiscal), el valor de mercado, o el mayor de los tres? Indicar artículo del código fiscal.]
- **Inmuebles:** [COMPLETAR: base imponible específica para transmisiones de dominio. ¿Se aplica sobre el precio de la operación o sobre la valuación fiscal si es mayor?]
- **Hipotecas:** [COMPLETAR: ¿la base es el monto del crédito garantizado? ¿Incluye intereses y accesorios?]
- **Poderes y actas:** [COMPLETAR: ¿están gravados? Base y alícuota si corresponde.]

### 5.3 Alícuotas

| Acto | Alícuota | Norma |
|------|----------|-------|
| Compraventa inmobiliaria | [COMPLETAR] % | [COMPLETAR art.] |
| Donación | [COMPLETAR] % | [COMPLETAR art.] |
| Hipoteca | [COMPLETAR] % | [COMPLETAR art.] |
| Cesión de derechos hereditarios | [COMPLETAR] % | [COMPLETAR art.] |
| Constitución de sociedad / aporte inmobiliario | [COMPLETAR] % | [COMPLETAR art.] |
| Otros actos frecuentes | [COMPLETAR] % | [COMPLETAR art.] |

```
[VERIFICAR VIGENCIA: tabla de alícuotas [PROVINCIA] - verificar ley impositiva del año en curso]
```

### 5.4 Exenciones

[COMPLETAR: listar las exenciones más relevantes para la práctica notarial corriente. Ej: vivienda única y de ocupación permanente (si existe), donaciones entre ascendientes y descendientes, operaciones del Estado provincial, escrituras de primera vivienda social, etc. Indicar artículo del código fiscal o ley especial para cada exención.]

> **Regla operativa:** no omitir la liquidación del Impuesto de Sellos basándose en una exención sin verificar previamente si esa exención requiere certificado o trámite ante la DGR/ARBA provincial. Algunas exenciones son automáticas (se declaran en la escritura); otras requieren constancia previa del organismo recaudador. La omisión sin acreditación puede generar intimación de pago con intereses y multas.

```
[VERIFICAR VIGENCIA: exenciones Impuesto de Sellos [PROVINCIA] - verificar condiciones y acreditación ante el registro antes de omitir la liquidación]
```

### 5.5 Sujeto obligado y forma de pago

- **Sujeto pasivo:** [COMPLETAR: ¿el vendedor, el comprador, ambos solidariamente, o depende del acto? Indicar artículo.]
- **Forma de pago:** [COMPLETAR: ¿se paga ante el registro al inscribir, ante la DGR/ARBA provincial por boleta, o se retiene en la escritura?]
- **Retención en la escritura:** [COMPLETAR: ¿el escribano actúa como agente de retención? Si sí, indicar el mecanismo y la norma.]

```
[VERIFICAR JURISDICCIÓN: mecanismo de pago Impuesto de Sellos [PROVINCIA] - verificar si el escribano actúa como agente de retención y el procedimiento vigente]
```

---

## Bloque 6 - Fuero de litigios derivados

### 6.1 Competencia judicial

- **Fuero:** [COMPLETAR: denominación exacta del fuero competente para litigios derivados de actos notariales en [PROVINCIA]. Ej: "Juzgados Civiles y Comerciales" / "Juzgados de Primera Instancia en lo Civil" / "Cámara Civil - organización por departamentos judiciales".]
- **Organización territorial:** [COMPLETAR: ¿se organiza por departamentos judiciales, circunscripciones, ciudades? ¿Cuáles son los principales centros judiciales?]
- **Código de procedimiento:** [COMPLETAR: número y año del código procesal civil provincial aplicable. Si el código es el CPCCN por adhesión o supletoriedad, consignarlo expresamente.]

### 6.2 Tipos de litigios frecuentes y su encuadre procesal

- **Nulidad de escritura pública:** [COMPLETAR: ¿proceso ordinario o sumario? ¿Plazo de prescripción aplicable?]
- **Responsabilidad civil del escribano:** [COMPLETAR: ¿fuero civil ordinario? ¿Plazo de prescripción - art. 2561 CCCN (3 años) o plazo provincial si es más extenso?]
- **Impugnación de actos registrales:** [COMPLETAR: ¿se plantea por vía contencioso-administrativa o civil? ¿Hay fuero especializado?]
- **Acción de reducción por donación inoficiosa:** [COMPLETAR: ¿fuero civil? ¿Proceso ordinario?]
- **Medidas cautelares sobre inmuebles:** [COMPLETAR: ¿se tramitan ante el juez del domicilio del demandado, del lugar del inmueble o del juez competente en la causa principal?]

### 6.3 Prescripción de acciones notariales

- **Responsabilidad civil del escribano:** [COMPLETAR: plazo. Base: art. 2561 CCCN (3 años) salvo ley provincial más favorable al damnificado.]
- **Nulidad de escritura por vicio de forma:** [COMPLETAR: plazo. Base: art. 2562 CCCN inc. b (2 años) - verificar si la provincia tiene régimen propio.]
- **Acciones reales sobre inmuebles:** [COMPLETAR: art. 2560 CCCN (5 años) - verificar si aplica el plazo general o uno específico según la acción.]

```
[VERIFICAR VIGENCIA: plazos de prescripción [PROVINCIA] - verificar si la provincia tiene ley propia sobre prescripción de acciones notariales o si aplica íntegramente el CCCN]
```

---

## Bloque 7 - Alertas específicas de la jurisdicción

### 7.1 Alertas normativas

[COMPLETAR: listar las alertas más importantes derivadas de la normativa provincial específica. Incluir:
- Reformas recientes a la ley orgánica notarial o al código fiscal que cambien la práctica habitual
- Disposiciones técnico-registrales con impacto operativo inmediato
- Cambios en la plataforma digital del colegio
- Resoluciones del colegio de escribanos con vigencia reciente
Si no hay alertas activas: consignar "Sin alertas normativas activas al corte de este perfil".]

```
[PENDIENTE: alertas normativas específicas [PROVINCIA] - verificar en el portal del colegio y boletín oficial provincial]
```

### 7.2 Particularidades registrales locales

[COMPLETAR: listar particularidades del Registro de la Propiedad de [PROVINCIA] que no se infieren del régimen nacional. Ej:
- Zonas con superposición de matrículas históricas
- Departamentos con catastro desactualizado
- Inmuebles rurales sin mensura aprobada
- Subdivisiones en trámite frecuentes en zonas específicas
Si no hay particularidades conocidas: [PENDIENTE].]

```
[PENDIENTE: particularidades registrales [PROVINCIA] - aportar práctica local del registro para completar esta sección]
```

### 7.3 Particularidades fiscales locales

[COMPLETAR: listar situaciones fiscales que generan errores frecuentes o riesgo de observación. Ej:
- Liquidación de Sellos en operaciones con precio en moneda extranjera (tipo de cambio aplicable)
- Tratamiento de operaciones a plazo o con retención de precio
- Inmuebles con valuaciones fiscales muy por debajo del mercado y riesgo de ajuste
- Exenciones que requieren certificado previo de la autoridad fiscal provincial
Si no hay particularidades conocidas: [PENDIENTE].]

```
[PENDIENTE: particularidades fiscales locales [PROVINCIA] - aportar práctica local para completar esta sección]
```

### 7.4 Alerta de vigencia permanente

```
[ALERTA PERMANENTE: verificar antes de cada operación en [PROVINCIA]:
1. Alícuota Impuesto de Sellos vigente (ley impositiva del ejercicio en curso)
2. Plazos de vigencia de certificados registrales (disposiciones técnico-registrales vigentes)
3. Disposiciones y circulares del Colegio de Escribanos de [PROVINCIA] (portal del colegio)
4. Estado operativo de la plataforma digital ([nombre del sistema])
5. Umbrales UIF vigentes (uif.gob.ar - Res. UIF 242/2023 y modificatorias)]
```

---

## Bloque 8 - Fuentes primarias

Acceder directamente y pegar el texto en la sesión cuando el dato es crítico o el conector MCP no responde.

| Necesidad | Fuente |
|---|---|
| Texto oficial ley orgánica notarial | [COMPLETAR: URL del digesto provincial o boletín oficial] |
| Boletín Oficial provincial | [COMPLETAR: URL] |
| Código Fiscal / ley de Sellos | [COMPLETAR: URL digesto tributario provincial] |
| Registro de la Propiedad provincial | [COMPLETAR: URL del portal del registro] |
| Colegio de Escribanos (circulares y disposiciones) | [COMPLETAR: URL del portal del colegio] |
| Plataforma digital certificados | [COMPLETAR: URL de GEDONO u otro sistema] |
| Catastro provincial | [COMPLETAR: URL] |
| ARBA / DGR provincial (Sellos) | [COMPLETAR: URL del organismo recaudador provincial] |
| Jurisprudencia civil provincial | [COMPLETAR: URL del portal del Poder Judicial provincial] |

---

## Bloque 9 - Reglas de citación específicas

Las reglas generales de `kb/especialidades/notarial/notarial-CLAUDE.md` aplican íntegramente. Específicas para [PROVINCIA]:

**Disposiciones técnico-registrales del Colegio de Escribanos de [PROVINCIA]:** nunca citar número de disposición sin material aportado. Usar:
```
[INSERTAR DISPOSICIÓN VERIFICADA: Colegio de Escribanos [PROVINCIA] - materia - número y fecha]
```

**Disposiciones del Registro de la Propiedad de [PROVINCIA]:** nunca citar resolución o instrucción del registro sin material aportado. Usar:
```
[INSERTAR INSTRUCCIÓN VERIFICADA: Registro de la Propiedad [PROVINCIA] - materia - número y fecha]
```

**Alícuotas de Sellos:** nunca consignar alícuota sin verificar la ley impositiva del año en curso. Usar:
```
[VERIFICAR VIGENCIA: alícuota Impuesto de Sellos [PROVINCIA] - verificar ley impositiva [año] antes de liquidar]
```

**Jurisprudencia registral o notarial provincial:** nunca citar fallo o dictamen del colegio sin material aportado. Usar:
```
[INSERTAR FALLO/DICTAMEN VERIFICADO: fuente [PROVINCIA] - doctrina requerida]
```

---

## Bloque 10 - Instrucciones operativas

- Identificar la ubicación del inmueble y el domicilio del colegio actuante antes de aplicar este perfil.
- Verificar siempre la alícuota de Sellos vigente contra la ley impositiva del ejercicio en curso. No usar valores del perfil sin confirmar.
- Calcular los plazos de vigencia de los certificados registrales según las disposiciones técnico-registrales del Registro de [PROVINCIA], no los plazos genéricos del art. 24 Ley 17.801.
- No asumir que las disposiciones técnico-registrales del Colegio de Escribanos de [PROVINCIA] coinciden con las de CABA o PBA. Verificar la norma local.
- No completar datos registrales (matrícula, folio, nomenclatura catastral, partida inmobiliaria) sin el certificado aportado.
- En tracto abreviado: verificar los requisitos específicos del Registro de [PROVINCIA] antes de estructurar el acápite "Corresponde". Incluir siempre la referencia registral completa del auto de inscripción (tomo, folio y, si corresponde, matrícula o partida) para evitar observaciones del registro local.
- En cedular inmobiliario: aplicar íntegramente las instrucciones del perfil nacional (`kb/especialidades/notarial/notarial-CLAUDE.md`). El escribano no retiene el cedular bajo ninguna circunstancia; no introducir reglas provinciales que contradigan esa regla. Ante la opción de reemplazo, no escriturar sin el certificado de no retención ARCA previo.
- Todo escrito o escritura cierra con "Estado del escrito" estándar más los campos específicos de este perfil:
  - Certificados registrales: tipo solicitado, fecha de solicitud y fecha de vencimiento
  - Impuesto de Sellos: alícuota aplicada y norma verificada (ley impositiva [año])
  - Normas con `[VERIFICAR VIGENCIA]` o `[PENDIENTE]` pendientes de resolución
  - Control UIF: nivel de riesgo asignado y documentación pendiente (Res. UIF 242/2023)
  - Datos registrales faltantes para completar la escritura
  - Estado de la plataforma digital: si los certificados fueron gestionados en línea o hay contingencia activa

---

*Última actualización: [COMPLETAR: fecha]*
*Normativa base: [COMPLETAR: ley orgánica notarial provincial, código fiscal provincial, disposiciones técnico-registrales vigentes incorporadas al completar el template]*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
