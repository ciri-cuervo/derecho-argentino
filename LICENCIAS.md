# Licencias

Este repositorio tiene **cuatro capas de autoría** con licencias distintas. Este archivo es el
mapa; cada licencia vive en su propio archivo y ninguna se modifica desde acá.

| Capa | Licencia | Archivo |
| --- | --- | --- |
| 1. Código base upstream de Anthropic | Apache License 2.0 | `LICENSE` |
| 2. Contribuciones originales de Cristian Aboitiz | Dual: no comercial libre / comercial con autorización | `LICENSE-ABOITIZ.md` |
| 3a. Contribuciones de este fork — **contenido** | CC BY-SA 4.0 | `LICENSE-CC-BY-SA-4.0.md` |
| 3b. Contribuciones de este fork — **código** | MIT | `LICENSE-MIT` |
| 4. Fuentes oficiales incorporadas | Libre reproducción, por su propio régimen | ver sección 4 |

**Ante duda sobre un archivo, manda la capa más restrictiva que le aplique.**

---

## Linaje

    Anthropic, Inc.  ·  claude-for-legal              Apache 2.0
        └─ Probanza-ar  ·  Cristian Aboitiz           licencia dual
             └─ ciri-cuervo  ·  este repositorio      CC BY-SA 4.0 el contenido, MIT el código

Cada eslabón agrega contenido propio sin poder relicenciar el anterior.

---

## 1 · Código base de Anthropic — Apache 2.0

El repositorio nació como fork de `claude-for-legal` de **Anthropic, Inc.**, publicado bajo
**Apache License 2.0** (`LICENSE`). Esa licencia es irrevocable respecto de ese código,
conforme al art. 2, y este repositorio no la modifica ni la reemplaza.

**En el árbol actual no queda ningún archivo de Anthropic.** Los trece plugins de derecho
estadounidense, el tooling de `scripts/` y los cookbooks se eliminaron en el refactor de
septiembre de 2026; no subsiste ningún encabezado de copyright ni identificador SPDX de
Anthropic. El historial de git sí los conserva, y por eso la licencia se mantiene.

**Marca.** "Claude" es marca registrada de Anthropic, PBC. Su mención acá es uso descriptivo,
permitido por la cláusula 6 de la Apache 2.0, y no otorga derechos sobre la marca.

## 2 · Contribuciones de Cristian Aboitiz — licencia dual

**Copyright (c) 2024-2026 Cristian Aboitiz. Todos los derechos reservados.**
Términos completos en `LICENSE-ABOITIZ.md`, conservados palabra por palabra.

En síntesis, y sin sustituir ese texto: uso no comercial, académico o de investigación libre
manteniendo la nota de copyright y la atribución; **todo uso comercial requiere autorización
previa y expresa** del titular (`cristianaboitiz@gmail.com`).

**Qué cubre hoy: todo lo que está bajo `derecho/kb/`** — 109 archivos, unas 31.500 líneas, contando `kb/project/`.

Desde la reestructura de septiembre de 2026 **la frontera es estructural**: si el archivo está
bajo `kb/`, es capa 2; si no, es capa 3 —contenido CC BY-SA 4.0, código MIT, según la sección 3—.
`kb/README.md` detalla qué hay en cada
subdirectorio. Hay **una sola excepción, en el sentido inverso**, declarada abajo:
`kb/project/README.md`.

> **`kb/project/` es capa 2, aunque sea el camino anterior a la skill.** De sus 1.272 líneas,
> **1.169 son de Cristian Aboitiz** —`CLAUDE.md` 422 de 495, `setup-interview.md` 360 de 363,
> `setup-output-TEMPLATE.md` 310 de 319, `legal.local.md.template` 180 de 180—, así que su
> lugar es bajo `kb/` y no afuera. La regla es estructural justamente para que esto no dependa
> de una nota al pie: el repositorio es público y no puede declarar como propio lo que no lo es.
>
> **`kb/README.md` y `kb/project/README.md` son la excepción inversa,** y son las dos únicas:
> están escritas por el titular del fork para explicar qué hay en ese directorio, con qué
> licencia entra y en qué contradice a la skill. Son **capa 3a (CC BY-SA 4.0) bajo una ruta de
> capa 2**, y `fuga_textual.py` las excluye del corpus por eso: si no, compara nuestro texto
> contra sí mismo y reporta como fuga lo que es nuestro.

