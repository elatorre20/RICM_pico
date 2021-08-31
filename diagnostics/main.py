import time
import random
from machine import ADC, Pin      # Get the ADC and Pin libraries
from ws2812b import ws2812b

#Configuration variables for the LEDs
led_count = 9
led_state_machine = 0
led_pin = 16
led_brightness = 63 #Maximum brightness for the LEDs = 255
led_red = 0
led_green = 0
led_blue = 0

#Configure the potentiometer
potentiometer = machine.ADC(0)
conversion_factor = 255 / (65535)
led_brightness = int(potentiometer.read_u16() * conversion_factor)

print("\nConfiguring WS2812B on pin:", led_pin)
pixels = ws2812b(led_count, led_state_machine, led_pin, delay=0)

#Trap a ^c to stop the loop and turn off the LEDs
try:
    while(True):
        print("Writing random colors to WS2812B and rotating 1 LED position")
        loop = 1
        while(loop < 50):
            led_brightness = int(potentiometer.read_u16() * conversion_factor)
            led_red = random.randint(0,led_brightness)
            led_green = random.randint(0,led_brightness)
            led_blue = random.randint(0,led_brightness)
            pixels.rotate_right(1)
            pixels.set_pixel(0,led_red,led_green,led_blue)
            pixels.show()
            time.sleep_ms(150)
            loop = loop + 1

        print("Writing random color to random WS2812B LED")
        loop = 1
        while(loop < 100):
            led_brightness = int(potentiometer.read_u16() * conversion_factor)
            led = random.randint(0,8)
            led_red = random.randint(0,led_brightness)
            led_green = random.randint(0,led_brightness)
            led_blue = random.randint(0,led_brightness)
            pixels.set_pixel(led,led_red,led_green,led_blue)
            pixels.show()
            time.sleep_ms(150)
            loop = loop + 1
    
#A ^c was entered, so turn off the LEDs
except:
    print("Turning LEDs off")
    pixels.fill(0,0,0)
    pixels.show()
