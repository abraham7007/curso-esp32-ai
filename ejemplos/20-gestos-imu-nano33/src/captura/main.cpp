// Ejemplo 20 · Entorno «captura» - Grabar gestos con el IMU de la Nano 33 BLE Sense Rev2
// Espera un movimiento brusco (más de 2,5 g sumando los tres ejes) y entonces
// imprime 119 muestras (≈ 1,2 s a 100 Hz) de aceleración y giro en CSV:
//     aX,aY,aZ,gX,gY,gZ
// con una línea vacía al final de cada gesto. Ese texto, copiado a punch.csv o
// flex.csv, es lo que lee el cuaderno de Colab (entrenamiento/).
//
// Adaptación del sketch IMU_Capture del tutorial oficial de Arduino
// (Don Coleman, Sandeep Mistry, Dominic Pajak; «This example code is in the public
// domain»): https://github.com/arduino/ArduinoTensorFlowLiteTutorials
// Cambios: librería del IMU de la Rev2 (BMI270 + BMM150), 115200 baudios y el LED
// naranja encendido mientras se graba un gesto. El formato CSV es el mismo.
//
// Rev1 (IMU LSM9DS1): cambia el #include por <Arduino_LSM9DS1.h> y la librería en
// platformio.ini por arduino-libraries/Arduino_LSM9DS1. El resto no cambia.

#include <Arduino.h>
#include <Arduino_BMI270_BMM150.h>   // IMU de la Rev2: BMI270 (acel. + giro) y BMM150 (brújula)

// Umbral para decidir que empieza un gesto, en g (gravedad = 1 g).
// En reposo |aX| + |aY| + |aZ| vale alrededor de 1; un golpe seco pasa de 2,5.
const float UMBRAL_ACELERACION = 2.5;
const int N_MUESTRAS = 119;          // muestras por gesto (las mismas que espera el modelo)

int muestrasLeidas = N_MUESTRAS;     // N_MUESTRAS = «no hay gesto en curso»

void setup() {
  Serial.begin(115200);
  // La Nano 33 BLE tiene USB nativo: espera a que abras el monitor serie para
  // no perder la cabecera del CSV.
  while (!Serial);

  pinMode(LED_BUILTIN, OUTPUT);      // LED naranja: encendido mientras graba

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Cabecera del CSV (los nombres de columna que usa el cuaderno)
  Serial.println("aX,aY,aZ,gX,gY,gZ");
}

void loop() {
  float aX, aY, aZ, gX, gY, gZ;

  // 1) Esperar un movimiento significativo
  while (muestrasLeidas == N_MUESTRAS) {
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(aX, aY, aZ);   // en g, rango ±4 g en la Rev2

      float aSuma = fabs(aX) + fabs(aY) + fabs(aZ);
      if (aSuma >= UMBRAL_ACELERACION) {
        muestrasLeidas = 0;               // empieza un gesto
        digitalWrite(LED_BUILTIN, HIGH);
        break;
      }
    }
  }

  // 2) Leer las 119 muestras del gesto (acelerómetro y giroscopio a la vez)
  while (muestrasLeidas < N_MUESTRAS) {
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      IMU.readAcceleration(aX, aY, aZ);   // g
      IMU.readGyroscope(gX, gY, gZ);      // grados/s, rango ±2000 en la Rev2

      muestrasLeidas++;

      // Una línea CSV con 3 decimales
      Serial.print(aX, 3);
      Serial.print(',');
      Serial.print(aY, 3);
      Serial.print(',');
      Serial.print(aZ, 3);
      Serial.print(',');
      Serial.print(gX, 3);
      Serial.print(',');
      Serial.print(gY, 3);
      Serial.print(',');
      Serial.print(gZ, 3);
      Serial.println();

      if (muestrasLeidas == N_MUESTRAS) {
        Serial.println();                 // línea vacía: separa un gesto del siguiente
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}
