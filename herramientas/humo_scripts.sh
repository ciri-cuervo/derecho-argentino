#!/usr/bin/env bash
# Corre una vez cada script que viaja con el plugin, con el intérprete que se le pase, y falla si
# alguno sale con un código que no es el suyo.
#
#     herramientas/humo_scripts.sh python3
#     PYTHONIOENCODING=cp1252 herramientas/humo_scripts.sh /usr/bin/python3
#
# Existe para el job de Windows del CI. El desarrollo es en Linux y macOS, así que las suites no
# corren ahí; la skill sí, y esto es lo que ejecuta. Con la salida a un pipe, Python en Windows
# escribe en cp1252: un carácter que no entra corta el script a mitad de la salida.
#
# No mide resultados —eso lo hacen las suites—: mide que cada script arranque, lea sus datos e
# imprima sin romper. No sale a la red: los descargadores corren sólo con --help.
set -u
PY=${1:?falta el intérprete: python3, python o "py -3"}
AQUI=$(cd "$(dirname "$0")/.." && pwd)
S="$AQUI/derecho/skills/derecho-argentino/scripts"
F="$AQUI/derecho/fuentes/scripts"
CFG=$(mktemp -d)
export XDG_CONFIG_HOME="$CFG"
fallas=0

# esperado: los códigos aceptados, separados por coma. estado.py sale con 1 si hay datos vencidos.
correr() {
  local esperado=$1; shift
  local salida rc
  salida=$($PY "$@" 2>&1 < /dev/null); rc=$?
  if [[ ",$esperado," == *",$rc,"* ]]; then
    echo "ok    rc=$rc  $(basename "$1") ${*:2}"
  else
    echo "FALLA rc=$rc  $(basename "$1") ${*:2}"
    echo "$salida" | tail -15 | sed 's/^/      /'
    fallas=$((fallas + 1))
  fi
}

correr 0,1 "$S/estado.py"
correr 0   "$S/perfil.py" --json
correr 0   "$S/configurar.py" --mostrar
correr 0   "$S/honorarios_pba.py" --monto 10000000 --porcentaje 20
correr 0   "$S/uma_csjn.py" --fecha 2026-09-01
correr 0   "$S/uma_caba.py" --help
correr 0   "$S/liquidacion_lct.py" --ingreso 2020-03-02 --extincion 2026-06-30 \
             --mejor-remuneracion 1500000 --empleador privado --regimen lct
correr 2   "$S/liquidacion_lct.py" --ingreso 2020-03-02 --extincion 2026-06-30 \
             --mejor-remuneracion 1500000 --regimen casas-particulares
correr 0   "$S/plazos.py" --tipo habiles --desde 2026-09-01 --dias 5 --fuero pba
correr 0   "$S/intereses.py" --modo tasa --capital 1000000 --desde 2025-01-01 --hasta 2025-12-31 --tna 50
correr 0   "$S/articulo.py" lct-20744 245
correr 0   "$S/verificar_respuesta.py" --vocabulario
correr 0   "$F/verificar_normas.py" --help
correr 0   "$F/descargar_normas.py" --help
correr 0   "$F/descargar_series.py" --help
correr 0   "$F/descargar_jurisprudencia.py" --help
correr 0   "$F/diagnostico.py" --help

rm -rf "$CFG"
echo
if [ "$fallas" -gt 0 ]; then echo "$fallas scripts fallaron con $PY"; exit 1; fi
echo "todos los scripts corrieron con $PY"
