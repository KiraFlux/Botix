// Copyright (c) 2026 KiraFlux
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

namespace botix::protocol {

enum class Kind : unsigned char {
    Raw = 0x00,
    Mavlink = 0x01,
};

}