# Perfil de práctica · Derecho administrativo · Provincia del Chaco

> Archivo de configuración para el sistema derecho-argentino.
> Complementa el perfil general (argentina/kb/project/CLAUDE.md) y el perfil administrativo nacional (kb/perfiles/administrativo-CLAUDE.md) con lógica específica del fuero contencioso administrativo del Chaco.
> Cargar junto con kb/perfiles/administrativo-CLAUDE.md en el Project. Este archivo no reemplaza al nacional - lo extiende.
>
> **Estado del perfil:** operativo. Actualización v1.1 (mayo 2026): resueltos los bloques de procedimiento administrativo (Ley 179-A), control judicial (Ley 135-A), empleo público (estatutos sectoriales), contrataciones (Ley 1092-A + Decreto 3566/77 + Ley 1121-A), responsabilidad del Estado (Art. 76 CP), cautelares (Ley 2559-M), Defensor del Pueblo (Ley 1172-B), Fiscalía de Estado, Tribunal de Cuentas (Ley 931-A) y recurso extraordinario provincial (Ley 1-B). Subsisten pendientes menores indicados en el texto.

---

## Sistema de etiquetas

- **[CONFIRMADO]** Dato extraído directamente del texto legal citado; sin reformas conocidas al corte de la fecha de actualización del perfil.
- **[A VERIFICAR]** Dato probable o historico que debe confirmarse en el Boletin Oficial provincial o en el portal del Poder Judicial antes de aplicar al caso concreto.
- **[PENDIENTE]** Dato no disponible en este perfil; requiere investigacion activa antes de operar.

---

## Changelog

| Version | Fecha | Cambios principales |
|---------|-------|---------------------|
| 1.1 | mayo 2026 | Resolucion de pendientes: plazos y articulos Ley 179-A (Arts. 82, 89, 95, 68, 36-42, 43-48); pretensiones CCA con articulos exactos (Art. 2 incs. a-c y Art. 5); declaracion de oficio de caducidad por STJ confirmada; sedes y composicion Camara CA completadas; recurso extraordinario provincial (Ley 1-B Arts. 12, 15, 18, plazo 10 dias habiles); empleo publico (estatuto Ley 2017-A, escalafon Ley 1276-A, estatutos sectoriales completos, negociacion colectiva Ley 2361-A); contrataciones (Ley 1092-A + Decreto 3566/77); obra publica (Ley 1121-A); redeterminacion de precios (Decreto 1121/04); responsabilidad del Estado (Art. 76 CP, regimen objetivo directo); cautelares (informe previo no obligatorio, contracautela juratoria descartada en afectacion fiscal); Defensor del Pueblo (Ley 1172-B, legitimacion en fuero CA); Fiscalia de Estado (parte obligatoria, sin dictamenes en linea); Tribunal de Cuentas (Ley 931-A, competencia sobre municipios); fuentes primarias actualizadas |
| 1.0 | mayo 2026 | Version inicial - completado con documento de referencia sobre regimen chaqueno |

---

## Bloque 0 - Configuracion inicial

**PROVINCIA:** Chaco

**FUERO_HABITUAL:** Camara en lo Contencioso Administrativo - Resistencia. Para actos de los maximos poderes publicos provinciales: Superior Tribunal de Justicia (competencia originaria).

**AREAS_PRACTICA:** Empleo publico provincial, impugnacion de actos administrativos, responsabilidad patrimonial del Estado provincial, contratacion publica provincial, amparo administrativo.

**ORGANISMO_CONTRALOR_HABITUAL:** Tribunal de Cuentas provincial, Fiscalia de Estado, organismos del Poder Ejecutivo provincial.

---

## Bloque 1 - Identidad y alcance

Este perfil cubre practica de derecho administrativo en la provincia del Chaco: procedimiento administrativo ante organismos provinciales y municipales, recursos administrativos en sede provincial, control judicial contencioso administrativo provincial, responsabilidad del Estado provincial, empleo publico provincial y contratacion publica provincial.

**Articulacion con el perfil nacional:** cuando actua un organismo federal con sede en Chaco (ARCA/ex AFIP, ANSES, organismos desconcentrados nacionales), aplica el regimen federal (LNPA + RLNPA) - ver kb/perfiles/administrativo-CLAUDE.md. Cuando actua la Administracion provincial o municipal, aplica este perfil. No transpolar plazos ni institutos entre ambos regimenes sin advertencia.

**Actos mixtos:** cuando en un mismo caso coexisten actos de organismos provinciales y federales, cada regimen se aplica al acto correspondiente por separado. Los plazos del regimen federal no se extienden al acto provincial, ni viceversa.

**Tercer nivel - organismos municipales:** [PENDIENTE: verificar si el fuero contencioso administrativo provincial tiene competencia sobre actos municipales del Chaco o si existe fuero o competencia civil/comercial diferenciada. Verificar si los municipios chaquenos tienen ordenanza de procedimiento propio y que recursos preveen ante el Intendente o el Concejo Deliberante antes de ocurrir al fuero judicial.]

```
[VERIFICAR REGIMEN MUNICIPAL: Chaco - actos de municipios pueden tener fuero, plazos y via de agotamiento distintos del regimen provincial - verificar antes de encuadrar]
```

**Primer paso obligatorio en toda consulta:** identificar si el acto es de un organismo provincial, municipal o federal antes de aplicar este perfil o el nacional.

---

## Bloque 2 - Normativa de procedimiento administrativo provincial

