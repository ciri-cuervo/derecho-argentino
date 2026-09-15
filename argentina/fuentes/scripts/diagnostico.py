#!/usr/bin/env python3
"""Prueba la conectividad con los sitios oficiales y mide cuanto tardan.

Para cuando una descarga falla y no se sabe si el problema es el sitio, la red local o el
certificado. No guarda nada: solo mide y reporta.

    python3 diagnostico.py
    python3 diagnostico.py --timeout 300
"""
from __future__ import annotations

import argparse
import socket
import ssl
import time
import urllib.request
from urllib.parse import urlparse

from _comun import UA, _contexto_ssl

SITIOS = [
    ("InfoLEG", "https://servicios.infoleg.gob.ar/infolegInternet/anexos/25000-29999/25552/texact.htm"),
    ("argentina.gob.ar", "https://www.argentina.gob.ar/normativa/nacional/ley-19549-22363/actualizacion"),
    ("normas.gba.gob.ar (Ley 11.653)", "https://normas.gba.gob.ar/documentos/BE3q5SQ0.html"),
    ("normas.gba.gob.ar (CPCCBA)", "https://normas.gba.gob.ar/documentos/VrQlgSOB.html"),
    ("SCBA", "https://www.scba.gov.ar/includes/descarga.asp?id=54872&n=Ver+Resolucion+SC1840.pdf"),
    ("API series de tiempo", "https://apis.datos.gob.ar/series/api/series/?ids=145.3_INGNACNAL_DICI_M_15&format=csv&limit=1"),
]


def probar(nombre: str, url: str, timeout: int):
    host = urlparse(url).hostname
    print(f"\n  {nombre}")
    print(f"    {url[:100]}")
    t0 = time.monotonic()
    try:
        ip = socket.gethostbyname(host)
        print(f"    DNS      {host} -> {ip}  ({time.monotonic() - t0:.2f}s)")
    except OSError as e:
        print(f"    DNS      FALLA: {e}")
        return
    t0 = time.monotonic()
    try:
        with socket.create_connection((host, 443), timeout=timeout) as s:
            print(f"    TCP:443  abierto  ({time.monotonic() - t0:.2f}s)")
            t0 = time.monotonic()
            with _contexto_ssl().wrap_socket(s, server_hostname=host) as ss:
                cert = ss.getpeercert()
                emisor = dict(x[0] for x in cert.get("issuer", ())).get("organizationName", "?")
                print(f"    TLS      ok, emisor: {emisor}  ({time.monotonic() - t0:.2f}s)")
    except ssl.SSLCertVerificationError as e:
        print(f"    TLS      FALLA DE CERTIFICADO: {e}")
        print("             -> pip install certifi y volver a correr")
        return
    except (socket.timeout, TimeoutError):
        print(f"    TCP:443  TIMEOUT tras {timeout}s")
        return
    except OSError as e:
        print(f"    TCP:443  FALLA: {e}")
        return
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Encoding": "gzip, deflate"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_contexto_ssl()) as r:
            cuerpo = r.read()
        seg = time.monotonic() - t0
        vel = len(cuerpo) / seg / 1024 if seg else 0
        print(f"    GET      HTTP 200, {len(cuerpo):,} bytes en {seg:.1f}s  ({vel:,.0f} KB/s)")
        if seg > 60:
            print("             -> lento: correr el descargador con --timeout 300")
    except (socket.timeout, TimeoutError):
        print(f"    GET      TIMEOUT tras {timeout}s (la conexion abre pero no completa)")
        print("             -> el sitio responde pero transfiere muy lento, o corta la "
              "conexion.\n                Probar --timeout 300 --reintentos 5, o desde otra red")
    except Exception as e:
        print(f"    GET      FALLA: {type(e).__name__}: {e}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--url", action="append", default=[], help="Probar solo esta URL")
    a = p.parse_args()
    print("DIAGNOSTICO DE CONECTIVIDAD CON LAS FUENTES OFICIALES")
    sitios = [("URL indicada", u) for u in a.url] or SITIOS
    for nombre, url in sitios:
        probar(nombre, url, a.timeout)
    print("\n  Lectura: si DNS, TCP y TLS pasan y solo falla el GET, el sitio esta vivo pero\n"
          "  lento o cortando la transferencia. Si falla TLS, es certifi. Si falla TCP, es\n"
          "  red o firewall.")


if __name__ == "__main__":
    main()
