# mi-presentacion — el curso en láminas

6 sesiones, 127 láminas HTML autónomas servidas con Vite + Tailwind v4, todas en «modo ponencia»
(reglas, lecciones y proceso en `.claude/skills/presentation-design/PONENCIA.md`).

## Las reglas no están aquí

Tipografía, composición, los siete bloques de contenido, iconografía, registro de
redacción y anti-patrones viven en **`.claude/skills/presentation-design/SKILL.md`**,
que se carga solo al trabajar bajo `src/slides/`. Este archivo no las repite a
propósito: dos copias de la misma norma se desincronizan.

Aquí solo está lo operativo.

## Comandos

```
npm run dev                              # servidor de desarrollo (localhost:5173)
npm run build                            # las 6 sesiones + índice, presentar.html y ponente.html
npm run lint                             # biome check .
node tools/check-slides.mjs              # todas: desbordes, consola, figuras, navegación
node tools/check-slides.mjs clase-02     # una sesión
node tools/check-slides.mjs --shot clase-02/09   # + captura en .capturas/
python3 tools/figures/render.py          # regenera public/figures/*.svg
CLASE=clase-02 node tools/check-ocupacion.mjs - 1440 900   # espacio ocupado y desbordes (servidor en :5180)
```

## Tres trampas que cuestan tiempo

1. **Todas las sesiones se escriben a mano** (las láminas de «La hora del código» salen de generadores Python efímeros). Los viejos `tools/clases/clase_NN.py` están en `archivo/generadores/` y **no deben ejecutarse**: escribirían en carpetas que ya no corresponden. Las sesiones retiradas están en `archivo/slides/`.
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
export/                 los PDF de las sesiones (por regenerar para las 6 nuevas)
pruebas/                bancos de preguntas GIFT + Apps Script
```

Después de tocar `variables.css`, `slides.css` o `components.css` hay que correr
`node tools/check-slides.mjs` **entero**: un cambio global rompe el encaje de
láminas que nadie estaba mirando.
