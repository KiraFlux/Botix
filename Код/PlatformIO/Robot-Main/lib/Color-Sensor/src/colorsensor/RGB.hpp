#pragma once

#include "Arduino.h"


namespace colorsensor {
    /// Значения частот
    struct RGB {
        const uint32_t r, g, b;

        /// На сколько показания частот отличаются
        uint32_t difference(const RGB &other) const {
            int32_t delta_r = r - other.r;
            int32_t delta_g = g - other.g;
            int32_t delta_b = b - other.b;

            return abs(delta_r) + abs(delta_g) + abs(delta_b);
        }
    };
}