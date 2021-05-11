from machine import Pin
from machine import Timer

clk = Pin(16, Pin.OUT)
enb = Pin(17, Pin.OUT)
data = Pin(18, Pin.OUT)

clock = Timer(1, Timer.PWM)