### El estado de la capa 2, y cómo se sostiene

`derecho/kb/` difiere del fork de Cristian Aboitiz al 23/07/2026 **sólo por reescritura de
rutas y por la marca del repositorio** — las cuatro diferencias restantes están en
`kb/project/CLAUDE.md` y son de ese tipo.

**La frontera se cruza en los dos sentidos, y cada uno tiene su herramienta.**

| Sentido | Qué sería | Qué lo vigila |
| --- | --- | --- |
| Prosa de `kb/` que entra a un módulo | Copiar en vez de reescribir contra fuente primaria | `herramientas/fuga_textual.py` |
| Texto propio que sale hacia `kb/` | Corregir el perfil heredado en el archivo del perfil | `herramientas/frontera_kb.py` |

El segundo importa más de lo que parece, porque **desactiva al primero**: `fuga_textual.py`
compara los módulos contra `kb/`, así que reescribir una línea de `kb/` con palabras propias
hace desaparecer la coincidencia que el detector busca. `frontera_kb.py` guarda el sha256 de
cada archivo en `herramientas/kb-procedencia.json` y sale con código 1 si alguno cambia. No
prohíbe editar `kb/` —corregir un error puntual es mantenimiento legítimo, y así lo dice
`kb/README.md`— pero obliga a que el cambio sea deliberado y quede fechado.

**Y hay un tercer riesgo, propio de los bloques de contradicciones nominadas.** Esos bloques
citan entre comillas lo que dice el perfil heredado para nombrar su error. Si la cita no es
textual, el módulo termina discutiendo con una frase que nadie escribió. `test_scripts.py`
verifica que **toda cita entrecomillada de un bloque de contradicciones exista literalmente bajo
`kb/`**, y `fuga_textual.py` excluye esos tramos citados para no reportar como fuga la cita que
el otro test exige que sea verbatim.

**Cómo se verifica el corte, ahora que este repositorio no tiene historial.** Se publicó sin
historia, así que el límite **no se puede reconstruir desde acá** con `git log` ni con
`git blame`. Se verifica contra el origen, que es público y sigue en pie:

```sh
git ls-tree -r --name-only 224c8401fcb0463d9646ab00a1fedd71fde3e878
# repositorio: https://github.com/Probanza-ar/claude-for-legal-argentina
```

Ese commit es el estado del fork de Cristian Aboitiz al 23/07/2026, y **todo lo que liste bajo
`derecho/` es capa 2**, esté hoy donde esté en este árbol. Lo que no figure ahí es de la capa
3 o de la 4. Contenido de la capa 2:

- Perfiles de área: `*-CLAUDE.md` y `*-DOCTRINA*.md` de laboral, civil, penal, previsional,
  administrativo, tributario, societario, concursos, consumidor, familia, tránsito,
  discapacidad y protección de datos
- `kb/jurisdicciones/administrativo/` — 19 perfiles jurisdiccionales por provincia
- `kb/especialidades/` — notarial, medicina legal, violencia digital
- Escritos y modelos: `civil/`, `consumidor/`, `familia/`, `penal/`, `previsional/`,
  `transito/`, y `kb/escritos/laboral/telegrama/` con sus ocho bloques
- `kb/contratos/` — perfil, red flags e índices
- Transversales: `kb/marcadores-GLOSARIO.md`, `kb/transversales/plazos-SKILL.md`, `kb/transversales/diagnostico-SKILL.md`,
  `kb/transversales/bucles-SKILL.md`, `kb/transversales/fuentes-y-conectores.md`, `kb/ejemplos/`, `kb/CHANGELOG.md`
