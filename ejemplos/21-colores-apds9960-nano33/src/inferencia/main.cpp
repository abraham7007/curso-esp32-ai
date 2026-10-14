// Ejemplo 21 · Entorno «inferencia» - Clasificar colores con un modelo CUANTIZADO int8
// Al acercar un objeto al APDS9960, la placa normaliza su color (r, g, b), lo
// CUANTIZA a int8 con la escala y el punto cero que trae el propio modelo, ejecuta
// la red de include/model.h (3 -> 8 -> 3) y DESCUANTIZA las probabilidades.
// El LED RGB se enciende del color detectado; si la red duda, se queda apagado.
//
// Aquí no se usa ArduTFLite (su API solo maneja tensores float): se usa
// directamente el intérprete de Chirale_TensorFLowLite (TensorFlow Lite Micro para
// Arduino, Apache 2.0: https://github.com/spaziochirale/Chirale_TensorFlowLite),
// con la misma cuantización que su ejemplo hello_world.
// Idea y flujo: sketch object_color_classify del tutorial FruitToEmoji de Arduino
// («public domain»), reescrito para el modelo int8.

#include <Arduino.h>
#include <Arduino_APDS9960.h>
#include <Chirale_TensorFlowLite.h>
#include <tensorflow/lite/micro/micro_mutable_op_resolver.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
// Modelo int8 entrenado en Colab (entrenamiento/). Si vuelves a entrenar,
// reemplaza include/model.h y vuelve a compilar.
#include "model.h"

// Mismo orden que la lista CLASSES del cuaderno
const char* const CLASES[] = {"rojo", "verde", "azul"};
const int N_CLASES = sizeof(CLASES) / sizeof(CLASES[0]);
const float UMBRAL_CONFIANZA = 0.80;

// --- TensorFlow Lite Micro ---
// Solo se registran las 2 operaciones que usa la red (las imprime el cuaderno:
// FULLY_CONNECTED y SOFTMAX). Ocupa menos flash que registrar todas (AllOpsResolver).
tflite::MicroMutableOpResolver<2> resolver;
const tflite::Model* modelo = nullptr;
tflite::MicroInterpreter* interprete = nullptr;
TfLiteTensor* entrada = nullptr;
TfLiteTensor* salida = nullptr;

// Memoria de trabajo de la red. setup() imprime cuánto usa de verdad.
constexpr int TAM_ARENA = 4 * 1024;
alignas(16) uint8_t tensorArena[TAM_ARENA];

int numeroObjeto = 0;

// LED RGB integrado: cada color se enciende con LOW (activo en bajo)
void ledRGB(bool rojo, bool verde, bool azul) {
  digitalWrite(LEDR, rojo ? LOW : HIGH);
  digitalWrite(LEDG, verde ? LOW : HIGH);
  digitalWrite(LEDB, azul ? LOW : HIGH);
}

void detener(const char* mensaje) {
  Serial.println(mensaje);
  while (true) {                 // parpadeo rojo: algo falló al arrancar
    ledRGB(true, false, false);
    delay(200);
    ledRGB(false, false, false);
    delay(200);
  }
}

// real -> int8:  q = real / scale + zero_point, limitado a -128..127
int8_t cuantizar(float x) {
  int32_t q = lroundf(x / entrada->params.scale) + entrada->params.zero_point;
  if (q < -128) q = -128;
  if (q > 127) q = 127;
  return (int8_t)q;
}

// int8 -> real:  real = (q - zero_point) * scale
float descuantizar(int8_t q) {
  return (q - salida->params.zero_point) * salida->params.scale;
}

void imprimirTensor(const char* nombre, TfLiteTensor* t) {
  Serial.print("[MODELO] ");
  Serial.print(nombre);
  Serial.print(t->type == kTfLiteInt8 ? " int8" : " NO int8");
  Serial.print(" scale=");
  Serial.print(t->params.scale, 6);
  Serial.print(" zero_point=");
  Serial.println(t->params.zero_point);
}

