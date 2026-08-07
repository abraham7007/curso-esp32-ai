#include <Arduino.h>
#include "Led.h"

// Instancia de la clase Led asignada al GPIO 2
Led led(2);

void setup() {
    Serial.begin(115200);
    delay(100);

    // Inicializa el pin a través del método encapsulado begin()
    led.begin();

    Serial.println();
    Serial.println("Iniciando control de LED mediante Clase Encapsulada");
}

void loop() {
    // Alterna el estado del LED utilizando la clase
    bool estado = led.toggle();

    // Emite por el puerto serie el formato exacto requerido
    Serial.print("[LED] estado=");
    Serial.println(estado ? "ENCENDIDO" : "APAGADO");

    delay(2000);
}
