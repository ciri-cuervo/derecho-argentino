# Perfil de práctica · Derecho administrativo · Provincia de San Luis

> Archivo de configuración para el sistema derecho-argentino.
> Complementa el perfil general y el perfil administrativo nacional (kb/perfiles/administrativo-CLAUDE.md) con lógica específica del proceso contencioso administrativo de San Luis.
> Cargar junto con kb/perfiles/administrativo-CLAUDE.md en el Project. Este archivo no reemplaza al nacional - lo extiende.
> **Configuración inicial obligatoria:** completar las variables del Bloque 0 antes de usar.
>
> **Estado del perfil:** operativo y completo. Todos los campos estructurales, sustantivos y de configuración inicial completados y verificados. Sin [A VERIFICAR] operativos ni [PENDIENTE] estructurales.

---

## Sistema de etiquetas

- **[CONFIRMADO]** Dato extraído directamente del texto legal citado; sin reformas conocidas al corte de la fecha de actualización del perfil.
- **[A VERIFICAR]** Dato probable o histórico que debe confirmarse en el Boletín Oficial provincial o en el portal del Poder Judicial antes de aplicar al caso concreto.
- **[PENDIENTE]** Dato no disponible en este perfil; requiere investigación activa antes de operar.

---

## Changelog

| Versión | Fecha | Cambios principales |
|---------|-------|---------------------|
| 1.0 | Mayo 2025 | Versión inicial - fuente: documento de trabajo del usuario (sistema CA de San Luis, estructura general) |
| 1.1 | Mayo 2025 | Completado: arts. 766-769 CPCC (texto íntegro); arts. 84, 90, 92 y 93 LPA (recursos, pronto despacho y silencio con artículos exactos); Fiscalía de Estado (arts. 235 y ss. CP + Ley N° V-0164-2004, parte necesaria, nulidad insanable); amparo local (Ley N° IV-0087-2004: legitimación, plazo 15 días hábiles art. 4, informe 5 días art. 8, sentencia 48 hs art. 12, apelación 48 hs efecto devolutivo art. 15); estatutos de empleo público (general Ley N° I-0054-2004; docente Ley N° XV-0387-2004; policial Ley N° VII-0167-2004; sanitario Ley N° I-0550-2006); contrataciones (Ley N° VI-0158-2004, DGCC); Tribunal de Cuentas (art. 229 CP + Ley N° V-0163-2004); Defensor del Pueblo (figura vacante); tasa de interés (pasiva BNA histórica / giro hacia activa BNA en créditos alimentarios); competencia CA municipal (art. 766 CPCC + Ley N° XII-0349-2004 + cartas orgánicas); eliminados todos los [PENDIENTE] estructurales |
| 1.2 | Mayo 2025 | Completado: notificación Fiscalía de Estado en GIAJ (dominio @giajsanluis.gov.ar, alta como co-demandada obligatoria, alerta de nulidad por omision de traslado electrónico); tasa de interes STJ (giro jurisprudencial: reemplaza doctrina "Fleitas" - nueva tasa TNA Préstamos Personales agente financiero oficial provincial, efecto retroactivo a expedientes sin sentencia firme, calculadora GIAJ); contrataciones: sistema de Unidades de Compra (UC) actualizables por resolución ministerial - regla de cotejo obligatoria por fecha del acto de llamado |
| 1.3 | Mayo 2025 | Configuración inicial completada: AREAS_PRACTICA (Empleo Público / Contratos y Pliegos / Amparo / Responsabilidad del Estado) y ORGANISMO_CONTRALOR_HABITUAL (Tribunal de Cuentas + DGCC). Perfil operativo completo. |
| 1.4 | Mayo 2025 | Completado: Bloque 7.1 Responsabilidad del Estado (vacío legislativo post-CCyCN, solución jurisprudencial STJ, falta de servicio como factor objetivo, agotamiento según origen del daño, regla de solicitud de conversión a proceso ordinario en escrito de inicio); corrección punto 5 checklist impugnación (canal exclusivo GIAJ - Fiscalía de Estado); normalización tipográfica. Sin [A VERIFICAR] operativos ni [PENDIENTE] estructurales. |
| 1.5 | Mayo 2025 | Completado: decreto reglamentario LPA (Decreto N° 1823 y actualizaciones de tramitación digital - naturaleza ordenatoria y NO bloqueante; principio de informalismo a favor del administrado; principio de informalismo documentado). Perfil cerrado: sin marcadores abiertos. |

---

## Bloque 0 - Configuración inicial

**PROVINCIA:** Provincia de San Luis

