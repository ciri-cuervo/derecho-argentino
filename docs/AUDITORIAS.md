# 📋 Auditorías contra fuente primaria

Registro de las auditorías que este fork corre contra `argentina/fuentes/`: qué se leyó, contra
qué texto, y qué se encontró. Es **capa 3a, CC BY-SA 4.0** — ver [`LICENCIAS.md`](../LICENCIAS.md).

**Una auditoría vale por su fecha**, así que cada entrada la lleva: dice contra qué texto se
cotejó y cuándo, no qué se cambió. Va acá y no en `argentina/kb/CHANGELOG.md` porque ese archivo
es el historial de la base heredada, capa 2, y la frontera de licencia es la ruta.

Lo que va en cada lugar:

| Qué | Dónde |
| --- | --- |
| Una auditoría de este fork contra fuente primaria | **Este archivo** |
| El estado de verificación por bloque, con fecha y volatilidad | `references/changelog-normativo.md` |
| Un cambio en la base heredada | `argentina/kb/CHANGELOG.md`, y sólo si se tocó `kb/` |
| La versión del plugin | [`CHANGELOG.md`](../CHANGELOG.md), sólo al publicar |

---

### Septiembre 2026 - Incorporación de fuentes doctrinarias: CCyC Comentado y derecho de daños

Dos obras de referencia sumadas al repositorio, con tratamiento distinto según su licencia.

**Código Civil y Comercial de la Nación Comentado (SAIJ-INFOJUS, 2ª ed. actualizada 2022).**
Directores: Marisa Herrera, Gustavo Caramelo y Sebastián Picasso. Publicación de distribución
gratuita del Ministerio de Justicia y Derechos Humanos, de libre reproducción total o parcial
citando la fuente. Los seis tomos se incorporan completos en `argentina/fuentes/ccyc-comentado/`
(~18 MB), junto con `INDICE.md`, que:

- mapea cada tomo a su rango de artículos y al archivo PDF correspondiente;
- detalla la estructura interna de cada tomo (Libro / Título / Capítulo) con la página del PDF
  donde arranca cada sección, verificada contra el cuerpo de la obra y no calculada;
- consigna el desfasaje entre página impresa y página PDF, constante dentro de cada tomo
  (T1 +39, T2 +23, T3 +27, T4 +29, T5 +25, T6 +25);
- incluye una tabla de ruteo rápido por instituto, pensada para ir directo al comentario de un
  artículo mientras se redacta;
- señala que "contratos en particular" queda partido entre los tomos 3 y 4, que es el error de
  navegación más probable;
- registra una discrepancia de la fuente sin corregirla: los tomos 1 a 5 imprimen como ISBN de
  obra completa 978-987-8338-31-6 y el tomo 6 imprime 978-987-8338-37-8.

**Manual de Derecho de Daños, 2ª ed. (Weingarten -dir.-, La Ley, 2015).** Obra comercial con
todos los derechos reservados: el editor prohíbe expresamente su reproducción total o parcial.
Como este repositorio es público, **el PDF no se incorpora y no debe incorporarse**. En su lugar
se agrega `argentina/kb/doctrina/civil-DOCTRINA-danos.md`, un índice doctrinario con 38 entradas por
instituto, cada una con síntesis propia, artículos del CCCN y del Código derogado, fallos
citados y remisión a capítulo y página. No contiene transcripción de la obra: el texto
entrecomillado corresponde a carátulas de fallos y a expresiones de la ley.

El archivo consigna además qué institutos la obra **no** trata de forma autónoma -antijuridicidad,
relación de causalidad, eximentes y prescripción no tienen capítulo propio; el daño punitivo solo
tres menciones breves- y una sección de advertencias de vigencia, porque la obra es de 2015 y
comenta el CCCN recién sancionado: DNU 70/2023 en locaciones y obligaciones en moneda extranjera,
art. 1764 CCCN y adhesión provincial a la Ley 26.944, tope del daño punitivo hoy en canastas
básicas por la Ley 27.701, y las fórmulas de cuantificación, que no tienen consagración legal.
Se deja señalado que la obra atribuye el art. 52 bis LDC a la "ley 26.367" cuando corresponde a
la Ley 26.361.

