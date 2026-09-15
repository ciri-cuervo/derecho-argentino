# Setup interview · derecho argentino

> Entrevista de configuración inicial. Responder una sola vez por estudio o abogado.
> El sistema usa las respuestas para generar el CLAUDE.md personalizado que se carga
> en las instrucciones del Project (Claude.ai) o en el perfil del plugin (Claude Code / Cowork).
>
> Tiempo estimado: 10 minutos.
> Las respuestas quedan guardadas en tu CLAUDE.md. Podés editarlas en cualquier momento
> o volver a correr la entrevista para regenerarlas.

---

## Cómo usar este archivo

**En Claude.ai (Projects):**
1. Crear un nuevo Project.
2. Pegar el contenido de este archivo en las instrucciones del sistema.
3. En el chat, escribir: "Corré la entrevista de configuración".
4. Responder las preguntas. Al terminar, pedirle al sistema que genere tu CLAUDE.md personalizado.
5. Reemplazar el contenido de las instrucciones del sistema con el CLAUDE.md generado.

**En Claude Code / Cowork:**
1. Instalar el plugin según las instrucciones del README.
2. Ejecutar `/argentina:setup` en la terminal.
3. Responder las preguntas. El sistema escribe el CLAUDE.md en
   `~/.claude/plugins/config/derecho-argentino/argentina/kb/project/CLAUDE.md`.

---

## Preguntas de la entrevista

El sistema hace estas preguntas en secuencia. Para cada una hay un ejemplo de respuesta
y una nota sobre el impacto en el comportamiento del sistema.

---

### Bloque 1 - Identidad profesional

**P1. Nombre del estudio o profesional**

Ejemplo: `Estudio Aboitiz Abogados` / `Dr. Juan Pérez, abogado`

Impacto: aparece en el encabezado de escritos y en el cierre de informes.

---

**P2. Matrícula y colegio**

Ejemplo: `CPACF T° XX F° XX` / `CALZ T° XX F° XX`

Impacto: el sistema incluye la matrícula en escritos donde corresponde. Si no querés que
aparezca en los borradores, indicá "no incluir en escritos".

---

**P3. Jurisdicción principal**

Indicar la jurisdicción donde tramitan la mayoría de las causas.

Opciones orientativas:
- CABA (fueros nacionales)
- PBA - indicar departamento judicial
- Otra provincia - indicar cuál
- Multijurisdiccional

Impacto: determina el código procesal que el sistema aplica por defecto sin preguntar
en cada sesión. Si trabajás en más de una jurisdicción, indicá el orden de prioridad.

---

**P4. Áreas de práctica**

Listar las áreas en orden de volumen de trabajo, de mayor a menor.

Ejemplo:
```
1. Laboral (trabajadores y empleadores)
2. Civil - daños y perjuicios
3. Societario
```

Impacto: el sistema carga los perfiles de área correspondientes con mayor prioridad
y sugiere los módulos relevantes en cada consulta.

---

### Bloque 2 - Configuración laboral

Responder solo si laboral figura entre las áreas de práctica.

---

**P5. Fuero laboral habitual**

Opciones: fuero nacional del trabajo (CABA) / fuero laboral PBA - [departamento judicial] / ambos / otro.

Impacto: el sistema aplica el código procesal correcto (Ley 18.345 vs. Ley 11.653)
y verifica el SECLO solo cuando corresponde al fuero nacional.

---

**P6. Rol predominante en causas laborales**

Opciones: trabajador / empleador / ambos (indicar proporción aproximada si la sabés).

Ejemplo: `Ambos, 70% trabajadores / 30% empleadores`

Impacto: el sistema activa el módulo de análisis estratégico correspondiente por defecto.
En cada sesión podés cambiarlo con una instrucción explícita.

---

**P7. CCTs más frecuentes**

Listar los convenios colectivos que aparecen con mayor frecuencia, con número si lo tenés.

Ejemplo:
```
- CCT 130/75 (comercio)
- CCT 389/04 (gastronómico)
- CCT 40/89 (construcción - UOCRA)
```

Si trabajás con múltiples CCTs sin uno predominante: `Variable - verificar en cada caso`.

