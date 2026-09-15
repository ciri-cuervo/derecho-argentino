# Fallos de la CSJN verificados · índice

> Módulo de referencia de la skill `derecho-argentino`. Numeración global, sección 34.

---

## 34 · Leading cases de la Corte Suprema

Los 39 fallos de la CSJN que están **descargados en `fuentes/jurisprudencia/`**, con su hash de
procedencia. Para cada uno: la **carátula oficial**, la cita de la colección **Fallos** y la
**fecha**, todo tomado del registro de la Secretaría de Jurisprudencia — no de una fuente
secundaria.

**Para qué sirve este módulo.** Para saber qué precedente hay a mano y citarlo bien. Un fallo
descargado deja de estar alcanzado por la prohibición de la sección 2: pasa a ser material
verificado. **Verificado que existe y que dice lo que dice** — no que su texto extraído sea
transcribible, que es cosa aparte y está en 34.1. **Que esté verificado no significa que siga siendo buen derecho**, y por eso se
acompaña igual con `[VERIFICAR PRECEDENTE: ...]` antes de llevarlo a un escrito.

### 34.1 Cuáles se pueden transcribir y cuáles no

**Antes que nada: extraer siempre con `pdftotext -layout`.** Sin esa opción, el extractor
reordena las palabras de los PDF a dos columnas y **un documento sano parece roto**. Es el
diagnóstico falso más frecuente acá: cinco de estos fallos —"Góngora", "Buffoni", "Duarte", el de
reintegro de hijo y "Villamil"— se leen enteros con `-layout` y son perfectamente transcribibles.

**No hay regla por época.** Un PDF de 2013 puede extraerse mal y uno de 1984 puede estar limpio;
lo que decide es cómo se hizo la capa de texto, no cuándo. Antes de clasificar un fallo como
ilegible, reextraerlo con `-layout`.

Hay dos defectos reales, y el segundo es el que engaña:

