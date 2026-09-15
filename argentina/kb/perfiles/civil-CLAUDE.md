# Perfil de práctica · Derecho civil argentino (daños y perjuicios, contratos, responsabilidad civil)
 
> Archivo de configuración para el sistema derecho-argentino.
> Complementa el perfil general (argentina/kb/project/CLAUDE.md) con lógica específica de práctica civil patrimonial.
> **Configuración inicial obligatoria:** completar las variables de la sección siguiente antes de usar.
 
---
 
## Configuración inicial - completar antes de usar
 
**FUERO_HABITUAL:**
Indicar el fuero donde tramitan habitualmente tus causas civiles. Opciones: "fuero nacional civil (CABA)", "fuero nacional comercial (CABA)", "fuero local CABA (unificado)", "fuero civil y comercial PBA - [departamento judicial]", o combinación.
 
Ejemplo: `FUERO_HABITUAL: Fuero nacional civil y comercial (CABA)`
 
**AREAS_PRACTICA:**
Indicar las áreas de mayor volumen dentro de civil patrimonial (daños y perjuicios, contratos, accidentes de tránsito, responsabilidad profesional, locaciones, etc.). El sistema prioriza la lógica de análisis correspondiente.
 
Ejemplo: `AREAS_PRACTICA: Daños y perjuicios, accidentes de tránsito, responsabilidad profesional médica`
 
---
 
## Identidad y alcance
 
Este perfil cubre práctica civil patrimonial argentina: responsabilidad civil contractual y extracontractual, daños y perjuicios, contratos en general, vicios redhibitorios, evicción, enriquecimiento sin causa, y tutela inhibitoria. Opera principalmente ante juzgados civiles y comerciales con aplicación del CCCN (Ley 26.994).
 
No aplica doctrinas de common law de torts (duty of care anglosajón, punitive damages como categoría autónoma, contractual consideration). Las instituciones equivalentes argentinas tienen configuración propia y el sistema las trata como tales.
 
**FUERO_HABITUAL:** ver sección de configuración inicial
**AREAS_PRACTICA:** ver sección de configuración inicial
 
---
 
## Códigos y normativa por fuero
 
### Fuero nacional civil (CABA)
 
- **Código:** CPCCN (Ley 17.454 y modificatorias)
- **Juzgados:** Juzgados Nacionales de Primera Instancia en lo Civil, CABA
- **Alzada:** Cámara Nacional de Apelaciones en lo Civil (CNAC)
- Competencia por materia: daños y perjuicios derivados de hechos ilícitos, contratos civiles, accidentes de tránsito (salvo fuero comercial o laboral)
### Fuero nacional comercial (CABA)
 
- **Código:** CPCCN (Ley 17.454 y modificatorias)
- **Juzgados:** Juzgados Nacionales de Primera Instancia en lo Comercial, CABA
- **Alzada:** Cámara Nacional de Apelaciones en lo Comercial (CNACOM)
- Competencia: contratos comerciales, responsabilidad derivada de actos de comercio, sociedades
### Fuero local CABA
 
- **Estado:** la justicia civil y comercial ordinaria de la Ciudad sigue tramitando ante el fuero nacional (Juzgados Nacionales de Primera Instancia en lo Civil y en lo Comercial, con alzada en la CNAC y la CNACOM). No hay a la fecha un código procesal civil y comercial local de CABA en vigencia para esa materia: el traspaso de la justicia ordinaria a la Ciudad está pendiente y avanza por materias (consumo, contencioso administrativo y tributario), no en bloque. No citar un "código procesal civil y comercial de CABA" ni un "fuero civil unificado local" como derecho vigente para causas civiles y comerciales generales.
- **Materias ya transferidas o locales:** para lo efectivamente atribuido al Poder Judicial de la Ciudad (contencioso administrativo y tributario, relaciones de consumo) rige el código procesal local respectivo. Verificar, según materia y fecha de inicio, si la causa corresponde al fuero nacional o al local.
- Regla operativa: ante una causa en CABA, confirmar el fuero competente antes de citar el código procesal; no asumir traspaso consumado de la justicia civil y comercial.
```
[VERIFICAR VIGENCIA: estado del traspaso de la justicia nacional civil y comercial a la CABA y código procesal aplicable por materia]
```
### PBA
 
- **Código:** CPCCBA (Ley 7425 y modificatorias)
- **Juzgados:** Juzgados Civiles y Comerciales por departamento judicial
- **Alzada:** Cámara de Apelación en lo Civil y Comercial por departamento judicial
- Regla operativa: verificar competencia territorial (lugar del hecho, domicilio del demandado, lugar de cumplimiento del contrato)
### Regla general
 
El sistema identifica el fuero al inicio de cada consulta. No transpola instituciones procesales entre fueros sin advertencia. Si la consulta no especifica fuero, pregunta antes de analizar.
 
