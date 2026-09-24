# 📌 Lo que queda pendiente

Lo que **ninguna herramienta mide**. Lo que sí miden está en los comandos que lista
[`AGENTS.md`](../AGENTS.md); acá va lo otro: lo que se decide leyendo.

**Y no todo lo de acá es deuda.** Mezclar una decisión que se puede tomar con un hecho del
mundo que no se va a mover hace que la lista entera se lea como atraso, y una lista que se lee
como atraso se deja de leer. Por eso van separadas, y por eso **se referencian por su título y
no por un número**: el número cambia cada vez que una se cierra, y las remisiones de otros
archivos quedan apuntando a otra cosa.

Cada entrada dice por qué no se puede automatizar. Lo que se resuelve se saca.

---

## Decisiones abiertas

Se cierran decidiendo. Ninguna espera una herramienta nueva: esperan un criterio.

### El formato de los casos de prueba

**Los casos de prueba están en un formato propio y `claude plugin eval` lee otro.** El nativo es
`prompt.md` con `graders/*.md` —o `case.yaml`— y lo corre el comando con arm de ablación sin
plugin; el nuestro es la terna `caso.md`, `rubrica.md` y `resultado.md`, que se lee a mano. El
manifiesto ya declara `experimental.evals`, y hay **dos migrados** que sirven de molde:
`laboral-despido-tramos-reforma-pba` y `dipr-prorroga-tacita-y-jurisdiccion-exclusiva`. Los dos
conservan la terna además del formato nativo, así que la primera pregunta quedó contestada en
los hechos: **conviven**, porque `rubrica.md` dice en prosa lo que los graders dicen ejecutable
y `resultado.md` es un registro fechado de lo que se vio. Falta decidir la otra: qué pasa con
los casos heredados de capa 2, que se pueden envolver pero no reescribir.

**Y hay cinco más migrados, elegidos por un criterio y no por orden de lista:** aquellos en los
que **retener un dato es la respuesta correcta** —`honorarios-nacional-uma-caba-y-art64`,
`transito-uf-prescripcion-y-art64`, `previsional-compensacion-de-edad-y-pba`,
`honorarios-pba-jus-y-etapas` y `civil-danos-transito-factor-objetivo-pba`—. Son los que miden lo
único que hace distinta a esta skill, y lo que primero se cae con un modelo de menor capacidad.

**Sus criterios negativos van todos deterministas, y esa es la decisión de diseño.** Este mismo
repositorio tiene registrado que un juez chico reprueba respuestas correctas cuando el criterio
pide que algo NO aparezca, así que «no dio un número» se mide con `match: not_contains` sobre un
importe en pesos, que es un hecho de la cadena de caracteres. Lo que sí queda en manos de un juez
son los criterios de fondo, que son afirmaciones sobre derecho y no sobre la forma de la salida.

**Cuidado con prohibir de más.** El grader de `honorarios-pba-jus-y-etapas` excluye con un
lookahead el capital de sentencia que el propio enunciado trae, porque una respuesta correcta lo
cita de vuelta: sin esa exclusión, el control reprobaría exactamente lo que quiere premiar.
**Migrar no es medir.** De los siete, uno se corrió —`laboral-despido-tramos-reforma-pba`, con
la comparación en `BITACORA.md`— y el precio está ahí: tres pasadas por brazo y del orden de diez
dólares por corrida. De los otros seis, tres declaran «Sin correr» en su `resultado.md` y tres
traen el resultado esperado en prosa, que describe qué se espera y no qué pasó.

### Los reclamos de faltante que no nombran una norma

**El control cruza el párrafo contra dos catálogos** —normas por número y jurisprudencia por el
apellido de la carátula— **y lo que queda afuera lo dice su propia salida:**
`python3 herramientas/deuda_vencida.py --sin-cruzar`. No copies la cifra acá: la mide el comando.

