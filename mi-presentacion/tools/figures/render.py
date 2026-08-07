#!/usr/bin/env python3
"""Genera las figuras cuantitativas del curso a public/figures/*.svg.

Por qué existe este archivo en lugar de dibujar cada figura a mano en SVG:

1. Las figuras salen de los MISMOS números que la diapositiva enseña en el
   texto. Los datos viven aquí arriba, en una constante con nombre. Si un
   dato cambia (el tamaño de un artefacto, la resolución del ADC), se
   corrige en un sitio y la figura deja de contradecir al texto.
2. Una curva de transferencia o una forma de onda tiene cientos de puntos.
   Escribirlos a mano no es viable y "dibujarlos a ojo" produce gráficos que
   mienten sobre la magnitud de lo que ilustran.

Los SVG resultantes NO llevan colores fijos: al final se sustituye cada tinta
por la variable CSS equivalente (--fig-ink, --fig-accent, ...), de modo que
deck.js los inserta en línea y el mismo archivo se dibuja correcto en tema
claro y en tema oscuro.

Uso:  python3 tools/figures/render.py
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "public" / "figures"

# Tintas de trabajo. Son marcadores: cada una se reemplaza por su variable
# CSS al escribir el archivo. Se eligen valores muy separados entre sí para
# que la sustitución textual no pueda confundir dos tintas distintas.
INK = "#111111"
MUTED = "#666666"
GRID = "#cccccc"
SURFACE = "#f2f2f2"
PAPER = "#fdfdfd"
ACCENT = "#c8102e"
NAVY = "#1f3864"
OK = "#1a7f4b"
WARN = "#a86a00"

VARIABLE_POR_TINTA = {
    INK: "var(--fig-ink)",
    MUTED: "var(--fig-muted)",
    GRID: "var(--fig-grid)",
    SURFACE: "var(--fig-surface)",
    PAPER: "var(--fig-paper)",
    ACCENT: "var(--fig-accent)",
    NAVY: "var(--fig-navy)",
    OK: "var(--fig-ok)",
    WARN: "var(--fig-warn)",
}

MONO = ["IBM Plex Mono", "DejaVu Sans Mono", "monospace"]

plt.rcParams.update(
    {
        "font.family": "monospace",
        "font.monospace": MONO,
        "font.size": 9,
        "axes.edgecolor": GRID,
        "axes.labelcolor": MUTED,
        "axes.titlecolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "svg.fonttype": "none",  # el texto viaja como texto, no como curvas
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
    }
)


def escribir(fig, nombre: str) -> None:
    """Guarda la figura como SVG con las tintas convertidas en variables CSS."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / f"{nombre}.svg"
    fig.savefig(destino, format="svg", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)

    svg = destino.read_text(encoding="utf-8")

    # matplotlib emite las tintas en minúscula y a veces en forma rgb().
    for tinta, variable in VARIABLE_POR_TINTA.items():
        svg = svg.replace(tinta, variable).replace(tinta.upper(), variable)

    # El <svg> sale con width/height en pt: se quitan para que el marco de la
    # diapositiva mande y la figura escale con el contenedor.
    svg = re.sub(r'\s(width|height)="[\d.]+pt"', "", svg, count=2)
    # El prólogo XML y el DOCTYPE solo son válidos en un documento SVG
    # independiente. Aquí el archivo se inserta DENTRO del HTML de la
    # diapositiva, donde ambos son marcado ilegal que el navegador arrastra
    # al DOM como texto suelto.
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!DOCTYPE.*?>", "", svg, flags=re.S)
    # Los metadatos de matplotlib (fecha de creación, versión) harían que cada
    # regeneración produjera un archivo distinto aunque la figura no cambie.
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<!-- Created with matplotlib.*?-->", "", svg, flags=re.S)

    destino.write_text(svg.strip(), encoding="utf-8")
    print(f"  {destino.relative_to(RAIZ)}")


def limpiar_ejes(ax, *, ocultar=("top", "right")):
    for lado in ocultar:
        ax.spines[lado].set_visible(False)
    ax.tick_params(length=3, width=0.8)


# --------------------------------------------------------------------------
# 1. Curva de transferencia del ADC — cuantización de 12 bits
# --------------------------------------------------------------------------
# RESERVA — figuras escritas y correctas que NINGUNA lámina muestra hoy
# --------------------------------------------------------------------------
# No están en FIGURAS a propósito: generarlas dejaría archivos en
# public/figures/ que nadie enseña, y una figura que nadie enseña puede
# divergir del texto sin que nadie lo note, que es justo lo que este archivo
# existe para impedir.
#
# Las tres quedaron sin sitio porque la lámina de su tema resolvió lo mismo
# con un elemento interactivo, que es la forma más fuerte:
#
#   adc_transferencia   → clase-01/10 dibuja la curva completa con un
#                         deslizador; la figura solo amplía el escalón.
#   pwm_ciclo_trabajo   → clase-01/13 muestra la onda y el valor medio en vivo
#                         para cualquier ciclo; la figura compara tres fijos.
#   mapa_memoria        → clase-01/04 tiene un selector cuyos bloques ya están
#                         dimensionados a escala logarítmica de su capacidad.
#
# mapa_memoria SÍ tiene destino previsto: la sesión 10, cuyo Tema A es
# «Organización de la memoria aplicada al diseño: Flash, SRAM, RTC y PSRAM;
# contenido que se conserva y que se pierde en cada reinicio». Allí no existe
# el selector de la sesión 1 y la figura es el apoyo correcto. Al montar esa
# sesión, añadir mapa_memoria a FIGURAS.
# --------------------------------------------------------------------------
#   costo_de_preguntar      → clase-08/02 ya lleva una tabla de cuatro filas que
#                             compara los dos modelos escenario por escenario;
#                             la curva repetiría su primera fila.
#   tipos_memoria_arreglo   → clase-02/11 tiene lectura interactiva: el arreglo
#                             se redimensiona con un mando y las cuatro cifras
#                             se recalculan solas. Una figura estática resta.
# Ambas quedan escritas por si una edición futura reordena esas láminas.


# --------------------------------------------------------------------------
# Datos reales de la lámina: ADC de 12 bits, 4096 niveles, fondo de escala
# nominal 3.3 V con la atenuación de 11 dB. El escalón vale 3.3/4095 V.
ADC_BITS = 12
ADC_NIVELES = 2**ADC_BITS
ADC_FONDO_V = 3.3


def adc_transferencia():
    lsb = ADC_FONDO_V / (ADC_NIVELES - 1)

    fig, ax = plt.subplots(figsize=(6.6, 1.9))

    # Tramo ampliado: si se dibujaran los 4096 escalones no se vería ninguno.
    # Se muestran los primeros 8 códigos, que es donde el escalón se entiende.
    codigos = np.arange(0, 9)
    v = codigos * lsb

    ax.plot(
        [0, 8 * lsb],
        [0, 8],
        color=MUTED,
        lw=1.0,
        ls=(0, (4, 3)),
        label="magnitud continua",
    )
    ax.step(v, codigos, where="post", color=ACCENT, lw=2.0, label="código entregado")

    ax.annotate(
        f"1 LSB = {lsb * 1000:.2f} mV",
        xy=(2.5 * lsb, 2.4),
        xytext=(4.2 * lsb, 1.1),
        color=NAVY,
        fontsize=8.5,
        arrowprops={"arrowstyle": "->", "color": NAVY, "lw": 1.0},
    )

    ax.set_xlabel("tensión en el pin  (mV)")
    ax.set_ylabel("código del ADC")
    ax.set_xticks(v[::2])
    ax.set_xticklabels([f"{x * 1000:.1f}" for x in v[::2]])
    ax.set_yticks(codigos[::2])
    ax.grid(color=GRID, lw=0.6, alpha=0.9)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=8)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "adc-transferencia")


# --------------------------------------------------------------------------
# 2. PWM — el mismo período con tres ciclos de trabajo
# --------------------------------------------------------------------------
PWM_FREQ_HZ = 1000
PWM_CICLOS = [(0.25, OK), (0.50, NAVY), (0.80, ACCENT)]


def onda_cuadrada(periodo, ciclo, n_periodos):
    """Vértices exactos de la onda: solo los flancos, no un muestreo denso.

    Muestrear la onda punto a punto produce un SVG de cientos de miles de
    vértices para dibujar seis escalones. Una señal cuadrada queda descrita
    sin pérdida por sus transiciones.
    """
    t, y = [0.0], [1.0]
    for k in range(n_periodos):
        t0 = k * periodo
        t += [t0 + ciclo * periodo, t0 + ciclo * periodo, t0 + periodo, t0 + periodo]
        y += [1.0, 0.0, 0.0, 1.0]
    return np.array(t[:-1]), np.array(y[:-1])


def pwm_ciclo_trabajo():
    periodo_ms = 1000 / PWM_FREQ_HZ

    fig, axes = plt.subplots(
        3, 1, figsize=(6.8, 2.1), sharex=True, gridspec_kw={"hspace": 0.42}
    )

    for ax, (ciclo, color) in zip(axes, PWM_CICLOS):
        t, y = onda_cuadrada(periodo_ms, ciclo, 3)
        ax.plot(t, y, color=color, lw=1.8)
        ax.fill_between(t, 0, y, color=color, alpha=0.14)

        # El valor medio es lo que "ve" la carga: es la razón de ser del PWM.
        ax.axhline(ciclo, color=MUTED, lw=0.9, ls=(0, (3, 3)))
        ax.text(
            3 * periodo_ms * 1.01,
            ciclo,
            f"{ciclo * 100:.0f} %  →  {ciclo * 3.3:.2f} V medios",
            va="center",
            fontsize=8,
            color=color,
        )

        ax.set_yticks([0, 1])
        ax.set_yticklabels(["0", "3V3"], fontsize=8)
        ax.set_ylim(-0.18, 1.28)
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        limpiar_ejes(ax)

    axes[-1].set_xlabel(f"tiempo (ms)   ·   período fijo = {periodo_ms:.0f} ms")
    axes[-1].set_xticks(np.arange(0, 3 * periodo_ms + 0.1, periodo_ms / 2))

    escribir(fig, "pwm-ciclo-trabajo")


# --------------------------------------------------------------------------
# 3. Cadena de construcción — tamaño del artefacto en cada etapa
# --------------------------------------------------------------------------
# Mismos valores que la simulación de la diapositiva 20. Viven aquí para que
# la figura y el panel interactivo no puedan divergir.
CADENA = [
    ("main.cpp", 2, MUTED),
    ("main.i", 820, WARN),
    ("main.s", 96, NAVY),
    ("main.o", 34, NAVY),
    ("firmware.elf", 1150, ACCENT),
    ("firmware.bin", 262, OK),
]


def cadena_tamanos():
    nombres = [n for n, _, _ in CADENA]
    tam = [t for _, t, _ in CADENA]
    colores = [c for _, _, c in CADENA]

    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    barras = ax.bar(nombres, tam, color=colores, width=0.62)

    for barra, valor in zip(barras, tam):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 30,
            f"{valor} KB",
            ha="center",
            fontsize=8,
            color=MUTED,
        )

    ax.set_ylabel("tamaño del artefacto (KB)")
    ax.set_ylim(0, max(tam) * 1.18)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=8, labelrotation=18)
    limpiar_ejes(ax)

    escribir(fig, "cadena-tamanos")


# --------------------------------------------------------------------------
# 4. Xtensa frente a RISC-V — reparto real de la familia
# --------------------------------------------------------------------------
# Las siete variantes citadas en la lámina, con su año de anuncio. El eje de
# tiempo es lo que hace visible el argumento: RISC-V no sustituyó a Xtensa,
# convive con él y concentra las variantes recientes de bajo coste.
FAMILIA = [
    ("ESP32", 2016, "Xtensa LX6", 2, NAVY),
    ("ESP32-S2", 2019, "Xtensa LX7", 1, NAVY),
    ("ESP32-C3", 2020, "RISC-V", 1, ACCENT),
    ("ESP32-S3", 2021, "Xtensa LX7", 2, NAVY),
    ("ESP32-C6", 2022, "RISC-V", 1, ACCENT),
    ("ESP32-H2", 2022, "RISC-V", 1, ACCENT),
    ("ESP32-P4", 2023, "RISC-V", 2, ACCENT),
]


def familia_arquitecturas():
    # Formato apaisado: la figura convive con una columna de texto a su
    # derecha dentro de la misma diapositiva, y el alto es el recurso escaso.
    fig, ax = plt.subplots(figsize=(6.6, 2.5))

    for i, (nombre, anio, nucleo, _cores, color) in enumerate(FAMILIA):
        y = len(FAMILIA) - 1 - i
        ax.scatter(anio, y, s=170, color=color, zorder=3, edgecolor=PAPER, linewidth=1.4)
        ax.text(anio + 0.16, y + 0.16, nombre, fontsize=9, color=INK, va="center")
        ax.text(anio + 0.16, y - 0.24, nucleo, fontsize=7.5, color=MUTED, va="center")

    ax.set_yticks([])
    ax.set_xlim(2015.4, 2025.4)
    ax.set_ylim(-0.9, len(FAMILIA) - 0.1)
    ax.set_xticks(range(2016, 2025, 2))
    ax.set_xlabel("año de anuncio")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    # Leyenda construida a mano: la de matplotlib obligaría a duplicar cada
    # serie solo para tener dos entradas.
    # En «lower left»: los puntos caen en diagonal de arriba-izquierda a
    # abajo-derecha, así que la esquina inferior izquierda es la única que
    # queda libre. En «lower right» la leyenda pisaba la etiqueta del P4.
    ax.scatter([], [], s=110, color=NAVY, label="Xtensa (Cadence, propietaria)")
    ax.scatter([], [], s=110, color=ACCENT, label="RISC-V (abierta, sin regalías)")
    leg = ax.legend(loc="lower left", frameon=False, fontsize=8, scatterpoints=1)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "familia-arquitecturas")


# --------------------------------------------------------------------------
# 5. Mapa de memoria del ESP32 clásico
# --------------------------------------------------------------------------
# Cifras del ESP32-WROOM-32 usado en el curso: 520 KB de SRAM interna
# repartida, 448 KB de ROM y la Flash externa de 4 MB del módulo.
MEMORIA = [
    ("Flash externa\nSPI  ·  4 MB", 4096, ACCENT, "código + datos persistentes"),
    ("SRAM interna\n520 KB", 520, NAVY, "variables, pila, heap"),
    ("ROM interna\n448 KB", 448, MUTED, "bootloader de fábrica"),
    ("RTC RAM\n16 KB", 16, OK, "sobrevive al sueño profundo"),
]


def mapa_memoria():
    fig, ax = plt.subplots(figsize=(6.8, 1.9))

    etiquetas = [m[0] for m in MEMORIA]
    tam = [m[1] for m in MEMORIA]
    colores = [m[2] for m in MEMORIA]
    notas = [m[3] for m in MEMORIA]

    y = np.arange(len(MEMORIA))
    ax.barh(y, tam, color=colores, height=0.55)

    for i, (valor, nota) in enumerate(zip(tam, notas)):
        ax.text(valor + 60, i, nota, va="center", fontsize=8, color=MUTED)

    ax.set_yticks(y)
    ax.set_yticklabels(etiquetas, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("capacidad (KB, escala logarítmica)")
    ax.set_xscale("log")
    ax.set_xlim(8, 40000)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "mapa-memoria")


# --------------------------------------------------------------------------
# 6. Qué ocurre por detrás al pulsar «Upload»
# --------------------------------------------------------------------------
def flujo_flasheo():
    """Diagrama de secuencia entre el host y el chip durante el flasheo.

    Es la respuesta a "¿qué pasa por detrás?": la placa no se programa sola,
    hay una negociación por el puerto serie antes de transferir un solo byte.
    """
    pasos = [
        ("host", "chip", "DTR/RTS →  EN + GPIO0 a masa", NAVY),
        ("chip", "host", "waiting for download", MUTED),
        ("host", "chip", "sincronización  ·  0x07 0x07 0x12", NAVY),
        ("host", "chip", "cargador stub en SRAM", ACCENT),
        ("host", "chip", "bloques de firmware.bin  +  suma de verificación", ACCENT),
        ("chip", "host", "hash comprobado", OK),
        ("host", "chip", "reinicio  ·  EN liberado", NAVY),
    ]

    fig, ax = plt.subplots(figsize=(5.9, 3.4))
    x_host, x_chip = 0.0, 1.0

    for x, titulo in ((x_host, "host  (esptool)"), (x_chip, "ESP32  (ROM)")):
        ax.plot([x, x], [0, len(pasos) + 0.4], color=GRID, lw=1.2, zorder=1)
        ax.add_patch(
            Rectangle(
                (x - 0.24, len(pasos) + 0.4),
                0.48,
                0.55,
                facecolor=SURFACE,
                edgecolor=GRID,
                lw=1.0,
                zorder=2,
            )
        )
        ax.text(
            x,
            len(pasos) + 0.67,
            titulo,
            ha="center",
            va="center",
            fontsize=8.5,
            color=INK,
            zorder=3,
        )

    for i, (origen, _destino, texto, color) in enumerate(pasos):
        y = len(pasos) - i - 0.3
        desde, hasta = (x_host, x_chip) if origen == "host" else (x_chip, x_host)
        ax.add_patch(
            FancyArrowPatch(
                (desde, y),
                (hasta, y),
                arrowstyle="-|>",
                mutation_scale=11,
                color=color,
                lw=1.3,
                zorder=3,
                shrinkA=2,
                shrinkB=2,
            )
        )
        ax.text(0.5, y + 0.16, texto, ha="center", fontsize=7.8, color=color, zorder=4)

    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-0.2, len(pasos) + 1.2)
    ax.axis("off")

    escribir(fig, "flujo-flasheo")


# ==========================================================================
# FIGURAS DE LAS LÁMINAS DE PAPER
# ==========================================================================
# Estas figuras NO reproducen las de los artículos: dibujan, con la
# composición propia de este mazo, las CIFRAS que cada artículo publica en
# su texto. Los datos son hechos citables; el dibujo es nuestro. Importa
# porque uno de los tres artículos es CC BY-NC-ND, licencia que permite
# copiar el original íntegro pero no distribuir versiones derivadas de sus
# figuras. Cada valor lleva al lado la referencia de dónde sale.


# --------------------------------------------------------------------------
# 7. Ruido y error del ADC interno frente a un ADC externo
# --------------------------------------------------------------------------
# Cifras declaradas en Espinosa-Gavira et al. (2024), Procedia Comput. Sci.
# 237: el error del conversor interno se reparte en un intervalo de unos
# ±10 mV, mientras que el ADS1115 externo (16 bits, I2C) se mantiene en
# torno a ±2 mV, para los cuatro períodos de muestreo ensayados
# (200, 100, 50 y 10 ms). El artículo mitiga el ruido con un condensador de
# 0,1 uF en el pin y con sobremuestreo.
ADC_ERROR_INTERNO_MV = 10.0
ADC_ERROR_EXTERNO_MV = 2.0


def adc_interno_vs_externo():
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(7.4, 2.3), gridspec_kw={"width_ratios": [1.2, 1]}
    )

    # (a) Dispersión del error: dos distribuciones a la misma escala. La
    # comparación honesta exige el mismo eje, que es justo lo que hace
    # visible el orden de magnitud.
    x = np.linspace(-14, 14, 400)
    for sigma, color, etiqueta in (
        (ADC_ERROR_INTERNO_MV / 2.5, ACCENT, "ADC interno del ESP32"),
        (ADC_ERROR_EXTERNO_MV / 2.5, OK, "ADS1115 externo, 16 bits"),
    ):
        y = np.exp(-0.5 * (x / sigma) ** 2)
        ax1.plot(x, y, color=color, lw=1.8, label=etiqueta)
        ax1.fill_between(x, 0, y, color=color, alpha=0.15)

    ax1.axvline(0, color=GRID, lw=0.8)
    ax1.set_xlabel("error de medida (mV)")
    ax1.set_ylabel("densidad")
    ax1.set_yticks([])
    ax1.set_ylim(0, 1.05)
    ax1.set_xticks([-10, -5, 0, 5, 10])
    ax1.grid(axis="x", color=GRID, lw=0.6)
    ax1.set_axisbelow(True)
    limpiar_ejes(ax1, ocultar=("top", "right", "left"))
    # La leyenda va FUERA de los ejes, encima: dentro se montaba sobre la
    # cresta de la campana, que es justo el rasgo que hay que ver.
    leg = ax1.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        frameon=False,
        fontsize=7.5,
        ncol=1,
        handlelength=1.4,
    )
    for t in leg.get_texts():
        t.set_color(MUTED)

    # (b) Lo que gana cada medida de mitigación, en amplitud de ruido
    # relativa. El artículo las ordena así: sin nada, con condensador de
    # 0,1 uF, y con condensador + sobremuestreo.
    etiquetas = ["sin\nnada", "con\n0,1 µF", "+ sobre-\nmuestreo"]
    amplitud = [1.0, 0.45, 0.12]
    colores = [ACCENT, WARN, OK]
    barras = ax2.bar(etiquetas, amplitud, color=colores, width=0.58)
    for b, v in zip(barras, amplitud):
        ax2.text(
            b.get_x() + b.get_width() / 2,
            v + 0.04,
            f"{v:.2f}",
            ha="center",
            fontsize=8.5,
            color=MUTED,
        )
    ax2.set_ylabel("ruido relativo")
    ax2.set_ylim(0, 1.2)
    ax2.set_yticks([0, 0.5, 1.0])
    ax2.grid(axis="y", color=GRID, lw=0.6)
    ax2.set_axisbelow(True)
    ax2.tick_params(axis="x", labelsize=8)
    limpiar_ejes(ax2)

    fig.subplots_adjust(wspace=0.4, top=0.84)
    escribir(fig, "paper-adc-error")


# --------------------------------------------------------------------------
# 8. Mapa de la imagen que se graba en la Flash
# --------------------------------------------------------------------------
# Direcciones fijas del ESP32 documentadas por Espressif y recogidas en
# Howard & Irvin (2023), arXiv:2303.10204, Fig. 3.
IMAGEN_FLASH = [
    ("0x1000", "Bootloader\nde segunda etapa", 0x1000, 0x8000, NAVY),
    ("0x8000", "Tabla de\nparticiones", 0x8000, 0x10000, WARN),
    ("0x10000", "Aplicación\n(firmware.bin)", 0x10000, 0x40000, ACCENT),
]


