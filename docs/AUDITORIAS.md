# 📋 Auditorías contra fuente primaria

Registro de las auditorías que este fork corre contra `derecho/fuentes/`: qué se leyó, contra
qué texto, y qué se encontró. Es **capa 3a, CC BY-SA 4.0** — ver [`LICENCIAS.md`](../LICENCIAS.md).

**Una auditoría vale por su fecha**, así que cada entrada la lleva: dice **contra qué texto se
cotejó y cuándo**. Varias anotan además dónde se corrigió lo que encontraron, y se quedan como
están: es parte de lo que se hizo ese día. Lo que no va acá es el cambio sin el cotejo — para eso
están `references/changelog-normativo.md` y `derecho/kb/CHANGELOG.md` —este último es el
historial de la base heredada, capa 2, y la frontera de licencia es la ruta—.

**El orden es de la más nueva a la más vieja, y una entrada no se reescribe.** Si un hallazgo
posterior la supera, se anota **debajo de la entrada**, con su fecha, y la original queda: lo que
se registró es lo que se verificó ese día. Las tres entradas de septiembre entraron en el mismo
commit, así que su orden relativo no sale de una fecha sino de sus referencias internas —la de la
Ley 15.057 cita a la normativa cruzada como anterior—; la de fuentes doctrinarias no tiene ninguna
que la ubique y quedó al final.

Lo que va en cada lugar:

| Qué | Dónde |
| --- | --- |
| Una auditoría de este fork contra fuente primaria | **Este archivo** |
| El estado de verificación por bloque, con fecha y volatilidad | `references/changelog-normativo.md` |
| Un cambio en la base heredada | `derecho/kb/CHANGELOG.md`, y sólo si se tocó `kb/` |
| La versión del plugin | [`CHANGELOG.md`](../CHANGELOG.md), sólo al publicar |

---

## 18/09/2026 - El CPCCBA, que se citaba en catorce módulos y no tenía dueño

**Contra qué se cotejó.** `fuentes/normas/pba-cpccba-7425.txt` y `fuentes/normas/cpccn-17454.txt`,
enfrentados artículo por artículo. **No se citó jurisprudencia.**

**Por qué se leyó.** Medido: el CPCCBA aparece en catorce módulos y `proceso-nacional.md` existía
para el CPCCN sin espejo bonaerense. Excepciones previas y caducidad de instancia en PBA no
estaban en ningún módulo.

**Qué salió.**

- **La caducidad no funciona igual, y decide expedientes.** El **art. 315 CPCCBA** (texto según
  Ley 13.986) sustancia el pedido *"previa intimación por única vez a las partes para que en el
  término de cinco (5) días manifiesten su intención de continuar"*, y el **art. 316** condiciona
  la declaración de oficio a esa misma intimación. El **art. 315 CPCCN** sustancia *"únicamente
  con un traslado"* y el **316** declara de oficio *"sin otro trámite que la comprobación del
  vencimiento"*. **En PBA hay un acto que salva la instancia y en la Nación no.**
- **El art. 310 tampoco coincide.** El bonaerense pone en los tres meses la **Justicia de Paz** y
  los procesos **sumarios**; el nacional pone las **ejecuciones especiales y los incidentes**, que
  el provincial no enumera.
- **Las excepciones previas son el art. 345 y no el 347.** El art. 347 del CPCCBA es otra cosa: el
  requisito de admisión. Es el número el que engaña, no el instituto.
- **El deber de fundar sí coincide**: art. 34 inc. 4 en los dos códigos, mismo número y mismo
  texto. Junto con el art. 29 inc. 4 de la Ley 189 —mismo texto, otro número— completa el mapa de
  dónde se cita bien y dónde se cita mal.

**Y el arancel de PBA salió de donde no correspondía.** La Ley 14.967 vivía como sección 1.6.6 de
`sede-judicial-pba.md`, que es del fuero laboral, cuando es la ley arancelaria de **toda** la
justicia bonaerense y sus hermanas —Leyes 27.423 y 5.134— ya tenían módulo. Pasó a
`honorarios-pba.md`, **conservando el número 1.6.6**: la numeración de este repositorio es global
y no se renumera.

---

## 18/09/2026 - La sentencia en la justicia nacional y en el fuero CAyT porteño

