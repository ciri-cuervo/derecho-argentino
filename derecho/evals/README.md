# Casos de verificación del sistema

Esta carpeta contiene casos de prueba que permiten verificar que los perfiles
de área del sistema funcionan correctamente. La idea es simple: si un abogado
sabe que un acta de allanamiento tiene una nulidad evidente por falta de
testigos, puede comprobar que el sistema también la detecta. Si no la detecta,
hay un problema en el perfil que hay que corregir.

En el mundo del desarrollo de software esto se llama "eval" (abreviatura de
"evaluation"). En la práctica jurídica es lo mismo que un caso de control:
un expediente o pieza procesal con solución conocida que se usa para verificar
que una herramienta funciona antes de usarla en un caso real.

No es automatización. No corre solo. El abogado pega el caso en el sistema,
lee el análisis que produce y lo compara contra la solución esperada.

---

## Estructura de un caso de verificación

Además de los casos, `PROCEDIMIENTO.md` lleva los puntos que se puntúan en **todos** los
casos: no qué identificó el análisis, sino cómo llegó —si preguntó antes, si abrió el módulo,
si corrió la herramienta en vez de calcular, si pegó su salida sin rearmarla, si los marcadores
están verbatim—. Una rúbrica de contenido no ve esa clase de fallas porque la respuesta sale
bien formada igual.

Cada caso es una carpeta con tres archivos:

```
evals/
  README.md
  administrativo-caba-recursos-agotamiento-via/
    caso.md       # Pieza procesal inventada
    rubrica.md    # Puntos que el sistema debe identificar (binarios: lo detecta o no)
    resultado.md  # Solución esperada: análisis de referencia o criterios mínimos de aprobación
  laboral-prescripcion-suspension-concurrente/
    caso.md       # Pieza procesal inventada
    rubrica.md    # Puntos que el sistema debe identificar (binarios: lo detecta o no)
    resultado.md  # Solución esperada: análisis de referencia o criterios mínimos de aprobación
```

> [!NOTE]
> **Un caso está migrado a `claude plugin eval`.** `laboral-despido-tramos-reforma-pba` tiene,
> además de los tres archivos de abajo, un `prompt.md` y una carpeta `graders/`: es el formato
> que corre el harness de Claude Code sin intervención humana. Los demás casos están solo en
> el formato manual. La migración está parada a propósito, y lo que costó averiguar probándola
> quedó anotado en [`docs/DESARROLLO.md`](../../docs/DESARROLLO.md), sección *Qué queda
> pendiente*.

### caso.md

Pieza procesal **inventada** que se pega en el contexto del sistema. Puede ser
un acta, un escrito, un contrato, una resolución o cualquier documento
relevante para el caso.

**Inventada, no anonimizada.** Este repositorio es público. Anonimizar un
expediente real deja los hechos, y los hechos identifican: una fecha, un
departamento judicial, un monto y una secuencia alcanzan para reconocer una
causa aunque no figure ningún nombre. Un caso de prueba se arma desde cero con
datos verosímiles pero falsos, tomando de la práctica el **problema jurídico**,
nunca el expediente.

Encabezado obligatorio:

```
---
titulo: nombre descriptivo del caso (ej. "Prescripción bienal LCT - suspensiones concurrentes")
area: penal | laboral | civil | familia | administrativo | tributario | societario | concursal | contratos
perfil: nombre del archivo CLAUDE.md que corresponde a este caso
fuero: CPPN | CPPF | CPPCABA | CPPBA | CNAT | Nacional Civil | otro
problema: descripción breve del vicio o vulnerabilidad que contiene el caso
---
```

### rubrica.md

Lista de puntos que el análisis del sistema debe cubrir para considerar
el caso aprobado. Cada punto es binario: el sistema lo identifica o no.

Formato:

```
## Rúbrica · [nombre del caso]

### Obligatorios (el sistema debe identificar todos)
- [ ] Punto 1
- [ ] Punto 2

### Deseables (mejoran el análisis pero no son bloqueantes)
- [ ] Punto 3
- [ ] Punto 4

### Ausentes esperados (el sistema no debe mencionar esto)
- [ ] Punto 5
```

### resultado.md

