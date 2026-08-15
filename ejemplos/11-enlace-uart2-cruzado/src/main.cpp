#include <Arduino.h>

const uint8_t PIN_RX2 = 16;  // RX del enlace (recibe el TX2 de la otra placa)
const uint8_t PIN_TX2 = 17;  // TX del enlace (va al RX2 de la otra placa)

bool inicioLineaRx = true;   // true cuando el próximo byte de Serial2 empieza una línea nueva

void setup() {
    Serial.begin(115200);                                    // Monitor por USB
    Serial2.begin(115200, SERIAL_8N1, PIN_RX2, PIN_TX2);      // Enlace entre placas
    
    // Mensaje de confirmación al arrancar
    Serial.println("\n--- ENLACE UART INICIADO ---");
    Serial.println("Escribe algo para enviarlo al otro ESP32...");
}

void loop() {
    // Monitor -> enlace: todo lo tecleado en el monitor sale por Serial2
    while (Serial.available() > 0) {
        char c = Serial.read();
        // Hacemos "eco" local para que VEAS lo que estás escribiendo
        Serial.print(c);
        // Enviamos el caracter a la otra placa
        Serial2.write(c);
    }

    // Enlace -> monitor: todo lo que llega de la otra placa se imprime con prefijo
    while (Serial2.available() > 0) {
        char c = Serial2.read();
        if (inicioLineaRx) {
            Serial.print("\n[recibido] ");
            inicioLineaRx = false;
        }
        Serial.write(c);
        if (c == '\n' || c == '\r') {
            inicioLineaRx = true;
        }
    }
}
