#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time

# Set function to calculate percent from angle
def angle_to_percent(angle):
    if angle > 180 or angle < 0:
        return False

    start = 4
    end = 12.5
    ratio = (end - start) / 180  # Calculate ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

# GPIO setup
GPIO.setmode(GPIO.BOARD)  # Use Board numerotation mode
GPIO.setwarnings(False)  # Disable warnings

# Setup for PWM and button
pwm_gpio = 12  # PWM signal pin
button_gpio = 3  # Button pin
frequence = 50

GPIO.setup(pwm_gpio, GPIO.OUT)
GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Setup button with pull-up resistor
pwm = GPIO.PWM(pwm_gpio, frequence)

# Function to move servo to a specific angle
def move_servo_to(angle):
    duty_cycle = angle_to_percent(angle)
    if duty_cycle:
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Allow the servo to reach the position
        pwm.ChangeDutyCycle(0)  # Stop sending PWM signal

# Function to control servo sequence in normal order
def servo_sequence_normal():
    pwm.start(0)  # Initialize with no signal
    move_servo_to(0)    # Move to 0°
    move_servo_to(90)   # Move to 90°
    move_servo_to(180)  # Move to 180°
    move_servo_to(0)    # Return to 0°
    pwm.stop()  # Stop PWM after sequence

# Function to control servo sequence in reverse order
def servo_sequence_reverse():
    pwm.start(0)  # Initialize with no signal
    move_servo_to(0)    # Start at 0°
    move_servo_to(180)  # Move to 180°
    move_servo_to(90)   # Move to 90°
    move_servo_to(0)    # Return to 0°
    pwm.stop()  # Stop PWM after sequence

# Track state for sequence direction
sequence_normal = True

try:
    print("Waiting for button press...")
    while True:
        button_state = GPIO.input(button_gpio)
        if button_state == GPIO.LOW:  # Button pressed (active low)
            print("Button pressed, starting servo sequence.")
            if sequence_normal:
                servo_sequence_normal()
            else:
                servo_sequence_reverse()
            # Toggle sequence direction
            sequence_normal = not sequence_normal
            print("Sequence completed, waiting for next press.")
        time.sleep(0.1)  # Small delay to debounce

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    # Close GPIO & cleanup
    pwm.stop()
    GPIO.cleanup()
