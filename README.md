<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/marca/banner-oscuro.png">
    <img src="assets/marca/banner-claro.png" width="760"
         alt="Sello de cargo con la leyenda DERECHO ARGENTINO y los campos PBA, NACIÓN y CABA">
  </picture>
</p>

<h1 align="center">Derecho argentino</h1>

<p align="center">
  <b>Un asistente jurídico para Claude y ChatGPT que no inventa:<br>
  cuando no puede verificar un dato, te lo dice.</b>
</p>

<p align="center">
  <a href="CHANGELOG.md"><img src="assets/marca/chapa-version.png" width="106" height="32" alt="Versión 1.4.3"></a>
  <a href="LICENCIAS.md"><img src="assets/marca/chapa-licencia.png" width="168" height="32" alt="Licencias: contenido CC BY-SA 4.0, código MIT"></a>
  <img src="assets/marca/chapa-agentes.png" width="172" height="32" alt="Corre en Claude y Codex (ChatGPT)">
</p>

<p align="center">
  <a href="#-instalar"><b>Instalar</b></a> ·
  <a href="#-qué-le-podés-pedir">Qué le podés pedir</a> ·
  <a href="#-así-se-ve">Un ejemplo</a> ·
  <a href="#-si-algo-no-anda">Si algo no anda</a> ·
  <a href="#-contar-cómo-te-fue">Contar cómo te fue</a>
</p>

<img src="assets/marca/separador.png" width="100%" alt="">

**Para abogados, jueces y personal de tribunales.** Se instala en la app de Claude o en la de
ChatGPT, y después se le habla como a un colega: le contás el caso y te devuelve la norma
aplicable, el cálculo o el borrador, **con la fuente de cada cosa a la vista**. No hace falta saber
programar ni configurar nada.

**Lo que lo distingue es lo que se niega a hacer.** No cita un fallo que no tenga verificado, no
completa un monto de memoria y no da por sentado desde dónde consultás. Cuando le falta algo, lo
deja marcado y te dice qué falta, en vez de entregarte un dato plausible que nadie va a revisar.

## 🧭 Qué le podés pedir

| Le pedís… | Y te devuelve… |
| --- | --- |
| 💼 **Liquidar un despido** | El régimen que rige según la fecha, cada rubro con su artículo, y el tope que falta cargar marcado como tal |
| 📅 **Contar un plazo** | El vencimiento con ferias, feriados y plazo de gracia, y cuándo quedó notificado en PBA |
| 💰 **Actualizar un crédito o regular honorarios** | La cuenta hecha con la serie oficial —jus, UMA, IPC— y el criterio que la sostiene |
| 📚 **Qué dice la ley hoy** | El artículo vigente, la reforma que lo cambió y desde cuándo |
| ✍️ **Revisar o armar un escrito** | Lo que falta, lo que se cita mal y lo que conviene preguntar antes de presentar |
| ⚖️ **Trabajar desde el juzgado** | La sentencia o el proveído del lado del órgano: qué se controla de oficio y qué no se construye |

El alcance es el **derecho argentino**, y lo que ya está auditado crece versión a versión: hoy son
**68 módulos**, cada uno con su fecha de verificación contra el texto oficial. Donde todavía no hay
módulo, la skill abre material de apoyo y **avisa cada vez que ese material no está auditado**. El
mapa de lo cubierto está en [`docs/COBERTURA.md`](docs/COBERTURA.md).

## 🛡️ Por qué podés confiar en lo que te dice

**📜 Trabaja con los textos oficiales, sin conexión.** Trae guardado el texto consolidado de
**273 normas** y **99 fallos**, bajados de InfoLEG, el Boletín Oficial, `normas.gba.gob.ar`, SAIJ y
JUBA, cada uno con su dirección de origen y su fecha. Una vez por semana se vuelve a comparar
cada norma contra el sitio oficial para detectar una reforma.

