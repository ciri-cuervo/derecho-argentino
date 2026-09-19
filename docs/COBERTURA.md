# 🗺️ Qué ramas del derecho existen, y cuáles cubre el repositorio

Este documento **no enuncia el alcance del plugin**. El alcance es el derecho argentino, y así se
dice siempre. Esto es un mapa interno para decidir **por dónde crece**, y para que esa decisión se
tome leyendo y no de memoria.

Existe porque ninguna herramienta puede contestar la pregunta. Todas miden contra lo declarado:
`cobertura_normativa.py` reporta la norma que un módulo cita y no bajamos, **nunca la que ningún
módulo cita todavía**. Para saber qué falta hay que traer una taxonomía de afuera y cruzarla.

**Relevado el 15/09/2026**, y lo que vale por esa fecha es **la taxonomía**: lo que se trajo de afuera para cruzar, que cambia. **La columna de módulo no lleva fecha porque se mantiene con cada módulo que entra** —un test exige que los nombre a todos—, así que una fila más nueva que el relevamiento no es una inconsistencia.

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
fuente. El PDF se leyó de un espejo de la Legislatura de La Rioja: es el documento oficial del
Ministerio, servido por un tercero, y la URL de la tabla es ésa y no una de `saij.gob.ar`.

**No existe una nómina pública de "abogado especialista".** Se buscó en CPACF, COLPROBA, CASI,
CALP y CASM: la guía de matriculados del CPACF sólo busca por apellido, nombre, tomo y folio, sin
campo de especialidad. Por eso la capa profesional se tomó de los **institutos de derecho**, que es
lo más cercano que los colegios publican como taxonomía por materia.

## El cruce judicial, que es el test chico y honesto

**Fueros de la Provincia de Buenos Aires.** Con módulo: civil y comercial (`civil.md`),
contencioso administrativo (`contencioso-pba.md`), familia (`familia.md`, con `violencia-digital.md` para la modalidad digital de la Ley 26.485), laboral
(`laboral.md` para el contrato y su extinción, `laboral-licencias.md` para las licencias,
enfermedades inculpables y suspensiones, `laboral-riesgos.md` para la Ley 24.557 y
`laboral-colectivo.md` para convenios, sindicatos y conflicto),
penal (`penal.md` para el régimen procesal aplicable y la libertad durante el proceso,
`penal-impugnacion.md` para nulidades y recursos, `penal-parte-general.md` para el Código Penal y
la extinción de la acción, `penal-leyes-especiales.md` para los ocho cuerpos que están fuera del
Código y `ejecucion-penal.md` para lo que sigue a la condena firme) y
responsabilidad penal juvenil (`penal-juvenil-pba.md`, el Título III de la Ley 13.634; el régimen
de fondo de la **Ley 27.801** está en `penal-leyes-especiales.md`) y **justicia de paz**
(`justicia-de-paz-pba.md`, la Ley 5.827 y el Código de Faltas). **Con esto, el cruce por fueros
bonaerenses no deja ninguno sin módulo.**

**Fueros nacionales y federales.** Con módulo: civil, criminal y correccional, trabajo, y seguridad
social por vía de `previsional.md`; comercial queda cubierto en parte entre `societario.md` y
`concursos.md`. **Sin módulo: contencioso administrativo federal** —`contencioso-pba.md` es
provincial y no se traslada—, **penal económico**, **civil y comercial federal** y **casación
penal**. Del **electoral** está cubierta su materia penal y contravencional —delitos y faltas,
deber de votar, doble instancia del art. 146— en `penal-leyes-especiales.md` 24.9.7; **lo que no
tiene módulo es el contencioso electoral**: oficialización de listas, impugnaciones y escrutinio.

## Materias con módulo que no son un fuero

El cruce por fueros deja afuera lo que se litiga **dentro** de otro fuero, y ahí el repositorio
tiene desarrollo propio que ninguna taxonomía judicial muestra:

