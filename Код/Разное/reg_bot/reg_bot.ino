void setMotors(int L, int R) {
	L = constrain(L, -255, 255);
	R = constrain(R, -255, 255);
	digitalWrite(4, L < 0);
	digitalWrite(7, R < 0);
	analogWrite(5, abs(L));
	analogWrite(6, abs(R));
}

void setMotorsU(int base, int u) {
	setMotors(base + u, base - u);
}

#define BREAK_MOTORS_ITERATIONS 16
#define BREAK_MOTORS_PERIOD 8

void breakMotors() {
	for (int i = 0, k = 255; i < BREAK_MOTORS_ITERATIONS; i++, k *= -1) {
		setMotors(k, k);
		delay(BREAK_MOTORS_PERIOD);
	}
	setMotors(0, 0);
}

int readLineL() {return analogRead(A1);}

int readLineR() {return analogRead(A0);}

bool getWall() {return not digitalRead(8);}

#define ON_LINE_BORDER 800

int onLine(int line_value) {return line_value < ON_LINE_BORDER;}

bool onLineL() {return onLine(readLineL());}

bool onLineR() {return onLine(readLineR());}

int calcLineError() {return readLineL() - readLineR();}

void algRelayLeft(int base, int other) {
	if (onLineL()) {
		setMotors(other, base);
	} else {
		setMotors(base, other);
	}
}

void algRelayRight(int base, int other) {
	if (onLineR()) {
		setMotors(base, other);
	} else {
		setMotors(other, base);
	}
}

void algRelayBoth(int base, int other) {
	if (onLineL() == onLineR()) {
		setMotors(base, base);
	} else if (onLineL()) {
		setMotors(other, base);
	} else {
		setMotors(base, other);
	}
}

#define P2_K 0.4
#define P2_D 0.5

void algPD(int base) {
	static int last_error = 0;
	int error = calcLineError();	
	setMotorsU(base, (error * P2_K) + (error - last_error) * P2_D);
	last_error = error;
	delay(10);
}

void lineTime(uint32_t runtime, int speed = 255) {
	runtime += millis();
	while (millis() < runtime) {
		algPD(speed);
	}
	breakMotors();
}

void lineCross(int speed = 255) {
	while(not (onLineL() and onLineR())) {
		algPD(255);     
	}
	breakMotors();
}

void lineToWall(int speed = 255) {
	while(not getWall()) {
		algPD(speed);
	}
	breakMotors();
}

void goTime(uint32_t runtime, int speed = 255) {
	setMotors(speed, speed);
	delay(runtime);
	breakMotors();
}

void align(uint32_t duration = 500) {
	duration += millis();
	
	while (millis() < duration) {
		setMotorsU(0, calcLineError());
	}
	
	breakMotors();
}

void turnL(int speed = 255) {
	setMotors(-speed, speed);
	while (not onLineL()) {}
	align();
}

void turnR(int speed = 255) {
	setMotors(speed, -speed);
	while (not onLineR()) {}
	align();
}

void wallToLine(int speed = 255) {
	while (not (onLineL() or onLineR())) {
		if (getWall()) {
			setMotors(0, speed);
		} else {
			setMotors(speed, 0);
		}
	}
	breakMotors();
}

void go() {
	lineCross();
	lineTime(300);
}

void goL() {
	go();
	turnL();
}

void goR() {
	go();
	turnR();
}

void setup() {
	pinMode(4, OUTPUT);
	pinMode(5, OUTPUT);
	pinMode(6, OUTPUT);
	pinMode(7, OUTPUT);
	pinMode(8, INPUT);
	pinMode(A0, INPUT);
	pinMode(A1, INPUT);
	Serial.begin(9600);
	
	// task
	lineTime(400);
	goL();
	goL();
	goR();
	lineToWall();
	wallToLine();
	goR();
	lineCross();
	goTime(500);

}

void loop() {}
