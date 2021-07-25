import time
import random
from ws2812b import ws2812b

num_leds = 6
pixels = ws2812b(num_leds, 0,16, delay=0)

x = 0
y = 0
z = 0

while(True):
    for i in range(num_leds):
        x = random.randint(0,63)
        y = random.randint(0,63)
        z = random.randint(0,63)
        pixels.set_pixel(i,x,y,z)
        pixels.show()
    time.sleep_ms(1000)
    
    
