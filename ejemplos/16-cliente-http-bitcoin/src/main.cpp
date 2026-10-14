#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// En Wokwi, la red "Wokwi-GUEST" no tiene contraseña y da salida real a Internet
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Tope de espera para conectarse al WiFi. Si se agota, se reinicia la placa:
// sin red este programa no tiene nada que hacer, y el reinicio vuelve a
// intentarlo desde cero con la pila WiFi limpia.
const unsigned long WIFI_TIMEOUT_MS = 20000;

// URL pública de CoinGecko para el precio del Bitcoin (BTC) a Dólares (USD).
// OJO: es https, pero no le damos ningún certificado a HTTPClient. En ese caso
// la conexión va cifrada pero SIN verificar la identidad del servidor (equivale
// a WiFiClientSecure::setInsecure()). Sirve para aprender; en un producto real
// hay que cargar el certificado raíz con http.begin(url, certificadoCA).
const char* url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd";

// CoinGecko guarda esta respuesta en caché (cabecera cache-control: max-age
// entre 30 y 60 s): consultar más seguido devuelve el mismo precio y gasta
// el límite de peticiones gratuitas. Por eso consultamos cada 60 s.
const unsigned long INTERVALO_CONSULTA = 60000;

void setup() {
    Serial.begin(115200);

    // Conectarse al WiFi
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    Serial.print("\nConectando a WiFi ");
    unsigned long inicio = millis();
    while (WiFi.status() != WL_CONNECTED) {
        // Si pasan 20 s sin conectar, avisar y reiniciar (no esperar para siempre)
        if (millis() - inicio >= WIFI_TIMEOUT_MS) {
            Serial.println("\n[WiFi] Sin conexión tras 20 s. Revisa el SSID, la contraseña o la cobertura.");
            Serial.println("[WiFi] Reiniciando la placa en 5 s para volver a intentarlo...");
            delay(5000);
            ESP.restart();
        }
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

                // 4. Deserializamos el JSON. StaticJsonDocument reserva sus 200 bytes
                //    en la PILA (stack) de loop(): es una variable local que se crea
                //    y se destruye en cada vuelta, no memoria estática ni global.
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

    // 6. Esperamos 60 segundos: coincide con la caché de CoinGecko y evita que
    //    bloquee nuestra IP por consultar demasiado rápido (error 429)
    delay(INTERVALO_CONSULTA);
}
