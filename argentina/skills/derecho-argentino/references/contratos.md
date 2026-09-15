# Revisión de contratos

> Módulo de referencia de la skill `derecho-argentino`. La numeración de secciones es global y
> se mantiene igual que en el SKILL.md original: las remisiones cruzadas entre módulos siguen siendo
> válidas. Las reglas de integridad de la sección 2 rigen acá también.

---

## 7 · Revisión de contratos — disparo automático

Ante un contrato aportado en sesión, el análisis de red-flags **se corre sin que nadie lo
pida**. Se reconoce por lo que el texto es —cláusulas numeradas, partes identificadas,
obligaciones recíprocas— y no por cómo se llame el archivo.

**Si viene con instrucción de modificarlo, el análisis va igual y va primero.** Se entrega el
informe y recién entonces se pregunta si se modifica. El motivo no es formal: una cláusula
nula que se reescribe sin señalarla deja al cliente con un contrato que parece sano, y quien
lo firma ya no tiene manera de enterarse.

**El orden de la revisión, y por qué es ese.** Primero la validez, después el riesgo: una
cláusula inválida no se negocia, se saca. Dentro de la validez **se recorre el contrato
entero antes de informar** — encontrada la primera cláusula inválida, el reflejo es detenerse,
y es el error que deja la segunda adentro.

| Paso | Qué se busca | Qué se hace con el hallazgo |
|---|---|---|
| **1 · Encuadre** | Tipo —adhesión, paritario, de consumo, laboral encubierto—, partes, objeto, ley aplicable | Decide todo lo demás: la misma cláusula es válida entre empresas e inválida frente a un consumidor |
| **2 · Validez** | Cláusulas que la ley no deja en pie, del catálogo de 7.1 | **Recorrer el contrato completo** y listarlas todas, cada una con `[RED FLAG - NULIDAD ABSOLUTA: ...]`. No se proponen alternativas: se señala que no valen |
| **3 · Riesgo alto** | Lo que es válido pero puede costar caro | `[RED FLAG - RIESGO ALTO: ...]` y desarrollar **con redacción alternativa concreta** |
| **4 · Riesgo medio** | Lo que conviene corregir sin urgencia | `[RED FLAG - RIESGO MEDIO: ...]` y consignar en el informe |
| **5 · Vigencia** | Cada norma citada, la primera vez | `[VERIFICAR VIGENCIA]` |
| **6 · Informe** | — | Las tres categorías, más las normas con verificación pendiente |

> **La consecuencia no es siempre "nulidad", y conviene no decirlo de más.** El art. 988 manda
> **tener por no escritas** las cláusulas abusivas en los contratos de adhesión, que es
> distinto de anular el contrato; el art. 1743 dice que las dispensas anticipadas son
> **inválidas**; el art. 2533 dice que las normas de prescripción **no pueden ser modificadas
> por convención**. Cada una tiene su efecto y su alcance, y están en 7.1 uno por uno.

> **Cada hallazgo sale con su marcador, y el marcador es el nivel.** Los tres de la serie D
> —`[RED FLAG - NULIDAD ABSOLUTA]`, `[RED FLAG - RIESGO ALTO]`, `[RED FLAG - RIESGO MEDIO]`,
> sintaxis exacta en `marcadores.md` D4 a D6— existen para que el informe sea legible de un
> vistazo y para que quien firma se tropiece con lo grave. Describir el nivel en prosa y no
> emitir el marcador deja las tres categorías mezcladas en un texto corrido, que es justo lo
> que el paso 6 quiere evitar.

### 7.1 Catálogo de cláusulas de riesgo

Articulado cotejado contra `fuentes/normas/ccycn-26994.txt` y `fuentes/normas/ldc-24240.txt`.
Es la versión desarrollada de los niveles 2 a 4 de arriba: cada entrada dice **qué mirar**,
**qué norma la sostiene** y **cuál es la consecuencia**, que no siempre es la nulidad.

#### Nulidad absoluta o cláusula no escrita — `[RED FLAG - NULIDAD ABSOLUTA]`

