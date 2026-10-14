#include "Ventana.h"
#include <math.h>

Ventana::Ventana(uint8_t pin)
    : _pin(pin), _indice(0), _llenas(0), _nuevas(0), _lista(false),
      _numero(0), _ultimoMs(0) {
    for (uint8_t i = 0; i < N_MUESTRAS; i++) {
        _buffer[i] = 0;
    }
}

void Ventana::begin() {
    pinMode(_pin, INPUT);
    reiniciar();
    _ultimoMs = millis();
}

void Ventana::update() {
    unsigned long ahora = millis();
    if (ahora - _ultimoMs < PERIODO_MS) {
        return;  // todavía no toca muestrear
    }
    // Sumar el periodo (y no copiar «ahora») mantiene los 50 Hz exactos en
    // promedio aunque una vuelta de loop() llegue unos ms tarde.
    _ultimoMs += PERIODO_MS;
    // Si loop() estuvo bloqueado mucho tiempo (p. ej. conectando al WiFi),
    // no se intenta recuperar las muestras perdidas: se resincroniza.
    if (ahora - _ultimoMs >= PERIODO_MS) {
        _ultimoMs = ahora;
    }

    _buffer[_indice] = analogRead(_pin);  // una única muestra por llamada
    _indice = (_indice + 1) % N_MUESTRAS;
    if (_llenas < N_MUESTRAS) {
        _llenas++;  // la primera ventana todavía se está llenando
    }
    _nuevas++;

    // Ventana completa: búfer lleno y al menos SALTO muestras nuevas
    if (_llenas == N_MUESTRAS && _nuevas >= SALTO) {
        _nuevas = 0;
        _lista = true;
        _numero++;
    }
}

bool Ventana::hayVentana() {
    if (_lista) {
        _lista = false;  // consumir el evento (true una sola vez por ventana)
        return true;
    }
    return false;
}

void Ventana::extraer(Caracteristicas& c) const {
    // Copia en orden cronológico: la muestra más antigua está en _indice
    uint16_t x[N_MUESTRAS];
    for (uint8_t i = 0; i < N_MUESTRAS; i++) {
        x[i] = _buffer[(_indice + i) % N_MUESTRAS];
    }

    // 1) Media y rango
    uint32_t suma = 0;
    uint16_t minimo = x[0], maximo = x[0];
    for (uint8_t i = 0; i < N_MUESTRAS; i++) {
        suma += x[i];
        if (x[i] < minimo) minimo = x[i];
        if (x[i] > maximo) maximo = x[i];
    }
    float media = (float)suma / N_MUESTRAS;

    // 2) Desviación estándar poblacional: raíz del promedio de (x - media)^2
    float acumulado = 0.0f;
    for (uint8_t i = 0; i < N_MUESTRAS; i++) {
        float d = (float)x[i] - media;
        acumulado += d * d;
    }

    // 3) Cruces: cuántas veces la señal cambia de sentido (sube -> baja o
    //    baja -> sube). Para no contar el ruido del ADC, un cambio solo vale
    //    si la señal retrocede al menos BANDA_MUERTA códigos desde el último
    //    extremo (máximo si subía, mínimo si bajaba).
    int sentido = 0;          // 0 = aún sin sentido, +1 = sube, -1 = baja
    int32_t ref = x[0];       // último extremo visto
    uint16_t cruces = 0;
    for (uint8_t i = 1; i < N_MUESTRAS; i++) {
        int32_t v = x[i];
        if (sentido == 0) {
            if (v >= ref + BANDA_MUERTA)      { sentido = +1; ref = v; }
            else if (v <= ref - BANDA_MUERTA) { sentido = -1; ref = v; }
        } else if (sentido == +1) {
            if (v > ref) {
                ref = v;                                   // sigue subiendo: nuevo máximo
            } else if (v <= ref - BANDA_MUERTA) {
                cruces++; sentido = -1; ref = v;           // bajó lo bastante: cambio de sentido
            }
        } else {
            if (v < ref) {
                ref = v;                                   // sigue bajando: nuevo mínimo
            } else if (v >= ref + BANDA_MUERTA) {
                cruces++; sentido = +1; ref = v;           // subió lo bastante: cambio de sentido
            }
        }
    }

    c.media  = media;
    c.desv   = sqrtf(acumulado / N_MUESTRAS);
    c.rango  = (float)(maximo - minimo);
    c.cruces = (float)cruces;
}

void Ventana::reiniciar() {
    _indice = 0;
    _llenas = 0;
    _nuevas = 0;
    _lista = false;
}

uint32_t Ventana::numero() const {
    return _numero;
}