void setup() {
  Serial.begin(115200);
  unsigned long t0 = millis();
  while (!Serial && millis() - t0 < 5000);   // espera al monitor como mucho 5 s

  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  ledRGB(false, false, false);

  Serial.println("[INICIO] Ejemplo 21 - clasificador de colores int8 (TensorFlow Lite Micro)");

  if (!APDS.begin()) detener("[ERROR] No se pudo iniciar el APDS9960.");

  // 1) Mapear el modelo (no copia nada: lo lee directamente de la flash)
  modelo = tflite::GetModel(model);
  if (modelo->version() != TFLITE_SCHEMA_VERSION) detener("[ERROR] Version de esquema TFLite distinta.");

  // 2) Registrar las operaciones y crear el intérprete
  resolver.AddFullyConnected();
  resolver.AddSoftmax();
  static tflite::MicroInterpreter interpreteEstatico(modelo, resolver, tensorArena, TAM_ARENA);
  interprete = &interpreteEstatico;

  // 3) Reservar los tensores dentro de la arena
  if (interprete->AllocateTensors() != kTfLiteOk) detener("[ERROR] AllocateTensors fallo: sube TAM_ARENA.");
  entrada = interprete->input(0);
  salida = interprete->output(0);

  Serial.print("[MODELO] model.h: ");
  Serial.print(sizeof(model));
  Serial.print(" bytes en flash, arena usada ");
  Serial.print(interprete->arena_used_bytes());
  Serial.print(" de ");
  Serial.print(TAM_ARENA);
  Serial.println(" bytes");
  imprimirTensor("entrada", entrada);
  imprimirTensor("salida ", salida);
  if (entrada->type != kTfLiteInt8 || salida->type != kTfLiteInt8) {
    detener("[ERROR] El modelo no es int8: copia el model.h del cuaderno de este ejemplo.");
  }
  Serial.println("[MODELO] listo. Acerca un objeto rojo, verde o azul hasta casi tocar el sensor.");
}

void loop() {
  int r, g, b, c, p;

  while (!APDS.colorAvailable() || !APDS.proximityAvailable()) {}
  APDS.readColor(r, g, b, c);
  p = APDS.readProximity();
  float suma = r + g + b;

  // Igual que la captura: objeto pegado y bien iluminado
  if (p != 0 || c <= 10 || suma <= 0) return;

  float rojo = r / suma, verde = g / suma, azul = b / suma;

  // 1) Cuantizar la entrada
  entrada->data.int8[0] = cuantizar(rojo);
  entrada->data.int8[1] = cuantizar(verde);
  entrada->data.int8[2] = cuantizar(azul);

  // 2) Inferencia
  unsigned long t = micros();
  if (interprete->Invoke() != kTfLiteOk) {
    Serial.println("[ERROR] Fallo la inferencia (Invoke).");
    return;
  }
  unsigned long usInferencia = micros() - t;

  // 3) Resultado
  numeroObjeto++;
  Serial.print("[OBJETO ");
  Serial.print(numeroObjeto);
  Serial.print("] r=");
  Serial.print(rojo, 3);
  Serial.print(" g=");
  Serial.print(verde, 3);
  Serial.print(" b=");
  Serial.print(azul, 3);
  Serial.print(" -> int8 [");
  Serial.print(entrada->data.int8[0]);
  Serial.print(", ");
  Serial.print(entrada->data.int8[1]);
  Serial.print(", ");
  Serial.print(entrada->data.int8[2]);
  Serial.print("], inferencia en ");
  Serial.print(usInferencia);
  Serial.println(" us");

  int mejor = 0;
  float probMejor = -1;
  for (int i = 0; i < N_CLASES; i++) {
    float prob = descuantizar(salida->data.int8[i]);
    Serial.print("  ");
    Serial.print(CLASES[i]);
    Serial.print(": ");
    Serial.print(prob * 100, 2);
    Serial.println(" %");
    if (prob > probMejor) {
      probMejor = prob;
      mejor = i;
    }
  }

  if (probMejor < UMBRAL_CONFIANZA) {
    Serial.println("  -> dudoso (LED apagado)");
    ledRGB(false, false, false);
  } else {
    Serial.print("  -> ");
    Serial.print(CLASES[mejor]);
    Serial.print(" (LED ");
    Serial.print(CLASES[mejor]);
    Serial.println(")");
    ledRGB(mejor == 0, mejor == 1, mejor == 2);
  }
  Serial.println();

  // 4) Una sola clasificación por objeto: esperar a que lo retires
  while (!APDS.proximityAvailable() || APDS.readProximity() == 0) {}
  ledRGB(false, false, false);
}
