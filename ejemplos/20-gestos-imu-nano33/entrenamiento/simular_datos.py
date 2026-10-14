"""Genera punch.csv y flex.csv SINTÉTICOS con el formato exacto del sketch de captura.

¡No son datos medidos! Sirven para que el cuaderno y el ejemplo funcionen desde el
primer día. Para la clase, captura tus propios gestos con el entorno «captura»
(ver README) y reemplaza estos archivos. NO ejecutes este script después de copiar
tu captura: la sobrescribe.

Formato (igual que src/captura/main.cpp):
    aX,aY,aZ,gX,gY,gZ          <- cabecera
    119 líneas por gesto, aceleración en g y giro en grados/s, 3 decimales
    una línea vacía entre gesto y gesto

Modelo aproximado del movimiento (placa en la mano, con el USB hacia el codo):
- punch (puñetazo): golpe de aceleración hacia delante (+aY) que supera 2,5 g,
  frenazo brusco (-aY) y vuelta al reposo; el giro es pequeño.
- flex (flexión del brazo, como una pesa): la muñeca rota en torno a X; la gravedad
  pasa de aZ a aY y el giroscopio gX marca un pico de cientos de grados/s.
"""
import math
import os
import random

SEMILLA = 2026
N_GRABACIONES = 40          # por gesto (el tutorial oficial pide unas 10 como mínimo)
MUESTRAS = 119              # igual que numSamples en el sketch
FS = 100.0                  # Hz, frecuencia del BMI270 en la librería Arduino_BMI270_BMM150

CARPETA = os.path.dirname(os.path.abspath(__file__))


def recortar(v, lim):
    return max(-lim, min(lim, v))


def mezclar_ejes(v, ang):
    """Gira un poco el vector en torno a Z: nadie sujeta la placa siempre igual."""
    x, y, z = v
    c, s = math.cos(ang), math.sin(ang)
    return (c * x - s * y, s * x + c * y, z)


def punch(rng):
    amp = rng.uniform(2.8, 3.9)          # g del empuje inicial
    freno = rng.uniform(2.5, 4.0)        # g del frenazo
    t_freno = rng.uniform(0.12, 0.22)    # s
    ang = rng.uniform(-0.35, 0.35)
    filas = []
    for n in range(MUESTRAS):
        t = n / FS
        empuje = amp * math.exp(-t / 0.05)
        frenazo = -freno * math.exp(-((t - t_freno) / 0.05) ** 2)
        rebote = 0.6 * math.exp(-(t - t_freno) / 0.15) * math.sin(2 * math.pi * 6 * (t - t_freno)) if t > t_freno else 0.0
        ay = empuje + frenazo + rebote
        ax = 0.3 * math.sin(2 * math.pi * 3 * t) * math.exp(-t / 0.3)
        az = 1.0 + 0.4 * math.exp(-t / 0.1)
        ax, ay, az = mezclar_ejes((ax, ay, az), ang)
        gx = 60 * math.sin(2 * math.pi * 2 * t) * math.exp(-t / 0.4)
        gy = 40 * math.exp(-t / 0.2)
        gz = 30 * math.sin(2 * math.pi * 4 * t) * math.exp(-t / 0.3)
        filas.append((ax, ay, az, gx, gy, gz))
    return filas


def flex(rng):
    pico = rng.uniform(450, 1100)        # grados/s del giro máximo
    dur = rng.uniform(0.45, 0.7)         # s que dura la subida
    ang = rng.uniform(-0.35, 0.35)
    arranque = rng.uniform(2.6, 3.3)     # g del tirón inicial que dispara la captura
    filas = []
    theta = 0.0
    for n in range(MUESTRAS):
        t = n / FS
        gx = pico * math.sin(math.pi * t / dur) if t < dur else -0.15 * pico * math.sin(math.pi * (t - dur) / dur) * math.exp(-(t - dur) / 0.3)
        theta += math.radians(gx) / FS
        centripeta = (math.radians(gx) ** 2) * 0.03          # brazo ~30 cm
        ax = 0.2 * math.sin(2 * math.pi * 2 * t)
        ay = math.sin(theta) + arranque * math.exp(-t / 0.04)
        az = math.cos(theta) + centripeta
        ax, ay, az = mezclar_ejes((ax, ay, az), ang)
        gy = 80 * math.sin(2 * math.pi * 1.5 * t)
        gz = 50 * math.sin(math.pi * t / dur) if t < dur else 0.0
        filas.append((ax, ay, az, gx, gy, gz))
    return filas


def ruido(filas, rng):
    out = []
    for ax, ay, az, gx, gy, gz in filas:
        out.append((
            recortar(ax + rng.gauss(0, 0.03), 4.0),
            recortar(ay + rng.gauss(0, 0.03), 4.0),
            recortar(az + rng.gauss(0, 0.03), 4.0),
            recortar(gx + rng.gauss(0, 4.0), 2000.0),
            recortar(gy + rng.gauss(0, 4.0), 2000.0),
            recortar(gz + rng.gauss(0, 4.0), 2000.0),
        ))
    return out


def escribir(nombre, generador, rng):
    ruta = os.path.join(CARPETA, nombre + ".csv")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("aX,aY,aZ,gX,gY,gZ\n")
        for _ in range(N_GRABACIONES):
            for fila in ruido(generador(rng), rng):
                f.write(",".join(f"{v:.3f}" for v in fila) + "\n")
            f.write("\n")
    print(f"{ruta}: {N_GRABACIONES} gestos x {MUESTRAS} muestras")


if __name__ == "__main__":
    rng = random.Random(SEMILLA)
    escribir("punch", punch, rng)
    escribir("flex", flex, rng)