def imagen_flash():
    # Mapa horizontal, no vertical: apilada resultaba más alta que ancha y en
    # una lámina con dos figuras no cabían las dos. Las direcciones se leen de
    # izquierda a derecha, que es además como se recorre la Flash al grabar.
    fig, ax = plt.subplots(figsize=(5.8, 2.1))

    total = max(fin for _, _, _, fin, _ in IMAGEN_FLASH)
    for direccion, nombre, inicio, fin, color in IMAGEN_FLASH:
        ancho = fin - inicio
        ax.add_patch(Rectangle((inicio, 0), ancho, 1, facecolor=color,
                               alpha=0.16, edgecolor=color, lw=1.6))
        # El gestor de arranque y la tabla ocupan una fracción mínima de la
        # Flash: su rótulo no cabe dentro y se saca arriba con guía.
        estrecho = ancho / total < 0.12
        if estrecho:
            ax.annotate(nombre.replace(" de ", "\nde "),
                        xy=(inicio + ancho / 2, 1.0),
                        xytext=(inicio + ancho / 2, 1.55),
                        ha="center", va="bottom", fontsize=7.5, color=INK,
                        arrowprops=dict(arrowstyle="-", color=GRID, lw=0.7))
        else:
            ax.text(inicio + ancho / 2, 0.5, nombre, ha="center", va="center",
                    fontsize=8.5, color=INK)
        ax.text(inicio, -0.14, direccion, ha="center", va="top", fontsize=7.5,
                color=color)

    ax.set_xlim(0x800, total)
    ax.set_ylim(-0.5, 2.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for lado in ("top", "right", "bottom", "left"):
        ax.spines[lado].set_visible(False)

    escribir(fig, "imagen-flash")


# --------------------------------------------------------------------------
# 9. Hasta dónde llega hoy un asistente generando firmware
# --------------------------------------------------------------------------
# Izquierda: Babiuch & Smutny (2026), Future Internet 18(2) 94. De 27
# modelos evaluados, cuántos entregan una solución utilizable según sube la
# complejidad del escenario (del 1 al 8).
# Derecha: Xu et al. (2026), EmbedAgent, ICSE'26. pass@1 del mejor modelo
# en cada tipo de tarea.
LLM_ESCENARIOS = [
    ("sensor", 19),
    ("distancia", 23),
    ("ThingSpeak", 20),
    ("Beebotte", 19),
    ("Firebase", 9),
    ("InfluxDB", 11),
    ("+ Grafana", 3),
]

LLM_TAREAS = [
    ("Código con el\nesquema dado", 55.6, NAVY),
    ("Código sin\nesquema", 50.0, NAVY),
    ("Migrar a Pico\n(MicroPython)", 73.8, OK),
    ("Migrar a ESP32\n(ESP-IDF)", 29.4, ACCENT),
]


def paper_llm_limites():
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(7.6, 2.4), gridspec_kw={"width_ratios": [1.25, 1]}
    )

    nombres = [n for n, _ in LLM_ESCENARIOS]
    valores = [v for _, v in LLM_ESCENARIOS]
    colores = [OK if v >= 18 else (WARN if v >= 9 else ACCENT) for v in valores]

    ax1.bar(range(len(valores)), valores, color=colores, width=0.62)
    for i, v in enumerate(valores):
        ax1.text(i, v + 0.7, str(v), ha="center", fontsize=8, color=MUTED)
    ax1.axhline(27, color=MUTED, lw=0.9, ls=(0, (3, 3)))
    ax1.text(6.45, 27.7, "27 evaluados", ha="right", fontsize=7.5, color=MUTED)

    ax1.set_xticks(range(len(nombres)))
    ax1.set_xticklabels(nombres, rotation=28, ha="right", fontsize=7.5)
    ax1.set_xlabel("escenario, de menor a mayor complejidad  →", fontsize=7.5)
    ax1.set_ylabel("modelos con solución\nutilizable  (de 27)")
    ax1.set_ylim(0, 31)
    ax1.grid(axis="y", color=GRID, lw=0.6)
    ax1.set_axisbelow(True)
    limpiar_ejes(ax1)

    etiquetas = [n for n, _, _ in LLM_TAREAS]
    pass1 = [v for _, v, _ in LLM_TAREAS]
    cols = [c for _, _, c in LLM_TAREAS]
    y = np.arange(len(etiquetas))
    ax2.barh(y, pass1, color=cols, height=0.6)
    for i, v in enumerate(pass1):
        ax2.text(v + 1.5, i, f"{v:.1f} %", va="center", fontsize=8, color=MUTED)
    ax2.set_yticks(y)
    ax2.set_yticklabels(etiquetas, fontsize=7.5)
    ax2.invert_yaxis()
    ax2.set_xlabel("pass@1 del mejor modelo (%)")
    ax2.set_xlim(0, 100)
    ax2.grid(axis="x", color=GRID, lw=0.6)
    ax2.set_axisbelow(True)
    limpiar_ejes(ax2, ocultar=("top", "right", "left"))

    fig.subplots_adjust(wspace=0.5)
    escribir(fig, "paper-llm-limites")


# --------------------------------------------------------------------------
# 10. Tiempo de ejecución por lenguaje sobre el mismo ESP32
# --------------------------------------------------------------------------
# Cifras de la Tabla 5 de Plauska, Liutkevicius y Janaviciute (2023),
# Electronics 12(1) 143, para la longitud de entrada de 1024 muestras.
# Escala logarítmica: sin ella, MicroPython aplasta al resto y no se ve la
# diferencia —pequeña— entre los tres lenguajes compilados.
LENGUAJES = ["C/C++", "TinyGo", "Rust", "MicroPython"]
TIEMPOS_US = {
    "FFT": [1821.5, 3331.0, 3525.5, 844854.8],
    "CRC-32": [117.6, 110.0, 113.8, 47035.1],
    "Filtro FIR": [30054.7, 29934.0, 24219.2, 9066768.4],
}


def paper_lenguajes_esp32():
    fig, ax = plt.subplots(figsize=(7.2, 2.3))

    n = len(TIEMPOS_US)
    ancho = 0.2
    x = np.arange(n)
    colores = [NAVY, OK, WARN, ACCENT]

    for i, (lenguaje, color) in enumerate(zip(LENGUAJES, colores)):
        valores = [TIEMPOS_US[alg][i] for alg in TIEMPOS_US]
        ax.bar(x + (i - 1.5) * ancho, valores, ancho, color=color, label=lenguaje)

    ax.set_yscale("log")
    ax.set_ylabel("tiempo medio (µs, escala log.)")
    ax.set_xticks(x)
    ax.set_xticklabels(list(TIEMPOS_US.keys()), fontsize=8.5)
    ax.set_xlabel("entrada de 1024 muestras", fontsize=8)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(
        loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=4, frameon=False, fontsize=8
    )
    for t in leg.get_texts():
        t.set_color(MUTED)

    fig.subplots_adjust(top=0.84)
    escribir(fig, "paper-lenguajes-esp32")


# --------------------------------------------------------------------------
# 11. Tramas recibidas completas sobre un enlace serie
# --------------------------------------------------------------------------
# Cifras de Cakic, Zigic y Milosavljevic (2022), Zbornik Radova 32, 95-100:
# porcentaje de paquetes de 50 caracteres recibidos completos en una sola
# lectura, y porcentaje total tras recomponer los partidos entre lecturas.
UART_ENVIOS = [10, 100, 1000, 10000]
UART_DIRECTO = [54.0, 51.4, 51.13, 49.92]
UART_RECOMPUESTO = [77.0, 75.7, 70.76, 70.05]


def paper_uart_tramas():
    fig, ax = plt.subplots(figsize=(7.0, 2.2))

    x = np.arange(len(UART_ENVIOS))
    ax.bar(x - 0.19, UART_DIRECTO, 0.38, color=ACCENT, label="en una sola lectura")
    ax.bar(
        x + 0.19,
        UART_RECOMPUESTO,
        0.38,
        color=OK,
        label="tras recomponer la trama",
    )

    for i, (a, b) in enumerate(zip(UART_DIRECTO, UART_RECOMPUESTO)):
        ax.text(i - 0.19, a + 1.5, f"{a:.0f}", ha="center", fontsize=8, color=MUTED)
        ax.text(i + 0.19, b + 1.5, f"{b:.0f}", ha="center", fontsize=8, color=MUTED)

    ax.set_ylabel("tramas completas (%)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{n:,}".replace(",", " ") for n in UART_ENVIOS], fontsize=8.5)
    ax.set_xlabel("paquetes enviados", fontsize=8)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper right", frameon=False, fontsize=8)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-uart-tramas")


# --------------------------------------------------------------------------
# 12. Sesión 5 — banderas frente a estados: crecimiento del espacio
# --------------------------------------------------------------------------
# El argumento de la lámina de apertura: n banderas admiten 2^n situaciones
# representables, de las que el programa define un puñado. Una variable de
# estado con n valores admite exactamente n.
BANDERAS_MAX = 10
ESTADOS_DEFINIDOS = 5


def banderas_vs_estados():
    n = np.arange(1, BANDERAS_MAX + 1)
    fig, ax = plt.subplots(figsize=(6.2, 2.4))

    ax.plot(n, 2.0**n, color=ACCENT, lw=2.2, marker="o", ms=4,
            label="banderas independientes · 2ⁿ combinaciones")
    ax.plot(n, n, color=OK, lw=2.2, marker="o", ms=4,
            label="variable de estado · n valores")
    ax.axhline(ESTADOS_DEFINIDOS, color=MUTED, lw=1.1, ls="--")
    ax.text(BANDERAS_MAX, ESTADOS_DEFINIDOS * 1.35,
            f"{ESTADOS_DEFINIDOS} situaciones definidas en el código",
            ha="right", fontsize=7.5, color=MUTED)

    ax.annotate("1024 situaciones\nalcanzables sin especificar",
                (BANDERAS_MAX, 2.0**BANDERAS_MAX), textcoords="offset points",
                xytext=(-12, -34), ha="right", fontsize=7.5, color=ACCENT)

    ax.set_yscale("log")
    ax.set_xlabel("número de banderas, o de estados declarados")
    ax.set_ylabel("situaciones representables")
    ax.set_xlim(1, BANDERAS_MAX)
    ax.set_xticks(n)
    ax.grid(color=GRID, lw=0.6, which="both")
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=8)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "banderas-vs-estados")


# --------------------------------------------------------------------------
# 13. Sesión 5 · artículo — análisis plano frente a compositivo
# --------------------------------------------------------------------------
# Cifras publicadas por Carnevali et al. (2022): de 27 modelos, el análisis
# plano resolvió 2 antes del plazo de 4 h; el compositivo, los 27 en menos de
# 30 min.
STATECHARTS_TOTAL = 27
STATECHARTS_PLANO = 2


def paper_statecharts_escala():
    fig, ax = plt.subplots(figsize=(5.6, 2.3))
    etiquetas = ["análisis plano", "análisis compositivo"]
    resueltos = [STATECHARTS_PLANO, STATECHARTS_TOTAL]
    colores = [ACCENT, OK]

    barras = ax.barh(etiquetas, resueltos, color=colores, height=0.46)
    ax.barh(etiquetas, [STATECHARTS_TOTAL] * 2, color=GRID, height=0.46,
            zorder=0, alpha=0.35)

    for barra, valor in zip(barras, resueltos):
        ax.text(valor + 0.5, barra.get_y() + barra.get_height() / 2,
                f"{valor} de {STATECHARTS_TOTAL}", va="center", fontsize=8.5,
                color=INK)

    ax.text(STATECHARTS_PLANO + 0.5, -0.42, "los 25 restantes se interrumpieron a las 4 h",
            fontsize=7.5, color=MUTED)
    ax.text(0.4, 1.36, "todos resueltos en menos de 30 min",
            fontsize=7.5, color=MUTED)

    ax.set_xlim(0, STATECHARTS_TOTAL + 3)
    ax.set_xlabel("modelos evaluados con éxito")
    ax.tick_params(axis="y", labelsize=8.5)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "paper-statecharts-escala")


# --------------------------------------------------------------------------
# 14. Sesión 6 · artículo — conmutación dentro y entre núcleos
# --------------------------------------------------------------------------
# Cifras publicadas por Arm et al. (2022) sobre ESP32 a 240 MHz. La escala
# logarítmica es obligada: hay cuatro órdenes de magnitud entre las dos.
CONMUTACION_MS = [("mismo núcleo", 0.012, OK), ("entre núcleos", 190.334, ACCENT)]


def paper_conmutacion_nucleos():
    nombres = [n for n, _, _ in CONMUTACION_MS]
    valores = [v for _, v, _ in CONMUTACION_MS]
    colores = [c for _, _, c in CONMUTACION_MS]

    fig, ax = plt.subplots(figsize=(5.6, 2.4))
    barras = ax.bar(nombres, valores, color=colores, width=0.5)
    ax.set_yscale("log")

    for barra, valor in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width() / 2, valor * 1.35,
                f"{valor:.3f} ms".replace(".", ","), ha="center", fontsize=9,
                color=INK)

    razon = valores[1] / valores[0]
    ax.annotate("", xy=(0.5, valores[1]), xytext=(0.5, valores[0]),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.1))
    ax.text(0.56, np.sqrt(valores[0] * valores[1]), f"×{razon:,.0f}".replace(",", " "),
            fontsize=9, color=MUTED, va="center")

    ax.set_ylabel("tiempo de conmutación (ms)")
    ax.set_ylim(0.005, 900)
    ax.grid(axis="y", color=GRID, lw=0.6, which="both")
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=9)
    limpiar_ejes(ax)

    escribir(fig, "paper-conmutacion-nucleos")


# --------------------------------------------------------------------------
# 15. Sesión 6 · artículo — costo del tick según cuántas tareas despiertan
# --------------------------------------------------------------------------
# Cifras publicadas por Miranda et al. (2021): 1,5 µs sin desbloqueos y
# 60,75 µs en el instante crítico con diez tareas; cada tarea que entra en su
# lista cuesta unos 3,7 µs.
TICK_BASE_US = 1.5
TICK_POR_TAREA_US = 3.7
TICK_PEOR_US = 60.75
TICK_TAREAS = 10


def paper_costo_tick():
    n = np.arange(0, TICK_TAREAS + 1)
    modelo = TICK_BASE_US + TICK_POR_TAREA_US * n

    fig, ax = plt.subplots(figsize=(7.0, 2.0))
    ax.plot(n, modelo, color=NAVY, lw=2, marker="o", ms=4,
            label="modelo: 1,5 µs + 3,7 µs por tarea")
    ax.scatter([TICK_TAREAS], [TICK_PEOR_US], s=90, color=ACCENT, zorder=4,
               label="peor caso medido en el instante crítico")

    ax.annotate(f"{TICK_PEOR_US} µs".replace(".", ","),
                (TICK_TAREAS, TICK_PEOR_US), textcoords="offset points",
                xytext=(-8, 6), ha="right", fontsize=8, color=ACCENT)
    ax.annotate(f"{TICK_BASE_US} µs".replace(".", ","), (0, TICK_BASE_US),
                textcoords="offset points", xytext=(8, 4), fontsize=8, color=NAVY)

    ax.set_xlabel("tareas que se desbloquean en el mismo tick")
    ax.set_ylabel("duración del tick (µs)")
    ax.set_xlim(0, TICK_TAREAS)
    ax.set_ylim(0, 70)
    ax.set_xticks(n)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5, scatterpoints=1)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-costo-tick")


# --------------------------------------------------------------------------
# 16. Sesión 6 — periodo de muestreo con bucle único y con tareas
# --------------------------------------------------------------------------
# Reproduce la traza de la lámina: el bucle único pierde el periodo mientras
# publica, y las tareas lo conservan. La escala logarítmica hace visible el
# pico sin aplastar el resto.
PERIODO_OBJETIVO_MS = 1.0
PERIODO_BLOQUEO_MS = 380.0
PERIODO_N = 600
PERIODO_INSTANTE = 300


def periodo_bucle_vs_tareas():
    n = np.arange(PERIODO_N)
    generador = np.random.default_rng(11)

    bucle = PERIODO_OBJETIVO_MS + generador.normal(0, 0.02, PERIODO_N)
    bucle[PERIODO_INSTANTE] = PERIODO_BLOQUEO_MS + PERIODO_OBJETIVO_MS
    tareas = PERIODO_OBJETIVO_MS + generador.normal(0, 0.02, PERIODO_N)
    tareas = np.clip(tareas, 0.94, 1.06)

    fig, ax = plt.subplots(figsize=(6.4, 2.4))
    ax.plot(n, bucle, color=ACCENT, lw=1.4, label="bucle único")
    ax.plot(n, tareas, color=OK, lw=1.4, label="dos tareas")
    ax.set_yscale("log")

    ax.annotate(f"{PERIODO_BLOQUEO_MS:.0f} ms: la publicación bloquea el bucle",
                (PERIODO_INSTANTE, PERIODO_BLOQUEO_MS), textcoords="offset points",
                xytext=(-10, -6), ha="right", fontsize=7.5, color=ACCENT)

    ax.set_xlabel("número de muestra")
    ax.set_ylabel("periodo real (ms)")
    ax.set_xlim(0, PERIODO_N - 1)
    ax.set_ylim(0.7, 700)
    ax.grid(color=GRID, lw=0.6, which="both")
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=8)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "periodo-bucle-vs-tareas")


# --------------------------------------------------------------------------
# 17. Sesión 7 — lo que cada capa añade a 12 bytes de dato
# --------------------------------------------------------------------------
# Cifras de la lámina: el dato útil y las cabeceras de HTTP, TCP, IP y el
# enlace inalámbrico.
CAPAS = [
    ("dato útil", 12, OK),
    ("HTTP", 180, ACCENT),
    ("TCP", 20, NAVY),
    ("IP", 20, MUTED),
    ("WiFi", 34, WARN),
]


def capas_sobrecarga():
    total = sum(v for _, v, _ in CAPAS)
    fig, ax = plt.subplots(figsize=(6.4, 1.6))

    izquierda = 0
    for nombre, valor, color in CAPAS:
        ax.barh(0, valor, left=izquierda, color=color, height=0.5,
                edgecolor=PAPER, linewidth=1.2)
        if valor >= 18:
            ax.text(izquierda + valor / 2, 0, f"{valor}", ha="center",
                    va="center", fontsize=8, color=PAPER)
        ax.text(izquierda + valor / 2, -0.44, nombre, ha="center", va="top",
                fontsize=7.5, color=MUTED)
        izquierda += valor

    ax.text(total, 0.42, f"{total} bytes en total · {12 / total:.1%} es dato",
            ha="right", fontsize=8, color=INK)

    ax.set_xlim(0, total)
    ax.set_ylim(-1.0, 0.62)
    ax.set_yticks([])
    ax.set_xlabel("bytes transmitidos")
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "capas-sobrecarga")


# --------------------------------------------------------------------------
# 18. Sesión 7 — solapamiento de los canales de 2,4 GHz
# --------------------------------------------------------------------------
# Trece canales separados 5 MHz con una anchura ocupada de 22 MHz: solo 1, 6
# y 11 no se solapan entre sí. Es el argumento de la lámina, dibujado.
WIFI_CANALES = 13
WIFI_SEPARACION_MHZ = 5
WIFI_ANCHO_MHZ = 22
WIFI_BASE_MHZ = 2412
WIFI_NO_SOLAPADOS = (1, 6, 11)


def canales_wifi():
    fig, ax = plt.subplots(figsize=(6.4, 2.3))

    for canal in range(1, WIFI_CANALES + 1):
        centro = WIFI_BASE_MHZ + (canal - 1) * WIFI_SEPARACION_MHZ
        destacado = canal in WIFI_NO_SOLAPADOS
        color = ACCENT if destacado else MUTED
        x = np.linspace(centro - WIFI_ANCHO_MHZ / 2, centro + WIFI_ANCHO_MHZ / 2, 120)
        # Perfil triangular suavizado: basta para mostrar la anchura ocupada.
        y = np.cos(np.pi * (x - centro) / WIFI_ANCHO_MHZ) ** 2
        ax.plot(x, y, color=color, lw=2.0 if destacado else 0.9,
                alpha=1.0 if destacado else 0.5)
        if destacado:
            ax.fill_between(x, 0, y, color=color, alpha=0.13)
        ax.text(centro, -0.09, str(canal), ha="center", fontsize=7.5,
                color=color if destacado else GRID)

    ax.text(WIFI_BASE_MHZ, 1.12, "1, 6 y 11 son los únicos que no se solapan",
            fontsize=8, color=ACCENT)

    ax.set_xlabel("frecuencia (MHz)")
    ax.set_ylabel("potencia relativa")
    ax.set_xlim(WIFI_BASE_MHZ - 15, WIFI_BASE_MHZ + (WIFI_CANALES - 1) * 5 + 15)
    ax.set_ylim(-0.16, 1.26)
    ax.set_yticks([])
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "canales-wifi")


# --------------------------------------------------------------------------
# 19. Sesión 8 — política periódica frente a envío por variación
# --------------------------------------------------------------------------
# Serie de temperatura interior con la deriva lenta que describe la lámina.
# La política por variación publica solo al superar el umbral, más un
# mensaje de seguridad cada periodo largo.
TRANSMISION_HORAS = 24
TRANSMISION_PERIODO_S = 5
TRANSMISION_UMBRAL_C = 0.3
TRANSMISION_SEGURIDAD_S = 3600


def politica_transmision():
    generador = np.random.default_rng(3)
    n = TRANSMISION_HORAS * 3600 // TRANSMISION_PERIODO_S
    t = np.linspace(0, TRANSMISION_HORAS, n)
    # Ciclo diario suave más ruido de medida.
    serie = 22.5 + 2.2 * np.sin(2 * np.pi * (t - 6) / 24) + generador.normal(0, 0.05, n)

    enviados, ultimo, ultimo_t = [], serie[0], 0.0
    for i in range(n):
        vence = (t[i] - ultimo_t) * 3600 >= TRANSMISION_SEGURIDAD_S
        if abs(serie[i] - ultimo) >= TRANSMISION_UMBRAL_C or vence or i == 0:
            enviados.append(i)
            ultimo, ultimo_t = serie[i], t[i]

    fig, ax = plt.subplots(figsize=(6.4, 2.4))
    ax.plot(t, serie, color=GRID, lw=0.9, label="magnitud medida cada 5 s")
    ax.scatter(t[enviados], serie[enviados], s=13, color=ACCENT, zorder=3,
               label=f"publicaciones por variación: {len(enviados)}")

    ax.text(TRANSMISION_HORAS, serie.min() - 0.35,
            f"la política periódica habría enviado {n:,} mensajes".replace(",", " "),
            ha="right", fontsize=7.5, color=MUTED)

    ax.set_xlabel("hora del día")
    ax.set_ylabel("temperatura (°C)")
    ax.set_xlim(0, TRANSMISION_HORAS)
    ax.set_xticks(range(0, TRANSMISION_HORAS + 1, 4))
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5, scatterpoints=1)
    for txt in leg.get_texts():
        txt.set_color(MUTED)

    escribir(fig, "politica-transmision")


# --------------------------------------------------------------------------
# 20. Sesión 8 — paquetes por mensaje según el nivel de calidad de servicio
# --------------------------------------------------------------------------
QOS = [("QoS 0", 1, OK, "como máximo una vez"),
       ("QoS 1", 2, NAVY, "al menos una vez"),
       ("QoS 2", 4, ACCENT, "exactamente una vez")]


def qos_paquetes():
    nombres = [n for n, _, _, _ in QOS]
    valores = [v for _, v, _, _ in QOS]
    colores = [c for _, _, c, _ in QOS]

    fig, ax = plt.subplots(figsize=(5.8, 2.2))
    barras = ax.bar(nombres, valores, color=colores, width=0.5)

    for barra, (nombre, valor, _c, garantia) in zip(barras, QOS):
        ax.text(barra.get_x() + barra.get_width() / 2, valor + 0.12,
                f"{valor}", ha="center", fontsize=10, color=INK)
        ax.text(barra.get_x() + barra.get_width() / 2, -0.55, garantia,
                ha="center", fontsize=7, color=MUTED)

    ax.set_ylabel("paquetes por mensaje")
    ax.set_ylim(0, 4.9)
    ax.set_yticks(range(0, 5))
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=9)
    limpiar_ejes(ax)

    escribir(fig, "qos-paquetes")



# --------------------------------------------------------------------------
# 21. Sesión 2 — alcance de un cambio de componente según la arquitectura
# --------------------------------------------------------------------------
# El artículo describe el problema como que cualquier cambio de componente
# obliga a revisar la implementación entera. La figura traduce esa frase a lo
# único que la hace medible: cuántos módulos hay que tocar. Con el acceso al
# hardware repartido por todo el programa, esa cuenta crece con el proyecto;
# con la capa de acceso separada, no crece.
CAPAS_MODULOS = np.arange(3, 31)


