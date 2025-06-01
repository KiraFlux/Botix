#pragma once

#include "Arduino.h"

namespace colorsensor {

/// @brief Подветка датчика цвета
struct Lighting {
  /// @brief Пин подсветки
  const uint8_t pin_led;

  Lighting(uint8_t pin_led) : pin_led{pin_led} { pinMode(pin_led, OUTPUT); }

  void enable(bool state) const { digitalWrite(pin_led, state); }
};
}  // namespace colorsensor
