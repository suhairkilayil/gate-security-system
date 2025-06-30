import RPi.GPIO as GPIO
import time

BUZZER = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

try:
    print("Buzzer is sounding...")
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER, GPIO.LOW)
    print("Buzzer stopped. Exiting program.")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.output(BUZZER, GPIO.LOW)
    GPIO.cleanup()
