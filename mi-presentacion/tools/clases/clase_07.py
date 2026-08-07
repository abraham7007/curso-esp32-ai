#!/usr/bin/env python3
"""Sesión 7 — Redes TCP/IP y protocolo HTTP. El ESP32 como cliente.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_07.py
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

A = "01 · Fundamentos de red"
B = "02 · Protocolo HTTP y APIs REST"

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
    "Sesión 7 · Redes TCP/IP y protocolo HTTP",
    "Redes TCP/IP y protocolo HTTP",
    portada(
        "Sesión 7",
        "Redes TCP/IP y<br />protocolo HTTP",
        "Direccionamiento, transporte e interfaz inalámbrica.",
        "El ESP32 en el papel de cliente.",
        [
         ("i-layers", "Direccionamiento: IP, MAC, DHCP y DNS"),
         ("i-flow", "TCP frente a UDP"),
         ("i-link", "Conexión con backoff exponencial"),
         ("i-alert", "API REST: métodos y códigos"),
        ],
        "02-modelo-capas.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ────────────────────────────────────────────────── 02 · modelo de capas
lamina(
    "modelo-capas",
    "Las cuatro capas recorridas por una sola lectura · Sesión 7",
    "Las cuatro capas de la pila",
    envolver(f"""{cabecera(A, "Las cuatro capas recorridas por una sola lectura", "i-layers")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Cada capa envuelve a la anterior y añade su cabecera.</strong>
\t\t\t\t\tSeguimos un dato de 12 bytes desde el programa hasta la antena.
\t\t\t\t</p>

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Aplicación · HTTP</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Qué significa el dato. <code>POST /medidas</code> con el cuerpo en JSON.</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">+ unos 180 bytes de cabeceras</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Transporte · TCP</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">A qué programa del anfitrión va, y con qué garantía de entrega y de orden.</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">+ 20 bytes · puertos origen y destino</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Red · IP</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">A qué equipo de qué red. Es la capa que permite atravesar routers.</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">+ 20 bytes · direcciones origen y destino</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Enlace · WiFi 802.11</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">A qué equipo del mismo tramo físico. Direcciones MAC y acceso al medio.</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">+ unos 34 bytes · cifrado del enlace</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="capas-sobrecarga"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\tLa cabecera de HTTP pesa quince veces más que el dato que
\t\t\t\t\t\t\t\ttransporta; las tres capas inferiores juntas, algo menos que ella
\t\t\t\t\t\t\t\tsola.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Consecuencia práctica</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEnviar 12 bytes cuesta unos 266. Con una publicación por segundo
\t\t\t\t\t\t\t\tson <b>23 MB al mes</b> de los que solo 1 MB es dato. Esa relación
\t\t\t\t\t\t\t\tes la que motiva el protocolo de la sesión 8, cuya cabecera mínima
\t\t\t\t\t\t\t\tson <b>2 bytes</b> frente a los 192 de HTTP.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ─────────────────────────── 02b · simulación del rendimiento útil
lamina(
    "simulacion-sobrecarga",
    "Rendimiento útil según el tamaño de la carga · Sesión 7",
    "Rendimiento útil de la transmisión",
    envolver(f"""{cabecera(A, "Rendimiento útil según el tamaño de la carga", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué se compara
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas cabeceras de transporte, red y enlace son las mismas en ambos
\t\t\t\t\t\t\t\tcasos: <b>74 bytes</b>. Lo que cambia es la capa de aplicación,
\t\t\t\t\t\t\t\tunos 192 bytes en HTTP frente a 2 en el protocolo de la sesión 8.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCon cargas pequeñas, las de un sensor, el protocolo pesa mucho más
\t\t\t\t\t\t\t\tque el dato y la diferencia entre ambos es de un orden de magnitud.
\t\t\t\t\t\t\t\tPor encima de unos 500 bytes las dos curvas convergen: ahí la
\t\t\t\t\t\t\t\telección del protocolo deja de decidirse por la sobrecarga.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="ovh-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Dos barras apiladas que comparan el reparto entre dato útil y cabeceras de protocolo para HTTP y para una conexión mantenida, según el tamaño de la carga"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<label for="ovh-carga" class="text-sm font-medium">
\t\t\t\t\t\t\t\t\tDato útil por mensaje
\t\t\t\t\t\t\t\t</label>
\t\t\t\t\t\t\t\t<input type="range" id="ovh-carga" min="4" max="600" step="4" value="12" />
\t\t\t\t\t\t\t\t<span class="readout" id="ovh-carga-lectura">12 bytes</span>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item metric__item--bad">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">HTTP · útil</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="ovh-http">4,5 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item metric__item--ok">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Conexión mantenida · útil</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="ovh-mqtt">14 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Al día, uno por segundo</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="ovh-dia">23 MB</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Ahorro del segundo</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="ovh-ahorro">×3,1</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Cifras de la lámina anterior: TCP 20 + IP 20 + enlace 34 = 74 bytes
\t\t\t// comunes, y la capa de aplicación que distingue a los dos casos.
\t\t\tconst COMUN = 74;
\t\t\tconst APP = { http: 192, mantenida: 2 };

\t\t\tconst lienzo = document.getElementById("ovh-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst deslizador = document.getElementById("ovh-carga");
\t\t\tconst lectura = document.getElementById("ovh-carga-lectura");
\t\t\tconst salHttp = document.getElementById("ovh-http");
\t\t\tconst salMqtt = document.getElementById("ovh-mqtt");
\t\t\tconst salDia = document.getElementById("ovh-dia");
\t\t\tconst salAhorro = document.getElementById("ovh-ahorro");

\t\t\tfunction variable(nombre) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();
\t\t\t}

\t\t\tfunction coma(n, dec) {
\t\t\t\treturn n.toFixed(dec).replace(".", ",");
\t\t\t}

\t\t\tfunction dibujar(carga) {
\t\t\t\tconst w = lienzo.width;
\t\t\t\tconst h = lienzo.height;
\t\t\t\tctx.clearRect(0, 0, w, h);

\t\t\t\tconst filas = [
\t\t\t\t\t{ rotulo: "HTTP", app: APP.http, y: 96 },
\t\t\t\t\t{ rotulo: "Conexión mantenida", app: APP.mantenida, y: 216 },
\t\t\t\t];
\t\t\t\tconst maximo = carga + COMUN + APP.http;
\t\t\t\tconst izq = 210;
\t\t\t\tconst ancho = w - izq - 30;
\t\t\t\tconst alto = 54;

\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst texto = variable("--color-text");
\t\t\t\tconst ok = variable("--color-ok");
\t\t\t\tconst acento = variable("--color-accent");
\t\t\t\tconst navy = variable("--color-navy");

\t\t\t\tfor (const fila of filas) {
\t\t\t\t\tconst total = carga + COMUN + fila.app;
\t\t\t\t\tconst px = (v) => (v / maximo) * ancho;

\t\t\t\t\tlet x = izq;
\t\t\t\t\tconst tramos = [
\t\t\t\t\t\t{ v: carga, color: ok, nombre: "dato" },
\t\t\t\t\t\t{ v: fila.app, color: acento, nombre: "aplicación" },
\t\t\t\t\t\t{ v: COMUN, color: navy, nombre: "TCP + IP + enlace" },
\t\t\t\t\t];
\t\t\t\t\tfor (const tramo of tramos) {
\t\t\t\t\t\tconst dx = px(tramo.v);
\t\t\t\t\t\tctx.fillStyle = tramo.color;
\t\t\t\t\t\tctx.fillRect(x, fila.y, dx, alto);
\t\t\t\t\t\tif (dx > 42) {
\t\t\t\t\t\t\tctx.fillStyle = variable("--color-surface");
\t\t\t\t\t\t\tctx.font = "11px ui-monospace, monospace";
\t\t\t\t\t\t\tctx.textAlign = "center";
\t\t\t\t\t\t\tctx.fillText(String(tramo.v), x + dx / 2, fila.y + alto / 2 + 4);
\t\t\t\t\t\t}
\t\t\t\t\t\tx += dx;
\t\t\t\t\t}

\t\t\t\t\tctx.fillStyle = texto;
\t\t\t\t\tctx.font = "600 13px system-ui";
\t\t\t\t\tctx.textAlign = "right";
\t\t\t\t\tctx.fillText(fila.rotulo, izq - 14, fila.y + alto / 2 - 2);
\t\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\t\tctx.font = "11px ui-monospace, monospace";
\t\t\t\t\tctx.fillText(`${total} bytes`, izq - 14, fila.y + alto / 2 + 15);

\t\t\t\t\tctx.fillStyle = carga / total > 0.3 ? ok : acento;
\t\t\t\t\tctx.font = "600 13px ui-monospace, monospace";
\t\t\t\t\tctx.textAlign = "left";
\t\t\t\t\tctx.fillText(`${coma((carga / total) * 100, 1)} % útil`, izq + px(total) + 10, fila.y + alto / 2 + 4);
\t\t\t\t}

\t\t\t\t// Leyenda
\t\t\t\tconst leyenda = [
\t\t\t\t\t["dato útil", ok],
\t\t\t\t\t["cabecera de aplicación", acento],
\t\t\t\t\t["TCP + IP + enlace", navy],
\t\t\t\t];
\t\t\t\tlet lx = izq;
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.textAlign = "left";
\t\t\t\tfor (const [nombre, color] of leyenda) {
\t\t\t\t\tctx.fillStyle = color;
\t\t\t\t\tctx.fillRect(lx, 36, 11, 11);
\t\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\t\tctx.fillText(nombre, lx + 17, 45);
\t\t\t\t\tlx += ctx.measureText(nombre).width + 46;
\t\t\t\t}
\t\t\t}

\t\t\tfunction actualizar() {
\t\t\t\tconst carga = Number(deslizador.value);
\t\t\t\tlectura.textContent = `${carga} bytes`;
\t\t\t\tdibujar(carga);

\t\t\t\tconst totalHttp = carga + COMUN + APP.http;
\t\t\t\tconst totalMant = carga + COMUN + APP.mantenida;
\t\t\t\tsalHttp.textContent = `${coma((carga / totalHttp) * 100, 1)} %`;
\t\t\t\tsalMqtt.textContent = `${coma((carga / totalMant) * 100, 1)} %`;
\t\t\t\tsalDia.textContent = `${coma((totalHttp * 86400) / 1e6, 1)} MB`;
\t\t\t\tsalAhorro.textContent = `×${coma(totalHttp / totalMant, 1)}`;
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

# ─────────────────────────────────── 03 · cliente, servidor, puerto, socket
lamina(
    "cliente-servidor-socket",
    "Cliente, servidor, puerto y socket · Sesión 7",
    "Cliente, servidor, puerto y socket",
    envolver(f"""{cabecera(A, "Cliente, servidor, puerto y socket", "i-link")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-book")}Cliente y servidor</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tNo son tipos de equipo sino <b>papeles en una conexión</b>. El
\t\t\t\t\t\t\tcliente toma la iniciativa; el servidor permanece a la escucha y
\t\t\t\t\t\t\tresponde.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tEl mismo ESP32 es cliente en esta sesión y servidor en la 9.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-plug")}Puerto</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tNúmero de 16 bits que identifica <b>qué programa</b> del equipo
\t\t\t\t\t\t\tatiende la conexión. La dirección IP llega al equipo; el puerto,
\t\t\t\t\t\t\tal programa.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t80 para HTTP, 443 para HTTPS, 1883 para MQTT sin cifrar.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-target")}Socket</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tExtremo de una conexión, identificado por el par <b>dirección IP más
\t\t\t\t\t\t\tpuerto</b>. Una conexión queda determinada por sus dos sockets.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>192.168.1.47:52310 ⇄ 104.18.2.15:443</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\tEn el código
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tEl puerto de origen del cliente lo asigna la pila de red de forma
\t\t\t\t\t\tautomática y cambia en cada conexión; solo se indica el del servidor.
\t\t\t\t\t\tPor eso <code>http.begin("http://api.ejemplo.com/v1/datos")</code> no
\t\t\t\t\t\tmenciona ningún puerto: el 80 va implícito en el esquema
\t\t\t\t\t\t<code>http</code>, y el 443 en <code>https</code>.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Aplicaciones habituales</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-terminal")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Dos servicios en el mismo equipo</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tUn servidor doméstico ofrece la interfaz web en el 80 y el broker
\t\t\t\t\t\t\t\tMQTT en el 1883, con una sola dirección IP.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Puerto cerrado por el cortafuegos</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tUna red institucional que solo permite el 443 impide MQTT en su
\t\t\t\t\t\t\t\tpuerto habitual; la solución es el mismo protocolo sobre 443.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Varias conexiones simultáneas</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tEl ESP32 puede tener abiertas la petición HTTP y la conexión al
\t\t\t\t\t\t\t\tbroker: se distinguen por su puerto de origen.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-link",
)

# ─────────────────────────────────────────────── 04 · direccionamiento
lamina(
    "direccionamiento",
    "Direcciones MAC e IP y los servicios que las reparten · Sesión 7",
    "Direccionamiento y servicios de red",
    envolver(f"""{cabecera(A, "Direcciones MAC e IP y los servicios que las reparten", "i-chip")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Dirección MAC</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSeis bytes grabados en fabricación. Identifica al equipo <b>dentro
\t\t\t\t\t\t\tde su tramo físico</b> y no cambia al mudar de red.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tEn el ESP32 se lee con <code>WiFi.macAddress()</code>. Los tres
\t\t\t\t\t\t\tprimeros bytes identifican al fabricante, y por eso sirve de
\t\t\t\t\t\t\tidentificador único del dispositivo, uso que retoma la sesión 9.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Dirección IP</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCuatro bytes asignados <b>por la red</b> en que se entra. Cambia al
\t\t\t\t\t\t\tconectarse a otra red, y puede cambiar dentro de la misma.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tSe lee con <code>WiFi.localIP()</code>. Por eso un dispositivo no
\t\t\t\t\t\t\tpuede darse a conocer por su IP: la resolución por nombre local es
\t\t\t\t\t\t\tel mecanismo que lo sustituye.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Elemento</th><th>Qué resuelve</th><th>Valor habitual en una red doméstica</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr><td><b>DHCP</b></td><td>Reparte direcciones IP a los equipos que entran</td><td>Lo ejecuta el router; concede la dirección por un plazo</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Máscara de subred</b></td><td>Separa qué parte de la IP identifica la red y qué parte el equipo</td><td><code>255.255.255.0</code>: 254 equipos posibles</td></tr>
\t\t\t\t\t\t\t<tr><td><b>Puerta de enlace</b></td><td>Equipo al que se envía todo lo que no pertenece a la red local</td><td><code>192.168.1.1</code>, el propio router</td></tr>
\t\t\t\t\t\t\t<tr><td><b>DNS</b></td><td>Traduce un nombre a una dirección IP</td><td>El router, o un servicio público como <code>8.8.8.8</code></td></tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Direcciones privadas y públicas</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tLos rangos <code>192.168.x.x</code>, <code>10.x.x.x</code> y
\t\t\t\t\t\t<code>172.16-31.x.x</code> son <b>privados</b>: se repiten en millones
\t\t\t\t\t\tde redes y ningún router de internet los encamina. Una dirección
\t\t\t\t\t\tpública es única en todo internet. Que el ESP32 tenga una privada es lo
\t\t\t\t\t\tque explica la pregunta de apertura, y lo resuelve la lámina siguiente.
\t\t\t\t\t</p>
\t\t\t\t</div>"""),
    icono="i-chip",
)

# ────────────────────────────────────────────────────────── 05 · NAT
lamina(
    "traduccion-direcciones",
    "Traducción de direcciones y su efecto sobre la arquitectura · Sesión 7",
    "Traducción de direcciones (NAT)",
    envolver(f"""{cabecera(A, "Traducción de direcciones y su efecto sobre la arquitectura", "i-flow")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>traducción de direcciones de red</b> (NAT) sustituye, en cada
\t\t\t\t\t\t\t\tpaquete que sale, la dirección privada de origen por la pública del
\t\t\t\t\t\t\t\trouter, y anota la correspondencia en una tabla para saber a quién
\t\t\t\t\t\t\t\tentregar la respuesta.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Respuesta a la pregunta de apertura</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa entrada en esa tabla <b>solo la crea un paquete de salida</b>. Un
\t\t\t\t\t\t\t\tpaquete que llega desde internet sin corresponder a ninguna
\t\t\t\t\t\t\t\tconexión iniciada dentro no tiene destinatario y se descarta. Por
\t\t\t\t\t\t\t\teso el dispositivo alcanza al exterior pero el exterior no lo
\t\t\t\t\t\t\t\talcanza a él.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tConsecuencia sobre la arquitectura
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn servidor en la nube no puede iniciar una conexión hacia el
\t\t\t\t\t\t\t\tdispositivo. Las arquitecturas de IoT resuelven esto de dos formas:
\t\t\t\t\t\t\t\tel dispositivo <b>consulta de forma periódica</b> (lo que hace HTTP
\t\t\t\t\t\t\t\ty se examina en el Tema B) o <b>mantiene abierta</b> una conexión
\t\t\t\t\t\t\t\tque él mismo inició, que es lo que hace MQTT en la sesión 8.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Salida · el dispositivo inicia</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">192.168.1.47:52310 → el router lo reescribe como 190.12.44.8:61002 y anota el par.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Respuesta</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Llega a 190.12.44.8:61002. La tabla dice a quién pertenece y se entrega.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Entrada no solicitada</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Llega a 190.12.44.8:8080 sin entrada en la tabla. No hay destinatario: se descarta.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa asimetría no es una medida de seguridad deliberada, sino la
\t\t\t\t\t\t\tconsecuencia de que la tabla solo se rellena desde dentro. Su efecto
\t\t\t\t\t\t\tprotector es real de todos modos.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
)

# ──────────────────────────────────────────────────── 06 · TCP y UDP
lamina(
    "tcp-vs-udp",
    "Garantía de entrega frente a menor sobrecarga: TCP y UDP · Sesión 7",
    "TCP y UDP",
    envolver(f"""{cabecera(A, "Garantía de entrega frente a menor sobrecarga: TCP y UDP", "i-wave")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>TCP</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEstablece la conexión antes de enviar, numera cada byte, retransmite
\t\t\t\t\t\t\tlo que no se confirma y entrega en orden. El programa recibe lo
\t\t\t\t\t\t\tenviado o un error, nunca datos desordenados.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Costo:</b> 20 bytes de cabecera, tres paquetes de establecimiento
\t\t\t\t\t\t\tantes del primer dato, y memoria por conexión abierta.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>UDP</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEnvía el paquete y no espera confirmación. Puede perderse, duplicarse
\t\t\t\t\t\t\to llegar desordenado, y el programa no se entera salvo que lo
\t\t\t\t\t\t\tcompruebe él mismo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Ventaja:</b> 8 bytes de cabecera, sin establecimiento previo y sin
\t\t\t\t\t\t\testado que mantener.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Criterio de aplicación en proyectos embebidos</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<b>TCP</b> cuando el dato importa de forma individual: una medida de
\t\t\t\t\t\tconsumo que se factura, una orden de apertura. <b>UDP</b> cuando el
\t\t\t\t\t\tvalor se repite pronto y el retraso es peor que la pérdida: telemetría
\t\t\t\t\t\ta 100 Hz, sincronización horaria, descubrimiento de dispositivos en la
\t\t\t\t\t\tred local. HTTP y MQTT emplean TCP; NTP y mDNS, UDP.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tTCP garantiza la <b>entrega</b>, no el <b>plazo</b>. Una retransmisión
\t\t\t\t\t\ttras un paquete perdido introduce cientos de milisegundos, y el
\t\t\t\t\t\tprograma no puede acortarlos. Por eso una tarea con requisito temporal
\t\t\t\t\t\testricto nunca debe esperar a una operación de red, criterio que ya
\t\t\t\t\t\tdecidió el reparto en tareas de la sesión 6.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-wave",
)

# ────────────────────────────────────── 07 · interfaz WiFi del ESP32
lamina(
    "interfaz-wifi",
    "Modos de operación, canales y potencia recibida · Sesión 7",
    "Interfaz inalámbrica del ESP32",
    envolver(f"""{cabecera(A, "Modos de operación, canales y potencia recibida", "i-wave")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tModos de operación
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Estación</b> (<code>WIFI_STA</code>): se une a una red
\t\t\t\t\t\t\t\texistente. <b>Punto de acceso</b> (<code>WIFI_AP</code>): crea su
\t\t\t\t\t\t\t\tpropia red. <b>Combinado</b> (<code>WIFI_AP_STA</code>): ambas a la
\t\t\t\t\t\t\t\tvez, con la salvedad de que comparten una sola radio y un solo
\t\t\t\t\t\t\t\tcanal.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tExploración de redes
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>WiFi.scanNetworks()</code> devuelve cuántas encontró;
\t\t\t\t\t\t\t\t<code>WiFi.SSID(i)</code>, <code>WiFi.RSSI(i)</code> y
\t\t\t\t\t\t\t\t<code>WiFi.channel(i)</code> describen cada una. La exploración
\t\t\t\t\t\t\t\tbloquea la radio unos <b>2 s</b>, de modo que no se ejecuta dentro
\t\t\t\t\t\t\t\tde una tarea con requisito temporal.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Banda de 2,4 GHz y canales</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl ESP32 clásico opera solo en 2,4 GHz. De los 13 canales, solo
\t\t\t\t\t\t\t\t<b>1, 6 y 11</b> no se solapan entre sí. Un punto de acceso en el
\t\t\t\t\t\t\t\tcanal 3 interfiere con los del 1 y del 6 a la vez, y esa es una
\t\t\t\t\t\t\t\tcausa habitual de enlace inestable en entornos con muchas redes.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t\t\t<tr><th>RSSI</th><th>Calidad</th><th>Comportamiento esperable</th></tr>
\t\t\t\t\t\t\t\t</thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>−30 a −55</b></td><td>Excelente</td><td>Sin retransmisiones apreciables</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>−56 a −70</b></td><td>Suficiente</td><td>Operación normal</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>−71 a −80</b></td><td>Marginal</td><td>Sube el consumo y la latencia</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>bajo −80</b></td><td>Insuficiente</td><td>El enlace se pierde y se recupera</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="canales-wifi"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\tUn punto de acceso en el canal 3 interfiere a la vez con el 1 y con
\t\t\t\t\t\t\t\tel 6. Es una causa habitual de enlace inestable con RSSI aceptable.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>


\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-wave",
)

# ───────────────────────────────────── 08 · La hora del código · 28
lamina(
    "codigo-28-conexion-reintentos",
    "Código 28 · Conexión inalámbrica con reintentos · Sesión 7",
    "La hora del código · Conexión con reintentos",
    hora_del_codigo(
        28,
        "Conexión inalámbrica con reintentos y backoff exponencial",
        "La máquina de gestión de la conexión de la sesión 5 llevada a código, en una tarea propia del "
        "<b>núcleo 0</b> que nunca detiene el resto del programa. Una segunda tarea parpadea un LED cada 200 ms "
        "para dejar a la vista que el bucle sigue vivo durante la negociación.",
        "<code>WiFi.status()</code> devuelve el estado del enlace, y la tentación es esperarlo dentro de un "
        "<code>while</code>: eso bloquea todo el programa. Aquí se consulta <b>una vez por iteración</b> y su "
        "resultado es un evento más. El <b>RSSI</b> mide la potencia recibida en dBm, siempre negativa y mejor "
        "cuanto más cerca de cero. El <b>código de razón</b> de la desconexión distingue una contraseña incorrecta "
        "de un punto de acceso fuera de alcance.",
        "El <b>ESP32</b> enciende tres LED de estado en los <b>GPIO 25, 26 y 27</b> y un cuarto en el "
        "<b>GPIO 32</b> que parpadea siempre, todos con resistencia de 220 Ω a masa.",
        """[RED] t=0      DESCONECTADO -&gt; ASOCIANDO   intento=1  ssid=LAB-UNI
[RED] t=15000  plazo excedido -&gt; ESPERANDO   espera=1000 ms
[RED] t=18240  ASOCIANDO -&gt; CONECTADO  ip=192.168.1.47  rssi=-58
[VIVO] t=18400 parpadeos=92  el bucle no se detuvo
[RED] t=94100  enlace perdido (razon=8) -&gt; ESPERANDO  espera=1000""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Implementa la conexión como máquina de estados con DESCONECTADO, ASOCIANDO, ESPERANDO y CONECTADO, en una tarea del núcleo 0 con prioridad 2. Nunca uses <code>while (WiFi.status() != WL_CONNECTED)</code>: el estado se consulta una vez por iteración. Plazo de asociación 15000 ms; espera entre reintentos desde 1000 ms, duplicándose hasta 60000 ms, reiniciada al conectar. Al conectar imprime dirección, puerta de enlace, máscara, DNS y RSSI; registra la pérdida de enlace con su código de razón. Una segunda tarea en el núcleo 1 parpadea un LED cada 200 ms y los cuenta. Emite a 115200 baudios y guarda las credenciales en <code>credenciales.h</code>, excluido del control de versiones.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los cuatro LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la tarea de red, con la consulta del estado y el cálculo de la espera como pasos separados. Y el <b>diagrama de estados</b> del enlace junto a su tabla de transiciones, con una fila por flecha.""",
        "La línea <code>[VIVO]</code> es la comprobación del ejercicio: <b>92 parpadeos</b> durante los 18 s de "
        "negociación. Si la conexión se hubiera resuelto con una espera dentro de <code>setup()</code>, ese "
        "contador valdría cero. Fijarse también en la última línea: la <b>razón 8</b> identifica la causa de la "
        "caída, y sin ella una contraseña mal escrita y un punto de acceso apagado se leerían igual.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ────────────────────── 09 · artículo · elección del protocolo
lamina(
    "paper-protocolos-mensajeria",
    "Criterios de elección entre los cuatro protocolos de mensajería · Sesión 7",
    "Artículo · Elección de protocolo",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Naik, N.</b> (2017). Choice of effective messaging protocols for IoT systems: MQTT, CoAP, AMQP and "
        "HTTP. <i>2017 IEEE International Systems Engineering Symposium</i>. "
        "<code>doi:10.1109/SysEng.2017.8088251</code>",
        "Criterios de elección entre los cuatro protocolos de mensajería",
        ["Establecer <b>con qué criterio</b> se elige el protocolo de mensajería de un sistema de IoT.",
         "El autor parte de que <b>ninguno de los cuatro</b> cubre todos los requisitos.",
         "Análisis documental y sistemático, sin medidas propias sobre hardware."],
        ["Cabecera mínima de MQTT: <b>2 bytes</b>, frente a los <b>≈192</b> de una petición HTTP.",
         "Con cargas pequeñas, el protocolo <b>pesa más que el dato</b>.",
         "HTTP y CoAP usan <b>petición y respuesta</b>: obligan al equipo a preguntar.",
         "Tras la traducción de direcciones, el servidor <b>no puede iniciar</b> la conexión."],
        ["HTTP conserva ventaja en <b>interoperabilidad</b>: lo entiende cualquier servicio.",
         "Su modelo lo hace <b>inadecuado</b> cuando el servidor necesita alcanzar al equipo.",
         "La pregunta correcta no es cuál es mejor, sino <b>cuál conviene a cada escenario</b>."],
        [("paper-cabecera-fraccion",
          "Elaboración propia con las dos cifras de cabecera. Lo que decide es la fracción del envío que ocupa: con 20 bytes de dato, en HTTP el 90 % es protocolo."),
         ("paper-protocolos-dimensiones",
          "Las dimensiones que compara el autor. Ninguna columna está completa: de ahí que la elección sea por escenario.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ──────────────────────────────────── 10 · petición y respuesta HTTP
lamina(
    "peticion-respuesta-http",
    "Estructura de una petición y de una respuesta HTTP · Sesión 7",
    "Estructura de petición y respuesta",
    envolver(f"""{cabecera(B, "Estructura de una petición y de una respuesta HTTP", "i-terminal")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tCuatro partes en cada dirección
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa petición lleva <b>método</b>, <b>ruta</b>, <b>cabeceras</b> y
\t\t\t\t\t\t\t\t<b>cuerpo</b>. La respuesta sustituye las dos primeras por un
\t\t\t\t\t\t\t\t<b>código de estado</b> y conserva las otras dos. Una línea en
\t\t\t\t\t\t\t\tblanco separa las cabeceras del cuerpo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa biblioteca <code>HTTPClient</code> compone esas partes:
\t\t\t\t\t\t\t\t<code>http.begin(url)</code>,
\t\t\t\t\t\t\t\t<code>http.addHeader("Content-Type", "application/json")</code>,
\t\t\t\t\t\t\t\t<code>int codigo = http.POST(cuerpo)</code> y
\t\t\t\t\t\t\t\t<code>http.getString()</code>. Un <b>código negativo</b> señala un
\t\t\t\t\t\t\t\tfallo de la propia biblioteca, no del servidor.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>http.getString()</code> reserva en memoria la respuesta
\t\t\t\t\t\t\t\t<b>completa</b>. Con una respuesta de 200 kB agota la memoria libre
\t\t\t\t\t\t\t\ty el dispositivo se reinicia. La alternativa es leer del flujo por
\t\t\t\t\t\t\t\tpartes, que es el contenido de una lámina posterior.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">lo que viaja por el socket</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code><span class="hl hl--hit">POST /v1/medidas HTTP/1.1</span>        ← método y ruta
Host: api.ejemplo.com               ← cabeceras
Authorization: Bearer a1b2c3d4
Content-Type: application/json
Content-Length: 46
                                    ← línea en blanco
<span class="hl hl--add">{{"id":"esp32-07","t":23.4,"h":61.2}}</span>   ← cuerpo</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">respuesta del servidor</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code><span class="hl hl--hit">HTTP/1.1 201 Created</span>               ← código de estado
Content-Type: application/json
X-RateLimit-Remaining: 4998         ← límite de uso restante

{{"ok":true,"id":18342}}</code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-terminal",
)

# ───────────────────────────────────── 10b · La hora del código · 29
lamina(
    "codigo-29-diagnostico-enlace",
    "Código 29 · Exploración de redes y diagnóstico del enlace · Sesión 7",
    "La hora del código · Diagnóstico del enlace",
    hora_del_codigo(
        29,
        "Exploración de redes y diagnóstico de la calidad del enlace",
        "Explorar las redes visibles al arrancar, clasificarlas por banda y por canal y avisar de las que el "
        "ESP32 no puede usar. Ya conectado, medir el <b>RSSI cada 10 s</b> y traducirlo a las cuatro categorías "
        "de calidad, que el LED codifica con su ritmo.",
        "El <b>canal</b> es la porción de banda que ocupa una red. En 2,4 GHz los canales se solapan entre sí, y "
        "solo <b>1, 6 y 11</b> no comparten espectro: dos redes en canales vecinos se estorban aunque ambas se "
        "reciban fuertes. Un canal por encima del 14 corresponde a <b>5 GHz</b>, banda que este módulo no "
        "sintoniza. <code>WiFi.scanNetworks()</code> devuelve la lista con nombre, canal, RSSI y cifrado.",
        "El <b>ESP32</b> enciende un LED en el <b>GPIO 25</b> con resistencia de 220 Ω, cuyo ritmo de parpadeo "
        "codifica la calidad: fijo para excelente, lento para suficiente, rápido para marginal, apagado sin enlace.",
        """[SCAN] 6 redes en 2114 ms
[SCAN] LAB-UNI      ch= 6  rssi=-48  WPA2   utilizable
[SCAN] LAB-UNI-5G   ch=36  rssi=-52  WPA2   NO: banda de 5 GHz
[SCAN] vecino-3b ch= 3  rssi=-79  WPA2   aviso: solapa 1 y 6
[RSSI] t=10000  -51 dBm calidad=EXCELENTE
[RSSI] t=40000  -73 dBm calidad=MARGINAL""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Al arrancar, llama a <code>WiFi.scanNetworks()</code> e imprime para cada red su nombre, canal, RSSI y cifrado. Marca como no utilizable toda red cuyo canal supere el 14, porque corresponde a la banda de 5 GHz. Avisa de las que ocupan un canal distinto de 1, 6 u 11, indicando con cuáles se solapan. Después conéctate y mide el RSSI cada 10000 ms, clasificándolo en EXCELENTE, SUFICIENTE, MARGINAL o SIN_ENLACE según los umbrales de −55, −70 y −80 dBm. El LED codifica la categoría por su ritmo. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la exploración: recorrer la lista, decidir utilizable o no y emitir el aviso de solapamiento. Y la <b>banda de 2,4 GHz</b> con sus 13 canales dibujados con su anchura real, para que se vea por qué solo 1, 6 y 11 no se solapan.""",
        "La tercera línea del barrido es la que enseña: <code>vecino-3b</code> está en el canal 3 y <b>solapa con "
        "el 1 y con el 6</b>, que es el canal propio. Un enlace inestable con RSSI aceptable casi siempre se "
        "explica así, y sin este listado no hay manera de sospecharlo desde el dispositivo. Comparar después las "
        "dos líneas <code>[RSSI]</code>: 22 dB de caída bastan para pasar de excelente a marginal.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="yellow"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-resistor></wokwi-resistor></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ──────────────────────────── 11 · métodos y códigos de estado
lamina(
    "metodos-codigos-estado",
    "Métodos y familias de códigos de estado · Sesión 7",
    "Métodos y códigos de estado",
    envolver(f"""{cabecera(B, "Métodos y familias de códigos de estado", "i-target")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Método</th><th>Operación sobre el recurso</th><th>Repetible sin efecto añadido</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>GET</b></td><td>Obtener su estado actual</td><td>Sí</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>POST</b></td><td>Crear uno nuevo</td><td><b>No</b>: dos envíos crean dos</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>PUT</b></td><td>Sustituir uno existente por completo</td><td>Sí</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>DELETE</b></td><td>Eliminarlo</td><td>Sí</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa tercera columna importa cuando hay reintentos. Si un
\t\t\t\t\t\t\t\t<code>POST</code> vence su plazo de espera, el dispositivo no sabe
\t\t\t\t\t\t\t\tsi llegó: reintentar puede duplicar el registro. Con
\t\t\t\t\t\t\t\t<code>PUT</code> sobre una ruta que incluye un identificador propio,
\t\t\t\t\t\t\t\treintentar es inofensivo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Familia</th><th>Significado</th><th>Qué debe hacer el dispositivo</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>2xx</b></td><td>La petición se atendió</td><td>Continuar</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>4xx</b></td><td>Error en la petición</td><td><b>No reintentar</b>: repetir la misma da lo mismo</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>5xx</b></td><td>Error del servidor</td><td>Reintentar con backoff exponencial</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>429</b></td><td>Límite de uso superado</td><td>Esperar lo que indique la cabecera y reducir el ritmo</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">La distinción que decide el reintento</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>4xx</b> señala un fallo del dispositivo (token caducado, ruta
\t\t\t\t\t\t\t\tmal escrita, cuerpo con formato incorrecto) y reintentarlo consume
\t\t\t\t\t\t\t\tenergía sin ninguna posibilidad de éxito. Un <b>5xx</b> señala un
\t\t\t\t\t\t\t\tfallo transitorio del servidor y sí admite reintento.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-target",
)

# ────────────────────────────────────────────────────── 12 · API REST
lamina(
    "api-rest",
    "Lectura de la documentación de una API REST · Sesión 7",
    "Lectura de una API REST",
    envolver(f"""{cabecera(B, "Lectura de la documentación de una API REST", "i-book")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna <b>API REST</b> expone recursos identificados por una ruta,
\t\t\t\t\t\t\t\tsobre los que se opera con los métodos de HTTP. El servidor no
\t\t\t\t\t\t\t\tguarda memoria de peticiones anteriores: cada una lleva toda la
\t\t\t\t\t\t\t\tinformación necesaria, incluida la autenticación.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tCuatro datos que buscar en la documentación
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Punto de acceso</b> con su método y sus parámetros;
\t\t\t\t\t\t\t\t<b>forma de autenticación</b> y dónde va la credencial;
\t\t\t\t\t\t\t\t<b>límite de uso</b>, expresado en peticiones por minuto o por día;
\t\t\t\t\t\t\t\t<b>formato y tamaño</b> de la respuesta. El último decide si la
\t\t\t\t\t\t\t\trespuesta cabe en memoria.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">El límite de uso se calcula antes de programar</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn límite de <b>1000 peticiones diarias</b> admite una consulta cada
\t\t\t\t\t\t\t\t<b>86 s</b>. Un dispositivo que consulte cada 10 s agota la cuota en
\t\t\t\t\t\t\t\t2 h 47 min y recibe 429 el resto del día. La división se hace antes
\t\t\t\t\t\t\t\tde escribir el firmware, no después del primer corte de servicio.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">documentación típica de un punto de acceso</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>GET /data/2.5/weather

Parámetros
  lat, lon   obligatorios   grados decimales
  units      opcional       metric | imperial
  appid      obligatorio    clave de la cuenta

Autenticación  parámetro appid en la consulta
Límite de uso  60 por minuto · 1 000 000 al mes
Respuesta      JSON, entre 1,1 kB y 1,4 kB</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tUna respuesta de 1,4 kB cabe holgadamente en memoria. La lámina de
\t\t\t\t\t\t\t\tdeserialización trata el caso contrario, que es el habitual en
\t\t\t\t\t\t\t\tservicios que devuelven pronósticos de varios días.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────── 13 · autenticación y gestión de credenciales
lamina(
    "autenticacion-credenciales",
    "Autenticación por token y custodia de la credencial · Sesión 7",
    "Autenticación y credenciales",
    envolver(f"""{cabecera(B, "Autenticación por token y custodia de la credencial", "i-plug")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDónde viaja la credencial
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEn una <b>cabecera</b>
\t\t\t\t\t\t\t\t(<code>Authorization: Bearer …</code>) o como
\t\t\t\t\t\t\t\t<b>parámetro de la consulta</b>
\t\t\t\t\t\t\t\t(<code>?appid=…</code>). La primera es preferible: los parámetros
\t\t\t\t\t\t\t\tde la consulta quedan registrados en los historiales de los
\t\t\t\t\t\t\t\tservidores intermedios.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna clave escrita en el código fuente y subida a un repositorio
\t\t\t\t\t\t\t\tpúblico queda expuesta de forma permanente: aunque se borre después,
\t\t\t\t\t\t\t\tpermanece en el historial. La única corrección válida es
\t\t\t\t\t\t\t\t<b>revocarla y generar otra</b>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Procedimiento, establecido antes de la primera integración</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas credenciales viven en un archivo aparte, listado en
\t\t\t\t\t\t\t\t<code>.gitignore</code>, con una plantilla de ejemplo versionada
\t\t\t\t\t\t\t\tpara que el proyecto siga siendo reproducible. A partir de la
\t\t\t\t\t\t\t\tsesión 10 pasan a NVS (memoria no volátil), fuera del binario.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--no">Así no</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">main.cpp versionado</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code><span class="hl hl--hit">const char *CLAVE = "a1b2c3d4e5f6a7b8";  // queda en el historial</span></code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--si">Así sí</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">tres archivos</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>// credenciales.h        ← NO versionado
#define WIFI_SSID  "LAB-UNI"
#define API_CLAVE  "a1b2c3d4e5f6a7b8"

// credenciales.ejemplo.h ← sí versionado
#define WIFI_SSID  "nombre-de-tu-red"
#define API_CLAVE  "pon-aqui-tu-clave"

// .gitignore
<span class="hl hl--add">credenciales.h</span></code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-plug",
)

# ────────────────────────────────── 14 · HTTPS en un microcontrolador
lamina(
    "https-microcontrolador",
    "Costo y requisitos de HTTPS en un microcontrolador · Sesión 7",
    "HTTPS en un microcontrolador",
    envolver(f"""{cabecera(B, "Costo y requisitos de HTTPS en un microcontrolador", "i-chip")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-book")}Certificado raíz</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl dispositivo comprueba que el certificado del servidor procede de
\t\t\t\t\t\t\tuna autoridad en la que confía. Necesita llevar ese certificado raíz
\t\t\t\t\t\t\tincorporado: no hay almacén del sistema del que tomarlo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-clock")}Hora válida</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tTodo certificado tiene fecha de inicio y de caducidad. Un ESP32 que
\t\t\t\t\t\t\tarranca sin sincronizar la hora cree estar en 1970 y <b>rechaza todo
\t\t\t\t\t\t\tcertificado válido</b>.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Memoria</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa negociación reserva memoria para las claves y las memorias
\t\t\t\t\t\t\tintermedias de cifrado. Es la causa de que añadir HTTPS a un proyecto
\t\t\t\t\t\t\ten marcha produzca fallos aparentemente ajenos.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>client.setInsecure()</code> deshabilita la validación de la
\t\t\t\t\t\t\t\tcadena de confianza. La conexión sigue cifrada, pero el dispositivo
\t\t\t\t\t\t\t\tdeja de comprobar <b>con quién</b> habla: cualquier equipo
\t\t\t\t\t\t\t\tinterpuesto puede presentarse como el servidor legítimo. Es
\t\t\t\t\t\t\t\tadmisible en una prueba de laboratorio y nunca en un producto.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="term">[TLS] sin sincronizar la hora: fecha del sistema = 1970-01-01
[TLS] error -0x2700 certificado no valido todavia
[NTP] hora sincronizada: 2026-07-28 14:22:05 UTC
[TLS] negociacion completada en 1842 ms
[MEM] libre antes=214512  durante negociacion=163208  despues=198744</div>

\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa hora se sincroniza <b>antes</b> del primer intento de conexión
\t\t\t\t\t\t\tsegura. El error de certificado no válido todavía es el síntoma más
\t\t\t\t\t\t\tfrecuente de haber invertido ese orden.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-chip",
)

# ───────────────────────────────────── 14b · La hora del código · 31
lamina(
    "codigo-30-https-con-hora",
    "Código 30 · Conexión segura con hora sincronizada · Sesión 7",
    "La hora del código · Conexión segura",
    hora_del_codigo(
        30,
        "Conexión segura con hora sincronizada y certificado verificado",
        "Establecer una conexión HTTPS con validación completa del certificado. Se intenta primero <b>sin</b> "
        "sincronizar la hora, para ver el error que produce, y se mide la memoria libre antes, durante y después "
        "de la negociación.",
        "Un certificado tiene <b>fechas de validez</b>, así que verificarlo exige que el equipo sepa qué día es: "
        "al arrancar cree estar en 1970 y todo certificado le parece futuro. <code>configTime()</code> pone la "
        "hora por NTP. <code>client.setCACert()</code> carga el certificado raíz con el que se comprueba la "
        "cadena; <code>setInsecure()</code> se salta esa comprobación y deja el cifrado sin autenticación, que es "
        "justamente lo que no se quiere.",
        "El <b>ESP32</b> enciende dos LED en los <b>GPIO 25 y 26</b> con resistencia de 220 Ω: el primero indica "
        "hora válida y el segundo, certificado verificado.",
        """[BOOT] fecha del sistema = 1970-01-01 00:00:00
[TLS]  sin hora -&gt; error -0x2700 certificado no valido todavia
[NTP]  sincronizado: 2026-07-28 14:22:05 UTC en 842 ms
[TLS]  negociacion completada en 1842 ms cadena verificada
[MEM]  antes=214512  durante=163208  minimo=161940  despues=198744
[HTTP] 200 OK  1284 bytes""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Tras conectar a la red, intenta primero una conexión HTTPS <b>sin</b> sincronizar la hora y registra el error que devuelve. Sincroniza después por NTP con <code>configTime()</code>, espera a que la fecha del sistema supere el año 2020 y repite la conexión, esta vez con el certificado raíz incorporado mediante <code>client.setCACert()</code>. Nunca uses <code>setInsecure()</code>. Registra la memoria libre antes, durante y después de la negociación con <code>ESP.getFreeHeap()</code>, y su mínimo histórico. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del arranque, con la comprobación de la fecha como una condición previa a la conexión segura. Y la <b>secuencia</b> red, hora, certificado y petición, señalando qué error aparece si se altera ese orden.""",
        "Las dos primeras líneas son el ejercicio: el equipo cree estar en <b>1970</b> y por eso el certificado le "
        "parece «no válido todavía». Nada en ese mensaje menciona la hora, y ahí está la dificultad. Mirar después "
        "la línea <code>[MEM]</code>: la negociación se lleva unos <b>51 kB</b> y el mínimo queda en 161 940. Esa "
        "es la cifra que hay que tener libre antes de añadir HTTPS a un proyecto que ya funciona.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ─────────────────────────── 15 · artículo · cifrado sobre el dispositivo
lamina(
    "paper-cifrado-tls",
    "Efecto de la elección del algoritmo sobre el consumo del dispositivo · Sesión 7",
    "Artículo · Costo del cifrado",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Suárez-Albela, M.; Fraga-Lamas, P.; Fernández-Caramés, T. M.</b> (2018). A Practical Evaluation on "
        "RSA and ECC-Based Cipher Suites for IoT High-Security Energy-Efficient Fog and Mist Computing Devices. "
        "<i>Sensors</i> 18(11), 3868. <code>doi:10.3390/s18113868</code>",
        "Efecto de la elección del algoritmo sobre el consumo del dispositivo",
        ["Decidir qué <b>conjunto de cifrado</b> conviene a un equipo con recursos limitados.",
         "Las recomendaciones se formulan por nivel de seguridad, <b>sin considerar el consumo</b>.",
         "Banco de ensayo propio, comparando conjuntos basados en RSA y en curva elíptica."],
        ["El banco toma <b>1000 muestras de corriente por segundo</b>.",
         "Desviación declarada entre duración del ensayo y periodo de medida: <b>0,011 %</b>.",
         "La <b>curva elíptica</b> consume menos y rinde más a igual nivel de seguridad, salvo una excepción.",
         "Resultado contraintuitivo: la curva <b>más segura</b> resultó también <b>más rápida</b>."],
        ["Elegir por tamaño de clave puede dar <b>menos seguridad y peor rendimiento a la vez</b>.",
         "La razón de fondo: a igual seguridad, RSA necesita claves que crecen mucho más deprisa.",
         "Declarar la exactitud del banco es lo que permite atribuir la diferencia al algoritmo."],
        [("paper-clave-equivalente",
          "Equivalencias de NIST SP 800-57 Parte 1 Rev. 5, no medidas del artículo: explican por qué RSA cuesta más en cómputo y en energía."),
         ("paper-tls-banco",
          "La exactitud declarada del banco. Sin ella, una diferencia de consumo no se puede atribuir al algoritmo.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────── 16 · deserialización con memoria limitada
lamina(
    "deserializacion-filtros",
    "Extracción de campos de una respuesta que no cabe en memoria · Sesión 7",
    "Deserialización con filtro",
    envolver(f"""{cabecera(B, "Extracción de campos de una respuesta que no cabe en memoria", "i-layers")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tEl problema
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn pronóstico de cinco días son unos <b>200 kB</b> de JSON, y el
\t\t\t\t\t\t\t\tESP32 dispone de unos <b>200 kB</b> de memoria libre. Reservar la
\t\t\t\t\t\t\t\trespuesta completa y su representación en memoria es imposible,
\t\t\t\t\t\t\t\taunque solo interesen tres campos.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>ArduinoJson</code> admite un <b>filtro</b>: un documento que
\t\t\t\t\t\t\t\tdescribe qué campos conservar. La biblioteca recorre el flujo
\t\t\t\t\t\t\t\tconforme llega y descarta el resto sin llegar a reservarlo. Se pasa
\t\t\t\t\t\t\t\tcon <code>DeserializationOption::Filter(filtro)</code>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Se lee del flujo, no de una cadena</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa clave es pasar <code>http.getStream()</code> en vez de
\t\t\t\t\t\t\t\t<code>http.getString()</code>. Con la cadena, los 200 kB ya están
\t\t\t\t\t\t\t\ten memoria antes de que el filtro intervenga y el dispositivo se ha
\t\t\t\t\t\t\t\treiniciado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--si">Así sí</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">filtro sobre el flujo</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>JsonDocument filtro;
filtro["main"]["temp"] = true;      // solo estos tres
filtro["main"]["humidity"] = true;
filtro["name"] = true;

JsonDocument doc;
deserializeJson(doc, <span class="hl hl--add">http.getStream()</span>,
                <span class="hl hl--add">DeserializationOption::Filter(filtro)</span>);

float t = doc["main"]["temp"];      // 220 bytes en memoria</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[HTTP] respuesta: 204812 bytes
[JSON] sin filtro:  reserva estimada 268 kB -&gt; sin memoria, reinicio
[JSON] con filtro:  reserva real 220 bytes  -&gt; 3 campos extraidos
[MEM]  libre tras deserializar: 198 440 bytes</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ──────────────────────────── 17 · cuatro fallos con el mismo síntoma
lamina(
    "cuatro-fallos-mismo-sintoma",
    "Cuatro fallos con el mismo síntoma y cuatro acciones distintas · Sesión 7",
    "Cuatro fallos, cuatro acciones",
    envolver(f"""{cabecera(B, "Cuatro fallos con el mismo síntoma y cuatro acciones distintas", "i-alert")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Para el usuario, el dispositivo «no funciona» en los cuatro
\t\t\t\t\tcasos.</strong> Para el firmware son situaciones distintas que exigen
\t\t\t\t\trespuestas distintas.
\t\t\t\t</p>

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr><th>Fallo</th><th>Cómo se detecta</th><th>Acción del dispositivo</th></tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Sin red inalámbrica</b></td>
\t\t\t\t\t\t\t\t<td><code>WiFi.status() != WL_CONNECTED</code></td>
\t\t\t\t\t\t\t\t<td>Reintentar la asociación con backoff exponencial. No tocar la capa HTTP.</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Red sin salida a internet</b></td>
\t\t\t\t\t\t\t\t<td>Asociado y con dirección, pero la resolución del nombre falla</td>
\t\t\t\t\t\t\t\t<td>Mantener el enlace y reintentar la consulta; avisar de red sin salida.</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Servidor sin respuesta</b></td>
\t\t\t\t\t\t\t\t<td>Nombre resuelto, conexión vencida por plazo</td>
\t\t\t\t\t\t\t\t<td>Reintentar con backoff exponencial; conservar el último dato válido.</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Servidor que responde con error</b></td>
\t\t\t\t\t\t\t\t<td>Código 4xx o 5xx en la respuesta</td>
\t\t\t\t\t\t\t\t<td><b>4xx:</b> registrar y no reintentar. <b>5xx:</b> reintentar.</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Por qué el diagnóstico debe estar en el firmware</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tUn dispositivo instalado en un tejado no admite depuración sobre el
\t\t\t\t\t\tterreno. Si la traza distingue los cuatro casos, quien atiende la avería
\t\t\t\t\t\tsabe si debe revisar el punto de acceso, la conexión del edificio o la
\t\t\t\t\t\tcuenta del servicio. Si solo dice <em>error de red</em>, hay que
\t\t\t\t\t\tcomprobar las tres.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────── 18 · La hora del código · 29
lamina(
    "codigo-31-cliente-api",
    "Código 31 · Cliente de una API con tratamiento de fallos · Sesión 7",
    "La hora del código · Cliente de API",
    hora_del_codigo(
        31,
        "Cliente de una API pública con los cuatro fallos diferenciados",
        "Consultar una API pública cada cinco minutos y extraer tres campos. Cada fallo se clasifica en una de las "
        "<b>cuatro causas</b> de la lámina anterior y cada una recibe su propio tratamiento, porque no todas se "
        "arreglan reintentando.",
        "Un <b>filtro de deserialización</b> indica de antemano qué campos interesan, de modo que el resto del "
        "documento no llega a ocupar memoria: leyendo de <code>http.getStream()</code> ni siquiera se guarda la "
        "respuesta entera. Los códigos <b>4xx</b> señalan un error del cliente (clave inválida, ruta inexistente) "
        "y repetir la petición no los corrige; los <b>5xx</b> y los tiempos agotados sí admiten reintento. El "
        "<b>dato caducado</b> es el último valor válido con su timestamp, conservado pero señalado.",
        "El <b>ESP32</b> enciende cuatro LED en los <b>GPIO 25, 26, 27 y 32</b>, uno por causa de fallo, con "
        "resistencia de 220 Ω a masa.",
        """[API] t=0       GET /data/2.5/weather intento=1
[API] t=1204    200 OK  1284 bytes temp=19.4 C  hum=72 %
[FALLO] t=300000   SIN_RED        reasociar espera=1000 ms
[FALLO] t=600000   SIN_INTERNET   reintentar consulta
[FALLO] t=900000   SERVIDOR_MUDO  reintentar espera=2000 ms
[FALLO] t=1200000  HTTP_401       NO reintentar (token invalido)
[DATO] ultimo valido hace 900 s -&gt; caducado""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Consulta una API pública cada 300000 ms y extrae tres campos con un filtro de ArduinoJson leyendo de <code>http.getStream()</code>. Clasifica cada fallo en SIN_RED, SIN_INTERNET, SERVIDOR_MUDO o HTTP_ERROR y aplica el tratamiento de la tabla: los 4xx no se reintentan. El plazo de espera de la petición es de 8000 ms. Conserva el último dato válido con su timestamp y márcalo como caducado si supera los 900 s. La clave va en <code>credenciales.h</code>, excluido del control de versiones. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los cuatro LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una consulta completa, desde la petición hasta la actualización del dato o su marcado como caducado. Y el <b>árbol de decisión</b> que lleva de una petición fallida a cada una de las cuatro causas, con la comprobación que las distingue.""",
        "La cuarta línea de fallo es la que cambia el comportamiento: ante un <b>401</b> la acción es <b>no</b> "
        "reintentar. Un token caducado no se arregla repitiendo la petición cada cinco minutos durante meses, y "
        "esa es la regla que más energía ahorra en un equipo con batería. La última línea muestra la otra "
        "decisión: el dato no se borra, se marca <b>caducado</b>, para que el equipo siga sirviendo sin mentir "
        "sobre la antigüedad de lo que muestra.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="orange"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=LED_SCRIPTS,
)

# ─────────────────────── 19 · artículo · MQTT frente a HTTP sobre ESP32
lamina(
    "paper-mqtt-vs-http",
    "Medida del costo de HTTP frente a publicación y suscripción sobre ESP32 · Sesión 7",
    "Artículo · HTTP frente a MQTT en ESP32",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Adriansyah, S.; Sumarno; Nurfuha, U. M. et al.</b> (2026). Performance Analysis of MQTT and HTTP "
        "Protocols on Low-Power ESP32 Devices for IoT Applications. <i>Jurnal Teknologi Informasi</i>. "
        "<code>doi:10.1109/ICITSI.2026.10412887</code>",
        "Medida del costo de HTTP frente a publicación y suscripción sobre ESP32",
        ["Cuantificar la diferencia entre los dos protocolos <b>sobre el hardware de este curso</b>.",
         "En latencia, consumo, sobrecarga y estabilidad ante red degradada.",
         "Revisión sistemática según <b>PRISMA 2020</b>: de 166 registros, 9 estudios empíricos."],
        ["MQTT responde entre <b>4,76× y 12,1×</b> más rápido que HTTP.",
         "El extremo alto corresponde a tráfico elevado y servidor remoto.",
         "Reducción de consumo: solo del <b>6 % al 8 %</b>. La radio domina en ambos casos.",
         "<b>9 de 166</b> registros superaron los criterios de inclusión."],
        ["MQTT supera a HTTP en <b>todas las dimensiones medidas</b>, y la diferencia crece con el tráfico.",
         "HTTP sigue siendo adecuado cuando priman la <b>compatibilidad y la simplicidad</b>.",
         "La proporción 9 de 166 dice cuánta literatura sobre el asunto no aporta medidas propias."],
        [("paper-mqtt-dos-ventajas",
          "Las dos ventajas publicadas a la misma escala: la de latencia es de otro orden que la de consumo."),
         ("paper-mqtt-prisma",
          "El filtro de la revisión. Casi todo lo publicado no aporta medidas comparables sobre este hardware.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────── 20 · verificación previa y operación sin red
lamina(
    "verificacion-previa-y-sin-red",
    "Verificación previa de la API y operación sin conectividad · Sesión 7",
    "Verificación previa y operación sin red",
    envolver(f"""{cabecera(B, "Verificación previa de la API y operación sin conectividad", "i-check")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-check")}
\t\t\t\t\t\t\t\tVerificar la API antes de escribir firmware
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa petición se prueba primero desde el navegador o desde un cliente
\t\t\t\t\t\t\t\tde escritorio, hasta obtener la respuesta esperada. Solo entonces se
\t\t\t\t\t\t\t\tlleva al dispositivo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tDepurar a la vez el enlace de red y el código de la petición
\t\t\t\t\t\t\t\timpide aislar la causa: un 401 puede deberse a la clave, al formato
\t\t\t\t\t\t\t\tde la cabecera o a la ruta, y sobre el dispositivo las tres se ven
\t\t\t\t\t\t\t\tigual.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-terminal")}
\t\t\t\t\t\t\t\tCon qué comprobarlo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa barra del navegador basta para un <code>GET</code> sin
\t\t\t\t\t\t\t\tcabeceras. Para lo demás, <code>curl</code> desde la terminal:
\t\t\t\t\t\t\t\tmuestra el código de estado, las cabeceras y el cuerpo, y su orden
\t\t\t\t\t\t\t\tse traslada casi literalmente al firmware.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tComportamiento sin conectividad
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn dispositivo sin red no debe detenerse ni mostrar el último valor
\t\t\t\t\t\t\t\tcomo si fuera actual. Las tres decisiones que hay que tomar antes de
\t\t\t\t\t\t\t\tprogramar:
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Qué conserva</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Último valor válido con su timestamp, para poder decir cuán antiguo es.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Cuándo lo declara caducado</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Un umbral explícito, propio de la magnitud: 15 min para temperatura exterior, 5 s para una consigna de control.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Qué sigue haciendo</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Adquirir y almacenar en local. La sesión 10 añade el envío diferido de lo acumulado.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">$ curl -i -H "Authorization: Bearer $CLAVE" \\
       https://api.ejemplo.com/v1/estado
HTTP/2 200
content-type: application/json
x-ratelimit-remaining: 4998</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
)

# ─────────────────────────────────────── 21 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes con la conexión y las peticiones · Sesión 7",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes con la conexión y las peticiones", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("No conecta con credenciales correctas", "El punto de acceso aparece en la exploración y la contraseña es la buena, pero la asociación nunca se completa.", "La red opera en 5 GHz y el ESP32 clásico solo admite 2,4 GHz. La exploración la muestra porque detecta la baliza, no porque pueda usarla.", "Imprimir el canal de la red en la exploración: un canal por encima de 14 corresponde a la banda de 5 GHz.", "i-wave")}
{problema("Se reinicia al activar HTTPS", "El proyecto funcionaba con HTTP y se reinicia al cambiar a HTTPS, con una traza que apunta a código sin relación.", "La negociación segura reserva memoria adicional. El proyecto operaba con poco margen y ahora lo agota.", "Imprimir <code>ESP.getFreeHeap()</code> antes y durante la negociación. Si el mínimo se acerca a cero, la causa es esa.", "i-layers")}
{problema("Certificado no válido todavía", "La conexión segura falla con un error de certificado pese a que el servidor es correcto.", "El dispositivo arrancó sin sincronizar la hora y cree estar en 1970, fecha anterior al inicio de validez de todo certificado.", "Imprimir la fecha del sistema antes del primer intento. Sincronizar por NTP antes de cualquier conexión segura.", "i-clock")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("El servicio deja de responder a media mañana", "Las consultas funcionan durante unas horas y luego devuelven siempre el mismo código de error.", "Se ha superado el límite de uso de la cuenta. El código 429 se mantiene hasta que la ventana se renueva.", "Leer la cabecera de límite restante en cada respuesta y registrarla. Dividir la cuota diaria entre el periodo de consulta antes de fijarlo.", "i-target")}
{problema("El dispositivo consume mucho más de lo previsto", "La autonomía con batería es una fracción de la estimada, sin que el programa haga nada visible.", "Reintentos demasiado frecuentes ante un fallo permanente, como un token caducado. Cada intento enciende la radio.", "Contar los intentos fallidos consecutivos y su causa. Un 4xx repetido señala reintentos que nunca podrán tener éxito.", "i-bolt")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 22 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 7 · Sesión 7",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("Socket", "", "Extremo de una conexión: el par dirección IP más puerto. Una conexión queda determinada por sus dos sockets.")}
{termino("NAT", "network address translation", "Sustitución de la dirección privada de origen por la pública del router. Solo un paquete de salida crea la entrada de la tabla.")}
{termino("DHCP y DNS", "DHCP / DNS", "El primero reparte dirección, máscara y puerta de enlace al entrar en la red; el segundo traduce nombres a direcciones y su fallo delata una red sin salida a internet.")}
{termino("RSSI", "received signal strength indicator", "Potencia de la señal recibida, en dBm. Por debajo de −80 dBm el enlace se pierde y se recupera de forma repetida.")}
{termino("MAC", "media access control address", "Dirección de seis bytes grabada en fabricación. No cambia al mudar de red.")}
{termino("TCP y UDP", "TCP / UDP", "Protocolos de transporte. TCP garantiza entrega y orden con 20 bytes de cabecera; UDP no garantiza nada y ocupa 8.")}
{termino("HTTPS", "HTTP over TLS", "HTTP cifrado con TLS. Exige hora válida, memoria adicional y un certificado raíz con el que verificar la cadena de confianza.")}
{termino("API REST", "REST API", "Interfaz que expone recursos por su ruta, operados con los métodos de HTTP. El servidor no guarda estado entre peticiones.")}
{termino("Idempotencia", "idempotence", "Propiedad de una operación que da el mismo resultado al repetirse. Decide si un reintento es seguro.")}
{termino("Token", "bearer token", "Credencial que acompaña a cada petición en la cabecera <code>Authorization</code>. Nunca se versiona.")}
{termino("Backoff exponencial", "exponential backoff", "Reintento que duplica la espera tras cada fallo, hasta un máximo. Reduce consumo y evita saturar al servidor.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 23 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 7 · Sesión 7",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Fundamentos de red</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada capa añade su cabecera: enviar 12 bytes de dato cuesta unos 266
\t\t\t\t\t\t\ten total. La traducción de direcciones explica que el dispositivo
\t\t\t\t\t\t\talcance al exterior sin ser alcanzable.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa conexión se modela como máquina de estados con reintentos y espera
\t\t\t\t\t\t\tcreciente, en su propia tarea. Nunca como una espera dentro de
\t\t\t\t\t\t\t<code>setup()</code>.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-terminal")}HTTP y APIs</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUn 4xx no se reintenta; un 5xx sí. El límite de uso se divide antes
\t\t\t\t\t\t\tde fijar el periodo de consulta, no después del primer corte.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa respuesta se lee del flujo con filtro, no como cadena completa.
\t\t\t\t\t\t\tLas credenciales viven fuera del código versionado.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a la sesión siguiente</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Las dos limitaciones de HTTP</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tCosto por mensaje e imposibilidad de que el servidor tome la
\t\t\t\t\t\t\t\tiniciativa. La sesión 8 parte de ambas.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-clock")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">La hora como requisito</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tSin hora válida no hay conexión segura. La sesión 10 la convierte en
\t\t\t\t\t\t\t\tparte de la puesta en marcha.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">El ESP32 en el papel de servidor</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa sesión 9 invierte los papeles: el dispositivo escucha, con las
\t\t\t\t\t\t\t\tconsecuencias de memoria que eso impone.
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
    "Referencias de la sesión 7 · Sesión 7",
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
\t\t\t\t\t\t\t\t<span class="ref__title">Choice of effective messaging protocols for IoT systems: MQTT, CoAP, AMQP and HTTP</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Naik, N. (2017). <i>IEEE ISSE 2017</i>, 1-7. Copia de repositorio institucional.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/SysEng.2017.8088251</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Elección de protocolo · Puente con la sesión 8</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">A Practical Evaluation on RSA and ECC-Based Cipher Suites for IoT Devices</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Suárez-Albela, M.; Fraga-Lamas, P.; Fernández-Caramés, T. M. (2018). <i>Sensors</i> 18(11), 3868. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3390/s18113868</span>
\t\t\t\t\t\t\t\t<span class="ref__where">HTTPS · Costo del cifrado</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Performance Analysis of MQTT and HTTP Protocols on Low-Power ESP32 Devices</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Adriansyah, S.; Sumarno; Nurfuha, U. M. et al. (2026). <i>CoreID Journal</i> 4(1), 38-45. CC BY-SA 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.60005/coreid.v4i1.160</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Latencia y consumo · Cierre de la sesión</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-07/</code>, junto a dos más sobre dispositivos ESP32 y servidor web embebido. El índice, en <code>src/paper/INDICE.md</code>.</span>
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
        {"clase": "clase-07", "sesion": "Sesión 7", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
