"""Genera gestos.csv con DATOS SINTÉTICOS (simulados), no capturados.

¡OJO! Este script existe solo para que el ejemplo 22 funcione «de fábrica»,
antes de que tengas tu propia captura. Los números de gestos.csv NO salen de
un potenciómetro real: salen de un modelo aproximado de cómo se mueve una mano.

Lo que tienes que hacer tú:
  1. Graba el ejemplo 21 en tu placa y captura varias sesiones (varios días,
     varias personas) de los tres gestos, etiquetando con el pulsador.
  2. Junta los registros en un solo archivo y guárdalo como gestos.csv en esta
     carpeta (las líneas que empiezan por # se ignoran solas).
  3. Ejecuta entrenar.py. No vuelvas a ejecutar este script: sobrescribiría
     tu captura.

Qué simula, por gesto (códigos del ADC, 0-4095, a 50 Hz):
  quieto  la mano apoyada: valor fijo + ruido del ADC + algún roce pequeño
  giro    girar el potenciómetro de un extremo a otro, despacio o deprisa,
          con una pausa al llegar al tope antes de volver
  vaiven  mover la perilla adelante y atrás, de 1 a 4 veces por segundo
Cada sesión tiene su propio nivel de ruido y su propia «mano» (velocidad,
amplitud, frecuencia), igual que dos personas o dos días distintos.

A cada señal se le aplica caracteristicas.extraer(): la MISMA función que
calcula el ESP32 en Ventana.cpp. Por eso el CSV tiene exactamente el formato
del ejemplo 21: sesion,ventana,etiqueta,media,desv,rango,cruces
"""
import csv
import math
import os
import random

from caracteristicas import N_MUESTRAS, extraer, ventanas

FS = 50.0                 # Hz
SEMILLA = 2026            # misma semilla -> mismo gestos.csv
N_SESIONES = 16
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gestos.csv")


def adc(valor, ruido, rng):
    """Valor ideal -> lectura del ADC: ruido gaussiano, algún pico suelto, recorte y entero."""
    v = valor + rng.gauss(0.0, ruido)
    if rng.random() < 0.004:                      # pico ocasional (interferencia, mal contacto)
        v += rng.choice([-1, 1]) * rng.uniform(40, 90)
    return int(min(4095, max(0, round(v))))


def senal_quieto(segundos, mano, rng):
    nivel = rng.uniform(150, 3950)
    n = int(segundos * FS)
    x, deriva = [], 0.0
    for _ in range(n):
        deriva += rng.gauss(0.0, 0.6)             # deriva lenta (temperatura, alimentación)
        if rng.random() < mano["roce"]:           # la mano roza la perilla
            nivel += rng.uniform(-70, 70)
        x.append(adc(nivel + deriva, mano["ruido"], rng))
    return x


def senal_giro(segundos, mano, rng):
    n = int(segundos * FS)
    lo = rng.uniform(0, 600)
    hi = rng.uniform(3300, 4095)
    pos = rng.uniform(lo, hi)
    sentido = rng.choice([-1, 1])
    pausa = 0
    x = []
    for _ in range(n):
        if pausa > 0:
            pausa -= 1                            # quieto un instante en el tope
        else:
            vel = mano["vel_giro"] * (1.0 + 0.35 * math.sin(len(x) / 17.0) + rng.gauss(0.0, 0.1))
            pos += sentido * max(vel, 50.0) / FS
            if pos >= hi or pos <= lo:            # llegó al tope: para y da la vuelta
                pos = min(hi, max(lo, pos))
                sentido = -sentido
                pausa = int(rng.uniform(0.1, 0.5) * FS)
        x.append(adc(pos, mano["ruido"], rng))
    return x


def senal_vaiven(segundos, mano, rng):
    n = int(segundos * FS)
    centro = rng.uniform(600, 3500)
    f = mano["f_vaiven"] * rng.uniform(0.8, 1.2)
    amp = mano["amp_vaiven"] * rng.uniform(0.7, 1.3)
    fase, x = 0.0, []
    for _ in range(n):
        f = min(4.5, max(0.9, f + rng.gauss(0.0, 0.03)))       # el ritmo de la mano varía
        amp = min(1100, max(50, amp + rng.gauss(0.0, 4.0)))
        centro += rng.gauss(0.0, 2.0)
        fase += 2 * math.pi * f / FS
        x.append(adc(centro + amp * math.sin(fase), mano["ruido"], rng))
    return x


GENERADORES = {"quieto": senal_quieto, "giro": senal_giro, "vaiven": senal_vaiven}


def main():
    rng = random.Random(SEMILLA)
    filas = []
    for _ in range(N_SESIONES):
        sesion = "%08x" % rng.getrandbits(32)     # como esp_random() en el ejemplo 21
        mano = {
            "ruido": rng.uniform(3, 14),          # ruido del ADC de esa placa / ese día
            "roce": rng.uniform(0.0, 0.01),
            "vel_giro": rng.uniform(500, 3000),   # códigos por segundo
            "f_vaiven": rng.uniform(1.0, 3.5),    # vaivenes por segundo
            "amp_vaiven": rng.uniform(80, 700),   # media amplitud, en códigos
        }
        numero = 0
        # Cada sesión graba los tres gestos varias veces, en orden variable,
        # tramos de 8 a 25 s (como quien pulsa el botón y repite).
        tramos = [g for g in GENERADORES for _ in range(2)]
        rng.shuffle(tramos)
        for gesto in tramos:
            senal = GENERADORES[gesto](rng.uniform(8, 25), mano, rng)
            # El ejemplo 21 vacía el búfer al cambiar de etiqueta: ninguna
            # ventana mezcla dos gestos. Aquí cada tramo se corta por separado.
            for v in ventanas(senal):
                numero += 1
                filas.append([sesion, numero, gesto] + extraer(v))

    with open(SALIDA, "w", newline="") as f:
        f.write("# DATOS SINTETICOS generados por simular_datos.py (semilla %d).\n" % SEMILLA)
        f.write("# Reemplazalos por tu captura del ejemplo 21 antes de sacar conclusiones.\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["sesion", "ventana", "etiqueta", "media", "desv", "rango", "cruces"])
        w.writerows(filas)

    cuenta = {g: sum(1 for r in filas if r[2] == g) for g in GENERADORES}
    print("gestos.csv: %d ventanas de %d sesiones (%d muestras por ventana)"
          % (len(filas), N_SESIONES, N_MUESTRAS))
    print("  " + "  ".join("%s=%d" % kv for kv in cuenta.items()))


if __name__ == "__main__":
    main()
