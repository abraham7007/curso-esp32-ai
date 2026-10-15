---
name: presentation-design
description: Design principles and content rules for building the ESP32 + AI course slides (PIT 2026 / OTI-UNI) as standalone HTML files — typography, layout, animation, the six content-block types, iconography, terminology, and anti-patterns. Use whenever creating or editing a file under src/slides/.
---

# Presentation design — Fundamentos de ESP32 + AI, Edición 10

This project rebuilds the course's slide decks (one folder per session, migrated from
`Edición 10/`) as standalone HTML files in `src/slides/`, styled with the design system in
`src/css/` (`variables.css`, `slides.css`, `animations.css`, `components.css`) plus Tailwind
CSS v4 utilities for one-off layout. Always reuse those tokens and classes instead of
hardcoding new colors, spacing, or fonts.

The audience is the student — projected in class and reviewed later on their own. It is not
a script for the instructor and not a planning document. **If an element only serves to
organize the class, it does not belong on a slide.**

Source content comes from `Edición 10/Temario_ESP32_AI_Edicion_10.docx` (the authoritative
list of what each session must cover) and the existing `Edición 10/Clase NN - .../*.html`
drafts (useful as a reference for depth and for concrete numbers/examples — but **do not
copy them literally**: the point of this rebuild is a more professional, more interactive,
higher-quality version of the same content, in this design system).

## Modo ponencia (octubre 2026) — manda sobre las reglas de densidad de abajo

Decisión del profesor tras ver el mazo proyectado: era demasiado cargado. Las
sesiones rehechas (**las 6**) usan `<body class="ponencia">` y
`src/css/ponencia.css`. En ellas:

- **Una idea, ~40 palabras proyectadas** por lámina de concepto. Título = sintagma
  nominal que dice de qué trata la lámina, sin verbo conjugado ni conclusión
  («Publicación y suscripción por temas en un broker», no «El broker entrega cada
  mensaje según su tema»), con la palabra clave en `<em>` (se pinta en rojo), en IBM
  Plex Sans. Criterio de la skill `correccion-anti-ia`, pedido por el profesor.
- **Sin papers** ni citas `[n]`, sin glosario ni lámina de referencias: el cierre
  enlaza solo documentación oficial. Sin tiras `.usecases` ni `.practice` visibles.
- Lo que sale de la pantalla cambia de capa: `<aside class="notas">` (tecla N, notas
  del ponente, con una pregunta de predicción) y `<details class="detalle">` «Para
  estudiar» (tecla D: En la práctica, Dónde aparece, Errores frecuentes).
- Revelado por pasos con `data-paso="N"` (→ / espacio; ← vuelve; la lámina previa
  se abre con `#fin`). Las simulaciones pueden escuchar el evento `paso`.
- Composiciones: `.escenario`, `.enunciado`, `.cifras`, `.puntos`, `.control`,
  `.lectura`, `canvas.lienzo`. Simulación solo donde el concepto es invisible y
  cabe en un control (entrada flotante, ADC, PWM, pulso de servo, arranque).
- «La hora del código» conserva su estructura y usa `ponencia ponencia--trabajo`
  (escala de lectura cercana). Su salida esperada debe ser **la que imprime el
  proyecto real** de `ejemplos/`, verificada contra el `printf`.
- Comprobación: `tools/check-slides.mjs` mide a 1440×900 con BASE 5173; revisar
  además a 1920×1080.

Reglas completas, lecciones de las revisiones y proceso: **`PONENCIA.md`** (en esta carpeta).

El curso pasa a 6 sesiones (1 hardware/GPIO/ADC/PWM/entorno · 2 C++ modular ·
3 UART/I²C/JSON · 4 WiFi y APIs HTTP · 5 plataformas IoT con Blynk · 6 IA en el
borde). La numeración «Ejemplo NN» sigue la de las carpetas de `ejemplos/`
(04b incluido), no la antigua de 51 ejemplos.

## Typography

- Two typefaces, one job each: `var(--font-display)` (IBM Plex Mono) for
  headings, `var(--font-mono)` for eyebrows/labels/code, `var(--font-sans)`
  (IBM Plex Sans) for everything else. Never introduce a third family.
- **The scale lives in `variables.css`, nowhere else.** `--fs-eyebrow`,
  `--fs-title`, `--fs-title-sm`, `--fs-lede`, `--fs-h3`, `--fs-body`,
  `--fs-small`, `--fs-micro`. Never write a `text-[clamp(...)]` utility for a
  headline: 80 of those existed once and produced titles that differed by
  0.05rem between slides for no reason. If a slide truly needs a size the
  scale doesn't have, add it to the scale.
- **Role = size + colour + family, not size alone.** At projector distance two
  consecutive levels that share a colour read as one block. The assignment is
  written at the top of the hierarchy section of `slides.css`:
  eyebrow (mono, accent red), title (mono, near-black), lede (sans, muted),
  h3 (mono, institutional navy), body (sans, text), support (sans, muted).
- One `h1` per slide: `.slide__title`, or `.slide__title--sm` when the slide
  carries dense content and the title must not eat a third of the height.
  Most concept slides want `--sm`.
- The framing sentence under the title is `.slide__lede`. Its first clause can
  go in `<strong>` to anchor the eye; that is the only bold allowed there.
- Prefer fewer, larger words over dense paragraphs. A slide is read in
  seconds, not studied like a document.
- Icons are sized in `em` so they track their text (`.icon` = 1.45em). Where an
  icon sits next to a small-caps label, give it an explicit `rem` size instead
  — inheriting the label's `em` makes it disappear.