**🔢 Las cuentas las hace una calculadora, no el modelo.** La liquidación, los plazos, los
intereses y los honorarios salen de programas que siempre dan el mismo resultado con los mismos
datos. Si falta un valor —el tope del art. 245, el jus del mes— la calculadora no lo inventa: se
detiene y lo pide.

**🙋 Pregunta antes de asumir.** No da por sentado si consultás por una parte o desde un
tribunal, ni qué régimen rige: en el fuero laboral bonaerense conviven dos códigos procesales según
la fecha de la audiencia de vista, y la skill pregunta esa fecha antes de citar uno.

**🏷️ Marca lo que no pudo verificar.** Un dato que no se pudo confirmar sale como
`[VERIFICAR ...]`, con lo que falta para resolverlo. Es una señal para vos, no un error: se completa
antes de presentar.

## 👀 Así se ve

Caso inventado. Lo que importa está al final: el número que **no** da.

```text
Vos:    Liquidación por despido sin causa. Ingresó el 03/03/2019, la despidieron el
        10/08/2026, mejor remuneración $1.450.000. Fábrica en Quilmes.

Skill:  Antes de liquidar, dos cosas que no asumo: ¿consultás por la trabajadora, por la
        empleadora o desde un tribunal? ¿Y el reclamo va por el fuero laboral bonaerense?

Vos:    Por la trabajadora. Laboral PBA.

Skill:  Acto extintivo del 10/08/2026: rige la LCT con la Ley 27.802. Corrí la calculadora
        y transcribo su salida; antes del resultado, los datos que tomó:
          fecha ingreso 2019-03-03 · fecha extinción 2026-08-10 · antigüedad 7 años y 5 meses
          Indemnización por antigüedad   11.600.000,00   Art. 245 LCT   base 1.450.000 x 8
          Indemnización sustitutiva de preaviso   2.900.000,00   Arts. 232 y 231 LCT
          [...]
        Sin tope informado: la base del art. 245 se calculó SIN tope y el resultado no es
        definitivo hasta cargar el tope del CCT del período. No lo cito de memoria:
          [VERIFICAR MONTO ACTUALIZADO: tope art. 245 LCT - CCT aplicable, resolución del MTEySS del período del acto extintivo]
          [VERIFICAR CCT APLICABLE: actividad del empleador - tope art. 245 y escalas salariales del período]
        Los agravantes de las Leyes 24.013 y 25.323 están derogados para esta fecha: no van.
```

<img src="assets/marca/separador.png" width="100%" alt="">

## 📥 Instalar

Se instala por menú, como cualquier programa, y **alcanza con hacerlo una vez**. Si no sabés qué
camino elegir, usá la app de Claude: es el más corto.

> [!IMPORTANT]
> **La descarga son unos 91 MB**, casi todo normas y fallos, para que funcione sin conexión. La
> primera vez tarda un rato.

En algún momento la app te va a pedir una dirección. **Es siempre esta, y es lo único que hay que
copiar y pegar:**

```text
ciri-cuervo/derecho-argentino
```

### <img src="assets/logos/claude.svg" height="20" alt=""> En la app de Claude

