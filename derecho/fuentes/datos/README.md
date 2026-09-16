# `datos/` — series y tablas

Los montos no se citan de memoria (sección 2 de la skill). Salen de acá, o no salen.

| Archivo | Contenido | Lo consume | Estado |
| --- | --- | --- | --- |
| `jus-scba.csv` | Valor del jus del art. 9 de la Ley 14.967 y del jus del dec-ley 8904/77 | `honorarios_pba.py` | Cargado hasta 01/08/2026 |
| `inhabiles.json` | Ferias judiciales, puentes turísticos y asuetos | `plazos.py` | **Cargado** 2026; 2027 parcial |
| `serie-ipc.csv` | IPC INDEC nivel general, índice base dic-2016 | `intereses.py` | Parcial: 2024-01 a 2026-08 |
| `serie-ripte.csv` | RIPTE | `intereses.py` | Parcial: tres períodos |
| `serie-cer.csv` | CER | `intereses.py` | **Pendiente** |

Completar las series con `python3 ../scripts/descargar_series.py`. Trae las tres desde la API
de Series de Tiempo del Estado, valida que el IPC arranque en `2016-12 = 100.0` y no escribe
el archivo si ese control falla.

## Dos jus, no uno

La SCBA publica en la misma tabla el **jus del art. 9 de la Ley 14.967** y el **jus
arancelario del decreto-ley 8904/77**. El segundo subsiste porque leyes arancelarias de otras
profesiones remiten a él — peritos contadores, entre otros. En una regulación a abogados va
el de la 14.967. Confundirlos produce una diferencia del orden del 30%.

Tabla oficial: https://www.scba.gov.ar/paginas.asp?id=41320
Serie histórica (dic-2017 a nov-2023): https://www.scba.gov.ar/paginas.asp?id=46792

El valor cambia todos los meses y se publica con rezago. **Verificar el día de cada
regulación**, no confiar en la última fila del CSV.

## `inhabiles.json` — qué se calcula y qué se carga

`plazos.py` **calcula** los feriados de la Ley 27.399: los inamovibles, y Carnaval y Viernes
Santo por cómputo de Pascua. Los trasladables los ubica con la regla del art. 6 (martes y
miércoles al lunes anterior; jueves y viernes al lunes siguiente).

Lo que **no se puede calcular** y por eso vive en este archivo:

- **Ferias judiciales.** La de enero es permanente en las dos jurisdicciones — art. 2 del
  Reglamento para la Justicia Nacional y art. 1 del Decreto-ley 7951/1972 en PBA — pero la de
  invierno la fija cada año una acordada de la CSJN y un acuerdo de la SCBA, por separado. En
  2026 coincidieron (20 al 31 de julio), por normas distintas. **No presumir coincidencia.**
- **Puentes turísticos.** Los fija la Jefatura de Gabinete conforme el art. 7 de la Ley 27.399,
  no un decreto del PEN. Los de 2026 salieron por Resolución JGM 164/2025.
- **Asuetos.** Los distritales de PBA se publican mes a mes por resolución de Presidencia de
  la SCBA. Van en `asuetos_distritales` y **no se descuentan automáticamente**: alcanzan a un
  partido, no a toda la jurisdicción. El script los informa y quien computa decide.

Dos controles que hace el script con este archivo: compara su cálculo de los trasladables
contra `trasladables_verificados` y avisa si difieren; y marca los trasladables que caen sábado
o domingo, cuya ubicación quedó indeterminada desde el Decreto 614/2025, que deja la opción a
la Jefatura de Gabinete.

## Series de índices

Formato `periodo,indice`, período en `YYYY-MM`, una fila por mes. Las carga
`../scripts/descargar_series.py` desde la API de Series de Tiempo del Estado, con estos
`serie_id` verificados:

| Serie | serie_id | Organismo |
| --- | --- | --- |
| IPC nivel general, índice base dic-2016 | `145.3_INGNACNAL_DICI_M_15` | INDEC |
| RIPTE | `158.1_REPTE_0_0_5` | Sec. de Trabajo, Empleo y Seguridad Social |
| CER diario, colapsado a fin de mes | `94.2_CD_D_0_0_10` | BCRA vía datos.gob.ar |

Cuidado con `145.3_INGNACUAL_DICI_M_38`: difiere en un carácter y es la **variación mensual**,
no el índice. Por eso el script valida que el primer valor sea `2016-12 = 100.0` antes de
escribir el archivo.

Para el CER del día, la serie estatal atrasa unas dos semanas: ir a la API del BCRA,
`https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/30` (variable 30, sin token; la v3.0
devuelve HTTP 410).

## Dos series que no consume ningún script, pero que se usan a mano

Ninguna de las dos entra en `intereses.py`: son topes y pautas, no índices de actualización.
Se toman del informe del mes, no de una copia guardada.

**Canasta Básica Total, hogar 3.** Fija el tope del daño punitivo: de 0,5 a 2.100 CBT hogar 3
(art. 47 inc. b LDC, texto según art. 119 de la Ley 27.701). Informe mensual del INDEC.
Referencia verificada: julio de 2026, **$1.645.736,79**.

**Canasta de Crianza de la primera infancia, la niñez y la adolescencia.** Pauta de
cuantificación de alimentos en PBA (art. 641 CPCCBA, texto según Ley 15.513), facultativa y
sólo para menores de edad. Cubre **hasta 12 años inclusive**. Serie oficial:
https://www.indec.gob.ar/ftp/cuadros/sociedad/serie_canasta_crianza.xlsx
Referencia verificada, julio de 2026: menor de 1 año $545.683 · 1 a 3 años $649.935 · 4 a 5
años $554.646 · 6 a 12 años $697.268.

El INDEC pone un hash aleatorio en el nombre de los PDF de prensa, así que la URL del informe
del mes no se puede construir: hay que entrar y buscarlo.