**Regla nueva de higiene del repositorio.** Se agrega `argentina/fuentes/_local/` al `.gitignore`:
es la carpeta donde el abogado guarda su ejemplar de obras comerciales, que nunca se commitean.
El criterio: una obra entra al repositorio solo si su propia licencia lo permite. Las que no,
entran como doctrina destilada con remisión, nunca como texto.

---

### Septiembre 2026 - Auditoría contra fuente primaria: Ley 15.057, mediación PBA, intereses y art. 245

Auditoría de verificación externa contra **InfoLEG**, el **Boletín Oficial** y
**normas.gba.gob.ar**. A diferencia de la auditoría anterior -que resolvió contradicciones
internas entre archivos-, esta contrastó el contenido del repositorio con el texto de las
normas. Los hallazgos se agrupan por gravedad.

**Reversión de un parche anterior (Ley 27.737).** La entrada previa de septiembre de 2026
había alineado `kb/contratos/CLAUDE.md` a la fórmula "la Ley 27.737 subsiste solo en lo no
derogado". La verificación en InfoLEG confirma lo contrario: el **DNU 70/2023 derogó tanto
la Ley 27.551 como la Ley 27.737**. Se revierte ese parche en sus tres puntos de
`kb/contratos/CLAUDE.md`, y se corrige `kb/perfiles/civil-CLAUDE.md` y `skills/derecho-argentino/SKILL.md`
en el mismo sentido.

**Críticos (afectan la validez del consejo):**

1. **La Ley 11.653 está DEROGADA.** El **art. 88 de la Ley 15.057** derogó la Ley 11.653 y
   sus modificatorias. El código procesal laboral vigente de PBA es la **Ley 15.057**
   (modificada por la **Ley 15.557**), cuya operatividad dispuso la **Res. SC 1840/2024**
   (03/07/2024), con aplicación inmediata a las causas en trámite en las que no se hubiera
   celebrado la audiencia de vista de causa. La 11.653 conserva ultraactividad **solo en
   materia de recusación**. La estructura es de **Juzgados del Trabajo unipersonales** y
   **Cámaras de Apelación del Trabajo**, no de Tribunales del Trabajo colegiados. Art. 17:
   plazos por días hábiles, perentorios e improrrogables; art. 89: CPCCBA supletorio.
   Corregido en `kb/perfiles/laboral-CLAUDE.md`, `kb/transversales/plazos-SKILL.md`, `skills/derecho-argentino/SKILL.md`,
   `setup-interview.md` y los tres archivos del eval laboral, con nota en cada lugar para
   que la 11.653 no se reintroduzca.

2. **Mediación PBA (Ley 13.951): no suspende como la nacional.** El **art. 40** le asigna
   **carácter de intimación**, con los efectos del segundo párrafo del **art. 3986 del
   Código Civil** (derogado), hoy reconducidos al **art. 2541 CCyCN**: suspensión por
   interpelación fehaciente, **por una sola vez y por seis meses**. No es el régimen del
   **art. 18 de la Ley 26.589** (suspensión durante todo el procedimiento, con reanudación
   a los 20 días del acta de cierre). Corregido en `kb/transversales/plazos-SKILL.md`, `kb/perfiles/civil-CLAUDE.md`,
   `kb/escritos/civil/escritos/escritos-civil-SKILL.md`, `skills/derecho-argentino/SKILL.md` y el eval
   civil.

