# Scripts de la skill `derecho-argentino`

Cuatro calculadoras deterministas y tres utilitarios, sin dependencias fuera de la biblioteca
estándar de Python 3. Las calculadoras están para lo mismo: **sacar la aritmética de la cabeza
del modelo**. Un error de cálculo en una liquidación o en un vencimiento es tan grave como una
cita inventada y bastante más difícil de ver leyendo.

| Script | Para qué |
| --- | --- |
| `liquidacion_lct.py` | Liquidación por extinción del contrato de trabajo, por tramo de reforma |
| `plazos.py` | Vencimiento en días hábiles judiciales, corridos, meses o años |
| `intereses.py` | Actualización por índice más interés puro, o tasa nominal |
| `honorarios_pba.py` | Regulación de honorarios y aportes bajo la Ley 14.967 |
| `uma_csjn.py` | Valor de la UMA **nacional** y conversión pesos ↔ UMA, art. 51 de la Ley 27.423 |
| `uma_caba.py` | Valor de la UMA **de la Ciudad** y conversión, art. 20 de la Ley 5.134. Otra unidad y otra ley que la de `uma_csjn.py` |
| `configurar.py` | Deja fija la ruta al repo en esta máquina, una sola vez |
| `estado.py` | Diagnóstico: qué encontró, qué datos hay cargados y qué quedó vencido |
| `perfil.py` | Lee y escribe el perfil de trabajo de quien consulta |
| `articulo.py` | Devuelve un artículo de una norma bajada, con título, URL, fecha de descarga y hash arriba. Es lo que se corre para transcribir: `Read` trunca a 2.000 renglones sin avisar y el CCyCN tiene 27.000 |
| `verificar_respuesta.py` | Revisa una respuesta ya escrita, de un archivo o de la entrada estándar con `-`: que sus marcadores sean del vocabulario y estén verbatim. Mide la FORMA, no si correspondía emitirlos |
| `_raiz.py` | No se corre solo: resuelve dónde está el repo para todos los demás |
| `_comun_tests.py` | No se corre solo: la raíz del checkout, el plantón fuera de él y las clases de letras que comparten las seis suites |

## Ninguna ruta hardcodeada

La skill se instala a nivel de cuenta y corre en cualquier máquina; el repo puede estar en
cualquier ruta. `_raiz.py` la resuelve, en este orden: el argumento `--repo`; la variable de
entorno `DERECHO_AR_REPO`; **la variable que define el agente cuando la skill llegó como plugin
instalado** —`CLAUDE_PLUGIN_ROOT` en Claude Code, `CODEX_PLUGIN_ROOT` en Codex, y
`AGENT_PLUGIN_ROOT`, que hoy no define ningún agente y está escrita a futuro—;
`~/.config/derecho-argentino/config.json`; subiendo desde la ubicación de la skill por si vive
dentro del repo; y unas pocas ubicaciones habituales del home. En los dos últimos casos exige el
marcador `derecho/fuentes/MANIFIESTO.md`: no alcanza con que la carpeta se llame parecido.

Instalar la skill no ejecuta nada, así que no hay dónde preguntar la ruta al instalar. Lo
resuelve el primer uso que la necesite: si la encuentra subiendo desde la skill o en una
ubicación habitual del home, **la deja escrita sola en el config** y avisa en una línea. De
ahí en adelante sale del config y no se vuelve a adivinar.

Para dejarlo fijo a mano:

    python3 configurar.py --repo /ruta/al/repo
    python3 configurar.py                      # busca solo e informa qué encontró y qué datos hay

Si no hay repo, los scripts que dependen de datos **cortan con código 2 y emiten el
marcador**. No estiman. Hay un test que lo comprueba, junto con el caso de la skill instalada
lejos del repo apuntando por variable de entorno.

## Principio de diseño: ningún script inventa un monto

Los scripts **no traen datos**. El tope del art. 245, el valor del jus y las series de índices
son exactamente lo que la sección 2 de la skill prohíbe citar de memoria, y por eso entran
como parámetro o se leen de `derecho/fuentes/datos/`. Cuando falta uno:

- si el dato es **determinante**, el script corta con código de salida 2 y emite el marcador;
- si el dato es **suplible**, calcula igual, marca el resultado como provisorio y emite el
  marcador que dice qué falta.

Los marcadores que devuelven son canónicos: se copian tal cual al escrito, sin reescribirlos.

## Datos que consumen

| Archivo | Lo usa | Estado |
| --- | --- | --- |
| `derecho/fuentes/datos/jus-scba.csv` | `honorarios_pba.py` | 23 períodos: 1/2024 a 8/2026 |
| `derecho/fuentes/datos/uma-csjn.csv` | `uma_csjn.py` | 22 vigencias: 10/2024 a 7/2026. No hay descargador: la consulta oficial es un formulario y se carga a mano |
| `derecho/fuentes/datos/uma-caba.csv` | `uma_caba.py` | 1 vigencia: desde 8/2026. La consulta oficial publica SÓLO el valor vigente, así que no hay serie histórica que cargar |
| `derecho/fuentes/datos/inhabiles.json` | `plazos.py` | 2026 completo (Nación y PBA); 2027 sólo feria de enero |
| `derecho/fuentes/datos/serie-ipc.csv` | `intereses.py` | 117 períodos: 2016-12 a 2026-08 |
| `derecho/fuentes/datos/serie-ripte.csv` | `intereses.py` | 385 períodos: 1994-07 a 2026-07 |
| `derecho/fuentes/datos/serie-cer.csv` | `intereses.py` | 117 períodos: 2016-12 a 2026-08 |

