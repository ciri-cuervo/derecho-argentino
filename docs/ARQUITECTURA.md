# 🧭 Cómo está armado

El repositorio es a la vez el **marketplace** y el **plugin**. `.claude-plugin/marketplace.json`
publica un solo plugin, `derecho`, cuyo `source` es `derecho/`. De ahí salen los nombres que se
ven en Claude: la skill queda como `derecho:derecho-argentino` —igual en la app de escritorio que
en la consola— y, en Claude Code, los comandos como `/derecho:...`.

El directorio se sigue llamando `derecho/` a propósito: es el `source` del plugin y renombrarlo
tocaría cientos de rutas en los módulos, para algo que el usuario no ve.

**Codex apunta a la misma carpeta.** `.agents/plugins/marketplace.json` —la ubicación que pide el
formato Agent Plugins— declara el mismo `./derecho` como `source`. La ruta se resuelve **desde la
raíz del marketplace, que es la raíz del repositorio, y no desde la carpeta que contiene el
`marketplace.json`**: esa confusión costó una versión entera apuntando a un `plugins/` que no
existe. Con `derecho/` como raíz del plugin, la disposición es la que el formato espera sin
inventar nada: el manifiesto portable en `derecho/plugin.json` y las skills en
`derecho/skills/`, que Codex descubre por convención. `.claude-plugin/` es el manifiesto de
compatibilidad de Claude sobre esa misma raíz.

## El árbol

```
README.md                           # la puerta de entrada: instalar, usar, reportar
CHANGELOG.md                        # versiones del plugin (SemVer)
LICENCIAS.md                        # mapa de las cuatro capas de autoría
LICENSE · LICENSE-ABOITIZ.md · LICENSE-MIT · LICENSE-CC-BY-SA-4.0.md
SECURITY.md                         # qué reportar, por dónde, y qué NO subir
.claude-plugin/marketplace.json     # el marketplace de Claude: un solo plugin
.agents/plugins/marketplace.json    # el mismo plugin en formato Agent Plugins (Codex)
.github/workflows/tests.yml         # los seis suites en cada push y cada pull request
derecho/                          # el plugin
  .claude-plugin/plugin.json        # manifiesto de Claude
  plugin.json                       # manifiesto portable, el que lee Codex
  commands/                         # ocho comandos slash
  skills/derecho-argentino/
    SKILL.md                        # núcleo: apertura, integridad, marcadores, ruteo
    references/                     # 31 módulos, numeración global estable, carga bajo demanda
    scripts/                        # calculadoras, perfil, diagnóstico y tests
  fuentes/                          # capa de fuente primaria offline
    MANIFIESTO.md                   # qué hay bajado, de dónde y con qué fecha
    normas/                         # texto consolidado + procedencia por hash
    jurisprudencia/                 # fallos verificados + INDICE.md
      ocr/                          # texto recuperado por OCR local, derivado del PDF
    datos/                          # jus, inhábiles, IPC, RIPTE, CER
    ccyc-comentado/                 # CCyC Comentado oficial (SAIJ-INFOJUS), seis tomos
    scripts/                        # descargadores y verificador de vigencia
  evals/                            # casos con rúbrica y resultado esperado
  kb/                               # base de conocimiento heredada · LICENCIA DISTINTA
    perfiles/                       # perfiles de área por rama
    doctrina/                       # doctrina y leading cases por instituto
    escritos/                       # 34 modelos y 7 guías de armado, incluidos telegramas
    jurisdicciones/administrativo/  # 19 provincias
    especialidades/ contratos/ ejemplos/ transversales/
    marcadores-GLOSARIO.md          # glosario heredado; la skill ya no depende de él
    CHANGELOG.md                    # historial de la base de conocimiento
    project/                        # camino anterior: perfil para pegar en un Project
herramientas/                       # control de la frontera de licencia, en los dos sentidos, y del OCR
assets/marca/                       # sello, ícono, chapitas y separadores; salen de un script
assets/logos/                       # logos de Claude y Codex, para las instrucciones de instalación
docs/
  ARQUITECTURA.md                   # esto
  DESARROLLO.md                     # cómo se trabaja sobre el plugin y qué se corre antes de cerrar
  TERMINAL.md                       # instalar por consola: Claude Code y Codex a mano
  AUDITORIAS.md                     # qué se verificó contra fuente primaria, y cuándo
```

## La frontera de licencia es la ruta

**`derecho/kb/` es de otro autor.** Es la contribución original de Cristian Aboitiz, con uso
comercial **sujeto a autorización previa**. Bajo `kb/`, capa 2. Fuera, este fork, con dos licencias
según qué sea el archivo: **el contenido es CC BY-SA 4.0** —los módulos, los comandos, los evals, la
documentación y la marca— y **el código es MIT** —los scripts, los descargadores y las
herramientas—. Las dos permiten el uso comercial; el contenido pide atribución y CompartirIgual. El
mapa completo, en [`LICENCIAS.md`](../LICENCIAS.md), y el detalle de `kb/` en
`derecho/kb/README.md`.

Ese material **no pasó la auditoría contra fuente primaria** que sí pasaron los módulos de
`references/`, y en varios puntos los contradice en derecho aplicable, no en vigencia. Cada tabla
de ruteo de la skill lleva un bloque de **contradicciones nominadas** que dice cuáles y cómo se
resuelven.

**La frontera se cruza en los dos sentidos y cada uno tiene su herramienta.** `fuga_textual.py`
mira que no entre prosa de `kb/` a un módulo; `frontera_kb.py` mira lo contrario, que no salga
texto propio hacia `kb/` —que es el sentido fácil de cruzar sin darse cuenta, porque se cruza
corrigiendo el perfil heredado, y además desactiva al primero—. Detalle en
[`LICENCIAS.md`](../LICENCIAS.md) §2.

