#include "Boton.h"

Boton::Boton(uint8_t pin) 
    : _pin(pin), _state(false), _lastRawState(false), 
      _pressedFlag(false), _lastDebounceTime(0) {
}

void Boton::begin() {
    pinMode(_pin, INPUT_PULLUP);
    // Con INPUT_PULLUP: LOW = PRESIONADO (true), HIGH = REPOSO (false)
    bool reading = (digitalRead(_pin) == LOW);
    _state = reading;
    _lastRawState = reading;
    _pressedFlag = false;
    _lastDebounceTime = millis();
}

void Boton::update() {
    // Lectura cruda instantánea (LOW = presionado = true)
    bool reading = (digitalRead(_pin) == LOW);
    unsigned long now = millis();

    // Si hubo un cambio en la lectura cruda respecto al estado previo
    if (reading != _lastRawState) {
        _lastDebounceTime = now; // Reiniciamos el temporizador de la ventana antirrebote
        _lastRawState = reading;
    }

    // Si la lectura se mantiene estable por más tiempo que la ventana de 30 ms
    if ((now - _lastDebounceTime) >= DEBOUNCE_DELAY) {
        // Si el estado estable cambió efectivamente
        if (reading != _state) {
            _state = reading;

            // Flanco de bajada / inicio de pulsación (Transición de Reposo -> Presionado)
            if (_state) {
                _pressedFlag = true;
            }
        }
    }
}

bool Boton::fuePulsado() {
    if (_pressedFlag) {
        _pressedFlag = false; // Consumir el evento (true una sola vez por pulsación)
        return true;
    }
    return false;
}
