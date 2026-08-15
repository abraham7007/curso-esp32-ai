#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// En Wokwi, la red "Wokwi-GUEST" no tiene contraseña y da salida real a Internet
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// URL pública de CoinGecko para el precio del Bitcoin (BTC) a Dólares (USD)
const char* url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd";

void setup() {
    Serial.begin(115200);
    
    // Conectarse al WiFi
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    Serial.print("\nConectando a WiFi ");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\n¡Conectado! IP: " + WiFi.localIP().toString());
}

void loop() {
    // 1. Validar que seguimos conectados
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        
        Serial.println("\n[HTTP] Consultando a CoinGecko...");
        // Configuramos la URL
        http.begin(url);
        
        // 2. Realizamos la petición GET
        int httpCode = http.GET();
        
        // 3. Verificamos si el servidor nos respondió correctamente
        if (httpCode > 0) {
            if (httpCode == HTTP_CODE_OK) {
                // Obtenemos el texto (JSON) crudo
                String payload = http.getString();
                Serial.println("[HTTP] JSON Recibido: " + payload);
                
                // 4. Deserializamos el JSON usando memoria estática
                StaticJsonDocument<200> doc;
                DeserializationError error = deserializeJson(doc, payload);
                
                if (error) {
                    Serial.print("[JSON] Error al parsear: ");
                    Serial.println(error.c_str());
                } else {
                    // 5. Navegamos por el JSON: {"bitcoin":{"usd":62500}}
                    float precioBTC = doc["bitcoin"]["usd"];
                    
                    Serial.println("------------------------------------");
                    Serial.printf("  PRECIO BITCOIN: $ %.2f USD\n", precioBTC);
                    Serial.println("------------------------------------");
                }
            } else {
                Serial.printf("[HTTP] Error de servidor: %d\n", httpCode);
            }
        } else {
            Serial.printf("[HTTP] Error de conexión: %s\n", http.errorToString(httpCode).c_str());
        }
        
        // Es obligatorio cerrar la conexión para liberar memoria
        http.end();
    } else {
        Serial.println("Error: WiFi desconectado.");
    }
    
    // 6. Esperamos 15 segundos (OJO: No consultar demasiado rápido o CoinGecko bloquea tu IP temporalmente)
    delay(15000);
}
