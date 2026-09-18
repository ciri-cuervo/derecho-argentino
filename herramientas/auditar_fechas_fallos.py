#!/usr/bin/env python3
"""Audita cada fallo bajado contra su propio texto: identidad primero, fecha después.

Dos controles.

EL PRIMERO ES LA IDENTIDAD, y aplica sobre todo a la CSJN. Ahí el documento se pide por un
identificador interno que no se deriva de la cita de Fallos y hay que curar a mano, así que un
id mal curado baja OTRO fallo: buscando "Acosta" -Fallos 331:858- aparece indexado un id que
devuelve "Llerena, Horacio Luis s/ abuso de armas". El descargador ya lo controla cuando lo
bajado es HTML, pero la CSJN devuelve PDF y ahí no puede: por eso el control vive también acá,
donde ya se extrae el texto con pdftotext.

EL SEGUNDO ES LA FECHA, y aplica a la SCBA: las fechas de los fallos bonaerenses circulan mal. Las fuentes secundarias
publican la fecha de la PRIMERA firma, la del juez que voto primero, y entre esa y la del
actuario pueden pasar semanas. Por el art. 4 del Ac. SCBA 3971/20 la rúbrica del acto se
perfecciona cuando la suscribe el secretario o subsecretario: esa es la fecha del fallo, y
los PDF la traen al pie en las constancias de firma digital. O sea que se puede comprobar
contra el documento en vez de contra un portal.

La primera corrida, el 13/09/2026, encontró cuatro fechas mal en el manifiesto, una de ellas
con dos meses de diferencia.

Uso, desde la raíz del repositorio:

    python3 herramientas/auditar_fechas_fallos.py

Requiere `pdftotext` (poppler-utils). Los fallos escaneados o guardados como HTML no traen
constancias y salen como ??? : esos hay que mirarlos a mano.

No se instala con el plugin: vive fuera de `derecho/`.
"""
import json, re, subprocess, pathlib, sys, unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _externos

J = pathlib.Path("derecho/fuentes/jurisprudencia")
SECRE = re.compile(r"SECRETARI|ACTUARI|SUBSECRETARI", re.I)


def clave(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t)


def cabeza_de(caratula: str) -> str:
    """Lo que identifica al fallo: lo que va antes de la coma, del c/ o del s/."""
    return re.split(r"[,.]| c/ | vs\. | contra | s/", caratula or "")[0].strip()


def texto_de(ruta: pathlib.Path) -> str | None:
    """Texto plano del documento, sea PDF o HTML.

    No todo lo que se baja es PDF: un fallo tomado de JUBA viene en HTML, y pasarle pdftotext
    devuelve vacío, que se confunde con un PDF escaneado. Son dos problemas distintos y el
    auditor tiene que poder distinguirlos.
    """
    crudo = ruta.read_bytes()
    if crudo[:5] == b"%PDF-":
        try:
            return subprocess.run(["pdftotext", "-q", str(ruta), "-"],
                                  capture_output=True, text=True, timeout=60).stdout
        except FileNotFoundError:
            # Falta el binario: es un problema de la máquina, no del documento. Meterlo en
            # el mismo sacó que un PDF roto hace que el resumen diga "0 A REVISAR" con el
            # auditor apagado. `main()` lo exige antes de empezar; esto es el cinturón.
            raise SystemExit(_externos.instruccion("pdftotext"))
        except Exception:
            return None
    texto = crudo.decode("utf-8", errors="replace")
    texto = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", texto)
    return re.sub(r"<[^>]+>", " ", texto)


MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
         "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11,
         "diciembre": 12}


def fecha_impresa(txt: str) -> str | None:
    """La fecha impresa en el cuerpo, para los tomos que no tienen firma digital.

    Los fallos de los 80 no traen constancias de firma: la fecha está impresa en el tomo,
    en la línea siguiente al título "FALLO DE LA CORTE SUPREMA". Se busca ahí y no en la
    primera "Buenos Aires" del documento, que suele ser la del dictamen del Procurador y
    lleva otra fecha: en "Fiorentino" el dictamen es del 21/05/1984 y el fallo del 27/11/1984.
    """
    titulo = re.search(r"FALLO\s+DE\s+LA\s+CORTE\s+SUPREMA", txt, re.I)
    if not titulo:
        return None
    hallado = re.search(r"Buenos\s+Aires,?\s*(\d{1,2})\s+de\s+([A-Za-zÁ-ÿ]+)\s+de\s+(\d{4})",
                        txt[titulo.end():titulo.end() + 400], re.I)
    if not hallado:
        return None
    dia, mes, anio = hallado.groups()
    numero = MESES.get(clave(mes).strip())
    if not numero:
        return None
    return f"{anio}-{numero:02d}-{int(dia):02d}"


