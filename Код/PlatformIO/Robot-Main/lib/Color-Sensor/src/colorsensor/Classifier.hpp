#pragma once

#include "colorsensor/RGB.hpp"
#include "colorsensor/ColorSensor.hpp"


namespace colorsensor {

    /// Классификатор объектов по цветам
    template<class T> struct Classifier {

        /// Описание объекта
        struct Object {

            /// Содержимое значение объекта
            T value;

            /// Компонент частот цвета
            RGB component;
        };

        const uint8_t objects_len;
        const Object objects[];

        /// Получить значение по цвету объекта
        const Object &getValue(const RGB &component) {
            return objects[getObjectIndex(component)];
        }

    private:
        uint8_t getObjectIndex(const RGB &component) {
            uint8_t ret = 0;
            uint32_t difference;

            uint32_t min_value = objects[0].component.difference(component);

            for (uint8_t index = 1; index < objects_len; index++) {
                difference = objects[index].component.difference(component);

                if (difference < min_value) {
                    min_value = difference;
                    ret = index;
                }
            }

            return ret;
        }
    };
}