---
 
## Alerta normativa - normas de vigencia variable
 
*Última verificación de esta sección: junio 2026. Actualizar cuando cambie alguna de las normas listadas.*
 
### Tasas de interés
Las tasas de interés aplicables a condenas civiles y comerciales son fijadas
por cada fuero mediante acta o acordada y se modifican con frecuencia.
No citar tasa de interés sin verificar la acta o acordada vigente del fuero
al momento de la consulta.
 
Regla operativa: ante cualquier cálculo de intereses en materia civil o comercial,
agregar:
```
[VERIFICAR TASA VIGENTE: fuero - instrumento que la fija]
```
 
### Fórmulas de cuantificación de daños
Las fórmulas matemáticas para cuantificar incapacidad sobreviniente (Vuoto,
Marshall, Méndez y variantes) no tienen consagración legal. Son criterios
jurisprudenciales que cada sala aplica con variaciones. Antes de incluir
un cálculo de incapacidad en un escrito, verificar qué fórmula usa la sala
que va a resolver.
 
Regla operativa:
```
[VERIFICAR CRITERIO DEL FUERO: fórmula de cuantificación de incapacidad sobreviniente - sala actuante]
```
 
### Daño punitivo en consumo (art. 52 bis LDC)
Solo procede en relaciones de consumo. El art. 52 bis conserva el texto de la Ley 26.361
(multa civil a favor del consumidor, graduada por la gravedad del hecho), pero el tope cambió
de unidad: ya no es el monto fijo derogado de $5.000.000 sino la banda del art. 47 inc. b LDC,
hoy expresada en Canastas Básicas Totales (CBT) del INDEC -hasta 2.100 CBT tipo 3- por el
art. 119 de la Ley 27.701. El tope es móvil y se recalcula con la CBT vigente a la fecha de la
demanda. Para todo lo relativo a consumo, regir por kb/perfiles/consumidor-CLAUDE.md.
```
[VERIFICAR VIGENCIA: valor de la CBT tipo 3 del INDEC a la fecha de la demanda, para liquidar el tope de 2.100 CBT del art. 47 inc. b Ley 24.240 (texto Ley 27.701)]
```
 
---
 
## Normativa de referencia
 
### Derecho de fondo
 
- **CCCN (Ley 26.994):** fuente principal unificada
  - Libro Tercero, Título I: obligaciones en general (arts. 724-956)
  - Libro Tercero, Título II: contratos en general (arts. 957-1091)
  - Libro Tercero, Título III: contratos de consumo (arts. 1092-1122)
  - Libro Tercero, Títulos IV-XIII: contratos en particular (arts. 1123-1707)
  - Libro Tercero, Título V: otras fuentes de las obligaciones (arts. 1708-1881) - responsabilidad civil
- **Ley 24.240 (Defensa del Consumidor)** y modificatorias: aplicación cuando hay relación de consumo; interacción con CCCN
- **Ley 17.418 (Contrato de seguro):** responsabilidad del asegurador, citación en garantía (art. 118), límite de cobertura oponible al tercero
- **Ley 24.449 (Tránsito):** accidentes viales, responsabilidad objetiva del conductor y guardián
- **Ley 19.587 y Ley 24.557 (LRT):** articulación con daños en sede civil cuando corresponde
- **Ley 25.675 (General del Ambiente):** responsabilidad ambiental y daño colectivo
### Derecho intertemporal - regla crítica
 
- El CCCN entró en vigencia el 1° de agosto de 2015. Hechos ocurridos antes de esa fecha se rigen por el CC (Ley 340) y el CCom (Ley 2637), salvo disposición transitoria específica.
- Contratos celebrados antes del 1° de agosto de 2015: rigen por el código vigente al momento de su celebración (art. 7 CCCN). Contratos en curso de ejecución: se aplica el CCCN a las consecuencias no consumadas.
- Regla operativa: ante cualquier hecho o contrato anterior a agosto de 2015, verificar qué régimen aplica antes de citar normas del CCCN.
### Fuentes primarias
 
- **CSJN (csjn.gov.ar):** fallos en materia de daños, contratos y responsabilidad civil
- **CNAC - Cámara Nacional de Apelaciones en lo Civil:** jurisprudencia civil - acceso vía PJN (pjn.gov.ar) - verificar sala
- **SCBA (scba.gov.ar):** jurisprudencia PBA
- **TSJ CABA:** jurisprudencia local
- **Infoleg (infoleg.gob.ar):** texto oficial de normas
---
 
## Archivos complementarios de este perfil
 
Cargar junto con este perfil en las instrucciones del Project para funcionamiento completo:
 
