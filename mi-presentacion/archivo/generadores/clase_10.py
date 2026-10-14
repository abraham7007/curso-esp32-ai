#!/usr/bin/env python3
"""Sesión 10 — Firmware de producción: memoria, robustez, energía y OTA.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_10.py
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

A = "01 · Memoria, persistencia y tiempo"
B = "02 · Robustez, consumo y actualización"

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
    "Sesión 10 · Firmware de producción: memoria, robustez, energía y OTA",
    "Firmware de producción",
    portada(
        "Sesión 10",
        "Firmware de producción",
        "Memoria, persistencia y referencia temporal.",
        "Robustez, consumo, seguridad y OTA.",
        [
         ("i-folder", "NVS, particiones y wear levelling"),
         ("i-alert", "Reset reason y registro por niveles"),
         ("i-bolt", "Deep sleep y consumo por batería"),
         ("i-flow", "OTA con reversión y secure boot"),
        ],
        "02-tabla-particiones.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ───────────────────────────────────── 02 · tabla de particiones
lamina(
    "tabla-particiones",
    "Reparto de la memoria Flash entre particiones · Sesión 10",
    "Tabla de particiones",
    envolver(f"""{cabecera(A, "Reparto de la memoria Flash entre particiones", "i-folder")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué es y por qué existe
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>tabla de particiones</b> declara cómo se reparten los 4 MB de
\t\t\t\t\t\t\t\tla Flash. El gestor de arranque la lee para saber dónde está la
\t\t\t\t\t\t\t\taplicación que debe ejecutar.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">La restricción que decide el reparto</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa OTA (actualización remota) exige <b>dos particiones de aplicación</b>
\t\t\t\t\t\t\t\tdel mismo tamaño: mientras una ejecuta, la otra recibe la versión
\t\t\t\t\t\t\t\tnueva. Eso reduce a la mitad el espacio disponible para el programa
\t\t\t\t\t\t\t\ty es lo que hay que decidir <b>antes</b> de empezar, porque cambiar
\t\t\t\t\t\t\t\tla tabla después borra todo lo guardado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe elige con <code>board_build.partitions</code> en
\t\t\t\t\t\t\t\t<code>platformio.ini</code>. Con el esquema por omisión, un firmware
\t\t\t\t\t\t\t\tque supere <b>1,3 MB</b> no cabe, y el error de compilación no dice
\t\t\t\t\t\t\t\tque falte cambiar el reparto: dice que la sección no entra.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Partición</th><th>Tamaño típico</th><th>Qué guarda</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><code>nvs</code></td><td>20 kB</td><td>Credenciales y configuración, por pares clave-valor</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>otadata</code></td><td>8 kB</td><td>Cuál de las dos aplicaciones debe arrancar</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>app0</code></td><td>1,3 MB</td><td>Aplicación en ejecución</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>app1</code></td><td>1,3 MB</td><td>Destino de la OTA</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>spiffs</code></td><td>1,4 MB</td><td>Sistema de archivos: interfaz web y registros</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="figure">\n\t\t\t\t\t\t\t<div class="figure__frame" data-figure="tabla-particiones"></div>\n\t\t\t\t\t\t\t<p class="figure__caption">\n\t\t\t\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#i-chart" /></svg>\n\t\t\t\t\t\t\t\t<span>\n\t\t\t\t\t\t\t\t\tLos mismos tamaños de la tabla, dibujados a escala sobre los 4 MB.\n\t\t\t\t\t\t\t\t\tLas dos particiones de aplicación son iguales por obligación y\n\t\t\t\t\t\t\t\t\tjuntas se llevan dos tercios de la Flash.\n\t\t\t\t\t\t\t\t</span>\n\t\t\t\t\t\t\t</p>\n\t\t\t\t\t\t</div>\n\n\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSin <code>app1</code> no hay OTA posible, y añadirla
\t\t\t\t\t\t\t\tmás tarde obliga a reescribir la tabla, lo que <b>borra la memoria no
\t\t\t\t\t\t\t\tvolátil y el sistema de archivos</b>. En un parque desplegado eso
\t\t\t\t\t\t\t\tsignifica perder las credenciales de cada unidad.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-folder",
)

