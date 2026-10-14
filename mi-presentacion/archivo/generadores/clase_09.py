#!/usr/bin/env python3
"""Sesión 9 — Servidor web embebido, provisioning e integración en un producto.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_09.py
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

A = "01 · Servidor web embebido"
B = "02 · Requisitos de un producto"

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
    "Sesión 9 · Servidor web embebido, provisioning e integración en un producto",
    "Servidor web embebido y producto",
    portada(
        "Sesión 9",
        "Servidor web embebido<br />e integración en un producto",
        "El dispositivo pasa de cliente a servidor.",
        "Provisioning de credenciales y requisitos de producto.",
        [
         ("i-flow", "Servidor asíncrono y rutas HTTP"),
         ("i-folder", "Interfaz servida desde LittleFS"),
         ("i-link", "Portal cautivo y provisioning"),
         ("i-check", "mDNS, identidad y factory reset"),
        ],
        "02-inversion-del-rol.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ───────────────────────────────────── 02 · inversión del rol
lamina(
    "inversion-del-rol",
    "Cambios en el dispositivo al pasar de cliente a servidor · Sesión 9",
    "De cliente a servidor",
    envolver(f"""{cabecera(A, "Cambios en el dispositivo al pasar de cliente a servidor", "i-link")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Como cliente · sesiones 7 y 8</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl dispositivo <b>elige cuándo</b> hablar. Abre una conexión, la usa
\t\t\t\t\t\t\ty la cierra. El consumo de memoria es conocido y ocurre en el
\t\t\t\t\t\t\tinstante que el programa decide.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Como servidor · esta sesión</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl dispositivo <b>no controla</b> cuándo llegan las peticiones ni
\t\t\t\t\t\t\tcuántas llegan a la vez. Cada conexión abierta reserva memoria, y
\t\t\t\t\t\t\tese consumo lo fija quien se conecta.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tLa consecuencia que sorprende
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn navegador moderno abre <b>varias conexiones simultáneas</b> para
\t\t\t\t\t\t\t\tcargar una sola página: una por el documento y una por cada
\t\t\t\t\t\t\t\trecurso. Una página con hoja de estilos, guion e icono son cuatro
\t\t\t\t\t\t\t\tconexiones de un solo visitante.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa pila de red del ESP32 admite un número limitado de sockets
\t\t\t\t\t\t\t\tsimultáneos, fijado en la configuración del proyecto. Superado ese
\t\t\t\t\t\t\t\tlímite, las conexiones nuevas se rechazan: el navegador muestra la
\t\t\t\t\t\t\t\tpágina a medias y el fallo parece del código de la interfaz.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="term">[HTTP] GET /            200  1284 B  conexion 1
[HTTP] GET /estilo.css   200   842 B  conexion 2
[HTTP] GET /panel.js     200  2110 B  conexion 3
[HTTP] GET /favicon.svg  200   312 B  conexion 4
[MEM]  libre antes=214512  con 4 conexiones=196880  por conexion≈4.4 kB</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Criterio de diseño</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tReducir el <b>número de recursos</b> de la página vale más que
\t\t\t\t\t\t\t\treducir su tamaño: cada archivo suelto cuesta una conexión, y las
\t\t\t\t\t\t\t\tconexiones son el recurso escaso. Una interfaz de un solo archivo
\t\t\t\t\t\t\t\tse sirve con una sola.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-link",
)

