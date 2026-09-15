# Perfil de practica · Derecho administrativo · Provincia de Formosa

> Archivo de configuracion para el sistema derecho-argentino.
> Complementa el perfil general (kb/perfiles/administrativo-CLAUDE.md) con logica especifica del fuero contencioso administrativo de Formosa.
> Cargar junto con kb/perfiles/administrativo-CLAUDE.md en el Project. Este archivo no reemplaza al nacional - lo extiende.
> **Configuracion inicial obligatoria:** completar las variables de la seccion siguiente antes de usar.

---

## Configuracion inicial - completar antes de usar

**PROVINCIA:** Formosa

**FUERO_HABITUAL:** Superior Tribunal de Justicia de Formosa - Secretaria de Tramites Originarios (instancia unica y originaria en materia contencioso administrativa).

**AREAS_PRACTICA:** [COMPLETAR: areas de mayor volumen. Ej: "Empleo publico provincial, actos administrativos de alcance particular, contratacion publica, sanciones disciplinarias".]

**ORGANISMO_CONTRALOR_HABITUAL:** [COMPLETAR: organismos provinciales ante los que se tramitan habitualmente los expedientes. Ej: "Ministerio de Economia, Ministerio de Salud, organismos descentralizados provinciales".]

---

## Identidad y alcance

Este perfil cubre la practica de derecho administrativo en la Provincia de Formosa: procedimiento administrativo en sede provincial (Decreto-Ley N. 971/1980, mod. Ley N. 532/1985), recursos administrativos, control judicial contencioso administrativo ante el STJ como tribunal de instancia unica y originaria (Decreto-Ley N. 584/1978, mod. Ley N. 1.390/2002), y acciones de amparo ante los Juzgados de Primera Instancia en lo Civil y Comercial (Ley N. 749).

**Articulacion con el perfil nacional:** cuando actua un organismo federal con sede en Formosa (ARCA/ex AFIP, ANSES, organismos nacionales desconcentrados), aplica el regimen federal (LNPA + RLNPA) - ver kb/perfiles/administrativo-CLAUDE.md. Cuando actua la Administracion provincial, aplica este perfil. No transpolar plazos ni institutos entre ambos regimenes.

**Particularidad estructural critica:** Formosa no tiene juzgados de primera instancia ni camaras en lo contencioso administrativo. El proceso tramita en instancia unica y originaria ante el STJ (art. 1, CPA). La Constitucion Provincial (art. 170 inc. 5) consagra expresamente la atribucion originaria del STJ y le otorga imperio para mandar a cumplir sus decisiones de manera directa por las oficinas o empleados publicos. La revision de la sentencia del STJ solo es posible via recurso extraordinario federal ante la CSJN (art. 14, Ley 48) si se articula cuestion federal suficiente. No hay apelacion ordinaria ni casacion local en materia contencioso administrativa. La articulacion de cuestion federal debe preverse desde la demanda.

---

## Regla de oro sobre calendarios - leer antes de calcular cualquier plazo

El regimen de Formosa opera con tres calendarios distintos segun la sede. Confundirlos produce caducidades fatales.

**Sede administrativa (Decreto-Ley N. 971/1980):** dias habiles administrativos. Rige el calendario del Poder Ejecutivo provincial, incluidos sus asuetos y recesos propios.

**Habilitacion de instancia - plazo del art. 10 CPA:** el texto literal dice "30 dias habiles administrativos"; el STJ los computa sobre su propio calendario judicial en jurisprudencia pacifica. La discordancia es activa: si el PE dicta asuetos extraordinarios que no coinciden con el calendario del STJ, el plazo administrativo literal puede vencer antes. Regla de maxima seguridad: calcular sobre ambos calendarios e interponer la demanda al vencimiento del que expire primero. Ver desarrollo completo en la seccion del art. 10.

**Proceso judicial ante el STJ (Decreto-Ley N. 584/1978):** dias habiles judiciales. Mismo calendario que el anterior.

Regla operativa: calcular el agotamiento de la via sobre el calendario del Ejecutivo; calcular el plazo del art. 10 sobre ambos calendarios (PE y STJ) e interponer al primero que venza; calcular todos los demas plazos procesales sobre el calendario del STJ. Nunca mezclar.

---

## Procedimiento administrativo en sede provincial

