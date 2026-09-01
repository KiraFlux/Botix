// Copyright (c) 2026 KiraFlux
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <kf/core.hpp>
#include <kf/gpio.hpp>

#include "botix/driver/sensor/Lidar.hpp"

#include "botix/unit/Kind.hpp"
#include "botix/unit/Unit.hpp"

namespace botix::unit {

// TODO: CRTP-base DriverUnit<Driver, kind>. needs Driver with init, quit, Dependencies
// TODO: ActuatorDriverUnit, SensorDriverUnit

/// @brief Lidar Unit
/// @note Uses Lidar driver
struct LidarUnit : Unit {

    using Driver = botix::driver::sensor::Lidar;

    struct Dependencies {
        Driver::Dependencies const &driver;
        Index index;
    };

    LidarUnit(Dependencies const &deps) noexcept :
        Unit{Kind::Lidar, deps.index},
        _driver{deps.driver} {}

    [[nodiscard]] decltype(auto) config() const noexcept {
        return _driver.config();
    }

    [[nodiscard]] decltype(auto) read() noexcept {
        return _driver.read();
    }

protected:
    bool onInit() noexcept override {
        _driver.init();
        // TODO: wait for _driver.running() ?
        return true;
    }

    void onQuit() noexcept override {
        _driver.quit();
        // TODO: wait for _driver.running() ?
    }

private:
    Driver _driver;
};

}// namespace botix::unit