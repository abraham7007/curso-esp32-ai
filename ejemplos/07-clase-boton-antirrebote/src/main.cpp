#include <Arduino.h>
#include "Boton.h"

// Instancia de la clase Boton asignada al GPIO 4
Boton boton(4);

void setup() {
    Serial.begin(115200);
    delay(100);

    // Inicializa el pin GPIO 4 como INPUT_PULLUP
    boton.begin();

    Serial.println();
    Serial.println("Iniciando detección de pulsaciones con filtrado antirrebote (30 ms)");
}

void loop() {
    static uint32_t contadorPulsaciones = 0;

    // Actualiza la máquina de estados y ventana antirrebote (sin bloqueos)
    boton.update();

    // Evalúa si se produjo un evento de pulsación
    if (boton.fuePulsado()) {
        contadorPulsaciones++;
        unsigned long t_ms = millis();

        // Formato exacto requerido: «[BOTON] pulsacion #N t=NNNN ms»
        char buffer[80];
        snprintf(buffer, sizeof(buffer), "[BOTON] pulsacion #%" PRIu32 " t=%lu ms", 
                 contadorPulsaciones, t_ms);
        Serial.println(buffer);
    }
}
