// Ejemplo 23 - Inferencia en vivo y publicación en Blynk
// El modelo entrenado en el PC (ejemplo 22) clasifica cada ventana del
// potenciómetro en el propio ESP32: quieto, giro o vaiven. El resultado
// enciende uno de tres LED y, SOLO cuando la clase cambia, se publica en
// Blynk: V2 = clase (0, 1, 2) y V3 = confianza en %.
// A la nube sube la CONCLUSIÓN (un par de números de vez en cuando), no la
// señal (50 muestras por segundo).

// --- CREDENCIALES DE BLYNK (fuera del código) ---
// BLYNK_TEMPLATE_ID, BLYNK_TEMPLATE_NAME y BLYNK_AUTH_TOKEN viven en
// include/secrets.h, que NO se sube al repositorio (.gitignore).
// Si el archivo no existe (proyecto recién clonado), se usa la plantilla
// secrets.example.h para que compile igual; Blynk responderá «Invalid auth token»
// y la clasificación con los LED funciona igual, sin nube.
// OJO: Blynk exige que estas tres macros estén definidas ANTES de incluir
// su cabecera; por eso este bloque va primero.
#if __has_include("secrets.h")
#include "secrets.h"
#else
#warning "No existe include/secrets.h: se usa la plantilla secrets.example.h (token falso, Blynk respondera Invalid auth token). Copia secrets.example.h como secrets.h y pon tus datos."
#include "secrets.example.h"
#endif

#define BLYNK_PRINT Serial  // Blynk imprime su diagnostico en el Monitor Serial

#include <Arduino.h>
#include <WiFi.h>
#include <BlynkSimpleEsp32_SSL.h>  // conexión cifrada (TLS, puerto 443), como en el ejemplo 19
#include "Ventana.h"
// Copia del include/modelo_gestos.h que genera el ejemplo 22
// (entrenamiento/entrenar.py). Si vuelves a entrenar, vuelve a copiarlo aquí.
// Es un bosque de 10 árboles: modelo_gestos_predict_proba() devuelve, para
// cada clase, la fracción de árboles que votan por ella (0.0, 0.1 ... 1.0).
// Esa fracción es la «confianza» de este ejemplo. (Si exportas un árbol solo,
// la función existe pero siempre da 1.0 a la clase ganadora: no informa nada.)
#include "modelo_gestos.h"

// --- Credenciales de WiFi para Wokwi ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

const unsigned long WIFI_TIMEOUT_MS = 20000;            // tope para el WiFi (luego reinicia)
const unsigned long BLYNK_TIMEOUT_CONEXION_MS = 10000;  // tope para el primer intento con Blynk

// --- Cuota de Blynk ---
// Se publica solo al cambiar de clase y, como mucho, una vez cada 5 s.
// Cada publicación son 2 mensajes (V2 y V3).
// PEOR CASO (la clase cambia sin parar, día y noche):
//   2 mensajes cada 5 s = 34 560 al día = 1 036 800 en 30 días,
//   unas 10 veces la cuota gratuita de 100 000 mensajes al mes:
//   se agotaría en menos de 3 días.
// Para que el peor caso quepa, el intervalo mínimo tendría que ser de 52 s
// (2 x 2 592 000 s / 52 s = 99 692 mensajes). Con uso normal sobra: cabe
// mientras la clase cambie, en promedio, menos de unas 69 veces por hora.
const unsigned long INTERVALO_MIN_ENVIO_MS = 5000;

const uint8_t PIN_POT = 32;
const uint8_t N_CLASES = 3;
const uint8_t PIN_LED[N_CLASES] = {25, 26, 27};   // quieto, giro, vaiven
const char* const NOMBRE_CLASE[N_CLASES] = {"quieto", "giro", "vaiven"};

Ventana ventana(PIN_POT);
BlynkTimer timer;

int claseActual = -1;           // última clase inferida (-1 = todavía ninguna)
float confianzaActual = 0.0f;   // su confianza (0.0 - 1.0)
int claseEnviada = -1;          // última clase publicada en Blynk
unsigned long ultimoEnvioMs = 0;

// Al (re)conectar con el servidor se olvida lo enviado: así el panel recibe
// el estado actual en cuanto se permita el siguiente envío.
BLYNK_CONNECTED() {
    Serial.println("[BLYNK] Conectado. Se publicara la clase actual.");
    claseEnviada = -1;
}

