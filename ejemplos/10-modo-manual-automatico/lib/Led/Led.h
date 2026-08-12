#ifndef LED_H
#define LED_H

#include <Arduino.h>

class Led {
private:
    uint8_t _pin;
    bool _state;

public:
    // Constructor: recibe el número de pin del GPIO
    explicit Led(uint8_t pin);

    // Inicializa el pin como salida
    void begin();

    // Enciende el LED
    void on();

    // Apaga el LED
    void off();

    // Alterna el estado del LED y retorna el nuevo estado (true=ENCENDIDO, false=APAGADO)
    bool toggle();

    // Consulta si el LED está encendido
    bool isOn() const;

    // Aplica un ciclo de trabajo PWM (0-255) al LED mediante LEDC
    void escribirPWM(uint8_t duty);
};

#endif // LED_H
