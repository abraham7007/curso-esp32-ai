# Fundamentos de ESP32 + AI

Materiales del curso de la Oficina de Tecnologías de la Información de la
Universidad Nacional de Ingeniería (PIT 2026): **12 sesiones, 322 láminas** en
HTML y los proyectos PlatformIO que se construyen en clase.

## Qué hay aquí

| Carpeta | Qué es |
|---|---|
| `mi-presentacion/` | El sitio de láminas. Vite + Tailwind v4, una página por lámina. **Es lo que se despliega.** |
| `ejemplos/` | Los proyectos PlatformIO terminados de «La hora del código», uno por ejemplo, con su simulación Wokwi y sus diagramas. |

## Poner en marcha el sitio

```bash
cd mi-presentacion
npm install
npm run dev          # http://localhost:5173
```

Otros comandos útiles:

```bash
npm run build                            # genera las 322 páginas
npm run lint                             # biome check .
node tools/check-slides.mjs              # desbordes, consola, figuras, navegación
python3 tools/figures/render.py          # regenera public/figures/*.svg
python3 tools/clases/clase_06.py         # regenera src/slides/clase-06/
```

Dos advertencias que ahorran tiempo: **las sesiones 5 a 12 se generan** desde
`tools/clases/clase_NN.py` y editar su HTML se pierde en la siguiente ejecución;
y **Tailwind solo mira los archivos que existían al arrancar `npm run dev`**, así
que tras crear o renombrar una lámina hay que reiniciar el servidor.

## Despliegue en Vercel

El sitio no está en la raíz del repositorio, así que hay que indicárselo:

- **Root Directory:** `mi-presentacion`
- **Framework Preset:** Vite
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

Vercel detecta Vite solo; lo único que hay que fijar a mano es el *Root
Directory*.

## Proyectos PlatformIO

Cada carpeta de `ejemplos/` es un proyecto independiente para `esp32dev` con el
framework de Arduino y el monitor a 115 200 baudios. Traen su simulación de
Wokwi (`wokwi.toml` + `diagram.json`) y sus diagramas de Excalidraw, de modo que
se pueden seguir sin la placa física.

Al añadir un proyecto nuevo hay que registrarlo como carpeta de primer nivel en
`esp32.code-workspace`, o IntelliSense y la compilación fallan en él.

## Qué no está en el repositorio

Tres exclusiones deliberadas, anotadas también en `.gitignore`:

- **Los bancos de preguntas** (`mi-presentacion/pruebas/`). Traen la respuesta
  correcta de cada ítem.
- **Los PDF de los artículos** (`src/paper/**/*.pdf`). Se conserva el índice con
  los DOI; ver [`src/paper/README.md`](mi-presentacion/src/paper/README.md).
- **Los artefactos regenerables**: `node_modules/`, `.pio/`, `dist/`,
  `.capturas/` y los PDF exportados de las sesiones.

## Licencia

El material del curso es de la OTI-UNI. Cada artículo citado conserva su propia
licencia, y las figuras de las láminas de artículo son elaboración propia a
partir de las cifras publicadas.