Solución de referencia. Puede ser:

- El análisis completo generado por el sistema en un momento en que
  funcionaba correctamente, o
- Una descripción de los criterios mínimos que debe cumplir cualquier
  análisis válido.

Si es un análisis de referencia, agregar en el encabezado la fecha y
el modelo usado.

---

## Cómo usar un caso de verificación

1. Abrí una sesión nueva con el perfil correspondiente cargado en el
   Project, en la app de escritorio o en Claude Code.
2. Pegá el contenido de `caso.md` como primer mensaje.
3. Pedile al sistema que analice el documento según su perfil de área.
4. Comparé el análisis contra `rubrica.md`. Marcá los puntos cubiertos.
5. Si todos los obligatorios están cubiertos: caso aprobado.
6. Si falla algún obligatorio: el perfil tiene un problema en esa área
   que hay que reportar o corregir.

---

## Casos prioritarios para contribución

| Área | Caso sugerido | Estado |
|---|---|---|
| Penal | Tenencia de estupefacientes - fuero, Arriola frente a Bazterrica y Montalvo, y consentimiento del allanamiento | Completo |
| Penal | Nulidad de allanamiento por falta de testigos | Pendiente |
| Penal | Nulidad de detención por ausencia de flagrancia | Pendiente |
| Laboral | Prescripción bienal art. 256 LCT - suspensiones concurrentes | Completo |
| Laboral | Despido post-Ley 27.742 - agravantes derogados y base del art. 245 por tramo | Completo |
| Laboral | Telegrama de renuncia con vicio de voluntad | Pendiente |
| Familia | Restitución internacional - grave riesgo por violencia, oposición del niño y regreso seguro | Completo |
| Civil | Accidente de tránsito - factor objetivo, prescripción y citación en garantía | Completo |
| Civil | Caducidad de instancia | Pendiente |
| Contratos | Cláusula abusiva en contrato de adhesión | Pendiente |
| Administrativo | Recursos Dec 1510/97 + plazo art. 7 CCAyT | Completo |
| Administrativo | Caducidad art. 25 LNPA | Pendiente |
| Salud y discapacidad | Cobertura de prepaga por Ley 24.901 y pensión por invalidez de una persona extranjera | Completo |
| Consumidor | Aumento de prepaga bajo DNU 70/23 con afiliado con discapacidad | Completo |
| Consumidor | Daño punitivo - prescripción quinquenal y tope en CBT | Completo |
| Consumidor | Garantía legal vs. comercial, art. 17 y publicidad vinculante | Completo |
| Laboral | SECLO - el plazo que la Ley 24.635 no contiene, y suspensión frente a interrupción | Completo |
| Datos personales | Habeas data contra informe crediticio - el art. 39 alcanza sólo a las operaciones pasivas | Completo |
| Familia | Violencia digital en PBA - por qué vía se pide la supresión de contenidos | Completo |

---

## Cómo aportar un caso

1. Creá una carpeta en `evals/` con el formato `area-descripcion-breve`
   (todo en minúsculas, sin espacios, por ejemplo: `penal-nulidad-allanamiento`).
2. Agregá los tres archivos (`caso.md`, `rubrica.md`, `resultado.md`)
   siguiendo el formato de esta guía.
3. **La pieza se inventa.** No van datos de partes, causas, expedientes,
   montos ni fechas de un caso real, ni siquiera con los nombres cambiados.
4. Lo que el caso debe detectar y por qué importa en la práctica argentina va
   escrito en `rubrica.md`, no sólo en el mensaje del commit.
5. **Pasá el caso por el detector de fuga textual** antes de darlo por hecho:

       python3 herramientas/fuga_textual.py derecho/evals/<tu-caso>/*.md

   Los evals son capa 3 igual que los módulos, así que no puede entrar prosa de
   `kb/`. Y hay una deuda conocida: esta carpeta **quedó fuera del checklist del
   proyecto**, así que los casos anteriores al 14/09/2026 tienen candidatos sin
   revisar. El detalle está en `docs/DESARROLLO.md`, sección *Si escribís
   contenido*. La trampa habitual no es copiar sino condensar: **citá textual al
   tribunal** en vez de resumirlo con palabras propias.
