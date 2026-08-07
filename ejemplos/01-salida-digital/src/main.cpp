#include <Arduino.h>

void setup() {
    pinMode(2, OUTPUT);  // SALIDA DIGITAL EN GPIO 2
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("Iniciando salida digital en GPIO 2");
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
