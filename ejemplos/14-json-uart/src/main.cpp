#include <Arduino.h>
#include <ArduinoJson.h>

void setup() {
    Serial.begin(115200);
    Serial.println("\n--- GENERADOR DE JSON INICIADO ---");
}

void loop() {
    // 1. Crear el documento JSON con memoria estática
    StaticJsonDocument<200> doc;
    
    // 2. Simular lectura de sensores con datos aleatorios
    float temp_simulada = 20.0 + random(0, 100) / 10.0;     // Entre 20.0 y 30.0
    int hum_simulada = random(40, 80);                      // Entre 40 y 80
    float presion_simulada = 1010.0 + random(0, 50) / 10.0; // Entre 1010.0 y 1015.0
    
    // 3. Asignar los valores al documento
    doc["temp"] = temp_simulada;
    doc["hum"] = hum_simulada;
    doc["presion"] = presion_simulada;
    doc["tiempo_ms"] = millis();
    
    // 4. Serializar (convertir el documento a texto JSON) e imprimir en el monitor
    Serial.print("Generando JSON: ");
    serializeJson(doc, Serial);
    Serial.println(); // Añadir un salto de línea al final
    
    // Esperar 3 segundos antes de generar el siguiente
    delay(3000);
}