1. **Bajá la app** desde [claude.com/download](https://claude.com/download), instalala y abrila.
   La primera vez pide iniciar sesión.
2. **Agregá el catálogo.** En la barra lateral: **Personalizar** → pestaña **Plugins** →
   **Agregar** → *Agregar marketplace* → *Agregar desde un repositorio*, y en *URL* pegá la
   dirección de arriba.
3. **Instalá el plugin.** En la lista aparece **Derecho argentino**, bajo *Nuevo*. Tocá el **+**
   de su tarjeta; cuando se convierte en una tilde, quedó instalado.

Queda disponible en los modos **Chat y Cowork** y **Code** de la app.

<details>
<summary><b>En la app de Codex / ChatGPT</b></summary>

<br>

1. **Bajá la app** desde [openai.com/es-419/codex](https://openai.com/es-419/codex/) —es el agente
   de ChatGPT para computadora—, instalala y abrila. La primera vez pide iniciar sesión.
2. **Agregá el catálogo.** En **Complementos** → **Agregar** → *Agregar marketplace*. En *Origen*
   pegá la dirección de arriba; *Referencia de Git* y *Rutas dispersas* quedan vacíos.
3. **Instalá el plugin.** No aparece en la pestaña *Público*: está en **Personal**, bajo
   *Derecho argentino*. Tocá el **+** de la fila `derecho`.

</details>

<details>
<summary><b>Desde la terminal</b>, si ya la usás</summary>

<br>

Claude Code por marketplace y Codex a mano, con los comandos para macOS, Linux y Windows:
**[Instalar desde la terminal](docs/TERMINAL.md)**.

</details>

**Y con eso ya está.** La skill se activa sola en cuanto le hacés una consulta jurídica argentina:
describile un caso como se lo contarías a un colega.

### Comprobar que quedó bien

Pedíselo en castellano: *"corré el estado de la skill de derecho argentino"*. Te dice si encontró
sus datos, qué tiene cargado y cuánto hace que se verificó contra las fuentes oficiales. En Claude
Code, `/derecho:estado`.

> [!TIP]
> **Si te dice que no puede hacer un cálculo, le falta Python** —3.9 o posterior—, el único
> programa aparte que necesita y **sólo para las calculadoras**: citar normas, revisar un escrito
> o contar un plazo funciona igual sin él. En Mac y Linux casi siempre ya viene. Si no, se baja de
> **[python.org](https://www.python.org/downloads/)** y se instala con las opciones que trae; en
> Windows, dejá tildado *"Add python.exe to PATH"*. Después cerrá y volvé a abrir la app.

> [!IMPORTANT]
> **Los datos vienen con fecha de corte: septiembre de 2026.** El jus, el IPC, el RIPTE, el CER y
> los días inhábiles cambian todos los meses, y de ellos salen las liquidaciones y los
> vencimientos. **El primer día, pedile que se actualice:** *"actualizá las series y las fuentes"*.
> Si alguna fuente oficial no le deja bajar, te dice cuál y cómo hacerlo.

<img src="assets/marca/separador.png" width="100%" alt="">

## 💬 Usar

No hay palabras especiales que aprender: se describe el caso con los datos que tengas.

```text
Liquidación por despido sin causa: ingresó el 03/03/2019, despido el 10/08/2026,
mejor remuneración $1.450.000, no le pagaron nada. Trabajaba en La Plata.
```

```text
Me notificaron la demanda el viernes 11/9. ¿Cuándo vence para contestar en PBA?
```

```text
Soy empleado de un juzgado civil de la Ciudad. Revisame este proyecto de sentencia.
```

Te va a preguntar lo que falte —si sos la parte o el juzgado, qué fuero, qué fecha— porque de eso
depende la respuesta.

**Si lo vas a usar seguido, armá un proyecto.** Son tres líneas de instrucciones —desde dónde
consultás, en qué fueros, cómo querés las respuestas— y deja de preguntarlo en cada conversación.
Cómo se hace en cada app: **[Armar el proyecto, paso a paso](docs/PROYECTO.md)**.

> [!WARNING]
> **Es una herramienta de trabajo profesional.** Ayuda a redactar, calcular y verificar; no
> reemplaza el criterio de quien firma. Lo que salga marcado con `[VERIFICAR ...]` se resuelve
> antes de presentar.

<details>
<summary><b>Atajos para Claude Code</b>, la versión de consola</summary>

<br>

En la consola hay **ocho comandos** que van directo a cada tarea. En las apps de escritorio no
hacen falta: se pide lo mismo con palabras —*"liquidame este despido"*, *"calculame el
vencimiento"*— y el resultado es el mismo.

| Comando | Qué hace |
| --- | --- |
| `/derecho:liquidacion` | Liquidación por extinción del contrato de trabajo |
| `/derecho:plazo` | Cómputo de un plazo, con ferias, feriados trasladables y gracia |
| `/derecho:intereses` | Actualización e intereses sobre un crédito |
| `/derecho:honorarios` | Honorarios y aportes, según la jurisdicción |
| `/derecho:configurar` | Guarda cómo trabajás para que la skill no lo pregunte cada vez |
| `/derecho:estado` | Diagnóstico: qué datos tiene y qué quedó vencido |
| `/derecho:actualizar` | Baja normas, fallos y series de índices que falten |
| `/derecho:verificar` | Compara cada norma contra el sitio oficial y avisa si alguna cambió |

Los de cálculo no van derecho a la cuenta: primero identifican qué régimen rige y piden los datos
que faltan.

</details>

<img src="assets/marca/separador.png" width="100%" alt="">

## 🧰 Si algo no anda

<details>
<summary><b>Dice que no puede hacer un cálculo</b></summary>

<br>

Falta Python, y sólo lo necesitan las calculadoras. Está explicado arriba, en
[Comprobar que quedó bien](#comprobar-que-quedó-bien).

</details>

<details>
<summary><b>En ChatGPT / Codex no aparece el plugin</b></summary>

<br>

No está en la pestaña *Público*: está en **Personal**, bajo *Derecho argentino*, y se instala con
el `+` de la fila `derecho`.

</details>

<details>
<summary><b>Avisa que los datos están vencidos</b></summary>

<br>

Es lo esperado si lo instalaste después de la fecha de corte. Pedile *"actualizá las series y las
fuentes"*; en Claude Code, `/derecho:actualizar`. Si una fuente oficial no le deja bajar, te pasa
el comando para correrlo vos.

</details>

<details>
<summary><b>Dice que no encuentra sus datos</b></summary>

<br>

Pasa si instalaste a mano en Codex y después moviste la carpeta. Pedile *"configurá la ruta del
repositorio de derecho argentino"*; la ruta queda guardada.

</details>

<details>
<summary><b>Me devolvió un <code>[VERIFICAR ...]</code> y no sé qué hacer</b></summary>

<br>

Es la respuesta correcta ante un dato que no pudo confirmar, y dice exactamente qué falta. Se
resuelve aportando el dato o cotejando la fuente que nombra.

</details>

<details>
<summary><b>Contestó algo que está mal en derecho</b></summary>

<br>

Es lo más valioso que podés reportar. Cómo hacerlo, justo acá abajo.

</details>

## 🗣️ Contar cómo te fue

**El uso real es lo que más falta.** Los controles automáticos dicen si una norma cambió o si una
cuenta da; ninguno dice si esto te sirve en tu trabajo. Eso sólo lo sabés vos.

| Qué querés hacer | Dónde |
| --- | --- |
| **Contar cómo te fue**, para qué lo usaste, qué te resultó y qué no | [Discusiones · Experiencias](../../discussions) |
| **Preguntar** cómo se hace algo, o por qué contestó lo que contestó | [Discusiones · Preguntas](../../discussions) |
| **Proponer** un fuero, un instituto o un cálculo que falte | [Discusiones · Ideas](../../discussions) |
| **Reportar un error de derecho** —una norma vencida, un fallo mal citado, un plazo equivocado— | [Issues](../../issues/new/choose), con el formulario que pide la fuente |
| Algo que preferís no publicar | Ver [`SECURITY.md`](SECURITY.md) |

**Para reportar un error, lo que más ayuda son tres cosas:** qué te contestó, qué debería haber
contestado, y **la fuente** —artículo, fallo con carátula y fecha, o Boletín Oficial—. Con eso se
corrige y queda un caso de prueba para que no vuelva.

> [!CAUTION]
> **Nunca pegues datos de un expediente real** —ni carátulas, ni partes, ni montos, ni piezas—.
> Este sitio es público y queda indexado. Para mostrar un problema alcanza con inventar el caso,
> que es lo que hacen los propios [casos de prueba](derecho/evals/).

<img src="assets/marca/separador.png" width="100%" alt="">

## ⚖️ Licencias

**Usarlo en un estudio no requiere permiso de nadie.** El contenido de este proyecto es
**CC BY-SA 4.0**: se usa y se adapta libremente, incluido el uso comercial, atribuyendo y
publicando con la misma licencia lo que se distribuya adaptado. El código es **MIT**.

**La excepción son los perfiles de área heredados**, bajo `derecho/kb/`: **su uso comercial
requiere autorización de su autor**. La skill los abre como complemento y avisa cada vez.

<details>
<summary>Las cuatro capas de autoría, en detalle</summary>

<br>

| Capa | Licencia |
| --- | --- |
| Código base de Anthropic (`claude-for-legal`) | Apache 2.0 — `LICENSE` |
| Contribuciones de Cristian Aboitiz — los perfiles de área, escritos, telegramas y transversales | Dual: **no comercial libre, comercial con autorización previa** — `LICENSE-ABOITIZ.md` |
| **Contenido** de este fork — la skill, los módulos, los comandos, los evals, la marca y la documentación | **CC BY-SA 4.0** — [`LICENSE-CC-BY-SA-4.0.md`](LICENSE-CC-BY-SA-4.0.md) |
| **Código** de este fork — los scripts de la skill, los descargadores y las herramientas | **MIT** — `LICENSE-MIT` |
| Textos normativos, jurisprudencia y CCyC Comentado (SAIJ-INFOJUS) | Libre reproducción |

El mapa completo, archivo por archivo, está en **[`LICENCIAS.md`](LICENCIAS.md)**.

</details>

> Basado en contribuciones originales de Cristian Aboitiz
> ([Probanza-ar](https://github.com/Probanza-ar)), publicadas bajo licencia dual. El código base
> proviene de claude-for-legal (Anthropic, Inc.), licenciado bajo Apache 2.0.

---

<details>
<summary><b>Para quien quiera ver cómo está hecho</b></summary>

<br>

<p>
  <a href="https://github.com/ciri-cuervo/derecho-argentino/actions/workflows/tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/ciri-cuervo/derecho-argentino/tests.yml?branch=main&style=flat-square&label=tests" alt="Estado de las suites de tests en main"></a>
  <a href="https://github.com/ciri-cuervo/derecho-argentino/actions/workflows/verificar.yml"><img src="https://img.shields.io/github/actions/workflow/status/ciri-cuervo/derecho-argentino/verificar.yml?branch=main&style=flat-square&label=fuentes%20verificadas" alt="Última verificación semanal de las normas contra los sitios oficiales"></a>
  <a href="derecho/.claude-plugin/plugin.json"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fciri-cuervo%2Fderecho-argentino%2Fmain%2Fderecho%2F.claude-plugin%2Fplugin.json&query=%24.version&label=manifiesto&style=flat-square" alt="Versión que declara el manifiesto del plugin"></a>
  <img src="assets/marca/chapa-python.png" width="135" height="32" alt="Requiere Python 3">
</p>

Cada norma guardada lleva su huella SHA-256, y `verificar_normas.py` la vuelve a comparar contra el
sitio oficial: si cambió, es una reforma. Las calculadoras son scripts de Python sin dependencias,
y salen con error antes que completar un valor que no tienen. El material heredado de
`derecho/kb/` no pasó la auditoría contra fuente primaria que sí pasaron los módulos; ante un
conflicto, manda la fuente primaria, después la skill y sus módulos, y al final los perfiles.

**[Cómo está armado](docs/ARQUITECTURA.md)** · **[Desarrollar el plugin](docs/DESARROLLO.md)** ·
[Auditorías contra fuente primaria](docs/AUDITORIAS.md) · [Qué ramas cubre](docs/COBERTURA.md) ·
[Versiones](CHANGELOG.md) · [Seguridad y reportes](SECURITY.md)

</details>
