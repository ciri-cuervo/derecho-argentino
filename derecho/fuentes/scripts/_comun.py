"""Utilidades compartidas por los scripts de derecho/fuentes/."""
from __future__ import annotations

import gzip
import hashlib
import html
import json
import re
from datetime import datetime, timedelta, timezone
import socket
import ssl
import time
import unicodedata
import urllib.error
import urllib.request
import zlib
from html.parser import HTMLParser
from pathlib import Path

UA = "derecho-argentino/fuentes (repositorio de conocimiento juridico)"
RAIZ = Path(__file__).resolve().parents[1]          # derecho/fuentes
NORMAS = RAIZ / "normas"
MANIFIESTO = NORMAS / "normas.json"
PROCEDENCIA = NORMAS / "procedencia.json"
REVISIONES = NORMAS / "revisiones.json"

BLOQUE = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "table", "article", "section"}


class ATexto(HTMLParser):
    """Extractor de texto: descarta script y style, respeta los saltos de bloque."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes, self.saltar = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.saltar += 1
        elif tag in BLOQUE:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.saltar = max(0, self.saltar - 1)
        elif tag in BLOQUE:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self.saltar:
            self.partes.append(data)

    def texto(self) -> str:
        t = html.unescape("".join(self.partes))
        t = t.replace("\xa0", " ")
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        return normalizar_cromo(t.strip())


# --- Cromo del portal con fecha de HOY -----------------------------------------------
#
# El Boletín Oficial y JURISTECA imprimen la fecha del día DENTRO del cuerpo de la página,
# encima del texto de la norma. Eso hace que `sha256_texto` cambie todos los días sin que la
# norma cambie, y `verificar_normas.py` cante CAMBIO -- cambió el texto de la norma sobre
# tres normas, todos los días. Una alarma que suena siempre es una alarma que se deja de
# mirar: por ahí es por donde se pierde un cambio real.
#
# Se saca la fecha, NO con una expresión que busque fechas -- eso se comería las de sanción y
# promulgación, que son parte de la norma y cuya desaparición es justo lo que hay que
# detectar -- sino ANCLADA a los dos rótulos que el portal pone alrededor. Sin esos rótulos
# no se toca nada.
CROMO_CON_FECHA = (
    # Boletín Oficial: "Edición del / <fecha> / Ediciones Anteriores"
    re.compile(r"(?P<antes>Edici[óo]n del\n+)\d{1,2} de \w+ de \d{4}\n+"
               r"(?P<despues>Ediciones Anteriores)", re.I),
    # JURISTECA: "Saltar al contenido / <fecha> / Las fuentes del Derecho a tu alcance"
    re.compile(r"(?P<antes>Saltar al contenido\n+)\d{1,2} \w+ \d{4}\n+"
               r"(?P<despues>Las fuentes del Derecho)", re.I),
)
SIN_FECHA = "[fecha del portal, no es parte de la norma]"


def normalizar_cromo(texto: str) -> str:
    """Saca del cuerpo la fecha de hoy que el portal imprime alrededor de la norma.

    Deja en su lugar un rótulo visible: quien lea el .txt tiene que ver que ahí había algo y
    que se sacó a propósito, no encontrarse dos renglones de maqueta pegados.
    """
    for patron in CROMO_CON_FECHA:
        texto = patron.sub(rf"\g<antes>{SIN_FECHA}\n\n\g<despues>", texto)
    return texto


def contexto_ssl():
    """Contexto TLS. Si certifi está instalado se usa su bundle: varios sitios oficiales
    argentinos sirven cadenas que el almacén del sistema no siempre valida."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class ErrorDeDescarga(Exception):
    """Error de descarga con una pista concreta de por qué falló."""


def _descomprimir(crudo: bytes, encoding: str) -> bytes:
    """Algunos sitios oficiales sirven HTML grande comprimido. Pedirlo así baja mucho el
    tiempo de transferencia en enlaces lentos, que es donde aparecen los timeouts."""
    encoding = (encoding or "").lower()
    try:
        if "gzip" in encoding:
            return gzip.decompress(crudo)
        if "deflate" in encoding:
            return zlib.decompress(crudo, -zlib.MAX_WBITS)
    except (OSError, zlib.error):
        pass
    return crudo