3. **Intereses laborales: numeración equivocada.** Los artículos del régimen son **de la
   Ley 27.802**, no de la LCT. **Art. 276 LCT** (texto art. 54 Ley 27.802): créditos nuevos,
   IPC Nivel General INDEC + 3% anual. **Art. 55 de la Ley 27.802** (norma autónoma):
   juicios en trámite al 06/03/2026, tasa pasiva BCRA con piso del 67% y tope IPC+3%,
   instrumentada por **Res. Directorio BCRA 45/2026**. **Art. 277 LCT** (texto art. 56
   Ley 27.802): depósito en cuenta sueldo, tope de costas y honorarios y pago en cuotas.
   Además: el **art. 54 LCT fue derogado por el art. 207 de la Ley 27.802**, y los **arts.
   55 y 57 LCT conservan su materia clásica** (presunciones procesales). Corregido en
   `kb/perfiles/laboral-CLAUDE.md`, `kb/escritos/laboral/telegrama/reglas-normativas.md`, `kb/ejemplos/ejemplos-laboral.md` y
   `skills/derecho-argentino/SKILL.md`.

4. **Base del art. 245 LCT.** El texto vigente (art. 51 Ley 27.802) excluye **SAC,
   vacaciones y premios que no sean de pago mensual**, y **no menciona las horas extras**.
   Define **habitual** (devengado durante al menos seis meses) y **normal** (para conceptos
   variables, promedio de los últimos seis meses). Tope: tres veces el importe del **salario
   mensual promedio** del CCT, **excluida la antigüedad**. Incorpora un **piso del 67% de la
   remuneración calculada** (el estándar de "Vizzoti" quedó en el texto legal para este
   tramo) y un **mínimo de un mes** -los regímenes anteriores tenían mínimo de dos-. Se
   eliminó "horas extras" de la exclusión y el pasaje que contraponía la base del preaviso a
   la del art. 245 sobre esa premisa. Se agregó la advertencia de que el **Título laboral del
   DNU 70/2023 estuvo judicialmente suspendido**, de modo que la exclusión de SAC en el tramo
   30/12/2023 a 08/07/2024 **no está confirmada**, con marcador
   `[REVISIÓN NORMATIVA REQUERIDA: vigencia efectiva del Título laboral del DNU 70/2023 en el
   tramo del acto extintivo - verificar estado cautelar a esa fecha]`.

5. **Art. 64 de la Ley 24.449.** No consagra responsabilidad objetiva: se titula
   **"Presunciones"** y fija presunciones **iuris tantum** (se presume responsable a quien
   carecía de prioridad de paso o cometió una infracción relacionada con la causa; beneficio
   de la duda a favor del peatón). La responsabilidad objetiva surge de los **arts. 1757-1758
   CCyCN**. Corregido en `kb/perfiles/civil-CLAUDE.md`, `kb/escritos/civil/escritos/escritos-civil-SKILL.md`,
   `kb/escritos/civil/escritos/modelos/demanda-danos-accidente-transito.md`,
   `skills/derecho-argentino/SKILL.md` y el eval civil.

**Citas y numeración corregidas:**

- **Ley 24.013:** el art. 99 de la Ley 27.742 derogó los **arts. 8 a 17** en bloque (incluye
  8, 9, 10, 11 y 15) y los **arts. 43 a 48 de la Ley 25.345**. El repositorio enumeraba solo
  "8, 9, 10 y 15".
- **CPCCBA:** el cómputo por días hábiles es el **art. 156**, no el 153. El art. 152 define
  días y horas hábiles; el art. 153 es la *habilitación* de días y horas inhábiles.
- **Plazo de gracia:** Nación, art. 124 CPCCN, **dos** primeras horas del despacho; PBA,
  art. 124 CPCCBA, **cuatro** primeras horas del despacho. Son horas de atención del
  tribunal, no "las 2:00 hs": se corrigieron también los ejemplos de output.
- **Ley 18.345:** traslado de la demanda por 10 días, **art. 68** (el art. 71 regula la
  *forma* de la contestación); apelación de interlocutorias por 3 días, **art. 117** (el
  art. 110 es el efecto diferido, sustituido por el art. 87 de la Ley 27.802); sentencias
  definitivas, 6 días, **art. 116**; caducidad de instancia del **art. 46** (texto art. 82
  Ley 27.802): **6 meses** en primera o única instancia y **3 meses** en segunda.
- **CPCCN:** el plazo de 5 días de la queja lo fija el **art. 282**; se cita "art. 285 en
  función del art. 282".