**Lo que queda es una sola clase, y no tiene contra qué cruzarse:** la categoría en vez de la
norma —"su ley arancelaria local", "los estatutos locales", "las acordadas de la CSJN", "la
reglamentación del BCRA"—. Lo que falta es un conjunto abierto, no una pieza, así que **no
existe una entrada de catálogo que nombrar**. Se lee. Por lo mismo no pide una convención nueva
en `references/marcadores.md`: nombrar el slug no sirve cuando no hay un slug.

**Las series de `fuentes/datos/` no se cruzan, y la medida está descartada.** Derivar el índice
de los nombres de archivo engancha la UMA porteña con `uma-csjn.csv` y las acordadas de la CSJN
con el `csjn` del mismo archivo, y no alcanza a los reclamos que dicen "la serie de valores" sin
nombrarla. Una medida que se equivoca sobre un caso conocido se descarta, no se calibra.

**Y hay tres límites del cruce de fallos que se declaran en vez de calibrarse.** Un apellido que
comparten varios fallos no los separa: en `fallos-csjn.md` conviven un "Bianchi" penal, que está
bajado, y un "Bianchi" de peaje, que no, y el cruce los ve iguales. Las carátulas anonimizadas,
que son las de familia y violencia, no tienen apellido que indexar y tampoco se citan así. Y el
apellido es el **primer token**, así que un compuesto que arranca con partícula corta —"San
Martín", "De la Rosa"— no se indexa; bajar el mínimo metería "DE" y "LA", que colisionan con
media biblioteca. Hoy no hay ninguna carátula así en el catálogo, y un test lo fija.

**Lo que NO es un límite: los diacríticos.** `pelado()` corre antes del regex y de los dos lados,
así que "Agüero" y AGÜERO llegan los dos como AGUERO, y "Peña" como PENA. La clase de letras va
sin acentos **a propósito**, y agregarle `ÜÁÑ` no arreglaría nada: haría creer que el acento se
maneja ahí.

**Lo que está cubierto por otro instrumento y no vuelve acá.** Un instrumento con número que no
es una ley —un decreto, una resolución, un acuerdo de la SCBA— lo mira `cobertura_normativa.py`
igual que a una ley, porque se citan igual. Un cuerpo normativo nombrado y sin número queda
declarado en `derecho/fuentes/MANIFIESTO.md` con slug aunque no tenga URL, y ahí el detector lo
alcanza. Y `references/changelog-normativo.md` está fuera del alcance a propósito: cada fila dice
qué se cotejó y qué falta **con su fecha**, y eso es su contenido, no un reclamo que se olvidó de
actualizar.

### En qué formato entrega lo que produce

**Hoy la skill entrega texto.** Un escrito, una liquidación o un cotejo salen como markdown en la
conversación, y quien los necesita en otro formato los copia y los maqueta.

**Y la pregunta no es de preferencia: el formato lo impone el tribunal.** Un escrito que se
presenta por el sistema de presentaciones electrónicas tiene **requisitos técnicos de archivo**
—formato, tamaño máximo, estándar de digitalización de lo que va adjunto, firma— y un documento que
no los cumple **se rechaza en la mesa de entradas, no en el fondo**. Entregar un `.docx` impecable
que el portal no acepta no resuelve nada.

**El repositorio tiene el reglamento y no tiene las especificaciones.** Para PBA está el
*Reglamento para las presentaciones y las notificaciones por medios electrónicos* en
`fuentes/normas/pba-scba-dosier-pyne-2021.pdf`, que manda acompañar los documentos digitalizados
como adjuntos, **pero las especificaciones concretas viven en resoluciones y anexos técnicos del
portal que no están bajados**. De Nación y de CABA no hay ni una cosa ni la otra.

**Y hay un hueco propio que sale a la luz al mirar esto:** `references/notificaciones-pba.md` 22 es
el módulo del expediente digital bonaerense **y no menciona el formato de archivo en ninguna
parte**. Antes de decidir qué genera la skill, ese módulo tiene que poder decir qué acepta el
sistema.

**A eso se suman dos restricciones técnicas que acotan la respuesta:**

- **El plugin corre en Claude y en Codex.** Una capacidad que dependa de una herramienta de un solo
  agente deja la skill funcionando distinto según dónde se instale, y eso es lo que `AGENTS.md`
  prohíbe: si algo funciona en uno solo, se dice cuál.
