#include <Arduino.h>
#include <Wire.h>

const uint8_t PIN_SDA = 21;
const uint8_t PIN_SCL = 22;

void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("Iniciando escaneo del bus I2C (SDA=21, SCL=22)");

    Wire.begin(PIN_SDA, PIN_SCL);
}

void loop() {
    uint8_t encontrados = 0;

    // Recorre todas las direcciones de 7 bits válidas para periféricos (0x08 - 0x77)
    for (uint8_t direccion = 0x08; direccion <= 0x77; direccion++) {
        Wire.beginTransmission(direccion);
        uint8_t error = Wire.endTransmission();

        if (error == 0) {
            char buffer[40];
            snprintf(buffer, sizeof(buffer), "[I2C] dispositivo en 0x%02X", direccion);
            Serial.println(buffer);
            encontrados++;
        }
    }

    char resumen[40];
    snprintf(resumen, sizeof(resumen), "[I2C] %d dispositivos encontrados", encontrados);
    Serial.println(resumen);

    delay(5000);  // Repite el escaneo cada 5 s
}