# ───────────────────────── 03 · pares clave-valor y sistema de archivos
lamina(
    "persistencia-y-desgaste",
    "Dónde se guarda cada dato y cuánto aguanta la Flash · Sesión 10",
    "Persistencia y desgaste",
    envolver(f"""{cabecera(A, "Dónde se guarda cada dato y cuánto aguanta la Flash", "i-layers")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Pares clave-valor</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tPara datos pequeños, pocos y de escritura ocasional: credenciales,
\t\t\t\t\t\t\tcalibración, contador de arranques. Se leen y escriben por nombre.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<code>Preferences</code> sobre la partición <code>nvs</code>.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Sistema de archivos</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tPara datos grandes o secuenciales: la interfaz web, un registro
\t\t\t\t\t\t\thistórico, un modelo. Se manejan como archivos.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>LittleFS</b>, que sustituye a SPIFFS: tolera el corte de
\t\t\t\t\t\t\talimentación a mitad de escritura y reparte el desgaste.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tDesgaste de la memoria Flash
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCada sector admite un número finito de ciclos de borrado, del orden
\t\t\t\t\t\t\t\tde <b>10 000 a 100 000</b>. Un registro que escriba cada segundo en
\t\t\t\t\t\t\t\tel mismo sector lo agota en <b>menos de un día</b>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Cómo se diseña para la vida útil</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe calcula al revés: si el equipo debe durar <b>diez años</b> y el
\t\t\t\t\t\t\t\tsector aguanta 100 000 ciclos, el límite es <b>una escritura cada
\t\t\t\t\t\t\t\t53 minutos</b> sobre ese sector. Acumular en memoria y escribir por
\t\t\t\t\t\t\t\tbloques, o repartir el desgaste entre sectores, es lo que hace que
\t\t\t\t\t\t\t\tesa cuenta salga.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa interfaz de <code>EEPROM</code> del ESP32 <b>no existe como
\t\t\t\t\t\t\t\thardware</b>: es una emulación sobre Flash. Cada escritura reescribe
\t\t\t\t\t\t\t\tun sector entero, aunque solo cambie un byte, y por eso el desgaste
\t\t\t\t\t\t\t\tes mucho mayor de lo que su nombre sugiere.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ────────────────────────── 04 · memoria en ejecución
lamina(
    "memoria-en-ejecucion",
    "Degradación progresiva de la memoria en ejecución · Sesión 10",
    "Memoria en ejecución",
    envolver(f"""{cabecera(A, "Degradación progresiva de la memoria en ejecución", "i-cpu")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-book")}Memoria libre</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCuánta queda sin reservar. Es la cifra que todo el mundo mira, y por
\t\t\t\t\t\t\tsí sola <b>no basta</b> para saber si la próxima reserva va a caber.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>ESP.getFreeHeap()</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Mayor bloque contiguo</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl trozo libre más grande de una pieza. Una reserva de 40 kB falla si
\t\t\t\t\t\t\testa cifra es 38, <b>aunque haya 190 kB libres</b> repartidos.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>ESP.getMaxAllocHeap()</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}Mínimo histórico</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLo más bajo que ha llegado a estar desde el arranque. Es el peor caso
\t\t\t\t\t\t\tobservado, y por tanto la magnitud que decide el margen.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>ESP.getMinFreeHeap()</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Cómo se distingue una fuga de una fragmentación</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSi <b>la memoria libre baja</b> de forma sostenida, hay una fuga:
\t\t\t\t\t\t\t\talgo se reserva y no se devuelve. Si la libre se mantiene pero
\t\t\t\t\t\t\t\t<b>el mayor bloque contiguo cae</b>, hay fragmentación: el espacio
\t\t\t\t\t\t\t\testá, pero troceado. Son fallos distintos con correcciones
\t\t\t\t\t\t\t\tdistintas, y las dos cifras juntas los separan.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="memoria-fragmentacion"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#i-chart" /></svg>
\t\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t\tLas cuatro lecturas de la traza del equipo, puestas juntas. La
\t\t\t\t\t\t\t\t\tmemoria libre apenas se movió en 31 horas; lo que se desplomó fue
\t\t\t\t\t\t\t\t\tel mayor bloque contiguo, hasta caer por debajo de los 40 kB que
\t\t\t\t\t\t\t\t\tla conexión cifrada necesita <b>de una pieza</b>. El síntoma
\t\t\t\t\t\t\t\t\taparece en el cifrado, sin relación aparente con la causa.
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ────────────────────────────────── 05 · referencia temporal
lamina(
    "referencia-temporal",
    "La hora del sistema como requisito de operación · Sesión 10",
    "Referencia temporal del sistema",
    envolver(f"""{cabecera(A, "La hora del sistema como requisito de operación", "i-clock")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDe qué depende la hora
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe sincroniza por <b>NTP</b> al arrancar y se mantiene con el reloj
\t\t\t\t\t\t\t\tinterno, que deriva. Sin red no hay hora, y sin hora no hay
\t\t\t\t\t\t\t\tconexión segura ni registro histórico fechable.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>configTzTime(zona, servidor)</code> fija a la vez el servidor y
\t\t\t\t\t\t\t\tla zona horaria con sus reglas de cambio estacional. Es preferible a
\t\t\t\t\t\t\t\t<code>configTime()</code> con un desplazamiento fijo, que deja de ser
\t\t\t\t\t\t\t\tcorrecto el día del cambio de hora.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Reloj interno o reloj externo</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl interno pierde la hora al cortar la alimentación y deriva del
\t\t\t\t\t\t\t\torden de <b>segundos al día</b>. Un reloj externo con pila la
\t\t\t\t\t\t\t\tconserva y deriva mucho menos. La decisión la impone el requisito:
\t\t\t\t\t\t\t\tsi el equipo debe fechar datos sin red, hace falta el externo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Sin hora válida</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">El sistema cree estar en 1970. Todo certificado se rechaza por no ser válido todavía.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓ NTP</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Con hora válida</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Se validan certificados, se fechan las medidas y el registro remoto es ordenable.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[BOOT] fecha del sistema = 1970-01-01 00:00:00
[NTP]  sincronizando con pool.ntp.org (zona &lt;-05&gt;5)
[NTP]  hora valida: 2026-07-28 09:22:05 -05  en 842 ms
[TLS]  cadena de certificados verificada
[DATO] t=2026-07-28T09:22:07-05  v=23.4  fechado en el dispositivo</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tEl orden de la puesta en marcha no es negociable: red, hora y solo
\t\t\t\t\t\t\tdespués cualquier conexión segura.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-clock",
)

# ────────────────────────────────────── 06 · La hora del código · 40
lamina(
    "codigo-40-persistencia-y-hora",
    "Código 40 · Configuración persistente y hora sincronizada · Sesión 10",
    "La hora del código · Persistencia y hora",
    hora_del_codigo(
        40,
        "Configuración persistente, hora sincronizada y vigilancia de la memoria",
        "Guardar la configuración en NVS, sincronizar la hora antes de cualquier conexión segura y "
        "escribir el registro <b>por bloques</b> en lugar de por muestra, para no agotar la Flash. Las tres "
        "cifras de memoria quedan a la vista en cada informe.",
        "La <b>NVS</b> guarda pares clave-valor que sobreviven al corte de alimentación, en su "
        "propia partición. La Flash se borra por <b>sectores</b> y aguanta un número finito de ciclos, así que lo "
        "que decide su vida no es cuántos datos se escriben sino <b>cuántas veces</b>: acumular en RAM y volcar "
        "una vez por hora cambia años por meses. <code>configTzTime()</code> fija hora y huso a la vez.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> como magnitud registrada y enciende un LED en "
        "el <b>GPIO 25</b> con resistencia de 220 Ω cuando la hora es válida.",
        """[NVS]  periodo=60 s umbral=0.30  arranques=47
[NTP]  hora valida: 2026-07-28 09:22:05 -05
[REG]  acumulando en memoria: 60 muestras
[REG]  volcado a /log/2026-07-28.csv  1 sector cada 60 min
[MEM]  libre=195 kB  mayor=182 kB  minimo=193 kB
[VIDA] a 1 escritura/hora y 100 000 ciclos: 11.4 anos""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, las bibliotecas Preferences y LittleFS, y un esquema de particiones con dos particiones de aplicación.

<b>2. Firmware.</b> Guarda en NVS el periodo de muestreo, el umbral y un contador de arranques que incremente en cada encendido. Sincroniza la hora con <code>configTzTime()</code> antes de cualquier conexión segura y no continúes hasta que la fecha supere el año 2020. Muestrea el GPIO 34 y <b>acumula en memoria</b>, volcando a un archivo diario solo una vez por hora: escribir por muestra agotaría el sector. Imprime a 115200 baudios las tres cifras de memoria y el cálculo de vida útil a partir del ritmo real de escritura.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del ciclo de registro, con la acumulación en memoria y el volcado horario como ramas distintas. Y el <b>mapa de particiones</b> con su tamaño y qué dato del ejercicio vive en cada una.""",
        "La última línea es el ejercicio hecho número: <b>11,4 años</b> a una escritura por hora. Recalcularla "
        "escribiendo por muestra, una cada 60 s, da menos de tres meses, con el mismo código y el mismo dato. "
        "Vigilar también las tres cifras de <code>[MEM]</code>: mientras la libre se mantenga y el mayor bloque "
        "no caiga, no hay ni fuga ni fragmentación.",
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

# ───────────────────── 07 · diagnóstico de un equipo remoto
lamina(
    "diagnostico-equipo-remoto",
    "Datos de diagnóstico de un equipo inaccesible · Sesión 10",
    "Diagnóstico de un equipo remoto",
    envolver(f"""{cabecera(B, "Datos de diagnóstico de un equipo inaccesible", "i-terminal")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}Reset reason</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl primer dato que hay que consultar. Distingue un corte de
\t\t\t\t\t\t\talimentación de un fallo de programa, de un watchdog o de una orden
\t\t\t\t\t\t\tde reinicio.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>esp_reset_reason()</code> · cuesta una línea.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-terminal")}Registro por niveles</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tError, aviso, información y depuración. El nivel se elige en
\t\t\t\t\t\t\tcompilación, de modo que la traza de producción no arrastra el detalle
\t\t\t\t\t\t\tdel desarrollo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tSustituye a imprimir sin estructura por el puerto serie.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-clock")}Watchdog</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tReinicia si una tarea deja de dar señales. Su aviso nombra a la tarea
\t\t\t\t\t\t\tculpable, que es la pista que el fallo no da por sí solo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tYa apareció en la sesión 6, aquí como herramienta de diagnóstico.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Estrategias de recuperación</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>contador de arranques fallidos</b> en NVS (memoria no volátil)
\t\t\t\t\t\t\t\tpermite escalar la respuesta: reintentar, después restituir valores
\t\t\t\t\t\t\t\tpor omisión y, si sigue fallando, arrancar en un modo mínimo que al
\t\t\t\t\t\t\t\tmenos permita actualizar. Sin ese contador, el equipo repite el
\t\t\t\t\t\t\t\tmismo fallo indefinidamente.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Causa registrada</th><th>Qué significa</th><th>Qué revisar</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><code>POWERON</code></td><td>Encendido normal</td><td>Nada; es el arranque esperado</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>PANIC</code></td><td>Fallo de programa</td><td>La traza de retorno decodificada</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>TASK_WDT</code></td><td>Una tarea dejó de ceder</td><td>La tarea nombrada en el aviso</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>BROWNOUT</code></td><td>Tensión insuficiente</td><td>Alimentación y consumo de picos</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>DEEPSLEEP</code></td><td>Despertar previsto</td><td>Nada; es el ciclo normal de bajo consumo</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>BROWNOUT</code> es la causa que más veces se confunde con un
\t\t\t\t\t\t\t\tfallo de programa: el equipo se reinicia al encender la radio porque
\t\t\t\t\t\t\t\tel pico de corriente hunde la tensión. El código no tiene ningún
\t\t\t\t\t\t\t\terror; la fuente o el cable, sí.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-terminal",
)

# ──────────────── 08 · artículo · vulnerabilidades del firmware
lamina(
    "paper-vulnerabilidades-firmware",
    "Alcance de una auditoría del entorno de firmware · Sesión 10",
    "Artículo · Vulnerabilidades de firmware",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Bakhshi, T.; Ghita, B.; Kuzminykh, I.</b> (2024). A Review of IoT Firmware Vulnerabilities and "
        "Auditing Techniques. <i>Sensors</i> 24(2), 708. <code>doi:10.3390/s24020708</code>",
        "Alcance de una auditoría del entorno de firmware",
        ["Determinar <b>qué hay que auditar</b> para reducir las vulnerabilidades del firmware.",
         "Estas vulnerabilidades <b>se pasan por alto</b> durante el desarrollo y el despliegue.",
         "Mientras la dependencia de los equipos conectados no deja de crecer."],
        ["La revisión recorre el <b>ciclo completo</b>: componentes, almacenamiento, configuración, entrega, mantenimiento y actualización.",
         "Examina además la eficacia de las herramientas disponibles para cada etapa.",
         "Esa eficacia resulta <b>desigual</b>: cubren unas partes mucho mejor que otras.",
         "Auditar el binario cubre <b>una de las seis</b> etapas."],
        ["Una estrategia eficaz debe cubrir <b>todo el ciclo y no solo el código</b>.",
         "Auditar el binario sin revisar cómo se almacena, configura y entrega deja abiertas las vías reales.",
         "Las cinco etapas restantes son por donde se compromete un equipo en operación."],
        [("paper-ciclo-firmware",
          "Elaboración propia con las seis etapas que recorren los autores: auditar el binario cubre una."),
         ("paper-auditoria-cobertura",
          "Dónde hay herramienta madura y dónde el trabajo sigue siendo manual, según lo que afirma la revisión.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────── 09 · La hora del código · 41
lamina(
    "codigo-41-diagnostico",
    "Código 41 · Diagnóstico de arranque y recuperación escalada · Sesión 10",
    "La hora del código · Diagnóstico de arranque",
    hora_del_codigo(
        41,
        "Diagnóstico de arranque con recuperación escalada",
        "Registrar el <b>reset reason</b> como primera operación y llevar en NVS un "
        "contador de arranques fallidos. Con tres fallos seguidos se restituyen los valores por omisión; con "
        "cinco, el equipo arranca en modo mínimo.",
        "<code>esp_reset_reason()</code> devuelve por qué se reinició el SoC y distingue un corte de alimentación "
        "de un fallo del programa o de un perro guardián vencido. El <b>perro guardián de tarea</b> reinicia el "
        "equipo cuando una tarea deja de ceder el procesador. La <b>escalada</b> consiste en responder distinto "
        "según cuántas veces seguidas ha fallado: sin contador, el equipo repite el mismo error para siempre.",
        "El <b>ESP32</b> lee un pulsador en el <b>GPIO 4</b> que provoca cada causa a voluntad (bucle sin ceder, "
        "fallo de programa, reinicio ordenado) y enciende tres LED de estado en los <b>GPIO 25, 26 y 27</b>.",
        """[BOOT] causa=TASK_WDT  tarea=publicacion fallos_seguidos=1
[BOOT] arranque normal, contador incrementado
[BOOT] causa=TASK_WDT  fallos=3 -&gt; restituye valores por omision
[BOOT] causa=PANIC     fallos=5 -&gt; modo minimo: red y actualizacion
[BOOT] causa=POWERON   arranque limpio -&gt; contador a cero""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y la biblioteca Preferences.

<b>2. Firmware.</b> La primera operación de <code>setup()</code> lee <code>esp_reset_reason()</code> y la registra con su nombre legible. Lleva en NVS un contador de arranques fallidos que se incrementa al arrancar y se pone a cero cuando el programa lleva 60 s funcionando sin reiniciar. Con tres fallos consecutivos, restituye la configuración por omisión; con cinco, arranca en un modo mínimo que solo levanta la red y la OTA. El pulsador provoca a voluntad un bucle sin ceder, una desreferencia nula y un reinicio ordenado, para poder observar las tres causas. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el pulsador en el GPIO 4 y los tres LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del arranque, desde la lectura de la causa hasta la decisión de modo. Y el <b>árbol de decisión</b> que va de la causa y el contador de fallos a cada una de las tres respuestas.""",
        "El detalle que decide si esto funciona está en la última línea: el contador se pone a cero <b>tras 60 s "
        "en marcha</b>, no al arrancar. Si se reiniciara al principio, un equipo que falla a los cinco segundos "
        "nunca acumularía fallos y la escalada jamás se activaría. Comprobarlo provocando el fallo tres veces "
        "seguidas y viendo aparecer la línea de restitución.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="red"></wokwi-pushbutton></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="orange"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/pushbutton-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
""",
)

# ─────────────────────── 10 · simulación de autonomía con batería
lamina(
    "simulacion-autonomia",
    "Autonomía según el ciclo de trabajo y el modo de reposo · Sesión 10",
    "Autonomía con batería",
    envolver(f"""{cabecera(B, "Autonomía según el ciclo de trabajo y el modo de reposo", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tLos tres modos
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Activo</b> con la radio encendida, del orden de 160 mA.
\t\t\t\t\t\t\t\t<b>Sueño ligero</b>, que conserva la memoria y despierta rápido,
\t\t\t\t\t\t\t\tunos 0,8 mA. <b>Deep sleep (sueño profundo)</b>, que apaga casi todo y conserva
\t\t\t\t\t\t\t\tsolo la memoria RTC, unos 10 µA.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCon una medida por minuto, pasar de sueño ligero a profundo
\t\t\t\t\t\t\t\tmultiplica la autonomía por más de veinte. Lo que domina no es el
\t\t\t\t\t\t\t\tconsumo activo sino <b>cuánto tiempo se pasa despierto</b>: alargar
\t\t\t\t\t\t\t\tel periodo entre medidas gana más que optimizar el código.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="aut-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Perfil de corriente de un ciclo de medida, con el tramo activo y el de reposo, y la autonomía resultante en días"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<label for="aut-per" class="text-sm font-medium">Periodo entre medidas</label>
\t\t\t\t\t\t\t\t<input type="range" id="aut-per" min="10" max="3600" step="10" value="60" />
\t\t\t\t\t\t\t\t<span class="readout" id="aut-per-lec">60 s</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="controls mt-2">
\t\t\t\t\t\t\t\t<label for="aut-act" class="text-sm font-medium">Tiempo despierto</label>
\t\t\t\t\t\t\t\t<input type="range" id="aut-act" min="200" max="8000" step="100" value="2500" />
\t\t\t\t\t\t\t\t<span class="readout" id="aut-act-lec">2500 ms</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="controls mt-2">
\t\t\t\t\t\t\t\t<label class="flex items-center gap-2 text-sm">
\t\t\t\t\t\t\t\t\t<input type="checkbox" id="aut-prof" class="accent-[var(--color-accent)]" checked />
\t\t\t\t\t\t\t\t\tdeep sleep entre medidas
\t\t\t\t\t\t\t\t</label>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Corriente media</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="aut-med">7,5 mA</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="aut-item-dias">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Autonomía · 2000 mAh</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="aut-dias">11 días</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Fracción despierto</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="aut-frac">4,2 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Corrientes del orden de las que se miden en el módulo empleado. La
\t\t\t// autonomía se calcula con la capacidad nominal, sin descontar el
\t\t\t// rendimiento del regulador: la conclusión cualitativa no cambia y el
\t\t\t// cálculo queda comprobable a mano.
\t\t\tconst I_ACTIVO_MA = 160;
\t\t\tconst I_LIGERO_MA = 0.8;
\t\t\tconst I_PROFUNDO_MA = 0.01;
\t\t\tconst BATERIA_MAH = 2000;

\t\t\tconst lienzo = document.getElementById("aut-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst dPer = document.getElementById("aut-per");
\t\t\tconst dAct = document.getElementById("aut-act");
\t\t\tconst cProf = document.getElementById("aut-prof");
\t\t\tconst lecPer = document.getElementById("aut-per-lec");
\t\t\tconst lecAct = document.getElementById("aut-act-lec");
\t\t\tconst salMed = document.getElementById("aut-med");
\t\t\tconst salDias = document.getElementById("aut-dias");
\t\t\tconst salFrac = document.getElementById("aut-frac");
\t\t\tconst itDias = document.getElementById("aut-item-dias");

\t\t\tfunction variable(n) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(n).trim();
\t\t\t}
\t\t\tfunction coma(n, d) {
\t\t\t\treturn n.toFixed(d).replace(".", ",");
\t\t\t}

\t\t\tfunction dibujar(perS, actMs, profundo) {
\t\t\t\tconst iReposo = profundo ? I_PROFUNDO_MA : I_LIGERO_MA;
\t\t\t\tconst fracAct = actMs / 1000 / perS;
\t\t\t\tconst media = I_ACTIVO_MA * fracAct + iReposo * (1 - fracAct);

\t\t\t\tconst w = lienzo.width;
\t\t\t\tctx.clearRect(0, 0, w, lienzo.height);
\t\t\t\tconst izq = 118;
\t\t\t\tconst der = w - 34;
\t\t\t\tconst ancho = der - izq;
\t\t\t\tconst base = 268;
\t\t\t\tconst alto = 170;

\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst borde = variable("--color-border");
\t\t\t\tconst acento = variable("--color-accent");
\t\t\t\tconst navy = variable("--color-navy");

\t\t\t\t// Escala logarítmica: entre 10 µA y 160 mA hay cuatro órdenes.
\t\t\t\tconst yDe = (mA) => {
\t\t\t\t\tconst lo = Math.log10(0.005);
\t\t\t\t\tconst hi = Math.log10(200);
\t\t\t\t\treturn base - ((Math.log10(Math.max(mA, 0.005)) - lo) / (hi - lo)) * alto;
\t\t\t\t};

\t\t\t\t// Rejilla de referencia
\t\t\t\tctx.strokeStyle = borde;
\t\t\t\tctx.lineWidth = 1;
\t\t\t\tctx.font = "10px ui-monospace, monospace";
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.textAlign = "right";
\t\t\t\tfor (const mA of [0.01, 0.1, 1, 10, 100]) {
\t\t\t\t\tconst y = yDe(mA);
\t\t\t\t\tctx.setLineDash([3, 4]);
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.moveTo(izq, y);
\t\t\t\t\tctx.lineTo(der, y);
\t\t\t\t\tctx.stroke();
\t\t\t\t\tctx.setLineDash([]);
\t\t\t\t\tctx.fillText(mA >= 1 ? `${mA} mA` : `${mA * 1000} µA`, izq - 8, y + 3);
\t\t\t\t}

\t\t\t\t// Perfil del ciclo: tramo activo seguido de tramo en reposo
\t\t\t\tconst xAct = Math.max(6, ancho * Math.min(0.45, fracAct * 4));
\t\t\t\tctx.fillStyle = acento;
\t\t\t\tctx.globalAlpha = 0.22;
\t\t\t\tctx.fillRect(izq, yDe(I_ACTIVO_MA), xAct, base - yDe(I_ACTIVO_MA));
\t\t\t\tctx.globalAlpha = 1;
\t\t\t\tctx.strokeStyle = acento;
\t\t\t\tctx.lineWidth = 2.4;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(izq, base);
\t\t\t\tctx.lineTo(izq, yDe(I_ACTIVO_MA));
\t\t\t\tctx.lineTo(izq + xAct, yDe(I_ACTIVO_MA));
\t\t\t\tctx.lineTo(izq + xAct, yDe(iReposo));
\t\t\t\tctx.lineTo(der, yDe(iReposo));
\t\t\t\tctx.stroke();

\t\t\t\t// Media, como referencia horizontal
\t\t\t\tctx.strokeStyle = navy;
\t\t\t\tctx.lineWidth = 1.6;
\t\t\t\tctx.setLineDash([6, 4]);
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(izq, yDe(media));
\t\t\t\tctx.lineTo(der, yDe(media));
\t\t\t\tctx.stroke();
\t\t\t\tctx.setLineDash([]);
\t\t\t\tctx.fillStyle = navy;
\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.font = "600 11px system-ui";
\t\t\t\tctx.fillText(`media ${coma(media, 3)} mA`, izq + 8, yDe(media) - 6);

\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.textAlign = "center";
\t\t\t\tctx.fillText("despierto", izq + xAct / 2, base + 18);
\t\t\t\tctx.fillText(profundo ? "deep sleep" : "sueño ligero", izq + xAct + (ancho - xAct) / 2, base + 18);
\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.fillText(`un ciclo de ${perS} s`, izq, 40);

\t\t\t\treturn { media, fracAct };
\t\t\t}

\t\t\tfunction actualizar() {
\t\t\t\tconst perS = Number(dPer.value);
\t\t\t\tconst actMs = Number(dAct.value);
\t\t\t\tconst prof = cProf.checked;
\t\t\t\tlecPer.textContent = perS >= 60 ? `${coma(perS / 60, 1)} min` : `${perS} s`;
\t\t\t\tlecAct.textContent = `${actMs} ms`;

\t\t\t\tconst { media, fracAct } = dibujar(perS, actMs, prof);
\t\t\t\tconst dias = BATERIA_MAH / media / 24;
\t\t\t\tsalMed.textContent = `${coma(media, 3)} mA`;
\t\t\t\tsalFrac.textContent = `${coma(fracAct * 100, 2)} %`;
\t\t\t\tsalDias.textContent =
\t\t\t\t\tdias >= 365 ? `${coma(dias / 365, 1)} años` : `${Math.round(dias)} días`;
\t\t\t\titDias.classList.toggle("metric__item--ok", dias >= 365);
\t\t\t\titDias.classList.toggle("metric__item--warn", dias < 365 && dias >= 30);
\t\t\t\titDias.classList.toggle("metric__item--bad", dias < 30);
\t\t\t}

\t\t\tfor (const el of [dPer, dAct, cProf]) el.addEventListener("input", actualizar);
\t\t\tnew MutationObserver(actualizar).observe(document.documentElement, {
\t\t\t\tattributes: true,
\t\t\t\tattributeFilter: ["data-theme"],
\t\t\t});
\t\t\tactualizar();
\t\t</script>
""",
)

# ──────────────────── 11 · artículo · medición del consumo
lamina(
    "paper-medicion-consumo",
    "Métodos para medir el consumo y por qué la estimación no basta · Sesión 10",
    "Artículo · Medición del consumo",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Guo, Y.; Chen, Y.; Wang, Y. et al.</b> (2021). A Survey of Energy Consumption Measurement in "
        "Embedded Systems. <i>IEEE Access</i> 9, 60516-60530. <code>doi:10.1109/ACCESS.2021.3074070</code>",
        "Métodos para medir el consumo y por qué la estimación no basta",
        ["Ordenar los métodos disponibles para medir <b>cuánta energía consume</b> un sistema embebido.",
         "La medida precisa es lo que permite <b>evaluar y comparar</b> diseños.",
         "Las revisiones previas del campo <b>carecían de comparación</b> entre métodos."],
        ["<b>Tres categorías</b>: medida directa, estimación por modelo e híbridos.",
         "De cada una se analizan exactitud, resolución y esfuerzo.",
         "Solo la <b>medida directa</b> capta el comportamiento del sistema completo.",
         "Los modelos sencillos <b>no representan los picos</b> de corriente."],
        ["Las tres responden a <b>compromisos distintos</b> entre exactitud y esfuerzo.",
         "<b>Ninguna sirve para todo</b>: la elección depende de la fase del diseño.",
         "Exactitud y esfuerzo son magnitudes que se intercambian, no un problema resuelto."],
        [("paper-medicion-consumo",
          "Trazo propio con las corrientes que maneja esta sesión, no medidas del artículo: el valor medio deja fuera los picos."),
         ("paper-consumo-metodos",
          "Las tres categorías en el plano esfuerzo-exactitud. Es una ordenación cualitativa tomada de sus conclusiones.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────── 12 · La hora del código · 42
lamina(
    "codigo-42-sueno-profundo",
    "Código 42 · Nodo por lotes con deep sleep · Sesión 10",
    "La hora del código · Deep sleep",
    hora_del_codigo(
        42,
        "Nodo alimentado por batería con deep sleep y estado conservado",
        "Medir cada 60 s durmiendo entre medidas. El contador de ciclos y el acumulador viven en <b>memoria "
        "RTC</b>, que sobrevive al deep sleep; cada diez medidas el equipo se conecta, publica el lote y "
        "vuelve a dormir.",
        "El <b>deep sleep</b> no es una pausa: apaga casi todo el SoC y al despertar el programa empieza otra "
        "vez por <code>setup()</code>, así que una variable normal vuelve a cero. <code>RTC_DATA_ATTR</code> "
        "coloca la variable en la <b>memoria RTC</b>, la única que se mantiene alimentada. Encender la <b>radio</b> "
        "cuesta más que las diez medidas juntas, y de ahí que se publique por lotes.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> y enciende un LED en el <b>GPIO 25</b> con "
        "resistencia de 220 Ω solo mientras está despierto.",
        """[WAKE] causa=DEEPSLEEP  ciclo=7 de 10  despierto=312 ms
[RTC]  acumulador conservado: 7 muestras media parcial=23.4
[SLEEP] durmiendo 59688 ms corriente estimada=10 uA
[WAKE] causa=DEEPSLEEP  ciclo=10 de 10 -&gt; toca publicar
[RED]  conectado en 2140 ms publicado lote de 10 muestras
[CICLO] despierto=2452 de 60000 ms = 4.1 %  media=6.6 mA""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Declara con <code>RTC_DATA_ATTR</code> un contador de ciclos y un acumulador de muestras: son las únicas variables que sobreviven al deep sleep. En cada despertar, lee el GPIO 34, acumula y vuelve a dormir con <code>esp_deep_sleep_start()</code> hasta completar 60 s de ciclo. Cada diez ciclos, conecta a la red, publica el lote y reinicia el acumulador. No enciendas la radio en los ciclos que no publican. Registra la causa del despertar, el tiempo despierto de cada ciclo y la fracción resultante, y calcula la corriente media con las cifras de la lámina de autonomía.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de un despertar, con la bifurcación entre acumular y publicar. Y el <b>ciclo completo</b> con sus fases (despertar, medir, decidir, dormir) y el tiempo que ocupa cada una.""",
        "La última línea reúne el ejercicio: el equipo está despierto el <b>4,1 %</b> del tiempo y la corriente "
        "media queda en 6,6 mA. Repetir el cálculo publicando en cada ciclo y comparar. Vigilar también la línea "
        "<code>[RTC]</code>: si el acumulador volviera a cero en cada despertar, la variable no está en memoria "
        "RTC y el lote no se completará nunca.",
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

# ──────────────────────────────── 13 · OTA
lamina(
    "actualizacion-remota",
    "Esquema de dos particiones con reversión automática · Sesión 10",
    "OTA",
    envolver(f"""{cabecera(B, "Esquema de dos particiones con reversión automática", "i-layers")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">1 · Descarga en la partición libre</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">La aplicación en curso sigue ejecutando desde la suya. Un corte aquí no rompe nada.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">2 · Verificación</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Integridad por resumen, versión superior a la actual y firma de quien la publica.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">3 · Marcar como pendiente y reiniciar</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">La nueva queda en prueba, no confirmada. Es el estado que hace posible la vuelta atrás.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">4 · Confirmar o revertir</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Si la nueva alcanza un estado sano, se confirma. Si no, el gestor de arranque vuelve a la anterior.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tQué significa «estado sano»
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLo define el programa, no el sistema. Arrancar no basta: un firmware
\t\t\t\t\t\t\t\tque arranca y no consigue conectar deja el equipo inalcanzable. La
\t\t\t\t\t\t\t\tcondición razonable es <b>haber conectado y haber publicado al menos
\t\t\t\t\t\t\t\tuna vez</b>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Por qué la reversión es lo que importa</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSin ella, una actualización defectuosa convierte un parque entero en
\t\t\t\t\t\t\t\tequipos que hay que recuperar a mano, uno por uno, con acceso físico.
\t\t\t\t\t\t\t\tCon ella, el peor caso es que el parque siga en la versión anterior.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[OTA] version disponible 1.3.0 &gt; actual 1.2.0
[OTA] descargando a app1  1284 kB  resumen verificado
[OTA] firma valida  -&gt; marcada como pendiente  reiniciando
[BOOT] arrancando app1 en modo prueba
[OTA] conectado y publicado  -&gt; confirmando app1 como valida</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ─────────────────── 14 · artículo · actualización sobre red restringida
lamina(
    "paper-actualizacion-remota",
    "Costo temporal de una actualización sobre una red de bajo consumo · Sesión 10",
    "Artículo · OTA medida",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Mahfoudhi, F.; Sultania, A. K.; Famaey, J.</b> (2022). Over-the-Air Firmware Updates for Constrained "
        "NB-IoT Devices. <i>Sensors</i> 22(19), 7572. <code>doi:10.3390/s22197572</code>",
        "Costo temporal de una actualización sobre una red de bajo consumo",
        ["Ver si es viable actualizar un equipo de recursos limitados por <b>banda estrecha</b>.",
         "Sin instalar <b>ninguna pasarela local</b>.",
         "El mantenimiento de un parque desplegado es, según los autores, el costo dominante."],
        ["Memoria repartida en <b>dos secciones iguales</b>: aplicación y gestor de arranque.",
         "Tiempo de actualización: de <b>178 s</b> para 2 kB a <b>4338 s</b> para 1000 kB.",
         "La relación es <b>lineal</b> con el tamaño en esta red.",
         "<b>Retransmisión por segmento</b>: solo se reenvía el trozo perdido o corrompido."],
        ["El crecimiento lineal contrasta con el <b>exponencial</b> que las simulaciones atribuyen a otras tecnologías.",
         "El diseño modular y la retransmisión por segmento son lo que hace <b>viable</b> el procedimiento.",
         "Sin ellos, un fallo de enlace obligaría a empezar de cero: setenta y dos minutos otra vez."],
        [("paper-ota-tiempo",
          "Los dos puntos publicados y la recta que los une. El extremo decide: 72 minutos con el equipo ocupado en actualizarse."),
         ("paper-ota-segmento",
          "Lo que evita la retransmisión por segmento, calculado con el tiempo por kB que se deduce de sus cifras.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────────────────────────── 15 · seguridad del dispositivo
lamina(
    "seguridad-dispositivo",
    "Cifrado de la memoria, secure boot y superficie de ataque · Sesión 10",
    "Seguridad del dispositivo",
    envolver(f"""{cabecera(B, "Cifrado de la memoria, secure boot y superficie de ataque", "i-plug")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-folder")}Cifrado de la memoria</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa Flash se cifra con una clave que vive dentro del chip. Quien
\t\t\t\t\t\t\textraiga el módulo y lea la memoria obtiene datos ilegibles, no las
\t\t\t\t\t\t\tcredenciales.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-check")}Secure boot</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl chip solo ejecuta binarios firmados con la clave del fabricante.
\t\t\t\t\t\t\tImpide sustituir el firmware por otro, que es la vía por la que se
\t\t\t\t\t\t\ttoma el control del equipo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}Superficie de ataque</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tTodo lo que el dispositivo escucha: el servidor web, la conexión al
\t\t\t\t\t\t\tbroker, el puerto de programación. Cada una es una vía, y las
\t\t\t\t\t\t\tque no se usan se cierran.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tAmbas medidas son <b>irreversibles</b>: se activan quemando fusibles del
\t\t\t\t\t\tchip y no se pueden desactivar. Con secure boot (arranque seguro) activo, un binario
\t\t\t\t\t\tsin firmar ya no se ejecuta nunca, y perder la clave de firma convierte
\t\t\t\t\t\tel parque en equipos que no admiten ninguna actualización más. Se
\t\t\t\t\t\tactivan al cerrar el producto, no durante el desarrollo.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">La actualización dentro de la política de seguridad</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tNingún firmware está libre de fallos, y los de las bibliotecas que
\t\t\t\t\t\tincorpora se publican después de venderlo. Por eso <b>la capacidad de
\t\t\t\t\t\tactualizar es en sí una medida de seguridad</b>, y probablemente la más
\t\t\t\t\t\timportante: un dispositivo que no se puede actualizar queda expuesto a
\t\t\t\t\t\ttoda vulnerabilidad que se descubra durante su vida útil.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-plug",
)

# ────────────────────────────────────── 16 · La hora del código · 43
lamina(
    "codigo-43-ota-con-reversion",
    "Código 43 · OTA con reversión automática · Sesión 10",
    "La hora del código · Actualización con reversión",
    hora_del_codigo(
        43,
        "OTA con verificación y reversión automática",
        "El ciclo completo de la actualización: la versión nueva arranca <b>en modo prueba</b> y solo se confirma "
        "tras conectar y publicar. Si no lo logra en 120 s, el gestor de arranque vuelve a la anterior sin que "
        "nadie intervenga.",
        "Con <b>dos particiones de aplicación</b>, la imagen nueva se escribe en la que no está corriendo. El "
        "<b>resumen</b> comprueba que la descarga llegó íntegra y la <b>firma</b>, que procede de quien dice: sin "
        "ella, el mecanismo de actualización es la vía por la que se sustituye el firmware. La versión queda "
        "<b>pendiente</b> hasta que "
        "<code>esp_ota_mark_app_valid_cancel_rollback()</code> la confirma; si el plazo vence, el gestor revierte.",
        "El <b>ESP32</b> enciende tres LED de fase en los <b>GPIO 25, 26 y 27</b> con resistencia de 220 Ω. No "
        "hace falta más: la actualización se sirve desde un servidor del ordenador.",
        """[OTA]  actual=1.2.0  disponible=1.3.0  destino=app1
[OTA]  descargando 1284 kB ... 100 %  resumen=ok firma=ok
[OTA]  marcada pendiente de verificacion reiniciando
[BOOT] app1 en modo PRUEBA  plazo de confirmacion=120 s
[RED]  conectado publicado -&gt; mark_app_valid_cancel_rollback()
[OTA]  app1 confirmada la anterior queda como respaldo""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, la biblioteca Update y un esquema de particiones con app0 y app1.

<b>2. Firmware.</b> Consulta a un servidor propio la versión disponible y compárala con la compilada. Si es superior, descarga la imagen a la partición libre, verifica el resumen y la firma, y márcala como pendiente antes de reiniciar. Al arrancar en modo prueba, el firmware dispone de 120 s para conectar y publicar al menos una vez: si lo consigue, llama a <code>esp_ota_mark_app_valid_cancel_rollback()</code>; si no, deja que el plazo venza y el gestor de arranque revierta. Registra cada fase con la versión y la partición implicadas. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los tres LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del arranque en modo prueba, con el plazo de confirmación como una rama que puede no tomarse. Y la <b>máquina de estados</b> de la actualización con la reversión dibujada, señalando el punto exacto en que la versión nueva pasa a ser la definitiva.""",
        "Fijarse en la penúltima línea: la confirmación llega tras <b>publicar</b>, no tras arrancar. Un firmware "
        "que arranca pero no conecta deja el equipo inalcanzable, y confirmarlo sería dar por buena la avería. "
        "Repetir la prueba con la red apagada: la traza debe detenerse en <code>[BOOT]</code> y, pasados los "
        "120 s, volver a la versión anterior sin que nadie toque nada.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="yellow"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ─────────────────────────────────────── 17 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes en firmware de operación continua · Sesión 10",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes en firmware de operación continua", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("Se reinicia al encender la radio", "El equipo funciona hasta que intenta conectar, y entonces se reinicia una y otra vez.", "El pico de corriente de la radio hunde la tensión de alimentación y dispara la protección de brownout. El código no tiene ningún error.", "Leer el reset reason: <code>BROWNOUT</code> lo confirma. Revisar fuente, cable y condensador de desacoplo, no el programa.", "i-bolt")}
{problema("Falla una reserva con memoria de sobra", "Una operación falla por falta de memoria mientras el informe dice que quedan casi 200 kB libres.", "Fragmentación: el espacio libre está troceado y no hay ningún bloque contiguo del tamaño pedido.", "Comparar memoria libre y mayor bloque contiguo. Si la primera se mantiene y el segundo cae, es fragmentación y no fuga.", "i-layers")}
{problema("La NVS deja de guardar", "Tras meses de operación, las escrituras dejan de conservarse entre reinicios.", "Se agotaron los ciclos de borrado del sector por escribir con demasiada frecuencia sobre la misma clave.", "Calcular escrituras por hora contra los ciclos que admite el sector. Acumular en memoria y volcar por bloques.", "i-folder")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("La actualización deja el parque inalcanzable", "Una versión nueva se despliega y los equipos dejan de responder, sin posibilidad de corregir en remoto.", "El firmware nuevo arranca pero no conecta, y se confirmó por el hecho de arrancar en vez de por haber publicado.", "Condicionar la confirmación a haber conectado y publicado al menos una vez, y dejar que el plazo venza en caso contrario.", "i-layers")}
{problema("La conexión segura falla tras el primer arranque", "El equipo conecta al principio y, tras un corte de alimentación, rechaza todos los certificados.", "Arrancó sin red, no pudo sincronizar la hora y quedó en 1970: toda fecha de validez está en el futuro.", "Imprimir la fecha del sistema antes del primer intento seguro y no continuar hasta que supere el año 2020.", "i-clock")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 18 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 10 · Sesión 10",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("Tabla de particiones", "partition table", "Declaración de cómo se reparten los 4 MB de Flash. El gestor de arranque la lee para saber qué aplicación ejecutar.")}
{termino("NVS", "memoria no volátil", "Partición de pares clave-valor para datos pequeños y de escritura ocasional: credenciales, calibración, contadores.")}
{termino("Wear levelling", "nivelado de desgaste", "Reparto del desgaste entre sectores para que ninguno agote sus ciclos de borrado antes que el resto.")}
{termino("Fragmentación", "heap fragmentation", "Situación en que hay memoria libre suficiente pero ningún bloque contiguo del tamaño pedido. Se detecta comparando dos cifras.")}
{termino("High water mark", "", "Peor valor observado desde el arranque, sea de pila libre o de memoria libre. Es la magnitud que decide el margen.")}
{termino("Reset reason", "causa del último reinicio", "Motivo por el que el equipo volvió a arrancar. Es el primer dato de diagnóstico y cuesta una línea registrarlo.")}
{termino("Brownout", "", "Reinicio provocado por una caída de la alimentación, típicamente al encender la radio. Se confunde con un fallo de programa.")}
{termino("Deep sleep", "sueño profundo", "Modo que apaga casi todo y conserva solo la memoria RTC. Al despertar, el programa recomienza desde <code>setup()</code>.")}
{termino("OTA", "actualización remota", "Sustitución del firmware a través de la red, con dos particiones, verificación y reversión automática si el arranque no llega a estado sano.")}
{termino("Secure boot", "arranque seguro", "Mecanismo por el que el chip solo ejecuta binarios firmados. Es irreversible: se activa al cerrar el producto.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 19 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 10 · Sesión 10",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-folder")}Memoria y tiempo</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa tabla de particiones se decide antes de empezar: añadir la segunda
\t\t\t\t\t\t\taplicación después borra todo lo guardado en cada unidad desplegada.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa Flash tiene ciclos contados. Se acumula en memoria y se vuelca por
\t\t\t\t\t\t\tbloques, con la vida útil calculada a partir del ritmo real de
\t\t\t\t\t\t\tescritura.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}Robustez y despliegue</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl reset reason (causa del último reinicio) se registra siempre. Un contador de
\t\t\t\t\t\t\tarranques fallidos permite escalar la respuesta en vez de repetir el
\t\t\t\t\t\t\tmismo fallo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa versión nueva se confirma por <b>haber publicado</b>, no por haber
\t\t\t\t\t\t\tarrancado. Sin esa condición, la reversión no llega a dispararse.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a las sesiones siguientes</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-layers")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Actualizar el binario frente a actualizar el comportamiento</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa sesión 11 compara esta operación con cambiar lo que el dispositivo
\t\t\t\t\t\t\t\thace sin tocar el firmware.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-cpu")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Memoria y consumo como restricción</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa sesión 12 parte de estas dos magnitudes para decidir si un modelo
\t\t\t\t\t\t\t\tcabe en el dispositivo.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-check")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Despliegue y versionado</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tEl mecanismo de actualización de esta sesión es el que distribuye el
\t\t\t\t\t\t\t\tmodelo en la sesión 12.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 20 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 10 · Sesión 10",
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
\t\t\t\t\t\t\t\t<span class="ref__title">Over-the-Air Firmware Updates for Constrained NB-IoT Devices</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Mahfoudhi, F.; Sultania, A. K.; Famaey, J. (2022). <i>Sensors</i> 22(19), 7572. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3390/s22197572</span>
\t\t\t\t\t\t\t\t<span class="ref__where">OTA · Ejemplo 43</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">A Survey of Energy Consumption Measurement in Embedded Systems</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Guo, Y.; Chen, Y.; Wang, Y. et al. (2021). <i>IEEE Access</i> 9, 60516-60530. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/ACCESS.2021.3074070</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Consumo · Alcance de la simulación</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">A Review of IoT Firmware Vulnerabilities and Auditing Techniques</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Bakhshi, T.; Ghita, B.; Kuzminykh, I. (2024). <i>Sensors</i> 24(2), 708. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3390/s24020708</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Diagnóstico · Seguridad del dispositivo</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-10/</code>, junto a dos más sobre secure boot y actualización segura. El índice, en <code>src/paper/INDICE.md</code>.</span>
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
        {"clase": "clase-10", "sesion": "Sesión 10", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