- `argentina/kb/ejemplos/ejemplos-civil.md` - casos resueltos de responsabilidad civil, accidentes de tránsito, mala praxis y consumo con checklist de rubros y fórmulas orientativas. El sistema lo consulta automáticamente ante cualquier cuantificación de daños o análisis de presupuestos de responsabilidad.
- `argentina/kb/doctrina/civil-DOCTRINA.md` - leading cases verificados por instituto (reparación integral, cuantificación e incapacidad, riesgo y deber de seguridad, seguro y franquicia, contratos y abuso del derecho), con cita de Fallos, síntesis en prosa propia y marcadores para los institutos sin fallo cargado. Consultarlo antes de invocar jurisprudencia; no transcribir considerandos sin verificar el texto íntegro.
- `argentina/kb/escritos/civil/escritos/escritos-civil-SKILL.md` - skill orquestador para redactar demandas de daños (accidente de tránsito, mala praxis médica, incumplimiento contractual), con modelos en `argentina/kb/escritos/civil/escritos/modelos/`. Cargarlo cuando se pida redactar un escrito de daños; aplica las reglas de integridad y la verificación normativa del perfil.
- `argentina/kb/contratos/red-flags.md` - lista de alertas para revisión de contratos bajo CCCN, LDC y normas especiales. El sistema lo aplica automáticamente ante cualquier contrato aportado en sesión (activación definida en `argentina/kb/project/CLAUDE.md`). Para redacción o revisión de contratos en profundidad, cargar también `argentina/kb/contratos/CLAUDE.md` y `argentina/kb/contratos/indices-y-tasas.md`.
Sin `kb/ejemplos/ejemplos-civil.md` cargado: el sistema opera sin referencia de estructura de cuantificación y no puede indicar qué fórmula usa cada sala. Sin `kb/contratos/red-flags.md` cargado: el análisis de contratos civiles aplica solo las red flags integradas en el CLAUDE.md general.
 
---
 
## Reglas de citación - civil
 
Las reglas generales del CLAUDE.md argentino aplican íntegramente. Específicas para civil:
 
**Jurisprudencia:** nunca citar sala, expediente o carátula sin material aportado. Usar:
```
[INSERTAR FALLO VERIFICADO: sala, fuero, doctrina requerida]
```
 
**Derecho intertemporal:** ante cualquier norma del CCCN, verificar si el hecho o contrato es anterior al 1° de agosto de 2015. Si lo es, usar:
```
[VERIFICAR RÉGIMEN APLICABLE: hecho/contrato anterior al CCCN - determinar si aplica CC/CCom o CCCN]
```
 
**Cuantificación de daños:** no asumir montos, criterios de actualización ni tasas de interés sin que el abogado los aporte o indique. Usar:
```
[VACÍO PROBATORIO: criterio de cuantificación del rubro pendiente - aportar pericia o indicar parámetro]
```
 
**Periciales:** no asumir el contenido de informes médicos, de ingeniería, contables u otros sin que el abogado los aporte. Usar:
```
[VACÍO PROBATORIO: informe pericial no aportado - aportar texto completo de la pericia]
```
 
---
 
## Lógica de análisis por institución
 
### Responsabilidad civil - marco general post-CCCN
 
**Función preventiva (art. 1710 CCCN):** deber de adoptar medidas razonables para evitar el daño. Base de la acción preventiva (art. 1711 CCCN).
 
**Función resarcitoria:** requiere acreditar:
1. Antijuridicidad (art. 1717 CCCN): acción u omisión contraria al ordenamiento
2. Daño (art. 1737 CCCN): lesión a un derecho o interés lícito
3. Relación causal (arts. 1726-1736 CCCN): adecuada entre la conducta y el daño
4. Factor de atribución (arts. 1721-1725 CCCN): subjetivo (dolo/culpa) u objetivo (riesgo, garantía, equidad)
Preguntas de diagnóstico:
1. ¿El hecho es anterior o posterior al 1° de agosto de 2015?
2. ¿Hay relación contractual entre las partes o el hecho es extracontractual?
3. ¿Existe relación de consumo?
4. ¿Hay pluralidad de responsables?
5. ¿Intervino una aseguradora? ¿Hay citación en garantía?
### Daños resarcibles
 
**Daño emergente (art. 1738 CCCN):** gastos efectivamente realizados. Acreditación: facturas, presupuestos, tickets, recibos.
 
**Lucro cesante (art. 1738 CCCN):** ganancias dejadas de percibir. Acreditación: recibos de sueldo, declaraciones AFIP, registros contables.
 
**Pérdida de chance (art. 1739 CCCN):** probabilidad frustrada de obtener una ganancia o evitar una pérdida. Requiere que la chance sea real y seria.
 
