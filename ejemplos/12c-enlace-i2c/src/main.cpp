#include <Arduino.h>
#include <Wire.h>

// Usaremos el pin 4 como "Jumper de Identidad"
// Si el pin 4 está conectado a GND, esta será la "Placa A" (Dirección 0x10)
// Si está desconectado (o a 3.3V), será la "Placa B" (Dirección 0x11)
const uint8_t PIN_ROL = 4;

uint8_t miDireccion;
uint8_t otraDireccion;

// Búfer para almacenar los mensajes que lleguen
String mensajeRecibido = "";
bool hayMensaje = false;

// Esta función se dispara (interrupción) automáticamente cuando alguien nos envía datos por I2C
void alRecibirI2C(int numBytes) {
    while (Wire.available()) {
        char c = Wire.read();
        mensajeRecibido += c;
    }
    hayMensaje = true;
}

void setup() {
    Serial.begin(115200);
    
    // Configurar el pin con pull-up interno para que no quede "flotando" si no hay cable
    pinMode(PIN_ROL, INPUT_PULLUP);
    
    // Leer el jumper para decidir nuestro rol en la red I2C
    if (digitalRead(PIN_ROL) == LOW) {
        miDireccion = 0x10;
        otraDireccion = 0x11;
        Serial.println("\n--- MODO PLACA A (Dir I2C: 0x10) ---");
    } else {
        miDireccion = 0x11;
        otraDireccion = 0x10;
        Serial.println("\n--- MODO PLACA B (Dir I2C: 0x11) ---");
    }

    // Inicializamos el bus I2C pasándole nuestra dirección
    // Al hacer esto, el ESP32 se une al bus y puede ser "esclavo" (escuchar)
    Wire.begin(miDireccion);
    
    // Registramos la función que debe ejecutarse cuando nos envíen algo
    Wire.onReceive(alRecibirI2C);
    
    Serial.println("Escribe un mensaje en el monitor para enviarlo por I2C...");
}

void loop() {
    // 1. Monitor Serial -> I2C: Enviar datos a la otra placa
    if (Serial.available() > 0) {
        // En I2C, para enviar, nos convertimos temporalmente en "Maestro" y abrimos transmisión hacia la OTRA dirección
        Wire.beginTransmission(otraDireccion);
        
        while (Serial.available() > 0) {
            char c = Serial.read();
            Serial.print(c); // Eco local para ver lo que escribimos
            Wire.write(c);   // Enviar por I2C
        }
        
        // Cerramos la transmisión (esto es lo que realmente envía los datos por el cable)
        Wire.endTransmission();
    }

    // 2. I2C -> Monitor Serial: Imprimir lo que nos llegó
    if (hayMensaje) {
        Serial.print("\n[Mensaje recibido por I2C]: ");
        Serial.print(mensajeRecibido);
        
        // Limpiamos el búfer para el próximo mensaje
        mensajeRecibido = "";
        hayMensaje = false;
    }
}
