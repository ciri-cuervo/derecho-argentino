# Changelog

Historial de **versiones** del plugin. Formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado [SemVer](https://semver.org/lang/es/).

Lleva versiones, no sesiones de trabajo, y **cada entrada va corta**: una línea de encuadre y
un renglón por cambio. El detalle de cada uno vive donde se puede verificar:

| Qué | Dónde |
| --- | --- |
| Qué cubre cada módulo y cómo está armado el repo | [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) |
| Cuándo se verificó cada instituto contra fuente primaria, y su volatilidad | `derecho/skills/derecho-argentino/references/changelog-normativo.md` |
| Qué hay cargado en la capa offline | `derecho/fuentes/MANIFIESTO.md` |
| La doctrina de cada precedente | El módulo que la usa; el índice, en `references/fallos-csjn.md` |
| Si el texto de un fallo se puede transcribir | `herramientas/lecturas-ocr.json` |

## [1.2.0] — 2026-09-17

Se destrabaron los dos registros judiciales que el repositorio daba por inconsultables, y de ahí
salió casi todo lo demás.

- **JUBA y el buscador de sumarios de la CSJN se consultan**, con la cadena escrita en `INDICE.md`.
- **Dieciséis ramas nuevas** entraron como sección de un módulo que ya existía, con su disparador.
- **Los textos ordenados de 2025 renumeraron gas y electricidad:** la jurisdicción previa del ente
  pasó del art. 66 al 53 y del art. 72 al 58, y el corrimiento no es parejo.
- **La LCT no rige a todos:** `liquidacion_lct.py` corta con código 2 ante `--empleador publico`.
- **Los datos se repiten antes de usarlos** y la skill para si alguno no coincide.
- **Identidad de los fallos:** el descargador coteja la carátula contra el documento y la registra.
- **El cotejo del OCR es un dato:** vive en `ocr/correcciones/` y se planta si deja de coincidir.
- **Políticas de género:** ocho leyes bajadas y escritas en siete módulos.
- **Normas huérfanas:** herramienta nueva para el texto bajado que ningún módulo usa. Hoy da cero.
- **Herramientas nuevas:** ortografía con diccionario, mapa de ruteo y verificador de marcadores.
- **Ninguna fuente oficial bloquea a los descargadores**, y eso ahora se mide antes de suponerlo.

## [1.1.1] — 2026-09-15

Procedencia y rutas internas: no entran normas ni fallos nuevos y ningún cálculo cambia de
resultado. **No hay nada que reinstalar.** Cada archivo bajado se coteja contra su propio hash sin
salir a la red, y de un fallo de JUBA se guarda la sentencia y no la página entera.

## [1.1.0] — 2026-09-15

Entra derecho nuevo: un módulo, **10 normas** bajadas y **6 fallos** leídos contra el documento.

- **Derecho internacional privado**, módulo nuevo: arts. 2594 a 2612, sin la parte especial.
- **Familia:** compensación económica y gestación por sustitución pasan a tener precedente propio.
- **Salario mínimo, vital y móvil** con sus ocho tramos, y los topes en SMVM remiten ahí.
- **De dónde sale un fallo:** lo que no viene del registro del tribunal lo declara `fallos.json`.
- La emergencia de la **Ley 14.407 de PBA** está vencida desde octubre de 2016.
- **[`docs/COBERTURA.md`](docs/COBERTURA.md):** qué ramas cubre el repositorio, para decidir por
  dónde crece.

## [1.0.2] — 2026-09-15

Íconos, banners y metadatos de marketplace, para los dos envoltorios: Claude Code y Codex.

## [1.0.1] — 2026-09-15

Correcciones: no entran normas ni fallos nuevos y ningún cálculo cambia de resultado.

- **Ortografía:** si se muestra se acentúa, si se compara no. Las carátulas, contra el documento.
- **Fechas:** las del derecho con día y mes; las del propio trabajo, por mes.
- **Títulos de las constituciones provinciales** en `normas.json`.
- **Si falta Python, la skill no calcula a mano:** emite el marcador y explica cómo instalarlo.
- La salida entra en la consola de Windows, donde un `→` cortaba el script ya habiendo escrito.
- Control nuevo de las cifras de inventario, con `herramientas/cifras.py`.

## [1.0.0] — 2026-09-14

Versión inicial.

Plugin de análisis, redacción y revisión jurídica bajo derecho argentino. Primera versión
publicable de un proyecto en desarrollo: la cobertura auditada crece módulo por módulo. Trae:

- La skill `derecho-argentino`: 30 módulos con numeración global estable, en dos modos de entrada.
- **Ocho comandos slash** y un perfil que ordena las preguntas sin elegir por el usuario.
- **Capa de fuente primaria offline:** 110 normas con hash SHA-256 y 64 fallos verificados, más el
  CCyC Comentado de SAIJ-INFOJUS y las series de índices.
- **Cuatro calculadoras deterministas**, que salen con código 2 antes que inventar un número.
- Texto **recuperado por OCR local** para los seis fallos con la capa de texto arruinada.
- La marca del repositorio en [`assets/marca/`](assets/marca/).

**Los datos vienen congelados a septiembre de 2026.** `/derecho:estado` dice qué quedó vencido y
`/derecho:actualizar` lo baja de las fuentes oficiales.
