# Marca

Un sello de cargo: lo más reconocible de un expediente argentino y lo que hace la herramienta
—fijar fecha y dejar constancia de algo verificable—. El marco de goma gastada **es** el logo;
el renglón del medio es el blanco que la skill completa, y el campo de abajo son tres celdas de
formulario con las jurisdicciones que hoy resuelve el ruteo: PBA, Nación y CABA.

Todo sale de `generar_marca.py`, que vive en `derecho-argentino-marca/` —al lado de este
repo, no adentro: ver `docs/DESARROLLO.md` § La marca— y describe cada figura una sola vez y la escribe
en SVG y en PNG:

```sh
cd ../derecho-argentino-marca
python3 generar_marca.py --salida ../derecho-argentino/assets/marca
python3 test_marca.py
```

## Archivos

| Archivo | Uso |
| --- | --- |
| `banner-claro.png` · `.svg` | Encabezado del README, tinta oscura. 1280 × 320, sin fondo. |
| `banner-oscuro.png` · `.svg` | Lo mismo con tinta clara; el README elige con `<picture>`. |
| `chapa-version` · `chapa-licencia` · `chapa-python` · `chapa-agentes` | La fila de etiquetas bajo el título. Alto 64, al doble: se muestran a la mitad. |
| `separador.png` · `.svg` | Renglón cosido entre bloques del README. 2560 × 56, al doble. |
| `icono.png` · `.svg` · `icono-128.png` | Avatar de la organización, ícono del plugin. 512 y 128. |
| `icono-oscuro.png` · `.svg` | El ícono para fondos oscuros. |
| `social-preview.png` · `.svg` | *Settings → General → Social preview*. 1280 × 640, se sube a mano. |

El banner, las chapitas y el separador van **sin fondo**, para que se apoyen sobre el color de la
página en vez de quedar como un recuadro pegado encima —papel sobre el blanco de GitHub, o gris
sobre su oscuro, se notan—. Eso obliga a que el desgaste del sello **borre** en lugar de pintar
del color del fondo: en el PNG se resta del canal alfa y en el SVG es una `<mask>`. El ícono y el
social preview sí llevan fondo: son imágenes que se ven solas.

La versión de `chapa-version` sale de `derecho/.claude-plugin/plugin.json`, no está escrita a
mano. Si cambia y el texto queda más ancho, `test_marca.py` avisa que hay que corregir el atributo
`width` del README.

## Paleta

| | |
| --- | --- |
| papel | `#F7F5F0` |
| tinta | `#1C1C1A` |
| celeste | `#5B93C7` |
| celeste profundo | `#2F6B9E` |
| gris foja | `#A8A29A` |
| oscuro | `#14181C` |

En tema oscuro el sello aclara a `#8FBEE4` para no perder contraste contra `#14181C`.

## Tipografías

**DIN Condensed Bold** en el sello: es la letra de los formularios oficiales, condensada y sin
gracia, y aguanta el interletrado abierto que necesita un sello. **Charter Roman** en la línea
descriptiva. Las dos son fuentes del sistema en macOS y en el SVG salen **convertidas a curvas**:
GitHub dibuja los SVG con las fuentes de su servidor, no con las de la máquina, así que con
`<text>` el sello se descolocaría en cualquier otra parte.

Por eso el README apunta a los PNG y no a los SVG: son los que se ven igual en todos lados. Los
SVG están para reescalar sin pérdida.