# ─────────────────────────────────────── 03 · modos de operación
lamina(
    "modos-operacion",
    "Estación, punto de acceso y modo combinado · Sesión 9",
    "Modos de operación de la radio",
    envolver(f"""{cabecera(A, "Estación, punto de acceso y modo combinado", "i-wave")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-link")}Estación</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSe une a una red existente. Recibe su dirección por DHCP y es
\t\t\t\t\t\t\talcanzable dentro de esa red, no desde fuera.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>WIFI_STA</code> · el modo de las sesiones 7 y 8.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-wave")}Punto de acceso</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCrea su propia red y reparte direcciones. Los clientes se conectan a
\t\t\t\t\t\t\tél <b>sin que exista ninguna otra red</b>.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>WIFI_AP</code> · máximo de 4 clientes por omisión.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Combinado</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tAmbos a la vez. Permite configurar el dispositivo mientras sigue
\t\t\t\t\t\t\tconectado, pero <b>comparten una sola radio y un solo canal</b>.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>WIFI_AP_STA</code> · el punto de acceso adopta el canal de la
\t\t\t\t\t\t\tred a la que se una.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tEn modo combinado <b>el canal no se elige</b>: al asociarse como
\t\t\t\t\t\testación, el punto de acceso propio se mueve al canal de esa red y los
\t\t\t\t\t\tclientes ya conectados a él pierden el enlace. Es el fallo
\t\t\t\t\t\tcaracterístico de este modo, y su síntoma (el móvil se desconecta justo
\t\t\t\t\t\tal guardar las credenciales) no señala la causa.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Cómo se usa en un producto</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tSin credenciales guardadas, el dispositivo arranca como <b>punto de
\t\t\t\t\t\tacceso</b> y ofrece el portal de configuración. Con credenciales
\t\t\t\t\t\tválidas, arranca como <b>estación</b> y sirve su interfaz dentro de la
\t\t\t\t\t\tred del usuario. El modo combinado se reserva para el instante de la
\t\t\t\t\t\ttransición, y se abandona en cuanto la conexión se confirma.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-wave",
)

# ──────────────────────────── 04 · servidor síncrono y asíncrono
lamina(
    "servidor-sincrono-asincrono",
    "Servidor síncrono frente a asíncrono y su efecto sobre las tareas · Sesión 9",
    "Servidor síncrono o asíncrono",
    envolver(f"""{cabecera(A, "Servidor síncrono frente a asíncrono y su efecto sobre las tareas", "i-cpu")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="compare">
\t\t\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t\t\t<h3>Síncrono</h3>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tSe consulta desde el bucle con
\t\t\t\t\t\t\t\t\t<code>server.handleClient()</code> y atiende una petición por
\t\t\t\t\t\t\t\t\tllamada. Mientras la atiende, el bucle está ocupado.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t\t\t<h3>Asíncrono</h3>
\t\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t\tAtiende en su propia tarea y llama a los manejadores por
\t\t\t\t\t\t\t\t\tsuceso. El bucle no interviene y varias peticiones se solapan.
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEn el asíncrono, el manejador se ejecuta <b>en el contexto de la
\t\t\t\t\t\t\t\ttarea del servidor</b>: no debe bloquear ni hacer trabajo largo,
\t\t\t\t\t\t\t\tigual que una rutina de interrupción. Un manejador que lee un
\t\t\t\t\t\t\t\tsensor lento detiene la atención de todas las demás peticiones.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tPartes de una ruta
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna <b>ruta</b> asocia un método y un camino a un
\t\t\t\t\t\t\t\t<b>manejador</b>. La petición aporta <b>parámetros de consulta</b>
\t\t\t\t\t\t\t\ty, en escritura, un <b>cuerpo</b>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">rutas de un panel mínimo</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>// Recurso estático: se sirve desde el sistema de archivos
server.serveStatic("/", LittleFS, "/www/")
      .setDefaultFile("index.html");

// Estado: solo lectura, devuelve JSON
server.on("/api/estado", HTTP_GET, [](AsyncWebServerRequest *r) {{
  <span class="hl hl--hit">r-&gt;send(200, "application/json", estadoEnJson());</span>
}});

// Comando: escritura, con parámetro de consulta
server.on("/api/led", HTTP_POST, [](AsyncWebServerRequest *r) {{
  <span class="hl hl--add">bool on = r-&gt;getParam("valor", true)-&gt;value() == "1";</span>
  solicitarLed(on);          // solo encola: no actúa aquí
  r-&gt;send(200);
}});</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tEl manejador de escritura <b>encola</b> la orden en vez de ejecutarla:
\t\t\t\t\t\t\tes el mismo patrón de la sesión 4, con la tarea del servidor en el
\t\t\t\t\t\t\tlugar de la rutina de interrupción.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ───────────────────── 05 · simulación de conexiones concurrentes
lamina(
    "simulacion-conexiones",
    "Coste en memoria de las conexiones simultáneas · Sesión 9",
    "Coste de las conexiones simultáneas",
    envolver(f"""{cabecera(A, "Coste en memoria de las conexiones simultáneas", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué se está contando
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCada visitante abre una conexión por <b>recurso</b> de la página.
\t\t\t\t\t\t\t\tCada conexión reserva memoria mientras dura, y con cifrado del
\t\t\t\t\t\t\t\ttransporte esa reserva se multiplica.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCon la interfaz repartida en cinco archivos, tres visitantes
\t\t\t\t\t\t\t\tsimultáneos agotan el límite de sockets antes que la memoria. Reunir
\t\t\t\t\t\t\t\tesos cinco en uno solo divide por cinco las conexiones sin cambiar
\t\t\t\t\t\t\t\tni un byte del contenido, y es la razón de comprimir e incorporar
\t\t\t\t\t\t\t\tlos recursos en un único archivo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="con-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Barras apiladas de conexiones abiertas por visitante frente al límite de sockets del dispositivo, y memoria reservada frente a la disponible"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<label for="con-vis" class="text-sm font-medium">Visitantes simultáneos</label>
\t\t\t\t\t\t\t\t<input type="range" id="con-vis" min="1" max="6" step="1" value="2" />
\t\t\t\t\t\t\t\t<span class="readout" id="con-vis-lec">2</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="controls mt-2">
\t\t\t\t\t\t\t\t<label for="con-rec" class="text-sm font-medium">Archivos de la interfaz</label>
\t\t\t\t\t\t\t\t<input type="range" id="con-rec" min="1" max="6" step="1" value="5" />
\t\t\t\t\t\t\t\t<span class="readout" id="con-rec-lec">5</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="controls mt-2">
\t\t\t\t\t\t\t\t<label class="flex items-center gap-2 text-sm">
\t\t\t\t\t\t\t\t\t<input type="checkbox" id="con-tls" class="accent-[var(--color-accent)]" />
\t\t\t\t\t\t\t\t\tcifrado del transporte
\t\t\t\t\t\t\t\t</label>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item" id="con-item-soc">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Conexiones pedidas</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="con-soc">10 de 8</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="con-item-mem">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Memoria reservada</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="con-mem">44 kB</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="con-item-res">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Resultado</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="con-res">se sirve</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Cifras del orden de las que se miden en el dispositivo: el límite de
\t\t\t// sockets simultáneos de la pila y lo que reserva cada conexión, con y
\t\t\t// sin cifrado del transporte.
\t\t\tconst LIMITE_SOCKETS = 8;
\t\t\tconst KB_POR_CONEXION = 4.4;
\t\t\tconst KB_POR_CONEXION_TLS = 26.0;
\t\t\tconst KB_LIBRES = 195;

\t\t\tconst lienzo = document.getElementById("con-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst dVis = document.getElementById("con-vis");
\t\t\tconst dRec = document.getElementById("con-rec");
\t\t\tconst cTls = document.getElementById("con-tls");
\t\t\tconst lecVis = document.getElementById("con-vis-lec");
\t\t\tconst lecRec = document.getElementById("con-rec-lec");
\t\t\tconst salSoc = document.getElementById("con-soc");
\t\t\tconst salMem = document.getElementById("con-mem");
\t\t\tconst salRes = document.getElementById("con-res");
\t\t\tconst itSoc = document.getElementById("con-item-soc");
\t\t\tconst itMem = document.getElementById("con-item-mem");
\t\t\tconst itRes = document.getElementById("con-item-res");

\t\t\tfunction variable(n) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(n).trim();
\t\t\t}
\t\t\tfunction coma(n, d) {
\t\t\t\treturn n.toFixed(d).replace(".", ",");
\t\t\t}

\t\t\tfunction dibujar(vis, rec, tls) {
\t\t\t\tconst pedidas = vis * rec;
\t\t\t\tconst servidas = Math.min(pedidas, LIMITE_SOCKETS);
\t\t\t\tconst kb = servidas * (tls ? KB_POR_CONEXION_TLS : KB_POR_CONEXION);

\t\t\t\tconst w = lienzo.width;
\t\t\t\tctx.clearRect(0, 0, w, lienzo.height);
\t\t\t\tconst izq = 150;
\t\t\t\tconst ancho = w - izq - 40;
\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst texto = variable("--color-text");
\t\t\t\tconst borde = variable("--color-border");
\t\t\t\tconst ok = variable("--color-ok");
\t\t\t\tconst acento = variable("--color-accent");
\t\t\t\tconst navy = variable("--color-navy");

\t\t\t\t// Fila 1: conexiones, una casilla por socket del límite
\t\t\t\tconst y1 = 86;
\t\t\t\tconst cw = ancho / LIMITE_SOCKETS;
\t\t\t\tfor (let i = 0; i < LIMITE_SOCKETS; i++) {
\t\t\t\t\tconst x = izq + i * cw;
\t\t\t\t\tctx.fillStyle = i < servidas ? ok : variable("--color-surface");
\t\t\t\t\tctx.strokeStyle = borde;
\t\t\t\t\tctx.lineWidth = 1.2;
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.roundRect(x + 3, y1, cw - 6, 46, 5);
\t\t\t\t\tctx.fill();
\t\t\t\t\tctx.stroke();
\t\t\t\t}
\t\t\t\t// Las que no caben, dibujadas fuera del límite
\t\t\t\tconst sobran = pedidas - servidas;
\t\t\t\tif (sobran > 0) {
\t\t\t\t\tctx.fillStyle = acento;
\t\t\t\t\tctx.font = "600 13px system-ui";
\t\t\t\t\tctx.textAlign = "left";
\t\t\t\t\tctx.fillText(`+${sobran} rechazadas`, izq + ancho + 6, y1 + 28);
\t\t\t\t}
\t\t\t\tctx.fillStyle = texto;
\t\t\t\tctx.font = "600 13px system-ui";
\t\t\t\tctx.textAlign = "right";
\t\t\t\tctx.fillText("Conexiones", izq - 14, y1 + 22);
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px ui-monospace, monospace";
\t\t\t\tctx.fillText(`límite ${LIMITE_SOCKETS}`, izq - 14, y1 + 38);

\t\t\t\t// Fila 2: memoria reservada sobre la disponible
\t\t\t\tconst y2 = 190;
\t\t\t\tconst frac = Math.min(1, kb / KB_LIBRES);
\t\t\t\tctx.fillStyle = variable("--color-surface");
\t\t\t\tctx.strokeStyle = borde;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.roundRect(izq, y2, ancho, 46, 6);
\t\t\t\tctx.fill();
\t\t\t\tctx.stroke();
\t\t\t\tctx.fillStyle = frac > 0.75 ? acento : navy;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.roundRect(izq, y2, Math.max(4, ancho * frac), 46, 6);
\t\t\t\tctx.fill();
\t\t\t\tctx.fillStyle = texto;
\t\t\t\tctx.font = "600 13px system-ui";
\t\t\t\tctx.textAlign = "right";
\t\t\t\tctx.fillText("Memoria", izq - 14, y2 + 22);
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px ui-monospace, monospace";
\t\t\t\tctx.fillText(`${KB_LIBRES} kB libres`, izq - 14, y2 + 38);

\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.fillText(
\t\t\t\t\t`${vis} visitantes × ${rec} archivos = ${pedidas} conexiones` +
\t\t\t\t\t\t(tls ? " · con cifrado del transporte" : ""),
\t\t\t\t\tizq,
\t\t\t\t\t50,
\t\t\t\t);
\t\t\t\tctx.fillText(`${coma(kb, 1)} kB reservados`, izq, y2 + 68);

\t\t\t\treturn { pedidas, servidas, kb };
\t\t\t}

\t\t\tfunction actualizar() {
\t\t\t\tconst vis = Number(dVis.value);
\t\t\t\tconst rec = Number(dRec.value);
\t\t\t\tconst tls = cTls.checked;
\t\t\t\tlecVis.textContent = String(vis);
\t\t\t\tlecRec.textContent = String(rec);

\t\t\t\tconst { pedidas, servidas, kb } = dibujar(vis, rec, tls);
\t\t\t\tsalSoc.textContent = `${pedidas} de ${LIMITE_SOCKETS}`;
\t\t\t\tsalMem.textContent = `${coma(kb, 1)} kB`;

\t\t\t\tconst faltanSockets = pedidas > LIMITE_SOCKETS;
\t\t\t\tconst faltaMemoria = kb > KB_LIBRES;
\t\t\t\tsalRes.textContent = faltaMemoria
\t\t\t\t\t? "sin memoria"
\t\t\t\t\t: faltanSockets
\t\t\t\t\t\t? "página a medias"
\t\t\t\t\t\t: "se sirve";

\t\t\t\titSoc.classList.toggle("metric__item--bad", faltanSockets);
\t\t\t\titSoc.classList.toggle("metric__item--ok", !faltanSockets);
\t\t\t\titMem.classList.toggle("metric__item--bad", faltaMemoria);
\t\t\t\titMem.classList.toggle("metric__item--ok", !faltaMemoria);
\t\t\t\titRes.classList.toggle("metric__item--bad", faltanSockets || faltaMemoria);
\t\t\t\titRes.classList.toggle("metric__item--ok", !faltanSockets && !faltaMemoria);
\t\t\t}

\t\t\tfor (const el of [dVis, dRec, cTls]) el.addEventListener("input", actualizar);
\t\t\tnew MutationObserver(actualizar).observe(document.documentElement, {
\t\t\t\tattributes: true,
\t\t\t\tattributeFilter: ["data-theme"],
\t\t\t});
\t\t\tactualizar();
\t\t</script>
""",
)

# ────────────────────────────────────── 06 · La hora del código · 36
lamina(
    "codigo-36-panel-servido",
    "Código 36 · Panel servido desde el sistema de archivos · Sesión 9",
    "La hora del código · Panel servido",
    hora_del_codigo(
        36,
        "Panel de control servido desde el sistema de archivos",
        "Servir una página de control desde <b>LittleFS</b>, no como cadenas dentro del código. Tres rutas: la "
        "estática, una de estado que devuelve JSON y una de comando. Se mide la memoria libre con el panel "
        "abierto y cerrado.",
        "<b>LittleFS</b> es un sistema de archivos sobre la partición de datos: la interfaz vive ahí y se "
        "sustituye sin recompilar. Un <b>servidor asíncrono</b> atiende cada petición en su propia tarea, así que "
        "el manejador se ejecuta en un contexto donde el trabajo largo detiene todo lo demás: se limita a encolar. "
        "<b>mDNS</b> publica un nombre local, de modo que el panel se abre por nombre y no por dirección.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> como magnitud a mostrar y controla un LED en el "
        "<b>GPIO 25</b> con resistencia de 220 Ω desde el panel.",
        """[FS]   LittleFS montado usado=48 kB de 1408 kB  archivos=3
[HTTP] servidor asincrono en el puerto 80  ip=192.168.1.47
[HTTP] GET /            200  1284 B
[HTTP] GET /api/estado  200    64 B  v=1.842
[HTTP] POST /api/led    200     0 B  valor=1
[MEM]  sin panel=214512  con panel=196880  diferencia=17.6 kB""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y las bibliotecas ESPAsyncWebServer y ArduinoJson.

<b>2. Firmware.</b> Monta LittleFS y sirve desde <code>/www/</code> una página con su hoja de estilos, sin incrustar HTML como cadenas en el código. Añade <code>GET /api/estado</code>, que devuelve en JSON la lectura del GPIO 34 y el estado del LED, y <code>POST /api/led?valor=0|1</code>, cuyo manejador solo encola la orden: la actuación ocurre en el bucle. Publica el nombre local con mDNS. Imprime a 115200 baudios cada petición atendida con su ruta, su código y su tamaño, y la memoria libre con el panel abierto y cerrado.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una orden, desde que el manejador la encola hasta que el bucle la ejecuta. Y el <b>árbol de rutas</b> del servidor, con el método de cada una, qué devuelve y si escribe algo en el dispositivo.""",
        "La línea <code>[MEM]</code> es la que decide: tener el panel abierto cuesta <b>17,6 kB</b>. Con varios "
        "navegadores conectados esa cifra se multiplica, y es la que hay que restar antes de añadir una conexión "
        "segura o un modelo. Comprobar además que la petición <code>POST</code> devuelve enseguida: si tardara lo "
        "que dura la actuación, el manejador estaría trabajando en vez de encolar.",
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

# ─────────────────── 07 · interfaz servida desde el sistema de archivos
lamina(
    "interfaz-fuera-del-binario",
    "Recursos servidos desde el sistema de archivos, no desde el código · Sesión 9",
    "La interfaz fuera del binario",
    envolver(f"""{cabecera(A, "Recursos servidos desde el sistema de archivos, no desde el código", "i-folder")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>HTML como cadena en el código</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCambiar un rótulo obliga a recompilar y regrabar. El HTML ocupa
\t\t\t\t\t\t\tespacio en la partición de aplicación y hay que escapar cada comilla.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Recursos en el sistema de archivos</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSe sustituye el archivo y basta. Los recursos viven en su propia
\t\t\t\t\t\t\tpartición y se editan con las herramientas habituales de la web.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLos archivos se colocan en <code>data/</code> y se suben con la
\t\t\t\t\t\t\t\torden de sistema de archivos de PlatformIO, que es <b>distinta</b>
\t\t\t\t\t\t\t\tde la de grabar el firmware: son dos particiones y dos
\t\t\t\t\t\t\t\toperaciones. Olvidar la segunda deja un servidor que responde 404 a
\t\t\t\t\t\t\t\ttodo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Sin acceso a internet</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl dispositivo debe presentar su interfaz <b>aunque no haya
\t\t\t\t\t\t\t\tinternet</b>: durante el provisioning (aprovisionamiento) no lo hay por
\t\t\t\t\t\t\t\tdefinición. Toda biblioteca externa se incorpora al sistema de
\t\t\t\t\t\t\t\tarchivos; una hoja de estilos traída de un servicio ajeno deja el
\t\t\t\t\t\t\t\tportal sin formato justo cuando más importa.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="file-tree">
\t\t\t\t\t\t\t<div class="file-tree__row"><span class="file-tree__name">data/www/index.html</span><span class="file-tree__annotation">página del panel</span></div>
\t\t\t\t\t\t\t<div class="file-tree__row"><span class="file-tree__name">data/www/estilo.css</span><span class="file-tree__annotation">comprimido con gzip</span></div>
\t\t\t\t\t\t\t<div class="file-tree__row"><span class="file-tree__name">data/www/panel.js</span><span class="file-tree__annotation">sin dependencias externas</span></div>
\t\t\t\t\t\t\t<div class="file-tree__row"><span class="file-tree__name">src/main.cpp</span><span class="file-tree__annotation">rutas y lógica, sin HTML</span></div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">$ pio run --target uploadfs     # sistema de archivos
$ pio run --target upload       # firmware
[FS] LittleFS montado  usado=48 kB de 1408 kB</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa compresión con gzip se sirve tal cual: el navegador la descomprime
\t\t\t\t\t\t\ty el dispositivo ahorra el espacio y el tiempo de transmisión.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-folder",
)

# ──────────────────── 08 · actualización de datos en la interfaz
lamina(
    "actualizacion-datos-interfaz",
    "Tres formas de mantener la interfaz al día y su costo · Sesión 9",
    "Actualización de datos en la interfaz",
    envolver(f"""{cabecera(A, "Tres formas de mantener la interfaz al día y su costo", "i-wave")}

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Mecanismo</th><th>Quién toma la iniciativa</th><th>Costo en el dispositivo</th><th>Cuándo se elige</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Polling</b></td>
\t\t\t\t\t\t\t\t<td>El navegador, cada intervalo</td>
\t\t\t\t\t\t\t\t<td>Una conexión nueva por consulta</td>
\t\t\t\t\t\t\t\t<td>Magnitudes que cambian despacio; es lo más simple</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Server-Sent Events (SSE)</b></td>
\t\t\t\t\t\t\t\t<td>El dispositivo, cuando hay novedad</td>
\t\t\t\t\t\t\t\t<td>Una conexión mantenida por visitante</td>
\t\t\t\t\t\t\t\t<td>Telemetría en un solo sentido</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>WebSocket</b></td>
\t\t\t\t\t\t\t\t<td>Ambos, en cualquier momento</td>
\t\t\t\t\t\t\t\t<td>Una conexión mantenida y memoria por marco</td>
\t\t\t\t\t\t\t\t<td>Cuando el panel también manda órdenes</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Criterio</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tEl polling (consulta periódica) es la única que <b>no mantiene conexión abierta</b>,
\t\t\t\t\t\ty por eso es la que escala a más visitantes con el límite de sockets de
\t\t\t\t\t\tla lámina anterior. Las otras dos consumen un socket por visitante
\t\t\t\t\t\tmientras el panel esté abierto: con cuatro pestañas olvidadas, el
\t\t\t\t\t\tdispositivo se queda sin sockets sin que nadie esté mirando.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tCon WebSocket hay que <b>cerrar las conexiones muertas</b>: un navegador
\t\t\t\t\t\tque se cierra sin despedirse deja el socket ocupado hasta que vence el
\t\t\t\t\t\tplazo de la pila. Es el mismo problema que resolvía el mensaje de última
\t\t\t\t\t\tvoluntad en la sesión 8, aquí sin nadie que lo publique.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-wave",
)

# ──────────────────────────── 09 · API propia y nombre local
lamina(
    "api-propia-y-mdns",
    "La API del dispositivo y su nombre en la red local · Sesión 9",
    "API propia y nombre local",
    envolver(f"""{cabecera(A, "La API del dispositivo y su nombre en la red local", "i-target")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tLa API es parte del producto
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLos puntos de acceso de estado y de configuración no sirven solo al
\t\t\t\t\t\t\t\tpanel propio: los consume cualquier aplicación externa, un panel de
\t\t\t\t\t\t\t\tterceros o un agente. Diseñarlos como interfaz pública, y no como
\t\t\t\t\t\t\t\tdetalle interno, es lo que hace integrable el dispositivo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t\t\tResolución por nombre local
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa dirección la asigna la red y cambia. <b>mDNS</b> publica un
\t\t\t\t\t\t\t\tnombre, <code>esp32-a4cf12.local</code>, que se resuelve dentro de
\t\t\t\t\t\t\t\tla red local sin ningún servidor de nombres.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t\t<code>MDNS.begin(nombre)</code> y
\t\t\t\t\t\t\t\t<code>MDNS.addService("http", "tcp", 80)</code>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Punto de acceso</th><th>Qué hace</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><code>GET /api/info</code></td><td>Modelo, número de serie, versión de firmware</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>GET /api/estado</code></td><td>Últimas medidas con su timestamp</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>GET /api/config</code></td><td>Configuración vigente, sin credenciales</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>POST /api/config</code></td><td>Modifica parámetros; responde con lo que quedó</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>POST /api/reset</code></td><td>Restablece valores de fábrica; exige confirmación</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Dos reglas que evitan rehacerla</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>GET /api/config</code> <b>nunca devuelve la contraseña</b> de
\t\t\t\t\t\t\t\tla red, solo su nombre: lo contrario expone la credencial a quien
\t\t\t\t\t\t\t\testé en la misma red. Y toda escritura responde con la
\t\t\t\t\t\t\t\tconfiguración <b>resultante</b>, no con un acuse vacío, para que el
\t\t\t\t\t\t\t\tcliente sepa qué quedó guardado de verdad.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-target",
)

# ────────────────────────── 10 · provisioning de credenciales
lamina(
    "provisioning-credenciales",
    "Portal cautivo: el procedimiento de puesta en marcha · Sesión 9",
    "Provisioning por portal cautivo",
    envolver(f"""{cabecera(B, "Portal cautivo: el procedimiento de puesta en marcha", "i-plug")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tPor qué no se puede grabar la contraseña
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas credenciales de red del usuario <b>no pueden estar en el
\t\t\t\t\t\t\t\tcódigo</b> de un producto distribuido: el fabricante no las conoce,
\t\t\t\t\t\t\t\ty un binario común a todas las unidades las expondría a quien lo
\t\t\t\t\t\t\t\textraiga de cualquiera de ellas.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tPortal cautivo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tRed propia más un servidor de nombres que responde <b>su propia
\t\t\t\t\t\t\t\tdirección a toda consulta</b>. Con eso, cualquier dirección que el
\t\t\t\t\t\t\t\tteléfono intente abrir lleva al formulario, y el sistema operativo
\t\t\t\t\t\t\t\tlo detecta y lo muestra solo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">1 · Arranque sin credenciales</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Modo punto de acceso con un nombre derivado de la dirección de fabricación.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">2 · Exploración y selección</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">El dispositivo lista las redes que ve y el usuario elige la suya y escribe la contraseña.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">3 · Prueba antes de guardar</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Se intenta la conexión y solo si tiene éxito se escribe en NVS.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">4 · Reinicio en modo estación</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">El punto de acceso desaparece. Desde aquí el dispositivo vive en la red del usuario.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">El paso 3 es el que suele faltar</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tGuardar la contraseña <b>sin probarla</b> deja el dispositivo
\t\t\t\t\t\t\t\treiniciándose contra una red a la que no puede entrar, y sin portal
\t\t\t\t\t\t\t\tal que volver. Probar primero convierte un error de tecleo en un
\t\t\t\t\t\t\t\tmensaje en pantalla.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-plug",
)

# ────────────────────────────────────── 11 · La hora del código · 37
lamina(
    "codigo-37-portal-cautivo",
    "Código 37 · Portal cautivo con prueba previa · Sesión 9",
    "La hora del código · Portal cautivo",
    hora_del_codigo(
        37,
        "Portal cautivo con prueba de credenciales antes de guardarlas",
        "El procedimiento completo de puesta en marcha: sin credenciales guardadas el equipo arranca como punto "
        "de acceso con portal cautivo; con ellas, como estación. Las credenciales <b>se prueban antes de "
        "escribirse</b> y una pulsación larga las borra.",
        "Un <b>portal cautivo</b> se consigue resolviendo toda consulta de nombres a la propia dirección del "
        "equipo: el teléfono cree que no hay internet y abre solo la página de configuración. La <b>memoria no "
        "volátil</b> conserva las credenciales entre arranques. Probar antes de guardar es lo que evita el "
        "callejón sin salida: unas credenciales erróneas escritas dejan al equipo reintentando contra una red "
        "inalcanzable y <b>sin portal al que volver</b>.",
        "El <b>ESP32</b> enciende tres LED de fase en los <b>GPIO 25, 26 y 27</b> con resistencia de 220 Ω y lee "
        "un pulsador de restablecimiento en el <b>GPIO 4</b> con <code>INPUT_PULLUP</code>.",
        """[NVS]  sin credenciales guardadas -&gt; modo punto de acceso
[AP]   ssid=ESP32-A4CF12  ip=192.168.4.1  portal activo
[DNS]  toda consulta resuelta a 192.168.4.1
[POST] /guardar ssid=LAB-UNI  probando credenciales...
[PRUEBA] fallo: WL_CONNECT_FAILED -&gt; NO se guarda, avisa
[POST] /guardar ssid=LAB-UNI  probando credenciales...
[PRUEBA] exito ip=192.168.1.47 -&gt; guardadas reiniciando""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, ESPAsyncWebServer y la biblioteca Preferences.

<b>2. Firmware.</b> Al arrancar lee las credenciales de la NVS. Si no las hay, activa el modo punto de acceso con nombre <code>ESP32-XXXXXX</code> derivado de los tres últimos bytes de la MAC, levanta un servidor de nombres que resuelva toda consulta a su propia dirección y sirve un formulario con las redes visibles. Al recibirlo, <b>intenta la conexión antes de guardar</b>: solo si tiene éxito escribe en NVS y reinicia; si falla, devuelve el motivo y no guarda nada. Una pulsación de más de 5 s en el GPIO 4 borra las credenciales. Emite a 115200 baudios cada paso con su resultado.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los tres LED y el pulsador en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del arranque, con la bifurcación según haya credenciales o no. Y la <b>máquina de estados</b> del provisioning, con las rutas de fallo y el punto exacto en que se escribe en NVS.""",
        "Las dos parejas de líneas <code>[POST]</code> y <code>[PRUEBA]</code> son el ejercicio entero. En la "
        "primera, la conexión falla y <b>no se escribe nada</b>; en la segunda tiene éxito y solo entonces se "
        "guarda. Si en la traza propia apareciera el guardado antes que la prueba, un error de tecleo dejaría el "
        "equipo reiniciándose contra una red inalcanzable, sin portal al que volver: de ahí que el borrado por "
        "pulsación larga forme parte del ejercicio y no sea un extra.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="black"></wokwi-pushbutton></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="yellow"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
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

# ──────────────────────────── 12 · artículo · taxonomía del NIST
lamina(
    "paper-incorporacion-red",
    "Vocabulario común para describir un procedimiento de incorporación · Sesión 9",
    "Artículo · Incorporación a la red",
    articulo(
        "Artículo de referencia",
        "Dominio público · NIST",
        "<b>Symington, S. et al.</b> (2020). Trusted Internet of Things (IoT) Device Network-Layer Onboarding and "
        "Lifecycle Management. <i>NIST Cybersecurity White Paper</i>. "
        "<code>doi:10.6028/NIST.CSWP.09082020-draft</code>",
        "Vocabulario común para describir un procedimiento de incorporación",
        ["Dar un <b>lenguaje común</b> para describir cómo un equipo recibe sus credenciales de red.",
         "Cada fabricante resuelve el problema a su manera y <b>llama distinto a lo mismo</b>.",
         "Eso impide comparar soluciones y decidir cuál es adecuada."],
        ["Aportan una <b>taxonomía</b> que expresa las capacidades de cualquier procedimiento.",
         "Describen un <b>proceso genérico de confianza</b> con sus fases.",
         "Y un <b>ciclo de vida</b> del equipo, de la fabricación a la retirada.",
         "No es un estudio experimental: es un marco de referencia."],
        ["La incorporación es la <b>primera fase de un ciclo</b>, no un paso aislado.",
         "El ciclo incluye <b>re-incorporación, transferencia de propiedad y retirada</b>.",
         "Un procedimiento pensado solo para el primer arranque deja las otras cinco fases sin resolver."],
        [("paper-ciclo-incorporacion",
          "Elaboración propia con las fases que define el documento: la incorporación es una de seis."),
         ("paper-proceso-confianza",
          "El proceso de confianza fase por fase. La última existe porque la primera creó una relación que hay que poder deshacer.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────────────────────────── 13 · identidad del dispositivo
lamina(
    "identidad-dispositivo",
    "Identificador derivado de la dirección de fabricación · Sesión 9",
    "Identidad del dispositivo",
    envolver(f"""{cabecera(B, "Identificador derivado de la dirección de fabricación", "i-chip")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tUn único origen
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>dirección MAC</b> viene grabada de fábrica y es única. De
\t\t\t\t\t\t\t\tella se derivan, sin que nadie tenga que asignarlos, el nombre de
\t\t\t\t\t\t\t\tla red de configuración, el nombre local, el identificador de
\t\t\t\t\t\t\t\tcliente del broker y el número de serie visible.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Por qué importa que sea uno solo</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCon un origen único, dos unidades <b>nunca coinciden</b> sin que
\t\t\t\t\t\t\t\thaya que programar cada una con un número distinto en fábrica. Es
\t\t\t\t\t\t\t\tlo que evita el fallo de identificador duplicado de la sesión 8, y
\t\t\t\t\t\t\t\thace que la etiqueta impresa y lo que el dispositivo publica digan
\t\t\t\t\t\t\t\tlo mismo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEmparejamiento por código QR
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl código impreso en la etiqueta lleva el nombre de la red de
\t\t\t\t\t\t\t\tconfiguración y su clave. El usuario lo escanea y el teléfono se une
\t\t\t\t\t\t\t\tal punto de acceso sin teclear nada: es lo que hace el
\t\t\t\t\t\t\t\tprovisioning accesible a quien no sabe qué es un SSID.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">MAC · 24:6F:28:A4:CF:12</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Grabada en fabricación. Los tres primeros bytes identifican al fabricante.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓ últimos tres bytes</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__body">
\t\t\t\t\t\t\t\t\tRed de configuración: <code>ESP32-A4CF12</code><br />
\t\t\t\t\t\t\t\t\tNombre local: <code>esp32-a4cf12.local</code><br />
\t\t\t\t\t\t\t\t\tCliente del broker: <code>esp01-a4cf12</code><br />
\t\t\t\t\t\t\t\t\tNúmero de serie impreso: <code>A4CF12</code>
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[ID] mac=24:6F:28:A4:CF:12
[ID] ap_ssid=ESP32-A4CF12  host=esp32-a4cf12  cliente=esp01-a4cf12
[ID] serie impreso en la etiqueta: A4CF12</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-chip",
)

# ────────────────── 14 · artículo · identidad y provisioning a escala
lamina(
    "paper-identidad-a-escala",
    "Provisión de identidad cuando el parque deja de configurarse a mano · Sesión 9",
    "Artículo · Identidad a escala",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Sousa, P. R.; Magalhães, L.; Resende, J. S. et al.</b> (2021). Provisioning, Authentication and "
        "Secure Communications for IoT Devices on FIWARE. <i>Sensors</i> 21(17), 5898. "
        "<code>doi:10.3390/s21175898</code>",
        "Provisión de identidad cuando el parque deja de configurarse a mano",
        ["Resolver cómo se dota de <b>identidad verificable</b> a un parque grande de equipos.",
         "La gestión de identidad es el <b>vector de ataque predominante</b>: permite suplantar.",
         "Toda medida de seguridad posterior descansa sobre ella."],
        ["Analizan la provisión de <b>certificados digitales</b> y su entrega a escala.",
         "El proceso tiene tres piezas: configuración del equipo, identidad y claves.",
         "El procedimiento habitual es <b>laborioso y depende de configuración manual</b>.",
         "Esa dependencia es la que <b>no admite crecimiento</b>."],
        ["La provisión de certificados a escala sigue siendo un <b>problema abierto</b>.",
         "Lo que funciona para un prototipo <b>no sirve para un parque</b>.",
         "El cuello de botella no es criptográfico: es de procedimiento."],
        [("paper-provision-escala",
          "Cálculo propio con el ritmo declarado en la leyenda, no medidas del artículo: pone cifra a la conclusión."),
         ("paper-identidad-piezas",
          "Las tres piezas del proceso, con las dos que siguen dependiendo de intervención manual marcadas.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ───────────────────────────── 15 · etiqueta y requisitos del producto
lamina(
    "etiqueta-producto",
    "Contenido obligado de la etiqueta de un producto · Sesión 9",
    "Etiqueta del producto",
    envolver(f"""{cabecera(B, "Contenido obligado de la etiqueta de un producto", "i-file")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué lleva y por qué
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa etiqueta es la única información disponible cuando el equipo no
\t\t\t\t\t\t\t\tarranca. Todo lo que haga falta para diagnosticar, reponer o dar de
\t\t\t\t\t\t\t\tbaja la unidad tiene que estar impreso en ella.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tLa versión de firmware también va impresa
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tParece redundante porque el dispositivo la publica en
\t\t\t\t\t\t\t\t<code>/api/info</code>, pero un equipo que no arranca no publica
\t\t\t\t\t\t\t\tnada. La impresa es la de fábrica; la publicada, la vigente tras las
\t\t\t\t\t\t\t\tactualizaciones. Que difieran es un dato de diagnóstico, no un
\t\t\t\t\t\t\t\terror.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Dato</th><th>Para qué sirve</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>Modelo</b></td><td>Identifica de qué producto se trata y qué documentación aplica</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Número de serie</b></td><td>Identifica la unidad concreta ante el servicio técnico</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Dirección MAC</b></td><td>Permite localizar el equipo en la red sin encenderlo</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Tensión y corriente</b></td><td>Evita alimentarlo con una fuente inadecuada</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Versión de hardware</b></td><td>Distingue revisiones con distinto comportamiento</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Versión de firmware</b></td><td>La de fábrica, como punto de partida del historial</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Código QR</b></td><td>Emparejamiento sin teclear el nombre de la red ni su clave</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-file",
)

# ──────────────── 16 · artículo · etiquetado de seguridad y decisión de compra
lamina(
    "paper-etiquetado-seguridad",
    "Efecto de una etiqueta de seguridad sobre la elección de compra · Sesión 9",
    "Artículo · Etiquetado de seguridad",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Johnson, S. D.; Blythe, J. M.; Manning, M.; Wong, G. T. W.</b> (2020). The impact of IoT security "
        "labelling on consumer product choice and willingness to pay. <i>PLOS ONE</i> 15(1), e0227800. "
        "<code>doi:10.1371/journal.pone.0227800</code>",
        "Efecto de una etiqueta de seguridad sobre la elección de compra",
        ["Ver si informar de la seguridad en la etiqueta <b>cambia lo que la gente compra</b>.",
         "La seguridad de un producto conectado <b>no es observable antes de comprarlo</b>.",
         "Estudio con participantes ante equipos que difieren en funcionalidad, precio y etiqueta."],
        ["Los equipos <b>con etiqueta</b> se eligieron con mayor frecuencia que los que no la llevaban.",
         "Con <b>una sola excepción</b>: la etiqueta que sugería seguridad deficiente.",
         "En dos de las etiquetas, la disposición a pagar por seguridad <b>igualó a la de más funcionalidad</b>.",
         "Se recogieron además las razones que los participantes daban."],
        ["Declarar una protección pobre <b>penaliza más que guardar silencio</b>.",
         "La etiqueta funciona porque traslada al lado observable algo que no lo era.",
         "Sin señal visible, el mercado no puede premiar la seguridad."],
        [("paper-etiqueta-observable",
          "Elaboración propia. El mecanismo que explica el resultado: la seguridad es el único atributo que no se juzga antes de comprar."),
         ("paper-etiqueta-efecto",
          "Sentido del efecto de cada etiqueta ensayada, con la única excepción marcada. El estudio no publica porcentajes.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ───────────────────────── 17 · restablecimiento de valores de fábrica
lamina(
    "restablecimiento-fabrica",
    "Restablecimiento de valores de fábrica y cambio de propietario · Sesión 9",
    "Factory reset",
    envolver(f"""{cabecera(B, "Restablecimiento de valores de fábrica y cambio de propietario", "i-alert")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué se borra y qué no
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe borra <b>todo lo que identifica al usuario</b>: credenciales de
\t\t\t\t\t\t\t\tred, claves de servicio, configuración y datos acumulados. No se
\t\t\t\t\t\t\t\tborra lo que identifica al equipo (dirección de fabricación, modelo,
\t\t\t\t\t\t\t\tnúmero de serie), que no le pertenece a nadie.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Por qué exige un gesto deliberado</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna pulsación larga con confirmación, no un botón accesible. La
\t\t\t\t\t\t\t\toperación es <b>irreversible</b> y deja el equipo sin conexión: si
\t\t\t\t\t\t\t\tocurre por accidente en una instalación remota, hay que desplazarse
\t\t\t\t\t\t\t\ta reconfigurarlo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tBorrar la clave de la NVS (memoria no volátil) <b>no borra sus restos</b>
\t\t\t\t\t\t\t\tde la Flash: la escritura marca la entrada como no válida, pero los
\t\t\t\t\t\t\t\tbytes siguen ahí hasta que el sector se reescriba. En un producto
\t\t\t\t\t\t\t\tque cambia de dueño eso importa, y es una de las razones del cifrado
\t\t\t\t\t\t\t\tde la memoria que trata la sesión 10.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[RESET] pulsacion larga detectada (5.2 s)
[RESET] confirmacion requerida: mantener 3 s mas
[RESET] borrando: credenciales_red, token_api, config_usuario
[RESET] conservando: mac, modelo, serie, version_hw
[RESET] reiniciando en modo punto de acceso</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa traza distingue de forma explícita lo borrado de lo conservado: es
\t\t\t\t\t\t\tlo que permite auditar que el equipo quedó realmente limpio.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-alert",
)

# ────────────────────────────────────── 18 · La hora del código · 38
lamina(
    "codigo-38-api-y-descubrimiento",
    "Código 38 · API del dispositivo con nombre local · Sesión 9",
    "La hora del código · API y descubrimiento",
    hora_del_codigo(
        38,
        "API del dispositivo con nombre local y factory reset",
        "Publicar la API completa de la lámina anterior y hacer al equipo localizable por nombre. La lectura de "
        "configuración <b>nunca devuelve la contraseña</b>, toda escritura responde con la configuración "
        "resultante, y el restablecimiento exige confirmación explícita.",
        "Un <b>punto de acceso</b> de la API es un método más una ruta; el método dice si la operación lee o "
        "escribe. Responder con la <b>configuración resultante</b> en lugar de con un acuse vacío ahorra una "
        "segunda petición y elimina la duda de qué quedó guardado. El código <b>409</b> significa que la petición "
        "es válida pero choca con el estado actual: aquí se usa para exigir confirmación antes de una operación "
        "que no se puede deshacer.",
        "El <b>ESP32</b> lee un pulsador de restablecimiento en el <b>GPIO 4</b> con <code>INPUT_PULLUP</code> y "
        "enciende un LED de confirmación en el <b>GPIO 25</b> con resistencia de 220 Ω, que parpadea durante la "
        "cuenta atrás.",
        """[MDNS] publicado esp32-a4cf12.local http/tcp puerto 80
[HTTP] GET  /api/info    200  modelo=UNI-01 serie=A4CF12 fw=1.2.0
[HTTP] GET  /api/config  200  ssid=LAB-UNI  (sin contrasena)
[HTTP] POST /api/config  200  devuelve la configuracion resultante
[HTTP] POST /api/reset   409  falta confirmacion explicita
[HTTP] POST /api/reset   200  confirmado=si borrando datos""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, ESPAsyncWebServer, ArduinoJson y Preferences.

<b>2. Firmware.</b> Publica el nombre local con mDNS y anuncia el servicio HTTP. Implementa <code>GET /api/info</code>, <code>GET /api/estado</code>, <code>GET /api/config</code>, <code>POST /api/config</code> y <code>POST /api/reset</code>. La lectura de configuración devuelve el nombre de la red pero <b>nunca la contraseña</b>. Toda escritura responde con la configuración resultante, no con un acuse vacío. El restablecimiento responde 409 si la petición no lleva confirmación explícita, y al ejecutarse registra por separado qué borra y qué conserva. Emite a 115200 baudios cada petición con su código.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el pulsador en el GPIO 4 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del restablecimiento, con la comprobación de la confirmación y la separación entre lo que se borra y lo que se conserva. Y la <b>tabla de la API</b>, una fila por punto de acceso: método, ruta, qué devuelve y si modifica el dispositivo.""",
        "Las dos líneas de <code>/api/reset</code>: la primera responde <b>409</b> y no borra nada. Esa negativa "
        "es lo que impide que una petición repetida o perdida deje el equipo en blanco, y es la idempotencia de "
        "la sesión 8 aplicada a algo que no se puede deshacer. Mirar además la línea de "
        "<code>GET /api/config</code>: si en la traza propia apareciera la contraseña, cualquiera dentro de la "
        "red la tendría con una sola petición.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="red"></wokwi-pushbutton></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
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

# ────────────────────────────────────── 19 · La hora del código · 39
lamina(
    "codigo-39-producto-completo",
    "Código 39 · Dispositivo completo listo para entregar · Sesión 9",
    "La hora del código · Producto completo",
    hora_del_codigo(
        39,
        "Dispositivo completo: provisioning, panel, API e identidad",
        "Integrar la sesión entera en un equipo que <b>una persona sin conocimientos técnicos</b> pueda poner en "
        "marcha: escanea el código, elige su red, escribe la contraseña y ve el panel. Sin manual y sin tocar el "
        "código.",
        "La <b>identidad</b> del equipo se deriva de la dirección de fabricación: número de serie y nombre local "
        "salen de ella, así que dos unidades nunca chocan. El <b>reset reason</b> la conserva el SoC "
        "y distingue un corte de alimentación de un fallo del firmware; cuesta una línea y es el primer dato que "
        "se consulta ante una avería. El <b>ritmo del LED</b> es la única interfaz cuando aún no hay red: cada "
        "fase necesita el suyo.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b>, controla un LED en el <b>GPIO 25</b>, indica "
        "el estado con otro en el <b>GPIO 26</b> y lee el pulsador de restablecimiento en el <b>GPIO 4</b>.",
        """[BOOT] fw=1.2.0  serie=A4CF12  causa_reinicio=POWERON
[NVS]  credenciales presentes -&gt; modo estacion
[RED]  conectado ip=192.168.1.47  rssi=-58 dBm
[MDNS] esp32-a4cf12.local publicado
[HTTP] servidor listo interfaz desde LittleFS (3 archivos)
[HTTP] GET /  200  primer visitante memoria libre=196880
[API]  GET /api/estado  200  v=1.842  desde el movil""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, ESPAsyncWebServer, ArduinoJson y Preferences.

<b>2. Firmware.</b> Reúne los ejemplos 36 a 38 en un solo proyecto: provisioning por portal cautivo con prueba previa, panel servido desde LittleFS, API con los cinco puntos de acceso, nombre local por mDNS, identidad derivada de la dirección de fabricación y restablecimiento con confirmación. El LED de estado codifica la fase con un ritmo distinto para sin configurar, conectando y conectado. Registra al arrancar la versión, el número de serie y el reset reason.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los cuatro componentes en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del arranque completo, desde la lectura de la NVS hasta el servidor en marcha. Y el <b>recorrido del usuario</b> desde que abre la caja hasta que ve el primer dato, marcando en cada paso qué hace el equipo y qué ve la persona.""",
        "La primera línea vale por sí sola: <b>versión, serie y causa del reinicio</b>. Cuando alguien devuelva "
        "una unidad, es lo único que habrá para empezar. Recorrer después la traza como si fuera el usuario: "
        "entre <code>[BOOT]</code> y el primer <code>GET /</code> no debería hacer falta explicar nada. Si algún "
        "paso necesitara una instrucción escrita, está mal resuelto.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="black"></wokwi-pushbutton></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/potentiometer-element.js";
\t\t\timport "@wokwi/elements/dist/esm/pushbutton-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
""",
)

# ─────────────────────────────────────── 20 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes con el servidor y el provisioning · Sesión 9",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes con el servidor y el provisioning", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("La página se carga a medias", "El panel aparece sin estilos o sin datos, y recargando a veces se arregla.", "Se agotó el límite de sockets simultáneos: cada archivo de la interfaz consume una conexión y varios visitantes las multiplican.", "Contar los recursos de la página y multiplicarlos por los visitantes. Reunirlos en un solo archivo comprimido y volver a probar.", "i-link")}
{problema("El servidor responde 404 a todo", "El firmware arranca bien y el servidor está en marcha, pero ninguna ruta estática funciona.", "Se grabó el firmware pero no el sistema de archivos: son dos particiones y dos operaciones distintas.", "Imprimir al arrancar cuántos archivos ve LittleFS. Si son cero, falta subir el sistema de archivos.", "i-folder")}
{problema("El teléfono se desconecta al guardar", "Durante el provisioning, el móvil pierde el punto de acceso justo al enviar las credenciales.", "En modo combinado, al asociarse como estación el punto de acceso propio salta al canal de esa red y los clientes conectados pierden el enlace.", "Confirmar la conexión antes de responder al formulario, o mostrar el resultado en la propia página antes de cambiar de modo.", "i-wave")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("El dispositivo queda inaccesible tras configurarlo", "Se guarda una contraseña equivocada y el equipo ya no ofrece el portal ni entra en la red.", "Las credenciales se escribieron sin probarlas: con credenciales guardadas el dispositivo arranca en modo estación y el portal ya no aparece.", "Probar la conexión antes de escribir en NVS. Mientras tanto, la salida es el restablecimiento por pulsación larga.", "i-plug")}
{problema("El panel deja de responder tras un rato", "Con el panel abierto un tiempo largo, las actualizaciones se detienen sin ningún error visible.", "Las conexiones mantenidas de pestañas cerradas sin despedirse siguen ocupando socket hasta que vence el plazo de la pila.", "Registrar el número de conexiones abiertas y cerrar las inactivas por plazo desde el propio firmware.", "i-clock")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 21 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 9 · Sesión 9",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("Punto de acceso", "access point", "Modo en que el dispositivo crea su propia red y reparte direcciones, sin depender de ninguna red existente.")}
{termino("Portal cautivo", "captive portal", "Red propia más un servidor de nombres que responde su propia dirección a toda consulta, de modo que cualquier página abre el formulario de configuración.")}
{termino("Servidor asíncrono", "asynchronous server", "Servidor que atiende en su propia tarea y llama a los manejadores por suceso. El manejador no debe bloquear, igual que una rutina de interrupción.")}
{termino("Ruta", "route", "Asociación de un método y un camino a un manejador. Es la unidad con la que se construye la API del dispositivo.")}
{termino("mDNS", "multicast DNS", "Publicación de un nombre resoluble dentro de la red local sin servidor de nombres. Sustituye a una dirección que cambia.")}
{termino("Server-Sent Events (SSE)", "eventos enviados por el servidor", "Conexión mantenida en un solo sentido por la que el dispositivo envía actualizaciones cuando las hay.")}
{termino("WebSocket", "", "Conexión mantenida bidireccional. Permite que el panel también mande órdenes, a costa de un socket por visitante.")}
{termino("Provisioning", "aprovisionamiento", "Procedimiento por el que el dispositivo recibe las credenciales de la red del usuario, que no pueden venir en el firmware.")}
{termino("NVS", "memoria no volátil", "Región donde se conservan las credenciales y la configuración entre reinicios. Se trata en profundidad en la sesión 10.")}
{termino("Factory reset", "restablecimiento de fábrica", "Borrado de todo lo que identifica al usuario, conservando lo que identifica al equipo. Es lo que permite el cambio de propietario.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 22 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 9 · Sesión 9",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-link")}Servidor embebido</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tComo servidor, el dispositivo no decide cuántas conexiones recibe.
\t\t\t\t\t\t\tReducir el número de archivos de la interfaz vale más que reducir su
\t\t\t\t\t\t\ttamaño: cada archivo cuesta un socket.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa interfaz vive en el sistema de archivos, no en el binario, y sin
\t\t\t\t\t\t\tninguna dependencia externa: durante el provisioning no hay
\t\t\t\t\t\t\tinternet.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-target")}Producto</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLas credenciales se <b>prueban antes de guardarse</b>. Sin esa
\t\t\t\t\t\t\tcomprobación, un error de tecleo deja el equipo sin portal al que
\t\t\t\t\t\t\tvolver.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUn solo origen de identidad, la dirección de fabricación, da nombre
\t\t\t\t\t\t\tde red, nombre local, identificador de cliente y número de serie sin
\t\t\t\t\t\t\tprovisionar nada.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a las sesiones siguientes</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-folder")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">NVS y sistema de archivos</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tAquí se han usado por primera vez; la sesión 10 los trata con su
\t\t\t\t\t\t\t\ttabla de particiones y su desgaste.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">El reset reason</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tCuesta una línea y es el primer dato de diagnóstico. La sesión 10 la
\t\t\t\t\t\t\t\thace obligatoria.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-robot")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">La API como interfaz para un agente</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLos puntos de acceso publicados aquí son lo que un agente consume en
\t\t\t\t\t\t\t\tla sesión 11.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 23 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 9 · Sesión 9",
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
\t\t\t\t\t\t\t\t<span class="ref__title">Trusted IoT Device Network-Layer Onboarding and Lifecycle Management</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Symington, S. et al. (2020). <i>NIST Cybersecurity White Paper</i>, borrador. Dominio público.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.6028/NIST.CSWP.09082020-draft</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Provisioning · Ciclo de vida</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Provisioning, Authentication and Secure Communications for IoT Devices on FIWARE</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Sousa, P. R.; Magalhães, L.; Resende, J. S. et al. (2021). <i>Sensors</i> 21(17), 5898. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3390/s21175898</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Identidad del dispositivo · Escala</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">The impact of IoT security labelling on consumer product choice and willingness to pay</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Johnson, S. D.; Blythe, J. M.; Manning, M.; Wong, G. T. W. (2020). <i>PLOS ONE</i> 15(1), e0227800. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1371/journal.pone.0227800</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Etiqueta del producto</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-09/</code>, junto a dos más sobre provisioning federado y un sistema completo con ESP32. El índice, en <code>src/paper/INDICE.md</code>.</span>
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
        {"clase": "clase-09", "sesion": "Sesión 9", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