RAYA = "=" * 78

# --- Los dos hashes de una descarga, y para que sirve cada uno -------------------------
#
# REGLA: procedencia.json guarda hash de lo que se GUARDA, y de nada más. De los bytes
# crudos no se conserva ninguno, porque no conservamos los bytes: un hash suyo no se podría
# volver a cotejar contra nada del repositorio. El hash de la descarga cruda va, legible, en
# el encabezado del propio .txt -- "SHA-256 (crudo)" --, que es una declaración de origen
# adentro del artefacto y no un dato que haya que mantener sincronizado.
#
#   sha256_texto    El TEXTO ya extraído, sin la maqueta del portal.
#                   Pregunta: cambio la norma?
#                   Es contra este que compara `verificar_normas.py`, reextrayendo la página.
#                   Comparar bytes no serviría: hay bases -argentina.gob.ar, juristeca- que
#                   reescriben su HTML en cada request con tokens y nonces sin que cambie una
#                   coma, y quedarían en rojo permanente, que es como una alarma se deja de
#                   mirar. Solo en normas, y solo cuando lo guardado es texto: de un PDF se
#                   guarda la descarga entera y ahí el byte a byte es la comparación correcta.
#
#   sha256_archivo  El ARCHIVO que quedó en disco, con su encabezado si lo tiene.
#                   Pregunta: alguien lo toco después de bajarlo?
#                   Es el único cotejable SIN salir a la red, va en los dos corpus con el
#                   mismo nombre, y es el único que cubre el encabezado -- que es justo por
#                   donde derivó una vez, cuando un barrido de ortografía acentuó la
#                   plantilla sin volver a bajar nada. Se controla en cada corrida de tests.
#
# `archivo` es el campo de al lado: `sha256_archivo` se lee "el hash de ese archivo".


