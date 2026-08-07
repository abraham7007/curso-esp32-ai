#!/usr/bin/env python3
"""Bloques comunes a todas las sesiones del curso.

Las láminas de concepto, de artículo y de «La hora del código» tienen una
estructura fija que el proyecto ya ha decidido. Vive aquí una sola vez para
que un cambio de criterio no haya que replicarlo en cada sesión.
"""


# Clases de .slide__content para una lámina cuyo sobrante vertical se reparte
# entre sus bloques en vez de acumularse al pie. Se pasa como segundo argumento
# de envolver().
#
# Cuándo lleva esto una lámina: cuando la medición dice que mejora, no por
# criterio estético. La decide `tools/proponer-stretch.mjs`, que prueba las
# variantes en el navegador y compara el mayor vacío contiguo; con solo dos
# bloques el reparto EMPEORA la lámina, porque todo el sobrante se va a una
# única separación.
ESPARCIDO = "slide__content stagger is-spread"


# Autoría y licencia del material. Viven aquí, en una sola cadena, para que
# cambiar la licencia sea cambiar una línea y no veinticuatro láminas.
#
# CC BY-NC-SA cubre LAS LÁMINAS Y LAS FIGURAS, que son obra propia. Cada
# artículo citado conserva la suya, y por eso la lámina de referencias muestra
# la licencia de cada uno por separado: son cosas distintas y confundirlas
# sería atribuirse permisos que no se tienen.
AUTOR = "Abraham Caso Torres"
LICENCIA = "CC BY-NC-SA 4.0"
LICENCIA_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es"


def credito(nota=""):
    """Línea de autoría y licencia, para la portada y para el cierre."""
    extra = f'\n\t\t\t\t\t<span>{nota}</span>' if nota else ""
    return (
        f'\t\t\t\t<div class="credito">\n'
        f'\t\t\t\t\t<span class="credito__autor">{AUTOR}</span>\n'
        f'\t\t\t\t\t<a class="credito__licencia" href="{LICENCIA_URL}"\n'
        f'\t\t\t\t\t\trel="license noopener" target="_blank">{LICENCIA}</a>'
        f'{extra}\n'
        f'\t\t\t\t</div>'
    )


def ico(nombre, clase="icon"):
    return f'<svg class="{clase}" aria-hidden="true"><use href="/course-icons.svg#{nombre}" /></svg>'


def cabecera(badge, titulo, icono="i-flow", pequeno=True):
    """Insignia de tema + título, el arranque común de una lámina de concepto."""
    t = "slide__title slide__title--sm" if pequeno else "slide__title"
    return f"""\t\t\t\t<span class="badge" data-animate="fade-up">
\t\t\t\t\t{ico(icono)}
\t\t\t\t\t{badge}
\t\t\t\t</span>

\t\t\t\t<h1 class="{t}" data-animate="fade-up">{titulo}</h1>"""


def envolver(interior, clases="slide__content stagger"):
    return f'\t\t\t<div class="{clases}">\n{interior}\n\t\t\t</div>'


def portada(sesion, titulo_html, tema_principal, tema_secundario,
            resultados, primera_lamina):
    """Portada de la sesión.

    Lleva EXACTAMENTE cinco cosas y ninguna más: quién imparte y qué sesión
    es, el título, los dos temas en una línea, los cuatro resultados de
    aprendizaje —solo su nombre— y la placa.

    Lo que se quitó y por qué: la «pregunta de apertura» ocupaba dos renglones
    para plantear algo que el profesor dice en voz alta, y cada resultado
    llevaba tres líneas de descripción que repetían lo que explican las
    láminas siguientes. Una portada anuncia; no enseña.

    `resultados` es una lista de (icono, nombre) con nombres de tres a seis
    palabras. Cuatro es el número: con más, la fila se parte y deja de leerse
    de un vistazo.
    """
    fichas = "\n".join(
        f"""\t\t\t\t\t<div class="usecase">
\t\t\t\t\t\t{ico(icono)}
\t\t\t\t\t\t<span class="usecase__name">{nombre}</span>
\t\t\t\t\t</div>"""
        for icono, nombre in resultados
    )
    return envolver(
        f"""\t\t\t\t<div class="layout layout--wide-left" data-animate="fade-up">
\t\t\t\t\t<div class="layout__text">
\t\t\t\t\t\t<span class="badge">
\t\t\t\t\t\t\t{sesion} · Fundamentos de ESP32 + AI · PIT 2026 — OTI-UNI
\t\t\t\t\t\t</span>

\t\t\t\t\t\t<h1 class="slide__title">{titulo_html}</h1>

\t\t\t\t\t\t<p class="slide__lede">
\t\t\t\t\t\t\t<strong>{tema_principal}</strong> {tema_secundario}
\t\t\t\t\t\t</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="hero-board">
\t\t\t\t\t\t<span class="hero-board__part" aria-hidden="true">
\t\t\t\t\t\t\t<wokwi-esp32-devkit-v1 led1="1"></wokwi-esp32-devkit-v1>
\t\t\t\t\t\t</span>
\t\t\t\t\t\t<span class="hero-board__caption">
\t\t\t\t\t\t\t<b>ESP32-WROOM-32</b>
\t\t\t\t\t\t\tDevKit V1
\t\t\t\t\t\t</span>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div data-animate="fade-up">
\t\t\t\t\t<div class="usecases-label">
\t\t\t\t\t\t{ico("i-target")}
\t\t\t\t\t\tAl terminar la sesión
\t\t\t\t\t</div>
\t\t\t\t\t<div class="usecases usecases--rotulos">
{fichas}
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<a class="btn btn--primary self-center" href="{primera_lamina}" data-animate="fade-up">
\t\t\t\t\tEmpezar →
\t\t\t\t</a>

{credito()}""",
        "slide__content stagger",
    )


