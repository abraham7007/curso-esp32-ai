#include <Arduino.h>

void setup() {
    pinMode(4, INPUT_PULLUP); // cambiar a INPUT para desactivar la pull-up interna
    Serial.begin(115200);
}

void loop() {
    int nivel = digitalRead(4);
    Serial.print("[GPIO4] nivel=");
    Serial.println(nivel);
    delay(200);
}
