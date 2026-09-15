# Perfil de práctica · Derecho del consumidor argentino (eje consumidor + acceso a la salud)

> Archivo de configuración para el sistema derecho-argentino.
> Complementa el perfil general (argentina/kb/project/CLAUDE.md) con lógica específica de práctica en derecho del consumidor, con foco en relaciones de consumo de servicios de salud (medicina prepaga y obras sociales como relación de consumo), servicios públicos domiciliarios y sobreendeudamiento.
> **Configuración inicial obligatoria:** completar las variables de la sección siguiente antes de usar.

---

## Configuración inicial - completar antes de usar

**FUERO_HABITUAL:**
Indicar el fuero donde tramitan habitualmente tus causas. Opciones: "Justicia Nacional en las Relaciones de Consumo (CABA)", "fuero civil y comercial federal (CABA)", "fuero contencioso administrativo y tributario CABA (CAyT)", "fuero civil y comercial PBA - [departamento judicial]", "fuero federal civil y comercial del interior", o combinación.

Ejemplo: `FUERO_HABITUAL: Justicia Nacional en las Relaciones de Consumo (CABA) + Civil y Comercial Federal para prepagas`

**Nota operativa de fuero - CABA:** la Justicia Nacional en las Relaciones de Consumo (Ley 26.993) funciona para reclamos de baja cuantía dentro de su tope de competencia. Verificar el monto del tope vigente y si el reclamo lo supera, porque por encima de ese umbral la competencia recae en la justicia ordinaria. Los amparos de salud contra obras sociales nacionales y prepagas tramitan ante el fuero Civil y Comercial Federal, no ante el fuero de consumo. [VERIFICAR VIGENCIA: tope de competencia y estado operativo de la Justicia Nacional en las Relaciones de Consumo]

**Nota operativa PBA:** si se selecciona cualquier fuero dentro de la Provincia de Buenos Aires, indicar obligatoriamente el departamento judicial. El procedimiento administrativo previo (Ley 13.133) y los criterios de cuantificación del daño directo y del daño punitivo varían entre Cámaras departamentales.

**AREAS_PRACTICA:**
Indicar las áreas de mayor volumen (medicina prepaga y obras sociales como relación de consumo, servicios públicos domiciliarios, bancos y entidades financieras, comercio electrónico, sobreendeudamiento, daño punitivo, acciones colectivas, etc.).

Ejemplo: `AREAS_PRACTICA: Prepagas y obras sociales (relación de consumo), servicios públicos domiciliarios, daño punitivo`

---

## Identidad y alcance

Este perfil cubre la práctica en derecho del consumidor argentino con énfasis en su intersección con el derecho a la salud: la relación de consumo entre el usuario y las empresas de medicina prepaga y obras sociales, los servicios públicos domiciliarios esenciales, las operaciones de crédito al consumo y el sobreendeudamiento. El eje protectorio es el mismo que vertebra el perfil de discapacidad: parte estructuralmente débil, asimetría informativa y de poder, e interpretación a favor del consumidor.

El marco normativo es constitucional (art. 42 CN, derechos de consumidores y usuarios), legal de fondo (Ley 24.240 de Defensa del Consumidor y el régimen de contratos de consumo del Código Civil y Comercial, arts. 1092 a 1122) y local (Ley 757 CABA, Ley 13.133 PBA y procedimientos administrativos provinciales y municipales). El sistema opera en la intersección de derecho privado patrimonial, derecho administrativo sancionador y, en el eje de salud, derecho a la salud como derecho humano.

Nexo con el perfil de discapacidad: cuando el reclamo de cobertura involucra a una persona con discapacidad (prestaciones bajo Ley 24.901, CUD), el encuadre primario es el del perfil de discapacidad (amparo de salud, Ley 24.901, CDPCD con jerarquía constitucional). El encuadre consumeril (relación de consumo, trato digno, daño punitivo) opera como refuerzo, no como fundamento principal. No subsumir un reclamo de prestación por discapacidad en la lógica de consumo: la obligación de cobertura integral de la Ley 24.901 tiene una fuente y una intensidad propias.

**FUERO_HABITUAL:** ver sección de configuración inicial
**AREAS_PRACTICA:** ver sección de configuración inicial

---

## Códigos y normativa por fuero

La competencia en materia de consumo depende de la cuantía, del tipo de pretensión (resarcitoria, de cese, colectiva) y de la naturaleza del proveedor demandado.

Fuero | Demandado / materia | Naturaleza de reclamo | Código procesal | Alzada
--- | --- | --- | --- | ---
Justicia Nacional en las Relaciones de Consumo (CABA) | Proveedor en relación de consumo, dentro del tope de competencia | Reclamo individual de baja cuantía | Ley 26.993 + CPCCN supletorio | Cámara de Apelaciones en las Relaciones de Consumo [VERIFICAR VIGENCIA: integración y estado del fuero]
Justicia Nacional en lo Comercial (CABA) | Proveedor en relación de consumo (sociedades, bancos y financieras, aseguradoras, prepagas en lo patrimonial), por encima del tope del fuero de consumo | Daños, nulidad de cláusulas, repetición, daño punitivo | CPCCN (Ley 17.454) | Cámara Nacional de Apelaciones en lo Comercial
Civil y Comercial Federal (CABA) | Obras sociales nacionales (Ley 23.660), empresas de medicina prepaga (Ley 26.682) | Amparo de salud / cobertura | CPCCN (Ley 17.454) | Cámara Nacional Civil y Comercial Federal
Civil y Comercial provincial | Proveedor en relación de consumo, por encima del tope del fuero de consumo local | Daños, nulidad de cláusulas, repetición, daño punitivo | CPCCBA u otro código provincial | Cámara respectiva por departamento judicial
CAyT CABA | Dirección General de Defensa y Protección al Consumidor (GCBA) | Impugnación de sanción administrativa (Ley 757) | CCAyT (Ley 189 CABA) | Cámara CAyT
Civil y Comercial PBA | OMIC municipal / autoridad provincial, o proveedor demandado | Impugnación de resolución administrativa (Ley 13.133) o demanda de daños | CPCCBA (Ley 7425) | Cámara de Apelación Civil y Comercial por departamento judicial

