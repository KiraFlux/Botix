#include "hardware/sensor/Line.hpp"
#include "hardware/MotorDriver.hpp"

#include "rustino/panic.hpp"
#include "Arduino.h"


void setup() {
    using rustino::pins::Pin;

    const auto driver = hardware::MotorDriver::New(Pin::D4, Pin::D5);

    if (driver.init().isFail()) {
        panic("driver init fail");
    }

    for (int i = 0, s = 255; i < 200; i++, s = -s) {
        driver.set(s);
    }


}

void loop() {}
