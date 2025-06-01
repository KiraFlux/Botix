#pragma once

#include <Adafruit_TCS34725.h>

#include <colorsensor/Lighting.hpp>
#include <colorsensor/RGB.hpp>

namespace colorsensor {

struct SensorTCS3472 {
  mutable Adafruit_TCS34725 tcs;
  const Lighting lighting;

  RGB readComponent() const {
    uint16_t r, g, b, c;
    tcs.setInterrupt(false);  // turn on LED

    delay(50);  // takes 50m

    tcs.getRawData(&r, &g, &b, &c);

    tcs.setInterrupt(true);  // turn off LED
    
    auto clear = float(c);
    auto red = float(r) / clear;
    auto blue = float(b) / clear;
    auto green = float(g) / clear;

    return (RGB){.r = red, .g = green, .b = blue};
  }
};

}  // namespace colorsensor