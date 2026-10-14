#include <Arduino.h>

const uint8_t PIN_RX2 = 16;
const uint8_t PIN_TX2 = 17;

const uint8_t HEADER = 0xAA;

// Variables para la máquina de estados del receptor
enum EstadoReceptor { ESPERANDO_CABECERA, LEYENDO_ID, LEYENDO_LONGITUD, LEYENDO_CARGA, LEYENDO_CHECKSUM };
EstadoReceptor estado = ESPERANDO_CABECERA;

uint8_t rx_id = 0;
uint8_t rx_longitud = 0;
uint8_t rx_carga[256];
uint8_t rx_indice_carga = 0;
uint8_t rx_checksum_calculado = 0;

unsigned long ultimoEnvio = 0;
bool enviarConError = false; // Alternar entre enviar tramas buenas y malas
uint8_t contadorPaquetes = 0;

// Función para calcular el checksum (Suma aritmética simple módulo 256)
uint8_t calcularChecksum(uint8_t id, uint8_t longitud, uint8_t* carga) {
    uint8_t suma = id + longitud;
    for (int i = 0; i < longitud; i++) {
        suma += carga[i];
    }
    return suma;
}

// Función para imprimir una trama en formato hexadecimal
void imprimirTramaHex(const char* prefijo, uint8_t id, uint8_t longitud, uint8_t* carga, uint8_t checksum, bool valida) {
    Serial.print(prefijo);
    Serial.printf(" [AA %02X %02X ", id, longitud);
    for(int i=0; i<longitud; i++) {
        Serial.printf("%02X ", carga[i]);
    }
    Serial.printf("%02X] -> ", checksum);
    if(valida) Serial.println("ACEPTADA");
    else Serial.println("RECHAZADA (Checksum erróneo)");
}

void enviarTrama() {
    uint8_t id = contadorPaquetes++;
    String texto = "Hola " + String(id);
    uint8_t longitud = texto.length();
    uint8_t carga[longitud + 1]; // +1: getBytes() escribe también el terminador nulo
    texto.getBytes(carga, longitud + 1);

    uint8_t checksum = calcularChecksum(id, longitud, carga);

    // Función que altera un byte para provocar rechazo
    if (enviarConError) {
        Serial.print("[ENVIANDO CON ERROR INTENCIONAL] ");
        carga[0] ^= 0xFF; // Corrompemos el primer byte de la carga
    } else {
        Serial.print("[ENVIANDO CORRECTO] ");
    }

    // Transmitimos por Serial2
    Serial2.write(HEADER);
    Serial2.write(id);
    Serial2.write(longitud);
    for (int i = 0; i < longitud; i++) {
        Serial2.write(carga[i]);
    }
    Serial2.write(checksum);

    imprimirTramaHex("Tx:", id, longitud, carga, checksum, !enviarConError);
    
    enviarConError = !enviarConError; // Alternamos para la próxima vez
}

void procesarReceptor() {
    while (Serial2.available() > 0) {
        uint8_t byteRecibido = Serial2.read();

        switch (estado) {
            case ESPERANDO_CABECERA:
                if (byteRecibido == HEADER) {
                    estado = LEYENDO_ID;
                }
                break;

            case LEYENDO_ID:
                rx_id = byteRecibido;
                estado = LEYENDO_LONGITUD;
                break;

            case LEYENDO_LONGITUD:
                rx_longitud = byteRecibido;
                rx_indice_carga = 0;
                if (rx_longitud > 0) {
                    estado = LEYENDO_CARGA;
                } else {
                    estado = LEYENDO_CHECKSUM;
                }
                break;

            case LEYENDO_CARGA:
                rx_carga[rx_indice_carga++] = byteRecibido;
                if (rx_indice_carga >= rx_longitud) {
                    estado = LEYENDO_CHECKSUM;
                }
                break;

            case LEYENDO_CHECKSUM:
                uint8_t checksumRecibido = byteRecibido;
                rx_checksum_calculado = calcularChecksum(rx_id, rx_longitud, rx_carga);
                
                bool valida = (checksumRecibido == rx_checksum_calculado);
                imprimirTramaHex("Rx:", rx_id, rx_longitud, rx_carga, checksumRecibido, valida);
                
                estado = ESPERANDO_CABECERA; // Reiniciar máquina de estados
                break;
        }
    }
}

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, PIN_RX2, PIN_TX2);
    Serial.println("\n--- TRAMAS UART CON CHECKSUM INICIADO ---");
}

void loop() {
    // Enviamos una trama cada 3 segundos
    if (millis() - ultimoEnvio > 3000) {
        enviarTrama();
        ultimoEnvio = millis();
    }

    // Procesar datos entrantes constantemente
    procesarReceptor();
}