### Regla general

El sistema identifica el fuero al inicio de cada consulta. La competencia consumeril no es única: depende de la cuantía, de si se demanda al proveedor (acción resarcitoria) o se impugna una sanción administrativa (acción contencioso-administrativa), y de la jurisdicción. Si la consulta no especifica fuero, cuantía y tipo de pretensión, preguntar antes de analizar.

### Regla especial - mudanza competencial en CABA

En el ámbito nacional/CABA conviven varios foros y el reparto está en transición. Precisión a junio de 2026: el convenio de traspaso del fuero nacional de consumo (Ley 26.993) a la Ciudad fue ratificado solo por la Legislatura porteña, no por el Congreso. Mientras tanto, CABA sancionó la Ley 6286, que atribuyó la materia de consumo al fuero Contencioso Administrativo, Tributario y de Relaciones de Consumo (CAyTyC) a través de juzgados que aplican el Código Procesal de la Justicia en las Relaciones de Consumo de la CABA, con competencia sobre las causas iniciadas a partir de su puesta en funcionamiento. En paralelo, en el ámbito nacional el consumo que excede la baja cuantía se litiga de forma masiva ante la Justicia Nacional en lo Comercial. El solapamiento genera conflictos de competencia positivos y negativos.

Regla operativa: antes de definir radicación de cualquier demanda de consumo en CABA, consultar el estado actual de la mudanza competencial y el criterio vigente de atribución entre la Justicia Nacional en lo Comercial, la Justicia Nacional en las Relaciones de Consumo (Ley 26.993) y el fuero CAyTyC porteño (Ley 6286). No asumir que la competencia sigue el esquema anterior.
```
[VERIFICAR VIGENCIA: estado del traspaso del fuero de consumo a la Ciudad, alcance de la Ley 6286 CABA y criterio de atribución frente a la Justicia Nacional en lo Comercial]
```
```
[VERIFICAR VIGENCIA: estado del traspaso de competencias de consumo a la Justicia de la Ciudad (CAyTyC) y criterio de atribución frente a la Justicia Nacional en lo Comercial y la Justicia Nacional en las Relaciones de Consumo]
```

### Regla especial - salud como relación de consumo

El contrato de medicina prepaga es, a la vez, contrato de consumo (Ley 24.240 + CCyC) y contrato regido por la Ley 26.682. La doble fuente habilita dos vías que conviene articular y no confundir:

- Para exigir cobertura inmediata o frenar una baja, una exclusión o un aumento abusivo: amparo de salud ante el fuero Civil y Comercial Federal, con fundamento principal en la Ley 26.682 y, si hay discapacidad, en la Ley 24.901 y la CDPCD. El encuadre consumeril (trato digno, cláusula abusiva) refuerza.
- Para el reclamo resarcitorio por el daño ya causado (incluido daño punitivo del art. 52 bis LDC): acción ordinaria por relación de consumo.

No tramitar un aumento abusivo de cuota o una negativa de cobertura urgente como simple reclamo de consumo de baja cuantía: la urgencia exige la vía del amparo.

---

## Alerta normativa - normas de vigencia variable

*Última verificación de esta sección: junio 2026. Actualizar cuando cambie alguna de las normas listadas.*

### DNU 70/2023 - desregulación e impacto sobre el régimen del consumidor

El DNU 70/2023 (B.O. 21/12/2023, vigencia 30/12/2023) introdujo una desregulación amplia con impacto directo en relaciones de consumo, en especial en medicina prepaga (liberación de cuotas y retroceso de las facultades de control de la autoridad de aplicación de la Ley 26.682) y en materia contractual. Estado a junio de 2026: el DNU sigue vigente; el Senado lo rechazó, pero la Cámara de Diputados no lo trató, y un DNU solo cae si ambas cámaras lo rechazan (art. 24 Ley 26.122). Verificar el estado parlamentario y judicial al momento de cada consulta.

```
[VERIFICAR VIGENCIA: DNU 70/2023 - estado parlamentario y judicial, e impacto vigente sobre Ley 26.682 (cuotas de prepaga) y sobre la Ley 24.240]
```

**Doctrina de aprovechamiento - aumentos de prepaga aún bajo DNU 70/23:** la liberación de cuotas no convierte en lícito cualquier aumento. La jurisprudencia ha calificado de abusivos, en los términos de la Ley 24.240, del art. 1122 CCyC y del art. 10 CCyC (ejercicio abusivo del derecho), aumentos desproporcionados de la cuota de medicina prepaga aun estando vigente el DNU 70/23, y ha ordenado en cautelar retrotraer el aumento a una pauta objetiva (v.gr. la variación del IPC). El argumento a usar: la desregulación tarifaria es de carácter comercial y no desplaza el control de abusividad, el deber de trato digno ni la veda del ejercicio abusivo del derecho; el aumento que altera de forma irrazonable la ecuación del contrato sigue siendo revisable judicialmente.
Fallos verificados:
- Precedente de alzada (CABA): Cámara Nacional de Apelaciones en lo Civil y Comercial Federal, Sala II, "Cainelli, Elsa Angélica c/ OMINT S.A. de Servicios s/ amparo sumarísimo valor cuota emp. - DNU 70/23" (CCF 4145/2024, 20/05/2025, jueces Nallar y Gottardi), que declaró la inconstitucionalidad de los arts. 267 y 269 del DNU 70/23, reputó ilegítimos los aumentos aplicados desde diciembre de 2023 y devolvió a la Superintendencia de Servicios de Salud el control de las cuotas.
- Ejemplo cautelar: Juzgado Federal de Concepción del Uruguay N° 2, "Morsentti, Fernando Ismael c/ OSDE s/ Amparo Ley 16.986" (causa 1461/2024, 13/03/2024), que dejó sin efecto el aumento bajo el DNU 70/23, retrotrajo la cuota a diciembre de 2023 y la ató al IPC del INDEC.

El grueso de estas causas se concentra en el fuero Civil y Comercial Federal (CABA). Verificar el texto íntegro de cada fallo antes de transcribir considerandos.

