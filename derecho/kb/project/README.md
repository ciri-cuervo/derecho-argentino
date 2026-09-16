# Camino Project · arquitectura anterior

Estos archivos **no son parte del plugin** y Claude Code no los carga. Son el camino previo a
la skill: pegar un perfil en un Project de claude.ai, correr una entrevista de configuración y
quedarse con un `CLAUDE.md` personalizado.

| Archivo | Qué es |
|---|---|
| `CLAUDE.md` | Perfil general. Se pega en las instrucciones de un Project |
| `setup-interview.md` | Entrevista de quince preguntas que genera el perfil personalizado |
| `setup-output-TEMPLATE.md` | Estructura exacta del perfil que la entrevista produce |
| `legal.local.md.template` | Plantilla de configuración local del estudio. Se copia como `legal.local.md` |

## Se superponen con la skill, y en un punto la contradicen

La skill `derecho-argentino` cubre lo mismo y mejor: el ruteo por área, el protocolo ante
alucinación normativa, las reglas de citación y el criterio de cierre están en `SKILL.md` y sus
módulos, verificados contra fuente primaria, cosa que estos archivos nunca fueron.

**La contradicción es de fondo, no de forma.** La entrevista genera campos de configuración
—`FUERO_HABITUAL`, `CCT_HABITUAL`, `AREAS_PRACTICA`— pensados para que el sistema no vuelva a
preguntar. La sección 0.1 de la skill dice lo contrario y a propósito: **no hay rol ni fuero
por defecto**, se preguntan al abrir cada conversación, porque quien consulta puede ser un
abogado de parte, un juez o un empleado de un tribunal de cualquier fuero. Y el CCT no es dato
de cartera: surge de lo que las partes invocan y prueban.

Si se usan los dos caminos a la vez, **manda la skill**. Un perfil personalizado que fije el
fuero no autoriza a saltear la pregunta de apertura.

## Por qué siguen acá

Porque el camino Project funciona sin Claude Code y hay quien lo usa así. Cuando deje de
usarse, este directorio entero se borra y hay que limpiar las referencias que quedan en
`kb/transversales/diagnostico-SKILL.md`, `kb/transversales/plazos-SKILL.md`, `kb/transversales/bucles-SKILL.md`, `kb/contratos/CLAUDE.md`,
`kb/especialidades/` y `kb/marcadores-GLOSARIO.md`.
