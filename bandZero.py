import lgpio
import time

try:
    h = lgpio.gpiochip_open(0)  
except lgpio.LgpioError as e:
    print(f"Fehler beim Öffnen des GPIO-Chips: {e}")
    exit(1)

PULSE_PIN = 20
DIR_PIN = 16
ENABLE_PIN = 21

try:
    lgpio.gpio_claim_output(h, PULSE_PIN)
    lgpio.gpio_claim_output(h, DIR_PIN)
    lgpio.gpio_claim_output(h, ENABLE_PIN)
except OSError as e:
    print(f"Fehler beim Anlegen der GPIOs: {e}")
    exit(1)

lgpio.gpio_write(h, DIR_PIN, 0)
lgpio.gpio_write(h, ENABLE_PIN, 0)

def moveBandBySteps(steps):
    for x in range(steps):
        lgpio.gpio_write(h, PULSE_PIN, 1)
        time.sleep(0.01)
        lgpio.gpio_write(h, PULSE_PIN, 0)
        time.sleep(0.01)  

def moveBandBySteps_Auto(steps):
    lgpio.gpio_write(h, DIR_PIN, 0)
    moveBandBySteps(steps)

def moveBandByStepsforward(steps):
    lgpio.gpio_write(h, DIR_PIN, 0)
    moveBandBySteps(steps)

def moveBandByStepsBackward(steps):
    lgpio.gpio_write(h, DIR_PIN, 1)
    moveBandBySteps(steps)

 

def clearGPIOS():
    lgpio.gpiochip_close(h)