- **Cuatro casos de `evals/`** y `evals/README.md` — `administrativo-caba-recursos-agotamiento-via`,
  `consumidor-dano-punitivo-prescripcion`, `consumidor-garantia-producto-defectuoso` y
  `consumidor-prepaga-aumento-dnu70`, que son los que figuran en el commit de arriba. **Quedan
  fuera de `kb/`** por estar junto a los demás evals: son la excepción a la regla estructural y
  se listan acá. Los otros trece se escribieron en este fork.
  **El README de `evals/` se llama `evals-README.md` en el fork de origen** y acá se renombró a
  `README.md`, que es el único nombre que GitHub muestra al abrir el directorio. Es un cambio de
  nombre y nada más: el contenido es de su autor. Se anota porque para los archivos de capa 2 que
  viven bajo `kb/` la procedencia la da la ruta, y para estas cinco excepciones la da esta lista

> **Sobre la enumeración de la sección 2 de `LICENSE-ABOITIZ.md`.** Ese listado se escribió
> cuando el repositorio tenía otra estructura y menciona `skills/` y `perfiles/`. Es, por sus
> propios términos, *"sin limitación"*: describe, no delimita. La lista de arriba no lo
> reinterpreta ni lo recorta — dice qué archivos de los que hoy están en el árbol venían de su
> fork. `derecho/skills/` **no** es uno de ellos: ese directorio no existía en su fork y su
> contenido se escribió en este, como muestra el historial.

### Una precisión sobre el vocabulario de marcadores

La skill **usa los mismos identificadores de marcador** que `derecho/kb/marcadores-GLOSARIO.md`
— `[ALERTA PLAZO FATAL: ...]`, `[SIN PERFIL DE ÁREA CARGADO: ...]`, `[VERIFICAR PRECEDENTE: ...]`
y los demás—, y eso es deliberado y necesario: son un **vocabulario controlado**, no prosa. La
sintaxis tiene que ser exacta porque los scripts emiten esas cadenas y las salidas se auditan
contra ellas; una paráfrasis rompería el sistema. Se reproducen como **identificadores
funcionales**.

Desde septiembre de 2026 la **definición** de ese vocabulario —qué significa cada marcador,
cuándo corresponde, qué campos lleva y qué formas hay que reemplazar— está escrita de cero en
`derecho/skills/derecho-argentino/references/marcadores.md`, que es capa 3a (CC BY-SA 4.0) y es la
fuente de verdad de la skill. El glosario heredado permanece bajo la licencia de la capa 2 y
ya no es consultado por ningún módulo. Esta nota queda acá para que el punto esté declarado y
no descubierto.

### Una precisión sobre las citas que nombran un error del perfil

Varios módulos traen tablas de **contradicción nominada**: una columna dice lo que afirma el
perfil heredado y la otra lo que dice la fuente primaria. Nombrar el error exige transcribir
la frase equivocada, siempre **entrecomillada e identificada como del perfil**, y siempre del
largo mínimo para que se entienda cuál es la afirmación que se corrige.

Es cita para crítica, no incorporación: el módulo no se sirve de esa prosa para explicar el
instituto —lo explica de cero contra fuente primaria— sino para advertir que no hay que
seguirla. Se deja declarado por la misma razón que el punto anterior: mejor dicho acá que
descubierto después.

### Cómo se controla que la frontera se respete

`herramientas/fuga_textual.py` compara secuencias contiguas de nueve palabras entre `kb/` y el
resto del repositorio. Descuenta lo que también aparece en `fuentes/normas/` —texto legal, de
libre reproducción— y lo que es vocabulario de cita —número de ley, artículo, inciso, fecha,
plazo—, porque el articulado, los plazos y las carátulas de fallos no son obra de nadie y se
mueven libres.

