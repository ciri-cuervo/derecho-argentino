---
name: escritos-familia
description: Redacta escritos de derecho de familia argentino (convenio regulador de divorcio, demanda de alimentos, solicitud de medidas de protección por violencia familiar, y piezas conexas de cuidado personal y régimen comunicacional). Activar ante cualquier pedido de redacción de un escrito de familia, aunque el usuario no nombre el modelo. Trabaja junto con el perfil kb/perfiles/familia-CLAUDE.md y la doctrina kb/doctrina/familia-DOCTRINA.md.
---

# Escritos de derecho de familia

> Parte del repositorio de conocimiento jurídico argentino.
> Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)

---

## Descripción

Redacta escritos de familia para abogados matriculados. El abogado firma y asume la
responsabilidad profesional de cada pieza. Este skill redacta; el abogado revisa y decide.
Opera siempre junto con el perfil `kb/perfiles/familia-CLAUDE.md`, que aporta la lógica de fondo (fueros,
institutos, plazos de caducidad, cautelares), y con `kb/doctrina/familia-DOCTRINA.md`, que aporta los
holdings verificados.

---

## Cuándo usar

Activar cuando el usuario pida redactar o preparar un escrito de familia: convenio regulador
de divorcio, demanda de alimentos, solicitud de medidas de protección por violencia familiar,
o piezas de cuidado personal y régimen comunicacional. No es necesario que nombre el modelo.

No activar:
- Para el solo análisis estratégico o de viabilidad sin redacción: alcanza `kb/perfiles/familia-CLAUDE.md`.
- Para mediación prejudicial previa: usar el skill de mediación (medy).
- Para daños y perjuicios derivados de un hecho familiar (p. ej. daño por incumplimiento del
  régimen): derivar al perfil civil y a `kb/escritos/civil/escritos/`.
- Para sucesiones: queda fuera de este bloque.

---

## Proceso

### Paso 1 - Encuadre y datos

Antes de redactar, definir con el usuario (si falta rama, tipo y jurisdicción, preguntarlos):

- Fuero y competencia: fuero nacional civil (CABA), fuero de familia PBA por departamento
  judicial, u otro. La materia de familia en CABA tramita ante la Justicia Nacional en lo
  Civil (no asumir un fuero local porteño operativo). En PBA, verificar la etapa previa ante
  el Consejero de Familia (CPCCBA, Decreto-Ley 7425/68, arts. 827 y ss.), salvo violencia.
- NNyA involucrados: edades, centro de vida, si fueron o serán oídos (art. 707 CCCN). El
  interés superior es el eje, no un argumento accesorio.
- Datos mínimos del instituto:
  - Convenio regulador (art. 438 CCCN): cuidado personal, régimen comunicacional, cuota
    alimentaria con moneda y ajuste, atribución de la vivienda, bienes, compensación
    económica. No redactar con vacíos sobre cuidado, comunicación y alimentos.
  - Alimentos: parentesco/legitimación, recursos del alimentante, centro de vida del niño,
    prueba del caudal económico.
  - Violencia familiar: tipo de violencia, riesgo actual, NNyA en el hogar, causa penal
    paralela, armas, componente digital.
- Material disponible: partidas, DNI, recibos, informes técnicos, comunicaciones. Sin
  material, los hechos van con marcador; no se asumen.

### Paso 2 - Verificación normativa (no opcional)

Antes de incluir cualquier cita, leer la sección `## Alerta normativa - normas de vigencia
variable` de `kb/perfiles/familia-CLAUDE.md` y aplicar sus reglas. Puntos críticos:

- Plazos de caducidad fatales: compensación económica 6 meses (art. 442 divorcio / art. 525
  unión convivencial); atribución de vivienda en unión convivencial máx. 2 años (art. 526);
  impugnación de filiación 1 año (art. 590). Emitir `[ALERTA PLAZO FATAL]` antes del fondo.
- Alimentos: subsistencia hasta 21 (arts. 658/662), hasta 25 si estudia (art. 663);
  prescripción bienal de cuotas devengadas (art. 2562 inc. c); competencia del centro de
  vida (art. 716). No usar art. 719 para alimentos a hijos (es para cónyuges/convivientes).
- Cuota alimentaria: el Índice de Crianza INDEC es parámetro de referencia [VERIFICAR MONTO
  ACTUALIZADO: valor IC-INDEC por franja etaria - INDEC]. No existe una unidad nacional
  uniforme de medida alimentaria.
- Violencia PBA (Ley 12.569, texto Ley 14.509 y Ley 14.657): medidas del art. 7 en 48 horas;
  secuestro de armas (art. 7 ter); apelación 3 días (art. 10); prohibición de mediación o
  conciliación (art. 11). Violencia digital: Ley 26.485 art. 6 inc. i y cautelares art. 26
  ap. a.8 y a.9 (texto Ley 27.736 "Olimpia").
- Moneda en convenios: arts. 765-766 CCCN (texto DNU 70/2023): la obligación en moneda
  extranjera se cancela en esa moneda [VERIFICAR VIGENCIA: post-DNU 70/2023].

### Paso 3 - Elegir el modelo

Leer el modelo que corresponda y redactar sobre su estructura:

| Situación | Modelo |
|---|---|
| Divorcio con propuesta de convenio regulador (cuidado, comunicación, alimentos, vivienda, bienes, compensación) | `modelos/kb/escritos/familia/escritos/modelos/convenio-regulador-divorcio.md` |
| Reclamo de alimentos para hijos (con pedido de provisorios) | `modelos/kb/escritos/familia/escritos/modelos/demanda-alimentos.md` |
| Protección urgente por violencia familiar o de género (medidas cautelares, incluido componente digital) | `modelos/kb/escritos/familia/escritos/modelos/medidas-proteccion-violencia-familiar.md` |