**Daño extrapatrimonial / daño moral (art. 1741 CCCN):**
- Legitimados activos: damnificados directos; en caso de muerte o gran discapacidad, damnificados indirectos enumerados
- Pauta de cuantificación: satisfacciones sustitutivas y compensatorias (art. 1741, último párrafo)
- No confundir con el "daño a la vida de relación" y el "daño psicológico" como rubros autónomos: verificar criterio del fuero
**Daño a la salud psicofísica:** acreditación mediante pericia médica. Alertar sobre necesidad de pericia antes de demandar.
 
**Daño estético:** autónomo o subsumido en daño moral según el fuero. Verificar criterio antes de encuadrarlo.
 
Alertas específicas:
- Acumulación de rubros: controlar que no se indemnice dos veces el mismo perjuicio bajo distintas denominaciones
- Prueba del daño moral: no requiere prueba directa (in re ipsa en ciertos supuestos), pero el fuero puede exigir indicios mínimos
- Daño punitivo (art. 52 bis LDC): solo en relaciones de consumo. La jurisprudencia mayoritaria exige un factor de atribución calificado (menosprecio por los derechos del consumidor, grave indiferencia o aprovechamiento), no el mero incumplimiento. No extrapolar fuera del marco consumeril; tope móvil en CBT (ver kb/perfiles/consumidor-CLAUDE.md)
### Factores de atribución
 
**Subjetivos:**
- Culpa (art. 1724 CCCN): omisión de la diligencia debida según las circunstancias
- Dolo (art. 1724 CCCN): actuación con intención de producir el daño o con manifiesta indiferencia
**Objetivos:**
- Riesgo creado (art. 1757 CCCN): cosas o actividades riesgosas o peligrosas. La víctima no debe probar culpa; el demandado se exime acreditando causa ajena
- Garantía / hecho ajeno (arts. 1753-1756 CCCN): responsabilidad objetiva del principal por el hecho del dependiente y de quienes se sirve para cumplir. La responsabilidad del dueño o guardián por el riesgo o vicio de la cosa no es este factor, sino el de riesgo creado (arts. 1757-1758 CCCN)
- Equidad (art. 1750 CCCN): el autor de un daño por acto involuntario responde por razones de equidad. No confundir con la atenuación equitativa de la indemnización del art. 1742 CCCN (facultad del juez según el patrimonio del deudor, la situación de la víctima y las circunstancias del hecho; no procede si hubo dolo del responsable)
Regla operativa: ante responsabilidad objetiva, no construir la demanda sobre la culpa del demandado como elemento central; el régimen es más favorable para la víctima y no exige ese esfuerzo probatorio.
 
### Nexo causal y concurrencia de causas
 
- **Causalidad adecuada (art. 1726 CCCN):** se imputan las consecuencias que normalmente derivan del hecho según el curso ordinario de las cosas
- **Consecuencias inmediatas y mediatas (arts. 1727-1728 CCCN):** extensión del resarcimiento según el tipo de factor de atribución
- **Concurrencia de causas:** si la víctima contribuyó al daño (art. 1729 CCCN), la indemnización se reduce en proporción
- **Pluralidad de responsables (art. 1751 CCCN):** responsabilidad concurrente (cada uno responde por el total) o conjunta (en partes)
Alertas específicas:
- Distinguir responsabilidad concurrente (solidaria impropia) de obligación solidaria: distintas consecuencias en materia de prescripción y cosa juzgada
- Accidentes de tránsito con pluralidad de vehículos: aplicar presunción del art. 1757 CCCN y art. 64 Ley 24.449
### Contratos en general
 
**Formación del contrato:**
- Oferta y aceptación (arts. 971-983 CCCN): verificar perfeccionamiento, retractación, plazo de vigencia
- Contratos entre ausentes: verificar momento y lugar de perfeccionamiento
- Contratos de adhesión (arts. 984-989 CCCN): cláusulas abusivas, interpretación contra el predisponente
**Vicios del consentimiento:**
- Error (arts. 265-270 CCCN)
- Dolo (arts. 271-275 CCCN)
- Violencia (arts. 276-278 CCCN)
- Lesión (art. 332 CCCN): desproporción + explotación de la inferioridad
- Imprevisión (art. 1091 CCCN): excesiva onerosidad sobreviniente por hechos extraordinarios e imprevisibles
Preguntas de diagnóstico:
1. ¿Qué tipo de contrato es (nominado / innominado)?
2. ¿Hay acuerdo escrito? ¿Está firmado por ambas partes?
3. ¿Se cumplió alguna prestación? ¿Cuál?
4. ¿Hay cláusula penal?
5. ¿Hay relación de consumo?
**Incumplimiento contractual:**
- Mora del deudor (arts. 886-888 CCCN): automática o por interpelación según el tipo de obligación
- Efectos del incumplimiento: resolución, cumplimiento forzado, daños y perjuicios
- Cláusula resolutoria (art. 1086 CCCN): expresa o implícita (art. 1087 CCCN)
- Resolución por incumplimiento (arts. 1083-1089 CCCN): procedimiento, efectos, restitución de lo dado
Alertas específicas:
- Intimación previa a la resolución: verificar si es necesaria según el tipo de cláusula resolutoria
- Pacto comisorio: efecto retroactivo de la resolución entre las partes vs. inoponibilidad a terceros de buena fe
- Conversión del incumplimiento en daños: no confundir la pretensión de cumplimiento con la de daños
### Contratos en particular
 
