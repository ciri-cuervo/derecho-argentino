# `argentina/fuentes/` — qué hay acá, de dónde salió y qué se puede hacer con cada cosa

Esta carpeta es la capa de **fuente primaria offline** del repo. Su función es que una
transcripción a un escrito salga de un texto verificable con procedencia registrada, y no de
la memoria del modelo ni de una consulta automática que puede venir truncada.

**El repositorio es público.** Nada que entre acá puede tener derechos reservados, y nada que
entre acá puede contener datos de expedientes.

## Estructura

| Carpeta | Qué es | Licencia / uso |
| --- | --- | --- |
| `normas/` | Texto consolidado de las normas de uso diario, con encabezado de procedencia y hash | Normas jurídicas: reproducción libre |
| `jurisprudencia/` | Precedentes verificados con enlace a la sentencia oficial. `INDICE.md` es la entrada | Sentencias: reproducción libre |
| `jurisprudencia/ocr/` | Texto **recuperado por OCR local** de los PDF que vinieron con la capa de texto arruinada. Es una derivación, no una descarga: ver abajo | Sentencias: reproducción libre |
| `datos/` | Series y tablas: valor del jus, inhábiles, IPC, RIPTE, CER | Datos públicos de organismos oficiales |
| `ccyc-comentado/` | *Código Civil y Comercial de la Nación Comentado*, SAIJ-INFOJUS, 2ª ed. 2022, seis tomos. `INDICE.md` rutea artículo a tomo y página | Publicación oficial de distribución gratuita y **libre reproducción citando la fuente**: se puede citar y transcribir |
| `scripts/` | Descargador y verificador de normas | — |
| `_local/` | Ejemplares personales del abogado. **Gitignoreado, no se commitea** | Obras comerciales con derechos reservados |

## Reglas

1. **Nada con derechos reservados.** El *Manual de Derecho de Daños* (Weingarten -dir.-, La
   Ley) vive en `_local/`, fuera del control de versiones. Lo que sí está versionado es
   `argentina/skills/derecho-argentino/references/danos-indice-doctrinario.md`: un índice destilado que dice dónde la obra trata cada
   instituto. En un escrito se cita la obra, nunca el archivo.
2. **Nada de expedientes.** Ni piezas, ni liquidaciones, ni datos de partes. Los entregables
   van a `~/guada/derecho`, nunca acá.
3. **Todo con procedencia.** URL, fecha de descarga y hash. Sin eso, un texto no sirve como
   fuente: sirve como apunte.
4. **Lo bajado no es publicación oficial.** Es material de trabajo verificable. Para
   transcribir un artículo, cotejar contra el Boletín Oficial de la fecha de publicación.

## Cómo poblar `normas/`

    cd argentina/fuentes/scripts
    python3 descargar_normas.py --prioridad 1     # lo imprescindible
    python3 descargar_normas.py                   # todo el manifiesto

Cada texto queda en `normas/<slug>.txt` con encabezado de procedencia, y el hash se registra
en `normas/procedencia.json`. Quedan **2 entradas sin URL**. Se declaran igual: una norma que un
módulo necesita y no está bajada queda **visible en el catálogo** en vez de perderse, y el
descargador la saltea e informa.

- **Constitución Nacional con los tratados** de jerarquía constitucional: se consolidó a mano y no
  tiene una URL única.
- **Ley 13.478**, de 1948: **InfoLEG no publica normas de esa época.** Buscada en septiembre de 2026 en
  InfoLEG, argentina.gob.ar y SAIJ; sólo hay fuentes secundarias. Su art. 9 se cotejo contra el
  Boletín Oficial de 1948 o contra el texto transcripto en el propio fallo que lo discute.

**Cómo salieron los últimos seis `id`.** InfoLEG responde 403 a los agentes, pero su **buscador no
tiene captcha**: `servicios.infoleg.gob.ar/infolegInternet/mostrarBusquedaNormas.do`, `tipoNorma=1`
para ley y el número. Devuelve el `id`, y la ficha `verNorma.do?id=<id>` dice si hay `texact.htm`.
El de argentina.gob.ar **sí tiene captcha** (Turnstile), así que no sirve para esto. Bajadas el
15/09/2026:

