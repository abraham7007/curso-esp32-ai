#include <Arduino.h>
#include <math.h>
#include "EntradaAnalogica.h"

const uint8_t PIN_ADC   = 32;  // GPIO32 para la lectura del potenciómetro
const uint8_t VENTANA_N = 16;  // Tamaño de la ventana de la media móvil

EntradaAnalogica entrada(PIN_ADC, VENTANA_N);

void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("Iniciando media movil de ADC (N=16, GPIO 32)");
}

void loop() {
    // Una única muestra por vuelta de loop(); la clase mantiene la ventana internamente
    entrada.update();

    uint16_t crudo   = entrada.leerCrudo();
    float    voltios = entrada.leerVoltios();

    // El promedio en código ADC se recupera del voltaje ya filtrado (mismo
    // escalado 3.3V/4095 que usa la clase), para mostrarlo junto al crudo.
    uint16_t promedio = (uint16_t)roundf(voltios * 4095.0f / 3.3f);

    char buffer[80];
    snprintf(buffer, sizeof(buffer), "[ADC] crudo=%4d promedio=%4d v=%.3f",
             crudo, promedio, voltios);
    Serial.println(buffer);

    // Muestreo a 10 Hz
    delay(100);
}
