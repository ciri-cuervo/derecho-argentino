# 🖥️ Instalar desde la terminal

Mismo resultado que por menú, para quien ya vive en la consola. Si preferís instalarlo sin tocar
la terminal, volvé al [README](../README.md#-instalar): ahí están los dos caminos por app de
escritorio, que son los que la mayoría usa.

**Lo único que hay que tener instalado aparte es Python 3.** Los scripts de la skill usan sólo
biblioteca estándar. Para saber si ya lo tenés: `python3 --version` —en Windows,
`python --version`—. Si responde un número, está.

> [!IMPORTANT]
> **La descarga son unos 91 MB** y son casi todo normas y fallos, para que la skill pueda
> trabajar sin conexión. Tarda un rato la primera vez y no hay que volver a hacerlo.

## En Claude Code

**1 · Instalá Claude Code.** En Mac o Linux, `curl -fsSL https://claude.ai/install.sh | bash`; en
Windows PowerShell, `irm https://claude.ai/install.ps1 | iex`. La primera vez pide iniciar
sesión: se abre el navegador y listo.

**2 · Instalá la skill.** Ya dentro de Claude Code, estas dos líneas, una después de la otra:

```sh
/plugin marketplace add ciri-cuervo/derecho-argentino
/plugin install derecho@derecho-argentino
```

> [!NOTE]
> **`/plugin` es un comando de la consola.** En las apps de escritorio no existe: ahí el
> marketplace se agrega por menú.

## En Codex / ChatGPT, a mano

Es el camino verificado para Codex: se clona el repositorio y se copia la carpeta de la skill
donde Codex busca las suyas. Una sola vez, en una terminal.

**macOS y Linux**

```sh
git clone https://github.com/ciri-cuervo/derecho-argentino.git
mkdir -p ~/.agents/skills
cp -R derecho-argentino/derecho/skills/derecho-argentino ~/.agents/skills/
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/ciri-cuervo/derecho-argentino.git
New-Item -ItemType Directory -Force -Path $HOME\.agents\skills
Copy-Item -Recurse derecho-argentino\derecho\skills\derecho-argentino $HOME\.agents\skills\
```

**No borres la carpeta clonada.** Acá se copia la skill sola, y las normas, los fallos y las
series quedan en el clon: si lo borrás, la skill se queda sin los datos con los que trabaja sin
conexión. La primera vez que haga falta va a preguntar dónde quedó el repositorio y lo va a
recordar. Por marketplace esto no pasa, porque la instalación se lleva los datos adentro.

## Comprobar que quedó bien

En Claude Code, dentro de la sesión: `/derecho:estado`. Si instalaste a mano en Codex,
pedíselo en castellano: *"corré el estado de la skill de derecho argentino"*. Qué informa está
en el [README](../README.md), «Comprobar que quedó bien».

---

[Volver al README](../README.md) · [Cómo está armado](ARQUITECTURA.md) ·
[Desarrollar el plugin](DESARROLLO.md)
