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

// --- CONFIGURACIÓN OPENWEATHERMAP ---
// REEMPLAZA "TU_API_KEY_AQUI" con tu llave gratuita de OpenWeatherMap
String apiKey = "TU_API_KEY_AQUI";
String ciudad = "Curitiba,BR";

// Construimos la URL pidiendo unidades métricas (Celsius)
String url = "http://api.openweathermap.org/data/2.5/weather?q=" + ciudad + "&units=metric&appid=" + apiKey;

// Variables Globales
float temperatura = 0.0;
int humedad = 0;
String nombreCiudad = "";
bool datosObtenidos = false;

unsigned long ultimoFetch = 0;
const unsigned long INTERVALO_FETCH = 60000; // Refrescar 1 vez por minuto

void setup() {
    Serial.begin(115200);
    
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("Error iniciando OLED");
        for(;;);
    }
    
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 10);
    display.println("Conectando WiFi...");
    display.display();

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nWiFi conectado!");
    display.println("WiFi OK!");
    display.display();
}

void actualizarClima() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url);
        int httpCode = http.GET();
        
        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            
            // JSON de OpenWeatherMap tiene muchos datos, usamos 1024 bytes
            DynamicJsonDocument doc(1024); 
            DeserializationError error = deserializeJson(doc, payload);
            
            if (!error) {
                // Extracción de la estructura del JSON
                nombreCiudad = doc["name"].as<String>();
                temperatura = doc["main"]["temp"];
                humedad = doc["main"]["humidity"];
                
                datosObtenidos = true;
                
                // Mostrar en el Monitor Serial
                Serial.println("\n--- REPORTE DEL CLIMA ---");
                Serial.printf("Ciudad: %s\n", nombreCiudad.c_str());
                Serial.printf("Temp: %.1f C\n", temperatura);
                Serial.printf("Humedad: %d %%\n", humedad);
                Serial.println("-------------------------");
            } else {
                Serial.println("Error parseando JSON");
            }
        } else {
            // Si pusiste mal la API KEY, httpCode será 401 (Unauthorized)
            Serial.printf("Error HTTP: %d (Revisa tu API KEY si es 401)\n", httpCode);
            
            display.clearDisplay();
            display.setCursor(0,0);
            display.println("ERROR DE API KEY");
            display.printf("Cod: %d", httpCode);
            display.display();
        }
        http.end();
    }
}

void refrescarPantallaOLED() {
    if (!datosObtenidos) return;

    display.clearDisplay();
    
    // 1. Mostrar nombre de la Ciudad extraído de la API
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print("Ciudad: ");
    display.print(nombreCiudad);
    display.drawLine(0, 10, 128, 10, WHITE);
    
    // 2. Mostrar la Temperatura (en grande)
    display.setTextSize(2);
    display.setCursor(0, 20);
    display.printf("%.1f C", temperatura);
    
    // 3. Mostrar Humedad (texto normal)
    display.setTextSize(1);
    display.setCursor(0, 45);
    display.printf("Humedad: %d %%", humedad);
    
    display.display();
}

void loop() {
    if (millis() - ultimoFetch >= INTERVALO_FETCH || ultimoFetch == 0) {
        actualizarClima();
        if (datosObtenidos) {
            refrescarPantallaOLED();
        }
        ultimoFetch = millis();
    }
}