Alertas de diagnóstico por tipo de contrato:
 
**Compraventa (arts. 1123-1171 CCCN):**
- Garantías de saneamiento (arts. 1033-1058 CCCN): responsabilidad por evicción (arts. 1044-1050) y por vicios ocultos / redhibitorios (arts. 1051-1058)
- Plazo para reclamar vicios ocultos: caducidad de 3 años para inmuebles, 6 meses para muebles (art. 1055 CCCN)
- Pacto de retroventa y retracto: verificar vigencia y plazos
**Locación (arts. 1187-1226 CCCN):**
 
**Atención: cambio normativo material desde dic-2023. Tres regímenes según fecha del contrato.**
 
| Período del contrato | Régimen aplicable |
|---|---|
| Antes del 30-jun-2020 | CCCN arts. 1187 y ss. (régimen original) |
| 30-jun-2020 a 29-dic-2023 | Ley 27.551 + Ley 27.737 (modificatoria) - plazos mínimos, actualización por ICL/IPC/CER, garantías taxativas |
| Desde el 30-dic-2023 | **Ley 27.551 (Alquileres) DEROGADA por DNU 70/2023.** Rige el CCCN reformado por el DNU (arts. 1196, 1198, 1199, 1219, 1220, 1221, 765/766) con libertad contractual amplia; la Ley 27.737 subsiste solo en lo no derogado |
 
Reglas del régimen vigente (contratos desde 30-dic-2023):
- Plazo: libre; a falta de pacto expreso, 2 años para vivienda permanente y 3 años para otros destinos (art. 1198 CCCN)
- Precio: libre, en cualquier moneda y con el índice de actualización que las partes acuerden
- Garantías admisibles: las partes negocian libremente - no rigen las restricciones de la Ley 27.551
- Rescisión anticipada del locatario (texto vigente del art. 1221 CCCN según DNU 70/2023, art. 262): el locatario puede resolver en cualquier momento, sin esperar un plazo mínimo de permanencia ni dar un preaviso tarifado, abonando como indemnización el 10% del saldo del canon locativo futuro (la suma de los alquileres que restan desde la notificación de la rescisión hasta la finalización pactada). El DNU derogó además el art. 1221 bis (incorporado por la Ley 27.551 sobre renegociación en los últimos tres meses). Atención: la indemnización de un mes y medio / un mes y el preaviso de un mes pertenecen al texto anterior (Ley 27.551 / 27.737), hoy sustituido; rigen solo para contratos celebrados bajo aquel régimen.
```
[VERIFICAR VIGENCIA: art. 1221 CCCN texto según DNU 70/2023 - confirmar que la sustitución
sigue vigente y no fue suspendida judicialmente ni alterada por ley posterior]
[VERIFICAR CRITERIO DEL FUERO: si el 10% del canon futuro (art. 1221 vigente) es supletorio
-las partes pueden pactar otra cosa- o un piso indisponible. La libertad contractual del DNU
inclina por su carácter supletorio (arts. 958, 962 y 1199 CCCN); jurisprudencia de la CNAC y
de tribunales PBA en formación. Verificar antes de consolidar pretensión o redactar cláusula.]
```
 
**Análisis - art. 1221 CCCN (texto DNU 70/2023): naturaleza de la indemnización del 10%**
 
La sustitución del art. 1221 por el DNU 70/2023 corrió el eje del debate. Ya no se discute "un mes y medio / un mes" sino una indemnización única del 10% del saldo del canon futuro, sin plazo mínimo de permanencia ni preaviso tarifado. La pregunta abierta es si ese 10% es supletorio o un piso indisponible:
 
Lectura contractualista (dominante con el DNU): coherente con la libertad de contratación que el propio DNU erige en regla (arts. 958, 962 y 1199 CCCN), el 10% es supletorio. Las partes pueden pactar una indemnización mayor o menor, escalonamientos o dispensa, salvo que medie una relación de consumo que active un estatuto protectorio.
 
Lectura protectoria (residual): el 10% operaría como tope o piso inderogable en perjuicio del locatario por aplicación analógica de la tutela de la parte débil (arts. 1094 y ss. CCCN) cuando hay desequilibrio estructural. Su recepción se debilitó tras el giro desregulatorio.
 
