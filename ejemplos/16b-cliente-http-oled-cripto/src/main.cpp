#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const char* ssid = "Wokwi-GUEST";
const char* password = "";
// Tope de espera para conectarse al WiFi. Si se agota, se reinicia la placa:
// sin red este programa no tiene nada que hacer, y el reinicio vuelve a
// intentarlo desde cero con la pila WiFi limpia.
const unsigned long WIFI_TIMEOUT_MS = 20000;

// URL consultando dos criptomonedas al mismo tiempo.
// OJO: es https, pero no le damos ningún certificado a HTTPClient. En ese caso
// la conexión va cifrada pero SIN verificar la identidad del servidor (equivale
// a WiFiClientSecure::setInsecure()). Sirve para aprender; en un producto real
// hay que cargar el certificado raíz con http.begin(url, certificadoCA).
const char* url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,dogecoin&vs_currencies=usd";

float precioBTC = 0.0;
float precioDOGE = 0.0;
bool datosObtenidos = false;

unsigned long ultimoFetch = 0;
const unsigned long INTERVALO_FETCH = 60000; // Bajar datos cada 60 s: la CDN de CoinGecko repite el precio hasta 60 s (s-maxage=60)

unsigned long ultimoCambioPantalla = 0;
const unsigned long INTERVALO_PANTALLA = 5000; // Cambiar moneda mostrada cada 5 segundos
bool mostrarBitcoin = true;

void setup() {
    Serial.begin(115200);
    
    // Iniciar OLED
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("Error iniciando OLED");
        for(;;);
    }
    
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 20);
    display.println("Conectando WiFi...");
    display.display();

    // Conectar a WiFi
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    unsigned long inicio = millis();
    while (WiFi.status() != WL_CONNECTED) {
        // Si pasan 20 s sin conectar, avisar y reiniciar (no esperar para siempre)
        if (millis() - inicio >= WIFI_TIMEOUT_MS) {
            Serial.println("\n[WiFi] Sin conexión tras 20 s. Revisa el SSID, la contraseña o la cobertura.");
            Serial.println("[WiFi] Reiniciando la placa en 5 s para volver a intentarlo...");
            display.clearDisplay();
            display.setCursor(0, 20);
            display.println("Sin WiFi tras 20 s");
            display.println("Reiniciando...");
            display.display();
            delay(5000);
            ESP.restart();
        }
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nWiFi conectado!");
    display.clearDisplay();
    display.setCursor(0, 20);
    display.println("WiFi OK!");
    display.display();
}

void actualizarPreciosHTTP() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url);
        int httpCode = http.GET();
        
        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            
            StaticJsonDocument<256> doc;
            DeserializationError error = deserializeJson(doc, payload);
            
            if (!error) {
                precioBTC = doc["bitcoin"]["usd"];
                precioDOGE = doc["dogecoin"]["usd"];
                datosObtenidos = true;
                
                // Mostrar en el Monitor Serial
                Serial.println("\n--- NUEVOS DATOS (CoinGecko) ---");
                Serial.printf("Bitcoin (BTC): $%.2f USD\n", precioBTC);
                Serial.printf("Dogecoin (DOGE): $%.4f USD\n", precioDOGE);
                Serial.println("--------------------------------");
            } else {
                Serial.println("Error parseando JSON");
            }
        } else if (httpCode > 0) {
            // El servidor respondió, pero no con 200 (p. ej. 429 = demasiadas peticiones)
            Serial.printf("Error HTTP: %d\n", httpCode);
        } else {
            // Código negativo: ni siquiera hubo respuesta (DNS, TLS, tiempo agotado...)
            Serial.printf("Error HTTP: %d (%s)\n", httpCode, HTTPClient::errorToString(httpCode).c_str());
        }
        http.end();
    }
}

void refrescarPantallaOLED() {
    if (!datosObtenidos) return;

    display.clearDisplay();
    
    // Encabezado
    display.setTextSize(1);
    display.setCursor(15, 0);
    display.println("MERCADO CRIPTO");
    display.drawLine(0, 10, 128, 10, WHITE);
    
    // Moneda y Precio
    display.setCursor(0, 25);
    display.setTextSize(2);
    
    if (mostrarBitcoin) {
        display.println("BTC");
        display.setTextSize(1);
        display.setCursor(0, 48);
        display.printf("$ %.2f USD", precioBTC);
    } else {
        display.println("DOGE");
        display.setTextSize(1);
        display.setCursor(0, 48);
        display.printf("$ %.4f USD", precioDOGE);
    }
    
    display.display();
}

void loop() {
    // Tarea 1: Consultar a internet de forma espaciada (cada 60 s)
    if (millis() - ultimoFetch >= INTERVALO_FETCH || ultimoFetch == 0) {
        actualizarPreciosHTTP();
        // Forzar la actualización visual inmediata tras recibir nuevos datos
        refrescarPantallaOLED(); 
        // Reiniciar también el reloj de la pantalla: así la moneda recién pintada
        // (BTC en el primer ciclo) se ve los 5 s completos antes de alternar
        ultimoCambioPantalla = millis();
        ultimoFetch = millis();
    }
    
    // Tarea 2: Alternar la pantalla entre BTC y DOGE rápido (cada 5s)
    if (millis() - ultimoCambioPantalla >= INTERVALO_PANTALLA && datosObtenidos) {
        mostrarBitcoin = !mostrarBitcoin; // Intercambiar moneda
        refrescarPantallaOLED();
        ultimoCambioPantalla = millis();
    }
}