def paper_capas_alcance():
    fig, ax = plt.subplots(figsize=(6.9, 2.2))

    ax.plot(CAPAS_MODULOS, CAPAS_MODULOS, color=ACCENT, lw=2,
            label="monolítico: el acceso al hardware está en todos")
    ax.plot(CAPAS_MODULOS, np.ones_like(CAPAS_MODULOS), color=OK, lw=2,
            label="por capas: solo la capa de acceso al hardware")

    ax.fill_between(CAPAS_MODULOS, np.ones_like(CAPAS_MODULOS), CAPAS_MODULOS,
                    color=ACCENT, alpha=0.07)
    ax.annotate("lo que ahorra la separación", (21, 11), fontsize=8,
                color=MUTED, ha="center")

    ax.set_xlabel("módulos del proyecto")
    ax.set_ylabel("módulos a revisar")
    ax.set_xlim(3, 30)
    ax.set_ylim(0, 31)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-capas-alcance")


# --------------------------------------------------------------------------
# 22. Sesión 2 — defectos hallados en firmware de código abierto
# --------------------------------------------------------------------------
# Cifras del artículo: 258 proyectos analizados, 709 defectos localizados, 535
# de ellos vulnerabilidades y 376 confirmados por quien mantiene el proyecto.
# El embudo es la forma honesta de presentarlo: cada barra es un subconjunto
# de la anterior, no una categoría paralela.
DEFECTOS = [
    ("localizados por el analizador", 709, NAVY),
    ("que son vulnerabilidades", 535, WARN),
    ("confirmados por el responsable", 376, ACCENT),
]
DEFECTOS_PROYECTOS = 258


def paper_defectos_firmware():
    fig, ax = plt.subplots(figsize=(7.0, 2.1))

    y = np.arange(len(DEFECTOS))[::-1]
    for pos, (etiqueta, valor, color) in zip(y, DEFECTOS):
        ax.barh(pos, valor, height=0.55, color=color)
        ax.text(valor + 12, pos, str(valor), va="center", fontsize=9, color=color)
        ax.text(12, pos, etiqueta, va="center", fontsize=8, color=PAPER)

    ax.text(709, len(DEFECTOS) - 0.4,
            "sobre %d proyectos embebidos de código abierto" % DEFECTOS_PROYECTOS,
            ha="right", fontsize=7.5, color=MUTED)

    ax.set_xlim(0, 800)
    ax.set_ylim(-0.6, len(DEFECTOS) - 0.1)
    ax.set_yticks([])
    ax.set_xlabel("defectos")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "paper-defectos-firmware")


# --------------------------------------------------------------------------
# 23. Sesión 3 — la trama y su campo de comprobación
# --------------------------------------------------------------------------
# La trama se dibuja a escala de bytes con los cinco campos que enumera la
# lámina. El código de comprobación no se inventa: se calcula aquí el FCS de
# X.25 (polinomio 0x1021 reflejado) sobre la carga real y sobre la misma carga
# con un bit alterado, y se muestran los dos valores resultantes.
TRAMA_CARGA = b"T=23.4C"


def _fcs_x25(datos):
    reg = 0xFFFF
    for byte in datos:
        reg ^= byte
        for _ in range(8):
            reg = (reg >> 1) ^ 0x8408 if reg & 1 else reg >> 1
    return (~reg) & 0xFFFF


def paper_trama_crc():
    carga_mala = bytes([TRAMA_CARGA[0] ^ 0x01]) + TRAMA_CARGA[1:]
    fcs_bien = _fcs_x25(TRAMA_CARGA)
    fcs_mal = _fcs_x25(carga_mala)

    campos = [
        ("delimitador", 1, MUTED),
        ("dirección", 1, NAVY),
        ("control", 1, NAVY),
        ("carga útil", len(TRAMA_CARGA), SURFACE),
        ("comprobación", 2, ACCENT),
        ("delimitador", 1, MUTED),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    x = 0.0
    for nombre, ancho, color in campos:
        claro = color == SURFACE
        ax.add_patch(Rectangle((x, 1.36), ancho, 0.70, facecolor=color,
                               edgecolor=GRID, lw=0.8))
        # Los campos de un byte no admiten el rótulo dentro, ni horizontal
        # —invade al vecino— ni girado —se sale de la caja—: va arriba con
        # una guía, igual que en el mapa de la Flash.
        estrecho = ancho < 2
        if estrecho:
            ax.annotate(nombre, xy=(x + ancho / 2, 2.08),
                        xytext=(x + ancho / 2, 2.36), ha="center", va="bottom",
                        fontsize=7, color=INK, rotation=38,
                        arrowprops=dict(arrowstyle="-", color=GRID, lw=0.7))
        else:
            ax.text(x + ancho / 2, 1.71, nombre, ha="center", va="center",
                    fontsize=8, color=INK if claro else PAPER)
        ax.text(x + ancho / 2, 1.20, "%d B" % ancho, ha="center", fontsize=7,
                color=MUTED)
        x += ancho

    ax.annotate("", xy=(3, 0.98), xytext=(3 + len(TRAMA_CARGA), 0.98),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.8))
    ax.text(3 + len(TRAMA_CARGA) / 2, 0.78,
            "el campo de comprobación se calcula sobre estos bytes",
            ha="center", fontsize=7.5, color=MUTED)

    ax.text(0, 0.48, "emisor", fontsize=8, color=MUTED)
    ax.text(2.6, 0.48, "%s  →  FCS = 0x%04X" % (TRAMA_CARGA.decode(), fcs_bien),
            fontsize=8.5, color=OK)
    ax.text(0, 0.12, "receptor", fontsize=8, color=MUTED)
    ax.text(2.6, 0.12, "un bit alterado  →  FCS = 0x%04X" % fcs_mal,
            fontsize=8.5, color=ACCENT)
    ax.text(9.6, 0.30, "≠  trama descartada", fontsize=8.5, color=ACCENT)

    ax.set_xlim(-0.4, 13.4)
    ax.set_ylim(0, 3.1)
    ax.axis("off")

    escribir(fig, "paper-trama-crc")


# --------------------------------------------------------------------------
# 24. Sesión 3 — lo que cuesta transmitir en un formato legible
# --------------------------------------------------------------------------
# El artículo sostiene que el formato se paga dos veces, en conversión y en
# bytes transmitidos, pero no publica una tabla de tamaños. Los tamaños de
# aquí son elaboración propia: se codifica EL MISMO registro de cuatro maneras
# y se cuenta. El binario empaquetado usa 4 B de marca temporal, dos enteros
# de 16 bits y un byte de estado.
REGISTRO_LEGIBLE = ('{"marca": 1753699325, "temperatura": 23.4, '
                    '"humedad": 61.2, "estado": "ok"}')
REGISTRO_COMPACTO = '{"marca":1753699325,"temp":23.4,"hum":61.2,"est":"ok"}'
REGISTRO_ABREVIADO = '{"t":1753699325,"c":234,"h":612,"e":1}'
REGISTRO_BINARIO_BYTES = 4 + 2 + 2 + 1


def paper_serializacion_bytes():
    datos = [
        ("legible, con espacios", len(REGISTRO_LEGIBLE), ACCENT),
        ("legible, sin espacios", len(REGISTRO_COMPACTO), WARN),
        ("legible, claves abreviadas", len(REGISTRO_ABREVIADO), NAVY),
        ("binario empaquetado", REGISTRO_BINARIO_BYTES, OK),
    ]

    fig, ax = plt.subplots(figsize=(6.2, 2.4))
    y = np.arange(len(datos))[::-1]
    for pos, (etiqueta, valor, color) in zip(y, datos):
        ax.barh(pos, valor, height=0.44, color=color)
        ax.text(valor + 1.5, pos, "%d B" % valor, va="center", fontsize=8.5,
                color=color)
        ax.text(1.5, pos + 0.40, etiqueta, fontsize=8, color=MUTED)

    mayor = datos[0][1]
    razon = ("%.1f" % (mayor / REGISTRO_BINARIO_BYTES)).replace(".", ",")
    ax.text(mayor, -0.85, "el mismo registro pesa %s× más" % razon,
            ha="right", fontsize=8, color=MUTED)

    ax.set_xlim(0, mayor + 16)
    ax.set_ylim(-1.2, len(datos) - 0.15)
    ax.set_yticks([])
    ax.set_xlabel("bytes que viajan por el enlace")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "paper-serializacion-bytes")


# --------------------------------------------------------------------------
# 25. Sesión 4 — qué hace la calibración con la salida del sensor
# --------------------------------------------------------------------------
# El único dato publicado es la exactitud alcanzada TRAS calibrar: del 96 al
# 99 %. La banda verde es ese dato. La recta sin calibrar se dibuja con una
# ganancia y un desplazamiento declarados aquí, a modo de ilustración de lo
# que la calibración corrige: el artículo no publica el error de partida.
CAL_EXACTITUD_MIN = 0.96
CAL_EXACTITUD_MAX = 0.99
CAL_GANANCIA = 0.88
CAL_DESPLAZAMIENTO = 90.0


def paper_calibracion():
    x = np.linspace(400, 2000, 60)

    fig, ax = plt.subplots(figsize=(7.0, 2.0))
    ax.fill_between(x, x * CAL_EXACTITUD_MIN, x * (2 - CAL_EXACTITUD_MIN),
                    color=OK, alpha=0.10)
    ax.fill_between(x, x * CAL_EXACTITUD_MAX, x * (2 - CAL_EXACTITUD_MAX),
                    color=OK, alpha=0.18)

    ax.plot(x, x, color=MUTED, lw=1, ls="--", label="referencia")
    ax.plot(x, x * CAL_GANANCIA + CAL_DESPLAZAMIENTO, color=ACCENT, lw=2,
            label="sin calibrar (trazo ilustrativo)")
    ax.plot(x, x * 0.985 + 6, color=OK, lw=2,
            label="tras calibrar: 96 – 99 % de exactitud")

    ax.set_xlabel("concentración de referencia (ppm)")
    ax.set_ylabel("lectura del equipo (ppm)")
    ax.set_xlim(400, 2000)
    ax.set_ylim(400, 2000)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-calibracion")


# --------------------------------------------------------------------------
# 26. Sesión 4 — lo que separa 12 bits de 18 bits
# --------------------------------------------------------------------------
# La resolución no se compara en bits sino en el escalón de tensión que cada
# una deja sin resolver. Con el mismo fondo de escala de 3,3 V el cálculo es
# exacto: 3,3 V / 2^n. De ahí que el artículo recurra a un conversor externo.
ADC_FONDO_V = 3.3
ADC_BITS = [12, 16, 18]
ADC_ETIQUETAS = ["12 bits\nintegrado en el SoC", "16 bits", "18 bits\nAD7606C-18"]


def paper_resolucion_adc():
    pasos_uv = [ADC_FONDO_V / (2 ** b) * 1e6 for b in ADC_BITS]
    colores = [ACCENT, WARN, OK]

    fig, ax = plt.subplots(figsize=(7.0, 2.0))
    x = np.arange(len(ADC_BITS))
    ax.bar(x, pasos_uv, width=0.5, color=colores)

    for xi, valor in zip(x, pasos_uv):
        texto = ("%.1f µV" % valor).replace(".", ",")
        ax.text(xi, valor * 1.3, texto, ha="center", fontsize=8.5, color=INK)

    ax.set_yscale("log")
    ax.set_ylabel("escalón mínimo (µV, log.)", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(ADC_ETIQUETAS, fontsize=8)
    ax.set_ylim(5, 4000)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-resolucion-adc")


# --------------------------------------------------------------------------
# 27. Sesión 4 — hasta dónde aguanta el plazo con interrupciones de red
# --------------------------------------------------------------------------
# El artículo no publica una curva: sostiene que la frecuencia de interrupción
# la fija el tráfico externo y que por eso el peor caso no se puede acotar. La
# figura hace ese razonamiento con un modelo de parámetros declarados: una
# tarea periódica de 10 ms que necesita 6 ms de procesador y una rutina de
# interrupción de red de 25 µs. El cruce marca dónde el plazo deja de cumplirse.
IRQ_PERIODO_MS = 10.0
IRQ_TAREA_MS = 6.0
IRQ_COSTO_US = 25.0


def paper_interrupciones_plazo():
    tasa = np.linspace(0, 30000, 400)
    por_periodo_ms = tasa * (IRQ_PERIODO_MS / 1000.0) * (IRQ_COSTO_US / 1000.0)
    disponible = IRQ_PERIODO_MS - por_periodo_ms
    limite = (IRQ_PERIODO_MS - IRQ_TAREA_MS) / (
        (IRQ_PERIODO_MS / 1000.0) * (IRQ_COSTO_US / 1000.0))

    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    ax.plot(tasa, disponible, color=NAVY, lw=2,
            label="procesador que queda para la tarea")
    ax.axhline(IRQ_TAREA_MS, color=ACCENT, lw=1.6, ls="--",
               label="lo que la tarea necesita: 6 ms")
    ax.axvline(limite, color=MUTED, lw=0.9, ls=":")

    ax.fill_between(tasa, 0, disponible, where=disponible < IRQ_TAREA_MS,
                    color=ACCENT, alpha=0.10)
    ax.annotate(("%d int/s" % round(limite)).replace(",", " "),
                (limite, 9.3), fontsize=8, color=MUTED, ha="center")
    ax.annotate("avalancha de paquetes:\nel plazo se pierde", (23500, 2.0),
                fontsize=8, color=ACCENT, ha="center")

    ax.set_xlabel("interrupciones de red por segundo (las fija el tráfico)")
    ax.set_ylabel("ms por periodo de 10 ms")
    ax.set_xlim(0, 30000)
    ax.set_ylim(0, 10.6)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="lower left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-interrupciones-plazo")



# --------------------------------------------------------------------------
# 28. Sesión 5 — por qué la tabla de transiciones se levanta y no se enumera
# --------------------------------------------------------------------------
# Cifras del artículo: 5 biestables de estado y 16 entradas, de donde salen
# 2 097 152 combinaciones. La figura muestra de dónde viene ese número y a qué
# ritmo crece: cada entrada añadida DUPLICA la tabla. La escala es logarítmica
# porque en lineal el punto del artículo aplastaría todo lo demás.
FSM_BIESTABLES = 5
FSM_ENTRADAS = 16


def paper_fsm_combinaciones():
    entradas = np.arange(0, FSM_ENTRADAS + 1)
    combinaciones = (2.0 ** FSM_BIESTABLES) * (2.0 ** entradas)

    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    ax.plot(entradas, combinaciones, color=NAVY, lw=2, marker="o", ms=3)
    ax.scatter([FSM_ENTRADAS], [combinaciones[-1]], s=90, color=ACCENT, zorder=4)

    ax.annotate("2 097 152\ncon las 16 entradas del equipo",
                (FSM_ENTRADAS, combinaciones[-1]), textcoords="offset points",
                xytext=(-10, -30), ha="right", fontsize=8, color=ACCENT)
    ax.annotate("32 estados\ncon 5 biestables", (0, 32),
                textcoords="offset points", xytext=(12, 6), fontsize=8,
                color=NAVY)

    ax.set_yscale("log")
    ax.set_xlabel("entradas consideradas")
    ax.set_ylabel("filas de la tabla (log.)", fontsize=8)
    ax.set_xlim(0, FSM_ENTRADAS)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-fsm-combinaciones")


# --------------------------------------------------------------------------
# 29. Sesión 5 — el umbral de disparo sobre el convertidor de 10 bits
# --------------------------------------------------------------------------
# El artículo fija el disparo de la alarma en 799 de 1023, valor que los
# autores determinan de forma experimental. La figura sitúa ese número sobre
# el recorrido completo del convertidor y muestra en qué se traduce: la
# fracción del rango que queda a cada lado de la decisión.
PN_UMBRAL = 799
PN_MAXIMO = 1023


def paper_umbral_fotorresistencia():
    fig, ax = plt.subplots(figsize=(6.2, 2.2))

    ax.add_patch(Rectangle((0, 0.45), PN_UMBRAL, 0.42, facecolor=OK,
                           alpha=0.75, edgecolor="none"))
    ax.add_patch(Rectangle((PN_UMBRAL, 0.45), PN_MAXIMO - PN_UMBRAL, 0.42,
                           facecolor=ACCENT, edgecolor="none"))

    ax.text(PN_UMBRAL / 2, 0.66, "reposo · sin disparo", ha="center",
            va="center", fontsize=8.5, color=PAPER)
    ax.text((PN_UMBRAL + PN_MAXIMO) / 2, 0.66, "alarma", ha="center",
            va="center", fontsize=8.5, color=PAPER)

    ax.axvline(PN_UMBRAL, color=INK, lw=1.4, ymin=0.28, ymax=0.78)
    ax.annotate("umbral 799, hallado midiendo:\nninguna hoja de datos lo aporta",
                (PN_UMBRAL, 1.02), ha="center", fontsize=8, color=INK)

    ax.annotate("", xy=(0, 0.28), xytext=(PN_UMBRAL, 0.28),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.8))
    ax.annotate("", xy=(PN_UMBRAL, 0.28), xytext=(PN_MAXIMO, 0.28),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.8))
    ax.text(PN_UMBRAL / 2, 0.13, "78,1 % del recorrido", ha="center",
            fontsize=8, color=MUTED)
    ax.text((PN_UMBRAL + PN_MAXIMO) / 2, 0.13, "21,9 %", ha="center",
            fontsize=8, color=MUTED)

    ax.set_xlim(0, PN_MAXIMO)
    ax.set_ylim(0, 1.35)
    ax.set_xticks([0, 256, 512, 768, PN_UMBRAL, PN_MAXIMO])
    ax.set_xticklabels(["0", "256", "512", "768", "799", "1023"], fontsize=8)
    ax.set_xlabel("lectura del convertidor de 10 bits")
    ax.set_yticks([])
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "paper-umbral-fotorresistencia")


# --------------------------------------------------------------------------
# 30. Sesión 6 — dónde queda el costo de sincronizar
# --------------------------------------------------------------------------
# El artículo no publica tiempos absolutos: su resultado es cualitativo y
# tajante —la parte crítica nunca repite una operación, la no crítica sí—. La
# figura lo expresa con un modelo de parámetros declarados: la parte crítica
# necesita 40 µs de trabajo propio y la no crítica ocupa el dato durante lo
# que marca el eje. Con exclusión mutua, la crítica hereda esa espera.
SINC_TRABAJO_US = 40.0


def paper_sincronizacion_costo():
    ocupacion = np.linspace(0, 400, 200)

    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    ax.plot(ocupacion, SINC_TRABAJO_US + ocupacion, color=ACCENT, lw=2,
            label="con exclusión mutua: espera a la parte sin plazo")
    ax.plot(ocupacion, np.full_like(ocupacion, SINC_TRABAJO_US), color=OK,
            lw=2, label="no bloqueante: la parte crítica no repite nunca")

    ax.fill_between(ocupacion, SINC_TRABAJO_US, SINC_TRABAJO_US + ocupacion,
                    color=ACCENT, alpha=0.07)
    ax.annotate("el costo que se traslada\na la parte sin plazo", (300, 190),
                ha="center", fontsize=8, color=MUTED)

    ax.set_xlabel("tiempo que la parte sin plazo retiene el dato (µs)")
    ax.set_ylabel("peor caso de la parte crítica (µs)", fontsize=8)
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 460)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-sincronizacion-costo")


# --------------------------------------------------------------------------
# 31. Sesión 7 — la cabecera frente a la carga útil
# --------------------------------------------------------------------------
# Cifras de la lámina: 2 bytes de cabecera mínima en MQTT frente a unos 192 en
# una petición HTTP típica. Lo que decide no es la cabecera en sí, sino qué
# fracción del envío ocupa: con cargas pequeñas el protocolo pesa más que el
# dato, y esa fracción se calcula exactamente.
CAB_MQTT_B = 2
CAB_HTTP_B = 192


def paper_cabecera_fraccion():
    carga = np.logspace(0, 3.2, 200)
    frac_mqtt = CAB_MQTT_B / (CAB_MQTT_B + carga) * 100
    frac_http = CAB_HTTP_B / (CAB_HTTP_B + carga) * 100

    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    ax.plot(carga, frac_http, color=ACCENT, lw=2)
    ax.plot(carga, frac_mqtt, color=OK, lw=2)
    # El rótulo va sobre la curva: una leyenda en este recuadro se solapa con
    # una de las dos trazas en cualquier esquina donde se coloque.
    ax.text(1.15, 96, "HTTP · 192 B de cabecera", fontsize=8, color=ACCENT)
    ax.text(1.15, 58, "MQTT · 2 B de cabecera", fontsize=8, color=OK)
    ax.axhline(50, color=MUTED, lw=0.9, ls=":")
    ax.text(1400, 52, "mitad del envío es protocolo", fontsize=7.5, color=MUTED,
            ha="right")

    ax.scatter([20], [CAB_HTTP_B / (CAB_HTTP_B + 20) * 100], s=60,
               color=ACCENT, zorder=4)
    ax.annotate("una lectura de 20 B:\n el 90 % del envío es cabecera",
                (20, 90), textcoords="offset points", xytext=(14, -6),
                fontsize=8, color=ACCENT)

    ax.set_xscale("log")
    ax.set_xlabel("carga útil del mensaje (bytes, log.)")
    ax.set_ylabel("% del envío ocupado\npor la cabecera", fontsize=8)
    ax.set_xlim(1, 1500)
    ax.set_ylim(0, 104)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-cabecera-fraccion")


# --------------------------------------------------------------------------
# 32. Sesión 7 — por qué la curva elíptica gasta menos
# --------------------------------------------------------------------------
# El artículo mide corriente, pero no publica la tabla de tamaños de clave. La
# razón de fondo de su resultado sí está tabulada y es pública: para un mismo
# nivel de seguridad, RSA necesita claves que crecen mucho más deprisa. Las
# equivalencias son las de NIST SP 800-57 Parte 1 Rev. 5, Tabla 2.
NIST_NIVEL = [80, 112, 128, 192, 256]
NIST_RSA = [1024, 2048, 3072, 7680, 15360]
NIST_CE = [160, 224, 256, 384, 512]


def paper_clave_equivalente():
    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    x = np.arange(len(NIST_NIVEL))
    ancho = 0.36

    ax.bar(x - ancho / 2, NIST_RSA, ancho, color=ACCENT, label="RSA")
    ax.bar(x + ancho / 2, NIST_CE, ancho, color=OK, label="curva elíptica")

    for xi, r, c in zip(x, NIST_RSA, NIST_CE):
        ax.text(xi - ancho / 2, r * 1.14, str(r), ha="center", fontsize=7.5,
                color=ACCENT)
        ax.text(xi + ancho / 2, c * 1.14, str(c), ha="center", fontsize=7.5,
                color=OK)

    ax.set_yscale("log")
    ax.set_ylabel("bits de clave (log.)", fontsize=8)
    ax.set_xlabel("nivel de seguridad equivalente (bits)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in NIST_NIVEL])
    ax.set_ylim(80, 60000)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=8, ncol=2)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-clave-equivalente")


# --------------------------------------------------------------------------
# 33. Sesión 7 — las dos ventajas medidas no son de la misma talla
# --------------------------------------------------------------------------
# Cifras de la revisión: MQTT responde entre 4,76 y 12,1 veces más rápido, y
# consume entre un 6 y un 8 % menos. Ponerlas juntas es el contenido de la
# figura: la ventaja de latencia es de otro orden que la de consumo, porque en
# ambos protocolos el consumo lo domina la radio.
MQTT_VELOCIDAD = (4.76, 12.1)
MQTT_CONSUMO = (6.0, 8.0)


