// Ejemplo 20 - Un umbral fijo sobre la ventana: quieto o movimiento
// El potenciómetro (GPIO 32) se muestrea a 50 Hz. Cada 0,5 s se cierra una
// ventana de 1 s (50 muestras, 50 % de solapamiento) y se resume en cuatro
// características: media, desviación, rango y cruces (lib/Ventana).
// La decisión es una sola regla: si la desviación supera UMBRAL_DESV, hay
// movimiento y se enciende el LED del GPIO 2.
//
// El pulsador (GPIO 4) dice qué gesto estás haciendo DE VERDAD: quieto ->
// giro -> vaiven -> quieto... Con esa etiqueta el programa cuenta aciertos y
// errores en una matriz de confusión 3 x 2. La matriz muestra el límite del
// umbral: separa quieto de movimiento, pero giro y vaiven caen en la misma
// columna. Para distinguirlos hace falta mirar más de una característica
// (los cruces), y eso es lo que aprende el modelo de los ejemplos 21 a 23.

#include <Arduino.h>
#include "Boton.h"
#include "Ventana.h"

const uint8_t PIN_POT = 32;  // potenciómetro (ADC1)
const uint8_t PIN_BOTON = 4; // pulsador a GND, INPUT_PULLUP
const uint8_t PIN_LED = 2;   // LED: encendido = movimiento

// Umbral de la desviación, en códigos del ADC. Con la mano quieta solo queda
// el ruido del ADC: desviaciones pequeñas (casi 0 en Wokwi; en una placa
// real, del orden de 10 códigos, según la placa y el cableado). Al mover la
// perilla suben a decenas o cientos. Prueba a subirlo y bajarlo y mira la matriz.
const float UMBRAL_DESV = 40.0f;

// Cada cuántas ventanas se imprime la matriz (40 ventanas = 20 s)
const uint32_t VENTANAS_POR_MATRIZ = 40;

const uint8_t N_ETIQUETAS = 3;
const char* const ETIQUETA[N_ETIQUETAS] = {"quieto", "giro", "vaiven"};
const char* const DECISION[2] = {"quieto", "movimiento"};

Ventana ventana(PIN_POT);
Boton boton(PIN_BOTON);
uint8_t etiqueta = 0;                     // gesto real, lo elige el pulsador
uint32_t matriz[N_ETIQUETAS][2] = {};     // filas = real, columnas = decisión

void imprimirMatriz() {
    Serial.printf("[MATRIZ] tras %lu ventanas (filas = real con el pulsador, columnas = decision)\n",
                  (unsigned long)ventana.numero());
    Serial.println("              quieto  movimiento");
    for (uint8_t f = 0; f < N_ETIQUETAS; f++) {
        Serial.printf("  %-8s  %8lu  %10lu\n", ETIQUETA[f],
                      (unsigned long)matriz[f][0], (unsigned long)matriz[f][1]);
    }
}

void setup() {
    Serial.begin(115200);
    delay(100);
    pinMode(PIN_LED, OUTPUT);
    digitalWrite(PIN_LED, LOW);
    boton.begin();
    ventana.begin();

    Serial.println();
    Serial.println("[INICIO] Ejemplo 20 - Umbral fijo sobre la ventana");
    Serial.println("[VENTANA] 50 Hz, 50 muestras (1 s), salto 25 (50 % de solapamiento)");
    Serial.printf("[UMBRAL] desv > %.1f -> movimiento\n", UMBRAL_DESV);
    Serial.printf("[ETIQUETA] real=%s (pulsa el boton del GPIO 4 para cambiarla)\n", ETIQUETA[etiqueta]);
}

void loop() {
    boton.update();
    ventana.update();  // toma una muestra cada 20 ms, sin bloquear

    // Pulsador: siguiente gesto real. Se vacía la ventana para que ninguna
    // ventana mezcle el gesto anterior con el nuevo.
    if (boton.fuePulsado()) {
        etiqueta = (etiqueta + 1) % N_ETIQUETAS;
        ventana.reiniciar();
        Serial.printf("[ETIQUETA] real=%s\n", ETIQUETA[etiqueta]);
    }

    if (ventana.hayVentana()) {
        Caracteristicas c;
        ventana.extraer(c);

        // La regla entera: una comparación
        uint8_t decision = (c.desv > UMBRAL_DESV) ? 1 : 0;
        digitalWrite(PIN_LED, decision ? HIGH : LOW);
        matriz[etiqueta][decision]++;

        Serial.printf("[V %03lu] media=%.1f desv=%.2f rango=%.0f cruces=%.0f -> %s real=%s\n",
                      (unsigned long)ventana.numero(), c.media, c.desv, c.rango, c.cruces,
                      DECISION[decision], ETIQUETA[etiqueta]);

        if (ventana.numero() % VENTANAS_POR_MATRIZ == 0) {
            imprimirMatriz();
        }
    }
}