Impacto: sin este dato, el sistema emite el marcador `[VERIFICAR CCT APLICABLE]`
en toda liquidación. Con los CCTs cargados, solo lo emite cuando el caso se sale de la lista.

---

### Bloque 2-bis - Configuración administrativa

Responder solo si derecho administrativo figura entre las áreas de práctica.

---

**P5-bis. Fuero administrativo habitual**

Opciones: contencioso administrativo federal (CABA) / CCAyT CABA / contencioso administrativo PBA - [departamento judicial] / combinación de los anteriores.

Impacto: el sistema aplica el código y los plazos del fuero indicado sin preguntar en cada sesión. El plazo de caducidad para accionar varía entre fueros (90 días hábiles judiciales en el federal, plazos distintos en CCAyT y PBA). Sin este dato, el sistema pregunta el fuero en cada consulta administrativa.

---

**P6-bis. Áreas dentro de administrativo**

Listar las áreas de mayor volumen dentro de la práctica administrativa, de mayor a menor.

Ejemplo:
```
1. Responsabilidad del Estado
2. Empleo público nacional
3. Contratación pública (obra pública)
```

Si la práctica administrativa es ocasional o de área única: indicarlo.

Impacto: el sistema prioriza la lógica de análisis correspondiente (vicios del acto, agotamiento de la vía, instancias recursivas, régimen de responsabilidad, sumario administrativo, etc.) según las áreas declaradas.

---

**P7-bis. Rol predominante en causas administrativas**

Opciones: actor (particular contra el Estado) / demandado (Estado o ente en defensa) / ambos (indicar proporción aproximada).

Ejemplo: `Predominantemente actor, 80% particulares contra organismos nacionales`

Impacto: el sistema activa el módulo de análisis estratégico correspondiente por defecto. En causas como actor: prioriza agotamiento de la vía, plazos de caducidad y requisitos de admisibilidad. En causas como demandado: prioriza análisis de vicios del acto, defensa de la regularidad del procedimiento y legitimidad del accionar estatal.

---

### Bloque 2-ter - Configuración medicina legal y pericia médica forense

Responder solo si medicina legal o pericia médica figura entre las áreas de práctica.

---

**P5-ter. Organismo o rol pericial**

Opciones: Cuerpo Médico Forense CSJN / Cuerpo Médico Forense del Poder Judicial de [Provincia] / Perito de parte / Consultor técnico / Combinación.

Impacto: el sistema adapta la estructura del informe y el punto de vista del análisis según el rol (perito oficial vs. perito de parte vs. consultor técnico).

---

**P6-ter. Fueros y especialidad principal**

Indicar los fueros en que se actúa habitualmente y la especialidad médica principal.

Ejemplo:
```
Fueros: penal (CPPN) y civil (CPCCN)
Especialidad: medicina legal general / traumatología forense / psiquiatría forense
```

Impacto: el sistema prioriza la normativa procesal y los criterios médico-legales correspondientes al fuero y la especialidad declarados. Sin este dato, pregunta el fuero en cada consulta pericial.

---

**P7-ter. Organismo requirente habitual**

Indicar el tribunal u organismo que requiere las pericias con mayor frecuencia.

Ejemplo:
```
Juzgado Nacional en lo Criminal y Correccional Federal N° X
Juzgado Nacional de Primera Instancia en lo Civil N° X
```

Impacto: el sistema aplica el baremo y los criterios de ese fuero por defecto y omite preguntar en cada sesión cuál es el tribunal requirente.

---

### Bloque 3 - Configuración societaria

Opciones: IGJ (CABA) / DPPJ (PBA) / ambas / otra provincia.

Impacto: el sistema aplica la normativa registral correcta en due diligence y constitución
de sociedades.

---

**P9. Tipo de operaciones societarias más frecuentes**

Ejemplo:
```
- Constitución de SAS y SRL para clientes PyME
- Due diligence en operaciones de compraventa de empresas medianas
- Pactos de accionistas
```

Impacto: el sistema prioriza los módulos de análisis correspondientes.

---

### Bloque 4 - Configuración tributaria

Responder solo si tributario figura entre las áreas de práctica.

---

**P10. Tributos y organismos más frecuentes**

Ejemplo:
```
- IVA y Ganancias ante AFIP
- Ingresos brutos CABA (AGIP)
- Litigio ante el TFN
```