### 2.1 Ley de procedimiento administrativo provincial

- **Norma principal:** Ley 179-A del Digesto Juridico Provincial (texto originario: Ley 1140, ano 1972). Denominacion: Codigo de Procedimientos Administrativos. [CONFIRMADO - fuente: Digesto Legislatura Chaco / Justia Argentina]
- **Reglamento:** [PENDIENTE: verificar si existe decreto reglamentario equivalente al Decreto 1759/72 federal.]
- **Texto vigente:** Consultar en digesto.legislaturachaco.gob.ar (texto ordenado como Ley 179-A). [CONFIRMADO que el texto ordenado existe en el Digesto provincial]
- **Articulado clave:** Arts. 36 al 42 (elementos del acto: competencia, causa, objeto, motivación, finalidad, formas/procedimiento). Arts. 43 al 48 (nulidades: Art. 44 nulidad absoluta e insanable, Art. 45 nulidad relativa). Arts. 82, 89, 95 (recursos). Art. 68 (silencio/pronto despacho). [CONFIRMADO]

```
[VERIFICAR VIGENCIA: Ley 179-A (Codigo de Procedimientos Administrativos, Chaco) - verificar modificaciones posteriores en el digesto o boletin oficial provincial]
```

### 2.2 Regimen de silencio administrativo provincial

- **Regla general:** silencio negativo. El silencio opera como ficcion legal para habilitar la via judicial (denegatoria tacita). [CONFIRMADO - Art. 68, Ley 179-A]
- **Secuencia:** el interesado debe interponer Pronto Despacho una vez vencidos los plazos ordinarios de resolucion. Transcurridos 30 dias habiles sin pronunciamiento tras el pronto despacho, opera la denegatoria tacita (efecto negativo). [CONFIRMADO - Art. 68, Ley 179-A]
- **Sin reforma analoga al silencio positivo de la Ley 27.742 nacional:** confirmado. El Chaco no adopto regimen de silencio positivo automatico. El silencio sigue siendo exclusivamente negativo. [CONFIRMADO]

### 2.3 Elementos esenciales del acto administrativo provincial

La Ley 179-A enumera expresamente los elementos del acto en los Arts. 36 al 42. [CONFIRMADO]

1. Competencia (Art. 36): irrenunciable e improrrogable
2. Causa (Art. 37): antecedentes de hecho y de derecho que fundamentan el acto
3. Objeto (Art. 38): cierto, licito, fisicamente posible
4. Motivacion (Art. 39): obligatoria; el acto debe expresar los motivos que lo determinan
5. Finalidad (Art. 40): adecuada a la causa del acto y al ordenamiento provincial
6. Formas y procedimiento (Arts. 41-42): cumplimiento de tramites esenciales previos

**Regimen de nulidades provincial:** La Ley 179-A distingue expresamente (Arts. 43-48):
- **Nulidad absoluta e insanable (Art. 44):** vicios graves en elementos esenciales del acto. Regla analoga al Art. 14 LNPA. [CONFIRMADO]
- **Nulidad relativa (Art. 45):** vicios leves saneables. Regla analoga al Art. 15 LNPA. [CONFIRMADO]

### 2.4 Recursos administrativos provinciales

Los recursos regulados en la Ley 179-A constituyen la via de agotamiento obligatorio. [CONFIRMADO que el agotamiento se formaliza a traves del recurso de reconsideracion y del recurso jerarquico regulados en la Ley 179-A.]

**Recurso de reconsideracion / revocatoria:**
- Plazo: 10 dias habiles administrativos [CONFIRMADO - Art. 82, Ley 179-A]
- Ante: mismo organo emisor [CONFIRMADO]
- Efecto subsidio: lleva implícito el jerarquico en subsidio; si el emisor mantiene su decision, eleva automaticamente las actuaciones [CONFIRMADO - Art. 82, Ley 179-A]
- Caracter: facultativo - puede omitirse e interponerse directamente el jerarquico [CONFIRMADO - Art. 82, Ley 179-A]

**Recurso jerarquico:**
- Plazo: 15 dias habiles administrativos [CONFIRMADO - Art. 89, Ley 179-A]
- Ante: autoridad superior / ministro / gobernador segun el caso [CONFIRMADO]
- Agota la via: si, como regla general [CONFIRMADO]
- **Interposicion directa:** puede interponerse sin reconsideracion previa (la reconsideracion no es obligatoria) [CONFIRMADO - Art. 82 y 89, Ley 179-A]

**Recurso de alzada:**
- Plazo: 15 dias habiles administrativos [CONFIRMADO - Art. 95, Ley 179-A]
- Procede: contra decisiones finales de entes autarquicos y descentralizados [CONFIRMADO]
- Ante: Poder Ejecutivo [CONFIRMADO - Art. 95, Ley 179-A]

**Queja:**
- [PENDIENTE: verificar si existe y sus efectos sobre otros plazos en la Ley 179-A.]

**Sin reforma analoga a la Ley 27.742 nacional:**
- Confirmado. No hubo duplicacion de plazos de recursos administrativos en sede provincial. Los plazos federales reformados no aplican a recursos ante la Administracion provincial chaqueña. [CONFIRMADO]

**Dias habiles administrativos Chaco:** son los dias habiles del Poder Ejecutivo provincial, que pueden diferir del calendario de dias habiles judiciales. Verificar decreto de asueto vigente al momento del acto.