| Estado | Qué le pasó al texto | Qué se puede hacer |
|---|---|---|
| **destruido** | El OCR no devolvió texto sino caracteres sueltos: `Considerando: 1*) ì BÊ`ì Que »`vêì segtin »Êµv`ì`. **`-layout` no lo arregla** | **Hay copia recuperada en `ocr/`.** Ver abajo |
| **sustituciones** | El OCR cambió letras y dejó **palabras válidas pero equivocadas**: *"apelanie remiten al andlisis de evestiones de hecho"*. **`-layout` tampoco**, porque el problema no está en el orden sino en las letras | El más peligroso: se lee natural y dice otra cosa. **Hay copia recuperada en `ocr/`**; igual se coteja cada cita contra el PDF |
| **layout** | Nada. Se lee entero **si se extrae con `-layout`** | Transcribible |
| **limpio** | Nada | Transcribible. Igual va con `[VERIFICAR PRECEDENTE: ...]` |

**Los seis con defecto real, confirmado por lectura:**

| Fallo | Estado del PDF |
|---|---|
| "Fiorentino" 306:1752 · "Bazterrica" 308:1392 · "Montalvo" 313:1333 | **destruido** |
| "Santa Coloma" 308:1160 · "Rodríguez Pereyra" 335:2333 · "S., D." 336:849 | **sustituciones** |

> **Estos seis tienen el texto recuperado en `fuentes/jurisprudencia/ocr/`.** Lo que estaba roto
> no era el papel sino la capa de texto que traía el PDF, hecha con un OCR de otra época, y
> `pdftotext` se limitaba a copiarla. Volver a leer las imágenes con tesseract la recupera: donde
> la capa vieja de "Bazterrica" daba `El] \^<+]Ky puede P^+*+y un ^Fy dia`, la página dice **"El
> sujeto puede un día probar la droga"**; y la frase que esta tabla usa como ejemplo de
> sustitución sale **"apelante remiten al análisis de cuestiones de hecho"**.
>
> Es una **derivación local, no una descarga**: cada archivo lleva el hash del PDF del que salió,
> la versión de la herramienta y la fecha, y **no es publicación oficial**. Sirve para leer y
> redactar; una cita literal a un escrito se coteja igual contra la página, que está numerada en
> el archivo. Se regenera con `python3 herramientas/reocr_jurisprudencia.py`. El OCR nuevo deja
> errores residuales visibles —"Orros" por "Otros", "demaudada" por "demandada"—: por eso el
> cotejo no es opcional.

**Y una cosa que NO es un defecto del documento.** En muchos fallos la **fecha** sale ilegible
—"Canales" la da como `Z 44 AA4-44,j49 de 2045`— porque está puesta a mano o con sello sobre el
escaneo, aunque el cuerpo se lea perfecto. Por eso la fecha de este módulo **sale del registro de
la Secretaría de Jurisprudencia y nunca del encabezado del PDF**.

Los tomos viejos tienen un segundo camino, y **es el que resolvió las tres fechas que faltaban**:
la fecha está **impresa en el cuerpo**, en la línea que sigue al título "FALLO DE LA CORTE
SUPREMA", que no es la del dictamen del Procurador —en "Fiorentino" el dictamen es del 21/5/1984 y
el fallo del 27/11/1984—. `herramientas/auditar_fechas_fallos.py` la lee de ahí y la compara contra
el manifiesto. Así se corrigieron, el 14/09/2026, tres fechas que estaban rellenadas con un 1 de
enero porque la capa de texto no se podía leer:

| Fallo | Decía | Es |
|---|---|---|
| "Fiorentino" 306:1752 | 1984-01-01 | **27/11/1984** |
| "Santa Coloma" 308:1160 | 1986-01-01 | **05/08/1986** |
| "Bazterrica" 308:1392 | 1986-01-01 | **29/08/1986** |

Con eso el auditor confirma **identidad en los 64** y ya no queda ningún fallo sin poder auditar.

> **Cómo se estableció esto.** No por regla ni por estimación: se midió lo que se puede medir y
> se leyó el resto. `herramientas/calidad_ocr.py` calcula la basura de caracteres, que es el
> único defecto que una medida detecta bien; los veredictos de lectura quedan en
> `herramientas/lecturas-ocr.json` con la fecha y lo que se vio. Se descartaron **cuatro**
> medidas automáticas que fallaban contra un caso conocido, y tres de ellas buscaban detectar
> la "mezcla" que después resultó no existir: estaban midiendo un fenómeno inventado.
>
> **Los 63 documentos están leídos**, uno por uno, cabecera y una franja del medio —el medio
> importa: "Santa Coloma" tiene la cabecera impecable y las sustituciones aparecen en el
> cuerpo—. Al 14/09/2026: **53 se transcriben sin más**, **4 piden `-layout`** y **6 tienen
> defecto real** —tres destruidos y tres con sustituciones—. Los seis tienen su copia recuperada
> en `ocr/`, así que **hoy hay texto legible de los 63**: 57 directo del PDF y 6 por relectura,
> éstos con cotejo obligatorio.
>
> Ese reparto cambió dos veces y las dos por leer, no por estimar. Primero, cinco documentos que
> parecían intranscribibles se leían con `-layout`. Después, "S., D." 336:849 estaba clasificado
> `layout` y en realidad tenía sustituciones —se descubrió al leerlo para escribir su holding—,
> así que pasó de 5 a 4 los que sólo piden `-layout` y de 5 a 6 los que tienen defecto real.

### 34.2 Penal y procesal penal

| Carátula oficial | Cita | Fecha | Archivo |
|---|---|---|---|
| **Fiorentino, Diego Enrique** | Fallos 306:1752 | 27/11/1984 | `csjn-fiorentino-fallos-306-1752` |
| **Bazterrica, Gustavo Mario — Alejandro Carlos Capalbo** | Fallos 308:1392 | 29/08/1986 | `csjn-bazterrica-fallos-308-1392` |
| **Montalvo, Ernesto Alfredo psa. inf. ley 20.771** | Fallos 313:1333 | 11/12/1990 | `csjn-montalvo-fallos-313-1333` |
| **Estévez, José Luis s/ solicitud de excarcelación** | Fallos 320:2105 | 03/10/1997 | `csjn-estevezjoseluis-fallos-320-2105` |
| **Nápoli, Erika Elizabeth y otros s/ infracción art. 139 bis CP** | Fallos 321:3630 | 22/12/1998 | `csjn-napolierikaelizabethyo-fallos-321-3630` |
| **Bianchi, Guillermo Oscar s/ defraudación** | Fallos 325:1404 | 27/06/2002 | `csjn-bianchiguillermooscar-fallos-325-1404` |
> **Cuidado con "Bianchi": hay dos y no tienen nada que ver.** El que está bajado es **"Bianchi,
> Guillermo Oscar s/ defraudación"**, Fallos 325:1404, **penal**. El que se cita en materia de
> **peaje y responsabilidad de concesionarias viales** es *"Bianchi, Isabel del Carmen Pereyra de
> c/ Provincia de Buenos Aires"*, del **7/11/2006**, que **no está en `fuentes/`** — aparece en
> `danos-indice-doctrinario.md` § 18-19 junto con "Colavita", "Bertinat" y "Ferreyra c/ VICOV".
> Buscar por apellido y tomar el primero que aparezca es, acá, citar un caso de defraudación para
> un accidente en una autopista.

| **Arancibia Clavel, Enrique Lautaro s/ homicidio calificado y asociación ilícita** | Fallos 327:3312 | 24/08/2004 | `csjn-arancibiaclavelenrique-fallos-327-3312` |
| **Verbitsky, Horacio s/ hábeas corpus** | Fallos 328:1146 | 03/05/2005 | `csjn-verbitskyhoracio-fallos-328-1146` |
| **Simón, Julio Héctor y otros s/ privación ilegítima de la libertad** | Fallos 328:2056 | 14/06/2005 | `csjn-simonjuliohectoryotros-fallos-328-2056` |
| **Casal, Matías Eugenio y otro s/ robo simple en grado de tentativa** | Fallos 328:3399 | 20/09/2005 | `csjn-casalmatiaseugenioyotr-fallos-328-3399` |
| **Maldonado, Daniel Enrique y otro s/ robo agravado** | Fallos 328:4343 | 07/12/2005 | `csjn-maldonadodanielenrique-fallos-328-4343` |
| **Minaglia, Mauro Omar y otra s/ infracción ley 23.737** | Fallos 330:3801 | 04/09/2007 | `csjn-minagliamauroomaryotra-fallos-330-3801` |
| **Larrabeiti Yáñez, Anatole Alejandro c/ Estado Nacional** | Fallos 330:4592 | 30/10/2007 | `csjn-larrabeitiyanezanatole-fallos-330-4592` |
| **Acosta, Alejandro Esteban s/ infracción art. 14, 1° párrafo, ley 23.737** | Fallos 331:858 | 23/04/2008 | `csjn-acostaalejandroesteban-fallos-331-858` |
| **Arriola, Sebastián y otros s/ causa n° 9080** | Fallos 332:1963 | 25/08/2009 | `csjn-arriolasebastianyotros-fallos-332-1963` |
| **Quaranta, José Carlos s/ inf. ley 23.737** | Fallos 333:1674 | 31/08/2010 | `csjn-quarantajosecarlos-fallos-333-1674` |
| **Góngora, Gabriel Arnaldo s/ causa n° 14.092** | Fallos 336:392 | 23/04/2013 | `csjn-gongora-fallos-336-392` |
| **Duarte, Felicia s/ recurso de casación** | Fallos 337:901 | 05/08/2014 | `csjn-duarte-fallos-337-901` |
| **Canales, Mariano Eduardo y otro s/ homicidio agravado — impugnación extraordinaria** | Fallos 342:697 | 02/05/2019 | `csjn-canales-fallos-342-697` |
| **P., S. M. y otro s/ homicidio simple** | Fallos 342:2389 | 26/12/2019 | `csjn-homicidio-simple-fallos-342-2389` |

**"Bianchi, Guillermo Oscar s/ defraudación"** (Fallos 325:1404, B. 66. XXXIV, 27/06/2002), leído
contra el documento el 14/09/2026. **Es el precedente de la CSJN sobre nulidades procesales**, y
hasta ahora era el único fallo bajado que ningún módulo citaba. La cámara había anulado la
declaración informativa de Bianchi (art. 236, 2ª parte, del Código de Procedimientos en Materia
Penal) porque no se lo había relevado expresamente del juramento prestado al ratificar la denuncia,
y lo había absuelto. La Corte **dejó sin efecto** esa decisión. **7 a 1**: Nazareno, Moliné
O'Connor, Belluscio, Boggiano, López, Bossert y Vázquez, con **Petracchi en disidencia**.

- **La doctrina** (cons. 7º): "en materia de nulidades procesales prima un criterio de
  interpretación restrictiva y **sólo cabe anular las actuaciones cuando el vicio afecte un derecho
  o interés legítimo y cause un perjuicio irreparable**, sin admitirlas cuando no existe una
  finalidad práctica, que es razón ineludible de su procedencia". "La nulidad por vicios formales
  carece de existencia autónoma dado el carácter accesorio e instrumental del derecho procesal":
  exige que el acto impugnado "tenga trascendencia sobre la garantía de la defensa en juicio o se
  traduzca en la restricción de algún otro derecho". Si no, la nulidad responde "a un **formalismo
  vacío**, en desmedro de la idea de justicia y de la pronta solución de las causas".
- **La distinción que lo hace útil** (cons. 10): "no debe confundirse el respeto a los recaudos que
  tienden a asegurar la protección del ejercicio de una garantía constitucional con la incolumidad
  de la garantía misma", porque suponer que una omisión formal que no afectó la libre determinación
  del imputado anula el acto "implicaría **convertir a los medios tendientes a proteger el ejercicio
  de aquella garantía en una garantía en sí misma**, con olvido del carácter meramente instrumental
  que tales medios revisten".
- **Cuándo sí se afecta la garantía** (cons. 9º): sólo si el imputado, por no haber sido informado
  de sus derechos, "hubiera confesado una conducta reprochable, susceptible de configurar una
  autoincriminación que conduzca a su condena en mérito a los hechos inconstitucionalmente
  admitidos".
- **Por qué se descalifica el fallo** (cons. 11): no precisó "cuál sería el agravio que la supuesta
  irregularidad habría ocasionado al imputado ni cuál habría sido el derecho o garantía que se
  habría visto impedido de ejercer" (con Fallos 298:373 y 301:177).

> **Errata del tomo, verificada.** En el cons. 9º el documento cita *"Miranda v. Arizona", 384 U.S.
> **463**, 1966*. La cita oficial de ese caso es **384 U.S. 436**: el tomo tiene los dígitos
> transpuestos. Quien copie la cita desde acá propaga el error; al citar "Miranda", corregirlo.

> **"Bazterrica" y "Montalvo" son el mismo debate y sentidos opuestos**, y conviene no
> confundirlos: en 1986 la Corte declaró inconstitucional la incriminación de la tenencia para
> consumo personal, en 1990 "Montalvo" volvió sobre sus pasos, y en 2009 "Arriola" retomó la
> línea de "Bazterrica". El material heredado los tenía etiquetados como si fueran el mismo
> fallo. Para el encuadre vigente, `penal.md` 24.9.2.

Los tres holdings que siguen se escribieron el 14/09/2026 **contra el texto recuperado en `ocr/`**,
porque la capa de texto de estos PDF está destruida. Las citas literales se cotejaron contra la
página; el número de página está en el archivo recuperado.

**"Fiorentino, Diego Enrique"** (Fallos 306:1752, 27/11/1984). No es de estupefacientes aunque la
condena lo fuera: es **el leading case de la inviolabilidad del domicilio y de la regla de
exclusión**. Detenido en el hall del edificio por una comisión de cuatro policías, Fiorentino
reconoció tener marihuana para consumo propio; con sus llaves la comisión entró al departamento
donde vivía con sus padres y secuestró el material del dormitorio. La Corte **dejó sin efecto la
condena** y, dato relevante para citarlo, dijo hacerlo apartándose "del criterio sustentado por el
Tribunal —en su anterior composición— al decidir la causa que se registra en Fallos: 301:676"
(cons. 4º).

- El art. 18 consagra "el derecho individual a la privacidad del domicilio de todo habitante
  —correlativo del principio general del art. 19— ... oponible a cualquier extraño, sea particular
  o funcionario público". Y aunque "no resulta exigencia del art. 18 que la orden de allanamiento
  emane de los jueces, **el principio es que sólo ellos pueden autorizar esa medida**" (cons. 5º).
- **El consentimiento no vale por el solo hecho de haberse dado.** El permiso "carecería de efectos
  por las circunstancias en que se prestó", habiendo sido el imputado "aprehendido e interrogado
  sorpresivamente por una comisión de cuatro hombres" y quedando detenido (cons. 6º).
- **Del silencio no se deduce consentimiento.** Exigir una resistencia verbal es "irrazonable", y
  derivar un consentimiento tácito de la falta de oposición "cuando ya se había consumado el
  ingreso de los extraños en la vivienda" es "carente de lógica": "esperar una actitud de
  resistencia en ese caso importaría reclamar una postura no exigible con arreglo a la conducta
  ordinaria de las personas" (cons. 6º).
- **Regla de exclusión.** Invalidado el registro, "igual suerte debe correr el secuestro", porque
  "la incautación del cuerpo del delito no es entonces sino el fruto de un procedimiento
  ilegítimo", y admitirlo "equivaldría a admitir la utilidad del empleo de medios ilícitos en la
  persecución penal"; hacerlo "compromete la buena administración de justicia al pretender
  constituirla en beneficiaria del hecho ilícito" (cons. 7º, con Fallos 46:36 y 303:1938).

**"Bazterrica, Gustavo Mario — Alejandro Carlos Capalbo"** (Fallos 308:1392, 29/08/1986). Declaró
la **inconstitucionalidad del art. 6º de la ley 20.771** en cuanto incriminaba la simple tenencia
para uso personal, y revocó la condena. **Se decidió 3 a 2**: Belluscio y Bacqué con el voto de
Petracchi —que votó según su propio voto, el más extenso—, y **Caballero y Fayt en disidencia**.
Citarlo como decisión unánime es citarlo mal.

- El art. 19 exige "que no se prohíba una conducta que se desarrolle dentro de la esfera privada
  entendida ésta no como la de las acciones que se realizan en la intimidad, protegidas por el
  art. 18, sino como aquéllas que no ofendan al orden o la moralidad pública, esto es, que no
  perjudiquen a terceros. **Las conductas del hombre que se dirijan sólo contra sí mismo, quedan
  fuera del ámbito de las prohibiciones**" (cons. 8º).
- Distingue "la ética privada de las personas, cuya transgresión está reservada por la Constitución
  al juicio de Dios, y la ética colectiva en la que aparecen custodiados bienes o intereses de
  terceros" (cons. 8º).
- **El problema es el peligro abstracto.** El art. 6º, "al prever una pena aplicable a un estado de
  cosas, y al castigar la mera creación de un riesgo", permite aludir "a perjuicios potenciales y
  peligros abstractos y no a daños concretos a terceros"; y "no está probado —aunque sí
  reiteradamente afirmado dogmáticamente— que la incriminación de la simple tenencia evite
  consecuencias negativas concretas" (cons. 9º).
- **La razón que cierra el fallo**: la prohibición constitucional de interferir con las conductas
  privadas "responde a una concepción según la cual **el Estado no debe imponer ideales de vida a
  los individuos, sino ofrecerles libertad para que ellos los elijan**, y ... es suficiente por sí
  misma para invalidar el art. 6º de la ley 20.771" (cons. 13).
- Trae además el argumento de la estigmatización: ante "su irremediable rotulación como
  delincuente, el individuo será empujado al accionar delictivo inducido por la propia ley", y "la
  función del derecho debería ser controlar o prevenir, sin estigmatizar" (cons. 12).

**"Montalvo, Ernesto Alfredo psa. inf. ley 20.771"** (Fallos 313:1333, 11/12/1990). **Volvió sobre
sus pasos**: rechazó la inconstitucionalidad del art. 6º de la ley 20.771 **y del art. 14, segunda
parte, de la ley 23.737** —que es la norma que sigue en juego— y confirmó la condena. Lo decidió la
Corte de nueve miembros, **7 a 2**, con Belluscio y Petracchi en disidencia: los dos que habían
formado la mayoría de "Bazterrica".

- Responde de frente al argumento de eficacia de "Bazterrica": allí "se dijo que no estaba probado
  que reprimir penalmente la tenencia de estupefacientes fuese un arbitrio eficiente para conjurar
  el problema de las drogas; pero lo cierto es que **la actitud permisiva de los últimos tiempos,
  lejos de disminuir el consumo, el tráfico y la actividad delictiva, ha coincidido con su
  preocupante incremento**" (cons. 26).
- Sostiene que el juicio de valor del legislador no es revisable acá: no advierte "el menor atisbo
  de irrazonabilidad o injusticia", y ese juicio "emana de un **mandato clamoroso de la
  comunidad**" (cons. 25).
- **Y la frase que define su alcance**: "la tenencia de estupefacientes, **cualquiera que fuese su
  cantidad**, es conducta punible en los términos del art. 14, segunda parte de la ley 23.737 y tal
  punición razonable no afecta ningún derecho reconocido por la Ley Fundamental, como no lo afecta
  tampoco la que reprime la tenencia de armas y explosivos" (cons. 27).

> **Cómo se cita esta línea sin equivocarse.** "Montalvo" es de 1990 y **"Arriola" (Fallos
> 332:1963, 25/8/2009) declaró la inconstitucionalidad del art. 14, segundo párrafo, de la ley
> 23.737** —el mismo texto que "Montalvo" llama "segunda parte"— aplicando el estándar de
> "Bazterrica": el alcance exacto, leído contra el documento, está en `penal.md` 24.9.2. O sea que
> **"Montalvo" ya no es el derecho vigente sobre el punto**: sirve para reconstruir la línea o para
> el período en que rigió, no para fundar una punición hoy. Y del otro lado, "Bazterrica" resolvió
> sobre el art. 6º de la ley 20.771, que "Montalvo" ya trata como ley anterior reemplazada por el
> art. 14 de la ley 23.737 (cons. 24). **La cita útil hoy es "Arriola"**; estos dos son su
> genealogía.

### 34.3 Laboral

| Carátula oficial | Cita | Fecha | Archivo |
|---|---|---|---|
| **Aquino, Isacio c/ Cargo Servicios Industriales S.A.** | Fallos 327:3753 | 21/09/2004 | `csjn-aquinoisacio-fallos-327-3753` |
| **Aróstegui, Pablo Martín c/ Omega ART S.A. y Pametal Peluso y Cía. S.R.L.** | Fallos 331:570 | 08/04/2008 | `csjn-arosteguipablomartin-fallos-331-570` |
| **Pogonza, Jonathan Jesús c/ Galeno ART S.A. s/ accidente — ley especial** | CNT 14604/2018/1/RH1 | 02/09/2021 | `csjn-pogonza-2021-09-02` |

**"Aquino"** (verificado contra el documento): la Cámara había declarado inconstitucional el
**art. 39 inc. 1 de la Ley 24.557** —que exime al empleador de responsabilidad civil frente al
trabajador, con la sola excepción del entonces art. 1072 del Código Civil— y condenado por el
derecho común; la Corte **confirmó la sentencia apelada** en cuanto fue materia de agravio.
Encuadre en `laboral.md` 5.8.

**"Aróstegui"** (verificado contra el documento): la Corte **dejó sin efecto** la sentencia que
había rechazado la reparación con base en el derecho común, y devolvió para nuevo
pronunciamiento. Se cita por el estándar de reparación y por el modo de cuantificar.

**"Pogonza, Jonathan Jesús c/ Galeno ART S.A."** (CNT 14604/2018/1/RH1, 02/09/2021), leído contra el
documento el 14/09/2026. **Es el fallo que valida la instancia administrativa previa ante las
comisiones médicas** de la Ley 27.348: la Corte **confirmó** la sentencia que había ordenado el
archivo por no estar cumplida esa instancia, o sea **rechazó el planteo de inconstitucionalidad**.
Firman Rosenkrantz, Highton y Maqueda; costas por su orden.

El armazón es **"Fernández Arias"**: atribuir competencia jurisdiccional a órganos administrativos
es válido si sus pronunciamientos quedan sujetos a **control judicial suficiente**, cuyo alcance "no
depende de reglas generales u omnicomprensivas" sino de "factores y circunstancias variables o
contingentes". Sobre eso, la Corte verifica cuatro recaudos:

- **Ley formal** (cons. 7º): las comisiones médicas fueron creadas por el art. 51 de la ley 24.241, y
  su competencia en riesgos del trabajo surge de los arts. 21 y 22 de la ley 24.557 y del art. 1º de
  la ley 27.348.
- **Independencia e imparcialidad** (cons. 8º), "a los efectos de la **materia específica y acotada**
  que el régimen de riesgos del trabajo les confiere": actúan en la órbita de la SRT, entidad
  autárquica, y la **Res. SRT 298/2017** manda que, cuando está controvertida la naturaleza laboral
  del accidente, intervenga un secretario técnico letrado con dictamen jurídico previo.
- **Finalidad razonable** (cons. 9º): el deber estatal del art. 14 bis CN comprende "la disposición
  de remedios apropiados y efectivos" para reparar los daños a la integridad física, la salud y la
  vida (con "Torrillo", Fallos 332:709, y "Ascua", Fallos 333:1361); el régimen es tarifado y busca
  "automaticidad y celeridad", lo que hace razonable una instancia administrativa previa.
- **Alcance de la revisión judicial** (cons. 10): se satisface con una instancia "en la que puedan
  **debatirse plenamente los hechos y el derecho aplicable**". Lo alinea con la Corte IDH: hay
  revisión suficiente cuando el juez examina todos los alegatos "sin declinar su competencia al
  resolverlos o al determinar los hechos", y **no la hay** si el órgano judicial "está impedido de
  determinar el objeto principal de la controversia" por considerarse limitado por las
  determinaciones del órgano administrativo ("Baena Ricardo y otros vs. Panamá", párr. 137;
  "Barbani Duarte y otros vs. Uruguay", párr. 204).

> **El dato que más se usa al litigar**, y está al final del fallo: pasar por las comisiones médicas
> "no impide que el damnificado pueda posteriormente reclamar con apoyo en esos otros sistemas de
> responsabilidad" (**art. 4º, cuarto párrafo, de la ley 26.773**, modificado por el art. 15 de la
> ley 27.348) — posibilidad que la ley 24.557 original había vedado, y que por eso cayó en
> **"Aquino"**. La instancia previa es un requisito de acceso, no una renuncia a la vía civil.

`[INSERTAR FALLO VERIFICADO: doctrina de la CSJN sobre las CONDICIONES de la opcion del art. 4 de la Ley 26.773 -momento, forma y efectos de la renuncia- que ninguno de los cargados desarrolla. "Pogonza" (2021) menciona ese articulo para decir que la instancia previa no cierra la via civil, y hasta ahi llega. Ver laboral.md 5.8.6 y el marcador de "Vera"]`

### 34.4 Civil y daños

| Carátula oficial | Cita | Fecha | Archivo |
|---|---|---|---|
| **Santa Coloma, Luis Federico y otros** | Fallos 308:1160 | 05/08/1986 | `csjn-santacoloma-fallos-308-1160` |
| **Mosca, Hugo Arnaldo c/ Provincia de Buenos Aires (Policía Bonaerense) y otros** | Fallos 330:563 | 06/03/2007 | `csjn-mosca-fallos-330-563` |
| **Cuello, Patricia Dorotea c/ Lucena, Pedro Antonio y otro** | Fallos 330:3483 | 07/08/2007 | `csjn-cuellopatriciadorotea-fallos-330-3483` |
| **Rodríguez Pereyra, Jorge Luis y otra c/ Ejército Argentino** | Fallos 335:2333 | 27/11/2012 | `csjn-rodriguezpereyrajorgel-fallos-335-2333` |
| **Buffoni, Osvaldo Omar c/ Castro, Ramiro Martín y otro** | Fallos 337:329 | 08/04/2014 | `csjn-buffoni-fallos-337-329` |
| **Villamil, Amelia Ana c/ Estado Nacional** | Fallos 340:345 | 28/03/2017 | `csjn-villamil-fallos-340-345` |
| **Vallejos, Julio César y otro c/ Hospital Interzonal Dr. José Penna y otros** | Fallos 344:1785 | 08/07/2021 | `csjn-vallejos-fallos-344-1785` |

**"Mosca"** (verificado contra el documento): hizo lugar a la demanda contra el club y la AFA
—condenándolos al pago— y **rechazó** la seguida contra la Provincia de Buenos Aires. Es el
precedente sobre responsabilidad del organizador de un espectáculo y sobre el alcance de la
responsabilidad del Estado por la actuación policial.

**"Cuello"** (verificado contra el documento): dejó sin efecto la decisión apelada, con votos
propios de Lorenzetti y Highton de Nolasco. Se lo cita en materia de **oponibilidad de la
franquicia** al damnificado, junto con "Buffoni". Encuadre en `civil.md` 6.5.

**"Buffoni"** (verificado contra el documento): **dejó sin efecto la sentencia apelada, con
costas**, y devolvió para nuevo pronunciamiento. Es el fallo que zanjó, del lado del contrato,
la discusión que "Cuello" había dejado abierta.

Los hechos importan porque el holding se apoya en ellos: la víctima y otro pasajero viajaban
**en la cajuela de un utilitario**, con tablones de madera a modo de asientos improvisados, sin
cinturones ni apoyacabezas, y **la póliza excluía específicamente** los daños a transportados en
esas condiciones. La Cámara había tenido la exclusión por inoponible apoyándose en el plenario
**"Obarrio"** y en la reforma de la Ley 26.361 a la Ley de Defensa del Consumidor.

Lo que resolvió la Corte, considerando por considerando:

| | |
|---|---|
| **9** | El contrato de seguro rige la relación entre los otorgantes (arts. 1137 y 1197 CC) y los damnificados son **terceros**: si quieren invocarlo, **deben circunscribirse a sus términos** (arts. 1195 y 1199 CC). Lo funda expresamente en el **voto del juez Lorenzetti en "Cuello"** — por eso los dos fallos van juntos |
| **10** | La **función social del seguro no implica** que deban repararse todos los daños sin consideración a las pautas del contrato, y menos cuando a los damnificados no podía pasarles inadvertido que viajaban en un lugar no habilitado |
| **12** | **La reforma de la Ley 26.361 a la LDC no altera el régimen del seguro**: una ley general posterior no deroga ni modifica, implícita ni tácitamente, la ley especial anterior ("Martínez de Costa", 9/12/2009) |
| **14** | **Demostrados los presupuestos fácticos y la existencia de la cláusula de exclusión, no hay razón legal para limitar los derechos de la aseguradora** |

**La regla operativa:** acreditada la exclusión de cobertura y sus presupuestos de hecho, **es
oponible al tercero damnificado**. Encuadre en `civil.md` 6.2.

> **Entonces "Cuello" y "Buffoni" no son dos posturas en pugna: son una línea.** "Cuello" (2007)
> dejó sin efecto con votos propios de Lorenzetti y Highton de Nolasco, y siete años después
> "Buffoni" adoptó el voto de Lorenzetti como fundamento de la mayoría. Lo que sigue siendo
> materia de sala es **cómo se aplica** —qué cuenta como presupuesto acreditado, y qué pasa con
> pólizas posteriores a la Res. SSN 34.225/09—, no si el contrato se le opone al tercero.
>
> El considerando 13 agrega una pauta interpretativa que conviene tener a mano aunque no fuera
> aplicable al caso por su fecha: **la Res. SSN 34.225/09**, que fija la cobertura mínima del
> art. 68 de la Ley 24.449, prevé que el asegurador **no indemniza** los daños a terceros
> transportados **en exceso de la capacidad del vehículo o en lugares no aptos**.

Los dos holdings que siguen se escribieron el 14/09/2026. Sus PDF tienen **sustituciones**, así que
se leyeron en la copia de `ocr/` y **cada cita se cotejó contra la página del PDF**.

**"Santa Coloma, Luis Federico y otros c/ E.F.A."** (Fallos 308:1160, 05/08/1986). Es **la raíz
constitucional de la reparación**. Un accidente ferroviario en Brandsen, el 8/3/1981, mató a tres
hermanas de 9, 10 y 13 años e hirió a un cuarto hijo; la cámara redujo la condena, negó todo daño
material a los padres y recortó el daño moral. La Corte **dejó sin efecto** la sentencia por
arbitraria. Firman **cuatro**: Belluscio, Fayt, Petracchi y Bacqué.

- **La frase por la que se lo cita** (cons. 7º): al fijar una suma cuyo carácter sancionatorio es
  "meramente nominal" y renunciar "en forma apriorística a mitigar de alguna manera —por imperfecta
  que sea— el dolor que dice comprender", la sentencia **"lesiona el principio del *alterum non
  laedere* que tiene raíz constitucional (art. 19, de la Ley Fundamental)"** y "ofende el sentido de
  justicia de la sociedad".
- **Chance** (cons. 4º): negar la indemnización por chance porque no puede asegurarse que del hecho
  resulte perjuicio "importa exigir una certidumbre extraña al concepto mismo de 'chance' de cuya
  reparación se trata". Y el apoyo económico que los hijos pueden dar "no se reduce a lo
  asistencial": en determinados medios se traduce en "la colaboración en la gestión del capital
  familiar".
- **Contra la tesis del daño moral como pena** (cons. 5º y 6º): si la cámara sostiene que lo punitivo
  es la única base del daño moral, y a la vez destaca la "notable negligencia" de la demandada y "el
  tremendo dolor" de los padres, entonces están reunidos todos los requisitos de su propia
  perspectiva y no aplicar la sanción "revela una evidente contradicción con las premisas
  aceptadas". Y es dogmático afirmar que el dolor "no es susceptible de ser aplacado, ni siquiera en
  grado mínimo, por la recepción de dinero": esa aserción "no intenta siquiera compatibilizarse" con
  los textos legales que relacionan la reparación con la obligación de resarcir.
- **El límite de la moral del juez** (cons. 8º): "no cabe que los jueces se guíen, al determinar el
  derecho, por patrones de moralidad que excedan los habitualmente admitidos por el sentimiento
  medio" —cita a Cardozo, *The nature of the judicial process*, pág. 106—, porque "la decisión
  judicial no ha de reemplazar las opciones éticas personales cuya autonomía también reconoce el
  art. 19". Imponer el renunciamiento de "soportar calladamente la pérdida de tres hijas" es algo
  que "no puede ser impuesto a los demás, sino solo libremente escogido por ellos".

> **Dos advertencias de transcripción, vistas en la página.** El tomo imprime **"alterum *nom*
> laedere"**, con *nom*: es errata del tomo, no del OCR, y quien transcriba literal va a copiarla.
> Unos renglones después imprime "en consonan a con lo consagrado", con letras faltantes. Para una
> cita textual a un escrito, corregir la errata evidente y citar la doctrina, no la tipografía.

**"Rodríguez Pereyra, Jorge Luis y otra c/ Ejército Argentino"** (Fallos 335:2333, R. 401. XLIII,
27/11/2012). Es **el fallo del control de constitucionalidad de oficio**. Un conscripto se
incapacitó cumpliendo el servicio militar obligatorio y reclamó por derecho común; la Corte
**declaró la inconstitucionalidad en el caso** del art. 76, inc. 3, ap. c, de la ley 19.101 —texto
ley 22.511— y confirmó el resto. Mayoría de Lorenzetti, Highton, Maqueda y Zaffaroni, **Fayt según
su voto**, y **Petracchi en disidencia** —adopta el dictamen de la Procuradora Fiscal y revoca—.

- **El argumento** (cons. 12): la jurisprudencia de la Corte IDH "no deja lugar a dudas de que los
  órganos judiciales de los países que han ratificado la Convención Americana ... están obligados a
  ejercer, **de oficio, el control de convencionalidad**" (cita, entre otros, "Fontevecchia y
  D'Amico vs. Argentina", 29/11/2011). Entonces **"resultaría un contrasentido"** que la
  Constitución, que le da rango constitucional a la Convención (art. 75, inc. 22) y habilita esa
  regla interpretativa, "impida, por otro lado, que esos mismos tribunales ejerzan similar examen
  con el fin de salvaguardar su supremacía frente a normas locales de menor rango".
- **Y los límites, que es la parte que se cita menos** (cons. 13): el control de oficio debe
  ejercerse "en el marco de sus respectivas competencias y de las regulaciones procesales
  correspondientes"; presupone un proceso ajustado a las reglas adjetivas, sobre todo las de
  competencia y las de admisibilidad y fundamentación; y **"la descalificación constitucional de un
  precepto normativo se encuentra supeditada a que en el pleito quede palmariamente demostrado que
  irroga a alguno de los contendientes un perjuicio concreto"**. "Cuanto mayor sea la claridad y el
  sustento fáctico y jurídico que exhiban las argumentaciones de las partes, mayores serán las
  posibilidades de que los jueces puedan decidir" la inconstitucionalidad. Reconocer la potestad
  "no significa invalidar el conjunto de reglas elaboradas por el Tribunal ... relativas a las
  demás condiciones, requisitos y alcances de dicho control".
- **Por qué cae la tarifa** (cons. 23): el régimen especial es insuficiente frente al daño que se
  propone reparar, y "no resulta razonable que una norma que tiene por objeto subsanar las
  consecuencias de la minusvalía provocada para 'el trabajo en la vida civil' prevea únicamente
  como pauta orientadora para la estimación del *quantum*" el haber de quien sólo se desempeña en
  las fuerzas armadas.
- **No hay doble indemnización** (cons. 24): haber percibido la tarifa única del art. 76 "no implica
  de por sí la admisión de una doble indemnización respecto del mismo rubro", porque las pautas
  difieren, y el monto percibido **se deduce** del que resulte del derecho común.

### 34.5 Familia

| Carátula oficial | Cita | Fecha | Archivo |
|---|---|---|---|
| **Winteker, Beatriz del Carmen c/ Vera, Benjamín Alcibíades y otra s/ violencia familiar (art. 1 Ley 12.569)** | Fallos 329:5514 | 28/11/2006 | `csjn-wintekerbeatrizdelcarm-fallos-329-5514` |
| **S., D. c/ R., L. M. s/ reintegro de hijo y alimentos** | Fallos 336:849 | 02/07/2013 | `csjn-reintegro-de-hijo-fallos-336-849` |
| **A. G. L. I. c/ R. M. G. H. s/ restitución internacional de menores** | Fallos 344:3078 | 28/10/2021 | `csjn-restitucion-internacional-fallos-344-3078` |
| **P. S., M. c/ S. M., M. V. s/ restitución internacional de menores de edad** | Fallos 345:358 | 24/05/2022 | `csjn-restitucion-internacional-fallos-345-358` |
| **D., H. C. y otros s/ guarda con fines de adopción — declaración de adoptabilidad** | Fallos 346:287 | 20/04/2023 | `csjn-guarda-adoptabilidad-fallos-346-287` |
| **M. S., M. G. c/ F., M. V. s/ restitución internacional de menores** | Fallos 347:1234 | 17/09/2024 | `csjn-restitucion-internacional-fallos-347-1234` |

**"Winteker"** (verificado contra el documento) es **una decisión de competencia**, de una sola
página: declaró competente al Juzgado Nacional de Primera Instancia en lo Civil n° 92 y lo hizo
saber al Juzgado de Paz Letrado de Ituzaingó. Citarla por otra cosa es citarla mal.

**"A. G., L. I. c/ R. M., G. H."** (Fallos 344:3078, CSJ 982/2021/CS1, 28/10/2021), leído contra
el documento. La SCBA había rechazado la restitución de dos niñas a Palafolls, Barcelona, por su
oposición a regresar (art. 13, penúltimo párrafo, del **CH 1980**). La Corte revocó y **hizo
lugar a la restitución** (art. 16, segunda parte, de la ley 48; costas por su orden).

Qué dice sobre la excepción por oposición del niño, que es para lo que sirve (cons. 3º):

- No alcanza cualquier negativa. Hace falta **una voluntad cualificada**: "no ha de consistir en
  una mera preferencia o negativa, sino en una verdadera oposición, entendida como un repudio
  genuino e irreductible a regresar".
- La excepción "exige la existencia de una situación delicada que exceda el natural padecimiento
  que puede ocasionar un cambio de lugar de residencia o la desarticulación de su grupo
  conviviente". "La mera invocación genérica del beneficio del niño, o los perjuicios que pueda
  aparejarle el cambio de ambiente o de idioma", **no bastan**.
- La integración al nuevo ambiente, o mantener la conexión afectiva con el círculo de pertenencia,
  "no constituye un motivo autónomo de oposición ni resulta decisivo para excusar el
  incumplimiento de la obligación internacional asumida, ceñida únicamente a evitar que se
  concreten sustracciones ilícitas en infracción al derecho de custodia de uno de los
  progenitores".
- Lo mismo con la preferencia por vivir con uno u otro progenitor, porque "no constituye objeto
  del proceso de restitución examinar lo atinente al cuidado personal": eso se decide en "la
  jurisdicción competente del país de residencia habitual".

Que las niñas fueran **oídas** —de manera directa por los magistrados de las tres instancias y por
profesionales especializados— y dijeran querer seguir viviendo en Bernal no configuró la
excepción: la Corte lo leyó como "una simple preferencia", y dejó a salvo que podrán ser oídas de
nuevo cuando se decida la custodia (cons. 5º). Y reafirmó que el objetivo del convenio es un
regreso **no sólo inmediato sino también seguro**: el magistrado a cargo determina "la forma, el
modo y las condiciones" del retorno, por las menos lesivas para las niñas (cons. 6º).

Los precedentes que encadena, según el propio fallo: para la voluntad cualificada, Fallos 333:604;
334:913; 335:1559; 336:97 y 458; 339:1742. Para que no basten el cambio de ambiente ni la
integración, Fallos 318:1269; 328:4511; 333:604 y 2396; 334:1445; 339:1763. Para el regreso
seguro, Fallos 339:1763 y 344:1757.

> **Un detalle del documento, antes de transcribir un considerando por su número.** Las dos
> extracciones —con `-layout` y sin— muestran los considerandos **1º, 2º, 3º, 5º y 6º**: no hay
> un 4º. Puede ser del original o de la copia bajada. Para citar "considerando 4º" de este fallo,
> cotejar antes contra la copia oficial.

**"P. S., M. c/ S. M., M. V."** (Fallos 345:358, CSJ 1003/2021/CS1 y CSJ 640/2021/RH1,
24/05/2022), leído contra el documento. **Es el fallo sobre violencia familiar y de género como
excepción de grave riesgo, y es el que más se cita mal.** El TSJ de Córdoba había rechazado la
restitución de una niña a México por tener configurado un escenario de violencia familiar, con
sustento además en el deber de juzgar los conflictos familiares transnacionales con perspectiva
de género. La Corte **revocó y admitió la restitución**, con medidas de retorno seguro.

Lo que resolvió, y es lo citable (cons. 8º):

- La violencia familiar o de género **no es una excepción distinta** de las que los convenios
  prevén taxativamente, "sino **una especie más del género 'grave riesgo'**".
- Quien la invoca "debe demostrar de forma ineludible, mediante prueba concreta, clara y
  contundente, que el efecto que aquella situación produce en el niño tras su restitución alcanza
  un **alto umbral de grave riesgo**".
- "La presunción, indicio y hasta la existencia misma de aquella situación no determina por sí
  sola la operatividad de la excepción en juego": lo que el convenio exige probar es el riesgo
  grave **para el niño y con motivo de la restitución**, y ese riesgo "deberá ser ponderado en
  forma **prospectiva**".
- Lo que decide el caso es la acreditación de ese riesgo "**y la ausencia de medidas de protección
  adecuadas y eficaces para eliminarlo, paliarlo o neutralizarlo** −circunstancia que hace que el
  regreso no sea seguro−, lo que sellará la suerte de la pretensión restitutoria".

Dos precisiones del mismo fallo que conviene tener a mano. Sobre el estándar de prueba, reitera
Fallos 339:1534 (cons. 11): "el simple temor, las sospechas o los miedos" no importan una
demostración que habilite la excepción, y las excepciones "son de carácter taxativo y deben ser
interpretadas de manera restrictiva" (cons. 7º, con Fallos 333:604 y 336:638). Y sobre el derecho
aplicable: el pedido se regía por la **Convención Interamericana sobre Restitución Internacional
de Menores** (ley 25.358), pero se resolvió con los criterios interpretativos del **CH 1980** (ley
23.857) "en virtud de que ambos convenios tienen idéntico propósito y contemplan semejantes
remedios básicos" (cons. 5º, con Fallos 334:1287, 341:1136 y 344:3078).

Cerró exhortando a los progenitores a cooperar en la ejecución y ratificando que las partes se
abstengan de exponer públicamente hechos de la vida de la niña, incluso por medios informáticos
(cons. 18).

**"M. S., M. G. c/ F., M. V."** (Fallos 347:1234, CSJ 1428/2023/RH1, 17/09/2024), leído contra el
documento. Ordenó la restitución de un niño a España. **Es un fallo per relationem y con
salvedades expresas**, así que hay que citarlo con cuidado: la Corte se remitió a los fundamentos
del dictamen del Procurador Fiscal **excluyendo** los últimos tres párrafos del apartado V, la
segunda cita del párrafo séptimo y la última parte del párrafo noveno de ese mismo apartado, y los
párrafos segundo y tercero del apartado VI (cons. 1º). Atribuirle a la Corte un fundamento que
esté en uno de esos pasajes es atribuirle lo contrario de lo que dijo.

De propio, la Corte sostuvo tres cosas (cons. 2º a 4º):

- Hay retención ilícita en los términos del **art. 3º del CH 1980**; no se configura la excepción
  de **grave riesgo** del art. 13, inc. b; y "las expresiones de I. que constan en autos no
  configuran una oposición con las características que debe reunir para encuadrar en la previsión
  del artículo 13, segundo párrafo" (con Fallos 336:97, 339:1763 y 344:3078).
- El peritaje ordenado como medida para mejor proveer refuerza la solución: el niño "cuenta con los
  recursos y mecanismos psicológicos necesarios para afrontar una situación de traslado".
- Reafirma el regreso "no solo inmediato sino también seguro", y que el magistrado a cargo
  determina "la forma y el modo" del retorno por lo menos lesivo (con Fallos 339:1763, 344:1757 y
  344:3078).

**"D., H. C. y otros"** (Fallos 346:287, CSJ 1645/2019/RH1, 20/04/2023), leído contra el documento.
No es de restitución: es **guarda con fines de adopción y declaración de adoptabilidad**. La Cámara
de Misiones había rechazado **in limine** la demanda conjunta de la madre biológica y el matrimonio
guardador —con quienes la niña convivía desde su nacimiento, el 1/9/2016—, ordenado el reintegro a
la familia de origen, y declarado que ni el tiempo transcurrido ni la guarda de hecho ni esa acción
podían computarse para una guarda con fines de adopción (art. 611 CCyCN). El STJ desestimó el
recurso por falta de sentencia definitiva. La Corte **dejó sin efecto** esa decisión y devolvió
para nuevo pronunciamiento.

**Lo primero, porque es lo que más se cita mal: la Corte no avaló la guarda de hecho.** Dijo, con
estas palabras, que dejar sin efecto el rechazo in limine "no importa admitir sin más la pretensión
de los guardadores, sino juzgar sobre la improcedencia de mantener una resolución desestimatoria"
(cons. 10). Y encomendó a los jueces de la causa evaluar, **previa declaración de adoptabilidad**,
la aptitud del matrimonio guardador —idoneidad que "aquí no ha sido controvertida ni puesta en
duda"— (cons. 11).

El resto de lo citable:

- El interés superior del niño no es un concepto abstracto: "no puede ser aprehendido ni entenderse
  satisfecho sino en la medida de las circunstancias comprobadas en cada asunto", y exige examinar
  las particularidades del caso y cómo se ven afectados sus derechos por la decisión cuestionada y
  por la que corresponda adoptar (cons. 6º, con Fallos 328:2870; 331:2047 y 2691; 341:1733;
  344:2647, 2669 y 2901; y 330:642).
- Las sentencias de la Corte "deben atender a las circunstancias existentes al tiempo de decidir la
  controversia, aun cuando fueran sobrevinientes a la interposición del remedio federal" (cons. 7º,
  con Fallos 316:1824; 321:865; 330:642; 344:449 y 2647).
- El apego a las formas tiene un límite: los jueces no deben omitir las consecuencias de su
  decisión "a fin de evitar que, so pena de un apego excesivo a las normas, se termine incurriendo
  en mayores daños que aquellos que se procuran evitar, minimizar o reparar" (cons. 9º, con Fallos
  326:3593; 328:4818 y 331:1262).
- **El paso del tiempo pesa.** Por motivos ajenos al niño, el tiempo transcurrido en los primeros
  años de vida "adquiere una consideración especial a la hora de definir el asunto" (cons. 9º).
- Hay que escuchar a la niña cuando la edad y la madurez lo permitan (cons. 11, arts. 12 CDN y 707
  CCyCN, con Fallos 344:2669).

Y una nota de método: la Corte entró al fondo aunque lo dicho hasta ahí conducía a descalificar la
sentencia local, "a fin de evitar que se prolongue aún más la adopción de una solución definitiva
acerca de la situación de la infante" (cons. 5º).

**"S., D. c/ R., L. M."** (Fallos 336:849, S. 977. XLVIII, 02/07/2013), leído contra las páginas
del PDF y no contra el texto extraído, por lo que se explica abajo. Es el más viejo de los cuatro y
**es donde están las fórmulas que después se repiten**. Confirmó la sentencia de la SCBA que había
ordenado la restitución de tres niñas a Corigliano Calabró, Cosenza, Italia: el traslado había sido
autorizado con fecha de regreso el 21/9/2008 y **la retención fue ilícita** por no haber retornado
(cons. 9º, con los arts. 155, 316, 317, 317 bis, 327 y 343 del Código Civil italiano, que le daban
al padre el ejercicio compartido de la responsabilidad parental).

Lo citable:

- **La opinión del niño.** Su ponderación "no pasa por indagar la voluntad de vivir con uno u otro
  de los progenitores", porque el convenio "no adhiere a una sumisión irrestricta respecto de los
  dichos del niño involucrado": la puerta del art. 13, penúltimo párrafo, "solo se abre frente a una
  **voluntad cualificada, que no ha de estar dirigida a la tenencia, sino al reintegro al país de
  residencia habitual**" (cons. 12).
- **El umbral del grave riesgo.** La excepción "solo procede cuando el traslado le configuraría un
  grado de perturbación **muy superior al impacto emocional que normalmente deriva de un cambio de
  lugar de residencia o la ruptura de la convivencia con uno de los padres**" (cons. 12).
- Que las niñas no quisieran regresar "bajo el cuidado de su padre" no es "una resistencia absoluta
  al retorno" ni "un repudio irreductible a regresar", y su adaptación a la vida en Argentina "no
  constituye un motivo autónomo de oposición" (cons. 12, con Fallos 318:1269; 328:4511 y 333:2396).
- **Restituir no es decidir la custodia.** Aun tomando en serio la gravedad de las declaraciones
  sobre comportamientos violentos del padre, "la decisión de restituir a las tres menores al lugar
  de residencia anterior al desplazamiento... no implica resolver que las niñas deberán retornar
  para convivir con su progenitor": el mérito para ejercer la guarda "no es materia de este proceso
  sino de las autoridades competentes del Estado de residencia habitual" (cons. 13).
- **El consentimiento del art. 13, inc. a, no se presume**: hacen falta "constancias claras y
  convincentes", y no las hay cuando el progenitor instó el retorno en todo momento (cons. 14).
- El proceso es "una solución de urgencia y provisoria", limitada a decidir si medió traslado o
  retención ilícita, sin extenderse al derecho de fondo (cons. 15, art. 16 CH 1980, con Fallos
  328:4511 y 333:604).
- **Qué se le puede pedir a la Autoridad Central.** Los cons. 16 y 17 son el mejor precedente para
  fundar un pedido concreto de retorno seguro: actuar coordinadamente con su par extranjera en
  función preventiva, arbitrando medios informativos, protectorios y de asistencia jurídica,
  financiera y social; poner en conocimiento del Estado requirente la urgencia de resolver custodia
  y visitas; y pedir un estricto seguimiento de las condiciones sociales, habitacionales y
  educativas después del retorno (art. 7º CH 1980, con Fallos 334:1287 y 1445). El cons. 18 exhorta
  al tribunal de familia a hacer la restitución "de la manera menos lesiva".

> **Este fallo se cita desde el PDF, no desde el texto extraído.** Estaba clasificado `layout` y en
> realidad tiene **sustituciones**: el extractor convierte la ñ en "ft" —"Seftaló", "niftas"—, "art."
> en "arto", "n° 1" en "nO 1", pierde acentos y parte palabras. Y en el encabezado degrada la
> propia identificación del expediente: donde el original dice **S. 977. XLVIII**, el texto
> extraído dice "S. 917. XLVIII", y el "c/" de la carátula sale como "el". El veredicto quedó
> corregido en `herramientas/lecturas-ocr.json` el 14/09/2026. Las citas de arriba se cotejaron
> contra las páginas 5 a 13 del PDF.

> **Las carátulas de familia vienen anonimizadas en el registro oficial**, y por eso los nombres
> de archivo de este bloque se armaron por materia y no por apellido. Al citar, se transcribe la
> carátula tal como figura arriba: no se reconstruye un nombre.

### 34.6 Salud, discapacidad y consumo

| Carátula oficial | Cita | Fecha | Archivo |
|---|---|---|---|
| **Cambiaso Peres de Nealón, Celia María Ana y otros c/ Centro de Educación Médica e Investigaciones Médicas s/ amparo** | Fallos 330:3725 | 28/08/2007 | `csjn-cambiasoperesdenealonc-fallos-330-3725` |
| **R. A., D. c/ Estado Nacional y otro s/ sumarísimo** | Fallos 330:3853 | 04/09/2007 | `csjn-reyes-aguilera-fallos-330-3853` |
| **ADDUC y otros c/ AySA SA y otro s/ proceso de conocimiento** | CAF 17990/2012/1/RH1 | 14/10/2021 | `csjn-adduc-aysa-2021-10-14` |

> **La carátula de "Cambiaso" se venía citando mal de dos maneras distintas.** El material
> heredado traía "Cambiaso Pereson", ya corregido allí una vez, y la corrección tampoco era
> exacta. La oficial es **"Cambiaso Peres de Nealón"**. Encuadre en `salud-discapacidad.md` 27.2.
>
> **"R. A., D."** es el fallo que circula como "Reyes Aguilera, Daniela": el registro oficial lo
> publica anonimizado. Se cita como figura arriba.

Los dos holdings que siguen se escribieron el 14/09/2026 leídos contra el documento. **De "ADDUC"
no hay holding acá porque ya está escrito en `consumidor.md` 17.4**, con la cita textual del
considerando 8º: es el fallo del que sale que el beneficio de justicia gratuita del art. 55 LDC
comprende las costas.

**"Cambiaso Peres de Nealón"** (Fallos 330:3725, C. 595. XLI, 28/08/2007). Confirmó el amparo que
había condenado a una **empresa de medicina prepaga** —CEMIC— a dar a un menor afiliado con
discapacidad, **"sin topes ni límites"**, la medicación psiquiátrica, 120 pañales descartables
mensuales y una silla de ruedas con arnés de tronco, apoya pies y sostén cefálico. **Se decidió 4 a
3**: Fayt, Maqueda, y Petracchi y Zaffaroni según sus votos; **Lorenzetti, Highton y Argibay en
disidencia**.

La cadena normativa que arma, que es para lo que se lo cita:

- El art. 1 de la **ley 24.754** obliga a las prepagas a cubrir "como mínimo ... las mismas
  prestaciones obligatorias dispuestas para las obras sociales" (cons. 4º).
- Y el art. 28 de la **ley 23.661** dice que ese programa de prestaciones **"se actualizará
  periódicamente"**. Con eso cae la defensa de la demandada, que sostenía que sólo le regía el PMO
  de la resolución 247/96 —el vigente cuando se sancionó la 24.754, en 1996— y no sus
  modificaciones posteriores: el art. 28 "descalifica esta defensa, toda vez que previó *expressis
  verbis*" la actualización (cons. 5º).
- La **ley 24.901** también alcanza a las prepagas por vía de la 24.754, porque "al no introducir
  salvedad alguna que la separe" de ese marco debe leerse comprendiéndolas, "a la luz del concepto
  amplio 'médico asistencial'" del art. 1 (cons. 6º).
- **La síntesis citable** (cons. 8º): las prepagas deben cubrir como mínimo lo mismo que las obras
  sociales, lo que comprende lo que la autoridad de aplicación establezca y actualice
  periódicamente (art. 28 ley 23.661), **todo lo que requiera la rehabilitación** de las personas
  con discapacidad, y las demás prestaciones de la ley 24.901 en cuanto conciernan al campo médico
  asistencial, más la cobertura de los medicamentos que esas prestaciones requieran.

Dos apoyos que conviene tener a mano. El art. 42 CN y los arts. 3 y 37 de la ley 24.240: la actora
está "situada como consumidora en una posición de **subordinación estructural**", y entre todos los
sentidos posibles hay que dar a la ley y al contrato "el que favorezca al consumidor" (cons. 7º, con
Fallos 324:677). Y el estatuto de la actividad: aunque tenga rasgos mercantiles, las prepagas
"**adquieren un compromiso social con sus usuarios**" que obsta a invocar cláusulas contractuales
"para apartarse de obligaciones impuestas por la ley", y la ley 24.754 "representa un instrumento al
que recurre el derecho a fin de equilibrar la medicina y la economía" (cons. 9º).

> **Hasta dónde llega.** El cons. 10 aclara el límite: si las prestaciones concretas reclamadas se
> adecuan a ese marco legal "es tema de hecho y prueba", ajeno a la instancia extraordinaria. El
> fallo fija el alcance de la obligación, no la lista de lo que hay que dar en cada caso.

**"R. A., D. c/ Estado Nacional"** (Fallos 330:3853, R. 350. XLI, 04/09/2007). Una joven boliviana
con **incapacidad congénita del 100 %** reclamó la pensión por invalidez del art. 9 de la ley 13.478;
se la negaron porque el art. 1.e del anexo I del **decreto 432/97** (texto originario) exigía a los
extranjeros **20 años de residencia**. La Corte revocó. **5 a 2**: Fayt y Zaffaroni, con Petracchi,
Maqueda y Argibay según sus votos; **Lorenzetti y Highton en disidencia**.

`[VERIFICAR VIGENCIA: art. 9 de la Ley 13.478, pension por invalidez - la ley es de 1948 e InfoLEG no publica normas de esa epoca; cotejar contra el Boletin Oficial de 1948 o contra el texto transcripto en el propio fallo, nunca contra una fuente secundaria]`

- **Primero desarma el argumento de la no justiciabilidad**, que es lo que había usado la cámara: el
  beneficio no deriva de la facultad de "dar pensiones" del art. 75.20 CN —las graciables— sino de
  la legislación de seguridad social del art. 75.12; la propia ley 24.241 las llama "prestaciones no
  contributivas" (art. 183), y **no es un "mero favor"** como la Corte había caracterizado a las
  graciables en "Ramos Mejía" (Fallos 192:260). Por eso "la no justiciabilidad predicada por el
  juzgador se vuelve ajena al *sub discussio*" (cons. 2º).
- **El núcleo** (cons. 7º): "por mayor que fuese el margen de apreciación que corresponda dispensar
  al legislador o reglamentador", sumar a esos requisitos un lapso de residencia de 20 años —"**aun
  cuando también rigiera en igual medida para los argentinos, incluso nativos**"— implica, "**puesto
  que la subsistencia no puede esperar**, un liso y llano desconocimiento del derecho a la seguridad
  social", en grado tal que compromete el derecho a la vida, cuya garantía mediante "acciones
  positivas" es una "obligación impostergable" (con "Campodónico de Beviacqua", Fallos 323:3229,
  cons. 15 y 16).
- Se apoya en la Corte IDH, "Niños de la Calle" (Villagrán Morales, 19/11/1999, párr. 144): el
  derecho a la vida comprende "el derecho a que no se le impida el acceso a las condiciones que le
  garanticen una existencia digna"; y en "Vizzotti" (Fallos 327:3677, cons. 8): la Constitución
  reconoce derechos "para que éstos resulten efectivos y no ilusorios" (cons. 8º).
- Y lee la seguridad social de las personas con discapacidad con la Observación General N° 5 del
  Comité de DESC y las Normas Uniformes de la resolución 48/96 de la Asamblea General de la ONU
  (cons. 6º).

> **El alcance es más preciso de lo que suele citarse.** La Corte no fulminó el decreto: dijo que el
> recaudo de residencia del art. 1.e "resulta **inaplicable, por inconstitucional, en los casos en
> que se encuentren reunidos todos y cada uno de los restantes requisitos**" para acceder a la
> prestación. Es una inconstitucionalidad **en el caso** y condicionada al cumplimiento del resto
> del régimen, no una derogación general del requisito.

### 34.7 Las nueve citas que no tienen documento

Aparecen en el material heredado pero **el buscador de la Secretaría no devuelve un documento
descargable** para ellas. No se les inventa URL: van con marcador hasta que se resuelvan por otra
vía —el tomo impreso, o `sjservicios.csjn.gov.ar/sj/verTomo`, según `fuentes/jurisprudencia/INDICE.md`,
con las tres limitaciones que ese archivo describe—.

**Lo que importa no es que falten, sino en qué rol se usan.** Medido el 14/09/2026 sobre SKILL.md y
los 30 módulos: **ninguna de las nueve se cita como autoridad propia**. Las cuatro que están en
juego se citan **a través de un fallo que sí está bajado y leído**, que es el modo correcto, y
cuatro no las usa nadie.

| Cita | Cómo se usa hoy |
|---|---|
| **308:733** "Rayford" | En `penal.md` 24.5, como la regla que **"Quaranta"** *toma* de ese fallo. Verificado: el documento de "Quaranta" lo nombra con su cita en los cons. 18 y 22 |
| **310:1847** "Ruiz" · **317:1985** "Daray" | Ídem: la línea que "Quaranta" reitera, y su propio texto las cita |
| **303:1938** | Dentro del razonamiento de **"Fiorentino"** (cons. 7º), que sí está bajado: es la Corte citándose a sí misma |
| **306:1409** | Sólo en `danos-indice-doctrinario.md`, que es el índice de una obra comercial: ahí figura como *"Sánchez Granel c. DNV"*. **Carátula de fuente secundaria**, sin verificar |
| **311:1337** · **321:1328** · **312:201** · **343:1691** | **Ningún módulo las usa.** Quedan como registro de lo que citaba el material heredado |

O sea que **el riesgo operativo es cero**: la skill no puede citar como propia una doctrina que no
tiene documento, porque en los cuatro casos vivos la cita viaja dentro de un fallo verificado y se
atribuye así. Bajar los tomos sigue siendo deseable —para poder transcribir "Rayford" en vez de
referirlo por "Quaranta"—, pero no es una deuda de integridad.

De **312:201** y **343:1691** el buscador directamente no devolvió resultados, y no las usa ningún
módulo: antes de darlas por existentes hay que cotejar la cita, que puede estar mal en el material
heredado.

`[VERIFICAR CITA DE FALLOS: Fallos 312:201 y 343:1691 - el buscador de la Secretaria de Jurisprudencia no devuelve resultados para esas dos citas. Cotejar tomo y pagina antes de usarlas]`

### 34.8 Estado de los holdings

**Con holding leído contra el documento: 39. Sin holding: 0.**

Los 39 fallos con documento tienen su doctrina escrita contra el documento, no contra un resumen.
El último tramo se cerró el **14/09/2026**: los cinco de familia (34.5), los tres de penal que
estaban trabados por el OCR (34.2), los dos de salud (34.6) y los cuatro que quedaban sueltos
—"Bianchi" en 34.2, "Pogonza" en 34.3, "Santa Coloma" y "Rodríguez Pereyra" en 34.4—.

Que estén escritos **no los hace vigentes**: cada uno se lleva a un escrito con
`[VERIFICAR PRECEDENTE: ...]`, y tres de ellos tienen advertencias propias que hay que leer antes de
citarlos —el par "Bazterrica"/"Montalvo" frente a "Arriola", la errata de la cita de "Miranda" en
"Bianchi", y la de *alterum nom laedere* en "Santa Coloma"—.

**Dónde vive cada holding.** El de "ADDUC" está en `consumidor.md` 17.4. Once de los de penal están
en `penal.md`, cada uno en la sección donde se usa: "Acosta" en 24.4.3, "Arancibia Clavel" en
24.4.2, "Nápoli" y "Estévez" en 24.3.2, "Quaranta" y "Minaglia" en 24.5, "Casal" en 24.6.3,
"Canales" en 24.6.4, "Verbitsky" en 24.8, "Maldonado" en 24.7.8 y "Arriola" en 24.9 —con el alcance
exacto de la declaración de inconstitucionalidad del art. 14 segundo párrafo, que es lo que se cita
mal—. El resto está en este módulo, en la sección de su materia.

**Lo que falta ahora es otra cosa**: no holdings, sino doctrina sin precedente propio en el repo.
Está señalada con marcadores `[INSERTAR FALLO VERIFICADO: ...]` —en 34.3, `civil.md`, `familia.md`,
`laboral.md`, `penal.md`, `societario.md` y `notificaciones-pba.md`— y con las nueve citas de 34.7,
que **no son una deuda de integridad**: ahí está medido por qué.

**De los 39, 37 se citan desde algún módulo.** Los dos que no: "Bianchi" 325:1404 —ver la
advertencia de 34.2 sobre los dos Bianchi— y "Fiorentino" 306:1752, que sólo aparece nombrado
por el estado de su OCR.

**Once de los de penal no tienen su desarrollo acá sino en `penal.md`**, cada uno en la sección
donde se usa: "Acosta" en 24.4.3, "Arancibia Clavel" en 24.4.2, "Nápoli" y "Estévez" en 24.3.2,
"Quaranta" y "Minaglia" en 24.5, "Casal" en 24.6.3, "Canales" en 24.6.4, "Verbitsky" en 24.8,
"Maldonado" en 24.7.8 y "Arriola" en 24.9 —con el alcance exacto de la declaración de
inconstitucionalidad del art. 14 segundo párrafo, que es lo que se cita mal—. El índice dice qué
hay; el módulo dice qué hacer con eso.

Los 39 están **descargados, hasheados, con carátula, cita y fecha confirmadas, y con la doctrina
escrita contra el documento**. Para lo que no está acá —los institutos con
`[INSERTAR FALLO VERIFICADO: ...]`— sigue sirviendo de orientación el material de `kb/doctrina/`,
con la advertencia de siempre: **no pasó auditoría**, y su carátula y su fecha ya se corrigieron
acá en varios casos. Lo que manda es la tabla de este módulo.

---

> **Al citar cualquiera de estos fallos**, acompañar con `[VERIFICAR PRECEDENTE: ...]`: estar
> descargado prueba que el fallo existe y dice lo que dice, no que siga siendo buen derecho.
