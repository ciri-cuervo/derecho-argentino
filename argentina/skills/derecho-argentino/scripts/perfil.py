#!/usr/bin/env python3
"""Perfil de trabajo del usuario: se pregunta una vez y ordena las preguntas de apertura.

    python3 perfil.py                         # muestra el perfil actual
    python3 perfil.py --set modo=sede-judicial --set jurisdicciones=pba,nacional
    python3 perfil.py --set rol=empleado-tribunal --set rol-fijo=si
    python3 perfil.py --borrar
    python3 perfil.py --json                  # para consumo programatico

QUE ES Y QUE NO ES
------------------
El perfil **no elige por el usuario**. La sección 0.1 de la skill prohíbe asumir el rol y el
fuero, y esta herramienta no la deroga: lo que hace el perfil es **ordenar la pregunta** --
poner primero las opciones probables-- y **fijar el modo de trabajo**, que si cambia
legitimamente la profundidad y el andamiaje de la respuesta.

La única excepción es `rol-fijo`, que el usuario tiene que pedir expresamente ("no me
preguntes más el rol"). Aun así la skill enuncia el rol asumido en la primera línea, para que
corregirlo cueste una palabra.

QUE NO SE GUARDA, NUNCA
-----------------------
- El CCT. No es dato de cartera: surge de lo que las partes invocan y prueban en cada causa.
- Datos de expedientes, partes, montos o cualquier cosa de un caso concreto.
- Nada que la skill deba verificar en cada consulta: topes, valor del jus, tasas.
El perfil describe COMO trabaja el usuario, no QUE dice el derecho.
"""
from __future__ import annotations

import argparse
import json
from datetime import date

from _raiz import archivo_config, leer_config

VERSION_PERFIL = 1

MODOS = {
    "sede-judicial": "Se trabaja desde el órgano: se verifica y se controla de oficio, no se produce el reclamo.",
    "ejercicio-profesional": "Se trabaja para una parte: se produce la pieza y se cuidan las decisiones irreversibles.",
    "estudio": "Uso academico o de formación: se explica el razonamiento y se citan las normas de apoyo.",
}

ROLES = {
    "juez": "Juez o jueza",
    "empleado-tribunal": "Empleado o funcionario de un tribunal",
    "abogado-parte": "Abogado o abogada de parte",
    "ministerio-publico": "Ministerio Publico fiscal o de la defensa",
    "asesor-perito": "Asesor, perito o cuerpo técnico",
    "estudiante": "Estudiante o docente",
    "otro": "Otro",
}

JURISDICCIONES = {
    "nacional": "Nacional y federal",
    "caba": "Ciudad Autónoma de Buenos Aires",
    "pba": "Provincia de Buenos Aires",
    "otra-provincia": "Otra provincia (sin perfil cargado)",
}

FUEROS = {
    "laboral": "Laboral", "civil-comercial": "Civil y comercial", "consumidor": "Consumidor",
    "familia": "Familia", "penal": "Penal", "previsional": "Previsional",
    "administrativo": "Contencioso administrativo", "tributario": "Tributario",
    "societario": "Societario", "concursal": "Concursal", "otro": "Otro",
}

LISTAS = {"jurisdicciones": JURISDICCIONES, "fueros": FUEROS}
SIMPLES = {"modo": MODOS, "rol": ROLES}
LIBRES = {"departamento-judicial", "notas"}
BOOLEANOS = {"rol-fijo"}

VACIO = {
    "version": VERSION_PERFIL, "modo": None, "rol": None, "rol_fijo": False,
    "jurisdicciones": [], "fueros": [], "departamento_judicial": None, "notas": None,
    "actualizado": None,
}


def _clave(k):
    return k.replace("-", "_")


def leer() -> dict:
    p = dict(VACIO)
    p.update(leer_config().get("perfil") or {})
    return p


def guardar(perfil: dict):
    f = archivo_config()
    f.parent.mkdir(parents=True, exist_ok=True)
    cfg = leer_config()
    perfil["version"] = VERSION_PERFIL
    perfil["actualizado"] = date.today().isoformat()
    cfg["perfil"] = perfil
    f.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f