```
[ALERTA PLAZO FATAL: recurso de reconsideracion - Ley 179-A Art. 82 - 10 dias habiles administrativos desde notificacion - vencimiento: calcular]
[ALERTA PLAZO FATAL: recurso jerarquico - Ley 179-A Art. 89 - 15 dias habiles administrativos desde notificacion del acto denegatorio o desde denegatoria tacita - vencimiento: calcular]
[ALERTA PLAZO FATAL: recurso de alzada - Ley 179-A Art. 95 - 15 dias habiles administrativos desde notificacion - solo contra actos de entes autarquicos/descentralizados - vencimiento: calcular]
```

### 2.5 Agotamiento de la via administrativa provincial

- **Regla general:** Es requisito previo de admisibilidad de la accion procesal administrativa ordinaria. El particular debe obtener el acto administrativo que cause estado (que no pueda ser revisado por otra autoridad superior). [CONFIRMADO - fuente: documento de referencia sobre el regimen chaqueño]
- **Via:** Recursos de reconsideracion y jerarquico regulados en la Ley 179-A. [CONFIRMADO]
- **Excepciones:** via de hecho administrativa, silencio administrativo negativo prolongado tras interponer pronto despacho, inoperancia manifiesta del ritualismo en supuestos de urgencia severa. [CONFIRMADO que rigen las dispensas clasicas - A VERIFICAR si hay norma o jurisprudencia local especifica que las regule en Chaco]
- **Fiscalia de Estado:** [PENDIENTE: verificar si interviene con dictamen obligatorio antes del acto, si la omision configura vicio de procedimiento, y si es parte necesaria en el proceso judicial.]
- **Organismos municipales:** [PENDIENTE: verificar si el agotamiento ante actos municipales tiene regulacion diferenciada.]

```
[VERIFICAR AGOTAMIENTO DE VIA: Chaco - Ley 179-A - verificar si se interpusieron los recursos en plazo y si la resolucion que agota la via fue notificada - determinar si aplica alguna excepcion]
```

### 2.6 Tabla unificada de plazos - sede administrativa

| Recurso / instituto | Plazo | Computo | Norma | Nivel de certeza |
|---------------------|-------|---------|-------|-----------------|
| Reconsideracion / revocatoria | 10 dias hab. adm. | desde notificacion | Ley 179-A Art. 82 | CONFIRMADO |
| Jerarquico | 15 dias hab. adm. | desde notificacion / denegatoria | Ley 179-A Art. 89 | CONFIRMADO |
| Alzada (entes autarquicos) | 15 dias hab. adm. | desde notificacion | Ley 179-A Art. 95 | CONFIRMADO |
| Pronto despacho / silencio | Pronto despacho: interponer al vencer plazos ordinarios. Luego 30 dias hab. sin pronunciamiento = denegatoria tacita | desde vencimiento de plazo ordinario | Ley 179-A Art. 68 | CONFIRMADO |

---

## Bloque 3 - Control judicial contencioso administrativo

### 3.1 Codigo / ley de proceso contencioso administrativo

- **Norma:** Ley 135-A del Digesto Juridico Provincial (texto originario: Ley 848, sancionada en 1967). Denominacion oficial: Codigo Contencioso Administrativo (CCA). [CONFIRMADO - fuente: documento de referencia / digesto.legislaturachaco.gob.ar]
- **Texto vigente:** Consultar en digesto.legislaturachaco.gob.ar (texto ordenado como Ley 135-A). [CONFIRMADO que el texto ordenado existe en el Digesto provincial]
- **Modificatorias:** [PENDIENTE: identificar leyes modificatorias relevantes posteriores a 1967.]
- **Subsidiariedad:** Se aplica supletoriamente el Codigo Procesal Civil y Comercial de la Provincia (Ley 2559-M). [CONFIRMADO - fuente: documento de referencia]

### 3.2 Plazo de caducidad para accionar judicialmente

**Este es el dato mas critico del perfil.**

- **Plazo general:** 30 dias habiles judiciales. [CONFIRMADO - fuente: documento de referencia que cita art. 12 del CCA, Ley 135-A]
- **Norma:** Art. 12 de la Ley 135-A (Codigo Contencioso Administrativo). [CONFIRMADO]
- **Computo:** desde la notificacion del acto administrativo definitivo que agota la instancia. [CONFIRMADO]
- **Naturaleza:** caducidad - vencido el plazo, el acto deviene firme e inimpugnable judicialmente por via ordinaria. [CONFIRMADO]
- **Declarable de oficio:** si. El STJ chaqueño aplica criterio riguroso: al estar involucrado el orden publico procesal y la habilitacion de la jurisdiccion, los plazos del Art. 12 de la Ley 135-A son de caducidad del derecho (no de prescripcion). El tribunal debe declararla de oficio si comprueba que la demanda ingreso fuera del termino legal, sin requerir peticion de la Fiscalia de Estado. [CONFIRMADO]
- **Perencia del tramite:** el STJ faculta declaracion oficiosa una vez constatada la inactividad absoluta por los plazos de rito (6 meses segun Art. 62 del CCA). [CONFIRMADO]
- **Advertencia - recursos optativos:** la reconsideracion es facultativa (Art. 82, Ley 179-A). Su interposicion suspende el plazo para el jerarquico mientras no se resuelva. El plazo de caducidad judicial del Art. 12 corre desde la notificacion del acto que causa estado, independientemente del recurso optativo interpuesto.

```
[ALERTA PLAZO FATAL: Ley 135-A art. 12 - 30 dias habiles judiciales - desde notificacion del acto que agota la via - vencimiento: calcular]
```

