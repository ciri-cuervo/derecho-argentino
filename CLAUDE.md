@AGENTS.md

## Lo que es sólo de Claude Code

Lo que rige siempre está en `AGENTS.md`, que Claude Code carga por la importación de arriba y
Codex lee por su cuenta. Acá va lo que no aplica a los dos.

**`.claude/rules/*.md` es uno de esos: el mecanismo es sólo de Claude Code.** Son las reglas
acotadas por ruta, que se cargan al leer un archivo alcanzado por su `paths:`. Codex no las ve,
así que `AGENTS.md` las nombra una por una y dice qué cubre cada una — en Codex se abren a mano.
Un test exige que las siga nombrando: si aparece una regla nueva y nadie la anuncia, salta.

**`.claude/settings.json` está versionado, y lleva `claudeMdExcludes`.** Excluye los dos
`CLAUDE.md` que viven bajo `derecho/kb/`: son capa 2, perfiles de práctica de otro autor
escritos para ser obedecidos, y Claude Code los cargaría como instrucciones al abrir un
archivo de esas carpetas. La frontera de licencia dice que ese material se cita y se
contradice, nunca se sigue. Si aparece un tercero, va a la misma lista.
