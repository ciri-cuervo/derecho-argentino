# Changelog

Historial de **versiones** del plugin. Formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado [SemVer](https://semver.org/lang/es/).

Lleva versiones, no sesiones de trabajo. El detalle de cada cambio vive donde se puede verificar:

| Qué | Dónde |
|---|---|
| Qué cubre cada módulo y cómo está armado el repo | [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) |
| Cuándo se verificó cada instituto contra fuente primaria, y su volatilidad | `argentina/skills/derecho-argentino/references/changelog-normativo.md` |
| Qué hay cargado en la capa offline | `argentina/fuentes/MANIFIESTO.md` |
| La doctrina de cada precedente | El módulo que la usa; el índice, en `references/fallos-csjn.md` |
| Si el texto de un fallo se puede transcribir | `herramientas/lecturas-ocr.json` |

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

**Los datos vienen congelados al 13/09/2026.** `/derecho:estado` dice qué quedó vencido y
`/derecho:actualizar` lo baja de las fuentes oficiales.
