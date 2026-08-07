#ifndef LED_INTERMITENTE_H
#define LED_INTERMITENTE_H

#include <Arduino.h>

class LedIntermitente {
private:
    uint8_t _pin;
    unsigned long _periodo;
    unsigned long _lastToggleTime;
    bool _state;
    const char* _nombre;

public:
    // Constructor: recibe pin, período en ms y un nombre identificador (ej: "LED-1")
    LedIntermitente(uint8_t pin, unsigned long periodo, const char* nombre = "LED");

    // Inicializa el pin como salida
    void begin();

    // Revisa si transcurrió el período con millis() y conmuta la salida sin bloquear
    void update();
};

#endif // LED_INTERMITENTE_H