| Norma | id | Qué se confirmó al abrirla |
| --- | --- | --- |
| **Ley 27.798** | 422000 | Presupuesto 2026. Su art. 62 excepciona los arts. 7 y 10 de la Ley 23.928 **sólo para préstamos y títulos públicos provinciales y de CABA**: no alcanza al crédito laboral |
| **Ley 23.857** | 257 | Trae el **Convenio de La Haya completo** como anexo, con el art. 13 inc. b —grave riesgo— |
| **Ley 25.358** | 65330 | Convención Interamericana sobre restitución internacional |
| **Ley 25.390** | 65899 | Trae el Estatuto de Roma como anexo, 302 KB. Arts. 6, 7 y 8: genocidio, lesa humanidad, crímenes de guerra. **No tiene art. 8 bis** |
| **Ley 26.200** | 123921 | Implementación del Estatuto, 52 artículos propios con las penas |
| **Ley 26.023** | 105500 | Ley aprobatoria **más** la Convención transcripta, arts. 1 a 23. Marcada para revisar y resuelta como falso positivo |

**Los acuerdos de la SCBA no están en InfoLEG, y tienen dos fuentes con roles distintos.**
`normas.gba.gob.ar` sirve el texto **tal como se publicó en el Boletín Oficial**: la ficha
`ar-b/resolucion/<año>/<número>/<id>` da número y fecha de BO, y linkea el documento en
`documentos/<hash>.html`, que viene en UTF-8 y con la acentuación correcta. El **digesto de la
SCBA** —`digesto.scba.gov.ar/VerTextoCompleto.aspx?idFallo=<id>`— sirve otra cosa y por eso vale
más para verificar: **declara el alcance de cada norma** (`Vigente` / `Anexo Histórico`) y lista
sus modificatorias. Su buscador numérico no tiene captcha; el `idFallo` sale del `VerTexto(<id>)`
del resultado. Para citar el texto publicado, `normas.gba.gob.ar`; para saber si sigue en pie y
qué lo modificó, el digesto.

**El texto del digesto viene envuelto en la maqueta del sitio, y eso no es un defecto.** Los dos
acuerdos modificatorios traen unos 370 renglones de navegación del digesto antes del articulado, y
más del 80% de sus líneas quedan vacías. El articulado está completo —el Ac. 4113 conserva sus 48
artículos y su VISTO—, así que `descargar_normas.py` **no los marca, y hace bien**: de los 132
textos bajados, **35 vienen con el cromo de argentina.gob.ar** y los 35 son completos. Por eso la
detección de cromo está condicionada a que además haya pocos artículos: sin esa condición, marcaría
las veintidós constituciones provinciales y el CPCCN.

Lo que sí conviene saber: como el `sha256_texto` se calcula sobre lo extraído, **un rediseño del
portal mueve el hash sin que cambie la norma**. `verificar_normas.py` lo va a reportar, y por eso su
salida dice qué mirar y no qué cambió.

**Cómo se completa una URL que falta.** El dato que hace falta es el **`id` interno de InfoLEG**,
que es lo que arma la ruta `anexos/<rango de 5.000>/<id>/<norma|texact>.htm`. Se encuentra en la
URL de argentina.gob.ar, que lo lleva al final: `/normativa/nacional/ley-23789-190` → id 190.
Con el id, la **ficha** `verNorma.do?id=<id>` dice si además del texto original hay **texto
actualizado**: si ofrece `texact.htm`, ésa es la URL que va, porque trae las modificaciones.
InfoLEG responde 403 a los agentes, así que la ficha se mira en un navegador; el texto lo baja
siempre el script, que es lo que le pone encabezado, hash y fecha.

## Cuando el descargador marca una norma para revisar

