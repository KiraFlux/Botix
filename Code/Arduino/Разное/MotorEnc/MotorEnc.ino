#define PIN_MOTOR_DIR 7
#define PIN_MOTOR_SPEED 6
#define PIN_ENC_A 3
#define PIN_ENC_B 8

#define DT 0.01
struct PID {
  float kp, ki, kd, max_i;
  float integral = 0;
  int old_error = 0;

  PID (float p, float i, float d, float mi) : kp(p), ki(i), kd(d), max_i(mi) {}
  
  int calc(int error) {
    integral += error * DT * ki;
    integral = constrain(integral, -max_i, max_i);
    float diff = (error - old_error) * kd / DT;
    return error * kp + integral + diff;
  }
};

PID pwm_pid(0.5, 0.01, 0.002, 100);
PID pos_pid(0.1, 0.01, 0, 0.8);

volatile long ticks = 0;
long target = 0;
long next = 0;
int delta = 0;

void set_pwmdir(int pwm_dir) {
  int pwm = constrain(abs(pwm_dir), 0, 255);
  analogWrite(PIN_MOTOR_SPEED, pwm);
  digitalWrite(PIN_MOTOR_DIR, pwm_dir > 0);
}

void reg_update() {
  int p_ret = pos_pid.calc(target - ticks);
  next += constrain(p_ret, -delta, delta);
  set_pwmdir(pwm_pid.calc(next - ticks));
}

long calcDelta() {
  static long old_ticks = 0;
  long ret = ticks - old_ticks;
  old_ticks = ticks;
  return ret;
}

void encoder_int() {
  if (digitalRead(PIN_ENC_B)) ticks++;
  else ticks--;
}

void setup() {
  pinMode(PIN_MOTOR_DIR, OUTPUT);
  pinMode(PIN_MOTOR_SPEED, OUTPUT);
  pinMode(PIN_ENC_A, INPUT);
  pinMode(PIN_ENC_B, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), encoder_int, RISING);

  Serial.begin(9600);

  target = 1000;
  delta = 5;
}

#define PT(x) Serial.print(x); Serial.print('\t')

void loop() {
  delay(1000 * DT);
  reg_update();
  
  if (Serial.available()) {
    char mode = Serial.read();
    if (mode == 'd') delta = Serial.parseInt();
    if (mode == 't') target = Serial.parseInt();
  }
  
  PT(calcDelta());
  PT(delta);
  PT(ticks);
  Serial.println(target);
}