def sha256_texto(texto: str) -> str:
    """Hash del texto ya extraído. Ver el contrato de los tres hashes, arriba."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def sha256_archivo(ruta) -> str:
    """Hash del archivo tal como está en disco, leído en BYTES.

    En bytes y no como texto: `read_text()` abre con saltos universales y colapsa `\\r\\n`
    en `\\n`, así que sobre los .txt que vienen con CRLF -los de normas.gba, digesto SCBA y
    JURISTECA- daría el hash de un archivo que no es el que hay. Es el error que hizo
    parecer desalineados a treinta archivos que estaban bien.
    """
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def cuerpo_consolidado(ruta) -> str | None:
    """Devuelve el texto de un .txt de `normas/` sin su encabezado de procedencia.

    `None` cuando no se puede: no está, no se deja leer, o no es texto. Eso último faltaba y
    no es hipotético: en `normas/` conviven cinco entradas que son PDF, y con un PDF esto
    reventaba con `UnicodeDecodeError` en vez de contestar "no puedo". Hoy los llamadores
    filtran por sufijo y por eso no se veía, pero una función que promete `None` tiene que
    devolverlo también cuando el archivo no es UTF-8.

    Y no sirve para VERIFICAR: `read_text()` abre con saltos universales y colapsa `\\r\\n`
    en `\\n`, así que sobre los .txt con CRLF -normas.gba, digesto SCBA, JURISTECA- devuelve
    un cuerpo distinto del que se hasheó. Para contrastar contra `sha256_texto` hay que leer
    en bytes; esto sirve para mirar el texto.
    """
    try:
        s = Path(ruta).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    i = s.find(RAYA)
    j = s.find(RAYA, i + len(RAYA)) if i >= 0 else -1
    if i < 0 or j < 0:
        return None
    return s[j + len(RAYA):].lstrip("\n")


# Un fallo tomado de JUBA llega como página entera: el menú del sitio, los scripts y el pie
# rodean a la sentencia, que vive en un solo <div class="contenido">. Guardar la página entera
# deja más de la mitad del archivo en maqueta, y esa maqueta cambia cuando el portal se
# rediseña, sin que cambie una línea del fallo.
_OCULTO = re.compile(rb"<!--.*?-->|<script\b.*?</script\s*>", re.S | re.I)
_DIV = re.compile(rb"<div\b|</div\s*>", re.I)


def fragmento_div(crudo: bytes, clase: str) -> bytes | None:
    """El `<div class="<clase>">` con su cierre BALANCEADO, o None si no está.

    Devuelve BYTES, tajados del original: el archivo guardado tiene que ser un tramo textual
    de lo que sirvió el portal, sin re-encodear ni tocar los fines de línea.

    Se cuenta la profundidad y no se corta en el primer `</div>`, porque el div de contenido
    trae divs adentro y cortar ahí trunca la sentencia. Y antes de contar se enmascaran los
    comentarios y los <script>: los dos traen tokens `<div` que no abren nada, y con ellos en
    el conteo el cierre cae en el lugar equivocado. Se enmascara con espacios de igual largo
    para que los índices sigan valiendo sobre el original.

    Si no encuentra el div devuelve None, y quien llama guarda la página entera. Guardar
    silenciosamente menos de lo que se bajó sería lo peor: nadie se enteraría de que falta.
    """
    mascara = _OCULTO.sub(lambda m: b" " * len(m.group(0)), crudo)
    patron = rb'<div\b[^>]*class="[^"]*\b' + re.escape(clase.encode()) + rb'\b[^"]*"[^>]*>'
    abre = re.search(patron, mascara, re.I)
    if not abre:
        return None
    profundidad = 1
    for etiqueta in _DIV.finditer(mascara, abre.end()):
        profundidad += 1 if etiqueta.group(0).lower().startswith(b"<div") else -1
        if profundidad == 0:
            return crudo[abre.start():etiqueta.end()]
    return None                     # abre y no cierra: HTML roto, se guarda entero


def bajar(url: str, timeout: int = 180, reintentos: int = 3, verboso: bool = False):
    """Devuelve (bytes_crudos, charset_declarado, content_type).

    Reintenta ante timeout y errores de red transitorios, con espera creciente. No reintenta
    ante un 404 ni ante un error de certificado: eso no se arregla insistiendo.

    Nunca desactiva la verificación TLS: si el certificado no valida, el problema se informa
    con la solución. Bajar una norma sin verificar de donde viene contradice el sentido de
    esta carpeta.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "close",
    })
    ultimo = None
    for intento in range(1, reintentos + 1):
        t0 = time.monotonic()
        try:
            r = urllib.request.urlopen(req, timeout=timeout, context=contexto_ssl())
        except urllib.error.HTTPError as e:
            raise ErrorDeDescarga(f"HTTP {e.code} {e.reason}") from e
        except urllib.error.URLError as e:
            motivo = getattr(e, "reason", e)
            if isinstance(motivo, ssl.SSLCertVerificationError):
                raise ErrorDeDescarga(
                    "la cadena TLS del sitio no validó contra el almacén de certificados. "
                    "Instalar certifi (pip install certifi) y volver a correr; el script lo "
                    "usa automáticamente si está disponible. NO desactivar la verificación."
                ) from e
            ultimo = f"{type(motivo).__name__}: {motivo}"
        except (socket.timeout, TimeoutError):
            ultimo = f"TimeoutError tras {timeout}s"
        except OSError as e:
            ultimo = f"{type(e).__name__}: {e}"
        else:
            with r:
                crudo = r.read()
                ctype = r.headers.get("Content-Type", "")
                cenc = r.headers.get("Content-Encoding", "")
            crudo = _descomprimir(crudo, cenc)
            if verboso:
                print(f"              (intento {intento}: {len(crudo):,} bytes en "
                      f"{time.monotonic() - t0:.1f}s)")
            charset = None
            m = re.search(r"charset=([\w\-]+)", ctype, re.I)
            if m:
                charset = m.group(1)
            if not charset:
                m = re.search(rb'charset=["\']?([\w\-]+)', crudo[:4096], re.I)
                if m:
                    charset = m.group(1).decode("ascii", "ignore")
            return crudo, charset, ctype
        if intento < reintentos:
            espera = 5 * intento
            if verboso:
                print(f"              (intento {intento} fallo: {ultimo}; reintento en "
                      f"{espera}s)")
            time.sleep(espera)
    raise ErrorDeDescarga(f"{ultimo} después de {reintentos} intentos")


