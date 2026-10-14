#include <Arduino.h>
#include <Wire.h>

// Usaremos el pin 4 como "Jumper de Identidad" (se lee una sola vez, al arrancar)
// Si el pin 4 está conectado a GND, esta será la "Placa A" = MAESTRO (envía)
// Si está desconectado (o a 3.3V), será la "Placa B" = ESCLAVO en 0x11 (recibe)
//
// En I2C los roles son fijos: el puerto que arranca como esclavo NO puede iniciar
// transmisiones (endTransmission devolvería 4, "Bus is in Slave Mode").
// Por eso el enlace es de un solo sentido: A escribe, B escucha.
const uint8_t PIN_ROL = 4;

const uint8_t PIN_SDA = 21;
const uint8_t PIN_SCL = 22;
const uint32_t FRECUENCIA_I2C = 100000;   // 100 kHz (modo estándar)
const uint8_t DIR_ESCLAVO = 0x11;         // Dirección de la Placa B

// El búfer de Wire es de 128 bytes; mandamos la línea en bloques pequeños
const uint8_t BLOQUE_I2C = 32;
const uint8_t MAX_LINEA = 120;            // Caracteres por línea (lo que sobre se descarta)

bool soyMaestro = false;

// ----- Maestro: línea que se está escribiendo en el monitor -----
char lineaTx[MAX_LINEA + 1];
uint8_t largoTx = 0;

// ----- Esclavo: línea que se va armando y último mensaje completo -----
char lineaRx[MAX_LINEA + 1];
uint8_t largoRx = 0;
char mensajeRecibido[MAX_LINEA + 1];
volatile bool hayMensaje = false;

// Esta función se dispara automáticamente cuando el maestro nos envía datos por I2C
// (en el núcleo 2.0.x la llama una tarea interna del driver, no el loop)
void alRecibirI2C(int numBytes) {
    while (Wire.available()) {
        char c = Wire.read();
        if (c == '\n') {
            // Fin de línea: dejamos el mensaje listo para que lo imprima el loop
            lineaRx[largoRx] = '\0';
            strcpy(mensajeRecibido, lineaRx);
            largoRx = 0;
            hayMensaje = true;
        } else if (largoRx < MAX_LINEA) {
            lineaRx[largoRx++] = c;
        }
    }
}

// Traduce el código de Wire.endTransmission() a un texto legible
const char* textoErrorI2C(uint8_t codigo) {
    switch (codigo) {
        case 1: return "datos demasiado largos para el búfer";
        case 2: return "NACK en la dirección (¿esclavo conectado y encendido?)";
        // El núcleo arduino-esp32 2.0.x nunca devuelve 3: cualquier NACK (de la dirección
        // o de los datos) sale como 2. Se deja por compatibilidad con otros núcleos.
        case 3: return "NACK en los datos";
        case 5: return "tiempo de espera agotado (¿faltan pull-ups o GND común?)";
        default: return "otro error del bus";
    }
}

// Envía la línea completa (más '\n' como marca de fin) al esclavo
void enviarLineaI2C(const char* texto, uint8_t largo) {
    uint8_t enviados = 0;
    uint8_t total = largo + 1;   // +1 por el '\n' final

    while (enviados < total) {
        Wire.beginTransmission(DIR_ESCLAVO);
        uint8_t enBloque = 0;
        while (enBloque < BLOQUE_I2C && enviados < total) {
            char c = (enviados < largo) ? texto[enviados] : '\n';
            Wire.write(c);
            enviados++;
            enBloque++;
        }

        // Cerramos la transmisión (esto es lo que realmente envía los datos por el cable)
        uint8_t resultado = Wire.endTransmission();
        if (resultado != 0) {
            Serial.printf("[Error I2C] endTransmission devolvió %u: %s\n",
                          resultado, textoErrorI2C(resultado));
            return;
        }
    }

    Serial.printf("[Enviado por I2C a 0x%02X]: %s\n", DIR_ESCLAVO, texto);
}

void setup() {
    Serial.begin(115200);

    // Configurar el pin con pull-up interno para que no quede "flotando" si no hay cable
    pinMode(PIN_ROL, INPUT_PULLUP);

    // Leer el jumper para decidir nuestro rol en la red I2C
    soyMaestro = (digitalRead(PIN_ROL) == LOW);

    if (soyMaestro) {
        Serial.println("\n--- MODO PLACA A (MAESTRO I2C) ---");
        // Maestro: solo pines; no tiene dirección propia
        Wire.begin(PIN_SDA, PIN_SCL);
        Serial.printf("Escribe un mensaje en el monitor y pulsa Enter para enviarlo a 0x%02X...\n",
                      DIR_ESCLAVO);
    } else {
        Serial.printf("\n--- MODO PLACA B (ESCLAVO I2C, Dir: 0x%02X) ---\n", DIR_ESCLAVO);
        // Registramos la función que debe ejecutarse cuando nos envíen algo
        Wire.onReceive(alRecibirI2C);
        // Esclavo (núcleo 2.0.x): begin(direccion, SDA, SCL, frecuencia)
        Wire.begin(DIR_ESCLAVO, PIN_SDA, PIN_SCL, FRECUENCIA_I2C);
        Serial.println("Esperando mensajes de la Placa A...");
    }
}

void loop() {
    if (soyMaestro) {
        // Monitor Serial -> I2C: armamos la línea y la enviamos al pulsar Enter
        while (Serial.available() > 0) {
            char c = Serial.read();
            if (c == '\r') {
                continue;                     // Ignoramos el CR si el monitor envía CRLF
            }
            if (c == '\n') {
                if (largoTx > 0) {
                    lineaTx[largoTx] = '\0';
                    enviarLineaI2C(lineaTx, largoTx);
                    largoTx = 0;
                }
            } else if (largoTx < MAX_LINEA) {
                lineaTx[largoTx++] = c;
            }
        }
    } else {
        // I2C -> Monitor Serial: imprimir lo que nos llegó
        if (hayMensaje) {
            Serial.print("[Mensaje recibido por I2C]: ");
            Serial.println(mensajeRecibido);

            // Bajamos la bandera para el próximo mensaje
            hayMensaje = false;
        }
    }
}