**Diferencia critica con el regimen federal:** el plazo federal (art. 25 LNPA) es de 180 dias habiles judiciales para actos notificados post-9-jul-2024. El plazo provincial chaqueño es de 30 dias habiles judiciales. No asumir equivalencia.

### 3.3 Organos jurisdiccionales

**Regimen mixto peculiar del Chaco.** [CONFIRMADO - fuente: documento de referencia]

**Camara en lo Contencioso Administrativo (fuero especializado):**
- Estructura: 3 salas. Sala I y Sala II con sede en Resistencia (Primera Circunscripcion). Sala III con sede en Presidencia Roque Saenz Pena (competencia territorial sobre el interior: Segunda a Sexta Circunscripcion Judicial). [CONFIRMADO]
- Cada sala funciona con dos jueces; admite integraciones cruzadas o subrogancias. [CONFIRMADO]
- Competencia: demandas de empleo publico, contratos, responsabilidad patrimonial ordinaria del Estado. Se tramitan directamente ante esta Camara; no ante el fuero Civil y Comercial. [CONFIRMADO]

**Superior Tribunal de Justicia (STJ) - instancia originaria:**
- El STJ retiene competencia originaria y exclusiva para demandas contencioso-administrativas dirigidas contra actos emanados directamente de los maximos poderes publicos provinciales. [CONFIRMADO - Art. 143 inc. 3, Constitucion Provincial del Chaco]
- **Criterio subjetivo estricto:** la competencia del STJ se activa unicamente cuando el acto es emitido por la cabeza maxima del organo de poder (Gobernador, pleno de la Legislatura, pleno del STJ, Miembros del Tribunal de Cuentas) en ejercicio de atribuciones institucionales o constitucionales directas. Si el acto proviene de un Ministro, Director General o subsecretaria, la competencia pertenece de manera exclusiva a las Salas de la Camara. [CONFIRMADO]
- Tambien tiene competencia en amparos de naturaleza nitidamente administrativa cuando el acto emana de los maximos poderes. [CONFIRMADO]

**Acceso al STJ en revision - Recurso Extraordinario Provincial:**
- Norma: Ley 1-B (Ley Organica del Poder Judicial, ex Ley 32). [CONFIRMADO]
- Plazo de interposicion: 10 dias habiles desde el dia siguiente de la notificacion de la sentencia definitiva de la Camara. [CONFIRMADO]
- Modalidades: Inconstitucionalidad (Art. 12, Ley 1-B), Casacion/inaplicabilidad de ley o doctrina legal (Art. 15, Ley 1-B), Nulidad (Art. 18, Ley 1-B). [CONFIRMADO]
- Requisitos formales: autosustentable, planteo nitido del caso constitucional o arbitrariedad manifiesta, rebate todos los fundamentos de la Camara, adecuacion a pautas de presentacion de las acordadas del STJ (analogas a las de la CSJN). [CONFIRMADO]

```
[ALERTA PLAZO FATAL: Recurso Extraordinario Provincial - Ley 1-B Arts. 12/15/18 - 10 dias habiles desde notificacion de sentencia definitiva de la Camara - vencimiento: calcular]
```

### 3.4 Pretensiones admisibles

La Ley 135-A estructura expresamente las pretensiones en el Art. 2 y el Art. 5. [CONFIRMADO]

- **Anulatoria** (anulacion total o parcial de actos administrativos): Art. 2 inc. a), Ley 135-A [CONFIRMADO]
- **Restablecimiento o reconocimiento** de derechos subjetivos vulnerados: Art. 2 inc. b), Ley 135-A [CONFIRMADO]
- **Resarcitoria** (indemnizacion de danos y perjuicios derivados de actividad licita o ilicita estatal): Art. 2 inc. c), Ley 135-A [CONFIRMADO]
- **Lesividad** (la propia Administracion demanda la nulidad de un acto propio firme pero ilegitimo): Art. 5, Ley 135-A [CONFIRMADO]

### 3.5 Medidas cautelares contra el Estado provincial

- **Regimen:** El Chaco no cuenta con ley especial de restricciones cautelares equivalente a la Ley federal 26.854. [CONFIRMADO - fuente: documento de referencia]. La Ley 26.854 rige solo contra el Estado nacional; no aplicarla al Estado provincial.
- **Norma aplicable:** El marco se rige supletoriamente por el Codigo Procesal Civil y Comercial de la Provincia (Ley 2559-M), articulado con los requisitos de la doctrina administrativa. [CONFIRMADO]
- **Requisitos:** verosimilitud del derecho, peligro en la demora, ponderacion de la no afectacion grave del interes publico. [CONFIRMADO que son los requisitos aplicables - A VERIFICAR regulacion especifica en la Ley 2559-M]
- **Informe previo del Estado:** no se exige con caracter general obligatorio antes del dictado de una cautelar ordinaria. Sin embargo, las Salas de la Camara aplican criterios de prudencia institucional, corriendo vistas breves cuando se puedan afectar servicios publicos esenciales. [CONFIRMADO - Ley 2559-M, practica del fuero]
- **Contracautela juratoria:** el CPCC provincial admite la graduacion de fianzas, pero en el fuero contencioso-administrativo el tribunal descarta la caucion meramente juratoria cuando la medida compromete directamente recursos fiscales o la ejecucion de politicas publicas del Estado. En esos supuestos se exige caucion real o personal suficiente, salvo beneficio de litigar sin gastos del peticionante. [CONFIRMADO - Ley 2559-M aplicada en el fuero CA]