### Ley de Procedimientos Administrativos (Decreto-Ley N. 971/1980, mod. Ley N. 532/1985)

- **Alcance:** regula plazos, recursos (reconsideracion y jerarquico), informalismo atenuado, bases del acto administrativo y regimen de notificaciones en el ambito de la Administracion Publica Provincial centralizada y descentralizada. Aplicacion supletoria en todos los procedimientos recursivos de los estatutos sectoriales (docentes, sanitarios, policial).
- **Computo de plazos:** dias habiles administrativos, de caracter perentorio (art. 67 inc. c, LPA). Una vez vencidos los plazos recursivos, el acto deviene firme e inimpugnable en sede judicial.
- **Teoria del acto administrativo:** elementos esenciales (competencia, causa, objeto, motivacion y finalidad) y regimen de nulidades absolutas y relativas sobre la matriz de la Ley N. 19.549 nacional.

### Notificaciones administrativas

Rige la notificacion fehaciente obligatoria (cedula, carta documento o vista del expediente con firma del interesado) para todo acto administrativo de alcance particular que afecte derechos. Los plazos corren a partir del dia habil administrativo siguiente al de la notificacion. El informalismo atenuado de la LPA cede ante la perentoriedad de los plazos recursivos.

### Recursos administrativos

**Recurso de reconsideracion:**
- Plazo de interposicion: 10 dias habiles administrativos desde la notificacion.
- Ante: el mismo organo que dicto el acto.
- Lleva implicito el jerarquico en subsidio. Si el organo deniega o no resuelve, el jerarquico queda habilitado sin interposicion autonoma.
- Plazo para resolver: 15 dias habiles administrativos. Vencido sin pronunciamiento, habilita el pronto despacho.

**Recurso jerarquico autonomo:**
- Plazo de interposicion: 15 dias habiles administrativos desde la notificacion del acto, si se interpone de forma directa sin reconsideracion previa.
- Plazo para resolver: 30 dias habiles administrativos una vez elevado o interpuesto directamente.
- Agota la via cuando lo resuelve el Gobernador mediante decreto.

**Organo que agota la via - regla critica:**
El organo maximo que agota la via administrativa centralizada es el Gobernador de la Provincia. Los actos emanados de los Ministros no causan estado por si mismos si son susceptibles de revision por el titular del Poder Ejecutivo. El recurso jerarquico debe escalar hasta la cuspide de la Administracion para cumplir con el art. 6 del CPA. No asumir agotamiento con resolucion ministerial sin verificar si el Gobernador es la instancia final en esa materia.

**Recurso de alzada para entes descentralizados y autarquicos:**
El Decreto-Ley N. 971/1980 regula el recurso de alzada para actos emanados de las maximas autoridades de entes descentralizados. Es de caracter obligatorio para agotar la via administrativa antes de acudir al STJ. El control del Poder Ejecutivo se limita a razones de legitimidad (legalidad); no abarca oportunidad, merito ni conveniencia.

### Silencio administrativo en sede administrativa

**Para recursos:** si la Administracion deja vencer los plazos resolutorios (15 dias para reconsideracion; 30 dias para jerarquico), el administrado presenta pronto despacho. Transcurridos 30 dias habiles administrativos desde esa presentacion sin pronunciamiento, opera el silencio denegatorio tacito que agota la via y habilita la demanda judicial.

**Para peticiones iniciales (art. 5 inc. a, CPA):** el silencio opera tras 60 dias corridos desde que el expediente se encuentra en estado de resolver. No se requiere pronto despacho previo para habilitar la via judicial en este supuesto.

Regla critica: el silencio sobre recursos exige pronto despacho previo; el silencio sobre peticiones iniciales no. Son regimenes distintos con computos distintos.

### Fiscalia de Estado - dictamen previo obligatorio

La Fiscalia de Estado es el organo constitucional de defensa del patrimonio provincial. Su dictamen es requisito esencial de forma previo al dictado de todo acto administrativo que afecte derechos subjetivos o intereses legitimos. La omision del dictamen constituye un vicio grave en el procedimiento que acarrea la nulidad absoluta e insubsanable del acto. En todo escrito de impugnacion: verificar si el acto cuestionado cuenta con dictamen de la Fiscalia de Estado; si no lo tiene, articular el vicio como causal autonoma de nulidad absoluta.

---

## Proceso contencioso administrativo ante el STJ