- **Los scripts declaran no tener dependencias externas**, y generar un `.docx` o un PDF con
  fidelidad exige una. Meterla cambia lo que significa instalar este plugin —hoy alcanza con
  Python— y hay que decidirlo a propósito, no de hecho.

**El orden importa y es éste:** primero bajar los requisitos técnicos de cada jurisdicción y
escribirlos donde se consultan, después decidir qué formato se genera. Al revés se construye una
capacidad sin saber contra qué especificación. Lo que sí es firme desde ahora: **el mismo pedido no
puede devolver un archivo en un agente y un texto en el otro sin avisarlo**.

### Negociación: si es un módulo o es otra cosa

**La skill sabe analizar y redactar; no sabe negociar.** Un acuerdo transaccional, una mediación
o una audiencia de conciliación tienen su propia lógica —zona de acuerdo posible, alternativas a
falta de acuerdo, secuencia de concesiones, qué se firma y qué se reserva— y hoy no hay nada de
eso en `references/`.

**La decisión no es si hace falta sino qué forma toma**, y las dos opciones tienen costos
distintos. Un **módulo** más entra por las puertas de siempre y queda sujeto a la disciplina de
fuente primaria, que acá es incómoda: **la negociación no se funda en normas**, así que un módulo
suyo no tendría articulado que citar y rompería el molde del resto. Una **sub-skill** separada
tiene su propio `SKILL.md` y su propio disparador, no arrastra la exigencia de fuente normativa, y
deja explícito que es otra clase de conocimiento — pero suma una segunda skill al plugin y hay que
decidir cómo se rutea entre las dos.

**Lo que sí está claro y vale para cualquiera de las dos:** el marco legal de lo que se negocia
—homologación, cosa juzgada, irrenunciabilidad del art. 12 LCT, el SECLO y la mediación previa—
**ya está en los módulos** y no se duplica.

## Restricciones que no se levantan

No son deuda: son hechos de afuera. Están escritas para que nadie las vuelva a discutir
creyendo que hay algo que hacer, y para que quien tropiece con ellas sepa que ya se midieron.

### Normas que no tienen URL oficial

**Las normas declaradas en `normas.json` que no tienen URL oficial son estructurales, y no la
van a tener.** Una es la Ley 13.478, de 1948, que InfoLEG no publica por época; la otra, la
publicación de los once instrumentos del art. 75 inc. 22 en un solo documento. Están en el
catálogo para que se vea que faltan, y el motivo de cada una está escrito en su entrada.

### Los registros judiciales no se pueden buscar

**Los registros judiciales oficiales se buscan con navegador, no con un cliente HTTP.** Ninguno
admite consulta por query string: JUBA opera por postback de ASP.NET y el buscador de sumarios de
la CSJN necesita el estado de sesión que deja el formulario. Con un navegador **los dos
responden**, y las dos cadenas están escritas en
[`derecho/fuentes/jurisprudencia/INDICE.md`](../derecho/fuentes/jurisprudencia/INDICE.md): el
navegador **ubica** y entrega un identificador, y el descargador **baja** por URL directa. **SAIJ
no tiene equivalente**: su `resultados.jsp` acepta la query sin rechazarla y devuelve *"SIN
RESULTADO"*, que es el peor modo de falla —parece una búsqueda vacía y es un buscador que no se
consulta así—.

Lo que queda sin registro consultable es **el fuero federal de cámara y los fueros de CABA**, y
ahí la búsqueda sigue dependiendo de afuera. Eso pesa sobre *El trabajo de fondo*: ampliar la
jurisprudencia leída es más caro de lo que parece, y el cuello no es leer sino ubicar.

**Y hay una dependencia que conviene tener presente:** esto exige que la extensión de navegador
esté conectada. Sin ella el repositorio no pierde nada de lo ya bajado, pero **no puede incorporar
jurisprudencia nueva** de esas dos fuentes.

