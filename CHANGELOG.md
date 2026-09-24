# Changelog

Historial de **versiones** del plugin. Formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado [SemVer](https://semver.org/lang/es/).

Lleva versiones, no sesiones de trabajo, y **cada entrada va corta**: una línea de encuadre y
un renglón por cambio. El detalle de cada uno vive donde se puede verificar:

| Qué | Dónde |
| --- | --- |
| Qué cubre cada módulo y cómo está armado el repo | [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) |
| Cuándo se verificó cada instituto contra fuente primaria, y su volatilidad | `derecho/skills/derecho-argentino/references/changelog-normativo.md` |
| Qué hay cargado en la capa offline | `derecho/fuentes/MANIFIESTO.md` |
| La doctrina de cada precedente | El módulo que la usa; el índice, en `references/fallos-csjn.md` |
| Si el texto de un fallo se puede transcribir | `herramientas/lecturas-ocr.json` |

## [1.4.3] — 2026-09-24

Correcciones: no entran normas ni fallos, y ningún cálculo cambia de resultado.

- **El plugin instalado ya no lee los datos de un clon**: correr una calculadora o la suite desde
  el repo dejaba el clon fijado en el config. Si los datos no son los de la propia copia, las
  calculadoras lo avisan, y `/derecho:estado` da el remedio según la causa.
- **Los scripts corren desde Python 3.9 y en Windows**, donde el comando puede ser `python` o
  `py -3`: los comandos autorizan los tres. El CI corre cada script en Linux y en Windows.

## [1.4.2] — 2026-09-24

Correcciones de una reevaluación del plugin instalado: no entran normas ni fallos, y ningún
cálculo de la LCT cambia de resultado.

- **Los scripts ya no leen la versión anterior** cuando queda al lado de la nueva después de
  actualizar. `/derecho:estado` avisa si los datos y los scripts son de versiones distintas.
- **`liquidacion_lct.py --regimen`** corta con código 2 ante casas particulares, construcción,
  viajantes y encargados de edificio, que se liquidan por su estatuto.
- **`verificar_respuesta.py` es paso obligatorio**: lee la respuesta por la entrada estándar y
  la sección 3 del `SKILL.md` lo exige antes de entregar una respuesta con marcadores.
- Textos: la descripción de `/derecho:honorarios` nombra la UMA, y el `--help` de
  `verificar_normas.py` ya no trae una cifra vieja.

## [1.4.1] — 2026-09-24

Cómo se entrega un escrito, y qué exige cada jurisdicción sobre la hoja.

- **El escrito sale en el chat, en texto plano y sin markdown**, listo para pegar; un `.docx` o
  un PDF, sólo si el entorno puede producirlo. "Estado del escrito" va fuera de la pieza.
- **Pautas de formato con su fuente bajada**: PBA, Nación, CSJN, TSJ porteño, Santa Fe y
  Tucumán, en once textos nuevos. Un test ata cada fila de la tabla a su norma descargada.

## [1.4.0] — 2026-09-23

Veinticuatro materias nuevas cotejadas contra su texto, los reglamentos que faltaban leídos, y la
documentación del repositorio a la mitad.

- **Materias nuevas, cada una como sección con su norma bajada y su marcador:** casas
  particulares, construcción, viajantes y encargados, jornada y teletrabajo; jurados en PBA,
  trata, ciberdelitos y régimen aduanero; propiedad horizontal, registro inmobiliario, uniones
  convivenciales, adopción y niñez; SAS, monotributo, tarjeta de crédito y asignaciones
  familiares; procedimiento administrativo, contrataciones y apremio bonaerenses, estatutos del
  empleo público y de la policía de PBA; recursos, contrataciones, demandas y cautelares contra
  la Nación.
- **Siete reglamentos leídos** que las secciones declaraban faltantes: los de contrataciones
  nacional y bonaerense, el del estatuto policial, el del teletrabajo, el de la Ley 11.683 y las
  Leyes 23.982 y 11.672 para cobrar una condena contra la Nación.
- **Jurisprudencia bajada de JUBA y leída del texto completo:** el pago previo en el contencioso
  bonaerense, el silencio del asegurador, la competencia del Juzgado de Paz tras el divorcio y el
  método de la compensación económica. Las búsquedas sin resultado quedaron fechadas en su
  marcador.
- **`articulo.py`** devuelve un artículo de una norma bajada con su procedencia: `Read` trunca a
  2.000 renglones sin avisar y el CCyCN tiene 27.000.
- **El Código Aduanero se baja por títulos**, porque el texto completo de InfoLEG es un índice.
- **Verificación semanal en CI:** `verificar.yml` vuelve a pedir cada norma los lunes y abre un
  issue si alguna cambió o no se pudo mirar. Formularios de issue: el error de derecho pide la
  fuente.
- **README:** cómo trabaja un turno, una transcripción con el número que no da, y qué hacer si
  algo no anda. El armado del proyecto, en `docs/PROYECTO.md`.
- **`docs/` reescrito:** `DESARROLLO.md` queda con las reglas y los comandos; `AUDITORIAS.md`,
  `BITACORA.md` y `REVALIDAR.md` conservan cada entrada con lo que se cotejó y lo que salió.
- **`SKILL.md` más corto**, y tres guardarraíles nuevos: los ordinales latinos hasta `decies`, la
  `Ü` en toda clase de letras, y el sufijo de una sección en la clave de su rama.

## [1.3.1] — 2026-09-18

Menos contexto por conversación y menos decisiones que tomar a ciegas: no entran normas ni fallos.

- **El `description` de la skill entra en el tope de la API** —1.024 caracteres— sin apagar
  ninguna rama: un test exige un disparador por módulo.
- **La disciplina de lectura de la sección 16**: un módulo se lee una vez y entero, y abrir otro
  se decide antes, nombrando qué pregunta contesta.
- **La serie de la UMA nacional está cargada**, y `uma_csjn.py` devuelve el valor con la
  resolución que lo fijó; fuera del tramo cargado se planta.
- **Los comandos invocan por `CLAUDE_PLUGIN_ROOT`**: son sólo de Claude Code y ya no fingen
  otro agente.
- **`traza_eval.py`**: lee la traza de una corrida de `claude plugin eval` y dice qué archivos
  abrió el modelo y en qué orden, que es lo que las rúbricas no ven.

## [1.3.0] — 2026-09-18

Siete módulos nuevos, y los dos más grandes partidos por materia.

- **Módulos nuevos:** violencia digital, notarial y **justicia de paz de PBA**.
- **`laboral.md` y `penal.md` se partieron**: riesgos, licencias, impugnación y parte general
  salieron con su numeración.
- **Derecho internacional:** exequátur, inmunidad de jurisdicción, arbitraje, Viena, extradición.
- **También:** PUAM, historia clínica, boleto de compraventa, interversión del título.

## [1.2.0] — 2026-09-17

- **JUBA y el buscador de sumarios de la CSJN se consultan**, con la cadena escrita en `INDICE.md`.
- **Dieciséis ramas nuevas** entraron como sección de un módulo que ya existía, con su disparador.
- **Los textos ordenados de 2025 renumeraron gas y electricidad:** la jurisdicción previa del ente
  pasó del art. 66 al 53 y del art. 72 al 58, y el corrimiento no es parejo.
- **Los datos se repiten antes de usarlos** y la skill para si alguno no coincide.
- **Identidad de los fallos:** el descargador coteja la carátula contra el documento y la registra.
- **El cotejo del OCR es un dato:** vive en `ocr/correcciones/` y se planta si deja de coincidir.
- **Políticas de género:** ocho leyes bajadas y escritas en siete módulos.
- **Herramientas nuevas:** ortografía con diccionario, mapa de ruteo y verificador de marcadores.

## [1.1.1] — 2026-09-15

Procedencia y rutas internas: no entran normas ni fallos nuevos y ningún cálculo cambia de
resultado. **No hay nada que reinstalar.** Cada archivo bajado se coteja contra su propio hash sin
salir a la red, y de un fallo de JUBA se guarda la sentencia y no la página entera.

## [1.1.0] — 2026-09-15

Entra derecho nuevo: un módulo, **10 normas** bajadas y **6 fallos** leídos contra el documento.

- **Derecho internacional privado**, módulo nuevo: arts. 2594 a 2612, sin la parte especial.
- **Familia:** compensación económica y gestación por sustitución pasan a tener precedente propio.
- **Salario mínimo, vital y móvil** con sus ocho tramos, y los topes en SMVM remiten ahí.
- **De dónde sale un fallo:** lo que no viene del registro del tribunal lo declara `fallos.json`.
- La emergencia de la **Ley 14.407 de PBA** está vencida desde octubre de 2016.
- **[`docs/COBERTURA.md`](docs/COBERTURA.md):** qué ramas cubre el repositorio, para decidir por
  dónde crece.

## [1.0.2] — 2026-09-15

Íconos, banners y metadatos de marketplace, para los dos envoltorios: Claude Code y Codex.

## [1.0.1] — 2026-09-15

Correcciones: no entran normas ni fallos nuevos y ningún cálculo cambia de resultado.

- **Ortografía:** si se muestra se acentúa, si se compara no. Las carátulas, contra el documento.
- **Fechas:** las del derecho con día y mes; las del propio trabajo, por mes.
- **Títulos de las constituciones provinciales** en `normas.json`.
- **Si falta Python, la skill no calcula a mano:** emite el marcador y explica cómo instalarlo.
- La salida entra en la consola de Windows, donde un `→` cortaba el script ya habiendo escrito.
- Control nuevo de las cifras de inventario, con `herramientas/cifras.py`.

## [1.0.0] — 2026-09-14

Versión inicial.

Plugin de análisis, redacción y revisión jurídica bajo derecho argentino. Primera versión
publicable de un proyecto en desarrollo: la cobertura auditada crece módulo por módulo. Trae:

- La skill `derecho-argentino`: 30 módulos con numeración global estable, en dos modos de entrada.
- **Ocho comandos slash** y un perfil que ordena las preguntas sin elegir por el usuario.
- **Capa de fuente primaria offline:** 110 normas con hash SHA-256 y 64 fallos verificados, más el
  CCyC Comentado de SAIJ-INFOJUS y las series de índices.
- **Cuatro calculadoras deterministas**, que salen con código 2 antes que inventar un número.
- Texto **recuperado por OCR local** para los seis fallos con la capa de texto arruinada.
- La marca del repositorio en [`assets/marca/`](assets/marca/).

**Los datos vienen congelados a septiembre de 2026.** `/derecho:estado` dice qué quedó vencido y
`/derecho:actualizar` lo baja de las fuentes oficiales.