def auditar(f: dict, proc: dict) -> str:
    archivo = proc.get(f["slug"], {}).get("archivo", f"{f['slug']}.pdf")
    ruta = J / archivo
    if not ruta.exists():
        return f"  ---       {f['slug']}: sin archivo bajado"

    # Si hay texto recuperado por OCR, se audita contra eso: para los seis documentos cuya capa
    # de texto vino arruinada, pdftotext devuelve basura y el control no podía ni empezar.
    recuperado = J / "ocr" / f"{f['slug']}.txt"
    desde_ocr = recuperado.exists()
    if desde_ocr:
        txt = recuperado.read_text(encoding="utf-8", errors="replace")
    else:
        txt = texto_de(ruta)
    if txt is None:
        return f"  ---       {f['slug']}: no se pudo extraer el texto"
    if not txt.strip():
        return f"  ???       {f['slug']}: sin texto extraible (PDF escaneado)"
    marca = " [ocr]" if desde_ocr else ""

    # 1 - IDENTIDAD. Es el control que importa y va primero: si el documento no es el
    # declarado, la fecha que traiga es irrelevante.
    cabeza = cabeza_de(f.get("caratula", ""))
    if len(cabeza) >= 4 and clave(cabeza) not in clave(txt):
        return (f"  IDENTIDAD {f['slug']}: el documento no menciona \"{cabeza}\" - puede ser "
                f"OTRO fallo, revisar el identificador antes de citarlo")

    # 2 - FECHA, contra la constancia de firma del actuario.
    crudo = re.sub(r"\s+", " ", txt)
    firmas = re.findall(r"Funcionario Firmante:\s*(\d{2}/\d{2}/\d{4})[^F]{0,120}", crudo)
    cargos = re.findall(r"Funcionario Firmante:\s*(\d{2}/\d{2}/\d{4})\s*[\d:]*\s*-\s*([^F]{0,90})", crudo)
    if not firmas:
        impresa = fecha_impresa(txt)
        if impresa is None:
            return (f"  id ok     {f['slug']}{marca}: identidad confirmada; sin constancias de "
                    f"firma para la fecha")
        if impresa == f.get("fecha"):
            return (f"  OK        {f['slug']}{marca}: identidad y fecha confirmadas ({impresa})"
                    f"  (fecha impresa en el tomo)")
        return (f"  DIFIERE   {f['slug']}{marca}: manifiesto {f.get('fecha')} | "
                f"impresa en el tomo {impresa}")
    act = [d for d, c in cargos if SECRE.search(c)]
    dd, mm, yy = (act[-1] if act else firmas[-1]).split("/")
    iso = f"{yy}-{mm}-{dd}"
    nota = "" if act else "  (sin cargo de actuario: se usa la última firma)"
    if iso == f.get("fecha"):
        return f"  OK        {f['slug']}{marca}: identidad y fecha confirmadas ({iso}){nota}"
    return f"  DIFIERE   {f['slug']}{marca}: manifiesto {f.get('fecha')} | actuario {iso}{nota}"


def main() -> int:
    if not J.is_dir():
        print(f"no encuentro {J}: corré el script desde la raíz del repo", file=sys.stderr)
        return 2
    _externos.exigir("pdftotext")
    m = json.loads((J / "fallos.json").read_text(encoding="utf-8"))
    proc = json.loads((J / "procedencia.json").read_text(encoding="utf-8"))["fallos"]
    lineas = [auditar(f, proc) for f in m["fallos"]]
    for l in lineas:
        print(l)
    graves = [l for l in lineas if "IDENTIDAD" in l or "DIFIERE" in l]
    # La identidad es el control que importa: se cuenta aparte de la fecha, porque un fallo
    # con identidad confirmada y sin constancias de firma NO es un fallo dudoso.
    # Una fecha que DIFIERE no pone en duda la identidad: el documento es el declarado y lo que
    # no coincide es su fecha. Contarlo como identidad sin confirmar la subdeclaraba.
    ident = sum(l.strip().startswith(("OK", "id ok", "DIFIERE")) for l in lineas)
    fecha = sum(l.strip().startswith("OK") for l in lineas)
    # Por resta daba negativo cuando una fecha DIFIERE, porque esa línea cuenta en identidad
    # y en graves a la vez. Se cuenta lo que efectivamente no se pudo auditar.
    sin = sum(l.strip().startswith(("---", "???")) for l in lineas)
    print(f"\n  {len(lineas)} fallos | identidad confirmada en {ident} | "
          f"fecha además confirmada en {fecha} | sin poder auditar {sin} | "
          f"{len(graves)} A REVISAR")
    return 1 if graves else 0


if __name__ == "__main__":
    raise SystemExit(main())
