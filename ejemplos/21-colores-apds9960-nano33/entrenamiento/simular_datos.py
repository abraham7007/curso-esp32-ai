"""Genera rojo.csv, verde.csv y azul.csv SINTÉTICOS con el formato del sketch de captura.

¡No son datos medidos! Las proporciones de partida son una suposición razonable para
cartulinas de colores bajo luz de aula; el APDS9960 real puede dar otras (su canal
azul y verde suelen pesar más de lo que esperas). Sirven para que el cuaderno y el
ejemplo funcionen desde el primer día. Para la clase, captura tus objetos con el
entorno «captura» (ver README) y reemplaza estos archivos. NO ejecutes este script
después de copiar tu captura: la sobrescribe.

Formato (igual que src/captura/main.cpp):
    r,g,b              <- cabecera
    0.552,0.241,0.207  <- r/(r+g+b), g/(r+g+b), b/(r+g+b) con 3 decimales; suman 1
"""
import os
import random

SEMILLA = 2026
MUESTRAS_POR_TANDA = 25     # lecturas seguidas con el objeto quieto frente al sensor
TANDAS = 6                  # veces que acercas el objeto (otra posición, otro ángulo)

# Proporción media (r, g, b) supuesta para cada clase
COLORES = {
    "rojo":  (0.55, 0.25, 0.20),
    "verde": (0.30, 0.42, 0.28),
    "azul":  (0.24, 0.33, 0.43),
}

CARPETA = os.path.dirname(os.path.abspath(__file__))


def normalizar(r, g, b):
    s = r + g + b
    return r / s, g / s, b / s


def escribir(nombre, media, rng):
    ruta = os.path.join(CARPETA, nombre + ".csv")
    n = 0
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("r,g,b\n")
        for _ in range(TANDAS):
            # cada tanda cambia un poco la luz y el ángulo: desplaza la media
            base = [max(0.02, m + rng.gauss(0, 0.025)) for m in media]
            for _ in range(MUESTRAS_POR_TANDA):
                v = [max(0.01, c + rng.gauss(0, 0.012)) for c in base]
                f.write(",".join(f"{c:.3f}" for c in normalizar(*v)) + "\n")
                n += 1
    print(f"{ruta}: {n} lecturas")


if __name__ == "__main__":
    rng = random.Random(SEMILLA)
    for nombre, media in COLORES.items():
        escribir(nombre, media, rng)
