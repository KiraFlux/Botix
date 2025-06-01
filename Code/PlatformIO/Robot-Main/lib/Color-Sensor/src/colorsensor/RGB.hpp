#pragma once

#include "Arduino.h"


namespace colorsensor {
    /// Значения частот
    struct RGB {
        const float r, g, b;

        /// На сколько показания частот отличаются
        float difference(const RGB &other) const {
            float delta_r = r - other.r;
            float delta_g = g - other.g;
            float delta_b = b - other.b;

            return (delta_r * delta_r) + (delta_g * delta_g) + (delta_b * delta_b);
        }
    };
}