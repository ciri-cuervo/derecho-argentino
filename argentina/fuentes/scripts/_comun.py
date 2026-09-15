"""Utilidades compartidas por los scripts de argentina/fuentes/."""
from __future__ import annotations

import gzip
import hashlib
import html
import json
import re
import socket
import ssl
import time
import urllib.error
import urllib.request
import zlib
from html.parser import HTMLParser
from pathlib import Path

UA = "derecho-argentino/fuentes (repositorio de conocimiento juridico)"
RAIZ = Path(__file__).resolve().parents[1]          # argentina/fuentes
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
# El Boletín Oficial y JURISTECA imprimen la fecha del dia DENTRO del cuerpo de la página,
# encima del texto de la norma. Eso hace que `sha256_texto` cambie todos los días sin que la
# norma cambie, y `verificar_normas.py` cante CAMBIO -- cambió el texto de la norma sobre
# tres normas, todos los días. Una alarma que suena siempre es una alarma que se deja de
# mirar: por ahí es por donde se pierde un cambio real.
#
# Se saca la fecha, NO con una expresión que busque fechas -- eso se comeria las de sanción y
# promulgacion, que son parte de la norma y cuya desaparicion es justo lo que hay que
# detectar -- sino ANCLADA a los dos rotulos que el portal pone alrededor. Sin esos rotulos
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

    Deja en su lugar un rotulo visible: quien lea el .txt tiene que ver que ahí habia algo y
    que se saco a proposito, no encontrarse dos renglones de maqueta pegados.
    """
    for patron in CROMO_CON_FECHA:
        texto = patron.sub(rf"\g<antes>{SIN_FECHA}\n\n\g<despues>", texto)
    return texto


def _contexto_ssl():
    """Contexto TLS. Si certifi esta instalado se usa su bundle: varios sitios oficiales
    argentinos sirven cadenas que el almacen del sistema no siempre valida."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class ErrorDeDescarga(Exception):
    """Error de descarga con una pista concreta de por que fallo."""


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


def sha256_texto(texto: str) -> str:
    """Hash del cuerpo consolidado, no de los bytes crudos.

    Existe porque algunas bases -argentina.gob.ar y juristeca, hoy- devuelven un HTML que
    cambia en cada request sin que cambie la norma: tokens, nonces, hashes de assets. El hash
    crudo de esas paginas nunca coincide dos veces, con lo que `verificar_normas.py` las
    marcaria como modificadas siempre y la alarma quedaria en rojo permanente. El cuerpo ya
    extraido si es estable, y es lo unico que importa juridicamente.
    """
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def cuerpo_consolidado(ruta) -> str | None:
    """Devuelve el texto de un .txt de `normas/` sin su encabezado de procedencia."""
    try:
        s = Path(ruta).read_text(encoding="utf-8")
    except OSError:
        return None
    i = s.find(RAYA)
    j = s.find(RAYA, i + len(RAYA)) if i >= 0 else -1
    if i < 0 or j < 0:
        return None
    return s[j + len(RAYA):].lstrip("\n")


def bajar(url: str, timeout: int = 180, reintentos: int = 3, verboso: bool = False):
    """Devuelve (bytes_crudos, charset_declarado, content_type).

    Reintenta ante timeout y errores de red transitorios, con espera creciente. No reintenta
    ante un 404 ni ante un error de certificado: eso no se arregla insistiendo.

    Nunca desactiva la verificacion TLS: si el certificado no valida, el problema se informa
    con la solucion. Bajar una norma sin verificar de donde viene contradice el sentido de
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
            r = urllib.request.urlopen(req, timeout=timeout, context=_contexto_ssl())
        except urllib.error.HTTPError as e:
            raise ErrorDeDescarga(f"HTTP {e.code} {e.reason}") from e
        except urllib.error.URLError as e:
            motivo = getattr(e, "reason", e)
            if isinstance(motivo, ssl.SSLCertVerificationError):
                raise ErrorDeDescarga(
                    "la cadena TLS del sitio no valido contra el almacen de certificados. "
                    "Instalar certifi (pip install certifi) y volver a correr; el script lo "
                    "usa automaticamente si esta disponible. NO desactivar la verificacion."
                ) from e
            ultimo = f"{type(motivo).__name__}: {motivo}"
        except (socket.timeout, TimeoutError) as e:
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
    raise ErrorDeDescarga(f"{ultimo} despues de {reintentos} intentos")


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


def cargar_manifiesto() -> list:
    return json.loads(MANIFIESTO.read_text(encoding="utf-8"))["normas"]


def cargar_procedencia() -> dict:
    if PROCEDENCIA.exists():
        return json.loads(PROCEDENCIA.read_text(encoding="utf-8"))
    return {"_descripcion": "Procedencia y hash de cada texto bajado. Lo escribe "
                            "scripts/descargar_normas.py; lo controla verificar_normas.py.",
            "normas": {}}


def cargar_revisiones() -> dict:
    """Veredictos de lectura que apagan una marca de revisar_texto(), por slug.

    Devuelve {slug: {texto exacto del problema: veredicto}}. La clave es el problema tal
    como lo redacta revisar_texto(): si esa redaccion cambia, o si la norma vuelve con un
    defecto distinto, el veredicto no aplica y la marca vuelve a sonar. Un veredicto vale
    para lo que se leyo, no para el slug.
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
    return {slug: {v["problema"]: v["veredicto"] for v in vs} for slug, vs in crudo.items()}


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
# Cromo de portal: si aparece, lo que bajo es la página del sitio y no el articulado.
MARCAS_DE_PORTAL = (
    "Pasar al contenido principal",
    "Cerrar el buscador",
    "Buscar en el sitio",
    "Ir a Mi Argentina",
)
# Hay leyes legitimamente cortas (la 26.944 tiene 12 artículos): el umbral es bajo a
# propósito y el resto del diagnóstico lo hacen las marcas.
MINIMO_RAZONABLE = 2500       # caracteres