**FUERO_HABITUAL:** Juzgados de Primera Instancia en lo Civil, Comercial y Minas de cada circunscripción judicial (no existe fuero CA especializado). Alzada: Cámaras de Apelaciones en lo Civil, Comercial, Minas y Laboral. Recurso extraordinario: Superior Tribunal de Justicia (STJ) de San Luis. [CONFIRMADO]

**AREAS_PRACTICA:** Empleo Público Provincial y Municipal / Impugnación de Contratos y Pliegos licitatorios / Amparos por Ilegalidad y Arbitrariedad Manifiesta contra el Estado Provincial / Daños y Perjuicios por Responsabilidad del Estado. Encuadre: el proceso sumarísimo del art. 768 CPCC y el plazo de caducidad de 30 días hábiles del art. 767 exigen concentrar la práctica en la velocidad de habilitación de instancia, la liquidación bajo TNA Préstamos Personales y la neutralización de vías de hecho estatales.

**ORGANISMO_CONTRALOR_HABITUAL:** Tribunal de Cuentas de la Provincia de San Luis (art. 229 CP / Ley N° V-0163-2004) - competencia exclusiva en juicios de cuentas y responsabilidad con impacto en empleo público y gestión de fondos. Dirección General de Compras y Contrataciones del Ministerio de Hacienda e Infraestructura Pública - autoridad técnica emisora del valor dinámico de las Unidades de Compra para fiscalización de licitaciones.

---

## Bloque 1 - Identidad y alcance

Este perfil cubre práctica de derecho administrativo en la Provincia de San Luis: procedimiento administrativo ante organismos provinciales y municipales (Ley N° VI-0156-2004), recursos administrativos en sede provincial, control judicial contencioso administrativo (Ley N° VI-0150-2004, Título IV, arts. 766 a 769), responsabilidad del Estado provincial y empleo público provincial.

**Particularidad estructural - sin fuero especializado:** San Luis no tiene juzgados ni cámaras contencioso administrativas propias. Las causas CA tramitan ante los Juzgados de Primera Instancia en lo Civil, Comercial y Minas bajo el proceso sumarísimo civil, con las adaptaciones del Título IV del CPCC local (arts. 766 a 769). El juez puede disponer por resolución fundada la aplicación del proceso ordinario si la complejidad del asunto lo justifica (art. 768). Esta estructura condiciona la lógica de audiencias, plazos procesales y el perfil del tribunal. [CONFIRMADO]

**Particularidad estructural - sin código CA propio:** el proceso CA no tiene cuerpo normativo propio. El Título IV del CPCC (arts. 766 a 769) opera por remisión al proceso sumarísimo, con las excepciones de los arts. 768 (posible conversión a ordinario) y 769 (no suspensión de la ejecución del acto). [CONFIRMADO]

**Articulación con el perfil nacional:** cuando actúa un organismo federal con sede en San Luis (ARCA/ex AFIP, ANSES, organismos desconcentrados nacionales), aplica el régimen federal (LNPA + RLNPA). Cuando actúa la Administración provincial o municipal puntana, aplica este perfil. No transpolar plazos ni institutos.

**Actos mixtos:** cuando en un mismo caso coexisten actos de organismos provinciales y federales, cada régimen se aplica al acto correspondiente por separado.

**Tercer nivel - organismos municipales:** el art. 766 del CPCC incluye taxativamente a municipios y comunas dentro de la materia CA provincial. Los juzgados civiles de la circunscripción correspondiente conocen en actos de intendentes y concejos deliberantes. El agotamiento de la vía municipal se rige por la Ley N° XII-0349-2004 y las cartas orgánicas de cada municipio (San Luis Capital, Villa Mercedes, Merlo). Los actos del intendente o las ordenanzas definitivas del concejo agotan la vía per se. [CONFIRMADO]

**Primer paso obligatorio en toda consulta:** identificar si el acto es del Estado provincial, de un municipio o de un organismo federal antes de aplicar este perfil o el nacional.

---

## Bloque 2 - Normativa de procedimiento administrativo provincial

### 2.1 Ley de procedimiento administrativo provincial

- **Norma principal:** Ley N° VI-0156-2004 (texto ordenado por el Digesto Provincial; históricamente Ley N° 5540). [CONFIRMADO]
- **Contenido:** regula los plazos internos de los expedientes administrativos, la teoría del acto administrativo y los recursos de reconsideración y jerárquico. [CONFIRMADO]
- **Reglamento:** existe. Decreto N° 1823 y sus actualizaciones de tramitación digital (módulos de expedientes). Es de naturaleza puramente ordenatoria y NO bloqueante. [CONFIRMADO]

