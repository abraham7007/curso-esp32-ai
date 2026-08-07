#!/usr/bin/env python3
"""Sesión 11 — Firmware compilado y runtime interpretado. Agentes de IA.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_11.py
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

A = "01 · Compilado frente a interpretado"
B = "02 · Agentes de IA en el flujo embebido"

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
    "Sesión 11 · Firmware compilado y runtime interpretado. Agentes de IA",
    "Compilado, interpretado y agentes",
    portada(
        "Sesión 11",
        "Firmware compilado y<br />runtime interpretado",
        "Comportamiento definido fuera del binario.",
        "Agentes de IA en el flujo de trabajo embebido.",
        [
         ("i-layers", "Runtime embebido frente a binario"),
         ("i-sliders", "Reglas interpretadas y su costo"),
         ("i-robot", "Agentes: ciclo, capacidades y permisos"),
         ("i-check", "Modos de fallo del código generado"),
        ],
        "02-modelo-de-las-diez-sesiones.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ─────────────────────── 02 · el modelo de las diez sesiones anteriores
lamina(
    "modelo-de-las-diez-sesiones",
    "El modelo empleado hasta aquí y su límite · Sesión 11",
    "El modelo empleado hasta aquí",
    envolver(f"""{cabecera(A, "El modelo empleado hasta aquí y su límite", "i-cpu")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tLo que se ha hecho en diez sesiones
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCódigo compilado en un <b>binario único</b>. Toda modificación del
\t\t\t\t\t\t\t\tcomportamiento (cambiar un umbral, añadir una regla) exige
\t\t\t\t\t\t\t\trecompilar y regrabar el dispositivo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Lo que eso da y lo que cuesta</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tDa el <b>máximo rendimiento y el máximo determinismo</b>: el
\t\t\t\t\t\t\t\tcompilador conoce todo el programa y no hay ninguna capa entre el
\t\t\t\t\t\t\t\tcódigo y el procesador. Cuesta que el ciclo de cambio sea largo, y
\t\t\t\t\t\t\t\tque el usuario no pueda adaptar nada sin herramientas de desarrollo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Cambiar un umbral · modelo compilado</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Editar, compilar, grabar, reiniciar. Con OTA, además: publicar, descargar, verificar y confirmar.</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">minutos, y un despliegue completo del parque</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↕</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Cambiar un umbral · comportamiento interpretado</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Enviar el valor nuevo. El firmware no cambia y no hay nada que revertir.</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">segundos, sin riesgo de dejar el equipo inalcanzable</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa comparación no es «uno mejor que otro». Un dispositivo que ya
\t\t\t\t\t\t\t\tacepta parámetros por su API, como el de la sesión 9, tiene la mitad
\t\t\t\t\t\t\t\tdel camino hecha: lo que esta sesión examina es hasta dónde conviene
\t\t\t\t\t\t\t\tllevar esa idea.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ──────────────────────────────── 03 · definición de runtime embebido
lamina(
    "runtime-embebido",
    "Runtime embebido: firmware que interpreta comportamiento externo · Sesión 11",
    "Runtime embebido",
    envolver(f"""{cabecera(A, "Runtime embebido: firmware que interpreta comportamiento externo", "i-layers")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tFirmware que <b>ejecuta comportamiento definido fuera del
\t\t\t\t\t\t\t\tbinario</b>, en forma de guiones, reglas, archivos de configuración
\t\t\t\t\t\t\t\to modelos. El binario deja de ser la funcionalidad y pasa a ser la
\t\t\t\t\t\t\t\tplataforma sobre la que se define.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tGradación, no dicotomía
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEntre el binario cerrado y el intérprete completo hay grados: un
\t\t\t\t\t\t\t\tumbral en NVS (memoria no volátil), una tabla de reglas en un archivo, un
\t\t\t\t\t\t\t\tguion. Cada paso gana flexibilidad y pierde algo de rendimiento, de
\t\t\t\t\t\t\t\tdeterminismo y de memoria.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Antecedente</th><th>Qué interpreta</th><th>Resultado observado</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>MicroPython</b></td><td>Guiones en Python</td><td>Iteración muy rápida; exige mucha más memoria</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Lua sobre NodeMCU</b></td><td>Guiones en Lua</td><td>Intérprete pequeño; pocas bibliotecas disponibles</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>ESPHome</b></td><td>Reglas declarativas</td><td>No hace falta programar; solo lo previsto es expresable</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Berry en Tasmota</b></td><td>Guiones compactos</td><td>Pensado para memoria escasa</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Node-RED</b></td><td>Flujos visuales</td><td>Se ejecuta fuera del dispositivo, no dentro</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>WebAssembly</b></td><td>Módulos compilados portables</td><td>Aislamiento y portabilidad; es lo que estudian los artículos</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tNinguno sustituyó al firmware compilado: cada uno ocupó el nicho en
\t\t\t\t\t\t\tque su compromiso concreto compensaba.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ───────────────────── 04 · comparación entre los dos modelos
lamina(
    "comparacion-modelos",
    "Ocho dimensiones para comparar los dos modelos · Sesión 11",
    "Comparación entre los dos modelos",
    envolver(f"""{cabecera(A, "Ocho dimensiones para comparar los dos modelos", "i-target")}

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Dimensión</th><th>Firmware compilado</th><th>Comportamiento interpretado</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr><td><b>Velocidad de iteración</b></td><td>Minutos: compilar, grabar, reiniciar</td><td>Segundos: enviar el guion</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Rendimiento</b></td><td>Máximo; sin capa intermedia</td><td>Menor; cada instrucción pasa por el intérprete</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Determinismo</b></td><td>Acotable; se puede medir el peor caso</td><td>Difícil de acotar: recolección de memoria y despacho dinámico</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Memoria</b></td><td>Solo el programa</td><td>Programa, intérprete y estructuras en ejecución</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Depuración</b></td><td>Traza de retorno y depurador por interfaz</td><td>Errores del guion, a veces solo en ejecución</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Superficie de ataque</b></td><td>La del firmware</td><td>Además: quien pueda enviar un guion decide qué hace el equipo</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Certificación</b></td><td>Se certifica un binario concreto</td><td>El comportamiento cambia después de certificar</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Mantenimiento</b></td><td>Una versión por parque</td><td>Tantas configuraciones como instalaciones</td></tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Las dos filas que suelen decidir</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<b>Certificación</b> y <b>superficie de ataque</b>. Un equipo con
\t\t\t\t\t\trequisito de seguridad funcional se certifica sobre un binario concreto,
\t\t\t\t\t\ty un comportamiento que cambia después invalida esa certificación. Y
\t\t\t\t\t\tquien pueda enviar un guion decide qué hace el dispositivo, lo que
\t\t\t\t\t\tconvierte el canal de envío en un mecanismo tan crítico como la firma del
\t\t\t\t\t\tfirmware de la sesión 10.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-target",
)

# ────────────────────────────────────── 05 · La hora del código · 44
lamina(
    "codigo-44-reglas-interpretadas",
    "Código 44 · Reglas interpretadas frente a umbral compilado · Sesión 11",
    "La hora del código · Reglas interpretadas",
    hora_del_codigo(
        44,
        "Reglas interpretadas frente a umbral compilado en el binario",
        "La misma función (encender una salida cuando la magnitud cruza un umbral) resuelta con el valor "
        "<b>compilado</b> y con una <b>regla leída de un archivo</b>. Se mide lo que cuesta cada versión al "
        "evaluar y lo que tarda cada una en aceptar un cambio de umbral.",
        "Una <b>constante de compilación</b> queda fijada en el binario: cambiarla obliga a compilar y grabar. Un "
        "<b>intérprete</b> lee la regla en ejecución, así que el mismo binario admite comportamientos distintos, "
        "pero paga la evaluación en cada muestra. Las magnitudes a medir son el <b>tiempo de evaluación</b> y el "
        "<b>tiempo de cambio</b>.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> y controla un LED en el <b>GPIO 25</b> con "
        "resistencia de 220 Ω.",
        """[COMP] umbral compilado=2.00 V  evaluacion=0.4 us binario=284 kB
[INT]  regla de /reglas.json: si v&gt;2.00 entonces led=1
[INT]  evaluacion=41 us binario=312 kB  memoria extra=6.2 kB
[CAMBIO] compilado: editar+compilar+grabar = 94 s
[CAMBIO] interpretado: subir archivo = 2 s
[RELACION] interpretado: 100x mas lento, 47x mas rapido de cambiar""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, LittleFS y ArduinoJson.

<b>2. Firmware.</b> Implementa las dos versiones seleccionables por constante de compilación. La compilada lleva el umbral como <code>constexpr</code>. La interpretada lee de <code>/reglas.json</code> una lista de reglas con condición y acción, y las evalúa en cada muestra. Mide con <code>esp_timer_get_time()</code> cuánto tarda cada versión en evaluar la condición, y registra el tamaño del binario y la memoria adicional que consume el intérprete. Cronometra además cuánto tarda cada forma de cambiar el umbral, desde la decisión hasta el dispositivo funcionando. Emite a 115200 baudios el resumen comparado.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una muestra en cada versión, uno al lado del otro, con la lectura y evaluación de la regla visible solo en la interpretada. Y las <b>dos rutas de cambio</b> enfrentadas, con sus pasos y sus tiempos.""",
        "La última línea reúne el compromiso: <b>100 veces más lento</b> al evaluar y <b>47 veces más rápido</b> "
        "de cambiar. Ninguna de las dos cifras decide sola. Multiplicar los 41 µs por la frecuencia de muestreo "
        "del proyecto propio y comparar con el periodo: si se lleva una fracción apreciable, la ruta interpretada "
        "no cabe por mucho que ahorre en el cambio.",
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

# ────────────────── 05b · simulación del costo de interpretar
lamina(
    "simulacion-costo-interpretar",
    "Costo de interpretar según el número de reglas · Sesión 11",
    "Costo de interpretar",
    envolver(f"""{cabecera(A, "Costo de interpretar según el número de reglas", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué se compara
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl mismo conjunto de condiciones evaluado con el valor compilado
\t\t\t\t\t\t\t\t(<b>0,4 µs</b> por condición) y con el intérprete de la lámina
\t\t\t\t\t\t\t\tanterior, <b>41 µs</b>. Ambas cifras son las que mide el ejemplo 44.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCon pocas reglas y periodo holgado, la diferencia no se nota y la
\t\t\t\t\t\t\t\tflexibilidad sale gratis. Al acortar el periodo o multiplicar las
\t\t\t\t\t\t\t\treglas, la versión interpretada agota el presupuesto del bucle
\t\t\t\t\t\t\t\tmientras la compilada sigue holgada. El punto en que eso ocurre es lo
\t\t\t\t\t\t\t\tque decide, y depende del caso concreto.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="int-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Ocupación del periodo por la evaluación de las reglas, comparada entre la versión compilada y la interpretada, frente al presupuesto disponible"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<label for="int-reglas" class="text-sm font-medium">Número de reglas</label>
\t\t\t\t\t\t\t\t<input type="range" id="int-reglas" min="1" max="120" step="1" value="20" />
\t\t\t\t\t\t\t\t<span class="readout" id="int-reglas-lec">20</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="controls mt-2">
\t\t\t\t\t\t\t\t<label for="int-periodo" class="text-sm font-medium">Periodo del bucle</label>
\t\t\t\t\t\t\t\t<input type="range" id="int-periodo" min="1" max="50" step="1" value="10" />
\t\t\t\t\t\t\t\t<span class="readout" id="int-periodo-lec">10 ms</span>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item metric__item--ok">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Compilado</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="int-comp">0,1 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="int-item-interp">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Interpretado</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="int-interp">8,2 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="int-item-res">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Resultado</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="int-res">cabe</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Cifras medidas en el ejemplo 44 sobre el módulo empleado.
\t\t\tconst US_COMPILADO = 0.4;
\t\t\tconst US_INTERPRETADO = 41.0;
\t\t\t// Fracción del periodo que puede ocupar la evaluación sin comprometer
\t\t\t// el resto del bucle: el presupuesto de la sesión 4.
\t\t\tconst PRESUPUESTO = 0.5;

\t\t\tconst lienzo = document.getElementById("int-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst dReglas = document.getElementById("int-reglas");
\t\t\tconst dPeriodo = document.getElementById("int-periodo");
\t\t\tconst lecReglas = document.getElementById("int-reglas-lec");
\t\t\tconst lecPeriodo = document.getElementById("int-periodo-lec");
\t\t\tconst salComp = document.getElementById("int-comp");
\t\t\tconst salInterp = document.getElementById("int-interp");
\t\t\tconst salRes = document.getElementById("int-res");
\t\t\tconst itInterp = document.getElementById("int-item-interp");
\t\t\tconst itRes = document.getElementById("int-item-res");

\t\t\tfunction variable(n) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(n).trim();
\t\t\t}
\t\t\tfunction coma(n, d) {
\t\t\t\treturn n.toFixed(d).replace(".", ",");
\t\t\t}

\t\t\tfunction dibujar(reglas, periodoMs) {
\t\t\t\tconst msComp = (reglas * US_COMPILADO) / 1000;
\t\t\t\tconst msInterp = (reglas * US_INTERPRETADO) / 1000;

\t\t\t\tconst w = lienzo.width;
\t\t\t\tctx.clearRect(0, 0, w, lienzo.height);
\t\t\t\tconst izq = 158;
\t\t\t\tconst ancho = w - izq - 40;
\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst texto = variable("--color-text");
\t\t\t\tconst borde = variable("--color-border");
\t\t\t\tconst ok = variable("--color-ok");
\t\t\t\tconst acento = variable("--color-accent");

\t\t\t\tconst filas = [
\t\t\t\t\t{ rotulo: "Compilado", ms: msComp, color: ok, y: 96 },
\t\t\t\t\t{ rotulo: "Interpretado", ms: msInterp, color: acento, y: 200 },
\t\t\t\t];

\t\t\t\tfor (const f of filas) {
\t\t\t\t\t// El carril representa el periodo completo del bucle.
\t\t\t\t\tctx.fillStyle = variable("--color-surface");
\t\t\t\t\tctx.strokeStyle = borde;
\t\t\t\t\tctx.lineWidth = 1.2;
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.roundRect(izq, f.y, ancho, 52, 6);
\t\t\t\t\tctx.fill();
\t\t\t\t\tctx.stroke();

\t\t\t\t\tconst frac = Math.min(1, f.ms / periodoMs);
\t\t\t\t\tctx.fillStyle = f.color;
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.roundRect(izq, f.y, Math.max(3, ancho * frac), 52, 6);
\t\t\t\t\tctx.fill();

\t\t\t\t\tctx.fillStyle = texto;
\t\t\t\t\tctx.font = "600 13px system-ui";
\t\t\t\t\tctx.textAlign = "right";
\t\t\t\t\tctx.fillText(f.rotulo, izq - 14, f.y + 24);
\t\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\t\tctx.font = "11px ui-monospace, monospace";
\t\t\t\t\tctx.fillText(`${coma(f.ms, 2)} ms`, izq - 14, f.y + 40);

\t\t\t\t\tif (f.ms > periodoMs) {
\t\t\t\t\t\tctx.fillStyle = acento;
\t\t\t\t\t\tctx.font = "600 12px system-ui";
\t\t\t\t\t\tctx.textAlign = "left";
\t\t\t\t\t\tctx.fillText("no cabe en el periodo", izq + ancho + 8, f.y + 30);
\t\t\t\t\t}
\t\t\t\t}

\t\t\t\t// Línea del presupuesto disponible
\t\t\t\tconst xPres = izq + ancho * PRESUPUESTO;
\t\t\t\tctx.strokeStyle = variable("--color-navy");
\t\t\t\tctx.lineWidth = 1.6;
\t\t\t\tctx.setLineDash([5, 4]);
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(xPres, 76);
\t\t\t\tctx.lineTo(xPres, 272);
\t\t\t\tctx.stroke();
\t\t\t\tctx.setLineDash([]);
\t\t\t\tctx.fillStyle = variable("--color-navy");
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.textAlign = "center";
\t\t\t\tctx.fillText("presupuesto", xPres, 66);

\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.fillText(
\t\t\t\t\t`${reglas} reglas evaluadas en cada iteración de ${periodoMs} ms`,
\t\t\t\t\tizq,
\t\t\t\t\t40,
\t\t\t\t);
\t\t\t\tctx.fillText("el carril completo es un periodo", izq, 300);

\t\t\t\treturn { msComp, msInterp };
\t\t\t}

\t\t\tfunction actualizar() {
\t\t\t\tconst reglas = Number(dReglas.value);
\t\t\t\tconst periodo = Number(dPeriodo.value);
\t\t\t\tlecReglas.textContent = String(reglas);
\t\t\t\tlecPeriodo.textContent = `${periodo} ms`;

\t\t\t\tconst { msComp, msInterp } = dibujar(reglas, periodo);
\t\t\t\tconst fComp = msComp / periodo;
\t\t\t\tconst fInterp = msInterp / periodo;
\t\t\t\tsalComp.textContent = `${coma(fComp * 100, 1)} %`;
\t\t\t\tsalInterp.textContent = `${coma(fInterp * 100, 1)} %`;

\t\t\t\tconst cabe = fInterp <= PRESUPUESTO;
\t\t\t\tsalRes.textContent = cabe ? "cabe" : "excede el presupuesto";
\t\t\t\titInterp.classList.toggle("metric__item--ok", cabe);
\t\t\t\titInterp.classList.toggle("metric__item--bad", !cabe);
\t\t\t\titRes.classList.toggle("metric__item--ok", cabe);
\t\t\t\titRes.classList.toggle("metric__item--bad", !cabe);
\t\t\t}

\t\t\tfor (const el of [dReglas, dPeriodo]) el.addEventListener("input", actualizar);
\t\t\tnew MutationObserver(actualizar).observe(document.documentElement, {
\t\t\t\tattributes: true,
\t\t\t\tattributeFilter: ["data-theme"],
\t\t\t});
\t\t\tactualizar();
\t\t</script>
""",
)

# ─────────────────── 06 · artículo · máquina virtual embebida
lamina(
    "paper-maquina-virtual-embebida",
    "Programación en alto nivel sin atarse a una arquitectura · Sesión 11",
    "Artículo · Máquina virtual embebida",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Lauwaerts, T.; Marr, S.; De Roover, C.</b> (2024). WARDuino: An embedded WebAssembly virtual "
        "machine. <i>Journal of Computer Languages</i> 79, 101268. <code>doi:10.1016/j.cola.2024.101268</code>",
        "Programación en alto nivel sin atarse a una arquitectura",
        ["Ver si un microcontrolador admite las herramientas de un <b>lenguaje de alto nivel</b>.",
         "Depurador avanzado, sistema de tipos, gestión automática de memoria.",
         "Las soluciones previas quedaban <b>atadas a una arquitectura</b> concreta."],
        ["Construyen una <b>máquina virtual de WebAssembly</b> que corre sobre el microcontrolador.",
         "Interpreta módulos compilados desde <b>cualquier lenguaje</b> que produzca ese formato.",
         "Sobre ella implementan herramientas de desarrollo, incluida la <b>depuración remota</b>.",
         "El mismo módulo se ejecuta en microcontroladores distintos <b>sin recompilar</b>."],
        ["La máquina virtual <b>desacopla el programa de la arquitectura</b>.",
         "La contrapartida declarada es el <b>costo de interpretar</b>, el mismo que mide el ejemplo 44.",
         "Los autores destacan la depuración remota tanto como la portabilidad."],
        [("paper-vm-artefactos",
          "Elaboración propia. Compilando, cada lenguaje se cruza con cada arquitectura; con la máquina virtual se suman en vez de multiplicarse."),
         ("paper-vm-herramientas",
          "Lo que cada flujo ofrece. La única casilla que gana el compilado es la que el artículo declara como contrapartida.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────── 07 · artículo · aislamiento y despliegue con WebAssembly
lamina(
    "paper-aislamiento-webassembly",
    "Aislamiento de fallos y despliegue seguro sobre dispositivos de bajo consumo · Sesión 11",
    "Artículo · Aislamiento y despliegue",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Wallentowitz, S.; Kersting, B.; Mendez Rial, D.</b> (2022). Potential of WebAssembly for Embedded "
        "Systems. <i>MECO 2022</i>, 1-4. <code>doi:10.1109/MECO55406.2022.9797106</code>",
        "Aislamiento de fallos y despliegue seguro sobre dispositivos de bajo consumo",
        ["Valorar si una <b>máquina virtual de aplicación</b> resulta adecuada para sistemas embebidos.",
         "Dos propiedades interesan en despliegues conectados: <b>aislamiento</b> y <b>portabilidad</b>.",
         "El trabajo es una <b>toma de posición razonada</b>, no un estudio experimental."],
        ["El <b>aislamiento fuerte</b> separa esta tecnología de un intérprete de guiones sin más.",
         "El módulo solo accede a <b>lo que el anfitrión le concede</b> de forma explícita.",
         "La <b>portabilidad</b> permite reutilizar el trabajo al cambiar de microcontrolador.",
         "Revisan los entornos de ejecución disponibles para recursos limitados."],
        ["El conjunto de herramientas disponible la convierte en <b>candidata razonable</b>.",
         "Su interés no está solo en cambiar el comportamiento, sino en <b>acotar lo que puede tocar</b>.",
         "Conviene leerlo como criterio de decisión, no como medida: no aporta cifras propias."],
        [("paper-aislamiento-modulo",
          "Elaboración propia. La propiedad que separa esta tecnología de un intérprete: el módulo no alcanza lo que no se le concede."),
         ("paper-wasm-propiedades",
          "Las dos propiedades declaradas frente a lo que cada una exige a cambio.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────────── 08 · binario frente a comportamiento
lamina(
    "binario-frente-a-comportamiento",
    "Dos operaciones con riesgos y permisos distintos · Sesión 11",
    "Actualizar el binario o el comportamiento",
    envolver(f"""{cabecera(A, "Dos operaciones con riesgos y permisos distintos", "i-check")}

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th></th><th>Actualizar el binario</th><th>Actualizar el comportamiento</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr><td><b>Qué cambia</b></td><td>La plataforma entera</td><td>Lo que la plataforma ejecuta</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Riesgo</b></td><td>Dejar el equipo inalcanzable</td><td>Comportamiento incorrecto, con el equipo accesible</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Tiempo</b></td><td>Minutos por unidad, más el despliegue</td><td>Segundos</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Reversión</b></td><td>Automática, con dos particiones</td><td>Volver a enviar la versión anterior</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Quién debería poder</b></td><td>Solo el fabricante, con firma</td><td>El integrador o el usuario, según el producto</td></tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Un sistema completo tiene las dos</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tNo se elige entre una y otra: se define <b>el ámbito de cada una</b>. La
\t\t\t\t\t\tactualización del binario corrige fallos y vulnerabilidades y es
\t\t\t\t\t\tprivativa del fabricante; la del comportamiento adapta el equipo a cada
\t\t\t\t\t\tinstalación y puede delegarse. Confundirlas (permitir que quien ajusta un
\t\t\t\t\t\tumbral pueda también sustituir el firmware) es un error de diseño de
\t\t\t\t\t\tpermisos, no de programación.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\tEfecto sobre la definición del producto
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tCuando el firmware pasa a ser plataforma, lo que se vende deja de ser un
\t\t\t\t\t\taparato con funciones fijas y pasa a ser un aparato <b>más el conjunto de
\t\t\t\t\t\tcomportamientos que admite</b>. Eso cambia el soporte (hay tantas
\t\t\t\t\t\tconfiguraciones como instalaciones) y cambia la garantía, porque no todo
\t\t\t\t\t\tlo que el equipo hace lo escribió el fabricante.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-check",
)

# ───────────────────────────────── 09 · ESP-Claw
lamina(
    "esp-claw",
    "Qué es ESP-Claw y qué exige · Sesión 11",
    "ESP-Claw",
    envolver(f"""{cabecera(B, "Un agente ejecutándose sobre el propio dispositivo", "i-robot")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué es
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tMarco de trabajo de Espressif que la propia documentación define como
\t\t\t\t\t\t\t\t<b>«Chat-as-Coding Edge Agent Framework for IoT»</b>: el
\t\t\t\t\t\t\t\tcomportamiento del equipo se describe conversando y queda fijado en
\t\t\t\t\t\t\t\t<b>guiones en Lua</b> que se guardan en el dispositivo. El ciclo de
\t\t\t\t\t\t\t\tadquirir, decidir y actuar se resuelve en local.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tNo es un producto cerrado sino <b>una aplicación de ejemplo más
\t\t\t\t\t\t\t\tcomponentes</b>: <code>application/edge_agent/</code> monta el
\t\t\t\t\t\t\t\tequipo concreto y los componentes aportan el runtime, las capacidades
\t\t\t\t\t\t\t\ty el acceso a los periféricos.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-folder")}
\t\t\t\t\t\t\t\tDónde vive lo que el equipo aprende
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tTodo el estado del agente es un <b>árbol de archivos en la partición
\t\t\t\t\t\t\t\tde datos</b>: <code>sessions/</code>, <code>memory/</code>,
\t\t\t\t\t\t\t\t<code>skills/</code>, <code>scripts/</code>,
\t\t\t\t\t\t\t\t<code>router_rules/</code> y <code>scheduler/</code>. Respaldar es
\t\t\t\t\t\t\t\tcopiar esas carpetas; reiniciar de fábrica es volver a grabar la
\t\t\t\t\t\t\t\tpartición.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="esp-claw-requisitos"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\t{ico("i-chart")}
\t\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t\tRequisito publicado frente al módulo empleado. La documentación
\t\t\t\t\t\t\t\t\tpide <b>8 MB de Flash y 8 MB de PSRAM</b> y admite ESP32-S3, P4 y
\t\t\t\t\t\t\t\t\tC5. El módulo de estas sesiones tiene 4 MB y no lleva PSRAM: no lo
\t\t\t\t\t\t\t\t\tejecuta, y saber por qué forma parte de la lección.
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-robot",
)

# ─────────────────────── 09b · ESP-Claw · cómo funciona por dentro
lamina(
    "esp-claw-por-dentro",
    "El ciclo del agente y las capacidades · Sesión 11",
    "ESP-Claw por dentro",
    envolver(f"""{cabecera(B, "Cómo decide y cómo actúa: el ciclo y las capacidades", "i-cpu")}

\t\t\t\t<div class="blockdiagram" data-animate="fade-up">
\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t<span class="bd-node__title">1 · Contexto</span>
\t\t\t\t\t\t<span class="bd-node__body">El núcleo arma la petición: instrucciones del sistema, historial de la sesión y catálogo de herramientas.</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t<span class="bd-node__title">2 · Turnos con el modelo</span>
\t\t\t\t\t\t<span class="bd-node__body">Varias vueltas de diálogo, no una. En cada una el modelo puede pedir que se ejecute una herramienta.</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t<span class="bd-node__title">3 · Ejecución</span>
\t\t\t\t\t\t<span class="bd-node__body">La llamada se resuelve por un despachador único, con el resultado devuelto al diálogo.</span>
\t\t\t\t\t</div>
\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t<span class="bd-node__title">4 · Persistencia</span>
\t\t\t\t\t\t<span class="bd-node__body">El historial se escribe en el sistema de archivos del equipo, que es lo que da continuidad entre arranques.</span>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Capacidad: la unidad de todo lo que se puede invocar</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada componente registra un descriptor con su nombre, su esquema de
\t\t\t\t\t\t\tentrada y su ciclo de vida. Las hay de <b>tres clases</b>: herramienta
\t\t\t\t\t\t\tinvocable, fuente de eventos y mixta.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tSe agrupan por familias (archivos, Lua, HTTP, MCP, planificador,
\t\t\t\t\t\t\tsistema) y el grupo es la unidad de registro y de permiso.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Tres vías de entrada, un solo despachador</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUna capacidad se ejecuta desde el <b>modelo</b>, desde la
\t\t\t\t\t\t\t<b>consola</b> o desde una <b>regla del enrutador de eventos</b>. La
\t\t\t\t\t\t\tllamada guarda quién la originó.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tEsa marca de origen es lo que permite tratar distinto una acción
\t\t\t\t\t\t\tpedida por una persona y otra decidida por el agente.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">El detalle que conviene retener</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tNo todas las capacidades registradas se le enseñan al modelo. Hay una
\t\t\t\t\t\t<b>lista de grupos visibles</b> que en el arranque deja a la vista solo
\t\t\t\t\t\tlo básico, y activar una habilidad amplía esa lista. Son las dos cosas a
\t\t\t\t\t\tla vez: una <b>economía de contexto</b>, porque cada herramienta declarada
\t\t\t\t\t\tocupa tokens en todas las peticiones, y un <b>límite de actuación</b>,
\t\t\t\t\t\tporque lo que no está declarado el modelo no lo puede pedir.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-cpu",
)

# ──────────────────────────────── 10 · los dos ámbitos de la IA
lamina(
    "dos-ambitos-de-la-ia",
    "La IA como herramienta de desarrollo y como componente en operación · Sesión 11",
    "Los dos ámbitos de la IA",
    envolver(f"""{cabecera(B, "La IA como herramienta de desarrollo y como componente en operación", "i-robot")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Herramienta de desarrollo</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tGenerar drivers, revisar código, documentar, diagnosticar. Es lo que
\t\t\t\t\t\t\thace «La hora del código» desde la sesión 1.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>El resultado lo revisa una persona antes de ejecutarse.</b> El
\t\t\t\t\t\t\terror se detecta en desarrollo y no llega al producto.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Componente del sistema en operación</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCapacidad de decisión y de actuación sobre el dispositivo mientras
\t\t\t\t\t\t\testá funcionando, sin nadie delante.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Nadie revisa cada decisión.</b> Lo que se revisa es el margen de
\t\t\t\t\t\t\tactuación que se le concede.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tSon <b>dos problemas de ingeniería distintos</b> y se confunden con
\t\t\t\t\t\tfacilidad porque la tecnología es la misma. En el primero, la pregunta es
\t\t\t\t\t\tcómo verificar lo generado. En el segundo, qué puede tocar el agente y
\t\t\t\t\t\tqué ocurre cuando se equivoca, que no es cuestión de verificación sino de
\t\t\t\t\t\tdiseño de permisos y de rutas de recuperación.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Lo que no cambia en ninguno de los dos</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tLa <b>definición de requisitos</b>, la <b>arquitectura</b>, la
\t\t\t\t\t\t<b>seguridad</b>, la <b>validación sobre hardware real</b> y la
\t\t\t\t\t\t<b>responsabilidad sobre el resultado</b> siguen siendo del
\t\t\t\t\t\tdesarrollador. Ninguna de las cinco se delega, y ninguna se cubre
\t\t\t\t\t\tgenerando más código.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-robot",
)

# ────────────────────── 11 · flujo de trabajo y contexto
lamina(
    "flujo-y-contexto",
    "Qué se automatiza del flujo y qué contexto exige · Sesión 11",
    "Flujo de trabajo y contexto",
    envolver(f"""{cabecera(B, "Qué se automatiza del flujo y qué contexto exige", "i-flow")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Etapa</th><th>¿Se automatiza?</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td>Especificación</td><td><b>No.</b> Es la entrada, y su calidad decide todo lo demás</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Arquitectura</td><td><b>No.</b> Decide qué se puede mantener después</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Generación</td><td>Sí, con supervisión</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Verificación</td><td>En parte: se generan pruebas, se revisan a mano</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Simulación</td><td>Sí</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Medición sobre hardware</td><td><b>No.</b> Es la única prueba de que funciona</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Despliegue</td><td>Sí, con los mecanismos de la sesión 10</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tQué contexto necesita un asistente
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>hoja de datos</b> del dispositivo, el <b>archivo de
\t\t\t\t\t\t\t\tconfiguración</b> del proyecto, las <b>interfaces existentes</b> y
\t\t\t\t\t\t\t\tlas <b>restricciones de memoria y de tiempo</b>. La calidad del
\t\t\t\t\t\t\t\tresultado se corresponde con la del contexto entregado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Por qué el prompt está escrito así</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas cuatro partes numeradas de «La hora del código» son exactamente
\t\t\t\t\t\t\t\tese contexto: la placa y el marco de trabajo, el comportamiento con
\t\t\t\t\t\t\t\tel formato de salida fijado, el montaje y el diagrama. Y el apartado
\t\t\t\t\t\t\t\t«por qué se pide así» es la parte que enseña a especificar, que es la
\t\t\t\t\t\t\t\tetapa que la tabla marca como no automatizable.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-flow",
)

# ─────────────── 12 · artículo · calidad del código generado
lamina(
    "paper-calidad-codigo-generado",
    "Proporción de código válido y correcto entre las herramientas de generación · Sesión 11",
    "Artículo · Calidad del código generado",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Yetiştiren, B.; Özsoy, I.; Ayerdem, M.; Tüzün, E.</b> (2023). Evaluating the Code Quality of "
        "AI-Assisted Code Generation Tools: An Empirical Study. <i>arXiv</i>. <code>arXiv:2304.10778</code>",
        "Proporción de código válido y correcto entre las herramientas de generación",
        ["Medir la calidad del código generado <b>más allá de si funciona</b>.",
         "Cinco dimensiones: validez, corrección, seguridad, fiabilidad y mantenibilidad.",
         "<b>164 problemas</b> planteados a tres herramientas de generación asistida."],
        ["Generaciones válidas: <b>150, 148 y 153 de 164</b> — entre el 90,2 % y el 93,3 %.",
         "La diferencia entre las tres herramientas <b>es pequeña</b>.",
         "Las generaciones no válidas puntúan <b>cero</b> en corrección: no se descartan.",
         "Solo <b>dos</b> de las cinco dimensiones se comprueban ejecutando."],
        ["Las tres producen código válido en proporción <b>alta y semejante</b>.",
         "La diferencia relevante no está en si el código se ejecuta, sino en las <b>otras cuatro dimensiones</b>.",
         "Un fragmento válido y correcto puede seguir siendo inseguro o inmantenible."],
        [("paper-codigo-generado",
          "Cifras publicadas. Las tres herramientas producen código válido en proporción alta y muy semejante."),
         ("paper-codigo-dimensiones",
          "Las cinco dimensiones evaluadas, repartidas según se comprueben ejecutando o leyendo.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ─────────────── 13 · modos de fallo del código generado
lamina(
    "modos-de-fallo-generado",
    "Cuatro modos de fallo característicos del código generado · Sesión 11",
    "Modos de fallo del código generado",
    envolver(f"""{cabecera(B, "Cuatro modos de fallo característicos del código generado", "i-alert")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">{ico("i-chip")}Registros y funciones inexistentes</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe invoca una función que no existe en esta versión de la biblioteca,
\t\t\t\t\t\t\t\to un registro de otra variante del chip.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Cómo se detecta.</b> El compilador lo rechaza. Es el modo más
\t\t\t\t\t\t\t\tbenigno de los cuatro, porque no llega a ejecutarse.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">{ico("i-clock")}Cumplimiento aparente</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl código hace lo que se pidió pero incumple un requisito temporal:
\t\t\t\t\t\t\t\tbloquea donde no debe, o consulta donde hacía falta una interrupción.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Cómo se detecta.</b> Solo midiendo sobre el hardware. Compila,
\t\t\t\t\t\t\t\tejecuta y supera cualquier prueba funcional.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">{ico("i-layers")}Dependencias innecesarias</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe incorpora una biblioteca entera para algo que resolvían diez
\t\t\t\t\t\t\t\tlíneas. El binario crece y con él la superficie de ataque.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Cómo se detecta.</b> Revisando las inclusiones y comparando el
\t\t\t\t\t\t\t\ttamaño del binario antes y después.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">{ico("i-plug")}Credenciales expuestas</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa clave aparece escrita en el código, o la validación del certificado
\t\t\t\t\t\t\t\tse deshabilita «para que funcione».
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Cómo se detecta.</b> Buscando cadenas literales y llamadas que
\t\t\t\t\t\t\t\trelajen la verificación. Nunca falla una prueba por esto.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Procedimiento de revisión de código que no se ha escrito</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tLeerlo entero antes de ejecutarlo; comprobar que cada función invocada
\t\t\t\t\t\texiste en la versión que usa el proyecto; <b>medir sobre el hardware</b>
\t\t\t\t\t\tlo que tenga requisito temporal; revisar las inclusiones y el tamaño del
\t\t\t\t\t\tbinario; y buscar credenciales literales y verificaciones relajadas. Tres
\t\t\t\t\t\tde los cuatro modos superan la compilación y las pruebas.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ────────────────────────────────────── 14 · La hora del código · 45
lamina(
    "codigo-45-verificar-lo-generado",
    "Código 45 · Verificación de un driver generado · Sesión 11",
    "La hora del código · Verificar lo generado",
    hora_del_codigo(
        45,
        "Verificación de un driver generado contra los cuatro modos de fallo",
        "Pedir a un asistente un driver para un sensor y <b>someterlo a la lista de comprobación</b> de la lámina "
        "anterior, midiendo sobre el hardware lo que tenga requisito temporal. El entregable no es el driver: es "
        "el informe de revisión.",
        "Los <b>cuatro modos de fallo</b> del código generado son funciones inexistentes, cumplimiento temporal "
        "aparente, dependencias desproporcionadas y credenciales incrustadas. Solo el primero lo detecta el "
        "compilador; el segundo se mide, el tercero se ve en el tamaño del binario y el cuarto solo leyendo.",
        "El <b>ESP32</b> lee un sensor de temperatura y humedad en el <b>GPIO 15</b> con su resistencia de "
        "polarización, y enciende un LED de actividad en el <b>GPIO 25</b> con resistencia de 220 Ω.",
        """[REV] 1. funciones inexistentes ... 0 hallazgos (compila)
[REV] 2. requisito temporal ....... 1: delay(250) bloquea el bucle
[REV] 3. dependencias ............. 1: 38 kB para formatear texto
[REV] 4. credenciales ............. 0 hallazgos
[MEDIDA] bucle sin driver=0.4 ms con driver=250.6 ms""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Pide a un asistente un driver para el sensor con la interfaz común de la sesión 4: un método de inicio y otro de lectura que devuelva el valor con indicación de validez. Después <b>revísalo</b> contra los cuatro modos de fallo y documenta cada punto en la cabecera. Mide con <code>esp_timer_get_time()</code> la lectura y la duración de una iteración con y sin el driver. Corrige lo que encuentres dejando constancia de qué cambiaste. Emite a 115200 baudios el informe.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el sensor en el GPIO 15 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la revisión: los cuatro puntos en orden, con lo que se comprueba en cada uno y qué hacer si aparece un hallazgo. Y la <b>lista de comprobación</b> con el resultado de cada punto y, para los hallazgos, qué se cambió.""",
        "La última línea es la prueba: el bucle pasa de <b>0,4 a 250,6 ms</b> al incorporar el driver. El punto 1 "
        "no encontró nada, compila, y aun así el proyecto ya no cumple su periodo. Los puntos 2, 3 y 4 no los "
        "detecta ninguna herramienta: hay que medir, mirar el binario y leer.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-dht22></wokwi-dht22></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="orange"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/dht22-element.js";
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
""",
)

# ────────────────────────────────────── 15 · La hora del código · 46
lamina(
    "codigo-46-agente-acotado",
    "Código 46 · Agente con margen de actuación acotado · Sesión 11",
    "La hora del código · Agente acotado",
    hora_del_codigo(
        46,
        "Agente con margen de actuación acotado y registro de decisiones",
        "Separar <b>quién decide</b> de <b>qué está permitido</b>. Una regla externa propone una consigna; el "
        "firmware la acota a un intervalo seguro, la aplica y registra por separado lo pedido y lo aplicado. "
        "Ninguna decisión queda sin traza.",
        "Un <b>límite compilado</b> es una constante del binario: el agente no puede ampliarlo porque no vive "
        "donde él escribe. Si los límites estuvieran en la configuración que el propio agente cambia, no serían "
        "límites. <b>Acotar</b> es sustituir el valor pedido por el más cercano permitido, no rechazar la "
        "petición. El código <b>429</b> corta un ritmo de peticiones excesivo antes de que sature al equipo.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b>, controla un LED con la consigna en el "
        "<b>GPIO 25</b> y enciende otro de rechazo en el <b>GPIO 26</b>, ambos con resistencia de 220 Ω.",
        """[AGENTE] propone consigna=95 %  motivo="por debajo del objetivo"
[LIMITE] permitido=[0, 70] % -&gt; consigna acotada a 70 %
[APLICA] consigna=70 %  pedido=95 %  acotado=si
[AGENTE] propone consigna=40 % -&gt; dentro de limite
[APLICA] consigna=40 %  pedido=40 %  acotado=no
[RESUMEN] 24 h: 118 decisiones  9 acotadas  0 fuera de rango""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, ESPAsyncWebServer y ArduinoJson.

<b>2. Firmware.</b> Expón <code>POST /api/consigna</code> para que un agente externo proponga un valor con su motivo. El firmware <b>no aplica lo pedido sin más</b>: lo acota a un intervalo declarado como constante de compilación, aplica el resultado y registra por separado el valor pedido, el aplicado y si hubo que acotarlo. Lleva un contador de decisiones y de recortes. Si llegan más de diez propuestas por minuto, rechaza con 429. Emite a 115200 baudios cada decisión con su motivo.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro y los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una propuesta, desde que llega hasta que se aplica o se acota, con el contador de ritmo incluido. Y la <b>frontera</b> entre lo que decide el agente y lo que el firmware garantiza pase lo que pase, con los límites concretos anotados.""",
        "El resumen de 24 h dice <b>9 acotadas de 118</b>. Ese número es el que hay que vigilar: si creciera, el "
        "agente llevaría semanas pidiendo valores absurdos y el recorte lo estaría tapando. Por eso se registran "
        "por separado <b>pedido</b> y <b>aplicado</b>: con una sola cifra, un agente que se ha desviado y otro "
        "que funciona bien producen exactamente la misma traza.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
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

# ────────────────────────────────────── 15b · La hora del código · 47
lamina(
    "codigo-47-comportamiento-versionado",
    "Código 47 · Comportamiento versionado y reversible · Sesión 11",
    "La hora del código · Comportamiento versionado",
    hora_del_codigo(
        47,
        "Comportamiento versionado, validado y reversible",
        "Dar al comportamiento externo las mismas garantías que la sesión 10 dio al firmware: <b>versionarlo, "
        "validarlo antes de aplicarlo y poder volver atrás</b>. El equipo publica qué versión de comportamiento "
        "lleva, junto a la del firmware.",
        "<b>Validar antes de aplicar</b> significa comprobar sintaxis, referencias y límites sobre el conjunto "
        "recibido <b>sin tocar</b> el que está vigente: si algo falla, no se ha sobrescrito nada. El <b>resumen</b> "
        "identifica cada versión de forma única, de modo que se puede saber qué ejecuta cada unidad del parque. "
        "El <b>modo prueba</b> con vuelta atrás es lo que la sesión 10 conseguía con dos particiones, aquí sin "
        "reiniciar.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b>, controla un LED con las reglas en el "
        "<b>GPIO 25</b> e indica el estado del comportamiento con otro en el <b>GPIO 26</b>, con 220 Ω.",
        """[INFO] firmware=1.2.0  comportamiento=reglas-v4  resumen=8f21ac
[CARGA] recibido reglas-v5  validando sintaxis y limites...
[CARGA] rechazado: la regla 3 referencia una entrada inexistente
[INFO] sigue vigente reglas-v4  (no se sobrescribio nada)
[CARGA] recibido reglas-v6  valido -&gt; en prueba durante 120 s
[CARGA] 120 s sin fallo -&gt; reglas-v6 confirmada v4 de respaldo""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, ESPAsyncWebServer, LittleFS y ArduinoJson.

<b>2. Firmware.</b> Guarda el conjunto de reglas en LittleFS con un número de versión y un resumen. Expón <code>POST /api/comportamiento</code>, que <b>valida antes de aplicar</b>: comprueba la sintaxis, que cada entrada y salida referenciada exista y que los valores caigan en los límites compilados. Si falla, rechaza sin sobrescribir nada y devuelve el motivo. Si es válido, lo aplica en modo prueba durante 120 s conservando el anterior; si no se registra ningún fallo, lo confirma. Publica en <code>/api/info</code> la versión del firmware y la del comportamiento con su resumen. Emite a 115200 baudios cada paso.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro y los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una carga: validar, aplicar en prueba, confirmar o revertir. Y la <b>máquina de estados</b> del comportamiento, con la rama de rechazo y la de reversión dibujadas.""",
        "Las líneas tercera y cuarta son el punto del ejercicio: la carga se rechaza y <b>reglas-v4 sigue "
        "vigente</b>. Si en la traza propia el rechazo dejara el equipo sin reglas, la validación se está "
        "haciendo después de sobrescribir. Comparar además los dos identificadores de <code>[INFO]</code>: sin "
        "versión y resumen no hay forma de saber qué ejecuta cada unidad del parque, por barato que sea cambiarlo.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
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

# ─────────────────────────────────────── 16 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes con comportamiento externo y asistentes · Sesión 11",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes con comportamiento externo y asistentes", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("El periodo deja de cumplirse tras añadir reglas", "El equipo cumplía su periodo con el umbral compilado y lo pierde al pasar a reglas interpretadas.", "Cada evaluación pasa por el intérprete y cuesta dos órdenes de magnitud más. Con muchas reglas o periodo corto, deja de caber en el presupuesto del bucle.", "Medir el tiempo de evaluación y multiplicarlo por el número de reglas y la frecuencia. Es el cálculo del ejemplo 44.", "i-clock")}
{problema("El código generado compila y falla en operación", "El driver supera las pruebas en el banco y en el equipo real pierde muestras.", "Cumplimiento aparente: el código hace lo pedido pero bloquea donde no debe. Ninguna prueba funcional lo detecta.", "Medir la duración de una iteración del bucle con y sin el código nuevo. Si crece un orden de magnitud, hay una espera bloqueante dentro.", "i-cpu")}
{problema("Nadie sabe qué está ejecutando el equipo", "Dos unidades del mismo modelo se comportan distinto y no consta por qué.", "Con comportamiento externo hay tantas configuraciones como instalaciones, y sin versionado del guion no queda registro de cuál lleva cada una.", "Publicar en <code>/api/info</code> la versión del firmware y también la del comportamiento cargado, con su resumen.", "i-folder")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("Una regla errónea deja el equipo inservible", "Se envía un guion con un fallo y el dispositivo deja de responder.", "El comportamiento externo se ejecuta sin aislamiento: un fallo suyo alcanza al resto del sistema.", "Acotar lo que el guion puede tocar y validar la regla antes de aplicarla. Conservar la anterior para poder volver a ella.", "i-layers")}
{problema("El agente pide valores absurdos y nadie se entera", "El sistema funciona con normalidad durante meses y al revisarlo se descubren decisiones sin sentido.", "El firmware acota las propuestas fuera de rango y aplica el valor recortado, pero registra solo el aplicado.", "Registrar por separado lo pedido y lo aplicado, con un contador de recortes. Un contador que crece es el aviso.", "i-robot")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 17 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 11 · Sesión 11",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("Runtime embebido", "embedded runtime", "Firmware que ejecuta comportamiento definido fuera del binario: guiones, reglas, configuración o modelos. El binario pasa a ser plataforma.")}
{termino("Máquina virtual de aplicación", "application virtual machine", "Entorno que ejecuta módulos compilados a un formato portable, con aislamiento entre el módulo y el resto del sistema.")}
{termino("Aislamiento de fallos", "fault isolation", "Propiedad por la que el fallo de un módulo no compromete al resto. Separa cargar código arbitrario de cargarlo con permisos declarados.")}
{termino("Determinismo", "determinism", "Propiedad de un sistema cuyo peor caso puede acotarse. La recolección de memoria y el despacho dinámico de un intérprete la dificultan.")}
{termino("Cumplimiento aparente", "apparent compliance", "Modo de fallo en que el código hace lo pedido pero incumple un requisito temporal. Supera la compilación y las pruebas funcionales.")}
{termino("Superficie de ataque", "attack surface", "Todo aquello por lo que se puede influir en el dispositivo. Con comportamiento externo incluye el canal por el que se envía el guion.")}
{termino("MCP", "model context protocol", "Protocolo por el que un agente consume herramientas y datos. El dispositivo puede actuar en los dos papeles: cliente y servidor.")}
{termino("Contexto", "context", "Información que se entrega a un asistente: hoja de datos, configuración del proyecto, interfaces y restricciones. Su calidad determina la del resultado.")}
{termino("Margen de actuación", "action bounds", "Intervalo dentro del cual se acota lo que un agente propone. Va compilado en el firmware, no en la configuración que el agente puede cambiar.")}
{termino("Versionado del comportamiento", "behaviour versioning", "Registro de qué guion o regla lleva cargada cada unidad. Sin él, dos equipos iguales se comportan distinto sin que conste por qué.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 18 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 11 · Sesión 11",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Compilado e interpretado</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tInterpretar comportamiento intercambia tiempo de ejecución por tiempo
\t\t\t\t\t\t\tde cambio. La elección se hace con las dos cifras medidas.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tActualizar el binario y actualizar el comportamiento son operaciones
\t\t\t\t\t\t\tdistintas, con riesgos y permisos distintos. Un sistema completo tiene
\t\t\t\t\t\t\tlas dos y declara el ámbito de cada una.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-robot")}Agentes</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa IA como herramienta de desarrollo y como componente en operación
\t\t\t\t\t\t\tson dos problemas distintos: verificar lo generado, frente a acotar lo
\t\t\t\t\t\t\tque puede tocar.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tRequisitos, arquitectura, seguridad, validación sobre hardware y
\t\t\t\t\t\t\tresponsabilidad <b>no se delegan</b>, y ninguna se cubre generando más
\t\t\t\t\t\t\tcódigo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a la sesión siguiente</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-cpu")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">El modelo como artefacto aparte</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tEn la sesión 12 el modelo de aprendizaje automático es comportamiento
\t\t\t\t\t\t\t\texterno con su propio despliegue y versionado.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-check")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Verificar lo que no se ha escrito</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tUn modelo entrenado tampoco se lee: se comprueba con métricas, que es
\t\t\t\t\t\t\t\tel asunto de la sesión 12.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Margen de actuación</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tAcotar lo que una decisión automática puede hacer vale igual para un
\t\t\t\t\t\t\t\tagente que para un modelo de inferencia.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 19 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 11 · Sesión 11",
    "Referencias",
    envolver(f"""{cabecera(B, "Referencias", "i-paper")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Los tres son de acceso abierto.</strong> El identificador lleva
\t\t\t\t\tal texto completo sin suscripción.
\t\t\t\t</p>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">WARDuino: An embedded WebAssembly virtual machine</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Lauwaerts, T.; Marr, S.; De Roover, C. (2024). <i>Journal of Computer Languages</i> 79, 101268. Copia de repositorio.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1016/j.cola.2024.101268</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Runtime embebido · Depuración</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Potential of WebAssembly for Embedded Systems</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Wallentowitz, S.; Kersting, B.; Mendez Rial, D. (2022). <i>MECO 2022</i>, 1-4. Copia de autor.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/MECO55406.2022.9797106</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Aislamiento · Superficie de ataque</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Evaluating the Code Quality of AI-Assisted Code Generation Tools</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Yetiştiren, B.; Özsoy, I.; Ayerdem, M.; Tüzün, E. (2023). <i>arXiv:2304.10778</i>. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">arXiv:2304.10778</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Modos de fallo · Ejemplo 45</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-11/</code>, junto a dos más sobre contenedores ligeros y acceso al hardware desde el runtime. El índice, en <code>src/paper/INDICE.md</code>.</span>
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
        {"clase": "clase-11", "sesion": "Sesión 11", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