- Register is technical documentation, not general audience: precise, sober,
  domain terminology. See **Terminology** below — simplifying vocabulary does
  not help learning; defining each term once and then using it rigorously does.

## Layout

- Every slide is a `<main class="slide">`: fixed at `100vw × 100dvh` (not
  `100vh` — `dvh` avoids mobile browser-chrome jumps). Don't override this
  sizing per-slide.
- One idea per slide. If content needs two headlines, it's two slides. A
  slide that needs scrolling to read is not a slide.
- `.slide__content` is **the physical sheet**: it draws the raised panel
  (border, inner light edge, contact shadow, drop shadow) and always claims
  the full free height, so two consecutive slides never show frames of
  different size. The padding of `.slide` around it is the dead zone reserved
  for the fixed chrome — progress bar and buttons above, prev/next strip
  below — which is why content can never collide with a button.
- When a slide is one block that already has its own frame (La hora del
  código), add `.slide__content--flush`: the panel styling is dropped so
  there aren't two concentric frames, and the inner block takes over the
  relief.
- Pick a composition explicitly instead of stacking everything in one column:
  `.layout--split` (text 32 / visual 68), `--split-even`, `--wide-left`,
  `--thirds`, `--focus`, `--code-pair`. A vertical stack of four blocks is
  almost always the wrong answer on a 16:9 sheet.
- Default alignment is centered (`.slide`); use `.slide--start` for
  left-aligned, top-anchored content (definitions, comparisons, code panels,
  tables — most concept slides).
- Use the `--space-*` scale (`variables.css`) or Tailwind's spacing utilities
  for gaps and padding — never a bare pixel value.
- Leave breathing room. Err on the side of more whitespace, not less;
  cramped slides are the most common failure mode.

## Animation

- Motion should orient the eye to what matters first, not decorate. Default
  to `data-animate="fade-up"` on the 2-4 elements that should draw attention
  in sequence.
- Wrap a group in `.stagger` to auto-delay each child via CSS `nth-child` —
  never hardcode delays with inline `style`.
- Keep entrance animations short (`animations.css` defaults to `0.6s` with an
  ease-out curve). Slower reads as sluggish, not elegant.
- Everything in `[data-animate]` already respects
  `prefers-reduced-motion: reduce` — don't build animations that bypass it.
- Animate at most one property group (opacity + transform) per element. Avoid
  combining fades, rotations, and color shifts on the same element.

## The six content blocks (GUIA-DE-PRESENTACIONES.md §4)

Every concept slide is built from these. Use the shared classes — don't invent
one-off equivalents.

1. **Definición** (`.def` + `.def__label`). Every new idea opens with a short,
   literal definition in a highlighted box, before any detail. One or two
   sentences, no chained subordinate clauses, no term that hasn't been defined yet.
2. **Ejemplo básico** (`.example` + `.example__label`). Immediately after the
   definition: a small, concrete case with real numbers — components the
   student will actually use, nothing hypothetical.
3. **Simulación interactiva**. A manipulable element with at least one control
   (slider, button, checkbox, selectable region). Build it with
   `.picker`/`.picker__item` + `.detail-panel` for select-and-inspect diagrams,
   `.controls` + `input[type=range]` + `.readout`/`.metric` for
   parametric simulations, and always close with `.sim-caption` explaining
   *what the simulation shows*, written as description — never as an
   instruction to the reader ("Consigna: mueva el deslizador..." is banned,
   see Anti-patterns). Required: labeled axes with units, a numeric scale (not
   just curve shape), each signal identified by color, values that appear on
   screen when the simulation demonstrates a measurement, and a correct
   initial state before any interaction.
4. **Comparación** (`.compare` + `.compare__panel`, or a `table`). Two
   alternatives set against each other, always closed with an explicit
   `.conclusion` block stating **which one is chosen and why** — never just
   the differences.
5. **Bloque de código explicativo** (`.codepanel` + `.codepanel__header` with
   a `.codepanel__tag`/`.codepanel__tag--si`/`.codepanel__tag--no`). Shown to
   explain a concept, never to be transcribed. Tag it `PARA ENTENDER EL
   CONCEPTO`, `COMPARACIÓN`, `ASÍ NO`, or `ASÍ SÍ`. May be incomplete or
   simplified if noted with a comment. Never contains instructions like
   "escribe esto en tu editor." Use `.hl--hit` / `.hl--add` to highlight the
   relevant line(s). Terminal/serial output goes in `.term` (inside or outside
   a `.codepanel`).