**Regla de oro - decreto reglamentario no bloqueante:** las formalidades del decreto reglamentario (orden de folios, pases entre oficinas, plazos internos para dictámenes, formalidades menores de escritos) no pueden ser invocadas por el Estado para declarar la caducidad, el rechazo in limine o la inadmisibilidad de un recurso sustantivo. [CONFIRMADO]

**Principio de informalismo a favor del administrado:** el STJ San Luis es pacífico en esto. Solo los plazos de raigambre legal (10 días para reconsideración y 15 días para jerárquico, arts. 84 y 90 LPA) pueden bloquear la vía por extemporaneidad. Cualquier defecto de forma derivado del decreto reglamentario debe ser reconducido por la Administración mediante apercibimiento para subsanar; nunca como obstáculo insalvable al derecho de defensa. [CONFIRMADO]



### 2.2 Recursos administrativos

**Recurso de reconsideración (art. 84, LPA):**
- Plazo de interposición: 10 días hábiles desde la notificación del acto.
- Plazo para resolver: 15 días hábiles.
- Autoridad: el mismo órgano que dictó el acto.
- Particularidad: si el acto proviene de la máxima autoridad, este recurso es optativo y su resolución agota la vía directamente. [CONFIRMADO]

**Recurso jerárquico (art. 90, LPA):**
- Plazo de interposición: 15 días hábiles desde la notificación de la denegatoria de la reconsideración o desde el vencimiento del plazo para resolverla (si se acude directamente en queja).
- Plazo para resolver: 30 días hábiles.
- Autoridad: máxima autoridad (Gobernador o Ministro según delegación estructural).
- Agota la vía administrativa cuando lo resuelve la máxima autoridad. [CONFIRMADO]

### 2.3 Silencio administrativo y pronto despacho

Secuencia obligatoria para configurar la denegatoria tácita:

1. Vencimiento del plazo legal para resolver el recurso definitivo (jerárquico: 30 días hábiles; o reconsideración ante la máxima autoridad: 15 días hábiles).
2. Presentación de pronto despacho por el interesado (art. 92, LPA).
3. Transcurso de 30 días hábiles sin resolución desde el pronto despacho (art. 93, LPA).
4. Configuración de la denegatoria tácita: queda expedita la vía judicial contencioso administrativa. [CONFIRMADO]

**Alerta:** el pronto despacho es un paso procesal obligatorio. Sin él, no se configura el silencio. No saltearlo.

---

## Bloque 3 - Proceso contencioso administrativo

### 3.1 Texto íntegro de los artículos 766 a 769 (CPCC, Ley N° VI-0150-2004)

**Art. 766 - Materia del proceso:**
Corresponde al conocimiento y decisión de los Jueces de Primera Instancia en lo Civil, Comercial y Minas las causas contencioso-administrativas, entendiéndose por tales aquellas en que se deduzca pretensión fundada en el derecho administrativo, contra la Provincia, sus municipios, comunas o entidades descentralizadas con facultades de imperio, y en las que se impugnen actos dictados en ejercicio de la función administrativa. [CONFIRMADO]

**Art. 767 - Habilitación de instancia. Plazo:**
Para la procedencia de la demanda contencioso-administrativa, es requisito indispensable el previo agotamiento de la vía administrativa, de conformidad con lo establecido en la Ley de Procedimientos Administrativos. La demanda deberá interponerse dentro del plazo perentorio de TREINTA (30) días, contados a partir del día siguiente al de la notificación del acto que agote la vía administrativa o, en su caso, del día en que quede configurada la denegación tácita por silencio. [CONFIRMADO]

**Art. 768 - Trámite. Tipo de proceso:**
La demanda contencioso-administrativa tramitará por las reglas del proceso sumarísimo, salvo que el Juez, por resolución fundada y atendiendo a la complejidad del asunto, disponga la aplicación de las reglas del proceso ordinario. No se admitirá la reconvención. [CONFIRMADO]

**Art. 769 - Efecto de la interposición:**
La interposición de la demanda contencioso-administrativa no suspende la ejecución del acto impugnado, salvo que el Juez, a petición de parte, ordene la suspensión como medida cautelar, cuando de la ejecución del acto puedan derivarse perjuicios graves o de imposible reparación, o cuando se alegue fundadamente una nulidad absoluta y manifiesta. [CONFIRMADO]

### 3.2 Habilitación de instancia

**Requisito de agotamiento de la vía:** obligatorio. Debe mediar acto definitivo dictado por la máxima autoridad o denegatoria tácita por silencio (conf. secuencia del Bloque 2.3). [CONFIRMADO - art. 767]