### Disolución del COPREC y nueva Ventanilla Única Federal de Reclamos

El COPREC (Servicio de Conciliación Previa en las Relaciones de Consumo, Ley 26.993) fue disuelto. Su reemplazo es la Ventanilla Única Federal de Reclamos de Defensa del Consumidor. No citar el COPREC como instancia conciliatoria previa vigente. Verificar el procedimiento, los plazos y el carácter (obligatorio o no) de la instancia conciliatoria actual antes de planificar el reclamo.
```
[VERIFICAR VIGENCIA: disolución del COPREC (Decreto 55/2025) y régimen de la Ventanilla Única Federal de Reclamos (Disposición 890/2025) - procedimiento, plazos y obligatoriedad de la conciliación previa]
```

**Impacto operativo - distinguir el plano nacional del local:** la disolución del COPREC operó en el plano nacional, pero no eliminó la instancia previa en las jurisdicciones locales. En CABA y en PBA la conciliación o mediación prejudicial (pública o privada) sigue siendo recaudo de admisibilidad antes de promover la demanda ordinaria de daños de consumo; su omisión expone a la inadmisibilidad o a la excepción de falta de cumplimiento de la instancia previa. No leer la caída del COPREC como una supresión general del requisito conciliatorio.

Regla operativa: definir, según la jurisdicción del consumidor, qué instancia previa corresponde y si es obligatoria: Ventanilla Única Federal en el plano nacional; conciliación o mediación prejudicial local en CABA y PBA; autoridad local de defensa del consumidor (OMIC, dirección provincial). Verificar el régimen vigente antes de planificar el reclamo.
```
[VERIFICAR VIGENCIA: carácter obligatorio de la conciliación o mediación prejudicial de consumo en CABA y en PBA como recaudo de admisibilidad de la demanda ordinaria de daños - normas locales vigentes]
```

### Daño punitivo (art. 52 bis Ley 24.240) - texto vigente y tope móvil en CBT

El art. 52 bis conserva el texto de la Ley 26.361: multa civil a favor del consumidor, graduada por la gravedad del hecho, con tope en el máximo de la sanción de multa del art. 47 inc. b de la Ley 24.240. Lo que cambió es la unidad del tope, y esto es determinante para cuantificar.

El tope nominal histórico de $5.000.000 está derogado. La Ley 27.701 (Presupuesto 2023, B.O. 01/12/2022), art. 119, sustituyó el art. 47 inc. b y reemplazó el monto fijo por una banda expresada en Canastas Básicas Totales para el Hogar (CBT) que publica el INDEC: de 0,5 a 2.100 CBT tipo 3. Como el art. 52 bis remite al art. 47, el tope del daño punitivo quedó atado a esa unidad móvil y se actualiza con la inflación.

Regla operativa de cuantificación: NO usar el valor nominal de $5.000.000 ni montos fijos de leyes desactualizadas. Calcular el tope como 2.100 CBT tipo 3 del INDEC vigentes a la fecha de la demanda. El marcador de verificación recae únicamente sobre el valor de la CBT al momento de cuantificar, no sobre la fórmula.

Orientación de magnitud (a mayo de 2026, dato que se actualiza todos los meses): la CBT del hogar tipo 3 del INDEC rondaba $1.500.000, de modo que el tope máximo de 2.100 CBT se ubicaba en el orden de los $3.150 millones. Es un techo, no un piso: la multa se gradúa por la gravedad del hecho. Recalcular siempre con la CBT del mes de la demanda.
```
[VERIFICAR VIGENCIA: valor de la Canasta Básica Total (CBT) tipo 3 del INDEC vigente a la fecha de la demanda, para liquidar el tope de 2.100 CBT del art. 47 inc. b Ley 24.240 (texto Ley 27.701)]
```

### Garantía legal de productos (art. 11 Ley 24.240)

Verificar el plazo de garantía legal vigente (texto histórico: tres meses para cosas muebles usadas y seis meses en los demás casos, desde la entrega; las partes pueden pactar plazo mayor). Antes de citar el plazo, confirmar que no haya sido modificado.
```
[VERIFICAR VIGENCIA: art. 11 Ley 24.240 - plazos de garantía legal vigentes]
```

### Operaciones de crédito al consumo (art. 36 Ley 24.240) y desregulación financiera

El art. 36 exige información financiera completa (TEA, costo financiero total, cantidad y monto de cuotas) bajo sanción de nulidad. La desregulación financiera de 2024-2026 modificó facultades de organismos de control; verificar que las exigencias informativas del art. 36 y la competencia para fijar la jurisdicción del consumidor (domicilio del consumidor, regla de orden público) sigan vigentes y no hayan sido alteradas por norma posterior.
```
[VERIFICAR VIGENCIA: art. 36 Ley 24.240 - deberes de información financiera y regla de competencia en favor del domicilio del consumidor]
```

### Servicios públicos domiciliarios (arts. 25 a 31 Ley 24.240)

Los regímenes tarifarios y los entes reguladores de energía, gas, agua y telecomunicaciones fueron objeto de reestructuración en 2024-2026. No invocar un régimen tarifario, un tope ni una facultad de un ente regulador sin verificar su vigencia. El derecho del usuario a la información, a la continuidad del servicio, a la reciprocidad de trato y al reintegro por error de facturación (art. 31) se mantiene como piso legal.
```
[VERIFICAR VIGENCIA: estructura de entes reguladores y regímenes tarifarios de servicios públicos domiciliarios - estado al momento de la consulta]
```

### Beneficio de justicia gratuita (art. 53 Ley 24.240)

El art. 53 establece el beneficio de gratuidad para el consumidor que inicia la acción. Su alcance (si cubre solo la tasa de justicia o también las costas) ha sido objeto de interpretación jurisprudencial divergente. Verificar el criterio de la sala o fuero actuante antes de afirmar que el consumidor está eximido de costas en caso de derrota.
```
[VERIFICAR VIGENCIA: alcance del beneficio de gratuidad del art. 53 Ley 24.240 - doctrina de la sala o fuero actuante sobre cobertura de costas]
```

### Procedimientos locales

