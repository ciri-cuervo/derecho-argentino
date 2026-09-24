---
name: liquidacion
description: Liquidación por extinción del contrato de trabajo (LCT). Calcula con script determinista, después de identificar qué tramo de reforma rige por la fecha del acto extintivo.
argument-hint: "[datos que ya tengas: ingreso, extinción, mejor remuneración...]"
allowed-tools: Read, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/liquidacion_lct.py:*), Bash(python ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/liquidacion_lct.py:*), Bash(py -3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/liquidacion_lct.py:*)
---

Datos que trae el usuario: `$ARGUMENTS`

**Antes de calcular nada, leé `${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/references/laboral.md`**, secciones 5.1 a 5.4 y el protocolo de
liquidación de 5.10. No es opcional: la LCT se reformó en tres tramos y **los regímenes no son
intercambiables**. Si estás actuando desde el órgano, leé también `${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/references/sede-judicial-pba.md`
1.6.4 — ahí no se liquida, se coteja.

## Orden

1. **¿Rige la LCT?** El art. 2 inc. a excluye a la Administración Pública salvo acto expreso de
   inclusión: un docente o un empleado provincial o municipal se liquida por su estatuto, no por
   los arts. 245 y siguientes, y la competencia suele ser contencioso administrativa. El script
   corta con código 2 ante `--empleador publico`; transcribí ese marcador y no liquides.
   **Y aunque rija, un estatuto puede desplazar la liquidación:** casas particulares, construcción,
   viajantes de comercio y encargados de edificio tienen otro preaviso, otra indemnización o un
   fondo en su lugar (`laboral.md` 5.17 quinquies y sexies). Con cualquiera de los cuatro,
   `--regimen` corta con código 2: transcribí el marcador y liquidá a mano con esa sección.
2. **Fecha del acto extintivo.** Decide el régimen. Sin ella no se calcula. Si cae entre el
   30/12/2023 y el 08/07/2024, rige la advertencia del DNU 70/2023 de la sección 5.1.
3. **Pedí en una sola tanda lo que falte**, no de a uno: quién era el empleador, qué tareas hacía y dónde, fecha de ingreso, fecha de extinción,
   mejor remuneración mensual normal y habitual del último año, remuneración del último mes,
   días de vacaciones ya gozados en el año, si hubo preaviso otorgado, si estaba en período de
   prueba, y la causal de extinción.
4. **El tope del art. 245 no se saca de memoria.** Depende del CCT, que surge de lo que las
   partes invocan y prueban. Si no consta, corré igual **sin** `--tope-245`: el script emite
   el marcador que corresponde en vez de suponer un tope.
5. **Corré el script.** No hagas la aritmética a mano:

   ```sh
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/scripts/liquidacion_lct.py \
     --ingreso AAAA-MM-DD --extincion AAAA-MM-DD \
     --mejor-remuneracion N [--empleador privado] [--regimen lct] \
     [--remuneracion-ultimo-mes N] [--tope-245 N] \
     [--dias-vacaciones-gozadas N] [--periodo-prueba] [--preaviso-otorgado]
   ```

   Si sale con código 2, **no completes el número que falta**: transcribí el marcador.

   **Corré sin `--json` y pegá esa salida tal cual.** Ya viene formateada y trae el tramo, el
   régimen, cada rubro con su norma y su detalle, el total, las advertencias y los marcadores.
   `--json` está para encadenar con otra herramienta: si lo usás para redactar, el que rearma
   la tabla sos vos, y una advertencia que no sobrevive al rearmado no deja rastro. Ya pasó:
   se perdieron la línea del tramo y la advertencia del divisor 25 de vacaciones.

6. **Abrí con el bloque de datos tomados**, copiado de la cabecera de la salida y cotejado
   contra lo que te dieron. Si un dato no coincide, pará y preguntá; no elijas vos cuál era
   el bueno. Ver `intake.md`, «Devolver los datos antes de usarlos».
7. **Cotejá la salida contra el texto vigente del artículo** antes de darla por buena, y aplicá
   la verificación aritmética de cierre.
8. **Los agravantes e indemnizaciones especiales no los calcula el script.** Revisá si
   corresponden (art. 2 Ley 25.323, art. 80 LCT, estabilidad por embarazo o matrimonio,
   registración) y decilo, con su norma y su recaudo.

Cerrá con el bloque "Estado del escrito" de `${CLAUDE_PLUGIN_ROOT}/skills/derecho-argentino/references/escritos.md` sección 11: marcadores
pendientes, normas con verificación pendiente, y decisiones tomadas por defecto.

**Si `python3` no responde** —`command not found`, `no se reconoce` o *Python was not
found*—, el mismo comando se corre con `python` y después con `py -3`, y el que ande se usa
en el resto. Si ninguno anda, falta Python: ver «Si un script no corre» en el `SKILL.md`.