**Excepciones al agotamiento:** las clásicas (vías de hecho, ineficacia manifiesta del carril recursivo, urgencia extrema con daño irreparable) se canalizan por amparo (Ley N° IV-0087-2004), no por la vía CA ordinaria. [CONFIRMADO]

**Pretensiones admisibles:** el art. 766 configura un sistema abierto basado en la naturaleza del acto (función administrativa) y en la calidad de la demandada (Provincia, municipios, comunas, entidades descentralizadas con facultades de imperio). No existe lista taxativa de pretensiones. [CONFIRMADO]

**Reconvención:** no admitida (art. 768). [CONFIRMADO]

### 3.3 Plazo de caducidad

**Plazo:** 30 días hábiles judiciales (art. 767). [CONFIRMADO]

**Cómputo:**
- Acto expreso: desde el día siguiente a la notificación del acto que agota la vía (resolución del jerárquico o de la reconsideración ante la máxima autoridad).
- Silencio: desde el día en que queda configurada la denegación tácita (conf. art. 93 LPA: 30 días hábiles desde el pronto despacho sin resolución).

**Efecto:** caducidad perentoria. Vencido el plazo, el acto queda firme. [CONFIRMADO]

**Diferencia con el régimen federal:** el plazo federal es de 180 días hábiles judiciales. El de San Luis es de 30 días hábiles judiciales. No asumir equivalencia.

**Diferencia con San Juan:** San Juan computa 30 días corridos (acto expreso) y 3 meses (silencio). San Luis computa 30 días hábiles judiciales en ambos casos. No transpolar plazos entre provincias.

### 3.4 Tribunal competente

- **Primera instancia:** Juzgados de Primera Instancia en lo Civil, Comercial y Minas de cada circunscripción judicial (art. 766). [CONFIRMADO]
- **Alzada:** Cámaras de Apelaciones en lo Civil, Comercial, Minas y Laboral. [CONFIRMADO]
- **Recurso extraordinario:** Superior Tribunal de Justicia (STJ) de San Luis. [CONFIRMADO]

### 3.5 Fiscalía de Estado

**Existencia y rango:** existe con raigambre constitucional. Norma fundamental: arts. 235 y ss. de la Constitución de la Provincia de San Luis. Ley orgánica: Ley N° V-0164-2004 (Estructura Orgánica y Funciones de la Fiscalía de Estado). [CONFIRMADO]

**Rol procesal:** el Fiscal de Estado es el defensor legítimo y obligatorio del patrimonio de la Provincia. Es parte necesaria en todos los juicios contencioso-administrativos. [CONFIRMADO]

**Consecuencia de la omisión:** la falta de traslado de la demanda a la Fiscalía de Estado produce nulidad insanable de todo lo actuado, por violación al derecho de defensa en juicio (art. 18 CN). [CONFIRMADO]

**Notificaciones - GIAJ:** la Fiscalía de Estado no recibe traslados por cédula de papel en su domicilio físico (calle Ayacucho). Opera exclusivamente bajo domicilio electrónico institucional bajo el subdominio @giajsanluis.gov.ar, conforme los protocolos del STJ San Luis. [CONFIRMADO]

**Mecánica de traslado en GIAJ:** al interponer la demanda mediante el sistema informático, dar de alta a la Fiscalía de Estado como co-demandada obligatoria. El sistema despliega el casillero de notificación electrónica directamente vinculado al organismo.

**Control de nulidad proactivo:** si la mesa de entradas o el juzgado omiten ordenar el traslado electrónico al casillero de la Fiscalía, solicitarlo expresamente antes de que venzan los plazos de contestación. La omisión de ese traslado electrónico invalida la rebeldía y los plazos posteriores. [CONFIRMADO]

---

## Bloque 4 - Medidas cautelares contra el Estado

### 4.1 Régimen aplicado

San Luis no tiene ley especial de cautelares contra el Estado (no aplica la Ley Nacional 26.854). Se aplican las reglas generales del CPCC provincial (arts. 195 y ss.). [CONFIRMADO]

### 4.2 Suspensión del acto impugnado (art. 769, CPCC)

La interposición de la demanda no suspende la ejecución del acto. Para obtener la suspensión, el art. 769 exige petición de parte y uno de estos dos presupuestos:
- Perjuicios graves o de imposible reparación derivados de la ejecución, o
- Alegación fundada de nulidad absoluta y manifiesta.

Este estándar es autónomo respecto del régimen cautelar general del CPCC. Cuando se pide cautelar de suspensión del acto CA, encuadrar en art. 769 y no en los arts. 195 y ss. [CONFIRMADO]

### 4.3 Ponderación del interés público