- **CABA - Ley 757:** procedimiento administrativo de defensa del consumidor ante la Dirección General de Defensa y Protección al Consumidor. Verificar montos de multa y reglas de impugnación judicial vigentes. [VERIFICAR VIGENCIA: Ley 757 CABA - escala sancionatoria y procedimiento]
- **PBA - Ley 13.133 (Código Provincial de Implementación de los Derechos de los Consumidores y Usuarios):** procedimiento ante OMIC municipales y autoridad provincial. Verificar competencia municipal/provincial y régimen de impugnación. [VERIFICAR VIGENCIA: Ley 13.133 PBA - procedimiento y autoridad de aplicación]

---

## Normativa de referencia

### Fundamento constitucional

- **Art. 42 CN:** derechos de consumidores y usuarios a la protección de la salud, seguridad e intereses económicos; a información adecuada y veraz; a la libertad de elección; a condiciones de trato equitativo y digno. Manda a las autoridades a proveer la defensa de la competencia y el control de los monopolios naturales y legales.
- **Art. 43 CN:** acción de amparo, incluida la vía colectiva para la protección de derechos de incidencia colectiva (consumidores y usuarios).

### Régimen de fondo

- **Ley 24.240 (Defensa del Consumidor, LDC):** ley base. Modificada por Ley 26.361, Ley 26.994 (sanción del CCyC) y DNU 70/2023, entre otras. Artículos clave:
  - Art. 1 y 2: relación de consumo, consumidor y proveedor.
  - Art. 4: deber de información.
  - Art. 8 bis: trato digno; prohibición de prácticas vergonzantes, vejatorias o intimidatorias.
  - Arts. 10 a 11 y 14 a 16: garantía legal de productos.
  - Arts. 25 a 31: servicios públicos domiciliarios.
  - Arts. 32 a 34: venta domiciliaria, por correspondencia y a distancia; derecho de revocación.
  - Art. 36: operaciones de crédito; nulidad por falta de información financiera; competencia en favor del consumidor.
  - Art. 37: cláusulas abusivas; interpretación contra el predisponente.
  - Art. 40: responsabilidad solidaria de toda la cadena por el daño al consumidor; eximición solo por causa ajena.
  - Art. 47: escala de sanciones administrativas; tope de multa expresado en Canastas Básicas Totales del INDEC (0,5 a 2.100 CBT, texto Ley 27.701).
  - Art. 50: prescripción de las sanciones administrativas (tres años). No regula la prescripción de la acción civil del consumidor.
  - Art. 52: acciones judiciales.
  - Art. 52 bis: daño punitivo (multa civil), con tope del art. 47 inc. b.
  - Art. 53: beneficio de justicia gratuita.
  - Art. 54: acciones colectivas; cosa juzgada con efecto expansivo.
- **Código Civil y Comercial - contratos de consumo (arts. 1092 a 1122):**
  - Arts. 1092-1093: relación y contrato de consumo.
  - Art. 1094: interpretación y prelación normativa a favor del consumidor (principio in dubio pro consumidor).
  - Art. 1095: interpretación del contrato en el sentido más favorable al consumidor.
  - Arts. 1096-1099: prácticas abusivas; trato digno; trato equitativo y no discriminatorio; libertad de contratar.
  - Arts. 1100-1103: información y publicidad.
  - Arts. 1117-1122: cláusulas abusivas y su control judicial.
- **Ley 26.682 (Medicina prepaga):** marco regulatorio de las empresas de medicina prepaga; obligación de cobertura del PMO y de las prestaciones de la Ley 24.901; control de la autoridad de aplicación sobre cuotas y planes. Impactada por el DNU 70/2023. [VERIFICAR VIGENCIA]
- **Ley 23.660 / 23.661 (Obras sociales y sistema nacional del seguro de salud):** marco del sistema de obras sociales; base de la obligación de cobertura.
- **Ley 26.993 (Sistema de resolución de conflictos en las relaciones de consumo):** creó el COPREC (disuelto), la auditoría en las relaciones de consumo y la Justicia Nacional en las Relaciones de Consumo. Verificar qué institutos siguen vigentes tras la disolución del COPREC. [VERIFICAR VIGENCIA]
- **DNU 274/2019 (Lealtad comercial):** sustituyó la Ley 22.802. Publicidad engañosa, publicidad comparativa y prácticas comerciales. [VERIFICAR VIGENCIA]
- **Ley 18.829 (agentes de viaje) y Ley 25.997 (Ley Nacional de Turismo):** responsabilidad en la contratación de servicios turísticos, complementarias de la LDC. [VERIFICAR VIGENCIA]
- **Ley 17.418 (Seguros):** la prescripción anual del art. 58 cede ante el plazo quinquenal del CCyC (art. 2560) cuando media relación de consumo. [VERIFICAR VIGENCIA]

### Acciones colectivas

- **Art. 43 CN + art. 54 Ley 24.240:** base de la legitimación colectiva del consumidor y de las asociaciones.
- **Registro Público de Procesos Colectivos (CSJN):** inscripción obligatoria del proceso colectivo para evitar superposición y litispendencia. Verificar la acordada vigente y el procedimiento de inscripción. [VERIFICAR VIGENCIA: reglamento del Registro Público de Procesos Colectivos de la CSJN]
- Doctrina de legitimación colectiva (verificada en SAIJ y fuentes oficiales): CSJN, "Halabi, Ernesto C. c/ P.E.N.", Fallos 332:111 (24/02/2009), que fija las tres categorías de derechos y habilita la acción de clase para intereses individuales homogéneos; y CSJN, "PADEC c/ Swiss Medical S.A. s/ nulidad de cláusulas contractuales", P.361.XLIII, Fallos 336:1236 (21/08/2013), que reconoce la legitimación de las asociaciones de consumidores para impugnar de forma colectiva la cláusula que autoriza la modificación unilateral de la cuota de la prepaga. Verificar el texto íntegro antes de transcribir considerandos.

### Normativa local

