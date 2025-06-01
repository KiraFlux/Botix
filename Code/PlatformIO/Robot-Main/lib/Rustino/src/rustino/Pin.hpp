#pragma once

#include <Arduino.h>
#include "primitives.hpp"


namespace rustino {
    /// Пины
    namespace pins {

        enum class Pin : u8 {
            D0 = 0,
            D1 = 1,
            D2 = 2,
            D3 = 3,
            D4 = 4,
            D5 = 5,
            D6 = 6,
            D7 = 7,
            D8 = 8,
            D9 = 9,
            D10 = 10,
            D11 = 11,
            D12 = 12,
            D13 = 13,
            A0 = PIN_A0,
            A1 = PIN_A1,
            A2 = PIN_A2,
            A3 = PIN_A3,
            A4 = PIN_A4,
            A5 = PIN_A5,
        };

        /// Режим работы пина
        enum class Mode : u8 { Input = INPUT, Output = OUTPUT, InputPullUp = INPUT_PULLUP };

        /// Состояние пина
        enum class State : u8 { High = HIGH, Low = LOW };

        /// Событие на пине
        enum class Event : u8 { Low = LOW, Rising = RISING, Falling = FALLING, Change = CHANGE };

        template<typename E> struct Result {
            E result;

            constexpr bool isOk() const { return result == static_cast<E>(0); }

            constexpr bool isFail() const { return not isOk(); }
        };

        /// Общий пин (только инициализация
        struct GenericPin {
            const Pin pin;

            void init(Mode mode) const {
                pinMode(getNumber(), static_cast<u8>(mode));
            }

            constexpr inline u8 getNumber() {
                return static_cast<u8>(pin);
            }

            constexpr inline bool hasPWM() const {
                return digitalPinHasPWM(getNumber());
            }
        };

        /// Только цифровой выход
        struct DigitalOutput {
            const GenericPin pin;

            void init() const {
                pin.init(Mode::Output);
            }

            void write(State state) const {
                digitalWrite(pin.getNumber(), static_cast<bool>(state));
            }
        };

        /// Только цифровой вход
        struct DigitalInput {
            const GenericPin pin;

            void init(bool is_pull_up = false) const {
                pin.init(is_pull_up ? Mode::InputPullUp : Mode::Input);
            }

            State read() const {
                return static_cast<State>(digitalRead(pin.getNumber()));
            }
        };

        /// Пин с прерыванием
        struct Interrupt {
            enum class AttachError : u8 { Ok = 0, PinNotSupport };
            using AttachResult = Result<AttachError>;
            using Handler = void();

            const DigitalInput input;

            AttachResult attach(Handler handler, Event event) const {
                const int i = digitalPinToInterrupt(input.pin.getNumber());

                if (i == NOT_AN_INTERRUPT) {
                    return {AttachError::PinNotSupport};
                }

                attachInterrupt(i, handler, static_cast<int>(event));
                return {AttachError::Ok};
            }
        };

        /// Только Аналоговый вход
        struct AnalogInput {
            using Value = u16;

            const GenericPin pin;

            void init() const {
                pin.init(Mode::Output);
            }

            Value read() const {
                return analogRead(pin.getNumber());
            }
        };

        /// Только Аналоговый Выход
        struct AnalogOutput {
            enum class InitError : u8 { Ok = 0, NotSupportPWM };

            using InitResult = Result<InitError>;
            using Value = u8;

            const GenericPin pin;

            InitResult init() const {
                if (pin.hasPWM()) {
                    pin.init(Mode::Input);
                    return {InitError::Ok};
                }

                return {InitError::NotSupportPWM};
            }

            void write(Value pwm) const {
                analogWrite(pin.getNumber(), pwm);
            }
        };
    }
}