**Contra qué se cotejó.** `fuentes/normas/cpccn-17454.txt`, `fuentes/normas/ley-18345.txt` y
`fuentes/normas/caba-ley-189.txt`, artículo por artículo, leídos del texto consolidado. **No se
citó jurisprudencia**: lo que necesita precedente quedó marcado en los módulos.

**Qué se leyó y qué salió.**

- **El art. 155 de la Ley 18.345 lista al art. 163 del CPCCN.** La pregunta que abrió la lectura
  era si el contenido de la sentencia laboral nacional sale de la Ley 18.345 o del CPCCN, y la
  respuesta no es "por analogía" ni "por supletoriedad genérica": el art. 155 enumera los
  artículos aplicables uno por uno, y adentro están los **arts. 160, 161, 163, 164 y 165** y el
  **art. 34 incs. 2, 4, 5 y 6**. De ahí que el civil y el laboral nacionales compartan pieza, y
  que `sede-judicial-nacional.md` sea **uno solo** y no dos.
- **Lo que la Ley 18.345 no cede son los plazos recursivos.** El art. 155 **no** lista el art. 244
  CPCCN. Apelar la definitiva son **seis días con los agravios adentro** (art. 116), la
  interlocutoria **tres días sin fundar** (art. 117), y sin agravios el recurso **se deniega sin
  más trámite** (art. 118). Informar los cinco días del art. 244 en este fuero es error.
- **El deber de fundar cambia de número y no de texto.** Art. 34 inc. 4 CPCCN y **art. 29 inc. 4
  de la Ley 189** dicen lo mismo, palabra por palabra, incluido *"bajo pena de nulidad"*. Es el
  error de cita más difícil de ver leyendo, porque la frase citada es exacta.
- **El art. 147 de la Ley 189 no es el art. 163 del CPCCN con otro número.** Tres diferencias
  salieron del cotejo: el **inc. 5 exige la valoración de la prueba** como contenido escrito,
  donde el CPCCN pide sólo "los fundamentos y la aplicación de la ley"; el mérito de los hechos
  sobrevinientes es **inciso autónomo** (inc. 7) y no un párrafo del de la decisión; y el **inc. 8
  remite al art. 397** para el plazo de cumplimiento cuando la condenada es la autoridad
  administrativa, que no tiene equivalente nacional.
- **El art. 148 condiciona los daños a que hayan sido reclamados.** Es congruencia escrita en el
  código del fuero, y quedó como el nudo del caso de prueba porteño.

**Qué quedó sin cerrar.** El régimen de notificaciones electrónicas de los dos fueros —acordadas
de la CSJN, resoluciones del Consejo de la Magistratura porteño— **no está bajado**, así que
desde cuándo corre un plazo va con marcador y no con fecha. Y ningún estándar de nulidad por falta
de fundamentación se afirmó: sin fallo leído, marcador.

---

## 18/09/2026 - Incorporación de cinco normas nuevas, y dos resultados que contradicen su origen

Segunda tanda de la revisión que abrió la auditoría del régimen penal juvenil. Cinco textos
bajados de InfoLEG y del registro provincial bonaerense, con procedencia y hash, y cotejados
antes de escribir una línea.

**Ley 27.799, Régimen Penal Tributario.** El repo ya razonaba sobre ella en `civil.md` 6.3 sin
tener el texto, y por eso `tributario.md` 33 arrastraba un marcador de monto sobre el umbral del
art. 1. **Ese marcador se cerró contra fuente**: son cien millones de pesos. Los doce umbrales del
Título IX quedaron escritos con su unidad de cómputo, verificados uno por uno contra el
consolidado de `ley-27430.txt`, que ya los trae con la nota de sustitución al pie de cada
artículo. Se incorporó además su reglamentación, el Decreto 93/2026.

**Ley 27.786, organizaciones criminales.** Dos tipos penales nuevos —arts. 210 ter y 210 quáter
CP—, autónomos de la zona especial por su art. 9, y en los dos el texto **desactiva expresamente
los arts. 46 y 47 CP**. Las seis facultades del art. 6 quedaron tabuladas por quién autoriza cada
una, que es donde se juegan las nulidades.

