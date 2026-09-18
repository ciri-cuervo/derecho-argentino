---
name: honorarios
description: Regulación de honorarios y aportes. Pregunta la jurisdicción antes de calcular: en PBA, Ley 14.967 y el jus de la serie; en la nacional y federal, la Ley 27.423 sin dar número.
argument-hint: "[monto del proceso, porcentaje]"
allowed-tools: Read, Bash(python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/honorarios_pba.py:*), Bash(python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/uma_csjn.py:*)
---

Consulta: `$ARGUMENTS`

**Leé `${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/references/sede-judicial-pba.md` sección 1.6.6 antes de regular.** Ahí están las cuatro cosas
que hacen nula o mal hecha una regulación bonaerense.

## Primero: ¿qué justicia interviene?

**Preguntarlo antes de calcular, y no darlo por sentado.** Este comando regula por la **Ley
14.967**, que es el arancel de la Provincia de Buenos Aires, y su unidad es el **jus**. Fuera de
PBA no rige.

**La pregunta es por el fuero, no por la ciudad.** Una dirección no dice qué arancel se aplica.
En la Ciudad de Buenos Aires conviven **juzgados nacionales** y **juzgados de la Ciudad**, y cada
uno se rige por una ley arancelaria distinta, así que *"tramita en CABA"* no contesta nada: hay
que preguntar **si el juzgado es nacional o local**. El reparto entre uno y otro viene cambiando
por el traspaso de competencias, y no se da por sabido.

- **Justicia nacional o federal** —incluidos los juzgados nacionales con asiento en CABA—: el
  arancel es la **Ley 27.423** y la unidad es la **UMA**, no el jus. **El texto está bajado y el
  régimen está en `references/honorarios-nacional.md` 37**: la escala del art. 21, las etapas del
  art. 29, el 40% del procurador y la nulidad del art. 51. **Lo que no hay es el valor de la
  UMA**: `fuentes/datos/uma-csjn.csv` existe y está vacío, y se llena a mano porque la consulta
  oficial de la CSJN es un formulario y no una tabla. La conversión del art. 51 la hace
  `scripts/uma_csjn.py --fecha AAAA-MM-DD`, que **se planta** mientras no haya valores. Hasta
  entonces se explica el régimen y **no se entrega un número**.
- **Justicia local de la Ciudad de Buenos Aires:** rige la **Ley 5.134**, no la 27.423, aunque el
  juzgado quede a la vuelta de uno nacional. **Y acá está la trampa peor de toda la materia: esa
  ley también llama UMA a su unidad, y no es la misma.** La UMA porteña del art. 20 de la Ley
  5.134 es el **1,5% de la remuneración TOTAL** de un juez de primera instancia **de la Ciudad**
  —todos los rubros, incluida la bonificación por antigüedad de cinco años—; la nacional del art.
  19 de la Ley 27.423 es el **3% de la remuneración BÁSICA** de un juez **federal**. **Y las
  publica otro organismo:** la porteña, el Consejo de la Magistratura de CABA; la nacional, la
  CSJN. Buscar una en la fuente de la otra devuelve un número oficial y equivocado, expresado en
  «UMA» igual. El texto está en `fuentes/normas/caba-ley-5134.txt`.
- **Otra provincia:** cada una tiene la suya y **ninguna está cargada**. Ahí no se explica ni se
  calcula.

```text
[VERIFICAR MONTO ACTUALIZADO: valor de la UMA - art. 19 Ley 27.423, se consulta en csjn.gov.ar/transparencia/uma. El archivo fuentes/datos/uma-csjn.csv está sin valores, así que el valor no se toma de memoria ni se estima]
```

```text
[CONFIGURACIÓN INCOMPLETA: la causa tramita ante la justicia local de la Ciudad de Buenos Aires o de una provincia distinta de Buenos Aires, y esa ley arancelaria no está en fuentes/ - sin ese texto no se regula: la Ley 14.967 y el jus son de PBA, la Ley 27.423 y la UMA son de la justicia nacional y federal, y aplicar cualquiera de las dos afuera da un número plausible y equivocado]
```

**Un número con la unidad equivocada no es un error de redondeo.** El jus y la UMA son unidades
distintas de leyes distintas, así que el resultado sale con cara de correcto. Por eso la puerta
va antes del cálculo y no después.

## Lo que hay que tener resuelto

1. **La cuantía** (art. 23): el total reclamado en demanda o reconvención, no lo que prosperó.
2. **Las etapas.** En procesos orales ante tribunales colegiados el **art. 28 inc. h** cuenta
   **tres** etapas, no las del proceso escrito. Pasalas con `--etapas-cumplidas` y
   `--etapas-totales`.
3. **El monto en jus es requisito de validez** — art. 15 inc. d, bajo pena de nulidad. Y el
   valor definitivo del jus es **el del momento del pago**, no el de la regulación.
4. **Diferimiento del art. 51**: si hay intereses pendientes de determinación, corresponde
   diferir. Verificá si es el caso antes de dar un número cerrado.

## Después

**Abrí con el bloque de datos tomados**, copiado de la cabecera de la salida del script y
cotejado contra lo que te dieron. Un dato mal tipeado no rompe nada: devuelve un resultado
plausible. Si alguno no coincide, pará y preguntá. Ver `intake.md`, «Devolver los datos
antes de usarlos».

```sh
python3 ${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/derecho-argentino/scripts/honorarios_pba.py --monto N --porcentaje N \
  [--valor-jus N] [--etapas-cumplidas N] [--etapas-totales N] \
  [--con-intereses] [--tipo {contradictorio|voluntario}] [--tasa-justicia N]
```

**No pases `--valor-jus` de memoria.** Sin ese flag el script lo lee de
`fuentes/datos/jus-scba.csv` e informa a qué fecha corresponde el valor usado. Si la serie
está vieja, el script lo dice: transcribí esa advertencia, no la borres. Si sale con código 2,
el marcador es la respuesta.

Informá siempre **el monto en jus y el valor del jus con su fecha**, más los aportes de la Ley
6.716 art. 12 si corresponden.
