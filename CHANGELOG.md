# Changelog

Historial de **versiones** del plugin. Formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado [SemVer](https://semver.org/lang/es/).

Lleva versiones, no sesiones de trabajo. El detalle de cada cambio vive donde se puede verificar:

| Qué | Dónde |
| --- | --- |
| Qué cubre cada módulo y cómo está armado el repo | [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) |
| Cuándo se verificó cada instituto contra fuente primaria, y su volatilidad | `argentina/skills/derecho-argentino/references/changelog-normativo.md` |
| Qué hay cargado en la capa offline | `argentina/fuentes/MANIFIESTO.md` |
| La doctrina de cada precedente | El módulo que la usa; el índice, en `references/fallos-csjn.md` |
| Si el texto de un fallo se puede transcribir | `herramientas/lecturas-ocr.json` |

## [1.0.2] — 2026-09-15

Actualizado: íconos y banners actualizados junto con los metadatos de Marketplace para ambos plugins: Claude y Codex.

## [1.0.1] — 2026-09-15

Correcciones: no entran normas ni fallos nuevos y ningún cálculo cambia de resultado.

- **Ortografía.** Acentos y `ñ` en los módulos, en los marcadores que la skill emite y en la salida
  de los scripts. Las carátulas se corrigieron contra el documento. Lo que se compara sigue en
  ASCII: si se muestra, se acentúa; si se compara, no.
- **Fechas.** Las del derecho, con día y mes de dos dígitos; las del propio trabajo, por mes.
- **Títulos de las constituciones provinciales** en `normas.json`.
- **Si falta Python, la skill no calcula a mano:** emite el marcador y explica cómo instalarlo. Sin
  repo conectado, en cambio, sí se calcula.
- La salida de las herramientas entra en la consola de Windows, donde un `→` cortaba el script
  después de haber medido y escrito.
- Control nuevo de las cifras de inventario de la documentación, con `herramientas/cifras.py`.

**Los datos vienen congelados a septiembre de 2026.** `/derecho:estado` dice qué quedó vencido y
`/derecho:actualizar` lo baja de las fuentes oficiales.

## [1.0.0] — 2026-09-14

Versión inicial.

Plugin de análisis, redacción y revisión jurídica bajo derecho argentino. Primera versión
publicable de un proyecto en desarrollo: la cobertura auditada crece módulo por módulo. Trae:

- La skill `derecho-argentino`: 30 módulos de referencia con numeración global estable, modo desde
  una parte y modo desde el órgano jurisdiccional.
- **Ocho comandos slash** y un perfil de usuario que ordena las preguntas sin elegir por el usuario.
- Una **capa de fuente primaria offline**: 110 normas con URL, fecha y hash SHA-256, y 64 fallos
  verificados, más el CCyC Comentado de SAIJ-INFOJUS y las series de índices.
- **Cuatro calculadoras deterministas** sin dependencias externas, que piden el dato que falta en
  lugar de estimarlo y salen con código 2 antes que inventar un número.
- Texto **recuperado por OCR local** en `argentina/fuentes/jurisprudencia/ocr/` para los seis fallos
  cuyo PDF trae la capa de texto arruinada. Es una derivación, no una descarga.
- La marca del repositorio en [`assets/marca/`](assets/marca/).

**Los datos vienen congelados a septiembre de 2026.** `/derecho:estado` dice qué quedó vencido y
`/derecho:actualizar` lo baja de las fuentes oficiales.