def decodificar(crudo: bytes, charset: str | None) -> str:
    for c in [charset, "utf-8", "cp1252", "latin-1"]:
        if not c:
            continue
        try:
            return crudo.decode(c)
        except (UnicodeDecodeError, LookupError):
            continue
    return crudo.decode("latin-1", "replace")


def sha256(crudo: bytes) -> str:
    return hashlib.sha256(crudo).hexdigest()


# Todas las fechas del repositorio se escriben en hora argentina, con offset FIJO y no con la
# zona del sistema. Las dos decisiones tienen motivo:
#
# Argentina, porque una fecha de este repositorio se lee como "el día en que lo hicimos", y con
# UTC un trabajo de las nueve de la noche queda fechado al día siguiente. Pasaba de verdad:
# `descargado` iba en UTC y el `Descargado:` del encabezado en hora local, así que el mismo
# archivo podía decir dos días distintos.
#
# Offset fijo y no `astimezone()`, porque el workflow de CI corre en UTC: la zona del sistema
# haría que la misma corrida feche distinto según dónde se corra, y eso es exactamente lo que una
# fecha que lee una máquina no puede hacer. Argentina no usa horario de verano desde 2009, así
# que -03:00 no necesita base de datos de zonas.
#
# Está escrito en tres lugares -acá, en `herramientas/_veredictos.py` y en la skill- porque los
# tres árboles de scripts no comparten ningún módulo, a propósito. Que no se separen lo sostiene
# `TestUnaSolaZonaHoraria`.
ARGENTINA = timezone(timedelta(hours=-3))


def ahora() -> str:
    """El instante, en hora argentina y con segundos. Para un registro de cuándo se hizo algo."""
    return datetime.now(ARGENTINA).isoformat(timespec="seconds")


def hoy() -> str:
    """La fecha de hoy en hora argentina, ISO."""
    return datetime.now(ARGENTINA).date().isoformat()


def cargar_manifiesto() -> list:
    return json.loads(MANIFIESTO.read_text(encoding="utf-8"))["normas"]


def exigir_slugs_conocidos(pedidos: list[str], catalogo: list[dict]) -> None:
    """Se planta si un `--slug` no está en el manifiesto. No hace nada si no se pasó ninguno.

    Un slug con un dedazo dejaba la lista de descargas vacía, y los descargadores imprimían
    "0 bajadas" y salían con código 0: el pedido no se cumplió y nada lo dijo. Eso es peor que
    un error, porque quien lo corrió cree que ya está. `reocr_jurisprudencia.py` ya se plantaba
    en ese caso; los dos descargadores no, y son los que salen a la red.
    """
    conocidos = {e["slug"] for e in catalogo}
    desconocidos = [s for s in pedidos if s not in conocidos]
    if desconocidos:
        raise SystemExit(f"no están en el manifiesto: {', '.join(desconocidos)}\n"
                         f"  Se corta antes de bajar: un slug mal escrito no baja nada y sin "
                         f"esto salía en silencio.")


def cargar_procedencia() -> dict:
    if PROCEDENCIA.exists():
        return json.loads(PROCEDENCIA.read_text(encoding="utf-8"))
    return {"_descripcion": "Procedencia y hash de cada texto bajado. Lo escribe "
                            "scripts/descargar_normas.py; lo controla verificar_normas.py.",
            "normas": {}}


