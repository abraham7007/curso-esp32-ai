#include <Arduino.h>
#include "LedIntermitente.h"

// Instanciación de los tres objetos en GPIO 2, 4 y 5 con sus respectivos períodos
LedIntermitente led1(2, 500, "LED-1");   // GPIO 2 -> 500 ms
LedIntermitente led2(4, 800, "LED-2");   // GPIO 4 -> 800 ms
LedIntermitente led3(5, 1300, "LED-3");  // GPIO 5 -> 1300 ms

void setup() {
    Serial.begin(115200);
    delay(100);

    // Inicialización de cada LED
    led1.begin();
    led2.begin();
    led3.begin();

    Serial.println();
    Serial.println("Iniciando control multitarea no bloqueante para 3 LEDs intermitentes");
}

void loop() {
    // Llamadas seguidas a update() sin ningún delay()
    led1.update();
    led2.update();
    led3.update();
}
