// Ejemplo 21 - Captura de datos etiquetados en CSV por el puerto serie
// Mismo muestreo y mismas características que el ejemplo 20 (lib/Ventana),
// pero aquí el ESP32 no decide nada: solo ANOTA. Cada ventana sale como una
// línea CSV con la etiqueta que eliges con el pulsador (GPIO 4):
//
//   sesion,ventana,etiqueta,media,desv,rango,cruces
//   9f3a01c2,1,quieto,2047.3,3.21,12,0
//
// Ese texto, guardado en un archivo, es el conjunto de datos con el que se
// entrena el modelo en el PC (ejemplo 22). Ver README.md: cómo capturarlo.
//
// Todo lo que NO es un dato empieza por «#», para que Python lo ignore
// (pandas.read_csv(..., comment="#")).

#include <Arduino.h>
#include <esp_random.h>
#include "Boton.h"
#include "Ventana.h"

const uint8_t PIN_POT = 32;
const uint8_t PIN_BOTON = 4;

// Cada cuántas ventanas se imprime el balance de clases (20 ventanas = 10 s)
const uint32_t VENTANAS_POR_BALANCE = 20;
// Si la clase con más ventanas tiene más de 3 veces las de la que menos,
// el modelo tenderá a responder siempre la mayoritaria: se avisa.
const float RAZON_MAXIMA = 3.0f;

const uint8_t N_ETIQUETAS = 3;
const char* const ETIQUETA[N_ETIQUETAS] = {"quieto", "giro", "vaiven"};

Ventana ventana(PIN_POT);
Boton boton(PIN_BOTON);
uint8_t etiqueta = 0;
uint32_t cuenta[N_ETIQUETAS] = {};  // ventanas capturadas de cada clase
uint32_t sesion = 0;                // identificador de esta sesión de captura

void imprimirBalance() {
    uint32_t mayor = cuenta[0], menor = cuenta[0];
    uint8_t claseMenor = 0;
    for (uint8_t i = 1; i < N_ETIQUETAS; i++) {
        if (cuenta[i] > mayor) mayor = cuenta[i];
        if (cuenta[i] < menor) { menor = cuenta[i]; claseMenor = i; }
    }
    Serial.printf("#BALANCE quieto=%lu giro=%lu vaiven=%lu",
                  (unsigned long)cuenta[0], (unsigned long)cuenta[1], (unsigned long)cuenta[2]);
    if (menor == 0) {
        // Razón infinita: falta una clase entera
        Serial.printf(" razon=--:1 AVISO: aun no hay ventanas de %s\n", ETIQUETA[claseMenor]);
        return;
    }
    float razon = (float)mayor / menor;
    Serial.printf(" razon=%.1f:1", razon);
    if (razon > RAZON_MAXIMA) {
        Serial.printf(" AVISO: mas de %.0f:1, captura mas %s\n", RAZON_MAXIMA, ETIQUETA[claseMenor]);
    } else {
        Serial.println();
    }
}

void setup() {
    Serial.begin(115200);
    delay(100);
    boton.begin();
    ventana.begin();

    // Un número aleatorio distinto en cada arranque identifica la sesión.
    // Sirve para separar entrenamiento y prueba POR SESIÓN en el PC: las
    // ventanas de una misma sesión se parecen demasiado entre sí.
    // (Sin WiFi activo, esp_random() es pseudoaleatorio, pero distinto en
    // cada arranque: basta para un identificador.)
    sesion = esp_random();

    Serial.println();
    Serial.println("# Ejemplo 21 - Captura CSV etiquetada (50 Hz, ventana 50, salto 25)");
    Serial.printf("# sesion %08lx. Pulsa el boton del GPIO 4 para cambiar de gesto.\n",
                  (unsigned long)sesion);
    Serial.printf("#ETIQUETA %s\n", ETIQUETA[etiqueta]);
    Serial.println("sesion,ventana,etiqueta,media,desv,rango,cruces");  // cabecera del CSV
}

void loop() {
    boton.update();
    ventana.update();

    // Cambio de gesto: se vacía la ventana. Así la primera ventana del gesto
    // nuevo llega 1 s después y no mezcla muestras del gesto anterior
    // (una ventana mezclada sería un dato con la etiqueta equivocada).
    if (boton.fuePulsado()) {
        etiqueta = (etiqueta + 1) % N_ETIQUETAS;
        ventana.reiniciar();
        Serial.printf("#ETIQUETA %s\n", ETIQUETA[etiqueta]);
    }

    if (ventana.hayVentana()) {
        Caracteristicas c;
        ventana.extraer(c);
        cuenta[etiqueta]++;

        // Una línea CSV por ventana. Los decimales importan: el modelo se
        // entrena con estos números tal como salen aquí.
        Serial.printf("%08lx,%lu,%s,%.1f,%.2f,%.0f,%.0f\n",
                      (unsigned long)sesion, (unsigned long)ventana.numero(),
                      ETIQUETA[etiqueta], c.media, c.desv, c.rango, c.cruces);

        if (ventana.numero() % VENTANAS_POR_BALANCE == 0) {
            imprimirBalance();
        }
    }
}
