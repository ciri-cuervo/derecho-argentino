# 🧾 Bitácora de cambios de estructura

Lo que se hizo sobre el repositorio y no es un cotejo contra fuente primaria: una partición de
módulo, un eval corrido, un registro que se mudó, una herramienta que empezó a mirar algo. Es
**capa 3a, CC BY-SA 4.0** — ver [`LICENCIAS.md`](../LICENCIAS.md). **Cada entrada vale por su fecha**:
el estado vigente está en el archivo que lo explica, y acá queda cómo se llegó.

## Índice

| Fecha | Entrada |
| --- | --- |
| 10/11/2026 | [Las reformas que el consolidado no trae y los módulos que no se enteran](#10112026---las-reformas-que-el-consolidado-no-trae-y-los-módulos-que-no-se-enteran) |
| 09/11/2026 | [Cuatro módulos partidos, treinta evals corridos y las rutas que no se encontraban](#09112026---cuatro-módulos-partidos-treinta-evals-corridos-y-las-rutas-que-no-se-encontraban) |
| 01/11/2026 | [Las series que las calculadoras usaban atrasadas, y el RIPTE desde la página oficial](#01112026---las-series-que-las-calculadoras-usaban-atrasadas-y-el-ripte-desde-la-página-oficial) |
| 01/11/2026 | [Seis evals corridos por primera vez, y lo que reprobaban sin razón](#01112026---seis-evals-corridos-por-primera-vez-y-lo-que-reprobaban-sin-razón) |
| 01/11/2026 | [Una revisión de los scripts: el preaviso, los días trabajados y lo que Windows rompía](#01112026---una-revisión-de-los-scripts-el-preaviso-los-días-trabajados-y-lo-que-windows-rompía) |
| 24/09/2026 | [El config que fijaba el clon, y el aviso que las calculadoras no daban](#24092026---el-config-que-fijaba-el-clon-y-el-aviso-que-las-calculadoras-no-daban) |
| 24/09/2026 | [La versión anterior al lado de la nueva, y los estatutos que el script no frenaba](#24092026---la-versión-anterior-al-lado-de-la-nueva-y-los-estatutos-que-el-script-no-frenaba) |
| 24/09/2026 | [El escrito sale en texto plano, y la hoja de cada jurisdicción tiene su fuente bajada](#24092026---el-escrito-sale-en-texto-plano-y-la-hoja-de-cada-jurisdicción-tiene-su-fuente-bajada) |
| 23/09/2026 | [Dieciséis materias entran como sección, y dos cosas que el corte destapó](#23092026---dieciséis-materias-entran-como-sección-y-dos-cosas-que-el-corte-destapó) |
| 19/09/2026 | [Diez hallazgos de una evaluación en runtime, y lo que cambió](#19092026---diez-hallazgos-de-una-evaluación-en-runtime-y-lo-que-cambió) |
| 18/09/2026 | [El eval de despido, corrido dos veces: bajaron los turnos y tres rúbricas medían mal](#18092026---el-eval-de-despido-corrido-dos-veces-bajaron-los-turnos-y-tres-rúbricas-medían-mal) |
| 18/09/2026 | [Penal se parte en tres](#18092026---penal-se-parte-en-tres) |
| 18/09/2026 | [Medicina legal no era un módulo: eran cinco huecos](#18092026---medicina-legal-no-era-un-módulo-eran-cinco-huecos) |
| 18/09/2026 | [Laboral se parte dos veces: riesgos del trabajo y licencias](#18092026---laboral-se-parte-dos-veces-riesgos-del-trabajo-y-licencias) |
| 18/09/2026 | [El reparto de OCR y las tres fechas salen de la skill](#18092026---el-reparto-de-ocr-y-las-tres-fechas-salen-de-la-skill) |

---

## 10/11/2026 - Las reformas que el consolidado no trae y los módulos que no se enteran

El cotejo de la Ley 15.657 —`AUDITORIAS.md`, misma fecha— dejó cinco defectos de herramienta,
y cada uno tiene ahora su control:

- **`articulo.py` contestaba «no se encontró» para un artículo que el repositorio tenía en otro
  archivo.** `normas.json` declara en cada modificatoria qué norma modifica (`modifica`), y
  `_modificatorias.py` lo lee: si el artículo no está en el consolidado, se busca en sus
  modificatorias y se dice dónde está; si está pero el consolidado no menciona una modificatoria
  declarada, sale un `OJO`. `estado.py` suma el bloque `consolidados` con la misma medida. Al
  encenderla aparecieron seis textos atrasados, no uno. Vueltos a bajar, tres se pusieron al día
  —la 13.927, la 11.683 y el Decreto 1397/79— y tres no se movieron: la 27.799 y los Decretos
  93/2026 y 408/2026 se bajan de `norma.htm`, que es el texto como se publicó y no se actualiza
  nunca. Reportarlos era una alarma que suena siempre, así que `atrasados()` deja afuera los
  originales; `articulo.py` igual avisa al leerlos. Se declararon catorce modificatorias, todas
  leídas en una `nota` del catálogo o en `REVALIDAR.md`.
- **Una reforma se registraba en un módulo y los demás seguían con la regla vieja.**
  `TestUnaReformaLlegaATodosLosModulos`: la modificatoria declara sus `temas` y todo módulo que
  los use la nombra o dice por qué no, y una reforma de «Cambios recientes» no entra sin temas.
  Las cinco los declaran. Con los suyos, la 27.826 mostró tres módulos —`civil.md`,
  `penal-leyes-especiales.md` y `tributario-pba.md`— que usaban *discrepancia significativa* sin
  nombrarla, y ahora la nombran. Leerla entera para escribir sus temas mostró además que sustituye
  el art. 15 de la Ley 25.191, las sanciones del RENATRE. La 25.191 entró al catálogo y se bajó,
  y `laboral-estatutos.md` 5.17 quater recorre sus arts. 15 y 15 bis.
- **La comparación entre dos artículos se hacía a ojo.** `articulo.py --comparar` los alinea por
  la letra del inciso y lo advierte. Se probó alinear por contenido, con una medida de palabras en
  común: sobre el 41 contra el 28 quater se equivocó en cuatro de diez incisos, y en los que
  importaban —dejó sin par el g) 3, antecedente del h) y del i)—. Se descartó.
- **La vigencia de la Ley 15.657 quedó abierta cuando se podía calcular.** `vigencia.py` aplica
  los arts. 5 y 6 CCyCN, leídos de `fuentes/` —del 6, las dos oraciones que hacen la cuenta—, o
  la fecha propia de la norma.
- **El corte de artículos arrastraba el encabezado de la división siguiente**: el 28 quater del
  consolidado terminaba en «TÍTULO X BASES PARA EL PROCEDIMIENTO», y `--comparar` lo mostraba como
  un párrafo más. Medido sobre `fuentes/`, pasaba en 3.791 de 29.648 artículos. La regla tiene
  tres condiciones y cada una salió de un caso que se equivocaba sin ella: la palabra en minúscula
  es prosa; un «Capítulo 2 de este Titulo.» pegado al renglón anterior es una oración partida
  (art. 566 CCyCN); y un encabezado después de dos puntos es lo que el artículo transcribe (art.
  279 de la Ley 27.430, que aprueba el Régimen Penal Tributario).

**Y la misma medida, corrida sobre todo el catálogo, encontró dos bloques que explicaban como
vigente una ley que la 27.802 deroga.** La pregunta fue qué módulos citan una norma reformada sin
nombrar la reforma. Leída entera, la 27.802 toca bastante más que la LCT, la 18.345 y la 27.348
que declaraba. Deroga desde el 01/01/2027 la Ley 14.546 de viajantes y la 27.555 de teletrabajo,
y `laboral-estatutos.md` y `laboral-licencias.md` las explicaban sin decirlo. Además desvincula los
honorarios del perito nacional de la cuantía (art. 61 bis de la 27.423), y `honorarios-nacional.md`
le seguía aplicando el 5% a 10% del art. 21. **El test no lo veía, y no por un error: mide por
módulo.** Los dos módulos laborales nombran la 27.802 en otras secciones, así que una reforma que
llega al módulo y no al bloque da verde. Para una ley ómnibus el control es un piso más bajo que
para una reforma puntual, y lo que lo cubre es leer la ley entera al declararla. El `modifica` de
la 27.802 suma doce normas del catálogo. La 14.546 queda en la `nota` y no en `modifica`: InfoLEG
no anota una derogación diferida, y `estado.py` la reportaría atrasada hasta 2027.

**La 27.799 dio dos más.** `tributario-caba.md` 57.3 explicaba la prescripción del Código Fiscal
porteño sin la remisión del art. 2560 CCyCN a la Ley 11.683, que `tributario-pba.md` sí nombra:
ahora la nombra con la misma reserva. Y `penal.md` 24.11 daba por ausentes de `fuentes/` los
umbrales del Régimen Penal Tributario, que están bajados y desarrollados en
`penal-leyes-especiales.md` 24.9.5. **`deuda_vencida.py` lo había detectado, y el reclamo estaba
aceptado en la línea de base desde la 1.2.0**, en contra de su propio criterio: si la norma se
bajó, se corrige el renglón y no se acepta. Corregido el renglón, la entrada se purgó.

**Y la 27.793 mostró un caso que la herramienta no resolvía.** La Ley 13.478 no tiene texto oficial
descargable, y su art. 9 vigente —la pensión no contributiva— lo transcribe entero el art. 5 de la
27.793, que está bajada. `articulo.py ley-13478 9` cortaba en «No existe». Ahora busca la
transcripción, y el número no alcanzaba: la 27.793 tiene su propio art. 9, y su art. 15 transcribe
otro «Artículo 9º», el de la 24.901. La pista sale sólo del artículo que nombra a la norma pedida
antes de transcribir. `previsional.md` 32.4 quater remitía al art. 2 de la 22.431 sin decir que
la 27.793 cambió su definición, y ahora lo dice.

**Y la 27.348 cerró la tabla.** El art. 4 bis que le incorporó la 27.802 obliga a la jurisdicción
adherida a la *"estricta aplicación"* de la Tabla del Decreto 659/96 y a constituir cuerpos médicos
forenses en noventa días. `laboral-riesgos.md` 5.8.3 trataba el baremo sin decirlo, y ahora lo
dice, con el plazo calculado por `plazos.py` y la duda sobre a quién obliga en un marcador.

**El control por sección se midió y se descartó.** Llevar `TestUnaReformaLlegaATodosLosModulos`
de módulo a sección, a bloque temático y a párrafo dio 14, 34 y 44 candidatos. Ninguno separa el
caso que lo motivó: por sección, el marcador de cierre de 5.17 sexies nombra la 27.802 y tapa el
bloque de viajantes; por bloque y por párrafo, ese bloque sale marcado también después de
corregido, porque la derogación va en el aviso de abajo. Una medida que no distingue el caso
conocido no se calibra. La regla quedó en `DESARROLLO.md`.

**Y la relectura de la línea de base de deuda no encontró otro error como el de `penal.md`.** Las
44 aceptaciones que nombran una sola norma reclaman otra cosa: reglamentación, adhesiones,
fallos citados a través de otro o decretos sin bajar. Sí dejó un vencimiento a la vista: la
emergencia pediátrica de la Ley 27.796 se agotó el 22/10/2026, e InfoLEG no registra prórroga;
`salud-discapacidad.md` 27.2 ter lo dice con la fecha calculada.

Y tres de la verificación anterior: `_piso.py` corta con código 2 debajo de Python 3.9 —antes
corría en 3.8 sin medida detrás, y la regla del `SKILL.md` no tenía señal que leer—; `estado.py`
compara la carpeta de los datos además de la versión, como ya hacían las calculadoras; y el aviso
de datos ajenos sale una vez por corrida.

---

## 09/11/2026 - Cuatro módulos partidos, treinta evals corridos y las rutas que no se encontraban

**Cuatro módulos se partieron por materia**, con el criterio de `DESARROLLO.md` —se parte cuando
el bloque que sale no lo necesita el que se queda— y conservando la numeración:

| Módulo | Salió | Va a |
| --- | --- | --- |
| `laboral.md` | 5.17 quater, quinquies y sexies | `laboral-estatutos.md` |
| `civil.md` | 6.6, 6.7 y 6.8 | `civil-contratos.md` |
| `civil.md` | 6.9, cautelares del CPCCBA | `proceso-pba.md`, que es lo procesal local |
| `consumidor.md` | 17.11.5 bis a quinquies y 17.11.7 | `consumidor-sectores.md` |
| `familia.md` | 18.10, 18.10 ter y 18.10 quater | `familia-ninez.md` |

Una consulta de daños deja de cargar 42 KB, una de despido 21, una de consumo 22 y una de
alimentos 15. El `SKILL.md` bajó de 58 a 54 KB sin tocar lo que sus tests fijan. Para el
disparador de `familia-ninez.md` entró «adopción» al `description` y salió «jurados», que ya
cubren «penales» y su fila de ruteo.

**Veintitrés evals pasaron al formato de `claude plugin eval`** y se corrieron los treinta, con
Sonnet y a una pasada. La primera tanda, con juez Haiku y los dos brazos, costó 17,54 dólares; la
segunda, sólo con plugin y juez Sonnet, 16,65, y cortó por el techo de costo: **cuatro casos
—sucesiones, títulos, tránsito y tributario— quedaron con los graders `llm` sin juzgar** y su
puntaje no es una medición; violencia digital no llegó a lanzarse. Las dos trazas, limpias con `traza_eval.py`.

**Lo que destapó la traza y no el puntaje: las rutas.** En la primera tanda, 36 de 79 `Glob`
volvieron vacíos, en 21 casos, porque `**/laboral.md` se resuelve desde el directorio de trabajo y
no desde el de la skill; en dos casos la respuesta salió sin abrir ningún módulo. El `SKILL.md`
dice ahora que las rutas son del directorio base y que los módulos no se buscan con `Glob`, y en la
segunda tanda hubo 12 `Glob` y 3 vacíos. Entraron además dos reglas: no se responde el fondo sin
abrir el módulo de la fila, y sin shell el script se nombra con el comando armado.

**De las fallas de la primera tanda, las clases fueron cuatro**, leídas una por una contra la
respuesta, el módulo y la norma bajada:

- **El juez**: respuestas que cumplían, reprobadas por Haiku. Es la clase más grande, y la que
  explica buena parte de la mejora de la segunda tanda: el cambio de juez y el de contenido no se
  separan en esta medición.
- **El grader afirmaba más que la norma**: la opción del art. 4 de la Ley 26.773 como
  «irrevocable», el art. 2654 CCyCN —que es de jurisdicción internacional— para una prórroga
  interna, cuarenta y seis días bajo un art. 223 LCT que rige sólo para las sanciones
  disciplinarias, la Ley 22.278 ya derogada por la 27.801. Varios venían de la rúbrica, que se
  corrigió igual.
- **El módulo parafraseaba y dejaba afuera la cláusula que decide**: arts. 2049, 2255 y 1209
  CCyCN, 102 del Decreto-Ley 5965/63, 40 de la Ley 25.164, 223 LCT y el art. 3 de la Ley 15.057,
  que no estaba en ningún módulo. Van ahora textuales.
- **El modelo ignoró lo que el módulo decía**: queda como está, porque el módulo está bien.

**El ruteo pasó a dos niveles.** La sección 16 del `SKILL.md` trae una fila por área y las
transversales, y cada área tiene su tabla en `references/ruteo/` con las filas de antes, sin
reescribir. El `SKILL.md` bajó de 55 a 40 KB, y una consulta lee además la tabla de su área, de 2
a 4 KB. `ruteo.py` y `ramas_sin_disparador.py` leen las tablas de área como parte del router: sin
eso, casi todos los módulos quedaban a distancia 2, alcanzados por `intake.md`, y el control daba
verde sin medir el ruteo. Lo sostienen dos tests de `test_ruteo`, con su mutación.
**El ruteo nuevo se probó con diez consultas cortas de `evals/RUTEO.md`**, una por área y una que
cruza dos, con Sonnet, a una pasada y cortadas en cinco turnos: 1,96 dólares. Las diez activaron
la skill, abrieron la tabla del área antes que el módulo y llegaron al módulo principal esperado.
Las dos que cruzan áreas abrieron uno solo de los dos módulos esperados, y en una abrió las dos
tablas. No hay medición del ruteo de un nivel con la que comparar. Corridas de nuevo, las dos
contestaron con un solo módulo porque la pregunta no pedía más: lo que `RUTEO.md` exigía de R08 y
R46 era más de lo que esas consultas usan, contra su propia regla de que el esperado es «el que la
consulta exige». Las dos esperan ahora un módulo, con la nota de cuándo entra el segundo, y R101
es la consulta que sí exige dos —un pronto pago que hay que filtrar por `laboral.md` 5.3 y topear
con 5.12 bis—. Corrida una vez, R101 abrió las dos tablas y los dos módulos, y la respuesta
filtró las multas derogadas por fecha y topeó cada pago con el SMVM. Las cuatro pruebas costaron
2,85 dólares. El `description` quedó por temas, en su tope de 1.024 caracteres,
porque las palabras que `DISPARADORES` exige por módulo ocupan ya la mayor parte.

**El manifiesto de Claude declara `icon`**, que el validador del directorio de plugins pedía y
toma una sola vez: es `assets/icono.png`, el mismo logo del manifiesto portable.

`articulo.py` no encontraba el art. 102 del Decreto-Ley 5965/63: InfoLEG parte el encabezado en
`Art.` y `102. –`. Se unen antes del corte principal, con su test y su mutación.

---

## 01/11/2026 - Las series que las calculadoras usaban atrasadas, y el RIPTE desde la página oficial

Cargados contra el documento de cada valor: el **jus** de octubre y noviembre (RP-1517/2026), las
**UMA nacionales** de agosto y septiembre (Res. SGA 2372 y 2622/2026), la **UMA porteña** de julio
(Res. SAGyP 500/2026, cuyo art. 2 dice «mayo» por error material, anotado en el CSV), los
**asuetos de noviembre** de PBA (RP-1553/2026) y el **20/10/2026 inhábil** nacional (Acordada CSJN
26/2026). `honorarios_pba.py` y `uma_csjn.py` regulaban con valores de dos meses atrás.

**El RIPTE se completa con la página del organismo** cuando la API no lo trae, y sólo si los meses
comunes coinciden al centavo; lo cubren cuatro tests nuevos, y las dos mutaciones del cotejo se
vieron fallar. **El IPC pasó al CSV del INDEC** (`serie_ipc_divisiones.csv`, nivel general
nacional), que trae septiembre: sobre los 117 meses comunes con la serie anterior, la diferencia
máxima es 5e-4, el redondeo de la API. Un test fija el filtro por región y división.

**Los asuetos de octubre de PBA** (RP-1324 y RP-1495/2026) están escaneados sin capa de texto y se
leyeron en la imagen. **Los feriados de la visita del papa León XIV** (Decreto 1103/2026) se cargaron según
el alcance de cada uno: el 9/11 se descuenta en los dos fueros; el 11/11, en PBA, por el art. 152
CPCCBA; y el 10/11 y el 11/11 se informan sin descontar en el bloque nacional, porque alcanzan sólo
a los tribunales con asiento en esas jurisdicciones (art. 2 RJN).

**`articulo.py` no leía seis textos bajados**, entre ellos el Reglamento para la Justicia Nacional
y la Ley 24.156: numeran `2º —`, `Artículo 1o:` o parten `ARTICULO` en dos renglones. Un corte de
respaldo corre sólo cuando el principal no encuentra nada; la foto de las 280 normas antes y
después muestra que cambiaron esos seis y ninguno más. Con los de noviembre, `plazos.py` imprimía los 54 asuetos distritales del
año en cada cómputo; ahora informa sólo los que caen dentro del plazo.

Dos tests fijaban el estado del corpus —el jus «de agosto» y la fecha de verificación de
inhábiles— y se pusieron rojos por cargar datos nuevos. Ahora comparan contra el archivo.

---

## 01/11/2026 - Seis evals corridos por primera vez, y lo que reprobaban sin razón

Los seis casos migrados al formato de `claude plugin eval` que nunca se habían corrido, con una
pasada por brazo y con Sonnet: los procesos hijos no tenían acceso a Opus. Las doce trazas,
revisadas con `traza_eval.py`: ninguna corrida abrió rúbricas ni graders. Costo total de las dos
tandas y la repetición de `dipr`, del orden de cinco dólares.

| Caso | Primera corrida, con / sin | Después de corregir |
| --- | --- | --- |
| `civil-danos-transito-factor-objetivo-pba` | 1,00 / 0,20 | — |
| `transito-uf-prescripcion-y-art64` | 1,00 / 0,60 | — |
| `previsional-compensacion-de-edad-y-pba` | 0,75 / 0,25 | 1,00 / 0,50 |
| `honorarios-nacional-uma-caba-y-art64` | 0,67 / 0,50 | 1,00 / 0,67 |
| `honorarios-pba-jus-y-etapas` | 0,80 / 0,80 | 1,00 / 0,60 |
| `dipr-prorroga-tacita-y-jurisdiccion-exclusiva` | 0,80 / 0,70 | 0,85 / 0,65, dos pasadas |

**De las cuatro fallas, tres eran del caso y no de la skill**, y se vieron leyendo la respuesta
antes que el puntaje:

- **`previsional`** exigía el contencioso bonaerense para un beneficio del SIPA; ver
  `AUDITORIAS.md`.
- **`dipr`** había quedado atrás del módulo: daba por no bajado un tratado que está en
  `fuentes/` y exigía cerrar la prórroga por el Código; ver `AUDITORIAS.md`.
- **`honorarios-pba`** reprobaba cualquier importe, y la respuesta citaba el jus de la serie con
  su resolución y el marcador, que es lo que pide la rúbrica. El grader exige ahora el marcador
  y no la ausencia de números.

**Y dos defectos de la skill que sólo se vieron en la traza**, los dos al entrar por un comando
en vez de por la skill:

- **El `allowed-tools` de los comandos daba Read y no Glob ni Grep**, y los comandos nombran los
  módulos con ruta relativa: en un modo sin preguntas, `/derecho:honorarios` contestó sin abrir
  nada. Los cinco comandos que leen dan ahora las tres.
- **Un comando no carga el `SKILL.md`**, y las corridas que entraron por `/derecho:honorarios`
  emitieron `[DATO FALTANTE]`, que no existe. Los cuatro comandos de cálculo mandan ahora a
  `marcadores.md`.

---

## 01/11/2026 - Una revisión de los scripts: el preaviso, los días trabajados y lo que Windows rompía

Una revisión del código que se distribuye encontró defectos que las suites no veían: ninguna
fixture cruzaba el umbral. Cada uno tiene ahora su test, y cada test se vio fallar contra el
código anterior: 19 de los 22 nuevos fallaban; los otros tres fijan lo que ya estaba bien.

- **El preaviso de cinco años y seis meses salía de un mes.** El art. 231 inc. b LCT dice «que
  no exceda de cinco (5) años», y el script comparaba años enteros cumplidos. Lo mismo en las
  vacaciones, que además se medían a la extinción y no al 31 de diciembre que fija el art. 150
  in fine. Los dos usan ahora `excede_anios()`.
- **«Días trabajados del mes» ignoraba el ingreso** dentro del mismo mes, y pagaba desde el día 1.
- **`plazos.py` contaba dos veces un trasladable divergente** —el calculado y el verificado— y
  sólo cargaba el año de inicio y el siguiente. Los años se cargan ahora a medida que el
  cómputo los atraviesa, y un plazo no positivo corta.
- **`honorarios_pba.py` ignoraba `--etapas-cumplidas 0`** y una bandera de etapas sin la otra.
- **`bajar()` no reintentaba** un corte a mitad del cuerpo ni un 429 o 5xx, y un `deflate`
  ilegible pasaba como texto.
- **En Windows**: `write_text` traducía los saltos y cambiaba `sha256_archivo` —ahora
  `escribir_texto()`—; `verificar_respuesta.py -` leía stdin en cp1252; y `articulo.py` cortaba
  con los textos que traen caracteres fuera de cp1252, que se midieron en 12 normas bajadas.
- **Un `config.json` ilegible** se leía como vacío y se reescribía encima. Para escribir, ahora
  corta.
- **Las tablas de `fuentes/datos/` se leían sin validar** en cuatro lectores copiados: una
  vigencia `2026-9-1` se ordenaba como texto, un cero dividía y un período repetido pisaba al
  anterior. Las lee ahora `_tablas.py`, que corta con el archivo y el renglón. Los importes de
  `intereses.py` y `honorarios_pba.py` ya no pasan por `float`, que corría el centavo de un
  importe de quince cifras.
- **El CER pasó a bajarse del BCRA.** La copia de datos.gob.ar quedó congelada en octubre de 2024
  y la del RIPTE devolvía la serie vacía; el descargador no pisó nada porque la descarga traía
  menos períodos que el archivo. Sobre los 117 meses comunes, las dos fuentes difieren en menos
  de 5e-5.

Queda abierta una cuestión que no es de código: `antiguedad()` cuenta meses enteros, así que
cinco años, tres meses y un día dan multiplicador 5. Si eso es «fracción mayor de tres (3)
meses» del art. 245 se decide con el texto y la jurisprudencia, no en el script. Hasta entonces
el cálculo no lo decide: emite `[VERIFICAR CRITERIO DEL FUERO: ...]` exactamente en ese caso.

---

## 24/09/2026 - El config que fijaba el clon, y el aviso que las calculadoras no daban

La verificación de la 1.4.2, esta vez corriendo las suites desde un clon, encontró que dejaban
escrito `~/.config/derecho-argentino/config.json` apuntando al clon:

- **`resolver()` fijaba en el config lo hallado por «la skill vive dentro del repo».** El config
  va antes que los datos que trae el plugin instalado, así que una calculadora o la suite corrida
  desde un clon dejaba al plugin leyendo la rama del clon, sin aviso si la versión coincidía.
  Ahora se fija sólo lo adivinado en una ubicación habitual: subir desde `__file__` da lo mismo
  en cada uso. `test_una_corrida_desde_el_clon_no_fija_el_config` lo sostiene.
- **Las suites usaban el config de la máquina.** `_comun_tests.py` les pone un
  `XDG_CONFIG_HOME` temporal, que heredan los subprocesos.
- **Las calculadoras no avisaban.** `datos()` dice por stderr de qué ruta salen los datos cuando
  no son los que trae esa copia de la skill, y por qué se eligió esa.
- **El remedio de `estado.py` era uno solo**, reinstalar, que no borra un config ni desarma una
  variable. Ahora sigue al origen de la raíz.

De paso: `herramientas/cifras.py` saca el `re.sub` del f-string, que con la barra invertida no
compila antes de Python 3.12, y `markdownlint` queda en cero, con las copias de las licencias bajo
`derecho/` excluidas igual que las de la raíz. `evals/README.md` no se tocó: es capa 2.

**Y lo que se distribuye pasa a correr desde Python 3.9**, medido con el 3.9.6 de las
herramientas de Xcode: los scripts ya corrían, y lo único que rompía eran tres módulos de test con
`X | None` sin la importación de `annotations`. El CI corre las suites de la skill en 3.9 y 3.13;
`TestCorreDesdePython39` adelanta ese caso, y no se usa `ast.parse(feature_version=...)` porque
deja pasar los f-strings de 3.12.

**Y en Windows se ejecuta, pero no se desarrolla.** El instalador de python.org deja `python` y
`py`, no `python3`, y todo invocaba `python3`: la skill habría diagnosticado *falta Python* con
Python instalado. La fila nueva de «Si un script no corre» prueba los tres nombres, los comandos
los pre-aprueban y lo dicen, y `TestElInterpreteTieneTresNombres` lo sostiene. Los bloques `!` no
eligen solos: sin una expansión no se puede, y encadenar con `||` volvería a correr `estado.py`
cuando sale con 1. `herramientas/humo_scripts.sh` corre cada script una vez, y el CI lo lanza en
Windows con Git Bash; en Linux, con la salida en cp1252.

---

## 24/09/2026 - La versión anterior al lado de la nueva, y los estatutos que el script no frenaba

Una reevaluación del plugin instalado, de la 1.3.0 a la 1.4.1, encontró cuatro cosas que se
sostuvieron medidas:

- **`_raiz.py` leía los datos de la versión anterior.** Al actualizar, la copia nueva
  (`derecho~g2/`) quedó al lado de la vieja (`derecho/`), y con `CLAUDE_PLUGIN_ROOT` definida el
  bucle de `ENV_PLUGIN` miraba primero la carpeta madre, encontraba ahí un `derecho/` con forma de
  base y lo devolvía. Ahora la madre se reporta sólo si es un clon (`es_clon()`) y la variable
  apunta a su `derecho/`. `test_la_version_anterior_al_lado_no_le_gana_a_la_propia` lo reproduce.
- **`/derecho:estado` no lo podía ver.** Suma el bloque `plugin`, que compara la versión de los
  datos con la de los scripts que corren y da `REVISAR` si difieren; el comando ya no dice que con
  la variable definida no hay nada que revisar.
- **`liquidacion_lct.py` liquidaba estatutos como LCT.** `--regimen` corta con código 2 ante
  casas particulares, construcción, viajantes y encargados, igual que `--empleador publico`, y sin
  el dato la liquidación sale con su marcador. `intake.md` lo pide entre los datos que bloquean.
- **`verificar_respuesta.py` se instalaba y no lo corría nadie.** Estaba en una fila de la tabla
  de scripts y sólo leía archivos, cuando la respuesta vive en el chat. Ahora lee la entrada
  estándar con `-`, y la sección 3 del `SKILL.md` lo pone como paso antes de entregar una
  respuesta con marcadores. `TestElSKILLLoExige` sostiene el paso.

Tres no se tocaron: `evals/README.md` es capa 2; la diferencia entre los dos `plugin.json` es a
propósito y tiene test; y la interfaz de Codex no declara comandos, porque los `/derecho:` son
de Claude Code y Codex entra por la skill.

---

## 24/09/2026 - El escrito sale en texto plano, y la hoja de cada jurisdicción tiene su fuente bajada

**Qué cambió.** La skill no decía en qué formato entregar un escrito, así que cada agente hacía
otra cosa. `escritos.md` 11.1 fija la entrega: en el chat, en texto plano y sin markdown; un
`.docx` o un PDF sólo si el entorno ya puede producirlo, y si no, se dice; "Estado del escrito"
queda fuera de la pieza. El resumen de la sección 11 del `SKILL.md` lo repite en un renglón.

**La tabla de pautas de 11.2 está atada al catálogo.** `TestElEscritoSeEntregaListoParaPegar`
mapea cada fuente que la tabla nombra a su slug en `procedencia.json`, y una fila con una fuente
sin mapear falla. Una pauta de formato es una cifra, y una cifra sin texto bajado no se afirma.

---

## 23/09/2026 - Dieciséis materias entran como sección, y dos cosas que el corte destapó

**Qué entró.** Dieciséis materias, cada una como sección de un módulo existente, con su norma
bajada, su marcador, su fila de ruteo y su renglón en `changelog-normativo.md` y `REVALIDAR.md`:
propiedad horizontal y registro inmobiliario, uniones convivenciales, adopción y niñez,
teletrabajo, jornada, SAS, monotributo, apremio bonaerense, ciberdelitos, régimen aduanero,
contrataciones de la Provincia y de la Nación, demandas y cautelares contra la Nación y el
estatuto policial bonaerense. Las tres de familia absorben filas que `familia.md` 18.8 ruteaba al
perfil heredado. El trinquete de filas de ruteo pasó de 160 a 180.

**El Código Aduanero se baja por títulos.** El «texto completo» de la Ley 22.415 en InfoLEG es un
índice sin un artículo adentro. Quedaron cuatro entradas —`ley-22415-delitos`, `-infracciones`,
`-procedimiento` y `-recursos`— con el número de la ley en el slug, porque el detector de cobertura
lee sólo el slug para saber qué está declarado.

**Los ordinales latinos terminaban en `sexies`.** Tres parsers reconocían hasta ahí, así que `5.17
septies` daba la clave `5.17` y chocaba con la sección `5.17` de otro módulo. Llegan hasta
`decies`, con la mutación en `test_ramas.py`. La Ley 27.411 queda con la marca de «aprobatoria sin
anexo» resuelta a propósito: InfoLEG no transcribe el Convenio de Budapest.

---

## 19/09/2026 - Diez hallazgos de una evaluación en runtime, y lo que cambió

Otra corrida leyó el plugin instalado y reportó diez problemas; cada uno se midió con un comando
y tres no se sostenían como estaban dichos. Lo que sí estaba:

- **Cuatro textos decían que `uma-csjn.csv` estaba vacío** —el párrafo y el marcador enlatado de
  `/derecho:honorarios` y dos lugares de `honorarios-nacional.md`— un día después de cargar la
  serie. De ahí `TestLoQueLaProsaAfirmaDeLaSerie`, que cruza `references/` y `commands/` contra
  los csv.
- **`/derecho:estado` informaba verde sin haber medido**: desde la copia instalada las suites se
  plantan a propósito y el motivo, que va en el primer renglón, se lo llevaba el `tail -3`.
- **El censo de cifras excluía `commands/`** y `/derecho:verificar` decía «son 55 normas» cuando
  eran varios cientos. Los ocho comandos entraron al alcance.
- **La clave de respuestas era legible para el agente evaluado**: `rubrica.md`, `graders/` y
  `resultado.md` viven al lado del caso. `herramientas/traza_eval.py` lee la traza de cada brazo y
  rompe si se abrió una; se planta con rc=2 cuando la traza ya no está.
- **`modelos.md` 23.8 afirmaba que el contenido normativo de los evals estaba verificado.** Un
  `resultado.md` no tiene fila de verificación y no puede vencer: sirven para la forma.
- **La `description` pasó de 1.463 a 1.016 caracteres**, que es el tope de la API de Skills, y el
  control de activación por rama pasó de subcadena a palabra completa.
- **Las cinco licencias viajan adentro del paquete**, byte a byte con la raíz.

Abierto: `evals/README.md` dice que un caso está migrado y son siete, y es capa 2.

---

## 18/09/2026 - El eval de despido, corrido dos veces: bajaron los turnos y tres rúbricas medían mal

`laboral-despido-tramos-reforma-pba`, `with-without`, tres corridas por brazo, antes y después de
escribir la disciplina de lectura en la sección 16 del `SKILL.md`:

| | Antes | Después |
| --- | --- | --- |
| Turnos con la skill | 20 · 25 · 18 → **21,0** | 11 · 18 · 9 → **12,7** |
| Costo por corrida | **US$ 2,30** | **US$ 2,07** |
| Score con la skill | 0,583 | 0,633 |
| Score sin la skill | 0,583 | 0,500 |

Lo único que se mueve más allá del ruido son los turnos: −40%. El score no se puede leer: el
brazo sin skill se movió 0,083 sin que nada cambiara ahí.

**Tres rúbricas medían mal**, y se vio leyendo las respuestas: `base-del-245` pedía excluir el
SAC, que es el texto del art. 51 de la Ley 27.802 para un despido del 15/10/2025;
`no-liquida-multas-derogadas` exigía los agravantes derogados en el cuadro de rubros;
`antiguedad-multiplicador` castigaba cuantificar la diferencia entre la fecha real y la
registrada. Las tres se reescribieron en positivo. `laboral.md` 5.2 no decía cuál era la base para
un despido entre el 09/07/2024 y el 05/03/2026; se escribió 5.2.1.

---

## 18/09/2026 - Penal se parte en tres

`penal.md` prometía régimen aplicable, proceso y ejecución, y dos bloques eran Código Penal: 24.4
—extinción de la acción— y 24.7 —parte general— salieron a `penal-parte-general.md`; nulidades
(24.5) y recursos (24.6) a `penal-impugnacion.md`. **24.3, coerción y libertad, se queda**: está
organizado por el mismo eje que 24.1, qué código rige, y quien pregunta por una preventiva
necesita las dos cosas en la misma lectura.

| Consulta | Antes | Ahora |
| --- | --- | --- |
| Prescripción, probation o parte general | 165 KB | **108 KB** |
| Excarcelación, preventiva o extradición | 165 KB | **108 KB** |
| Nulidad o recurso | 165 KB | **139 KB** |

Después de partir, la pieza más pesada de una consulta penal son los 72 KB del núcleo —`SKILL.md`
con `intake.md` y `marcadores.md`— y no el módulo. El corte destapó dos números de sección repetidos en
`penal.md`, que el control fundía en un `set`; hoy cuenta por archivo.

---

## 18/09/2026 - Medicina legal no era un módulo: eran cinco huecos

El perfil heredado de medicina legal cita dieciséis leyes; trece ya las nombraba algún módulo. Su
columna vertebral es cómo redactar el informe pericial, que es trabajo del perito. Entraron cinco
leyes —26.529, 17.132, 24.655, 27.260 y 24.463— y cinco secciones: `salud-discapacidad.md` 27.4 bis
(historia clínica: copia en 48 horas, guarda de diez años, habeas data por el art. 20),
`previsional.md` 32.4 bis (PUAM) y 32.4 ter (fuero de la Ley 24.655, sin recurso administrativo
previo por el art. 15 de la Ley 24.463), `prueba-pericial.md` 20.1 y la mala praxis en `civil.md`.
De paso, `reformas_no_leidas.py` reclamó que `previsional.md` citaba los arts. 25 y 28 de la LNPA
sin la Ley 27.742: el plazo del art. 25 es hoy de ciento ochenta días hábiles judiciales.

---

## 18/09/2026 - Laboral se parte dos veces: riesgos del trabajo y licencias

`laboral.md` eran 117 KB y una consulta laboral cargaba 199 con el núcleo. Salieron por materia y
no por tamaño, conservando la numeración: **riesgos del trabajo** —5.8, la Ley 24.557, otra ley
con instancia administrativa y baremo propios— a `laboral-riesgos.md`, y **licencias, enfermedades
inculpables y suspensiones** —5.13 a 5.15, el contrato que sigue vivo— a `laboral-licencias.md`.
5.16, principios y orden público, se queda aunque pese 8,2 KB: el art. 15 y el art. 12 pesan en
un despido.

| Consulta | Antes | Ahora |
| --- | --- | --- |
| Accidente de trabajo | ~54k tokens | **~26k** |
| Suspensión o licencia | ~54k tokens | **~29k** |
| Despido sin causa | ~54k tokens | ~45k |
| Despido estando de licencia | ~54k tokens | ~52k |

El corte destapó un hueco: **la homologación del acuerdo ante la Comisión Médica no está cubierta**
—art. 4 de la Ley 27.348—, declarado en el borde con marcador. Y `reformas_no_leidas.py` reclamó ese
art. 4 contra la Ley 27.802: su art. 154 no lo sustituye, incorpora uno nuevo. Veredicto escrito.

---

## 18/09/2026 - El reparto de OCR y las tres fechas salen de la skill

El registro de qué documentos de `fuentes/jurisprudencia/` se transcriben vivía en
`fallos-csjn.md`, que se carga en cada consulta. Queda allá la regla —la fecha sale del registro de
la Secretaría de Jurisprudencia y una cita literal se coteja contra la página— y acá el cómo.

**Las tres fechas.** Los tomos viejos tienen la fecha impresa en la línea que sigue a "FALLO DE LA
CORTE SUPREMA", que no es la del dictamen del Procurador. `auditar_fechas_fallos.py` la lee de ahí
y corrigió tres rellenadas con un 1 de enero:

| Fallo | Decía | Es |
| --- | --- | --- |
| "Fiorentino" 306:1752 | 1984-01-01 | **27/11/1984** |
| "Santa Coloma" 308:1160 | 1986-01-01 | **05/08/1986** |
| "Bazterrica" 308:1392 | 1986-01-01 | **29/08/1986** |

**El reparto.** `calidad_ocr.py` mide la basura de caracteres, que es el único defecto que una
medida detecta; el resto se lee documento por documento, cabecera y una franja del medio, y el
veredicto va a `lecturas-ocr.json`. El repaso del 14/09/2026 cerró sobre 63 documentos: 53 se
transcribían sin más, 4 pedían `-layout` y 6 tenían defecto real, con copia recuperada en `ocr/`.

---

[Volver al README](../README.md) · [Auditorías](AUDITORIAS.md) · [Cómo revalidar](REVALIDAR.md)