Lo que sobrevive a esos filtros es **candidato**, no culpable: decidir si una coincidencia es
cita legal, dato o prosa copiada es una lectura, y por eso el resultado de haberla hecho queda
registrado en `herramientas/fuga-revisada.json`. La corrida reporta sólo lo nuevo, que es lo
único sobre lo que hay que decidir algo.

La revisión de septiembre de 2026 pasó por todos los módulos de `references/`. Las coincidencias
que quedaron aceptadas son de cuatro tipos: texto legal citado, filas de tabla con norma y
plazo, rutas de ruteo que apuntan a `kb/` por construcción, y las citas para crítica del punto
anterior. Las que no entraban en ninguno —siete al momento de la partición, más dos halladas
en septiembre en el art. 76 ter y en la enumeración del art. 14 CP— se reescribieron contra
fuente.

### Atribución requerida

La sección 3 de su licencia exige incluirla en lugar visible en toda redistribución. Está en
el `README.md` y se reproduce acá:

> "Basado en contribuciones originales de Cristian Aboitiz (github.com/Probanza-ar),
> publicadas bajo licencia dual. El código base proviene de claude-for-legal (Anthropic,
> Inc.), licenciado bajo Apache 2.0."

Además, sus términos prohíben que forks de su fork usen su nombre, `@abogadoaboitiz` o
denominaciones que confundan sobre la autoría original, sin autorización escrita.

## 3 · Contribuciones de este fork — dos licencias, y la frontera es la ruta

**Copyright (c) 2026 ciri-cuervo.** Lo creado en este fork se divide en dos capas según
**qué es el archivo**: lo que se lee y se cita va con licencia de contenido; lo que se
ejecuta, con licencia de código.

| | Licencia | Texto |
| --- | --- | --- |
| **3a · Contenido** | **CC BY-SA 4.0** | `LICENSE-CC-BY-SA-4.0.md` |
| **3b · Código y datos de máquina** | **MIT** | `LICENSE-MIT` |

### 3a · Contenido — CC BY-SA 4.0

Atribución y **CompartirIgual**: se usa y se adapta libremente, **incluido el uso comercial**, y lo
que se distribuya adaptado lleva la misma licencia.

