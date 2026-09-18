# Perfiles heredados · qué cubre el módulo y qué queda en el perfil

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

**Dieciséis ramas tienen módulo auditado contra fuente primaria:** laboral (5), civil y comercial
(6), consumidor (17), familia (18), penal (24), salud y discapacidad (27), contencioso
administrativo de PBA (26), tránsito (28), concursos (29), datos personales (30), societario (31),
previsional (32), tributario (33), derecho internacional privado (35, capítulos 1 y 2) y
responsabilidad penal juvenil de PBA (36, el fuero de la Ley 13.634) y honorarios
de la justicia nacional y federal (37, Ley 27.423). **Cada
uno cubre una parte de su rama y tiene precedencia sobre el perfil**; el mapa de abajo dice, rama
por rama, qué cubre el módulo y qué queda en el perfil.

Lo que **no** tiene módulo son las especialidades del final del mapa —medicina legal, violencia
digital y notarial— y lo contencioso administrativo de las demás jurisdicciones. Para eso hay
material: más de cinco mil líneas de perfiles de área en el repo, con sus modelos de escritos. Este
módulo existe para que `[SIN PERFIL DE ÁREA CARGADO]` deje de ser un encogimiento de hombros y pase
a ser un traspaso: se dice qué falta **y se abre lo que hay**.

## Protocolo

1. **Identificada la materia** (sección 0.1 bis), **primero el módulo de la rama**: el mapa de
   abajo dice qué cubre cada uno. El perfil se abre por lo que el módulo deja afuera, nunca en su
   lugar, y si la materia no tiene módulo se abre el perfil directamente.
2. **Si el repo está disponible, leerlo antes de responder.** Un perfil de cuatrocientas
   líneas escrito para esa rama supera a cualquier respuesta con conocimiento general.
3. **Decirlo de entrada**, no al final, y emitir el marcador:

        [SIN PERFIL DE ÁREA CARGADO: el diagnóstico se realizó con conocimiento normativo general.
        Cargar el perfil del área correspondiente para un diagnóstico más preciso.]

   Cuando el perfil **sí** se pudo leer, cambia el texto: se dice que se trabajó con el perfil
   del repo, y se mantiene la advertencia de verificación del punto siguiente.
4. **La advertencia no es opcional.** Estos perfiles se consolidaron en **julio de 2026** y
   **no pasaron la auditoría contra fuente primaria** que sí pasaron los módulos de `references/`.
   Rige la precedencia de la sección 15: fuente primaria → esta skill → docs del Project → perfiles
   del repo. Ante conflicto, gana lo de arriba. Y tres perfiles quedaron **vencidos por normas
   posteriores** a su consolidación: discapacidad por la Ley 27.793, tributario por la Ley 27.799 y
   lo que el mapa señale en cada fila.
5. **Lo procesal no se transpola.** Ninguno de estos perfiles fue revisado contra la Ley 15.057
   ni contra la Res. SC 1840/2024. Si la consulta toca el proceso laboral bonaerense, mandan
   `sede-judicial-pba.md` y `parte.md`, no el perfil de la rama.

Los **modelos de escritos** de estas ramas —penal, previsional, tránsito— están inventariados
aparte, en `modelos.md` sección 23.7.

## Mapa

Rutas relativas a la raíz del repo, bajo `derecho/`.

