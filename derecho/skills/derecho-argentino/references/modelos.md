# Modelos de escritos del repo · mapa y criterio de uso

> Módulo de referencia de la skill `derecho-argentino`. Numeración global: las remisiones cruzadas
> entre módulos siguen siendo válidas. **Rigen las reglas de integridad de la sección 2 del
> SKILL.md.**

---

## 23 · Modelos de escritos

`escritos.md` (secciones 9 a 11) tiene el **método**: cómo diagnosticar un escrito aportado,
cómo armar uno desde cero y cuál es el criterio de salida. Este módulo tiene el **inventario**:
34 modelos y siete guías de armado por rama que están en el repo y que, sin esta
tabla, no se encuentran.

**Cuándo abrirlo.** Antes de redactar un escrito desde cero, siempre — no para copiarlo, sino
para no omitir un acápite que el modelo prevé. Después de haber leído el módulo de la rama, no
antes: el modelo da la estructura, no el encuadre.

### 23.1 Cómo se usa un modelo — y cómo no

1. **El modelo es estructura, no contenido.** Da el orden de los acápites, los rubros que no se
   pueden olvidar y el articulado de entrada. Los hechos, las normas verificadas y el petitorio
   salen del caso, no del archivo.
2. **Las reglas de la sección 2 rigen sobre el modelo.** Si el modelo trae una cita, una tasa o
   un plazo, se verifica igual que si lo hubiera dicho la skill. Un modelo con una norma
   derogada adentro es exactamente el riesgo que estos archivos introducen.
3. **La precedencia de la sección 15 también rige acá**, y estos archivos están en el escalón
   más bajo: fuente primaria → esta skill → docs del Project → material del repo.
4. **La calidad es despareja.** Los de familia, penal y previsional siguen las convenciones de
   salida de la sección 11 —guion corto, comillas rectas, cierre con "Estado del escrito"—. Los
   de civil, consumo y tránsito son de una consolidación anterior y traen notas de uso en prosa
   larga, con separadores de otro formato. Se toma el contenido, no el formato: **la salida
   sigue siempre la sección 11**, no la del archivo.
5. **Ninguno fue auditado contra fuente primaria.** Se usan con la advertencia que corresponde,
   y todo lo cuantitativo o de vigencia va marcado.
6. **Ninguno es procesalmente bonaerense por defecto.** Nada de esto fue revisado contra la Ley
   15.057 ni contra la Res. SC 1840/2024. Si el escrito va al fuero laboral de PBA, mandan
   `sede-judicial-pba.md` y `parte.md`.

### 23.2 Guías de armado por rama

Cada una tiene el proceso de encuadre, la verificación normativa previa, la elección de modelo
y su propio checklist de cierre. Leer la guía de la rama **antes** que el modelo.

| Rama | Guía |
| --- | --- |
| Civil y comercial | `kb/escritos/civil/escritos/escritos-civil-SKILL.md` |
| Familia | `kb/escritos/familia/escritos/escritos-familia-SKILL.md` |
| Consumidor | `kb/escritos/consumidor/escritos/escritos-consumidor-SKILL.md` |
| Penal | `kb/escritos/penal/escritos/escritos-penal-SKILL.md` |
| Previsional | `kb/escritos/previsional/escritos/escritos-previsional-SKILL.md` |
| Tránsito (descargos) | `kb/escritos/transito/descargos/descargos-SKILL.md` |
| Telegramas laborales | `kb/escritos/laboral/telegrama/telegramas-SKILL.md`, con `kb/escritos/laboral/telegrama/reglas-normativas.md` y `kb/escritos/laboral/telegrama/tipos-de-telegrama.md` |

### 23.3 Civil y comercial — `kb/escritos/civil/escritos/modelos/`

| Escrito | Archivo |
| --- | --- |
| Demanda de daños por accidente de tránsito | `kb/escritos/civil/escritos/modelos/demanda-danos-accidente-transito.md` |
| Demanda de daños por mala praxis médica (art. 1768 CCyCN) | `kb/escritos/civil/escritos/modelos/demanda-danos-mala-praxis.md` |
| Demanda de daños por incumplimiento contractual | `kb/escritos/civil/escritos/modelos/demanda-danos-incumplimiento-contractual.md` |

Encuadre: `civil.md` sección 6, y el ruteo por instituto de 6.5. Los tres tienen versión como
doc del Project (`derecho/modelo-demanda-danos-*.md`), utilizable cuando el repo no está
conectado.

### 23.4 Familia — `kb/escritos/familia/escritos/modelos/`

| Escrito | Archivo |
| --- | --- |
| Demanda de alimentos para hijos, con provisorios (arts. 658-670 CCyCN) | `kb/escritos/familia/escritos/modelos/demanda-alimentos.md` |
| Convenio regulador de divorcio (art. 438 CCyCN) | `kb/escritos/familia/escritos/modelos/convenio-regulador-divorcio.md` |
| Solicitud de medidas de protección por violencia familiar | `kb/escritos/familia/escritos/modelos/medidas-proteccion-violencia-familiar.md` |