Esta tabla es una foto y se vence. **La medición viva la da `python3 estado.py`**, que lee los
archivos en vez de recordarlos, y avisa cuántos días pasaron desde el último período cargado.
Para completar lo que falte: `python3 derecho/fuentes/scripts/descargar_series.py`.

Mientras un archivo esté pendiente, el script correspondiente lo dice en su salida. No hay
degradación silenciosa.

## Si un script no corre

Dos causas, y piden cosas opuestas. La tabla corta está en la sección 16 del `SKILL.md`; acá va
el porqué.

**Falta Python en esta computadora.** La consola devuelve `command not found: python3`,
`'python3' no se reconoce como un comando` o `xcrun: error: invalid active developer path`, una
por plataforma. El script está y los datos están: lo que no hay es con qué ejecutarlo. Y **este
diagnóstico no puede salir de un script**: `estado.py` es Python y tampoco corre, así que
`/derecho:estado` falla igual y por la misma causa. La conclusión se saca de la señal de la
consola, no de una corrida.

Lo que se emite es el marcador `[CONFIGURACIÓN INCOMPLETA: falta Python 3 ...]` del `SKILL.md`, y
la explicación en castellano y sin jerga: que **falta Python**, que es el único programa aparte que
esta herramienta necesita y **sólo para los cálculos** —citar una norma, revisar un escrito o leer
un módulo funcionan igual sin él—, que se baja de <https://www.python.org/downloads/> y se instala
con las opciones que vienen por defecto, que **en Windows conviene dejar tildado *"Add python.exe
to PATH"*** porque si no el comando sigue sin responder, y que después hay que cerrar y volver a
abrir la aplicación.

**Y lo que no se hace es calcular a mano.** Es la única de las dos causas donde el cálculo manual
está prohibido, y la razón es la asimetría: acá el usuario **cree que corrió la calculadora**. Un
número hecho a ojo sale con el mismo tono que uno determinista, así que entregarlo convierte una
falta de instalación —que se arregla en dos minutos— en un error de liquidación que nadie ve.

**No hay repo conectado, o la ruta es otra.** La consola devuelve `No such file or directory`
sobre la ruta del script. Se pide la ruta —ver «Ninguna ruta hardcodeada»—. Si no hay repo, ahí sí
se calcula a mano, con la verificación aritmética de cierre de `plazos.md` 8.6 y diciendo que se
hizo sin el script.

## Qué NO hacen

- No deciden el criterio jurídico. `intereses.py` calcula el tramo que se le pide; **cuál
  régimen rige** el crédito lo resuelve `references/laboral.md` 5.5 bis.
- No liquidan intereses dentro de `liquidacion_lct.py`: son dos pasos separados a propósito.
- No regulan honorarios periciales: la Ley 14.967 no los rige.
- No reemplazan la verificación de cierre de `plazos.md` 8.6.

## Tests

    python3 -m unittest discover -s . -p 'test_*.py' -v

**330 tests**, sin dependencias externas, en dos grupos.

**Y repartidos en varios archivos, uno por lo que cada suite afirma.** `test_scripts.py` llegó a 6149
renglones, **tres veces el corte de `Read`** que este repositorio le impone a los módulos, y ese
control miraba sólo los `.md`. Lo compartido —la raíz del checkout, el plantón fuera de él— está
en `_comun_tests.py`:

| Archivo | Qué afirma |
| --- | --- |
| `test_calculadoras.py` | Las calculadoras deterministas y sus datos |
| `test_descargadores.py` | El descargador de normas y su procedencia |
| `test_fuentes.py` | La capa offline: manifiesto, OCR, series, identidad de cada documento |
| `test_contenido.py` | El contenido de la skill: SKILL.md, módulos, marcadores, remisiones, ruteo |
| `test_ortografia_salida.py` | Ortografía y codificación de lo que se muestra |
| `test_scripts.py` | Plomería del plugin: raíz, perfil, manifiestos y comandos |

**Aritmética.** Cómputo de antigüedad y tramos, cómputo de Pascua y feriados móviles, descuento
de ferias y asuetos, suma de meses del art. 6 CCyCN, mínimo del art. 22 y monto en jus de la
Ley 14.967, lectura de los archivos de datos, y resolución de la raíz del repo —incluido el
caso de la skill instalada fuera de él y el de que no haya repo, donde el script tiene que
negarse a calcular—.

**Afirmaciones de la documentación**, que son las que se vencen en silencio: que los números de
`fuentes/MANIFIESTO.md` coincidan con lo que hay en disco —los de la tabla, los de la frase que
los explica, y que la fecha con que encabeza su foto no sea anterior a la última norma bajada—,
que los contadores de
`references/fallos-csjn.md` coincidan con sus propias tablas, que el texto recuperado por OCR
siga derivando del PDF que dice, que **toda ruta que un módulo cita exista**, que **toda cita
entrecomillada de un bloque de contradicciones nominadas esté literal en `kb/`**, y que este
archivo no mienta sobre la cantidad de tests.

Si se toca una fórmula, el test cambia en el mismo commit.