- **Art. 1198 CCyCN** (texto art. 256 DNU 70/2023): **no hay plazo mínimo imperativo**. A
  falta de plazo pactado: locación **temporal**, usos y costumbres del lugar; **vivienda
  permanente**, dos años; **restantes destinos**, tres años. El repositorio traía "2 años
  para cualquier destino".
- **Art. 47 inc. b LDC** (texto art. 119 Ley 27.701): la denominación legal es "de cero coma
  cinco (0,5) a dos mil cien (2.100) **canastas básicas total para el hogar 3**". "CBT tipo
  3" no es la expresión de la ley.

**Matices incorporados:**

- **Art. 9 LCT** (texto art. 3 Ley 27.802): el texto legal adopta el "criterio de
  **agrupamiento por instituciones**, es decir, el conjunto de normas que rige cada una de
  las instituciones en el derecho del trabajo" (conglobamiento por instituciones). Se
  eliminó la fórmula "instituto por instituto".
- **Ley 14.250:** la derogación de los arts. 10, 16 y 21 por el art. 211 de la Ley 27.802 es
  correcta, pero el **art. 6 sigue previendo la subsistencia de las cláusulas normativas**
  hasta que entre en vigencia un nuevo convenio.
- **Ley 26.944:** su art. 11 **invita a las provincias a adherir** y **PBA no adhirió**; en
  el fuero contencioso administrativo bonaerense el plazo de 3 años del art. 7 no se toma
  automáticamente. Incorporado en `kb/perfiles/civil-CLAUDE.md` y
  `kb/jurisdicciones/administrativo/administrativo-PBA-CLAUDE.md`.
- **Arts. 2537, 2560 y 2561 CCyCN:** modificados por la **Ley 27.586** (BO 16/12/2020), que
  incorporó al art. 2560 la **imprescriptibilidad de las acciones civiles derivadas de
  delitos de lesa humanidad**.
- **Art. 1275 CCyCN:** no es un plazo para demandar - exige que **el daño se produzca**
  dentro de los diez años de aceptada la obra. Explicitado en `kb/perfiles/civil-CLAUDE.md`.

**Estado judicial de la Ley 27.802 - hitos agregados a la cronología:**

- **07/05/2026:** la CSJN rechazó el per saltum del Gobierno.
- **08/07/2026:** la Sala IV de la Cámara Contencioso Administrativo Federal confirmó el
  rechazo de una nueva cautelar de la CGT sobre 81 artículos.
- El fondo sigue pendiente ante el **JCAF N°12 sin cautelar activa**.
- **Advertencia:** esta cronología **se sostiene solo en fuentes secundarias**, sin fuente
  primaria pública del expediente. Por eso va acompañada de marcador de verificación y no
  debe citarse como dato firme en un escrito.

**Normas nuevas incorporadas a las alertas normativas:**

- **Res. 4/2026 del Consejo Nacional del Empleo** (BO 02/09/2026): nuevo SMVM y prestación por
  desempleo.
- **Res. SRT 39/2026** (BO 02/09/2026): montos RIPTE de las prestaciones de la LRT.
- **RG ARCA 5844/2026** (RIFL) y **RG ARCA 5862/2026** (PER); **Resolución 1276/2026** (Fondo
  de Asistencia Laboral, 12/08/2026).
- **PBA - Ley 15.563** (BO 26/12/2025): redujo del 10% al 5% el aporte adicional sobre la
  tasa de justicia (art. 12 inc. g Ley 6.716).
- **PBA - Ley 15.513** (sancionada 12/12/2024): reforma del proceso de alimentos en el CPCCBA
  (arts. 635 bis notificación por apps, 636 bis alimentos provisorios, 641 Canasta de Crianza
  INDEC).
- **Decreto 409/2026:** según el listado oficial es el **Régimen de Promoción del Empleo
  Registrado**. `kb/perfiles/laboral-CLAUDE.md` lo describía como "moratoria laboral": se marcó con
  `[VERIFICAR VIGENCIA: contenido y denominación del Decreto 409/2026]` en lugar de
  reescribirlo a ciegas.