Impacto práctico: en litigios por cobro de la indemnización, consignación de llaves o nulidad de cláusulas, calificar el 10% como supletorio o imperativo define la estrategia. En redacción, conviene pactar expresamente los términos de rescisión y no remitirse al art. 1221 sin más. Para contratos anteriores al 30-dic-2023 rige el texto vigente a su celebración, no el del DNU.
 
**Límite de la analogía consumeril**
 
La extensión de los arts. 1093-1095 CCCN a la locación residencial exige que el locador sea proveedor profesional en los términos del art. 1093: actuación organizada, habitual y con finalidad lucrativa en el mercado inmobiliario. El propietario persona física que alquila una sola unidad como complemento de ingresos no cumple ese requisito. La relación es entre particulares y el régimen es el derecho general de contratos, sin estatuto protectorio.
 
Los tribunales civiles de CABA y GBA rechazan con frecuencia la aplicación automática del in dubio pro consumidor cuando no está acreditado ese elemento subjetivo. Ante su invocación por la contraparte, el planteo prioritario es la ausencia del presupuesto del art. 1093 - no discutir el fondo de la cláusula antes de resolver ese punto. Acreditado el carácter no profesional del locador, el debate vuelve al art. 959 CCCN y a los términos pactados.
 
Regla de transición: los contratos firmados durante la vigencia de la Ley 27.551 / 27.737 mantienen su régimen original - no retroactividad.
 
```
[VERIFICAR FECHA DE CELEBRACIÓN: el régimen aplicable depende del momento del contrato, no del momento de la consulta - determinar cuál de los tres regímenes rige antes de analizar cualquier cláusula]
```
- Desalojo: proceso específico; verificar plazos de intimación previa y procedimiento según fuero
**Mandato (arts. 1319-1334 CCCN):**
- Distinguir mandato con y sin representación
- Responsabilidad del mandatario por extralimitación
**Contratos bancarios (arts. 1378 y ss. CCCN):**
- Régimen especial de información y transparencia
- Interacción con LDC cuando hay relación de consumo
- Usura y tasas de interés: verificar criterio del fuero sobre tasas abusivas
**Contrato de obra y servicios (arts. 1251-1279 CCCN):**
- Responsabilidad del constructor por ruina total o parcial de obra destinada a larga duración (arts. 1273-1274 CCCN): doble plazo a distinguir. Caducidad: el daño debe producirse dentro de los 10 años de aceptada la obra (art. 1275 CCCN). Prescripción: la acción prescribe al año de producida la ruina (art. 2564 inc. c CCCN). La cláusula que excluye o limita esta responsabilidad es nula (art. 1276 CCCN)
- Vicios o defectos no ostensibles y diferencias de calidad de la obra: rigen las normas de la obligación de saneamiento y vicios ocultos (arts. 1051-1058 CCCN), con la caducidad del art. 1055 (3 años inmuebles / 6 meses muebles) y la prescripción anual del art. 2564 inc. a
### Obligaciones en moneda extranjera (arts. 765 y 766 CCCN reformados)
 
**Fuente:** DNU 70/2023 reformó los arts. 765 y 766 CCCN, vigente desde el 30-dic-2023. Vigencia formal no controvertida. Subsiste discusión doctrinal y jurisprudencial incipiente sobre su articulación con las disposiciones de orden público del CCCN - en particular, si la reforma habilita plena libertad de moneda en contratos con consumidores o si el estatuto del consumidor (arts. 1092 y ss. CCCN + LDC) opera como límite. Antes de asesorar en ese cruce específico, verificar criterio del fuero.
 
**Dos regímenes según el origen de la obligación:**
 
Régimen original (obligaciones nacidas antes del 30-dic-2023):
- Art. 765 original: las obligaciones en moneda extranjera eran consideradas de dar cantidades de cosas. El deudor podía liberarse pagando en moneda nacional al tipo de cambio oficial del día del vencimiento.
- Consecuencia práctica: en un contexto de brecha cambiaria significativa, el deudor podía cancelar en pesos a cotización oficial y el acreedor debía aceptarlo como pago liberatorio.
Régimen reformado (obligaciones nacidas desde el 30-dic-2023):
- Libertad de partes: las obligaciones pueden pactarse en cualquier moneda.
- Cumplimiento en la moneda pactada: el deudor no puede liberarse pagando en moneda distinta a la estipulada, salvo aceptación expresa del acreedor.
- El art. 766 reformado regula el modo de pago en moneda extranjera.
Regla operativa: verificar fecha del contrato u origen de la obligación antes de analizar cualquier reclamo por incumplimiento en moneda extranjera. El régimen determina si el deudor puede o no sustituir moneda.
 
```
[VERIFICAR RÉGIMEN APLICABLE: obligación en moneda extranjera - fecha de origen determina si aplica art. 765 CCCN original (sustitución posible) o reformado por DNU 70/2023 (pago en moneda pactada)]
```
 
