#!/usr/bin/env python3
"""Sesión 12 — TinyML y Edge AI: inferencia en microcontroladores.

Ejecutar desde la raíz del proyecto:  python3 tools/clases/clase_12.py
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

A = "01 · Fundamentos y restricciones"
B = "02 · Herramientas y criterios de aplicación"

LAMINAS = []

SENSOR_SCRIPTS = """\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/dht22-element.js";
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/potentiometer-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
"""



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
    "Sesión 12 · TinyML y Edge AI: inferencia en microcontroladores",
    "TinyML e inferencia en el dispositivo",
    portada(
        "Sesión 12",
        "TinyML y Edge AI:<br />inferencia en microcontroladores",
        "Fundamentos y restricciones.",
        "Herramientas, flujo de trabajo y criterios de aplicación.",
        [
         ("i-cpu", "Entrenamiento fuera, inferencia en el chip"),
         ("i-wave", "Cuantización, pruning y destilación"),
         ("i-chart", "Matriz de confusión y umbral"),
         ("i-target", "Recolección, etiquetado y reentrenamiento"),
        ],
        "02-delimitacion-de-terminos.html",
    ),
    clases="slide",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/esp32-devkit-v1-element.js";
\t\t</script>
""",
)

# ──────────────────────────────── 02 · delimitación de términos
lamina(
    "delimitacion-de-terminos",
    "Relación de inclusión entre los términos del campo · Sesión 12",
    "Delimitación de términos",
    envolver(f"""{cabecera(A, "Relación de inclusión entre los términos del campo", "i-layers")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="blockdiagram blockdiagram--stack">
\t\t\t\t\t\t\t<div class="bd-node bd-node--ghost">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Inteligencia artificial</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Sistemas que resuelven tareas que se atribuían a la inteligencia humana. Incluye métodos que no aprenden nada.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">⊃</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--ok">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Aprendizaje automático</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">El comportamiento se deriva de datos, no se programa regla a regla.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">⊃</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--warn">
\t\t\t\t\t\t\t\t<span class="bd-node__title">Aprendizaje profundo</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Redes con muchas capas que extraen las características por sí mismas.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<span class="bd-arrow" aria-hidden="true">⊃</span>
\t\t\t\t\t\t\t<div class="bd-node bd-node--accent">
\t\t\t\t\t\t\t\t<span class="bd-node__title">TinyML</span>
\t\t\t\t\t\t\t\t<span class="bd-node__body">Inferencia sobre microcontroladores: memoria del orden de kilobytes y consumo del orden de milivatios.</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tAprendizaje en el borde
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tNo es un subconjunto de los anteriores sino <b>una decisión de
\t\t\t\t\t\t\t\tarquitectura</b>: dónde se ejecuta el cálculo. Puede ser en un equipo
\t\t\t\t\t\t\t\tcon sistema operativo completo cerca de los sensores, que no es un
\t\t\t\t\t\t\t\tmicrocontrolador.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Lo que distingue a TinyML</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tNo es el tipo de modelo sino la <b>magnitud de las restricciones</b>.
\t\t\t\t\t\t\t\tEntre un equipo de borde con 4 GB de memoria y el módulo de este
\t\t\t\t\t\t\t\tcurso con 320 kB hay cuatro órdenes de magnitud, y esa diferencia
\t\t\t\t\t\t\t\tcambia el planteamiento del problema, no solo el tamaño del modelo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-layers",
)

# ──────────────────────── 03 · entrenamiento e inferencia
lamina(
    "entrenamiento-e-inferencia",
    "Por qué solo la inferencia se ejecuta en el dispositivo · Sesión 12",
    "Entrenamiento e inferencia",
    envolver(f"""{cabecera(A, "Por qué solo la inferencia se ejecuta en el dispositivo", "i-cpu")}

\t\t\t\t<div class="compare" data-animate="fade-up">
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Entrenamiento</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tRecorre el conjunto de datos muchas veces ajustando parámetros.
\t\t\t\t\t\t\tNecesita <b>todos los datos a la vez</b> y aritmética de coma flotante
\t\t\t\t\t\t\ten gran volumen.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tSe hace en un ordenador, una vez, antes de desplegar.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="compare__panel">
\t\t\t\t\t\t<h3>Inferencia</h3>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tAplica los parámetros ya fijados a <b>una entrada</b>. Es un recorrido
\t\t\t\t\t\t\túnico, sin necesidad de conservar el conjunto de datos.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)]">
\t\t\t\t\t\t\tEs lo que cabe en el dispositivo, y solo tras reducir el modelo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tPor qué ejecutar la inferencia en el dispositivo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Latencia</b>: la decisión no espera a la red. <b>Tratamiento
\t\t\t\t\t\t\t\tlocal</b>: los datos no salen del equipo. <b>Costo de
\t\t\t\t\t\t\t\tcomunicación</b>: se transmite la conclusión, no la señal completa.
\t\t\t\t\t\t\t\t<b>Autonomía</b>: la radio es lo que más consume. <b>Operación sin
\t\t\t\t\t\t\t\tconectividad</b>: sigue decidiendo sin enlace.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">La cifra que ordena la decisión</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn acelerómetro a 100 Hz en tres ejes produce <b>300 valores por
\t\t\t\t\t\t\t\tsegundo</b>. Transmitirlos con la política periódica de la sesión 8
\t\t\t\t\t\t\t\tson decenas de megabytes al mes; transmitir una decisión por minuto
\t\t\t\t\t\t\t\tson unos pocos kilobytes. La inferencia local no es solo más rápida:
\t\t\t\t\t\t\t\tcambia el orden de magnitud del tráfico y del consumo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas restricciones (memoria del orden de <b>kilobytes</b> y consumo del
\t\t\t\t\t\t\t\torden de <b>milivatios</b>) condicionan <b>el planteamiento del
\t\t\t\t\t\t\t\tproblema</b>, no solo el tamaño del modelo. Un problema que exige
\t\t\t\t\t\t\t\tclasificar mil categorías no se resuelve reduciendo el modelo: se
\t\t\t\t\t\t\t\treplantea o se resuelve en otro sitio.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-cpu",
)

