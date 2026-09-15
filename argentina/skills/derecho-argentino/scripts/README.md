# Scripts de la skill `derecho-argentino`

Cuatro calculadoras deterministas y tres utilitarios, sin dependencias fuera de la biblioteca
estándar de Python 3. Las calculadoras están para lo mismo: **sacar la aritmética de la cabeza
del modelo**. Un error de cálculo en una liquidación o en un vencimiento es tan grave como una
cita inventada y bastante más difícil de ver leyendo.

| Script | Para qué |
|---|---|
| `liquidacion_lct.py` | Liquidación por extinción del contrato de trabajo, por tramo de reforma |
| `plazos.py` | Vencimiento en días hábiles judiciales, corridos, meses o años |
| `intereses.py` | Actualización por índice más interés puro, o tasa nominal |
| `honorarios_pba.py` | Regulación de honorarios y aportes bajo la Ley 14.967 |
| `configurar.py` | Deja fija la ruta al repo en esta máquina, una sola vez |
| `estado.py` | Diagnóstico: qué encontró, qué datos hay cargados y qué quedó vencido |
| `perfil.py` | Lee y escribe el perfil de trabajo de quien consulta |
| `_raiz.py` | No se corre solo: resuelve dónde está el repo para todos los demás |

## Ninguna ruta hardcodeada

La skill se instala a nivel de cuenta y corre en cualquier máquina; el repo puede estar en
cualquier ruta. `_raiz.py` la resuelve, en este orden: el argumento `--repo`, la variable de
entorno `DERECHO_AR_REPO`, `~/.config/derecho-argentino/config.json`, subiendo desde la
ubicación de la skill por si vive dentro del repo, y unas pocas ubicaciones habituales del
home. En los dos últimos casos exige el marcador `argentina/fuentes/MANIFIESTO.md`: no
alcanza con que la carpeta se llame parecido.

Instalar la skill no ejecuta nada, así que no hay dónde preguntar la ruta al instalar. Lo
resuelve el primer uso que la necesite: si la encuentra subiendo desde la skill o en una
ubicación habitual del home, **la deja escrita sola en el config** y avisa en una línea. De
ahí en adelante sale del paso 3 y no se vuelve a adivinar.

Para dejarlo fijo a mano:

    python3 configurar.py --repo /ruta/al/repo
    python3 configurar.py                      # busca solo e informa qué encontró y qué datos hay

Si no hay repo, los scripts que dependen de datos **cortan con código 2 y emiten el
marcador**. No estiman. Hay un test que lo comprueba, junto con el caso de la skill instalada
lejos del repo apuntando por variable de entorno.

## Principio de diseño: ningún script inventa un monto

Los scripts **no traen datos**. El tope del art. 245, el valor del jus y las series de índices
son exactamente lo que la sección 2 de la skill prohíbe citar de memoria, y por eso entran
como parámetro o se leen de `argentina/fuentes/datos/`. Cuando falta uno:

- si el dato es **determinante**, el script corta con código de salida 2 y emite el marcador;
- si el dato es **suplible**, calcula igual, marca el resultado como provisorio y emite el
  marcador que dice qué falta.

Los marcadores que devuelven son canónicos: se copian tal cual al escrito, sin reescribirlos.

## Datos que consumen

| Archivo | Lo usa | Estado |
|---|---|---|
| `argentina/fuentes/datos/jus-scba.csv` | `honorarios_pba.py` | 6 períodos: 1/2026 a 8/2026 |
| `argentina/fuentes/datos/inhabiles.json` | `plazos.py` | 2026 completo (Nación y PBA); 2027 sólo feria de enero |
| `argentina/fuentes/datos/serie-ipc.csv` | `intereses.py` | 117 períodos: 2016-12 a 2026-08 |
| `argentina/fuentes/datos/serie-ripte.csv` | `intereses.py` | 385 períodos: 1994-07 a 2026-07 |
| `argentina/fuentes/datos/serie-cer.csv` | `intereses.py` | 117 períodos: 2016-12 a 2026-08 |

Esta tabla es una foto y se vence. **La medición viva la da `python3 estado.py`**, que lee los
archivos en vez de recordarlos, y avisa cuántos días pasaron desde el último período cargado.
Para completar lo que falte: `python3 argentina/fuentes/scripts/descargar_series.py`.

Mientras un archivo esté pendiente, el script correspondiente lo dice en su salida. No hay
degradación silenciosa.

## Qué NO hacen

- No deciden el criterio jurídico. `intereses.py` calcula el tramo que se le pide; **cuál
  régimen rige** el crédito lo resuelve `references/laboral.md` 5.5 bis.
- No liquidan intereses dentro de `liquidacion_lct.py`: son dos pasos separados a propósito.
- No regulan honorarios periciales: la Ley 14.967 no los rige.
- No reemplazan la verificación de cierre de la sección 8.6.

## Tests

    python3 -m unittest discover -s . -p 'test_*.py' -v

**128 tests**, sin dependencias externas, en dos grupos.

**Aritmética.** Cómputo de antigüedad y tramos, cómputo de Pascua y feriados móviles, descuento
de ferias y asuetos, suma de meses del art. 6 CCyCN, mínimo del art. 22 y monto en jus de la
Ley 14.967, lectura de los archivos de datos, y resolución de la raíz del repo —incluido el
caso de la skill instalada fuera de él y el de que no haya repo, donde el script tiene que
negarse a calcular—.

**Afirmaciones de la documentación**, que son las que se vencen en silencio: que los números de
`fuentes/MANIFIESTO.md` coincidan con lo que hay en disco, que los contadores de
`references/fallos-csjn.md` coincidan con sus propias tablas, que el texto recuperado por OCR
siga derivando del PDF que dice, que **toda ruta que un módulo cita exista**, que **toda cita
entrecomillada de un bloque de contradicciones nominadas esté literal en `kb/`**, y que este
archivo no mienta sobre la cantidad de tests.

Si se toca una fórmula, el test cambia en el mismo commit.