| Cláusula | Norma | Consecuencia exacta |
|---|---|---|
| **Renuncia anticipada a defensas** oponibles en juicio | Art. 944 | La renuncia de derechos se admite sólo si **no está prohibida y sólo afecta intereses privados**; el mismo artículo cierra: **no se admite la renuncia anticipada de las defensas** que puedan hacerse valer en juicio |
| **Dispensa o limitación de responsabilidad** | Art. 1743 | Son **inválidas** las que eximen o limitan la obligación de indemnizar cuando **afectan derechos indisponibles, atentan contra la buena fe, las buenas costumbres o leyes imperativas, o son abusivas**; y también las que liberan anticipadamente, **total o parcialmente, del daño por dolo** del deudor o de quienes responde |
| **Cláusulas abusivas en contrato de adhesión** | Art. 988 | **Se tienen por no escritas** las que desnaturalizan las obligaciones del predisponente, las que importan renuncia o restricción de derechos del adherente **o amplían los del predisponente que resultan de normas supletorias**, y las que **por su contenido, redacción o presentación no son razonablemente previsibles** |
| **Cláusulas abusivas en consumo** | Arts. 1119 y 37 LDC | Es abusiva la que, **negociada individualmente o no**, tiene por objeto o efecto un **desequilibrio significativo** en perjuicio del consumidor. El art. 37 LDC suma tres supuestos propios, incluida la **inversión de la carga de la prueba** |
| **Prórroga de jurisdicción en contrato de consumo** | Art. 2654 | **"En esta materia no se admite el acuerdo de elección de foro"**, y la acción contra el consumidor **sólo** puede interponerse ante los jueces de su domicilio. No es una cláusula atacable: es inadmisible |
| **Modificación convencional de la prescripción** | Art. 2533 | **"Las normas relativas a la prescripción no pueden ser modificadas por convención"**. Ni ampliar ni reducir |
| **Renuncia a derechos laborales** | Art. 12 LCT | Nula toda convención que suprima o reduzca derechos de la ley, los estatutos o el CCT, **al celebrar, al ejecutar o al ejercer derechos de la extinción**. Ver `laboral.md` 5.16.2 sobre lo que el texto vigente ya no enumera |

> **Una diferencia que el DNU 70/2023 abrió y conviene no pasar por alto.** El **art. 989** fue
> sustituido por su art. 254 y hoy dice **sólo** que la aprobación administrativa de las
> cláusulas generales no obsta al control judicial: **ya no manda integrar** el contrato al
> declararse la nulidad parcial. En **consumo**, en cambio, el deber de integración sigue vivo
> —**art. 1122 inc. c**: "si el juez declara la nulidad parcial del contrato, simultáneamente lo
> debe integrar, si no puede subsistir sin comprometer su finalidad"—, y el art. 37 LDC lo
> repite. O sea: en adhesión no consumeril hay que **pedir** la integración y fundarla; en
> consumo es un deber del juez.
> `[VERIFICAR VIGENCIA: texto del art. 989 CCyCN a la fecha del contrato - sustituido por el DNU 70/2023 desde el 21/12/2023]`

**Límites del control (art. 1121).** No pueden declararse abusivas las cláusulas relativas a la
**relación entre el precio y el bien o servicio** procurado, ni las que **reflejan disposiciones
de tratados internacionales o de normas legales imperativas**. Es la defensa estándar contra un
planteo de abusividad dirigido al precio, y hay que anticiparla.

**Situación jurídica abusiva (arts. 1120 y 1122 inc. d).** Cuando el mismo resultado se alcanza
por una **pluralidad de actos jurídicos conexos**, hay situación jurídica abusiva aunque ninguna
cláusula aislada lo sea. Probada, el juez aplica el art. 1075. Es el encuadre para los esquemas
armados con varios contratos que por separado parecen inocuos.

#### Riesgo alto — `[RED FLAG - RIESGO ALTO]`, con propuesta de redacción

- **Ausencia de mecanismo de actualización** en contratos de larga duración. No hay norma que la
  prohíba: el riesgo es económico y se trata redactando. Qué índice usar está en 7.2.
- **Pacto comisorio sin el procedimiento de los arts. 1083 a 1089.** La resolución por
  incumplimiento tiene requisitos —incumplimiento esencial, emplazamiento, plazo— que una
  cláusula no puede saltear sin quedar expuesta.
- **Confidencialidad sin plazo determinado.** Perpetua es de interpretación restrictiva y
  discutible; conviene plazo y definición de información confidencial.
- **Arbitraje con sede en el extranjero.** En consumo choca de frente con el art. 2654. Fuera de
  consumo, mirar si hay parte débil y si la sede vuelve ilusoria la defensa.
- **Relación laboral encubierta** bajo contrato de servicios. El encuadre es el art. 14 LCT con
  los arts. 22 y 23: ver `laboral.md` 5.16.5 y 5.4, incluidas las excepciones que introdujo la
  Ley 27.802 al art. 23 y su constitucionalidad en litigio.
- **Cláusula de no competencia post-contractual sin contraprestación ni límites** de tiempo,
  territorio y objeto.

