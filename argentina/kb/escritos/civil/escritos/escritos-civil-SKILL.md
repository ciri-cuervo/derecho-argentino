---
name: escritos-civil
description: Redacta escritos de daños y responsabilidad civil del derecho argentino (demanda de daños por accidente de tránsito, demanda por mala praxis médica, demanda de daños por incumplimiento contractual). Activar ante cualquier pedido de redacción de una demanda de daños civil, aunque el usuario no nombre el modelo. Trabaja junto con el perfil kb/perfiles/civil-CLAUDE.md y la doctrina kb/doctrina/civil-DOCTRINA.md.
---

# Escritos de daños y responsabilidad civil

> Parte del repositorio de conocimiento jurídico argentino.
> Autor: Dr. Cristian Aboitiz · [@abogadoaboitiz](https://x.com/abogadoaboitiz)

---

## Descripción

Redacta escritos de daños para abogados matriculados. El abogado firma y asume la responsabilidad profesional de cada pieza. Este skill redacta; el abogado revisa y decide. Opera siempre junto con el perfil `kb/perfiles/civil-CLAUDE.md`, que aporta la lógica de fondo (fueros, factores de atribución, rubros, prescripción, cautelares), y con `kb/doctrina/civil-DOCTRINA.md`, que aporta los leading cases verificados.

---

## Cuándo usar

Activar cuando el usuario pida redactar o preparar una demanda de daños civil: accidente de tránsito, mala praxis médica, o incumplimiento contractual con reclamo resarcitorio. No es necesario que nombre el modelo.

No activar:
- Para el solo análisis estratégico o de viabilidad sin redacción: alcanza el perfil `kb/perfiles/civil-CLAUDE.md`.
- Para cartas documento o intimaciones civiles y comerciales extrajudiciales: usar el skill de cartas documento (carty) o `kb/contratos/`.
- Para daños en relación de consumo con daño punitivo: usar `kb/escritos/consumidor/escritos/`.
- Para amparos de salud o reclamos contra obras sociales y prepagas: usar el perfil de discapacidad o de consumidor según el caso.
- Para demandas contra el Estado por responsabilidad extracontractual: derivar al perfil administrativo (art. 1764 CCCN; Ley 26.944 o ley provincial).

---

## Proceso

### Paso 1 - Encuadre y datos

Antes de redactar, definir con el usuario:

- Fuente de la responsabilidad: contractual o extracontractual. Define el plazo de prescripción y el factor de atribución de partida.
- Factor de atribución: objetivo (riesgo de la cosa o actividad, art. 1757 CCCN; garantía, art. 1753) o subjetivo (culpa o dolo, art. 1724). En responsabilidad objetiva la víctima no prueba culpa; en mala praxis la regla es subjetiva (art. 1768).
- Derecho intertemporal: si el hecho o contrato es anterior al 1° de agosto de 2015, verificar si rige el Código Civil de Vélez (Ley 340) y no el CCCN.
- Fuero y competencia: por materia, lugar del hecho, domicilio del demandado o lugar de cumplimiento. No transpolar institutos entre CPCCN y CPCCBA.
- Seguro: si hay aseguradora, prever la citación en garantía (art. 118 Ley 17.418) y verificar cobertura, límite y franquicia.
- Mediación prejudicial obligatoria: en CABA (Ley 26.589) y PBA (Ley 13.951) es recaudo de admisibilidad y suspende la prescripción. Verificar su cumplimiento antes de demandar.
- Material disponible: pericia, comprobantes, historia clínica, contrato, comunicaciones. Sin material, los hechos y la cuantía van con marcador, no se asumen.

### Paso 2 - Verificación normativa (no opcional)

Antes de incluir cualquier cita, leer la sección `## Alerta normativa - normas de vigencia variable` de `kb/perfiles/civil-CLAUDE.md` y aplicar sus reglas. Puntos críticos:

- Prescripción: la acción por responsabilidad civil (extracontractual y contractual de daños) prescribe a los 3 años (art. 2561 CCCN); el plazo genérico contractual es de 5 años (art. 2560). Verificar el dies a quo (desde que el daño es conocido o pudo conocerse).
- Tasa de interés: no citar tasa sin verificar el acta o acordada vigente del fuero. Varía entre CNAC, CNACOM y fueros provinciales.
- Fórmula de incapacidad: Vuotto, Méndez y variantes no tienen consagración legal. Verificar cuál aplica la sala actuante antes de liquidar (ver `kb/doctrina/civil-DOCTRINA.md` y `kb/ejemplos/ejemplos-civil.md`).
- Cuantía: no cuantificar rubros sin material aportado. El monto va con la fórmula "o lo que en más o en menos resulte de la prueba".

### Paso 3 - Elegir el modelo

Leer el modelo que corresponda y redactar sobre su estructura:

| Situación | Modelo |
|---|---|
| Daños por accidente de tránsito (responsabilidad objetiva por riesgo, con citación en garantía) | `modelos/kb/escritos/civil/escritos/modelos/demanda-danos-accidente-transito.md` |
| Daños por mala praxis médica (responsabilidad subjetiva del profesional, art. 1768; institución por el dependiente) | `modelos/kb/escritos/civil/escritos/modelos/demanda-danos-mala-praxis.md` |
| Daños por incumplimiento contractual (responsabilidad contractual, mora, resolución) | `modelos/kb/escritos/civil/escritos/modelos/demanda-danos-incumplimiento-contractual.md` |

Si hay aseguradora, integrar en cualquiera de ellos la citación en garantía (art. 118 Ley 17.418).

---

## Reglas de integridad (inmodificables)

- Jurisprudencia: prohibido citar carátula, sala, año o expediente sin material aportado. Usar `[INSERTAR FALLO VERIFICADO: sala, fuero, doctrina requerida]`. Los leading cases ya verificados en `kb/doctrina/civil-DOCTRINA.md` (Santa Coloma, Aquino, Rodríguez Pereyra, Arostegui, Vuotto, Méndez, Mosca, Cuello, Buffoni, Automóviles Saavedra) pueden citarse, verificando el texto íntegro antes de transcribir considerandos.
- Hechos: no asumir nada que no figure en el material. Usar `[VACÍO PROBATORIO: descripción]`.
- Normas: en la primera mención, `[VERIFICAR VIGENCIA]`. Si se sabe derogada o modificada, informarlo y proponer la vigente.
- Cuantificación: no asumir montos, tasas ni fórmulas. Usar `[VACÍO PROBATORIO: criterio de cuantificación del rubro - aportar pericia o indicar parámetro]` y `[VERIFICAR CRITERIO DEL FUERO: fórmula de incapacidad / tasa de interés - sala actuante]`.
- Periciales: no asumir el contenido de informes (médico, ingeniería, contable). Usar `[VACÍO PROBATORIO: informe pericial no aportado]`.

---

## Restricciones absolutas

- No inventar hechos no aportados por el usuario.
- No cuantificar incapacidad con una fórmula sin verificar la que usa la sala actuante.
- No citar una tasa de interés sin verificar el acta o acordada vigente del fuero.
- No aplicar normas del CCCN a hechos o contratos anteriores al 1° de agosto de 2015 sin verificar el derecho intertemporal.
- No confundir el plazo de prescripción de la responsabilidad civil (3 años, art. 2561) con el genérico contractual (5 años, art. 2560).
- No construir una demanda de responsabilidad objetiva sobre la culpa del demandado como elemento central.
- No demandar al Estado por el CCCN: deriva al perfil administrativo (art. 1764 CCCN).

---

## Racionalizaciones comunes

| Racionalización | Realidad |
|---|---|
| "En el accidente hay que probar la culpa del conductor" | En responsabilidad objetiva por riesgo (art. 1757-1758 CCCN + art. 64 Ley 24.449) la víctima no prueba culpa; el demandado se exime acreditando causa ajena. |
| "La aseguradora paga todo el daño" | La sentencia se ejecuta contra la aseguradora en la medida del seguro: límite de cobertura y franquicia son oponibles al damnificado (Cuello, Buffoni). |
| "El médico responde por el mal resultado" | La obligación del profesional liberal es de medios y la responsabilidad subjetiva (art. 1768), salvo resultado comprometido. Hay que probar el apartamiento del estándar de cuidado. |
| "La fórmula da el monto exacto de la incapacidad" | Las fórmulas son una pauta, no una regla mecánica (Arostegui). El juez pondera además circunstancias personales; verificar la fórmula de la sala. |
| "La acción de daños prescribe a los 5 años" | La acción por responsabilidad civil prescribe a los 3 años (art. 2561). Los 5 años (art. 2560) son el plazo genérico; controlar la fuente del reclamo. |

---

## Señales de alerta

Indicadores de que el borrador está mal antes de entregarlo:

- Construir la demanda de tránsito sobre la culpa del conductor en vez del riesgo de la cosa.
- Liquidar la incapacidad con una fórmula sin marcar que se verifique el criterio de la sala.
- Citar una tasa de interés concreta sin verificar el acta del fuero.
- Aplicar el CCCN a un hecho anterior a agosto de 2015 sin advertirlo.
- Reclamar a la aseguradora más allá del límite de cobertura o ignorar la franquicia.
- Citar un fallo con carátula y sala sin material aportado, fuera de los verificados en `kb/doctrina/civil-DOCTRINA.md`.
- Omitir la mediación prejudicial obligatoria como recaudo de admisibilidad.

---

## Verificación al cierre

Antes de entregar el borrador:

- [ ] Fuente de la responsabilidad y factor de atribución identificados y fundados
- [ ] Derecho intertemporal verificado (CCCN vs. CC/CCom según fecha del hecho o contrato)
- [ ] Fuero y competencia determinados; sin transpolación entre CPCCN y CPCCBA
- [ ] Sección de alerta normativa de `kb/perfiles/civil-CLAUDE.md` consultada (Paso 2)
- [ ] Modelo correspondiente leído (Paso 3)
- [ ] Prescripción correcta (3 años, art. 2561, salvo plazo especial) y dies a quo señalado
- [ ] Citación en garantía prevista si hay seguro; límite y franquicia considerados
- [ ] Mediación prejudicial obligatoria considerada (suspende la prescripción)
- [ ] Cuantificación con marcadores; fórmula de incapacidad y tasa con verificación de la sala
- [ ] Marcadores de integridad colocados (fallos, hechos, normas, periciales)
- [ ] Cierre con "Estado del escrito"

---

*Última actualización: junio 2026*
*Normativa base: CCCN (Ley 26.994) arts. 1708-1780 (responsabilidad civil), 1757-1758 (riesgo), 1768 (profesionales liberales), 2560-2561 (prescripción); Ley 17.418 (seguros) art. 118; Ley 24.449 (tránsito) art. 64; Ley 26.529 (derechos del paciente); Ley 26.589 y Ley 13.951 (mediación prejudicial). Perfil de fondo en kb/perfiles/civil-CLAUDE.md; doctrina en kb/doctrina/civil-DOCTRINA.md*