| Materia | Módulo | Dónde se litiga |
| --- | --- | --- |
| Datos personales y hábeas data | `datos-personales.md` | Civil, o contencioso administrativo contra la autoridad de aplicación |
| Salud y discapacidad | `salud-discapacidad.md` | Civil o federal, por amparo |
| Tránsito | `transito.md` | Faltas, y el encuadre civil del accidente |
| Tributario | `tributario.md` | Contencioso administrativo y penal económico |
| Tributario de la Provincia de Buenos Aires | `tributario-pba.md` | Tribunal Fiscal de Apelación de PBA, y contencioso administrativo bonaerense con pago previo |
| Consumidor | `consumidor.md` | Civil y comercial, y sede administrativa |
| Concursos | `concursos.md` | Comercial, con el cruce laboral |
| Societario | `societario.md` | Comercial |
| Previsional | `previsional.md` | Seguridad social en Nación |
| Previsional de la Provincia de Buenos Aires (IPS) | `previsional-pba.md` | Contencioso administrativo bonaerense: el art. 5 inc. b de la Ley 12.008 le da regla de competencia propia |
| Proceso de consumo de la Ciudad | `consumo-caba.md` | Justicia en las Relaciones de Consumo de CABA |
| Contravencional y faltas de la Ciudad | `contravencional-caba.md` | Fuero Penal, Contravencional y de Faltas de CABA, después de la vía administrativa en faltas |
| Tributario y contencioso administrativo de la Ciudad | `tributario-caba.md` | Fuero Contencioso Administrativo y Tributario de CABA, después de agotar la vía ante AGIP |
| Ejecución de la pena | `ejecucion-penal.md` | Juzgados de ejecución penal, federales y de PBA, después de la condena firme |
| Procedimiento administrativo nacional | `administrativo-nacional.md` | Contencioso administrativo federal |
| Empleo público nacional | `empleo-publico.md` | Contencioso administrativo federal, no laboral |
| Defensa de la competencia | `competencia.md` | Civil y comercial; sede administrativa ante la autoridad de competencia |
| Firma digital y documento electrónico | `firma-digital.md` | Transversal: prueba en cualquier fuero |
| Salud mental | `salud-mental.md` | Civil y familia; cruza capacidad y cobertura |
| Pagaré y cheque | `titulos-ejecutivos.md` | Civil y comercial, por juicio ejecutivo |
| Locación de inmuebles | `locacion.md` | Civil y comercial; el desalojo, en el fuero que corresponda |
| Derechos reales y propiedad horizontal | `derechos-reales.md` | Civil y comercial |
| Función notarial y documento notarial | `notarial.md` | Transversal: el fondo del CCyCN rige en todo el país y la organización es local. Con módulo: CABA (Ley 404) y PBA (Decreto-Ley 9.020). **Sin módulo: las leyes notariales de las demás provincias** |
| Proceso civil y comercial de la Nación | `proceso-nacional.md` | Justicia nacional y federal; no se transpola a PBA |
| Proceso civil y comercial de la PBA | `proceso-pba.md` | Justicia provincial. El fuero laboral tiene rito propio y el CPCCBA le es supletorio |
| Amparo | `amparo.md` | Transversal: es la vía, no la materia. Entra por él salud, ambiental, datos y consumo |
| Ambiental | `ambiental.md` | Civil, contencioso administrativo y federal penal por residuos peligrosos |
| Propiedad industrial e intelectual | `propiedad-industrial.md` | Civil y comercial federal |
| Seguros | `seguros.md` | Civil y comercial, casi siempre adentro de un juicio de daños |
| Sucesiones, porción legítima y testamentos | `sucesiones.md` | Civil, o el fuero que cada provincia asigne al sucesorio |
| Derecho internacional privado | `dipr.md` | Transversal: no tiene fuero, se plantea dentro del que corresponda |
| Modo órgano jurisdiccional | `sede-judicial.md` | Transversal: no tiene fuero. La pieza y la alzada sí, y van por fuero |
| La pieza que firma el órgano | `sede-judicial-pba.md` (laboral PBA), `sede-judicial-nacional.md` (justicia nacional y federal) y `sede-judicial-caba.md` (CAyT de la Ciudad) | Sin módulo: la sentencia penal, la de familia y la de cualquier otra provincia |
| Honorarios de abogados y auxiliares | `honorarios-nacional.md` (Ley 27.423), `honorarios-caba.md` (Ley 5.134) y `honorarios-pba.md` (Ley 14.967) | Dentro del proceso donde se regula, en cualquier fuero. Sin módulo: las leyes arancelarias de las demás provincias |

Esta tabla es la que explica por qué la vara judicial sola no alcanza: **`transito.md` y
`datos-personales.md` no tienen fuero propio y son de los módulos más usados.**

## Lo que la capa profesional revela y las estatales no

Los institutos de los colegios nombran prácticas de alto volumen que ninguna lista estatal
reconoce como rama, y son justamente las que tocan liquidaciones y plazos todos los días:
consumidor, daños, salud, **seguros** y **propiedad horizontal**. El repositorio cubre las dos
primeras; salud está cubierta pero acotada a discapacidad y prepagas.

## Huecos con respaldo cruzado en varias fuentes

- **Derechos reales** y **propiedad horizontal** — UBA y CPACF. El articulado está en casa, en
  `fuentes/normas/ccycn-26994.txt`: Libro IV y arts. 2037 y siguientes. **No esperan descarga,
  esperan módulo.**
- **Los aranceles locales que no son el de PBA, el nacional ni el de CABA.** Están cargados el
  bonaerense (Ley 14.967, con calculadora), el nacional y federal (Ley 27.423) y el de la justicia
  de la Ciudad (Ley 5.134). Falta el resto de las provincias, y ninguna serie de valores está
  cargada: ni la del jus porteño ni la de las dos UMA.

## Cómo entra una rama nueva

No por este documento. **Un fuero nuevo entra entero o no entra**, y qué significa entero está
escrito en [`PENDIENTES.md`](PENDIENTES.md), bajo *El trabajo de fondo*.

Este mapa dice **en qué orden conviene**, no autoriza a saltearse ningún paso.

## Lo que este documento no hace

No se mantiene solo. Un test verifica que los módulos que nombra existan y que ningún módulo del
repositorio quede sin mencionar, pero **nadie puede verificar que la taxonomía siga siendo la de
las fuentes**: eso se vuelve a relevar leyendo, y se cambia la fecha de arriba.