def paper_mqtt_dos_ventajas():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(6.2, 2.3))

    izq.barh([0], [MQTT_VELOCIDAD[1] - MQTT_VELOCIDAD[0]], left=[MQTT_VELOCIDAD[0]],
             height=0.34, color=OK)
    izq.axvline(1, color=MUTED, lw=1, ls=":")
    izq.text(1.1, 0.30, "HTTP = 1×", fontsize=7.5, color=MUTED)
    izq.text(MQTT_VELOCIDAD[0], -0.34, "4,76×", ha="center", fontsize=8.5, color=OK)
    izq.text(MQTT_VELOCIDAD[1], -0.34, "12,1×", ha="center", fontsize=8.5, color=OK)
    izq.set_xlim(0, 14)
    izq.set_ylim(-0.7, 0.7)
    izq.set_yticks([])
    izq.set_xlabel("veces más rápido que HTTP", fontsize=8)
    izq.grid(axis="x", color=GRID, lw=0.6)
    izq.set_axisbelow(True)
    limpiar_ejes(izq, ocultar=("top", "right", "left"))

    der.barh([0], [MQTT_CONSUMO[1] - MQTT_CONSUMO[0]], left=[MQTT_CONSUMO[0]],
             height=0.34, color=WARN)
    der.text(MQTT_CONSUMO[0], -0.34, "6 %", ha="center", fontsize=8.5, color=WARN)
    der.text(MQTT_CONSUMO[1], -0.34, "8 %", ha="center", fontsize=8.5, color=WARN)
    der.set_xlim(0, 14)
    der.set_ylim(-0.7, 0.7)
    der.set_yticks([])
    der.set_xlabel("% menos de consumo que HTTP", fontsize=8)
    der.grid(axis="x", color=GRID, lw=0.6)
    der.set_axisbelow(True)
    limpiar_ejes(der, ocultar=("top", "right", "left"))

    fig.subplots_adjust(wspace=0.18)
    escribir(fig, "paper-mqtt-dos-ventajas")


# --------------------------------------------------------------------------
# 34. Sesión 8 — lo que ahorra el intermediario
# --------------------------------------------------------------------------
# Los autores atribuyen la extensión de MQTT a la simplicidad de su modelo,
# por delante de cualquier ventaja técnica. Esa simplicidad se cuenta: sin
# intermediario, conectar N emisores con M receptores exige N×M enlaces; con
# intermediario, N+M. Aquí se toma M = N para poder dibujarlo en un eje.
BROKER_N = np.arange(1, 21)


def paper_broker_enlaces():
    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    ax.plot(BROKER_N, BROKER_N * BROKER_N, color=ACCENT, lw=2,
            label="punto a punto: N × M enlaces")
    ax.plot(BROKER_N, BROKER_N * 2, color=OK, lw=2,
            label="con intermediario: N + M enlaces")

    ax.scatter([20], [400], s=60, color=ACCENT, zorder=4)
    ax.annotate("400", (20, 400), textcoords="offset points", xytext=(-8, 4),
                ha="right", fontsize=8.5, color=ACCENT)
    ax.scatter([20], [40], s=60, color=OK, zorder=4)
    ax.annotate("40", (20, 40), textcoords="offset points", xytext=(-8, 6),
                ha="right", fontsize=8.5, color=OK)

    ax.set_xlabel("dispositivos que publican (y otros tantos que reciben)")
    ax.set_ylabel("enlaces a mantener", fontsize=8)
    ax.set_xlim(1, 20)
    ax.set_ylim(0, 420)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-broker-enlaces")


# --------------------------------------------------------------------------
# 35. Sesión 8 — qué se mide cuando se mide el tiempo de servicio
# --------------------------------------------------------------------------
# La magnitud del artículo es el intervalo entre que el intermediario recibe
# un mensaje y lo reenvía, publicando con QoS 1. La figura dibuja esa
# secuencia de protocolo para dejar claro qué tramo se cronometra y cuál no:
# el viaje por la red queda fuera, y por eso la cifra es del intermediario y
# no del enlace.
def paper_tiempo_de_servicio():
    fig, ax = plt.subplots(figsize=(6.4, 2.4))

    carriles = [("emisor", 2.2, NAVY), ("intermediario", 1.3, ACCENT),
                ("receptor", 0.4, OK)]
    for nombre, y, color in carriles:
        ax.plot([0.6, 9.6], [y, y], color=GRID, lw=1)
        ax.text(0.45, y, nombre, ha="right", va="center", fontsize=8.5,
                color=color)

    flechas = [
        (1.2, 2.2, 3.4, 1.3, "PUBLISH", NAVY),
        (5.2, 1.3, 7.4, 0.4, "PUBLISH", ACCENT),
        (7.6, 0.4, 9.4, 1.3, "PUBACK", OK),
    ]
    for x0, y0, x1, y1, texto, color in flechas:
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), color=color,
                                     arrowstyle="-|>", mutation_scale=11, lw=1.3))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.12, texto, ha="center",
                fontsize=7.5, color=color)

    ax.add_patch(Rectangle((3.4, 1.18), 1.8, 0.24, facecolor=ACCENT, alpha=0.18,
                           edgecolor="none"))
    ax.annotate("", xy=(3.4, 0.95), xytext=(5.2, 0.95),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1))
    ax.text(4.3, 0.72, "tiempo de servicio\ndel intermediario", ha="center",
            fontsize=8, color=INK)

    ax.text(9.6, 2.55, "el viaje por la red queda fuera de la medida",
            ha="right", fontsize=7.5, color=MUTED)

    ax.set_xlim(0, 10)
    ax.set_ylim(0.1, 2.8)
    ax.axis("off")

    escribir(fig, "paper-tiempo-de-servicio")


# --------------------------------------------------------------------------
# 36. Sesión 8 — un mensaje grande delante retrasa a los pequeños
# --------------------------------------------------------------------------
# El efecto que describe el artículo tiene nombre y se calcula: en una cola por
# orden de llegada, lo que un mensaje espera es la suma de lo que tarda todo lo
# que va delante. Con el enlace declarado abajo, un mensaje de 500 kB delante
# de nueve de 1 kB multiplica la espera de estos. Ordenar por tamaño lo evita.
COLA_ENLACE_KBPS = 250.0
COLA_GRANDE_KB = 500.0
COLA_PEQUENO_KB = 1.0
COLA_PEQUENOS = 9


def paper_cola_por_tamano():
    def esperas(orden):
        acumulado, salida = 0.0, []
        for tam in orden:
            acumulado += tam / COLA_ENLACE_KBPS
            salida.append(acumulado)
        return salida

    llegada = [COLA_GRANDE_KB] + [COLA_PEQUENO_KB] * COLA_PEQUENOS
    ordenado = [COLA_PEQUENO_KB] * COLA_PEQUENOS + [COLA_GRANDE_KB]

    e_llegada = esperas(llegada)[1:]
    e_ordenado = esperas(ordenado)[:COLA_PEQUENOS]

    fig, ax = plt.subplots(figsize=(6.0, 2.4))
    x = np.arange(1, COLA_PEQUENOS + 1)
    ancho = 0.38
    ax.bar(x - ancho / 2, e_llegada, ancho, color=ACCENT,
           label="por orden de llegada, con el grande delante")
    ax.bar(x + ancho / 2, e_ordenado, ancho, color=OK,
           label="planificando por tamaño")

    ax.annotate("%.1f s" % e_llegada[0], (1 - ancho / 2, e_llegada[0]),
                textcoords="offset points", xytext=(0, 5), ha="center",
                fontsize=8, color=ACCENT)
    # La barra ordenada del primer turno es tan baja que cualquier rótulo
    # pegado a ella cae encima de la barra vecina: sube por encima.
    ax.annotate("%.3f s" % e_ordenado[0], (1 + ancho / 2, e_ordenado[0]),
                textcoords="offset points", xytext=(0, 26), ha="center",
                fontsize=8, color=OK,
                arrowprops=dict(arrowstyle="-", color=OK, lw=0.7))

    # En lineal la serie ordenada es invisible: 4 ms contra 2 s. La escala
    # logarítmica es la única que deja ver las DOS, que es lo que compara.
    ax.set_yscale("log")
    ax.set_xlabel("mensaje pequeño (1 kB) según su turno")
    ax.set_ylabel("espera hasta entregarlo (s, log.)", fontsize=8)
    ax.set_xticks(x)
    ax.set_ylim(0.002, 20)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.24), ncol=2,
                    frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)
    fig.subplots_adjust(top=0.80)

    escribir(fig, "paper-cola-por-tamano")



# --------------------------------------------------------------------------
# 37. Sesión 9 — la incorporación como primera fase de un ciclo, no como paso
# --------------------------------------------------------------------------
# La aportación del artículo es situar la incorporación dentro de un ciclo de
# vida que llega hasta la retirada. La figura dibuja ese ciclo y marca cuánto
# cubre un procedimiento pensado solo para el primer arranque: una fase de seis.
CICLO_FASES = [
    ("fabricación", False),
    ("incorporación", True),
    ("operación", False),
    ("re-incorporación\na otra red", False),
    ("transferencia\nde propiedad", False),
    ("retirada", False),
]


def paper_ciclo_incorporacion():
    fig, ax = plt.subplots(figsize=(8.0, 1.9))

    n = len(CICLO_FASES)
    angulos = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, n, endpoint=False)
    radio = 1.0

    for k, ((nombre, cubierta), ang) in enumerate(zip(CICLO_FASES, angulos)):
        x, y = radio * np.cos(ang) * 1.55, radio * np.sin(ang)
        color = OK if cubierta else MUTED
        ax.add_patch(plt.Circle((x, y), 0.135, transform=ax.transData,
                                facecolor=color, edgecolor="none"))
        ax.text(x, y, str(k + 1), ha="center", va="center", fontsize=8.5,
                color=PAPER)
        fuera = 1.30 if abs(np.cos(ang)) > 0.5 else 1.0
        ax.text(x * fuera + (0.30 if x > 0.1 else -0.30 if x < -0.1 else 0),
                y + (0.30 if y > 0.1 else -0.30 if y < -0.1 else 0),
                nombre, ha="center", va="center", fontsize=8,
                color=INK if cubierta else MUTED)

        sig = angulos[(k + 1) % n]
        x2, y2 = radio * np.cos(sig) * 1.55, radio * np.sin(sig)
        ax.add_patch(FancyArrowPatch((x + (x2 - x) * 0.18, y + (y2 - y) * 0.18),
                                     (x + (x2 - x) * 0.82, y + (y2 - y) * 0.82),
                                     color=GRID, arrowstyle="-|>",
                                     mutation_scale=9, lw=1))

    # El centro solo admite una cifra: la frase que la explica vive en el pie,
    # y escribirla aquí se comía los rótulos de las fases 5 y 6.
    ax.text(0, 0.10, "1 de 6", ha="center", fontsize=13, color=OK)
    ax.text(0, -0.16, "fases cubiertas", ha="center", fontsize=8, color=MUTED)

    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

    escribir(fig, "paper-ciclo-incorporacion")


# --------------------------------------------------------------------------
# 38. Sesión 9 — dónde deja de servir la configuración a mano
# --------------------------------------------------------------------------
# El artículo no publica tiempos: su conclusión es que la provisión a escala
# depende de configuración manual y que ahí está el cuello de botella. La
# figura pone números al argumento con un ritmo declarado —seis minutos por
# equipo, sostenidos— y una jornada de ocho horas como unidad de lectura.
PROV_MINUTOS = 6.0
PROV_JORNADA_H = 8.0


def paper_provision_escala():
    parque = np.array([10, 50, 100, 500, 1000, 5000, 10000])
    jornadas = parque * PROV_MINUTOS / 60.0 / PROV_JORNADA_H

    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    ax.plot(parque, jornadas, color=ACCENT, lw=2, marker="o", ms=4,
            label="a mano: 6 min por equipo")
    ax.plot(parque, np.full_like(jornadas, 0.5), color=OK, lw=2,
            label="automatizada: no depende del tamaño del parque")

    ax.annotate("125 jornadas", (10000, jornadas[-1]),
                textcoords="offset points", xytext=(-6, 4), ha="right",
                fontsize=8.5, color=ACCENT)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("equipos del parque (log.)")
    ax.set_ylabel("jornadas de 8 h (log.)", fontsize=8)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-provision-escala")


# --------------------------------------------------------------------------
# 39. Sesión 9 — lo que se puede juzgar antes de comprar, y lo que no
# --------------------------------------------------------------------------
# El resultado del estudio es direccional —la etiqueta cambia la elección— y no
# se dibuja como si tuviera cifras que no publica. Lo que sí es exacto es el
# mecanismo: la seguridad es el único atributo no observable en el momento de
# comprar, y una etiqueta es lo que lo traslada al lado observable.
ATRIBUTOS_VISIBLES = ["precio", "funcionalidad", "aspecto", "marca"]
ATRIBUTOS_OCULTOS = ["actualizaciones", "cifrado", "datos que envía",
                     "vida de soporte"]


def paper_etiqueta_observable():
    fig, ax = plt.subplots(figsize=(6.2, 2.5))

    ax.add_patch(Rectangle((0.05, 0.12), 0.38, 0.76, facecolor=OK, alpha=0.10,
                           edgecolor=OK, lw=1))
    ax.add_patch(Rectangle((0.57, 0.12), 0.38, 0.76, facecolor=ACCENT,
                           alpha=0.08, edgecolor=ACCENT, lw=1, ls="--"))

    ax.text(0.24, 0.93, "se juzga antes de comprar", ha="center", fontsize=8.5,
            color=OK)
    ax.text(0.76, 0.93, "no se juzga antes de comprar", ha="center",
            fontsize=8.5, color=ACCENT)

    for k, nombre in enumerate(ATRIBUTOS_VISIBLES):
        ax.text(0.24, 0.74 - k * 0.155, nombre, ha="center", fontsize=8.5,
                color=INK)
    for k, nombre in enumerate(ATRIBUTOS_OCULTOS):
        ax.text(0.76, 0.74 - k * 0.155, nombre, ha="center", fontsize=8.5,
                color=MUTED)

    ax.add_patch(FancyArrowPatch((0.575, 0.50), (0.435, 0.50), color=NAVY,
                                 arrowstyle="-|>", mutation_scale=13, lw=1.6))
    ax.text(0.505, 0.56, "la etiqueta", ha="center", fontsize=8, color=NAVY)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.axis("off")

    escribir(fig, "paper-etiqueta-observable")


# --------------------------------------------------------------------------
# 40. Sesión 10 — auditar el binario deja fuera cinco sextas partes del ciclo
# --------------------------------------------------------------------------
# La conclusión del artículo es de alcance: una estrategia eficaz cubre el
# ciclo entero y no solo el código. La figura enumera las seis etapas que los
# autores recorren y marca la única que cubre auditar el binario.
CICLO_FIRMWARE = ["componentes\nde software", "almacenamiento", "configuración",
                  "entrega", "mantenimiento", "actualización"]


def paper_ciclo_firmware():
    fig, ax = plt.subplots(figsize=(6.4, 1.9))

    ancho, hueco = 1.5, 0.22
    for k, nombre in enumerate(CICLO_FIRMWARE):
        x = k * (ancho + hueco)
        cubierta = k == 0
        ax.add_patch(Rectangle((x, 0.45), ancho, 0.5,
                               facecolor=OK if cubierta else SURFACE,
                               edgecolor=GRID, lw=0.8))
        ax.text(x + ancho / 2, 0.70, nombre, ha="center", va="center",
                fontsize=7.5, color=PAPER if cubierta else INK)
        if k:
            ax.add_patch(FancyArrowPatch((x - hueco, 0.70), (x - 0.02, 0.70),
                                         color=GRID, arrowstyle="-|>",
                                         mutation_scale=8, lw=1))

    ancho_total = len(CICLO_FIRMWARE) * (ancho + hueco) - hueco
    ax.annotate("", xy=(0, 0.30), xytext=(ancho, 0.30),
                arrowprops=dict(arrowstyle="<->", color=OK, lw=1.1))
    ax.text(ancho / 2, 0.14, "auditar el binario", ha="center", fontsize=8,
            color=OK)
    ax.annotate("", xy=(ancho + hueco, 0.30), xytext=(ancho_total, 0.30),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.1))
    ax.text((ancho + hueco + ancho_total) / 2, 0.14,
            "lo que queda abierto si la auditoría se detiene ahí",
            ha="center", fontsize=8, color=ACCENT)

    ax.set_xlim(-0.2, ancho_total + 0.2)
    ax.set_ylim(0, 1.05)
    ax.axis("off")

    escribir(fig, "paper-ciclo-firmware")


# --------------------------------------------------------------------------
# 41. Sesión 10 — lo que un modelo medio no ve del consumo
# --------------------------------------------------------------------------
# Los autores concluyen que solo la medida directa capta el comportamiento del
# sistema completo, con los picos que un modelo sencillo no representa. La
# figura construye un ciclo de trabajo con las corrientes que la propia sesión
# maneja —sueño profundo, proceso y radio— y superpone el valor medio: la
# misma media puede corresponder a picos muy distintos.
CONSUMO_SUENO_MA = 0.010
CONSUMO_PROCESO_MA = 40.0
CONSUMO_RADIO_MA = 240.0


def paper_medicion_consumo():
    t = np.linspace(0, 10, 2000)
    corriente = np.full_like(t, CONSUMO_SUENO_MA)
    corriente[(t > 3.0) & (t < 3.9)] = CONSUMO_PROCESO_MA
    corriente[(t > 3.9) & (t < 4.4)] = CONSUMO_RADIO_MA
    corriente[(t > 7.5) & (t < 7.8)] = CONSUMO_PROCESO_MA
    media = corriente.mean()

    fig, ax = plt.subplots(figsize=(7.4, 2.0))
    ax.plot(t, corriente, color=NAVY, lw=1.4, label="medida directa")
    ax.axhline(media, color=ACCENT, lw=1.6, ls="--",
               label="valor medio: %.1f mA" % media)

    ax.annotate("pico de radio\n%d mA" % CONSUMO_RADIO_MA, (4.15, CONSUMO_RADIO_MA),
                textcoords="offset points", xytext=(14, -4), fontsize=8,
                color=NAVY)
    ax.annotate("sueño profundo\n%s mA" % ("%.3f" % CONSUMO_SUENO_MA).replace(".", ","),
                (1.2, CONSUMO_SUENO_MA), textcoords="offset points",
                xytext=(0, 16), fontsize=8, color=MUTED)

    ax.set_yscale("symlog", linthresh=0.05)
    ax.set_xlabel("tiempo (s)")
    ax.set_ylabel("corriente (mA, log.)", fontsize=8)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 600)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t_ in leg.get_texts():
        t_.set_color(MUTED)

    escribir(fig, "paper-medicion-consumo")


# --------------------------------------------------------------------------
# 42. Sesión 10 — el tiempo de una actualización por banda estrecha
# --------------------------------------------------------------------------
# Cifras del artículo: 178 s para 2 kB y 4338 s para 1000 kB, con relación
# lineal. La recta se traza entre esos dos puntos publicados y se anota lo que
# significa el extremo: setenta y dos minutos con el equipo actualizándose.
OTA_PUNTOS = [(2, 178), (1000, 4338)]


def paper_ota_tiempo():
    (x0, y0), (x1, y1) = OTA_PUNTOS
    pendiente = (y1 - y0) / (x1 - x0)
    tam = np.linspace(0, 1000, 200)
    tiempo = y0 + pendiente * (tam - x0)

    fig, ax = plt.subplots(figsize=(7.4, 2.0))
    ax.plot(tam, tiempo / 60.0, color=NAVY, lw=2,
            label="%.2f s por kB, medido" % pendiente)
    for x, y in OTA_PUNTOS:
        ax.scatter([x], [y / 60.0], s=70, color=ACCENT, zorder=4)

    ax.annotate("2 kB · 178 s", (2, 178 / 60.0), textcoords="offset points",
                xytext=(10, 8), fontsize=8, color=ACCENT)
    ax.annotate("1000 kB · 4338 s\n= 72 min", (1000, 4338 / 60.0),
                textcoords="offset points", xytext=(-8, -6), ha="right",
                fontsize=8, color=ACCENT)

    ax.set_xlabel("tamaño del firmware (kB)")
    ax.set_ylabel("duración de la actualización (min)", fontsize=8)
    ax.set_xlim(0, 1030)
    ax.set_ylim(0, 80)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-ota-tiempo")


# --------------------------------------------------------------------------
# 43. Sesión 11 — cuántos artefactos hay que producir y mantener
# --------------------------------------------------------------------------
# El resultado del artículo es que la máquina virtual desacopla el programa de
# la arquitectura. Eso se cuenta: compilando, cada lenguaje se cruza con cada
# arquitectura y salen L×A binarios; con la máquina virtual, L módulos más A
# runtimes, es decir L+A. La figura toma tres lenguajes para poder dibujarlo.
VM_LENGUAJES = 3


def paper_vm_artefactos():
    arqs = np.arange(1, 9)

    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    ax.plot(arqs, VM_LENGUAJES * arqs, color=ACCENT, lw=2, marker="o", ms=4,
            label="compilando: %d lenguajes × N arquitecturas" % VM_LENGUAJES)
    ax.plot(arqs, VM_LENGUAJES + arqs, color=OK, lw=2, marker="o", ms=4,
            label="máquina virtual: %d módulos + N runtimes" % VM_LENGUAJES)

    ax.annotate("24", (8, 24), textcoords="offset points", xytext=(-6, 4),
                ha="right", fontsize=8.5, color=ACCENT)
    ax.annotate("11", (8, 11), textcoords="offset points", xytext=(-6, 6),
                ha="right", fontsize=8.5, color=OK)

    ax.set_xlabel("arquitecturas de destino")
    ax.set_ylabel("artefactos a construir y mantener", fontsize=8)
    ax.set_xlim(1, 8)
    ax.set_ylim(0, 26)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-vm-artefactos")


# --------------------------------------------------------------------------
# 44. Sesión 11 — qué alcanza el módulo y qué no
# --------------------------------------------------------------------------
# La propiedad que el artículo destaca es el aislamiento: el módulo solo llega
# a lo que el anfitrión le concede de forma explícita. La figura contrapone esa
# superficie con la de un guion interpretado sin restricción, que alcanza todo
# lo que alcance el intérprete.
def paper_aislamiento_modulo():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(6.2, 2.5))

    recursos = ["memoria del\nfirmware", "red", "sistema de\narchivos",
                "GPIO", "claves"]

    for ax, titulo, permitido, color in (
        (izq, "guion interpretado sin restricción", [1, 1, 1, 1, 1], ACCENT),
        (der, "módulo aislado: solo lo concedido", [0, 1, 0, 1, 0], OK),
    ):
        ax.add_patch(Rectangle((0.06, 0.10), 0.30, 0.66, facecolor=color,
                               alpha=0.12, edgecolor=color, lw=1.2))
        ax.text(0.21, 0.43, "código\nque se\ncarga", ha="center", va="center",
                fontsize=8, color=color)
        ax.text(0.5, 0.90, titulo, ha="center", fontsize=8.5, color=color)

        for k, (nombre, ok) in enumerate(zip(recursos, permitido)):
            y = 0.72 - k * 0.145
            ax.text(0.98, y, nombre, ha="right", va="center", fontsize=7.5,
                    color=INK if ok else MUTED)
            if ok:
                ax.add_patch(FancyArrowPatch((0.37, 0.43), (0.55, y),
                                             color=color, arrowstyle="-|>",
                                             mutation_scale=8, lw=1))
            else:
                ax.text(0.47, 0.43 + (y - 0.43) * 0.42, "✕", ha="center",
                        va="center", fontsize=9, color=MUTED)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

    fig.subplots_adjust(wspace=0.10)
    escribir(fig, "paper-aislamiento-modulo")


# --------------------------------------------------------------------------
# 45. Sesión 11 — válido no es lo mismo que correcto
# --------------------------------------------------------------------------
# Cifras del artículo: de 164 problemas, las tres herramientas producen 150,
# 148 y 153 generaciones válidas. La figura muestra esa proporción alta y
# semejante, y deja marcado que la validez solo cubre una de las cinco
# dimensiones evaluadas: las otras cuatro no se comprueban ejecutando.
GEN_PROBLEMAS = 164
GEN_VALIDAS = [("herramienta A", 150), ("herramienta B", 148),
               ("herramienta C", 153)]


