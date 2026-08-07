#ifndef ENTRADAANALOGICA_H
#define ENTRADAANALOGICA_H

#include <Arduino.h>

class EntradaAnalogica {
private:
    uint8_t _pin;
    uint8_t _n;          // Tamaño de la ventana de la media móvil
    uint16_t* _buffer;   // Buffer circular con las últimas N muestras
    uint8_t _indice;     // Próxima posición del buffer a sobreescribir
    uint8_t _cuenta;     // Muestras acumuladas hasta ahora (satura en _n)
    uint32_t _suma;      // Suma corriente del contenido del buffer
    uint16_t _crudo;     // Última muestra cruda leída
    uint16_t _promedio;  // Media móvil vigente (en código del ADC)

public:
    // Constructor: recibe el pin del ADC y el tamaño N de la ventana
    EntradaAnalogica(uint8_t pin, uint8_t n);
    ~EntradaAnalogica();

    // Toma una única muestra por llamada y actualiza la media móvil.
    // No debe muestrear en bucle dentro de sí misma.
    void update();

    // Última muestra cruda: el código del conversor (0 - 4095)
    uint16_t leerCrudo();

    // Magnitud convertida a partir de la media móvil (0.000 - 3.300 V)
    float leerVoltios();
};

#endif // ENTRADAANALOGICA_H