`derecho/kb/project/` es la arquitectura previa a la skill y **Claude Code no la carga**: un
perfil general para pegar en un Project de claude.ai más la entrevista de configuración que lo
personaliza. Se superpone con la skill y en un punto la contradice —fija un fuero por defecto,
que es justo lo que la sección 0.1 prohíbe—. Sigue ahí porque funciona sin Claude Code. Ante
conflicto, manda la skill. Ver `derecho/kb/project/README.md`.

## Los módulos de `references/`

Son 30. Estos son los que se cargan más seguido; el listado completo está en el directorio.

| Módulo | Sección | Qué cubre |
| --- | --- | --- |
| `intake.md` | — | Qué datos pedir antes de analizar, según la tarea |
| `sede-judicial-pba.md` | 1.6 | Desde el órgano: veredicto, sentencia, control de oficio, congruencia, costas, honorarios |
| `parte.md` | 1.7 | Desde una parte: demanda, contestación, audiencia preliminar, prueba, recursos |
| `laboral.md` | 5 | Tramos de reforma, extinción, intereses, prescripción, riesgos del trabajo, liquidación |
| `civil.md` | 6 | Derecho intertemporal, responsabilidad, prescripción, contratos de entrada |
| `contratos.md` | 7 | Revisión y redacción, red flags |
| `plazos.md` | 8 | Tipos de plazo, gracia, ferias, suspensión por mediación |
| `escritos.md` | 9-11 | Diagnóstico, armado desde cero, formato de salida |
| `kb/transversales/fuentes-y-conectores.md` | 14 | Dónde verificar una norma, un fallo o un monto |
| `changelog-normativo.md` | 13 | Cambios recientes y estado de verificación por bloque |
| `consumidor.md` | 17 | Relación de consumo, daño punitivo, gratuidad, prescripción |
| `familia.md` | 18 | Fuero PBA, Consejero, alimentos y Ley 15.513, violencia |
| `otras-ramas.md` | 19 | Ruteo a los perfiles de área del repo |
| `prueba-pericial.md` | 20 | Designación, control, impugnación y valoración del dictamen |
| `ejecucion.md` | 21 | Liquidación, embargo, excepciones, vía ejecutiva |
| `notificaciones-pba.md` | 22 | Cédula electrónica, MEV, cuándo empieza a correr el plazo |
| `modelos.md` | 23 | Inventario de los modelos de escritos del repo |

La numeración es **global y estable**: las remisiones cruzadas entre módulos siguen siendo
válidas aunque el archivo se mueva.

## La capa de fuente primaria

Hay dos archivos y cuentan cosas distintas, así que los números no coinciden y no tienen por qué:
`normas.json` es el **catálogo** de lo que la skill espera encontrar, con la URL de origen de cada
entrada, y `procedencia.json` es el **registro de lo que se bajó**, con hash SHA-256 y fecha. Una
entrada puede estar catalogada y no bajada —falta la URL oficial— y otra puede estar bajada sin
URL propia, como `cn-tratados-ddhh`, la Constitución con los tratados de jerarquía constitucional,
que se consolidó a mano. De los fallos, catálogo y procedencia coinciden.

**Las cifras no van acá.** Están en `fuentes/MANIFIESTO.md`, donde `test_scripts.py` las compara
contra lo que hay en disco: una cifra escrita a mano sobre algo que crece envejece en silencio, y
repetirla en dos documentos garantiza que uno de los dos mienta. La medición viva la da
`estado.py`.

### Las fuentes viajan con el plugin, y es una decisión

`fuentes/` son 63 de los 67 MB que se lleva quien instala: el 94%. No es un descuido — **se
prefiere que el primer uso sea offline**. Quien instala el plugin tiene los textos normativos,
los fallos y el CCyC Comentado desde el minuto cero, sin depender de que InfoLEG esté arriba, de
que su red llegue, ni de correr nada antes de la primera consulta.

La alternativa —venir con los catálogos, los hashes y los índices, y bajar los cuerpos en el
primer uso— dejaría el plugin en 7 MB, y la maquinaria existe: `normas.json` tiene URL y hash,
`estado.py` dice qué falta y `/derecho:actualizar` lo baja. **Se evaluó y se descartó**: cambia
una descarga grande por una dependencia de red en el momento en que alguien está resolviendo un
expediente. Queda escrito para que no se "optimice" sin querer.

`verificar_normas.py` vuelve a pedir cada norma con URL y sale con código 1 si alguna cambió: es
una alarma de reforma legislativa, no un backup.

Las series con fecha —valor del jus, días inhábiles, IPC, RIPTE, CER— viven en
`fuentes/datos/`. Son las que vencen, y las que `/derecho:estado` mira para avisar.

## Cómo los scripts encuentran el repo

**No hay ninguna ruta absoluta en la skill.** Los scripts la resuelven en este orden: el
argumento `--repo`, la variable `DERECHO_AR_REPO`, la variable `CLAUDE_PLUGIN_ROOT` que define
Claude Code al instalar el plugin, `~/.config/derecho-argentino/config.json`, subiendo desde la
ubicación de la skill, y unas pocas ubicaciones habituales bajo el home. El primer hallazgo por
heurística queda fijado solo. Para fijarlo a mano:

```sh
python3 derecho/skills/derecho-argentino/scripts/configurar.py --repo /ruta/al/repo
```

También se puede clonar el repo y copiar `derecho/skills/derecho-argentino/` a
`~/.claude/skills/`, o cargar los perfiles de `derecho/` en un Project de claude.ai.

---

[Volver al README](../README.md) · [Desarrollar el plugin](DESARROLLO.md) ·
[Auditorías](AUDITORIAS.md)