```
[VERIFICAR REGIMEN CAUTELAR: Chaco - Ley 2559-M (CPCC provincial) - no asumir equivalencia con Ley 26.854 nacional]
```

### 3.6 Amparo provincial

- **Norma:** Ley 4297, ordenada en el Digesto actual como Ley 152-M. [CONFIRMADO - fuente: documento de referencia]. Reglamenta el procedimiento expedito del amparo en sede local.
- **Aplicacion directa:** Art. 43 de la Constitucion Nacional y CADH operan directamente con independencia de la Ley 152-M. [CONFIRMADO]
- **Competencia:** el STJ tiene competencia originaria en amparos de naturaleza nitidamente administrativa cuando el acto impugnado emana de los maximos poderes publicos provinciales. [CONFIRMADO]
- **Plazo:** 15 dias habiles desde que el afectado tomo conocimiento directo, efectivo y fehaciente del acto, hecho u omision que reputa lesivo, arbitrario o manifiestamente ilegal. [CONFIRMADO - Art. 5, Ley 152-M]
- **Subsidiariedad:** [A VERIFICAR: si la Ley 152-M exige expresamente que no haya otro remedio judicial mas idoneo o si se regula por aplicacion del Art. 43 CN.]

```
[ALERTA PLAZO FATAL - AMPARO: Ley 152-M Art. 5 - 15 dias habiles - desde que el afectado tomo conocimiento fehaciente del acto o hecho lesivo - vencimiento: calcular]
```

---

## Bloque 4 - Normativa de referencia provincial

### 4.1 Responsabilidad del Estado provincial

- **Ley propia:** no hay adhesion a la Ley 26.944 nacional ni ley local autonoma equivalente. La base es constitucional directa: Art. 76 de la Constitucion Provincial del Chaco, que establece un regimen de responsabilidad objetiva y directa del Estado. [CONFIRMADO]
- **Aplicacion de la Ley 26.944:** no aplicar. Rige solo contra el Estado nacional. [CONFIRMADO]
- **Aplicacion del CCCN:** verificar criterio del fuero antes de aplicarlo. El regimen constitucional local es la fuente primaria. [A VERIFICAR: jurisprudencia de la Camara CA sobre relacion entre Art. 76 CP y el CCCN]
- **Ejecucion de sentencias condenatorias:** las sentencias que obliguen al Estado Provincial o a sus municipios al pago de sumas de dinero revisten caracter declarativo en cuanto al modo de ejecucion inmediata. El Estado incorpora el credito al presupuesto del ejercicio subsiguiente. No pueden trabarse embargos sobre bienes dominiales publicos ni fondos afectados a servicios esenciales. [CONFIRMADO]
- **Prescripcion de la accion:** [PENDIENTE: plazo y norma aplicable. El Art. 76 CP no lo fija expresamente; verificar si la jurisprudencia aplica el plazo del CCCN, de la Ley 26.944 por analogia o un criterio propio.]

```
[VERIFICAR REGIMEN DE RESPONSABILIDAD: Chaco - base Art. 76 CP (responsabilidad objetiva y directa) - no aplicar Ley 26.944 ni CCCN sin verificar criterio del fuero provincial - prescripcion: pendiente]
```

### 4.2 Empleo publico provincial

- **Estatuto general:** Ley 2017-A del Digesto Juridico Provincial. [CONFIRMADO]
- **Escalafon general:** Ley 1276-A (ex Ley 5428). [CONFIRMADO]
- **Estatutos sectoriales:**
  - Docente: Ley 647-E (ex Ley 3529) [CONFIRMADO]
  - Carrera Sanitaria (salud): Ley 2551-G (ex Ley 5421) [CONFIRMADO]
  - Personal Policial: Ley 1394-J (ex Ley 5594) [CONFIRMADO]
- **Negociacion colectiva:** Chaco tiene ley propia; no aplica directamente la Ley 24.185 nacional. Norma local: Ley 2361-A (ex Ley 7293), regimen de convenciones colectivas de trabajo para el sector publico provincial. [CONFIRMADO]
- **Regimen disciplinario:** [PENDIENTE: norma que regula el sumario administrativo provincial. Plazos, garantias, recursos internos.]

```
[VERIFICAR ESTATUTO APLICABLE: Chaco - Ley 2017-A (general) / Ley 647-E (docentes) / Ley 2551-G (salud) / Ley 1394-J (policia) - identificar el aplicable segun el organismo y la categoria del agente antes de analizar derechos]
```

### 4.3 Contratacion publica provincial

- **Norma general:** Ley 1092-A (Ley de Administracion Financiera del Chaco). El regimen de contrataciones esta integrado en su Titulo VII. [CONFIRMADO]
- **Decreto reglamentario:** Decreto 3566/1977 (Regimen de Contrataciones de la Provincia) y sus actualizaciones de montos y topes para las Unidades de Contratacion. Siempre indexar el Decreto 3566/77 como brazo reglamentario de la Ley 1092-A. [CONFIRMADO]
- **Plataforma de compras:** "Contrataciones Chaco" o Portal de Compras y Contrataciones de la Provincia, gestionado por la Contaduria General de la Provincia. [CONFIRMADO]
- **Organismo rector:** Contaduria General de la Provincia. [CONFIRMADO]
- **Obra publica provincial:** Ley 1121-A (ex Ley 4990). Chaco tiene ley propia y no asimila la Ley 13.064 nacional. Rige la totalidad de los contratos de construccion publica provinciales. [CONFIRMADO]
- **Redeterminacion de precios:** regimen local autonomo. Decreto Provincial 1121/2004 (y modificatorios periodicos segun indices INDEC/Direccion de Estadisticas local). El regimen opera bajo el decreto base y sus resoluciones complementarias del Ministerio de Infraestructura. No fue sustituido por un digesto autonomo. [CONFIRMADO]