// Cada segundo (BlynkTimer): ¿hay que publicar?
void publicarSiCambio() {
    if (claseActual < 0 || claseActual == claseEnviada) {
        return;  // nada nuevo que contar
    }
    if (claseEnviada >= 0 && millis() - ultimoEnvioMs < INTERVALO_MIN_ENVIO_MS) {
        return;  // cambió, pero hace menos de 5 s del último envío: esperar
    }
    if (!Blynk.connected()) {
        return;  // sin conexión: se enviará al volver (claseEnviada sigue distinta)
    }
    int porcentaje = (int)(confianzaActual * 100.0f + 0.5f);
    Blynk.virtualWrite(V2, claseActual);
    Blynk.virtualWrite(V3, porcentaje);
    Serial.printf("[BLYNK] %s -> %s V2=%d V3=%d\n",
                  claseEnviada < 0 ? "inicio" : NOMBRE_CLASE[claseEnviada],
                  NOMBRE_CLASE[claseActual], claseActual, porcentaje);
    claseEnviada = claseActual;
    ultimoEnvioMs = millis();
}

void clasificarVentana() {
    // 1. Características (lib/Ventana): media, desviación, rango y cruces
    unsigned long t0 = micros();
    Caracteristicas c;
    ventana.extraer(c);
    // Mismo redondeo con el que llegan al PC en el CSV del ejemplo 21
    // (media con 1 decimal, desv con 2): el modelo ve lo mismo aquí que allí.
    float x[4] = {roundf(c.media * 10.0f) / 10.0f, roundf(c.desv * 100.0f) / 100.0f,
                  c.rango, c.cruces};
    unsigned long usExtraer = micros() - t0;

    // 2. Inferencia: votos de los 10 árboles -> clase ganadora y su confianza.
    //    Ante un empate gana la clase de índice menor, igual que en
    //    modelo_gestos_predict().
    t0 = micros();
    float votos[N_CLASES];
    modelo_gestos_predict_proba(x, 4, votos, N_CLASES);
    int clase = 0;
    for (int i = 1; i < N_CLASES; i++) {
        if (votos[i] > votos[clase]) {
            clase = i;
        }
    }
    unsigned long usInferir = micros() - t0;

    // 3. Actuar: un LED por clase
    for (int i = 0; i < N_CLASES; i++) {
        digitalWrite(PIN_LED[i], i == clase ? HIGH : LOW);
    }
    claseActual = clase;
    confianzaActual = votos[clase];

    Serial.printf("[V %04lu] desv=%.2f cruces=%.0f -> %s (%.2f) extraer=%lu us inferir=%lu us\n",
                  (unsigned long)ventana.numero(), x[1], x[3], NOMBRE_CLASE[clase],
                  confianzaActual, usExtraer, usInferir);
}

void setup() {
    Serial.begin(115200);
    for (int i = 0; i < N_CLASES; i++) {
        pinMode(PIN_LED[i], OUTPUT);
        digitalWrite(PIN_LED[i], LOW);
    }
    Serial.println();
    Serial.println("[INICIO] Ejemplo 23 - Inferencia en vivo + Blynk (V2 clase, V3 confianza)");

    // 1. WiFi con tope de 20 s (igual que el ejemplo 19)
    Serial.print("[WiFi] Conectando");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    unsigned long inicio = millis();
    while (WiFi.status() != WL_CONNECTED) {
        if (millis() - inicio >= WIFI_TIMEOUT_MS) {
            Serial.println("\n[WiFi] Sin conexión tras 20 s. Revisa el SSID, la contraseña o la cobertura.");
            Serial.println("[WiFi] Reiniciando la placa en 5 s para volver a intentarlo...");
            delay(5000);
            ESP.restart();
        }
        delay(500);
        Serial.print(".");
    }
    Serial.println("\n[WiFi] Conectado");

    // 2. Blynk: config() guarda el token; connect() lo intenta con tope.
    //    Si no conecta, no se bloquea: Blynk.run() reintenta en el loop() y
    //    los LED funcionan igual (la inferencia no necesita la nube).
    Blynk.config(BLYNK_AUTH_TOKEN);
    if (!Blynk.connect(BLYNK_TIMEOUT_CONEXION_MS)) {
        if (Blynk.isTokenInvalid()) {
            Serial.println("[BLYNK] Token inválido: revisa BLYNK_AUTH_TOKEN en include/secrets.h.");
        } else {
            Serial.println("[BLYNK] Sin conexión con el servidor por ahora. Se reintenta en segundo plano.");
        }
    }
    Serial.printf("[MEMORIA] heap libre = %lu bytes (con WiFi y TLS activos)\n",
                  (unsigned long)ESP.getFreeHeap());

    timer.setInterval(1000L, publicarSiCambio);
    ventana.begin();  // el muestreo empieza ahora, ya conectados
}

void loop() {
    Blynk.run();       // mantiene la conexión con Blynk
    timer.run();       // publicarSiCambio() cada segundo
    ventana.update();  // una muestra cada 20 ms, sin bloquear

    if (ventana.hayVentana()) {
        clasificarVentana();  // cada 0,5 s
    }
}
