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

### Los reclamos de faltante que no nombran una norma

**El control cruza el párrafo contra dos catálogos** —normas por número y jurisprudencia por el
apellido de la carátula— **y lo que queda afuera lo dice su propia salida:**
`python3 herramientas/deuda_vencida.py --sin-cruzar`. No copies la cifra acá: la mide el comando.

**Lo que queda es una sola clase, y no tiene contra qué cruzarse:** la categoría en vez de la
norma —"su ley arancelaria local", "los estatutos locales", "las acordadas de la CSJN", "la
reglamentación del BCRA"—. Lo que falta es un conjunto abierto, no una pieza, así que **no
existe una entrada de catálogo que nombrar**. Se lee. Por lo mismo no pide una convención nueva
en `references/marcadores.md`: nombrar el slug no sirve cuando no hay un slug.

**Las series de `fuentes/datos/` se midieron y la medida se descartó.** Derivar el índice de los
nombres de archivo dispara cuatro veces sobre el árbol y **las cuatro equivocado**: «la serie de
la UMA porteña no está cargada» engancha con `uma-csjn.csv`, que es la nacional, y «acordadas de
la CSJN» engancha con el `csjn` de ese mismo archivo. Y no alcanza a ninguno de los tres
reclamos de serie que sí existen, porque dicen "la serie de valores" sin nombrarla. Medido el
17/09/2026. Una medida que se equivoca sobre un caso conocido no sirve para los desconocidos: se
descarta, no se calibra.

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

### La justicia de paz de PBA, que es lo último del catálogo sin escribir

De las materias que [`COBERTURA.md`](COBERTURA.md) mapeó y el repositorio no cubría, **queda una
sola sin nada escrito**. Las demás entraron como sección de un módulo que ya existía, con su norma
cotejada y su disparador; qué se le exige a una materia frente a un fuero está en
[`DESARROLLO.md`](DESARROLLO.md), bajo *Una rama entra por módulo o por sección*, y qué sección
cubre cada una lo lleva `herramientas/ramas-revisadas.json`, que un test verifica.

**Entrar por adentro es un piso, no un techo.** Una sección no tiene caso de prueba propio ni
nombre de rama en el ruteo, y su cobertura llega hasta donde llega la sección: cada una lleva su
marcador diciendo qué articulado no recorrió. Darle módulo propio a alguna sigue siendo una
decisión abierta, y el costo de hacerlo está más arriba, en *Más derecho del que el plugin
contiene*.

### Derecho internacional, más allá de los dos primeros capítulos

`dipr.md` 35 cubre los capítulos 1 y 2 del Título IV del Libro Sexto. **Queda el resto del
articulado** —y queda, sobre todo, lo que no está en el CCyCN: los tratados. El ADPIC ya mostró
el problema en su forma más pura, y está anotado en `propiedad-industrial.md` 40.6: **la ley
aprobatoria no transcribe el acuerdo**, así que tener la ley no es tener el texto.

**Eso vale para toda la materia:** los tratados de derechos humanos del art. 75 inc. 22, los de
Montevideo, la CIDIP, el Protocolo de Buenos Aires y los convenios de La Haya se citan a diario y
**ninguno está en `fuentes/`** como articulado. Ampliar derecho internacional es, antes que
escribir módulos, **resolver de dónde se bajan textos que InfoLEG no publica**.

---
Fuera del repo, en `~/develop/derecho-argentino-marca/`, vive el generador de la marca con su
propio README — la única parte con dependencias externas. El detalle, en
`docs/DESARROLLO.md § La marca`.
