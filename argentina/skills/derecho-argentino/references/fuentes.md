# Fuentes primarias · enlaces, conectores y material del repo

> Módulo de referencia de la skill `derecho-argentino`. La numeración de secciones es global y
> se mantiene igual que en el SKILL.md original: las remisiones cruzadas entre módulos siguen siendo
> válidas. Las reglas de integridad de la sección 2 rigen acá también.

---

## 14.0 · Orden de consulta — antes de abrir un enlace

Tres capas, en este orden. Bajar a la siguiente sólo cuando la anterior no tiene la respuesta.

**1. El repo, si la carpeta está conectada.** Es lo más rápido y lo único que garantiza texto
literal sin truncar:

- `argentina/fuentes/normas/<slug>.txt` — texto consolidado con procedencia y hash. De acá se
  transcribe un artículo a un escrito.
- `argentina/fuentes/jurisprudencia/INDICE.md` — precedentes verificados, con enlace a la
  sentencia oficial y las sentencias descargadas al lado.
- `argentina/fuentes/datos/` — valor del jus, inhábiles, series de índices.
- `argentina/fuentes/ccyc-comentado/INDICE.md` — comentario oficial del CCyCN por artículo.
- `argentina/fuentes/MANIFIESTO.md` — qué está cargado y qué está pendiente.

**2. El hub `mcp-legal-ar`, si está activo.** Es un único conector MCP que da acceso a catorce
fuentes jurídicas argentinas: BORA, BOPBA, InfoLeg, Normativa PBA, JUBA, PTN, TFN, SCBA, PJN
Consulta, SAIJ, PJN Jurisprudencia, Portal PJN, JusCABA y CSJN.

Verificar que está cargado con **una** consulta, no catorce: cualquier `*__alcance_fuente`
(o `juba__info`) devuelve la cobertura del conector sin tocar la web. Si responde, el hub está
activo. Si un conector puntual no responde, el resto sigue funcionando: no reintentar la misma
consulta dos veces, pasar al enlace directo y **registrar en la sesión que la fuente no estaba
disponible**.

El ruteo detallado por tipo de consulta está en `argentina/kb/transversales/fuentes-y-conectores.md` del repo: tabla de
decisión por herramienta, ruteo por pieza de demanda y combinaciones recomendadas.

**3. Los enlaces directos** de las tablas que siguen. Cuando se pega texto en la sesión desde
un enlace, encabezarlo siempre con **fuente, fecha de consulta y URL de origen**.

Ante discrepancia entre el hub y la fuente primaria, prevalece la fuente primaria:

    [DISCREPANCIA ENTRE FUENTES: el conector X indica A / la fuente primaria indica B.
    Verificar directamente en fuente primaria antes de proceder.]

---

## 14 · Fuentes primarias — enlaces

Portales oficiales. Ante cualquier discrepancia, prevalece el texto que publican estos sitios.

### Portales

| Fuente | Qué tiene | Enlace |
|---|---|---|
| InfoLEG | Texto actualizado de normas nacionales | https://www.infoleg.gob.ar |
| Boletín Oficial | Publicación oficial, edición diaria y búsqueda por fecha | https://www.boletinoficial.gob.ar |
| Normativa nacional (arg.gob.ar) | Textos actualizados con listado de normas modificatorias | https://www.argentina.gob.ar/normativa |
| SAIJ | Jurisprudencia, doctrina y legislación provincial | https://www.saij.gob.ar |
| **Normas PBA** | Legislación bonaerense con texto actualizado | https://normas.gba.gob.ar |
| Boletín Oficial PBA | Publicación oficial provincial | https://www.boletinoficial.gba.gob.ar |
| **SCBA** | Jurisprudencia y acordadas de la Provincia | https://www.scba.gov.ar |
| JUBA | Base de jurisprudencia bonaerense | https://juba.scba.gov.ar |
| PJN — consulta de jurisprudencia | Fallos de los fueros nacionales y federales | https://sj.pjn.gov.ar |
| CSJN | Fallos de la Corte | https://www.csjn.gov.ar |
| ARCA | Registración laboral, "Trabajo en Blanco", RG vigentes | https://www.arca.gob.ar |
| Ministerio de Trabajo | CCT publicados, REPSAL | https://www.argentina.gob.ar/trabajo |
| SRT | Resoluciones y montos de prestaciones de la LRT | https://www.srt.gob.ar |
| INDEC | Canasta básica, IPC, RIPTE | https://www.indec.gob.ar |
| BCRA | Tasas y normativa cambiaria | https://www.bcra.gob.ar |

### Normas de uso diario

**Laboral**