`descargar_normas.py` mira cada texto recién bajado y marca lo que no cuadra: pocos artículos,
el cromo del portal en vez del articulado, acentuación degradada, una ley aprobatoria donde
debía estar su anexo. Son **candidatos, no defectos probados**. Hay leyes legítimamente cortas:
la 24.754 son dos artículos y 1.430 caracteres, y eso es la ley entera.

La marca se apaga leyendo el texto y anotando el veredicto en `normas/revisiones.json`:

```json
"ley-24754": [
  {"problema": "solo 2 articulos en 1430 caracteres: sospechosamente corto",
   "veredicto": "Falso positivo. La ley son dos articulos: el 1 sustantivo y el 2 de forma.",
   "fecha": "2026-09-14"}
]
```

El veredicto se indexa por el **texto exacto del problema**, no por el slug. Si esa norma vuelve
con otro defecto, o si cambia cómo el detector lo redacta, el veredicto deja de aplicar y la
marca vuelve a sonar: vale para lo que se leyó, no para el archivo. La corrida siguiente imprime
`REVISADO` con el veredicto a la vista, en vez de `REVISAR`, y `procedencia.json` lo guarda bajo
`revisado`. Sin esto la misma marca suena en cada descarga hasta que nadie la mira.

## Cuando el PDF viene con la capa de texto arruinada

Algunos fallos escaneados —los más viejos, pero no sólo ellos— traen una capa de texto hecha con
un OCR de otra época, y `pdftotext` se limita a copiarla. En "Bazterrica" devolvía
`El] \^<+]Ky puede P^+*+y un ^Fy dia` donde la página dice **"El sujeto puede un día probar la
droga"**. El papel está bien; lo que está roto es esa capa.

    python3 herramientas/reocr_jurisprudencia.py --listar
    python3 herramientas/reocr_jurisprudencia.py

Vuelve a leer las imágenes con `tesseract -l spa` y deja el resultado en `jurisprudencia/ocr/`,
con el hash del PDF del que salió, la versión de la herramienta y la fecha en el encabezado de
cada archivo y en `ocr/procedencia.json`. Requiere `poppler` y `brew install tesseract-lang`.

Tres cosas que no hay que perder de vista. **Es una derivación local, no una descarga**: no es
publicación oficial y no reemplaza al PDF. **El OCR nuevo deja errores residuales** —"Orros" por
"Otros", "demaudada" por "demandada"—, así que una cita literal a un escrito se coteja contra la
página, que está numerada en el archivo. Y **si el PDF se vuelve a bajar, la derivación queda
vieja**: `test_scripts.py` compara los hashes y avisa.

## Cómo detectar que una norma cambió

    python3 verificar_normas.py --prioridad 1

Vuelve a pedir cada URL y compara el hash contra el registrado. Sale con código 1 si alguna
cambió, así que se puede colgar de una tarea programada. Que el hash cambie no prueba que
cambió la ley — las bases oficiales retocan la maquetación de sus páginas — pero sí dice
cuál hay que mirar. Cuando el cambio es de fondo, anotarlo en
`argentina/skills/derecho-argentino/references/changelog-normativo.md`.

### Dos hashes, y por qué

Cada texto lleva **dos**. El **crudo** es de los bytes que sirvió el servidor; el **de texto**,
del articulado extraído, sin el encabezado de procedencia. Se necesitan los dos porque el crudo
se mueve solo: en una redescarga, **37 de 116 normas cambiaron el hash crudo y sólo 3 el detexto**
—33 de esas 37 son de `argentina.gob.ar`, que reescribe el HTML en cada pedido—. Por eso
`verificar_normas.py`, cuando el crudo no coincide, no grita: vuelve a extraer el texto y compara
ese hash, y recién ahí dice `CAMBIO`.

Lo que el hash de texto **no** filtraba era el cromo con fecha de hoy que el **Boletín Oficial**
y **JURISTECA** imprimen dentro del cuerpo, encima de la norma. Eran las tres del párrafo
anterior, y habrían cantado *"cambió el texto de la norma"* todos los días. Una alarma que suena
siempre es una alarma que se deja de mirar, y por ahí es por donde se pierde un cambio real.

