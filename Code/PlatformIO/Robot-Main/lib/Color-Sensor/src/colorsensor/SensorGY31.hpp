#pragma once

#include "colorsensor/Filter.hpp"
#include "colorsensor/Lighting.hpp"
#include "colorsensor/RGB.hpp"
#include "colorsensor/Scaling.hpp"

#include "Arduino.h"

/// Модуль датчика цвета
namespace colorsensor {

/// Датчик цвета
struct SensorGY31 {
 public:
  using u8 = uint8_t;

 private:
  /// Пины контроллера
  const u8 s0, s1, s2, s3;

  /// Выход частоты
  const u8 pin_out;

 public:
  /// Управление подсветкой
  const Lighting lighting;

  explicit SensorGY31(u8 s_0,
                      u8 s_1,
                      u8 s_2,
                      u8 s_3,
                      u8 pin_out,
                      Lighting pin_led)
      : s0(s_0),
        s1(s_1),
        s2(s_2),
        s3(s_3),
        pin_out(pin_out),
        lighting(lighting) {
    pinMode(s_0, OUTPUT);
    pinMode(s_1, OUTPUT);
    pinMode(s_2, OUTPUT);
    pinMode(s_3, OUTPUT);
    pinMode(pin_out, INPUT);
  }

  /// Установить масштабирование частоты
  void setFrequencyScaling(Scaling scaling) const {
    digitalWrite(s0, (scaling & 0b10) > 0);
    digitalWrite(s1, scaling & 0b01);
  }

  /// Считать компонент частот составного цвета
  RGB readComponent() const {
    auto clear = float(readFrequency(Filter::clean));
    auto r = float(readFrequency(Filter::red));
    auto g = float(readFrequency(Filter::green));
    auto b = float(readFrequency(Filter::blue));

    return {.r = r / clear, .g = g / clear, .b = b / clear};
  }

 private:
  /// Считать частоту с заданным фильтром
  uint32_t readFrequency(Filter filter) const {
    digitalWrite(s2, (filter & 0b10) > 0);
    digitalWrite(s3, filter & 0b01);
    return pulseIn(pin_out, LOW, 100000UL);
  }
};
}  // namespace colorsensor