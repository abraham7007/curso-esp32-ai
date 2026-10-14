#ifndef VENTANA_H
#define VENTANA_H

#include <Arduino.h>

// Las cuatro características con las que se resume una ventana de muestras.
// Todas en códigos del ADC (0 - 4095), salvo «cruces», que es un conteo.
//
// IMPORTANTE: la MISMA definición existe en Python, en
// ejemplos/22-entrenar-exportar/entrenamiento/caracteristicas.py.
// El modelo se entrena con lo que calcula Python y se ejecuta con lo que
// calcula esta clase: si una de las dos cambia (otra banda muerta, otra
// fórmula de la desviación, otro tamaño de ventana) y la otra no, el modelo
// recibe en el chip números que nunca vio y se equivoca sin avisar.
struct Caracteristicas {
    float media;   // promedio de las 50 muestras
    float desv;    // desviación estándar poblacional (divide entre N, no N-1)
    float rango;   // máximo - mínimo
    float cruces;  // cambios de sentido de la señal, con banda muerta
};

class Ventana {
public:
    static const uint32_t PERIODO_MS   = 20;  // 50 Hz: una muestra cada 20 ms
    static const uint8_t  N_MUESTRAS   = 50;  // 50 muestras = 1 s de señal
    static const uint8_t  SALTO        = 25;  // nueva ventana cada 25 muestras (50 % de solapamiento)
    static const uint16_t BANDA_MUERTA = 40;  // códigos que debe retroceder la señal para contar un cambio de sentido

    // Constructor: recibe el pin del ADC (GPIO 32 en todos los ejemplos de la sesión)
    explicit Ventana(uint8_t pin);

    // Configura el pin y deja el búfer vacío
    void begin();

    // Toma UNA muestra si ya pasaron 20 ms desde la anterior (usa millis, no bloquea).
    // Hay que llamarla en cada vuelta de loop().
    void update();

    // true una sola vez por cada ventana completa (la primera tras 50 muestras,
    // las siguientes cada 25 muestras nuevas)
    bool hayVentana();

    // Calcula las cuatro características de la ventana vigente
    void extraer(Caracteristicas& c) const;

    // Vacía el búfer. Se usa al cambiar de etiqueta: así ninguna ventana
    // mezcla muestras de dos gestos distintos.
    void reiniciar();

    // Número de ventanas entregadas desde el arranque (1, 2, 3...)
    uint32_t numero() const;

private:
    uint8_t  _pin;
    uint16_t _buffer[N_MUESTRAS];  // búfer circular con las últimas 50 muestras
    uint8_t  _indice;              // próxima posición a sobrescribir (= la muestra más antigua)
    uint8_t  _llenas;              // muestras válidas en el búfer (satura en 50)
    uint8_t  _nuevas;              // muestras tomadas desde la última ventana entregada
    bool     _lista;               // hay una ventana sin consumir
    uint32_t _numero;              // ventanas entregadas
    unsigned long _ultimoMs;       // instante de la última muestra
};

#endif // VENTANA_H
