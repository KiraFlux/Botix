#pragma once

#include "Arduino.h"


#define panic(msg) ({Serial.println("Panic: " #msg ); while(true) {}})