def paper_codigo_generado():
    fig, ax = plt.subplots(figsize=(6.0, 2.4))

    x = np.arange(len(GEN_VALIDAS))
    valores = [v for _, v in GEN_VALIDAS]
    ax.bar(x, valores, width=0.45, color=NAVY)
    ax.axhline(GEN_PROBLEMAS, color=MUTED, lw=1, ls=":")
    ax.text(len(GEN_VALIDAS) - 0.5, GEN_PROBLEMAS + 3,
            "164 problemas planteados", ha="right", fontsize=7.5, color=MUTED)

    for xi, valor in zip(x, valores):
        pct = ("%.1f %%" % (valor / GEN_PROBLEMAS * 100)).replace(".", ",")
        ax.text(xi, valor + 4, "%d  ·  %s" % (valor, pct), ha="center",
                fontsize=8.5, color=NAVY)

    ax.set_xticks(x)
    ax.set_xticklabels([n for n, _ in GEN_VALIDAS], fontsize=8.5)
    ax.set_ylabel("generaciones válidas", fontsize=8)
    ax.set_ylim(0, 190)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-codigo-generado")


# --------------------------------------------------------------------------
# 46. Sesión 12 — cuándo el modelo deja de caber
# --------------------------------------------------------------------------
# La cifra del artículo es la reducción de 32 a 8 bits por parámetro. Lo que
# esa cifra decide se ve al cruzarla con la memoria del módulo del curso: 320 kB
# de DRAM, de los que una parte ya la ocupan la pila de red y el programa. El
# cruce de cada recta con el presupuesto es el número de parámetros que caben.
CUANT_PRESUPUESTO_KB = 180.0
CUANT_BITS = [(32, "coma flotante · 32 bits", ACCENT),
              (16, "coma fija · 16 bits", WARN),
              (8, "coma fija · 8 bits", OK)]


def paper_cuantizacion_memoria():
    parametros = np.linspace(0, 250000, 300)

    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    for bits, etiqueta, color in CUANT_BITS:
        ax.plot(parametros, parametros * bits / 8 / 1024, color=color, lw=2,
                label=etiqueta)

    ax.axhline(CUANT_PRESUPUESTO_KB, color=INK, lw=1.2, ls="--")
    # Rótulo corto y pegado al eje: cualquier texto largo a esta altura lo
    # cruza alguna de las tres rectas. La frase completa va en el pie.
    ax.text(248000, CUANT_PRESUPUESTO_KB + 14, "presupuesto · 180 kB",
            ha="right", fontsize=7.5, color=INK)

    for bits, _, color in CUANT_BITS:
        cabe = CUANT_PRESUPUESTO_KB * 1024 * 8 / bits
        ax.scatter([cabe], [CUANT_PRESUPUESTO_KB], s=55, color=color, zorder=4)
        ax.annotate("%d k" % round(cabe / 1000), (cabe, CUANT_PRESUPUESTO_KB),
                    textcoords="offset points", xytext=(2, -14), fontsize=8,
                    color=color)

    ax.set_xlabel("parámetros del modelo")
    ax.set_ylabel("memoria que ocupan (kB)", fontsize=8)
    ax.set_xlim(0, 250000)
    ax.set_ylim(0, 320)
    ax.set_xticks([0, 50000, 100000, 150000, 200000, 250000])
    ax.set_xticklabels(["0", "50 k", "100 k", "150 k", "200 k", "250 k"])
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "paper-cuantizacion-memoria")


# --------------------------------------------------------------------------
# 47. Sesión 12 — por qué las cifras publicadas no se pueden comparar
# --------------------------------------------------------------------------
# El obstáculo que identifica el artículo es que cada fabricante trae su propia
# cadena cerrada. La figura lo dibuja como una rejilla: solo las casillas de la
# diagonal existen, de modo que dos cifras cualesquiera nunca comparten a la vez
# modelo y plataforma. El intérprete común es la fila que llena la rejilla.
COMP_PLATAFORMAS = ["fabricante A", "fabricante B", "fabricante C"]
COMP_CADENAS = ["cadena A", "cadena B", "cadena C", "intérprete\ncomún"]


def paper_comparabilidad():
    fig, ax = plt.subplots(figsize=(5.6, 2.6))

    for fila, cadena in enumerate(COMP_CADENAS):
        for col, _ in enumerate(COMP_PLATAFORMAS):
            comun = fila == len(COMP_CADENAS) - 1
            existe = comun or fila == col
            color = OK if comun else (NAVY if existe else SURFACE)
            ax.add_patch(Rectangle((col + 0.08, -fila + 0.08), 0.84, 0.84,
                                   facecolor=color if existe else SURFACE,
                                   edgecolor=GRID, lw=0.8))
            if existe:
                ax.text(col + 0.5, -fila + 0.5, "✓", ha="center", va="center",
                        fontsize=10, color=PAPER)

    for col, nombre in enumerate(COMP_PLATAFORMAS):
        ax.text(col + 0.5, 1.15, nombre, ha="center", fontsize=8, color=MUTED)
    for fila, nombre in enumerate(COMP_CADENAS):
        color = OK if fila == len(COMP_CADENAS) - 1 else MUTED
        ax.text(-0.12, -fila + 0.5, nombre, ha="right", va="center",
                fontsize=8, color=color)

    ax.text(1.5, -len(COMP_CADENAS) + 0.55,
            "sin casillas compartidas no hay dos cifras comparables",
            ha="center", fontsize=8, color=MUTED)

    ax.set_xlim(-1.5, 3.2)
    ax.set_ylim(-len(COMP_CADENAS) + 0.15, 1.5)
    ax.axis("off")

    escribir(fig, "paper-comparabilidad")


# --------------------------------------------------------------------------
# 48. Sesión 12 — vigilancia continua frente a vigilancia con enlace
# --------------------------------------------------------------------------
# El argumento del artículo es que la inferencia local hace viable la vigilancia
# donde la conectividad no puede garantizarse. La figura lo cuenta sobre una
# jornada con los cortes de enlace declarados: con el análisis en el servidor,
# lo vigilado es solo lo que el enlace deja pasar.
CORTES = [(2.0, 3.4), (7.1, 9.6), (13.0, 13.8), (17.4, 20.2)]
JORNADA_H = 24.0


def paper_vigilancia_continua():
    fig, ax = plt.subplots(figsize=(6.2, 2.2))

    ax.add_patch(Rectangle((0, 1.28), JORNADA_H, 0.34, facecolor=OK,
                           edgecolor="none"))
    ax.text(JORNADA_H / 2, 1.45, "inferencia en el propio equipo",
            ha="center", va="center", fontsize=8.5, color=PAPER)

    ax.add_patch(Rectangle((0, 0.62), JORNADA_H, 0.34, facecolor=OK,
                           alpha=0.30, edgecolor="none"))
    perdido = 0.0
    for inicio, fin in CORTES:
        ax.add_patch(Rectangle((inicio, 0.62), fin - inicio, 0.34,
                               facecolor=ACCENT, edgecolor="none"))
        perdido += fin - inicio
    ax.text(JORNADA_H / 2, 0.79, "análisis en el servidor", ha="center",
            va="center", fontsize=8.5, color=INK)

    ax.text(-0.4, 1.45, "24 h", ha="right", va="center", fontsize=8, color=MUTED)
    cubierto = (JORNADA_H - perdido) / JORNADA_H * 100
    ax.text(-0.4, 0.79, ("%.0f %%" % cubierto), ha="right", va="center",
            fontsize=8, color=ACCENT)

    ax.text(JORNADA_H, 0.34, "en rojo, las horas sin enlace: %.1f h de las 24"
            % perdido, ha="right", fontsize=8, color=ACCENT)

    ax.set_xlim(-3.2, JORNADA_H + 0.3)
    ax.set_ylim(0.15, 1.85)
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.set_xticklabels(["00:00", "06:00", "12:00", "18:00", "24:00"], fontsize=8)
    ax.set_yticks([])
    ax.tick_params(axis="x", colors=MUTED)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    escribir(fig, "paper-vigilancia-continua")



# --------------------------------------------------------------------------
# 49. Sesión 11 — lo que ESP-Claw exige frente a lo que trae el módulo
# --------------------------------------------------------------------------
# Cifras de la documentación del proyecto: "ESP-Claw requires at least 8MB
# Flash and 8MB PSRAM". El módulo de estas sesiones trae 4 MB de Flash y no
# lleva PSRAM. La figura pone las dos columnas juntas porque la conclusión no
# es una opinión sobre el marco de trabajo: es una resta.
CLAW_REQUIERE = (8, 8)
CLAW_MODULO = (4, 0)


def esp_claw_requisitos():
    fig, ax = plt.subplots(figsize=(5.2, 2.5))

    x = np.arange(2)
    ancho = 0.34
    ax.bar(x - ancho / 2, CLAW_REQUIERE, ancho, color=NAVY,
           label="lo que pide ESP-Claw")
    ax.bar(x + ancho / 2, CLAW_MODULO, ancho, color=ACCENT,
           label="ESP32-WROOM-32 del curso")

    for xi, (pide, hay) in enumerate(zip(CLAW_REQUIERE, CLAW_MODULO)):
        ax.text(xi - ancho / 2, pide + 0.25, "%d MB" % pide, ha="center",
                fontsize=8.5, color=NAVY)
        ax.text(xi + ancho / 2, hay + 0.25,
                "%d MB" % hay if hay else "no lleva", ha="center",
                fontsize=8.5, color=ACCENT)

    ax.set_xticks(x)
    ax.set_xticklabels(["Flash", "PSRAM"], fontsize=9)
    ax.set_ylabel("memoria (MB)", fontsize=8)
    ax.set_ylim(0, 10.5)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2,
                    frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)
    fig.subplots_adjust(top=0.83)

    escribir(fig, "esp-claw-requisitos")



# --------------------------------------------------------------------------
# 50. Sesión 10 — la fuga y la fragmentación no se parecen en la gráfica
# --------------------------------------------------------------------------
# Los puntos son los de la traza que la propia lámina imprime: a las 0, 6, 24
# y 31 horas. Puestos en una gráfica se ve de un vistazo lo que en la traza
# hay que deducir leyendo columnas: la memoria libre no se movió y el mayor
# bloque contiguo se desplomó, hasta caer por debajo de los 40 kB que la capa
# de cifrado necesita de una pieza.
FRAG_HORAS = [0, 6, 24, 31]
FRAG_LIBRE_KB = [195, 194, 193, 193]
FRAG_MAYOR_KB = [182, 96, 41, 38]
FRAG_EXIGE_KB = 40


def memoria_fragmentacion():
    fig, ax = plt.subplots(figsize=(6.0, 2.5))

    ax.plot(FRAG_HORAS, FRAG_LIBRE_KB, color=NAVY, lw=2, marker="o", ms=4,
            label="memoria libre total")
    ax.plot(FRAG_HORAS, FRAG_MAYOR_KB, color=ACCENT, lw=2, marker="o", ms=4,
            label="mayor bloque contiguo")
    ax.axhline(FRAG_EXIGE_KB, color=WARN, lw=1.4, ls="--",
               label="lo que pide la conexión cifrada: 40 kB de una pieza")

    ax.fill_between([0, 31], 0, FRAG_EXIGE_KB, color=ACCENT, alpha=0.06)
    ax.annotate("aquí falla el cifrado,\nno la reserva de memoria", (31, 22),
                ha="right", fontsize=8, color=ACCENT)

    ax.set_xlabel("horas desde el arranque")
    ax.set_ylabel("kB", fontsize=8)
    ax.set_xlim(0, 31)
    ax.set_ylim(0, 215)
    ax.set_xticks(FRAG_HORAS)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="center left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "memoria-fragmentacion")


# --------------------------------------------------------------------------
# 51. Sesión 10 — el reparto de la Flash, a escala
# --------------------------------------------------------------------------
# Los tamaños son los de la tabla de la lámina. Dibujarlos a escala enseña de
# golpe lo que la tabla dice en palabras: las dos particiones de aplicación
# son iguales y juntas se llevan dos tercios de la Flash, que es el precio de
# poder actualizar en remoto.
PARTICIONES = [
    ("nvs", 20 / 1024, NAVY),
    ("otadata", 8 / 1024, MUTED),
    ("app0", 1.3, ACCENT),
    ("app1", 1.3, WARN),
    ("spiffs", 1.4, OK),
]
FLASH_MB = 4.0


def tabla_particiones():
    fig, ax = plt.subplots(figsize=(6.4, 2.0))

    x = 0.0
    for nombre, tam, color in PARTICIONES:
        ax.add_patch(Rectangle((x, 0.52), tam, 0.40, facecolor=color,
                               edgecolor=PAPER, lw=1.2))
        if tam > 0.5:
            ax.text(x + tam / 2, 0.72, nombre, ha="center", va="center",
                    fontsize=9, color=PAPER)
            ax.text(x + tam / 2, 0.42, "%s MB" % ("%.1f" % tam).replace(".", ","),
                    ha="center", fontsize=8, color=color)
        x += tam

    ax.annotate("nvs + otadata\n28 kB", (0.014, 0.98), ha="left", fontsize=7.5,
                color=MUTED)
    ax.plot([0.028, 0.10], [0.94, 0.94], color=GRID, lw=0.8)

    ax.annotate("", xy=(20 / 1024 + 8 / 1024, 0.28), xytext=(2.63, 0.28),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1))
    ax.text(1.33, 0.12, "dos aplicaciones del mismo tamaño: el precio de la "
            "actualización remota", ha="center", fontsize=8, color=INK)

    ax.set_xlim(-0.05, FLASH_MB + 0.05)
    ax.set_ylim(0.05, 1.12)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels(["0", "1 MB", "2 MB", "3 MB", "4 MB"], fontsize=8)
    ax.set_yticks([])
    ax.tick_params(axis="x", colors=MUTED)
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)

    escribir(fig, "tabla-particiones")


# --------------------------------------------------------------------------
# 52. Sesión 2 — el factor cuatro no se nota hasta que se multiplica
# --------------------------------------------------------------------------
# Las dos cifras de la lámina —1,0 kB frente a 3,9 kB con mil muestras— son un
# punto de estas rectas. La figura las extiende para que se vea dónde deja de
# ser una discusión de estilo: cuando el arreglo se acerca a la SRAM del
# módulo, elegir el tipo por el rango real del dato pasa a decidir si cabe.
SRAM_KB = 520.0


def tipos_memoria_arreglo():
    muestras = np.linspace(0, 200000, 300)

    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    ax.plot(muestras, muestras * 4 / 1024, color=ACCENT, lw=2,
            label="arreglo de int · 4 bytes")
    ax.plot(muestras, muestras / 1024, color=OK, lw=2,
            label="arreglo de uint8_t · 1 byte")
    ax.axhline(SRAM_KB, color=INK, lw=1.2, ls="--")
    ax.text(198000, SRAM_KB + 18, "SRAM del módulo: 520 kB", ha="right",
            fontsize=7.5, color=INK)

    for n, color in ((1000, MUTED),):
        ax.scatter([n, n], [n * 4 / 1024, n / 1024], s=40, color=color, zorder=4)
    ax.annotate("mil muestras: 3,9 kB frente a 1,0 kB\n—la diferencia que la "
                "lámina discute—", (1000, 40), fontsize=8, color=MUTED)

    ax.set_xlabel("muestras almacenadas")
    ax.set_ylabel("memoria del arreglo (kB)", fontsize=8)
    ax.set_xlim(0, 200000)
    ax.set_ylim(0, 800)
    ax.set_xticks([0, 50000, 100000, 150000, 200000])
    ax.set_xticklabels(["0", "50 k", "100 k", "150 k", "200 k"])
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "tipos-memoria-arreglo")


# --------------------------------------------------------------------------
# 53. Sesión 8 — lo que cuesta preguntar
# --------------------------------------------------------------------------
# La cifra de la lámina —8640 conexiones diarias preguntando cada 10 s— es un
# punto de la curva 86 400 / periodo. La figura la dibuja entera para que se
# vea la forma del problema: acortar el periodo dispara las conexiones, y
# alargarlo retrasa el aviso. La conexión mantenida sale de esa disyuntiva.
SEGUNDOS_DIA = 86400


def costo_de_preguntar():
    periodo = np.logspace(0, np.log10(600), 200)
    conexiones = SEGUNDOS_DIA / periodo

    fig, ax = plt.subplots(figsize=(5.8, 2.5))
    ax.plot(periodo, conexiones, color=ACCENT, lw=2,
            label="HTTP: una conexión por consulta")
    ax.plot(periodo, np.ones_like(periodo), color=OK, lw=2,
            label="conexión mantenida: una al día")

    ax.scatter([10], [SEGUNDOS_DIA / 10], s=60, color=ACCENT, zorder=4)
    ax.annotate("cada 10 s → 8640 al día", (10, SEGUNDOS_DIA / 10),
                textcoords="offset points", xytext=(10, 4), fontsize=8,
                color=ACCENT)
    ax.annotate("alargar el periodo abarata,\npero retrasa el aviso", (420, 260),
                ha="right", fontsize=8, color=MUTED)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("periodo de consulta (s, log.)")
    ax.set_ylabel("conexiones al día (log.)", fontsize=8)
    ax.set_xlim(1, 600)
    ax.set_ylim(0.7, 200000)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    leg = ax.legend(loc="lower left", frameon=False, fontsize=7.5)
    for t in leg.get_texts():
        t.set_color(MUTED)

    escribir(fig, "costo-de-preguntar")


# --------------------------------------------------------------------------
# 54. Sesión 12 — el detector que acierta el 95 % y no sirve
# --------------------------------------------------------------------------
# El caso que plantea la lámina, con las cuentas hechas: mil ventanas, la
# anomalía ocurre el 5 % del tiempo y el detector responde siempre «normal».
# La matriz de confusión enseña por qué la exactitud engaña: la columna de
# anomalía está vacía, y ninguna cifra global lo dice.
EVAL_VENTANAS = 1000
EVAL_PREVALENCIA = 0.05


def metricas_matriz_confusion():
    anomalias = int(EVAL_VENTANAS * EVAL_PREVALENCIA)
    normales = EVAL_VENTANAS - anomalias
    celdas = [[normales, 0], [anomalias, 0]]
    exactitud = normales / EVAL_VENTANAS * 100

    fig, ax = plt.subplots(figsize=(5.6, 2.5))

    for fila in range(2):
        for col in range(2):
            valor = celdas[fila][col]
            acierto = fila == col
            color = OK if (acierto and valor) else (ACCENT if valor else SURFACE)
            ax.add_patch(Rectangle((col, -fila), 1, 1, facecolor=color,
                                   edgecolor=PAPER, lw=2))
            ax.text(col + 0.5, -fila + 0.58, str(valor), ha="center",
                    va="center", fontsize=13,
                    color=PAPER if valor else MUTED)
            etiquetas = [["correcto", "falso positivo"],
                         ["falso negativo", "correcto"]]
            ax.text(col + 0.5, -fila + 0.28, etiquetas[fila][col], ha="center",
                    va="center", fontsize=7.5,
                    color=PAPER if valor else MUTED)

    ax.text(0.5, 1.12, "predice normal", ha="center", fontsize=8.5, color=MUTED)
    ax.text(1.5, 1.12, "predice anomalía", ha="center", fontsize=8.5, color=MUTED)
    ax.text(-0.08, 0.5, "es normal", ha="right", va="center", fontsize=8.5,
            color=MUTED)
    ax.text(-0.08, -0.5, "es anomalía", ha="right", va="center", fontsize=8.5,
            color=MUTED)

    ax.text(2.25, 0.62, "exactitud", fontsize=8.5, color=MUTED)
    ax.text(2.25, 0.30, "%.0f %%" % exactitud, fontsize=15, color=OK)
    ax.text(2.25, -0.28, "anomalías detectadas", fontsize=8.5, color=MUTED)
    ax.text(2.25, -0.62, "0 de %d" % anomalias, fontsize=15, color=ACCENT)

    ax.set_xlim(-1.15, 3.9)
    ax.set_ylim(-1.15, 1.35)
    ax.axis("off")

    escribir(fig, "metricas-matriz-confusion")



# --------------------------------------------------------------------------
# 55. Sesión 1 — qué trae resuelto cada nivel de integración
# --------------------------------------------------------------------------
# Los elementos son los que enumera la propia lámina al describir los tres
# niveles. Puestos en rejilla, la implicación de producto deja de ser una
# frase y pasa a ser una cuenta: nueve elementos a tu cargo con el chip
# desnudo, tres con el módulo, ninguno con la placa de desarrollo.
INTEGRACION_NIVELES = ["chip", "módulo", "placa de\ndesarrollo"]
INTEGRACION_ELEMENTOS = [
    ("oscilador", [0, 1, 1]),
    ("memoria\nFlash", [0, 1, 1]),
    ("adaptación\nde antena", [0, 1, 1]),
    ("blindaje\nelectromag.", [0, 1, 1]),
    ("certificación\nde emisiones", [0, 1, 1]),
    ("regulación\nde tensión", [0, 0, 1]),
    ("conversor\nUSB-serie", [0, 0, 1]),
    ("reinicio\nautomático", [0, 0, 1]),
    ("conectores", [0, 0, 1]),
]


def niveles_integracion():
    cols = len(INTEGRACION_ELEMENTOS)
    fig, ax = plt.subplots(figsize=(11.8, 2.05))

    # Transpuesta: los elementos van en columnas y los niveles en filas. En
    # vertical la rejilla salía más alta que ancha y, escalada al ancho de la
    # lámina, no cabía por altura.
    for c, (nombre, trae) in enumerate(INTEGRACION_ELEMENTOS):
        ax.text(c + 0.5, 3.14, nombre, ha="center", va="bottom", fontsize=7,
                color=INK, linespacing=1.35)
        for f, incluido in enumerate(trae):
            y = 2 - f
            ax.add_patch(Rectangle((c + 0.06, y + 0.08), 0.88, 0.84,
                                   facecolor=OK if incluido else SURFACE,
                                   edgecolor=GRID, lw=0.7))
            if not incluido:
                ax.text(c + 0.5, y + 0.5, "a tu\ncargo", ha="center",
                        va="center", fontsize=6.5, color=MUTED)

    for f, nivel in enumerate(INTEGRACION_NIVELES):
        ax.text(-0.14, 2 - f + 0.5, nivel.replace("\n", " "), ha="right",
                va="center", fontsize=9, color=NAVY)

    pendientes = [sum(1 for _, t in INTEGRACION_ELEMENTOS if not t[f])
                  for f in range(3)]
    for f, n in enumerate(pendientes):
        ax.text(cols + 0.32, 2 - f + 0.5, str(n), ha="center", va="center",
                fontsize=13, color=ACCENT if n else OK)
    ax.text(cols + 0.32, 3.12, "a tu\ncargo", ha="center", va="bottom",
            fontsize=7.5, color=MUTED)

    ax.set_xlim(-2.6, cols + 0.9)
    ax.set_ylim(-0.15, 4.05)
    ax.axis("off")

    escribir(fig, "niveles-integracion")


# --------------------------------------------------------------------------
# 56. Sesión 1 — qué parámetro alcanza cada entorno
# --------------------------------------------------------------------------
# Los parámetros son los que nombra la lámina. La figura enseña la relación
# real: el núcleo de Arduino cubre un subconjunto, y lo que no cubre se invoca
# desde el mismo archivo, sin cambiar de proyecto. De ahí que los autores del
# curso los traten como capas y no como alternativas.
ENTORNO_PARAMETROS = [
    ("nivel\nde salida", 1),
    ("lectura\ndel ADC", 1),
    ("frecuencia\ndel PWM", 1),
    ("resolución\ndel PWM", 1),
    ("prioridad\nde tarea", 0),
    ("afinidad\nde núcleo", 0),
    ("tamaño\nde pila", 0),
]


