# 🧾 Bitácora de cambios de estructura

Lo que se hizo sobre el repositorio y no es un cotejo contra fuente primaria: una partición de
módulo, un eval corrido, un registro que se mudó, una herramienta que empezó a mirar algo. Es
**capa 3a, CC BY-SA 4.0** — ver [`LICENCIAS.md`](../LICENCIAS.md). **Cada entrada vale por su fecha**:
el estado vigente está en el archivo que lo explica, y acá queda cómo se llegó.

## Índice

| Fecha | Entrada |
| --- | --- |
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