- `derecho/skills/derecho-argentino/SKILL.md` y los **61 módulos** de `references/`
- `derecho/commands/` — los **8 comandos slash**, que son instrucciones y no programas
- `derecho/evals/` — los **49 casos** de verificación con su rúbrica y su resultado esperado
- `derecho/fuentes/MANIFIESTO.md` y `derecho/fuentes/jurisprudencia/INDICE.md`
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/rules/`, los **6 documentos** de `docs/`,
  `CHANGELOG.md`, `assets/marca/README.md` y este archivo
- `assets/marca/` — el sello, el ícono, las chapitas y el separador, con sus fuentes SVG
- `assets/logos/` **queda afuera**: son marcas de terceros; ver sección 4
- `derecho/skills/derecho-argentino/references/danos-indice-doctrinario.md` — índice destilado de
  obra de terceros; ver sección 4

**Por qué CompartirIgual y no MIT.** El valor de esta capa no es el texto sino **el trabajo de
verificación que hay detrás**: cada norma cotejada contra su fuente, cada holding leído contra el
documento, cada número medido y no recordado. CompartirIgual no impide que alguien lo use ni que
gane dinero con él: impide que lo **cierre**. Si mejora un módulo y lo publica, vuelve con la misma
licencia. Es la única condición que pide esta capa.

**Y por qué permite el uso comercial.** Porque el público son abogados en ejercicio, y usar esto en
un estudio **es** uso comercial. Una licencia que lo prohibiera excluiría a quien la herramienta
está pensada para servir.

### 3b · Código y datos de máquina — MIT

Permisiva, sin condiciones más allá de conservar el aviso de copyright: el código está para que se
lo lleven a otro proyecto sin arrastrar nada.

- `derecho/skills/derecho-argentino/scripts/` — los scripts de la skill con su suite de tests
- `derecho/fuentes/scripts/` — los descargadores y verificadores de la capa de fuente primaria
- `herramientas/` — las **15 herramientas** de control: frontera de licencia, calidad de OCR,
  auditoría de fechas, cobertura normativa, cifras de la documentación, reformas sin leer,
  verificación de marcadores de una respuesta, mapa de ruteo, ortografía, y sus tests
- Los `.json` de manifiesto, procedencia y veredicto: `normas.json`, `fallos.json`, los
  `procedencia.json`, `inhabiles.json`, `herramientas/lecturas-ocr.json`,
  `herramientas/fuga-revisada.json`, `herramientas/cifras.json` y los `-revisad*.json`
- `.claude-plugin/marketplace.json` y `derecho/.claude-plugin/plugin.json`

### Lo que esta elección no toca

Alcanza **solo a la capa 3** y no modifica en nada las condiciones de las capas 1, 2 y 4. `kb/`
sigue con la licencia dual de su autor, las normas y sentencias con su régimen de libre
reproducción, y el linaje de Anthropic con Apache 2.0.

> **Una consecuencia que conviene tener presente.** El titular del copyright puede relicenciar su
> propia obra cuando quiera; **lo que aporte un tercero bajo CC BY-SA, no** — salvo cesión expresa.
> Si en algún momento se quisiera una versión cerrada, la decisión hay que tomarla **antes** de
> aceptar el primer aporte externo.

## 4 · Fuentes oficiales y material de terceros

**Textos normativos y sentencias** (`derecho/fuentes/normas/`, `jurisprudencia/`): normas y
sentencias de organismos públicos argentinos, de libre reproducción y sin derechos de autor
(art. 1 de la Ley 11.723 y su interpretación corriente). Cada archivo lleva su URL de origen,
fecha de descarga y hash en `procedencia.json`.

**Código Civil y Comercial Comentado** (`derecho/fuentes/ccyc-comentado/`, seis tomos):
publicación oficial de **SAIJ - INFOJUS**, Ministerio de Justicia y Derechos Humanos de la
Nación, 2022, **de libre reproducción**. Se puede citar y transcribir.

**Series de datos** (`derecho/fuentes/datos/`): IPC, RIPTE y CER de la API de Series de
Tiempo del Estado; valor del jus de la SCBA. Datos públicos.

**Logos de Claude y de Codex** (`assets/logos/`): son **marcas registradas de sus titulares**
—Anthropic para Claude, OpenAI para Codex— y **no** quedan cubiertos por la CC BY-SA de la capa
3a: quien reutilice este repositorio no recibe ningún derecho sobre ellos. Están acá por **uso
nominativo**, para señalar en qué aplicación se instala cada camino de `## Instalar`, sin
modificarlos y sin quedar más prominentes que la marca propia, que es la condición que pone
OpenAI en sus [pautas de marca](https://openai.com/brand/). Si alguno de los dos titulares pide
retirarlos, se retiran y los encabezados siguen diciendo lo mismo en texto.

**Obras comerciales — no están en el repositorio.** `derecho/skills/derecho-argentino/references/danos-indice-doctrinario.md` es un
índice destilado del *Manual de Derecho de Daños* (2ª ed., Weingarten -dir.-, La Ley, 2015):
38 entradas por instituto con síntesis y remisión a capítulo y página. **La obra tiene derechos
reservados: su PDF no está acá y no debe incorporarse.** En un escrito se cita la obra, nunca
el archivo. `derecho/fuentes/_local/` está en `.gitignore` justamente para que los
ejemplares locales de obras comerciales no se suban nunca.

---

## Sin garantías

Los materiales se proveen "tal como están", sin garantía de ningún tipo, expresa o implícita.
Los autores no asumen responsabilidad por el uso que terceros hagan de ellos en el ejercicio
profesional. **Nada en este repositorio constituye asesoramiento jurídico**, y ninguna salida
de esta skill reemplaza el criterio del profesional que firma.