La jurisprudencia local exige ponderación rigurosa del interés público comprometido. La medida no debe afectar la continuidad de servicios esenciales ni funciones estatales básicas. Este estándar opera como requisito adicional para la verosimilitud del derecho y el peligro en la demora. [CONFIRMADO]

---

## Bloque 5 - Ejecución de sentencias contra el Estado

### 5.1 Régimen general

Las sentencias condenatorias de dar sumas de dinero tienen carácter declarativo respecto de la percepción inmediata. El Estado provincial debe incluir el crédito judicial en la Ley de Presupuesto del ejercicio del año siguiente. [CONFIRMADO]

### 5.2 Habilitación de la ejecución forzada

Si vencido el ejercicio presupuestario asignado la Administración no ejecuta el pago ni demuestra actividad destinada a cancelarlo, los tribunales civiles habilitan las medidas de ejecución forzosa comunes: embargos sobre bienes del dominio privado del Estado o cuentas comerciales no afectadas a servicios públicos esenciales. [CONFIRMADO]

### 5.3 Tasa de interés en condenas contra el Estado

**Giro jurisprudencial del STJ - doctrina vigente:** el Superior Tribunal de Justicia de San Luis abandonó la doctrina del caso "Fleitas" (que aplicaba tasa pasiva BNA) y modificó su estándar para ajustarse al contexto inflacionario. [CONFIRMADO]

**Tasa aplicable:** Tasa Nominal Anual (TNA) para Préstamos Personales (linea de consumo "Simple") del agente financiero oficial de la provincia. Descartada la tasa pasiva BNA para el cálculo de intereses moratorios judiciales. [CONFIRMADO]

**Efecto retroactivo:** esta tasa se aplica a todos los expedientes en trámite que no cuenten con sentencia firme sobre la cuantificacion del interes. [CONFIRMADO]

**Liquidaciones:** utilizar la calculadora del portal judicial GIAJ configurada bajo este esquema de tasa activa de préstamos. No usar la tasa pasiva histórica. En empleo público y contratos con naturaleza alimentaria, la aplicación de la tasa activa es la regla. [CONFIRMADO]

**Alerta de estrategia:** si existe liquidación practicada en autos bajo la doctrina "Fleitas" (tasa pasiva), impugnar y reliquidar conforme al nuevo estándar antes de la sentencia firme.

---

## Bloque 6 - Amparo local

### 6.1 Normativa aplicable

- **Norma:** Ley N° IV-0087-2004 (Procedimiento de Amparo de la Provincia de San Luis). [CONFIRMADO]

### 6.2 Legitimación

Amplia. Toda persona física o jurídica que invoque lesión, restricción, alteración o amenaza inminente, con arbitrariedad o ilegalidad manifiesta, de derechos reconocidos por la Constitución Nacional, Provincial o Tratados. [CONFIRMADO]

### 6.3 Plazo de interposición

15 días hábiles a partir de la fecha en que el acto se produjo o llegó a conocimiento del afectado (art. 4). El vencimiento opera como caducidad de la vía rápida. [CONFIRMADO]

### 6.4 Estructura procesal y plazos

| Etapa | Plazo | Norma |
|-------|-------|-------|
| Informe circunstanciado de la autoridad (equivalente a contestación) | 5 días (o menos si hay urgencia extrema) | Art. 8 |
| Prueba (si hay hechos controvertidos) | Máximo 5 días improrrogables | - |
| Sentencia | 48 horas de sustanciada la prueba o contestado el informe | Art. 12 |
| Apelación (solo sentencia definitiva y cautelares) | 48 horas de notificada; efecto devolutivo | Art. 15 |

[CONFIRMADO - arts. 4, 8, 12 y 15, Ley N° IV-0087-2004]

### 6.5 Aplicación convencional y constitucional

Los tribunales aplican directamente el art. 43 de la Constitución Nacional y el art. 25 de la Convención Americana sobre Derechos Humanos cuando los plazos o requisitos formales de la ley local pueden frustrar la tutela judicial efectiva. [CONFIRMADO]

### 6.6 Relación con la vía CA ordinaria

Las excepciones al agotamiento de la vía administrativa (vías de hecho, ineficacia manifiesta del carril recursivo, urgencia extrema con daño irreparable) se canalizan por amparo. Verificar siempre si el caso admite amparo antes de encuadrar como CA sumarísima. [CONFIRMADO]

---

## Bloque 7 - Áreas sustantivas

### 7.1 Responsabilidad del Estado provincial

**Marco normativo sustantivo:** San Luis no tiene ley especial de responsabilidad del Estado. Los arts. 1764 a 1766 del CCyCN desplazaron la materia al derecho administrativo local, pero la provincia no sancionó una norma equivalente a la Ley Nacional N° 26.944. No aplicar la ley nacional ni el CCyCN como régimen sustantivo directo. [CONFIRMADO]

