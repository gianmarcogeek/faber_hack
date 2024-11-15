import RPi.GPIO as GPIO
import time

# Configurazione dei pin (numerazione BOARD)
SERVO_PIN = 3  # Pin BOARD collegato al servo

# Configurazione GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Configurazione PWM
pwm = GPIO.PWM(SERVO_PIN, 50)  # Frequenza a 50 Hz
pwm.start(7.5)  # Posizione iniziale: neutro (90°)

# Funzione per spostare il servo
def move_servo(start_position, end_position, delay=0.05, steps=20):
    step_size = (end_position - start_position) / steps  # Calcola il passo
    for i in range(steps + 1):
        position = start_position + step_size * i
        pwm.ChangeDutyCycle(position)
        time.sleep(delay)
    pwm.ChangeDutyCycle(end_position)  # Assicura che resti nella posizione finale
    print(f"Movimento completato. Posizione finale: {end_position}")

try:
    # Movimento da 0° (duty cycle 5) a 180° (duty cycle 10)
    print("Inizio movimento...")
    move_servo(5, 10)  # Da 0° a 180°
    time.sleep(2)  # Attendi 2 secondi
    move_servo(10, 5)  # Torna a 0°
    print("Movimento completato!")
finally:
    pwm.stop()
    GPIO.cleanup()
