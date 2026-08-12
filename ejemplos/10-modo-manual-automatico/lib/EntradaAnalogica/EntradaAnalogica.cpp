#include "EntradaAnalogica.h"

EntradaAnalogica::EntradaAnalogica(uint8_t pin, uint8_t n)
    : _pin(pin), _n(n), _indice(0), _cuenta(0), _suma(0), _crudo(0), _promedio(0) {
    _buffer = new uint16_t[_n];
    for (uint8_t i = 0; i < _n; i++) {
        _buffer[i] = 0;
    }
}

EntradaAnalogica::~EntradaAnalogica() {
    delete[] _buffer;
}

void EntradaAnalogica::update() {
    uint16_t muestra = analogRead(_pin);  // Una única muestra por llamada

    // Retiramos de la suma la muestra que sale de la ventana
    _suma -= _buffer[_indice];
    // Insertamos la muestra nueva en su lugar
    _buffer[_indice] = muestra;
    _suma += muestra;

    // Avanzamos el índice circular
    _indice = (_indice + 1) % _n;
    if (_cuenta < _n) {
        _cuenta++;  // La ventana todavía se está llenando
    }

    _crudo = muestra;
    _promedio = (uint16_t)(_suma / _cuenta);
}

uint16_t EntradaAnalogica::leerCrudo() {
    return _crudo;
}

float EntradaAnalogica::leerVoltios() {
    return (float)_promedio * 3.3f / 4095.0f;
}
