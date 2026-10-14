// Ejemplo 22 - Entrenar en el PC, exportar a C y comprobar en el ESP32
// El modelo se entrenó en el ordenador (entrenamiento/entrenar.py) y llega
// aquí como código C generado por emlearn: include/modelo_gestos.h.
// Este programa NO lee el potenciómetro: toma las ventanas de PRUEBA que
// entrenar.py guardó en include/casos_prueba.h, las clasifica en el chip y
// comprueba que la matriz de confusión es idéntica a la que obtuvo el PC.
// Si coincide, el modelo llegó entero al ESP32; si no, algo cambió por el
// camino (otro .h, otra versión, otro tipo de dato) y hay que mirarlo antes
// de conectarlo a la señal real (ejemplo 23).
//
// El circuito (potenciómetro en GPIO 32, pulsador en GPIO 4) es el mismo de
// toda la sesión, pero este ejemplo no lo usa.

#include <Arduino.h>
#include "modelo_gestos.h"  // generado por emlearn: modelo_gestos_predict()
#include "casos_prueba.h"   // generado por entrenar.py: CASOS_X, CASOS_Y, MATRIZ_PC

// Cuántas veces se repite la clasificación de todos los casos para medir el
// tiempo: una sola inferencia dura menos que la resolución útil de micros().
const int REPETICIONES = 20;

void imprimirMatriz(const uint16_t m[N_CLASES][N_CLASES]) {
    Serial.println("[MATRIZ] filas = real, columnas = prediccion del ESP32");
    Serial.print("            ");
    for (int c = 0; c < N_CLASES; c++) {
        Serial.printf("%8s", NOMBRE_CLASE[c]);
    }
    Serial.println();
    for (int f = 0; f < N_CLASES; f++) {
        Serial.printf("  %-8s  ", NOMBRE_CLASE[f]);
        for (int c = 0; c < N_CLASES; c++) {
            Serial.printf("%8u", m[f][c]);
        }
        Serial.println();
    }
}

void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("[INICIO] Ejemplo 22 - Modelo entrenado en el PC, evaluado en el ESP32");
    Serial.printf("[MODELO] %s: %d nodos de decision, %d hojas\n",
                  MODELO_NOMBRE, MODELO_NODOS_DECISION, MODELO_HOJAS);
    Serial.printf("[PRUEBA] %d ventanas de sesiones que el modelo no vio al entrenar\n", N_CASOS);

    // 1. Clasificar cada caso de prueba y llenar la matriz de confusión
    uint16_t matriz[N_CLASES][N_CLASES] = {};
    int aciertos = 0;
    for (int i = 0; i < N_CASOS; i++) {
        int32_t pred = modelo_gestos_predict(CASOS_X[i], N_CARACTERISTICAS);
        if (pred < 0 || pred >= N_CLASES) {
            Serial.printf("[ERROR] el modelo devolvio %ld en el caso %d\n", (long)pred, i);
            continue;
        }
        matriz[CASOS_Y[i]][pred]++;
        if (pred == CASOS_Y[i]) {
            aciertos++;
        }
    }
    imprimirMatriz(matriz);
    Serial.printf("[EXACTITUD] ESP32 = %.1f %% (%d/%d)   PC = %.1f %%\n",
                  100.0f * aciertos / N_CASOS, aciertos, N_CASOS, 100.0f * EXACTITUD_PC);

    // 2. Comparar celda a celda con la matriz que obtuvo el PC
    int distintas = 0;
    for (int f = 0; f < N_CLASES; f++) {
        for (int c = 0; c < N_CLASES; c++) {
            if (matriz[f][c] != MATRIZ_PC[f][c]) {
                distintas++;
                Serial.printf("[DIFIERE] real=%s prediccion=%s: ESP32=%u PC=%u\n",
                              NOMBRE_CLASE[f], NOMBRE_CLASE[c], matriz[f][c], MATRIZ_PC[f][c]);
            }
        }
    }
    if (distintas == 0) {
        Serial.printf("[COINCIDE] PC=ESP32 (las %d celdas de la matriz son iguales)\n",
                      N_CLASES * N_CLASES);
    }

    // 3. Tiempo de una inferencia: se clasifican todos los casos REPETICIONES
    //    veces y se divide. «volatile» impide que el compilador se salte las
    //    llamadas porque su resultado no se usa.
    volatile int32_t sumidero = 0;
    unsigned long t0 = micros();
    for (int r = 0; r < REPETICIONES; r++) {
        for (int i = 0; i < N_CASOS; i++) {
            sumidero = sumidero + modelo_gestos_predict(CASOS_X[i], N_CARACTERISTICAS);
        }
    }
    unsigned long total = micros() - t0;
    Serial.printf("[TIEMPO] inferencia = %.2f us por ventana (media de %d x %d llamadas)\n",
                  (float)total / (REPETICIONES * N_CASOS), REPETICIONES, N_CASOS);

    // 4. Memoria. El tamaño del modelo en flash no se puede medir desde el
    //    programa; aquí va el tamaño del .h generado y el del programa entero.
    //    (Para el coste exacto en flash: compilar con y sin el modelo y restar.)
    Serial.printf("[MEMORIA] modelo_gestos.h = %ld bytes de texto C, programa = %lu bytes en flash\n",
                  MODELO_BYTES_H, (unsigned long)ESP.getSketchSize());
    Serial.printf("[MEMORIA] heap libre = %lu bytes (minimo desde el arranque = %lu)\n",
                  (unsigned long)ESP.getFreeHeap(), (unsigned long)ESP.getMinFreeHeap());
    Serial.println("[FIN] Prueba terminada. Pulsa RESET para repetirla.");
}

void loop() {
    // Nada que hacer: la prueba se ejecuta una sola vez en setup()
}
