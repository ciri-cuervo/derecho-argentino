# Base de conocimiento heredada

Todo lo que está bajo `derecho/kb/` es **la capa 2** de `LICENCIAS.md`: contribuciones
originales de **Cristian Aboitiz**, bajo licencia dual —uso no comercial libre, **uso comercial
con autorización previa y expresa**— y con atribución obligatoria en toda redistribución.
Términos completos en `LICENSE-ABOITIZ.md`.

Lo de afuera de `kb/` es de este fork, con dos licencias según qué sea el archivo: el
**contenido** —la skill, los módulos, los comandos y los evals nuevos— es **CC BY-SA 4.0**, y el
**código** —los scripts, los descargadores y las herramientas— es **MIT**. Esa es la razón de que
este directorio exista: **la frontera de licencia se ve en la ruta**, no hay que ir a buscarla a
un archivo.

## Qué hay acá

| Directorio | Contenido |
|---|---|
| `perfiles/` | Perfiles de área por rama: `laboral-CLAUDE.md`, `civil-CLAUDE.md`, `penal-CLAUDE.md` y once más |
| `doctrina/` | `*-DOCTRINA*.md` — doctrina y leading cases por instituto |
| `escritos/` | 34 modelos de escritos y 7 guías de armado, por rama. Incluye `laboral/telegrama/` |
| `jurisdicciones/administrativo/` | 19 perfiles de contencioso administrativo por provincia |
| `especialidades/` | Notarial, medicina legal, violencia digital |
| `contratos/` | Perfil de contratos, red flags e índices y tasas |
| `transversales/` | `plazos-SKILL.md`, `diagnostico-SKILL.md`, `bucles-SKILL.md`, `fuentes-y-conectores.md` y los casos de prueba |
| `ejemplos/` | Consultas resueltas de punta a punta, por rama |
| `marcadores-GLOSARIO.md` | Vocabulario canónico de marcadores. **La skill depende de él** |
| `CHANGELOG.md` | Historial de la base de conocimiento: auditorías normativas y cambios de fondo |

## Cómo se relaciona con la skill

**Este material no pasó la auditoría contra fuente primaria** que sí pasaron los módulos de
`skills/derecho-argentino/references/`. La precedencia ante conflicto, de mayor a menor:

    fuente primaria (fuentes/ o los portales oficiales)
      → la skill y sus módulos
        → docs del Project
          → esto

La skill rutea acá por instituto, desde las secciones 5.11, 6.5, 17.8, 18.8 y 19 de sus
módulos. **Cada una de esas tablas lleva un bloque de contradicciones nominadas**: puntos
concretos donde un perfil de `kb/` dice lo contrario que el módulo auditado, con la norma o el
fallo que lo resuelve. Leerlas antes de usar el perfil, porque no son diferencias de
actualización: son errores de derecho aplicable.

Dos casos para tener presentes:

- **`perfiles/consumidor-CLAUDE.md` tiene cuatro errores de derecho aplicable en PBA** y no
  aporta ventaja neta en lo que se superpone con el módulo. Ver el bloque de advertencias de
  `consumidor.md` 17.8 antes de abrirlo.
- **`transversales/plazos-SKILL.md` y los perfiles laborales tratan a la Ley 11.653 como el
  código procesal laboral bonaerense vigente y no mencionan la Ley 15.057**, cuyo art. 88 la
  derogó y que la Res. SC 1840/2024 puso operativa para las causas sin audiencia de vista
  celebrada. Ninguno de los dos códigos rige solo: hay que preguntar la fecha de la audiencia.
  Manda `sede-judicial-pba.md` 1.6.1.

## Si se modifica algo de acá

Es material de un tercero bajo su propia licencia. Corregir un error puntual y anotarlo en
`CHANGELOG.md` es mantenimiento normal. **Lo que no corresponde es mover su texto a la capa 3**:
para llevar un instituto a un módulo de la skill hay que reescribirlo verificado contra fuente
primaria, no copiarlo. Citas de articulado, plazos y carátulas de fallos no son obra suya y se
mueven libremente.
