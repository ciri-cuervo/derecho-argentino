# 🗺️ Qué ramas del derecho existen, y cuáles cubre el repositorio

Este documento **no enuncia el alcance del plugin**. El alcance es el derecho argentino, y así se
dice siempre. Esto es un mapa interno para decidir **por dónde crece**, y para que esa decisión se
tome leyendo y no de memoria.

Existe porque ninguna herramienta puede contestar la pregunta. Todas miden contra lo declarado:
`cobertura_normativa.py` reporta la norma que un módulo cita y no bajamos, **nunca la que ningún
módulo cita todavía**. Para saber qué falta hay que traer una taxonomía de afuera y cruzarla.

**Relevado el 15/09/2026.** Vale por su fecha: las taxonomías cambian y los módulos también.

## Las tres capas no son intercambiables

Es lo más importante de todo este documento. Hay tres formas de cortar el derecho en ramas y
sirven para cosas distintas; usar una sola como vara mide mal.

| Capa | Qué ordena | Para qué sirve acá |
| --- | --- | --- |
| **Académica** — planes de estudio y posgrados | Cómo se enseña, agrupado por tradición dogmática | Cobertura conceptual. "Derecho Privado I a VIII" no dice qué problema resuelve |
| **Profesional** — institutos de los colegios | Qué trabajo entra realmente a un estudio | Es la única capa donde aparecen consumidor, daños, salud, seguros o propiedad horizontal. También la más volátil: un instituto se crea porque veinte matriculados lo piden |
| **Judicial** — fueros | **Dónde se litiga** | Es la vara operativa de este repositorio, porque las calculadoras son procesales. Es gruesa a propósito |

## Las fuentes, con su fecha y sus defectos

| Fuente | Qué es | Enlace |
| --- | --- | --- |
| CONEAU — Tabla de Disciplinas y Subdisciplinas | Clasificación oficial para acreditación académica | https://www.coneau.gob.ar/archivos/resoluciones/IF-2018-11486845-APN-DAC-CONEAUAnexo-convocatoria.pdf |
| Tesauro SAIJ de Derecho Argentino | Clasificación oficial por materia del MJyDH | https://legislaturalarioja.gob.ar/documentos/normativa-legislativa/Tesauro-saij.pdf |
| UBA — departamentos, plan 1985 y orientaciones del CPO | Taxonomía académica | https://www.derecho.uba.ar/institucional/deptos_acad.php |
| UBA — carreras de especialización | Posgrado | https://www.derecho.uba.ar/academica/posgrados/carr_especializacion.php |
| UNLP — plan de estudios 6 | Taxonomía académica | https://www.jursoc.unlp.edu.ar/documentos/academica/2022/plan_estudio_6.pdf |
| UNC — programas de Abogacía | Taxonomía académica | https://derecho.unc.edu.ar/programas-carrera-de-abogacia/ |
| CPACF — institutos de derecho | Taxonomía profesional, la más granular | https://www.cpacf.org.ar/public/noticia/5240/institutos |
| CALP — institutos | Taxonomía profesional del lado PBA | https://www.calp.org.ar/institutos/ |
| Poder Judicial de la Nación — fueros | Taxonomía judicial | https://justicia.ar/poderes-judiciales/poder-judicial-de-la-nacion |
| Poder Judicial de PBA — fueros | Taxonomía judicial | https://www.justicia.ar/poderes-judiciales/buenos-aires |

**Las dos listas oficiales se contradicen, y fuerte.** CONEAU **no tiene** procesal, familia,
ambiental ni consumidor. El Tesauro SAIJ tampoco tiene familia ni consumidor como faceta, pero sí
tiene contravencional, canónico y bienestar social. Cruzar contra una sola da un resultado
equivocado; hay que usar la unión y anotar cuál la reclama.

**Y el Tesauro tiene dos defectos que conviene saber antes de apoyarse en él.** Es de **enero de
2011**, o sea **anterior al CCyC**. Y se contradice a sí mismo sobre cuántas facetas tiene: el
cuerpo dice un número, después otro, y la enumeración da un tercero — la discrepancia está en la
fuente. Además `saij.gob.ar` responde 403 a los agentes, así que el PDF se leyó de un espejo de la
Legislatura de La Rioja: es el documento oficial del Ministerio, servido por un tercero.

**No existe una nómina pública de "abogado especialista".** Se buscó en CPACF, COLPROBA, CASI,
CALP y CASM: la guía de matriculados del CPACF sólo busca por apellido, nombre, tomo y folio, sin
campo de especialidad. Por eso la capa profesional se tomó de los **institutos de derecho**, que es
lo más cercano que los colegios publican como taxonomía por materia.

