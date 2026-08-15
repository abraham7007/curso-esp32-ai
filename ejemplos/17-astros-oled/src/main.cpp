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

// URL abierta de astronautas (¡Ojo! Es HTTP normal, sin la S)
const char* url = "http://api.open-notify.org/astros.json";

// Variables Globales
int totalAstronautas = 0;
String nombresAstronautas[15]; // Asumimos un máximo de 15 personas para reservar memoria

unsigned long ultimoFetch = 0;
const unsigned long INTERVALO_FETCH = 60000; // Refrescar internet 1 vez por minuto

unsigned long ultimoCambioPantalla = 0;
const unsigned long INTERVALO_PANTALLA = 4000; // Cambiar de página cada 4 segundos
int paginaActual = 0;
int astrosPorPagina = 5;

void setup() {
    Serial.begin(115200);
    
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

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nWiFi conectado!");
}

void descargarListaAstronautas() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url);
        int httpCode = http.GET();
        
        if (httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            
            // Requerimos un documento más grande (Dynamic) por el array JSON largo
            DynamicJsonDocument doc(2048); 
            DeserializationError error = deserializeJson(doc, payload);
            
            if (!error) {
                totalAstronautas = doc["number"];
                
                // Limitar al tamaño de nuestro array local de C++ por seguridad
                int cantidadLeer = (totalAstronautas > 15) ? 15 : totalAstronautas;
                
                Serial.println("\n--- ASTRONAUTAS EN EL ESPACIO ---");
                Serial.printf("Total: %d\n", totalAstronautas);
                
                // Extraer el array JSON "people" y guardarlo en el array String de C++
                JsonArray people = doc["people"];
                for (int i = 0; i < cantidadLeer; i++) {
                    nombresAstronautas[i] = people[i]["name"].as<String>();
                    Serial.printf("%d. %s\n", i + 1, nombresAstronautas[i].c_str());
                }
                Serial.println("---------------------------------");
            } else {
                Serial.println("Error parseando JSON de astronautas");
            }
        }
        http.end();
    }
}

void refrescarPantallaOLED() {
    if (totalAstronautas == 0) {
        display.clearDisplay();
        display.setCursor(0, 25);
        display.println("Buscando astros...");
        display.display();
        return;
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.printf(" EN EL ESPACIO: %d", totalAstronautas);
    display.drawLine(0, 10, 128, 10, WHITE);
    
    // Calcular en qué posición del array empezar según la página actual
    int indiceInicio = paginaActual * astrosPorPagina;
    int y = 14; // Coordenada Y donde empezará a imprimirse el primer nombre
    
    // Imprimir nombres hasta llenar la página
    for (int i = 0; i < astrosPorPagina; i++) {
        int indiceAst = indiceInicio + i;
        
        // Si ya imprimimos a todos, abortar el ciclo
        if (indiceAst >= totalAstronautas || indiceAst >= 15) {
            break;
        }
        
        display.setCursor(0, y);
        // Mostrar numeración requerida por el profesor: "1. Nombre"
        display.printf("%d.%s", indiceAst + 1, nombresAstronautas[indiceAst].c_str());
        y += 10; // Bajar un renglón
    }
    
    display.display();
    
    // Lógica para avanzar de página en el siguiente turno
    paginaActual++;
    int totalPaginas = (totalAstronautas + astrosPorPagina - 1) / astrosPorPagina; // División redondeada hacia arriba
    if (paginaActual >= totalPaginas) {
        paginaActual = 0; // Volver a la primera página si ya vimos todos
    }
}

void loop() {
    // Tarea 1: Internet cada 60s
    if (millis() - ultimoFetch >= INTERVALO_FETCH || ultimoFetch == 0) {
        descargarListaAstronautas();
        ultimoFetch = millis();
    }
    
    // Tarea 2: OLED con Paginación cada 4s
    if (millis() - ultimoCambioPantalla >= INTERVALO_PANTALLA && totalAstronautas > 0) {
        refrescarPantallaOLED();
        ultimoCambioPantalla = millis();
    }
}