**Ley 25.520 en texto actualizado, con el Decreto 941/2025.** Medido contra el texto: las cinco
prohibiciones del art. 4 siguen, **cuatro tienen excepción nueva y la única que quedó entera es el
inciso 3** —no producir inteligencia por raza, fe, opinión política, pertenencia sindical o
partidaria, ni por actividad lícita—. El art. 10 nonies habilita al personal de inteligencia a
aprehender personas. Queda marcado que es un DNU que reforma una ley del Congreso y que su trámite
ante la Comisión Bicameral no está verificado.

**Ley 27.796, emergencia sanitaria pediátrica.** Nació por insistencia de ambas cámaras con dos
tercios, y el propio texto de InfoLEG trae la comunicación del Senado que lo acredita. Lo
determinante no es su contenido sino su plazo: **se declaró por un año desde el 22/10/2025**.

**Dos resultados que contradicen la hipótesis con la que se empezó.** El informe que motivó la
revisión atribuía a la Ley 15.557 de PBA un efecto sobre el cobro de deudas; leído el texto
completo, **la emergencia que declara no suspende ejecuciones, no declara inembargables los fondos
públicos ni consolida deuda**, y eso se registró como negativo en `contencioso-pba.md` 26.9 bis,
porque la inferencia contraria es automática. Y de las leyes que ese informe presentaba como
novedad, la 27.784 y la 27.785 **ya estaban cotejadas** en `penal.md`. El material sirvió para
elegir dónde mirar; lo que decidió cada punto fue el texto oficial.

## 18/09/2026 - Auditoría contra fuente primaria: la Ley 22.278 está derogada y tres módulos la daban por vigente

**Ley 27.801 de Régimen Penal Juvenil**, bajada de InfoLEG (id 423722) con procedencia y hash en
`fuentes/normas/ley-27801.txt`, y cotejada artículo por artículo. **Su art. 48 deroga la Ley
22.278 y sus modificatorias**; su art. 52 difiere la vigencia a los ciento ochenta días de la
publicación en el Boletín Oficial, que fue el 09/03/2026, de modo que **rige desde el 05/09/2026**.

La sección 24.9.4 de `penal-leyes-especiales.md` describía el régimen de la 22.278 —no punibilidad
por debajo de los dieciséis, punibilidad de dieciséis a dieciocho, los tres requisitos
acumulativos del art. 4 para imponer pena— y se reescribió entera sobre la ley nueva.

**Dos hechos medidos contra el texto, no recordados.** La ley alcanza a los adolescentes **desde
los catorce años**, donde la anterior empezaba en los dieciséis: el universo de punibles se
amplió sin que cambiara una coma del art. 32 de la Ley 13.634, que remite a "la legislación
nacional" sin nombrarla. Y el texto de la 27.801 **no contiene ninguna remisión al art. 44 CP ni
a la escala de la tentativa**, comprobado por búsqueda sobre el archivo: ése era el vehículo legal
del primer holding de *"Maldonado"*, Fallos 328:4343, que `penal.md` 24.7.8 citaba sin condición.

**El texto derogado no se da de baja.** El art. 2 CP manda aplicar siempre la ley más benigna, y
para un hecho anterior al 05/09/2026 cometido por alguien de catorce o quince años la 22.278 lo
declaraba no punible. `ley-22278.txt` queda en `fuentes/` porque es lo que permite cotejar de qué
lado cae cada caso, y los tres módulos ahora preguntan primero la fecha del hecho.

**Lo que queda abierto y está marcado**: el decreto reglamentario, que no está cargado; la
adecuación procesal de la Provincia de Buenos Aires, que el art. 49 invita y no impone; y la
suerte de la doctrina de *"Maldonado"* sin la remisión derogada, que no tiene precedente bajado.

**Corrección de origen.** La hipótesis de trabajo que disparó esta auditoría venía de un informe
generado con un modelo de lenguaje, no de una fuente. De su listado, dos leyes que figuraban como
novedad —la 27.784 de juicio en ausencia y la 27.785 de reincidencia y reiterancia— **ya estaban
cotejadas** en `penal.md` 24.2.1 y 24.3.1, y un pasaje suyo sobre el estado cautelar de la Ley
27.802 contradecía lo que `laboral.md` 5.1 tiene verificado con fechas. El informe sirvió para
elegir dónde mirar; lo que decidió cada punto fue el texto oficial.