# ──────────────────────── 04 · arquitectura del sistema con inferencia
lamina(
    "arquitectura-con-inferencia",
    "Las seis etapas entre el sensor y la actuación · Sesión 12",
    "Arquitectura del sistema con inferencia",
    envolver(f"""{cabecera(A, "Las seis etapas entre el sensor y la actuación", "i-flow")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Etapa</th><th>Memoria</th><th>Tiempo</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td>Sensor</td><td>—</td><td>según el periférico</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Ventana de muestras</td><td>N × tamaño del dato</td><td>N × periodo</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Extracción de características</b></td><td>intermedia, reutilizable</td><td><b>a menudo la mayor</b></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Modelo</td><td>parámetros + tensor arena</td><td>tiempo de inferencia</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Posprocesado</td><td>despreciable</td><td>despreciable</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Decisión y actuación</td><td>—</td><td>—</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-wave")}
\t\t\t\t\t\t\t\tEl peso del procesamiento de señal
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>selección de características determina el resultado en mayor
\t\t\t\t\t\t\t\tmedida que la complejidad del modelo</b>. Con las características
\t\t\t\t\t\t\t\tadecuadas, un clasificador sencillo basta; con las equivocadas, no
\t\t\t\t\t\t\t\thay red que lo arregle.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="example">
\t\t\t\t\t\t\t<div class="example__label">
\t\t\t\t\t\t\t\t{ico("i-bulb")}
\t\t\t\t\t\t\t\tEjemplo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tPara detectar una anomalía en una bomba, la señal cruda del
\t\t\t\t\t\t\t\tacelerómetro son 128 valores; su espectro, unas pocas bandas de
\t\t\t\t\t\t\t\tenergía. El modelo que trabaja sobre las bandas es mucho menor y
\t\t\t\t\t\t\t\tacierta más, porque la transformada ya hizo el trabajo difícil.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Consecuencia para el presupuesto</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl tiempo de inferencia no es el único que cuenta: la extracción de
\t\t\t\t\t\t\t\tcaracterísticas suele ocupar más. El presupuesto del bucle de la
\t\t\t\t\t\t\t\tsesión 4 se aplica aquí a la cadena completa, no solo al modelo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-flow",
)

# ───────────────────── 05 · reducción del modelo
lamina(
    "reduccion-del-modelo",
    "Cuantización, pruning y destilación · Sesión 12",
    "Reducción del modelo",
    envolver(f"""{cabecera(A, "Cuantización, pruning y destilación", "i-layers")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-chip")}Cuantización</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSustituir la coma flotante de 32 bits por enteros de 8. Cada parámetro
\t\t\t\t\t\t\tpasa de 4 bytes a 1: el modelo ocupa <b>la cuarta parte</b>.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tAdemás, muchos microcontroladores calculan con enteros más rápido que
\t\t\t\t\t\t\tcon coma flotante.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-target")}Pruning</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEliminar conexiones o unidades que aportan poco. Reduce el número de
\t\t\t\t\t\t\tparámetros, a veces de forma drástica.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tSi se pruning (poda) de forma dispersa, la reducción no se traduce en velocidad:
\t\t\t\t\t\t\thay que pruningr por bloques.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-layers")}Destilación</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEntrenar un modelo pequeño para que reproduzca la salida de uno grande
\t\t\t\t\t\t\tya entrenado.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p class="text-[length:var(--fs-small)] text-[var(--color-text-muted)]">
\t\t\t\t\t\t\tEs la más costosa de aplicar: exige el modelo grande y otro
\t\t\t\t\t\t\tentrenamiento completo.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="conclusion" data-animate="fade-up">
\t\t\t\t\t<span class="conclusion__label">Las tres magnitudes se mueven juntas</span>
\t\t\t\t\t<p>
\t\t\t\t\t\t<b>Exactitud, tamaño y tiempo de inferencia</b> no se optimizan por
\t\t\t\t\t\tseparado: reducir el modelo baja las tres. La pregunta no es cuánto se
\t\t\t\t\t\tpuede reducir sino <b>cuánta exactitud admite el requisito</b>, y esa
\t\t\t\t\t\tcifra sale de la aplicación, no del modelo.
\t\t\t\t\t</p>
\t\t\t\t</div>

\t\t\t\t<div class="warn-box" data-animate="fade-up">
\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t<p>
\t\t\t\t\t\tLa reducción se mide <b>sobre el dispositivo</b>, no sobre el ordenador
\t\t\t\t\t\tdonde se entrenó. El tiempo de inferencia depende de qué operaciones
\t\t\t\t\t\testén optimizadas para ese procesador, y dos modelos del mismo tamaño
\t\t\t\t\t\tpueden tardar cosas muy distintas.
\t\t\t\t\t</p>
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-layers",
)

# ───────────────── 06 · artículo · cuantización y despliegue
lamina(
    "paper-cuantizacion",
    "Despliegue de una red cuantizada sobre un microcontrolador · Sesión 12",
    "Artículo · Cuantización y despliegue",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Novac, P.-E.; Boukli Hacene, G.; Pegatoquet, A. et al.</b> (2021). Quantization and Deployment of "
        "Deep Neural Networks on Microcontrollers. <i>Sensors</i> 21(9), 2984. "
        "<code>doi:10.3390/s21092984</code>",
        "Despliegue de una red cuantizada sobre un microcontrolador",
        ["Llevar una red entrenada a un microcontrolador con memoria y cómputo limitados.",
         "La coma flotante de 32 bits ofrece un <b>rango muy superior</b> al que una red necesita.",
         "Proponen una cadena <b>extremo a extremo</b>: entrenar, cuantizar y desplegar."],
        ["Reducir de <b>32 a 8 bits</b> por parámetro deja cada uno en la cuarta parte de memoria.",
         "La <b>aritmética entera</b> resulta más rápida en muchos microcontroladores.",
         "La eficiencia energética <b>depende del hardware y del marco</b>, no solo del modelo.",
         "Alcance de la propuesta: una sola cadena, frente a herramientas cerradas."],
        ["Las cifras de tamaño y de tiempo <b>no se transfieren</b> de una placa a otra.",
         "Un modelo que cabe y responde en el hardware del artículo puede no hacerlo en otro.",
         "La única forma de saberlo es <b>desplegarlo y medir</b>, no extrapolar."],
        [("paper-cuantizacion-memoria",
          "Elaboración propia a partir de la reducción publicada, cruzada con la memoria del módulo empleado: el cruce con el presupuesto dice cuántos parámetros caben."),
         ("paper-cuantizacion-efectos",
          "Qué cambia al cuantizar y qué no se puede dar por bueno sin medirlo en el hardware de destino.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ─────────────────────────────── 07 · métricas de evaluación
lamina(
    "metricas-de-evaluacion",
    "Por qué la exactitud global no basta · Sesión 12",
    "Métricas de evaluación",
    envolver(f"""{cabecera(A, "Por qué la exactitud global no basta", "i-chart")}

\t\t\t\t<div class="slide__split" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="warn-box">
\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUna exactitud del <b>95 %</b> puede corresponder a un detector que
\t\t\t\t\t\t\t\t<b>nunca detecta nada</b>: si la anomalía ocurre el 5 % del tiempo,
\t\t\t\t\t\t\t\tresponder siempre «normal» acierta el 95 % de las veces y no sirve
\t\t\t\t\t\t\t\tpara nada.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tLos dos errores no cuestan lo mismo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>falso negativo</b> en detección de avería deja pasar el fallo:
\t\t\t\t\t\t\t\tcuesta la máquina. Un <b>falso positivo</b> provoca una revisión
\t\t\t\t\t\t\t\tinnecesaria: cuesta una visita. La relación entre ambos costos es lo
\t\t\t\t\t\t\t\tque fija el umbral de decisión, y sale de la aplicación.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="figure">\n\t\t\t\t\t\t\t<div class="figure__frame" data-figure="metricas-matriz-confusion"></div>\n\t\t\t\t\t\t\t<p class="figure__caption">\n\t\t\t\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#i-chart" /></svg>\n\t\t\t\t\t\t\t\t<span>\n\t\t\t\t\t\t\t\t\tEl caso del párrafo, con las cuentas hechas sobre mil ventanas. La\n\t\t\t\t\t\t\t\t\tcolumna de la derecha está vacía: el detector nunca dice «anomalía».\n\t\t\t\t\t\t\t\t\tLa exactitud sigue siendo del 95 %.\n\t\t\t\t\t\t\t\t</span>\n\t\t\t\t\t\t\t</p>\n\t\t\t\t\t\t</div>\n\n\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Las cuatro cifras que hay que dar</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLa <b>matriz de confusión</b> completa, no la exactitud sola. El
\t\t\t\t\t\t\t\t<b>tiempo de inferencia</b> medido en el dispositivo. La <b>memoria
\t\t\t\t\t\t\t\tde trabajo</b> que exige. Y la <b>tasa de cada error</b> con su costo
\t\t\t\t\t\t\t\ten la aplicación. Sin las cuatro, no se puede decidir si el modelo
\t\t\t\t\t\t\t\tsirve.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-chart",
)

# ───────────────── 08 · artículo · qué se mide en TinyML
lamina(
    "paper-benchmark-tinyml",
    "Dificultad de comparar sistemas de inferencia entre plataformas · Sesión 12",
    "Artículo · Comparación entre sistemas",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · arXiv",
        "<b>Banbury, C. R.; Reddi, V. J.; Lam, M. et al.</b> (2020). Benchmarking TinyML Systems: Challenges and "
        "Direction. <i>arXiv</i>. <code>arXiv:2003.04821</code>",
        "Dificultad de comparar sistemas de inferencia entre plataformas",
        ["Establecer qué hace falta para <b>comparar de forma justa</b> sistemas de inferencia.",
         "Cada fabricante ofrece sus propias herramientas y <b>compiladores propietarios</b>.",
         "Eso impide comparar resultados y dificulta llevar el trabajo de una plataforma a otra."],
        ["Identifican tres obstáculos: diversidad de hardware, herramientas cerradas y <b>ausencia de cargas comunes</b>.",
         "La generación de código optimizado por fabricante <b>resuelve el rendimiento, no la comparabilidad</b>.",
         "Un <b>intérprete común</b> permite intercambiar modelos a costa de algo de eficiencia.",
         "Su estructura es idéntica en todas las plataformas: el modelo se sustituye sin rehacer la integración."],
        ["Sin cargas y métricas compartidas, las cifras publicadas <b>solo valen dentro del trabajo que las produjo</b>.",
         "Proponen la dirección que debe seguir un procedimiento de comparación del campo.",
         "Es la razón por la que en esta sesión toda cifra se mide en el hardware propio."],
        [("paper-comparabilidad",
          "Elaboración propia. Con cadenas cerradas, cada cifra vive en su casilla y ninguna comparte a la vez modelo y plataforma con otra."),
         ("paper-tinyml-obstaculos",
          "Cada obstáculo identificado emparejado con lo que haría falta para resolverlo.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────── 09 · La hora del código · 47
lamina(
    "codigo-48-umbral-antes-que-modelo",
    "Código 48 · Umbral y transformada antes de entrenar nada · Sesión 12",
    "La hora del código · Umbral antes que modelo",
    hora_del_codigo(
        48,
        "Umbral y transformada como línea de base antes de entrenar nada",
        "Establecer la <b>línea de base</b> antes de plantear ningún modelo: detectar la condición con un umbral "
        "sobre la señal filtrada y sobre la energía de una banda, y registrar la matriz de confusión completa "
        "contra 200 casos etiquetados a mano.",
        "La <b>matriz de confusión</b> son las cuatro cuentas, verdaderos y falsos positivos y negativos, y no se "
        "puede sustituir por la exactitud, que oculta el reparto entre los dos tipos de error. La <b>energía de "
        "banda</b> mide cuánta señal hay en un rango de frecuencias: convierte una forma de onda en un número "
        "comparable. La <b>línea de base</b> es el mejor resultado alcanzable sin aprendizaje, y es contra ella "
        ",no contra la nada, como se juzga después un modelo.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> como magnitud vigilada, enciende un LED de "
        "detección en el <b>GPIO 25</b> y otro de falso positivo en el <b>GPIO 26</b>, con 220 Ω.",
        """[BASE] 200 casos etiquetados: 40 anomalias, 160 normales
[UMBRAL] señal cruda:    VP=28 FN=12 FP=31 VN=129
[UMBRAL] señal filtrada: VP=35 FN= 5 FP=11 VN=149
[BANDA]  energia de banda: VP=38 FN= 2 FP= 4 VN=156
[COSTO]  filtrado=0.3 ms banda=4.1 ms memoria=1.2 kB
[EXACTITUD] cruda=78.5 %  filtrada=92.0 %  banda=97.0 %""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino.

<b>2. Firmware.</b> Guarda en el sistema de archivos 200 ventanas de señal etiquetadas como normal o anomalía. Implementa tres detectores: umbral sobre la señal cruda, umbral sobre la señal filtrada con el filtro exponencial de la sesión 4, y umbral sobre la energía de una banda obtenida por transformada. Para cada uno, calcula la <b>matriz de confusión completa</b> sobre los 200 casos, y mide el tiempo de proceso y la memoria adicional. Emite a 115200 baudios la comparación de los tres. No entrenes ningún modelo en este ejemplo.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de un caso a través de los tres detectores, con la etapa que añade cada uno. Y la <b>cadena de etapas</b> con el costo en tiempo y memoria de cada una y la exactitud que alcanza.""",
        "La última línea es la que cambia la conversación: <b>97 % sin ningún modelo</b>. A partir de ahí la "
        "pregunta ya no es qué modelo usar sino si hace falta alguno. Mirar además las columnas de la primera "
        "fila: exactitud del 78,5 % con <b>31 falsos positivos</b>. Una misma exactitud puede repartirse de "
        "maneras muy distintas entre los dos errores, y solo la matriz completa lo enseña.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=SENSOR_SCRIPTS,
)

# ──────────────── 09b · simulación del umbral de decisión
lamina(
    "simulacion-umbral-decision",
    "Efecto del umbral sobre los dos tipos de error · Sesión 12",
    "El umbral y los dos errores",
    envolver(f"""{cabecera(A, "Efecto del umbral sobre los dos tipos de error", "i-play")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tPor qué no hay un umbral óptimo
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tLas dos poblaciones, normal y anomalía, se solapan. Cualquier umbral
\t\t\t\t\t\t\t\tdeja errores de los dos tipos, y moverlo <b>intercambia unos por
\t\t\t\t\t\t\t\totros</b>: no los reduce a la vez.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="sim-caption">
\t\t\t\t\t\t\t{ico("i-sliders")}
\t\t\t\t\t\t\t<p class="m-0">
\t\t\t\t\t\t\t\tLa exactitud apenas se mueve en un tramo amplio del recorrido,
\t\t\t\t\t\t\t\tmientras el reparto entre falsos positivos y negativos cambia por
\t\t\t\t\t\t\t\tcompleto. Por eso el umbral no se elige maximizando la exactitud sino
\t\t\t\t\t\t\t\t<b>minimizando el costo</b>, y ese costo lo fija la aplicación: aquí,
\t\t\t\t\t\t\t\tcuánto vale una avería no detectada frente a una revisión innecesaria.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="card">
\t\t\t\t\t\t\t<canvas
\t\t\t\t\t\t\t\tid="umb-canvas"
\t\t\t\t\t\t\t\tclass="w-full aspect-[5/2]"
\t\t\t\t\t\t\t\twidth="900"
\t\t\t\t\t\t\t\theight="360"
\t\t\t\t\t\t\t\trole="img"
\t\t\t\t\t\t\t\taria-label="Dos distribuciones solapadas, normal y anomalía, con la línea de umbral y las áreas correspondientes a falsos positivos y falsos negativos"
\t\t\t\t\t\t\t></canvas>

\t\t\t\t\t\t\t<div class="controls mt-3">
\t\t\t\t\t\t\t\t<label for="umb-valor" class="text-sm font-medium">Umbral de decisión</label>
\t\t\t\t\t\t\t\t<input type="range" id="umb-valor" min="20" max="80" step="1" value="50" />
\t\t\t\t\t\t\t\t<span class="readout" id="umb-valor-lec">5,0</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="controls mt-2">
\t\t\t\t\t\t\t\t<label for="umb-costo" class="text-sm font-medium">
\t\t\t\t\t\t\t\t\tCosto de un fallo no detectado frente a una revisión
\t\t\t\t\t\t\t\t</label>
\t\t\t\t\t\t\t\t<input type="range" id="umb-costo" min="1" max="50" step="1" value="20" />
\t\t\t\t\t\t\t\t<span class="readout" id="umb-costo-lec">×20</span>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="metric mt-3">
\t\t\t\t\t\t\t\t<div class="metric__item">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Exactitud</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="umb-exac">94 %</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item metric__item--warn">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Falsos positivos</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="umb-fp">8</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item metric__item--bad">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Falsos negativos</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="umb-fn">4</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<div class="metric__item" id="umb-item-costo">
\t\t\t\t\t\t\t\t\t<span class="text-xs text-[var(--color-text-muted)]">Costo total</span>
\t\t\t\t\t\t\t\t\t<span class="readout" id="umb-total">88</span>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-play",
    scripts="""\t\t<script type="module">
\t\t\t// Dos poblaciones gaussianas solapadas, con los tamaños del ejemplo 48:
\t\t\t// 160 casos normales y 40 anomalías.
\t\t\tconst N_NORMAL = 160;
\t\t\tconst N_ANOMALIA = 40;
\t\t\tconst MU_NORMAL = 4.0;
\t\t\tconst MU_ANOMALIA = 6.4;
\t\t\tconst SIGMA = 0.9;

\t\t\tconst lienzo = document.getElementById("umb-canvas");
\t\t\tconst ctx = lienzo.getContext("2d");
\t\t\tconst dUmbral = document.getElementById("umb-valor");
\t\t\tconst dCosto = document.getElementById("umb-costo");
\t\t\tconst lecUmbral = document.getElementById("umb-valor-lec");
\t\t\tconst lecCosto = document.getElementById("umb-costo-lec");
\t\t\tconst salExac = document.getElementById("umb-exac");
\t\t\tconst salFP = document.getElementById("umb-fp");
\t\t\tconst salFN = document.getElementById("umb-fn");
\t\t\tconst salTotal = document.getElementById("umb-total");
\t\t\tconst itCosto = document.getElementById("umb-item-costo");

\t\t\tfunction variable(n) {
\t\t\t\treturn getComputedStyle(document.documentElement).getPropertyValue(n).trim();
\t\t\t}
\t\t\tfunction coma(n, d) {
\t\t\t\treturn n.toFixed(d).replace(".", ",");
\t\t\t}

\t\t\tconst densidad = (x, mu) =>
\t\t\t\tMath.exp(-((x - mu) ** 2) / (2 * SIGMA ** 2)) / (SIGMA * Math.sqrt(2 * Math.PI));

\t\t\t// Proporción de una población por encima del umbral, por integración
\t\t\t// numérica: basta para la lámina y evita depender de una función de
\t\t\t// error que JavaScript no trae.
\t\t\tfunction proporcionSobre(umbral, mu) {
\t\t\t\tconst paso = 0.01;
\t\t\t\tlet total = 0;
\t\t\t\tlet sobre = 0;
\t\t\t\tfor (let x = 0; x <= 10; x += paso) {
\t\t\t\t\tconst d = densidad(x, mu) * paso;
\t\t\t\t\ttotal += d;
\t\t\t\t\tif (x >= umbral) sobre += d;
\t\t\t\t}
\t\t\t\treturn sobre / total;
\t\t\t}

\t\t\tfunction dibujar(umbral) {
\t\t\t\tconst w = lienzo.width;
\t\t\t\tconst h = lienzo.height;
\t\t\t\tctx.clearRect(0, 0, w, h);

\t\t\t\tconst izq = 60;
\t\t\t\tconst der = w - 30;
\t\t\t\tconst base = 286;
\t\t\t\tconst alto = 210;
\t\t\t\tconst x = (v) => izq + (v / 10) * (der - izq);
\t\t\t\tconst maxD = densidad(MU_NORMAL, MU_NORMAL);
\t\t\t\tconst y = (d) => base - (d / maxD) * alto;

\t\t\t\tconst ok = variable("--color-ok");
\t\t\t\tconst acento = variable("--color-accent");
\t\t\t\tconst atenuado = variable("--color-text-muted");
\t\t\t\tconst borde = variable("--color-border");

\t\t\t\t// Áreas de error, dibujadas antes que las curvas
\t\t\t\tfor (const [mu, color, esFP] of [[MU_NORMAL, acento, true], [MU_ANOMALIA, ok, false]]) {
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tctx.moveTo(x(esFP ? umbral : 0), base);
\t\t\t\t\tfor (let v = esFP ? umbral : 0; esFP ? v <= 10 : v <= umbral; v += 0.02) {
\t\t\t\t\t\tctx.lineTo(x(v), y(densidad(v, mu)));
\t\t\t\t\t}
\t\t\t\t\tctx.lineTo(x(esFP ? 10 : umbral), base);
\t\t\t\t\tctx.closePath();
\t\t\t\t\tctx.fillStyle = color;
\t\t\t\t\tctx.globalAlpha = 0.3;
\t\t\t\t\tctx.fill();
\t\t\t\t\tctx.globalAlpha = 1;
\t\t\t\t}

\t\t\t\t// Curvas
\t\t\t\tfor (const [mu, color, rotulo] of [[MU_NORMAL, ok, "normal"], [MU_ANOMALIA, acento, "anomalía"]]) {
\t\t\t\t\tctx.beginPath();
\t\t\t\t\tfor (let v = 0; v <= 10; v += 0.02) {
\t\t\t\t\t\tconst px = x(v);
\t\t\t\t\t\tconst py = y(densidad(v, mu));
\t\t\t\t\t\tif (v === 0) ctx.moveTo(px, py);
\t\t\t\t\t\telse ctx.lineTo(px, py);
\t\t\t\t\t}
\t\t\t\t\tctx.strokeStyle = color;
\t\t\t\t\tctx.lineWidth = 2.2;
\t\t\t\t\tctx.stroke();
\t\t\t\t\tctx.fillStyle = color;
\t\t\t\t\tctx.font = "600 12px system-ui";
\t\t\t\t\tctx.textAlign = "center";
\t\t\t\t\tctx.fillText(rotulo, x(mu), y(densidad(mu, mu)) - 10);
\t\t\t\t}

\t\t\t\t// Umbral
\t\t\t\tctx.strokeStyle = variable("--color-navy");
\t\t\t\tctx.lineWidth = 2;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(x(umbral), base + 6);
\t\t\t\tctx.lineTo(x(umbral), base - alto - 6);
\t\t\t\tctx.stroke();
\t\t\t\tctx.fillStyle = variable("--color-navy");
\t\t\t\tctx.font = "600 12px ui-monospace, monospace";
\t\t\t\tctx.fillText(coma(umbral, 1), x(umbral), base - alto - 14);

\t\t\t\t// Eje
\t\t\t\tctx.strokeStyle = borde;
\t\t\t\tctx.lineWidth = 1;
\t\t\t\tctx.beginPath();
\t\t\t\tctx.moveTo(izq, base);
\t\t\t\tctx.lineTo(der, base);
\t\t\t\tctx.stroke();
\t\t\t\tctx.fillStyle = atenuado;
\t\t\t\tctx.font = "11px system-ui";
\t\t\t\tctx.textAlign = "right";
\t\t\t\tctx.fillText("característica extraída", der, base + 20);
\t\t\t\tctx.textAlign = "left";
\t\t\t\tctx.fillText("relleno rojo: falsos positivos · relleno verde: falsos negativos", izq, 30);
\t\t\t}

\t\t\tfunction actualizar() {
\t\t\t\tconst umbral = Number(dUmbral.value) / 10;
\t\t\t\tconst razon = Number(dCosto.value);
\t\t\t\tlecUmbral.textContent = coma(umbral, 1);
\t\t\t\tlecCosto.textContent = `×${razon}`;

\t\t\t\tdibujar(umbral);

\t\t\t\tconst fp = Math.round(N_NORMAL * proporcionSobre(umbral, MU_NORMAL));
\t\t\t\tconst fn = Math.round(N_ANOMALIA * (1 - proporcionSobre(umbral, MU_ANOMALIA)));
\t\t\t\tconst exac = ((N_NORMAL + N_ANOMALIA - fp - fn) / (N_NORMAL + N_ANOMALIA)) * 100;
\t\t\t\tconst costo = fp + fn * razon;

\t\t\t\tsalExac.textContent = `${coma(exac, 1)} %`;
\t\t\t\tsalFP.textContent = String(fp);
\t\t\t\tsalFN.textContent = String(fn);
\t\t\t\tsalTotal.textContent = String(costo);
\t\t\t\t// Se resalta cuando el costo se acerca a su mínimo en el recorrido.
\t\t\t\tlet mejor = Infinity;
\t\t\t\tfor (let u = 2; u <= 8; u += 0.1) {
\t\t\t\t\tconst f1 = Math.round(N_NORMAL * proporcionSobre(u, MU_NORMAL));
\t\t\t\t\tconst f2 = Math.round(N_ANOMALIA * (1 - proporcionSobre(u, MU_ANOMALIA)));
\t\t\t\t\tmejor = Math.min(mejor, f1 + f2 * razon);
\t\t\t\t}
\t\t\t\tconst cerca = costo <= mejor * 1.1;
\t\t\t\titCosto.classList.toggle("metric__item--ok", cerca);
\t\t\t\titCosto.classList.toggle("metric__item--bad", !cerca);
\t\t\t}

\t\t\tfor (const el of [dUmbral, dCosto]) el.addEventListener("input", actualizar);
\t\t\tnew MutationObserver(actualizar).observe(document.documentElement, {
\t\t\t\tattributes: true,
\t\t\t\tattributeFilter: ["data-theme"],
\t\t\t});
\t\t\tactualizar();
\t\t</script>
""",
)

# ────────────────────────────────────── 09c · La hora del código · 49
lamina(
    "codigo-49-entrenar-y-exportar",
    "Código 49 · Entrenar fuera, medir dentro · Sesión 12",
    "La hora del código · Entrenar y exportar",
    hora_del_codigo(
        49,
        "Modelo entrenado fuera y medido sobre el dispositivo",
        "Llevar al equipo un modelo entrenado fuera y <b>medir allí sus cuatro cifras</b>: matriz de confusión "
        "sobre el conjunto de prueba, tiempo de inferencia, tensor arena y comparación contra la línea de "
        "base del ejemplo anterior.",
        "<b>Cuantizar</b> es pasar los parámetros de coma flotante a enteros de 8 bits: ocupan la cuarta parte y "
        "la aritmética entera es más rápida. El <b>tensor arena</b> del intérprete es aparte de los "
        "parámetros y se reserva entera al arrancar, así que hay que contarla en el presupuesto. Las cifras "
        "medidas en el ordenador <b>no se transfieren</b> al microcontrolador: por eso la evaluación se repite "
        "aquí sobre los mismos 200 casos.",
        "El <b>ESP32</b> lee un potenciómetro en el <b>GPIO 34</b> para recorrer el rango de la característica y "
        "enciende un LED en el <b>GPIO 25</b> con resistencia de 220 Ω que indica la clase decidida.",
        """[MODELO] cargado parametros=4.2 kB  tensor arena=6.0 kB
[PRUEBA] 200 casos: VP=39 FN=1 FP=3 VN=157  exactitud=98.0 %
[TIEMPO] inferencia=2.7 ms extraccion=4.1 ms total=6.8 ms
[BASE]   umbral sobre banda (ej. 48): 97.0 %  total=4.1 ms
[JUICIO] gana 1.0 punto y cuesta 2.7 ms mas y 10.2 kB
[MEM]    libre antes=195 kB  durante inferencia=184 kB""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y un intérprete de modelos para microcontroladores.

<b>2. Firmware.</b> Entrena fuera un clasificador sobre las características del ejemplo 48, cuantízalo a enteros de 8 bits y expórtalo. Cárgalo del sistema de archivos y evalúalo sobre los mismos 200 casos, calculando la <b>matriz de confusión completa</b>. Mide por separado inferencia y extracción, y el tensor arena del intérprete. Imprime la comparación contra la línea de base del ejemplo 48: qué exactitud gana y cuánto tiempo y memoria cuesta. Emite a 115200 baudios.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el potenciómetro en el GPIO 34 y el LED en el GPIO 25.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una inferencia, desde la ventana hasta la clase decidida, con las dos etapas cronometradas señaladas. Y el <b>flujo completo</b> desde la recolección de datos hasta la integración, con el esfuerzo relativo de cada etapa.""",
        "La línea <code>[JUICIO]</code> es el entregable: <b>un punto de exactitud</b> a cambio de 2,7 ms y "
        "10,2 kB. Con esas tres cifras delante, decidir que <b>no</b> compensa es una conclusión tan válida como "
        "la contraria — y sin ellas no hay decisión, hay preferencia. Comprobar también que el total de 6,8 ms "
        "cabe en el periodo del sistema: una exactitud mejor que llega tarde no sirve.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-potentiometer></wokwi-potentiometer></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="green"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=SENSOR_SCRIPTS,
)

# ─────────────────────── 10 · herramientas y flujo de trabajo
lamina(
    "herramientas-y-flujo",
    "Herramientas disponibles y reparto real del esfuerzo · Sesión 12",
    "Herramientas y flujo de trabajo",
    envolver(f"""{cabecera(B, "Herramientas disponibles y reparto real del esfuerzo", "i-flow")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text">
\t\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t\t<table>
\t\t\t\t\t\t\t\t<thead><tr><th>Etapa del flujo</th><th>Esfuerzo real</th></tr></thead>
\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t<tr><td><b>Recolección de datos</b></td><td><b>La mayor parte</b></td></tr>
\t\t\t\t\t\t\t\t\t<tr><td><b>Etiquetado</b></td><td>Grande, y a menudo manual</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Diseño del procesamiento</td><td>Medio; decide el resultado</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Entrenamiento</td><td>Pequeño; está automatizado</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Evaluación</td><td>Medio; hay que interpretar</td></tr>
\t\t\t\t\t\t\t\t\t<tr><td>Exportación e integración</td><td>Medio; aparecen los límites del dispositivo</td></tr>
\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Lo que sorprende del reparto</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl entrenamiento, lo que se asocia con «hacer un modelo», es la etapa
\t\t\t\t\t\t\t\tmás corta y la más automatizada. <b>Los datos ocupan la mayor parte
\t\t\t\t\t\t\t\tdel trabajo</b>, y su calidad decide el resultado mucho antes de que
\t\t\t\t\t\t\t\tintervenga ningún algoritmo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\tCriterios de recolección
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>Representatividad</b> de las condiciones reales de operación,
\t\t\t\t\t\t\t\t<b>equilibrio entre clases</b> y <b>variabilidad</b> de las
\t\t\t\t\t\t\t\tcondiciones de captura. Un conjunto tomado en una sola tarde con un
\t\t\t\t\t\t\t\tsolo equipo produce un modelo que funciona esa tarde con ese equipo.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="practice">
\t\t\t\t\t\t\t<div class="practice__label">
\t\t\t\t\t\t\t\t{ico("i-keyboard")}
\t\t\t\t\t\t\t\tHerramientas
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn <b>intérprete de modelos para microcontroladores</b>, las
\t\t\t\t\t\t\t\tbibliotecas optimizadas del fabricante y los entornos integrados que
\t\t\t\t\t\t\t\tcubren el flujo completo. El intérprete es la opción que permite
\t\t\t\t\t\t\t\tsustituir el modelo sin rehacer la integración, según el artículo
\t\t\t\t\t\t\t\tanterior.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Selección de hardware</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tEl módulo de este curso sirve para clasificación sobre "
\t\t\t\t\t\t\t\tcaracterísticas ya extraídas. Para audio o visión conviene una
\t\t\t\t\t\t\t\tvariante con instrucciones vectoriales y memoria adicional, y hay
\t\t\t\t\t\t\t\tproblemas que exigen otra plataforma. Reconocerlo a tiempo es parte
\t\t\t\t\t\t\t\tdel criterio.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-flow",
)

# ────────────────────────────────────── 10b · La hora del código · 51
lamina(
    "codigo-50-recoleccion-etiquetado",
    "Código 50 · Recolección y etiquetado sobre el propio equipo · Sesión 12",
    "La hora del código · Recolección y etiquetado",
    hora_del_codigo(
        50,
        "Recolección y etiquetado de datos sobre el propio equipo",
        "Construir el conjunto de datos <b>en el equipo que después va a decidir</b>. Dos pulsadores etiquetan la "
        "ventana en curso como normal o anomalía; cada captura se guarda con su procedencia y el firmware vigila "
        "el equilibrio entre clases.",
        "Una <b>ventana deslizante</b> es el último tramo de señal, siempre disponible: al pulsar se guarda lo ya "
        "capturado, sin esperar. El <b>equilibrio entre clases</b> importa porque un clasificador entrenado con "
        "ocho normales por cada anomalía aprende a responder siempre «normal» y acierta el 89 %. La "
        "<b>procedencia</b> (qué equipo, qué día, en qué condiciones) es lo que permite saber después a qué se "
        "parece el conjunto: a una tarde suelta o al equipo en general.",
        "El <b>ESP32</b> lee un sensor en el <b>GPIO 15</b>, dos pulsadores de etiqueta en los <b>GPIO 4 y 5</b> "
        "con <code>INPUT_PULLUP</code>, y enciende un LED de captura en el <b>GPIO 25</b>.",
        """[CAPTURA] etiqueta=normal id=A4CF12  t=2026-07-28T09:22:05
[CAPTURA] etiqueta=anomalia id=A4CF12  t=2026-07-28T09:24:11
[BALANCE] normal=147 anomalia=18  8.2:1 -&gt; desequilibradas
[BALANCE] normal=160 anomalia=40  4.0:1 -&gt; aceptable
[AVISO] todas las capturas son del mismo equipo y del mismo dia""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino y LittleFS.

<b>2. Firmware.</b> Muestrea en una ventana deslizante de 128 muestras. Al pulsar uno de los botones, guarda la ventana con su etiqueta, timestamp, identificador del equipo y condiciones. Lleva la cuenta por clase y <b>avisa cuando la relación supere 3:1</b>. Si todas las capturas comparten equipo y día, emite un aviso de que el conjunto no es representativo. Exporta a un archivo diario y emite a 115200 baudios cada captura y el balance.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el sensor y los dos pulsadores en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> de una captura, desde la pulsación hasta el archivo, con la comprobación del balance. Y la <b>ficha de una captura</b> con todos sus campos, indicando para qué sirve cada uno al entrenar y al diagnosticar después.""",
        "Los dos avisos son el ejercicio. El de <b>desequilibrio</b> aparece a 8,2:1 y desaparece a 4,0:1: con el "
        "primero, un clasificador que responda siempre «normal» ya acierta el 89 %. El de <b>procedencia "
        "única</b> es el más caro de ignorar — un conjunto tomado en una tarde con un solo equipo produce un "
        "modelo que funciona esa tarde con ese equipo, y eso no se descubre hasta el despliegue.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-dht22></wokwi-dht22></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="green"></wokwi-pushbutton></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-pushbutton color="red"></wokwi-pushbutton></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts="""\t\t<script type="module">
\t\t\timport "@wokwi/elements/dist/esm/dht22-element.js";
\t\t\timport "@wokwi/elements/dist/esm/led-element.js";
\t\t\timport "@wokwi/elements/dist/esm/pushbutton-element.js";
\t\t\timport "@wokwi/elements/dist/esm/resistor-element.js";
\t\t</script>
""",
)

# ──────────────── 11 · artículo · detección de anomalías en operación
lamina(
    "paper-deteccion-anomalias",
    "Detección de anomalías sin etiquetas en entorno industrial · Sesión 12",
    "Artículo · Detección de anomalías",
    articulo(
        "Artículo de referencia",
        "Acceso abierto · CC BY 4.0",
        "<b>Antonini, M.; Pincheira, M.; Vecchio, M.; Antonelli, F.</b> (2023). An Adaptable and Unsupervised "
        "TinyML Anomaly Detection System for Extreme Industrial Environments. <i>Sensors</i> 23(4), 2344. "
        "<code>doi:10.3390/s23042344</code>",
        "Detección de anomalías sin etiquetas en entorno industrial",
        ["Detectar el fallo de un equipo industrial ejecutando el análisis <b>en el propio dispositivo</b>.",
         "El enfoque habitual aumenta la complejidad y <b>falla sin conectividad</b>.",
         "Resulta inaplicable donde el enlace no se puede garantizar."],
        ["Sistema de detección <b>no supervisada</b>: sin conjunto de fallos etiquetados.",
         "En un equipo industrial, ese conjunto <b>rara vez existe</b>.",
         "Desplegado sobre el hardware para vigilar una <b>bomba</b>.",
         "Las métricas recogidas son del <b>sistema de pruebas</b>, no del despliegue."],
        ["La inferencia local hace viable la <b>vigilancia continua</b> donde el enlace no se garantiza.",
         "Se sitúa en la línea del <b>mantenimiento según el estado</b>: intervenir solo cuando hace falta.",
         "Los autores <b>esperan</b> que las cifras del banco se aproximen a las del despliegue, sin afirmarlo."],
        [("paper-vigilancia-continua",
          "Cálculo propio sobre una jornada con los cortes indicados, no medidas del artículo: si el análisis vive en el servidor, lo vigilado es lo que el enlace deja pasar."),
         ("paper-anomalias-requisitos",
          "Lo que cada enfoque exige antes de poder funcionar. La columna de la derecha es la que hace viable el caso industrial.")],
    ),
    clases="slide",
    icono="i-paper",
)

# ────────────────────────────────────── 12 · La hora del código · 48
lamina(
    "codigo-51-inferencia-completa",
    "Código 51 · Sistema completo con inferencia y publicación · Sesión 12",
    "La hora del código · Sistema con inferencia",
    hora_del_codigo(
        51,
        "Sistema completo: adquisición, inferencia local y publicación de la decisión",
        "Cerrar el curso con la cadena entera: muestrear, extraer características, ejecutar la inferencia y "
        "<b>publicar la decisión</b> con su grado de confianza en lugar de la señal. El tráfico resultante se "
        "compara con el de enviar la señal cruda.",
        "Cargar el modelo <b>del sistema de archivos</b> permite sustituirlo sin regrabar. La <b>confianza</b> "
        "acompaña a la clase y decide si la conclusión merece publicarse. Publicar solo el <b>cambio de clase</b> "
        "es la política por variación de la sesión 8 aplicada a una decisión.",
        "El <b>ESP32</b> lee un sensor en el <b>GPIO 15</b> y enciende dos LED, decisión y estado del enlace, en "
        "los <b>GPIO 25 y 26</b>, con resistencia de 220 Ω.",
        """[MODELO] cargado de /modelo.tflite parametros=4.2 kB  arena=6.0 kB
[TIEMPO] extraccion=4.1  inferencia=2.7  total=6.8 de 10 ms
[INFER]  clase=normal confianza=0.94 -&gt; no se publica
[INFER]  clase=anomalia confianza=0.88 -&gt; publica .../estado
[TRAFICO] decision=38 B/min señal cruda=36 kB/min (x950)""",
        """<b>1. Proyecto.</b> Crea un proyecto nuevo de PlatformIO para la placa esp32dev con el framework Arduino, un intérprete de modelos para microcontroladores y PubSubClient.

<b>2. Firmware.</b> Carga el modelo desde el sistema de archivos, no compilado en el binario. Muestrea a 100 Hz en ventanas de 128 muestras, extrae las características del ejemplo 48 y ejecuta la inferencia. Mide por separado extracción e inferencia y comprueba que la suma cabe en el periodo. Publica solo el cambio de clase con su confianza, y lleva la cuenta del tráfico frente al que habría supuesto enviar la señal cruda. Registra la versión del modelo junto a la del firmware.

<b>3. Simulación.</b> Añade la simulación de Wokwi con el sensor en el GPIO 15 y los dos LED en los GPIO indicados.

<b>4. Diagramas.</b> Entrega dos en Excalidraw. El <b>diagrama de flujo</b> del ciclo completo, con la comprobación de que extracción e inferencia caben en el periodo. Y la <b>arquitectura</b> desde el sensor hasta el panel, marcando dónde se toma la decisión y qué viaja por la red.""",
        "La última línea justifica la sesión entera: <b>38 bytes por minuto</b> frente a los 36 kB de la señal "
        "cruda. Comprobar antes <code>[TIEMPO]</code>: 6,8 ms de un periodo de 10 ms, con un <b>32 % de "
        "margen</b>. Si ese margen desapareciera, el sistema dejaría de cumplir su periodo aunque el modelo "
        "siguiera acertando.",
        piezas=(
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-dht22></wokwi-dht22></span>'
            '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item"><wokwi-led color="red"></wokwi-led></span>\n\t\t\t\t\t\t\t\t\t'
        ),
    ),
    clases="slide",
    icono="i-terminal",
    scripts=SENSOR_SCRIPTS,
)

# ──────────────── 13 · ciclo de vida del modelo y criterio final
lamina(
    "ciclo-de-vida-del-modelo",
    "Versionado, despliegue y reentrenamiento del modelo · Sesión 12",
    "Ciclo de vida del modelo",
    envolver(f"""{cabecera(B, "Versionado, despliegue y reentrenamiento del modelo", "i-check")}

\t\t\t\t<div class="slide__split is-stretch" data-animate="fade-up">
\t\t\t\t\t<div class="slide__split-text is-spread">
\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t\t\tEl modelo es un artefacto aparte
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tTiene <b>su propia versión</b> y su propio despliegue, independientes
\t\t\t\t\t\t\t\tdel firmware. Se distribuye con el mecanismo de actualización de la
\t\t\t\t\t\t\t\tsesión 10 y se declara en <code>/api/info</code> junto a la versión
\t\t\t\t\t\t\t\tdel programa.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="def">
\t\t\t\t\t\t\t<div class="def__label">
\t\t\t\t\t\t\t\t{ico("i-alert")}
\t\t\t\t\t\t\t\tLa distribución de los datos cambia
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\tUn modelo entrenado con datos de un año deja de acertar cuando el
\t\t\t\t\t\t\t\tequipo envejece, se cambia una pieza o varía la estación. La
\t\t\t\t\t\t\t\texactitud cae sin que nadie toque nada, y por eso hace falta
\t\t\t\t\t\t\t\t<b>vigilarla en operación</b>, no solo al desplegar.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="slide__split-visual">
\t\t\t\t\t\t<div class="conclusion">
\t\t\t\t\t\t\t<span class="conclusion__label">Criterio de aplicabilidad, en orden</span>
\t\t\t\t\t\t\t<p>
\t\t\t\t\t\t\t\t<b>1.</b> Un umbral sobre la señal filtrada. <b>2.</b> Un umbral
\t\t\t\t\t\t\t\tsobre una característica derivada, como la energía de una banda.
\t\t\t\t\t\t\t\t<b>3.</b> Solo si las dos anteriores no alcanzan el requisito, un
\t\t\t\t\t\t\t\tmodelo entrenado. Y en ese caso, comparado contra la línea de base
\t\t\t\t\t\t\t\tque las dos primeras establecieron.
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="usecases">
\t\t\t\t\t\t\t<span class="usecases-label">Aplicaciones habituales</span>
\t\t\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t\t\t{ico("i-wave")}
\t\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t\t<span class="usecase__name">Mantenimiento por vibración</span>
\t\t\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\t\t\tUn rodamiento que se degrada cambia el espectro antes de fallar:
\t\t\t\t\t\t\t\t\t\tla decisión se toma sobre bandas de energía.
\t\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t\t<span class="usecase__name">Reconocimiento de actividad</span>
\t\t\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\t\t\tDistinguir caminar de correr con un acelerómetro: pocas clases y
\t\t\t\t\t\t\t\t\t\tcaracterísticas bien conocidas.
\t\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t\t\t{ico("i-bolt")}
\t\t\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t\t\t<span class="usecase__name">Detección de palabra clave</span>
\t\t\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\t\t\tEl caso que hizo conocido a este campo, y el que más exige del
\t\t\t\t\t\t\t\t\t\thardware: requiere instrucciones vectoriales.
\t\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
)

# ─────────────────────────────────────── 14 · problemas frecuentes
lamina(
    "problemas-frecuentes",
    "Problemas frecuentes al llevar un modelo al dispositivo · Sesión 12",
    "Problemas frecuentes",
    envolver(f"""{cabecera(B, "Problemas frecuentes al llevar un modelo al dispositivo", "i-alert")}

\t\t\t\t<div class="layout layout--thirds" data-animate="fade-up">
{problema("El modelo acierta en el banco y falla en campo", "La exactitud medida al validar era alta y en operación el equipo se equivoca constantemente.", "Los datos de entrenamiento no representaban las condiciones reales: se tomaron con un solo equipo, en una sola sesión y sin variabilidad.", "Comparar la distribución de las características en operación con la del conjunto de entrenamiento. Si difieren, el problema son los datos.", "i-chart")}
{problema("No cabe en memoria pese a haberlo cuantizado", "El modelo cuantizado ocupa poco y el dispositivo se queda sin memoria al ejecutarlo.", "Se contó solo el tamaño de los parámetros y no el tensor arena que el intérprete necesita durante la inferencia.", "Sumar parámetros y tensor arena. El intérprete la declara al inicializarse; hay que reservarla y comprobar que quepa.", "i-layers")}
{problema("No cumple el periodo aunque la inferencia sea rápida", "El tiempo de inferencia es de pocos milisegundos y aun así el bucle pierde su ritmo.", "La extracción de características ocupa más que la inferencia, y solo se midió la segunda.", "Medir por separado extracción e inferencia y sumarlas contra el presupuesto del bucle de la sesión 4.", "i-clock")}
\t\t\t\t</div>

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{problema("La exactitud se degrada con los meses", "El sistema funcionaba bien al desplegarlo y va acertando cada vez menos sin que nadie lo toque.", "La distribución de los datos ha cambiado: el equipo envejece, se cambió una pieza o varió la estación.", "Vigilar en operación la proporción de cada clase predicha. Una deriva sostenida indica que toca reentrenar.", "i-wave")}
{problema("Dos equipos iguales deciden distinto", "Dos unidades con el mismo firmware clasifican de forma diferente la misma señal.", "Llevan versiones distintas del modelo y solo se versionaba el firmware.", "Publicar la versión del modelo junto a la del firmware en <code>/api/info</code> y compararlas.", "i-folder")}
\t\t\t\t</div>""", ESPARCIDO),
    icono="i-alert",
)

# ───────────────────────────────────────────────────── 15 · glosario
lamina(
    "glosario",
    "Glosario de la sesión 12 · Sesión 12",
    "Glosario de la sesión",
    envolver(f"""{cabecera(B, "Glosario de la sesión", "i-book")}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
{termino("TinyML", "tiny machine learning", "Inferencia de modelos sobre microcontroladores, con memoria del orden de kilobytes y consumo del orden de milivatios.")}
{termino("Inferencia", "inference", "Aplicación de un modelo ya entrenado a una entrada. Es un recorrido único y es lo único que cabe en el dispositivo.")}
{termino("Extracción de características", "feature extraction", "Transformación de la señal cruda en las magnitudes sobre las que decide el modelo. Suele ocupar más tiempo que la propia inferencia.")}
{termino("Cuantización", "quantization", "Sustitución de la coma flotante de 32 bits por enteros de 8 o 16. Reduce memoria y aprovecha la aritmética entera del procesador.")}
{termino("Pruning", "poda", "Eliminación de conexiones o unidades poco relevantes. Solo se traduce en velocidad si se pruning por bloques y no de forma dispersa.")}
{termino("Destilación", "distillation", "Entrenamiento de un modelo pequeño para reproducir la salida de uno grande. Exige el modelo grande y otro entrenamiento completo.")}
{termino("Matriz de confusión", "confusion matrix", "Reparto de aciertos y errores entre las clases. Sustituye a la exactitud global, que puede ser alta y no significar nada.")}
{termino("Tensor arena", "memoria de trabajo", "Región que el intérprete reserva durante la inferencia, aparte de los parámetros. Olvidarla es causa frecuente de falta de memoria.")}
{termino("Aprendizaje no supervisado", "unsupervised learning", "Método que no exige ejemplos etiquetados. Útil cuando obtener casos de fallo reales es difícil o costoso.")}
{termino("Drift", "deriva de la distribución", "Cambio con el tiempo de las condiciones que generan los datos. Degrada la exactitud sin que nadie modifique el sistema.")}
\t\t\t\t</div>"""),
    icono="i-book",
)

# ────────────────────────────────────── 16 · resumen y cierre del curso
lamina(
    "resumen",
    "Resumen de la sesión 12 y cierre del curso · Sesión 12",
    "Resumen y cierre del curso",
    envolver(f"""{cabecera(B, "Del primer pin a un dispositivo que decide", "i-check", pequeno=False)}

\t\t\t\t<div class="layout layout--split-even" data-animate="fade-up">
\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-cpu")}De esta sesión</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tSolo la inferencia se ejecuta en el dispositivo, y la selección de
\t\t\t\t\t\t\tcaracterísticas decide el resultado más que la complejidad del modelo.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tUn modelo se justifica frente a una <b>línea de base medida</b> con
\t\t\t\t\t\t\tumbrales y transformada, nunca frente a la nada. Y se evalúa con la
\t\t\t\t\t\t\tmatriz de confusión, no con la exactitud global.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="def">
\t\t\t\t\t\t<div class="def__label">{ico("i-flow")}Del curso</div>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tEl recorrido va de configurar un pin a un dispositivo que adquiere,
\t\t\t\t\t\t\tvalida, decide en local, publica su conclusión, se actualiza en remoto
\t\t\t\t\t\t\ty vuelve atrás si algo falla.
\t\t\t\t\t\t</p>
\t\t\t\t\t\t<p>
\t\t\t\t\t\t\tCada sesión respondió a una limitación de la anterior. Esa progresión
\t\t\t\t\t\t\tes lo que separa doce temas sueltos de un sistema.
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="usecases is-stretch" data-animate="fade-up">
\t\t\t\t\t<span class="usecases-label">Líneas de continuación</span>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-chip")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Otras variantes de la familia</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tInstrucciones vectoriales y memoria adicional abren audio y visión,
\t\t\t\t\t\t\t\tque este módulo no alcanza.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Tiempo real estricto</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tCuando el plazo no admite incumplimiento, la función se separa en un
\t\t\t\t\t\t\t\tmicrocontrolador dedicado sin pila de comunicaciones.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico("i-book")}
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<span class="usecase__name">Los 62 artículos del curso</span>
\t\t\t\t\t\t\t<span class="usecase__what">
\t\t\t\t\t\t\t\tTodos de acceso abierto, en <code>src/paper/</code>, con el índice de
\t\t\t\t\t\t\t\tqué lámina sostiene cada uno.
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>"""),
    icono="i-check",
    clases="slide",
)

# ─────────────────────────────────────────────────── 17 · referencias
lamina(
    "referencias",
    "Referencias de la sesión 12 · Sesión 12",
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
\t\t\t\t\t\t\t\t<span class="ref__title">Quantization and Deployment of Deep Neural Networks on Microcontrollers</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Novac, P.-E.; Boukli Hacene, G.; Pegatoquet, A. et al. (2021). <i>Sensors</i> 21(9), 2984. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3390/s21092984</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Cuantización · Medir sobre el destino</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Benchmarking TinyML Systems: Challenges and Direction</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Banbury, C. R.; Reddi, V. J.; Lam, M. et al. (2020). <i>arXiv:2003.04821</i>.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">arXiv:2003.04821</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Métricas · Elección de herramientas</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="refs">
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">An Adaptable and Unsupervised TinyML Anomaly Detection System for Extreme Industrial Environments</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Antonini, M.; Pincheira, M.; Vecchio, M.; Antonelli, F. (2023). <i>Sensors</i> 23(4), 2344. CC BY 4.0.</span>
\t\t\t\t\t\t\t\t<span class="ref__doi">doi:10.3390/s23042344</span>
\t\t\t\t\t\t\t\t<span class="ref__where">Caso de aplicación · Ejemplo 51</span>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t</div>
\t\t\t\t\t\t<div class="ref">
\t\t\t\t\t\t\t<span class="ref__body">
\t\t\t\t\t\t\t\t<span class="ref__title">Los 62 artículos del curso</span>
\t\t\t\t\t\t\t\t<span class="ref__meta">Todos de acceso abierto, en <code>src/paper/clase-NN/</code>. El índice con cita completa, licencia y qué lámina sostiene cada uno, en <code>src/paper/INDICE.md</code>.</span>
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
        {"clase": "clase-12", "sesion": "Sesión 12", "laminas": LAMINAS},
        "--dry" in sys.argv,
    )
