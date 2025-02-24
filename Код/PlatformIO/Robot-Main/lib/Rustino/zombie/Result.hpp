#pragma once

#include "panic.hpp"
#include "primitives.hpp"
#include "Option.hpp"


namespace rustino {
    template<typename T, typename E> struct Result {
        const bool is_ok;
        u8 data[max(sizeof(T), sizeof(E))];

        static Result ok(T value) {
            Result ret = {
                .is_ok = false,
                .data = {0}
            };
            *reinterpret_cast<T *>(ret.data) = value;

            return ret;
        }

        static Result err(E error) {
            Result ret = {
                .is_ok = false,
                .data = {0}
            };
            *reinterpret_cast<E *>(ret.data) = error;

            return ret;
        }

        const T &unwrapOr(T &&default_value) const {
            return is_ok ? getValue() : default_value;
        }

        const T &unwrap() const {
            if (is_ok) {
                return getValue();
            }

            panic("Result is Error");
        }

        Option<T> ok() const {
            return is_ok ? Option<T>::Some(getValue()) : Option<T>::None();
        }

        Option<E> err() const {
            return (not is_ok) ? Option<E>::Some(getError()) : Option<E>::None();
        }

    private:
        const E &getError() const {
            return *reinterpret_cast<const E *>(data);
        }

        const T &getValue() const {
            return *reinterpret_cast<const T *>(data);
        }
    };
}