## 17/09/2026 - Auditoría contra fuente primaria: dos textos ordenados de 2025 y tres números de norma mal atribuidos

Se bajaron y leyeron las normas de dieciséis materias que ningún módulo cubría. Lo que sigue no
es el contenido —eso está en `references/changelog-normativo.md`, fila por fila— sino **lo que la
lectura desmintió**.

1. **Los textos ordenados de 2025 renumeraron el gas y la electricidad, y nadie lo tenía escrito.**
   El **Decreto 451/2025** (B.O. 07/07/2025) aprobó la *"Ley N° 24.076 - T.O. 2025"* y el
   **Decreto 450/2025**, del mismo día, el de la Ley 24.065. La jurisdicción previa del ente pasó
   del **art. 66 al 53** en gas y del **art. 72 al 58** en electricidad.

   Se detectó leyendo *"Y.P.F. S.A. c/ ENARGAS"* (CSJN, 29/09/2015), que cita el art. 66 para el
   texto que el consolidado numera 53. **El corrimiento no es parejo**: los arts. 9 y 14 conservan
   su número, así que no se puede restar. Y **ninguno de los dos decretos publica tabla de
   correspondencia**: el mapeo se establece leyendo. Toda cita anterior a julio de 2025 —incluidas
   las notas de InfoLEG al pie— usa la numeración vieja.

2. **Tres números de norma estaban mal atribuidos, y dos venían de confundir decretos del mismo
   número.**

   - **El baremo es el Decreto 659/96, no el 658/96.** El 658 es el **listado de enfermedades
     profesionales**; el 659 es la **Tabla de Evaluación de Incapacidades**. El perfil heredado
     decía *"baremo del Decreto 658/96"* y la columna de contradicciones de `laboral.md` no
     corregía el número. Corregido, y el 658 bajado: son 187 entradas «AGENTE:».
   - **La reglamentación de la Ley 27.636 es el Decreto 659/2021, no el 721/2020.** El 721 es
     **anterior a la ley** y fijó el cupo del 1% por decreto. Mismo número que el baremo, otro año.
   - **El art. 63 LDC sigue vigente porque su derogación fue vetada.** El art. 32 de la Ley 26.361
     lo derogaba, y el **art. 1° del Decreto 565/2008** —publicado el mismo día— lo observó. La
     **Resolución 344/2009 de Diputados** declaró la validez del decreto. Un texto que liste el
     art. 63 como derogado invierte la prelación del transporte aéreo.

3. **El baremo vigente NO está completo en texto, y la diferencia importa.** El Anexo I del 659/96
   sustituido por el **Decreto 549/2025** está en `fuentes/` en prosa, con los porcentajes que
   enuncia en línea. **Las tablas no**: donde el anexo dice *"deberá determinarse utilizando la
   siguiente tabla"*, la extracción no trae nada, porque son imágenes.

   **No se suplen con OCR**, y está medido: de las **25 correcciones** que dejó el cotejo página
   por página de "Fiorentino", **14 cambian dígitos**, y una convirtió `art. 6°` en `art. 62`. En
   prosa el idioma delata la sustitución; en una tabla de porcentajes no hay nada que la delate.
   Los valores se piden o se marcan.

4. **Ninguna fuente oficial bloquea a los descargadores.** El repositorio documentaba en seis
   lugares que InfoLEG, `normas.gba.gob.ar` y SAIJ devuelven 403 a los agentes. Medido con
   `diagnostico.py` y con `verificar_normas.py`, que no escribe nada: **los seis sitios responden
   HTTP 200**, incluido SAIJ. Lo que sí se confirmó es que el buscador de SAIJ **no se consulta
   por query string** —devuelve *"SIN RESULTADO"* sin rechazar la consulta, que es el peor modo de
   falla—. Corregidos los seis renglones, y lo de JUBA y los sumarios de la CSJN quedó intacto:
   eso no es un 403 sino postback de ASP.NET y estado de sesión.

## 16/09/2026 - Lectura de imagen: las 27 páginas de "Fiorentino" y dos erratas del tomo

