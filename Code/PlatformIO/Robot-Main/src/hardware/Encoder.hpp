#pragma once

#include "rustino/Pin.hpp"


namespace hardware {
    using namespace rustino::pins;
    using rustino::i32;

    struct Encoder {

        const Interrupt phase_a;
        const DigitalInput phase_b;
        volatile i32 position;

        constexpr Interrupt::AttachResult init(Interrupt::Handler handler) const {
            return phase_a.attach(handler, Event::Rising);
        }

        void onRisingPhaseA() {
            i32 d;

            if (phase_b.read() == State::High) {
                d = 1;
            } else {
                d = -1;
            }

            position += d;
        }
    };
}