- **CABA - Ley 757:** procedimiento administrativo de defensa del consumidor. Autoridad: Dirección General de Defensa y Protección al Consumidor (GCBA). [VERIFICAR VIGENCIA]
- **CABA - Justicia Nacional en las Relaciones de Consumo (Ley 26.993):** fuero para reclamos individuales de baja cuantía. [VERIFICAR VIGENCIA: estado e integración]
- **PBA - Ley 13.133:** Código Provincial de Implementación de los Derechos de los Consumidores y Usuarios. OMIC municipales y autoridad provincial. [VERIFICAR VIGENCIA]

### Fuentes primarias de consulta

- **Infoleg (infoleg.gob.ar):** texto oficial de leyes y decretos nacionales.
- **Defensa del Consumidor - Nación (argentina.gob.ar/defensadelconsumidor):** Ventanilla Única Federal, normativa y disposiciones.
- **BOCBA (boletinoficial.buenosaires.gob.ar):** normativa CABA.
- **BOPBA (gob.gba.gov.ar):** normativa PBA.
- **CSJN (csjn.gov.ar) y Registro Público de Procesos Colectivos:** jurisprudencia y registro de colectivos.
- **SCBA (scba.gov.ar):** jurisprudencia PBA.

---

## Institutos frecuentes y lógica de diagnóstico

### Encuadre inicial - ¿es relación de consumo?

Antes de cualquier análisis, verificar:

1. ¿Hay relación de consumo (art. 1 LDC, art. 1092 CCyC): destinatario final, persona humana o jurídica, que adquiere o usa bienes o servicios como consumidor o usuario?
2. ¿El demandado es proveedor profesional (art. 2 LDC)?
3. ¿Qué pretensión persigue el cliente: cese de una conducta, cobertura o prestación, restitución de sumas, o resarcimiento (con o sin daño punitivo)?
4. ¿La cuantía y la urgencia determinan la vía (administrativa, judicial de consumo, amparo, ordinaria)?

Si el cliente es una persona con discapacidad y reclama una prestación bajo Ley 24.901, derivar el encuadre principal al perfil de discapacidad y usar el consumeril como refuerzo.

### Aumento abusivo o baja de cobertura de medicina prepaga

Vía y diagnóstico:

1. ¿Hay urgencia (baja del servicio, exclusión de afiliado, corte de una prestación en curso)? Si la hay, la vía es el amparo de salud ante el fuero Civil y Comercial Federal, con cautelar de mantenimiento del servicio. El reclamo de consumo de baja cuantía no es la vía para una urgencia.
2. ¿El aumento altera de forma irrazonable la ecuación del contrato? Aun bajo el DNU 70/23, el aumento desproporcionado es revisable por abusividad (art. 1122 CCyC, art. 8 bis y 37 LDC) y por ejercicio abusivo del derecho (art. 10 CCyC); la cautelar puede pedir retrotraer el aumento a una pauta objetiva como el IPC.
3. ¿Hubo trato indigno (información engañosa, maltrato, traba burocrática para dar de baja un aumento)? Activa el art. 8 bis LDC y los arts. 1097-1098 CCyC, base del daño punitivo.
4. ¿El afiliado es adulto mayor o persona con discapacidad? Refuerza la tutela y agrava la conducta del proveedor a los fines del art. 52 bis.

**Instrucción operativa - prueba del contrato y del aumento:** requerir al cliente el contrato o plan, los últimos cupones o liquidaciones de cuota, la comunicación del aumento o de la baja y toda constancia de reclamo previo. Sin la secuencia documentada del aumento y del reclamo, la verosimilitud para la cautelar y la base del daño punitivo se debilitan.

### Daño punitivo (art. 52 bis LDC)

Verificar antes de incluirlo en la demanda:

1. **Conducta cualificada:** la jurisprudencia mayoritaria exige algo más que el mero incumplimiento: un factor de atribución calificado -menosprecio por los derechos del consumidor, grave indiferencia, o aprovechamiento de su situación-. Acreditar la conducta, no solo el daño. Leading case verificado: Cámara de Apelaciones en lo Civil y Comercial de Mar del Plata, Sala II, "Machinandiarena Hernández, Nicolás c/ Telefónica de Argentina S.A. s/ reclamo contra actos de particulares" (27/05/2009), primera aplicación del daño punitivo del art. 52 bis, en un caso de barreras de accesibilidad para una persona con movilidad reducida (nexo con el eje de discapacidad). Verificar el texto íntegro antes de transcribir.
2. **Trato indigno o práctica abusiva:** documentar la secuencia (reclamos sin respuesta, derivaciones, información falsa, demoras deliberadas). Es el sustrato fáctico del daño punitivo.
3. **Graduación y tope:** la multa se gradúa por la gravedad del hecho y demás circunstancias, con tope en el art. 47 inc. b. El tope es móvil: 2.100 CBT tipo 3 del INDEC (texto Ley 27.701), no el viejo monto fijo de $5.000.000. Liquidar con el valor de la CBT vigente a la fecha de la demanda.
4. **Solidaridad:** si más de un proveedor incumplió, responden solidariamente (art. 52 bis, segundo párrafo, y art. 40 LDC).

```
[VERIFICAR VIGENCIA: valor de la CBT tipo 3 del INDEC a la fecha de la demanda, para liquidar el tope de 2.100 CBT del art. 47 inc. b Ley 24.240]
```

### Cláusulas abusivas

1. Identificar la cláusula y subsumirla en el art. 37 LDC y/o en los arts. 1117-1122 CCyC (desnaturalización de obligaciones, renuncia o restricción de derechos, inversión de la carga de la prueba).
2. La declaración de nulidad es parcial: se tiene por no escrita la cláusula y el contrato subsiste (art. 37, último párrafo, LDC; art. 1122 CCyC).
3. En servicios de salud: las cláusulas de exclusión de cobertura por enfermedad preexistente, carencias prolongadas o caducidades automáticas son terreno habitual de control. Confrontar con la Ley 26.682.

### Servicios públicos domiciliarios

