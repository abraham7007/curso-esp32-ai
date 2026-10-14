#!/usr/bin/env python3
"""Sesión 5 — Máquinas de estados finitos.

Contenido de las láminas. La plantilla, la cadena de navegación y el total
los resuelve `tools/generar-clase.py`; aquí solo vive lo que distingue a cada
lámina. Ejecutar desde la raíz del proyecto:

    python3 tools/clases/clase_05.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "generador", Path(__file__).resolve().parents[1] / "generar-clase.py"
)
_gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen)

from comun import ESPARCIDO, articulo, cabecera, credito, envolver, hallazgo, hora_del_codigo, ico, portada, problema, termino

A = "01 · Modelado del comportamiento"
B = "02 · Implementación y casos de aplicación"

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


# ───────────────────────────────────────────────────────── 01 · portada
lamina(
    "portada",
    "Sesión 5 · Máquinas de estados finitos",
    "Máquinas de estados finitos",
    portada(
        "Sesión 5",
        "Máquinas de<br />estados finitos",
        "Modelado del comportamiento mediante estados.",
        "Implementación no bloqueante y casos de aplicación.",
        [
         ("i-flow", "Estados, eventos y transiciones"),
         ("i-target", "Moore, Mealy y tabla de transiciones"),
         ("i-clock", "Implementación con enum y switch"),
         ("i-alert", "Rutas de excepción y recuperación"),
        ],
        "02-acumulacion-banderas.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ───────────────────────────────────────────── 02 · situación de partida
lamina(
    "acumulacion-banderas",
    "Acumulación de variables de control · Sesión 5",
    "Acumulación de variables de control",
    envolver(f"""{cabecera(A, "Acumulación de variables de control", "i-alert")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tSituación de partida
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn programa que crece añadiendo una variable booleana por cada
\t\t\t\t\t\t\t\tcondición termina con un conjunto de banderas independientes:
\t\t\t\t\t\t\t\t<code>enMarcha</code>, <code>esperandoPeaton</code>,
\t\t\t\t\t\t\t\t<code>yaAviso</code>, <code>bloqueado</code>.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCon <b>n</b> banderas hay <b>2<sup>n</sup></b> combinaciones
\t\t\t\t\t\t\t\tposibles, y el programa solo define el comportamiento de unas
\t\t\t\t\t\t\t\tpocas. El resto son estados alcanzables que nadie ha especificado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-terminal")}
\t\t\t\t\t\t\t\tSíntoma reconocible
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCorregir un fallo obliga a añadir otra bandera, y esa corrección
\t\t\t\t\t\t\t\thabilita una combinación nueva que vuelve a fallar. La causa no es
\t\t\t\t\t\t\t\tfalta de cuidado: el modelo permite representar situaciones que el
\t\t\t\t\t\t\t\tdispositivo no puede tener.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t<div class="figure__frame" data-figure="banderas-vs-estados"></div>
\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\tCon diez banderas hay 1024 situaciones alcanzables y el programa
\t\t\t\t\t\t\t\tdefine cinco. Con diez estados declarados hay exactamente diez.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">enMarcha=1 esperandoPeaton=1 yaAviso=0 bloqueado=1
&gt; ninguna rama del if contempla esta combinacion</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Solución estructural</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSe sustituye el conjunto de banderas por <b>una sola variable de
\t\t\t\t\t\t\t\testado</b> con un número cerrado de valores. El espacio de
\t\t\t\t\t\t\t\tsituaciones deja de crecer de forma exponencial y pasa a ser
\t\t\t\t\t\t\t\tenumerable, que es la condición para poder verificarlo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>""",
    ),
    icono="i-alert",
)

# ─────────────────────────────────── 03 · estado, evento, transición
lamina(
    "estado-evento-transicion",
    "Estado, evento y transición · Sesión 5",
    "Estado, evento y transición",
    envolver(f"""{cabecera(A, "Estado, evento y transición")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Tres términos y una regla.</strong> En cada instante hay
\t\t\t\t\texactamente un estado activo, y solo un evento puede cambiarlo.
\t\t\t\t</p>

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\tEstado
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSituación en la que el dispositivo permanece hasta que ocurre algo.
\t\t\t\t\t\t\tDetermina qué salidas están activas y qué eventos se atienden.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>VERDE_VEHICULOS</code>, <code>AMBAR</code>,
\t\t\t\t\t\t\t<code>ROJO_CON_PASO</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t{ico("i-bolt")}
\t\t\t\t\t\t\tEvento
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tHecho instantáneo que el sistema observa: un flanco en un terminal,
\t\t\t\t\t\t\tel vencimiento de un temporizador, la llegada de una trama.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>PULSADOR_PEATON</code>, <code>VENCE_TEMPORIZADOR</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t\tTransición
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tPaso de un estado a otro provocado por un evento concreto. Es la
\t\t\t\t\t\t\túnica forma de cambiar de estado.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\t<code>VERDE — VENCE_TEMPORIZADOR → AMBAR</code>
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\tEn el código
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tEl estado es una variable de tipo <code>enum class</code>; el evento,
\t\t\t\t\t\tun valor devuelto por la función que consulta las entradas; la
\t\t\t\t\t\ttransición, una asignación a esa variable dentro de un
\t\t\t\t\t\t<code>switch</code>. El estado inicial se fija en <code>setup()</code>
\t\t\t\t\t\ty es parte de la especificación, no un detalle de implementación.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Aplicaciones habituales</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-plug")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Cargador de batería por etapas</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tCorriente constante, tensión constante y mantenimiento son estados:
\t\t\t\t\t\t\t\tcada uno fija un límite distinto y atiende eventos distintos.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-link")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Enlace inalámbrico</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tDesconectado, asociando, obteniendo dirección y conectado. La
\t\t\t\t\t\t\t\tpérdida de portadora es un evento que devuelve al primero.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-clock")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Portón automático</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa detección de obstáculo durante el cierre es un evento que
\t\t\t\t\t\t\t\tinvierte el movimiento; sin estado, esa regla no tiene dónde vivir.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
)

# ──────────────────────────────── 04 · acciones y condiciones de guarda
lamina(
    "acciones-guardas",
    "Acciones de entrada, de salida y condiciones de guarda · Sesión 5",
    "Acciones y condiciones de guarda",
    envolver(f"""{cabecera(A, "Acciones de entrada, de salida y condiciones de guarda")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>acción de entrada</b> se ejecuta una sola vez al llegar al
\t\t\t\t\t\t\t\testado; la <b>acción de salida</b>, una sola vez al abandonarlo.
\t\t\t\t\t\t\t\tNinguna de las dos se repite mientras el estado permanece activo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>condición de guarda (condición de guarda)</b> (condición de guarda) es una expresión booleana que
\t\t\t\t\t\t\t\tacompaña a una transición: el evento la dispara solo si la condición
\t\t\t\t\t\t\t\tse cumple. Un mismo evento puede llevar a estados distintos según la
\t\t\t\t\t\t\t\tguarda que se satisfaga.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tEjemplo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEn un cargador, el evento <code>VENCE_MEDIDA</code> lleva a
\t\t\t\t\t\t\t\t<code>TENSION_CONSTANTE</code> si la guarda
\t\t\t\t\t\t\t\t<code>v &gt;= 4,20 V</code> se cumple, y mantiene el estado actual
\t\t\t\t\t\t\t\tsi no. Mismo evento, dos destinos.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">acción de entrada · una vez</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>// La transición cambia el estado y ejecuta la acción de entrada.
// Al estar dentro del if, se ejecuta una sola vez.
if (evento == VENCE_TEMPORIZADOR) {{
  estado = Estado::AMBAR;
  <span class="hl hl--hit">digitalWrite(PIN_AMBAR, HIGH);   // acción de entrada</span>
  <span class="hl hl--hit">tInicio = millis();              // acción de entrada</span>
}}</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--no">Así no</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">acción repetida en cada iteración</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>case Estado::AMBAR:
  <span class="hl hl--hit">tInicio = millis();   // se reinicia en cada vuelta del bucle</span>
  if (millis() - tInicio &gt; 3000) estado = Estado::ROJO;
  break;   // la condición nunca se cumple: el estado no avanza</code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Regla de implementación</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tLo que debe ocurrir <b>una vez</b> va en la transición; lo que debe
\t\t\t\t\t\tevaluarse <b>en cada iteración</b> va en el cuerpo del estado. Confundir
\t\t\t\t\t\tambos produce el fallo del panel derecho: un timestamp que se
\t\t\t\t\t\treinicia sola y un estado que no progresa nunca.
\t\t\t\t\t</p>
\t\t\t\t</div>"""),
)

# ────────────────────────────────────────────────── 05 · Moore y Mealy
lamina(
    "moore-mealy",
    "Modelos de Moore y de Mealy · Sesión 5",
    "Modelos de Moore y de Mealy",
    envolver(f"""{cabecera(A, "Modelos de Moore y de Mealy", "i-layers")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>La diferencia es dónde se sitúan las salidas.</strong> El mismo
\t\t\t\t\tsistema admite ambos formalismos, y la elección tiene consecuencias
\t\t\t\t\tmedibles sobre el número de estados y sobre la latencia.
\t\t\t\t</p>

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Moore — la salida depende del estado</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada estado fija sus salidas. Para representar dos salidas distintas
\t\t\t\t\t\t\thacen falta dos estados, de modo que el diagrama crece.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<div class="term">estado AMBAR  → salida: ambar=1, verde=0, rojo=0
estado ROJO   → salida: ambar=0, verde=0, rojo=1</div>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tLa salida cambia en el instante de la transición y se mantiene
\t\t\t\t\t\t\testable mientras dure el estado.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Mealy — la salida depende del estado y del evento</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa salida se asocia a la transición. El mismo estado produce salidas
\t\t\t\t\t\t\tdistintas según el evento que lo abandone, y hacen falta menos
\t\t\t\t\t\t\testados.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<div class="term">ESPERA,  moneda/devolver_cambio → ESPERA
ESPERA,  seleccion/entregar    → ENTREGA</div>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tLa salida responde en el mismo instante del evento, sin esperar a
\t\t\t\t\t\t\tconsolidar el estado.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Opción adoptada</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<b>Moore</b>, por dos razones verificables. Las salidas quedan
\t\t\t\t\t\tdeterminadas por una sola variable, de modo que el estado impreso por
\t\t\t\t\t\tel monitor serie describe por completo lo que hace el dispositivo. Y el
\t\t\t\t\t\tdiagrama admite lectura directa: cada nodo lleva escritas sus salidas.
\t\t\t\t\t\tMealy se reserva para las transiciones que deben producir un efecto
\t\t\t\t\t\tinmediato, como emitir una trama de acuse.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\tEn el código
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tEn una máquina de Moore, las salidas se escriben en la acción de
\t\t\t\t\t\tentrada de cada estado o en una única función
\t\t\t\t\t\t<code>aplicarSalidas(estado)</code> llamada tras cada transición. Esta
\t\t\t\t\t\tsegunda forma concentra en un punto todas las escrituras a
\t\t\t\t\t\t<code>digitalWrite()</code> y evita que una salida quede activa al
\t\t\t\t\t\tcambiar de estado.
\t\t\t\t\t</p>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ─────────────────────────────────────────────────── 06 · notación UML
lamina(
    "notacion-uml",
    "Notación UML de máquina de estados · Sesión 5",
    "Notación UML de máquina de estados",
    envolver(f"""{cabecera(A, "Notación UML de máquina de estados", "i-diagram")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tNotación normalizada para dibujar máquinas de estados. Rectángulo
\t\t\t\t\t\t\t\tredondeado para el estado, flecha para la transición, círculo
\t\t\t\t\t\t\t\trelleno para el estado inicial y círculo con anillo para el final.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCada flecha se rotula
\t\t\t\t\t\t\t\t<code>evento [guarda] / acción</code>. Las tres partes son
\t\t\t\t\t\t\t\topcionales salvo el evento.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tFunción del diagrama
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl diagrama es la <b>especificación acordada</b> entre quien define
\t\t\t\t\t\t\t\tel requisito y quien lo implementa. Se revisa y se corrige antes de
\t\t\t\t\t\t\t\tescribir código, cuando modificar una transición cuesta mover una
\t\t\t\t\t\t\t\tflecha. Un desacuerdo detectado aquí no llega a ser un fallo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">● → VERDE_VEHICULOS</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Estado inicial. Salidas: verde de vehículos activo, rojo de peatones activo.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__meta">pulsador [t ≥ 8 s] / —</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">La guarda impide acortar el verde por debajo del mínimo, aunque se pulse antes.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">AMBAR</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Duración fija de 3 s. Único evento admitido: el vencimiento del temporizador.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">ROJO_CON_PASO</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Salidas invertidas. Al vencer, retorna al estado inicial y la solicitud queda atendida.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLa guarda <code>[t ≥ 8 s]</code> es el elemento que convierte un
\t\t\t\t\t\t\tdiagrama correcto en un semáforo utilizable: sin ella, pulsar
\t\t\t\t\t\t\trepetidamente detiene el tráfico.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-diagram",
)

# ──────────────────────────────── 06b · simulación del semáforo
lamina(
    "simulacion-semaforo",
    "Recorrido del semáforo estado por estado · Sesión 5",
    "Recorrido del semáforo",
    envolver(f"""{cabecera(A, "Recorrido del semáforo estado por estado", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tQué dispara cada transición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tDos estados salen por vencimiento de plazo y uno por pulsación
\t\t\t\t\t\t\t\t<em>si</em> la guarda lo permite. La solicitud del peatón queda
\t\t\t\t\t\t\t\tregistrada aunque llegue antes del tiempo mínimo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tEl estado activo se resalta sobre el diagrama mientras el reloj
\t\t\t\t\t\t\t\tavanza. Al pulsar antes del tiempo mínimo, la guarda impide la
\t\t\t\t\t\t\t\ttransición y la solicitud pasa a pendiente: el semáforo cambia al
\t\t\t\t\t\t\t\tcumplirse el plazo, no al pulsar. Pulsar durante el paso peatonal no
\t\t\t\t\t\t\t\tproduce ningún efecto, y esa fila también está en la tabla.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="fsm-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Diagrama de los tres estados del semáforo con el estado activo resaltado, el tiempo transcurrido en el estado y la solicitud peatonal pendiente"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<button id="fsm-pulsar" type="button" class="btn btn--primary">
\t\t\t\t\t\t\t\t\tPulsador de peatón
\t\t\t\t\t\t\t\t</button>
\t\t\t\t\t\t\t\t<button id="fsm-reiniciar" type="button" class="btn btn--secondary">
\t\t\t\t\t\t\t\t\tReiniciar
\t\t\t\t\t\t\t\t</button>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Estado activo</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="fsm-estado">VERDE_VEHICULOS</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Tiempo en el estado</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="fsm-tiempo">0,0 s</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="fsm-item-guarda">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Guarda t ≥ 8 s</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="fsm-guarda">no</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="fsm-item-solicitud">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Solicitud peatonal</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="fsm-solicitud">ninguna</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Los plazos son los mismos que enuncia la tabla de transiciones de la
\t\t\t// lámina siguiente. Si cambian allí, cambian aquí: la simulación no
\t\t\t// puede contradecir al texto.
\t\t\tconst PLAZOS = { VERDE: 8000, AMBAR: 3000, PASO: 10000 };
\t\t\tconst ESTADOS = [
\t\t\t\t{ id: "VERDE_VEHICULOS", rotulo: "VERDE_VEHICULOS", plazo: PLAZOS.VERDE, tinta: "--color-ok" },
\t\t\t\t{ id: "AMBAR", rotulo: "AMBAR", plazo: PLAZOS.AMBAR, tinta: "--color-warn" },
\t\t\t\t{ id: "ROJO_CON_PASO", rotulo: "ROJO_CON_PASO", plazo: PLAZOS.PASO, tinta: "--color-accent" },
\t\t\t];

\t\t\tconst lienzo = document.getElementById("fsm-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst salidaEstado = document.getElementById("fsm-estado");
\t\t\tconst salidaTiempo = document.getElementById("fsm-tiempo");
\t\t\tconst salidaGuarda = document.getElementById("fsm-guarda");
\t\t\tconst salidaSolicitud = document.getElementById("fsm-solicitud");
\t\t\tconst itemGuarda = document.getElementById("fsm-item-guarda");
\t\t\tconst itemSolicitud = document.getElementById("fsm-item-solicitud");

\t\t\tlet indice = 0;
\t\t\tlet entrada = performance.now();
\t\t\tlet pendiente = false;

\t\t\tfunction variable(nombre) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();
\t\t\t}

\t\t\tfunction coma(n, dec) {
\t\t\t\treturn n.toFixed(dec).replace(".", ",");
\t\t\t}

\t\t\t// El estado VERDE solo avanza si hay solicitud pendiente Y se cumplió
\t\t\t// el mínimo. Los otros dos avanzan por vencimiento del plazo.
\t\t\tfunction avanzar(transcurrido) {
\t\t\t\tconst actual = ESTADOS[indice];
\t\t\t\tif (actual.id === "VERDE_VEHICULOS") {
\t\t\t\t\tif (pendiente && transcurrido >= actual.plazo) {
\t\t\t\t\t\tindice = 1;
\t\t\t\t\t\treturn true;
\t\t\t\t\t}
\t\t\t\t\treturn false;
\t\t\t\t}
\t\t\t\tif (transcurrido >= actual.plazo) {
\t\t\t\t\tif (actual.id === "ROJO_CON_PASO") pendiente = false;
\t\t\t\t\tindice = (indice + 1) % ESTADOS.length;
\t\t\t\t\treturn true;
\t\t\t\t}
\t\t\t\treturn false;
\t\t\t}

\t\t\tfunction dibujar(transcurrido) {
\t\t\t\tconst w = lienzo.width;
\t\t\t\tconst h = lienzo.height;
\t\t\t\tctx.clearRect(0, 0, w, h);

\t\t\t\tconst borde = variable("--color-border");
\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst superficie = variable("--color-surface");

\t\t\t\tconst cy = 96;
\t\t\t\tconst rx = 118;
\t\t\t\tconst ry = 46;
\t\t\t\tconst centros = [150, 450, 750];

\t\t\t\t// Flechas entre estados, dibujadas antes para que los nodos las tapen.
\t\t\t\tctx.strokeStyle = borde;
\t\t\t\tctx.lineWidth = 1.6;
\t\t\t\tfor (let i = 0; i < 2; i++) {
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.moveTo(centros[i] + rx / 2, cy);
\t\t\t\t\tctx.lineTo(centros[i + 1] - rx / 2, cy);
\t\t\t\t\tctx.stroke();
\t\t\t\t}
\t\t\t\t// Retorno del último al primero, por debajo.
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(centros[2], cy + ry);
\t\t\t\tctx.bezierCurveTo(centros[2], cy + 130, centros[0], cy + 130, centros[0], cy + ry);
\t\t\t\tctx.stroke();

\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "12px system-ui";
\t\t\t\tctx.textAlign = "center";
\t\t\t\tctx.fillText("pulsador [t ≥ 8 s]", (centros[0] + centros[1]) / 2, cy - 12);
\t\t\t\tctx.fillText("vence 3 s", (centros[1] + centros[2]) / 2, cy - 12);
\t\t\t\tctx.fillText("vence 10 s · borra la solicitud", (centros[0] + centros[2]) / 2, cy + 148);

\t\t\t\tESTADOS.forEach((estado, i) => {
\t\t\t\t\tconst activo = i === indice;
\t\t\t\t\tconst tinta = variable(estado.tinta);
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.roundRect(centros[i] - rx / 2, cy - ry / 2, rx, ry, 10);
\t\t\t\t\tctx.fillStyle = activo ? tinta : superficie;
\t\t\t\t\tctx.fill();
\t\t\t\t\tctx.strokeStyle = activo ? tinta : borde;
\t\t\t\t\tctx.lineWidth = activo ? 2.4 : 1.2;
\t\t\t\t\tctx.stroke();

\t\t\t\t\tctx.fillStyle = activo ? variable("--color-surface") : atenuado;
\t\t\t\t\tctx.font = activo ? "600 12px ui-monospace, monospace" : "12px ui-monospace, monospace";
\t\t\t\t\tctx.fillText(estado.rotulo, centros[i], cy + 4);
\t\t\t\t});

\t\t\t\t// Barra de progreso del estado activo: hace visible el plazo.
\t\t\t\tconst actual = ESTADOS[indice];
\t\t\t\tconst fraccion = Math.min(1, transcurrido / actual.plazo);
\t\t\t\tconst bx = 150;
\t\t\t\tconst bw = 600;
\t\t\t\tconst by = 296;
\t\t\t\tctx.fillStyle = borde;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.roundRect(bx, by, bw, 10, 5);
\t\t\t\tctx.fill();
\t\t\t\tctx.fillStyle = variable(actual.tinta);
\t\t\t\tctx.beginPath();
\t\t\t\tctx.roundRect(bx, by, Math.max(6, bw * fraccion), 10, 5);
\t\t\t\tctx.fill();

\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "12px system-ui";
\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.fillText("plazo del estado activo", bx, by - 10);
\t\t\t\tctx.textAlign = "right";
\t\t\t\tctx.fillText(`${coma(actual.plazo / 1000, 0)} s`, bx + bw, by - 10);

\t\t\t\tif (pendiente) {
\t\t\t\t\tctx.fillStyle = variable("--color-accent");
\t\t\t\t\tctx.textAlign = "center";
\t\t\t\t\tctx.font = "600 12px system-ui";
\t\t\t\t\tctx.fillText("solicitud peatonal pendiente", w / 2, 26);
\t\t\t\t}
\t\t\t}

\t\t\tfunction cuadro(ahora) {
\t\t\t\tlet transcurrido = ahora - entrada;
\t\t\t\tif (avanzar(transcurrido)) {
\t\t\t\t\tentrada = ahora;
\t\t\t\t\ttranscurrido = 0;
\t\t\t\t}

\t\t\t\tconst actual = ESTADOS[indice];
\t\t\t\tconst cumple = transcurrido >= actual.plazo;
\t\t\t\tsalidaEstado.textContent = actual.rotulo;
\t\t\t\tsalidaTiempo.textContent = `${coma(transcurrido / 1000, 1)} s`;
\t\t\t\tsalidaGuarda.textContent =
\t\t\t\t\tactual.id === "VERDE_VEHICULOS" ? (cumple ? "sí" : "no") : "—";
\t\t\t\tsalidaSolicitud.textContent = pendiente ? "pendiente" : "ninguna";
\t\t\t\titemGuarda.classList.toggle("metric__item--ok", actual.id === "VERDE_VEHICULOS" && cumple);
\t\t\t\titemSolicitud.classList.toggle("metric__item--warn", pendiente);

\t\t\t\tdibujar(transcurrido);
\t\t\t\trequestAnimationFrame(cuadro);
\t\t\t}

\t\t\tdocument.getElementById("fsm-pulsar").addEventListener("click", () => {
\t\t\t\t// Solo el estado VERDE atiende la pulsación; en los otros dos la
\t\t\t\t// tabla dice «ignorar», y eso es lo que ocurre aquí.
\t\t\t\tif (ESTADOS[indice].id === "VERDE_VEHICULOS") pendiente = true;
\t\t\t});
\t\t\tdocument.getElementById("fsm-reiniciar").addEventListener("click", () => {
\t\t\t\tindice = 0;
\t\t\t\tpendiente = false;
\t\t\t\tentrada = performance.now();
\t\t\t});

\t\t\trequestAnimationFrame(cuadro);
\t\t</script>
""",
)

# ────────────────────────────────────────────── 07 · tabla de transiciones
lamina(
    "tabla-transiciones",
    "La tabla de transiciones como diseño y como prueba · Sesión 5",
    "Tabla de transiciones",
    envolver(f"""{cabecera(A, "La tabla de transiciones como diseño y como prueba", "i-target")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Cada fila es un caso de prueba.</strong> La tabla enumera el
\t\t\t\t\tproducto de estados por eventos, de modo que una casilla vacía es una
\t\t\t\t\tsituación cuyo comportamiento nadie ha decidido.
\t\t\t\t</p>

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<th>Estado actual</th>
\t\t\t\t\t\t\t\t<th>Evento</th>
\t\t\t\t\t\t\t\t<th>Guarda</th>
\t\t\t\t\t\t\t\t<th>Estado siguiente</th>
\t\t\t\t\t\t\t\t<th>Acción</th>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><code>VERDE_VEHICULOS</code></td>
\t\t\t\t\t\t\t\t<td><code>PULSADOR</code></td>
\t\t\t\t\t\t\t\t<td><code>t ≥ 8 s</code></td>
\t\t\t\t\t\t\t\t<td><code>AMBAR</code></td>
\t\t\t\t\t\t\t\t<td>arrancar temporizador de 3 s</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><code>VERDE_VEHICULOS</code></td>
\t\t\t\t\t\t\t\t<td><code>PULSADOR</code></td>
\t\t\t\t\t\t\t\t<td><code>t &lt; 8 s</code></td>
\t\t\t\t\t\t\t\t<td><code>VERDE_VEHICULOS</code></td>
\t\t\t\t\t\t\t\t<td>registrar solicitud pendiente</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><code>AMBAR</code></td>
\t\t\t\t\t\t\t\t<td><code>PULSADOR</code></td>
\t\t\t\t\t\t\t\t<td>—</td>
\t\t\t\t\t\t\t\t<td><code>AMBAR</code></td>
\t\t\t\t\t\t\t\t<td>ignorar</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><code>AMBAR</code></td>
\t\t\t\t\t\t\t\t<td><code>VENCE_TEMP</code></td>
\t\t\t\t\t\t\t\t<td>—</td>
\t\t\t\t\t\t\t\t<td><code>ROJO_CON_PASO</code></td>
\t\t\t\t\t\t\t\t<td>arrancar temporizador de 10 s</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><code>ROJO_CON_PASO</code></td>
\t\t\t\t\t\t\t\t<td><code>PULSADOR</code></td>
\t\t\t\t\t\t\t\t<td>—</td>
\t\t\t\t\t\t\t\t<td><code>ROJO_CON_PASO</code></td>
\t\t\t\t\t\t\t\t<td>ignorar: ya está atendida</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><code>ROJO_CON_PASO</code></td>
\t\t\t\t\t\t\t\t<td><code>VENCE_TEMP</code></td>
\t\t\t\t\t\t\t\t<td>—</td>
\t\t\t\t\t\t\t\t<td><code>VERDE_VEHICULOS</code></td>
\t\t\t\t\t\t\t\t<td>borrar solicitud pendiente</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Por qué se redacta completa</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tCon 3 estados y 2 eventos hay <b>6 combinaciones</b>, y las seis están
\t\t\t\t\t\ten la tabla. Las filas cuya acción es <em>ignorar</em> son tan necesarias
\t\t\t\t\t\tcomo las demás: dejan constancia de que la situación se consideró y se
\t\t\t\t\t\tdecidió. Una casilla ausente no significa que el evento no llegue,
\t\t\t\t\t\tsignifica que el programa hará algo que nadie especificó.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-target",
)

# ─────────────────────────────────────── 08 · La hora del código · 20
lamina(
    "codigo-20-semaforo-peatonal",
    "Código 20 · Semáforo con paso peatonal · Sesión 5",
    "La hora del código · Semáforo peatonal",
    hora_del_codigo(
        20,
        "Semáforo con paso peatonal controlado por una máquina de estados",
        "Un cruce con paso peatonal resuelto con tres estados. El pulsador no acorta el verde: una guarda de "
        "tiempo mínimo decide si la solicitud se atiende ahora o queda pendiente hasta que se cumpla el plazo. "
        "Es la tabla de transiciones de la lámina anterior llevada a firmware, sin una sola pausa en el bucle.",
        "<b><code>enum class</code></b> declara un tipo con un conjunto cerrado de valores: el compilador rechaza "
        "cualquier otro, y ahí se acaban los estados inventados sobre la marcha. <b><code>millis()</code></b> "
        "devuelve los milisegundos transcurridos desde el arranque; guardando el instante de entrada al estado y "
        "restándolo, el tiempo pasa a ser una condición más y el bucle nunca se detiene. Una <b>guarda</b> es "
        "justamente esa condición: la transición solo ocurre si se cumple, y si no, el evento espera o se descarta.",
        "El <b>ESP32</b> controla cinco LED: los tres de vehículos en los <b>GPIO 25, 26 y 27</b> y los dos de "
        "peatones en los <b>GPIO 32 y 33</b>, cada uno con su resistencia de 220 Ω a masa. El pulsador de "
        "solicitud va entre el <b>GPIO 4</b> y masa, declarado <code>INPUT_PULLUP</code>.",
        """[SETUP] verde_min=8000  ambar=3000  paso=10000 ms
[EVENTO] t=3410   PULSADOR  guarda t&gt;=8000 -&gt; pendiente
[ESTADO] t=8001   VERDE_VEHICULOS -&gt; AMBAR
[ESTADO] t=11001  AMBAR -&gt; ROJO_CON_PASO
[EVENTO] t=13750  PULSADOR en ROJO_CON_PASO -&gt; ignorar
[ESTADO] t=21001  ROJO_CON_PASO -&gt; VERDE  solicitud borrada""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Declara un <code>enum class Estado</code> con VERDE_VEHICULOS, AMBAR y ROJO_CON_PASO, y una sola variable de ese tipo. El bucle lee el pulsador, calcula el evento y resuelve la transición en un <code>switch</code>. Prohibido <code>delay()</code> y prohibido añadir banderas salvo una para la solicitud peatonal. El verde dura un mínimo de 8000 ms aunque se pulse antes; el ámbar, 3000 ms; el paso, 10000 ms. Imprime a 115200 baudios una línea [ESTADO] por transición y una [EVENTO] por pulsación, con la guarda evaluada.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los cinco LED en los GPIO indicados y el pulsador entre el GPIO 4 y GND.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una vuelta del bucle: leer entradas, calcular el evento, evaluar la guarda, transitar o no. Y el <b>diagrama de estados</b> con los tres estados, el inicial marcado y cada flecha rotulada <code>evento [guarda] / acción</code>.""",
        "Comparar las dos líneas <code>[EVENTO]</code>. La de los 3410 ms encuentra la guarda sin cumplir y la "
        "solicitud queda <b>pendiente</b>; la de los 13 750 ms llega con el paso ya concedido y se <b>ignora</b>. "
        "Entre aplazar y descartar está la diferencia que la tabla declara. Comprobar además que entre dos líneas "
        "<code>[ESTADO]</code> consecutivas nunca transcurre menos de lo que fija <code>[SETUP]</code>: si "
        "transcurriera, la guarda no se está evaluando y el pulsador estaría cortando el verde.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="yellow"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="black"></wokwi-pushbutton></span>\n\t\t\t\t\t\t\t\t\t'
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

# ────────────────────────────────────────────── 09 · rutas de excepción
lamina(
    "rutas-excepcion",
    "Rutas de excepción: evento ausente, repetido o inesperado · Sesión 5",
    "Rutas de excepción",
    envolver(f"""{cabecera(A, "Rutas de excepción: evento ausente, repetido o inesperado", "i-alert")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Tres situaciones que el diagrama nominal no cubre.</strong> Las
\t\t\t\t\ttres ocurren en operación normal, no solo ante un fallo.
\t\t\t\t</p>

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">
\t\t\t\t\t\t\t{ico("i-clock")}
\t\t\t\t\t\t\tEl evento esperado no llega
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn portón que ordena abrir y nunca recibe el fin de carrera queda
\t\t\t\t\t\t\t\ten <code>ABRIENDO</code> de forma indefinida, con el motor
\t\t\t\t\t\t\t\talimentado.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Tratamiento:</b> todo estado transitorio lleva un plazo máximo.
\t\t\t\t\t\t\t\tSu vencimiento es un evento que conduce a un estado de error, no
\t\t\t\t\t\t\t\tuna condición que se comprueba aparte.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">
\t\t\t\t\t\t\t{ico("i-bolt")}
\t\t\t\t\t\t\tEl evento llega repetido
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn pulsador sin filtrado produce siete eventos por pulsación; una
\t\t\t\t\t\t\t\ttrama de red retransmitida llega dos veces.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Tratamiento:</b> la transición debe ser idempotente. Recibir el
\t\t\t\t\t\t\t\tmismo evento dos veces en el mismo estado produce el mismo
\t\t\t\t\t\t\t\tresultado que recibirlo una vez.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">
\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\tEl evento llega en un estado no previsto
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLlega el fin de carrera de apertura mientras la máquina está
\t\t\t\t\t\t\t\tcerrando: o el sensor falla, o el modelo no representa la realidad.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Tratamiento:</b> la rama por defecto del <code>switch</code>
\t\t\t\t\t\t\t\tregistra el par estado-evento por el puerto serie. Ignorarlo en
\t\t\t\t\t\t\t\tsilencio elimina la única pista del fallo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="practice" data-animate="fade-up">
\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\tComprobación obligatoria
\t\t\t\t\t</div>
\t\t\t\t\t<p>
\t\t\t\t\t\tPor cada estado transitorio del diagrama debe existir una fila de la
\t\t\t\t\t\ttabla cuyo evento sea el vencimiento del plazo máximo. Si un estado no
\t\t\t\t\t\ttiene esa fila, el dispositivo puede quedarse en él para siempre, y esa
\t\t\t\t\t\tes una avería que ningún ensayo de corta duración revela.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────── 10 · estados de error y recuperación
lamina(
    "estados-error-recuperacion",
    "Estados de error y rutas de recuperación · Sesión 5",
    "Estados de error y recuperación",
    envolver(f"""{cabecera(A, "Estados de error y rutas de recuperación", "i-alert")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>estado de error</b> es un estado más del modelo, con sus
\t\t\t\t\t\t\t\tsalidas declaradas y sus transiciones de salida. No es una
\t\t\t\t\t\t\t\tcondición excepcional tratada fuera de la máquina.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSus salidas fijan el sistema en una situación segura: motor
\t\t\t\t\t\t\t\tdetenido, válvula cerrada, calefactor sin alimentación. Esa
\t\t\t\t\t\t\t\tcondición se decide al diseñar, no al depurar.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa ausencia de estados de error y de recuperación es la carencia
\t\t\t\t\t\t\t\tmás frecuente en las primeras implementaciones, y es la que
\t\t\t\t\t\t\t\tdistingue un prototipo de un dispositivo utilizable. Un prototipo
\t\t\t\t\t\t\t\tfunciona mientras todo ocurre en el orden previsto.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Detección</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Vence el plazo máximo del estado transitorio, o llega un evento imposible en el estado actual.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">ERROR</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Acción de entrada: llevar las salidas a la condición segura y registrar la causa por el puerto serie.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">→</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Recuperación</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Reintento con número de intentos acotado, o rearme manual. Sin ruta de salida, el error equivale a una avería permanente.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[ERROR] t=42310  estado=ABRIENDO  causa=PLAZO_EXCEDIDO (12000 ms)
[ERROR] t=42310  salidas seguras: motor=0 freno=1
[ERROR] t=42310  reintento 1 de 3
[ESTADO] t=44310 ERROR -&gt; ABRIENDO</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Criterio de diseño</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tUn estado de error sin transición de salida detiene el dispositivo
\t\t\t\t\t\thasta que alguien lo reinicie. Es aceptable cuando la intervención
\t\t\t\t\t\thumana es obligatoria por seguridad, y no lo es cuando el equipo debe
\t\t\t\t\t\toperar sin vigilancia. La decisión pertenece al requisito, y por eso
\t\t\t\t\t\tfigura en el diagrama antes de escribir el código.
\t\t\t\t\t</p>
\t\t\t\t</div>"""),
    icono="i-alert",
)


# ──────────────────────────────────── 11 · artículo · diálisis peritoneal
lamina(
    "paper-fsm-dialisis",
    "Alcance de la tabla de transiciones en un equipo con requisitos de seguridad · Sesión 5",
    "Artículo · Máquina de estados en equipo médico",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Baroudi, W. A.; Alnahdi, F. B.; Aljohani, R. S. et al.</b> (2025). State machine design for an "
        "automated peritoneal dialysis machine. <i>Frontiers in Medical Technology</i> 7. "
        "<code>10.3389/fmedt.2025.1630829</code>",
        "Alcance de la tabla de transiciones en un equipo con requisitos de seguridad",
        ["Especificar por completo una <b>máquina de diálisis peritoneal</b> antes de construirla.",
         "Las etapas de llenado, permanencia y drenaje <b>no pueden solaparse ni invertirse</b>.",
         "La máquina de estados se plantea como la representación que fija ese orden de forma verificable."],
        ["<b>16 entradas y 18 salidas</b>; el estado en <b>cinco biestables</b>.",
         "Estado y entradas dan <b>2²¹ = 2 097 152</b> casos, que la tabla organiza por filas.",
         "La alarma de error es <b>un estado más</b>, con código 11111 reservado.",
         "Los códigos 10001 a 11110 quedan declarados <b>no alcanzables</b>."],
        ["Permite garantizar que las etapas se ejecutan <b>en el orden previsto</b>.",
         "Declarar lo no alcanzable obliga a decidirlo, en vez de dejarlo como residuo.",
         "Enumerar dos millones de casos a mano no es viable: la tabla se levanta por reglas."],
        [("paper-fsm-combinaciones",
          "Elaboración propia con las cifras del artículo. Cada entrada añadida <b>duplica</b> la tabla: de ahí los 2 097 152 casos."),
         ("paper-fsm-codigos",
          "Los 32 códigos que dan cinco biestables, repartidos en los tres grupos que el diseño declara.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────── 12 · implementación con enumerado y switch
lamina(
    "implementacion-enum-switch",
    "Implementación con tipo enumerado y selección múltiple · Sesión 5",
    "Implementación con enumerado y switch",
    envolver(f"""{cabecera(B, "Implementación con tipo enumerado y selección múltiple", "i-keyboard")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tForma de referencia
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl estado se declara como <code>enum class</code> y el bucle
\t\t\t\t\t\t\t\tresuelve la transición en un <code>switch</code> con un
\t\t\t\t\t\t\t\t<code>case</code> por estado. Es la forma de referencia hasta unos
\t\t\t\t\t\t\t\tdiez estados; por encima de esa escala conviene la tabla en memoria
\t\t\t\t\t\t\t\tde la lámina siguiente.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tPor qué <code>enum class</code> y no <code>#define</code>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCon <code>enum class</code> el compilador rechaza asignar un entero
\t\t\t\t\t\t\t\ta la variable de estado y, con
\t\t\t\t\t\t\t\t<code>-Wswitch</code> activo, advierte de todo <code>case</code>
\t\t\t\t\t\t\t\tque falte. Una constante numérica no ofrece ninguna de las dos
\t\t\t\t\t\t\t\tcomprobaciones, y ambas son gratuitas.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">estructura mínima completa</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>enum class Estado : uint8_t {{ VERDE, AMBAR, ROJO }};
<span class="hl hl--hit">Estado estado = Estado::VERDE;   // estado inicial declarado</span>

void loop() {{
  Evento e = leerEvento();       // entradas → evento
  Estado anterior = estado;

  switch (estado) {{              // una rama por estado
    case Estado::VERDE:
      if (e == Evento::PULSADOR &amp;&amp; millis() - tEntrada &gt;= 8000)
        estado = Estado::AMBAR;
      break;
    case Estado::AMBAR: /* … */ break;
    case Estado::ROJO:  /* … */ break;
  }}

  <span class="hl hl--add">if (estado != anterior) {{     // acciones de entrada, una vez</span>
  <span class="hl hl--add">  tEntrada = millis(); aplicarSalidas(estado);</span>
  <span class="hl hl--add">}}</span>
}}</code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-keyboard",
)

# ─────────────────────────────────────── 13 · La hora del código · 21
lamina(
    "codigo-21-porton-automatico",
    "Código 21 · Portón automático con detección de obstáculo · Sesión 5",
    "La hora del código · Portón automático",
    hora_del_codigo(
        21,
        "Portón automático con plazo máximo y detección de obstáculo",
        "Un portón motorizado con cinco estados, dos de ellos transitorios y uno de error. Cada maniobra lleva un "
        "plazo máximo: si el fin de carrera no llega a tiempo, la máquina no se queda esperando de forma "
        "indefinida con el motor alimentado, sino que pasa a un estado con las salidas apagadas.",
        "Un <b>estado transitorio</b> se abandona por un suceso externo que puede no llegar nunca; por eso "
        "necesita <b>plazo máximo</b>, un temporizador que al vencer produce su propio evento. Las <b>acciones de "
        "entrada</b> se ejecutan una sola vez al llegar al estado, no en cada vuelta. La <b>rama por defecto</b> "
        "del <code>switch</code> recoge el par estado-evento que nadie previó.",
        "El <b>ESP32</b> lee los fines de carrera en los <b>GPIO 18 y 19</b> y la barrera en el <b>GPIO 21</b>, "
        "los tres <code>INPUT_PULLUP</code>. El motor son dos LED en los <b>GPIO 25 y 26</b> y la luz de error "
        "va en el <b>GPIO 27</b>.",
        """[SETUP] estado=CERRADO  plazo_max=12000 ms
[ESTADO] t=2140   CERRADO -&gt; ABRIENDO   abre=1 cierra=0
[ESTADO] t=7602   ABRIENDO -&gt; ABIERTO   causa=FIN_CARRERA (5462 ms)
[ESTADO] t=12610  ABIERTO -&gt; CERRANDO   abre=0 cierra=1
[EVENTO] t=15330  BARRERA  estado=CERRANDO -&gt; ABRIENDO (invierte)
[ERROR]  t=27331  PLAZO_EXCEDIDO en ABRIENDO  abre=0 cierra=0""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Declara el estado como <code>enum class</code> con los cinco valores indicados. Los estados ABRIENDO y CERRANDO llevan un plazo máximo de 12000 ms; al vencer, la máquina pasa a ERROR, cuya acción de entrada apaga las dos salidas del motor y enciende la luz de error. La barrera activa durante CERRANDO transita a ABRIENDO. Desde ERROR se sale solo con una pulsación larga del fin de carrera de cierre. La rama por defecto del switch registra el par estado-evento no previsto.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los tres pulsadores y los tres LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del bucle, con el vencimiento del plazo como una comprobación más entre las entradas. Y el <b>diagrama de estados</b> con los cinco estados y las flechas al estado de error dibujadas desde los dos transitorios.""",
        "Restar los instantes de las dos últimas líneas: la máquina entró en ABRIENDO a los 15 330 ms y el error "
        "salta a los 27 331, exactamente <b>12 001 ms</b> después. Ese cálculo comprueba que el plazo se mide desde "
        "la entrada al estado y no desde el arranque. Mirar después qué salidas quedan tras <code>[ERROR]</code>: "
        "si alguna sigue en 1, el motor continúa alimentado.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="green"></wokwi-pushbutton></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
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

# ─────────────────────────── 14 · implementaciones alternativas
lamina(
    "implementaciones-alternativas",
    "Tabla en memoria y punteros a función · Sesión 5",
    "Tabla en memoria y punteros a función",
    envolver(f"""{cabecera(B, "Tabla en memoria y punteros a función", "i-layers")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Dos alternativas al <code>switch</code>.</strong> Ambas cuestan
\t\t\t\t\tmás de escribir y solo se justifican cuando el número de estados hace
\t\t\t\t\tilegible la selección múltiple.
\t\t\t\t</p>

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Tabla de transiciones en memoria</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa tabla de diseño se traslada a un arreglo de estructuras. Buscar la
\t\t\t\t\t\t\tfila que corresponde al par estado-evento sustituye al
\t\t\t\t\t\t\t<code>switch</code>.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<pre><code>struct Fila {{
  Estado desde; Evento ev; Estado hasta; void (*accion)();
}};
const Fila TABLA[] PROGMEM = {{
  {{Estado::VERDE, Evento::PULSADOR,   Estado::AMBAR, arrancarAmbar}},
  {{Estado::AMBAR, Evento::VENCE_TEMP, Estado::ROJO,  arrancarPaso }},
}};</code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Ventaja:</b> la tabla del diseño y la del código son el mismo
\t\t\t\t\t\t\tobjeto, de modo que no pueden divergir. Con
\t\t\t\t\t\t\t<code>PROGMEM</code> reside en Flash y no ocupa SRAM.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Punteros a función por estado</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada estado es una función, y una variable de tipo puntero apunta a
\t\t\t\t\t\t\tla del estado activo. La transición reasigna ese puntero.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<pre><code>void (*estadoActual)(Evento);

void enVerde(Evento e) {{
  if (e == Evento::PULSADOR) estadoActual = enAmbar;
}}
void loop() {{ estadoActual(leerEvento()); }}</code></pre>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\t<b>Ventaja:</b> cada estado queda aislado en su propia función, lo
\t\t\t\t\t\t\tque facilita añadir estados sin tocar los existentes.
\t\t\t\t\t\t\t<b>Costo:</b> el flujo deja de leerse en un solo punto y la
\t\t\t\t\t\t\ttraza de retorno resulta menos informativa.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Cuál se elige</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tEl <code>switch</code> hasta unos <b>diez estados</b>, que cubre todos
\t\t\t\t\t\tlos ejemplos de este curso. La <b>tabla en memoria</b> cuando el
\t\t\t\t\t\tnúmero de filas crece y conviene generarla o revisarla como dato. Los
\t\t\t\t\t\t<b>punteros a función</b> cuando cada estado tiene lógica extensa
\t\t\t\t\t\tpropia. Adoptar la tercera forma en un problema de tres estados añade
\t\t\t\t\t\tindirección sin resolver ningún problema real.
\t\t\t\t\t</p>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ───────────────────────────────── 15 · máquinas no bloqueantes
lamina(
    "maquinas-no-bloqueantes",
    "El vencimiento del temporizador como evento del modelo · Sesión 5",
    "El temporizador como evento",
    envolver(f"""{cabecera(B, "El vencimiento del temporizador como evento del modelo", "i-clock")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna máquina es <b>no bloqueante</b> cuando ninguna de sus
\t\t\t\t\t\t\t\ttransiciones detiene el bucle. El paso del tiempo se observa
\t\t\t\t\t\t\t\tcomparando <code>millis()</code> contra la marca de entrada al
\t\t\t\t\t\t\t\testado, y su vencimiento es un evento igual que cualquier otro.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>millis()</code> devuelve un <code>unsigned long</code> de 32
\t\t\t\t\t\t\t\tbits que desborda a los <b>49,7 días</b>. La resta
\t\t\t\t\t\t\t\t<code>millis() - tEntrada</code> sigue dando el valor correcto tras
\t\t\t\t\t\t\t\tel desbordamiento porque la aritmética sin signo es modular; la
\t\t\t\t\t\t\t\tcomparación <code>millis() &gt; tEntrada + plazo</code> no lo hace.
\t\t\t\t\t\t\t\tPor eso la forma con resta es la única admisible.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Consecuencia sobre el modelo</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCuando el plazo es un evento, aparece en la tabla de transiciones y
\t\t\t\t\t\t\t\tse verifica como los demás. Cuando es un <code>delay()</code>, no
\t\t\t\t\t\t\t\testá en ninguna parte del modelo y sus efectos solo se descubren en
\t\t\t\t\t\t\t\tejecución.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--no">Así no</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">el bucle se detiene</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>case Estado::AMBAR:
  digitalWrite(PIN_AMBAR, HIGH);
  <span class="hl hl--hit">delay(3000);   // 3 s sin leer entradas ni atender nada</span>
  estado = Estado::ROJO;
  break;</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--si">Así sí</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">el plazo es un evento</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>case Estado::AMBAR:
  <span class="hl hl--add">if (millis() - tEntrada &gt;= 3000)   // resta, no suma</span>
    estado = Estado::ROJO;
  break;</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tCon <code>delay(3000)</code> el bucle ejecuta unas 0,3 iteraciones
\t\t\t\t\t\t\t\tpor segundo durante el ámbar; con la comparación, mantiene las
\t\t\t\t\t\t\t\tdecenas de miles habituales. La diferencia es la que decide si el
\t\t\t\t\t\t\t\tpulsador se atiende o se pierde.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-clock",
)

# ─────────────────────────────────────── 16 · La hora del código · 22
lamina(
    "codigo-22-cargador-etapas",
    "Código 22 · Cargador de batería por etapas · Sesión 5",
    "La hora del código · Cargador por etapas",
    hora_del_codigo(
        22,
        "Cargador de batería por etapas con guardas sobre la medida",
        "Un cargador que recorre cuatro etapas, pero cuyas transiciones no las decide el reloj sino una magnitud "
        "medida. Es el caso donde una condición mal escrita hace conmutar la máquina decenas de veces por segundo "
        "sin que nada del circuito haya cambiado.",
        "Una <b>guarda sobre una medida</b> compara una lectura con un umbral. Con un solo umbral, el ruido la "
        "cruza en los dos sentidos sin parar; con <b>histéresis</b> se usan dos umbrales separados, uno para "
        "entrar y otro para salir, y el cambio deja de repetirse. <b>Promediar</b> varias lecturas ataca el mismo "
        "problema en su origen: el conversor del ESP32 tiene dispersión para cruzar un umbral él solo.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> que hace de tensión de celda, ajustado para "
        "cubrir de 3,0 V a 4,3 V. Tres LED de etapa en los <b>GPIO 25, 26 y 27</b> con resistencia de 220 Ω.",
        """[SETUP] etapa=CORRIENTE_CONSTANTE  v_paso=4.200  hist=0.030 V
[MEDIDA] t=1000  v=3.712 V  etapa=CORR_CONST  i_lim=500 mA
[MEDIDA] t=8000  v=4.198 V  guarda v&gt;=4.200 -&gt; NO
[ESTADO] t=9000  CORR_CONST -&gt; TENSION_CONST  v=4.203 V
[MEDIDA] t=21000 v=4.201 V  etapa=TENSION_CONST  i=48 mA
[ESTADO] t=34000 TENSION_CONST -&gt; MANTENIMIENTO  i=24 &lt; 25 mA
[ERROR]  t=41200 SOBRETENSION v=4.412 V  carga=0""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Declara las cuatro etapas como <code>enum class</code>. La transición de CORRIENTE_CONSTANTE a TENSION_CONSTANTE ocurre cuando la tensión medida supera 4,200 V; la de TENSION_CONSTANTE a MANTENIMIENTO, cuando la corriente estimada baja de 25 mA. Aplica una histéresis de 30 mV en ambas guardas. Cualquier medida por encima de 4,350 V lleva a ERROR de forma inmediata, con la salida de carga apagada y sin retorno automático. Promedia 16 lecturas del ADC antes de evaluar la guarda. Imprime a 115200 baudios una línea [MEDIDA] por segundo y una [ESTADO] en cada transición.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y los tres LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de la secuencia medir, promediar, comparar contra la guarda y transitar. Y el <b>diagrama de estados</b> donde cada flecha lleve escrita su guarda con el valor numérico y la histéresis aplicada.""",
        "Mirar la línea <code>[MEDIDA]</code> de los 8000 ms: <b>v = 4,198 V</b> y la guarda responde NO aunque el "
        "umbral sea 4,200. Dos milivoltios deciden. En la traza propia hay que buscar lo contrario: varias líneas "
        "<code>[ESTADO]</code> seguidas en el mismo instante significan que la histéresis no se aplica y la "
        "máquina conmuta con el ruido de la medida.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="orange"></wokwi-led></span>'
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

# ────────────────────────────── 17 · varias máquinas en un mismo bucle
lamina(
    "varias-maquinas-un-bucle",
    "Coexistencia de máquinas independientes en el mismo bucle · Sesión 5",
    "Varias máquinas en un mismo bucle",
    envolver(f"""{cabecera(B, "Coexistencia de máquinas independientes en el mismo bucle", "i-layers")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tPrincipio
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCada actividad con su propio ritmo lleva su propia máquina, con su
\t\t\t\t\t\t\t\tvariable de estado y su timestamp. El bucle las evalúa todas
\t\t\t\t\t\t\t\ten cada iteración, y ninguna bloquea a las demás.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tEjemplo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn equipo con tres actividades: muestrear un sensor cada 100 ms,
\t\t\t\t\t\t\t\tparpadear un indicador cada 500 ms y atender un pulsador con
\t\t\t\t\t\t\t\tpulsación larga. Tres máquinas, tres variables de estado, un solo
\t\t\t\t\t\t\t\tbucle.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl límite aparece cuando dos actividades tienen requisitos
\t\t\t\t\t\t\t\ttemporales incompatibles: una necesita responder en 1 ms y otra
\t\t\t\t\t\t\t\tocupa 40 ms por iteración. Ahí el bucle único deja de bastar, y esa
\t\t\t\t\t\t\t\tes la condición que justifica las tareas de la sesión 6.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--si">Así sí</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">tres máquinas, un bucle</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>void loop() {{
  uint32_t ahora = millis();
  <span class="hl hl--add">maquinaSensor(ahora);     // estado propio, marca propia</span>
  <span class="hl hl--add">maquinaIndicador(ahora);</span>
  <span class="hl hl--add">maquinaPulsador(ahora);</span>
}}
// Cada función es un switch sobre SU variable de estado.
// Ninguna espera: todas retornan en microsegundos.</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="blockdiagram">
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Sensor</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--ok"><span class="bd-node__body">REPOSO ⇄ MIDIENDO · periodo 100 ms</span></div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Indicador</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost"><span class="bd-node__body">ENCENDIDO ⇄ APAGADO · periodo 500 ms</span></div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="bd-lane">
\t\t\t\t\t\t\t\t<span class="bd-lane__label">Pulsador</span>
\t\t\t\t\t\t\t\t<div class="bd-node bd-node--accent"><span class="bd-node__body">SUELTO → PULSADO → LARGA · umbral 1200 ms</span></div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tLas tres máquinas comparten el bucle pero no comparten estado: la
\t\t\t\t\t\t\tpulsación larga no altera el periodo de muestreo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ──────────────────────────────────────── 18 · máquinas jerárquicas
lamina(
    "maquinas-jerarquicas",
    "Estados que contienen su propia máquina · Sesión 5",
    "Máquinas jerárquicas",
    envolver(f"""{cabecera(B, "Estados que contienen su propia máquina", "i-layers")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tDefinición
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>statechart (máquina de estados jerárquica)</b> admite que un estado
\t\t\t\t\t\t\t\tcontenga a su vez una máquina completa. El estado exterior atiende
\t\t\t\t\t\t\t\tlos eventos comunes a todos sus subestados; el interior, los suyos
\t\t\t\t\t\t\t\tpropios.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Qué problema resuelve</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEvita repetir una misma transición en cada estado. Si la pérdida de
\t\t\t\t\t\t\t\tenlace debe llevar a <code>DESCONECTADO</code> desde los cuatro
\t\t\t\t\t\t\t\tsubestados de operación, en una máquina plana son cuatro flechas
\t\t\t\t\t\t\t\tidénticas que pueden divergir al modificarse; en una jerárquica es
\t\t\t\t\t\t\t\t<b>una sola</b>, dibujada sobre el estado que las contiene.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tDos variables de estado, una por nivel, y un <code>switch</code>
\t\t\t\t\t\t\t\tanidado. El nivel exterior se evalúa primero: si su transición se
\t\t\t\t\t\t\t\tdispara, el interior no llega a evaluarse y su variable se
\t\t\t\t\t\t\t\treinicializa al entrar de nuevo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">DESCONECTADO</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Sin enlace. Reintento con backoff exponencial.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↓ enlace establecido</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">CONECTADO</span>
\t\t\t\t\t\t\t\t<span class="bd-node__meta">contiene su propia máquina</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">
\t\t\t\t\t\t\t\t\tSubestados: SINCRONIZANDO_HORA → PUBLICANDO → ESPERANDO_RESPUESTA → REPOSO.
\t\t\t\t\t\t\t\t\tUna sola flecha de salida atiende la pérdida de enlace desde cualquiera de los cuatro.
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">↑ enlace perdido · una única transición</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\tSin jerarquía harían falta cuatro transiciones de pérdida de enlace,
\t\t\t\t\t\t\tuna por subestado, y bastaría olvidar una para dejar el dispositivo
\t\t\t\t\t\t\tpublicando sobre un enlace caído.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ───────────────────────── 19 · artículo · statecharts jerárquicos
lamina(
    "paper-statecharts-jerarquicos",
    "Efecto de la jerarquía sobre la verificabilidad del modelo · Sesión 5",
    "Artículo · Análisis de statecharts jerárquicos",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Kirshin, A.; Moshkovich, D.; Hoppe, A.</b> (2007). Compositional analysis of hierarchical state "
        "machines. <i>IBM Haifa Research Lab</i>. <code>doi:10.1145/1274900.1274918</code>",
        "Efecto de la jerarquía sobre la verificabilidad del modelo",
        ["Ver si un modelo <b>organizado en jerarquía</b> puede analizarse por partes.",
         "Analizarlo completo obliga a recorrer todas las combinaciones de subestados.",
         "Ese número crece de forma <b>multiplicativa</b> con los componentes."],
        ["Batería de <b>27 modelos</b> de complejidad creciente, con plazo de 4 h cada uno.",
         "El análisis plano resolvió <b>2 de 27</b>: los demás se interrumpieron sin resultado.",
         "El compositivo resolvió <b>27 de 27</b>, todos en menos de 30 minutos.",
         "El error que introduce descomponer se mantiene en el orden de <b>10⁻³</b>."],
        ["La jerarquía sustituye un análisis único e inviable por <b>una serie de análisis pequeños</b>.",
         "La ganancia en tiempo <b>no se paga</b> con pérdida de exactitud apreciable.",
         "La jerarquía no solo ordena el diagrama: es lo que hace comprobable el modelo."],
        [("paper-statecharts-escala",
          "Elaboración propia con las cifras publicadas. Modelos que cada procedimiento logró resolver, de 27."),
         ("paper-statecharts-tiempo",
          "Lo que tarda cada uno. El plazo de 4 h del análisis plano no es tiempo de cálculo: es una rendición.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────────── 20 · casos de aplicación
lamina(
    "casos-aplicacion",
    "Cinco sistemas modelados con estados · Sesión 5",
    "Cinco sistemas modelados con estados",
    envolver(f"""{cabecera(B, "Cinco sistemas modelados con estados", "i-target")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>El mismo formalismo en cinco dominios.</strong> Lo que cambia
\t\t\t\t\tentre ellos es el origen del evento, no la estructura del modelo.
\t\t\t\t</p>

\t\t\t\t<div class="table-scroll" data-animate="fade-up">
\t\t\t\t\t<table>
\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<th>Sistema</th>
\t\t\t\t\t\t\t\t<th>Estados</th>
\t\t\t\t\t\t\t\t<th>Origen de los eventos</th>
\t\t\t\t\t\t\t\t<th>Rasgo que lo distingue</th>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</thead>
\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Semáforo con paso peatonal</b></td>
\t\t\t\t\t\t\t\t<td>3</td>
\t\t\t\t\t\t\t\t<td>Pulsador y temporizador</td>
\t\t\t\t\t\t\t\t<td>Guarda de tiempo mínimo que acota la solicitud del peatón</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Máquina expendedora</b></td>
\t\t\t\t\t\t\t\t<td>4</td>
\t\t\t\t\t\t\t\t<td>Monedas, selección y sensor de entrega</td>
\t\t\t\t\t\t\t\t<td>El estado acumula un valor: el crédito forma parte de él</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Portón automático</b></td>
\t\t\t\t\t\t\t\t<td>5</td>
\t\t\t\t\t\t\t\t<td>Fines de carrera, barrera y plazo máximo</td>
\t\t\t\t\t\t\t\t<td>Estado de error alcanzable desde los dos estados transitorios</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Cargador por etapas</b></td>
\t\t\t\t\t\t\t\t<td>4</td>
\t\t\t\t\t\t\t\t<td>Magnitud medida por el ADC</td>
\t\t\t\t\t\t\t\t<td>Guardas con histéresis sobre una medida ruidosa</td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t<td><b>Gestión de la conexión</b></td>
\t\t\t\t\t\t\t\t<td>4 + subestados</td>
\t\t\t\t\t\t\t\t<td>Pila de red y temporizadores de reintento</td>
\t\t\t\t\t\t\t\t<td>Jerarquía: los subestados de operación cuelgan de <code>CONECTADO</code></td>
\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Lo que tienen en común</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tEn los cinco, el número de estados se mantiene por debajo de seis
\t\t\t\t\t\taunque el sistema sea complejo. Cuando un modelo empieza a necesitar
\t\t\t\t\t\tquince estados, casi siempre está mezclando dos máquinas distintas que
\t\t\t\t\t\tconviene separar, o pidiendo jerarquía.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-target",
)

# ─────────────────────────────── 21 · la conexión como máquina
lamina(
    "maquina-conexion-red",
    "La conexión de red modelada como máquina de estados · Sesión 5",
    "La conexión de red como máquina",
    envolver(f"""{cabecera(B, "La conexión de red modelada como máquina de estados", "i-link")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tPor qué se modela así
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tConectarse a una red no es una operación instantánea ni fiable:
\t\t\t\t\t\t\t\ttarda un tiempo variable, puede fallar y puede caerse después de
\t\t\t\t\t\t\t\thaber tenido éxito. Escrita como una espera dentro de
\t\t\t\t\t\t\t\t<code>setup()</code>, ninguna de esas tres situaciones tiene
\t\t\t\t\t\t\t\ttratamiento.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tEn el código
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<code>WiFi.begin()</code> retorna de inmediato y no indica éxito;
\t\t\t\t\t\t\t\tel resultado se consulta con <code>WiFi.status()</code>, que
\t\t\t\t\t\t\t\tdevuelve <code>WL_CONNECTED</code>,
\t\t\t\t\t\t\t\t<code>WL_CONNECT_FAILED</code> o
\t\t\t\t\t\t\t\t<code>WL_DISCONNECTED</code>. Ese valor es el evento que alimenta
\t\t\t\t\t\t\t\tla máquina en cada iteración.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Backoff exponencial entre reintentos</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl estado <code>ESPERANDO_REINTENTO</code> duplica su plazo en cada
\t\t\t\t\t\t\t\tfallo consecutivo, de 1 s a un máximo de 60 s. Reintentar cada
\t\t\t\t\t\t\t\tsegundo de forma indefinida consume energía y satura el punto de
\t\t\t\t\t\t\t\tacceso sin aumentar la probabilidad de éxito.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t\t\t<tr><th>Estado</th><th>Evento</th><th>Siguiente</th></tr>
\t\t\t\t\t\t\t\t</thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><code>DESCONECTADO</code></td><td>arranque</td><td><code>ASOCIANDO</code></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>ASOCIANDO</code></td><td><code>WL_CONNECTED</code></td><td><code>CONECTADO</code></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>ASOCIANDO</code></td><td>plazo 15 s</td><td><code>ESPERANDO_REINTENTO</code></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>ESPERANDO_REINTENTO</code></td><td>vence espera</td><td><code>ASOCIANDO</code></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><code>CONECTADO</code></td><td>enlace perdido</td><td><code>ESPERANDO_REINTENTO</code></td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[RED] t=0      DESCONECTADO -&gt; ASOCIANDO   intento=1
[RED] t=15000  plazo excedido -&gt; ESPERANDO_REINTENTO  espera=1000 ms
[RED] t=16000  ESPERANDO_REINTENTO -&gt; ASOCIANDO  intento=2
[RED] t=31000  plazo excedido -&gt; ESPERANDO_REINTENTO  espera=2000 ms
[RED] t=48200  ASOCIANDO -&gt; CONECTADO  ip=192.168.1.47  rssi=-63 dBm</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-link",
)

# ─────────────────────────────── 22 · registro de transiciones
lamina(
    "registro-transiciones",
    "Registro de transiciones como mecanismo de trazabilidad · Sesión 5",
    "Registro de transiciones",
    envolver(f"""{cabecera(B, "Registro de transiciones como mecanismo de trazabilidad", "i-terminal")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tPrincipio
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tCada transición emite una línea con timestamp, estado de
\t\t\t\t\t\t\t\torigen, evento, guarda evaluada y estado de destino. Al ser la
\t\t\t\t\t\t\t\ttransición el único mecanismo de cambio, esa traza describe por
\t\t\t\t\t\t\t\tcompleto la historia del dispositivo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tFormato de la línea
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn prefijo entre corchetes identifica el módulo, igual que en las
\t\t\t\t\t\t\t\tsesiones anteriores. Los campos se separan con un solo espacio y
\t\t\t\t\t\t\t\tllevan nombre, de modo que la traza puede filtrarse con
\t\t\t\t\t\t\t\t<code>grep</code> y representarse después sin volver a capturarla.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Costo y cuándo se retira</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tImprimir 80 caracteres a 115200 baudios ocupa unos <b>7 ms</b>. Es
\t\t\t\t\t\t\t\tdespreciable con una transición por segundo e inadmisible con cien.
\t\t\t\t\t\t\t\tPor eso el registro se condiciona a una constante de compilación y
\t\t\t\t\t\t\t\tse retira del binario de producción sin tocar el resto del código.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__path">un solo punto de registro</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>constexpr bool TRAZA = true;   // false en producción

void registrar(Estado de, Evento e, Estado a) {{
  if (!TRAZA) return;          // el compilador elimina la llamada
  Serial.printf("[FSM] t=%lu %s --%s--&gt; %s\\n",
                millis(), nombre(de), nombre(e), nombre(a));
}}</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">[FSM] t=8001   VERDE_VEHICULOS --VENCE_MIN--&gt; AMBAR
[FSM] t=11001  AMBAR --VENCE_TEMP--&gt; ROJO_CON_PASO
[FSM] t=13750  ROJO_CON_PASO --PULSADOR--&gt; ROJO_CON_PASO
[FSM] t=21001  ROJO_CON_PASO --VENCE_TEMP--&gt; VERDE_VEHICULOS</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tLa tercera línea documenta una transición hacia el mismo estado. No
\t\t\t\t\t\t\t\tes ruido: deja constancia de que el evento llegó y de que la
\t\t\t\t\t\t\t\tdecisión de ignorarlo fue deliberada.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-terminal",
)

# ─────────────────────────── 23 · verificación sin hardware
lamina(
    "verificacion-sin-hardware",
    "Inyección de eventos por el puerto serie · Sesión 5",
    "Inyección de eventos por el puerto serie",
    envolver(f"""{cabecera(B, "Inyección de eventos por el puerto serie", "i-check")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tProcedimiento
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tSi la función que produce los eventos admite además una fuente por
\t\t\t\t\t\t\t\tel puerto serie, la máquina puede recorrerse entera sin tocar el
\t\t\t\t\t\t\t\thardware. Un carácter por evento basta.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tQué permite comprobar
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tRecorrer las seis filas de la tabla de transiciones toma segundos, y
\t\t\t\t\t\t\t\tpuede repetirse tras cada cambio. Situaciones que exigirían averiar
\t\t\t\t\t\t\t\tun sensor, un fin de carrera que no llega, se provocan sin más que
\t\t\t\t\t\t\t\tno enviar el carácter correspondiente.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Relación con la prueba automatizada</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna secuencia de caracteres y la traza que debe producir constituyen
\t\t\t\t\t\t\t\tun caso de prueba reproducible. Es el primer paso hacia la prueba
\t\t\t\t\t\t\t\tautomatizada del firmware, y no exige más herramientas que el
\t\t\t\t\t\t\t\tmonitor serie.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="codepanel">
\t\t\t\t\t\t\t<div class="codepanel__header">
\t\t\t\t\t\t\t\t<span class="codepanel__tag codepanel__tag--si">Así sí</span>
\t\t\t\t\t\t\t\t<span class="codepanel__path">dos fuentes, un solo evento</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<pre><code>Evento leerEvento() {{
  <span class="hl hl--add">if (Serial.available()) {{        // fuente de ensayo</span>
  <span class="hl hl--add">  switch (Serial.read()) {{</span>
  <span class="hl hl--add">    case 'p': return Evento::PULSADOR;</span>
  <span class="hl hl--add">    case 'a': return Evento::FIN_CARRERA_ABRE;</span>
  <span class="hl hl--add">  }}</span>
  <span class="hl hl--add">}}</span>
  return leerEntradasFisicas();  // fuente real
}}</code></pre>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="term">&gt; p
[FSM] t=1204  VERDE_VEHICULOS --PULSADOR--&gt; VERDE_VEHICULOS  guarda=NO
&gt; p
[FSM] t=9310  VERDE_VEHICULOS --PULSADOR--&gt; AMBAR  guarda=SI
&gt; x
[FSM] t=9800  evento no reconocido: 'x'</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
)

# ─────────────────────────────────────── 24 · La hora del código · 23
lamina(
    "codigo-23-maquina-verificable",
    "Código 23 · Máquina verificable por inyección de eventos · Sesión 5",
    "La hora del código · Máquina verificable",
    hora_del_codigo(
        23,
        "Máquina de conexión verificable por inyección de eventos",
        "La máquina que controla la conexión de red, con backoff exponencial entre reintentos y una fuente de eventos "
        "que se puede accionar a mano desde el monitor serie. Permite recorrer la máquina entera (incluidas las "
        "transiciones de error, que son las que nunca se prueban) sin necesitar un punto de acceso.",
        "<b>Inyectar eventos</b> separa la fuente del suceso de su tratamiento: la función que produce el evento "
        "acepta el estado real de la radio o un carácter tecleado, y la máquina no distingue. La <b>espera "
        "exponencial</b> duplica el tiempo entre reintentos hasta un tope y se reinicia al primer éxito. La "
        "<b>cobertura</b> es la cuenta de cuántas flechas de la tabla se recorrieron de verdad.",
        "El <b>ESP32</b> enciende cuatro LED de estado en los <b>GPIO 25, 26, 27 y 32</b>, cada uno con su "
        "resistencia de 220 Ω. No hace falta más: los eventos de red se inyectan por el monitor serie.",
        """[FSM] t=0     DESCONECTADO --ARRANQUE--&gt; ASOCIANDO  n=1
&gt; f
[FSM] t=2100  ASOCIANDO --FALLO--&gt; ESPERANDO  espera=1000 ms
[FSM] t=3100  ESPERANDO --VENCE--&gt; ASOCIANDO  n=2
&gt; f
[FSM] t=4200  ASOCIANDO --FALLO--&gt; ESPERANDO  espera=2000 ms
&gt; c
[FSM] t=6300  ASOCIANDO --CONECTADO--&gt; CONECTADO  espera=1000 ms
[COBERTURA] 7 de 8; falta CONECTADO--PERDIDA--&gt;ESPERANDO""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Implementa la máquina con los estados DESCONECTADO, ASOCIANDO, ESPERANDO_REINTENTO y CONECTADO. La espera entre reintentos parte de 1000 ms, se duplica en cada fallo consecutivo hasta un máximo de 60000 ms, y vuelve al valor inicial al conectar. La función que produce los eventos acepta caracteres por el puerto serie: 'c' conectado, 'f' fallo, 'p' pérdida de enlace. Lleva la cuenta de qué transiciones de la tabla se han recorrido e imprime una línea [COBERTURA] con las que faltan.

<b>3. Simulación.</b> Añade la simulación de Wokwi con los cuatro LED de estado en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del bucle, con la lectura del puerto serie y la del estado de la radio entrando por el mismo punto. Y el <b>diagrama de estados</b> junto a la tabla de transiciones completa, con una fila por flecha.""",
        "La última línea es el resultado del ejercicio: <b>7 de 8</b> transiciones recorridas, y dice cuál falta. "
        "Provocarla con la tecla 'p' y volver a leerla. Observar además la espera en las dos líneas de "
        "<code>ESPERANDO_REINTENTO</code>, 1000 y luego 2000 ms, y comprobar que vuelve a 1000 al conectar: si se "
        "quedara en 2000, no se está reiniciando y el siguiente corte de red empezaría ya penalizado.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="blue"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="yellow"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-resistor></wokwi-resistor></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
""",
)

# ────────────────────────────────── 25 · artículo · PN2ARDUINO
lamina(
    "paper-pn2arduino",
    "Del modelo gráfico al control ejecutable sobre el microcontrolador · Sesión 5",
    "Artículo · Del modelo gráfico al control",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Riera, D.; Vidal, G.; Yepes, S. et al.</b> (2021). PN2ARDUINO: control de sistemas de eventos "
        "discretos mediante redes de Petri. <i>Revista Iberoamericana de Automática e Informática Industrial</i>. "
        "<code>doi:10.4995/riai.2021.15104</code>",
        "Del modelo gráfico al control ejecutable sobre el microcontrolador",
        ["Controlar un sistema de eventos discretos <b>dibujando su modelo</b> en vez de escribir el control.",
         "Formalismo: <b>redes de Petri</b>, emparentado con las máquinas de estados.",
         "Verificación sobre una maqueta de alarma de incendios con zumbador y fotorresistencia."],
        ["El modelo tiene <b>tres plazas y cinco transiciones</b>: basta para controlar la maqueta.",
         "El disparo se fija en <b>799 de 1023</b>, hallado midiendo y no en una hoja de datos.",
         "Se comparan dos arquitecturas según dónde vive la lógica de control.",
         "Con la lógica fuera, el modelo se cambia <b>sin recompilar</b>."],
        ["El modelo gráfico resulta <b>suficiente</b> para controlar el sistema.",
         "La escala de estos sistemas es pequeña aunque el comportamiento no lo parezca.",
         "Sacar la lógica del microcontrolador se paga con la <b>autonomía</b> del equipo."],
        [("paper-umbral-fotorresistencia",
          "El umbral 799 sobre el recorrido completo del convertidor: la decisión reparte el rango en 78 % y 22 %."),
         ("paper-pn-arquitecturas",
          "El compromiso entre las dos arquitecturas que compara el artículo, propiedad por propiedad.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────── 26 · estado del sistema y de la interfaz
lamina(
    "estado-sistema-vs-interfaz",
    "Separación entre el estado del sistema y el de la interfaz · Sesión 5",
    "Estado del sistema y de la interfaz",
    envolver(f"""{cabecera(B, "Separación entre el estado del sistema y el de la interfaz", "i-layers")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Estado del sistema</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tQué está haciendo el dispositivo: <code>CARGANDO</code>,
\t\t\t\t\t\t\t<code>MANTENIMIENTO</code>, <code>ERROR</code>. Existe aunque no haya
\t\t\t\t\t\t\tnadie mirando y aunque no haya pantalla conectada.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tCambia por eventos físicos y por vencimientos de plazo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Estado de la interfaz</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tQué se está mostrando: <code>PANTALLA_PRINCIPAL</code>,
\t\t\t\t\t\t\t<code>MENU_AJUSTES</code>, <code>CONFIRMANDO_BORRADO</code>. Depende
\t\t\t\t\t\t\tde por dónde navega el usuario.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tCambia por pulsaciones y por tiempos de inactividad.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tUnificar ambos produce estados como
\t\t\t\t\t\t<code>CARGANDO_MOSTRANDO_MENU</code>. El número de estados pasa a ser
\t\t\t\t\t\tel <b>producto</b> de los dos conjuntos, y entrar en un menú deja de
\t\t\t\t\t\tser independiente de lo que hace el equipo: navegar por los ajustes
\t\t\t\t\t\tpodría detener la carga.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Cómo se relacionan</span>
\t\t\t\t\t<p>
\t\t\t\t\t\tSon dos máquinas independientes que se comunican en un solo sentido: la
\t\t\t\t\t\tinterfaz <b>lee</b> el estado del sistema para representarlo, y le envía
\t\t\t\t\t\teventos, <code>SOLICITUD_PARADA</code>, en lugar de escribir su
\t\t\t\t\t\tvariable de estado. Con 4 estados de sistema y 5 de interfaz son
\t\t\t\t\t\t<b>9 estados</b> separados frente a los <b>20</b> del producto.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-layers",
)

# ─────────────────────────────────────── 27 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes al implementar una máquina de estados · Sesión 5",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes al implementar una máquina de estados", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("El estado no avanza nunca", "La máquina entra en un estado temporizado y no sale de él, aunque el plazo se cumpla de sobra.", "El timestamp se actualiza dentro del cuerpo del estado en vez de en la transición, de modo que <code>millis() - tEntrada</code> vale casi cero en cada iteración.", "Registrar el valor de la resta junto al estado: si no crece entre líneas consecutivas, la marca se está reiniciando.", "i-clock")}
{problema("Una salida queda activa de más", "Al cambiar de estado, un LED o un relé permanece encendido pese a que el nuevo estado no lo contempla.", "Las salidas se escriben en cada <code>case</code> por separado, y el nuevo estado solo activa las suyas sin apagar las anteriores.", "Concentrar todas las escrituras en una función <code>aplicarSalidas(estado)</code> que fije el valor de <b>todas</b> las salidas, y llamarla solo tras una transición.", "i-bolt")}
{problema("Un evento se atiende dos veces", "Una sola pulsación provoca dos transiciones encadenadas y la máquina salta un estado.", "El evento se calcula por nivel y no por flanco: mientras el pulsador siga presionado, cada iteración lo vuelve a producir.", "Imprimir el evento en cada iteración: si aparece repetido durante decenas de líneas, se está leyendo nivel en lugar de flanco.", "i-wave")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("La máquina se queda en un estado transitorio", "El dispositivo deja de responder y solo se recupera con un reinicio manual.", "El estado transitorio no tiene plazo máximo, de modo que la ausencia del evento esperado no está contemplada en ninguna fila de la tabla.", "Recorrer la tabla y verificar que todo estado transitorio tiene una fila cuyo evento es el vencimiento del plazo.", "i-target")}
{problema("El número de estados crece sin control", "El diagrama pasa de cinco a quince estados al añadir una función menor.", "Se están mezclando dos máquinas en una, normalmente la del sistema y la de la interfaz, o falta jerarquía.", "Comprobar si los nombres de los estados contienen dos conceptos unidos, como <code>CARGANDO_MOSTRANDO_MENU</code>. Es la señal de que hay dos máquinas.", "i-layers")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 28 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 5 · Sesión 5",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("Estado", "state", "Situación en la que el dispositivo permanece hasta que ocurre un evento. Determina las salidas activas y los eventos que se atienden.")}
{termino("Evento", "event", "Hecho instantáneo observable por el sistema: un flanco en un terminal, el vencimiento de un plazo o la llegada de una trama.")}
{termino("Transición", "transition", "Paso de un estado a otro provocado por un evento. Es el único mecanismo admitido para cambiar de estado.")}
{termino("Condición de guarda", "condición de guarda", "Expresión booleana asociada a una transición. El evento la dispara únicamente si la condición se cumple.")}
{termino("Acción de entrada", "entry action", "Instrucción que se ejecuta una sola vez al llegar a un estado, no en cada iteración del bucle mientras el estado dure.")}
{termino("Modelo de Moore", "Moore machine", "Formalismo en el que las salidas dependen solo del estado activo. Es el que emplea este curso por su lectura directa sobre el diagrama.")}
{termino("Modelo de Mealy", "Mealy machine", "Formalismo en el que las salidas dependen del estado y del evento. Requiere menos estados y responde en el instante del evento.")}
{termino("UML", "Unified Modeling Language", "Lenguaje de modelado normalizado. De su repertorio esta sesión emplea el diagrama de máquina de estados, con flechas rotuladas <code>evento [guarda] / acción</code>.")}
{termino("Statechart", "máquina de estados jerárquica", "Máquina en la que un estado contiene a su vez otra máquina completa. Evita repetir una misma transición en cada subestado.")}
{termino("Tabla de transiciones", "state transition table", "Enumeración de todas las combinaciones de estado y evento con su destino y su acción. Cada fila constituye un caso de prueba.")}
{termino("Máquina no bloqueante", "non-blocking state machine", "Máquina cuyas transiciones no detienen el bucle. El paso del tiempo se observa comparando <code>millis()</code> contra la marca de entrada al estado.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────────────────────── 29 · resumen
lamina(
    "resumen",
    "Resumen de la sesión 5 · Sesión 5",
    "Resumen de la sesión",
    envolver(f"""{cabecera(B, "Lo que queda establecido", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-flow")}Modelado</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUna variable de estado con un número cerrado de valores sustituye al
\t\t\t\t\t\t\tconjunto de banderas. El espacio de situaciones deja de crecer de
\t\t\t\t\t\t\tforma exponencial y pasa a ser enumerable.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tLa tabla de transiciones se redacta completa, incluidas las filas
\t\t\t\t\t\t\tcuya acción es ignorar el evento: dejan constancia de que la
\t\t\t\t\t\t\tsituación se consideró.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-keyboard")}Implementación</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t<code>enum class</code> y <code>switch</code> hasta unos diez
\t\t\t\t\t\t\testados. Las acciones de entrada van en la transición, no en el
\t\t\t\t\t\t\tcuerpo del estado.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl vencimiento de un plazo es un evento del modelo, observado con la
\t\t\t\t\t\t\tresta <code>millis() - tEntrada</code>. Ningún
\t\t\t\t\t\t\t<code>delay()</code> dentro de la máquina.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Lo que se lleva a la sesión siguiente</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Estados de error con ruta de salida</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tTodo estado transitorio lleva plazo máximo; su vencimiento conduce a
\t\t\t\t\t\t\t\tun estado con salidas seguras y recuperación acotada.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-check")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Verificación por inyección de eventos</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tLa tabla es finita, de modo que la cobertura de transiciones puede
\t\t\t\t\t\t\t\tmedirse y comunicarse por el monitor serie.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-cpu")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">El límite del bucle único</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tVarias máquinas conviven en un bucle mientras sus requisitos
\t\t\t\t\t\t\t\ttemporales sean compatibles. La sesión 6 trata el caso en que no lo
\t\t\t\t\t\t\t\tson.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 30 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 5 · Sesión 5",
    "Referencias",
    envolver(f"""{cabecera(B, "Referencias", "i-paper")}

\t\t\t\t<p class="slide__lede" data-animate="fade-up">
\t\t\t\t\t<strong>Los tres artículos son de acceso abierto.</strong> El DOI lleva
\t\t\t\t\tal texto completo sin suscripción.
\t\t\t\t</p>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">State machine design for an automated peritoneal dialysis machine</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Baroudi, W. A.; Alnahdi, F. B.; Aljohani, R. S. et al. (2025). <i>Front. Med. Technol.</i> 7. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3389/fmedt.2025.1630829</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Tabla de transiciones · Estados de error</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Compositional Analysis of Hierarchical UML Statecharts</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Carnevali, L.; German, R.; Santoni, F.; Vicario, E. (2022). <i>IEEE Trans. Softw. Eng.</i> 48(12). CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.1109/TSE.2021.3125720</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Máquinas jerárquicas · Verificación</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">PN2ARDUINO: A New Petri Net Software Tool for Control of Discrete-Event and Hybrid Systems</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Kučera, E.; Haffner, O.; Leskovský, R. (2019). <i>Ann. Comput. Sci. Inf. Syst.</i> 18, 915-919. CC BY-NC-ND 3.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.15439/2019F20</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Notación UML · Del modelo al código</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Archivos y índice del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Los PDF de esta sesión están en <code>src/paper/clase-05/</code>. El índice completo, con licencia y láminas que sostiene cada artículo, en <code>src/paper/INDICE.md</code>.</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Las doce sesiones</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>

{credito("El material del curso; cada artículo citado conserva su propia licencia.")}"""),
    clases="slide",
    icono="i-paper",
)

if __name__ == "__main__":
    _gen.generar_desde(
        {"clase": "clase-05", "sesion": "Sesión 5", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
