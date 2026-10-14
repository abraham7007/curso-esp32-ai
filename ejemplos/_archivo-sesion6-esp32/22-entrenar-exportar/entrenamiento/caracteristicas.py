"""Las cuatro características de una ventana, igual que en el ESP32.

Este archivo es el gemelo en Python de lib/Ventana/Ventana.cpp (ejemplos 20,
21 y 23). Las dos versiones DEBEN calcular lo mismo:

    ventana   50 muestras a 50 Hz (1 s), una ventana nueva cada 25 muestras
              (50 % de solapamiento)
    media     suma / 50
    desv      desviación estándar POBLACIONAL: raíz de la media de (x - media)^2
              (divide entre N, como np.std por defecto; no entre N - 1)
    rango     máximo - mínimo
    cruces    cambios de sentido de la señal; un cambio solo cuenta si la
              señal retrocede al menos BANDA_MUERTA = 40 códigos desde el
              último extremo (máximo si subía, mínimo si bajaba)

Y se redondean como los imprime el ejemplo 21 (media con 1 decimal, desv con
2, rango y cruces enteros), para que los datos sintéticos tengan la misma
resolución que una captura real.

Si cambias algo aquí (la banda muerta, el tamaño de la ventana...), cambia lo
mismo en Ventana.h / Ventana.cpp de los ejemplos 21 y 23, vuelve a capturar
y vuelve a entrenar. Si no, el modelo recibe en el chip números que nunca vio.
"""
import math

N_MUESTRAS = 50      # 1 s a 50 Hz
SALTO = 25           # 50 % de solapamiento
BANDA_MUERTA = 40    # códigos del ADC

NOMBRES = ["media", "desv", "rango", "cruces"]


def contar_cruces(x, banda=BANDA_MUERTA):
    """Cambios de sentido con banda muerta (mismo algoritmo que Ventana.cpp)."""
    sentido = 0          # 0 = aún sin sentido, +1 = sube, -1 = baja
    ref = x[0]           # último extremo visto
    cruces = 0
    for v in x[1:]:
        if sentido == 0:
            if v >= ref + banda:
                sentido, ref = +1, v
            elif v <= ref - banda:
                sentido, ref = -1, v
        elif sentido == +1:
            if v > ref:
                ref = v                              # sigue subiendo: nuevo máximo
            elif v <= ref - banda:
                cruces, sentido, ref = cruces + 1, -1, v
        else:
            if v < ref:
                ref = v                              # sigue bajando: nuevo mínimo
            elif v >= ref + banda:
                cruces, sentido, ref = cruces + 1, +1, v
    return cruces


def extraer(x):
    """x: lista de 50 enteros (códigos del ADC, 0-4095). Devuelve las 4 características."""
    assert len(x) == N_MUESTRAS
    n = len(x)
    media = sum(x) / n
    desv = math.sqrt(sum((v - media) ** 2 for v in x) / n)
    rango = max(x) - min(x)
    return [round(media, 1), round(desv, 2), int(rango), contar_cruces(x)]


def ventanas(senal):
    """Corta una señal larga en ventanas de 50 muestras con salto de 25."""
    for inicio in range(0, len(senal) - N_MUESTRAS + 1, SALTO):
        yield senal[inicio:inicio + N_MUESTRAS]
