#ifndef BOTON_H
#define BOTON_H

#include <Arduino.h>

class Boton {
private:
    uint8_t _pin;
    bool _state;                // Estado estable filtrado (true = PRESIONADO / LOW)
    bool _lastRawState;         // Último estado crudo leído del pin
    bool _pressedFlag;          // Flag de evento de pulsación detectada
    unsigned long _lastDebounceTime; // Tiempo de la última transición cruda
    static const unsigned long DEBOUNCE_DELAY = 30; // Ventana antirrebote de 30 ms

public:
    // Constructor: recibe el número de pin del GPIO
    explicit Boton(uint8_t pin);

    // Inicializa el pin como INPUT_PULLUP
    void begin();

    // Actualiza el estado del botón sin bloqueos (usando millis)
    void update();

    // Devuelve true una sola vez por cada pulsación detectada
    bool fuePulsado();
};

#endif // BOTON_H
