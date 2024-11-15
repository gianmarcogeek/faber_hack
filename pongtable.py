import RPi.GPIO as GPIO
import time

# Configurazione dei pin (numerazione BOARD)
SERVO_PIN = 3  # Board pin 3
BUTTON_PIN = 5  # Board pin 5

GPIO.setmode(GPIO.BOARD)  # Usa la numerazione fisica dei pin
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN)  # Pull-up fisico gestito a livello hardware

# Configurazione PWM per il servo
pwm = GPIO.PWM(SERVO_PIN, 200)  # Frequenza a 50 Hz
pwm.start(5)  # Posizione iniziale: neutro (90°)

# Variabili di stato
positions = [5, 7.5, 10]  # Duty cycle per 0°, 90°, 180°
current_position = 0

# def button_pressed_callback(channel):
#     global current_position
#     current_position = (current_position + 1) % len(positions)
#     pwm.ChangeDutyCycle(positions[current_position])
#     print(f"Posizione attuale: {current_position * 90}°")

# # Configura l'evento del pulsante con debouncing
# GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # Mantieni attivo il programma
        pwm.ChangeDutyCycle(7.5)
        time.sleep(2) 
        pwm.ChangeDutyCycle(10)
        time.sleep(2) 
        pwm.ChangeDutyCycle(7.5)
        time.sleep(2)
        pwm.ChangeDutyCycle(5)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