Encuadre: `familia.md` sección 18, y el ruteo por instituto de 18.8. **Dos advertencias
específicas de PBA que los modelos no traen**: la etapa previa ante el Consejero de Familia
(18.3) y la reforma de la Ley 15.513 a los arts. 635 bis, 636 bis y 641 CPCCBA — alimentos
provisorios en el primer auto, notificación por aplicaciones de mensajería, Canasta de Crianza
(18.5). Un escrito de alimentos armado con el modelo solo, sin 18.5, sale desactualizado.

### 23.5 Consumidor — `kb/escritos/consumidor/escritos/modelos/`

| Escrito | Archivo |
| --- | --- |
| Demanda por daños y daño punitivo en relación de consumo | `kb/escritos/consumidor/escritos/modelos/demanda-dano-punitivo.md` |
| Demanda por garantía y producto defectuoso (art. 11 LDC) | `kb/escritos/consumidor/escritos/modelos/demanda-garantia-producto.md` |
| Amparo de salud contra empresa de medicina prepaga | `kb/escritos/consumidor/escritos/modelos/amparo-salud-prepaga.md` |
| Reclamo administrativo de consumo (ventanilla, OMIC) | `kb/escritos/consumidor/escritos/modelos/reclamo-ventanilla-omic.md` |
| Cartas documento e intimaciones de consumo | `kb/escritos/consumidor/escritos/modelos/cartas-documento-intimaciones.md` |

Encuadre: `consumidor.md` sección 17, y el ruteo de 17.8. **Verificar antes de usar el modelo
de reclamo administrativo**: la instancia previa cambió (17.2, disolución del COPREC por el
Dec. 55/2025), y el modelo puede describir un procedimiento que ya no existe. Para daño
punitivo, el requisito subjetivo en PBA no es el de la doctrina mayoritaria (17.5).

### 23.6 Telegramas laborales — `kb/escritos/laboral/telegrama/modelos/`

**Leer primero `telegramas.md` sección 25.** Ahí está, verificado contra el texto consolidado,
lo que exige cada norma, qué plazo rige de verdad y en qué orden van los actos. Los archivos de
`kb/` que se listan abajo aportan la redacción y la casuística; no aportan la verificación.

Ocho bloques temáticos. **El telegrama es el acto que más caro sale mal redactado.**

| Bloque | Archivo | Materia |
| --- | --- | --- |
| 1 | `kb/escritos/laboral/telegrama/modelos/bloque-01-registro.md` | Registración, Ley 24.013, arts. 7 y ss. (el art. 11 está **derogado**) |
| 2 | `kb/escritos/laboral/telegrama/modelos/bloque-02-estabilidad-despido.md` | Estabilidad, despido, injuria |
| 3 | `kb/escritos/laboral/telegrama/modelos/bloque-03-salarios.md` | Salarios, diferencias, art. 74 LCT |
| 4 | `kb/escritos/laboral/telegrama/modelos/bloque-04-ius-variandi.md` | Ius variandi, art. 66 LCT |
| 5 | `kb/escritos/laboral/telegrama/modelos/bloque-05-renuncia.md` | Renuncia y su retractación |
| 6 | `kb/escritos/laboral/telegrama/modelos/bloque-06-vacaciones-licencias.md` | Vacaciones y licencias |
| 7 | `kb/escritos/laboral/telegrama/modelos/bloque-07-salud-hostigamiento.md` | Salud, enfermedades inculpables, hostigamiento |
| 8 | `kb/escritos/laboral/telegrama/modelos/bloque-08-construccion.md` | Régimen de la construcción |

Encuadre: `laboral.md` sección 5, y el ruteo de 5.11. Los ocho bloques y las dos guías están
además como docs del Project (`derecho/telegramas-*.md`). **Verificar el tramo de reforma que
rige** (5.1) antes de usar cualquier modelo: los apercibimientos y los plazos cambiaron con las
Leyes 27.742 y 27.802.

> **Defecto concreto que hay que corregir a mano en cada uso.** Los modelos del bloque 1 y el de
> despido por falta de registro del bloque 2 intiman **"en el plazo de 30 días"** citando los
> **arts. 7 y 7 bis de la Ley 24.013**. Esos artículos **no contienen ningún plazo**: el de 30 días
> lo fijaba el **art. 11 inc. a**, derogado por la Ley 27.742 junto con los agravantes que
> habilitaba. Ver `laboral.md` 5.3. Al usar esos modelos, reemplazar el plazo por uno razonable según el caso
> —el art. 57 LCT exige que nunca sea inferior a dos días hábiles— y no atribuirlo a los
> arts. 7 y 7 bis. Los apercibimientos de multa sí fueron depurados en una consolidación anterior;
> el plazo quedó.