def plano(s: str) -> str:
    """Minúsculas, sin tildes y con los espacios colapsados: la forma para COMPARAR."""
    sin = unicodedata.normalize("NFD", s)
    sin = "".join(c for c in sin if unicodedata.category(c) != "Mn")
    return " ".join(sin.lower().split())


def cargar_revisiones() -> dict:
    """Veredictos de lectura que apagan una marca de revisar_texto(), por slug.

    Devuelve {slug: {forma plana del problema: veredicto}}. La clave es el problema tal como
    lo redacta revisar_texto(): si esa redacción cambia, o si la norma vuelve con un defecto
    distinto, el veredicto no aplica y la marca vuelve a sonar. Un veredicto vale para lo
    que se leyó, no para el slug.

    SE COMPARA EN FORMA PLANA, y no por el texto exacto. El texto del problema es las dos
    cosas a la vez: la clave de este archivo y un mensaje que el descargador imprime. Como
    mensaje va acentuado, y como clave eso lo volvía frágil: alcanzó con que `revisar_texto()`
    pasara a decir `artículos` para que el veredicto de `ley-24754` --que decía `articulos`--
    dejara de encontrarse. La marca volvió a sonar sin que nadie hubiera tocado la norma, y
    volvió en silencio, que es lo que la hace difícil de ver. Es la misma solución que
    `verificar_respuesta.plano()` usa para el nombre de un marcador, y por el mismo motivo.
    """
    if not REVISIONES.exists():
        return {}
    d = json.loads(REVISIONES.read_text(encoding="utf-8"))
    # Mismo sobre que los otros cuatro archivos de veredicto del repo -- lo documenta
    # `herramientas/_veredictos.py` --, pero cargado acá y no importado de allá: este script
    # viaja dentro del plugin y el plugin tiene que ser autocontenido para poder instalarse.
    # Lo que los mantiene alineados es el test del sobre, que lee los cinco.
    for clave in ("_descripcion", "fijado"):
        if not d.get(clave):
            raise ValueError(f"{REVISIONES.name}: falta `{clave}` en el sobre")
    crudo = d.get("revisiones", {})
    return {slug: {plano(v["problema"]): v["veredicto"] for v in vs}
            for slug, vs in crudo.items()}


def guardar_procedencia(p: dict) -> None:
    PROCEDENCIA.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")


# --- Controles de sanidad de lo descargado ------------------------------------------

MARCAS_DE_FICHA = (
    "Texto completo de la norma",
    "Esta norma modifica o complementa a",
    "Esta norma es complementada o modificada por",
)
# Ley aprobatoria cuyo contenido real vive en un anexo que la página no transcribe.
# Se compara en minúsculas: "Apruebase" y "Apruebase" con tilde escriben distinto.
MARCAS_DE_ANEXO = ("como anexo", "integra la presente", "forma parte de la presente")
MARCAS_DE_APROBATORIA = ("aprueb", "apruéb")
# Cromo de portal: si aparece, lo que bajó es la página del sitio y no el articulado.
MARCAS_DE_PORTAL = (
    "Pasar al contenido principal",
    "Cerrar el buscador",
    "Buscar en el sitio",
    "Ir a Mi Argentina",
)
# Hay leyes legítimamente cortas (la 26.944 tiene 12 artículos): el umbral es bajo a
# propósito y el resto del diagnóstico lo hacen las marcas.
MINIMO_RAZONABLE = 2500       # caracteres


def contar_articulos(texto: str) -> int:
    """Cantidad de artículos DISTINTOS mencionados. Es la señal más confiable de que lo que
    se bajó es un articulado y no una página de sitio: el cromo del portal puede envolver un
    texto perfectamente completo, y el largo total no distingue un código de una ficha.

    Cuenta las dos formas: "artículo 66" y la abreviada "art. 66". Contar solo la primera
    subestimaba los textos de las fuentes que abrevian -- el Código Procesal de Consumo de
    CABA en JURISTECA escribe "Art. 135 -" y parecía tener 18 artículos en vez de 269."""
    numeros = re.findall(r"\bart[ií]culos?\s+(\d+)|\bart\.?\s+(\d+)", texto, re.I)
    return len({a or b for a, b in numeros})