**Evals corregidos:**

- `evals/laboral-despido-tramos-reforma-pba/` - Ley 11.653 reemplazada por la **Ley 15.057**
  en `caso.md`, `rubrica.md` y `resultado.md` (fuero del encabezado: "Juzgado del Trabajo PBA
  (Ley 15.057)"). El obligatorio sobre el código procesal ahora exige identificar la 15.057 y
  **detectar como error** citar la 11.653. Agregado a los ausentes esperados: no debe citar
  la Ley 11.653 como vigente, ni excluir las horas extras de la base del art. 245.
- `evals/civil-danos-transito-factor-objetivo-pba/` - reescrita la premisa de la
  prescripción. El obligatorio pasa a ser que el sistema advierta que la mediación de la
  Ley 13.951 **no suspende como la nacional**, sino que opera como interpelación del
  art. 2541 CCyCN (seis meses, una sola vez), y que compute sobre esa base: accidente del
  12/05/2023, prescripción del art. 2561 al 12/05/2026, mediación iniciada el 10/03/2026,
  vencimiento corrido a alrededor del **12/11/2026**, de modo que a la fecha de la consulta
  (20/08/2026) **la acción sigue viva pero por poco**. Agregado a los ausentes esperados: no
  debe aplicar el régimen del art. 18 de la Ley 26.589 a una mediación bonaerense. Corregido
  además el obligatorio sobre el art. 64 de la Ley 24.449 (presunciones, no responsabilidad
  objetiva).

**Fuentes de verificación:** InfoLEG, Boletín Oficial de la República Argentina y
normas.gba.gob.ar.

---

### Septiembre 2026 - Auditoría normativa cruzada: art. 25 LNPA, art. 256 LCT, SECLO y locaciones

Auditoría de consistencia interna entre perfiles, skills transversales y glosario. Seis
divergencias corregidas, todas por contradicción entre archivos del propio repositorio:

1. **Art. 25 LNPA - plazo de caducidad.** `kb/transversales/plazos-SKILL.md`, `kb/marcadores-GLOSARIO.md` y
   `kb/transversales/bucles-SKILL.md` citaban 90 días hábiles judiciales. `kb/perfiles/administrativo-CLAUDE.md` ya
   tenía documentada la reforma de la Ley 27.742 (BO 09/07/2024), que duplicó el plazo a
   **180 días hábiles judiciales** para actos notificados desde esa fecha. Corregidos los
   tres archivos, con el deslinde de los plazos locales (CABA 90 días art. 7 Ley 189;
   PBA 90 días art. 18 Ley 12.008) para evitar la aplicación analógica del plazo federal.
   El ejemplo de output completo de `kb/transversales/plazos-SKILL.md` quedó marcado: su aritmética
   corresponde a 90 días sobre un acto de 2025, que hoy tiene 180; se conserva como
   ilustración del método con `[REVISIÓN NORMATIVA REQUERIDA]` para recomputarlo.

2. **Prescripción laboral - art. 256, no art. 258.** El ejemplo canónico del marcador A10
   en `kb/marcadores-GLOSARIO.md`, y su reproducción en `kb/transversales/diagnostico-SKILL.md` y
   `kb/transversales/bucles-SKILL.md`, citaban el art. 258 LCT. El art. 256 es la prescripción bienal de
   los créditos laborales; el art. 258 rige las acciones por accidente de trabajo y
   enfermedad profesional. `kb/perfiles/laboral-CLAUDE.md`, `kb/transversales/plazos-SKILL.md` y `kb/ejemplos/ejemplos-laboral.md`
   ya usaban el art. 256. Unificado al art. 256 con la aclaración del deslinde.

3. **SECLO - dies a quo de la reanudación.** `kb/perfiles/laboral-CLAUDE.md` decía "30 días después de
   la audiencia" en dos puntos; `kb/transversales/plazos-SKILL.md` decía "30 días desde la notificación de
   la clausura" (art. 7 Ley 24.635). Unificado al segundo criterio, que es el del texto
   legal, con cita del artículo.

4. **Corte temporal de la Ley 27.742.** La tabla de transición de `kb/perfiles/laboral-CLAUDE.md`
   ubicaba el corte el 10/07/2024, mientras que todas las reglas sustantivas del mismo
   archivo operan desde el 09/07/2024. Unificado al 09/07/2024.

5. **Actas CNAT 2764/2022 y 2788/2024.** Aparecían en `kb/perfiles/laboral-CLAUDE.md` sin relación
   explícita, lo que se leía como contradicción. Aclarado: son actas distintas - la
   2788/2024 derogó la 2783/2024 y dejó sin efecto la recomendación unificada; la
   2764/2022 (tasa activa con capitalización) fue dejada sin efecto por la CSJN en "Oliva".

6. **Ley 27.737 en locaciones.** `kb/contratos/CLAUDE.md` la daba por derogada en bloque;
   `kb/perfiles/civil-CLAUDE.md` decía que subsiste en lo no derogado. Alineado `kb/contratos/CLAUDE.md`
   a la fórmula conservadora, en tres puntos.

**Casos de verificación agregados:**

- `evals/laboral-despido-tramos-reforma-pba/` - despido sin causa del 15/10/2025 con
  registración deficiente e intimación previa, ante Tribunal del Trabajo PBA. Pone a
  prueba el tramo temporal del art. 245, la derogación de los agravantes de la Ley 24.013
  y de la Ley 25.323, la inaplicabilidad del SECLO en PBA y el cómputo de la prescripción
  crédito por crédito.
- `evals/civil-danos-transito-factor-objetivo-pba/` - peatón embestido, prescripción
  trienal vencida salvo suspensión por mediación prejudicial de la Ley 13.951 PBA. Pone a
  prueba el factor de atribución objetivo frente a un planteo del abogado basado en la
  culpa, la citación en garantía del art. 118 Ley 17.418 y la negativa a cuantificar
  incapacidad sin pericia.

**Agregado:** `skills/derecho-argentino/SKILL.md` - skill destilada de laboral y
civil/comercial PBA, autosuficiente, con las reglas de integridad, los marcadores
canónicos y los anclajes normativos de ambas ramas.

### 14/09/2026 - Auditoría contra fuente primaria: la cadena de cobertura de la medicina prepaga

Se bajaron los textos de las **Leyes 23.660, 23.661 y 24.754** y se leyó la cadena que
`salud-discapacidad.md` 27.5 usaba para sostener que la Ley 24.901 alcanza a las prepagas. El
módulo la afirmaba de memoria; ahora los dos eslabones están cotejados y citados textualmente.

1. **El art. 1 de la Ley 24.754 tiene una fe de erratas que cambia el sentido.** El texto
   publicado el 02/01/1997 decía *"prestaciones obligatorias dispuestas **por** las obras
   sociales"*; la fe de erratas lo corrigió a *"dispuestas **para** las obras sociales"*. No es
   lo mismo: "para" son las obligaciones que se les imponen, que es el piso que se traslada a la
   prepaga; "por" sugeriría que cada obra social las fija. Las fuentes secundarias reproducen el
   texto con el error. Anotado en el módulo como advertencia de transcripción.

2. **El art. 28 de la Ley 23.661 dice más de lo que el módulo le atribuía.** El módulo sólo
   decía que "manda actualizar periódicamente" el programa de prestaciones. El texto además
   exige que dentro de las prestaciones obligatorias *"deberán incluirse todas aquéllas que
   requieran la rehabilitación de las personas discapacitadas"*, más los medicamentos que
   requieran. Es el eslabón que cierra el argumento: **la rehabilitación no es una inferencia,
   está en el texto**. Reescrito 27.5 con las dos citas.

3. **Ley 24.455 sin declarar, y con más adentro de lo que se le atribuía.** El art. 1 de la
   24.754 remite a las Leyes 23.660, 23.661 **y 24.455**, y esta última no estaba en el
   manifiesto. Declarada y bajada. Leída, **son siete artículos**, no los tres del resumen que
   circula, y dos no se deducen de la cadena:

   - **Art. 1**: el piso que se traslada a la prepaga incluye, nominadas, la cobertura de
     tratamientos *"médicos, psicológicos y farmacológicos"* de sida —con las enfermedades
     intercurrentes— y de dependencia de estupefacientes, más los programas de prevención.
     Agregado como tercer eslabón en 27.5.
   - **Art. 2**: los tratamientos de los **arts. 16 a 19 de la Ley 23.737** los cubre la obra
     social del beneficiario y **es el juez de la causa quien debe dirigirse a ella**. `penal.md`
     24.9.2 tenía la tabla de esas tres salidas curativas y el art. 19, pero no decía quién paga.
     Agregado ahí, con reenvío a 27.5 para el caso de la prepaga.
   - **Art. 5**: condiciona la ejecutoriedad de la ley a que haya partida presupuestaria
     específica. Es una defensa disponible para el obligado y el repositorio no tiene precedente
     propio sobre su oponibilidad: queda con `[VERIFICAR CRITERIO DEL FUERO]`, sin afirmar que
     está descartada.

   **No existe texact.htm para la 24.455**: la ficha de InfoLEG (id 14919) ofrece sólo "Texto
   completo de la norma", y las diez normas vinculadas son reglamentarias o complementarias
   —Decreto 580/1995, la propia 24.754, la Ley 25.543— sin reforma del articulado. La URL
   declarada es `norma.htm`.

4. **Un defecto de fuente que ninguna medida detecta.** El texto de InfoLEG titula el art. 1 de
   la 24.455 como *"ARTCULO 1°"*, sin la I. `contar_articulos()` no lo cuenta, y el ojo lo
   completa solo al leer. No es un problema del articulado —es el mismo artículo— pero quien
   transcriba desde el repo copia el error. Anotado como advertencia de transcripción en 27.5,
   con la referencia al BO del 08/03/1995, nro. 28.098, p. 1. Es el tercer defecto de OCR/fuente,
   el de las sustituciones que dejan texto plausible, y se registra leyendo, no midiendo.

**Veredictos de lectura sobre las marcas del descargador.** `revisar_texto()` marcó la Ley
24.754 como "sospechosamente corta": son dos artículos en 1.430 caracteres. Leído el texto, es
la ley entera - el 1 sustantivo y el 2 de forma. Para que un falso positivo así no vuelva a
sonar en cada descarga hasta que nadie lo mire, los veredictos se anotan en
`fuentes/normas/revisiones.json`, indexados por el **texto exacto del problema**: si la norma
vuelve con otro defecto, o si cambia cómo el detector lo redacta, la marca vuelve a sonar. Un
veredicto vale para lo que se leyó, no para el archivo.

### 14/09/2026 - Auditoría contra fuente primaria: las trece normas citadas sin texto

Trece normas estaban citadas **con articulado** en los módulos y no tenían su texto en
`fuentes/`. Se completaron doce URLs oficiales, se bajaron y **se leyeron una por una contra lo
que el módulo afirmaba**. Dos afirmaciones no resistieron la lectura.

**1. La prescripción del SECLO estaba mal, en dos módulos y con la cita equivocada.**
`laboral.md` 5.6 y `plazos.md` decían que el art. 7 de la Ley 24.635 suspende *"hasta 30 días
después de notificada la clausura"*. El art. 7 dice otra cosa: *"Esta presentación suspenderá el
curso de la prescripción **por el término que establece el art. 257 de la ley de contrato de
trabajo**"*, y el art. 257 LCT fija **seis meses como máximo**. Recorrida la ley completa, **el
plazo de treinta días no aparece**: la única mención de "treinta" es el tope del 30% de
honorarios del conciliador.

Una entrada anterior de este documento había "unificado" dos versiones contradictorias del
perfil heredado *al criterio del texto legal*, citando ese art. 7. Eligió una de las dos sin
leer el artículo. Corregido en los dos módulos, con dos marcadores: dónde localizar el plazo de
treinta días si rige, y el conflicto que crea la propia ley al decir **suspenderá** y remitir a
un artículo que dice **interrumpirá**.

**2. El "secreto financiero" del art. 39 de la Ley 21.526 es más angosto de lo que decía
`datos-personales.md`.** El módulo listaba entre las excepciones al consentimiento del art. 5
LPDP "las operaciones de entidades financieras". El art. 39 dice: *"Las entidades comprendidas
en esta ley no podrán revelar las **operaciones pasivas** que realicen"*. **Pasivas**: depósitos.
Las **activas** —los préstamos, y con ellos el historial crediticio— no están alcanzadas, y por
lo tanto tampoco lo está la excepción que la LPDP construye remitiendo a él. Es la distinción
que decide un habeas data contra un informe crediticio. Reescrito, con los cuatro supuestos en
que sí hay que informar aun tratándose de operaciones pasivas.

**3. La adhesión de PBA a la Ley 26.485 no sostiene lo que `familia.md` apoyaba en ella.** El
módulo afirmaba *"PBA adhirió por la Ley 14.407"* y de ahí derivaba que el art. 26 de la 26.485
—con la supresión de contenidos digitales que agregó la Ley Olimpia— rige en la provincia. La
cadena, cotejada: el **art. 1 de la 26.485** exceptúa de su orden público *"las disposiciones de
carácter procesal establecidas en el Capítulo II del Título III"*; **el art. 26 está exactamente
ahí**; el **art. 19** da a las jurisdicciones locales la opción de *"dictar sus normas de
procedimiento o adherir"*, y **PBA dictó las suyas**, la 12.569. Y la **Ley 14.407** no es una
adhesión permanente: declara una **emergencia de dos años** desde el 18/10/2012 y el adherir es
el inciso a) de sus bases. La vía firme en PBA es el **inc. n) del art. 7 de la 12.569**, la
medida urgente residual, con su plazo de 48 horas; en toda la 12.569 no aparece la palabra
"digital".