**Solución jurisprudencial del STJ:** el Superior Tribunal aplica de forma directa los principios constitucionales de la Carta Magna Provincial (inviolabilidad de derechos fundamentales y de la propiedad) combinados con los presupuestos clásicos de la responsabilidad: daño cierto, relación de causalidad adecuada y factor de atribución. [CONFIRMADO]

**Factor de atribución - falta de servicio:** objetivo. Históricamente anclado en el art. 1112 del Código Civil derogado; hoy reconvertido como principio general del derecho administrativo provincial. El Estado responde objetivamente cuando cumple de manera irregular, tardía o defectuosa las funciones que legalmente le corresponden. [CONFIRMADO]

**Agotamiento de la vía según el origen del daño:**

- Daño derivado de acto administrativo (ej. cesantía ilegal con daños morales y materiales): agotamiento obligatorio de la vía recursiva (art. 767 CPCC) antes de demandar el perjuicio. [CONFIRMADO]
- Daño derivado de hecho administrativo o vía de hecho (ej. accidente de ambulancia oficial, negligencia médica hospitalaria, mal estado de rutas): la doctrina procesal local exime del agotamiento riguroso del recurso jerárquico, pero exige reclamo administrativo previo de indemnización ante el ministerio respectivo como condición de habilitación. Excepción: acción directa accesoria en amparo ante urgencia prestacional (ej. falta de entrega de medicamento vital). [CONFIRMADO]

**El laberinto del art. 768 - estrategia en el escrito de inicio:**

El proceso sumarísimo limita severamente los plazos probatorios. En demandas de responsabilidad estatal (mala praxis médica, accidentes viales, falta de servicio policial) la etapa probatoria es compleja: pericias médicas, mecánicas, contables, testimonial. Presentar el expediente bajo sumarísimo sin solicitar la conversión expone al litigante a caducidades y negligencias procesales en la etapa de prueba.

Regla de redacción obligatoria: en el acápite "Objeto" de toda demanda de daños y perjuicios contra el Estado, solicitar expresamente al juez que, por resolución fundada y atendiendo a la complejidad del asunto, disponga la aplicación de las reglas del proceso ordinario (art. 768, segunda parte, CPCC). Esa solicitud en el escrito de inicio es el único momento procesal idóneo para plantearla. [CONFIRMADO]

### 7.2 Empleo público provincial

**Identificar el estatuto aplicable antes de encuadrar el caso:**

| Sector | Norma |
|--------|-------|
| Administración Central (general) | Ley N° I-0054-2004 (Estatuto del Empleado Público de San Luis). Regula estabilidad, sumarios, licencias y escalafón general. |
| Docente | Ley N° XV-0387-2004 (Estatuto del Docente Provincial). Regula ingreso por concurso, puntajes, juntas de clasificación y régimen disciplinario especial. |
| Policial | Ley N° VII-0167-2004 (Ley del Personal Policial de San Luis), en conjunto con el régimen de la Ley de Personal de Seguridad. |
| Sanitario (Salud Pública) | Ley N° I-0550-2006 (Régimen de la Carrera Sanitaria Provincial). Sistema de dedicación exclusiva ("bloqueo de título") y escalafón propio separado de la administración central. |

[CONFIRMADO]

**Verificar siempre:**
- Situación de revista del agente (planta permanente con estabilidad / sin estabilidad / contratado / transitorio / gabinete).
- Si hubo sumario con garantías de debido proceso conforme al régimen disciplinario del estatuto aplicable.
- Si la sanción expulsiva encuadra en alguna causal taxativa del estatuto aplicable.
- Si el agotamiento de la vía sigue el estatuto general o el régimen del estatuto sectorial.

### 7.3 Contrataciones públicas provinciales

- **Norma:** Ley N° VI-0158-2004 (Ley de Contrataciones de la Provincia de San Luis). [CONFIRMADO]
- **Organismo rector:** Dirección General de Compras y Contrataciones (DGCC), dependiente del Ministerio de Hacienda e Infraestructura Pública. Coordina el sistema de proveedores del Estado y los pliegos únicos de bases y condiciones generales. [CONFIRMADO]
- **Umbrales de procedimiento - sistema de Unidades de Compra (UC):** la Ley N° VI-0158-2004 no fija montos fijos en pesos. Utiliza Unidades de Compra (UC) cuyo valor en pesos es actualizado periódicamente por resoluciones del Ministerio de Hacienda e Infraestructura Pública a propuesta de la DGCC. [CONFIRMADO]