`normalizar_cromo()` la saca **anclada a los rótulos que el portal pone alrededor** —"Edición
del … Ediciones Anteriores", "Saltar al contenido … Las fuentes del Derecho"— y no con una
expresión que busque fechas: eso se comería las de sanción, promulgación y vigencia, que son
parte de la norma y cuya desaparición es justo lo que hay que detectar. Donde estaba queda
`[fecha del portal, no es parte de la norma]`, para que quien lea el `.txt` vea que ahí se sacó
algo a propósito. Hay tests que lo fijan, incluido el que comprueba que una fecha suelta, sin esos
rótulos, no se toca.

## Estado a septiembre de 2026

Esta tabla es una foto, y las fotos se vencen. La medición viva la da
`python3 argentina/skills/derecho-argentino/scripts/estado.py`, que lee los archivos en vez de
recordarlos. Para que la foto no se separe del repo en silencio, `test_scripts.py` lee estos
números y los compara contra lo que hay: si alguno deja de coincidir, los tests fallan.

| Pieza | Estado |
| --- | --- |
| `ccyc-comentado/` | Completo, con índice de ruteo |
| `normas/normas.json` | **138 entradas**, 136 con URL verificada |
| `normas/*.txt` | **132 descargadas**; `procedencia.json` registra **137 textos con hash** |
| `jurisprudencia/fallos.json` | **64 fallos**, todos con URL |
| `jurisprudencia/*.pdf` | **63 descargados** |
| `datos/jus-scba.csv` | **6 filas**, cargado hasta el 01/08/2026 |
| `datos/inhabiles.json` | Cargado: 2026 completo para Nación y PBA; 2027 sólo la feria de enero |
| `datos/serie-ipc.csv` | **Completa**: 117 períodos, 2016-12 a 2026-08 |
| `datos/serie-ripte.csv` | **Completa**: 385 períodos, 1994-07 a 2026-07 |
| `datos/serie-cer.csv` | **Completa**: 117 períodos, 2016-12 a 2026-08 |

Los tres números de `normas/` cuentan cosas distintas y no tienen por qué coincidir: **138** es lo
que la skill espera encontrar, **137** es lo que tiene texto bajado con hash registrado, y **132**
son los `.txt` en disco, porque los **5** restantes son PDF. La única entrada declarada que no
tiene texto es la Ley 13.478, por lo dicho arriba: está en el catálogo para que se vea que falta.

## Qué hacer con esto ya cargado

Los textos consolidados sirven para **cotejar antes de transcribir**, y ese cotejo ya
corrigió cuatro cosas del módulo de sede judicial: el art. 11 de la Ley 15.057 dice que el
procedimiento *"podrá"* ser impulsado, no *"deberá"*; el art. 83 **no** es equivalente al
art. 56 de la Ley 11.653; el art. 28 inc. h de la Ley 14.967 fija **tres etapas** para los
procesos orales ante tribunales colegiados; y el art. 51 manda **diferir** el auto regulatorio
cuando la condena incluye intereses.

Una advertencia que quedó confirmada: `normas.gba.gob.ar` sirve la **Ley 11.653** con la
acentuación degradada en algunos pasajes ("deber" por "deberá", "m‚rito" por "mérito"). Las
demás normas bonaerenses vinieron limpias. Para una transcripción literal a una resolución,
cotejar contra el Boletín Oficial.

## Control periódico

    python3 verificar_normas.py --prioridad 1

Vuelve a pedir cada norma, compara el hash contra la copia local y sale con código 1 si alguna
cambió. Sirve como alarma de reforma legislativa. Si una descarga falla con error de
certificado, `pip install certifi`. Si falla con timeout en un solo dominio, revisar el DNS:
una VPN activa puede resolver `gba.gob.ar` a una dirección interna.