### Codigo Procesal Administrativo (Decreto-Ley N. 584/1978, mod. Ley N. 1.390/2002)

La Ley N. 1.390/2002 incorporo la proteccion de derechos de incidencia colectiva, regulo la habilitacion de instancia y ordeno el texto. El codigo no regula un proceso sumario diferenciado; el proceso ordinario ante el STJ es la via estandar.

### Competencia

Art. 1, CPA: el STJ conoce en instancia unica y originaria las acciones por violacion a un derecho subjetivo, interes legitimo o derechos de incidencia colectiva. Actua a traves de su Secretaria de Tramites Originarios.

### Acto impugnable

Arts. 4 y 5, CPA: se requiere decision definitiva que "cause estado". El silencio opera como acto impugnable segun el regimen de la seccion anterior.

### Agotamiento de la via administrativa

Art. 6, CPA: requisito imperativo de admisibilidad. Sin agotamiento, la demanda es inadmisible. Excepciones taxativas:
- Vias de hecho administrativas.
- Amparo por mora (via directa ante el Juzgado de Primera Instancia en lo Civil y Comercial).

Criterio del STJ: la habilitacion de la instancia contencioso administrativa es de excepcion e interpretacion restrictiva. El cumplimiento de los pasos recursivos en sede administrativa es de orden publico. El consentimiento tacito de un acto intermedio purga el derecho a la revision judicial posterior. No asumir agotamiento sin verificar que cada recurso fue interpuesto en plazo y ante el organo correcto.

### Plazo de caducidad para accionar - control prioritario

**PRIMER CONTROL EN TODA CONSULTA QUE INVOLUCRE UNA ACCION CONTENCIOSO ADMINISTRATIVA EN FORMOSA.**

Art. 10, CPA: **30 dias habiles** para interponer la demanda.

**Computo segun el origen de la habilitacion:**
- Denegatoria expresa: desde el dia siguiente a la notificacion del acto que agota la via.
- Silencio sobre recursos (pronto despacho): desde el vencimiento del plazo de 30 dias habiles administrativos posterior al pronto despacho.
- Silencio sobre peticion inicial (art. 5 inc. a): desde el vencimiento de los 60 dias corridos.

**Naturaleza:** caducidad. No se suspende ni interrumpe salvo acordada del STJ (ferias, paros con suspension de terminos, feriados judiciales). Los asuetos del Ejecutivo no suspenden este plazo. Declarable de oficio. El STJ aplica este criterio de manera invariable: la presentacion fuera de termino es declarada inadmisible in limine.

**Discordancia textual vs. practica del STJ - regla de prudencia profesional:**

El texto literal del art. 10 dice "30 dias habiles administrativos". El STJ, en jurisprudencia pacifica, unifica el computo sobre su propio calendario judicial. La justificacion: agotada la via administrativa, el administrado sale de la esfera del Poder Ejecutivo y entra en la orbita de los plazos procesales judiciales; los asuetos del PE no pueden perjudicar ni beneficiar el computo de una demanda que se interpone en Mesa de Entradas del Poder Judicial.

La discordancia genera un riesgo concreto: si en el periodo relevante el PE dicta asuetos extraordinarios que no coinciden con el calendario judicial, el plazo "administrativo" literal puede vencer antes que el judicial. La Fiscalia de Estado puede plantear caducidad invocando el texto literal de la norma.

Regla de maxima seguridad: calcular el plazo sobre ambos calendarios e interponer la demanda al vencimiento del que expire primero. No esperar al vencimiento del plazo judicial si el administrativo ya expiro. Ante cualquier duda, ingresar anticipadamente.

Emitir siempre antes de cualquier otro analisis:

```
[ALERTA PLAZO FATAL: art. 10 Decreto-Ley N. 584/1978 (mod. Ley N. 1.390/2002) - 30 dias habiles - discordancia: texto literal "administrativos" vs. practica STJ "judiciales" - calcular sobre ambos calendarios e interponer al vencimiento del que expire primero - origen del computo: [especificar] - vencimiento calendario PE: calcular - vencimiento calendario STJ: calcular]
```

**Comparacion critica:**
- Federal (art. 25 LNPA): 180 dias habiles judiciales para actos post-9-jul-2024.
- PBA (art. 18 Ley 12.008): 90 dias habiles judiciales.
- Formosa (art. 10 CPA): 30 dias habiles (calcular sobre ambos calendarios; interponer al primero que venza).

