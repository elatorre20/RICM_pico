import time
import random

from ws2812b import ws2812b

num_leds = 9
state_machine = 0
pin = 16

print("\nConfiguring WS2812B on pin:", pin)
pixels = ws2812b(num_leds, state_machine, pin, delay=0)

x = 0
y = 0
z = 0

print("Writing random colors to WS2812B and rotating 1 LED position")
loop = 1
while(loop < 50):
    x = random.randint(0,63)
    y = random.randint(0,63)
    z = random.randint(0,63)
    pixels.rotate_right(1)
    pixels.set_pixel(0,x,y,z)
    pixels.show()
    time.sleep_ms(150)
    loop = loop + 1

print("Writing random color to random WS2812B LED")
loop = 1
while(loop < 100):
    led = random.randint(0,8)
    x = random.randint(0,63)
    y = random.randint(0,63)
    z = random.randint(0,63)
    pixels.set_pixel(led,x,y,z)
    pixels.show()
    time.sleep_ms(150)
    loop = loop + 1
    
print("Turning LEDs off")
pixels.fill(0,0,0)
pixels.show()
