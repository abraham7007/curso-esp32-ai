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
// URL consultando dos criptomonedas al mismo tiempo
const char* url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,dogecoin&vs_currencies=usd";

float precioBTC = 0.0;
float precioDOGE = 0.0;
bool datosObtenidos = false;

unsigned long ultimoFetch = 0;
const unsigned long INTERVALO_FETCH = 20000; // Bajar datos cada 20 segundos

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
    
    while (WiFi.status() != WL_CONNECTED) {
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
                
                // Mostrar en el Monitor Serial como requeriste
                Serial.println("\n--- NUEVOS DATOS (CoinGecko) ---");
                Serial.printf("Bitcoin (BTC): $%.2f USD\n", precioBTC);
                Serial.printf("Dogecoin (DOGE): $%.4f USD\n", precioDOGE);
                Serial.println("--------------------------------");
            } else {
                Serial.println("Error parseando JSON");
            }
        } else {
            Serial.printf("Error HTTP: %d\n", httpCode);
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
    // Tarea 1: Consultar a internet de forma espaciada (cada 20s)
    if (millis() - ultimoFetch >= INTERVALO_FETCH || ultimoFetch == 0) {
        actualizarPreciosHTTP();
        // Forzar la actualización visual inmediata tras recibir nuevos datos
        refrescarPantallaOLED(); 
        ultimoFetch = millis();
    }
    
    // Tarea 2: Alternar la pantalla entre BTC y DOGE rápido (cada 5s)
    if (millis() - ultimoCambioPantalla >= INTERVALO_PANTALLA && datosObtenidos) {
        mostrarBitcoin = !mostrarBitcoin; // Intercambiar moneda
        refrescarPantallaOLED();
        ultimoCambioPantalla = millis();
    }
}