**La UMA es de la misma familia, y por eso se carga con navegador.** La consulta oficial de la
CSJN —`csjn.gov.ar/transparencia/uma`— es un **formulario de búsqueda**: lista las resoluciones
con su fecha y su número, y **el valor está adentro de cada PDF**, no en la página. Un cliente
HTTP no llega: con navegador, sí. **La serie está cargada** —22 vigencias, 01/10/2024 a
01/07/2026, leídas una por una de las resoluciones de la SGA el 18/09/2026— y el procedimiento
para extenderla está en el encabezado de `derecho/fuentes/datos/uma-csjn.csv`.

**Lo que no se levanta es la automatización:** no hay descargador ni lo va a haber, así que
mantener esa serie al día es trabajo de persona con navegador, igual que la jurisprudencia.

**Y la UMA porteña tiene una restricción más dura, que sí es definitiva.** Es otra unidad —art. 20
de la Ley 5.134, 1,5% de la remuneración total de un juez de la Ciudad— y su consulta oficial
publica **un solo valor, el vigente**, sin tabla ni buscador de resoluciones anteriores. Está
cargado el que publica, desde el 01/08/2026, y `uma_caba.py` **se planta para cualquier fecha
anterior**. Eso no es deuda: **la serie histórica no se puede reconstruir desde el organismo que la
fija**, así que una regulación porteña vieja se expresa en UMA y su equivalente en pesos se pide o
se marca. Las resoluciones anteriores circulan por el CPACF, que es quien las informa a las
Cámaras; incorporarlas exigiría cotejar cada una y anotar de dónde salió.

## El trabajo de fondo

No es un pendiente: es para qué existe el proyecto. Va acá porque ninguna herramienta lo
mide, no porque esté atrasado.

### Más derecho del que el plugin contiene

**El plugin tiene que contener mucho más derecho del que contiene.** Es el trabajo de fondo, no
mantenimiento: fueros nuevos, más normas bajadas y auditadas, más jurisprudencia leída. El
alcance enunciado es el derecho argentino y lo auditado es una fracción — la respuesta es
agrandar lo cubierto, nunca ablandar la disciplina ni recortar la promesa.
Un fuero nuevo entra entero o no entra: módulo con fuente primaria a la vista, normas bajadas por
el descargador, fallos **leídos** y su caso de prueba. Sin el caso, `pendientes.py` lo reporta
como módulo que ningún eval nombra, y tiene razón.
Y **ninguna herramienta dice qué falta**, porque todas miden contra lo declarado:
`cobertura_normativa.py` reporta la norma que un módulo cita y no bajamos, no la que ningún
módulo cita todavía. El orden en que crece se decide leyendo, y para eso está
[`docs/COBERTURA.md`](COBERTURA.md): una taxonomía traída de fuentes externas —CONEAU, el
Tesauro SAIJ, planes de estudio, institutos de los colegios y los fueros de Nación y PBA—
cruzada contra lo que el repositorio cubre. Es un mapa fechado para decidir el orden, **no un
enunciado de alcance**: el alcance sigue siendo el derecho argentino.

### La pieza que firma el órgano, en los fueros que todavía no tienen módulo

La skill trata al órgano como un modo de trabajo propio —se verifica en vez de producir, se
controla de oficio, no se construye estrategia— y eso **no tiene fuero**: vive en
`sede-judicial.md` 1.6 y le sirve a cualquier juez. Lo que sí tiene fuero es **la pieza que firma**,
y ahí la cobertura está repartida:

| Fuero | Módulo | Contra qué texto |
| --- | --- | --- |
| Laboral de la PBA | `sede-judicial-pba.md` | Leyes 11.653 y 15.057, Res. SC 1840/24, Const. PBA |
| Justicia nacional y federal, civil y laboral | `sede-judicial-nacional.md` 1.8 | CPCCN y Ley 18.345 |
| Contencioso administrativo y tributario de la Ciudad | `sede-judicial-caba.md` 1.9 | Ley 189 |
| **Penal —nacional, federal, PBA y porteño—** | **no hay** | |
| **Familia** | **no hay** | |
| **Cualquier otra provincia** | **no hay** | |

