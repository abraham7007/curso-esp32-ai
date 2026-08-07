#include <Arduino.h>
#include <esp_arduino_version.h>

const uint8_t PIN_ADC   = 32;   // GPIO32 para la lectura del potenciómetro
const uint8_t PIN_SERVO = 18;   // GPIO18 para la señal PWM del servo

const uint32_t SERVO_FREQ    = 50;  // 50 Hz -> periodo de 20 ms (estándar para servos)
const uint8_t  SERVO_RES     = 16;  // Resolución de 16 bits (0 - 65535)
const uint8_t  SERVO_CHANNEL = 0;   // Canal LEDC (para versiones del Core < 3.0)

const uint16_t PULSO_MIN_US = 1000;                    // Pulso para 0°
const uint16_t PULSO_MAX_US = 2000;                    // Pulso para 180°
const uint32_t PERIODO_US   = 1000000UL / SERVO_FREQ;  // 20000 us
const uint32_t DUTY_MAX     = (1UL << SERVO_RES) - 1;  // 65535

void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println();
    Serial.println("Iniciando control de servo por PWM (potenciometro -> angulo)");

    // Compatibilidad automática entre Core v2.x (PlatformIO) y v3.x (Wokwi Web)
    #if defined(ESP_ARDUINO_VERSION_MAJOR) && (ESP_ARDUINO_VERSION_MAJOR >= 3)
        ledcAttach(PIN_SERVO, SERVO_FREQ, SERVO_RES);
    #else
        ledcSetup(SERVO_CHANNEL, SERVO_FREQ, SERVO_RES);
        ledcAttachPin(PIN_SERVO, SERVO_CHANNEL);
    #endif
}

void loop() {
    // 1. Leer ADC (12 bits: 0 - 4095)
    uint16_t adc_val = analogRead(PIN_ADC);

    // 2. Reescalar la lectura a un ángulo de servo (0° - 180°)
    uint16_t angulo = map(adc_val, 0, 4095, 0, 180);

    // 3. Convertir el ángulo a ancho de pulso (1000 - 2000 us) y luego a duty
    uint32_t pulso_us = map(angulo, 0, 180, PULSO_MIN_US, PULSO_MAX_US);
    uint32_t duty = (pulso_us * DUTY_MAX) / PERIODO_US;

    // 4. Aplicar el ciclo de trabajo
    #if defined(ESP_ARDUINO_VERSION_MAJOR) && (ESP_ARDUINO_VERSION_MAJOR >= 3)
        ledcWrite(PIN_SERVO, duty);
    #else
        ledcWrite(SERVO_CHANNEL, duty);
    #endif

    // 5. Formato exacto: «[SERVO] adc=NNNN angulo=NNN pulso=NNNNus duty=NNNNN»
    char buffer[100];
    snprintf(buffer, sizeof(buffer), "[SERVO] adc=%4d angulo=%3d  pulso=%4lu us  duty=%5lu",
             adc_val, angulo, (unsigned long)pulso_us, (unsigned long)duty);
    Serial.println(buffer);

    // Muestreo a 10 Hz
    delay(100);
}
