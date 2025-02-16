import pygame
import serial
import time

# Set Arduino COM Port
ARDUINO_PORT = 'COM9'  # Change if needed
BAUD_RATE = 9600

# Connect to Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow Arduino to initialize
    print(f"Connected to Arduino on {ARDUINO_PORT}")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Initialize pygame for joystick input
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No gamepad found. Make sure DS4Windows is running.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("PS4 Controller Connected! Waiting for joystick input...")

DEAD_ZONE = 0.2  # Ignore small joystick movements
last_command = None  # Track last sent command to avoid duplicates

while True:
    pygame.event.pump()

    # Get left joystick Y-axis movement
    axis_y = joystick.get_axis(1)  # Left stick vertical (Range: -1 to 1)

    if axis_y < -DEAD_ZONE:  # Joystick pushed forward (Move CW)
        if last_command != 'F':  # Prevent duplicate commands
            print("Joystick Forward → Sending 'F' to Arduino.")
            arduino.write(b'F')
            last_command = 'F'
    elif axis_y > DEAD_ZONE:  # Joystick pulled backward (Move CCW)
        if last_command != 'B':
            print("Joystick Backward → Sending 'B' to Arduino.")
            arduino.write(b'B')
            last_command = 'B'
    else:  # Joystick in neutral position
        if last_command != 'S':
            print("Joystick Released → Sending 'S' to Arduino.")
            arduino.write(b'S')
            last_command = 'S'

    # Detect Button Presses
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # X button
                print("X Button Pressed! Sending 'X' to Arduino.")
                arduino.write(b'X')
            elif event.button == 1:  # O button
                print("O Button Pressed! Sending 'O' to Arduino.")
                arduino.write(b'O')

    time.sleep(0.1)  # Prevent spamming