def arduino_frente_a_espidf():
    cols = len(ENTORNO_PARAMETROS)
    fig, ax = plt.subplots(figsize=(10.4, 2.2))

    for c, (nombre, en_arduino) in enumerate(ENTORNO_PARAMETROS):
        ax.text(c + 0.5, 2.14, nombre, ha="center", va="bottom", fontsize=7.5,
                color=INK, linespacing=1.35)
        ax.add_patch(Rectangle((c + 0.06, 1.08), 0.88, 0.84,
                               facecolor=NAVY if en_arduino else SURFACE,
                               edgecolor=GRID, lw=0.7))
        ax.add_patch(Rectangle((c + 0.06, 0.08), 0.88, 0.84, facecolor=OK,
                               edgecolor=GRID, lw=0.7))
        if not en_arduino:
            ax.add_patch(FancyArrowPatch((c + 0.5, 1.02), (c + 0.5, 0.99),
                                         color=ACCENT, arrowstyle="-|>",
                                         mutation_scale=9, lw=1.2))

    ax.text(-0.14, 1.5, "núcleo de Arduino", ha="right", va="center",
            fontsize=9, color=NAVY)
    ax.text(-0.14, 0.5, "ESP-IDF", ha="right", va="center", fontsize=9,
            color=OK)
    ax.set_xlim(-3.1, cols + 0.2)
    ax.set_ylim(-0.18, 3.0)
    ax.axis("off")

    escribir(fig, "arduino-frente-a-espidf")



# --------------------------------------------------------------------------
# 57. Sesión 1 — el error del conversor no depende del ritmo de muestreo
# --------------------------------------------------------------------------
# Los autores repiten la comparación para cuatro periodos de muestreo —200,
# 100, 50 y 10 ms— y comunican que la banda de error del conversor integrado
# no muestra dependencia apreciable del periodo. La figura pone esa constancia
# delante: muestrear más despacio no compra exactitud, que es la conclusión
# práctica y la que contradice la intuición.
ADC_PERIODOS_MS = [200, 100, 50, 10]
ADC_BANDA_INTEGRADO_MV = 10.0
ADC_BANDA_EXTERNO_MV = 2.0


def paper_adc_periodos():
    fig, ax = plt.subplots(figsize=(7.0, 2.0))
    x = np.arange(len(ADC_PERIODOS_MS))

    ax.fill_between([-0.5, len(x) - 0.5], -ADC_BANDA_INTEGRADO_MV,
                    ADC_BANDA_INTEGRADO_MV, color=ACCENT, alpha=0.13)
    ax.fill_between([-0.5, len(x) - 0.5], -ADC_BANDA_EXTERNO_MV,
                    ADC_BANDA_EXTERNO_MV, color=OK, alpha=0.22)

    for xi in x:
        ax.errorbar(xi - 0.11, 0, yerr=ADC_BANDA_INTEGRADO_MV, color=ACCENT,
                    capsize=5, lw=2)
        ax.errorbar(xi + 0.11, 0, yerr=ADC_BANDA_EXTERNO_MV, color=OK,
                    capsize=5, lw=2)

    ax.text(len(x) - 0.6, ADC_BANDA_INTEGRADO_MV - 1.6, "integrado: ±10 mV",
            ha="right", fontsize=8, color=ACCENT)
    ax.text(len(x) - 0.6, ADC_BANDA_EXTERNO_MV + 0.7, "ADS1115: ±2 mV",
            ha="right", fontsize=8, color=OK)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{p} ms" for p in ADC_PERIODOS_MS])
    ax.set_xlabel("periodo de muestreo ensayado")
    ax.set_ylabel("error de medida (mV)", fontsize=8)
    ax.set_xlim(-0.5, len(x) - 0.5)
    ax.set_ylim(-13, 13)
    ax.axhline(0, color=GRID, lw=0.8)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-adc-periodos")


# --------------------------------------------------------------------------
# 58. Sesión 1 — qué cambia al ejecutar el firmware sin la placa
# --------------------------------------------------------------------------
# El artículo declara una sustitución obligada: el emulador no dispone de
# radio, así que la aplicación se recompila contra una interfaz Ethernet
# emulada. La figura enfrenta las dos ejecuciones para que se vea qué se
# conserva —el binario y su juego de instrucciones— y qué no.
EMU_PIEZAS = [
    ("aplicación", 1, 1),
    ("juego de instrucciones Xtensa", 1, 1),
    ("gestor de arranque", 1, 1),
    ("tabla de particiones", 1, 1),
    ("interfaz 802.11", 1, 0),
    ("interfaz Ethernet emulada", 0, 1),
]


def paper_emulacion_sustitucion():
    filas = len(EMU_PIEZAS)
    fig, ax = plt.subplots(figsize=(6.8, 2.2))

    for f, (nombre, real, emu) in enumerate(EMU_PIEZAS):
        y = filas - f - 1
        ax.text(-0.1, y + 0.5, nombre, ha="right", va="center", fontsize=8,
                color=INK)
        for c, hay in enumerate((real, emu)):
            ax.add_patch(Rectangle((c + 0.06, y + 0.1), 0.88, 0.8,
                                   facecolor=(NAVY if c == 0 else OK) if hay else SURFACE,
                                   edgecolor=GRID, lw=0.7))
            if not hay:
                ax.text(c + 0.5, y + 0.5, "no", ha="center", va="center",
                        fontsize=7.5, color=MUTED)

    ax.text(0.5, filas + 0.22, "placa", ha="center", va="bottom",
            fontsize=9, color=NAVY)
    ax.text(1.5, filas + 0.22, "emulador", ha="center", va="bottom",
            fontsize=9, color=OK)
    ax.text(1.0, -0.55, "una sola sustitución, y obliga a recompilar",
            ha="center", fontsize=8, color=ACCENT)

    ax.set_xlim(-2.9, 2.1)
    ax.set_ylim(-0.85, filas + 0.85)
    ax.axis("off")

    escribir(fig, "paper-emulacion-sustitucion")


# --------------------------------------------------------------------------
# 59. Sesión 1 — de qué depende que el código generado sirva
# --------------------------------------------------------------------------
# Dos cifras publicadas que apuntan a la misma causa. A la izquierda, la tasa
# de referencias a librerías inexistentes, que los autores señalan como fallo
# dominante. A la derecha, lo que mejora el acierto cuando se le da al modelo
# el esquema del circuito y se le devuelven los errores del compilador.
LLM_INEXISTENTES = [("modelos\nabiertos", 21.7, ACCENT), ("modelos\ncerrados", 5.2, WARN)]
LLM_CONTEXTO = [("una sola\npasada", 53.1), ("con esquema y\nrealimentación", 65.1)]


def paper_llm_causas():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.2, 2.3))

    x = np.arange(len(LLM_INEXISTENTES))
    izq.bar(x, [v for _, v, _ in LLM_INEXISTENTES], width=0.5,
            color=[c for _, _, c in LLM_INEXISTENTES])
    for xi, (_, v, c) in zip(x, LLM_INEXISTENTES):
        izq.text(xi, v + 0.8, ("%.1f %%" % v).replace(".", ","), ha="center",
                 fontsize=8.5, color=c)
    izq.set_xticks(x)
    izq.set_xticklabels([n for n, _, _ in LLM_INEXISTENTES], fontsize=8)
    izq.set_ylabel("referencias a librerías\ninexistentes", fontsize=8)
    izq.set_ylim(0, 27)
    izq.grid(axis="y", color=GRID, lw=0.6)
    izq.set_axisbelow(True)
    limpiar_ejes(izq)

    x2 = np.arange(len(LLM_CONTEXTO))
    der.bar(x2, [v for _, v in LLM_CONTEXTO], width=0.5, color=[MUTED, OK])
    for xi, (_, v) in zip(x2, LLM_CONTEXTO):
        der.text(xi, v + 1.5, ("%.1f %%" % v).replace(".", ","), ha="center",
                 fontsize=8.5, color=INK)
    der.annotate("", xy=(1, 63), xytext=(0, 55),
                 arrowprops=dict(arrowstyle="-|>", color=OK, lw=1.4))
    der.text(0.5, 44, "+12 puntos", ha="center", fontsize=8, color=OK)
    der.set_xticks(x2)
    der.set_xticklabels([n for n, _ in LLM_CONTEXTO], fontsize=8)
    der.set_ylabel("acierto del mejor modelo", fontsize=8)
    der.set_ylim(0, 80)
    der.grid(axis="y", color=GRID, lw=0.6)
    der.set_axisbelow(True)
    limpiar_ejes(der)

    fig.subplots_adjust(wspace=0.42)
    escribir(fig, "paper-llm-causas")



# --------------------------------------------------------------------------
# 60. Sesión 2 — dónde vive el acceso al hardware en cada arquitectura
# --------------------------------------------------------------------------
# El artículo propone tres capas. La figura dibuja dónde queda el código que
# toca el hardware en cada una de las dos formas de organizar el mismo
# programa: repartido por todas partes, o confinado en una sola capa.
CAPAS_NOMBRES = ["aplicación", "servicios", "acceso al hardware"]


def paper_capas_tres():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.0, 2.1))

    for ax, titulo, tocan, color in (
        (izq, "monolítico", [1, 1, 1], ACCENT),
        (der, "por capas", [0, 0, 1], OK),
    ):
        ax.text(0.5, 3.35, titulo, ha="center", fontsize=9, color=color)
        for k, nombre in enumerate(CAPAS_NOMBRES):
            y = 2 - k
            marcada = tocan[k]
            ax.add_patch(Rectangle((0.04, y + 0.08), 0.92, 0.84,
                                   facecolor=color if marcada else SURFACE,
                                   alpha=1.0 if marcada else 1.0,
                                   edgecolor=GRID, lw=0.8))
            ax.text(0.5, y + 0.5, nombre, ha="center", va="center", fontsize=8,
                    color=PAPER if marcada else INK)
        ax.text(0.5, -0.45, "en rojo, el código que toca el hardware"
                if color is ACCENT else "solo una capa lo toca",
                ha="center", fontsize=7.5, color=color)
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.8, 3.7)
        ax.axis("off")

    fig.subplots_adjust(wspace=0.12)
    escribir(fig, "paper-capas-tres")


# --------------------------------------------------------------------------
# 61. Sesión 2 — la brecha entre lo compilado y lo interpretado
# --------------------------------------------------------------------------
# Solo hay dos cifras publicadas para la FFT de 1024 muestras: 1821 µs en
# C/C++ y 844 855 µs en MicroPython. De Rust y TinyGo el artículo dice que
# quedan «a pocos microsegundos» de C/C++, sin dar el valor: por eso aquí son
# una banda y no una barra — dibujarles una altura concreta sería inventarla.
FFT_C_US = 1821
FFT_MICROPYTHON_US = 844855


def paper_lenguajes_brecha():
    fig, ax = plt.subplots(figsize=(6.8, 2.1))

    ax.bar([0], [FFT_C_US], width=0.5, color=NAVY)
    ax.bar([1], [FFT_MICROPYTHON_US], width=0.5, color=ACCENT)
    ax.axhspan(FFT_C_US * 0.75, FFT_C_US * 1.35, color=OK, alpha=0.16)
    ax.text(1.62, FFT_C_US * 1.05, "Rust y TinyGo, a pocos µs\nde C/C++ según el artículo",
            ha="right", va="bottom", fontsize=7.5, color=OK)

    ax.text(0, FFT_C_US * 1.7, "1 821 µs", ha="center", fontsize=8.5, color=NAVY)
    ax.text(1, FFT_MICROPYTHON_US * 1.5, "844 855 µs", ha="center", fontsize=8.5,
            color=ACCENT)
    ax.annotate("", xy=(1, 200000), xytext=(0, 200000),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1))
    ax.text(0.5, 240000, "≈464×", ha="center", fontsize=11, color=ACCENT)

    ax.set_yscale("log")
    ax.set_ylabel("FFT de 1024 muestras (µs, log.)", fontsize=8)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["C/C++", "MicroPython"], fontsize=9)
    ax.set_xlim(-0.6, 1.7)
    ax.set_ylim(400, 6e6)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-lenguajes-brecha")


# --------------------------------------------------------------------------
# 62. Sesión 2 — lo que arrastra de media un proyecto publicado
# --------------------------------------------------------------------------
# Las cifras absolutas del artículo dicen poco sin el tamaño de la muestra.
# Divididas entre los 258 proyectos analizados, dan la magnitud que importa a
# quien va a reutilizar uno: cuántos defectos trae de serie.
DEF_PROYECTOS = 258
DEF_TOTAL = 709
DEF_VULNERABILIDADES = 535
DEF_CONFIRMADOS = 376


def paper_defectos_por_proyecto():
    datos = [
        ("defectos localizados", DEF_TOTAL / DEF_PROYECTOS, NAVY),
        ("que son vulnerabilidades", DEF_VULNERABILIDADES / DEF_PROYECTOS, WARN),
        ("confirmados por su autor", DEF_CONFIRMADOS / DEF_PROYECTOS, ACCENT),
    ]
    fig, ax = plt.subplots(figsize=(5.8, 2.1))
    y = np.arange(len(datos))[::-1]
    for pos, (etq, v, c) in zip(y, datos):
        ax.barh(pos, v, height=0.5, color=c)
        ax.text(v + 0.05, pos, ("%.2f" % v).replace(".", ","), va="center",
                fontsize=9, color=c)
        ax.text(0.06, pos + 0.42, etq, fontsize=8, color=MUTED)

    ax.text(3.05, -0.85, "por cada proyecto de los %d analizados" % DEF_PROYECTOS,
            ha="right", fontsize=8, color=MUTED)
    ax.set_xlim(0, 3.2)
    ax.set_ylim(-1.15, len(datos) - 0.15)
    ax.set_yticks([])
    ax.set_xlabel("defectos por proyecto")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "paper-defectos-por-proyecto")



# --------------------------------------------------------------------------
# 63. Sesión 3 — detectar no es corregir
# --------------------------------------------------------------------------
# El artículo insiste en que el código de comprobación es un mecanismo de
# DETECCIÓN. La figura separa las dos cosas que se confunden: lo que el
# receptor sabe al comparar el campo y lo que hace falta para recuperar el
# dato, que ya no está en la trama recibida.
CRC_PASOS = [
    ("el emisor calcula el campo sobre la carga", True),
    ("el receptor lo recalcula y compara", True),
    ("sabe si la trama llegó alterada", True),
    ("sabe qué bit cambió", False),
    ("puede reconstruir el dato original", False),
    ("por eso hay que pedir la retransmisión", True),
]


def paper_crc_detectar():
    filas = len(CRC_PASOS)
    fig, ax = plt.subplots(figsize=(7.0, 2.1))

    for k, (texto, si) in enumerate(CRC_PASOS):
        y = filas - k - 1
        color = OK if si else ACCENT
        ax.text(0.06, y + 0.5, "✓" if si else "✕", fontsize=10, color=color,
                ha="center", va="center")
        ax.text(0.16, y + 0.5, texto, fontsize=8.5, va="center",
                color=INK if si else MUTED)

    ax.annotate("", xy=(0.03, 2.9), xytext=(0.03, 5.9),
                arrowprops=dict(arrowstyle="-", color=OK, lw=2.5))
    ax.annotate("", xy=(0.03, 0.9), xytext=(0.03, 2.9),
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=2.5))
    ax.text(-0.005, 4.4, "detecta", rotation=90, ha="right", va="center",
            fontsize=8, color=OK)
    ax.text(-0.005, 1.9, "no corrige", rotation=90, ha="right", va="center",
            fontsize=8, color=ACCENT)

    ax.set_xlim(-0.06, 1.0)
    ax.set_ylim(-0.2, filas + 0.1)
    ax.axis("off")

    escribir(fig, "paper-crc-detectar")


# --------------------------------------------------------------------------
# 64. Sesión 3 — el formato se paga dos veces
# --------------------------------------------------------------------------
# La tesis del artículo es que el formato tiene dos costos y que ambos salen
# de la batería: el tiempo de conversión dentro del nodo y los bytes que hay
# que emitir por radio. Los tiempos no están publicados, así que la figura
# solo ordena los dos conceptos y su efecto común, sin cifras inventadas.
def paper_serializacion_dos_costos():
    fig, ax = plt.subplots(figsize=(7.0, 2.0))

    cajas = [
        (0.02, "convertir en el nodo", "ciclos de procesador", NAVY),
        (0.37, "transmitir por radio", "bytes al aire", WARN),
    ]
    for x, titulo, detalle, color in cajas:
        ax.add_patch(Rectangle((x, 0.55), 0.29, 0.38, facecolor=color,
                               alpha=0.14, edgecolor=color, lw=1.4))
        ax.text(x + 0.145, 0.80, titulo, ha="center", fontsize=8.5, color=color)
        ax.text(x + 0.145, 0.65, detalle, ha="center", fontsize=7.5, color=MUTED)
        ax.add_patch(FancyArrowPatch((x + 0.145, 0.52), (0.55, 0.34),
                                     color=color, arrowstyle="-|>",
                                     mutation_scale=10, lw=1.2))

    ax.add_patch(Rectangle((0.40, 0.06), 0.30, 0.26, facecolor=ACCENT,
                           alpha=0.14, edgecolor=ACCENT, lw=1.4))
    ax.text(0.55, 0.19, "vida útil del nodo", ha="center", va="center",
            fontsize=9, color=ACCENT)

    ax.text(0.98, 0.80, "la legibilidad se paga\nen los dos", ha="right",
            fontsize=8, color=MUTED)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    escribir(fig, "paper-serializacion-dos-costos")


# --------------------------------------------------------------------------
# 65. Sesión 3 — el intervalo por debajo del cual el enlace no aguanta
# --------------------------------------------------------------------------
# Cifra publicada: 111 ms es el intervalo mínimo sostenible en su montaje. La
# figura sitúa ese umbral frente a los tres intervalos ensayados, para que se
# vea que dos de los tres caen por debajo y por eso degradan la recepción.
UART_INTERVALOS_MS = [1000, 100, 10]
UART_MINIMO_MS = 111


def paper_uart_intervalo_minimo():
    fig, ax = plt.subplots(figsize=(7.0, 2.0))

    x = np.arange(len(UART_INTERVALOS_MS))
    colores = [OK if v >= UART_MINIMO_MS else ACCENT for v in UART_INTERVALOS_MS]
    ax.bar(x, UART_INTERVALOS_MS, width=0.45, color=colores)
    ax.axhline(UART_MINIMO_MS, color=INK, lw=1.3, ls="--")
    ax.text(len(x) - 0.55, UART_MINIMO_MS * 1.35,
            "mínimo sostenible: 111 ms", ha="right", fontsize=8, color=INK)

    for xi, v, c in zip(x, UART_INTERVALOS_MS, colores):
        ax.text(xi, v * 1.35, f"{v} ms", ha="center", fontsize=8.5, color=c)
        if v < UART_MINIMO_MS:
            ax.text(xi, v * 0.45, "no\naguanta", ha="center", va="center",
                    fontsize=7.5, color=PAPER)

    ax.set_yscale("log")
    ax.set_ylabel("intervalo entre envíos\n(ms, log.)", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(["1 s", "100 ms", "10 ms"], fontsize=9)
    ax.set_ylim(4, 4000)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)

    escribir(fig, "paper-uart-intervalo-minimo")


# --------------------------------------------------------------------------
# 66. Sesión 4 — qué se compra con la calibración y a qué precio
# --------------------------------------------------------------------------
# Las dos cifras publicadas son la exactitud tras calibrar —96 a 99 %— y el
# costo del equipo, unas 155 £. Juntas dan el argumento del artículo: la
# calibración es lo que convierte un montaje barato en un instrumento, y no
# encarece el equipo, solo exige el procedimiento.
CAL_EXACTITUD_BANDA = (96, 99)
CAL_COSTO_GBP = 155


def paper_calibracion_valor():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.2, 2.0),
                                   gridspec_kw={"width_ratios": [1.35, 1]})

    izq.barh([0], [CAL_EXACTITUD_BANDA[1] - CAL_EXACTITUD_BANDA[0]],
             left=[CAL_EXACTITUD_BANDA[0]], height=0.3, color=OK)
    izq.axvspan(60, CAL_EXACTITUD_BANDA[0], color=MUTED, alpha=0.10)
    izq.text(CAL_EXACTITUD_BANDA[0], -0.32, "96 %", ha="center", fontsize=8.5,
             color=OK)
    izq.text(CAL_EXACTITUD_BANDA[1], -0.32, "99 %", ha="center", fontsize=8.5,
             color=OK)
    izq.text(78, 0.34, "sin calibrar: el fabricante no la garantiza",
             ha="center", fontsize=7.5, color=MUTED)
    izq.set_xlim(60, 101)
    izq.set_ylim(-0.7, 0.7)
    izq.set_yticks([])
    izq.set_xlabel("exactitud tras calibrar (%)", fontsize=8)
    izq.grid(axis="x", color=GRID, lw=0.6)
    izq.set_axisbelow(True)
    limpiar_ejes(izq, ocultar=("top", "right", "left"))

    der.bar([0], [CAL_COSTO_GBP], width=0.42, color=NAVY)
    der.text(0, CAL_COSTO_GBP + 12, f"≈{CAL_COSTO_GBP} £", ha="center",
             fontsize=9, color=NAVY)
    der.text(0, CAL_COSTO_GBP * 0.45, "equipo\ncompleto", ha="center",
             va="center", fontsize=8, color=PAPER)
    der.set_xlim(-0.6, 0.6)
    der.set_ylim(0, 240)
    der.set_xticks([])
    der.set_ylabel("costo del montaje (£)", fontsize=8)
    der.grid(axis="y", color=GRID, lw=0.6)
    der.set_axisbelow(True)
    limpiar_ejes(der)

    fig.subplots_adjust(wspace=0.32)
    escribir(fig, "paper-calibracion-valor")


# --------------------------------------------------------------------------
# 67. Sesión 4 — por qué la sincronización se hace por cable
# --------------------------------------------------------------------------
# El artículo declara que el reloj de muestreo se comparte conectando
# físicamente las placas, no por software. La figura contrapone las dos
# formas: con relojes independientes cada placa muestrea en su instante y la
# comparación entre canales deja de ser válida.
def paper_reloj_comun():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.2, 2.0))

    t = np.linspace(0, 4, 400)
    for ax, titulo, desfase, color in ((izq, "relojes independientes", 0.22, ACCENT),
                                       (der, "reloj de muestreo común", 0.0, OK)):
        ax.text(0.5, 1.24, titulo, transform=ax.transAxes, ha="center",
                fontsize=9, color=color)
        for k, (fila, d) in enumerate(((1.0, 0.0), (0.0, desfase))):
            for m in np.arange(0, 4.01, 1.0):
                ax.plot([m + d, m + d], [fila, fila + 0.55], color=color, lw=1.6)
            ax.text(-0.25, fila + 0.27, f"placa {k + 1}", ha="right",
                    va="center", fontsize=8, color=MUTED)
        if desfase:
            ax.annotate("", xy=(2 + desfase, -0.3), xytext=(2, -0.3),
                        arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1))
            ax.text(2 + desfase / 2, -0.62, "desfase que\nnadie mide",
                    ha="center", fontsize=7.5, color=ACCENT)
        else:
            ax.text(2, -0.5, "mismo instante en las dos", ha="center",
                    fontsize=7.5, color=OK)
        ax.set_xlim(-1.3, 4.6)
        ax.set_ylim(-1.0, 1.9)
        ax.axis("off")

    fig.subplots_adjust(wspace=0.18)
    escribir(fig, "paper-reloj-comun")


# --------------------------------------------------------------------------
# 68. Sesión 4 — por qué el peor caso no se puede acotar
# --------------------------------------------------------------------------
# La conclusión del artículo es de método: el análisis del peor caso necesita
# el tiempo de ejecución de cada parte, y el del controlador de radio no está
# disponible. La figura enumera las piezas del cálculo y marca la única que
# falta, que basta para invalidar el resultado.
# Rótulos cortos y en dos líneas: los nombres completos no caben dentro de
# cajas que representan una fracción del tiempo, y se solapaban entre sí.
WCET_PIEZAS = [
    ("tarea de\naplicación", True),
    ("rutinas\npropias", True),
    ("pila de\nprotocolos", True),
    ("controlador\nde red", False),
]


