# 🗂️ Armar el proyecto

Un **proyecto** es una carpeta de trabajo con instrucciones propias: sirve para que el agente
sepa de entrada cómo trabajás, sin que se lo expliques en cada conversación. **No es
obligatorio** —la skill funciona igual sin él— pero si vas a usarla seguido, ahorra una vuelta.

**Cómo se crea.** En la **app de Claude**, "Nuevo proyecto" en la barra lateral: trae sus
propios campos de nombre, descripción e instrucciones. En **Claude Code** desde la terminal,
alcanza con abrir Claude parado en una carpeta y poner las instrucciones en un archivo
`CLAUDE.md` adentro. En **Codex (ChatGPT)**, lo mismo con un archivo `AGENTS.md`. En todos los
casos el contenido es texto común y es lo que sigue.

**Nombre.** Algo que distinga la cartera, no la herramienta. *Estudio · laboral y civil*,
*Juzgado Civil y Comercial 5*, *Consultas de familia*.

**Descripción** (opcional). Una línea sobre qué entra ahí. Sirve para acordarte dentro de seis
meses por qué lo creaste.

**Instrucciones.** Es lo único que cambia de verdad el resultado. **No repitas lo que la skill ya
sabe** —el derecho aplicable, los plazos, las fórmulas—: poné lo que la skill **no puede
adivinar** de vos. Tres cosas alcanzan:

```text
Desde dónde consulto: abogado de parte, habitualmente por el trabajador.
Fueros y jurisdicción: laboral y civil, Provincia de Buenos Aires, Departamento
Judicial de La Plata; ocasionalmente fuero laboral nacional.
Cómo quiero las respuestas: al grano, sin resúmenes de lo que ya dije.
```

**Las dos primeras son las que más rinden**, porque son exactamente lo que la skill pregunta al
abrir cada conversación: desde dónde consultás y en qué fuero. Con eso escrito, deja de
preguntarlo.

> [!NOTE]
> **Si no ponés instrucciones, no se rompe nada: la skill pregunta.** En el primer turno, antes de
> analizar, pide el rol y el fuero, y si hace falta el repositorio. Y si no querés contestar,
> trabaja igual **en modo neutro** y lo dice: expone el derecho aplicable y las posiciones en
> juego, sin construir estrategia para ninguna parte ni controlar de oficio nada.

**Lo que NO conviene poner.** Datos de expedientes reales en las instrucciones del proyecto: van
en la conversación, donde corresponden. Y ninguna instrucción que le pida dar por buenos montos,
plazos o fallos sin verificarlos — es justo lo que la skill está hecha para no hacer.

---

[Volver al README](../README.md) · [Instalar desde la terminal](TERMINAL.md) · [Cómo está armado](ARQUITECTURA.md)