```
[VERIFICAR VIGENCIA: montos de licitacion - Decreto 3566/77 y actualizaciones - verificar antes de encuadrar el procedimiento de seleccion]
```

### 4.4 Organismos de control externo

- **Tribunal de Cuentas:** existe y tiene funcion jurisdiccional (juicio de cuentas y de responsabilidad, fallos de cargo). Norma: Ley 931-A. Sus resoluciones son revisables judicialmente por demanda CA de plena jurisdiccion ante la Camara o por recurso de revision ante el STJ. [CONFIRMADO]
- **Competencia sobre municipios:** el Tribunal de Cuentas provincial tiene competencia de control externa, obligatoria y exclusiva sobre los municipios. La Constitucion Provincial no faculta a las comunas a crear tribunales de cuentas municipales autonomos independientes del provincial. Todas las intendencias y concejos rinden sus cuentas directamente ante el Tribunal de Cuentas de la Provincia. [CONFIRMADO - Ley 931-A]
- **Fiscalia de Estado:** parte obligatoria en todos los juicios CA, expropiaciones, ejecuciones fiscales y amparos contra la Administracion provincial. Domicilio en Resistencia. No cuenta con plataforma abierta de consulta publica de dictamenes; su portal esta abocado a la gestion del Cuerpo de Abogados del Estado y notificaciones procesales. [CONFIRMADO]

### 4.5 Defensor del Pueblo provincial

[PENDIENTE: verificar si existe Defensor del Pueblo provincial en el Chaco y si tiene legitimacion procesal en el fuero contencioso administrativo. Norma y articulo.]

### 4.6 Tabla de responsables procesales por instancia

[PENDIENTE: completar para evitar errores de notificacion y de legitimacion pasiva.]

| Instancia | Representante del Estado | Normativa |
|-----------|--------------------------|-----------|
| Camara Contencioso Administrativa | [PENDIENTE] | [PENDIENTE] |
| STJ (instancia originaria) | [PENDIENTE] | [PENDIENTE] |
| Notificaciones | [PENDIENTE: domicilio procesal del representante] | [PENDIENTE] |

```
[VERIFICAR REPRESENTACION PROCESAL: Chaco - identificar el representante del Estado por instancia antes de radicar - las notificaciones deben cursarse en el domicilio procesal correcto]
```

---

## Bloque 5 - Alerta normativa

*Ultima verificacion de esta seccion: mayo 2026. Actualizar cuando cambie alguna de las normas listadas.*

### Plazos de caducidad

Los plazos para impugnar actos administrativos provinciales del Chaco son breves y fatales. No asumir equivalencia con el regimen federal.

```
[ALERTA PLAZO FATAL: Ley 135-A art. 12 - 30 dias habiles judiciales - desde notificacion del acto que agota la via - vencimiento: calcular]
```

### Matriz de vigencia por norma

| Norma | Materia | Estado | Ultima verificacion | Fuente |
|-------|---------|--------|--------------------|----|
| Ley 135-A (ex Ley 848) | Proceso contencioso administrativo | CONFIRMADO | mayo 2026 | digesto.legislaturachaco.gob.ar |
| Ley 179-A (ex Ley 1140) | Procedimiento administrativo | CONFIRMADO | mayo 2026 | digesto.legislaturachaco.gob.ar / Justia Argentina |
| Ley 2559-M | CPCC provincial (supletorio) | CONFIRMADO | mayo 2026 | documento de referencia |
| Ley 152-M (ex Ley 4297) | Amparo provincial | CONFIRMADO | mayo 2026 | documento de referencia |
| Estatuto empleo publico | Empleo publico | PENDIENTE | - | - |
| Norma contrataciones | Contratacion publica | PENDIENTE | - | - |
| Ley resp. Estado | Responsabilidad del Estado | PENDIENTE | - | - |

### Normas de vigencia variable a verificar en cada consulta

- **Montos de contratacion publica:** se actualizan por decreto o resolucion - verificar antes de encuadrar el procedimiento de seleccion.
- **Escala salarial del empleo publico provincial:** se modifica por paritarias - no asumir montos sin verificar.
- **Presupuesto provincial vigente:** relevante para el regimen de ejecucion de sentencias (consolidacion de creditos y partidas presupuestarias).

---

## Bloque 6 - Fuentes primarias

- **Boletin Oficial:** [PENDIENTE: URL del boletin oficial provincial del Chaco]
- **Digesto / Portal juridico provincial:** digesto.legislaturachaco.gob.ar [CONFIRMADO]
- **Tribunal superior provincial:** [PENDIENTE: URL de jurisprudencia del STJ chaqueño]
- **Fiscalia de Estado:** [PENDIENTE: URL si publica dictamenes]
- **Organismo de compras:** [PENDIENTE: URL de la plataforma de contrataciones provincial]
- **Poder Judicial provincial:** [PENDIENTE: URL portal general]

---

## Bloque 7 - Reglas de citacion

