#include "colorsensor/ColorSensor.hpp"
#include "colorsensor/Classifier.hpp"
#include "Arduino.h"


colorsensor::ColorSensor sensor(10, 11, 12, 13, A2, A3);

colorsensor::Classifier<const char *> classifier{
    4, {
        {"BLUE", {72, 58, 35}},
        {"GREEN", {88, 61, 66}},
        {"YELLOW", {47, 71, 122}},
        {"RED", {33, 90, 70}},
    }
};

void setup() {
    sensor.setFrequencyScaling(colorsensor::Scaling::p_100);
    sensor.enableLighting(false);

    Serial.begin(9600);
    delay(1000);

    sensor.enableLighting(true);
}

#define DBG(x) Serial.print("\t" #x ": "); Serial.print(x)

void loop() {
    auto c = sensor.readComponent();
    auto &v = classifier.getValue(c);

    DBG(c.r);
    DBG(c.g);
    DBG(c.b);
    DBG(v.value);
    Serial.println();

    delay(50);
}