#### Riesgo medio — `[RED FLAG - RIESGO MEDIO]`, consignar

- **Falta de domicilio especial constituido en Argentina.**
- **Moneda extranjera sin previsión de pago.** El régimen cambió: obligaciones nacidas **desde
  el 30/12/2023** se liberan **sólo entregando la moneda pactada** (arts. 250 y 251 DNU
  70/2023), y los jueces no pueden modificar forma de pago ni moneda. Ver `civil.md` 6.4.
- **Garantías sin inscripción registral** cuando corresponde: sin inscripción no hay
  oponibilidad a terceros.
- **Plazos de prescripción mencionados en el contrato.** Aunque sean los legales, invitan a
  discutir el art. 2533; si difieren, la cláusula no vale.

### 7.1 bis Qué queda en el perfil heredado

`kb/contratos/` es **capa 2** —de Cristian Aboitiz, con su propia licencia— y **no pasó la
auditoría contra fuente primaria** que sí pasó este módulo. Rige la precedencia de la sección
15: fuente primaria → esta skill → docs del Project → perfiles del repo.

| Instituto | Dónde |
|---|---|
| Catálogo de red-flags por nivel | **7.1** de este módulo. Absorbido: ya no se rutea al perfil |
| Protocolo de revisión y orden de los pasos | **7** de este módulo. Absorbido: ya no se rutea al perfil |
| Índices y tasas de referencia | **7.2** de este módulo, contra las series de `fuentes/datos/`. Absorbido: ya no se rutea al perfil |
| Locaciones urbanas y los tres regímenes por fecha | `civil.md`, y `kb/contratos/CLAUDE.md` § Régimen de locaciones urbanas |
| Régimen cambiario y obligaciones en moneda extranjera | `kb/contratos/CLAUDE.md` § Régimen cambiario y § Obligaciones en moneda extranjera, **sin auditar**, con `[VERIFICAR RÉGIMEN CAMBIARIO VIGENTE]` |

#### Contradicciones nominadas — el perfil dice lo contrario que este módulo

| El perfil dice | Lo correcto |
|---|---|
| `red-flags.md` § Nulidad absoluta, punto 3: *"Limitación de responsabilidad por dolo o culpa grave"* | **La culpa grave no está en el texto.** El art. 1743 CCyCN invalida las cláusulas que liberan anticipadamente del daño **por dolo** del deudor o de las personas por las que responde; la culpa grave no figura. Lo que sí invalida, por la otra vía del mismo artículo, es lo que afecta derechos indisponibles, la buena fe, las buenas costumbres o leyes imperativas, o resulta abusivo. Alegar "culpa grave" como causal autónoma es ofrecer una defensa: está en 7.1, cotejado contra `fuentes/normas/ccycn-26994.txt` |

### 7.2 Índices y tasas — dónde se saca el valor

La regla no cambió y conviene repetirla: **el módulo dice cuál índice, nunca cuánto**. El valor
se toma de `fuentes/datos/` —que trae `serie-ipc.csv`, `serie-cer.csv`, `serie-ripte.csv` y
`jus-scba.csv`, con su procedencia— o del portal oficial, y nunca de un archivo de doctrina o de
un perfil.

| Para | Serie | Dónde |
|---|---|---|
| Actualización de créditos en general | **IPC Nivel General INDEC** | `fuentes/datos/serie-ipc.csv` |
| Obligaciones con cláusula CER | **CER** | `fuentes/datos/serie-cer.csv` |
| Base de prestaciones de riesgos del trabajo | **RIPTE** | `fuentes/datos/serie-ripte.csv` — se publica con **dos meses de rezago**, y eso es normal, no desactualización |
| Honorarios en PBA | **jus previsional SCBA** | `fuentes/datos/jus-scba.csv` |

Para intereses del crédito laboral, el régimen aplicable y su discusión están en `laboral.md`
5.5 y 5.5 bis; para el civil, en `civil.md` 6.2. La calculadora es
`scripts/intereses.py`, que exige el régimen y no lo adivina.

`[VERIFICAR TASA VIGENTE: tasa y régimen aplicables al crédito - fuero y fecha de exigibilidad]`

**Anatocismo.** La capitalización de intereses sólo procede en los casos del **art. 770 CCyCN**;
fuera de ellos, una cláusula que capitalice mensualmente es de las que hay que marcar. Y la
abusividad de la tasa no se mide contra un número fijo sino contra la tasa de plaza para
operaciones similares a la fecha del contrato, que es una cuestión de prueba.
