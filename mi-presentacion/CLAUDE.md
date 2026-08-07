# mi-presentacion — el curso en láminas

12 sesiones, 322 láminas HTML autónomas servidas con Vite + Tailwind v4.

## Las reglas no están aquí

Tipografía, composición, los siete bloques de contenido, iconografía, registro de
redacción y anti-patrones viven en **`.claude/skills/presentation-design/SKILL.md`**,
que se carga solo al trabajar bajo `src/slides/`. Este archivo no las repite a
propósito: dos copias de la misma norma se desincronizan.

Aquí solo está lo operativo.

## Comandos

```
npm run dev                              # servidor de desarrollo (localhost:5173)
npm run build                            # las 322 páginas + presentar.html
npm run lint                             # biome check .
node tools/check-slides.mjs              # todas: desbordes, consola, figuras, navegación
node tools/check-slides.mjs clase-02     # una sesión
node tools/check-slides.mjs --shot clase-02/09   # + captura en .capturas/
python3 tools/figures/render.py          # regenera public/figures/*.svg
python3 tools/clases/clase_06.py         # regenera src/slides/clase-06/
```

## Tres trampas que cuestan tiempo

1. **Sesiones 5 a 12 se generan.** Su fuente es `tools/clases/clase_NN.py`; editar el HTML se pierde en la siguiente ejecución. Las sesiones 1 a 4 sí se escriben a mano.
2. **Tailwind solo mira los archivos que existían al arrancar `npm run dev`.** Si se crea o renombra una lámina, hay que reiniciar el servidor antes de verificar, o las utilidades no generan regla y una composición correcta se ve rota. `npm run build` no sufre esto.
3. **Nunca renumerar a mano.** `node tools/renumber.mjs plan.json` renombra, reescribe los enlaces anterior/siguiente y corrige `data-deck-total`. Al cambiar el título de una lámina, hay que actualizar también las etiquetas entrantes de sus vecinas, que llevan la forma corta del título.

## Estructura

```
src/slides/clase-NN/    las láminas (01-portada … NN-referencias)
src/css/                variables · slides · components · animations · base
src/paper/clase-NN/     los PDF de acceso abierto de cada sesión
public/course-icons.svg juego de iconos monocromo (nunca un mapa de bits)
public/figures/         SVG generados por tools/figures/render.py
tools/                  generadores, auditorías y verificadores
export/                 los PDF de las 12 sesiones
pruebas/                bancos de preguntas GIFT + Apps Script
```

Después de tocar `variables.css`, `slides.css` o `components.css` hay que correr
`node tools/check-slides.mjs` **entero**: un cambio global rompe el encaje de
láminas que nadie estaba mirando.
