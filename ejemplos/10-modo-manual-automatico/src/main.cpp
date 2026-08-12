#include <Arduino.h>
#include "Led.h"
#include "Boton.h"
#include "EntradaAnalogica.h"

Led led(2);
Boton boton(4);
EntradaAnalogica entrada(32, 16);
bool automatico = false;
uint8_t dutyPrevio = 0;

void setup() {
    Serial.begin(115200);
    led.begin();
    boton.begin();
    Serial.println("[MODO] MANUAL");
}

void loop() {
    boton.update();
    entrada.update();

    if (boton.fuePulsado()) {
        automatico = !automatico;
        Serial.println(automatico ? "[MODO] AUTOMATICO" : "[MODO] MANUAL");
    }

    if (automatico) {
        float voltios = entrada.leerVoltios();
        uint8_t duty = (uint8_t)((voltios / 3.3f) * 255.0f);
        led.escribirPWM(duty);

        if (duty != dutyPrevio) {
            Serial.print("[AUTO] adc=");
            Serial.print(voltios, 3);
            Serial.print("V pwm=");
            Serial.println(duty);
            dutyPrevio = duty;
        }
    }
}
