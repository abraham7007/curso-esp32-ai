# Curso «Fundamentos de ESP32 + AI» — mapa del espacio de trabajo

Materiales del curso de la OTI-UNI (PIT 2026). Esto **no es un repositorio git**:
no hay historial ni forma de deshacer. Antes de mover, sobrescribir o borrar algo,
mirar qué hay dentro y confirmarlo.

## Qué es cada carpeta

| Carpeta | Qué es | Se edita |
|---|---|---|
| `mi-presentacion/` | **El curso actual.** 6 sesiones en láminas HTML + sus herramientas. Es donde se trabaja. Lo retirado está en `mi-presentacion/archivo/`. | Sí |
| `metodologia-curso/` | Kit portátil para arrancar un curso **de otro tema**: sistema de diseño, 17 herramientas genéricas y `METODOLOGIA-DE-CURSO.md`. Autocontenido a propósito. | Solo al mejorar el método |
| `ejemplos/` | Los proyectos PlatformIO terminados que el estudiante construye en «La hora del código». Uno por ejemplo. | Sí |
| `borrador ejemplos/` | Pruebas desechables (`prueba1`…`prueba8`) previas a los ejemplos definitivos. **El material del estudiante nunca cita estos nombres.** | No |
| `Edición 10/` | Fuente autorizada del curso: `Temario_ESP32_AI_Edicion_10.docx` (qué cubre cada sesión), `GUIA-DE-PRESENTACIONES.md` y los borradores HTML antiguos. | No, es referencia |
| `Edición 9/` | Archivo de la edición anterior: PDF y bancos de preguntas GIFT. | No, es histórico |

## Rutas que se confunden

- Las láminas están en **`mi-presentacion/src/slides/clase-NN/`**, no en `src/slides/` desde la raíz. Es el error más frecuente al dar una ruta.
- `mi-presentacion/dist/` es salida de compilación. Editar ahí no sirve: se regenera con `npm run build`.
- `Edición 10/Clase NN - .../*.html` son los borradores **viejos**. Sirven de referencia de profundidad, nunca para copiar literal.

## Las dos fuentes de reglas, y cuál manda

1. `mi-presentacion/.claude/skills/presentation-design/SKILL.md` — las convenciones de **este** curso. Se carga sola al tocar `mi-presentacion/`. **Manda sobre todo lo demás.**
2. `metodologia-curso/METODOLOGIA-DE-CURSO.md` — el método general, independiente del tema. Disponible como skill en `.claude/skills/curso-en-diapositivas` (enlace simbólico al kit, no una copia).

Cuando se contradigan, gana la primera: un curso concreto tiene decisiones que el método general no puede prever.

## Proyectos PlatformIO

Cada carpeta de `ejemplos/` es un proyecto independiente (`esp32dev`, framework Arduino, monitor a 115 200 baudios) con su simulación Wokwi (`wokwi.toml` + `diagram.json`) y sus diagramas Excalidraw.

**Al crear un proyecto nuevo hay que registrarlo como carpeta de primer nivel en `esp32.code-workspace`**, o IntelliSense y la compilación fallan en él.