Para cuidado personal y régimen comunicacional autónomos: usar la estructura del convenio
regulador adaptada a demanda contenciosa, con la lógica de los arts. 648-657 y 652 CCCN.

---

## Reglas de integridad (inmodificables)

- Jurisprudencia: prohibido citar carátula, sala, año o expediente sin material aportado. En
  familia las sentencias se publican anonimizadas; los holdings de `kb/doctrina/familia-DOCTRINA.md`
  están anclados a sumarios SAIJ verificados y pueden invocarse como doctrina del tribunal,
  verificando el texto íntegro antes de transcribir. Si falta precedente: `[INSERTAR FALLO
  VERIFICADO: doctrina requerida - aportar expediente, sala, fuero y año]`.
- Hechos: no asumir nada que no figure en el material. Usar `[VACÍO PROBATORIO: descripción]`.
- Informes técnicos: no asumir el contenido de informes psicológicos, socioambientales o
  periciales. Usar `[VACÍO PROBATORIO: contenido del informe/pericia no aportado]`.
- Normas: en la primera mención, `[VERIFICAR VIGENCIA]`. Si se sabe modificada, informarlo y
  proponer la vigente.
- Montos y valores: `[VERIFICAR MONTO ACTUALIZADO: concepto - fuente]`. Criterios que varían
  por fuero: `[VERIFICAR CRITERIO DEL FUERO: materia - fuero o sala]`.

---

## Restricciones absolutas

- No asumir un fuero de familia local porteño operativo ni un código procesal propio de CABA
  aplicable a familia.
- No omitir la alerta de los plazos de caducidad fatales (compensación económica, atribución
  de vivienda, impugnación de filiación) antes de analizar el fondo.
- No proponer ni aceptar mediación o conciliación en un proceso de violencia familiar de PBA
  (art. 11 Ley 12.569).
- No usar el art. 719 CCCN para la competencia de alimentos a hijos (es art. 716).
- No fijar el cese de la obligación alimentaria a los 18 años (subsiste hasta 21, art. 662; y
  hasta 25 si estudia, art. 663).
- No exponer innecesariamente al NNyA en el proceso; canalizar su voz por la vía del art. 707
  CCCN y el equipo técnico.

---

## Racionalizaciones comunes

| Racionalización | Realidad |
|---|---|
| "El divorcio se pelea por culpa" | El divorcio es incausado (art. 437 CCCN). No hay causales; la conflictividad se resuelve en el convenio regulador y los institutos conexos. |
| "La compensación económica se puede pedir cuando se liquiden los bienes" | Caduca a los 6 meses de la sentencia de divorcio (art. 442) o del cese de la convivencia (art. 525). Es fatal y de oficio. |
| "Los alimentos cesan cuando el hijo cumple 18" | Subsisten de pleno derecho hasta 21 (arts. 658/662) y hasta 25 si estudia o se capacita (art. 663). |
| "En violencia conviene una audiencia para conciliar" | En PBA están prohibidas las audiencias de mediación o conciliación (art. 11 Ley 12.569). |
| "El contenido íntimo difundido se baja con una intimación" | La cautelar específica la ordena el juez por el art. 26 ap. a.9 Ley 26.485 (texto Ley 27.736), con URL identificada y aseguramiento de datos. |

---

## Señales de alerta

Indicadores de que el borrador está mal antes de entregarlo:

- Redactar un convenio regulador con vacíos sobre cuidado personal, comunicación o alimentos.
- No alertar el plazo de caducidad de 6 meses de la compensación económica.
- Citar el art. 719 para la competencia de alimentos a hijos.
- Proponer mediación en un proceso de violencia de PBA.
- Cuantificar la cuota alimentaria sin remitir al IC-INDEC ni marcar su verificación.
- Citar un fallo con carátula y sala sin material, fuera de los holdings anclados en
  `kb/doctrina/familia-DOCTRINA.md`.
- Omitir el derecho del NNyA a ser oído (art. 707 CCCN) cuando corresponde.

---

## Verificación al cierre

Antes de entregar el borrador:

- [ ] Fuero y competencia determinados (sin asumir fuero local CABA operativo)
- [ ] NNyA: edades, centro de vida, derecho a ser oído (art. 707) considerado
- [ ] Sección de alerta normativa de `kb/perfiles/familia-CLAUDE.md` consultada (Paso 2)
- [ ] Modelo correspondiente leído (Paso 3)
- [ ] Plazos de caducidad fatales verificados y alertados (`[ALERTA PLAZO FATAL]` si aplica)
- [ ] Alimentos: competencia art. 716, subsistencia hasta 21/25, prescripción bienal
- [ ] Violencia PBA: medidas 48 hs, armas (art. 7 ter), sin mediación; componente digital
- [ ] Compensación económica: desequilibrio acreditado y plazo de 6 meses controlado
- [ ] Marcadores de integridad colocados (fallos, hechos, informes, normas, montos)
- [ ] Cierre con "Estado del escrito" (bloque de familia: fuero, NNyA, cautelares, plazo fatal)

---

*Última actualización: junio 2026*
*Normativa base: CCCN (Ley 26.994) Libro Segundo - matrimonio y divorcio (arts. 401-445),
compensación económica (441-442, 524-525), cuidado personal (648-657), comunicación (652,
557), alimentos (658-670, 716, 719), filiación (558-593), procesos de familia (705-723); Ley
26.485 (mod. Ley 27.736 "Olimpia"); Ley 12.569 PBA (texto Ley 14.509 y Ley 14.657); Ley
23.857 (La Haya). Perfil de fondo en kb/perfiles/familia-CLAUDE.md; doctrina en kb/doctrina/familia-DOCTRINA.md.*
