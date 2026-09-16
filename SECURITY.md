# 🔐 Seguridad y reportes

Este repositorio **no es un servicio**. No hay servidor, no hay cuentas, no hay base de datos y no
recibe datos de nadie: es una skill que se instala y corre localmente, con texto de normas y fallos
al lado. Eso hace que la superficie de riesgo sea chica y distinta de la de una aplicación web, así
que conviene decir qué es lo que sí importa acá.

## Lo que más daño hace en una herramienta jurídica

**Un error de derecho silencioso.** Un plazo mal contado, una norma derogada citada como vigente,
un fallo atribuido a una sala que no lo dictó. No es una vulnerabilidad en el sentido informático,
pero **es el daño real de este proyecto**: alguien presenta un escrito con un dato equivocado.

Todo el diseño del repositorio está orientado a eso —fuente primaria con hash, marcadores de
verificación, tests que comparan las afirmaciones de la documentación contra el disco— y aun así
puede fallar. **Si encontrás uno, reportalo: es la contribución más valiosa que existe acá.**

- **Público**, que es lo preferible: abrí un [issue](../../issues) con qué contestó la skill, qué
  debería haber contestado y **la fuente** —artículo, fallo con carátula y fecha, o Boletín
  Oficial—. Con la fuente se corrige y queda un caso de prueba; sin la fuente es una opinión.
- **En privado**, si por algún motivo no querés publicarlo: ver abajo.

## Vulnerabilidades en el código

Los scripts son Python de biblioteca estándar y hacen tres cosas con el mundo exterior: **piden
páginas por HTTPS** a sitios oficiales, **escriben archivos** dentro del repositorio y **leen PDF**
con `pdftotext` y `tesseract`. Ahí es donde puede haber algo:

| Superficie | Qué mirar |
| --- | --- |
| Descargadores (`derecho/fuentes/scripts/`) | Escritura fuera del árbol previsto, redirecciones a otro host, tamaño sin límite |
| Lectores de PDF (`herramientas/reocr_jurisprudencia.py`, `calidad_ocr.py`) | Un PDF preparado para explotar el binario externo |
| Resolución de rutas (`_raiz.py`) | Que una variable de entorno haga leer o escribir fuera del repositorio |

**Lo que el proyecto se compromete a no hacer:** ejecutar código descargado, desactivar la
verificación TLS, pedir credenciales, ni mandar nada a ningún servidor. Si ves cualquiera de esas
cuatro cosas en el código, es un bug de seguridad por definición.

## Cómo reportar en privado

Usá **[Private vulnerability reporting](../../security/advisories/new)** de GitHub, que abre un
canal privado con el mantenedor y no queda público hasta que se resuelva.

**Qué esperar:** esto lo mantiene una persona, no un equipo. No hay compromiso de tiempo de
respuesta ni programa de recompensas. Lo que sí hay es que se lee, se contesta y, si corresponde,
se corrige y se acredita a quien lo reportó.

## Datos de expedientes: la regla que aplica a todos

> [!IMPORTANT]
> **El repositorio es público.** Nunca subas —ni en un issue, ni en una discusión, ni en un caso de
> prueba— carátulas, partes, montos, liquidaciones ni piezas de un expediente real. Para mostrar un
> problema alcanza con inventar el caso, y es exactamente lo que hace este repositorio en sus
> propios [casos de prueba](derecho/evals/).

`derecho/fuentes/_local/` está en `.gitignore` y es donde el abogado deja ejemplares de obras
comerciales con derechos reservados. **No se commitea nada de ahí.**

**Si algo se filtró igual** —tuyo o de un tercero— avisá por el canal privado de arriba y se saca.
Tené en cuenta que este repositorio se publica **con un solo commit y se reescribe con `--amend`**,
así que un dato borrado no queda en el historial; lo que sí puede quedar es una copia en la caché
de GitHub o en un fork ajeno.

## Licencias, que es lo otro que se reporta acá

Si creés que un archivo está bajo la licencia equivocada, o que hay texto de un tercero donde no
corresponde, el mapa completo está en [`LICENCIAS.md`](LICENCIAS.md) y la frontera se vigila con
`herramientas/fuga_textual.py` y `herramientas/frontera_kb.py`. Un reporte de ese tipo va por
issue, salvo que involucre datos personales.

---

[Volver al README](README.md) · [Mapa de licencias](LICENCIAS.md) ·
[Cómo está armado](docs/ARQUITECTURA.md)