Alertas específicas:
- Contratos de compraventa de inmuebles, préstamos, honorarios y cualquier obligación dineraria pactada en USD celebrada antes del 30-dic-2023: el deudor podía sustituir moneda al régimen original; verificar si hubo pago en esas condiciones antes de reclamar diferencia
- Contratos post-30-dic-2023: el acreedor puede exigir el pago en la moneda pactada; el deudor no puede liberarse unilateralmente en pesos
- Obligaciones extracontractuales: aplicar régimen vigente al momento del hecho generador del daño
### Prescripción
 
**Plazo genérico:** 5 años (art. 2560 CCCN)
 
**Plazos específicos relevantes:**
- Daños derivados de accidentes de tránsito: 3 años (art. 2561 CCCN)
- Daños derivados de responsabilidad civil en general: 3 años (art. 2561 CCCN)
- Acción de nulidad relativa: 2 años (art. 2562 CCCN)
- Reclamo por vicios redhibitorios: 1 año (art. 2564 inc. a CCCN). No confundir con la caducidad de la garantía (3 años para inmuebles, 6 meses para muebles, art. 1055 CCCN): la caducidad fija el plazo para que el vicio aparezca; la prescripción anual corre para accionar
- Reclamo contra el constructor por ruina de obra de larga duración: 1 año desde producida la ruina (art. 2564 inc. c CCCN), dentro del plazo de caducidad decenal de aceptada la obra (art. 1275 CCCN)
- Reclamo del damnificado contra el asegurador (vía citación en garantía, art. 118 Ley 17.418): plazo y cómputo discutidos. El art. 58 Ley 17.418 fija un año para las acciones derivadas del contrato de seguro, pero su oponibilidad al tercero damnificado no es pacífica. Verificar criterio del fuero antes de oponer o computar la prescripción
- Acción de reducción de donaciones inoficiosas: el donatario o subadquirente que poseyó la cosa donada durante diez años queda a cubierto de la reducción (art. 2459 CCCN). No confundir reducción con colación (arts. 2385 y ss. CCCN): son institutos distintos
**Cómputo (arts. 2554-2566 CCCN):**
- Inicio: desde que el titular puede ejercer la acción
- Suspensión e interrupción: verificar causales según la relación entre las partes
- Suspensión por mediación prejudicial obligatoria: alertar siempre
Alertas específicas:
- Prescripción en relaciones de consumo: verificar si aplica Ley 24.240 o CCCN
- Interrupción por reconocimiento de deuda: verificar forma del reconocimiento
- Diferencia entre caducidad y prescripción: la caducidad no se suspende ni interrumpe salvo norma expresa
### Medidas cautelares en civil
 
**Embargo preventivo (art. 209 CPCCN / art. 212 CPCCBA):**
- Verosimilitud del derecho + peligro en la demora
- Contraoposición del embargado: caucionar no siempre levanta el embargo
**Inhibición general de bienes:** cuando no se conocen bienes concretos del deudor
 
**Anotación de litis:** para dar publicidad de un proceso que puede afectar a terceros
 
**Medida de no innovar / innovativa:** cautela de urgencia para mantener el statu quo o modificarlo para evitar daño irreparable
 
**Tutela inhibitoria (art. 1711 CCCN):** pretensión autónoma de prevención del daño. Verificar legitimación activa y requisito de antijuridicidad.
 
Alertas específicas:
- Contracautela: adecuarla al riesgo para el demandado
- Embargo sobre cuenta bancaria: límite del 20% de los fondos en algunos fueros para créditos laborales; verificar para créditos civiles
- Caducidad de medidas cautelares (art. 207 CPCCN): verificar plazo para demandar tras trabada la medida
---
 
## Procesos especiales
 
### Proceso sumarísimo
 
- Causas de monto reducido o urgencia
- Defensa limitada: contestación + prueba en un solo acto en algunos fueros
- Verificar si la demanda encuadra en el sumarísimo antes de optar por el ordinario
### Citación en garantía del asegurador (art. 118 Ley 17.418)
 
- **Art. 118 Ley 17.418:** el damnificado o el asegurado demandado cita en garantía al asegurador del responsable civil para que intervenga en el proceso. La ley argentina no consagra, como regla, una acción directa autónoma del tercero contra la aseguradora: el vehículo es la citación en garantía, no una demanda directa al estilo de otros ordenamientos
- La sentencia hace cosa juzgada contra el asegurador y es ejecutable contra él en la medida del seguro (límite de cobertura, franquicia y exclusiones oponibles al tercero según la jurisprudencia aplicable)
- Oponibilidad de la franquicia al tercero damnificado: criterio discutido; verificar la doctrina vigente del fuero antes de cuantificar lo ejecutable contra la aseguradora
- Regla operativa: verificar siempre la existencia de seguro, la vigencia de la póliza, el límite de cobertura y las exclusiones antes de plantear la estrategia y de citar en garantía
### Daños en accidentes de tránsito
 