def aplicar(perfil: dict, asignaciones):
    """Aplica 'clave=valor'. Devuelve la lista de errores; no escribe nada."""
    errores = []
    for a in asignaciones:
        if "=" not in a:
            errores.append(f"'{a}': falta el '='. Se espera clave=valor.")
            continue
        k, v = a.split("=", 1)
        k, v = k.strip().lower(), v.strip()
        if k in BOOLEANOS:
            if v.lower() not in ("si", "sí", "no", "true", "false"):
                errores.append(f"{k}: se espera si o no, no '{v}'.")
            else:
                perfil[_clave(k)] = v.lower() in ("si", "sí", "true")
        elif k in SIMPLES:
            if v == "":
                perfil[_clave(k)] = None
            elif v not in SIMPLES[k]:
                errores.append(f"{k}: '{v}' no es una opción. Válidas: {', '.join(SIMPLES[k])}.")
            else:
                perfil[_clave(k)] = v
        elif k in LISTAS:
            vals = [x.strip() for x in v.split(",") if x.strip()]
            malos = [x for x in vals if x not in LISTAS[k]]
            if malos:
                errores.append(f"{k}: {', '.join(malos)} no son opciones. "
                               f"Validas: {', '.join(LISTAS[k])}.")
            else:
                perfil[_clave(k)] = vals
        elif k in LIBRES:
            perfil[_clave(k)] = v or None
        else:
            validas = sorted(set(SIMPLES) | set(LISTAS) | LIBRES | BOOLEANOS)
            errores.append(f"'{k}' no es un campo del perfil. Campos: {', '.join(validas)}.")
    return errores


def describir(perfil: dict) -> str:
    if not any(perfil.get(k) for k in ("modo", "rol", "jurisdicciones", "fueros")):
        return ("  Perfil sin configurar.\n"
                "  La skill va a preguntar rol, fuero y jurisdicción en cada conversación,\n"
                "  que es el comportamiento correcto por defecto.\n\n"
                "  Para que ordene las opciones según como trabajás:\n"
                "    python3 perfil.py --set modo=... --set jurisdicciones=... --set fueros=...")
    L = ["  Perfil de trabajo:"]
    m = perfil.get("modo")
    L.append(f"    modo             {m or '(sin definir)'}")
    if m:
        L.append(f"                     {MODOS[m]}")
    r = perfil.get("rol")
    L.append(f"    rol habitual     {ROLES[r] if r else '(sin definir)'}"
             + ("  [FIJO: no se vuelve a preguntar]" if perfil.get("rol_fijo") and r
                else "  (se pregunta igual; el perfil solo ordena las opciones)" if r else ""))
    for k, cat in (("jurisdicciones", JURISDICCIONES), ("fueros", FUEROS)):
        v = perfil.get(k) or []
        L.append(f"    {k:16} {', '.join(cat[x] for x in v) if v else '(sin definir)'}")
    if perfil.get("departamento_judicial"):
        L.append(f"    departamento     {perfil['departamento_judicial']}")
    if perfil.get("notas"):
        L.append(f"    notas            {perfil['notas']}")
    L.append(f"    actualizado      {perfil.get('actualizado') or '-'}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", dest="sets", action="append", default=[], metavar="CLAVE=VALOR")
    ap.add_argument("--borrar", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--opciones", action="store_true", help="Lista los valores validos")
    a = ap.parse_args()

    if a.opciones:
        for nombre, cat in (("modo", MODOS), ("rol", ROLES),
                            ("jurisdicciones", JURISDICCIONES), ("fueros", FUEROS)):
            print(f"\n{nombre}:")
            for k, d in cat.items():
                print(f"  {k:24} {d}")
        print("\nrol-fijo: si | no      (pedirlo expresamente; por defecto no)")
        print("departamento-judicial, notas: texto libre")
        return

    if a.borrar:
        guardar(dict(VACIO))
        print(f"  Perfil borrado. La configuracion del repo no se toca.")
        return

    perfil = leer()
    if a.sets:
        errores = aplicar(perfil, a.sets)
        if errores:
            for e in errores:
                print(f"  ERROR  {e}")
            raise SystemExit(2)
        destino = guardar(perfil)
        print(describir(perfil))
        print(f"\n  Guardado en {destino}")
        return

    if a.json:
        print(json.dumps(perfil, ensure_ascii=False, indent=2))
        return
    print(describir(perfil))


if __name__ == "__main__":
    main()
