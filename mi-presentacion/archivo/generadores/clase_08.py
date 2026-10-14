#!/usr/bin/env python3
"""Sesión 8 — Protocolo MQTT y plataformas de IoT.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_08.py
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

A = "01 · Protocolo MQTT"
B = "02 · Plataformas y arquitectura de sistema"

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
    "Sesión 8 · Protocolo MQTT y plataformas de IoT",
    "Protocolo MQTT y plataformas de IoT",
    portada(
        "Sesión 8",
        "Protocolo MQTT y<br />plataformas de IoT",
        "Publicación y suscripción como modelo de intercambio.",
        "Arquitectura completa de un sistema supervisado.",
        [
         ("i-link", "Publicación y suscripción con broker"),
         ("i-folder", "Topics, comodines y jerarquía"),
         ("i-check", "QoS, retained y Last Will"),
         ("i-layers", "TLS y control de acceso por topic"),
        ],
        "02-limitaciones-http.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ──────────────────────────────────────── 02 · limitaciones de HTTP
lamina(
    "limitaciones-http",
    "Cuatro limitaciones de HTTP en aplicaciones de IoT · Sesión 8",
    "Limitaciones de HTTP en IoT",
    envolver(f"""{cabecera(A, "Cuatro limitaciones de HTTP en aplicaciones de IoT", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-clock")}Polling</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tPara enterarse de un cambio, el dispositivo debe preguntar. Preguntar
\t\t\t\t\t\t\tcada 10 s significa <b>8640 peticiones diarias</b>, de las que casi
\t\t\t\t\t\t\ttodas responden que no hay novedad.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Sobrecarga por petición</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada consulta abre una conexión, envía unos <b>192 bytes</b> de
\t\t\t\t\t\t\tcabeceras y la cierra. Con 12 bytes de dato, el protocolo pesa
\t\t\t\t\t\t\tdieciséis veces más que lo transportado.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-bolt")}Consumo energético</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada petición enciende la radio, negocia el transporte y espera. En un
\t\t\t\t\t\t\tequipo alimentado por batería, ese ciclo repetido domina el consumo
\t\t\t\t\t\t\ttotal.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">{ico("i-flow")}Dispositivo no alcanzable</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa cuarta limitación es la de la sesión anterior: tras la traducción
\t\t\t\t\t\t\t\tde direcciones, el servidor <b>no puede iniciar</b> una conexión
\t\t\t\t\t\t\t\thacia el dispositivo. Una orden de apagado tiene que esperar a la
\t\t\t\t\t\t\t\tsiguiente consulta.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Lo que las cuatro tienen en común</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tTodas derivan del mismo rasgo: HTTP <b>abre y cierra una conexión
\t\t\t\t\t\t\t\tpor mensaje</b>. Mantener una sola conexión abierta, iniciada por el
\t\t\t\t\t\t\t\tdispositivo, resuelve las cuatro a la vez. Ese es el planteamiento
\t\t\t\t\t\t\t\tde MQTT.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Escenario</th><th>Con HTTP</th><th>Con conexión mantenida</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td>Enviar una medida cada 10 s</td><td>8640 conexiones al día</td><td>1 conexión, 8640 mensajes</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Bytes de protocolo al día</td><td>~1,66 MB</td><td>~17 kB más el mantenimiento</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Recibir una orden</td><td>Hasta 10 s de retraso</td><td>Inmediata</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Saber si el equipo sigue vivo</td><td>Solo al recibir su consulta</td><td>El broker lo detecta y avisa</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLas cifras de la segunda fila corresponden a 192 bytes de cabecera
\t\t\t\t\t\t\tpor petición frente a 2 bytes por mensaje publicado.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-alert",
)

# ─────────────────────────────────── 03 · publicación y suscripción
lamina(
    "publicacion-suscripcion",
    "Publicación y suscripción frente a petición y respuesta · Sesión 8",
    "Publicación y suscripción",
    envolver(f"""{cabecera(A, "Publicación y suscripción frente a petición y respuesta", "i-link")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl emisor <b>publica</b> en un nombre de asunto sin saber quién
\t\t\t\t\t\t\t\tescucha. El receptor se <b>suscribe</b> a ese nombre sin saber quién
\t\t\t\t\t\t\t\tpublica. Un <b>broker</b> reparte.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tDos desacoplamientos
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>En el direccionamiento:</b> ninguno de los dos extremos conoce la
\t\t\t\t\t\t\t\tdirección del otro, y ambos inician su conexión hacia el
\t\t\t\t\t\t\t\tbroker, lo que sortea la traducción de direcciones.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>En el tiempo:</b> emisor y receptor no necesitan estar conectados
\t\t\t\t\t\t\t\ta la vez. Un retained message (mensaje retenido) espera al suscriptor que aún no ha
\t\t\t\t\t\t\t\tllegado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Qué gana el sistema</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tAñadir un consumidor (un panel, un registro histórico, una alarma)
\t\t\t\t\t\t\t\t<b>no exige modificar el dispositivo</b>. Se suscribe al mismo
\t\t\t\t\t\t\t\tnombre y recibe lo mismo. Con petición y respuesta habría que
\t\t\t\t\t\t\t\treprogramar el emisor para que enviara a un destino más.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">ESP32 · publicador</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Publica en <code>uni/lab3/sensor01/temperatura</code>. No sabe cuántos escuchan.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓ conexión iniciada por el dispositivo</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Broker</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Recibe y reparte a todos los suscritos a ese nombre. No interpreta el contenido.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓ conexiones iniciadas por cada suscriptor</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Tres suscriptores</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Panel de visualización, registro histórico y regla de alarma. Ninguno conoce al ESP32.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tTodas las flechas apuntan hacia el broker en el momento de
\t\t\t\t\t\t\testablecer la conexión. Por eso ninguno de los extremos necesita ser
\t\t\t\t\t\t\talcanzable desde fuera.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-link",
)

# ─────────────────────────────────────────── 04 · función del broker
lamina(
    "funcion-broker",
    "Operaciones que realiza el broker y las que no · Sesión 8",
    "Función del broker",
    envolver(f"""{cabecera(A, "Operaciones que realiza el broker y las que no", "i-cpu")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Lo que hace</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tAcepta conexiones, mantiene la lista de suscripciones, reparte cada
\t\t\t\t\t\t\tmensaje a quien corresponde, aplica el nivel de QoS (calidad de servicio)
\t\t\t\t\t\t\tacordado y vigila que cada cliente siga vivo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tGuarda además el último retained message de cada nombre y el mensaje
\t\t\t\t\t\t\tde Last Will (mensaje de última voluntad) de cada cliente.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Lo que no hace</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tNo interpreta el contenido, no lo transforma, no lo almacena como
\t\t\t\t\t\t\thistórico, no calcula promedios ni genera alarmas. Para el
\t\t\t\t\t\t\tbroker la carga útil es una secuencia de bytes.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tTodo eso corresponde a una <b>plataforma</b>, que es el asunto del
\t\t\t\t\t\t\tTema B.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\tSentido de establecimiento de la conexión
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tLa conexión siempre la inicia el <b>cliente</b> hacia el broker,
\t\t\t\t\t\tnunca al revés, y se mantiene abierta. Sobre esa conexión viajan los
\t\t\t\t\t\tmensajes en <b>ambos sentidos</b>: es lo que permite que el sistema
\t\t\t\t\t\talcance a un dispositivo situado tras una traducción de direcciones.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Implementaciones habituales</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-terminal")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Mosquitto</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tBroker de código abierto, ejecutable en un equipo de la red
\t\t\t\t\t\t\t\tlocal. Es el que se usa en los ejemplos de esta sesión.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Broker público de pruebas</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tAccesible sin credenciales para desarrollo. Cualquiera puede leer y
\t\t\t\t\t\t\t\tescribir en los mismos nombres: no vale para operación.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-chart")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Broker gestionado en la nube</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tParte de una plataforma, con autenticación por dispositivo y
\t\t\t\t\t\t\t\tcontrol de acceso por nombre de asunto.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ────────────────────────────────────────────────────────── 05 · topics
lamina(
    "topics-jerarquia",
    "Jerarquía de nombres de asunto y comodines · Sesión 8",
    "Jerarquía de topics y comodines",
    envolver(f"""{cabecera(A, "Jerarquía de nombres de asunto y comodines", "i-folder")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tEstructura
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>topic</b> es una cadena con niveles separados por barras, de
\t\t\t\t\t\t\t\tlo general a lo particular. No se declara en ninguna parte: existe
\t\t\t\t\t\t\t\ten cuanto alguien publica en él.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t\t<code>uni/lab3/sensor01/temperatura</code>
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tConvenciones que evitan rehacer el sistema
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tMinúsculas y sin acentos ni espacios. Nunca empezar por barra. El
\t\t\t\t\t\t\t\tidentificador del dispositivo en un nivel propio, para poder
\t\t\t\t\t\t\t\tsuscribirse a todos con un comodín. Separar los sentidos:
\t\t\t\t\t\t\t\t<code>.../estado</code> para lo que el dispositivo publica y
\t\t\t\t\t\t\t\t<code>.../comando</code> para lo que recibe.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">El árbol determina la estructura del sistema</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSi el identificador va al final, <code>uni/lab3/temperatura/s01</code>,
\t\t\t\t\t\t\t\tno hay forma de suscribirse a todas las magnitudes de un solo
\t\t\t\t\t\t\t\tdispositivo. La jerarquía se decide antes de desplegar, porque
\t\t\t\t\t\t\t\tcambiarla después obliga a tocar todos los clientes.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Suscripción</th><th>Alcance</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><code>uni/lab3/s01/temperatura</code></td><td>Solo esa magnitud de ese sensor</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>uni/lab3/s01/<b>+</b></code></td><td>Todas las magnitudes de ese sensor, un solo nivel</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>uni/lab3/<b>+</b>/temperatura</code></td><td>La temperatura de todos los sensores del laboratorio</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>uni/lab3/<b>#</b></code></td><td>Todo lo que cuelgue del laboratorio, a cualquier profundidad</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>uni/<b>#</b></code></td><td>El sistema entero. Útil para diagnóstico, costoso en operación</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLos comodines valen para <b>suscribirse</b>, nunca para publicar.
\t\t\t\t\t\t\t\tPublicar en <code>uni/lab3/#</code> no envía a todos los nombres:
\t\t\t\t\t\t\t\tcrea un asunto llamado literalmente así, al que nadie se suscribe.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-folder",
)

# ──────────────────────── 05b · simulación de suscripción con comodines
lamina(
    "simulacion-comodines",
    "Alcance de una suscripción sobre el árbol de topics · Sesión 8",
    "Alcance de una suscripción",
    envolver(f"""{cabecera(A, "Alcance de una suscripción sobre el árbol de topics", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tLas dos reglas
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>+</code> sustituye <b>exactamente un nivel</b>;
\t\t\t\t\t\t\t\t<code>#</code> cubre <b>todos los restantes</b> y solo puede ir al
\t\t\t\t\t\t\t\tfinal. Un topic coincide o no coincide: no hay coincidencia
\t\t\t\t\t\t\t\tparcial.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCada patrón resalta los topics que entrega el broker. Con el
\t\t\t\t\t\t\t\tidentificador del dispositivo en su propio nivel,
\t\t\t\t\t\t\t\t<code>uni/lab3/+/temperatura</code> reúne la misma magnitud de todos
\t\t\t\t\t\t\t\tlos equipos y <code>uni/lab3/esp01/+</code> reúne todas las magnitudes
\t\t\t\t\t\t\t\tde uno. Con el identificador al final, ninguna de las dos consultas
\t\t\t\t\t\t\t\tes expresable.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<div class="picker" id="cmd-picker">
\t\t\t\t\t\t\t\t<button type="button" class="picker__item" data-patron="uni/lab3/esp01/temperatura">esp01/temperatura</button>
\t\t\t\t\t\t\t\t<button type="button" class="picker__item" data-patron="uni/lab3/esp01/+">esp01/+</button>
\t\t\t\t\t\t\t\t<button type="button" class="picker__item" data-patron="uni/lab3/+/temperatura">+/temperatura</button>
\t\t\t\t\t\t\t\t<button type="button" class="picker__item" data-patron="uni/lab3/#">lab3/#</button>
\t\t\t\t\t\t\t\t<button type="button" class="picker__item" data-patron="uni/#">uni/#</button>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="detail-panel mt-3">
\t\t\t\t\t\t\t\t<p class="m-0 text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t\t\tSuscripción activa:
\t\t\t\t\t\t\t\t\t<code id="cmd-patron">uni/lab3/esp01/temperatura</code>
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<ul class="m-0 mt-2 list-none p-0" id="cmd-lista"></ul>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item metric__item--ok">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Topics entregados</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="cmd-entregados">1 de 9</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Mensajes por minuto</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="cmd-carga">12</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Árbol de ejemplo con dos dispositivos y una rama de comandos, y el
\t\t\t// ritmo con que publica cada uno. El segundo dato es lo que convierte
\t\t\t// la elección del patrón en una decisión de ingeniería y no de estilo.
\t\t\tconst TOPICS = [
\t\t\t\t{ t: "uni/lab3/esp01/temperatura", min: 12 },
\t\t\t\t{ t: "uni/lab3/esp01/humedad", min: 12 },
\t\t\t\t{ t: "uni/lab3/esp01/estado", min: 1 },
\t\t\t\t{ t: "uni/lab3/esp01/comando/led", min: 0 },
\t\t\t\t{ t: "uni/lab3/esp02/temperatura", min: 12 },
\t\t\t\t{ t: "uni/lab3/esp02/estado", min: 1 },
\t\t\t\t{ t: "uni/lab5/esp07/temperatura", min: 60 },
\t\t\t\t{ t: "uni/lab5/esp07/estado", min: 1 },
\t\t\t\t{ t: "uni/planta/caudal", min: 30 },
\t\t\t];

\t\t\tconst picker = document.getElementById("cmd-picker");
\t\t\tconst salPatron = document.getElementById("cmd-patron");
\t\t\tconst lista = document.getElementById("cmd-lista");
\t\t\tconst salEntregados = document.getElementById("cmd-entregados");
\t\t\tconst salCarga = document.getElementById("cmd-carga");

\t\t\t// Regla de coincidencia del protocolo, escrita tal cual: '+' consume un
\t\t\t// nivel y '#' consume el resto y termina.
\t\t\tfunction coincide(patron, topic) {
\t\t\t\tconst p = patron.split("/");
\t\t\t\tconst t = topic.split("/");
\t\t\t\tfor (let i = 0; i < p.length; i++) {
\t\t\t\t\tif (p[i] === "#") return true;
\t\t\t\t\tif (i >= t.length) return false;
\t\t\t\t\tif (p[i] !== "+" && p[i] !== t[i]) return false;
\t\t\t\t}
\t\t\t\treturn p.length === t.length;
\t\t\t}

\t\t\tfunction pintar(patron) {
\t\t\t\tsalPatron.textContent = patron;
\t\t\t\tlista.textContent = "";

\t\t\t\tlet entregados = 0;
\t\t\t\tlet carga = 0;
\t\t\t\tfor (const { t, min } of TOPICS) {
\t\t\t\t\tconst hit = coincide(patron, t);
\t\t\t\t\tif (hit) {
\t\t\t\t\t\tentregados += 1;
\t\t\t\t\t\tcarga += min;
\t\t\t\t\t}
\t\t\t\t\tconst li = document.createElement("li");
\t\t\t\t\tli.className = hit
\t\t\t\t\t\t? "font-semibold text-[var(--color-ok)]"
\t\t\t\t\t\t: "is-dimmed";
\t\t\t\t\tconst code = document.createElement("code");
\t\t\t\t\tcode.textContent = t;
\t\t\t\t\tli.append(code);
\t\t\t\t\tif (hit && min > 0) {
\t\t\t\t\t\tconst span = document.createElement("span");
\t\t\t\t\t\tspan.className = "text-[length:var(--fs-micro)] text-[var(--color-text-muted)]";
\t\t\t\t\t\tspan.textContent = ` · ${min}/min`;
\t\t\t\t\t\tli.append(span);
\t\t\t\t\t}
\t\t\t\t\tlista.append(li);
\t\t\t\t}

\t\t\t\tsalEntregados.textContent = `${entregados} de ${TOPICS.length}`;
\t\t\t\tsalCarga.textContent = String(carga);
\t\t\t}

\t\t\tpicker.addEventListener("click", (ev) => {
\t\t\t\tconst boton = ev.target.closest(".picker__item");
\t\t\t\tif (!boton) return;
\t\t\t\tfor (const b of picker.querySelectorAll(".picker__item")) {
\t\t\t\t\tb.classList.toggle("is-selected", b === boton);
\t\t\t\t}
\t\t\t\tpintar(boton.dataset.patron);
\t\t\t});

\t\t\tpicker.querySelector(".picker__item").classList.add("is-selected");
\t\t\tpintar(TOPICS[0].t);
\t\t</script>
""",
)

# ────────────────────────────────────── 06 · La hora del código · 32
lamina(
    "codigo-32-primer-publicador",
    "Código 32 · Publicador y suscriptor sobre el mismo dispositivo · Sesión 8",
    "La hora del código · Publicador y suscriptor",
    hora_del_codigo(
        32,
        "Publicador y suscriptor sobre el mismo dispositivo",
        "Publicar una lectura cada 5 s y, por la misma conexión, atender comandos que encienden un LED desde el "
        "broker. La conexión al broker se modela como máquina de estados, igual que la de red en la "
        "sesión anterior.",
        "Un <b>asunto</b> (topic) es la ruta jerárquica donde se publica; el comodín <code>#</code> suscribe a "
        "toda una rama. El <b>identificador de cliente</b> debe ser único en el broker: si se repite, los "
        "dos dispositivos se expulsan mutuamente sin descanso, y derivarlo de la <b>MAC</b> lo garantiza. La "
        "función de recepción se ejecuta en un contexto donde no conviene trabajar: copia el mensaje, marca una "
        "bandera y devuelve, igual que una rutina de interrupción.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> como sensor y controla un LED en el "
        "<b>GPIO 25</b> con resistencia de 220 Ω según los comandos recibidos.",
        """[MQTT] conectando a 192.168.1.20:1883  id=esp01-a4cf12
[MQTT] conectado suscrito a uni/lab3/esp01/comando/#
[PUB]  t=5000   .../temperatura  &lt;- 23.4  (18 bytes)
[SUB]  t=9120   .../comando/led  -&gt; "on"   led=1
[PUB]  t=10000  .../temperatura  &lt;- 23.6  (18 bytes)
[MQTT] desconectado (rc=-2)  reintento en 1000 ms""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y la biblioteca PubSubClient.

<b>2. Firmware.</b> Conecta al broker con un identificador de cliente derivado de la dirección MAC, para que sea único. Modela la conexión como máquina de estados con reintentos y backoff exponencial, igual que la de red, y no la resuelvas con un bucle de espera. Publica la lectura del GPIO 34 cada 5000 ms en <code>uni/lab3/esp01/temperatura</code> y suscríbete a <code>uni/lab3/esp01/comando/#</code>. La función de recepción solo copia el mensaje a una variable y marca una bandera: el trabajo se hace en el bucle. Emite a 115200 baudios una línea por publicación y por mensaje recibido, con el nombre del asunto y el tamaño.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del bucle, con la recepción marcando la bandera y el tratamiento ocurriendo fuera de ella. Y el <b>árbol de asuntos</b> completo, señalando en cada rama quién publica y quién se suscribe.""",
        "Comparar la línea <code>[SUB]</code> con las de <code>[PUB]</code>: entran y salen mensajes por la "
        "<b>misma conexión</b>, sin que el dispositivo pregunte nada. Ese es el cambio respecto de la sesión "
        "anterior. La última línea es la que conviene provocar: si aparece una y otra vez con "
        "<code>rc=-2</code> cada pocos segundos, casi siempre hay otro equipo usando el mismo identificador de "
        "cliente, y el mensaje no lo dice.",
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

# ────────────────────────────────────────── 07 · niveles de servicio
lamina(
    "niveles-calidad-servicio",
    "Los tres niveles de QoS y su costo · Sesión 8",
    "Niveles de QoS",
    envolver(f"""{cabecera(A, "Los tres niveles de QoS y su costo", "i-check")}

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Nivel</th><th>Garantía</th><th>Mensajes intercambiados</th><th>Tipo de dato al que corresponde</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>QoS 0</b></td>
\t\t\t\t\t\t\t\t<td>Como máximo una vez. Puede perderse</td>
\t\t\t\t\t\t\t\t<td>1</td>
\t\t\t\t\t\t\t\t<td>Medida periódica que se repite pronto: temperatura cada 5 s</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>QoS 1</b></td>
\t\t\t\t\t\t\t\t<td>Al menos una vez. Puede duplicarse</td>
\t\t\t\t\t\t\t\t<td>2</td>
\t\t\t\t\t\t\t\t<td>Aviso de alarma, cambio de estado: perderlo es peor que repetirlo</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>QoS 2</b></td>
\t\t\t\t\t\t\t\t<td>Exactamente una vez</td>
\t\t\t\t\t\t\t\t<td>4</td>
\t\t\t\t\t\t\t\t<td>Orden con efecto acumulativo: incrementar un contador de facturación</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Criterio de elección</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa pregunta no es cuánta fiabilidad se desea sino <b>qué pasa si el
\t\t\t\t\t\t\t\tmensaje se pierde y qué pasa si llega dos veces</b>. Una temperatura
\t\t\t\t\t\t\t\tperdida se sustituye por la siguiente en 5 s: QoS 0. Una orden de
\t\t\t\t\t\t\t\tapertura duplicada abre una puerta ya abierta, lo que es inofensivo
\t\t\t\t\t\t\t\tsi la orden es idempotente: QoS 1 basta.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>QoS 2 rara vez es la respuesta correcta.</b> Cuadruplica los
\t\t\t\t\t\t\t\tmensajes y su latencia, y casi siempre resulta más barato hacer la
\t\t\t\t\t\t\t\toperación idempotente (incluir un identificador de mensaje y
\t\t\t\t\t\t\t\tdescartar el repetido) y quedarse en QoS 1.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="qos-paquetes"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\tSubir un nivel duplica el tráfico; subir dos lo cuadruplica. Es el
\t\t\t\t\t\t\t\tprecio de la garantía, y se paga en cada mensaje.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
)

# ──────────────────── 08 · retenidos, Last Will y sesión
lamina(
    "retenidos-ultima-voluntad",
    "Mensajes retenidos, Last Will y sesión persistente · Sesión 8",
    "Retenidos, Last Will y sesión",
    envolver(f"""{cabecera(A, "Mensajes retenidos, Last Will y sesión persistente", "i-clock")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-folder")}Retained message</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl broker guarda el <b>último</b> mensaje publicado con esa
\t\t\t\t\t\t\tmarca en cada nombre, y lo entrega de inmediato a quien se suscribe
\t\t\t\t\t\t\tdespués.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tSin él, un panel recién abierto queda vacío hasta la siguiente
\t\t\t\t\t\t\tpublicación.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-alert")}Last Will</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tMensaje que el cliente entrega <b>al conectarse</b> y que el
\t\t\t\t\t\t\tbroker publica en su nombre si la conexión se corta sin
\t\t\t\t\t\t\tdespedida.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tEs la única forma de que el sistema distinga «sin novedad» de
\t\t\t\t\t\t\t«desconectado».
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-link")}Sesión persistente</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl broker conserva las suscripciones del cliente y los mensajes
\t\t\t\t\t\t\tde QoS 1 y 2 que llegaron mientras estaba ausente.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tExige un identificador de cliente estable entre reinicios.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Los dos primeros se usan juntos</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl dispositivo publica <code>en linea</code> como retained message en
\t\t\t\t\t\t\t\t<code>.../estado</code> al conectar, y declara <code>desconectado</code>
\t\t\t\t\t\t\t\tcomo Last Will <b>en ese mismo nombre y también retenido</b>.
\t\t\t\t\t\t\t\tCon esa combinación, cualquier panel que se abra en cualquier momento
\t\t\t\t\t\t\t\tve el estado real del equipo, incluso tras un corte de corriente.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-clock")}
\t\t\t\t\t\t\t\tKeepalive
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl cliente promete dar señales al menos cada <b>keepalive (intervalo de mantenimiento)</b>
\t\t\t\t\t\t\t\tsegundos. Si el broker no recibe nada en 1,5 veces ese plazo,
\t\t\t\t\t\t\t\tda la conexión por perdida y publica el Last Will. Un valor de
\t\t\t\t\t\t\t\t60 s detecta la caída en unos 90 s.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="term">[CONN] id=esp01-a4cf12  keepalive=60 s  sesion_persistente=si
[CONN] ultima voluntad: uni/lab3/esp01/estado = "desconectado" (retenido)
[PUB]  uni/lab3/esp01/estado = "en linea" (retenido)
...
[CORTE] alimentacion perdida, sin despedida
[BROKER] t+90 s  keepalive vencido
[BROKER] publica uni/lab3/esp01/estado = "desconectado" (retenido)
[PANEL] suscriptor nuevo recibe de inmediato: "desconectado"</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tEl panel no necesita lógica de vigilancia: el broker publica el
\t\t\t\t\t\t\testado real y el retenido se lo entrega a quien llegue después.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-clock",
)

# ────────────────────────────────────────────── 09 · seguridad de MQTT
lamina(
    "seguridad-mqtt",
    "Autenticación, cifrado del transporte e brokers públicos · Sesión 8",
    "Seguridad del intercambio",
    envolver(f"""{cabecera(A, "Autenticación, cifrado del transporte e brokers públicos", "i-plug")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Broker público</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSin credenciales y sin cifrar. <b>Cualquier cliente conectado puede
\t\t\t\t\t\t\tleer y escribir en cualquier nombre</b>, incluidos los de comando.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tAdecuado para desarrollo y para las prácticas de esta sesión. Nunca
\t\t\t\t\t\t\tpara un sistema en operación, ni siquiera con nombres poco
\t\t\t\t\t\t\tpredecibles: la oscuridad no es una medida de protección.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Broker privado</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCredenciales por dispositivo, cifrado del transporte y <b>control de
\t\t\t\t\t\t\tacceso por nombre</b>: cada equipo solo puede publicar en su rama y
\t\t\t\t\t\t\tsuscribirse a sus comandos.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tEl cifrado usa el puerto 8883 y trae el mismo costo de memoria y la
\t\t\t\t\t\t\tmisma dependencia de la hora que HTTPS en la sesión anterior.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Por qué el control por nombre importa más de lo que parece</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tCon credenciales pero sin control de acceso por nombre, un dispositivo
\t\t\t\t\t\tcomprometido puede publicar en los nombres de comando de <b>todos los
\t\t\t\t\t\tdemás</b>. La autenticación dice quién es; el control de acceso dice qué
\t\t\t\t\t\tpuede tocar, y sin lo segundo el sistema entero comparte la seguridad de
\t\t\t\t\t\tsu equipo más débil.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tEl paso de broker público a privado se planifica <b>desde el
\t\t\t\t\t\tprincipio</b>. Cambia el puerto, añade credenciales, exige certificado y
\t\t\t\t\t\tconsume memoria adicional: descubrirlo al final del proyecto obliga a
\t\t\t\t\t\trevisar el dimensionado de todas las tareas.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-plug",
)

# ──────────────────────── 10 · artículo · panorámica del protocolo
lamina(
    "paper-mqtt-revision",
    "Extensión del uso de MQTT y ámbitos de aplicación documentados · Sesión 8",
    "Artículo · Panorámica de MQTT",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Mishra, B.; Kertesz, A.</b> (2020). The Use of MQTT in M2M and IoT Systems: A Survey. "
        "<i>IEEE Access</i> 8, 201071-201086. <code>doi:10.1109/ACCESS.2020.3035849</code>",
        "Extensión del uso de MQTT y ámbitos de aplicación documentados",
        ["Establecer qué lugar ocupa MQTT entre los protocolos <b>entre máquinas</b>.",
         "La elección suele justificarse por características declaradas, <b>no por adopción</b>.",
         "Revisión de literatura sobre <b>veinte años</b>, sin medidas propias sobre hardware."],
        ["El crecimiento de la investigación sobre MQTT <b>se separa</b> del de AMQP y CoAP.",
         "La separación es <b>sostenida</b>, no de un solo año.",
         "Se documentan aplicaciones en <b>seis ámbitos</b>, del hogar a la energía.",
         "Los autores atribuyen la extensión a la <b>simplicidad del modelo</b>."],
        ["Es el <b>más extendido</b> de su clase por volumen de literatura y de aplicaciones.",
         "Esa extensión <b>no procede</b> de superioridad técnica en todas las dimensiones.",
         "La simplicidad se puede contar: el broker cambia un crecimiento cuadrático de enlaces por uno lineal."],
        [("paper-broker-enlaces",
          "Elaboración propia. La simplicidad del modelo, contada: el broker convierte N × M enlaces en N + M."),
         ("paper-mqtt-ambitos",
          "Los ámbitos con aplicaciones documentadas, que es el dato concreto que aporta la revisión.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────── 11 · La hora del código · 33
lamina(
    "codigo-33-estado-y-calidad",
    "Código 33 · Estado del dispositivo con retenido y Last Will · Sesión 8",
    "La hora del código · Estado y calidad",
    hora_del_codigo(
        33,
        "Estado del dispositivo con retained message y Last Will",
        "Conseguir que el estado publicado coincida con el estado real incluso cuando el equipo pierde la "
        "alimentación sin avisar. Incluye una medida comparada de los tres niveles de QoS sobre "
        "1000 mensajes.",
        "Un mensaje <b>retenido</b> lo guarda el broker y se lo entrega a quien se suscriba después: es lo "
        "que hace que un panel abierto más tarde vea el estado actual y no una pantalla vacía. La <b>última "
        "voluntad</b> es un mensaje que el dispositivo deja declarado al conectar y que el broker publica "
        "en su nombre si desaparece sin despedirse. El <b>keepalive</b> fija cuánto tarda en "
        "darlo por muerto.",
        "El <b>ESP32</b> enciende un LED en el <b>GPIO 25</b> con resistencia de 220 Ω que refleja el estado "
        "publicado. La desconexión brusca se provoca retirando la alimentación de la placa.",
        """[CONN] keepalive=60 s lwt: .../estado="desconectado" (retenido)
[PUB]  .../estado = "en linea" (retenido, qos=1)
[QoS0] 1000 msg paquetes=1000  t=4.2 s perdidos=3
[QoS1] 1000 msg paquetes=2000  t=7.8 s duplicados=2
[QoS2] 1000 msg paquetes=4000  t=16.4 s duplicados=0
[CORTE] alimentacion retirada sin despedida
[BROKER] t+90 s publica estado=desconectado (retenido)""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y la biblioteca PubSubClient.

<b>2. Firmware.</b> Al conectar, declara como Last Will el mensaje <code>desconectado</code> en <code>uni/lab3/esp01/estado</code>, con la marca de retenido activada, y publica en ese mismo nombre <code>en linea</code>, también retenido. Fija el keepalive en 60 s. Implementa después una prueba que publique 1000 mensajes con cada uno de los tres niveles de QoS, midiendo para cada nivel el tiempo total y contando los mensajes que llegan a un suscriptor propio. Emite a 115200 baudios el resumen comparado de los tres.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el LED en el GPIO 25 reflejando el estado publicado.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la conexión, con la declaración de el Last Will antes de la primera publicación. Y la <b>línea de tiempo</b> de una desconexión brusca, marcando el corte, el vencimiento del mantenimiento y el instante en que el broker publica el Last Will.""",
        "Las tres líneas de QoS se leen en la columna de paquetes: <b>1000, 2000 y 4000</b> para "
        "los mismos mil mensajes, y el tiempo pasa de 4,2 a 16,4 s. Ahí está el precio de cada nivel, medido. "
        "Después, la línea del broker: publica la desconexión <b>90 s</b> tras el corte, no en el instante "
        "del corte. Esa demora es el keepalive, y es lo que hay que tener en cuenta al decidir "
        "cuánto puede tardar un panel en enterarse.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-resistor></wokwi-resistor></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ───────────────────────────── 12 · qué aporta una plataforma
lamina(
    "que-aporta-plataforma",
    "Funciones que una plataforma añade sobre un broker · Sesión 8",
    "Qué aporta una plataforma",
    envolver(f"""{cabecera(B, "Funciones que una plataforma añade sobre un broker", "i-chart")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna <b>plataforma de IoT</b> incorpora un broker y añade lo
\t\t\t\t\t\t\t\tque este deliberadamente no hace: guardar, mostrar, avisar y
\t\t\t\t\t\t\t\tadministrar.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Cuándo basta el broker solo</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCuando el consumidor de los datos es otro programa propio y no hacen
\t\t\t\t\t\t\t\tfalta ni panel ni histórico. En cuanto aparece la pregunta «¿qué
\t\t\t\t\t\t\t\ttemperatura hizo el martes?», hace falta almacenamiento, y
\t\t\t\t\t\t\t\tconstruirlo cuesta más que adoptar una plataforma.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Función</th><th>Para qué sirve</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>Almacenamiento histórico</b></td><td>Conservar la serie temporal para consultarla y representarla después</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Paneles de visualización</b></td><td>Mostrar el estado sin programar una aplicación propia</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Alertas</b></td><td>Avisar cuando un valor cruza un umbral o un equipo deja de publicar</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Gestión del parque</b></td><td>Saber qué dispositivos existen, cuáles responden y con qué versión</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Control de acceso</b></td><td>Credenciales por dispositivo y permisos por rama del árbol</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Distribución de actualizaciones</b></td><td>Publicar una versión nueva de firmware al parque; se desarrolla en la sesión 10</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-chart",
)

# ──────────────────────────────── 13 · comparación de plataformas
lamina(
    "comparacion-plataformas",
    "Criterios de elección entre plataformas de IoT · Sesión 8",
    "Criterios de elección de plataforma",
    envolver(f"""{cabecera(B, "Criterios de elección entre plataformas de IoT", "i-target")}

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Plataforma</th><th>Dónde se ejecuta</th><th>Punto fuerte</th><th>Contrapartida</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Blynk</b></td><td>Servicio del proveedor</td>
\t\t\t\t\t\t\t\t<td>Panel web y aplicación móvil sin programar nada</td>
\t\t\t\t\t\t\t\t<td>Dependencia del proveedor; límites en el plan gratuito</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>ThingsBoard</b></td><td>Propio o del proveedor</td>
\t\t\t\t\t\t\t\t<td>Gestión de parque y reglas; instalable en equipo propio</td>
\t\t\t\t\t\t\t\t<td>Requiere administrar el servidor</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Node-RED</b></td><td>Propio</td>
\t\t\t\t\t\t\t\t<td>Integración entre servicios mediante flujos visuales</td>
\t\t\t\t\t\t\t\t<td>No es una plataforma completa: no almacena por sí solo</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Home Assistant</b></td><td>Propio</td>
\t\t\t\t\t\t\t\t<td>Automatización doméstica con descubrimiento automático</td>
\t\t\t\t\t\t\t\t<td>Orientado al hogar, no al despliegue industrial</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Plataformas industriales</b></td><td>Nube del proveedor</td>
\t\t\t\t\t\t\t\t<td>Escala, integración con analítica y garantías de servicio</td>
\t\t\t\t\t\t\t\t<td>Costo y dependencia; complejidad excesiva para un proyecto pequeño</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Los tres criterios que deciden</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<b>Dónde se ejecuta</b> (equipo propio o servicio ajeno), porque
\t\t\t\t\t\tdetermina quién custodia los datos. <b>Costo según el volumen</b> de
\t\t\t\t\t\tmensajes previsto, que hay que calcular antes de elegir. Y <b>grado de
\t\t\t\t\t\tdependencia</b>: si el dispositivo habla MQTT, cambiar de plataforma
\t\t\t\t\t\tsupone reconfigurar; si usa una biblioteca propia del proveedor, supone
\t\t\t\t\t\treprogramar el firmware.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\tPlataforma adoptada
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tLos ejemplos usan <b>Blynk</b> por su plantilla de dispositivo y sus
\t\t\t\t\t\tflujos de datos asociados a pines virtuales, que permiten tener un panel
\t\t\t\t\t\ten marcha en minutos. El firmware se escribe de modo que la publicación
\t\t\t\t\t\tquede aislada en una capa propia, para que sustituirla por MQTT directo
\t\t\t\t\t\tno afecte al resto.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-target",
)

# ────────────────────── 14 · artículo · comparación de plataformas
lamina(
    "paper-plataformas-nube",
    "Comportamiento medido de tres plataformas de nube ante carga creciente · Sesión 8",
    "Artículo · Plataformas de nube",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Pierleoni, P.; Concetti, R.; Belli, A.; Palma, L.</b> (2020). Amazon, Google and Microsoft Solutions "
        "for IoT: Architectures and a Performance Comparison. <i>IEEE Access</i> 8, 5455-5470. "
        "<code>doi:10.1109/ACCESS.2019.2961511</code>",
        "Comportamiento medido de tres plataformas de nube ante carga creciente",
        ["Comparar las tres principales plataformas en sus servicios para IoT.",
         "Medir el <b>tiempo de servicio del broker</b>: de recibir un mensaje a reenviarlo.",
         "Los autores declaran que <b>no buscan recomendar una</b>, sino aportar criterios."],
        ["Publicación con <b>QoS 1</b> y marcas temporales en los dos extremos.",
         "<b>100 ensayos</b> por simulación y <b>23 simulaciones</b>.",
         "Las tres responden de forma <b>uniforme y predecible</b> al aumentar la carga.",
         "Los tiempos difieren entre ellas, pero cada una se mantiene en lo que documenta."],
        ["Se verifican además las <b>limitaciones del plan gratuito</b> de cada proveedor.",
         "El trabajo aporta criterios de comparación, incluido el costo por tipo de carga.",
         "La repetición es lo que permite dar media y desviación en vez de una lectura suelta."],
        [("paper-tiempo-de-servicio",
          "Elaboración propia. Qué tramo cronometran los autores: solo lo que tarda el broker, con el viaje por la red fuera."),
         ("paper-nube-repeticion",
          "Lo que compra repetir la medida 2300 veces: sin eso, la comparación entre plataformas no significaría nada.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────── 15 · arquitectura completa
lamina(
    "arquitectura-completa",
    "Recorrido de un dato y recorrido inverso de un comando · Sesión 8",
    "Arquitectura completa del sistema",
    envolver(f"""{cabecera(B, "Recorrido de un dato y recorrido inverso de un comando", "i-flow")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Dispositivo</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Adquiere, valida, agrega y publica. Guarda en local si no hay enlace.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓ telemetría</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Broker o plataforma</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Reparte, autentica y controla el acceso por rama del árbol.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Almacenamiento y visualización</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Serie temporal, paneles y reglas de alerta.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↕ comandos, en sentido inverso</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Usuario</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Consulta el estado y emite órdenes, que recorren el mismo camino al revés.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="compare">
\t\t\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t\t\t<h3>Telemetría</h3>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tMuchos mensajes, pequeños y periódicos. Perder uno es tolerable
\t\t\t\t\t\t\t\t\tporque el siguiente llega pronto.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t\t\tQoS 0 o 1 · sentido dispositivo → sistema
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t\t\t<h3>Comandos</h3>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tPocos mensajes, esporádicos y con efecto físico. Perder uno deja
\t\t\t\t\t\t\t\t\tal usuario sin saber si su orden se ejecutó.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t\t\tQoS 1 con confirmación · sentido sistema → dispositivo
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Idempotencia y confirmación</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn comando es <b>idempotente</b> si ejecutarlo dos veces produce el
\t\t\t\t\t\t\t\tmismo resultado que una: <code>led=on</code> lo es,
\t\t\t\t\t\t\t\t<code>alternar led</code> no. Con comandos idempotentes, QoS 1 basta
\t\t\t\t\t\t\t\tpese a admitir duplicados. Además, el dispositivo <b>confirma</b>
\t\t\t\t\t\t\t\tpublicando su nuevo estado, con lo que el panel refleja lo ocurrido
\t\t\t\t\t\t\t\ty no lo solicitado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
)

# ──────────────────────────────────── 16 · política de transmisión
lamina(
    "politica-transmision",
    "Envío por variación significativa frente a envío periódico · Sesión 8",
    "Política de transmisión",
    envolver(f"""{cabecera(B, "Envío por variación significativa frente a envío periódico", "i-wave")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t<div class="slide__split-text">
\t\t\t\t<div class="compare">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Envío periódico</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUn mensaje cada intervalo fijo, cambie o no la magnitud. El volumen
\t\t\t\t\t\t\tes conocido de antemano.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tCada 5 s son <b>17 280 mensajes al día</b> por dispositivo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Envío por variación significativa</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSolo cuando la magnitud se aparta del último valor enviado más de un
\t\t\t\t\t\t\tumbral.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tUna temperatura interior con umbral de 0,3 °C: unos <b>200 mensajes al
\t\t\t\t\t\t\tdía</b>.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion">
\t\t\t\t\t<span class="conclusion__label">La combinación es lo que se usa</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tEnvío por variación <b>más un mensaje de seguridad</b> cada cierto
\t\t\t\t\t\ttiempo aunque no haya cambio. Sin ese refuerzo el silencio es ambiguo:
\t\t\t\t\t\tun sensor estable y uno averiado producen lo mismo.
\t\t\t\t\t</p>
\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t<div class="figure__frame" data-figure="politica-transmision"></div>
\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tCada punto rojo es un mensaje publicado. La magnitud se sigue
\t\t\t\t\t\t\tmidiendo cada 5 s: lo que cambia es cuántas veces se transmite.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-layers")}
\t\t\t\t\t\tAgregación previa en el dispositivo
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tMuestrear a 100 Hz no obliga a publicar a 100 Hz: el dispositivo puede
\t\t\t\t\t\tenviar cada minuto la <b>media, el mínimo, el máximo y el número de
\t\t\t\t\t\tmuestras</b>, cuatro números en lugar de 6000. Lo que se descarta hay
\t\t\t\t\t\tque decidirlo, no dejarlo al azar del ancho de banda.
\t\t\t\t\t</p>
\t\t\t\t</div>"""),
    icono="i-wave",
)

# ────────────────────────────────────── 17 · La hora del código · 34
lamina(
    "codigo-34-telemetria-comandos",
    "Código 34 · Telemetría y comandos con confirmación · Sesión 8",
    "La hora del código · Telemetría y comandos",
    hora_del_codigo(
        34,
        "Telemetría por variación y comandos con confirmación de ejecución",
        "Separar telemetría y comandos como flujos con requisitos distintos: la telemetría se publica <b>por "
        "variación</b>, con un mensaje de seguridad cada 60 s, y los comandos son <b>idempotentes</b> y se "
        "confirman publicando el estado resultante.",
        "Publicar <b>por variación</b> es enviar solo cuando el valor se aparta del último enviado; el "
        "<b>mensaje de seguridad</b> periódico evita que el silencio se confunda con una avería. Una orden "
        "<b>idempotente</b> deja el mismo resultado se aplique una vez o tres, y comparar su identificador con el "
        "último atendido descarta los duplicados que QoS 1 admite. La <b>confirmación</b> es el estado resultante "
        "publicado como retenido: dice lo que ocurrió, no lo que se pidió.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> y controla un LED en el <b>GPIO 25</b> con "
        "resistencia de 220 Ω mediante los comandos.",
        """[TELE] t=5000   valor=23.4  variacion=0.0  -&gt; no se publica
[TELE] t=12000  valor=23.8  variacion=0.4  -&gt; publica qos=0
[TELE] t=65000  valor=23.8  seguridad 60 s -&gt; publica qos=0
[CMD]  t=71200  recibido led=on (qos=1)  id=8f21
[CMD]  t=71205  ejecutado publica estado/led=on (retenido)
[CMD]  t=73000  recibido id=8f21  DUPLICADO -&gt; descartado
[RESUMEN] 1 h: por variacion=41 | periodico habria sido=720""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y la biblioteca PubSubClient.

<b>2. Firmware.</b> Muestrea el GPIO 34 cada 1000 ms pero publica solo si el valor se aparta más de 0,3 del último enviado, o si han pasado 60000 ms desde la última publicación. La telemetría va con QoS 0 a <code>uni/lab3/esp01/temperatura</code>. Suscríbete a <code>uni/lab3/esp01/comando/led</code> con QoS 1; los comandos llevan un identificador y descartas los repetidos comparándolo con el último atendido. Tras ejecutar, publica el estado resultante en <code>uni/lab3/esp01/estado/led</code> como retained message. Lleva la cuenta de los mensajes enviados y de los que habría enviado una política periódica de 5 s. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la decisión de publicar: variación, plazo de seguridad, enviar o callar. Y los <b>dos flujos enfrentados</b>, con su nivel de servicio y el camino de la confirmación.""",
        "La última línea es la medida: <b>41 mensajes</b> frente a los 720 de una política periódica, sobre la "
        "misma hora y el mismo dato. Sin ella el ahorro sería una afirmación. Mirar también las dos líneas con "
        "<code>id=8f21</code>: la segunda se descarta.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="orange"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
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

# ───────────────────── 18 · artículo · latencia entre borde y nube
lamina(
    "paper-latencia-borde-nube",
    "Efecto del tamaño de los mensajes sobre la latencia y la memoria del broker · Sesión 8",
    "Artículo · Latencia y memoria del broker",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Tseng, Y.-H.; Wang, C.; Wei, Y.-T.; Chiang, Y.-T.</b> (2025). Cloud-edge MQTT messaging for latency "
        "mitigation and broker memory footprint reduction. <i>PeerJ Computer Science</i>. "
        "<code>doi:10.7717/peerj-cs.2647</code>",
        "Efecto del tamaño de los mensajes sobre la latencia y la memoria del broker",
        ["Ver qué ocurre cuando por un mismo broker circulan <b>tamaños muy distintos</b>.",
         "MQTT <b>no distingue los flujos</b> por tamaño.",
         "Trabajo con análisis, implementación y evaluación empírica y analítica."],
        ["Ante congestión pasajera, los mensajes grandes <b>añaden retraso a los pequeños</b>.",
         "El broker puede <b>quedarse sin memoria</b> al acumular copias pendientes.",
         "Se proponen <b>tres políticas</b> de planificación para los suscriptores del borde.",
         "Y un esquema de <b>reserva explícita</b> de memoria."],
        ["Separar por tamaño y planificar la entrega <b>reduce el retraso</b> impuesto a los pequeños.",
         "Reservar memoria evita que el broker se agote cuando se acumulan copias.",
         "Cada problema observado tiene su respuesta: no son dos mejoras sueltas."],
        [("paper-cola-por-tamano",
          "Cálculo propio con el enlace y los tamaños indicados, no medidas del artículo: reproduce el efecto que describen."),
         ("paper-borde-problema-respuesta",
          "Los dos problemas que produce mezclar tamaños, emparejados con la respuesta que propone cada uno.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ─────────────────── 19 · formato de la carga y operación sin red
lamina(
    "formato-carga-y-sin-red",
    "Formato de la carga útil y operación sin conectividad · Sesión 8",
    "Formato de la carga y operación sin red",
    envolver(f"""{cabecera(B, "Formato de la carga útil y operación sin conectividad", "i-folder")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="compare">
\t\t\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t\t\t<h3>JSON</h3>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tLegible, autodescriptivo y admitido por cualquier herramienta. Una
\t\t\t\t\t\t\t\t\tmedida ocupa unos <b>48 bytes</b>.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<div class="term">{{"id":"esp01","t":23.4,"h":61.2}}</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t\t\t<h3>Codificación binaria</h3>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tCompacta pero opaca: hace falta el esquema para interpretarla. La
\t\t\t\t\t\t\t\t\tmisma medida ocupa <b>10 bytes</b>.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t\t<div class="term">65 73 70 30 31 | 00 EA | 02 65</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Cuándo compensa el cambio</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCon un dispositivo publicando cada minuto, la diferencia es de
\t\t\t\t\t\t\t\t<b>2 MB al año</b>: irrelevante. Con mil dispositivos publicando
\t\t\t\t\t\t\t\tcada segundo son <b>1,2 TB al año</b>, y ahí sí decide el costo de
\t\t\t\t\t\t\t\toperación. El criterio es el volumen, no la elegancia del formato.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tAlmacenar y reenviar
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSin enlace, el dispositivo guarda las medidas en local y las envía
\t\t\t\t\t\t\t\tal recuperarlo. Tres decisiones que hay que tomar antes de
\t\t\t\t\t\t\t\tprogramarlo:
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Cuánto guarda</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Capacidad finita: al llenarse hay que decidir si se descarta lo más antiguo o lo más reciente.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Con qué timestamp</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">La del instante de la medida, no la del envío. Sin ella el histórico queda mal fechado.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Cómo evita duplicados</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Un identificador por medida permite al receptor descartar lo que ya tiene tras un reenvío parcial.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tEl timestamp se toma en el dispositivo, lo que exige la hora
\t\t\t\t\t\t\tsincronizada de la sesión anterior y la NVS (memoria no volátil) de la
\t\t\t\t\t\t\tsesión 10.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-folder",
)

# ────────────────────────────────────── 20 · La hora del código · 35
lamina(
    "codigo-35-sistema-completo",
    "Código 35 · Sistema completo con panel y reenvío diferido · Sesión 8",
    "La hora del código · Sistema completo",
    hora_del_codigo(
        35,
        "Sistema completo con panel de visualización y reenvío diferido",
        "Reunir la sesión entera en un sistema con panel: telemetría agregada por minuto, comandos con "
        "confirmación, y las medidas tomadas sin enlace <b>guardadas y reenviadas</b> con su timestamp "
        "original cuando la red vuelve.",
        "<b>Agregar</b> es sustituir muchas muestras por una que las resume (media, mínimo, máximo y cuántas "
        "eran), y es lo que separa reducir tráfico de perder información. Un <b>arreglo circular</b> guarda las "
        "últimas N agregaciones sobreescribiendo las más viejas; contar los <b>descartes</b> es lo que impide que "
        "el sistema aparente no haber perdido nada. El <b>timestamp original</b> viaja con cada medida: "
        "fechar en el momento del reenvío convertiría el corte en un salto falso de todos los valores.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b>, controla un LED de comando en el "
        "<b>GPIO 25</b> y otro de estado del enlace en el <b>GPIO 26</b>, ambos con resistencia de 220 Ω.",
        """[AGRE] t=60000  n=60  media=23.6  min=23.1  max=24.2  -&gt; 1 msg
[CORTE] broker no responde -&gt; almacenamiento local
[LOCAL] guardadas 14 agregaciones capacidad=60  descartes=0
[REENV] enlace vuelve tras 842 s: 14 msg con marca original
[RESUMEN] 1 h: enviados=41  periodico=720  ahorro=94 %""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, la biblioteca PubSubClient y ArduinoJson.

<b>2. Firmware.</b> Muestrea el GPIO 34 cada 1000 ms y publica una agregación por minuto con media, mínimo, máximo y número de muestras, en JSON y con timestamp del reloj sincronizado. Sin broker, guarda las agregaciones en un arreglo circular de 60 posiciones contando los descartes. Al recuperar el enlace reenvía lo acumulado, conservando la marca original y un identificador por medida. Atiende comandos idempotentes con QoS 1 y confirma publicando el estado resultante como retenido. Emite a 115200 baudios el resumen de mensajes enviados frente a una política periódica.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del ciclo completo, con la rama que lleva al almacenamiento local y la que reenvía al volver el enlace. Y la <b>arquitectura</b> (dispositivo, broker, plataforma, panel y usuario) con el sentido de la telemetría y el de los comandos por separado.""",
        "La línea <code>[LOCAL]</code>: 14 agregaciones guardadas sobre una capacidad de 60 y "
        "<b>descartes = 0</b>. Ese cero es la afirmación de que no se perdió nada; si el corte hubiera durado más "
        "de una hora dejaría de serlo, y el sistema tiene que decirlo en vez de aparentar. En "
        "<code>[REENV]</code>, comprobar que los 14 mensajes llevan la <b>marca original</b>: si llevaran la del "
        "reenvío, las 842 s de corte aparecerían en el panel como un salto instantáneo de todos los valores.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
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

# ─────────────────────────────────────── 21 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes con MQTT y con la plataforma · Sesión 8",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes con MQTT y con la plataforma", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("Desconexiones cíclicas cada pocos segundos", "Dos equipos se conectan y desconectan sin parar, sin que ninguno llegue a publicar de forma estable.", "Ambos usan el mismo identificador de cliente. El protocolo exige que sea único: al conectarse el segundo, el broker expulsa al primero, que reintenta y expulsa al segundo.", "Derivar el identificador de la dirección MAC e imprimirlo al conectar. Dos equipos con el mismo valor en la traza confirman la causa.", "i-link")}
{problema("El panel muestra el equipo activo tras un corte", "Se retira la alimentación del dispositivo y el panel sigue indicando que está en línea.", "No se declaró mensaje de Last Will, o se declaró sin la marca de retenido. Sin él, el broker no tiene nada que publicar en nombre del equipo caído.", "Suscribirse al nombre de estado desde otro cliente y retirar la alimentación. Si no llega nada tras el keepalive, falta el Last Will.", "i-alert")}
{problema("El panel arranca vacío", "Al abrir el panel no aparece ningún valor hasta la siguiente publicación, que puede tardar un minuto.", "Los mensajes se publican sin la marca de retenido, de modo que el broker no guarda el último valor para los suscriptores que llegan después.", "Suscribirse con un cliente nuevo y comprobar si llega algo de inmediato. El silencio indica que no hay retenido.", "i-folder")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("Un comando se ejecuta dos veces", "Una orden enviada una vez produce dos actuaciones sobre el equipo.", "QoS 1 garantiza al menos una entrega y admite duplicados. Si el comando no es idempotente ni lleva identificador, la repetición se ejecuta.", "Registrar el identificador de cada comando atendido. Dos líneas con el mismo identificador confirman el duplicado y no un doble envío.", "i-check")}
{problema("La cuenta de la plataforma se bloquea a media jornada", "Los mensajes dejan de aceptarse tras unas horas de funcionamiento normal.", "Se ha superado el límite del plan contratado. Un dispositivo publicando cada segundo consume 86 400 mensajes diarios, muy por encima de los planes gratuitos.", "Dividir el límite mensual entre los días y entre el número de dispositivos antes de fijar el periodo. La política por variación reduce el volumen en más de un orden de magnitud.", "i-chart")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 22 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 8 · Sesión 8",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("MQTT", "message queuing telemetry transport", "Protocolo de publicación y suscripción sobre TCP, con cabecera mínima de 2 bytes y conexión mantenida iniciada por el cliente.")}
{termino("Broker", "", "Broker que acepta conexiones, mantiene las suscripciones y reparte cada mensaje. No interpreta ni almacena el contenido.")}
{termino("Topic", "", "Nombre de asunto con niveles separados por barras. No se declara: existe en cuanto alguien publica en él.")}
{termino("Comodín de un nivel", "single-level wildcard", "El signo <code>+</code> sustituye exactamente un nivel de la jerarquía en una suscripción. No se admite al publicar.")}
{termino("Comodín de varios niveles", "multi-level wildcard", "El signo <code>#</code> cubre todos los niveles restantes. Solo puede aparecer al final de la suscripción.")}
{termino("QoS", "calidad de servicio", "Garantía de entrega acordada por mensaje: como máximo una vez, al menos una vez o exactamente una vez. Cuesta 1, 2 o 4 paquetes.")}
{termino("Retained message", "mensaje retenido", "Último mensaje publicado con esa marca en un nombre. El broker lo entrega de inmediato a quien se suscriba después.")}
{termino("Last Will", "mensaje de última voluntad", "Mensaje que el broker publica en nombre de un cliente cuando su conexión se corta sin despedida.")}
{termino("Keepalive", "intervalo de mantenimiento", "Plazo máximo que el cliente promete no permanecer en silencio. El broker da la conexión por perdida a 1,5 veces ese valor.")}
{termino("Idempotencia", "idempotence", "Propiedad de un comando cuya repetición produce el mismo resultado. Permite quedarse en QoS 1 en vez de recurrir a QoS 2.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 23 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 8 · Sesión 8",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-link")}Protocolo</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUna conexión mantenida, iniciada por el dispositivo, resuelve a la vez
\t\t\t\t\t\t\tel costo por mensaje, el consumo y la imposibilidad de alcanzar al
\t\t\t\t\t\t\tequipo tras la traducción de direcciones.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl nivel de servicio se elige preguntando qué pasa si el mensaje se
\t\t\t\t\t\t\tpierde y qué pasa si llega dos veces. QoS 2 rara vez es la respuesta.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-chart")}Sistema</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tRetenido y Last Will, usados juntos, hacen que el estado
\t\t\t\t\t\t\tpublicado coincida con el real ante cualquier interrupción.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tTelemetría y comandos son flujos distintos. La agregación en el
\t\t\t\t\t\t\tdispositivo y el envío por variación reducen el tráfico en más de un
\t\t\t\t\t\t\torden de magnitud.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a las sesiones siguientes</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Interfaz local frente a interfaz remota</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa sesión 9 añade una interfaz servida por el propio dispositivo, que
\t\t\t\t\t\t\t\tfunciona sin acceso a internet.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-folder")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Almacenamiento no volátil</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tEl reenvío diferido exige conservar las medidas entre reinicios, que
\t\t\t\t\t\t\t\tes materia de la sesión 10.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-cpu")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Transmisión del resultado de una inferencia</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa sesión 12 publica por esta misma vía la decisión de un modelo
\t\t\t\t\t\t\t\tejecutado en el dispositivo.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 24 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 8 · Sesión 8",
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
\t\t\t\t\t\t\t\t<span class="ref__title">The Use of MQTT in M2M and IoT Systems: A Survey</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Mishra, B.; Kertesz, A. (2020). <i>IEEE Access</i> 8, 201071-201086. Dominio público.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/ACCESS.2020.3035849</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Panorámica del protocolo · Extensión de uso</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Amazon, Google and Microsoft Solutions for IoT: Architectures and a Performance Comparison</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Pierleoni, P.; Concetti, R.; Belli, A.; Palma, L. (2020). <i>IEEE Access</i> 8, 5455-5470. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/ACCESS.2019.2961511</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Elección de plataforma · Método de medida</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Cloud-edge MQTT messaging for latency mitigation and broker memory footprint reduction</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Tseng, Y.-H.; Wang, C.; Wei, Y.-T.; Chiang, Y.-T. (2025). <i>PeerJ Computer Science</i> 11, e2741. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.7717/peerj-cs.2741</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Agregación · Tamaño de la carga útil</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-08/</code>, junto a dos más sobre límites del broker y brokers distribuidos. El índice, en <code>src/paper/INDICE.md</code>.</span>
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
        {"clase": "clase-08", "sesion": "Sesión 8", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