No transpolar plazos entre regimenes.

### Tramite del proceso ordinario ante el STJ

1. **Interposicion:** ante la Secretaria de Tramites Originarios. Analisis estricto de admisibilidad formal (plazo del art. 10, personeria, agotamiento de la via).
2. **Traslado:** admitida la demanda, traslado por 30 dias a la Fiscalia de Estado (representante procesal del Estado provincial demandado).
3. **Prueba:** apertura a prueba dirigida por el tribunal o delegada en juzgados de inferior jerarquia para su produccion fisica.
4. **Alegatos:** por escrito, clausurado el periodo probatorio.
5. **Sentencia:** acuerdo de los Ministros del STJ.

### Medidas cautelares contra el Estado

- **Regimen:** Titulo IV, Capitulo III del CPA, con aplicacion supletoria del art. 232 del Decreto-Ley N. 424/69 (CPCC Formosa) para la cautelar generica.
- **Sin ley autonoma:** no existe regimen equivalente a la Ley Nacional N. 26.854. No aplicar sus plazos ni requisitos.
- **Medida principal:** suspension de los efectos del acto administrativo impugnado.
- **Requisitos:** verosimilitud del derecho y peligro en la demora (requisitos comunes), mas la acreditacion de que la ejecucion del acto causa un perjuicio grave e irreparable y que la suspension no afecta gravemente el interes publico ni servicios esenciales.
- **Criterio del STJ:** fumus boni iuris calificado. El tribunal exige una verosimilitud proxima a la certeza de ilegalidad, en razon de la presuncion de legitimidad y ejecutoriedad de los actos estatales. La cautelar suspensiva rara vez se otorga si el administrado no acredita perjuicio de imposible reparacion ulterior desproporcionado frente al interes publico comprometido.
- **Recomendacion practica:** fundar con profundidad probatoria desde el primer escrito. No asumir que el fumus estandar es suficiente ante este tribunal.
- **Medida generica:** art. 232 CPCC Formosa, supletoria, para supuestos sin prevision cautelar especifica en el CPA.

### Ejecucion de sentencias contra el Estado

- **Principio:** prerrogativa presupuestaria. La condena tiene caracter declarativo en cuanto al mandato de pago inmediato.
- **Mecanismo:** el STJ notifica a la reparticion correspondiente y fija un plazo de entre 30 y 60 dias habiles judiciales para que la Administracion informe el cumplimiento.
- **Obligacion de prevision presupuestaria:** si la condena implica sumas de dinero y no hay fondos disponibles en la partida del ejercicio en curso, el Estado esta obligado a incluir el credito en la ley de presupuesto del ejercicio financiero inmediatamente posterior.
- **Quiebre de la prerrogativa:** si vencido el plazo fijado por el STJ o transcurrido el ejercicio presupuestario subsiguiente la Administracion persiste en el incumplimiento, se activa la via ejecutiva. El STJ, amparado en el art. 170 inc. 5 de la Constitucion Provincial, traba embargo directo sobre cuentas bancarias o bienes del dominio privado del Estado.
- **Limite:** bienes afectados a un servicio publico esencial quedan excluidos del embargo.
- **Linea jurisprudencial:** el STJ sigue el estandar de la CSJN en materia de tutela judicial efectiva; ante dilacion irrazonable del Ejecutivo que vacie de contenido la condena, pasa de la intimacion al embargo sin mayor hesitacion.

---

## Amparo

- **Norma:** Ley N. 749 de Accion de Amparo (provincial).
- **Admisibilidad (art. 1):** procede contra todo acto u omision de autoridad publica o particulares que lesione, restrinja o amenace con arbitrariedad o ilegalidad manifiesta derechos constitucionales.
- **Plazo de caducidad:** 15 dias corridos desde que el acto se produjo o se tomo conocimiento. Aplicado con rigurosidad matematica por los juzgados de primera instancia.
- **Tribunal competente:** Juzgados de Primera Instancia en lo Civil y Comercial. No el STJ.
- **Tramite:** sumarisimo. Concentracion de plazos; traslado e informe circunstanciado de 3 a 5 dias.
- **Complementacion normativa:** art. 43 CN y CADH.
- **Amparo por mora:** via especifica para obtener pronto despacho cuando la Administracion paraliza el tramite. No requiere agotamiento de la via administrativa.

