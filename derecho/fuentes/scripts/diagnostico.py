#!/usr/bin/env python3
"""Prueba la conectividad con los sitios oficiales y mide cuánto tardan.

Para cuando una descarga falla y no se sabe si el problema es el sitio, la red local o el
certificado. No guarda nada: solo mide y reporta.

    python3 diagnostico.py
    python3 diagnostico.py --timeout 300
    python3 diagnostico.py --url https://servicios.infoleg.gob.ar/...

Va capa por capa —DNS, TCP:443, TLS y GET— porque el renglón donde se corta es el que dice
dónde está el problema. Sale con código 1 si alguno no completó el GET, así que sirve para
colgarlo de algo; antes salía 0 incluso informando que fallaban todos.
"""
from __future__ import annotations

import argparse
import socket
import ssl
import sys
import time
import urllib.request
from urllib.parse import urlparse

from _comun import UA, contexto_ssl

# Cada URL de acá tiene que estar en `normas.json` -lo exige un test-, y eso deja afuera a SAIJ y a
# los registros judiciales: de ellos el repo no baja nada, así que una sonda suya no mediría si las
# descargas funcionan. Para esos, `diagnostico.py --url <url>` mide sin tocar la lista.
SITIOS = [
    ("InfoLEG", "https://servicios.infoleg.gob.ar/infolegInternet/anexos/25000-29999/25552/texact.htm"),
    ("argentina.gob.ar", "https://www.argentina.gob.ar/normativa/nacional/ley-19549-22363/actualizacion"),
    ("normas.gba.gob.ar (Ley 14.997)", "https://normas.gba.gob.ar/documentos/VRN88f5V.html"),
    ("normas.gba.gob.ar (CPCCBA)", "https://normas.gba.gob.ar/documentos/VrQlgSOB.html"),
    ("SCBA", "https://www.scba.gov.ar/includes/descarga.asp?id=54872&n=Ver+Resolucion+SC1840.pdf"),
    ("API series de tiempo", "https://apis.datos.gob.ar/series/api/series/?ids=145.3_INGNACNAL_DICI_M_15&format=csv&limit=1"),
]


def probar(nombre: str, url: str, timeout: int) -> bool:
    """Prueba un sitio capa por capa. True si el GET completó.

    Devuelve el resultado en vez de sólo imprimirlo para que `main()` pueda salir con código
    distinto de cero: un diagnóstico que informa seis fallas y termina en 0 no se puede colgar de
    nada, y quien lo lea de una tarea programada lo va a leer como que todo anda.
    """
    host = urlparse(url).hostname
    print(f"\n  {nombre}")
    print(f"    {url[:100]}")
    t0 = time.monotonic()
    try:
        # getaddrinfo y no gethostbyname: el segundo resuelve sólo IPv4 y reportaría "DNS FALLA"
        # sobre un host que publica nada más que AAAA, que es un diagnóstico falso justo en el
        # renglón donde alguien va a empezar a buscar el problema.
        familias = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
        direcciones = sorted({info[4][0] for info in familias})
        print(f"    DNS      {host} -> {', '.join(direcciones)}  "
              f"({time.monotonic() - t0:.2f}s)")
    except OSError as e:
        print(f"    DNS      FALLA: {e}")
        return False
    t0 = time.monotonic()
    try:
        with socket.create_connection((host, 443), timeout=timeout) as s:
            print(f"    TCP:443  abierto  ({time.monotonic() - t0:.2f}s)")
            t0 = time.monotonic()
            with contexto_ssl().wrap_socket(s, server_hostname=host) as ss:
                cert = ss.getpeercert()
                emisor = dict(x[0] for x in cert.get("issuer", ())).get("organizationName", "?")
                print(f"    TLS      ok, emisor: {emisor}  ({time.monotonic() - t0:.2f}s)")
    except ssl.SSLCertVerificationError as e:
        print(f"    TLS      FALLA DE CERTIFICADO: {e}")
        print("             -> pip install certifi y volver a correr")
        return False
    except (socket.timeout, TimeoutError):
        print(f"    TCP:443  TIMEOUT tras {timeout}s")
        return False
    except OSError as e:
        print(f"    TCP:443  FALLA: {e}")
        return False
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Encoding": "gzip, deflate"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=contexto_ssl()) as r:
            cuerpo = r.read()
            # El código se LEE de la respuesta. Estaba escrito "HTTP 200" a mano, y un 204 o un
            # 203 salían informados como 200: la única línea del script que afirma algo sin
            # medirlo, en la herramienta que existe para medir.
            codigo = r.status
        seg = time.monotonic() - t0
        vel = len(cuerpo) / seg / 1024 if seg else 0
        print(f"    GET      HTTP {codigo}, {len(cuerpo):,} bytes en {seg:.1f}s  "
              f"({vel:,.0f} KB/s)")
        if seg > 60:
            print("             -> lento: correr el descargador con --timeout 300")
        return True
    except (socket.timeout, TimeoutError):
        print(f"    GET      TIMEOUT tras {timeout}s (la conexión abre pero no completa)")
        # `--reintentos` es del descargador, no de acá: la sugerencia lo nombraba suelto y quien
        # la copiara sobre este script se comía un error de argparse.
        print("             -> el sitio responde pero transfiere muy lento, o corta la "
              "conexión.\n                Probar con --timeout 300, correr el descargador con "
              "--timeout 300 --reintentos 5,\n                o desde otra red")
    except Exception as e:
        print(f"    GET      FALLA: {type(e).__name__}: {e}")
    return False


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--url", action="append", default=[], help="Probar solo esta URL")
    a = p.parse_args()
    print("DIAGNÓSTICO DE CONECTIVIDAD CON LAS FUENTES OFICIALES")
    sitios = [("URL indicada", u) for u in a.url] or SITIOS
    fallaron = [nombre for nombre, url in sitios if not probar(nombre, url, a.timeout)]
    print("\n  Lectura: si DNS, TCP y TLS pasan y solo falla el GET, el sitio está vivo pero\n"
          "  lento o cortando la transferencia. Si falla TLS, es certifi. Si falla TCP, es\n"
          "  red o firewall.")
    if fallaron:
        print(f"\n  {len(fallaron)} de {len(sitios)} no completaron: {', '.join(fallaron)}")
    # Sale con 1 si alguno falló. Antes salía 0 siempre, incluso informando seis fallas: un
    # diagnóstico que no se puede colgar de nada, y que desde una tarea programada se lee como
    # que todo anda.
    return 1 if fallaron else 0


if __name__ == "__main__":
    sys.exit(main())
