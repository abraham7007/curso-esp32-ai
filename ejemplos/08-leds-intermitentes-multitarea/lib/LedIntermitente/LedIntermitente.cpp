#include "LedIntermitente.h"

LedIntermitente::LedIntermitente(uint8_t pin, unsigned long periodo, const char* nombre)
    : _pin(pin), _periodo(periodo), _lastToggleTime(0), _state(false), _nombre(nombre) {
}

void LedIntermitente::begin() {
    pinMode(_pin, OUTPUT);
    digitalWrite(_pin, LOW);
    _state = false;
    _lastToggleTime = millis();
}

void LedIntermitente::update() {
    unsigned long now = millis();

    // Verificamos si ha transcurrido el período (sin bloqueos)
    if (now - _lastToggleTime >= _periodo) {
        _lastToggleTime = now;
        _state = !_state;
        digitalWrite(_pin, _state ? HIGH : LOW);

        // Formato exacto requerido: «t=NNNNN ms [LED-X] gpio=N nivel=N»
        char buffer[100];
        snprintf(buffer, sizeof(buffer), "t=%lu ms [%s] gpio=%u nivel=%u", 
                 now, _nombre, _pin, _state ? 1 : 0);
        Serial.println(buffer);
    }
}
