// Ejemplo 21 · Entorno «captura» - Muestrear el color de un objeto con el APDS9960
// Mientras haya un objeto pegado al sensor (proximidad = 0) y con luz suficiente,
// lee el color y lo imprime NORMALIZADO por la suma, en CSV:
//     r,g,b
//     0.552,0.241,0.207
// Normalizar quita el brillo: un rojo con poca o mucha luz da casi las mismas
// proporciones. Ese texto, copiado a rojo.csv, verde.csv o azul.csv, es lo que lee
// el cuaderno de Colab (entrenamiento/).
//
// Adaptación del sketch object_color_capture del tutorial oficial de Arduino
// FruitToEmoji («This example code is in the public domain»):
// https://github.com/arduino/ArduinoTensorFlowLiteTutorials
// Cambios: 115200 baudios, cabecera r,g,b, se detiene si el sensor no responde y
// el LED naranja se enciende mientras imprime datos.
// El APDS9960 es el mismo en la Rev1 y la Rev2: no hay que cambiar nada.

#include <Arduino.h>
#include <Arduino_APDS9960.h>   // color, proximidad y gestos (sensor junto al LED de encendido)

void setup() {
  Serial.begin(115200);
  while (!Serial);              // USB nativo: espera a que abras el monitor serie

  pinMode(LED_BUILTIN, OUTPUT);

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS9960 sensor.");
    while (true);
  }

  // Cabecera del CSV (los nombres de columna que usa el cuaderno)
  Serial.println("r,g,b");
}

void loop() {
  int r, g, b, c, p;

  // Esperar a que haya lectura nueva de color Y de proximidad
  while (!APDS.colorAvailable() || !APDS.proximityAvailable()) {}

  APDS.readColor(r, g, b, c);   // c = luz total (canal «clear»)
  p = APDS.readProximity();     // 0 = pegado al sensor ... 255 = nada cerca
  float suma = r + g + b;

  // Solo si el objeto está pegado y bien iluminado
  if (p == 0 && c > 10 && suma > 0) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print(r / suma, 3);
    Serial.print(',');
    Serial.print(g / suma, 3);
    Serial.print(',');
    Serial.print(b / suma, 3);
    Serial.println();
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
