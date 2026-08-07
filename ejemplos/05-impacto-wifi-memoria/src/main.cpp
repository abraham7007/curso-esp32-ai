#include <Arduino.h>

// =============================================================
// DESCOMENTAR LAS SIGUIENTES LÍNEAS PARA LA VERSIÓN CON WIFI
// =============================================================
#include <WiFi.h>
const char* ssid = "Wokwi-GUEST";
const char* password = "";

void setup() {
    pinMode(2, OUTPUT);
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("Iniciando salida digital en GPIO 2");

    // =============================================================
    // DESCOMENTAR LA SIGUIENTE LÍNEA PARA LA VERSIÓN CON WIFI
    // =============================================================
    WiFi.begin(ssid, password);
}

void loop() {
    static unsigned long segundos = 0;

    digitalWrite(2, HIGH);
    Serial.print("t = ");
    Serial.print(segundos);
    Serial.println(" s   GPIO2 = ALTO");
    delay(2000);
    segundos += 2;

    digitalWrite(2, LOW);
    Serial.print("t = ");
    Serial.print(segundos);
    Serial.println(" s   GPIO2 = BAJO");
    delay(2000);
    segundos += 2;
}
