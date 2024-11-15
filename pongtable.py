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

# Function to control servo sequence
def servo_sequence():
    # Init at 0°
    pwm.start(angle_to_percent(0))
    time.sleep(2)

    # Go at 90°
    pwm.ChangeDutyCycle(angle_to_percent(90))
    time.sleep(2)

    # Finish at 180°
    pwm.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(2)

    # Return to 0°
    pwm.ChangeDutyCycle(angle_to_percent(0))
    time.sleep(2)

try:
    print("Waiting for button press...")
    while True:
        button_state = GPIO.input(button_gpio)
        if button_state == GPIO.LOW:  # Button pressed (active low)
            print("Button pressed, starting servo sequence.")
            servo_sequence()
            print("Sequence completed, waiting for next press.")
        time.sleep(0.1)  # Small delay to debounce

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    # Close GPIO & cleanup
    pwm.stop()
    GPIO.cleanup()
