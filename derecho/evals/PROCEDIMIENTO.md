# Procedimiento · lo que se puntúa en todos los casos

> Complemento de cada `rubrica.md`. Las rúbricas puntúan **qué identificó** el análisis; esto
> puntúa **cómo llegó**. Se aplica a todos los casos de `evals/`, cualquiera sea el área.

## Por qué hace falta

Una rúbrica lee la respuesta final. Hay una clase entera de fallas que ahí no se ve, porque la
respuesta sale bien formada igual: el análisis corre la calculadora, obtiene la salida correcta
y después la rearma a mano perdiendo una advertencia; tipea una fecha distinta de la que le
dieron y el total sale plausible; contesta de memoria sin abrir el módulo y acierta; reescribe
un marcador con otras palabras. En los cuatro casos la rúbrica de contenido da aprobado.

Pasó de verdad, en un uso real de la skill: el agente hizo el procedimiento casi entero bien
—leyó el módulo, ubicó el script, preguntó los datos en una sola tanda, corrió la calculadora—
y la pérdida ocurrió toda **entre la salida de la herramienta y la tabla que mostró**. Ninguna
de las rúbricas del repositorio habría detectado nada.

Estos puntos se puntúan sobre la **traza** —lo que se ve que el sistema hizo, no sólo lo que
escribió— y son binarios como los demás.

## Obligatorios de procedimiento

- [ ] **Preguntó antes de analizar.** Los datos determinantes, en una sola tanda, y esperó la
      respuesta. No ofreció valores de ejemplo para que se los confirmaran.

- [ ] **Abrió el módulo que correspondía.** Se ve qué leyó. No contestó de memoria: acertar de
      memoria no es aprobar, porque la próxima vez la memoria falla igual de silenciosamente.

- [ ] **Corrió la herramienta en vez de calcular**, cuando había herramienta para ese cálculo.

- [ ] **Abrió con el bloque de datos tomados** y los datos coinciden con los aportados. Ver
      `references/intake.md`, «Devolver los datos antes de usarlos».

- [ ] **Pegó la salida de la herramienta en vez de rearmarla.** Nada de lo que la herramienta
      devolvió —tramo, régimen, rubros con su norma, total, advertencias, marcadores— se
      perdió en el camino a la respuesta.

- [ ] **Los marcadores están verbatim y pertenecen al vocabulario** de `references/marcadores.md`.
      Ninguno reescrito, ninguno inventado, ninguno mal acentuado.

- [ ] **No afirmó norma, plazo, monto ni fallo sin fuente primaria a la vista.** Lo que no pudo
      cotejar salió como marcador, no como afirmación matizada.

- [ ] **No afirmó nada sobre lo que pasó sin la constancia.** Que el escrito diga que se notificó
      el 12 no es la cédula; que un resumen diga que la Corte sostuvo algo no es el fallo. Ver
      `SKILL.md`, sección 2, *Procedimiento*.

- [ ] **Cerró con el estado del trabajo**: marcadores pendientes, normas con verificación
      pendiente y decisiones tomadas por defecto (`references/escritos.md`, sección 11).

## Qué de esto se puede medir sin leer

El último obligatorio de marcadores es mecánico y tiene herramienta:

```sh
python3 derecho/skills/derecho-argentino/scripts/verificar_respuesta.py respuesta.md
```

Reclama tres cosas que a ojo pasan por buenas: el marcador inventado, el que existe pero está
escrito distinto —sin tilde, en minúscula, con un espacio de más— y el que la propia tabla de
`marcadores.md` declara como "no usar". Sale con código 1 si encuentra alguno.

Los demás obligatorios se leen. Que no sean automáticos no los hace opinables: cada uno se
contesta mirando la traza, con sí o con no.

## Lo que esto NO puntúa

**Si correspondía emitir ese marcador** es una pregunta de fondo y la contesta la rúbrica del
caso. Poner `[VERIFICAR PLAZO: ...]` donde hacía falta `[ALERTA PLAZO FATAL: ...]` es un error
grave que acá pasa limpio: el nombre existe y está bien escrito. Son dos controles distintos y
ninguno reemplaza al otro.