def paper_peor_caso_incompleto():
    fig, ax = plt.subplots(figsize=(7.0, 1.9))

    x = 0.0
    anchos = [0.21, 0.19, 0.22, 0.25]
    for (nombre, medible), w in zip(WCET_PIEZAS, anchos):
        color = NAVY if medible else ACCENT
        ax.add_patch(Rectangle((x, 0.45), w, 0.34,
                               facecolor=color if medible else PAPER,
                               alpha=1.0 if medible else 1.0,
                               edgecolor=color, lw=1.4,
                               hatch=None if medible else "///"))
        ax.text(x + w / 2, 0.62, nombre, ha="center", va="center", fontsize=7.5,
                linespacing=1.3, color=PAPER if medible else ACCENT)
        x += w

    ax.annotate("", xy=(0, 0.34), xytext=(0.62, 0.34),
                arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.1))
    ax.text(0.31, 0.19, "se puede medir", ha="center", fontsize=8, color=NAVY)
    ax.annotate("", xy=(0.62, 0.34), xytext=(0.87, 0.34),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.1))
    ax.text(0.745, 0.19, "no se publica", ha="center", fontsize=8, color=ACCENT)
    ax.text(0.435, 0.92, "peor caso = suma de todas las piezas",
            ha="center", fontsize=8.5, color=INK)
    ax.text(0.435, 0.03, "falta una y la cota deja de ser una cota",
            ha="center", fontsize=8, color=ACCENT)

    ax.set_xlim(-0.02, 0.9)
    ax.set_ylim(0, 1.05)
    ax.axis("off")

    escribir(fig, "paper-peor-caso-incompleto")



# --------------------------------------------------------------------------
# 69. Sesión 5 — el código reservado de la alarma y lo que obliga a declarar
# --------------------------------------------------------------------------
# El artículo codifica el estado en cinco biestables y asigna 11111 a la
# alarma, dejando de 10001 a 11110 como no alcanzables. La figura recorre los
# 32 códigos posibles y los reparte en los tres grupos que el diseño declara:
# lo que se usa, lo que se reserva y lo que se descarta de forma explícita.
FSM_BITS = 5
FSM_UTILIZADOS = 17  # 00000 a 10000
FSM_ALARMA = 1  # 11111


def paper_fsm_codigos():
    total = 2 ** FSM_BITS
    no_alcanzables = total - FSM_UTILIZADOS - FSM_ALARMA

    fig, ax = plt.subplots(figsize=(7.0, 2.0))
    grupos = [
        ("etapas del tratamiento", FSM_UTILIZADOS, OK),
        ("no alcanzables, declarados", no_alcanzables, MUTED),
        ("alarma (11111)", FSM_ALARMA, ACCENT),
    ]
    x = 0
    for nombre, n, color in grupos:
        ax.add_patch(Rectangle((x, 0.45), n, 0.4, facecolor=color, alpha=0.85,
                               edgecolor=PAPER, lw=1.2))
        ax.text(x + n / 2, 0.65, str(n), ha="center", va="center", fontsize=9,
                color=PAPER)
        ax.annotate(nombre, xy=(x + n / 2, 0.42), xytext=(x + n / 2, 0.14),
                    ha="center", va="top", fontsize=7.5, color=color,
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.7))
        x += n

    ax.text(total / 2, 1.02, f"{FSM_BITS} biestables = {total} códigos posibles",
            ha="center", fontsize=8.5, color=INK)
    ax.set_xlim(-0.6, total + 0.6)
    ax.set_ylim(-0.35, 1.25)
    ax.axis("off")

    escribir(fig, "paper-fsm-codigos")


# --------------------------------------------------------------------------
# 70. Sesión 5 — dónde vive la lógica y qué se paga por ello
# --------------------------------------------------------------------------
# El artículo compara dos arquitecturas: con la lógica en el ordenador el
# modelo se cambia sin recompilar, pero el equipo deja de ser autónomo. La
# figura enfrenta las dos propiedades para que el compromiso quede a la vista.
PN_ARQUITECTURAS = [
    ("lógica en el ordenador", [("cambiar sin recompilar", True),
                                ("funciona sin el ordenador", False)]),
    ("lógica en el microcontrolador", [("cambiar sin recompilar", False),
                                       ("funciona sin el ordenador", True)]),
]


def paper_pn_arquitecturas():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.0, 2.0))
    for ax, (titulo, filas) in zip((izq, der), PN_ARQUITECTURAS):
        ax.text(0.5, 0.92, titulo, ha="center", fontsize=8.5, color=NAVY)
        for k, (texto, si) in enumerate(filas):
            y = 0.58 - k * 0.28
            color = OK if si else ACCENT
            ax.text(0.08, y, "✓" if si else "✕", fontsize=11, color=color)
            ax.text(0.2, y, texto, fontsize=8.5, va="center", color=INK)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
    fig.subplots_adjust(wspace=0.05)
    escribir(fig, "paper-pn-arquitecturas")


# --------------------------------------------------------------------------
# 71. Sesión 5 — el tiempo que separa lo inviable de lo resuelto
# --------------------------------------------------------------------------
# La figura que ya existe cuenta cuántos modelos resolvió cada análisis. Esta
# cuenta lo otro que publican: el análisis compositivo terminó todos en menos
# de 30 minutos, mientras el plano se interrumpía al llegar al plazo de 4 h
# sin dar resultado. El plazo no es un tiempo de cálculo: es una rendición.
STATE_PLAZO_H = 4.0
STATE_COMPOSITIVO_H = 0.5
STATE_ERROR = 1e-3


def paper_statecharts_tiempo():
    fig, ax = plt.subplots(figsize=(7.0, 1.9))

    ax.barh([1], [STATE_PLAZO_H], height=0.42, color=ACCENT, alpha=0.35,
            hatch="///", edgecolor=ACCENT)
    ax.barh([0], [STATE_COMPOSITIVO_H], height=0.42, color=OK)

    ax.text(STATE_PLAZO_H + 0.08, 1, "se interrumpe sin resultado", va="center",
            fontsize=8.5, color=ACCENT)
    ax.text(STATE_COMPOSITIVO_H + 0.08, 0, "termina: menos de 30 min",
            va="center", fontsize=8.5, color=OK)
    ax.text(STATE_PLAZO_H, 1.42, "plazo máximo: 4 h", ha="center", fontsize=8,
            color=MUTED)

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["compositivo", "plano"], fontsize=9)
    ax.set_xlabel("tiempo de análisis por modelo (h)")
    ax.set_xlim(0, 6.6)
    ax.set_ylim(-0.55, 1.75)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right"))

    escribir(fig, "paper-statecharts-tiempo")


# --------------------------------------------------------------------------
# 72. Sesión 6 — el planificador cumple el periodo, la sincronización no
# --------------------------------------------------------------------------
# Las tres cifras del artículo pertenecen a dos asuntos distintos que conviene
# no confundir. El planificador es fiable: una tarea de 10 ms sale a 9,996 ms.
# Lo que se desborda es la sincronización entre núcleos: 190,3 ms, cuatro
# órdenes de magnitud por encima de la del mismo núcleo.
FREERTOS_PERIODO_OBJ_MS = 10.0
FREERTOS_PERIODO_MED_MS = 9.996
FREERTOS_PERIODO_MIN_MS = 9.632
FREERTOS_MISMO_MS = 0.012
FREERTOS_ENTRE_MS = 190.3


def paper_freertos_dos_asuntos():
    fig, (izq, der) = plt.subplots(1, 2, figsize=(7.2, 2.0),
                                   gridspec_kw={"width_ratios": [1, 1.1]})

    izq.axhline(FREERTOS_PERIODO_OBJ_MS, color=MUTED, lw=1, ls=":")
    izq.bar([0], [FREERTOS_PERIODO_MED_MS], width=0.4, color=OK)
    izq.errorbar([0], [FREERTOS_PERIODO_MED_MS],
                 yerr=[[FREERTOS_PERIODO_MED_MS - FREERTOS_PERIODO_MIN_MS], [0.0]],
                 color=INK, capsize=6, lw=1.2)
    izq.text(0, 10.55, "9,996 ms de 10", ha="center", fontsize=8.5, color=OK)
    izq.text(0.32, FREERTOS_PERIODO_MIN_MS, "mín. 9,632", fontsize=7.5,
             color=MUTED, va="center")
    izq.set_xlim(-0.6, 0.9)
    izq.set_ylim(9.4, 10.9)
    izq.set_xticks([])
    izq.set_ylabel("periodo de la tarea (ms)", fontsize=8)
    izq.set_title("el planificador cumple", fontsize=8.5, color=OK, pad=6)
    izq.grid(axis="y", color=GRID, lw=0.6)
    izq.set_axisbelow(True)
    limpiar_ejes(izq)

    x = np.arange(2)
    der.bar(x, [FREERTOS_MISMO_MS, FREERTOS_ENTRE_MS], width=0.45,
            color=[OK, ACCENT])
    for xi, v, c in zip(x, (FREERTOS_MISMO_MS, FREERTOS_ENTRE_MS), (OK, ACCENT)):
        der.text(xi, v * 2.2, ("%g ms" % v).replace(".", ","), ha="center",
                 fontsize=8.5, color=c)
    der.set_yscale("log")
    der.set_xticks(x)
    der.set_xticklabels(["mismo\nnúcleo", "entre\nnúcleos"], fontsize=8.5)
    der.set_ylabel("conmutación (ms, log.)", fontsize=8)
    der.set_ylim(0.004, 3000)
    der.set_title("la sincronización, no", fontsize=8.5, color=ACCENT, pad=6)
    der.grid(axis="y", color=GRID, lw=0.6)
    der.set_axisbelow(True)
    limpiar_ejes(der)

    fig.subplots_adjust(wspace=0.34)
    escribir(fig, "paper-freertos-dos-asuntos")


# --------------------------------------------------------------------------
# 73. Sesión 6 — el pesimismo que introduce suponer el peor caso
# --------------------------------------------------------------------------
# La primera figura ya dibuja el modelo lineal y el peor caso. Esta cuenta lo
# otro que aporta el artículo: que exigir el peor caso en TODOS los ticks
# reserva cuarenta veces más de lo que el tick cuesta en su caso más
# frecuente. Ese factor es el pesimismo que su modelo viene a reducir.
TICK_FRECUENTE_US = 1.5
TICK_PEOR_US_ART = 60.75


def paper_tick_pesimismo():
    fig, ax = plt.subplots(figsize=(7.0, 1.9))

    ax.barh([1], [TICK_PEOR_US_ART], height=0.36, color=ACCENT, alpha=0.35,
            hatch="///", edgecolor=ACCENT)
    ax.barh([0], [TICK_FRECUENTE_US], height=0.36, color=OK)

    ax.text(TICK_PEOR_US_ART + 1.2, 1,
            "lo que se reserva si se supone el peor caso en cada tick",
            va="center", fontsize=8.5, color=ACCENT)
    ax.text(TICK_FRECUENTE_US + 1.2, 0, "lo que cuesta en el caso más frecuente",
            va="center", fontsize=8.5, color=OK)
    ax.annotate("", xy=(TICK_PEOR_US_ART, 0.55), xytext=(TICK_FRECUENTE_US, 0.55),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1))
    razon = TICK_PEOR_US_ART / TICK_FRECUENTE_US
    ax.text(TICK_PEOR_US_ART / 2, 0.68,
            ("%.0f× de margen" % razon), ha="center", fontsize=9, color=MUTED)

    ax.set_yticks([])
    ax.set_xlabel("duración atribuida al tick (µs)")
    ax.set_xlim(0, 168)
    ax.set_ylim(-0.55, 1.7)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))

    escribir(fig, "paper-tick-pesimismo")


# --------------------------------------------------------------------------
# 74. Sesión 6 — los cuatro casos que cubren los cinco protocolos
# --------------------------------------------------------------------------
# El artículo desarrolla cinco protocolos para cuatro escenarios de productor
# y consumidor, según de qué lado esté el requisito temporal. La figura los
# ordena en rejilla: lo que decide el protocolo es quién escribe y quién tiene
# el plazo, no el tipo de dato.
SINC_CASOS = [
    ("dato compartido", "lector con plazo", True),
    ("dato compartido", "escritor con plazo", True),
    ("cola compartida", "lector con plazo", True),
    ("cola compartida", "escritor con plazo", True),
]


def paper_sincronizacion_casos():
    fig, ax = plt.subplots(figsize=(7.0, 2.0))

    for k, (recurso, lado, cubierto) in enumerate(SINC_CASOS):
        col, fila = k % 2, k // 2
        x, y = col * 0.5, 0.52 - fila * 0.30
        ax.add_patch(Rectangle((x + 0.02, y), 0.46, 0.25, facecolor=OK,
                               alpha=0.13, edgecolor=OK, lw=1.2))
        ax.text(x + 0.25, y + 0.165, recurso, ha="center", fontsize=8.5,
                color=INK)
        ax.text(x + 0.25, y + 0.06, lado, ha="center", fontsize=7.5, color=MUTED)

    ax.text(0.5, 0.90, "cinco protocolos para estos cuatro casos", ha="center",
            fontsize=8.5, color=INK)
    ax.text(0.5, 0.03, "la parte con plazo nunca reintenta; la otra sí",
            ha="center", fontsize=8, color=ACCENT)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    escribir(fig, "paper-sincronizacion-casos")


# --------------------------------------------------------------------------
# 75. Sesión 7 — las dimensiones en que el autor compara los cuatro protocolos
# --------------------------------------------------------------------------
# El trabajo es documental y sistemático: compara MQTT, CoAP, AMQP y HTTP
# sobre un conjunto común de dimensiones. La rejilla las ordena para que se
# vea la conclusión del autor —ninguno cubre todas— sin necesidad de leerla.
MSG_PROTOCOLOS = ["MQTT", "CoAP", "AMQP", "HTTP"]
MSG_DIMENSIONES = [
    ("cabecera pequeña", [1, 1, 0, 0]),
    ("el servidor alcanza al equipo", [1, 0, 1, 0]),
    ("niveles de calidad de servicio", [1, 0, 1, 0]),
    ("interoperabilidad universal", [0, 0, 0, 1]),
]


def paper_protocolos_dimensiones():
    filas = len(MSG_DIMENSIONES)
    fig, ax = plt.subplots(figsize=(7.2, 2.0))

    for f, (nombre, valores) in enumerate(MSG_DIMENSIONES):
        y = filas - f - 1
        ax.text(-0.12, y + 0.5, nombre, ha="right", va="center", fontsize=8,
                color=INK)
        for c, v in enumerate(valores):
            ax.add_patch(Rectangle((c + 0.08, y + 0.12), 0.84, 0.76,
                                   facecolor=OK if v else SURFACE,
                                   edgecolor=GRID, lw=0.7))
            if not v:
                ax.text(c + 0.5, y + 0.5, "no", ha="center", va="center",
                        fontsize=7, color=MUTED)

    for c, nombre in enumerate(MSG_PROTOCOLOS):
        ax.text(c + 0.5, filas + 0.2, nombre, ha="center", va="bottom",
                fontsize=9, color=NAVY)
    ax.text(len(MSG_PROTOCOLOS) / 2, -0.6, "ninguna columna está completa",
            ha="center", fontsize=8, color=ACCENT)

    ax.set_xlim(-3.4, len(MSG_PROTOCOLOS) + 0.1)
    ax.set_ylim(-0.9, filas + 0.9)
    ax.axis("off")

    escribir(fig, "paper-protocolos-dimensiones")


# --------------------------------------------------------------------------
# 76. Sesión 7 — la exactitud del banco de ensayo del artículo
# --------------------------------------------------------------------------
# Antes de dar por buena una medida de consumo conviene saber con qué se tomó.
# Los autores declaran 1000 muestras de corriente por segundo y una desviación
# del 0,011 % entre la duración del ensayo y el periodo de medida. La figura
# pone esa cifra en contexto: es la que permite atribuir la diferencia al
# algoritmo y no al instrumento.
TLS_MUESTRAS_S = 1000
TLS_DESVIACION = 0.011


def paper_tls_banco():
    fig, ax = plt.subplots(figsize=(7.0, 1.9))

    ax.barh([1], [TLS_MUESTRAS_S], height=0.34, color=NAVY)
    ax.text(TLS_MUESTRAS_S * 1.04, 1, "1000 muestras de corriente por segundo",
            va="center", fontsize=8.5, color=NAVY)
    ax.barh([0], [TLS_DESVIACION * 1000], height=0.34, color=OK)
    ax.text(TLS_DESVIACION * 1000 + 12, 0,
            "desviación declarada: 0,011 % del periodo de medida",
            va="center", fontsize=8.5, color=OK)

    ax.set_xscale("symlog", linthresh=10)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlim(0, 9000)
    ax.set_ylim(-0.6, 1.7)
    ax.text(0, -0.42, "una diferencia de consumo solo se puede atribuir al "
            "algoritmo si el banco es más preciso que ella", fontsize=8,
            color=MUTED)
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)

    escribir(fig, "paper-tls-banco")


# --------------------------------------------------------------------------
# 77. Sesión 7 — cuánta literatura aporta medidas propias
# --------------------------------------------------------------------------
# La revisión parte de 166 registros y se queda con 9 estudios empíricos que
# cumplen los criterios: medidas sobre ESP32, con ambos protocolos y magnitudes
# comparables. Esa proporción es un dato en sí mismo sobre el estado del asunto.
PRISMA_INICIAL = 166
PRISMA_INCLUIDOS = 9


def paper_mqtt_prisma():
    fig, ax = plt.subplots(figsize=(7.0, 1.9))

    ax.barh([1], [PRISMA_INICIAL], height=0.38, color=MUTED, alpha=0.55)
    ax.barh([0], [PRISMA_INCLUIDOS], height=0.38, color=OK)
    ax.text(PRISMA_INICIAL + 3, 1, f"{PRISMA_INICIAL} registros iniciales",
            va="center", fontsize=8.5, color=MUTED)
    ax.text(PRISMA_INCLUIDOS + 3, 0,
            f"{PRISMA_INCLUIDOS} con medidas propias sobre ESP32", va="center",
            fontsize=8.5, color=OK)
    ax.text(PRISMA_INICIAL / 2, -0.62,
            "el 95 % de lo publicado no aporta medidas comparables",
            ha="center", fontsize=8, color=ACCENT)

    ax.set_xlim(0, 260)
    ax.set_ylim(-0.9, 1.7)
    ax.set_yticks([])
    ax.set_xticks([])
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)

    escribir(fig, "paper-mqtt-prisma")


# --------------------------------------------------------------------------
# 78. Sesión 8 — veinte años de literatura y qué se deduce de ellos
# --------------------------------------------------------------------------
# La revisión no publica una serie anual: su resultado es que el crecimiento de
# MQTT se separa del de AMQP y CoAP de forma sostenida. La figura ordena los
# ámbitos de aplicación documentados, que es el dato concreto que sí aportan, y
# deja el crecimiento como lo que es: una afirmación cualitativa.
MQTT_AMBITOS = ["hogar y edificios", "industria", "salud", "agricultura",
                "transporte", "energía"]


def paper_mqtt_ambitos():
    fig, ax = plt.subplots(figsize=(7.2, 1.9))

    for k, nombre in enumerate(MQTT_AMBITOS):
        col, fila = k % 3, k // 3
        x, y = col * 0.34, 0.52 - fila * 0.30
        ax.add_patch(Rectangle((x + 0.01, y), 0.31, 0.24, facecolor=NAVY,
                               alpha=0.12, edgecolor=NAVY, lw=1))
        ax.text(x + 0.165, y + 0.12, nombre, ha="center", va="center",
                fontsize=8, color=INK)

    ax.text(0.5, 0.90, "ámbitos con aplicaciones de MQTT documentadas",
            ha="center", fontsize=8.5, color=NAVY)
    ax.text(0.5, 0.03, "veinte años analizados: la extensión viene de la "
            "simplicidad del modelo, no de superioridad técnica",
            ha="center", fontsize=8, color=MUTED)

    ax.set_xlim(0, 1.03)
    ax.set_ylim(0, 1)
    ax.axis("off")

    escribir(fig, "paper-mqtt-ambitos")


# --------------------------------------------------------------------------
# 79. Sesión 8 — para qué sirve repetir la medida
# --------------------------------------------------------------------------
# Los autores no publican los tiempos absolutos de cada proveedor, pero sí el
# diseño: 100 ensayos por simulación y 23 simulaciones. La figura explica qué
# compra esa repetición —poder dar media y desviación en vez de una lectura— y
# por qué sin ella la comparación entre plataformas no significaría nada.
NUBE_ENSAYOS = 100
NUBE_SIMULACIONES = 23


def paper_nube_repeticion():
    fig, ax = plt.subplots(figsize=(7.0, 1.9))

    total = NUBE_ENSAYOS * NUBE_SIMULACIONES
    ax.barh([1], [1], height=0.34, color=ACCENT)
    ax.text(1.4, 1, "una sola lectura: no se puede distinguir una plataforma "
            "de otra", va="center", fontsize=8.5, color=ACCENT)
    ax.barh([0], [total], height=0.34, color=OK)
    ax.text(total * 1.03, 0, f"{NUBE_ENSAYOS} × {NUBE_SIMULACIONES} = {total} "
            "medidas: media y desviación", va="center", fontsize=8.5, color=OK)

    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlim(0, 60000)
    ax.set_ylim(-0.6, 1.7)
    ax.set_yticks([])
    ax.set_xticks([])
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)

    escribir(fig, "paper-nube-repeticion")


# --------------------------------------------------------------------------
# 80. Sesión 8 — los dos problemas que produce mezclar tamaños
# --------------------------------------------------------------------------
# El artículo describe dos consecuencias de que el intermediario no distinga
# los flujos por tamaño, y propone una respuesta para cada una. La figura las
# empareja para que la solución no quede suelta del problema.
BORDE_PARES = [
    ("los mensajes grandes retrasan a los pequeños",
     "tres políticas de planificación en el borde"),
    ("el intermediario se queda sin memoria al acumular copias",
     "reserva explícita de memoria"),
]


def paper_borde_problema_respuesta():
    fig, ax = plt.subplots(figsize=(7.2, 1.9))

    for k, (problema, respuesta) in enumerate(BORDE_PARES):
        y = 0.62 - k * 0.34
        ax.add_patch(Rectangle((0.01, y), 0.44, 0.26, facecolor=ACCENT,
                               alpha=0.12, edgecolor=ACCENT, lw=1))
        ax.text(0.23, y + 0.13, problema, ha="center", va="center",
                fontsize=8, color=INK, wrap=True)
        ax.add_patch(FancyArrowPatch((0.46, y + 0.13), (0.53, y + 0.13),
                                     color=MUTED, arrowstyle="-|>",
                                     mutation_scale=11, lw=1.2))
        ax.add_patch(Rectangle((0.54, y), 0.44, 0.26, facecolor=OK,
                               alpha=0.12, edgecolor=OK, lw=1))
        ax.text(0.76, y + 0.13, respuesta, ha="center", va="center",
                fontsize=8, color=INK)

    ax.text(0.23, 0.94, "problema observado", ha="center", fontsize=8,
            color=ACCENT)
    ax.text(0.76, 0.94, "respuesta propuesta", ha="center", fontsize=8,
            color=OK)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.axis("off")

    escribir(fig, "paper-borde-problema-respuesta")


