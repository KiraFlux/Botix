#pragma once

#include <stdint.h> // NOLINT(*-deprecated-headers)


namespace colorsensor {

    /// Масштабирование частоты
    enum Scaling : uint8_t {

        /// Масштабирование отключено
        off = 0b00,

        /// Масштабирование 2%
        p_02 = 0b01,

        /// Масштабирование 20%
        p_20 = 0b10,

        /// Масштабирование 100%
        p_100 = 0b11
    };
}