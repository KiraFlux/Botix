#pragma once

#include "panic.hpp"
#include "primitives.hpp"


namespace rustino {

    template<typename T> struct Option {
        const bool is_some;
        u8 some[sizeof(T)];

        static Option<T> None() {
            return {
                .is_some = false,
                .some = {0}
            };
        }

        static Option<T> Some(T value) {
            Option ret = {
                .is_some = true,
                .some = {0}
            };

            *reinterpret_cast<T *>(ret.some) = value;

            return ret;
        }

        const T &unwrap() const {
            if (is_some) { return some; }
            panic("Option is None");
        }

    private:
        const T &getSome() const {
            return *reinterpret_cast<const T *>(some);
        }
    };
}