def hora_del_codigo(
    ref,
    titulo,
    sobre,
    conceptos,
    conexion,
    salida,
    prompt,
    observar=None,
    *sobrantes,
    piezas="",
):
    """Estructura canónica de «La hora del código».

    Dos columnas con un reparto deliberado. A la izquierda, lo que el
    estudiante LEE antes de tocar nada: los conceptos que le faltan y el
    prompt que va a copiar. A la derecha, lo que MIRA delante del equipo:
    cómo conectarlo, qué sale por el monitor y qué buscar en esa salida.

    El análisis estuvo como franja al pie y bajó a la columna derecha: al pie
    quedaba separado de la traza que comenta, y se lee justamente mirándola.

    La tira de entregables, «por qué se pide así» y «concepto que se verifica»
    estuvieron aquí y se quitaron: los tres repetían algo que ya decía el
    prompt o el bloque de conceptos.

    El diagrama de conexión SIEMPRE lleva la placa, no solo los periféricos:
    una fila de piezas sueltas no es un montaje.
    """
    if sobrantes or observar is None:
        raise TypeError(
            "hora_del_codigo() recibió la forma antigua de once argumentos. "
            "La estructura nueva es (ref, titulo, sobre, conceptos, conexion, "
            "salida, prompt, observar): ver el apartado 4 de "
            "METODOLOGIA-DE-CURSO.md. Esta sesión aún está sin convertir."
        )

    # La placa va dibujada, no rotulada. Estuvo como etiqueta de texto porque
    # el elemento de Wokwi exige un import por lámina y donde faltaba no se
    # renderizaba nada; ahora el import lo añade el generador al ver la
    # etiqueta, así que el riesgo ya no existe. Ver generar-clase.py.
    devkit = (
        '\n\t\t\t\t\t\t\t\t\t\t<span class="hw-set__item hw-set__board">'
        "\n\t\t\t\t\t\t\t\t\t\t\t<wokwi-esp32-devkit-v1></wokwi-esp32-devkit-v1>"
        "\n\t\t\t\t\t\t\t\t\t\t\t<small>ESP32-WROOM-32</small>"
        "\n\t\t\t\t\t\t\t\t\t\t</span>"
    )
    hw = (
        f'\n\t\t\t\t\t\t\t\t\t<div class="hw-set">{devkit}{piezas}</div>'
        if piezas
        else ""
    )
    return envolver(
        f"""\t\t\t\t<div class="code-hour" data-animate="fade-up">
\t\t\t\t\t<div class="code-hour__header">
\t\t\t\t\t\t{ico("i-terminal")}
\t\t\t\t\t\t<span class="code-hour__label">La hora del código</span>
\t\t\t\t\t\t<span class="code-hour__ref">Ejemplo {ref}</span>
\t\t\t\t\t</div>

\t\t\t\t\t<h2 class="code-hour__title">{titulo}</h2>

\t\t\t\t\t<div class="code-hour__intro">
\t\t\t\t\t\t{ico("i-project")}
\t\t\t\t\t\t<p><b>Sobre el proyecto.</b> {sobre}</p>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="code-hour__body code-hour__body--pair-alt">
\t\t\t\t\t\t<div class="code-hour__stack">
\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-book")}Conceptos clave</h4>
\t\t\t\t\t\t\t\t<p>{conceptos}</p>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-robot")}Prompt para el asistente</h4>
\t\t\t\t\t\t\t\t<div class="prompt-box">{prompt}</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="code-hour__stack">
\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-plug")}Diagrama de conexión</h4>
\t\t\t\t\t\t\t\t<p>{conexion}</p>{hw}
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-terminal")}Monitor serial</h4>
\t\t\t\t\t\t\t\t<div class="term">{salida}</div>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="code-hour__section">
\t\t\t\t\t\t\t\t<h4>{ico("i-chart")}Análisis</h4>
\t\t\t\t\t\t\t\t<p>{observar}</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>""",
        "slide__content slide__content--flush stagger",
    )


