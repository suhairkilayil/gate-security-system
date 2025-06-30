import RPi.GPIO as GPIO
import time
import subprocess

SWITCH_1 = 0  # Facial recognition
SWITCH_2 = 5  # PIN lock
SWITCH_3 = 6  # Calling bell

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(["python3", script_name])

def start_blynk_stream():
    print("Starting Blynk Stream Control...")
    return subprocess.Popen(["python3", "blynk_stream_cntrl.py"])

blynk_process = start_blynk_stream()

try:
    print("Monitoring switch states...")
    while True:
        if GPIO.input(SWITCH_1) == GPIO.LOW:
            print("Stopping Blynk Stream for Facial Recognition...")
            blynk_process.terminate()
            blynk_process.wait()
            run_script("facial_detection.py")
            print("Restarting Blynk Stream...")
            blynk_process = start_blynk_stream()
            while GPIO.input(SWITCH_1) == GPIO.LOW:
                time.sleep(0.2)
        if GPIO.input(SWITCH_2) == GPIO.LOW:
            run_script("pin_lock.py")
            while GPIO.input(SWITCH_2) == GPIO.LOW:
                time.sleep(0.2)
        if GPIO.input(SWITCH_3) == GPIO.LOW:
            run_script("calling_bell.py")
            while GPIO.input(SWITCH_3) == GPIO.LOW:
                time.sleep(0.2)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    if blynk_process:
        blynk_process.terminate()
        blynk_process.wait()
