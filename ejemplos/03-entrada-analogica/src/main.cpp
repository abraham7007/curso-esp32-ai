#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("Iniciando lectura de ADC (GPIO 32)");
}

void loop() {
    int codigo = analogRead(32);
    float voltios = (float)codigo * 3.3 / 4095.0;
    
    char buffer[100];
    // Alineamos el código a 4 dígitos y la tensión a 3 decimales
    sprintf(buffer, "[ADC1] canal=4  codigo=%4d  v=%.3f", codigo, voltios);
    Serial.println(buffer);
    
    // Muestreo a 10 Hz
    delay(100);
}