| Materia | Perfil | Complementos |
| --- | --- | --- |
| **Penal** | **`references/penal.md`, sección 24**, auditado contra fuente primaria y con precedencia sobre el perfil. Cubre régimen procesal aplicable, coerción, extinción y probation, nulidades, recursos, parte general, ejecución de la pena y leyes especiales. El perfil `kb/perfiles/penal-CLAUDE.md` (1041 líneas) queda **sólo para la parte especial** —los tipos penales concretos— que es lo único que el módulo no cubre | **Jurisprudencia: `references/fallos-csjn.md` 34.2**, veinte fallos de la CSJN bajados y verificados, que desplaza a `kb/doctrina/penal-DOCTRINA.md` y `penal-APUNTES-DOCTRINA.md` en carátula, cita y fecha. Y cinco modelos en `kb/escritos/penal/escritos/modelos/`: excarcelación y cese de prisión preventiva, hábeas corpus correctivo, nulidad de allanamiento, recurso de casación, solicitud de probation. **Ninguno registra la convivencia de códigos de 24.1**, y el de casación no distingue la impugnación del CPPF (24.6). Antes de usarlos, leer la sección del módulo que corresponda |
| **Contencioso administrativo** | **PBA: `references/contencioso-pba.md`, sección 26**, auditado contra la Ley 12.008 y con precedencia. Para las demás jurisdicciones, `kb/perfiles/administrativo-CLAUDE.md` (694 líneas) | `kb/jurisdicciones/administrativo/` trae perfiles por provincia: PBA, CABA y otras diecisiete, más una plantilla `_PROVINCIA_`. **El de PBA quedó desplazado por la sección 26**; los demás siguen con la advertencia |
| **Protección de datos** | **`references/datos-personales.md`, sección 30**, auditado contra la Ley 25.326 y con precedencia: derechos previos y sus plazos, datos sensibles, informes crediticios y la acción. Queda fuera el régimen sancionatorio, la autoridad de aplicación y el Decreto 1558/2001, para lo que sigue `kb/perfiles/proteccion-datos-CLAUDE.md` (553 líneas) con la advertencia | — |
| **Previsional** | **`references/previsional.md`, sección 32**, auditado contra las Leyes 24.241 **y 26.425** y con precedencia: PBU, compensatoria, **prestación adicional por permanencia**, retiro por invalidez y pensión, más el destino de cada modalidad del régimen de capitalización. Quedan fuera la movilidad, los regímenes diferenciales y el procedimiento ante ANSES, para lo que sigue `kb/perfiles/previsional-CLAUDE.md` (504 líneas) con la advertencia | Tres modelos en `kb/escritos/previsional/escritos/modelos/`: impugnación de denegatoria, pensión derivada, reajuste de haberes |
| **Discapacidad y salud** | **`references/salud-discapacidad.md`, sección 27**, auditado contra las Leyes 22.431, 24.901 y 26.682 y con precedencia. El perfil `kb/perfiles/discapacidad-CLAUDE.md` (477 líneas) se consolidó **antes de la Ley 27.793 (BO 22/09/2025)**, que reescribió el concepto de discapacidad y el régimen de aranceles: lo que diga sobre esos dos puntos está vencido | Jurisprudencia de la CSJN: `references/fallos-csjn.md` 34.6, donde "Cambiaso" y "R. A., D." tienen la carátula oficial — **las dos circulan mal citadas**. Para el resto, `kb/doctrina/discapacidad-DOCTRINA.md` con la misma advertencia |
| **Societario** | **`references/societario.md`, sección 31**, auditado contra la Ley 19.550 y con precedencia, para lo que decide contra quién se demanda: Sección IV, art. 54 tercer párrafo, arts. 59, 60 y 274. Para la constitución, los tipos, las asambleas y la reorganización societaria sigue `kb/perfiles/societario-CLAUDE.md` (476 líneas) con la advertencia | — |
| **Concursos y quiebras** | **El cruce con el crédito laboral en `references/concursos.md`, sección 29**, auditado y con precedencia. Para el resto del proceso concursal, `kb/perfiles/concursos-CLAUDE.md` (426 líneas) | — |
| **Tributario** | **`references/tributario.md`, sección 33**, auditado contra la Ley 11.683 t.o. 1998 y con precedencia: prescripción, recursos del art. 76, clausura del art. 77 y demanda del art. 82. Quedan fuera la determinación de oficio, el régimen sancionatorio, la ejecución fiscal y los impuestos en particular, para lo que sigue `kb/perfiles/tributario-CLAUDE.md` (350 líneas) con la advertencia | El perfil incluye el procedimiento ante ARCA. **Se consolidó antes de la Ley 27.799 (BO 02/01/2026)**, que reescribió el art. 56: lo que diga sobre prescripción está vencido. **Y lo provincial no lo cubre: medido, el perfil no nombra a ARBA ni una vez** —sólo instruye a mirar el código fiscal de cada provincia—, así que ahí el perfil no sirve: para PBA está `references/tributario-pba.md` 54 y para la Ciudad `references/tributario-caba.md` 57, los dos auditados |
| **Tránsito** | **`references/transito.md`, sección 28**, auditado y con precedencia: régimen nacional de la Ley 24.449 **y procedimiento bonaerense de la Ley 13.927** (28.5). Queda fuera el Decreto 532/2009 y sus Anexos, de donde salen montos y formularios. El perfil `kb/perfiles/transito-CLAUDE.md` (306 líneas) sigue para otras jurisdicciones, con la advertencia | Siete modelos de descargo en `kb/escritos/transito/descargos/modelos/`, más un modelo de prescripción para CABA |
| **Medicina legal** | `kb/especialidades/medicina-legal-CLAUDE.md` | Útil para control de pericias médicas en cualquier fuero |
| **Violencia digital** | `kb/especialidades/violencia-digital-CLAUDE.md` | Cruza con penal y con familia |
| **Notarial** | `kb/especialidades/notarial/notarial-CLAUDE.md` | Con `kb/especialidades/notarial/notarial-clausulas.md` y plantilla por provincia |

Los perfiles de **consumidor** y **familia** también siguen en el repo. Ya no se usan como
fuente primaria de la skill —para eso están `consumidor.md` y `familia.md`, auditados— pero
sirven de profundidad adicional, con la misma advertencia.

## Dos cruces que aparecen seguido en materia laboral

**Concursos y quiebras.** Cuando el empleador quiebra o se concursa, el expediente laboral se
cruza con pronto pago, verificación del crédito, privilegios y fuero de atracción. Ese cruce
**ya tiene módulo propio**: `concursos.md` sección 29, auditado contra la Ley 24.522 y con
precedencia. Para el proceso concursal en sí —presentación, categorización, acuerdo,
liquidación, acciones de ineficacia— sigue el perfil `kb/perfiles/concursos-CLAUDE.md` con la
advertencia de siempre.

**Empleo público.** Es la frontera de competencia del fuero laboral: en PBA el empleado público
provincial y municipal va, por regla, al contencioso administrativo. Ante duda de competencia,
resolver primero (sección 4) y mirar `contencioso-pba.md` sección 26.

## Lo que este módulo NO hace

No convierte estas ramas en materias cubiertas. Un perfil leído mejora mucho la respuesta
frente a no tener nada, pero **no equivale a un módulo auditado**: no tiene el literal de las
normas cotejado, ni jurisprudencia con enlace a la sentencia, ni casos de verificación. Decirlo
con esas palabras cuando corresponda es parte del trabajo.
