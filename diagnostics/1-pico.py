from machine import Pin
from utime import sleep

#blinks the onboard LED
#tests: pico

led = Pin(25, Pin.OUT)

while(True):
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)
    