Lo que sí conviene tomar de estos modelos es la **secuencia**: intimación, plazo, respuesta o
silencio, y recién entonces el acto extintivo haciendo efectivo el apercibimiento. Esa estructura
no cambió con las reformas. Lo que cambió son los números y las normas que se citan, y eso se
verifica contra `laboral.md` cada vez.

### 23.7 Ramas sin módulo propio

Se usan junto con `perfiles-heredados.md` (sección 19) y con el perfil de la rama, que es donde está
el encuadre. Aplica en pleno la advertencia del punto 23.1.6.

**Penal** — `kb/escritos/penal/escritos/modelos/`: excarcelación y cese de prisión preventiva
(`kb/escritos/penal/escritos/modelos/excarcelacion-cese-prision-preventiva.md`), hábeas corpus correctivo
(`kb/escritos/penal/escritos/modelos/habeas-corpus-correctivo.md`), nulidad de allanamiento y prueba derivada
(`kb/escritos/penal/escritos/modelos/nulidad-allanamiento.md`), recurso de casación (`kb/escritos/penal/escritos/modelos/recurso-casacion.md`), suspensión del juicio
a prueba (`kb/escritos/penal/escritos/modelos/solicitud-probation.md`).

**Previsional** — `kb/escritos/previsional/escritos/modelos/`: impugnación judicial de denegatoria de ANSES
(`kb/escritos/previsional/escritos/modelos/demanda-impugnacion-denegatoria.md`), reajuste de haberes, inicial y movilidad
(`kb/escritos/previsional/escritos/modelos/demanda-reajuste-haberes.md`), pensión derivada para conviviente sin matrimonio
(`kb/escritos/previsional/escritos/modelos/demanda-pension-derivada.md`).

**Tránsito** — `kb/escritos/transito/descargos/modelos/`, siete descargos numerados:

| Descargo | Archivo |
| --- | --- |
| Nulidad por defectos formales del acta o fotomulta | `kb/escritos/transito/descargos/modelos/modelo-01-nulidad-formal.md` |
| Estado de necesidad o fuerza mayor | `kb/escritos/transito/descargos/modelos/modelo-02-urgencia-fuerza-mayor.md` |
| Denuncia de venta anterior al hecho | `kb/escritos/transito/descargos/modelos/modelo-03-denuncia-de-venta.md` |
| Falta de notificación en término y prescripción | `kb/escritos/transito/descargos/modelos/modelo-04-falta-notificacion-prescripcion.md` |
| Error de identificación y cesión de uso en flota | `kb/escritos/transito/descargos/modelos/modelo-05-error-identificacion.md` |
| Apelación contra la resolución que confirma la sanción | `kb/escritos/transito/descargos/modelos/modelo-06-recurso-apelacion.md` |
| Defensa por escrito a distancia (art. 71, 1er párr., Ley 24.449) | `kb/escritos/transito/descargos/modelos/modelo-07-defensa-a-distancia-art71.md` |

Más un acápite suelto: `kb/escritos/transito/descargos/modelo-acapite-prescripcion-CABA.md`.

### 23.8 Casos trabajados de punta a punta

Distintos de los modelos: son casos resueltos completos, con el razonamiento a la vista. Sirven
para calibrar el nivel de detalle y el uso de marcadores, no para copiar.

**Los de referencia son los `resultado.md` de `derecho/evals/`**, y sirven para la FORMA: qué se
resuelve antes del fondo, qué marcador va en cada hueco, hasta dónde llega el detalle y qué hace
fallar el caso.

**Para el contenido no mandan, y la razón es de mecanismo:** un `resultado.md` se escribió contra
el derecho de su fecha y **no tiene fila** en `references/changelog-normativo.md`, así que **no
puede vencer** — ninguna reforma lo va a marcar. Lo normativo
sale del módulo de la materia y de `fuentes/`, como siempre; del eval sale la forma.

**Y no se abre la `rubrica.md` ni los `graders/` de ningún caso.** Eso es el criterio con que se
puntúa una respuesta, no material de consulta: leerlos mientras se trabaja convierte la medición
en una lectura, y el repositorio lo controla sobre la traza de cada corrida.

Hay siete casos más en `kb/ejemplos/` —laboral, civil, familia, previsional, penal, societario y
discapacidad—, de los cuales los dos primeros están además como docs del Project. Se usan con la
misma regla, y con la advertencia de siempre: consolidados **sin auditoría**.

### 23.9 Qué no hay

No hay modelo de: contestación de demanda en ninguna rama, recursos del fuero laboral
(extraordinarios de la 11.653, apelación de la 15.057), incidentes, liquidación, ejecución, ni
ninguna pieza redactada **desde el órgano** —veredicto, sentencia, interlocutoria—. Para eso
manda `sede-judicial-pba.md`, que tiene la estructura de la pieza aunque no un modelo completo.
Decirlo cuando corresponda, en vez de forzar un modelo de demanda a hacer de contestación.
