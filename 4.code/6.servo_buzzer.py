import pigpio
import time

servo_pin = 19
buzzer_pin = 16
pi = pigpio.pi()

def set_angle(angle):
    pulse_width = 500 + (angle * 2000 // 180)
    pi.set_servo_pulsewidth(servo_pin, pulse_width)
    time.sleep(0.5)

def buzz(duration):
    pi.write(buzzer_pin, 1)
    time.sleep(duration)
    pi.write(buzzer_pin, 0)

pi.set_mode(buzzer_pin, pigpio.OUTPUT)

try:
    buzz(0.2)
    set_angle(90)
    print("Gate opened")
    time.sleep(10)
    buzz(1.0)
    set_angle(0)
    print("Gate closed")
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(servo_pin, 0)
    pi.write(buzzer_pin, 0)
    pi.stop()