Las reglas generales del CLAUDE.md argentino y del kb/perfiles/administrativo-CLAUDE.md nacional aplican integramente. Especificas para este fuero:

**Jurisprudencia:** nunca citar sala, expediente o caratula sin material aportado. El criterio de la sala actuante es determinante; la Camara y el STJ pueden tener posiciones diferentes en cuestiones no unificadas. Usar:
```
[INSERTAR FALLO VERIFICADO: Camara Contencioso Administrativa Chaco / STJ Chaco - sala/instancia - doctrina requerida]
```

**Actos administrativos provinciales:** no asumir el contenido de resoluciones, disposiciones, dictamenes o actos impugnados sin que el abogado los aporte. Usar:
```
[VACIO PROBATORIO: texto del acto administrativo provincial/municipal no aportado - aportar copia del acto impugnado con sello de notificacion]
```

**Plazos provinciales:** no transpolar plazos del regimen federal. Usar:
```
[ALERTA PLAZO FATAL: [norma provincial art. X] - [X] dias [habiles/corridos] - desde [inicio del computo] - vencimiento: calcular]
```

**Dictamenes de Fiscalia de Estado:** no asumir su contenido sin material aportado. Usar:
```
[VACIO PROBATORIO: dictamen de Fiscalia de Estado no aportado - aportar texto del dictamen si fue emitido en el expediente]
```

---

## Bloque 8 - Logica de analisis por institucion

Las instituciones que siguen tienen base en el derecho administrativo general argentino. Donde la ley o jurisprudencia provincial difiera del regimen nacional, prevalece la regla local indicada en los bloques anteriores.

### Acto administrativo - elementos y vicios

Aplicar Ley 179-A. Elementos segun seccion 2.3.

Preguntas de diagnostico:
1. El acto impugnado, es definitivo o de mero tramite? Es del Estado provincial, de un municipio o de los maximos poderes (Legislatura, PE, Tribunal de Cuentas)?
2. El acto fue notificado? En que fecha? (inicio del computo del plazo de caducidad)
3. Que elementos del acto se cuestionan?
4. Hay expediente administrativo que lo respalda? El abogado lo tiene o hay que pedirlo por vista?
5. Se recurrio en sede administrativa? Que recursos se interpusieron y en que plazo?
6. Intervino Fiscalia de Estado cuando era obligatorio? El dictamen fue emitido antes del acto?

### Recursos administrativos provinciales

Aplicar el esquema de la seccion 2.4. Verificar siempre:
- Plazo desde la notificacion (habiles administrativos provinciales, no judiciales)
- Organo ante el que se interpone
- Si la reconsideracion es obligatoria o el jerarquico puede interponerse directamente
- Si el recurso de alzada ante entes descentralizados es obligatorio u optativo
- Si el recurso agota la via o hay que interponer el jerarquico

```
[ALERTA PLAZO FATAL: recurso [denominacion] - Ley 179-A art. [PENDIENTE] - [X] dias habiles administrativos desde notificacion - vencimiento: calcular]
```

### Agotamiento de la via administrativa provincial

Antes de analizar cualquier accion judicial:
1. Verificar si la via esta agotada (seccion 2.5)
2. Si no lo esta, determinar si aplica alguna excepcion local (via de hecho, silencio, inutilidad del ritualismo)
3. Verificar si la Fiscalia de Estado requiere intervencion previa
4. Alertar sobre el plazo de caducidad para accionar: 30 dias habiles judiciales desde la notificacion del acto que agota la via (art. 12, Ley 135-A)

### Responsabilidad del Estado provincial

Alertas:
- No aplicar la Ley 26.944 nacional a demandas contra el Estado provincial chaqueño sin verificar si la provincia tiene ley propia
- No aplicar el CCCN sin verificar el regimen local
- Las sentencias condenatorias son declarativas en cuanto a su ejecucion inmediata; el Estado incorpora el credito al presupuesto del ejercicio subsiguiente
- No trabarse embargos sobre bienes dominiales ni fondos de servicios esenciales

### Empleo publico provincial

Verificar siempre:
- Situacion de revista del agente (planta permanente con estabilidad / sin estabilidad / contratado / transitorio / gabinete)
- Estatuto aplicable (general o sectorial) - ver seccion 4.2
- Si hubo sumario con garantias de debido proceso (notificacion de cargos, vista, descargo, prueba)
- Si la sancion expulsiva encuadra en alguna causal taxativa del estatuto
- Prescripcion de la accion disciplinaria segun el estatuto provincial

### Contratacion publica provincial

Verificar siempre:
- Montos vigentes para encuadrar el tipo de procedimiento (licitacion publica / privada / directa)
- Plazos de impugnacion de pliegos y preadjudicacion segun la norma local
- Si la redeterminacion de precios aplica y bajo que regimen
- Si el contrato es de obra publica: verificar si aplica ley provincial propia o Ley 13.064 nacional

---

## Bloque 9 - Instrucciones operativas

### Alerta critica - plazo de caducidad para accionar judicialmente

**Este es el primer paso en toda consulta que involucre una accion judicial contra el Estado provincial del Chaco.**

```
[ALERTA PLAZO FATAL: Ley 135-A art. 12 - 30 dias habiles judiciales - desde notificacion del acto que agota la via - vencimiento: calcular]
```

El plazo para demandar es un plazo de caducidad, no de prescripcion:
- No se suspende ni interrumpe por las mismas causales que la prescripcion
- Vencido el plazo, la accion caduca aunque el derecho de fondo este vigente
- La caducidad puede declararse de oficio

