#include <Arduino.h>
#include <esp_arduino_version.h>

const uint8_t PIN_ADC = 32;       // GPIO32 para la lectura analógica
const uint8_t PIN_LED = 2;        // GPIO2 para el LED
const uint32_t LEDC_FREQ = 5000;  // Frecuencia de 5000 Hz
const uint8_t LEDC_RES = 8;       // Resolución de 8 bits (0 - 255)
const uint8_t LEDC_CHANNEL = 0;   // Canal LEDC (para versiones del Core < 3.0)

void setup() {
    Serial.begin(115200);
    delay(100);

    // Compatibilidad automática entre Core v2.x (PlatformIO) y v3.x (Wokwi Web)
    #if defined(ESP_ARDUINO_VERSION_MAJOR) && (ESP_ARDUINO_VERSION_MAJOR >= 3)
        ledcAttach(PIN_LED, LEDC_FREQ, LEDC_RES);
    #else
        ledcSetup(LEDC_CHANNEL, LEDC_FREQ, LEDC_RES);
        ledcAttachPin(PIN_LED, LEDC_CHANNEL);
    #endif
}

void loop() {
    // 1. Leer ADC (12 bits: 0 - 4095)
    uint16_t adc_val = analogRead(PIN_ADC);

    // 2. Reescalar lectura a 8 bits (0 - 255)
    uint8_t duty_val = map(adc_val, 0, 4095, 0, 255);

    // 3. Aplicar ciclo de trabajo
    #if defined(ESP_ARDUINO_VERSION_MAJOR) && (ESP_ARDUINO_VERSION_MAJOR >= 3)
        ledcWrite(PIN_LED, duty_val);
    #else
        ledcWrite(LEDC_CHANNEL, duty_val);
    #endif

    // 4. Cálculos para el reporte
    float porcentaje = (duty_val / 255.0f) * 100.0f;
    float v_medio = (duty_val / 255.0f) * 3.3f;

    // 5. Formato exacto: «[LEDC] adc=NNNN duty=NNN  PP.P% Vm=N.NNN V»
    char buffer[100];
    snprintf(buffer, sizeof(buffer), "[LEDC] adc=%4d duty=%3d  %4.1f%% Vm=%.3f V", 
             adc_val, duty_val, porcentaje, v_medio);

    Serial.println(buffer);

    delay(100);
}
