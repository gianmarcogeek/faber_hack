import RPi.GPIO as GPIO
import time

# Configurazione dei GPIO
SERVO_PIN = 3  # Pin PWM per il servomotore
BUTTON_PIN = 5  # Pin per il pulsante

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up interno attivato

# Configurazione PWM per il servomotore
pwm = GPIO.PWM(SERVO_PIN, 50)  # Frequenza a 50 Hz
pwm.start(7.5)  # Posizione iniziale a 90°

# Variabili per il controllo
positions = [5, 7.5, 10]  # Duty cycle per 0°, 90°, 180°
current_position = 0

def button_pressed_callback(channel):
    global current_position
    current_position = (current_position + 1) % len(positions)
    pwm.ChangeDutyCycle(positions[current_position])
    print(f"Posizione attuale: {current_position * 90}°")

# Configurazione dell'evento per il pulsante
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # Mantieni il programma attivo
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
