#pragma once

#include "rustino/Pin.hpp"


namespace hardware {

    using namespace rustino::pins;

    struct MotorDriver {
        enum class Direction { Forward = 0, Backward = 1 };

        const DigitalOutput direction_pin;
        const AnalogOutput enable_pin;
        const bool is_reversed;

        static MotorDriver New(Pin dir_pin, Pin pwm_pin, Direction direction = Direction::Forward) {
            return {
                .direction_pin = {dir_pin},
                .enable_pin = {pwm_pin},
                .is_reversed = static_cast<bool>(direction)
            };
        }

        AnalogOutput::InitResult init() const {
            const auto r = enable_pin.init();

            if (r.isOk()) {
                direction_pin.init();
            }

            return r;
        }

        void set(rustino::i16 power) const {
            setPower(abs(power));
            setDirection(static_cast<Direction>((power > 0)));
        }

    private:

        void setDirection(Direction direction) const {
            direction_pin.write(static_cast<State>(static_cast<bool>(direction) xor is_reversed));
        }

        void setPower(u8 pwm) const {
            enable_pin.write(constrain(pwm, 0, 255));
        }
    };
}