1. **Error de facturación (art. 31 LDC):** ante facturación en exceso ya pagada, el usuario tiene derecho a la devolución con un recargo legal. Verificar el régimen vigente del recargo antes de cuantificar.
2. **Continuidad y reciprocidad de trato:** el usuario no puede ser tratado peor que el prestador en mora; la suspensión del servicio esencial exige procedimiento y aviso.
3. **Reclamo ante el ente regulador:** verificar si existe instancia administrativa previa ante el ente del sector y si es presupuesto de la acción judicial.
```
[VERIFICAR VIGENCIA: régimen del recargo por error de facturación (art. 31 LDC) y entes reguladores sectoriales]
```

### Operaciones de crédito y sobreendeudamiento

1. **Información financiera (art. 36 LDC):** la omisión de TEA, costo financiero total o detalle de cuotas acarrea nulidad de la cláusula y puede habilitar la recomposición del crédito. Verificar el contrato y la documentación precontractual.
2. **Competencia en favor del consumidor (art. 36, último párrafo):** la regla de orden público fija la competencia en el domicilio real del consumidor y anula la prórroga en su contra. Es defensa habitual frente a ejecuciones en jurisdicción ajena.
3. **Anatocismo y cláusulas abusivas de intereses:** confrontar las tasas y la capitalización con los arts. 1117-1122 CCyC.
4. Sobreendeudamiento: no existe en el orden nacional un régimen general de insolvencia de la persona consumidora equivalente al de otros países; la herramienta es la revisión contractual y, en su caso, el concurso preventivo de persona humana. [REVISIÓN NORMATIVA REQUERIDA: vías disponibles para el sobreendeudamiento del consumidor según jurisdicción]

### Comercio electrónico y venta a distancia

1. **Derecho de revocación (arts. 32-34 LDC):** plazo de diez días corridos desde la entrega o la celebración, sin expresión de causa, sin costo. Verificar el deber de informar este derecho de forma destacada; su omisión amplía el plazo.
2. **Deber de información y constancia de la operación (art. 4 y arts. 1100 ss. CCyC).**

### Garantía legal y vicios de productos

Régimen propio del consumo, distinto de los vicios redhibitorios del CCyC. Verificar antes de plantear:

1. **Garantía legal (arts. 10 a 11 LDC):** cubre defectos o vicios de cosas muebles no consumibles, aun ostensibles, que afecten la identidad entre lo ofrecido y lo entregado o su correcto funcionamiento. Plazos (texto histórico): 3 meses para usados y 6 meses en los demás casos desde la entrega; las partes pueden pactar plazo mayor. [VERIFICAR VIGENCIA: plazos del art. 11.]
2. **Cadena de responsables (art. 13):** productor, importador, distribuidor y vendedor responden solidariamente por la garantía.
3. **Prolongación del plazo (art. 16):** el tiempo de privación de uso por reparación se suma al plazo de garantía.
4. **Reparación no satisfactoria (art. 17):** si la reparación no devuelve la cosa a condiciones óptimas, el consumidor puede optar por (a) sustitución por otra de idénticas características, (b) devolución del precio pagado, o (c) quita proporcional del precio. Es una opción del consumidor, no del proveedor.
5. **Vicios redhibitorios (CCyC arts. 1051 a 1058):** vía concurrente para defectos ocultos; confrontar plazos de caducidad y prescripción con el régimen de la LDC y optar por el más favorable al consumidor (art. 1094 CCyC).

Regla operativa: identificar primero si el reclamo encuadra en la garantía legal de la LDC (más favorable, con cadena solidaria) antes de ir a los vicios redhibitorios del CCyC. No confundir la garantía legal con la garantía contractual o comercial extendida.

### Oferta, publicidad y prácticas comerciales (lealtad comercial)

1. **Oferta y publicidad vinculantes (arts. 7 a 8 LDC):** las precisiones de la publicidad o el anuncio integran el contrato y obligan al proveedor. La negativa a cumplir la oferta publicada es resistible.
2. **Publicidad engañosa y comparativa (DNU 274/2019, lealtad comercial):** el DNU 274/2019 derogó la Ley 22.802 y rige hoy el régimen de lealtad comercial; prohíbe la publicidad que por inexactitud u ocultamiento induzca a error, y regula la comparativa. [VERIFICAR VIGENCIA: DNU 274/2019 y su estado parlamentario.]
3. **Prácticas comerciales abusivas (arts. 1096 a 1099 CCyC; art. 8 bis LDC):** trato digno, no discriminación, libertad de contratar; prohibición de prácticas que limiten la libertad de elección (ventas atadas, condicionamientos).
4. **Información cierta y detallada (art. 4 LDC):** estándar transversal; su incumplimiento alimenta la nulidad, el daño y el daño punitivo.

### Trato digno y cobranzas extrajudiciales abusivas

1. **Trato digno (art. 8 bis LDC; arts. 1097-1098 CCyC):** prohibición de prácticas vergonzantes, vejatorias o intimidatorias. La gestión de cobranza con hostigamiento, llamados a horarios indebidos, comunicación a terceros o amenazas configura trato indigno.
2. **Consecuencia:** el trato indigno es fuente autónoma de daño moral y sustrato del daño punitivo (art. 52 bis), con independencia de que la deuda exista.
3. Documentar la secuencia (registros de llamados, mensajes, testigos) como prueba de la conducta.

### Daño directo (art. 40 bis LDC)

La autoridad administrativa de aplicación puede fijar un resarcimiento del daño directo efectivamente sufrido por el consumidor, dentro de los límites y con los recaudos del art. 40 bis. Verificar el alcance vigente y el tope, y su articulación con la reparación judicial plena (el daño directo administrativo no agota el reclamo judicial por el resto del daño). [VERIFICAR VIGENCIA: art. 40 bis LDC - alcance y límites del daño directo.]

### Verticales de alto volumen - red flags

Sin desarrollo exhaustivo; checklist de entrada por rubro. En todos rige la LDC y el CCyC de consumo como piso.