6. **La hora del código** (`.code-hour`). Proposes an example to implement in
   VS Code during class. **Never contains the code itself** — only what to
   build, how to ask for it, and what must come out. Canonical structure, in
   this order (see `clase-01/06-codigo-01-salida-digital.html`):

   - The slide is `.slide__content--flush`: this block *is* the sheet.
   - `.code-hour__header` → `.code-hour__ref` = `Ejemplo NN`, **continuous
     numbering across all 12 sessions**, never resets, two digits.
   - `.code-hour__title` — what gets built, in plain words ("El brillo de un
     LED gobernado por el potenciómetro"), not a spec-sheet noun phrase.
   - `.deliverables` — the three artefacts the student ends up with. This is
     the contract of the exercise and it comes *before* the prompt, because
     the prompt is only the way to ask for them:
     **Proyecto** (`i-project`), **Simulación** (`i-simulate`, `--sim`),
     **Diagrama** (`i-diagram`, `--diagram`).
   - `.code-hour__body--pair` — left `.code-hour__stack` with
     **Qué debe hacer** (`i-target`), **Montaje** (`i-plug`, GPIO number *and*
     peripheral function, plus the `@wokwi/elements` parts in a `.hw-set`) and
     **Salida esperada** (`i-terminal`, the real serial trace verbatim in
     `.term`); right, the prompt.
   - `.code-hour__why` — the concept the example verifies.

   **The prompt (`.prompt-box`) has four numbered parts, always these:**

   1. **Proyecto.** Create a *new PlatformIO project* for `esp32dev` with the
      Arduino framework. Never "en src/main.cpp": half the failures of the
      first sessions are the declared board or the port, not the code, and
      starting from a file hides that entirely.
   2. **Firmware.** What it must do, with the exact trace format fixed and the
      forbidden shortcuts named.
   3. **Simulación.** Add the Wokwi simulation to the same project, wired as
      the Montaje section shows, so the student can keep going when the board
      fails or is not at hand.
   4. **Diagrama.** An Excalidraw diagram that *complements this specific
      example*. Choose the kind by what the example teaches: flow when the
      point is control (`setup()` vs `loop()`), circuit when the cause is
      electrical, block chain when the point is a data path, comparison when
      the point is two magnitudes side by side.

   `.prompt-note` then answers **"por qué se pide así"** — every constraint in
   the prompt must have a stated reason. That paragraph is what teaches
   specifying, which is the actual skill; the code is the by-product.
   deck.js adds a copy button to every `.prompt-box` automatically.

   - Extension: implementable in 5-10 minutes of assisted coding. If it
     extends a previous example, say which one and what it adds.
   - Serial traces are identified by module
     (`[ADC] canal=4 codigo=2048 v=1.650`).
   - Minimum 4 "La hora del código" slides per session, distributed across
     both temas — never all bunched at the end.

Two more reusable blocks: `.glossary-item` (term + English equivalent in
`.glossary-item__en` + short definition) for the closing glosario slide, and
`.problem-card` (`__head` + `__body`) for the "problemas frecuentes" slide —
each one states symptom, cause (`Por qué ocurre`), and how to confirm it
(`Cómo comprobarlo`).

### A 7th block: En la práctica (`.practice` + `.practice__label`)

Added on top of the original guide after direct user feedback: concept slides
were reading as generic ("SoC vs. microcontroller", "what a floating input
is") without landing on what the student will actually type. **Every concept
slide that has an ESP32-specific API, header, or library behind it must
include a `.practice` block after its `.def`/`.example`**, naming the exact
function(s), header, or library — not just "se puede leer con el ADC" but
`analogRead(pin)` (núcleo de Arduino, sin librería adicional). If a concept is
purely architectural with no direct API (SoC classification, chip vs. módulo
vs. placa, memory hierarchy as a concept), it's fine to omit `.practice` — don't
force one where there's nothing concrete to name. When in doubt, ask: "if a
student opens VS Code right now, what do they type because of this slide?" —
if there's an answer, it belongs in a `.practice` block, not buried in prose.

## Iconography

Fixed monochrome SVG set at `public/course-icons.svg` — never a bitmap image,
never an icon invented outside this set. Reference with:

```html
<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#i-chip"/></svg>
```

`aria-hidden="true"` is required on every one of these — they always sit next
to a visible text label (title, block label), so they're decorative to
assistive tech and Biome's `noSvgWithoutTitle` rule requires either a
`<title>` or `aria-hidden`. Never add a `<title>` to these instead; that's for
the one or two large standalone diagrams (SoC block diagram, pin map) that
have their own `role="img"` and `aria-label`.

Available: `i-chip`, `i-bolt`, `i-clock`, `i-wave`, `i-folder`, `i-layers`,
`i-link`, `i-terminal`, `i-keyboard`, `i-target`, `i-bulb`, `i-alert`,
`i-check`, `i-book`, `i-plug`, `i-flow`, `i-cpu`, `i-sliders`. Icons accompany
titles and block labels — never used loose as decoration. Use `.icon--lg` for
larger contexts (portada goals, section headers).

## Components

- Reach for `.card`, `.badge`, `.btn` (`.btn--primary` / `.btn--secondary`)
  and the content blocks above before writing new component CSS. Compose them
  with Tailwind utilities for spacing/grid, don't restyle their core look.
- Use `var(--color-*)` tokens (or Tailwind's generated `bg-accent`,
  `text-navy`, etc. from the same `@theme` block) for any color — this is
  what makes dark mode (`prefers-color-scheme`) work for free.
- Institutional palette (fixed, do not change): `--color-accent` is red
  `#C8102E` (Tema A, La hora del código, primary emphasis); `--color-navy` is
  blue `#1F3864` (definitions, Tema B, secondary emphasis). Both are
  intentional and both are used — this is not the "one accent color" rule
  from a generic design system.
- Semantic status colors are separate from the brand pair: `--color-ok` /
  `--color-warn` / `--color-danger` (+ their `-soft` backgrounds) for
  simulation states, pin classifications, problem cards.

## Terminology (GUIA-DE-PRESENTACIONES.md §7)

- Domain terms are introduced with a definition and their English equivalent
  in parentheses the first time they appear (e.g. "firmware", "toolchain",
  "pull-up", "backtrace") — that's how they appear in the datasheet and in
  Espressif's documentation.
- Short, affirmative sentences. One idea per sentence. Titles as technical
  noun phrases ("Jerarquía de memoria y persistencia"), not questions or
  colloquial framing ("Dónde vive cada cosa").
- No analogies or metaphors: describe the real mechanism and cite the
  governing parameter. No colloquialisms, no "no es X, es Y" constructions,
  no emotional-reinforcement phrases ("lo importante aquí es...").
  Explanations are third person or first-person plural ("el receptor
  muestrea", "vamos a construir") — never a direct order to the reader.
  Numbers carry units and, where relevant, tolerance.
- Opening questions pose an engineering problem, not a curiosity or a
  narrated anecdote.
- **"Montaje", not "conexionado".** *Conexionado* is Peninsular industrial
  jargon and reads stiff to a Latin American engineering student; *montaje*
  is the ordinary word for assembling a circuit. Same rule for the section
  headings of La hora del código: "Qué debe hacer" beats "Especificación",
  which reads like a procurement document.
- **A literal calque is an error, even when it is understandable.** Translate
  into the term the Spanish-speaking field actually uses, not the nearest-
  looking word: `merge the flash image` → **componer / integrar** la imagen
  (never *"fundir"*); `host` → **anfitrión**; `bootloader` → **gestor de
  arranque**. Keep the anglicism only where the tooling prints it verbatim and
  the student will read it on screen.
- **No colloquialisms anywhere, not only in body copy.** Figure captions,
  block lead-ins and `.usecase__name` labels are read aloud too: "El fallo
  número uno" is a headline, "Causa dominante del fallo" is the register this
  deck uses. The full list of banned constructions is in the paper-slide
  section below; it applies to every slide.

### Labels and titles: the most-corrected failure in this deck

Two patterns keep reappearing and both read as machine-written. Check every
new label and title against them.

**1. Topic labels (`.badge`) must be noun phrases naming the subject matter**,
the way a syllabus names it. No verbs, no interrogatives, no atmosphere.

| No | Sí |
|---|---|
| `02 · De la magnitud al dato` | `02 · Tratamiento de la señal` |
| `05 · Avanzar sin bloquear` | `05 · Temporización no bloqueante` |
| `06 · Que el enlace no falle` | `06 · Robustez del enlace` |
| `07 · Cuando algo falla` | `07 · Diagnóstico de fallos` |
| `01 · Cómo se reparte el código` | `01 · Organización del proyecto` |

The same rule governs `.usecases-label`, `.practice__label` and
`.paper__section-label`: `Dónde aparece esto` → `Aplicaciones habituales`;
`Qué comprobar siempre` → `Comprobación obligatoria`.

**2. Slide titles must state the content, not name the category.** A title
that could head the same slide in any course on the subject is too generic.
Ask whether the title alone tells the reader something.

| Demasiado genérico | Específico |
|---|---|
| `Validación del dato` | `Criterios de validez de una lectura` |
| `Filtrado de la señal` | `Media móvil y filtro exponencial` |
| `Bus SPI` | `Líneas y selección de dispositivo en SPI` |
| `Modos de transmisión` | `Transmisión serie, paralela y dúplex` |
| `Criterios de selección` | `Criterios de selección entre UART, I²C y SPI` |

**Interrogative titles are banned**, including on paper slides, where they
crept in as `Qué se gana al separar el firmware en capas`. Rewrite as a noun
phrase: `Efecto medible de separar el firmware en capas`. Same for
`Qué ocurre al pulsar «Build»` → `Etapas de la cadena de construcción`.

**3. Never frame content as "used in the course".** The student is *in* the
course; saying so adds nothing and turns a technical statement into a note
about the syllabus. This was swept out of 27 places across 17 slides. State
the engineering fact instead, or drop the qualifier — the sentence is almost
always shorter and more precise without it.

| No | Sí |
|---|---|
| `Dónde se usa en el curso` (encabezado de tabla) | `Uso habitual` |
| `Elección del curso` (rótulo de `.conclusion`) | `Opción adoptada` |
| `Criterio del curso` | `Criterio operativo` |
| `Cuál se usa en este curso` | `Opción adoptada` |
| `Plataforma del curso` | `Plataforma adoptada` |
| `Núcleo 3.x (del curso):` | `Núcleo 3.x:` |
| `el hardware del curso` · `el módulo del curso` | `el hardware empleado` · `el módulo empleado` |
| `La convención del curso marca…` | `La convención adoptada marca…` |
| `xtensa-esp32-elf-gcc en este curso` | `xtensa-esp32-elf-gcc para el ESP32 clásico` |

The exception is where **«curso» names an artefact** rather than qualifying a
use: `Índice del curso`, `Archivos e índice del curso`, `Los 62 artículos del
curso`, `Resumen y cierre del curso`, and the licence line `El material del
curso; cada artículo citado conserva su propia licencia`. Those are navigation
and legal furniture — stripping the word there leaves them meaningless.

Audit with `grep -rn 'del curso\|en el curso\|en este curso' src/slides/`, and
watch for `del cursor` (potentiometer wiper), which is a false positive.

To audit the whole deck at once, dump every badge and title side by side and
read the two columns — the offending ones stand out immediately:

```
grep -h -A2 'class="badge"' src/slides/*/*.html
```

## Use cases are part of the explanation, not an extra

A correct but abstract definition does not stick. Every concept slide should
name where the thing actually shows up, in the `.usecases` strip, and each
entry must be verifiable and specific:

- **No**: "control de motores", "aplicaciones industriales", "domótica".
- **Yes**: "un contacto magnético a varios metros de cable actúa como antena:
  la polarización es lo que evita falsas aperturas".

Three entries is the working size. Put the strip after the definition, full
width under the split when the columns are narrow — never in place of the
definition.

## Paper slides (`.paper`) and the references slide

Each session carries 2-4 open-access papers. They are **not** footnote citations:
each gets a full slide (`.paper`, navy header — the deliberate contrast with La
hora del código's red) placed right after the slide whose topic it settles.
PDFs live in `src/paper/clase-NN/`. **Read the PDF in full before writing the
slide** — the abstract is not enough to state a method or a conclusion.

### The obligatory structure

The slide follows the same path a reader follows through the article. Skipping a
step turns it into a heap of loose figures:

1. `__header` — label + licence, both visible. A student must be able to see the
   PDF is downloadable without a subscription.
2. `__cite` — full bibliographic reference, max 2 lines.
3. `__title` — **the question the article settles**, as a technical noun phrase:
   "Aptitud del conversor integrado para instrumentación". Not the article's own
   title, and not a slogan.
4. `__body` → left `.paper__notes` with `.paper__section` blocks, right the
   figure. The sections, in order and with these exact labels:
   - **Objetivo del estudio** — what the authors set out to determine, and *why
     it was open*. If the slide introduces an unfamiliar concept (an emulator, a
     benchmark, pass@1), define it **here**, in one clause.
   - **Procedimiento experimental** — how it was measured: instrument, reference
     device, sample sizes, conditions. Without this, the figures are unfounded.
   - **Discusión y conclusiones** — what the *authors* concluded, attributed to
     them ("los autores concluyen…"), never merged with our own reading.
5. `.findings` — the quantitative results, in a full-width strip. Magnitude on
   its own line (it is what gets written down and re-cited), then one sentence
   interpreting it.
6. `.paper__relevance` — opens with the `Para esta sesión:` label. States **why
   this article is being shown in this class** and what the student does with it.
   Without it the slide merely invokes an external authority.

### Register: technical, academic, impersonal

This is the rule that has been corrected most often, so it is worth stating
sharply. The slide is read aloud to a lecture hall, not written to a colleague.

- **Never colloquial.** Banned outright: "lo dice sin rodeos", "sin más", "de un
  vistazo", "se cae", "arranca bien", "nadie hace X a mano", "el fallo número
  uno", "qué sí lo mejora". Their replacements are ordinary technical Spanish:
  *"la causa dominante del fallo"*, *"factor discriminante"*, *"el circuito de
  auto-reset gobierna estas señales"*.
- **Never address the reader.** No "te sirve para", no "verás que", no "si haces
  esto". The register is impersonal or first-person plural.
- **Never explain the slide to the person who commissioned it.** "Es la
  justificación de los dos primeros entregables" is a note to the author, not
  content for the class. Write what the audience needs: what was measured, what
  came out, what follows from it.
- **Translate into the Spanish the field actually uses.** A literal calque is an
  error even when it is understandable: `merge the flash image` is **componer /
  integrar** la imagen, never *"fundir"*; `host` is **anfitrión**; `bootloader`
  is **gestor de arranque** (the anglicism is admissible only where the tooling
  prints it verbatim). When unsure, prefer the term that appears in Espressif's
  Spanish documentation or in a Spanish-language datasheet.

### Other rules

- **Never summarise the whole paper.** Extract the one result that touches the
  previous slide. A paper that needs three findings needs three slides, or it
  needs to be cut.
- **Never reproduce the paper's own figures.** Report the published numbers —
  facts are not copyrightable — and draw your own figure in `render.py` from
  them, labelled "elaboración propia a partir de las cifras publicadas". This is
  a correctness requirement, not caution: one of the session-1 papers is
  CC BY-**ND**, which forbids distributing adapted versions of its figures.
- Inside other slides, cite with `<span class="cite">[1]</span>`, numbered to
  match the references slide.
- Nav labels for paper slides use the short form `Artículo · <tema>` so they stay
  readable in the prev/next strip while the slide title stays complete.
- The last slide of every session is `NN-referencias.html` (`.refs` / `.ref`),
  with each entry carrying a `.ref__where` chip naming the slides that use it.

## Building a whole session: `tools/clases/clase_NN.py`

Sessions 5-8 were built with a generator instead of 30 hand-written files, and
that is now the way to do it. `tools/generar-clase.py` owns the boilerplate —
the `<head>`, the `data-deck-total`, and the entire prev/next chain — and
`tools/clases/comun.py` owns the fixed structures (`hora_del_codigo`,
`articulo`, `cabecera`, `problema`, `termino`). A session file therefore holds
only what distinguishes each slide.

```
python3 tools/clases/clase_06.py          # emits src/slides/clase-06/*.html
python3 tools/clases/clase_06.py --dry    # lists what it would write
```

The output is ordinary standalone HTML, byte-identical in form to the
hand-written slides: the generator leaves no trace in the result and is not
needed to serve it. What it removes is the class of error that hand-editing
produces — a nav link pointing at the old filename, a `data-deck-total` left
at the previous count, a renumbering that skips a slide.

Consequences to respect:

- **Edit the Python, never the generated HTML.** A fix applied to
  `src/slides/clase-06/14-*.html` is lost on the next run.
- Reordering or inserting is done by moving a `lamina(...)` call; the file
  numbers and both nav links follow automatically. `tools/renumber.mjs` stays
  for the hand-written sessions 1-4.
- Deleting a slide requires `rm src/slides/clase-NN/*.html` before
  regenerating, or the old file survives with a stale number.
- **La hora del código: minimum 4 per session.** Session 7 was first written
  with 2 and had to be extended. Check the count before considering a session
  finished: `ls src/slides/clase-NN/*codigo*.html | wc -l`.
- **`Ejemplo NN` numbering is continuous across all 12 sessions.** After
  inserting one, verify there is no gap:
  `grep -rho 'Ejemplo [0-9]*' src/slides/ | sort -u`.

### The 12 px that no amount of trimming fixes

A `.code-hour` slide that overflows by a constant amount regardless of what
text is cut is not a text-length problem: the **taller of the two columns**
inside `.code-hour__body--pair` sets the height, and trimming the shorter one
changes nothing. Measure which column dominates before editing — usually the
prompt plus its `.prompt-note` — and cut a line from that one. One line of
`.prompt-note` is worth exactly the 12 px that keeps recurring.

## Inserting or reordering slides

Never renumber by hand. `node tools/renumber.mjs plan.json` takes a JSON list of
slugs in the desired order, renames every file, rewrites all prev/next links
with the right labels, and fixes `data-deck-total` everywhere. Create the new
slide with any number, add its slug to the plan, run `--dry` first. Restart the
dev server afterwards (Tailwind won't see the new filenames otherwise).

## Figures: Python for numbers, markup for topology

Two different tools, and picking the wrong one is the usual mistake.

**`tools/figures/render.py` (matplotlib → `public/figures/*.svg`)** for anything
with axes, magnitudes or hundreds of points: transfer curves, waveforms,
artefact sizes, memory maps, timelines. The data lives in a named constant at
the top of the script and is the *same* data the slide states in prose, so the
figure cannot drift from the text. Regenerate with
`python3 tools/figures/render.py`.

The generator rewrites every ink to a CSS variable (`--fig-ink`, `--fig-accent`,
…) before writing the file, and deck.js **inlines** the SVG rather than using
`<img src>` — an SVG loaded as an image lives in its own document and cannot see
the page's variables, so it would need two files to survive dark mode. Inlined,
one file re-inks itself. Markup is just:

```html
<div class="figure">
  <div class="figure__frame" data-figure="adc-transferencia"></div>
  <p class="figure__caption">…what the figure reveals, not what it shows…</p>
</div>
```

The caption states the **conclusion**, never a restatement of the axes. "El
tamaño no crece de forma monótona" is a caption; "Gráfico de tamaños por etapa"
is a label.

### Check what the slide already has before adding a figure

There are **three** visual forms, not two, and they rank. An interactive
simulation (block 3) beats a static figure on the same content: it lets the
student move the parameter and watch the conclusion change. Adding a
matplotlib figure to a slide that already carries a canvas simulation of the
same idea is duplication, and a figure nobody displays can drift from the text
without anyone noticing — which is the exact failure this whole file exists to
prevent.

So before writing a new figure, look:

```
grep -cE '<canvas|data-figure|class="picker"' src/slides/clase-NN/SS-*.html
```

This was learned the expensive way. Sessions 1-4 looked "figure-poor" by
counting `data-figure` alone (0-1 each), which prompted seven new figures for
them; all seven turned out to duplicate canvas simulations already on those
slides and were removed. The real gap was the opposite: sessions 5-8 had **no
interactive simulations at all**. Count all three forms before concluding
anything about a session's visual richness.

After wiring figures, verify none is orphaned — the digits in a name like
`paper-lenguajes-esp32` mean `[a-z-]*` is the wrong pattern:

```
grep -rho 'data-figure="[^"]*"' src/slides/ | sed 's/.*="//;s/"//' | sort -u > /tmp/u
ls public/figures/*.svg | xargs -n1 basename | sed 's/\.svg//' | sort > /tmp/t
comm -13 /tmp/u /tmp/t     # figuras que nadie muestra
comm -23 /tmp/u /tmp/t     # láminas que piden un archivo inexistente
```

**`.blockdiagram` / `.bd-node` / `.bd-arrow` / `.bd-lane` (plain markup)** for
boxes-and-arrows topology. Written as HTML so each box stays selectable,
translatable and zoomable, and inherits the theme. Do not render a block
diagram through matplotlib, and do not plot a curve by hand in SVG.

Keep generated figures wide and short (`figsize` around 6 × 2.5): they share
the sheet with a text column and height is the scarce resource.

## Verifying a slide visually (read this before trusting a screenshot)

**Tailwind's Vite plugin only scans the files that existed when `npm run dev`
started.** A slide file created *after* the dev server booted gets served with
stale CSS: its utility classes (especially arbitrary ones like
`md:grid-cols-[1fr_22rem]`) silently produce no rule, so a correct two-column
layout renders as one column and the page looks broken when it is not.

Therefore, after creating or renaming any slide file, **restart the dev server
before screenshotting**, or the verification is meaningless:

```
pkill -f vite; sleep 1; npm run dev &   # then wait ~4 s before loading a page
```

This has already produced one false "layout bug" investigation. `npm run build`
does a fresh scan every time and is not affected — only the long-running dev
server is.

### Fullscreen lives in `presentar.html`, not in the slide

The Fullscreen API is bound to the **document** that requested it. Every slide
is its own document, so any navigation destroys that document and the browser
drops out of fullscreen. This is browser behaviour, not a bug in the button —
no amount of re-requesting on load fixes it, because a fresh document has no
user activation to spend.

The fix is `presentar.html`: a shell whose only content is a full-viewport
`<iframe>`. Fullscreen is requested on the **shell**, which is never unloaded;
slides navigate inside the frame, which does not affect the containing
document. Consequences to preserve:

- `deck.js` detects being framed (`window.self !== window.top`) and points its
  fullscreen button at the parent document. User activation propagates from a
  same-origin frame to its ancestors, so the request is valid from inside.
- Outside the frame, the button **navigates into the shell** rather than
  requesting a fullscreen that would die on the next slide. The shell then
  arms a one-shot request that fires on the first gesture — normally the very
  keypress that advances.
- The shell returns focus to the frame on every load and on
  `fullscreenchange`. Without that, arrow keys land on the shell, `deck.js`
  never sees them, and the deck looks frozen.
- `presentar.html` must stay in `vite.config.js`'s input list.

`node tools/check-fullscreen.mjs` drives both routes with a real browser and
asserts fullscreen survives each slide change. Run it after touching
`deck.js`, `presenter.js` or the nav markup.

### Run the checker, don't eyeball the deck

```
node tools/check-slides.mjs             # las 233
node tools/check-slides.mjs clase-01    # una sesión
node tools/check-slides.mjs --shot clase-01/15   # + captura en .capturas/
```

It measures `scrollHeight - clientHeight` on `.slide__content` for every slide
and also flags console errors, figures that never loaded, and broken prev/next
links. This exists because a *global* change — a bump in the type scale, a
looser line-height — breaks the fit of slides nobody was looking at. Any change
to `variables.css`, `slides.css` or `components.css` requires a full run, not a
spot check on the slide being edited.

`npm run build` produces all 233 pages (see the multi-page input in
`vite.config.js`); if it ever emits only `index.html` again, that config
regressed.

## Anti-patterns to avoid

- **Inline styles** (`style="..."`) — always a CSS class or Tailwind utility.
  If a value needs to vary per-element (like animation delay), express it
  with a CSS selector (`:nth-child`), not inline `style`. For a one-off color
  override (e.g. tinting one icon accent-red inside an otherwise navy
  block), use Tailwind's arbitrary-value utility against the token instead —
  `class="text-[var(--color-accent)]"` — never `style="color: ..."`.
- **Time-block scaffolding** — no "Apertura 5 min", no "Tema A · 25 min", no
  "Índice de la sesión", no "Recorrido y asignación de tiempo". That's
  instructor planning, not student-facing content.
- **"Consigna" / instruction boxes** — "Consigna: observe...", "Determine...",
  "Anote..." read like exam instructions and break the reading flow.
  Simulations get a descriptive `.sim-caption`, not a command.
- **Curriculum jargon** — "Alcance de la sesión", "Objetivo terminal",
  "Criterio de logro", "Conceptos complementarios" as a heading. These are
  planning-document vocabulary; fold the content in without the label.
- **Quizzes or checkpoints inside the slide** — closing questions live in a
  separate form, not embedded in the HTML.
- **A third font family**, or weights/sizes invented outside the type scale
  already defined in `slides.css`.
- **A third brand color** — the accent/navy pair is fixed. Status colors
  (ok/warn/danger) are for simulation state, not decoration.
- **Hardcoded hex/rgb colors** — breaks dark mode. Always go through a
  `--color-*` token.
- **Gratuitous animation** — spinning, bouncing, or looping effects. Entrance
  animation should run once and settle.
- **Fixed pixel dimensions on the slide root** — always `100vw` / `100dvh`,
  never a fixed `px` width/height that breaks on other screen sizes.
- **Low-contrast text** — check headline/body contrast against both the
  light and dark `--color-bg` values, not just one.
- **Overusing shadows/gradients** — `--shadow-sm` / `--shadow-md` /
  `--shadow-lg` cover the real use cases (resting, hover, elevated); don't
  add ad-hoc `box-shadow` values.
- **"La hora del código" that contains the code** — it contains the
  specification, wiring, and expected output only. It never gives working
  source for the student to copy.
- **Referencing old project folder names** (`prueba1`, `prueba2`, etc.) — the
  student-facing material never cites a work-in-progress folder name, even
  when the `Edición 10` draft used one as a style reference.

## The order of work for a session

Producing a session runs through the skills in this order. It is not
interchangeable: each pass assumes the previous one already ran, and
inverting any pair means repeating work.

```
 1  paper-planner        ── only if the session needs new sources
 2  (write the slides)      structure, layouts, figures, code-hour blocks
 3  paper-visuals        ── figures and tables: palette, format, captions
 4  human-academic-writing  lexical AI-tell sweep
 5  presentation-design  ── labels and titles (the structural AI-tell layer)
 6  academic-register    ── verb tense, orthotypography, Spanish register
 7  paper-review         ── 18-dimension editorial check
 8  node tools/check-slides.mjs   fit, clipping, figures, nav chain
```

**Why 4 before 5.** `human-academic-writing` works on a closed word list and
changes wording; the **Labels and titles** section of this file works on
structure and changes whole labels. Running the structural pass first means
the lexical pass then edits text you just rewrote.

**Why 6 after 5.** Register checks tense and typography over settled text.
Titles rewritten afterwards would arrive unaudited.

**Why 7 last among the audits.** Editorial QC verifies cross-references,
acronym expansion and internal consistency. Any earlier pass can rename a
slide or a glossary term and break exactly what QC checks — that is how a
renamed slide (`guardas de inclusión` → `protección contra inclusión
múltiple`) left its glossary entry contradicting it until QC caught it.

### What each audit actually found here, and what it did not

Recording this so the next session does not re-derive it:

- **Lexical sweep**: 3 hits in 126 slides, all the same calque (`basado en`
  → `a partir de` / `con` / `gobernado por`). The closed list is otherwise
  clean. Do not extend the list by intuition — that is stated in the skill.
- **Parallel triads**: 1 hit, `compilador, ensamblador y enlazador`.
  **Left alone**: it is the real enumeration of the toolchain stages, i.e.
  fixed technical terminology, which the skill excludes explicitly.
- **Editorial QC**: the findings worth acting on were an acronym used across
  7 slides with no glossary entry (TX/RX), another across 4 (LEDC), a
  filename in straight quotes where the deck uses `<code>`, and the glossary
  inconsistency above.
- **False positives to expect** from a naive scan: numbers opening a
  `.finding__value` label read as "figure starting a sentence" — they are
  labels, not sentences; and the straight quotes inside JSON keys
  (`"t":23.4`), which are required by the notation.

### Confirmed false positives — do not "fix" these again

Recorded after sessions 5-8 so the next pass does not re-litigate them:

- **`lejos de`** flagged as an "unnecessary antithesis". The banned form is the
  rhetorical `Lejos de A, B` opening a sentence. `lejos de las interrupciones
  de la radio` and `el fallo se manifiesta lejos de donde se produjo` are
  literal and spatial, and are precise technical Spanish. Left alone.
- **`WROOM`**, **`ACCESS`**, **`ERROR`**, **`INDICE`** flagged as acronyms
  needing a glossary entry. The first is part of the module name
  (ESP32-WROOM-32), the second comes from the *IEEE Access* citations, the
  third is a code identifier inside `enum class Estado`, the fourth is a
  filename. None is an acronym the student must learn.
- What the same scan **did** catch and was worth acting on: `UML` (session 5),
  and `HTTPS`, `UDP` and `MAC` (session 7) — all genuinely used across many
  slides with no entry. A glossary slide holds **11 terms**; at 13 it
  overflows, so merge related pairs (`DHCP y DNS`, `TCP y UDP`) rather than
  dropping a term.

## The three academic-writing skills copied into this project

`Skill for paper/` holds a consolidated catalogue of nine skills for academic
writing (see its `CATALOGO.md`). All nine are installed globally; **three are
copied here** because they govern work this deck actually does. The other six
— venue selection, drafting paper sections, cover letters — do not apply.

| Skill | What it governs here | Relation to this file |
|---|---|---|
| `human-academic-writing` | The AI-tell sweep over labels, titles and captions | Its flag-word lists are the *lexical* layer; the **Labels and titles** section above is the *structural* layer. Run the skill first, then re-read that section. |
| `academic-register` | Verb tense, orthotypography, admissible vocabulary in Spanish | Use the `registro-es.md` annex only. Where it and this file disagree, **this file wins**: a slide is not a paper, and the deck's own terminology rules (Montaje, no calques, the raya) were set against the audience. |
| `paper-visuals` | Figures and tables | Already consistent with `render.py`: no `jet`/`rainbow`, accessible palettes, caption below a figure and above a table, no orphan elements. Consult it before adding a new figure type. |

They are decision aids, not authorities over the deck. This file and the
project's own conventions take precedence whenever they conflict.

## Using `design-taste-frontend` on this deck

A copy of the third-party skill lives at
`.claude/skills/design-taste-frontend/SKILL.md` (installed with
`npx skills add`, mirrored from `.agents/skills/`). It is written for landing
pages, portfolios and marketing redesigns — its own §13 declares dense
instructional UI out of scope. So it is **a checklist to run against slides,
not a mandate to redesign them into a landing page.**

**Design read for this project (its §0.B one-liner), fixed once:**
> Instructional slide deck for engineering undergraduates at UNI, with a
> laboratory-instrument language (oscilloscope grid, mono type, measurement
> brackets), built on Tailwind v4 + IBM Plex + restrained motion.

**Dials (its §1), fixed once:** `DESIGN_VARIANCE 5 · MOTION_INTENSITY 3 ·
VISUAL_DENSITY 6`. Low variance because 110+ slides must read as one
instrument; low motion because animation competes with the instructor's
voice; high density because a slide carries a full concept, not a headline.
Do not re-derive these per slide.

**What to take from it:**

- §9.C — no rows of three identical cards. Break with `.layout--split`,
  `.layout--wide-left` or `.layout--thirds` carrying genuinely different
  content per column.
- §9.D — no fake-perfect numbers. Timings, currents and byte counts must be
  the real ones, derivable from the values shown on the same slide.
- §9.F — no decorative status dots, no `Scroll` cues, no version stamps,
  no micro-meta-sentences under a heading, no vertical rotated text, no
  hairline grid lines used as decoration.
- §4.11 — one theme per slide. Never invert a single block to dark inside a
  light slide.
- §6.B / §6.C — reduced motion and dark mode are already wired in
  `animations.css` and `variables.css`; keep new work inside them.

**What this project overrides (do not "fix" these):**

- **The middle dot `·`** stays as the deck separator in badges, eyebrows and
  `.codepanel__header`. It is the established typographic voice of the whole
  course, and §9.F's rationing rule is aimed at marketing metadata strips.
- **The em-dash `—`** stays in Spanish prose. §9.G bans it as an English
  LLM tell; in Spanish it is the *raya*, the correct mark for incisos per the
  RAE. Removing it would make the copy wrong. It stays banned as a
  **decorative** element (never in a badge, pill or heading as a divider).
- **Icons** come from `public/course-icons.svg`, not Phosphor/Tabler. §9.E
  assumes an npm icon set is available; here a single hand-kept monochrome
  sprite is deliberate — it ships offline, inherits `currentColor`, and keeps
  every glyph in the same stroke language as the diagrams.
- **`.term`, `.codepanel` and the SVG diagrams** are not "div-based fake
  screenshots" (§9.E). They show real serial output and real source; the
  content is the point, not a simulated product UI.
- **Numbered theme badges** (`02 · Los pines y sus límites`) are not
  section-number eyebrows (§9.F). The number is the theme's index in the
  official `Temario_ESP32_AI_Edicion_10.docx`, so it carries information the
  student uses to navigate the syllabus.

**Pre-flight (its §14), reduced to what applies here:** one accent, one
radius system, WCAG AA on every text/background pair in both themes, no
hand-rolled decorative SVG that isn't a real diagram, no layout family
repeated three slides in a row, and every animation justifiable in one
sentence.