_LETRA = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
# Un carácter del rango de control de CP1252 PEGADO a una letra, de cualquier lado. En
# "m,rito" queda entre dos; en ",estos" queda al principio de la palabra. Hay que mirar los
# dos casos o se escapan la mitad de las ocurrencias.
RE_ACENTO_DEGRADADO = re.compile(
    f"[{_LETRA}][‚ƒ„†‡ˆ‰Š‹]|[‚ƒ„†‡ˆ‰Š‹][{_LETRA}]")
RE_MOJIBAKE = re.compile(r"[ÃÂ][\u0080-\u00bf]")


def revisar_texto(texto: str) -> list:
    """Devuelve la lista de problemas detectados en un texto recién extraído.

    El criterio principal es cuántos artículos distintos aparecen. El cromo del portal y el
    tamaño son señales secundarias: varias normas se sirven envueltas en la maqueta del
    sitio y el articulado está igual, y hay leyes legítimamente cortas.
    """
    problemas = []
    arts = contar_articulos(texto)
    hay_portal = any(m in texto for m in MARCAS_DE_PORTAL)
    hay_ficha = any(m in texto for m in MARCAS_DE_FICHA)

    if arts == 0:
        problemas.append("no se encontró ni un artículo: esto no es un articulado")
    elif arts < 5:
        if hay_portal:
            problemas.append(
                f"solo {arts} artículos y trae el cromo del portal: en argentina.gob.ar hay "
                "que pedir la URL terminada en /texto o /actualizacion")
        elif hay_ficha:
            problemas.append(
                f"solo {arts} artículos y parece la FICHA de InfoLEG: usar la URL de "
                "anexos/<rango>/<id>/texact.htm o norma.htm")
        elif len(texto) < MINIMO_RAZONABLE:
            problemas.append(
                f"solo {arts} artículos en {len(texto)} caracteres: sospechosamente corto")

    bajo = texto.lower()
    if arts and arts < 25 and any(m in bajo for m in MARCAS_DE_ANEXO) and \
            any(m in bajo[:4000] for m in MARCAS_DE_APROBATORIA):
        problemas.append(
            f"parece la ley APROBATORIA y no su contenido: solo {arts} artículos y el texto "
            "remite a un anexo. Buscar una fuente que transcriba el anexo")

    letras = sum(c.isalpha() for c in texto[:20000])
    acentos = sum(c in "áéíóúüñÁÉÍÓÚÜÑ" for c in texto[:20000])
    if letras > 2000 and acentos / letras < 0.002:
        problemas.append("casi no hay acentos: el charset puede estar mal resuelto")
    # Detección de acentuación degradada. El set original incluía "..." -U+2026, puntos
    # suspensivos- y eso hacía fallar el chequeo sobre texto perfectamente sano: una fe de
    # erratas que dice DONDE DICE: ... / DEBE DECIR: ... , o una tabla con puntos de relleno,
    # alcanzaba para marcar la norma. Tres de las cuatro normas que estaban marcadas por
    # codepage eran eso, texto limpio. El indicio no era el dato.
    #
    # Lo que sí delata la corrupción es un carácter del rango de control de CP1252 PEGADO A
    # LETRAS, que es como aparece cuando un byte de CP437 se decodifica mal: m,rito por
    # mérito, c,dula por cédula. Eso no ocurre en texto sano.
    if len(RE_ACENTO_DEGRADADO.findall(texto)) >= 3:
        problemas.append("hay acentuación degradada -caracteres de control entre letras-: la "
                         "fuente sirve el texto mal codificado; cotejar contra el Boletín "
                         "Oficial antes de transcribir")
    # Y el mojibake clásico de UTF-8 leído como latin-1.
    if len(RE_MOJIBAKE.findall(texto)) >= 3:
        problemas.append("hay mojibake de doble codificación -secuencias A-tilde o A-circunflejo-: "
                         "cotejar contra el Boletín Oficial antes de transcribir")
    return problemas