**4. Dos entradas del manifiesto estaban mal descriptas.** La **Ley 14.407** figuraba como
"Adhesión a la Ley 27.736", y es de 2012: no puede adherir a una ley de 2023. Y la **Ley 15.170**
se declaraba para verificar el alcance de la remisión del art. 32 de la Ley 13.927: leída, es la
**ley impositiva 2020** y su art. 72 es un cuadro de tasas —incluida la **tasa de justicia
administrativa de infracciones de tránsito**—, no una regla de competencia. Los dos marcadores
quedaron cerrados con lo que dice el texto.

**5. La Ley 13.478 no es un pendiente: es un límite.** Es de 1948 e InfoLEG no publica normas de
esa época. Buscada en InfoLEG, argentina.gob.ar y SAIJ. Su marcador ahora dice **por qué** falta
y contra qué cotejar —el Boletín Oficial de 1948 o el texto transcripto en el propio fallo—, en
vez de dejar un pendiente que invite a volver a buscarla.

**Un guardarraíl que faltaba: identidad de lo descargado.** Una de las doce URLs apuntaba a otra
norma. El id 44911 de InfoLEG es el texto ordenado del **Impuesto a las Ganancias**, y quedó
guardado como `ley-21526.txt`, que es Entidades Financieras: 488 KB de articulado impecable, de
otra ley. El descargador no lo marcó porque `revisar_texto()` valida la **forma** —que haya
articulado, que no sea la ficha del portal, que el charset esté sano— y no la **identidad**.
`TestIdentidadDeLasNormas` exige ahora que **el número de la norma aparezca en el cuerpo** del
texto bajado, descontando el encabezado de procedencia, que lo escribimos nosotros con el título
del manifiesto: buscar ahí confirmaría lo que ya creemos y no lo que se bajó. Corre sobre las 127
y es el mismo control que `auditar_fechas_fallos.py` hace con la jurisprudencia — identidad
primero, contenido después.

---

---

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) · [Desarrollar](DESARROLLO.md)
