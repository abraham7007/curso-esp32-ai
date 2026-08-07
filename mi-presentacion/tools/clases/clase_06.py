#!/usr/bin/env python3
"""Sesión 6 — FreeRTOS: ejecución concurrente sobre dos núcleos.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_06.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
_spec = importlib.util.spec_from_file_location(
    "generador", Path(__file__).resolve().parents[1] / "generar-clase.py"
)
_gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen)

from comun import ESPARCIDO, articulo, cabecera, credito, envolver, hallazgo, hora_del_codigo, ico, portada, problema, termino

A = "01 · Tareas y planificador"
B = "02 · Comunicación y sincronización"

LAMINAS = []


def lamina(slug, titulo, nav, contenido, icono="i-flow", clases="slide slide--start", scripts=""):
    LAMINAS.append(
        {
            "slug": slug,
            "titulo": titulo,
            "nav": nav,
            "icono": icono,
            "clases": clases,
            "contenido": contenido,
            "scripts": scripts,
        }
    )


LED_SCRIPTS = """\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
"""

# ───────────────────────────────────────────────────────── 01 · portada
lamina(
    "portada",
    "Sesión 6 · FreeRTOS: ejecución concurrente sobre dos núcleos",
    "FreeRTOS y ejecución concurrente",
    portada(
        "Sesión 6",
        "FreeRTOS: ejecución<br />concurrente sobre dos núcleos",
        "Tareas y planificador.",
        "Comunicación y sincronización entre tareas.",
        [
         ("i-cpu", "Tareas, prioridades y planificador"),
         ("i-layers", "Afinidad de núcleo en el ESP32"),
         ("i-link", "Colas, mutex y semáforos"),
         ("i-alert", "Dimensionado de pila por tarea"),
        ],
        "02-limite-bucle-unico.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ──────────────────────────────────────────── 02 · límite del bucle único
lamina(
    "limite-bucle-unico",
    "Límite del bucle único ante requisitos temporales incompatibles · Sesión 6",
    "Límite del bucle único",
    envolver(f"""{cabecera(A, "Límite del bucle único ante requisitos temporales incompatibles", "i-alert")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDónde falla
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEn un bucle único, el periodo de la actividad más rápida no puede
\t\t\t\t\t\t\t\tser menor que la duración de una iteración completa. Basta una
\t\t\t\t\t\t\t\tactividad lenta para fijar ese límite a todas las demás.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tCaso concreto
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn equipo que muestrea un acelerómetro a <b>1 kHz</b> (un periodo
\t\t\t\t\t\t\t\tde 1 ms) y publica por red cada 10 s. La publicación ocupa
\t\t\t\t\t\t\t\t<b>380 ms</b> entre la conexión y el envío. Durante esos 380 ms el
\t\t\t\t\t\t\t\tbucle no muestrea: se pierden unas <b>380 muestras</b>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Por qué no basta con más estados</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tTrocear la publicación en una máquina de estados de veinte etapas
\t\t\t\t\t\t\t\treduce el bloqueo, pero obliga a repartir a mano una operación que
\t\t\t\t\t\t\t\tes secuencial por naturaleza. La complejidad del modelo crece por
\t\t\t\t\t\t\t\tencima de lo mantenible, y ese es el criterio que justifica el
\t\t\t\t\t\t\t\tsistema operativo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram">
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Bucle único</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t\t<span class="bd-node__body">
\t\t\t\t\t\t\t\t\t\tmuestrear · muestrear · … · <b>publicar (380 ms)</b> · muestrear
\t\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t\t\t<span class="bd-node__meta">380 muestras perdidas en cada publicación</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Dos tareas</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t\t<span class="bd-node__body">
\t\t\t\t\t\t\t\t\t\tmuestreo (prioridad alta) · publicación (prioridad baja, se
\t\t\t\t\t\t\t\t\t\tinterrumpe y se reanuda)
\t\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t\t\t<span class="bd-node__meta">ninguna muestra perdida</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="periodo-bucle-vs-tareas"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\tLo que cambia no es la velocidad media, casi idéntica en ambos, sino
\t\t\t\t\t\t\t\tel valor máximo. El peor caso es el que decide si se cumple el
\t\t\t\t\t\t\t\tperiodo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-alert",
)