# --------------------------------------------------------------------------
# 81. Sesión 9 — las fases del proceso de confianza
# --------------------------------------------------------------------------
# El documento del NIST describe un proceso genérico de confianza con sus
# fases. La figura las pone en orden para que se vea que la incorporación no
# es un trámite de puesta en marcha, sino el momento en que se establece una
# relación que después hay que poder deshacer.
CONFIANZA_FASES = [
    ("identidad de fábrica", NAVY),
    ("prueba de identidad", NAVY),
    ("autorización de la red", OK),
    ("entrega de credenciales", OK),
    ("operación", MUTED),
    ("revocación", ACCENT),
]


def paper_proceso_confianza():
    fig, ax = plt.subplots(figsize=(7.6, 1.6))
    n = len(CONFIANZA_FASES)
    ancho = 1.0 / n
    for k, (nombre, color) in enumerate(CONFIANZA_FASES):
        x = k * ancho
        ax.add_patch(Rectangle((x + 0.004, 0.45), ancho - 0.008, 0.3,
                               facecolor=color, alpha=0.16, edgecolor=color, lw=1.1))
        ax.text(x + ancho / 2, 0.60, nombre.replace(" de ", "\nde ").replace(" la ", "\nla "),
                ha="center", va="center", fontsize=7.5, color=INK)
        if k:
            ax.add_patch(FancyArrowPatch((x - 0.004, 0.60), (x + 0.002, 0.60),
                                         color=GRID, arrowstyle="-|>",
                                         mutation_scale=7, lw=1))
    ax.text(0.5, 0.90, "el proceso de confianza, fase por fase", ha="center",
            fontsize=8.5, color=INK)
    ax.text(0.5, 0.22, "la última fase existe porque la primera creó una "
            "relación que hay que poder deshacer", ha="center", fontsize=8,
            color=ACCENT)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1.05)
    ax.axis("off")
    escribir(fig, "paper-proceso-confianza")


# --------------------------------------------------------------------------
# 82. Sesión 9 — las tres piezas de la provisión de identidad
# --------------------------------------------------------------------------
# El artículo descompone el proceso en configuración del equipo, provisión de
# la identidad y provisión de sus claves. La figura las separa y marca cuál de
# las tres es la que sigue dependiendo de intervención manual, que es donde
# los autores localizan el cuello de botella.
IDENTIDAD_PIEZAS = [
    ("configuración del equipo", "automatizable", True),
    ("provisión de la identidad", "problema abierto", False),
    ("provisión de las claves", "problema abierto", False),
]


def paper_identidad_piezas():
    fig, ax = plt.subplots(figsize=(7.2, 1.8))
    for k, (nombre, estado, resuelto) in enumerate(IDENTIDAD_PIEZAS):
        x = k * 0.34
        color = OK if resuelto else ACCENT
        ax.add_patch(Rectangle((x + 0.01, 0.42), 0.31, 0.34, facecolor=color,
                               alpha=0.13, edgecolor=color, lw=1.2))
        ax.text(x + 0.165, 0.63, nombre.replace(" del ", "\ndel ").replace(" de la ", "\nde la ").replace(" de las ", "\nde las "),
                ha="center", va="center", fontsize=8, color=INK)
        ax.text(x + 0.165, 0.48, estado, ha="center", fontsize=7.5, color=color)
    ax.text(0.51, 0.90, "el proceso en tres piezas", ha="center", fontsize=8.5,
            color=INK)
    ax.text(0.51, 0.24, "dos de las tres siguen dependiendo de configuración "
            "manual: ahí está el cuello de botella", ha="center", fontsize=8,
            color=ACCENT)
    ax.set_xlim(0, 1.03)
    ax.set_ylim(0.12, 1.05)
    ax.axis("off")
    escribir(fig, "paper-identidad-piezas")


# --------------------------------------------------------------------------
# 83. Sesión 9 — la única etiqueta que no mejoró la elección
# --------------------------------------------------------------------------
# El estudio es direccional y no publica porcentajes, así que la figura no los
# inventa: ordena las etiquetas ensayadas según el sentido del efecto que los
# autores describen, con la excepción marcada.
ETIQUETA_EFECTOS = [
    ("etiqueta con información de seguridad", "más elegidos", True),
    ("etiqueta con vida de soporte", "más elegidos", True),
    ("etiqueta que sugiere seguridad deficiente", "sin mejora", False),
]


def paper_etiqueta_efecto():
    fig, ax = plt.subplots(figsize=(7.2, 1.8))
    for k, (nombre, efecto, sube) in enumerate(ETIQUETA_EFECTOS):
        y = 0.66 - k * 0.24
        color = OK if sube else ACCENT
        ax.text(0.02, y, "↑" if sube else "→", fontsize=12, color=color,
                va="center")
        ax.text(0.08, y, nombre, fontsize=8.5, va="center", color=INK)
        ax.text(0.98, y, efecto, fontsize=8.5, va="center", ha="right",
                color=color)
    ax.text(0.02, 0.90, "sentido del efecto sobre la elección de compra",
            fontsize=8.5, color=INK)
    ax.text(0.02, 0.06, "declarar una protección pobre penaliza más que "
            "guardar silencio", fontsize=8, color=ACCENT)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    escribir(fig, "paper-etiqueta-efecto")


# --------------------------------------------------------------------------
# 84. Sesión 10 — eficacia desigual de las herramientas de auditoría
# --------------------------------------------------------------------------
# La revisión concluye que las herramientas cubren unas partes del ciclo mucho
# mejor que otras. No publica una tabla de eficacia, así que la figura ordena
# las etapas y marca solo lo que el texto afirma: dónde hay herramienta madura
# y dónde el trabajo sigue siendo manual.
AUDITORIA_ETAPAS = [
    ("componentes de software", "herramienta madura", True),
    ("almacenamiento", "parcial", None),
    ("configuración", "parcial", None),
    ("entrega", "manual", False),
    ("mantenimiento", "manual", False),
    ("actualización", "parcial", None),
]


def paper_auditoria_cobertura():
    fig, ax = plt.subplots(figsize=(7.4, 1.8))
    n = len(AUDITORIA_ETAPAS)
    ancho = 1.0 / n
    for k, (nombre, estado, madura) in enumerate(AUDITORIA_ETAPAS):
        x = k * ancho
        color = OK if madura else (ACCENT if madura is False else WARN)
        ax.add_patch(Rectangle((x + 0.004, 0.44), ancho - 0.008, 0.3,
                               facecolor=color, alpha=0.18, edgecolor=color, lw=1.1))
        ax.text(x + ancho / 2, 0.59, nombre.replace(" de ", "\nde "), ha="center",
                va="center", fontsize=7.5, color=INK)
        ax.text(x + ancho / 2, 0.36, estado, ha="center", fontsize=7, color=color)
    ax.text(0.5, 0.88, "el ciclo completo del firmware, etapa por etapa",
            ha="center", fontsize=8.5, color=INK)
    ax.text(0.5, 0.14, "auditar solo el binario cubre la primera; el resto es "
            "donde se compromete un equipo en operación", ha="center",
            fontsize=8, color=ACCENT)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.05, 1.02)
    ax.axis("off")
    escribir(fig, "paper-auditoria-cobertura")


# --------------------------------------------------------------------------
# 85. Sesión 10 — los tres métodos y qué intercambian
# --------------------------------------------------------------------------
# El artículo clasifica los métodos en tres categorías y concluye que ninguna
# sirve para todo, porque exactitud y esfuerzo se intercambian. La figura sitúa
# las tres en ese plano; es una ordenación cualitativa, tomada de sus
# conclusiones, no una medida.
CONSUMO_METODOS = [
    ("medida directa", 0.88, 0.85, OK),
    ("híbrido", 0.55, 0.5, WARN),
    ("estimación por modelo", 0.25, 0.2, ACCENT),
]


def paper_consumo_metodos():
    fig, ax = plt.subplots(figsize=(7.4, 1.8))
    for nombre, exactitud, esfuerzo, color in CONSUMO_METODOS:
        ax.scatter([esfuerzo], [exactitud], s=180, color=color, zorder=4)
        ax.annotate(nombre, (esfuerzo, exactitud), textcoords="offset points",
                    xytext=(12, -3), fontsize=8.5, color=color)
    ax.plot([0.15, 0.92], [0.12, 0.92], color=GRID, lw=1, ls="--")
    ax.text(0.52, 0.30, "exactitud y esfuerzo se intercambian", fontsize=8,
            color=MUTED, rotation=32)
    ax.set_xlabel("esfuerzo que exige")
    ax.set_ylabel("exactitud alcanzable", fontsize=8)
    ax.set_xlim(0, 1.35)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax)
    escribir(fig, "paper-consumo-metodos")


# --------------------------------------------------------------------------
# 86. Sesión 10 — lo que evita la retransmisión por segmento
# --------------------------------------------------------------------------
# El artículo declara retransmisión por segmento: solo se reenvía el trozo
# perdido, no la imagen entera. Con el tiempo publicado para 1000 kB —4338 s—
# la diferencia entre las dos estrategias ante un fallo se calcula exacta.
OTA_TOTAL_S = 4338
OTA_TAMANO_KB = 1000
OTA_SEGMENTO_KB = 8


def paper_ota_segmento():
    por_kb = OTA_TOTAL_S / OTA_TAMANO_KB
    fig, ax = plt.subplots(figsize=(7.2, 1.8))
    datos = [("reenviar la imagen entera", OTA_TOTAL_S, ACCENT),
             ("reenviar solo el segmento perdido", OTA_SEGMENTO_KB * por_kb, OK)]
    for k, (nombre, seg, color) in enumerate(datos):
        ax.barh([1 - k], [seg / 60], height=0.34, color=color)
        ax.text(seg / 60 + 1.2, 1 - k, f"{nombre}: {seg / 60:.0f} min"
                if seg > 300 else f"{nombre}: {seg:.0f} s", va="center",
                fontsize=8.5, color=color)
    ax.set_xlabel("coste de recuperarse de un fallo de enlace (min)")
    ax.set_xlim(0, 190)
    ax.set_ylim(-0.6, 1.7)
    ax.set_yticks([])
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    limpiar_ejes(ax, ocultar=("top", "right", "left"))
    escribir(fig, "paper-ota-segmento")


# --------------------------------------------------------------------------
# 87. Sesión 11 — qué herramientas hace posibles la máquina virtual
# --------------------------------------------------------------------------
# Los autores destacan tanto la portabilidad como las herramientas de
# desarrollo que la máquina virtual permite sobre el código que corre en el
# dispositivo. La figura las enumera frente a lo que ofrece el flujo compilado
# tradicional, que es el punto de comparación del artículo.
VM_HERRAMIENTAS = [
    ("depuración remota sobre el dispositivo", False, True),
    ("sistema de tipos del lenguaje", False, True),
    ("gestión automática de memoria", False, True),
    ("mismo binario en varias arquitecturas", False, True),
    ("tiempo de ejecución sin sobrecoste", True, False),
]


def paper_vm_herramientas():
    filas = len(VM_HERRAMIENTAS)
    fig, ax = plt.subplots(figsize=(7.4, 1.9))
    for k, (nombre, compilado, virtual) in enumerate(VM_HERRAMIENTAS):
        y = filas - k - 1
        ax.text(-0.12, y + 0.5, nombre, ha="right", va="center", fontsize=7.5,
                color=INK)
        for c, hay in enumerate((compilado, virtual)):
            ax.add_patch(Rectangle((c + 0.1, y + 0.14), 0.8, 0.72,
                                   facecolor=(NAVY if c == 0 else OK) if hay else SURFACE,
                                   edgecolor=GRID, lw=0.7))
            if not hay:
                ax.text(c + 0.5, y + 0.5, "no", ha="center", va="center",
                        fontsize=7, color=MUTED)
    ax.text(0.5, filas + 0.18, "compilado", ha="center", va="bottom",
            fontsize=8.5, color=NAVY)
    ax.text(1.5, filas + 0.18, "máquina virtual", ha="center", va="bottom",
            fontsize=8.5, color=OK)
    ax.set_xlim(-3.6, 2.1)
    ax.set_ylim(-0.3, filas + 0.9)
    ax.axis("off")
    escribir(fig, "paper-vm-herramientas")


# --------------------------------------------------------------------------
# 88. Sesión 11 — las dos propiedades y qué exige cada una
# --------------------------------------------------------------------------
# El trabajo es una toma de posición razonada, sin medidas propias. Sus dos
# propiedades declaradas son aislamiento y portabilidad. La figura las pone
# frente a lo que cada una pide a cambio, que es lo que el artículo analiza y
# lo único que se puede afirmar sin inventar cifras que no publica.
WASM_PROPIEDADES = [
    ("aislamiento fuerte",
     "el módulo solo alcanza lo que el anfitrión concede",
     "hay que declarar cada concesión, una por una"),
    ("portabilidad",
     "el mismo módulo sobre plataformas distintas",
     "un runtime por plataforma, y hay que mantenerlo"),
]


def paper_wasm_propiedades():
    fig, ax = plt.subplots(figsize=(7.4, 1.9))
    for k, (nombre, aporta, exige) in enumerate(WASM_PROPIEDADES):
        y = 0.60 - k * 0.34
        ax.add_patch(Rectangle((0.01, y), 0.24, 0.28, facecolor=NAVY,
                               alpha=0.14, edgecolor=NAVY, lw=1.1))
        ax.text(0.13, y + 0.14, nombre, ha="center", va="center", fontsize=8.5,
                color=INK)
        ax.text(0.29, y + 0.20, "aporta", fontsize=7, color=OK)
        ax.text(0.29, y + 0.09, aporta, fontsize=8, color=INK)
        ax.text(0.29, y - 0.03, "exige  " + exige, fontsize=8, color=ACCENT)
    ax.text(0.01, 0.94, "toma de posición razonada: el artículo no aporta "
            "medidas propias", fontsize=8, color=MUTED)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.05, 1.02)
    ax.axis("off")
    escribir(fig, "paper-wasm-propiedades")


# --------------------------------------------------------------------------
# 89. Sesión 11 — las cinco dimensiones y cuáles comprueba ejecutar
# --------------------------------------------------------------------------
# El artículo evalúa validez, corrección, seguridad, fiabilidad y
# mantenibilidad. Solo las dos primeras se comprueban ejecutando; las otras
# tres exigen leer. La figura reparte las cinco según eso, que es el punto que
# el estudio deja escrito.
GEN_DIMENSIONES = [
    ("validez", True), ("corrección", True), ("seguridad", False),
    ("fiabilidad", False), ("mantenibilidad", False),
]


def paper_codigo_dimensiones():
    fig, ax = plt.subplots(figsize=(7.4, 1.8))
    for k, (nombre, ejecutando) in enumerate(GEN_DIMENSIONES):
        x = k * 0.2
        color = OK if ejecutando else ACCENT
        ax.add_patch(Rectangle((x + 0.01, 0.46), 0.18, 0.3, facecolor=color,
                               alpha=0.16, edgecolor=color, lw=1.1))
        ax.text(x + 0.1, 0.61, nombre, ha="center", va="center", fontsize=8,
                color=INK)
    ax.annotate("", xy=(0.01, 0.36), xytext=(0.39, 0.36),
                arrowprops=dict(arrowstyle="<->", color=OK, lw=1.1))
    ax.text(0.2, 0.24, "se comprueban ejecutando", ha="center", fontsize=8,
            color=OK)
    ax.annotate("", xy=(0.41, 0.36), xytext=(0.99, 0.36),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.1))
    ax.text(0.7, 0.24, "exigen leer el código", ha="center", fontsize=8,
            color=ACCENT)
    ax.text(0.5, 0.88, "las cinco dimensiones evaluadas", ha="center",
            fontsize=8.5, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.12, 1.02)
    ax.axis("off")
    escribir(fig, "paper-codigo-dimensiones")


# --------------------------------------------------------------------------
# 90. Sesión 12 — las tres cosas que la cuantización cambia a la vez
# --------------------------------------------------------------------------
# El artículo propone una cadena extremo a extremo y advierte de que la
# eficiencia depende del hardware y del marco de trabajo, no solo del modelo.
# La figura separa qué cambia al pasar de 32 a 8 bits y qué NO se transfiere de
# una placa a otra, que es la advertencia que más veces se pasa por alto.
CUANT_EFECTOS = [
    ("memoria del modelo", "a la cuarta parte", True),
    ("aritmética", "entera, más rápida en muchos MCU", True),
    ("exactitud", "puede degradarse: hay que medirla", None),
    ("eficiencia energética", "depende de la placa y del marco", False),
]


def paper_cuantizacion_efectos():
    fig, ax = plt.subplots(figsize=(7.4, 2.1))
    for k, (nombre, efecto, seguro) in enumerate(CUANT_EFECTOS):
        y = 0.78 - k * 0.17
        color = OK if seguro else (ACCENT if seguro is False else WARN)
        ax.text(0.02, y, "✓" if seguro else ("✕" if seguro is False else "?"),
                fontsize=10, color=color, va="center")
        ax.text(0.07, y, nombre, fontsize=8.5, va="center", color=INK)
        ax.text(0.42, y, efecto, fontsize=8.5, va="center", color=color)
    ax.text(0.02, 0.94, "qué cambia al pasar de 32 a 8 bits por parámetro",
            fontsize=8.5, color=INK)
    ax.text(0.02, 0.03, "las cifras de tamaño y de tiempo no se transfieren de "
            "una placa a otra: hay que medir en el hardware de destino",
            fontsize=8, color=ACCENT)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    escribir(fig, "paper-cuantizacion-efectos")


# --------------------------------------------------------------------------
# 91. Sesión 12 — lo que falta para que las cifras signifiquen algo
# --------------------------------------------------------------------------
# Los autores identifican los obstáculos y proponen la dirección. La figura
# empareja cada obstáculo con lo que haría falta, para que la conclusión no
# quede como una lista de quejas.
TINYML_PARES = [
    ("cada fabricante trae sus herramientas", "cargas de trabajo comunes"),
    ("compiladores propietarios y cerrados", "métricas compartidas"),
    ("diversidad de hardware", "un intérprete común para intercambiar modelos"),
]


def paper_tinyml_obstaculos():
    fig, ax = plt.subplots(figsize=(7.4, 1.9))
    for k, (obstaculo, falta) in enumerate(TINYML_PARES):
        y = 0.62 - k * 0.22
        ax.add_patch(Rectangle((0.01, y), 0.42, 0.17, facecolor=ACCENT,
                               alpha=0.12, edgecolor=ACCENT, lw=1))
        ax.text(0.22, y + 0.085, obstaculo, ha="center", va="center",
                fontsize=8, color=INK)
        ax.add_patch(FancyArrowPatch((0.44, y + 0.085), (0.51, y + 0.085),
                                     color=MUTED, arrowstyle="-|>",
                                     mutation_scale=10, lw=1.1))
        ax.add_patch(Rectangle((0.52, y), 0.46, 0.17, facecolor=OK,
                               alpha=0.12, edgecolor=OK, lw=1))
        ax.text(0.75, y + 0.085, falta, ha="center", va="center", fontsize=8,
                color=INK)
    ax.text(0.22, 0.87, "obstáculo identificado", ha="center", fontsize=8,
            color=ACCENT)
    ax.text(0.75, 0.87, "lo que haría falta", ha="center", fontsize=8, color=OK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    escribir(fig, "paper-tinyml-obstaculos")


# --------------------------------------------------------------------------
# 92. Sesión 12 — lo que la detección no supervisada evita pedir
# --------------------------------------------------------------------------
# El sistema del artículo no necesita un conjunto de fallos etiquetados, que en
# un equipo industrial rara vez existe. La figura contrapone lo que cada
# enfoque exige antes de poder funcionar.
ANOM_ENFOQUES = [
    ("supervisado", [("ejemplos de funcionamiento normal", True),
                     ("ejemplos de cada fallo, etiquetados", True),
                     ("que los fallos ya hayan ocurrido", True)]),
    ("no supervisado", [("ejemplos de funcionamiento normal", True),
                        ("ejemplos de cada fallo, etiquetados", False),
                        ("que los fallos ya hayan ocurrido", False)]),
]


def paper_anomalias_requisitos():
    fig, ax = plt.subplots(figsize=(7.4, 1.9))
    for c, (titulo, filas) in enumerate(ANOM_ENFOQUES):
        x = c * 0.5
        color = ACCENT if c == 0 else OK
        ax.text(x + 0.24, 0.90, titulo, ha="center", fontsize=8.5, color=color)
        for k, (texto, exige) in enumerate(filas):
            y = 0.66 - k * 0.20
            ax.text(x + 0.02, y, "•" if exige else "—", fontsize=10,
                    color=color if exige else MUTED, va="center")
            ax.text(x + 0.06, y, texto, fontsize=7.5, va="center",
                    color=INK if exige else MUTED)
    ax.text(0.5, 0.04, "en un equipo industrial, un conjunto de fallos "
            "etiquetados rara vez existe", ha="center", fontsize=8, color=MUTED)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    escribir(fig, "paper-anomalias-requisitos")

FIGURAS = [
    cadena_tamanos,
    familia_arquitecturas,
    flujo_flasheo,
    paper_lenguajes_esp32,
    paper_uart_tramas,
    adc_interno_vs_externo,
    imagen_flash,
    paper_llm_limites,
    banderas_vs_estados,
    paper_statecharts_escala,
    paper_conmutacion_nucleos,
    paper_costo_tick,
    periodo_bucle_vs_tareas,
    capas_sobrecarga,
    canales_wifi,
    politica_transmision,
    qos_paquetes,
    paper_capas_alcance,
    paper_defectos_firmware,
    paper_trama_crc,
    paper_serializacion_bytes,
    paper_calibracion,
    paper_resolucion_adc,
    paper_interrupciones_plazo,
    paper_fsm_combinaciones,
    paper_umbral_fotorresistencia,
    paper_sincronizacion_costo,
    paper_cabecera_fraccion,
    paper_clave_equivalente,
    paper_mqtt_dos_ventajas,
    paper_broker_enlaces,
    paper_tiempo_de_servicio,
    paper_cola_por_tamano,
    paper_ciclo_incorporacion,
    paper_provision_escala,
    paper_etiqueta_observable,
    paper_ciclo_firmware,
    paper_medicion_consumo,
    paper_ota_tiempo,
    paper_vm_artefactos,
    paper_aislamiento_modulo,
    paper_codigo_generado,
    paper_cuantizacion_memoria,
    paper_comparabilidad,
    paper_vigilancia_continua,
    esp_claw_requisitos,
    memoria_fragmentacion,
    tabla_particiones,
    metricas_matriz_confusion,
    niveles_integracion,
    arduino_frente_a_espidf,
    paper_adc_periodos,
    paper_emulacion_sustitucion,
    paper_llm_causas,
    paper_capas_tres,
    paper_lenguajes_brecha,
    paper_defectos_por_proyecto,
    paper_crc_detectar,
    paper_serializacion_dos_costos,
    paper_uart_intervalo_minimo,
    paper_calibracion_valor,
    paper_reloj_comun,
    paper_peor_caso_incompleto,
    paper_fsm_codigos,
    paper_pn_arquitecturas,
    paper_statecharts_tiempo,
    paper_freertos_dos_asuntos,
    paper_tick_pesimismo,
    paper_sincronizacion_casos,
    paper_protocolos_dimensiones,
    paper_tls_banco,
    paper_mqtt_prisma,
    paper_mqtt_ambitos,
    paper_nube_repeticion,
    paper_borde_problema_respuesta,
    paper_proceso_confianza,
    paper_identidad_piezas,
    paper_etiqueta_efecto,
    paper_auditoria_cobertura,
    paper_consumo_metodos,
    paper_ota_segmento,
    paper_vm_herramientas,
    paper_wasm_propiedades,
    paper_codigo_dimensiones,
    paper_cuantizacion_efectos,
    paper_tinyml_obstaculos,
    paper_anomalias_requisitos,
]


def main() -> None:
    print(f"Generando {len(FIGURAS)} figuras en {SALIDA.relative_to(RAIZ)}/")
    for figura in FIGURAS:
        figura()
    print("Listo.")


if __name__ == "__main__":
    main()
