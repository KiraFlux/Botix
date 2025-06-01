#pragma once

#include "colorsensor/RGB.hpp"

namespace colorsensor {

    /// Классификатор объектов по цветам
    template<class T> struct Classifier {

        /// Описание объекта
        struct Item {

            /// Содержимое значение объекта
            T value;

            /// Компонент частот цвета
            RGB component;
        };

        const uint8_t items_len;
        const Item items[];

        /// Получить значение по цвету объекта
        const Item &getItem(const RGB &component) const {
            return items[getItemIndex(component)];
        }

    private:
        uint8_t getItemIndex(const RGB &component) const {
            uint8_t ret = 0;
            float difference;

            float min_value = items[0].component.difference(component);

            for (uint8_t index = 1; index < items_len; index++) {
                difference = items[index].component.difference(component);

                if (difference < min_value) {
                    min_value = difference;
                    ret = index;
                }
            }

            return ret;
        }
    };
}