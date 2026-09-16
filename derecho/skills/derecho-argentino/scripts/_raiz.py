"""Localiza la raíz del repo de conocimiento jurídico, sin ninguna ruta hardcodeada.

La skill se instala como skill de cuenta y corre en cualquier máquina; el repo puede estar
en cualquier lado y llamarse de cualquier forma. Esta resolución es lo unico que sabe donde
esta, y todos los scripts pasan por acá.

Orden de busqueda, del más explícito al más adivinado:

1. El argumento --repo, si el script lo recibe.
2. La variable de entorno DERECHO_AR_REPO.
3. La variable de entorno que define el agente al instalar el plugin. Cuales son, en
   ENV_PLUGIN: no se enumeran acá para que no queden dos listas que puedan diferir.
4. El archivo de configuración, por defecto ~/.config/derecho-argentino/config.json.
5. Subiendo desde la ubicación de este archivo, por si la skill vive dentro del repo.
6. Un puniado de ubicaciones habituales bajo el home.

En los casos 5 y 6 se exige el marcador: no alcanza con que exista una carpeta con el
nombre parecido, tiene que ser el repo.

Dos disposiciones posibles, porque el marketplace publica el plugin desde derecho/:

    repo clonado        <raiz>/derecho/fuentes/MANIFIESTO.md
    plugin instalado    <raiz>/fuentes/MANIFIESTO.md

En la segunda, la carpeta derecho/ del repo ES la raíz instalada, rodeada de los otros
plugins. Por eso la raíz y la carpeta que contiene fuentes/ y kb/ son dos cosas distintas
-- raiz_repo() devuelve la primera, base() la segunda -- y toda ruta de datos se arma con
base(), nunca concatenando "derecho".

Y las dos disposiciones se parecen mucho: `<plugins>/derecho/fuentes/` y
`<repo>/derecho/fuentes/` tienen la misma forma, porque el marketplace instala la carpeta
con el nombre del plugin y la carpeta del repo se llama igual. Distinguirlas por el nombre
no alcanza, y confundirlas tiene consecuencia: la copia instalada quedaria fijada en el
archivo de configuración, con una ruta que cambia en cada actualización. La discriminación
la hace es_clon(), y es estructural -- sólo el repo trae el manifiesto del marketplace --
porque el nombre lo elige quien empaqueta y la estructura no.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

SUB = "derecho"
MARCADOR_BASE = Path("fuentes") / "MANIFIESTO.md"
MARCADOR = Path(SUB) / MARCADOR_BASE
ENV = "DERECHO_AR_REPO"
# Variables que define el agente cuando la skill llega como plugin instalado. Se prueban
# todas, en orden: la skill corre en cualquier agente que lea el formato SKILL.md y el nombre
# de la variable es lo único que cambia entre uno y otro. Sumar un agente es sumar un nombre.
#
# Las dos primeras las define un agente real. La tercera NO la define ninguno hoy: es una
# apuesta a la convención genérica que insinua el esquema agent-plugins.org, con el que Codex
# valida su plugin.json. Cuesta una línea y no puede dar un falso positivo -si la variable no
# está, el bucle sigue; si está y no apunta al repo, es_repo() la descarta-, pero está escrita
# a futuro y conviene no presentarla como algo que ya funciona en algún lado.
ENV_PLUGIN = ("CLAUDE_PLUGIN_ROOT", "CODEX_PLUGIN_ROOT", "AGENT_PLUGIN_ROOT")
# Ubicaciones habituales bajo el home, todas con el nombre con el que el repo se
# publica. Gana la primera que exista y tenga el marcador; sin marcador no cuenta,
# así que una carpeta que solo se llame parecido no confunde la resolución.
# Un clon con otro nombre no se adivina: para eso están --repo, DERECHO_AR_REPO y
# el archivo de configuración, que van antes que esta lista.
CANDIDATOS = [
    "Documents/derecho-argentino",
    "Downloads/derecho-argentino",
    "claude/derecho-argentino",
    "develop/derecho-argentino",
    "skills/derecho-argentino",
    "derecho-argentino",
]


def archivo_config() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")
    return Path(base) / "derecho-argentino" / "config.json"


def es_base(p: Path) -> bool:
    """True si p es la carpeta que contiene fuentes/ y kb/: derecho/ en el repo."""
    try:
        return (p / MARCADOR_BASE).is_file()
    except OSError:
        return False


MARCADOR_CLON = Path(".claude-plugin") / "marketplace.json"


def es_clon(p: Path) -> bool:
    """True si p es la raíz del repo CLONADO, no la copia que instala el marketplace.

    La marca es ESTRUCTURAL y no un nombre: sólo el repo trae el manifiesto del marketplace. El
    nombre no serviría, porque la copia instalada llega llamada como el plugin y la carpeta del
    repo se llama igual: las dos disposiciones tienen la misma forma.

    Lo que está en juego si se confunden: la copia instalada se toma por clon y se fija en el
    archivo de configuración, con una ruta que cambia en cada actualización.
    """
    try:
        return es_base(p / SUB) and (p / MARCADOR_CLON).is_file()
    except OSError:
        return False


def es_repo(p: Path) -> bool:
    """True para las dos disposiciones: repo clonado y copia instalada del plugin.

    Acá alcanza con el marcador de datos: si alguien apunta `--repo` o la variable de entorno
    a una ruta, se le cree. La discriminación fina es la del descubrimiento automático, que
    hace `es_clon()`.
    """
    return es_base(p / SUB) or es_base(p)


def base(raiz: Path) -> Path:
    """La carpeta con fuentes/ y kb/ dentro de una raíz ya resuelta.

    Es <raiz>/argentina en el repo clonado y la raíz misma en el plugin instalado. Alcanza
    con que exista la subcarpeta: el marcador ya lo exigio quien resolvió la raíz, y pedirlo
    de nuevo acá mandaria a leer la carpeta equivocada -- la raíz -- cuando falta.
    """
    raiz = Path(raiz)
    sub = raiz / SUB
    return sub if sub.is_dir() else raiz


def leer_config() -> dict:
    f = archivo_config()
    if f.is_file():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
    return {}


def guardar_raiz(p: Path) -> Path:
    """Deja la ruta en el archivo de configuración. Devuelve la ruta del archivo."""
    p = Path(p).expanduser().resolve()
    if not es_repo(p):
        raise SystemExit(f"{p} no parece el repo: falta {MARCADOR}")
    f = archivo_config()
    f.parent.mkdir(parents=True, exist_ok=True)
    cfg = leer_config()
    cfg["repo"] = str(p)
    f.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f


_aviso_dado = False


def resolver(explicita=None, fijar=True, avisar=True):
    """raiz_repo() + persistencia automática del primer hallazgo.

    Instalar una skill no ejecuta nada: no hay paso de instalación donde preguntar la ruta.
    Entonces el primer uso que la necesite hace las dos cosas -- la encuentra y la fija --,
    para que no se resuelva por adivinanza cada vez. Solo se persiste lo que se hallo por
    heurística: si vino de --repo, de la variable de entorno o del propio config, no hay nada
    que guardar.
    """
    global _aviso_dado
    p, origen = raiz_repo(explicita)
    if p and fijar and origen.startswith(("ubicación habitual", "la skill vive")):
        try:
            destino = guardar_raiz(p)
            origen += " (queda fijada)"
            if avisar and not _aviso_dado:
                print(f"  Repo encontrado en {p} y anotado en {destino}.")
                print("  Los próximos usos lo toman de ahí. Para cambiarlo: configurar.py "
                      "--repo <ruta>")
                _aviso_dado = True
        except (OSError, SystemExit):
            pass          # sin permiso de escritura se sigue igual, solo no queda fijado
    return p, origen


def raiz_repo(explicita=None):
    """Devuelve (Path, procedencia) o (None, motivo) si no la encuentra."""
    if explicita:
        p = Path(explicita).expanduser()
        return (p.resolve(), "--repo") if es_repo(p) else (None, f"--repo {p} no es el repo")

    env = os.environ.get(ENV)
    if env:
        p = Path(env).expanduser()
        if es_repo(p):
            return p.resolve(), f"variable {ENV}"

    for nombre in ENV_PLUGIN:
        plug = os.environ.get(nombre)
        if not plug:
            continue
        # La variable puede apuntar a la raíz del repo, a derecho/ dentro del repo, o a
        # la copia que instala el marketplace, que es derecho/ renombrada y sin repo
        # arriba. Se busca primero el repo completo -- en la carpeta y en su madre -- para
        # que cuando exista sea el que se reporte; recién después se acepta la copia.
        dir_plug = Path(plug).expanduser()
        for p in (dir_plug, dir_plug.parent):
            if es_base(p / SUB):
                return p.resolve(), f"variable {nombre} (plugin instalado)"
        for p in (dir_plug, dir_plug.parent):
            if es_base(p):
                return p.resolve(), f"variable {nombre} (plugin instalado)"

    cfg = leer_config().get("repo")
    if cfg:
        p = Path(cfg).expanduser()
        if es_repo(p):
            return p.resolve(), f"config {archivo_config()}"

    aqui = Path(__file__).resolve()
    for padre in aqui.parents:
        if es_clon(padre):
            return padre, "la skill vive dentro del repo"
    for padre in aqui.parents:
        if es_base(padre):
            # Instalada por el marketplace: los datos viajan al lado de la skill. No se
            # fija en el archivo de configuración, porque esta ruta cambia al actualizar.
            return padre, "el plugin instalado trae los datos"

    for c in CANDIDATOS:
        p = Path.home() / c
        if es_repo(p):
            return p.resolve(), f"ubicación habitual ~/{c}"

    return None, "no encontrado"


AYUDA = f"""No encuentro el repo de conocimiento juridico.

Los datos que este script necesita -- valor del jus, calendario de inhabiles, series de
indices -- viven ahi, y sin ellos no se puede calcular: estimarlos seria inventar montos,
que es justo lo que la seccion 2 de la skill prohibe.

Para dejarlo configurado una sola vez en esta maquina:

    python3 {Path(__file__).parent / 'configurar.py'} --repo /ruta/al/repo

Alternativas, si preferis no escribir configuracion:

    export {ENV}=/ruta/al/repo          # en el perfil del shell
    <script> --repo /ruta/al/repo       # por unica vez

El repo se reconoce porque contiene {MARCADOR}."""


def exigir_raiz(explicita=None, silencioso=False):
    """Como raiz_repo, pero corta el programa con un mensaje útil si no la encuentra."""
    p, origen = raiz_repo(explicita)
    if p is None:
        if silencioso:
            return None
        print(AYUDA)
        raise SystemExit(2)
    return p


def datos(explicita=None):
    """Carpeta de datos del repo, o None si no hay repo configurado.

    Es la puerta que usan las calculadoras. Pasa por resolver(), así que el primer uso que
    encuentre el repo por heurística lo deja fijado.
    """
    p, _ = resolver(explicita)
    return None if p is None else base(p) / "fuentes" / "datos"