- **Automotores (0 km y usados):** vicios de fábrica y garantía del fabricante; planes de ahorro previo (control de la IGJ y de la autoridad de aplicación; reajuste de cuota y valor móvil; resolución por imposibilidad de pago). Verificar normativa específica de planes de ahorro. [VERIFICAR VIGENCIA: régimen de planes de ahorro/círculos cerrados.]
- **Turismo y viajes:** responsabilidad de la agencia por el incumplimiento del paquete; marco de la Ley 18.829 (agentes de viaje) y Ley 25.997 (turismo), más la LDC. [VERIFICAR VIGENCIA: Ley 18.829 y Ley 25.997.] Cancelaciones, sobreventa, información del prestador.
- **Telecomunicaciones (telefonía, internet, TV paga):** facturación, baja del servicio (debe ser tan simple como el alta), continuidad, portabilidad; control del ENACOM. [VERIFICAR VIGENCIA: facultades del ENACOM y régimen del sector.]
- **Bancos, financieras y seguros:** información financiera (art. 36 LDC); cargos y comisiones; en seguros, la prescripción del reclamo del consumidor se rige por el plazo más favorable del CCyC (5 años, art. 2560), no por el año del art. 58 de la Ley 17.418, cuando media relación de consumo. [VERIFICAR VIGENCIA: criterio de prescripción quinquenal en seguros de consumo.]

### Acción colectiva de consumo

1. **Legitimación:** asociación de consumidores registrada, autoridad de aplicación o Ministerio Público (art. 54 LDC, art. 43 CN).
2. **Inscripción en el Registro Público de Procesos Colectivos** antes o al inicio, para evitar litispendencia con otro colectivo. Verificar la acordada vigente.
3. **Definición de la clase y del hecho único o continuado** que justifica el tratamiento colectivo.
4. **Cosa juzgada expansiva (art. 54, segundo párrafo, LDC):** la sentencia hace cosa juzgada para todos los consumidores, salvo los que se excluyan.

### Prescripción

No hay un plazo único. La regla varía según el tipo de pretensión:

Tipo de pretensión | Plazo | Observación
--- | --- | ---
Sanción administrativa (procedimiento de defensa del consumidor) | 3 años (art. 50 LDC) | Se interrumpe por nuevas infracciones o por el inicio de actuaciones administrativas
Acción del consumidor por daños derivados de la relación de consumo contractual | 5 años (art. 2560 CCyC) | Plazo genérico; criterio dominante por aplicación de la norma más favorable al consumidor (art. 1094 CCyC). El art. 50 LDC, tras la Ley 26.994, ya no rige la acción civil. Es el plazo a usar por defecto
Daños de fuente extracontractual (accidente, producto elaborado sin vínculo contractual) | 3 años (art. 2561 CCyC) | Deslinde por la fuente del daño: si no hay relación contractual de consumo, rige la prescripción de la responsabilidad civil
Garantía legal de productos (LDC arts. 11 y 17) | Plazo de garantía 3 meses (usados) / 6 meses (resto) para reclamar el defecto; la acción de daños prescribe a 5 años (art. 2560 CCyC) | No confundir el plazo de la garantía con el de prescripción de la acción. [VERIFICAR plazos del art. 11]
Vicios redhibitorios (CCyC arts. 1054-1058) | Caducidad y prescripción propias del CCyC | Vía concurrente; optar por el régimen más favorable al consumidor (art. 1094)
Seguros en relación de consumo | 5 años (art. 2560 CCyC) | Desplaza el plazo anual del art. 58 Ley 17.418 cuando media relación de consumo
Servicios públicos - repetición por error de facturación | Verificar | Según naturaleza del reclamo

**Regla operativa:** por defecto, la acción de daños del consumidor en relación de consumo contractual prescribe a los 5 años (art. 2560 CCyC). Tomar el art. 50 LDC (3 años) como plazo de esa acción es un error frecuente posterior a la reforma de 2015: ese artículo rige hoy solo las sanciones administrativas. El único deslinde a hacer antes de aplicar los 5 años es por la fuente del daño: si el reclamo es de fuente extracontractual pura (accidente, producto elaborado sin vínculo contractual), rige el art. 2561 CCyC (3 años). Alertar siempre sobre el plazo aplicable y la fecha de inicio del cómputo antes de analizar el fondo.

---

## Procesos especiales

### Reclamo administrativo de defensa del consumidor

- Vía: Ventanilla Única Federal de Reclamos o autoridad local (CABA Ley 757, PBA Ley 13.133, OMIC municipal), según jurisdicción del consumidor.
- Etapa conciliatoria y, si fracasa, instrucción del sumario y resolución sancionatoria con eventual fijación de daño directo a favor del consumidor.
- Verificar el carácter (obligatorio o facultativo) de la instancia conciliatoria tras la disolución del COPREC.
- La resolución sancionatoria se impugna por vía judicial: en CABA, ante el fuero CAyT; en PBA, ante el fuero civil y comercial conforme Ley 13.133.

### Acción judicial individual de consumo

- Para reclamo resarcitorio (daños, restitución, daño punitivo) o de cese.
- Determinar fuero por cuantía: Justicia Nacional en las Relaciones de Consumo dentro de su tope; por encima, justicia ordinaria.
- Petitorio: incluir, según el caso, restitución, indemnización de daños, daño punitivo (art. 52 bis), nulidad de cláusulas abusivas, y costas a la demandada.
- Invocar el beneficio de gratuidad del art. 53 LDC al inicio.

### Amparo de salud por relación de consumo (prepaga / obra social)

- Vía para urgencias: baja de afiliación, exclusión de cobertura, aumento confiscatorio que pone en riesgo la continuidad, corte de prestación en curso.
- Fuero: Civil y Comercial Federal (obras sociales nacionales y prepagas).
- Fundamento principal: Ley 26.682 y, si hay discapacidad, Ley 24.901 y CDPCD; refuerzo consumeril (art. 42 CN, trato digno art. 8 bis LDC, abusividad art. 1122 CCyC).
- Cautelar de mantenimiento o restablecimiento del servicio mientras tramita el fondo.
- Para el reclamo resarcitorio por el daño ya causado, acumular o reservar la acción ordinaria de consumo (incluido daño punitivo).

### Acción colectiva de consumo

- Legitimación del art. 54 LDC; inscripción en el Registro Público de Procesos Colectivos.
- Apta para incumplimientos masivos y homogéneos (aumentos generalizados, cargos indebidos, cláusulas uniformes).
- Verificar el reglamento de procesos colectivos vigente y la definición de la clase antes de promover.