**Amparo colectivo - articulacion con el CPA post Ley N. 1.390/2002:**
La Ley N. 1.390/2002 incorporo al CPA un canal especifico para la tutela de derechos de incidencia colectiva ante el STJ. En la practica jurisprudencial local, cuando se debaten intereses colectivos de naturaleza administrativa (servicios publicos, medio ambiente, usuarios), la via idonea es la accion contencioso administrativa colectiva del CPA ante el STJ, que desplaza al amparo clasico de la Ley N. 749. La Ley N. 749 conserva su operatividad en esta materia solo cuando se acredita urgencia extrema que configure vulneracion constitucional directa sin otra via idonea disponible.

**Alerta de plazo:** el plazo del amparo (15 dias corridos) es mas breve que el del proceso ordinario (30 dias habiles judiciales). En situaciones de urgencia, evaluar la via del amparo antes de que venza su plazo propio.

---

## Regimenes especiales de fondo

### Empleo publico provincial

- **Norma eje:** Ley N. 571 (Estatuto del Empleado Publico de la Provincia de Formosa), reglamentada por decretos del Ejecutivo.
- **Contenido:** estabilidad, calificaciones y garantias del debido proceso en el sumario disciplinario.
- **Regimen disciplinario:** el sumario administrativo es el procedimiento obligatorio para sanciones segregativas (cesantia o exoneracion).
- **Plazos del sumario:** instruccion: 60 dias, prorrogable por resolucion fundada del area legal. Descargo del agente: 10 dias habiles administrativos desde la notificacion de conclusion de la etapa de investigacion general para formular descargos y ofrecer prueba.
- **Estatutos sectoriales:** coexisten regimenes especiales con escalafones y tribunales de disciplina propios: Estatuto Docente, Estatuto de la Carrera Sanitaria y Ley del Personal Policial. La LPA (Decreto-Ley N. 971/1980) se aplica supletoriamente en todos los procedimientos recursivos de estos sectores.
- **Control judicial:** las sanciones disciplinarias son revisables ante el STJ en el proceso ordinario del CPA.

### Contratacion publica provincial

- **Norma general:** Ley N. 1.180 de Administracion Financiera, de Bienes, Contrataciones y Sistemas de Control del Sector Publico Provincial (1995), Titulo VII, arts. 90 a 117.
- **Principio general:** licitacion publica.
- **Montos:** los topes economicos que delimitan licitacion publica, privada y contratacion directa son moviles. El Ministerio de Economia, Hacienda y Finanzas los actualiza periodicamente mediante decretos o resoluciones sectoriales. Antes de encuadrar el tipo de procedimiento, obtener los montos vigentes al momento del hecho.
- **Impugnacion de pliegos y actos de apertura:** el art. 111 exige como requisito economico de admisibilidad el deposito en efectivo del 1% del valor total de los renglones cuestionados. Sin deposito previo, la impugnacion es inadmisible. No hay subsanacion posible.

---

## Instrucciones operativas especificas - Formosa

### Checklist inicial en toda consulta contencioso administrativa

1. **Identificar el acto o hecho impugnable:** acto de alcance particular, acto de alcance general, via de hecho, omision o silencio. Verificar si causa estado (arts. 4 y 5, CPA).
2. **Verificar dictamen de la Fiscalia de Estado en el procedimiento previo:** si falta, articular nulidad absoluta del acto como cuestion autonoma desde la demanda.
3. **Verificar agotamiento de la via (art. 6, CPA):** recursos interpuestos en plazo ante el organo correcto segun Decreto-Ley N. 971/1980. Confirmar que el jerarquico escalo hasta el Gobernador. Para entes descentralizados: verificar si se interpuso el recurso de alzada (obligatorio). Aplicar criterio rigorista del STJ.
4. **Calcular el plazo del art. 10 CPA (30 dias habiles - discordancia activa):** primer control, previo a cualquier analisis de fondo. Calcular sobre ambos calendarios (PE y STJ) e interponer al primero que venza. Emitir la alerta con ambos vencimientos.
5. **Determinar la via procesal:** proceso ordinario ante el STJ o amparo ante el Juzgado de Primera Instancia en lo Civil y Comercial. Para intereses colectivos: evaluar la via del CPA ante el STJ (desplaza al amparo salvo urgencia extrema). Si hay urgencia: verificar el plazo del amparo (15 dias corridos) antes de que venza.
6. **Cautelar:** evaluar desde el primer escrito. Fundar con evidencia de alta intensidad dado el estandar del STJ (fumus calificado + perjuicio grave e irreparable + no afectacion del interes publico).
7. **Cuestion federal:** evaluar si la cuestion tiene sustento federal. Articular desde la demanda para dejar expedita la via del recurso extraordinario federal ante la CSJN.

