import subprocess
from gpiozero import DigitalOutputDevice, Button
import smbus
import time
import RPi.GPIO as GPIO
import os
import signal

I2C_ADDR = 0x27
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
ENABLE = 0b00000100
E_DELAY = 0.0005

GPIO.setmode(GPIO.BCM)
rows_pins = [17, 18, 27, 22]
cols_pins = [25, 12, 13, 26]
keys = [["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]]

class LCD:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.lcd_init()
    def lcd_init(self):
        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD)
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x0C, LCD_CMD)
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)
        time.sleep(E_DELAY)
    def lcd_byte(self, bits, mode):
        BACKLIGHT = 0x08
        high_bits = mode | (bits & 0xF0) | ENABLE
        low_bits = mode | ((bits << 4) & 0xF0) | ENABLE
        self.bus.write_byte(I2C_ADDR, high_bits)
        self.lcd_toggle_enable(high_bits)
        self.bus.write_byte(I2C_ADDR, low_bits)
        self.lcd_toggle_enable(low_bits)
    def lcd_toggle_enable(self, bits):
        time.sleep(E_DELAY)
        self.bus.write_byte(I2C_ADDR, (bits & ~ENABLE) | 0x08)
        time.sleep(E_DELAY)
    def lcd_display_string(self, message, line):
        message = message.ljust(LCD_WIDTH, " ")
        if line == 1:
            self.lcd_byte(LCD_LINE_1, LCD_CMD)
        elif line == 2:
            self.lcd_byte(LCD_LINE_2, LCD_CMD)
        for char in message:
            self.lcd_byte(ord(char), LCD_CHR)
    def lcd_clear(self):
        self.lcd_byte(0x01, LCD_CMD)

lcd = LCD()
rows = [DigitalOutputDevice(pin) for pin in rows_pins]
cols = [Button(pin, pull_up=False) for pin in cols_pins]
CORRECT_PIN = "5234"

def read_keypad():
    entered_pin = ""
    lcd.lcd_display_string("Enter PIN:", 1)
    lcd.lcd_display_string(" ", 2)
    while len(entered_pin) < 4:
        for row_index, row in enumerate(rows):
            row.on()
            for col_index, col in enumerate(cols):
                if col.is_pressed:
                    key = keys[row_index][col_index]
                    entered_pin += key
                    lcd.lcd_display_string("*" * len(entered_pin), 2)
                    time.sleep(0.3)
            row.off()
    return entered_pin

def trigger_gate():
    lcd.lcd_display_string("Gate Opening...", 1)
    lcd.lcd_display_string("Welcome!", 2)
    subprocess.run(["python3", "servo_buzzer.py"])
    time.sleep(2)
    lcd.lcd_clear()
    terminate_script()

def terminate_script():
    lcd.lcd_display_string("System Off", 1)
    time.sleep(1)
    GPIO.cleanup()
    os.kill(os.getpid(), signal.SIGTERM)

try:
    while True:
        entered_pin = read_keypad()
        if entered_pin == CORRECT_PIN:
            trigger_gate()
        else:
            lcd.lcd_display_string("Incorrect PIN", 1)
            lcd.lcd_display_string("Try Again", 2)
            time.sleep(2)
            lcd.lcd_clear()
except KeyboardInterrupt:
    terminate_script()