El PDF de **"Fiorentino, Diego Enrique"** (Fallos 306:1752) trae la capa de texto arruinada, así
que lo que hay en `fuentes/jurisprudencia/ocr/` es una relectura de las imágenes con tesseract.
Se leyeron **las 27 páginas una por una contra la imagen ampliada**, y el resultado está
declarado como dato en `ocr/correcciones/csjn-fiorentino-fallos-306-1752.json`: **25
correcciones**, que el script vuelve a aplicar en cada regeneración.

**Lo que más importa de esta lectura no son las correcciones, son las dos que NO se hicieron.**

Había seis secuencias que parecían defectos de OCR. Cuatro lo eran: `regisiro` por «registro»,
`setiva` por «sativa» —`cannabis sativa` va en cursiva y el OCR lee la `a` como `e`—,
`consintendo` por «consintiendo», y dos volados de ordinal leídos como dígito, uno de los cuales
convertía el **art. 6° de la ley 20.771 en «art. 62»**: un número de artículo cambiado, que es
la peor clase de error que puede tener una transcripción.

Las otras dos son **erratas del tomo impreso**, y se transcriben como están:

| Página del PDF | Impresa | Lo que dice | Lo correcto sería |
| --- | --- | --- | --- |
| 11 | 1762 | `la defensa inpugnó el aludido` | «impugnó» |
| 13 | 1764 | `donde vvía de modo permanente` | «vivía» |

La de la pág. 11 se confirma con el propio volumen: el mismo pasaje, en el voto del doctor
Petracchi (pág. 15, impresa 1766), imprime «impugnó». O sea que el tomo se contradice a sí mismo
y la errata está en el primer voto, no en nuestra lectura.

**Se anotan porque, si no, la próxima lectura las "arregla".** Una transcripción reproduce el
documento; corregirle la ortografía al tribunal la convierte en otra cosa. Van declaradas en
`no_corregidas` del mismo archivo, con su motivo, y `herramientas/test_reocr.py` exige que
sigan textuales en el `.txt`.

---

## 14/09/2026 - Auditoría contra fuente primaria: la cadena de cobertura de la medicina prepaga

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

## 14/09/2026 - Auditoría contra fuente primaria: las trece normas citadas sin texto

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

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) · [Desarrollar](DESARROLLO.md)

## Septiembre 2026 - Auditoría contra fuente primaria: Ley 15.057, mediación PBA, intereses y art. 245

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

   > **Superado el 18/09/2026, y la entrada queda como registro de lo que se verificó ese día.**
   > Decir que la 11.653 conserva ultraactividad *"solo en materia de recusación"* no es lo que
   > rige: en las causas **con audiencia de vista ya celebrada** sigue aplicándose **entera**, y
   > por eso **conviven dos regímenes**. Está así en `.claude/rules/derecho-argentino.md`, que
   > carga siempre, y en la tabla de `sede-judicial-pba.md` 1.6. Lo que esta entrada sí fijó y
   > sigue en pie es que el art. 88 de la Ley 15.057 derogó la 11.653 y que el corte lo hace la
   > Res. SC 1840/2024 por la audiencia de vista.

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

## Septiembre 2026 - Auditoría normativa cruzada: art. 25 LNPA, art. 256 LCT, SECLO y locaciones

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

## Septiembre 2026 - Incorporación de fuentes doctrinarias: CCyC Comentado y derecho de daños

Dos obras de referencia sumadas al repositorio, con tratamiento distinto según su licencia.

**Código Civil y Comercial de la Nación Comentado (SAIJ-INFOJUS, 2ª ed. actualizada 2022).**
Directores: Marisa Herrera, Gustavo Caramelo y Sebastián Picasso. Publicación de distribución
gratuita del Ministerio de Justicia y Derechos Humanos, de libre reproducción total o parcial
citando la fuente. Los seis tomos se incorporan completos en `derecho/fuentes/ccyc-comentado/`
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
se agrega `derecho/kb/doctrina/civil-DOCTRINA-danos.md`, un índice doctrinario con 38 entradas por
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

**Regla nueva de higiene del repositorio.** Se agrega `derecho/fuentes/_local/` al `.gitignore`:
es la carpeta donde el abogado guarda su ejemplar de obras comerciales, que nunca se commitean.
El criterio: una obra entra al repositorio solo si su propia licencia lo permite. Las que no,
entran como doctrina destilada con remisión, nunca como texto.

---
