// Ejemplo 20 · Entorno «inferencia» - Clasificar gestos con TensorFlow Lite Micro
// La Nano 33 BLE Sense Rev2 espera un movimiento brusco, graba 119 muestras del IMU
// (igual que el entorno «captura»), las normaliza igual que el cuaderno de Colab y
// se las pasa a la red de include/model.h (714 -> 50 -> 15 -> 2, float32).
// El LED RGB muestra la respuesta: punch = rojo, flex = azul, dudoso = amarillo.
//
// Basado en el ejemplo ArduinoNano33BLE_GestureClassifier de la librería ArduTFLite
// (Spazio Chirale, licencia Apache 2.0: https://github.com/spaziochirale/ArduTFLite),
// que a su vez actualiza el IMU_Classifier del tutorial oficial de Arduino
// (Don Coleman, Sandeep Mistry, Dominic Pajak, 2019). El sketch original se publica
// como «public domain». Cambios: comentarios en español, LED RGB, umbral de confianza,
// medición de tiempos y trazas por el puerto serie.
//
// Rev1 (IMU LSM9DS1): cambia el #include por <Arduino_LSM9DS1.h> y la librería en
// platformio.ini por arduino-libraries/Arduino_LSM9DS1.

#include <Arduino.h>
#include <Arduino_BMI270_BMM150.h>   // IMU de la Rev2
#include <ArduTFLite.h>              // envoltorio sencillo de TensorFlow Lite Micro (Chirale)
// Modelo entrenado en Colab (entrenamiento/). Si vuelves a entrenar, reemplaza
// include/model.h y vuelve a compilar: el resto del programa no cambia.
#include "model.h"

// --- Captura: los MISMOS valores que en el entorno «captura» ---
const float UMBRAL_ACELERACION = 2.5;   // g
const int N_MUESTRAS = 119;
const int N_ENTRADAS = N_MUESTRAS * 6;  // 714 números de entrada

// Por debajo de esta probabilidad no nos fiamos de la respuesta
const float UMBRAL_CONFIANZA = 0.80;

// --- Memoria de trabajo de TensorFlow Lite Micro (tensor arena) ---
// Aquí viven la entrada, la salida y los resultados intermedios de la red.
// Su tamaño se ajusta probando; 8 KB sobran para esta red (la entrada son 714 x 4 B).
// alignas(16): alineada a 16 bytes, como pide la librería en Cortex-M.
constexpr int TAM_ARENA = 8 * 1024;
alignas(16) byte tensorArena[TAM_ARENA];

// Mismo orden que la lista GESTURES del cuaderno
const char* const GESTOS[] = {"punch", "flex"};
const int N_GESTOS = sizeof(GESTOS) / sizeof(GESTOS[0]);

int numeroGesto = 0;

// LED RGB integrado: cada color se enciende con LOW (activo en bajo)
void ledRGB(bool rojo, bool verde, bool azul) {
  digitalWrite(LEDR, rojo ? LOW : HIGH);
  digitalWrite(LEDG, verde ? LOW : HIGH);
  digitalWrite(LEDB, azul ? LOW : HIGH);
}

void setup() {
  Serial.begin(115200);
  // USB nativo: espera al monitor serie como mucho 5 s; sin PC, sigue igual
  // (los LED funcionan con la placa alimentada por batería).
  unsigned long t0 = millis();
  while (!Serial && millis() - t0 < 5000);

  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  ledRGB(false, false, false);

  Serial.println("[INICIO] Ejemplo 20 - clasificador de gestos (TensorFlow Lite Micro)");

  if (!IMU.begin()) {
    Serial.println("[ERROR] No se pudo iniciar el IMU (BMI270). Se detiene el programa.");
    ledRGB(true, false, false);
    while (true);
  }
  Serial.print("[IMU] acelerometro ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.print(" Hz, giroscopio ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");

  Serial.print("[MODELO] model.h: ");
  Serial.print(sizeof(model));
  Serial.print(" bytes en flash, arena de ");
  Serial.print(TAM_ARENA);
  Serial.println(" bytes en RAM");
  if (!modelInit(model, tensorArena, TAM_ARENA)) {
    Serial.println("[ERROR] modelInit fallo: model.h no es un modelo TFLite valido.");
    ledRGB(true, false, false);
    while (true);
  }
  Serial.println("[MODELO] listo. Haz un gesto (punch o flex) con la placa en la mano.");
}

void loop() {
  float aX, aY, aZ, gX, gY, gZ;

  // 1) Esperar un movimiento significativo (igual que la captura)
  while (true) {
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(aX, aY, aZ);
      if (fabs(aX) + fabs(aY) + fabs(aZ) >= UMBRAL_ACELERACION) break;
    }
  }

  // 2) Leer 119 muestras y colocarlas en el tensor de entrada
  unsigned long inicioCaptura = millis();
  int leidas = 0;
  while (leidas < N_MUESTRAS) {
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      IMU.readAcceleration(aX, aY, aZ);
      IMU.readGyroscope(gX, gY, gZ);

      // Normalizar a 0..1 EXACTAMENTE como en el cuaderno:
      // aceleración -4..+4 g, giro -2000..+2000 grados/s
      modelSetInput((aX + 4.0) / 8.0, leidas * 6 + 0);
      modelSetInput((aY + 4.0) / 8.0, leidas * 6 + 1);
      modelSetInput((aZ + 4.0) / 8.0, leidas * 6 + 2);
      modelSetInput((gX + 2000.0) / 4000.0, leidas * 6 + 3);
      modelSetInput((gY + 2000.0) / 4000.0, leidas * 6 + 4);
      modelSetInput((gZ + 2000.0) / 4000.0, leidas * 6 + 5);
      leidas++;
    }
  }
  unsigned long msCaptura = millis() - inicioCaptura;

  // 3) Inferencia: la red calcula una probabilidad por gesto
  unsigned long t = micros();
  if (!modelRunInference()) {
    Serial.println("[ERROR] Fallo la inferencia (Invoke).");
    return;
  }
  unsigned long usInferencia = micros() - t;

  // 4) Resultado por el puerto serie y en el LED
  numeroGesto++;
  Serial.print("[GESTO ");
  Serial.print(numeroGesto);
  Serial.print("] ");
  Serial.print(N_MUESTRAS);
  Serial.print(" muestras en ");
  Serial.print(msCaptura);
  Serial.print(" ms, inferencia en ");
  Serial.print(usInferencia);
  Serial.println(" us");

  int mejor = 0;
  float probMejor = -1;
  for (int i = 0; i < N_GESTOS; i++) {
    float p = modelGetOutput(i);
    Serial.print("  ");
    Serial.print(GESTOS[i]);
    Serial.print(": ");
    Serial.print(p * 100, 2);
    Serial.println(" %");
    if (p > probMejor) {
      probMejor = p;
      mejor = i;
    }
  }

  if (probMejor < UMBRAL_CONFIANZA) {
    Serial.print("  -> dudoso: maximo ");
    Serial.print(probMejor * 100, 2);
    Serial.println(" % < 80 % (LED amarillo)");
    ledRGB(true, true, false);
  } else if (mejor == 0) {
    Serial.println("  -> punch (LED rojo)");
    ledRGB(true, false, false);
  } else {
    Serial.println("  -> flex (LED azul)");
    ledRGB(false, false, true);
  }
  Serial.println();
}
