#include "Arduino.h"


const int left_phase_a = 2, left_phase_b = 8, left_speed = 5, left_dir = 4;

const int right_phase_a = 3, right_phase_b = 9, right_speed = 6, right_dir = 7;

const int left_line = A0, right_line = A1;

volatile long left_current_position = 0, right_current_position = 0;

long left_target_position = 0, right_target_position = 0;

void on_left_encoder_phase_a_rising() {
    if (digitalRead(left_phase_b)) {
        left_current_position++;
    } else {
        left_current_position--;
    }
}

void on_right_encoder_phase_a_rising() {
    if (digitalRead(left_phase_b)) {
        right_current_position++;
    } else {
        right_current_position--;
    }
}

void setup() {
    Serial.begin(9600);

    // Инициализация левого мотор-энкодера
    pinMode(left_phase_a, INPUT);
    pinMode(left_phase_b, INPUT);
    pinMode(left_dir, OUTPUT);
    pinMode(left_speed, OUTPUT);
    attachInterrupt(digitalPinToInterrupt(left_phase_a), on_left_encoder_phase_a_rising, RISING);

    // Инициализация правого мотор-энкодера
    pinMode(right_phase_a, INPUT);
    pinMode(right_phase_b, INPUT);
    pinMode(right_dir, OUTPUT);
    pinMode(right_speed, OUTPUT);
    attachInterrupt(digitalPinToInterrupt(right_phase_a), on_right_encoder_phase_a_rising, RISING);
}

void setMotors(long L, long R) {
    L = constrain(L, -255, 255);
    digitalWrite(left_dir, L < 0);
    analogWrite(left_speed, abs(L));

    R = constrain(R, -255, 255);
    digitalWrite(right_dir, R < 0);
    analogWrite(right_speed, abs(R));
}

bool isEncoderReady(long error) {
    const int max_error = 5;
    return abs(error) < max_error;
}

bool isMotorsMoving() {
    bool right_motor_ready = isEncoderReady(right_target_position - right_current_position);
    bool left_motor_ready = isEncoderReady(left_target_position - left_current_position);
    return not(right_motor_ready and left_motor_ready);
}

void resetEncoders() {
    left_current_position = 0;
    right_current_position = 0;
}

long calcPower(long error) {
    const int position_kp = 8;
    return error * position_kp;
}

void updateMotors(int L, int R) {
    const int update_period_ms = 20;
    delay(update_period_ms);

    left_target_position += L;
    right_target_position += R;

    long left_power = calcPower(left_target_position - left_current_position);
    long right_power = calcPower(right_target_position - right_current_position);

    setMotors(left_power, right_power);
}

void goTime(int L, int R, unsigned long run_time_ms) {
    unsigned long end_time_ms = millis() + run_time_ms;

    resetEncoders();

    while (millis() < end_time_ms) {
        updateMotors(L, R);
    }

    setMotors(0, 0);
}

void stop(unsigned long stop_time_ms = 500) {
    goTime(0, 0, stop_time_ms);
}

void goTick(long L, long R, int speed) {
    resetEncoders();

    left_target_position = L;
    right_target_position = R;

    while (isMotorsMoving()) {
        updateMotors(speed, speed);
    }

    stop();
}

long mmToTicks(long mm) {
    const long ticks_ride = 500;
    const long mm_ridden = 126;
    return (mm * ticks_ride) / mm_ridden;
}

void goDist(long left_mm, long right_mm, int speed) {
    goTick(mmToTicks(left_mm), mmToTicks(right_mm), speed);
}

void turnAngle(int angle, int speed) {
    const int track_width_mm = 250;
    long path_mm = M_PI * angle * track_width_mm / 360;
    goDist(-path_mm, path_mm, speed);
}

int readLeftLine() {
    return analogRead(left_line);
}

int readRightLine() {
    return analogRead(right_line);
}

void lineFollowRegulator(int speed) {
    const float kp = 0.02; // Коэф. подобрать
    int u = (readLeftLine() - readRightLine()) * kp;
    updateMotors(speed + u, speed - u);
}

void lineTime(unsigned long run_time_ms, int speed) {
    unsigned long end_time_ms = millis() + run_time_ms;

    resetEncoders();

    while (millis() < end_time_ms) {
        lineFollowRegulator(speed);
    }

    stop();
}

void lineDist(long distance_mm, int speed) {
    resetEncoders();

    const long double_target_position = mmToTicks(distance_mm) * 2;
    long error;

    do {
        lineFollowRegulator(speed);
        error = left_current_position + right_current_position - double_target_position;
    } while (isEncoderReady(error));

    stop();
}

bool isLine(int line_value) {
    const int gray = 500;
    return line_value > gray;
}

void align(unsigned long align_durations_ms = 1000) {
    lineTime(align_durations_ms, 0);
}

void lineTurnLeft(int speed) {
    resetEncoders();

    while (not isLine(readLeftLine())) {
        updateMotors(-speed, speed);
    }

    align();
}

void lineTurnRight(int speed) {
    resetEncoders();

    while (not isLine(readRightLine())) {
        updateMotors(speed, -speed);
    }

    align();
}


void loop() {}
