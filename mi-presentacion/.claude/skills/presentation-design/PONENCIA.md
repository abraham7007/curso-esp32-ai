# Especificación general del modo ponencia (vale para todas las sesiones)

Destilada de la sesión 1, que el profesor APROBÓ tras dos rechazos/correcciones. Léela entera.
Proyecto = /Users/mecatronica/Documents/UNI/cursos/esp32/curso-web-esp/mi-presentacion (servidor en http://localhost:5180)
Proyectos reales de los estudiantes: /Users/mecatronica/Documents/UNI/cursos/esp32/ejemplos/NN-*/ (NUNCA los modifiques)

## Qué quiere el profesor
1. Estilo de clase/ponencia, minimalista: una idea por lámina, ~40 palabras proyectadas como máximo
   en láminas de concepto. Título = sintagma nominal descriptivo, sin verbo conjugado ni conclusión
   («Suavizado y retraso de la media móvil», no «La media móvil retrasa la respuesta»), con la
   palabra clave en `<em>` (se pinta en rojo).
2. Sin láminas de papers, sin citas [n], sin glosario ni lámina de referencias (el cierre enlaza solo
   documentación oficial). Sin tiras `.usecases` ni `.practice` visibles.
3. Gráficos y simulaciones donde aclaran algo abstracto o invisible (no en todas). Una simulación
   se queda si muestra algo invisible o temporal, se manipula para sostener la pregunta de
   predicción y se entiende sin leer código.
3b. **Sin código en la explicación** (pedido el 2026-10-17): el curso enseña conceptos, criterios y
   métodos; el código lo escribe el asistente. Pseudocódigo en español, flujos, estados, líneas de
   tiempo, árboles de archivos, arquitectura, formatos de datos y tablas comparativas en lugar de
   listados o líneas de C++. Nombres de función solo como nombre de concepto, sin argumentos.
4. **Que aproveche TODO el espacio.** Rechazó una versión con el contenido «solo al centro».
5. Lo que sale de la pantalla no se pierde: `<aside class="notas">` (ponente, tecla N → ventana
   aparte) y `<details class="detalle"><summary>Para estudiar</summary><div class="detalle__cuerpo">`
   con `<h4>` «En la práctica» (API exacta), «Dónde aparece», «Errores frecuentes» (≤ 120 palabras).

## Ejemplos de referencia — ESTÚDIALOS ANTES DE ESCRIBIR
Sesión 1 aprobada en `src/slides/clase-01/`. Mira especialmente:
- 09-entrada-flotante.html (simulación canvas con lienzo.js, franja de texto + visual a todo el ancho)
- 13-pwm.html, 11-conversion-adc.html (mandos grandes `.mandos`, lecturas tabulares)
- 04-bloques-funcionales.html (animación que hace VER una idea)
- 07-limites-electricos.html (`.cifras` + esquema SVG)
- 17-capas-software.html, 19-cadena-construccion.html, 20-proyecto-platformio.html (diagramas que
  llenan con contenido real, sin doble marco)
- 14-codigo-04-pwm-ledc.html (La hora del código: `ponencia ponencia--trabajo`)
- 23-cierre.html
Estilos: `src/css/ponencia.css` (léelo: composiciones `.escenario` [apilado por defecto: franja de
texto bajo el título, visual a todo el ancho y alto], `.escenario--lado`, `.escenario--solo`,
`.crece`, `.lienzo-caja`, `.enunciado`, `.cifras`, `.puntos`, `.mandos`, `.lectura(s)`, `.control`,
`.franja-fila`…). Motor: `src/js/deck.js` (pasos `data-paso`, evento `paso`), `src/js/lienzo.js`
(`lienzoAdaptable(canvas, (ctx,w,h)=>…)`, `token("--color-x")`).

## Reglas duras (cada una nace de un fallo real ya corregido)
- `<body class="ponencia" data-deck-total="N">`; La hora del código: `class="ponencia ponencia--trabajo"`.
- Llenar el espacio AGRANDANDO EL CONTENIDO (simulación, dibujo, código, cifras), nunca estirando
  cajas vacías, nunca columnas de texto flotando en un vacío, nunca doble/triple marco
  (.card que envuelve tarjetas), nunca iconos pequeños en cajas enormes ni cajas enormes con 6 palabras.
- Texto proyectado ≥ 20 px a 1920×1080 (incluido texto dentro de SVG y canvas).
- Sin barra inferior que repita lo que ya dice la franja de arriba.
- El estado inicial (sin pulsar →) nunca es una lámina vacía o con medio lienzo en blanco; los
  pasos (`data-paso`, máx. 3) revelan en el orden de lectura (izquierda→derecha, arriba→abajo).
- Lecturas numéricas que cambian: `font-variant-numeric: tabular-nums` y ancho mínimo, para que
  los controles no salten.
- Simulaciones: un control principal, estado inicial que ya muestra el fenómeno, ejes con unidades,
  colores por tokens (getComputedStyle), canvas en `.lienzo-caja` con lienzo.js, redibujo al cambiar
  tema; sin bucles decorativos. Comprueba claro y oscuro.
- Corrección técnica verificable: cifras, pines, nombres de API, coherencia entre láminas y con la
  sesión 1. Ante la duda, consulta la documentación oficial (Espressif / Arduino-ESP32 / PlatformIO)
  con WebFetch o quítalo.
- «La hora del código»: estructura canónica (ver SKILL.md §6 y la 14 de clase-01): entregables
  (con los .excalidraw que de verdad tiene el proyecto), Qué debe hacer, Montaje (figuras ≥ 180 px a
  1080p, rótulos ≥ 16 px), Salida esperada **idéntica al printf real del proyecto** (calcula los
  valores), prompt de 4 partes, «Por qué se pide así» (2 frases), «Qué comprueba» (1 frase). Copia
  la estructura de las láminas de código aprobadas de las sesiones 1–3.
- Registro: español técnico, impersonal o 1.ª plural, sin coloquialismos, sin «en el curso», sin
  títulos interrogativos; término inglés en cursiva la primera vez; coma decimal y espacio (3,3 V).
- Sin `style="..."` en línea, sin hex; iconos solo de /course-icons.svg con aria-hidden. Utilidades
  Tailwind solo estándar (el servidor no ve clases arbitrarias de archivos nuevos). Si necesitas CSS
  nuevo, añádelo AL FINAL de src/css/ponencia.css bajo `/* <sesión> agente <X>: … */`, prefijado
  `.ponencia`, sin tocar reglas existentes.
- Agrupaciones con nombre accesible: `<section aria-label>` o `<fieldset>`, no `div role="group"`.
  `for…of` en vez de `forEach` con retorno. Pasa `npx biome check <tus archivos>` sin errores.
- Navegación: cada lámina enlaza anterior/siguiente con la etiqueta corta de la tabla de la sesión;
  la portada usa `a.btn.btn--primary` hacia la 02; la última no lleva «siguiente».

## Verificación obligatoria
```
CLASE=clase-NN node tools/check-ocupacion.mjs <carpeta-capturas> 1920 1080 [NN-x.html …]
CLASE=clase-NN node tools/check-ocupacion.mjs - 1440 900                 # «-» = sin capturas
```
(Requiere el servidor de desarrollo en el puerto 5180: `npx vite --port 5180`.)
Mide la tinta real. Exigido en ambas resoluciones: alto ≥ 88 %, huecos ≤ 6 %, ov 0, sin errores;
visual ≥ 40 % donde haya visual. Luego MIRA cada captura con Read y pregúntate: ¿zonas muertas?
¿cajas vacías? ¿letra pequeña? ¿se entiende la idea en 3 s? ¿estado inicial vacío? Prueba los
controles con Playwright.

## Informe final (≤ 250 palabras)
Tabla por lámina (alto/visual a 1920 y 1440), qué hiciste, dudas técnicas sin verificar.

## Proceso que funcionó (sesiones 1–3)
1. Auditoría de la sesión contra `ejemplos/` (salidas reales carácter a carácter, .excalidraw reales).
2. Plan de láminas (archivo, etiqueta, título descriptivo, visual) y reparto entre 4 grupos:
   conceptos · «La hora del código» · simulaciones · diagramas y cierre.
3. Construcción + `tools/check-ocupacion.mjs` a 1920×1080 y 1440×900.
4. **Revisor independiente** (no escribió las láminas), dos rondas: la primera siempre encuentra
   estados iniciales vacíos, cajas estiradas, letra pequeña y algún error técnico.
5. Los errores de los proyectos de `ejemplos/` se corrigen en el proyecto (con permiso del profesor)
   y en las dos copias del repositorio, compilando con `pio run`.
CSS: lo común en `src/css/ponencia.css`; lo propio de una sesión puede ir en `src/css/clase-NN.css`
importado desde `base.css` (así se hizo la 3).
