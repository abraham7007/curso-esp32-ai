#include "Led.h"
#include <esp_arduino_version.h>

const uint32_t LED_PWM_FREQ = 5000;  // 5 kHz
const uint8_t LED_PWM_RES = 8;       // 8 bits (0 - 255)
const uint8_t LED_PWM_CHANNEL = 0;   // Canal LEDC (para versiones del Core < 3.0)

Led::Led(uint8_t pin) : _pin(pin), _state(false) {
}

void Led::begin() {
    pinMode(_pin, OUTPUT);
    digitalWrite(_pin, LOW);
    _state = false;

    // Compatibilidad automática entre Core v2.x (PlatformIO) y v3.x (Wokwi Web)
    #if defined(ESP_ARDUINO_VERSION_MAJOR) && (ESP_ARDUINO_VERSION_MAJOR >= 3)
        ledcAttach(_pin, LED_PWM_FREQ, LED_PWM_RES);
    #else
        ledcSetup(LED_PWM_CHANNEL, LED_PWM_FREQ, LED_PWM_RES);
        ledcAttachPin(_pin, LED_PWM_CHANNEL);
    #endif
}

void Led::on() {
    digitalWrite(_pin, HIGH);
    _state = true;
}

void Led::off() {
    digitalWrite(_pin, LOW);
    _state = false;
}

bool Led::toggle() {
    if (_state) {
        off();
    } else {
        on();
    }
    return _state;
}

bool Led::isOn() const {
    return _state;
}

void Led::escribirPWM(uint8_t duty) {
    #if defined(ESP_ARDUINO_VERSION_MAJOR) && (ESP_ARDUINO_VERSION_MAJOR >= 3)
        ledcWrite(_pin, duty);
    #else
        ledcWrite(LED_PWM_CHANNEL, duty);
    #endif
    _state = (duty > 0);
}