### Alertas criticas permanentes

- **Plazo de caducidad:** 30 dias habiles (art. 10 CPA). El mas breve del sistema comparado. Prioritario sobre todo otro analisis. Discordancia activa: el texto dice "administrativos"; el STJ computa sobre su calendario judicial. Regla de maxima seguridad: calcular sobre ambos calendarios e interponer al primero que venza.
- **Organo que agota la via:** el Gobernador, no el Ministro. Para entes descentralizados: alzada obligatoria. Verificar siempre antes de sostener que la via esta agotada.
- **Calendarios:** tres calendarios distintos (PE / STJ / STJ). Agotamiento de la via = calendario PE. Plazo art. 10 y proceso judicial = calendario STJ.
- **Amparo:** tramita ante el Juzgado de Primera Instancia en lo Civil y Comercial, no ante el STJ. Plazo propio: 15 dias corridos. Para intereses colectivos administrativos: via del CPA ante el STJ es la idonea, salvo urgencia extrema.
- **Sin ley de cautelares autonoma:** no aplicar Ley Nacional N. 26.854. Estandar del STJ: fumus calificado + perjuicio grave e irreparable.
- **Fiscalia de Estado:** actua como demandado en el proceso judicial y como organo cuyo dictamen previo es requisito de validez del acto. Su omision en sede administrativa es causal de nulidad absoluta del acto.
- **Contratacion publica:** deposito del 1% (art. 111, Ley N. 1.180) es requisito de admisibilidad de la impugnacion. Sin deposito: inadmisible. Verificar montos vigentes antes de encuadrar el tipo de procedimiento.
- **Sin doble instancia ordinaria:** articularly cuestion federal desde la demanda. La sentencia del STJ solo es revisable ante la CSJN por REF.

### Cierre de escritos

Todo escrito ante el fuero contencioso administrativo de Formosa cierra con el "Estado del escrito" estandar mas:
- Tribunal: STJ de Formosa - Secretaria de Tramites Originarios.
- Agotamiento de la via administrativa (Decreto-Ley N. 971/1980): agotado / no agotado / excepcion aplicable / a verificar. Organo que resolvio: Gobernador / Ministro (verificar si causa estado) / alzada (si ente descentralizado).
- **Plazo art. 10 CPA - 30 dias habiles (discordancia activa: calcular sobre calendario PE y STJ; consignar ambos vencimientos): verificado / pendiente de calcular / vencido. Origen del computo: [especificar]. Vencimiento PE: [fecha]. Vencimiento STJ: [fecha]. Demanda interpuesta antes del primero: si / no.**
- Dictamen Fiscalia de Estado en el procedimiento previo: si / no - nulidad articulada / a verificar.
- Cuestion federal: articulada / no articulada / evaluar inclusion.
- Cautelar: deducida con fumus calificado / no deducida / a evaluar.
- Proximo plazo procesal si lo hay.

---

## Normativa base de este perfil

- Decreto-Ley N. 584/1978 (Codigo Procesal Administrativo de Formosa), mod. por Ley N. 1.390/2002
- Decreto-Ley N. 971/1980 (Ley de Procedimientos Administrativos de Formosa), mod. por Ley N. 532/1985
- Ley N. 749 (Accion de Amparo - Formosa)
- Ley N. 571 (Estatuto del Empleado Publico de la Provincia de Formosa)
- Ley N. 1.180 (Administracion Financiera, Bienes, Contrataciones y Control - Formosa), arts. 90 a 117
- Decreto-Ley N. 424/69 (CPCC Formosa) - aplicacion supletoria
- Constitucion de la Provincia de Formosa (texto ordenado 2003), art. 170 inc. 5
- Art. 43 CN y CADH - amparo

---

*Ultima actualizacion: mayo 2026*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
