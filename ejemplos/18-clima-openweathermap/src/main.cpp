#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --- CLAVE DE OPENWEATHERMAP (fuera del código) ---
// La clave vive en include/secrets.h, que NO se sube al repositorio (.gitignore).
// Si el archivo no existe (proyecto recién clonado), se usa la plantilla
// secrets.example.h para que compile igual; la API responderá 401.
#if __has_include("secrets.h")
#include "secrets.h"
#else
#warning "No existe include/secrets.h: se usa la plantilla secrets.example.h (clave falsa, la API respondera 401). Copia secrets.example.h como secrets.h y pon tu clave."
#include "secrets.example.h"
#endif

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Tope de espera para conectarse al WiFi. Si se agota, se reinicia la placa:
// sin red este programa no tiene nada que hacer, y el reinicio vuelve a
// intentarlo desde cero con la pila WiFi limpia.
const unsigned long WIFI_TIMEOUT_MS = 20000;

// --- CONFIGURACIÓN OPENWEATHERMAP ---
String ciudad = "Lima,PE";

// Construimos la URL pidiendo unidades métricas (Celsius).
// Va por https para que la clave (appid) no viaje en texto plano. OJO: no le
// damos ningún certificado a HTTPClient, así que la conexión va cifrada pero
// SIN verificar la identidad del servidor (equivale a setInsecure()). Sirve
// para aprender; en un producto real hay que cargar el certificado raíz con
// http.begin(url, certificadoCA).
String url = "https://api.openweathermap.org/data/2.5/weather?q=" + ciudad + "&units=metric&appid=" + OWM_API_KEY;

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
    display.setCursor(0, 10);
    display.println("WiFi OK!");
    display.display();
}

// Explica el error en el Monitor Serial y en la OLED.
// (La fuente de la OLED no tiene tildes: ahí se escribe sin acentos.)
void mostrarErrorHTTP(int httpCode) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);

    if (httpCode == 401) {
        // 401 Unauthorized: la clave está mal copiada, es la de la plantilla,
        // o es nueva y todavía no se activa (puede tardar unas horas)
        Serial.println("Error HTTP 401: clave API inválida o aún no activa (revisa include/secrets.h).");
        display.println("ERROR 401");
        display.println("API KEY invalida");
        display.println("o aun no activa");
    } else if (httpCode == 404) {
        // 404 Not Found: OpenWeatherMap no conoce la ciudad pedida
        Serial.printf("Error HTTP 404: ciudad no encontrada (%s).\n", ciudad.c_str());
        display.println("ERROR 404");
        display.println("Ciudad no encontrada");
        display.println(ciudad);
    } else if (httpCode == 429) {
        // 429 Too Many Requests: se superó el límite de consultas del plan gratuito
        Serial.println("Error HTTP 429: límite de consultas superado. Espera y consulta con menos frecuencia.");
        display.println("ERROR 429");
        display.println("Limite de consultas");
        display.println("superado");
    } else if (httpCode < 0) {
        // Código negativo: ni siquiera hubo respuesta (DNS, TLS, tiempo agotado...)
        Serial.printf("Error de conexión %d: %s\n", httpCode, HTTPClient::errorToString(httpCode).c_str());
        display.println("ERROR DE CONEXION");
        display.printf("Cod: %d", httpCode);
    } else {
        // Cualquier otro código del servidor (500, 503...)
        Serial.printf("Error HTTP %d: respuesta inesperada del servidor.\n", httpCode);
        display.println("ERROR HTTP");
        display.printf("Cod: %d", httpCode);
    }

    display.display();
}

// Devuelve true si se obtuvieron datos nuevos del clima
bool actualizarClima() {
    bool exito = false;

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url);
        int httpCode = http.GET();

        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();

            // El JSON de OpenWeatherMap trae muchos campos (coord, weather, wind,
            // sys...): con 2048 bytes caben todos, con margen
            DynamicJsonDocument doc(2048);
            DeserializationError error = deserializeJson(doc, payload);

            if (!error) {
                // Extracción de la estructura del JSON
                nombreCiudad = doc["name"].as<String>();
                temperatura = doc["main"]["temp"];
                humedad = doc["main"]["humidity"];

                datosObtenidos = true;
                exito = true;

                // Mostrar en el Monitor Serial
                Serial.println("\n--- REPORTE DEL CLIMA ---");
                Serial.printf("Ciudad: %s\n", nombreCiudad.c_str());
                Serial.printf("Temp: %.1f C\n", temperatura);
                Serial.printf("Humedad: %d %%\n", humedad);
                Serial.println("-------------------------");
            } else {
                Serial.print("Error parseando JSON: ");
                Serial.println(error.c_str());
            }
        } else {
            // Distinguir el motivo: 401, 404, 429, sin conexión u otro
            mostrarErrorHTTP(httpCode);
        }
        http.end();
    }

    return exito;
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
        // Sólo se repinta el clima si llegó un dato nuevo; si hubo error,
        // la OLED conserva el mensaje de error hasta la próxima consulta
        if (actualizarClima()) {
            refrescarPantallaOLED();
        }
        ultimoFetch = millis();
    }
}