def articulo(etiqueta, licencia, cita, titulo, objetivo, resultados,
             conclusiones, figuras, icono_cab="i-paper"):
    """Lámina de artículo: tres bloques en lista y dos figuras.

    El texto no compite con las figuras, las interpreta. Va en puntos cortos
    —cada uno localizable de un vistazo mientras se explica el gráfico de al
    lado— y no en párrafos corridos, que obligan a leerlos enteros para
    encontrar la cifra.

    Los tres bloques son EXACTAMENTE objetivo, resultados y conclusiones.
    Quedaron fuera el procedimiento experimental —que se cuenta de viva voz—,
    la tira de hallazgos —sus cifras están ahora en resultados— y el cierre
    «para esta sesión».

    `figuras` son dos: la que aporta las cifras del artículo y una segunda que
    saca de ellas la consecuencia. Una sola dejaba media lámina en blanco.
    """
    marcas = {"resultados": "i-chart", "conclusiones": "i-book"}

    def seccion(clave, rotulo, puntos):
        icono = marcas.get(clave, "i-target")
        variante = f" paper__section--{clave}" if clave in marcas else ""
        filas = "\n".join(
            f"\t\t\t\t\t\t\t\t\t<li>{x}</li>" for x in puntos
        )
        return f"""\t\t\t\t\t\t\t<div class="paper__section{variante}">
\t\t\t\t\t\t\t\t<div class="paper__section-label">{ico(icono)}{rotulo}</div>
\t\t\t\t\t\t\t\t<ul class="paper__lista">
{filas}
\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t</div>"""

    def figura(nombre, pie):
        return f"""\t\t\t\t\t\t\t<div class="figure">
\t\t\t\t\t\t\t\t<div class="figure__frame" data-figure="{nombre}"></div>
\t\t\t\t\t\t\t\t<p class="figure__caption">
\t\t\t\t\t\t\t\t\t{ico("i-chart")}
\t\t\t\t\t\t\t\t\t<span>{pie}</span>
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>"""

    bloques = "\n\n".join([
        seccion("objetivo", "Objetivo", objetivo),
        seccion("resultados", "Resultados", resultados),
        seccion("conclusiones", "Conclusiones", conclusiones),
    ])
    graficos = "\n\n".join(figura(n, pie) for n, pie in figuras)

    return envolver(
        f"""\t\t\t\t<div class="paper" data-animate="fade-up">
\t\t\t\t\t<div class="paper__header">
\t\t\t\t\t\t{ico(icono_cab)}
\t\t\t\t\t\t<span class="paper__label">{etiqueta}</span>
\t\t\t\t\t\t<span class="paper__license">{licencia}</span>
\t\t\t\t\t\t<span class="paper__fuente">Figuras propias a partir de las cifras publicadas</span>
\t\t\t\t\t</div>

\t\t\t\t\t<p class="paper__cite">{cita}</p>

\t\t\t\t\t<h2 class="paper__title">{titulo}</h2>

\t\t\t\t\t<div class="paper__body paper__body--figuras">
\t\t\t\t\t\t<div class="paper__notes">
{bloques}
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="paper__figuras">
{graficos}
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>""",
        "slide__content slide__content--flush stagger",
    )


def hallazgo(valor, texto, variante=""):
    v = f" finding--{variante}" if variante else ""
    return (
        f'\t\t\t\t\t\t<div class="finding{v}">\n'
        f'\t\t\t\t\t\t\t<span class="finding__value">{valor}</span>\n'
        f'\t\t\t\t\t\t\t<span class="finding__what">{texto}</span>\n'
        f"\t\t\t\t\t\t</div>"
    )


def problema(titulo, sintoma, porque, comprobar, icono="i-alert"):
    return f"""\t\t\t\t\t<div class="problem-card">
\t\t\t\t\t\t<div class="problem-card__head">{ico(icono)}{titulo}</div>
\t\t\t\t\t\t<div class="problem-card__body">
\t\t\t\t\t\t\t<p>{sintoma}</p>
\t\t\t\t\t\t\t<p><b>Por qué ocurre.</b> {porque}</p>
\t\t\t\t\t\t\t<p><b>Cómo comprobarlo.</b> {comprobar}</p>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>"""


def termino(es, en, definicion):
    return f"""\t\t\t\t\t<div class="glossary-item">
\t\t\t\t\t\t<h3>{es} <span class="glossary-item__alt">{en}</span></h3>
\t\t\t\t\t\t<p class="glossary-item__body">{definicion}</p>
\t\t\t\t\t</div>"""


