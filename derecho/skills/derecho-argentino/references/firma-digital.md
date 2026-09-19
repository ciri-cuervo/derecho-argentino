# Firma digital y documento electrónico · Ley 25.506

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

Cotejado contra `fuentes/normas/ley-25506.txt`.

**Es transversal:** sostiene el expediente digital de `notificaciones-pba.md` 22, la prueba del
telegrama y del correo de `telegramas.md` 25, y cualquier documento que llegue en soporte
electrónico a un escrito.

## 52 · Firma digital, firma electrónica y documento digital

### 52.1 Firma digital y firma electrónica no son lo mismo, y la diferencia es la carga de la prueba

| | Firma digital | Firma electrónica |
| --- | --- | --- |
| Qué es | Resultado de aplicar al documento **un procedimiento matemático** con información de exclusivo conocimiento y control del firmante, **susceptible de verificación** por terceras partes (art. 2) | Conjunto de datos electrónicos usado por el signatario como medio de identificación **al que le falta alguno de los requisitos legales** para ser digital (art. 5) |
| Autoría | **Se presume** del titular del certificado, salvo prueba en contrario (art. 7) | **No hay presunción**: el art. 5 pone la carga de probarla en quien la invoca |
| Integridad | **Se presume** si la verificación da verdadero (art. 8) | — |

**Ésa es toda la materia en una tabla.** Llamar «firma digital» a un PDF firmado con una imagen
escaneada, o a un clic de aceptación, invierte la carga de la prueba en contra del que lo invoca.

### 52.2 Las tres equivalencias que hacen funcionar el expediente digital

1. **Firma manuscrita (art. 3):** cuando la ley requiere firma manuscrita, **esa exigencia también
   se satisface con firma digital**, incluso donde la ley prescribe consecuencias por su ausencia.
2. **Escritura (art. 6):** el **documento digital** —la representación digital de actos o hechos,
   con independencia del soporte— **satisface el requerimiento de escritura**.
3. **Remitente (art. 10, texto Ley 27.446):** si un documento electrónico está firmado por un
   **certificado de aplicación**, se presume que proviene del titular del certificado.

**El art. 6 es el que se usa sin nombrarlo** cada vez que se acompaña un documento electrónico como
prueba: es lo que permite tratarlo como escrito y no como indicio.

### 52.3 Lo que el módulo no puede afirmar sin más

**El art. 4 está DEROGADO** por la ley que su propia nota indica en el texto consolidado — era el
que excluía ciertos actos del ámbito de la firma digital. **No se cita como vigente**, y la
exclusión de un acto hay que buscarla en el régimen que corresponda, no ahí.

`[REVISIÓN NORMATIVA REQUERIDA: el art. 4 de la Ley 25.506 está derogado y el art. 10 lleva texto según la Ley 27.446. Antes de sostener que un acto queda fuera del régimen de firma digital, cotejar el texto consolidado de fuentes/normas/ley-25506.txt y no doctrina anterior a esas reformas]`

### 52.4 Lo que este módulo NO hace

- **No trae la reglamentación** de la Ley 25.506, que vive en otra ficha de InfoLEG y **no está
  bajada**: de ella salen los requisitos del certificado, los certificadores licenciados y la
  autoridad de aplicación.
- **No cubre el expediente judicial electrónico** de cada jurisdicción, que se rige por acordadas:
  para PBA, `notificaciones-pba.md` 22.
- **No cubre la prueba informática ni la pericia**, que va por `prueba-pericial.md` 20.
- **No cubre los delitos informáticos.** La Ley 26.388 no tiene entrada propia porque **sólo
  modifica el Código Penal**, y el consolidado de `fuentes/normas/cp-11179.txt` ya la
  incorpora: sus artículos llevan la nota de esa ley. El encuadre penal va por `penal.md` 24.
- **No calcula.**

#### 52.4 bis Contratación por canal electrónico — precedente leído, y hasta dónde llega

**Precedente leído.** *Banco de la Provincia de Buenos Aires c/ Beltrame Guadalupe Milagros s/
Cobro sumario sumas dinero*, **Cámara Segunda de Apelación en lo Civil y Comercial de La Plata,
Sala Primera**, causa **135587**, **19/12/2023**, voto de Sosa Aubone. Texto completo bajado desde
JUBA en `fuentes/jurisprudencia/`.

**Qué revoca.** La primera instancia había rechazado tres préstamos tramitados por home banking y
por cajero automático, razonando que pulsar *"aceptar"* o usar el cajero **no puede asimilarse a
una firma digital ni electrónica**. La Cámara lo descarta: ese razonamiento *"esta desconociendo la
normativa que regula la materia, y llevaría a invalidar la gran mayoría de los contratos que se
realizan hoy en día"*.

**Los dos apoyos normativos que usa**, y sirven para armar el escrito:

- **Art. 1106 CCyCN**: cuando la ley exige que el contrato conste por escrito, el requisito **se
  satisface** si el contrato con el consumidor *"contiene soporte electrónico u otra tecnología
  similar"*.
- **La tuitiva no se lee al revés.** El orden público del art. 65 y la presunción a favor del
  consumidor de los arts. 3 y 37 de la Ley 24.240 *"no se puede interpretarse en contra de los
  consumidores para limitar su actuación a lo presencial o al papel"*.

> **El límite del precedente, que es lo que hay que mirar antes de citarlo.** La Cámara razona
> sobre contratos que **no fueron negados** y sobre una firma electrónica cuya **autoría e
> integridad no se cuestionaron** —hubo rebeldía y operó el reconocimiento del art. 354 inc. 1
> CPCCBA—. **No resuelve el caso del desconocimiento**, que es justamente donde el art. 5 pone la
> carga sobre quien invoca la firma. Citarlo para un caso contradicho es pedirle lo que no dice.

`[VERIFICAR PRECEDENTE: «Beltrame», Cámara Segunda de La Plata Sala Primera, causa 135587, 19/12/2023 - es doctrina de Cámara departamental: cotejar el criterio del departamento judicial del caso]`

`[INSERTAR FALLO VERIFICADO: firma electrónica DESCONOCIDA - quién prueba qué cuando el atribuido la niega, art. 5 in fine de la Ley 25.506, y el alcance de la presunción del art. 10 - JUBA tiene sumarios en punto -entre otros «Afluenta c/ Celentano Acevedo», CC0002 LM, 08/06/2022, y «Banco de Galicia c/ Zamora», CC0002 SM, 16/04/2025- pero SIN texto completo publicado: un sumario no cierra este marcador]`

### 52.5 Qué preguntar antes de contestar

1. **Qué firma tiene el documento**, porque de eso depende quién prueba qué.
2. **Si hay certificado digital y de qué certificador**, por las presunciones de los arts. 7 y 8.
3. **Si la ley exigía firma manuscrita para ese acto**, por la equivalencia del art. 3.
4. **Si la contraria desconoció el documento**, y con qué alcance.
5. **Si se pretende excluir el acto del régimen**, para no apoyarse en el art. 4 derogado.