def contar_articulos(texto: str) -> int:
    """Cantidad de articulos DISTINTOS mencionados. Es la senal más confiable de que lo que
    se bajo es un articulado y no una pagina de sitio: el cromo del portal puede envolver un
    texto perfectamente completo, y el largo total no distingue un codigo de una ficha.

    Cuenta las dos formas: "articulo 66" y la abreviada "art. 66". Contar solo la primera
    subestimaba los textos de las fuentes que abrevian -- el Codigo Procesal de Consumo de
    CABA en JURISTECA escribe "Art. 135 -" y parecia tener 18 articulos en vez de 269."""
    numeros = re.findall(r"\bart[ií]culos?\s+(\d+)|\bart\.?\s+(\d+)", texto, re.I)
    return len({a or b for a, b in numeros})


_LETRA = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
# Un caracter del rango de control de CP1252 PEGADO a una letra, de cualquier lado. En
# "m,rito" queda entre dos; en ",estos" queda al principio de la palabra. Hay que mirar los
# dos casos o se escapan la mitad de las ocurrencias.
RE_ACENTO_DEGRADADO = re.compile(
    f"[{_LETRA}][‚ƒ„†‡ˆ‰Š‹]|[‚ƒ„†‡ˆ‰Š‹][{_LETRA}]")
RE_MOJIBAKE = re.compile(r"[ÃÂ][\u0080-\u00bf]")


def revisar_texto(texto: str) -> list:
    """Devuelve la lista de problemas detectados en un texto recien extraido.

    El criterio principal es cuantos articulos distintos aparecen. El cromo del portal y el
    tamanio son senales secundarias: varias normas se sirven envueltas en la maqueta del
    sitio y el articulado esta igual, y hay leyes legitimamente cortas.
    """
    problemas = []
    arts = contar_articulos(texto)
    hay_portal = any(m in texto for m in MARCAS_DE_PORTAL)
    hay_ficha = any(m in texto for m in MARCAS_DE_FICHA)

    if arts == 0:
        problemas.append("no se encontro ni un articulo: esto no es un articulado")
    elif arts < 5:
        if hay_portal:
            problemas.append(
                f"solo {arts} articulos y trae el cromo del portal: en argentina.gob.ar hay "
                "que pedir la URL terminada en /texto o /actualizacion")
        elif hay_ficha:
            problemas.append(
                f"solo {arts} articulos y parece la FICHA de InfoLEG: usar la URL de "
                "anexos/<rango>/<id>/texact.htm o norma.htm")
        elif len(texto) < MINIMO_RAZONABLE:
            problemas.append(
                f"solo {arts} articulos en {len(texto)} caracteres: sospechosamente corto")

    bajo = texto.lower()
    if arts and arts < 25 and any(m in bajo for m in MARCAS_DE_ANEXO) and \
            any(m in bajo[:4000] for m in MARCAS_DE_APROBATORIA):
        problemas.append(
            f"parece la ley APROBATORIA y no su contenido: solo {arts} articulos y el texto "
            "remite a un anexo. Buscar una fuente que transcriba el anexo")

    letras = sum(c.isalpha() for c in texto[:20000])
    acentos = sum(c in "áéíóúüñÁÉÍÓÚÜÑ" for c in texto[:20000])
    if letras > 2000 and acentos / letras < 0.002:
        problemas.append("casi no hay acentos: el charset puede estar mal resuelto")
    # Deteccion de acentuación degradada. El set original incluia "..." -U+2026, puntos
    # suspensivos- y eso hacía fallar el chequeo sobre texto perfectamente sano: una fe de
    # erratas que dice DONDE DICE: ... / DEBE DECIR: ... , o una tabla con puntos de relleno,
    # alcanzaba para marcar la norma. Tres de las cuatro normas que estaban marcadas por
    # codepage eran eso, texto limpio. El indicio no era el dato.
    #
    # Lo que si delata la corrupcion es un caracter del rango de control de CP1252 PEGADO A
    # LETRAS, que es como aparece cuando un byte de CP437 se decodifica mal: m,rito por
    # mérito, c,dula por cédula. Eso no ocurre en texto sano.
    if len(RE_ACENTO_DEGRADADO.findall(texto)) >= 3:
        problemas.append("hay acentuacion degradada -caracteres de control entre letras-: la "
                         "fuente sirve el texto mal codificado; cotejar contra el Boletin "
                         "Oficial antes de transcribir")
    # Y el mojibake clasico de UTF-8 leido como latin-1.
    if len(RE_MOJIBAKE.findall(texto)) >= 3:
        problemas.append("hay mojibake de doble codificacion -secuencias A-tilde o A-circunflejo-: "
                         "cotejar contra el Boletin Oficial antes de transcribir")
    return problemas