**Para los tres de abajo se dice y no se suple**, con `[SIN PERFIL DE ÁREA CARGADO: ...]`. El
`SKILL.md` 1.6 lo enuncia, `sede-judicial.md` lo repite en su borde y
`TestElModuloDeRolDiceDeQueFueroEs` exige que las dos secciones que rutean nombren el fuero. Eso
evita el error; no llena el hueco.

**Y hay un límite que los módulos escritos comparten: ninguno cita jurisprudencia.** Traen el
texto de la norma cotejado artículo por artículo, no su interpretación consolidada, así que el
alcance de la nulidad por falta de fundamentación sale marcado. Cerrarlo es leer fallos, que es
otra clase de trabajo.

Lo que falta bajar para avanzar: el régimen de **notificaciones electrónicas** de la justicia
nacional —acordadas de la CSJN— y del Poder Judicial de la Ciudad. Sin eso, desde cuándo corre un
plazo recursivo va con marcador en el módulo nacional y en el porteño.

### Lo que entra por adentro es un piso, no un techo

**De las materias que [`COBERTURA.md`](COBERTURA.md) mapeó, no queda ninguna sin nada escrito.**
Los fueros entraron con módulo propio; la mayoría de las materias, como sección de un módulo que
ya existía. Qué se le exige a una materia frente a un fuero está en
[`DESARROLLO.md`](DESARROLLO.md), bajo *Una rama entra por módulo o por sección*, y qué sección
cubre cada una lo lleva `herramientas/ramas-revisadas.json`, que un test verifica.

**Pero entrar por adentro sigue siendo un piso.** Una sección no tiene caso de prueba propio ni
nombre de rama en el ruteo, y su cobertura llega hasta donde llega la sección: cada una lleva su
marcador diciendo qué articulado no recorrió. Darle módulo propio a alguna sigue siendo una
decisión abierta, y el costo de hacerlo está más arriba, en *Más derecho del que el plugin
contiene*.

**Y las secciones nuevas comparten un hueco que es del trabajo de fondo: ninguna cita un fallo.**
Traen el texto de la norma cotejado, no su interpretación consolidada, y cada una lo dice en su
marcador de cierre. De la Justicia de Paz bonaerense no hay ni un fallo bajado, y sus dos
remisiones a normas derogadas —el art. 61 de la Ley 5.827 y el art. 144 del Código de Faltas—
no las resuelve ningún precedente cargado.

### Derecho internacional, más allá de los dos primeros capítulos

`dipr.md` 35 cubre los capítulos 1 y 2 del Título IV del Libro Sexto. **Queda el resto del
articulado** —y queda, sobre todo, lo que no está en el CCyCN: los tratados. El ADPIC ya mostró
el problema en su forma más pura, y está anotado en `propiedad-industrial.md` 40.6: **la ley
aprobatoria no transcribe el acuerdo**, así que tener la ley no es tener el texto.

**Eso valía para toda la materia, y en septiembre de 2026 dejó de valer para la mitad.** Están
bajados con su articulado los **Tratados de Montevideo de 1940** —`decreto-ley-7771-1956`, que trae
los cinco instrumentos—, el **Protocolo de Las Leñas** (Ley 24.578), el **Protocolo de Buenos
Aires** (Ley 24.669), la **Convención de Viena** sobre compraventa (Ley 22.765), la de **Nueva
York** sobre reconocimiento de laudos (Ley 23.619) y el **Convenio de La Haya de 1980** sobre
sustracción de menores (Ley 23.857), cuyo texto va como anexo de la ley aprobatoria.

**Lo que sigue faltando es la CIDIP**, que no tiene ninguna entrada, y **los instrumentos de
derechos humanos del art. 75 inc. 22**, que tienen su propia restricción más arriba: no hay
publicación oficial de los once en un solo documento. Para esos dos sigue en pie la pregunta de
fondo: **de dónde se bajan textos que InfoLEG no publica.**

---
Fuera del repo, en `~/develop/derecho-argentino-marca/`, vive el generador de la marca con su
propio README — la única parte con dependencias externas. El detalle, en
`docs/DESARROLLO.md § La marca`.