**Regla de cotejo obligatoria para impugnaciones por encuadre de procedimiento:**

1. Tomar el número de expediente administrativo de la contratación cuestionada.
2. Verificar la fecha exacta de emisión del acto de llamado (Decreto de Convocatoria o Disposición).
3. Cruzar esa fecha con la Resolución Ministerial de Hacienda vigente en ese mes exacto para conocer el valor de la UC.
4. Multiplicar ese valor por los topes legales para: Contratación Directa (menor cuantía) / Licitación Privada (cuantía intermedia) / Licitación Pública (tope superior).
5. Comparar el monto del contrato cuestionado contra esos topes calculados a la fecha del llamado.

**Trampa frecuente:** si se alega que una contratación debió ser licitación pública usando valores de UC desactualizados, el Estado gana la excepción demostrando que al valor de la UC del mes del llamado el monto encuadraba legítimamente en un procedimiento menor. Nunca usar montos nominales de ejercicios anteriores. [CONFIRMADO]

---

## Bloque 8 - Organismos de control

### 8.1 Tribunal de Cuentas

- **Norma constitucional:** art. 229 de la Constitución Provincial. [CONFIRMADO]
- **Ley orgánica:** Ley N° V-0163-2004 (Ley Orgánica del Tribunal de Cuentas). [CONFIRMADO]
- **Competencia:** control de legitimidad del gasto público y juicios de cuentas/responsabilidad a funcionarios. Competencia exclusiva en la materia. [CONFIRMADO]

### 8.2 Defensor del Pueblo

No se encuentra operativo ni regulado con efectividad institucional práctica en el orden provincial de San Luis. La figura está en situación de vacancia real como herramienta de reclamo sustantivo, a diferencia de otras provincias argentinas. No invocar como canal de reclamo ni como legitimado procesal activo. [CONFIRMADO]

### 8.3 Fiscalía de Estado

Ver Bloque 3.5. Es parte necesaria en todos los procesos CA. Su omisión produce nulidad insanable.

---

## Bloque 9 - Instrucciones operativas

### Alerta crítica - plazo de caducidad para accionar judicialmente

**Este es el primer paso en toda consulta que involucre una acción judicial contra el Estado provincial de San Luis.**

El plazo para demandar es un plazo de caducidad, no de prescripción:
- No se suspende ni interrumpe por las mismas causales que la prescripción.
- Vencido el plazo, la acción caduca automáticamente; el acto queda firme y consentido.

**Plazo provincial:** 30 días hábiles judiciales (art. 767, CPCC). [CONFIRMADO]
- Acto expreso: desde el día siguiente a la notificación del acto que agota la vía.
- Silencio: desde el día en que queda configurada la denegación tácita (art. 93, LPA: pronto despacho + 30 días hábiles sin resolución).

Antes de analizar cualquier otra cuestión en una consulta sobre acción contenciosa provincial, emitir:

```
[ALERTA PLAZO FATAL: art. 767 CPCC San Luis - 30 días hábiles judiciales desde notificación del acto que agota la vía (acto expreso) o desde configuración de la denegación tácita (silencio: art. 93 LPA - pronto despacho + 30 días hábiles sin resolución) - vencimiento: calcular]
```

**Diferencia con el régimen federal:** el plazo federal es de 180 días hábiles judiciales. El de San Luis es de 30 días hábiles judiciales. No asumir equivalencia.

**Diferencia con San Juan:** San Juan computa 30 días corridos (acto expreso) y 3 meses (silencio). San Luis computa 30 días hábiles judiciales en ambos casos.

### Checklist operativo por tipo de caso

**Impugnación de acto administrativo provincial**

1. Verificar si el acto es de autoridad provincial, municipal o federal.
2. Confirmar que la vía administrativa está agotada (acto definitivo de máxima autoridad o silencio configurado - conf. Bloque 2.3).
3. Calcular el plazo de caducidad de 30 días hábiles judiciales (art. 767).
4. Identificar el juzgado civil competente en la circunscripción correspondiente.
5. Notificar a la Fiscalía de Estado exclusivamente por domicilio electrónico GIAJ (@giajsanluis.gov.ar): darla de alta como co-demandada obligatoria en el sistema al interponer la demanda. La cédula en papel en sede fisica no es el canal valido. Su omision produce nulidad insanable.
6. Evaluar si solicitar conversión a proceso ordinario por complejidad (art. 768).
7. Si se requiere suspensión del acto: encuadrar en art. 769 (perjuicios graves o de imposible reparación / nulidad absoluta y manifiesta alegada fundadamente).

**Medidas cautelares contra el Estado**