## El cruce judicial, que es el test chico y honesto

**Fueros de la Provincia de Buenos Aires.** Con módulo: civil y comercial (`civil.md`),
contencioso administrativo (`contencioso-pba.md`), familia (`familia.md`), laboral (`laboral.md`)
y penal (`penal.md`). **Sin módulo: responsabilidad penal juvenil** —hay
`pba-ley-13634` bajada y `penal.md` toca la Ley 22.278, pero el fuero no tiene desarrollo propio— y
**justicia de paz**, que no aparece en ningún módulo.

**Fueros nacionales y federales.** Con módulo: civil, criminal y correccional, trabajo, y seguridad
social por vía de `previsional.md`; comercial queda cubierto en parte entre `societario.md` y
`concursos.md`. **Sin módulo: contencioso administrativo federal** —`contencioso-pba.md` es
provincial y no se traslada—, **electoral**, **penal económico**, **civil y comercial federal** y
**casación penal**.

## Materias con módulo que no son un fuero

El cruce por fueros deja afuera lo que se litiga **dentro** de otro fuero, y ahí el repositorio
tiene desarrollo propio que ninguna taxonomía judicial muestra:

| Materia | Módulo | Dónde se litiga |
| --- | --- | --- |
| Datos personales y hábeas data | `datos-personales.md` | Civil, o contencioso administrativo contra la autoridad de aplicación |
| Salud y discapacidad | `salud-discapacidad.md` | Civil o federal, por amparo |
| Tránsito | `transito.md` | Faltas, y el encuadre civil del accidente |
| Tributario | `tributario.md` | Contencioso administrativo y penal económico |
| Consumidor | `consumidor.md` | Civil y comercial, y sede administrativa |
| Concursos | `concursos.md` | Comercial, con el cruce laboral |
| Societario | `societario.md` | Comercial |
| Previsional | `previsional.md` | Seguridad social en Nación; en PBA va por el laboral |
| Derecho internacional privado | `dipr.md` | Transversal: no tiene fuero, se plantea dentro del que corresponda |

Esta tabla es la que explica por qué la vara judicial sola no alcanza: **`transito.md` y
`datos-personales.md` no tienen fuero propio y son de los módulos más usados.**

## Lo que la capa profesional revela y las estatales no

Los institutos de los colegios nombran prácticas de alto volumen que ninguna lista estatal
reconoce como rama, y son justamente las que tocan liquidaciones y plazos todos los días:
consumidor, daños, salud, **seguros** y **propiedad horizontal**. El repositorio cubre las dos
primeras; salud está cubierta pero acotada a discapacidad y prepagas.

## Huecos con respaldo cruzado en varias fuentes

- **Sucesiones** — UBA, UNLP y CPACF. Es de los expedientes más frecuentes de cualquier estudio y
  el articulado ya está en `fuentes/normas/ccycn-26994.txt`.
- **Derechos reales** — UBA y CPACF. Mismo caso: el texto ya está en casa.
- **Seguros** — CPACF y CALP. La **Ley 17.418 ya está bajada** y hoy se usa sólo de costado.
- **Ambiental y recursos naturales** — facetas propias en el Tesauro, dos especializaciones en UBA,
  materias en UNLP y UNC, institutos en los dos colegios.
- **Propiedad industrial** — instituto propio en CPACF. El repositorio no lo cubre, y el art. 2609
  inc. c) del CCyCN ya lo nombra: los jueces argentinos tienen jurisdicción **exclusiva** sobre
  validez de patentes y marcas registradas acá (`dipr.md` 35.6).

## Cómo entra una rama nueva

No por este documento. La regla está en [`../CLAUDE.md`](../CLAUDE.md) y no se relaja: **un fuero
nuevo entra entero o no entra** — módulo con fuente primaria a la vista, normas bajadas por el
descargador, fallos **leídos** y su caso de prueba. Sin el caso, `pendientes.py` lo reporta como
módulo que ningún eval nombra, y tiene razón.

Este mapa dice **en qué orden conviene**, no autoriza a saltearse ningún paso.

## Lo que este documento no hace

No se mantiene solo. Un test verifica que los módulos que nombra existan y que ningún módulo del
repositorio quede sin mencionar, pero **nadie puede verificar que la taxonomía siga siendo la de
las fuentes**: eso se vuelve a relevar leyendo, y se cambia la fecha de arriba.