Impacto: el sistema activa los módulos de verificación correspondientes y aplica
los plazos del fuero correcto.

---

### Bloque 5 - Configuración procesal general

---

**P11. Código procesal por defecto para causas civiles y comerciales**

Opciones: CPCCN (fueros nacionales) / CPCCBA / ambos (indicar cuál es principal).

Impacto: el sistema no equipara automáticamente plazos e institutos entre códigos.
Este dato evita preguntas repetitivas sobre el fuero en cada sesión.

---

**P12. ¿Actuás en fuero federal (contencioso administrativo federal, penal federal)?**

Sí / No / Ocasionalmente.

Impacto: si la respuesta es sí u ocasionalmente, el sistema activa el módulo federal
y verifica agotamiento de vía administrativa antes de analizar acciones judiciales.

---

### Bloque 6 - Estilo y documentos de referencia

---

**P13. Documentos semilla de la firma**

Listar los documentos que el sistema usará como referencia de estilo y criterio.
Estos son los más importantes para la calidad del output: el sistema aprende
el estilo de redacción de la firma leyendo estos modelos.

Ejemplos:
```
- Contrato de prestación de servicios profesionales estándar de la firma
- Modelo de NDA usado habitualmente
- Sentencia o resolución favorable representativa
- Escrito de demanda laboral tipo
```

Para cargarlos: adjuntarlos como archivos en el Project (Claude.ai) o incluirlos
en la carpeta `argentina/semilla/` del repo (Claude Code).

Si no tenés documentos para cargar ahora: indicá `Pendiente` y completarlo después.
El sistema funciona sin documentos semilla, pero la calidad de estilo mejora con ellos.

---

**P14. Preferencias de formato en escritos**

Indicar si tenés preferencias sobre:
- Tratamiento ("V.S." / "V.E." / "Su Señoría")
- Encabezado habitual
- Estructura de petitorio
- Cualquier convención interna de la firma

Si no tenés preferencias específicas: `Seguir convenciones estándar del fuero`.

---

**P15. ¿Querés que el sistema haga diagnóstico previo antes de modificar cualquier escrito aportado?**

Opciones: Sí, siempre / Solo en escritos de más de 500 palabras / No por defecto (activar por instrucción).

Impacto: cuando está activado, antes de modificar cualquier escrito el sistema entrega
un bloque de diagnóstico con argumentos sin norma de respaldo, hechos no acreditados,
citas no verificadas y contradicciones internas. Luego espera instrucción antes de proceder.

---

## Output de la entrevista

Al terminar de responder, el sistema genera un CLAUDE.md personalizado con:

1. Identidad y jurisdicción completadas con tus datos.
2. Normativa de referencia priorizada por tus áreas de práctica.
3. Configuración laboral (si aplica): fuero, rol y CCTs cargados.
4. Configuración administrativa (si aplica): fuero, áreas y rol (actor/demandado) cargados.
5. Configuración medicina legal (si aplica): organismo/rol pericial, fueros, especialidad y organismo requirente cargados.
6. Configuración societaria (si aplica): jurisdicción de inscripción y módulos activados.
7. Configuración tributaria (si aplica): tributos y fuero de litigio.
8. Documentos semilla referenciados (si los cargaste).
9. Preferencias de formato registradas.
10. Regla de diagnóstico previo configurada según tu respuesta.

El archivo generado reemplaza el CLAUDE.md genérico del repo. Podés editarlo
directamente o volver a correr la entrevista para regenerarlo.

---

## Actualización del perfil

El perfil no es estático. Actualizarlo cuando:

- Cambia la jurisdicción principal o se agrega un fuero nuevo.
- Se incorpora un área de práctica nueva.
- Cambia el CCT predominante en la cartera.
- Se agregan documentos semilla nuevos.
- Hay un cambio normativo relevante que afecta el perfil (el sistema también puede
  sugerir actualizaciones cuando detecta normas modificadas).

Para actualizar: editar el CLAUDE.md directamente, o correr `/argentina:setup --update`
en Claude Code para hacer solo las preguntas cuyas respuestas cambiaron.

---

*Última actualización: mayo 2026*
*Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)*
