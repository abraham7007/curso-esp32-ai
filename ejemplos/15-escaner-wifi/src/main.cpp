#include <Arduino.h>
#include <WiFi.h>

void setup() {
    Serial.begin(115200);

    // Configurar ESP32 en modo estación (cliente), no como punto de acceso
    WiFi.mode(WIFI_STA);

    // Desconectar de cualquier red a la que estuviera conectado previamente
    WiFi.disconnect();
    delay(100);

    Serial.println("\n--- ESCÁNER DE REDES WIFI INICIADO ---");
}

void loop() {
    Serial.println("Iniciando escaneo...");

    // WiFi.scanNetworks() bloquea la ejecución hasta terminar el barrido de todos
    // los canales (unos 2 segundos) y devuelve la cantidad de redes encontradas.
    // Si el escaneo falla devuelve un número NEGATIVO (WIFI_SCAN_FAILED = -2).
    int n = WiFi.scanNetworks();
    Serial.println("Escaneo finalizado.");

    if (n < 0) {
        // Un valor negativo es un código de error, no una cantidad de redes
        Serial.printf("Error: el escaneo falló (código %d). Se reintenta en el próximo ciclo.\n", n);
    } else if (n == 0) {
        Serial.println("No se encontraron redes WiFi.");
    } else {
        // Singular o plural según la cantidad
        Serial.print(n);
        Serial.println(n == 1 ? " red encontrada:" : " redes encontradas:");

        for (int i = 0; i < n; ++i) {
            // Imprimir Índice
            Serial.print(i + 1);
            Serial.print(": ");

            // Imprimir Nombre de la red (SSID)
            Serial.print(WiFi.SSID(i));

            // Imprimir Potencia de la señal (RSSI) en decibelios-milivatio (dBm)
            Serial.print(" (");
            Serial.print(WiFi.RSSI(i));
            Serial.print(" dBm)");

            // Imprimir el canal de la red (1 a 13 en la banda de 2,4 GHz)
            Serial.print(" canal ");
            Serial.print(WiFi.channel(i));

            // Indicar si la red es abierta o requiere contraseña
            if (WiFi.encryptionType(i) == WIFI_AUTH_OPEN) {
                Serial.println(" [Red Abierta]");
            } else {
                Serial.println(" [Red Cifrada]");
            }
            delay(10);
        }
    }

    Serial.println("\n-----------------------------------\n");

    // Esperar 5 segundos antes de realizar el próximo escaneo
    delay(5000);
}