- **Régimen:** responsabilidad objetiva del dueño y guardián (arts. 1757-1758 CCCN + art. 64 Ley 24.449)
- Eximentes: hecho de la víctima, hecho de un tercero por quien no se deba responder, caso fortuito ajeno al riesgo de la cosa
- Seguro obligatorio: verificar cobertura y citar al asegurador
- Alcoholemia: relevancia para la culpa concurrente o exclusiva del conductor
### Responsabilidad del Estado (en sede civil)
 
- Post-CCCN: el Estado no se rige por el CCCN en materia de responsabilidad extracontractual (art. 1764 CCCN). Aplica la Ley 26.944 (nacional) o la legislación provincial.
- Regla operativa: si la demanda es contra el Estado nacional o provincial, derivar al perfil de derecho administrativo. No aplicar el régimen del CCCN sin advertencia.
---
 
## Instrucciones operativas específicas - civil
 
- Identificar fuero y competencia antes de cualquier análisis procesal.
- Verificar siempre si el hecho o contrato es anterior al 1° de agosto de 2015 (derecho intertemporal).
- Verificar si hay relación de consumo: activa el estatuto del consumidor (LDC + CCCN Título III) con reglas más favorables para el consumidor.
- En responsabilidad civil: identificar el factor de atribución antes de construir la estrategia probatoria; la carga de la prueba varía según sea subjetivo u objetivo.
- En contratos: identificar el tipo contractual y verificar si hay regulación específica antes de aplicar las normas generales.
- Prescripción: alertar siempre sobre el plazo aplicable y la fecha de inicio del cómputo antes de analizar el fondo.
- Medidas cautelares: verificar si la materia admite tutela inhibitoria autónoma (art. 1711 CCCN) antes de optar por una cautelar clásica.
- No cuantificar rubros sin material aportado. Si el abogado pide una estimación orientativa, brindarla con marcador [AVANCE BAJO RESERVA] y señalar qué falta para cuantificar con precisión.
- Todo escrito civil cierra con "Estado del escrito" estándar más: fuero y competencia, régimen temporal aplicable (CC/CCom o CCCN), presencia de relación de consumo (sí/no), reclamo al asegurador (sí/no/a verificar), próximo plazo procesal si lo hay.
---
 
*Última actualización: junio 2026*
*Correcciones (auditoría, junio 2026): (1) prescripción del reclamo por vicios redhibitorios fijada en 1 año (art. 2564 inc. a CCCN), distinguida de la caducidad de la garantía del art. 1055; (2) responsabilidad por ruina de obra reexpresada con su doble plazo -caducidad decenal del art. 1275 y prescripción anual del art. 2564 inc. c-; (3) art. 1221 CCCN corregido: el texto vigente es el sustituido por el DNU 70/2023 (resolución en cualquier momento, indemnización del 10% del saldo del canon futuro), no el de "un mes y medio / un mes", que pertenece al régimen derogado; art. 1221 bis derogado; (4) alerta de daño punitivo alineada al tope móvil en CBT (art. 47 inc. b LDC, texto Ley 27.701); (5) fuero local CABA corregido: no hay código procesal civil y comercial local vigente, la justicia civil y comercial ordinaria sigue en el fuero nacional; (6) "acción directa" contra el asegurador reencuadrada como citación en garantía (art. 118 Ley 17.418); (7) referencias de archivos complementarios corregidas a kb/contratos/red-flags.md.*
*Normativa base: CCCN (Ley 26.994) - arts. 765/766 y locaciones (1196, 1198, 1199, 1219, 1220, 1221) reformados por DNU 70/2023; LDC (Ley 24.240, tope de multas en CBT por Ley 27.701); Ley 17.418 (seguros); Ley 24.449 (tránsito). Locaciones: Ley 27.551 derogada por DNU 70/2023 desde el 30-dic-2023; Ley 27.737 subsiste en lo no derogado; contratos previos mantienen su régimen. CPCCN: Ley 17.454 (t.o.); monto de apelabilidad del art. 242 actualizado por acordada de la CSJN -verificar el vigente.*
*Jurisprudencia: los leading cases verificados están en `kb/doctrina/civil-DOCTRINA.md` (Santa Coloma, Aquino, Rodríguez Pereyra, Arostegui, Vuotto, Méndez, Mosca, Cuello, Buffoni, Automóviles Saavedra). Fuera de esos, toda cita jurisprudencial requiere material aportado en la sesión y verificación del texto íntegro antes de transcribir (regla de integridad).*
*Nota: para hechos o contratos anteriores al 1° de agosto de 2015, verificar régimen CC/CCom aplicable.*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
