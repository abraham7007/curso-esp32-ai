// Ejemplo 19 - Dashboard IoT con Blynk
// El ESP32 deja de ser un cliente que "pregunta" (HTTP GET) y pasa a mantener
// una conexion permanente con la nube: recibe ordenes (V0) y publica datos (V1).

// --- CREDENCIALES DE BLYNK (fuera del código) ---
// BLYNK_TEMPLATE_ID, BLYNK_TEMPLATE_NAME y BLYNK_AUTH_TOKEN viven en
// include/secrets.h, que NO se sube al repositorio (.gitignore).
// Si el archivo no existe (proyecto recién clonado), se usa la plantilla
// secrets.example.h para que compile igual; Blynk responderá «Invalid auth token».
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
// Versión SSL de la librería: conecta a blynk.cloud por el puerto 443 con TLS
// y verifica el certificado del servidor (la librería trae el certificado raíz).
// El token y los datos viajan cifrados. La versión sin SSL (BlynkSimpleEsp32.h)
// usa el puerto 80 y manda todo en texto plano.
#include <BlynkSimpleEsp32_SSL.h>

// --- Credenciales de WiFi para Wokwi ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Tope de espera para conectarse al WiFi. Si se agota, se reinicia la placa:
// sin red este programa no tiene nada que hacer, y el reinicio vuelve a
// intentarlo desde cero con la pila WiFi limpia.
const unsigned long WIFI_TIMEOUT_MS = 20000;

// Tope para el primer intento de conexión con el servidor de Blynk.
// Si se agota NO se bloquea: Blynk.run() sigue reintentando en el loop().
const unsigned long BLYNK_TIMEOUT_CONEXION_MS = 10000;

// Cada cuánto se publica la temperatura en V1.
// El plan gratuito de Blynk permite 100 000 mensajes al mes. Un envío cada
// 5 s son 17 280 al día: la cuota se agotaría en unos 6 días. Cada 30 s son
// 2 880 al día (~86 400 al mes): cabe en la cuota con margen.
const long INTERVALO_ENVIO_MS = 30000L;

// --- Configuracion del Hardware ---
const int ledPin = 15;
BlynkTimer timer;

// Se ejecuta cada vez que llega un valor nuevo a V0, venga de donde venga:
// del widget Switch (web o app), de una automatización, de la API HTTP de
// Blynk o de la respuesta a Blynk.syncVirtual(V0) (ver BLYNK_CONNECTED).
BLYNK_WRITE(V0) {
  int pinValue = param.asInt();
  digitalWrite(ledPin, pinValue);
  Serial.print("Comando recibido de Blynk! Estado del LED: ");
  Serial.println(pinValue);
}

// Se ejecuta cada vez que el ESP32 termina de conectarse (o reconectarse) al
// servidor. Tras un reinicio el LED arranca apagado aunque el Switch esté en
// ON: syncVirtual(V0) le pide al servidor el último valor guardado de V0, que
// llega por BLYNK_WRITE(V0) y deja el LED igual que el Switch.
BLYNK_CONNECTED() {
  Serial.println("Conectado a Blynk. Sincronizando V0...");
  Blynk.syncVirtual(V0);
}

// Esta funcion envia datos del sensor simulado al Datastream V1
void sendSensorData() {
  float temperaturaSimulada = random(180, 280) / 10.0;
  Blynk.virtualWrite(V1, temperaturaSimulada);
  Serial.print("Enviando Temperatura a Blynk: ");
  Serial.println(temperaturaSimulada);
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  // 1. WiFi con tope de 20 s. (Blynk.begin() también conecta el WiFi, pero
  //    espera para siempre si la red no responde; por eso lo hacemos aparte.)
  Serial.print("Conectando a WiFi");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

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
  Serial.println("\nWiFi conectado!");

  // 2. Blynk: config() sólo guarda el token y el servidor (blynk.cloud:443);
  //    connect() intenta conectar durante BLYNK_TIMEOUT_CONEXION_MS como mucho
  //    (el saludo TLS en curso puede alargarlo unos segundos).
  Blynk.config(BLYNK_AUTH_TOKEN);
  if (!Blynk.connect(BLYNK_TIMEOUT_CONEXION_MS)) {
    if (Blynk.isTokenInvalid()) {
      // Con el token rechazado Blynk ya no reintenta: hay que corregirlo
      Serial.println("[Blynk] Token inválido: revisa BLYNK_AUTH_TOKEN en include/secrets.h.");
    } else {
      Serial.println("[Blynk] Sin conexión con el servidor por ahora. Se reintenta en segundo plano.");
    }
  }

  // Temporizador: publicar la temperatura cada 30 s (ver INTERVALO_ENVIO_MS)
  timer.setInterval(INTERVALO_ENVIO_MS, sendSensorData);
}

void loop() {
  Blynk.run(); // Mantiene la conexion con el servidor Blynk (y reconecta si se cae)
  timer.run(); // Ejecuta las tareas del temporizador
}