---

## Instrucciones operativas específicas - consumidor

- Identificar siempre: (a) si hay relación de consumo; (b) la pretensión (cese, prestación, restitución, resarcimiento, daño punitivo, colectiva); (c) la cuantía y la urgencia, que determinan la vía y el fuero.
- No confundir vías: la urgencia de salud va por amparo; el resarcimiento por relación de consumo, por la acción ordinaria o de consumo. No tramitar una urgencia como reclamo de baja cuantía.
- No citar el COPREC como instancia vigente. Verificar el régimen de la Ventanilla Única Federal y de las autoridades locales antes de planificar el reclamo administrativo.
- Cuantificar el daño punitivo con el tope móvil de 2.100 CBT tipo 3 del INDEC (texto Ley 27.701), no con el monto fijo derogado de $5.000.000. Verificar el valor de la CBT a la fecha de la demanda.
- Aplicar por defecto el plazo de 5 años (art. 2560 CCyC) a la acción de daños de consumo contractual. No remitir al art. 50 LDC, que tras la Ley 26.994 rige solo las sanciones administrativas. Único deslinde: daño extracontractual puro, 3 años (art. 2561 CCyC).
- Verificar el alcance del beneficio de gratuidad (art. 53 LDC) en el fuero actuante antes de asegurar al cliente que no afrontará costas en caso de derrota.
- En reclamos contra prepagas y obras sociales que involucren personas con discapacidad, derivar el encuadre principal al perfil de discapacidad (Ley 24.901, CDPCD) y usar el consumeril como refuerzo. No subsumir la cobertura por discapacidad en la lógica de consumo.
- En aumentos de prepaga: aun bajo el DNU 70/23, sostener la revisión por abusividad; documentar la secuencia del aumento y del reclamo previo.
- En acciones colectivas: inscribir en el Registro Público de Procesos Colectivos y verificar litispendencia antes de avanzar.
- Todo escrito en consumidor cierra con "Estado del escrito" estándar más este bloque analítico obligatorio:
  1. Relación de consumo verificada (Sí / No / A precisar).
  2. Pretensión (Cese / Prestación o cobertura / Restitución / Daños / Daño punitivo / Colectiva).
  3. Vía y fuero determinados (Administrativa / Justicia de consumo / Amparo de salud / Ordinaria / Colectiva).
  4. Urgencia y cautelar (Sí / No / Tipo de medida).
  5. Cuantía frente al tope de competencia del fuero de consumo (Dentro / Excede / A verificar).
  6. Daño punitivo planteado y tope verificado (Sí / No / Tope a verificar).
  7. Instancia conciliatoria previa (Ventanilla Única Federal / Autoridad local / No exigible / A verificar).
  8. Beneficio de gratuidad invocado (Sí / No).
  9. Si hay discapacidad: encuadre derivado al perfil de discapacidad (Sí / No / No aplica).
  10. Próximo plazo procesal o estado de la vía administrativa previa.

---

*Versión inicial: junio 2026 (v1) - perfil derivado de la estructura del perfil de discapacidad.*
*Correcciones v2 (auditoría del titular, junio 2026): (1) prescripción de la acción de daños de consumo contractual fijada en 5 años (art. 2560 CCyC), con deslinde extracontractual a 3 años (art. 2561); (2) tope del daño punitivo reexpresado en CBT del INDEC (2.100 CBT, texto Ley 27.701), abandonando el monto fijo de $5.000.000; (3) conciliación/mediación prejudicial local CABA y PBA reconocida como recaudo de admisibilidad subsistente pese a la caída del COPREC; (4) art. 10 CCyC (abuso del derecho) y candidatos jurisprudenciales nominados (Halabi, PADEC c/ Swiss Medical; cautelares de prepagas); (5) Justicia Nacional en lo Comercial incorporada a la tabla de fueros y alerta de mudanza competencial en CABA.*
*Ampliación v3 (junio 2026): cobertura de consumo general con la misma profundidad operativa - garantía legal y vicios de productos (arts. 10-17 LDC y vicios redhibitorios CCyC); oferta, publicidad y lealtad comercial (DNU 274/2019); trato digno y cobranzas extrajudiciales abusivas; daño directo (art. 40 bis); verticales de alto volumen (automotores, turismo, telecomunicaciones, bancos y seguros). Tabla de prescripción extendida (garantía, vicios redhibitorios, seguros de consumo). Nueva plantilla: kb/escritos/consumidor/escritos/modelos/demanda-garantia-producto.md.*
*Eje: consumidor + acceso a la salud, sobre una base de consumo general completa. Jurisdicciones: Nacional/Federal, CABA, PBA.*
*Normativa base: art. 42 CN, Ley 24.240 (texto Ley 27.701 para multas en CBT), CCyC arts. 10, 1092-1122, 2560-2561, vicios redhibitorios 1051-1058, DNU 274/2019 (lealtad comercial), Ley 26.682, Ley 26.993, Ley 18.829 y 25.997 (turismo), Ley 17.418 (seguros), Ley 757 CABA, Ley 13.133 PBA.*
*Nota: el derecho del consumidor fue fuertemente impactado por el DNU 70/2023 y la disolución del COPREC (Decreto 55/2025), reemplazado por la Ventanilla Única Federal (Disposición 890/2025). Verificar vigencia de todas las normas marcadas al momento de cada consulta.*
*Fallos cargados (verificados jun. 2026): legitimación colectiva - Halabi (Fallos 332:111) y PADEC c/ Swiss Medical (Fallos 336:1236); aumentos de prepaga bajo DNU 70/23 - Cainelli c/ OMINT (Cám. CC Federal, Sala II, CCF 4145/2024, 20/05/2025) y cautelar Morsentti c/ OSDE (Juzg. Fed. Concepción del Uruguay N° 2, causa 1461/2024); daño punitivo - Machinandiarena c/ Telefónica (Cám. CC Mar del Plata, Sala II, 27/05/2009, leading case, con nexo de accesibilidad/discapacidad).*
*Pendiente de carga: valor de la CBT del INDEC a la fecha de uso; precedentes locales de graduación del daño punitivo según el fuero del usuario.*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