# ────────────────────────────────────── 03 · RTOS y determinismo
lamina(
    "rtos-determinismo",
    "Sistema operativo de tiempo real y determinismo · Sesión 6",
    "Sistema de tiempo real y determinismo",
    envolver(f"""{cabecera(A, "Sistema operativo de tiempo real y determinismo", "i-clock")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\tSistema operativo de tiempo real
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSistema operativo cuyo planificador garantiza un <b>plazo máximo</b>
\t\t\t\t\t\t\tentre que una tarea queda preparada y recibe el procesador. La
\t\t\t\t\t\t\tgarantía es sobre el peor caso, no sobre el promedio.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tSe abrevia <b>RTOS</b>, del inglés <i>real-time operating system</i>.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\tDeterminismo
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tPropiedad de un sistema cuyo tiempo de respuesta está <b>acotado y es
\t\t\t\t\t\t\tconocido</b>. Un sistema determinista no es necesariamente rápido: es
\t\t\t\t\t\t\tuno cuyo retraso máximo puede calcularse antes de ejecutarlo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tUn sistema que responde en 2 ms el 99 % de las veces y en 400 ms el
\t\t\t\t\t\t\t1 % restante no es determinista.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Tiempo real estricto</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tIncumplir el plazo constituye un fallo del sistema, con
\t\t\t\t\t\t\tconsecuencias sobre la seguridad o sobre el producto.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tDisparo de un airbag, control de un motor de tracción, corte de una
\t\t\t\t\t\t\tprensa ante la detección de un obstáculo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Tiempo real flexible</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tIncumplir el plazo degrada la calidad del resultado sin invalidarlo.
\t\t\t\t\t\t\tSe tolera una proporción acotada de incumplimientos.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tRefresco de una pantalla, registro de temperatura cada minuto,
\t\t\t\t\t\t\ttransmisión de telemetría a una plataforma.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Dónde se sitúa este curso</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tFreeRTOS sobre ESP32 con el núcleo de Arduino cubre <b>tiempo real
\t\t\t\t\t\tflexible</b>. La pila de comunicaciones inalámbricas introduce
\t\t\t\t\t\tinterrupciones cuya frecuencia no controla el programa, de modo que el
\t\t\t\t\t\tpeor caso no puede acotarse con rigor. Los proyectos con requisito
\t\t\t\t\t\testricto separan esa función en un microcontrolador dedicado.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-clock",
)

# ─────────────────────────────────────────────────── 04 · qué es una tarea
lamina(
    "definicion-tarea",
    "La tarea y su pila de ejecución · Sesión 6",
    "La tarea y su pila de ejecución",
    envolver(f"""{cabecera(A, "La tarea y su pila de ejecución", "i-cpu")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna <b>tarea</b> es una función con bucle propio y, sobre todo, con
\t\t\t\t\t\t\t\t<b>pila propia</b>. Esa pila guarda sus variables locales y la
\t\t\t\t\t\t\t\tdirección de retorno de cada llamada, y es lo que permite
\t\t\t\t\t\t\t\tinterrumpirla en cualquier punto y reanudarla exactamente ahí.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>xTaskCreatePinnedToCore(funcion, "nombre", pila, param,
\t\t\t\t\t\t\t\tprioridad, &amp;handle, nucleo)</code>. El tamaño de pila se
\t\t\t\t\t\t\t\texpresa en <b>palabras</b>, no en bytes: en el ESP32 una palabra
\t\t\t\t\t\t\t\tson 4 bytes, de modo que 4096 reserva 16 kB.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa función de una tarea <b>no debe retornar nunca</b>. Si termina,
\t\t\t\t\t\t\t\thay que eliminarla con <code>vTaskDelete(NULL)</code>; salir por el
\t\t\t\t\t\t\t\tfinal de la función provoca el reinicio del sistema.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">creación y estructura</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>void tareaMuestreo(void *param) {{
  <span class="hl hl--hit">for (;;) {{                    // no retorna nunca</span>
    int v = analogRead(34);
    vTaskDelay(pdMS_TO_TICKS(1));  // cede el procesador
  }}
}}

void setup() {{
  xTaskCreatePinnedToCore(
    tareaMuestreo, "muestreo",
    <span class="hl hl--add">4096,</span>        // pila en palabras → 16 kB
    nullptr,
    <span class="hl hl--add">3,</span>           // prioridad; loop() usa 1
    nullptr,
    <span class="hl hl--add">1);</span>          // núcleo 1
}}</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCada tarea reserva su pila en SRAM al crearse. Diez tareas de 4096
\t\t\t\t\t\t\t\tpalabras ocupan <b>160 kB</b> de los 320 kB disponibles, y esa
\t\t\t\t\t\t\t\tmemoria se reserva aunque la tarea esté bloqueada.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ─────────────────────────────────────────── 05 · estados de una tarea
lamina(
    "estados-tarea",
    "Los cuatro estados de una tarea · Sesión 6",
    "Los cuatro estados de una tarea",
    envolver(f"""{cabecera(A, "Los cuatro estados de una tarea", "i-flow")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>El planificador es una máquina de estados por tarea.</strong>
\t\t\t\t\tEs el mismo formalismo de la sesión anterior, aplicado por el sistema
\t\t\t\t\toperativo en lugar de por el programa.
\t\t\t\t</p>

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-bolt")}En ejecución</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tOcupa un núcleo. Con dos núcleos hay como máximo <b>dos tareas</b> en
\t\t\t\t\t\t\teste estado a la vez.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-clock")}Preparada</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tPodría ejecutarse pero otra de prioridad igual o mayor tiene el
\t\t\t\t\t\t\tnúcleo. Espera turno, no espera un suceso.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-link")}Bloqueada</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEspera un suceso: que venza un plazo, que llegue un mensaje a una
\t\t\t\t\t\t\tcola o que se libere un mutex. <b>No consume procesador.</b>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}Suspendida</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tFuera del planificador hasta que otra tarea la reanude con
\t\t\t\t\t\t\t<code>vTaskResume()</code>. A diferencia de la bloqueada, ningún
\t\t\t\t\t\t\tsuceso la despierta por sí solo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t<span class="conclusion__label">La distinción que importa</span>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEntre <b>preparada</b> y <b>bloqueada</b>. Una tarea que espera con
\t\t\t\t\t\t\t<code>while (!hayDato) {{}}</code> permanece <em>preparada</em> y
\t\t\t\t\t\t\tconsume el núcleo entero sin hacer nada. La misma espera con
\t\t\t\t\t\t\t<code>xQueueReceive()</code> la deja <em>bloqueada</em> y libera el
\t\t\t\t\t\t\tprocesador para las demás. Es la diferencia entre un sistema que
\t\t\t\t\t\t\tfunciona y uno que consume el 100 % de un núcleo esperando.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>""", ESPARCIDO),
)

# ───────────────────────────────────── 06 · La hora del código · 24
lamina(
    "codigo-24-primeras-tareas",
    "Código 24 · Dos tareas con periodos incompatibles · Sesión 6",
    "La hora del código · Dos tareas",
    hora_del_codigo(
        24,
        "Dos tareas con periodos incompatibles sobre el mismo dispositivo",
        "La misma función resuelta dos veces: primero en un bucle único y después en dos tareas. Una actividad "
        "debe repetirse cada <b>1 ms</b> y otra ocupa <b>380 ms</b> cada diez segundos. Se implementan ambas "
        "versiones y se comparan el periodo medio y el máximo.",
        "Una <b>tarea</b> de FreeRTOS es una función con su propia pila que el planificador puede interrumpir; la "
        "<b>prioridad</b> decide a quién devuelve el procesador y la <b>afinidad</b>, en qué núcleo corre. "
        "<code>uxTaskGetStackHighWaterMark()</code> devuelve la pila libre mínima que ha tenido una tarea. Ojo con "
        "<code>delay()</code>: en FreeRTOS <b>cede</b> el procesador, así que no sirve para simular carga.",
        "El <b>ESP32</b> conmuta un LED en el <b>GPIO 25</b> en cada muestreo y enciende otro en el "
        "<b>GPIO 26</b> mientras dura la operación lenta, ambos con resistencia de 220 Ω a masa.",
        """[BUCLE]  n=10000  periodo medio=1.02 ms max=381.4 ms perdidas=379
[TAREAS] n=10000  periodo medio=1.00 ms max=1.06 ms perdidas=0
[PILA]   muestreo: libre minima=2884 palabras de 4096
[PILA]   publicacion: libre minima=1120 palabras de 4096
[NUCLEO] muestreo=1  publicacion=0  loop=1""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Implementa las dos versiones seleccionables por una constante de compilación. La versión de bucle único hace ambas cosas en <code>loop()</code>. La versión con tareas crea una tarea de muestreo con prioridad 3 fijada al núcleo 1 y una de publicación con prioridad 1 fijada al núcleo 0; la operación lenta se simula con un cálculo de 380 ms, nunca con <code>delay()</code>. Ambas versiones miden el periodo real entre muestreos y su valor máximo. Imprime a 115200 baudios el resumen y, con <code>uxTaskGetStackHighWaterMark()</code>, la pila libre mínima de cada tarea.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de cada versión, uno al lado del otro, para ver dónde entra la operación lenta en cada caso. Y <b>dos líneas de tiempo</b> superpuestas a la misma escala, con los instantes de muestreo marcados y el hueco de 380 ms visible solo en la de arriba.""",
        "Comparar las dos primeras líneas: el <b>periodo medio</b> apenas cambia (1,02 y 1,00 ms) mientras el "
        "<b>máximo</b> pasa de 381,4 a 1,06 ms. La media no distingue las dos versiones; el máximo sí, y es el "
        "máximo el que decide si se cumple el requisito. Mirar después las líneas <code>[PILA]</code>: si la libre "
        "mínima cayera a unas pocas centenas de palabras, el reinicio que vendría después no diría por qué.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="orange"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ──────────────────────────────── 07 · planificador expropiativo
lamina(
    "planificador-expropiativo",
    "Planificador expropiativo por prioridades · Sesión 6",
    "Planificador expropiativo",
    envolver(f"""{cabecera(A, "Planificador expropiativo por prioridades", "i-sliders")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tRegla del planificador
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEn cada instante ejecuta la tarea <b>preparada de mayor
\t\t\t\t\t\t\t\tprioridad</b>. Que sea <b>expropiativo</b> significa que si una
\t\t\t\t\t\t\t\ttarea de prioridad superior queda preparada, la que está corriendo
\t\t\t\t\t\t\t\tse interrumpe de inmediato, sin esperar a que ceda.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-clock")}
\t\t\t\t\t\t\t\tLa interrupción periódica del sistema
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn temporizador interrumpe cada <b>1 ms</b> en el ESP32
\t\t\t\t\t\t\t\t(<code>configTICK_RATE_HZ</code> = 1000). En esa interrupción el
\t\t\t\t\t\t\t\tsistema comprueba qué plazos han vencido y decide si cambia de
\t\t\t\t\t\t\t\ttarea. Es la unidad mínima de tiempo del planificador:
\t\t\t\t\t\t\t\t<code>vTaskDelay(1)</code> no espera menos de 1 ms.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tDos tareas de <b>igual prioridad</b> se reparten el núcleo por
\t\t\t\t\t\t\t\tturnos de un tick. Una tarea de prioridad alta que nunca se bloquea
\t\t\t\t\t\t\t\timpide ejecutarse a todas las inferiores, incluida la tarea de
\t\t\t\t\t\t\t\treposo que alimenta al watchdog: el resultado es un reinicio.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t\t\t<tr><th>Prioridad</th><th>Uso previsto</th><th>Ejemplo</th></tr>
\t\t\t\t\t\t\t\t</thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>0</b></td><td>Tarea de reposo del sistema</td><td>Reservada; alimenta el watchdog</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>1</b></td><td>Trabajo de fondo</td><td><code>loop()</code> de Arduino, registro en memoria</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>2</b></td><td>Comunicación</td><td>Publicación por red, atención de peticiones</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>3</b></td><td>Adquisición periódica</td><td>Muestreo con periodo fijo</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>4-24</b></td><td>Respuesta a sucesos</td><td>Tarea despertada desde una interrupción</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Criterio de asignación</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa prioridad se asigna según el <b>requisito temporal</b>, no según
\t\t\t\t\t\t\t\tla importancia aparente de la función. Una tarea de interfaz es muy
\t\t\t\t\t\t\t\tvisible y no tiene requisito estricto: darle prioridad alta impide
\t\t\t\t\t\t\t\tcumplir el periodo de muestreo. Es el error de asignación más
\t\t\t\t\t\t\t\tfrecuente.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-sliders",
)

# ────────────────────────── 07b · simulación del planificador
lamina(
    "simulacion-planificador",
    "Reparto del procesador entre tres tareas · Sesión 6",
    "Reparto del procesador",
    envolver(f"""{cabecera(A, "Reparto del procesador entre tres tareas", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué decide el planificador
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEn cada tick ejecuta la tarea <b>preparada</b> de mayor prioridad.
\t\t\t\t\t\t\t\tUna tarea bloqueada no compite: no consume procesador aunque su
\t\t\t\t\t\t\t\tprioridad sea la más alta.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCada carril es una tarea y el color indica su estado: en ejecución,
\t\t\t\t\t\t\t\tpreparada esperando turno, o bloqueada. Al subir la prioridad de la
\t\t\t\t\t\t\t\tinterfaz por encima de la de muestreo, la barra de ocupación del
\t\t\t\t\t\t\t\tmuestreo cae y su periodo deja de cumplirse: es el error de
\t\t\t\t\t\t\t\tasignación más frecuente, medido.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="sch-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Tres carriles temporales, uno por tarea, con tramos coloreados según la tarea esté en ejecución, preparada o bloqueada, sobre un eje de tiempo en milisegundos"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<label for="sch-prio" class="text-sm font-medium">
\t\t\t\t\t\t\t\t\tPrioridad de la tarea de interfaz
\t\t\t\t\t\t\t\t</label>
\t\t\t\t\t\t\t\t<input type="range" id="sch-prio" min="1" max="4" step="1" value="1" />
\t\t\t\t\t\t\t\t<span class="readout" id="sch-prio-lectura">1</span>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item" id="sch-item-muestreo">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Muestreo · prio 3</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="sch-muestreo">100 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Interfaz</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="sch-interfaz">0 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Fondo · prio 1</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="sch-fondo">0 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="sch-item-plazo">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Periodo de 10 ms</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="sch-plazo">se cumple</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Modelo de un solo núcleo con planificación expropiativa por
\t\t\t// prioridades. Se simula tick a tick, que es exactamente como decide
\t\t\t// FreeRTOS: en cada interrupción periódica elige la preparada de mayor
\t\t\t// prioridad.
\t\t\tconst VENTANA_MS = 120;
\t\t\tconst TAREAS = [
\t\t\t\t{ id: "muestreo", rotulo: "Muestreo", prio: 3, periodo: 10, trabajo: 2, tinta: "--color-ok" },
\t\t\t\t{ id: "interfaz", rotulo: "Interfaz", prio: 1, periodo: 30, trabajo: 12, tinta: "--color-accent" },
\t\t\t\t{ id: "fondo", rotulo: "Fondo", prio: 1, periodo: 40, trabajo: 6, tinta: "--color-navy" },
\t\t\t];

\t\t\tconst lienzo = document.getElementById("sch-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst deslizador = document.getElementById("sch-prio");
\t\t\tconst lecturaPrio = document.getElementById("sch-prio-lectura");
\t\t\tconst salidas = {
\t\t\t\tmuestreo: document.getElementById("sch-muestreo"),
\t\t\t\tinterfaz: document.getElementById("sch-interfaz"),
\t\t\t\tfondo: document.getElementById("sch-fondo"),
\t\t\t};
\t\t\tconst itemMuestreo = document.getElementById("sch-item-muestreo");
\t\t\tconst itemPlazo = document.getElementById("sch-item-plazo");
\t\t\tconst salidaPlazo = document.getElementById("sch-plazo");

\t\t\tfunction variable(nombre) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();
\t\t\t}

\t\t\t// Devuelve, para cada milisegundo de la ventana, qué tarea ocupa el
\t\t\t// núcleo y en qué estado está cada una.
\t\t\tfunction simular(prioInterfaz) {
\t\t\t\tconst estado = TAREAS.map((t) => ({
\t\t\t\t\t...t,
\t\t\t\t\tprio: t.id === "interfaz" ? prioInterfaz : t.prio,
\t\t\t\t\trestante: 0,
\t\t\t\t\tliberada: 0,
\t\t\t\t}));
\t\t\t\tconst traza = [];
\t\t\t\tlet peorRetraso = 0;
\t\t\t\tlet incumplidos = 0;

\t\t\t\tfor (let t = 0; t < VENTANA_MS; t++) {
\t\t\t\t\tfor (const tarea of estado) {
\t\t\t\t\t\tif (t % tarea.periodo === 0) {
\t\t\t\t\t\t\t// Si al llegar el nuevo periodo aún queda trabajo del
\t\t\t\t\t\t\t// anterior, ese plazo se incumplió. Medirlo solo al terminar
\t\t\t\t\t\t\t// ocultaría justo el caso que la lámina quiere mostrar: una
\t\t\t\t\t\t\t// tarea hambrienta nunca termina y nunca se contaría.
\t\t\t\t\t\t\tif (tarea.id === "muestreo" && tarea.restante > 0) {
\t\t\t\t\t\t\t\tincumplidos += 1;
\t\t\t\t\t\t\t\tpeorRetraso = Math.max(peorRetraso, t - tarea.liberada);
\t\t\t\t\t\t\t}
\t\t\t\t\t\t\ttarea.restante = tarea.trabajo;
\t\t\t\t\t\t\ttarea.liberada = t;
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t\tconst listas = estado.filter((x) => x.restante > 0);
\t\t\t\t\tlistas.sort((a, b) => b.prio - a.prio);
\t\t\t\t\tconst corriendo = listas[0] || null;
\t\t\t\t\tif (corriendo) {
\t\t\t\t\t\tcorriendo.restante -= 1;
\t\t\t\t\t\tif (corriendo.id === "muestreo" && corriendo.restante === 0) {
\t\t\t\t\t\t\tpeorRetraso = Math.max(peorRetraso, t + 1 - corriendo.liberada);
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t\ttraza.push({
\t\t\t\t\t\tcorriendo: corriendo ? corriendo.id : null,
\t\t\t\t\t\tpreparadas: listas.slice(1).map((x) => x.id),
\t\t\t\t\t});
\t\t\t\t}
\t\t\t\treturn { traza, peorRetraso, incumplidos };
\t\t\t}

\t\t\tfunction dibujar(prioInterfaz) {
\t\t\t\tconst { traza, peorRetraso, incumplidos } = simular(prioInterfaz);
\t\t\t\tconst w = lienzo.width;
\t\t\t\tconst h = lienzo.height;
\t\t\t\tctx.clearRect(0, 0, w, h);

\t\t\t\tconst izq = 132;
\t\t\t\tconst der = w - 24;
\t\t\t\tconst ancho = der - izq;
\t\t\t\tconst px = (t) => izq + (t / VENTANA_MS) * ancho;
\t\t\t\tconst altoCarril = 54;
\t\t\t\tconst sep = 26;
\t\t\t\tconst arriba = 52;

\t\t\t\tconst borde = variable("--color-border");
\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst texto = variable("--color-text");

\t\t\t\tconst ocupacion = { muestreo: 0, interfaz: 0, fondo: 0 };

\t\t\t\tTAREAS.forEach((tarea, i) => {
\t\t\t\t\tconst y = arriba + i * (altoCarril + sep);
\t\t\t\t\tconst tinta = variable(tarea.tinta);

\t\t\t\t\tctx.fillStyle = variable("--color-surface");
\t\t\t\t\tctx.strokeStyle = borde;
\t\t\t\t\tctx.lineWidth = 1;
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.roundRect(izq, y, ancho, altoCarril, 6);
\t\t\t\t\tctx.fill();
\t\t\t\t\tctx.stroke();

\t\t\t\t\tfor (let t = 0; t < VENTANA_MS; t++) {
\t\t\t\t\t\tconst paso = traza[t];
\t\t\t\t\t\tconst x = px(t);
\t\t\t\t\t\tconst dx = Math.max(1, px(t + 1) - x);
\t\t\t\t\t\tif (paso.corriendo === tarea.id) {
\t\t\t\t\t\t\tocupacion[tarea.id] += 1;
\t\t\t\t\t\t\tctx.fillStyle = tinta;
\t\t\t\t\t\t\tctx.fillRect(x, y + 4, dx, altoCarril - 8);
\t\t\t\t\t\t} else if (paso.preparadas.includes(tarea.id)) {
\t\t\t\t\t\t\tctx.fillStyle = tinta;
\t\t\t\t\t\t\tctx.globalAlpha = 0.22;
\t\t\t\t\t\t\tctx.fillRect(x, y + altoCarril / 2 - 5, dx, 10);
\t\t\t\t\t\t\tctx.globalAlpha = 1;
\t\t\t\t\t\t}
\t\t\t\t\t}

\t\t\t\t\tconst prio = tarea.id === "interfaz" ? prioInterfaz : tarea.prio;
\t\t\t\t\tctx.fillStyle = texto;
\t\t\t\t\tctx.font = "600 13px system-ui";
\t\t\t\t\tctx.textAlign = "right";
\t\t\t\t\tctx.fillText(tarea.rotulo, izq - 12, y + altoCarril / 2 - 2);
\t\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\t\tctx.font = "11px ui-monospace, monospace";
\t\t\t\t\tctx.fillText(`prio ${prio} · ${tarea.trabajo}/${tarea.periodo} ms`, izq - 12, y + altoCarril / 2 + 14);
\t\t\t\t});

\t\t\t\t// Eje de tiempo
\t\t\t\tconst ejeY = arriba + 3 * (altoCarril + sep) - sep + 12;
\t\t\t\tctx.strokeStyle = borde;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(izq, ejeY);
\t\t\t\tctx.lineTo(der, ejeY);
\t\t\t\tctx.stroke();
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.textAlign = "center";
\t\t\t\tfor (let t = 0; t <= VENTANA_MS; t += 20) {
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.moveTo(px(t), ejeY);
\t\t\t\t\tctx.lineTo(px(t), ejeY + 5);
\t\t\t\t\tctx.stroke();
\t\t\t\t\tctx.fillText(`${t}`, px(t), ejeY + 18);
\t\t\t\t}
\t\t\t\tctx.textAlign = "right";
\t\t\t\tctx.fillText("tiempo (ms)", der, ejeY - 6);

\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.fillText("relleno: en ejecución · franja tenue: preparada esperando turno", izq, 26);

\t\t\t\treturn { ocupacion, peorRetraso, incumplidos };
\t\t\t}

\t\t\tfunction actualizar() {
\t\t\t\tconst prio = Number(deslizador.value);
\t\t\t\tlecturaPrio.textContent = String(prio);
\t\t\t\tconst { ocupacion, peorRetraso, incumplidos } = dibujar(prio);

\t\t\t\tfor (const id of Object.keys(salidas)) {
\t\t\t\t\tsalidas[id].textContent = `${Math.round((ocupacion[id] / VENTANA_MS) * 100)} %`;
\t\t\t\t}

\t\t\t\t// El muestreo tiene periodo de 10 ms: si un trabajo sigue pendiente
\t\t\t\t// cuando llega el siguiente, ese plazo se perdió.
\t\t\t\tconst cumple = incumplidos === 0;
\t\t\t\tsalidaPlazo.textContent = cumple
\t\t\t\t\t? "se cumple"
\t\t\t\t\t: `${incumplidos} plazos perdidos`;
\t\t\t\titemPlazo.classList.toggle("metric__item--ok", cumple);
\t\t\t\titemPlazo.classList.toggle("metric__item--bad", !cumple);
\t\t\t\titemMuestreo.classList.toggle("metric__item--ok", cumple);
\t\t\t\titemMuestreo.classList.toggle("metric__item--bad", !cumple);
\t\t\t}

\t\t\tdeslizador.addEventListener("input", actualizar);
\t\t\tnew MutationObserver(actualizar).observe(document.documentElement, {
\t\t\t\tattributes: true,
\t\t\t\tattributeFilter: ["data-theme"],
\t\t\t});
\t\t\tactualizar();
\t\t</script>
""",
)

# ─────────────────────────────────────── 08 · reparto entre núcleos
lamina(
    "reparto-nucleos",
    "Asignación de tareas a los dos núcleos · Sesión 6",
    "Asignación de tareas a los núcleos",
    envolver(f"""{cabecera(A, "Asignación de tareas a los dos núcleos", "i-cpu")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tReparto por omisión
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl <b>núcleo 0</b> (PRO_CPU) atiende la pila de comunicaciones
\t\t\t\t\t\t\t\tinalámbricas; el <b>núcleo 1</b> (APP_CPU) ejecuta
\t\t\t\t\t\t\t\t<code>setup()</code> y <code>loop()</code>. Ese reparto lo fija el
\t\t\t\t\t\t\t\tnúcleo de Arduino, no el hardware.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl último parámetro de
\t\t\t\t\t\t\t\t<code>xTaskCreatePinnedToCore()</code> fija el núcleo: <code>0</code>,
\t\t\t\t\t\t\t\t<code>1</code> o <code>tskNO_AFFINITY</code> para dejar que el
\t\t\t\t\t\t\t\tplanificador decida. <b>La tercera opción tiene un costo medido</b>
\t\t\t\t\t\t\t\tque se examina en la lámina siguiente.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Criterio de reparto</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLo que tiene requisito temporal estricto va al <b>núcleo 1</b>,
\t\t\t\t\t\t\t\tlejos de las interrupciones de la radio. Lo que usa la red va al
\t\t\t\t\t\t\t\t<b>núcleo 0</b>, donde ya reside la pila que va a invocar.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram">
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Núcleo 0 · PRO_CPU</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t\t<span class="bd-node__body">Pila WiFi y Bluetooth · interrupciones de la radio · tareas de comunicación</span>
\t\t\t\t\t\t\t\t\t<span class="bd-node__meta">carga variable, no controlada por el programa</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Núcleo 1 · APP_CPU</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t\t<span class="bd-node__body">setup() y loop() · tareas de adquisición y control</span>
\t\t\t\t\t\t\t\t\t<span class="bd-node__meta">carga que sí se conoce y se puede acotar</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[NUCLEO] tarea=muestreo      afinidad=1  ejecuciones=10000  nucleo_real=1
[NUCLEO] tarea=publicacion   afinidad=0  ejecuciones=12     nucleo_real=0
[NUCLEO] tarea=diagnostico   afinidad=libre  ejecuciones=500  nucleo_real=0/1</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa tercera tarea alterna de núcleo entre ejecuciones. Es legal y a
\t\t\t\t\t\t\tveces conveniente, pero deja de ser gratuito en cuanto la tarea se
\t\t\t\t\t\t\tsincroniza con otra.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ─────────────────────── 09 · artículo · FreeRTOS sobre ESP32 multinúcleo
lamina(
    "paper-freertos-multinucleo",
    "Costo medido de sincronizar tareas entre los dos núcleos · Sesión 6",
    "Artículo · FreeRTOS sobre dos núcleos",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Wenzel, V.; Silva, D. L.; Nunes, L. et al.</b> (2023). Analysis of FreeRTOS scheduling on the ESP32 "
        "dual-core platform. <i>SBESC / IEEE</i>. <code>doi:10.1109/SBESC60926.2023.10324061</code>",
        "Costo medido de sincronizar tareas entre los dos núcleos",
        ["Medir la penalización de ejecutar FreeRTOS sobre una arquitectura de <b>dos núcleos</b>.",
         "La adaptación multinúcleo procede de la comunidad y <b>no estaba caracterizada</b>.",
         "Medidas sobre el propio ESP32, con el contador de ciclos a 240 MHz y sin instrumentación externa."],
        ["Conmutación dentro del <b>mismo núcleo</b>: <b>0,012 ms</b>, con mínimo y máximo iguales a la media.",
         "La misma conmutación <b>entre núcleos</b>: <b>190,3 ms</b>.",
         "Una tarea programada a 10 ms sale a <b>9,996 ms</b>, con mínimo de 9,632.",
         "El planificador cumple el periodo; lo que se desborda es la sincronización."],
        ["Dentro de un núcleo la conmutación es <b>estable y despreciable</b>.",
         "Entre núcleos alcanza valores que los autores llaman <b>«inesperadamente altos»</b>.",
         "Toda tarea sincronizada necesita <b>afinidad fijada</b>: sin ella, el costo es impredecible."],
        [("paper-conmutacion-nucleos",
          "Elaboración propia con las cifras publicadas. Tiempo de conmutación en las dos configuraciones, en escala logarítmica."),
         ("paper-freertos-dos-asuntos",
          "Las tres cifras separadas en los dos asuntos que son: el planificador cumple, la sincronización entre núcleos no.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────────────────────── 10 · vTaskDelay, delay y espera activa
lamina(
    "ceder-o-retener-procesador",
    "Tres formas de esperar y su efecto sobre el procesador · Sesión 6",
    "Ceder o retener el procesador",
    envolver(f"""{cabecera(A, "Tres formas de esperar y su efecto sobre el procesador", "i-clock")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-check")}<code>vTaskDelay()</code></div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tBloquea la tarea y <b>cede el núcleo</b>. El planificador ejecuta
\t\t\t\t\t\t\totras tareas durante la espera y la reanuda al vencer el plazo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tResolución de 1 tick = 1 ms. Se escribe
\t\t\t\t\t\t\t<code>vTaskDelay(pdMS_TO_TICKS(20))</code>.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}<code>delay()</code></div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEn el núcleo de Arduino sobre ESP32 <b>también cede</b>: internamente
\t\t\t\t\t\t\tllama a <code>vTaskDelay()</code>. Es la excepción, no la regla: en
\t\t\t\t\t\t\totras placas Arduino ocupa el procesador.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tPor debajo de 1 ms no cede: <code>delay(0)</code> retorna sin
\t\t\t\t\t\t\tbloquear.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-bolt")}Espera activa</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t<code>while (!listo) {{}}</code> o
\t\t\t\t\t\t\t<code>delayMicroseconds()</code> <b>retienen el núcleo</b>. La tarea
\t\t\t\t\t\t\tsigue preparada y consume su turno completo sin avanzar.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tAdmisible solo para esperas de pocos microsegundos exigidas por un
\t\t\t\t\t\t\tperiférico.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tUna tarea de prioridad alta con espera activa impide ejecutarse a la
\t\t\t\t\t\t<b>tarea de reposo</b>, que es la que alimenta al watchdog de su
\t\t\t\t\t\tnúcleo. El sistema se reinicia con el mensaje
\t\t\t\t\t\t<code>Task watchdog got triggered</code>, y la causa no es el
\t\t\t\t\t\twatchdog: es la tarea que nunca cede.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Para un periodo estable, ninguna de las tres</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<code>vTaskDelay()</code> espera un plazo <em>desde el momento en que se
\t\t\t\t\t\tla llama</em>, de modo que el periodo real acumula el tiempo de proceso
\t\t\t\t\t\tde cada iteración y deriva. Para un periodo fijo se usa
\t\t\t\t\t\t<code>vTaskDelayUntil(&amp;ultimaVez, pdMS_TO_TICKS(10))</code>, que
\t\t\t\t\t\tespera <em>hasta</em> un instante absoluto y compensa esa variación.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-clock",
)

# ────────────────────────────────── 11 · dimensionamiento de la pila
lamina(
    "dimensionamiento-pila",
    "Dimensionamiento de la pila y detección del desbordamiento · Sesión 6",
    "Dimensionamiento de la pila",
    envolver(f"""{cabecera(A, "Dimensionamiento de la pila y detección del desbordamiento", "i-layers")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué ocupa la pila
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas variables locales de la tarea y de todas las funciones que
\t\t\t\t\t\t\t\tllame, más la dirección de retorno y el contexto guardado en cada
\t\t\t\t\t\t\t\tinterrupción. Un arreglo local de 1024 <code>float</code> ocupa
\t\t\t\t\t\t\t\t<b>4 kB de pila</b>, no del heap.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tCómo se mide
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>uxTaskGetStackHighWaterMark(handle)</code> devuelve, en
\t\t\t\t\t\t\t\tpalabras, la <b>menor cantidad de pila libre</b> que ha tenido la
\t\t\t\t\t\t\t\ttarea desde que arrancó. No es el valor actual: es el peor caso
\t\t\t\t\t\t\t\tobservado, que es la magnitud que decide.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Procedimiento de dimensionado</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tPartir de <b>4096 palabras</b>, ejercitar todos los caminos de la
\t\t\t\t\t\t\t\ttarea (incluidos los de error, que suelen ser los que más
\t\t\t\t\t\t\t\tconsumen), leer la marca y dejar un <b>margen del 30 %</b>. Ajustar
\t\t\t\t\t\t\t\tsin haber recorrido las rutas de error produce desbordamientos que
\t\t\t\t\t\t\t\tsolo aparecen cuando algo falla.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="term">[PILA] muestreo     asignada=4096  libre_min=2884  uso=1212 (30%)
[PILA] publicacion  asignada=4096  libre_min= 312  uso=3784 (92%)  &lt;-- ajustada
[PILA] interfaz     asignada=2048  libre_min=1602  uso= 446 (22%)
[HEAP] libre=178432  minima_historica=164208  fragmento_mayor=113804</div>

\t\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t\t<div class="problem-card__head">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tSíntoma del desbordamiento
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tReinicios sin patrón aparente, a veces tras horas de
\t\t\t\t\t\t\t\t\tfuncionamiento, con una traza de retorno que apunta a código sin
\t\t\t\t\t\t\t\t\trelación con la causa.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\t<b>Por qué ocurre.</b> La tarea escribe más allá de su pila y
\t\t\t\t\t\t\t\t\tcorrompe la memoria contigua, que pertenece a otra tarea. El
\t\t\t\t\t\t\t\t\tfallo se manifiesta donde se lee el dato corrompido, no donde se
\t\t\t\t\t\t\t\t\tescribió.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\t<b>Cómo comprobarlo.</b> Imprimir el high water mark de todas las
\t\t\t\t\t\t\t\t\ttareas cada pocos segundos. Una que se acerque a cero identifica
\t\t\t\t\t\t\t\t\ta la culpable antes de que corrompa nada.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ───────────────────────────────────── 12 · La hora del código · 25
lamina(
    "codigo-25-afinidad-nucleos",
    "Código 25 · Costo de sincronizar entre núcleos · Sesión 6",
    "La hora del código · Core affinity",
    hora_del_codigo(
        25,
        "Costo de sincronizar dos tareas dentro y entre núcleos",
        "Cuánto tarda un semáforo en pasar el control de una tarea a otra, medido sobre el hardware empleado en "
        "dos configuraciones: las dos tareas fijadas al mismo núcleo, y una en cada núcleo. Se repite "
        "<b>1000 veces</b> y se comunican mínimo, media y máximo.",
        "Un <b>semáforo binario</b> es una señal de un solo permiso: una tarea lo entrega, otra lo toma, y esa "
        "entrega es lo que se cronometra. <code>esp_timer_get_time()</code> da microsegundos desde el arranque, "
        "resolución suficiente aquí. El <b>error del instrumento</b> se obtiene llamando dos veces seguidas a la "
        "función de medida y restando: a esta escala no es despreciable.",
        "El <b>ESP32</b> conmuta un LED en el <b>GPIO 25</b> con resistencia de 220 Ω cada 100 intercambios. No "
        "hace falta nada más: la medida es interna al procesador.",
        """[CONFIG] repeticiones=1000  reloj=240 MHz error_medida=4.5 us
[MISMO_NUCLEO] min=0.012 ms media=0.012 ms max=0.013 ms
[ENTRE_NUCLEOS] min=0.164 ms media=0.171 ms max=0.209 ms
[RELACION] entre_nucleos / mismo_nucleo = 14.3x
[AVISO] sin afinidad fijada cae en cualquiera de los dos casos""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Crea dos tareas que se pasen el control con un semáforo binario: la primera lo entrega, la segunda lo toma y lo devuelve. Mide el tiempo de ida y vuelta con <code>esp_timer_get_time()</code> y repítelo 1000 veces. Ejecuta la medida en dos configuraciones seleccionables por constante: ambas tareas fijadas al núcleo 1, y una en cada núcleo. Descuenta el tiempo de la propia función de medida, obtenido llamándola dos veces seguidas. Imprime a 115200 baudios mínimo, media y máximo de cada configuración, y su cociente.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del ciclo de medida, con el descuento del error del instrumento como un paso explícito. Y un <b>diagrama de bloques</b> con las dos configuraciones enfrentadas, mostrando por dónde viaja la señalización en cada una.""",
        "La línea <code>[RELACION]</code>: pasar el control entre núcleos cuesta <b>14,3 veces</b> más que dentro "
        "del mismo. Comparar después mínimo y máximo de cada configuración: entre núcleos el máximo se separa de "
        "la media mucho más que dentro de uno, y esa dispersión es la que vuelve impredecible un plazo. La última "
        "línea es el aviso que importa al diseñar: sin afinidad fijada, cada ejecución cae en un caso o en otro.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-resistor></wokwi-resistor></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ────────────────────────── 13 · artículo · sobrecarga del planificador
lamina(
    "paper-sobrecarga-planificador",
    "Variabilidad del costo del planificador según la carga de tareas · Sesión 6",
    "Artículo · Sobrecarga del planificador",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY-NC-ND 4.0",
        "<b>Grosu, R.; Sifakis, J.; Tripakis, S.</b> (2021). Measurement-based timing analysis of the FreeRTOS "
        "scheduler overhead. <i>Journal of Systems Architecture</i>. <code>doi:10.1016/j.sysarc.2021.102132</code>",
        "Variabilidad del costo del planificador según la carga de tareas",
        ["Cuantificar el tiempo que consume el <b>propio sistema operativo</b>, al margen de la aplicación.",
         "Dos fuentes: la función de <b>tick</b> y la conmutación de contexto.",
         "Escenario de <b>diez tareas periódicas</b>, provocando el instante crítico a propósito."],
        ["Tick sin tareas que desbloquear: <b>1,5 µs</b>. Es el valor más frecuente.",
         "Cada tarea que entra en la lista de preparadas añade <b>3,7 µs</b>.",
         "Peor caso observado con las diez coincidiendo: <b>60,75 µs</b>.",
         "Cuarenta veces el valor habitual, en el mismo sistema y sin cambiar nada."],
        ["El costo del tick <b>no es constante</b>: depende de cuántas tareas se desbloquean.",
         "Suponer el peor caso en todos los ticks introduce un pesimismo que su modelo reduce.",
         "El valor que suele darse por bueno es el más frecuente, no el que decide el plazo."],
        [("paper-costo-tick",
          "Elaboración propia con las cifras publicadas. El modelo lineal y el peor caso medido en el instante crítico."),
         ("paper-tick-pesimismo",
          "El pesimismo que su modelo reduce: suponer el peor caso en cada tick reserva cuarenta veces lo que cuesta en el caso más frecuente.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────── 14 · condición de carrera
lamina(
    "condicion-carrera",
    "Acceso concurrente a un recurso compartido · Sesión 6",
    "Condición de carrera",
    envolver(f"""{cabecera(B, "Acceso concurrente a un recurso compartido", "i-alert")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tHay <b>condición de carrera</b> cuando el resultado depende del
\t\t\t\t\t\t\t\torden en que se intercalan dos tareas. Una operación que en el
\t\t\t\t\t\t\t\tcódigo fuente parece indivisible se traduce en varias
\t\t\t\t\t\t\t\tinstrucciones, y el planificador puede interrumpir entre ellas.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tPor qué <code>contador++</code> no es indivisible
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe compila en tres instrucciones: <b>leer</b> el valor de memoria a
\t\t\t\t\t\t\t\tun registro, <b>incrementar</b> el registro y <b>escribir</b> el
\t\t\t\t\t\t\t\tresultado. Si dos tareas leen antes de que ninguna escriba, ambas
\t\t\t\t\t\t\t\tescriben el mismo valor y un incremento se pierde.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>volatile</code> <b>no resuelve</b> una condición de carrera.
\t\t\t\t\t\t\t\tObliga al compilador a releer la variable de memoria, pero no hace
\t\t\t\t\t\t\t\tindivisible la secuencia de tres instrucciones. Sirve para que el
\t\t\t\t\t\t\t\tcompilador no cachee el valor, no para excluir accesos simultáneos.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--no">Así no</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">dos tareas, un contador</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>volatile uint32_t cuenta = 0;   // no basta

void tareaA(void *) {{ for(;;) <span class="hl hl--hit">cuenta++;</span> }}
void tareaB(void *) {{ for(;;) <span class="hl hl--hit">cuenta++;</span> }}

// Tras 1 000 000 de incrementos por tarea,
// cuenta vale menos de 2 000 000.</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[CARRERA] esperado=2000000  obtenido=1338472  perdidos=661528 (33%)
[CARRERA] mismo nucleo:    esperado=2000000  obtenido=1994310  perdidos=0.3%
[MUTEX]   esperado=2000000  obtenido=2000000  perdidos=0</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tLa segunda línea es la que hace peligroso este fallo: con ambas
\t\t\t\t\t\t\t\ttareas en el mismo núcleo se pierde el 0,3 %, y el programa parece
\t\t\t\t\t\t\t\tcorrecto en el ensayo. El error aparece al repartirlas entre
\t\t\t\t\t\t\t\tnúcleos, meses después.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-alert",
)

# ───────────────────────────────────── 15 · La hora del código · 26
lamina(
    "codigo-26-condicion-carrera",
    "Código 26 · Demostración de una condición de carrera · Sesión 6",
    "La hora del código · Condición de carrera",
    hora_del_codigo(
        26,
        "Demostración medible de una condición de carrera y de su corrección",
        "Dos tareas incrementan el mismo contador un millón de veces cada una. El ejercicio produce la pérdida de "
        "incrementos de forma reproducible, la mide en tres configuraciones (mismo núcleo, núcleos distintos y con "
        "mutex) y pone precio a la corrección.",
        "<code>cuenta++</code> no es una operación única: son <b>tres instrucciones</b> (leer, incrementar, "
        "escribir) y entre ellas puede entrar la otra tarea. <code>volatile</code> impide que el compilador guarde "
        "la variable en un registro, pero <b>no</b> hace atómico el incremento: es el error de concepto más "
        "frecuente. Un <b>mutex</b> sí lo consigue, cerrando el paso mientras dura la secuencia.",
        "El <b>ESP32</b> conmuta un LED en el <b>GPIO 25</b> y otro en el <b>GPIO 26</b>, uno por tarea, ambos con "
        "resistencia de 220 Ω a masa.",
        """[PRUEBA] incrementos por tarea=1000000
[MISMO_NUCLEO]  obtenido=1994310  perdidos=5690 (0.3%)
[DOS_NUCLEOS]   obtenido=1338472  perdidos=661528 (33.1%)
[CON_MUTEX]     obtenido=2000000  perdidos=0     tiempo=+41%
[CONCLUSION] corregir cuesta tiempo; no corregir cuesta datos""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Declara un contador <code>volatile uint32_t</code> compartido. Crea dos tareas que lo incrementen un millón de veces cada una y avisen al terminar. Ejecuta la prueba tres veces: ambas tareas en el núcleo 1, una en cada núcleo, y una en cada núcleo con el acceso protegido por un mutex creado con <code>xSemaphoreCreateMutex()</code>. Mide también el tiempo total de cada configuración. Imprime a 115200 baudios el valor obtenido, los incrementos perdidos, su porcentaje y el sobrecosto en tiempo de la versión con mutex.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una tarea, con la sección protegida marcada como un bloque aparte. Y un <b>diagrama de tiempos</b> con las tres instrucciones de <code>cuenta++</code> de ambas tareas intercaladas, señalando el punto exacto donde se pierde un incremento.""",
        "Comparar las dos primeras cifras de pérdida: <b>0,3 %</b> con las dos tareas en un núcleo y <b>33,1 %</b> "
        "con una en cada uno, con el código idéntico. Ahí está la razón de que estos fallos superen las pruebas y "
        "aparezcan en operación. La tercera línea da el precio de la corrección (un <b>41 %</b> más de tiempo), "
        "que conviene tener como dato y no como intuición a la hora de decidir dónde poner el mutex.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ───────────────────────────────────────────────────────── 16 · colas
lamina(
    "colas",
    "Colas: transferencia de mensajes por copia · Sesión 6",
    "Colas y patrón productor-consumidor",
    envolver(f"""{cabecera(B, "Colas: transferencia de mensajes por copia", "i-link")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna <b>cola</b> transfiere mensajes <b>por copia</b>: el dato se
\t\t\t\t\t\t\t\tduplica al enviarlo, de modo que emisor y receptor nunca tocan la
\t\t\t\t\t\t\t\tmisma memoria y no hace falta protegerla.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa cola tiene capacidad fija. Enviar a una cola llena bloquea al
\t\t\t\t\t\t\t\temisor; recibir de una vacía bloquea al receptor. Ese bloqueo es lo
\t\t\t\t\t\t\t\tque sincroniza a las dos tareas sin código adicional.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>xQueueCreate(largo, sizeof(Muestra))</code>,
\t\t\t\t\t\t\t\t<code>xQueueSend()</code> y <code>xQueueReceive()</code>, con un
\t\t\t\t\t\t\t\tplazo máximo de espera en cada una. Desde una rutina de
\t\t\t\t\t\t\t\tinterrupción hay que usar la variante
\t\t\t\t\t\t\t\t<code>xQueueSendFromISR()</code>, cuya semántica es distinta.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Qué desacopla</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn productor rápido y un consumidor lento. La cola absorbe las
\t\t\t\t\t\t\t\tráfagas mientras su capacidad lo permita; superada esa capacidad,
\t\t\t\t\t\t\t\thay que decidir <b>de forma explícita</b> qué se descarta, y esa
\t\t\t\t\t\t\t\tdecisión pertenece al requisito.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok"><span class="bd-node__title">Productor</span><span class="bd-node__body">Muestrea a 1 kHz. Copia cada muestra a la cola y sigue.</span></div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost"><span class="bd-node__title">Cola · 64 elementos</span><span class="bd-node__meta">64 ms de margen a 1 kHz</span></div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent"><span class="bd-node__title">Consumidor</span><span class="bd-node__body">Publica por red cada 10 s. Vacía la cola en bloque.</span></div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[COLA] capacidad=64  ocupacion_actual=3  ocupacion_maxima=61
[COLA] enviados=10000  recibidos=10000  descartados=0
[COLA] espera_maxima_productor=0 ms   espera_maxima_consumidor=998 ms</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa ocupación máxima de 61 sobre 64 avisa de que el margen es escaso:
\t\t\t\t\t\t\tuna ráfaga algo mayor empezaría a descartar muestras.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-link",
)

# ────────────────────────────────────────────────────────── 17 · mutex
lamina(
    "mutex",
    "Mutex e inversión de prioridad · Sesión 6",
    "Mutex e inversión de prioridad",
    envolver(f"""{cabecera(B, "Mutex e inversión de prioridad", "i-plug")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>mutex</b> garantiza que solo una tarea use a la vez un recurso
\t\t\t\t\t\t\t\tque no admite duplicado: un bus I²C, una pantalla, el puerto serie.
\t\t\t\t\t\t\t\tLa tarea lo toma, usa el recurso y lo devuelve.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t\tDel inglés <i>mutual exclusion</i>. Se traduce como exclusión mutua,
\t\t\t\t\t\t\t\taunque la interfaz mantiene el nombre abreviado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>xSemaphoreCreateMutex()</code>,
\t\t\t\t\t\t\t\t<code>xSemaphoreTake(m, plazo)</code> y
\t\t\t\t\t\t\t\t<code>xSemaphoreGive(m)</code>. Toda ruta de salida de la sección
\t\t\t\t\t\t\t\tprotegida, incluidos los retornos anticipados por error, debe
\t\t\t\t\t\t\t\tdevolverlo, o el recurso queda tomado para siempre.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tInversión de prioridad
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna tarea de prioridad <b>baja</b> toma el mutex. Una de prioridad
\t\t\t\t\t\t\t\t<b>alta</b> lo necesita y se bloquea. Entra entonces una de
\t\t\t\t\t\t\t\tprioridad <b>media</b>, que no necesita el mutex, expropia a la baja
\t\t\t\t\t\t\t\ty le impide devolverlo. La tarea de prioridad alta queda esperando
\t\t\t\t\t\t\t\tpor una de prioridad media.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost"><span class="bd-node__title">Baja</span><span class="bd-node__body">Toma el mutex y es expropiada antes de devolverlo.</span></div>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn"><span class="bd-node__title">Media</span><span class="bd-node__body">No usa el mutex, pero ocupa el procesador de forma indefinida.</span></div>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent"><span class="bd-node__title">Alta</span><span class="bd-node__body">Bloqueada esperando un recurso que la de baja no puede liberar.</span></div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Herencia de prioridad</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl mutex de FreeRTOS lo resuelve por sí solo: mientras retiene el
\t\t\t\t\t\t\t\trecurso, la tarea de prioridad baja <b>hereda</b> la prioridad de la
\t\t\t\t\t\t\t\tmás alta que lo espera, de modo que la media no puede expropiarla.
\t\t\t\t\t\t\t\tPor eso un mutex no es intercambiable con un semáforo binario: el
\t\t\t\t\t\t\t\tsemáforo no hereda.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-plug",
)

# ───────────────────────────────── 18 · semáforos y grupos de eventos
lamina(
    "semaforos-grupos-eventos",
    "Semáforos de señalización y grupos de eventos · Sesión 6",
    "Semáforos y grupos de eventos",
    envolver(f"""{cabecera(B, "Semáforos de señalización y grupos de eventos", "i-bolt")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-bolt")}Semáforo binario</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSeñaliza que algo ocurrió. Su uso característico es <b>avisar a una
\t\t\t\t\t\t\ttarea desde una rutina de interrupción</b>: la rutina lo entrega y
\t\t\t\t\t\t\tretorna en microsegundos; la tarea despierta y hace el trabajo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>xSemaphoreGiveFromISR()</code> desde la rutina;
\t\t\t\t\t\t\t<code>xSemaphoreTake()</code> desde la tarea.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Semáforo de conteo</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tAdministra un conjunto de recursos equivalentes y limitados. Se
\t\t\t\t\t\t\tinicializa con la cantidad disponible; tomarlo la reduce y devolverlo
\t\t\t\t\t\t\tla repone.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tTres memorias intermedias de captura: la cuarta tarea que las pida
\t\t\t\t\t\t\tqueda bloqueada hasta que se libere una.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-check")}Grupo de eventos</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tConjunto de bits, cada uno una condición. Una tarea espera a que
\t\t\t\t\t\t\t<b>varios se cumplan a la vez</b>, sin encadenar esperas.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tEnlace establecido, hora sincronizada y sensor calibrado: publicar
\t\t\t\t\t\t\texige los tres.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">{ico("i-target")}Notificación directa a tarea</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCuando el destinatario es <b>uno solo y conocido</b>, la
\t\t\t\t\t\t\t\tnotificación directa sustituye al semáforo. No crea ningún objeto:
\t\t\t\t\t\t\t\tusa un campo que toda tarea ya tiene, de modo que ahorra memoria y
\t\t\t\t\t\t\t\tciclos.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t\t<code>xTaskNotifyGive(handle)</code> y
\t\t\t\t\t\t\t\t<code>ulTaskNotifyTake()</code>. Su límite es justamente ese: un
\t\t\t\t\t\t\t\tdestinatario, no varios.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--si">Así sí</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">la rutina señala, la tarea trabaja</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>void IRAM_ATTR alFlanco() {{
  BaseType_t despertar = pdFALSE;
  <span class="hl hl--add">vTaskNotifyGiveFromISR(hTarea, &amp;despertar);</span>
  portYIELD_FROM_ISR(despertar);   // cede si procede
}}

void tareaEvento(void *) {{
  for (;;) {{
    <span class="hl hl--add">ulTaskNotifyTake(pdTRUE, portMAX_DELAY);</span>
    procesar();   // aquí sí se puede imprimir y calcular
  }}
}}</code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tEs el patrón «la rutina registra, el bucle procesa» de la sesión 4,
\t\t\t\t\t\t\tcon la tarea en el lugar del bucle.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-bolt",
)

# ────────────────────── 19 · artículo · sincronización no bloqueante
lamina(
    "paper-sincronizacion-no-bloqueante",
    "Reparto del costo de sincronización entre la sección crítica y el resto · Sesión 6",
    "Artículo · Sincronización no bloqueante",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Bertogna, M.; Marinoni, M.; Esposito, F.</b> (2020). Non-blocking synchronization protocols for "
        "mixed-criticality data sharing. <i>Real-Time Systems</i>. <code>doi:10.1007/s11241-020-09349-w</code>",
        "Reparto del costo de sincronización entre la sección crítica y el resto",
        ["Compartir datos entre una parte <b>con plazo</b> y otra sin él, en núcleos distintos.",
         "Con un mutex convencional, la parte crítica <b>queda esperando</b> a la que no lo es.",
         "Su peor caso pasa a depender de código sobre el que no se tiene control."],
        ["<b>Cinco protocolos no bloqueantes</b> para cuatro escenarios de productor y consumidor.",
         "La parte crítica <b>nunca repite</b> una operación: su tiempo queda acotado y pequeño.",
         "El costo se traslada por completo a la parte <b>sin plazo</b>, que sí reintenta.",
         "Evaluación sobre dos núcleos, con lector o escritor crítico en cada caso."],
        ["No repetir es la condición para que el tiempo de ejecución <b>tenga una cota</b>.",
         "La contrapartida asumida es el <b>peor tiempo de respuesta</b> de la parte no crítica.",
         "Lo que decide el protocolo es quién escribe y quién tiene el plazo, no el tipo de dato."],
        [("paper-sincronizacion-costo",
          "Modelo propio con los parámetros del eje, no medidas del artículo: con exclusión mutua el peor caso de la parte crítica hereda la espera ajena."),
         ("paper-sincronizacion-casos",
          "Los cuatro escenarios que cubren los cinco protocolos, según el recurso y el lado que tiene el plazo.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────────────────── 20 · mensajes frente a memoria compartida
lamina(
    "mensajes-vs-memoria-compartida",
    "Transferencia de mensajes frente a memoria compartida · Sesión 6",
    "Mensajes o memoria compartida",
    envolver(f"""{cabecera(B, "Transferencia de mensajes frente a memoria compartida", "i-layers")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Transferencia de mensajes</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada tarea posee sus datos y envía copias. No hay memoria que
\t\t\t\t\t\t\tproteger, de modo que no puede haber condición de carrera sobre ella.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Costo:</b> copiar. Una estructura de 200 bytes enviada a 1 kHz son
\t\t\t\t\t\t\t200 kB/s copiados dos veces, al enviar y al recibir.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Memoria compartida</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLas tareas acceden a la misma región, protegida con un mutex. No se
\t\t\t\t\t\t\tcopia nada.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Costo:</b> toda ruta de acceso debe tomar y devolver el mutex, y
\t\t\t\t\t\t\tbasta olvidarlo en una para introducir un fallo que no se reproduce.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Criterio</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<b>Mensajes por omisión.</b> La memoria compartida se justifica cuando
\t\t\t\t\t\tel dato es grande y la frecuencia alta (una imagen, un bloque de
\t\t\t\t\t\tmuestras) y copiarlo dominaría el tiempo de proceso. En ese caso se
\t\t\t\t\t\tcomparte el bloque y se envía por la cola <b>un puntero</b>, con la
\t\t\t\t\t\tregla de que quien lo recibe es su único propietario hasta devolverlo.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Mecanismo</th><th>Para qué</th><th>Memoria por objeto</th><th>Destinatarios</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr><td>Notificación directa</td><td>Avisar de un suceso</td><td>Ninguna: usa un campo de la tarea</td><td>Uno</td></tr>
\t\t\t\t\t\t\t<tr><td>Semáforo binario</td><td>Avisar de un suceso</td><td>Descriptor del objeto</td><td>Uno o varios</td></tr>
\t\t\t\t\t\t\t<tr><td>Cola</td><td>Transferir datos</td><td>Descriptor + largo × tamaño</td><td>Uno o varios</td></tr>
\t\t\t\t\t\t\t<tr><td>Mutex</td><td>Proteger un recurso único</td><td>Descriptor con herencia de prioridad</td><td>—</td></tr>
\t\t\t\t\t\t\t<tr><td>Grupo de eventos</td><td>Esperar varias condiciones</td><td>Descriptor de 24 bits útiles</td><td>Varios</td></tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ───────────────────────────────────── 21 · La hora del código · 27
lamina(
    "codigo-27-productor-consumidor",
    "Código 27 · Adquisición y publicación desacopladas por una cola · Sesión 6",
    "La hora del código · Productor y consumidor",
    hora_del_codigo(
        27,
        "Adquisición y publicación desacopladas por una cola",
        "El sistema completo de la sesión: una tarea muestrea a <b>200 Hz</b> y encola, otra vacía la cola cada "
        "<b>2 s</b> y promedia, y una tercera publica el diagnóstico. Las tres comparten el puerto serie, así que "
        "aparecen a la vez cola, mutex y prioridades.",
        "Una <b>cola</b> transporta datos entre tareas sin que ninguna espere a la otra: el productor deposita y "
        "sigue. <code>vTaskDelayUntil()</code> despierta en instantes fijos, no «N ms después de terminar», que es "
        "lo que va corriendo el periodo. Encolar <b>sin esperar</b> significa que si la cola está llena se "
        "descarta y se cuenta, en lugar de bloquear al productor.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> como sensor. Un LED en el <b>GPIO 25</b> "
        "conmuta cada 100 muestras y otro en el <b>GPIO 26</b> se enciende mientras el consumidor procesa, ambos "
        "con resistencia de 220 Ω.",
        """[TAREA] muestreo nucleo=1 prio=3 periodo=5 ms pila_min=2884
[TAREA] proceso nucleo=1 prio=2 periodo=2000 ms pila_min=2210
[TAREA] diagnost nucleo=0 prio=1 periodo=5000 ms pila_min=3012
[COLA]  ocupacion=12/64  max=51  enviados=40000  descartados=0
[PROC]  n=400  media=1.842 V  min=1.204 V  max=2.455 V
[SERIE] mutex: espera_maxima=3 ms contenciones=42""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Crea tres tareas. La de muestreo lee el GPIO 34 cada 5 ms con <code>vTaskDelayUntil()</code>, prioridad 3, núcleo 1, y encola la muestra con timestamp sin esperar si la cola está llena, contando los descartes. La de proceso, prioridad 2 y núcleo 1, vacía la cola cada 2 s y calcula media, mínimo y máximo. La de diagnóstico, prioridad 1 y núcleo 0, publica cada 5 s la ocupación de la cola, su máximo histórico y la pila libre mínima de las tres tareas. Todo acceso al puerto serie pasa por un mutex, y ninguna tarea lo retiene más de lo que dura su impresión. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la tarea de muestreo, con la rama del descarte cuando la cola está llena. Y un <b>diagrama de bloques</b> con las tres tareas, su núcleo y su prioridad, la cola que las une y el mutex que protege el puerto serie.""",
        "La línea <code>[COLA]</code>: ocupación 12 de 64, pero <b>máximo histórico 51</b>. La ocupación "
        "instantánea no dice nada; el máximo es lo que avisa de que la cola estuvo a punto de llenarse. Con "
        "<code>descartados=0</code> el reparto aguanta. Vigilar también la espera máxima del mutex del puerto "
        "serie: si creciera, alguna tarea lo estaría reteniendo más de lo que dura su impresión.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/potentiometer-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
""",
)

# ────────────────────────────────────────────────── 22 · deadlock
lamina(
    "deadlock",
    "Deadlock por orden de adquisición · Sesión 6",
    "Deadlock",
    envolver(f"""{cabecera(B, "Deadlock por orden de adquisición", "i-alert")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tCaso mínimo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tDos tareas y dos mutex. La tarea A toma el <b>bus</b> y pide la
\t\t\t\t\t\t\t\t<b>pantalla</b>; la tarea B toma la <b>pantalla</b> y pide el
\t\t\t\t\t\t\t\t<b>bus</b>. Cada una retiene lo que la otra necesita, y ninguna
\t\t\t\t\t\t\t\tpuede avanzar ni liberar.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Regla que lo elimina</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tFijar un <b>orden global de adquisición</b> y respetarlo en todo el
\t\t\t\t\t\t\t\tprograma: primero el bus, después la pantalla, siempre. Con un orden
\t\t\t\t\t\t\t\túnico el deadlock (interbloqueo) es imposible por construcción, sin necesidad
\t\t\t\t\t\t\t\tde detectarlo ni de recuperarse de él.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tRed de seguridad
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tTomar todo mutex con un <b>plazo máximo</b> en vez de
\t\t\t\t\t\t\t\t<code>portMAX_DELAY</code>. No corrige el diseño, pero convierte un
\t\t\t\t\t\t\t\tbloqueo silencioso en un error registrado que señala qué recurso y
\t\t\t\t\t\t\t\tqué tarea intervinieron.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--no">Así no</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">órdenes de adquisición opuestos</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>void tareaA(void *) {{
  <span class="hl hl--hit">xSemaphoreTake(mBus, portMAX_DELAY);</span>
  <span class="hl hl--hit">xSemaphoreTake(mPantalla, portMAX_DELAY);</span>
  ...
}}
void tareaB(void *) {{
  <span class="hl hl--hit">xSemaphoreTake(mPantalla, portMAX_DELAY);</span>
  <span class="hl hl--hit">xSemaphoreTake(mBus, portMAX_DELAY);</span>   // orden inverso
  ...
}}</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[BLOQUEO] tarea=A estado=Blocked espera=mPantalla retiene=mBus
[BLOQUEO] tarea=B estado=Blocked espera=mBus      retiene=mPantalla
[WDT] Task watchdog got triggered. The following tasks did not reset: A, B</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tEl deadlock no produce ningún mensaje propio: se manifiesta como
\t\t\t\t\t\t\tun aviso del watchdog, que señala el síntoma y no la causa.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-alert",
)

# ───────────────────────────── 23 · cuándo no está justificado
lamina(
    "cuando-no-usar-rtos",
    "Condiciones en las que el bucle único sigue siendo la respuesta · Sesión 6",
    "Cuándo no usar un sistema operativo",
    envolver(f"""{cabecera(B, "Condiciones en las que el bucle único sigue siendo la respuesta", "i-target")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tCriterio
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSi el problema se resuelve con un bucle y máquinas de estados,
\t\t\t\t\t\t\t\tincorporar tareas <b>añade complejidad y errores de reproducción
\t\t\t\t\t\t\t\tdifícil</b> sin resolver nada. La concurrencia no es una mejora por
\t\t\t\t\t\t\t\tsí misma.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn fallo de concurrencia aparece con baja frecuencia y no se
\t\t\t\t\t\t\t\treproduce a voluntad. El esfuerzo se desplaza de la depuración,
\t\t\t\t\t\t\t\tdonde deja de ser eficaz, hacia el diseño.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t\t\t<tr><th>Situación</th><th>Solución adecuada</th></tr>
\t\t\t\t\t\t\t\t</thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td>Todas las actividades ocupan menos de 1 ms por iteración</td><td>Bucle con máquinas de estados</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Los periodos son múltiplos entre sí y no compiten</td><td>Bucle con máquinas de estados</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Una operación bloqueante de cientos de ms convive con un periodo de pocos ms</td><td><b>Tareas</b></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Hay que usar una biblioteca cuya llamada es bloqueante y no se puede trocear</td><td><b>Tareas</b></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Se quiere aprovechar el segundo núcleo para trabajo de cálculo</td><td><b>Tareas</b></td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Medir antes de optimizar</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tAntes de repartir en tareas conviene disponer de tres cifras:
\t\t\t\t\t\t\t\t<b>ocupación de procesador por tarea</b>, <b>marca de ocupación
\t\t\t\t\t\t\t\tmáxima de pila</b> y <b>memoria libre</b>. Sin ellas, el reparto se
\t\t\t\t\t\t\t\tdecide por intuición y suele resultar peor que el bucle que
\t\t\t\t\t\t\t\tsustituye.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-target",
)

# ─────────────────────────────────────── 24 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes con tareas concurrentes · Sesión 6",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes con tareas concurrentes", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("Reinicio por watchdog", "El sistema se reinicia con <code>Task watchdog got triggered</code> y el nombre de una tarea.", "Esa tarea no cede el procesador: contiene una espera activa o un cálculo largo sin <code>vTaskDelay()</code>. La tarea de reposo no llega a ejecutarse y no alimenta al watchdog.", "Localizar el bucle sin cesión en la tarea nombrada. Añadir <code>vTaskDelay(1)</code> confirma el diagnóstico, aunque la corrección definitiva sea reestructurar el cálculo.", "i-clock")}
{problema("Traza serie entremezclada", "Las líneas del monitor aparecen cortadas y superpuestas entre sí.", "Varias tareas escriben en el puerto serie sin protección. La escritura no es indivisible y el planificador interrumpe a mitad de línea.", "Proteger todo acceso al puerto con un mutex. Si el desorden desaparece, la causa era esa.", "i-terminal")}
{problema("Reinicios aleatorios sin patrón", "El equipo se reinicia tras minutos u horas, con trazas de retorno distintas cada vez.", "Desbordamiento de pila de alguna tarea: escribe fuera de su región y corrompe memoria ajena. El fallo se manifiesta lejos de donde se produjo.", "Imprimir <code>uxTaskGetStackHighWaterMark()</code> de todas las tareas de forma periódica. La que se acerque a cero es la responsable.", "i-layers")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("El periodo de muestreo no se cumple", "La tarea de adquisición pierde su ritmo cuando el usuario interactúa con el equipo.", "Asignación de prioridades por visibilidad de la función y no por requisito temporal: la tarea de interfaz tiene prioridad superior a la de muestreo.", "Comparar la prioridad de ambas tareas con su plazo. La que tiene plazo más corto debe tener prioridad mayor.", "i-sliders")}
{problema("Retrasos de cientos de milisegundos sin causa aparente", "Dos tareas que se sincronizan responden con lentitud irregular pese a estar ambas desocupadas.", "Las tareas no tienen afinidad fijada y el planificador las ha repartido entre núcleos distintos, donde la sincronización cuesta mucho más.", "Fijarlas al mismo núcleo con <code>xTaskCreatePinnedToCore()</code> y volver a medir. Es el resultado del artículo de esta sesión.", "i-cpu")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 25 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 6 · Sesión 6",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("RTOS", "real-time operating system", "Sistema operativo cuyo planificador garantiza un plazo máximo entre que una tarea queda preparada y recibe el procesador. La garantía es sobre el peor caso.")}
{termino("Tarea", "task", "Función con bucle propio y pila propia. La pila es lo que permite interrumpirla en cualquier punto y reanudarla exactamente ahí.")}
{termino("Planificador expropiativo", "preemptive scheduler", "Planificador que interrumpe de inmediato a la tarea en ejecución cuando otra de prioridad superior queda preparada, sin esperar a que ceda.")}
{termino("Tick", "", "Interrupción periódica del sistema, de 1 ms en el ESP32. Es la unidad mínima de tiempo del planificador y el instante en que revisa los plazos vencidos.")}
{termino("Condición de carrera", "race condition", "Situación en que el resultado depende del orden en que se intercalan dos tareas sobre un dato compartido.")}
{termino("Cola", "queue", "Mecanismo que transfiere mensajes por copia entre tareas. Emisor y receptor no comparten memoria, de modo que no hace falta protegerla.")}
{termino("Mutex", "", "Objeto que garantiza el uso exclusivo de un recurso no replicable. En FreeRTOS aplica herencia de prioridad, a diferencia del semáforo binario.")}
{termino("Inversión de prioridad", "priority inversion", "Situación en que una tarea de prioridad alta espera de forma indirecta a una de prioridad media, a través de una de prioridad baja que retiene el recurso.")}
{termino("Deadlock", "interbloqueo", "Bloqueo mutuo de dos o más tareas, cada una reteniendo el recurso que la otra necesita. Se elimina fijando un orden global de adquisición.")}
{termino("Core affinity", "afinidad de núcleo", "Núcleo al que queda fijada una tarea. Dejarla sin fijar permite al planificador moverla, con un costo de sincronización medible.")}
{termino("High water mark de pila", "stack high water mark", "Menor cantidad de pila libre que ha tenido una tarea desde que arrancó. Es el peor caso observado, no el valor actual.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 26 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 6 · Sesión 6",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-cpu")}Tareas y planificador</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLas tareas no aceleran el sistema: acotan el peor caso. La prioridad
\t\t\t\t\t\t\tse asigna por requisito temporal, nunca por la importancia aparente
\t\t\t\t\t\t\tde la función.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tToda tarea sincronizada con otra se fija al mismo núcleo:
\t\t\t\t\t\t\tsincronizar entre núcleos costó <b>190 ms</b> frente a
\t\t\t\t\t\t\t<b>0,012 ms</b> en la medida de referencia.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-link")}Comunicación</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tColas por omisión, porque transfieren por copia y no hay memoria que
\t\t\t\t\t\t\tproteger. Mutex solo para recursos únicos, con orden global de
\t\t\t\t\t\t\tadquisición.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t<code>volatile</code> no resuelve una condición de carrera. La
\t\t\t\t\t\t\tcorrección tiene un costo en tiempo; la ausencia de corrección lo
\t\t\t\t\t\t\ttiene en datos.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a la sesión siguiente</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">La comunicación como tarea independiente</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLas peticiones de red se atienden en su propia tarea, en el núcleo 0,
\t\t\t\t\t\t\t\tsin detener la adquisición.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Medir antes de repartir</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tOcupación por tarea, high water mark y memoria libre son las tres
\t\t\t\t\t\t\t\tcifras previas a cualquier decisión de diseño.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">El costo de la pila TLS</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa sesión 7 añade cifrado del transporte, cuyo consumo de memoria
\t\t\t\t\t\t\t\tobliga a revisar el dimensionado que aquí se establece.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 27 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 6 · Sesión 6",
    "Referencias",
    envolver(f"""{cabecera(B, "Referencias", "i-paper")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Los tres artículos son de acceso abierto.</strong> El
\t\t\t\t\tidentificador lleva al texto completo sin suscripción.
\t\t\t\t</p>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Measuring the Performance of FreeRTOS on ESP32 Multi-Core</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Arm, J.; Baštán, O.; Mihálik, O.; Bradáč, Z. (2022). <i>IFAC-PapersOnLine</i> 55(4), 292-297. CC BY-NC-ND 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1016/j.ifacol.2022.06.048</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Core affinity · Ejemplo 25</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Analysis of FreeRTOS Overheads on Periodic Tasks</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Miranda, B. D.; de Oliveira, R. S.; Carminati, A. (2021). <i>Anais do XX WPerformance</i>, 119-130. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.5753/wperformance.2021.15728</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Costo del planificador · Elección de periodos</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Non-Blocking Synchronization Between Real-Time and Non-Real-Time Applications</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Ruiz, A.; Rivas, M. A.; Harbour, M. G. et al. (2020). <i>IEEE Access</i> 8, 147618-147634. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/ACCESS.2020.3015385</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Colas · Mutex · Reparto del costo</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-06/</code>, junto a otros tres sobre consumo y domótica. El índice completo, en <code>src/paper/INDICE.md</code>.</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Las doce sesiones</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

{credito("El material del curso; cada artículo citado conserva su propia licencia.")}"""),
    icono="i-paper",
    clases="slide",
)

if __name__ == "__main__":
    _gen.generar_desde(
        {"clase": "clase-06", "sesion": "Sesión 6", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