1. Suspensión del acto impugnado: art. 769 CPCC (petición de parte + presupuesto legal).
2. Otras cautelares: arts. 195 y ss. CPCC provincial (no Ley Nacional 26.854).
3. Acreditar verosimilitud del derecho y peligro en la demora.
4. Demostrar que la medida no afecta servicios esenciales ni funciones estatales básicas.

**Ejecución de sentencia contra el Estado**

1. Verificar si venció el ejercicio presupuestario asignado sin pago.
2. Si venció sin pago ni actividad de cancelación: habilitar ejecución forzosa sobre bienes del dominio privado o cuentas comerciales no afectadas a servicios esenciales.
3. Para liquidar intereses: aplicar TNA Préstamos Personales del agente financiero oficial provincial (doctrina vigente STJ - reemplaza "Fleitas"). Usar calculadora GIAJ. No aplicar tasa pasiva BNA.

**Amparo**

1. Verificar si el caso encuadra en las excepciones al agotamiento (vías de hecho, urgencia extrema, daño irreparable, ineficacia manifiesta del carril recursivo).
2. Controlar el plazo: 15 días hábiles desde el acto o su conocimiento (art. 4, Ley N° IV-0087-2004). Opera como caducidad.
3. Invocar arts. 43 CN y 25 CADH si los requisitos formales locales frustran la tutela efectiva.

**Empleo público provincial**

1. Identificar el estatuto aplicable al sector (conf. tabla Bloque 7.2).
2. Verificar situación de revista del agente.
3. Verificar si hubo sumario con debido proceso conforme al régimen disciplinario del estatuto sectorial.
4. Verificar si la sanción expulsiva encuadra en causal taxativa del estatuto.
5. Verificar si el agotamiento sigue el estatuto general o el régimen sectorial.

**Actos municipales**

1. Verificar si el municipio tiene carta orgánica propia (San Luis Capital, Villa Mercedes, Merlo y otros). Si la tiene, el agotamiento se rige por la carta orgánica y la Ley N° XII-0349-2004.
2. Los actos directos del intendente u ordenanzas definitivas del concejo deliberante agotan la vía per se.
3. Desde la notificación definitiva: 30 días hábiles judiciales para demandar ante el juzgado civil de la circunscripción correspondiente (art. 767).

### Instrucciones de entrega para escritos provinciales

Todo escrito CA provincial de San Luis cierra con "Estado del escrito" estándar más:
- Fuero y régimen aplicado (Juzgado Civil y Comercial + Ley N° VI-0150-2004, Título IV, arts. 766 a 769).
- Estado del agotamiento de la vía (acto definitivo de máxima autoridad / silencio configurado art. 93 LPA / pendiente).
- Plazo de caducidad provincial: 30 días hábiles judiciales art. 767 (verificado / pendiente / vencido - calcular).
- Intervención de la Fiscalía de Estado: parte necesaria (arts. 235 y ss. CP + Ley N° V-0164-2004) - citada / a citar - omisión: nulidad insanable.
- Tipo de proceso aplicado: sumarísimo (art. 768 regla) / ordinario (art. 768 excepción por resolución fundada).
- Cautelar de suspensión del acto: encuadre en art. 769 / solicitada / no solicitada.
- Alzada: Cámara en lo Civil, Comercial, Minas y Laboral / recurso extraordinario: STJ San Luis.
- Próximo plazo procesal si lo hay.
- Régimen de ejecución: declarativa - presupuesto ejercicio siguiente / excepción por vencimiento sin pago.
- Tasa de interés: TNA Préstamos Personales agente financiero oficial provincial (doctrina STJ vigente - reemplaza "Fleitas"). Calculadora GIAJ. No aplicar tasa pasiva.

---

*Última actualización: Mayo 2025*
*Normativa base: Ley N° VI-0150-2004 (CPCC San Luis, Título IV arts. 766 a 769) - proceso CA; Ley N° VI-0156-2004 (ex Ley N° 5540) - procedimiento administrativo provincial (arts. 84, 90, 92 y 93); Ley N° IV-0087-2004 - amparo local; arts. 235 y ss. Constitución de San Luis + Ley N° V-0164-2004 - Fiscalía de Estado; Ley N° I-0054-2004 - estatuto general del empleado público; Ley N° XV-0387-2004 - estatuto docente; Ley N° VII-0167-2004 - personal policial; Ley N° I-0550-2006 - carrera sanitaria; Ley N° VI-0158-2004 - contrataciones; art. 229 CP + Ley N° V-0163-2004 - Tribunal de Cuentas; Ley N° XII-0349-2004 - régimen municipal; arts. 43 CN y 25 CADH - tutela judicial efectiva y control de convencionalidad.*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
