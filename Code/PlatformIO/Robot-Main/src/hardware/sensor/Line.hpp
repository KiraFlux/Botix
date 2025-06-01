#pragma once

#include "rustino/Pin.hpp"
#include "rustino/primitives.hpp"


namespace hardware {
    using namespace rustino::pins;
    using namespace rustino;

    namespace sensor {
        struct Line {
            constexpr static u8 gray = 128;

            const AnalogInput pin;
            const u16 on_field;
            const u16 on_line;

            u8 read() const {
                u16 v = pin.read();

                const i32 i = (v - on_line) << 8;
                const i16 b = on_field - on_line;

                return i / b;
            }
        };
    }
}