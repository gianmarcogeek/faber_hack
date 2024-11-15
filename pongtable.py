import RPi.GPIO as GPIO
import time

# Configurazione dei pin (numerazione BOARD)
SERVO_PIN = 3  # Pin BOARD collegato al servo

# Configurazione GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Configurazione PWM
pwm = GPIO.PWM(SERVO_PIN, 20)  # Frequenza a 50 Hz
pwm.start(7.5)  # Posizione iniziale: neutro (90°)

# Funzione per spostare il servo
def move_servo_and_stop(start_position, end_position, hold_time=1, delay=0.05, steps=20):
    step_size = (end_position - start_position) / steps  # Calcola il passo
    for i in range(steps + 1):
        position = start_position + step_size * i
        pwm.ChangeDutyCycle(position)
        time.sleep(delay)
    pwm.ChangeDutyCycle(end_position)  # Assicura la posizione finale
    print(f"Servo in posizione: {end_position}")
    time.sleep(hold_time)  # Mantiene la posizione per il tempo stabilito
    pwm.ChangeDutyCycle(0)  # Disattiva il segnale PWM
    print("Servo disattivato per risparmiare energia.")

try:
    # Movimento da 0° (duty cycle 5) a 180° (duty cycle 10)
    print("Inizio movimento...")
    move_servo_and_stop(5, 10)  # Da 0° a 180°, fermando il PWM dopo 1 secondo
    time.sleep(2)  # Attendi 2 secondi
    move_servo_and_stop(10, 5)  # Torna a 0°, fermando il PWM dopo 1 secondo
    print("Movimento completato!")
finally:
    pwm.stop()
    GPIO.cleanup()
