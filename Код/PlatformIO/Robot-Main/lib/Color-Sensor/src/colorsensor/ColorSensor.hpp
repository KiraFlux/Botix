#pragma once

#include <wiring_private.h>
#include "colorsensor/Scaling.hpp"
#include "colorsensor/Filter.hpp"
#include "colorsensor/RGB.hpp"
#include "Arduino.h"

/// Модуль датчика цвета
namespace colorsensor {

    /// Датчик цвета
    class ColorSensor {

    public:

        using u8 = uint8_t;

    private:

        /// Пины контроллера
        const u8 s0, s1, s2, s3;

        /// Выход частоты
        const u8 pin_out;

        /// Управление подсветкой
        const u8 pin_led;

    public:

        explicit ColorSensor(u8 s_0, u8 s_1, u8 s_2, u8 s_3, u8 pin_out, u8 pin_led) :
            s0(s_0), s1(s_1), s2(s_2), s3(s_3),
            pin_out(pin_out), pin_led(pin_led) {
            pinMode(s_0, OUTPUT);
            pinMode(s_1, OUTPUT);
            pinMode(s_2, OUTPUT);
            pinMode(s_3, OUTPUT);
            pinMode(pin_out, INPUT);
            pinMode(pin_led, OUTPUT);
        }

        /// Включить подсветку
        void enableLighting(bool state) const {
            digitalWrite(pin_led, state);
        }

        /// Установить масштабирование частоты
        void setFrequencyScaling(Scaling scaling) const {
            digitalWrite(s0, (scaling & 0b10) > 0);
            digitalWrite(s1, scaling & 0b01);
        }

        /// Считать компонент частот составного цвета
        RGB readComponent() const {
            return {
                .r = readFrequency(Filter::red),
                .g = readFrequency(Filter::green),
                .b = readFrequency(Filter::blue)
            };
        }

    private:

        /// Считать частоту с заданным фильтром
        uint32_t readFrequency(Filter filter) const {
            digitalWrite(s2, (filter & 0b10) > 0);
            digitalWrite(s3, filter & 0b01);
            return pulseIn(pin_out, LOW, 100000UL);
        }
    };
}