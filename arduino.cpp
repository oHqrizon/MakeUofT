#include <Servo.h>
#include <Stepper.h>

#define STEPS 200  // Steps per revolution (adjust for your stepper)

Servo myServo;
Stepper stepperMotor(STEPS, 8, 10, 9, 11);  // Change pins if needed

const int servoPin = 6;
int servoAngle = 90;  // Start at middle position
int stepperDirection = 0;  // 0 = Stop, 1 = CW, -1 = CCW

void setup() {
    Serial.begin(9600);
    myServo.attach(servoPin);
    myServo.write(servoAngle);  // Set initial position
    stepperMotor.setSpeed(40);  // Adjust stepper speed (RPM)
    Serial.println("Waiting for input...");
}

void loop() {
    // Step 1: Read Serial Input
    if (Serial.available() > 0) {
        char command = Serial.read();
        Serial.print("Received: ");
        Serial.println(command);

        // Servo Control (+45° / -45° with X and O Buttons)
        if (command == 'X' && servoAngle < 180) {
            servoAngle += 90;  // Increase by 45°
            Serial.print("Rotating Servo to: ");
            Serial.println(servoAngle);
            myServo.write(servoAngle);
            delay(500);
        }
        else if (command == 'O' && servoAngle > 0) {
            servoAngle -= 90;  // Decrease by 45°
            Serial.print("Rotating Servo to: ");
            Serial.println(servoAngle);
            myServo.write(servoAngle);
            delay(500);
        }

        // Stepper Motor Control (Joystick)
        if (command == 'F') {  // Move Stepper Forward (Clockwise)
            stepperDirection = 1;
        } 
        else if (command == 'B') {  // Move Stepper Backward (Counterclockwise)
            stepperDirection = -1;
        } 
        else if (command == 'S') {  // Stop Stepper
            stepperDirection = 0;
        }
    }

    // Step 2: Move Stepper Motor Continuously While Joystick is Held
    if (stepperDirection == 1) {
        stepperMotor.step(5);  // Small step forward
    }
    else if (stepperDirection == -1) {
        stepperMotor.step(-5);  // Small step backward
    }
}