| Norma | Enlace |
|---|---|
| LCT (Ley 20.744), texto actualizado | https://servicios.infoleg.gob.ar/infolegInternet/anexos/25000-29999/25552/texact.htm |
| Ley 27.802 (Modernización Laboral) | https://servicios.infoleg.gob.ar/infolegInternet/anexos/420000-424999/423680/norma.htm |
| Ley 27.742 (Bases) | https://servicios.infoleg.gob.ar/infolegInternet/verNorma.do?id=401266 |
| DNU 70/2023 | https://servicios.infoleg.gob.ar/infolegInternet/verNorma.do?id=395521 |
| Ley 24.013 (Empleo), texto actualizado | https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/412/texact.htm |
| Ley 14.250 (CCT), texto actualizado | https://www.argentina.gob.ar/normativa/nacional/ley-14250-46379/actualizacion |
| Ley 27.555 (Teletrabajo) | https://www.argentina.gob.ar/normativa/nacional/ley-27555-341093 |
| Ley 18.345 (proceso laboral nacional), texto actualizado | https://servicios.infoleg.gob.ar/infolegInternet/anexos/45000-49999/45628/texact.htm |
| **Ley 15.057 (proceso laboral PBA)** | https://normas.gba.gob.ar/documentos/xAzwAFoB.html |

**Civil, comercial y consumo**

| Norma | Enlace |
|---|---|
| CCyCN (Ley 26.994), texto | https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm |
| LDC (Ley 24.240), texto actualizado | https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/638/texact.htm |
| Ley 17.418 (Seguros) | https://servicios.infoleg.gob.ar/infolegInternet/anexos/35000-39999/39520/norma.htm |
| Ley 26.944 (Responsabilidad del Estado) | https://servicios.infoleg.gob.ar/infolegInternet/anexos/230000-234999/233216/norma.htm |
| Ley 26.589 (Mediación nacional), texto actualizado | https://www.argentina.gob.ar/normativa/nacional/ley-26589-166999/actualizacion |

**Procesal y administrativo**

| Norma | Enlace |
|---|---|
| CPCCN (Ley 17.454), texto actualizado | https://www.argentina.gob.ar/normativa/nacional/ley-17454-16547/actualizacion |
| **CPCCBA (Decreto-Ley 7425/68)** | https://normas.gba.gob.ar/documentos/VrQlgSOB.html |
| **Ley 13.951 (Mediación PBA)** | https://normas.gba.gob.ar/documentos/VmKoWSlx.html |
| **Ley 12.008 (Contencioso administrativo PBA)** | https://normas.gba.gob.ar/documentos/BodPyhzV.html |
| Ley 19.549 (LNPA), texto actualizado | https://www.argentina.gob.ar/normativa/nacional/ley-19549-22363/actualizacion |
| Ley 15.513 (reforma alimentos CPCCBA) | https://normas.gba.gob.ar/documentos/BLaA8kIQ.html |

**Advertencia de uso.** Estas bases truncan los documentos largos cuando se los consulta de
forma automática. Para transcribir un artículo en un escrito, abrir el enlace y copiar el
texto, o ir al PDF del Boletín Oficial de la fecha de publicación. Una transcripción
"sustancial" no es una transcripción literal, y en un escrito la diferencia se ve.

### Comentario oficial del CCyCN — disponible sin conexión

Cuando el repo está disponible (ver 0.2: no hay ninguna ruta fija), tiene los **seis tomos del
*Código Civil y Comercial de la Nación Comentado*** (SAIJ-INFOJUS, 2ª ed. actualizada 2022;
directores Herrera, Caramelo y Picasso) en `argentina/fuentes/ccyc-comentado/`. Es publicación
oficial de distribución gratuita y libre reproducción citando la fuente, de modo que **sí puede
citarse y transcribirse** en un escrito.

No abrir los PDFs a ciegas: **`argentina/fuentes/ccyc-comentado/INDICE.md` rutea cada rango de
artículos a su tomo y a la página exacta.** Puntos de entrada más usados (página del PDF):

| Instituto | Arts. | Tomo y página |
|---|---|---|
| Obligaciones en general | 724-956 | T3 p. 28 |
| Contratos en general | 957-1091 | T3 p. 359 |
| Contratos de consumo | 1092-1122 | T3 p. 515 |
| Compraventa | 1123-1171 | T3 p. 552 |
| Locación | 1187-1226 | T3 p. 593 |
| Obra y servicios | 1251-1279 | T4 p. 30 |
| **Responsabilidad civil** | **1708-1780** | **T4 p. 445** |
| Derechos reales | 1882-2276 | T5 p. 26 |
| Sucesiones | 2277-2461 | T6 p. 26 |
| Prescripción y caducidad | 2532-2572 | T6 p. 298 |
| Familia | 401-723 | T2 p. 24 |
| Persona humana | 19-140 | T1 p. 87 |

Dos advertencias del índice: "contratos en particular" queda **partido entre los tomos 3 y 4**
(compraventa en T3, obra y servicios en adelante en T4), que es el error de navegación más
frecuente; y cada tomo tiene doble numeración — las páginas de arriba son **páginas del PDF**,
no impresas (desfasaje T1 +39, T2 +23, T3 +27, T4 +29, T5 +25, T6 +25).

