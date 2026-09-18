# Disciplina de medición para herramientas y tests

Rige siempre: carga al abrir la sesión. Lo que trae se aplica al tocar una herramienta, un descargador o un test.

## Cómo se mide, y cómo fallan las medidas

**Una medida que se equivoca sobre un caso conocido no sirve para los desconocidos: se descarta, no
se calibra.** Cuando no haya medida confiable, se lee y se registra el veredicto, con fecha y con
lo que se vio.

Las alarmas fallan de dos maneras, y las dos se buscan a propósito:

- **La que suena siempre** se calla con `--fijar` o se deja de mirar, y ahí se pierde el cambio real.
- **La que no suena nunca** reporta verde con el instrumento apagado. Es la peor: da confianza.

Si una herramienta no puede medir —falta un binario, falta una fuente— **lo dice y se planta**. No
hay verde por ausencia de instrumento.

**Después de agregar un guardarraíl, comprobalo con una mutación**: reintroducí el error que
debería atrapar y confirmá que falla. Dos cosas que se aprenden rompiéndolas:

- **A veces hay que mutar el alcance del control, no un archivo.** A las clases de letras de los
  regex les faltaba la `Ü`, así que `[VERIFICAR ANTIGÜEDAD: ...]` no era ni candidato: el control
  lo ignoraba en silencio y todo daba verde.
- **Un guardarraíl sólo cubre lo que su fixture ejercita.** Una nota que se imprime únicamente
  cuando el plazo cruza a otro año no está cubierta si el caso de prueba no lo cruza.

**Una frase de docstring que afirma cobertura tampoco se escribe de memoria.** Decir qué atrapa
un guardarraíl es una afirmación sobre el comportamiento, y ahí rige «del producto no se concluye
el proceso»: no se escribe hasta haber visto fallar la mutación que la respalda, y la mutación se
nombra en el mismo docstring. Así queda escrito qué hay que volver a romper cuando el control
cambie. Sin eso la frase dice lo que el guardarraíl quería hacer, y lo peor es la que manda a
otro archivo: el lector da el hueco por tapado y no va a mirar.

**Antes de reformatear en masa, buscá quién parsea eso.** Buena parte de las medidas de este
repositorio salen de leer los `.md` con un regex, así que un cambio de forma que a la vista no dice
nada les cambia la entrada. Y el parser no protesta: sigue, lee otra cosa y **reporta cero**. Pasó
con el relleno de las filas de tabla y `pendientes.py`.

Los archivos que la mutación necesite crear van al scratch de `/tmp`, porque adentro del repo **no
se pueden borrar**. Cuando la mutación tenga que estar adentro para que el guardarraíl la vea,
moverla a `_to_delete/` **en el mismo acto**, y avisar de `rm -rf _to_delete` antes de commitear.