**Diferencia con el regimen federal:** el plazo federal (art. 25 LNPA) es de 180 dias habiles judiciales para actos post-9-jul-2024. El plazo chaqueño es de 30 dias habiles judiciales (art. 12, Ley 135-A). No asumir equivalencia.

---

- Identificar si el acto es del Estado provincial, de un municipio o de un organismo federal antes de aplicar este perfil o el nacional.
- Identificar si el acto emana de los maximos poderes publicos provinciales (Legislatura, PE, Tribunal de Cuentas): en ese caso, la competencia es del STJ en instancia originaria, no de la Camara.
- En actos mixtos: aplicar cada regimen al acto correspondiente por separado.
- Verificar agotamiento de la via administrativa provincial antes de analizar la accion judicial.
- Plazos de recursos en sede administrativa son habiles administrativos, no judiciales. No confundir.
- En responsabilidad del Estado provincial: verificar primero si existe ley propia antes de aplicar principios generales. No aplicar Ley 26.944 ni CCCN sin verificar criterio del fuero. Las sentencias son declarativas en su ejecucion; no trabar embargos sobre bienes dominiales ni fondos esenciales.
- En empleo publico: identificar el estatuto aplicable (general o sectorial) antes de analizar los derechos del agente.
- En contratacion publica: verificar montos vigentes antes de encuadrar el tipo de procedimiento.
- No asumir el contenido de actos, expedientes, pliegos ni dictamenes de Fiscalia de Estado sin que el abogado los aporte.
- Todo escrito del fuero chaqueño cierra con "Estado del escrito" estandar mas: fuero y regimen aplicado (Camara CA o STJ instancia originaria), estado del agotamiento de la via administrativa provincial, **plazo de caducidad provincial (art. 12 Ley 135-A, 30 dias habiles judiciales - verificado / pendiente / vencido)**, intervencion de Fiscalia de Estado (si / no / a verificar), sala del tribunal si ya esta radicada la causa, proximo plazo procesal si lo hay, regimen de responsabilidad aplicable (ley provincial propia / principios generales / CCCN solo si es contratista privado).

---

## Lista consolidada de pendientes para completar el perfil

Antes de operar en un caso concreto, verificar los siguientes datos en las fuentes indicadas:

**Fuente: texto de la Ley 179-A (digesto.legislaturachaco.gob.ar)**
- Articulos sobre elementos del acto administrativo
- Plazo y efectos del recurso de reconsideracion
- Plazo y efectos del recurso jerarquico
- Si la reconsideracion es obligatoria antes del jerarquico o puede omitirse
- Recurso de alzada: si existe, plazo y ante quien
- Queja: si existe y sus efectos sobre otros plazos
- Silencio administrativo: positivo/negativo/mixto, plazo y si requiere pronto despacho previo
- Motivacion: si es obligatoria y en que supuestos
- Nulidades: si la ley distingue nulidad absoluta/relativa con criterios analogos a la LNPA

**Fuente: texto de la Ley 135-A (digesto.legislaturachaco.gob.ar)**
- Modificatorias posteriores a 1967
- Pretensiones admisibles (si el CCA las enumera o sigue sistema abierto)
- Si la caducidad es declarable de oficio segun jurisprudencia del STJ
- Si hay proceso sumario o abreviado con plazo distinto

**Fuente: Constitucion Provincial del Chaco**
- Articulo exacto que establece la competencia originaria del STJ en materia contencioso administrativa
- Limites jurisprudenciales de "actos de los maximos poderes" para distinguir del fuero de la Camara

**Fuente: Ley 152-M (digesto.legislaturachaco.gob.ar)**
- Plazo del amparo provincial (dias habiles o corridos, desde cuando corre)
- Subsidiariedad del amparo

**Fuente: Poder Judicial del Chaco / STJ**
- URL de acceso a jurisprudencia
- Numero de salas de la Camara CA, composicion y criterios de distribucion de causas
- Recurso extraordinario provincial: nombre, requisitos de admisibilidad
- Criterio del STJ sobre declaracion de oficio de la caducidad

**Fuente: Poder Ejecutivo provincial / Boletin Oficial**
- URL del Boletin Oficial provincial
- Estatuto del empleado publico provincial (numero de ley)
- Escalafon general y estatutos sectoriales (docente, salud, policia)
- Norma de contrataciones publicas provinciales
- Ley de responsabilidad del Estado provincial (si existe)
- Decreto reglamentario de la Ley 179-A (si existe)
- Si existe reforma analoga al regimen de silencio positivo de la Ley 27.742 nacional

**Fuente: Fiscalia de Estado del Chaco**
- URL institucional
- Si publica dictamenes en linea
- Si es parte necesaria en el proceso contencioso administrativo y en que supuestos
- Domicilio procesal para notificaciones

**Fuente: Tribunal de Cuentas del Chaco**
- Si tiene funcion jurisdiccional
- Si sus resoluciones son revisables judicialmente y por que via
- Si tiene competencia sobre municipios

**Fuente: CPCC provincial (Ley 2559-M)**
- Requisitos especificos de las medidas cautelares contra el Estado provincial
- Si se exige informe previo del organismo demandado antes de resolver la cautelar
- Contracautela: si se exige siempre y si puede ser juratoria

---

*Ultima actualizacion: mayo 2026*
*Normativa base incorporada: Ley 135-A (CCA), Ley 179-A (CPA), Ley 152-M (amparo), Ley 2559-M (CPCC supletorio)*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
