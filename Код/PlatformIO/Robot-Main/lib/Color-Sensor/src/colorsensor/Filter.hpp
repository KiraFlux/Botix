#pragma once

#include <stdint.h> // NOLINT(*-deprecated-headers)


namespace colorsensor {

    /// Цветовой фильтр
    enum Filter : uint8_t {

        /// Фильтр красного цвета
        red = 0b00,

        /// Фильтр синего цвета
        blue = 0b01,

        /// Фильтр общего цвета (Отключен)
        clean = 0b10,

        /// Фильтр зеленого цвета
        green = 0b11
    };
}