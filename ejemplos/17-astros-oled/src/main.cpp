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

// URL abierta de astronautas (¡Ojo! Es HTTP normal, sin la S)
// AVISO: open-notify ya no se mantiene y devuelve datos CONGELADOS (la
// tripulación de 2024). Responde 200 OK igual: un 200 sólo dice que el
// servidor contestó, no que el dato esté vigente. Úsalo para practicar el
// parseo de arrays JSON, no como fuente de quién está hoy en el espacio.
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
    // Sin salto de línea automático: un nombre que no cabe en 128 px se recorta
    // en el borde en lugar de pasar al renglón de abajo y pisar el siguiente
    display.setTextWrap(false);
    display.setCursor(0, 20);
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
    display.setCursor(0, 20);
    display.println("WiFi OK!");
    display.display();
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
        } else {
            // No fallar en silencio: decir qué pasó
            if (httpCode > 0) {
                // El servidor respondió, pero no con 200 (p. ej. 404 o 503)
                Serial.printf("Error HTTP: %d\n", httpCode);
            } else {
                // Código negativo: ni siquiera hubo respuesta (DNS, conexión, tiempo agotado...)
                Serial.printf("Error HTTP: %d (%s)\n", httpCode, HTTPClient::errorToString(httpCode).c_str());
            }

            // Si todavía no hay lista que mostrar, avisar también en la OLED
            if (totalAstronautas == 0) {
                display.clearDisplay();
                display.setCursor(0, 20);
                display.println("Error al consultar");
                display.printf("Cod: %d", httpCode);
                display.display();
            }
        }
        http.end();
    }
}

void refrescarPantallaOLED() {
    // Sólo se llama desde loop() cuando totalAstronautas > 0
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
        // Mostrar con numeración: "1.Nombre"
        display.printf("%d.%s", indiceAst + 1, nombresAstronautas[indiceAst].c_str());
        y += 10; // Bajar un renglón
    }
    
    display.display();
    
    // Lógica para avanzar de página en el siguiente turno
    paginaActual++;
    // Sólo se guardan hasta 15 nombres: las páginas se cuentan con ese mismo tope
    int cantidadMostrar = (totalAstronautas > 15) ? 15 : totalAstronautas;
    int totalPaginas = (cantidadMostrar + astrosPorPagina - 1) / astrosPorPagina; // División redondeada hacia arriba
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
