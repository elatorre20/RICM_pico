#Scans for I2C devices on bus I2C0 and I2C1
#Reads switches on the PCA9555s and changes the color of the corresponding LEDs

import utime
import GPIO
import random
from ws2812b import ws2812b
import OLED
from machine import ADC, Pin      # Get the ADC and Pin libraries

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

#Configure the I2C0 controller
sda=machine.Pin(20)
scl=machine.Pin(21)
i2c0=machine.I2C(0, sda=sda, scl=scl, freq=400000)

#Configure the I2C1 controller
sda=machine.Pin(18)
scl=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda, scl=scl, freq=400000)

#Scan I2C0 and report devices found
print("\nScanning I2C bus 0 on GP20 & GP21")
devices0 = i2c0.scan()
if len(devices0) == 0:
    print("\t No I2C devices found!")
else:
    print("\t I2C devices found:", len(devices0))
    for device0 in devices0:
        print("\t Decimal address:", device0, " | 7-bit heled_red address:", hex(device0))

#Scan I2C1 and report devices found
print("Scanning I2C bus 1 on GP18 & GP19")
devices1 = i2c1.scan()
if len(devices1) == 0:
    print("\t No I2C1 devices found!")
else:
    print("\t I2C devices found:", len(devices1))
    for device1 in devices1:
        print("\t Decimal address:", device1, " | 7-bit hex address:", hex(device1))

#Try to configure the PCA9555 on I2C0
gpio0 = GPIO.PCA9555(i2c0, 0x20)
try:
    print("\nConfiguring PCA9555 @ 0x20 on I2C0")
    gpio0.setup_inputs()
    print("Switches SW1 through SW9 will work")
except OSError:
    print("Could not configure PCA9555 @ 0x20 on I2C0")    
    print("Switches SW1 through SW9 will not work")

#Try to configure the PCA9555 on I2C1
gpio1 = GPIO.PCA9555(i2c1, 0x21)
try:
    print("Configuring PCA9555 @ 0x21 on I2C1")
    gpio1.setup_inputs()
    print("Switches SW10 through SW18 will work")
except OSError:
    print("Could not configure PCA9555 @ 0x21 on I2C1")    
    print("Switches SW10 through SW18 will not work")

#Configure the OLEDs
print("Configuring the OLED 1 @ 0x3c on I2C0")
oled1 = OLED.SSD1306_I2C(128, 64, i2c0, 0x3C)
oled1.poweron()
oled1.text("screen 1", 0, 0)
oled1.show()
print("Configuring the OLED 2 @ 0x3c on I2C1")
oled2 = OLED.SSD1306_I2C(128, 64, i2c1, 0x3C)
oled2.poweron()
oled2.text("screen 2", 0, 0)
oled2.show()

#Configure the LEDs
print("Configuring WS2812B LEDs on pin:", led_pin)
pixels = ws2812b(led_count, led_state_machine, led_pin, delay=0)

print("\nPress the buttons one at a time to randomly change the corresponding LED color")
print("The potentiometer will control the LED brightness")
print("Enter ^c to quit.\n")
utime.sleep_ms(2000)
pixels.fill(led_brightness,led_brightness,led_brightness)
pixels.show()

#Trap a ^c to stop the loop and turn off the LEDs
try:
    while(True):
        utime.sleep_ms(200)
        led_brightness = int(potentiometer.read_u16() * conversion_factor)
        led_red = random.randint(0,led_brightness)
        led_green = random.randint(0,led_brightness)
        led_blue = random.randint(0,led_brightness)
        
        gpio0input0 = gpio0.reg_read(GPIO.INPUT0)
        gpio0input1 = gpio0.reg_read(GPIO.INPUT1)
        gpio1input0 = gpio1.reg_read(GPIO.INPUT0)
        gpio1input1 = gpio1.reg_read(GPIO.INPUT1)

        if gpio0input0 != "0b11111111":
            bit = gpio0.reg_bit(GPIO.INPUT0, 0)
            if bit == "0b0":
                pixels.set_pixel(8,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 9", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 1)
            if bit == "0b0":
                pixels.set_pixel(7,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 8", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 2)
            if bit == "0b0":
                pixels.set_pixel(6,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 7", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 3)
            if bit == "0b0":
                pixels.set_pixel(5,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 6", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 4)
            if bit == "0b0":
                pixels.set_pixel(4,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 5", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 5)
            if bit == "0b0":
                pixels.set_pixel(3,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 4", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 6)
            if bit == "0b0":
                pixels.set_pixel(2,led_red,led_green,led_blue)
                pixels.show()
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 3", 0, 0)
                oled2.show()
            bit = gpio0.reg_bit(GPIO.INPUT0, 7)
            if bit == "0b0":
                pixels.set_pixel(1,led_red,led_green,led_blue)
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 2", 0, 0)
                oled2.show()
        elif gpio0input1 != "0b11111111":
            bit = gpio0.reg_bit(GPIO.INPUT1, 0)
            if bit == "0b0":
                pixels.set_pixel(0,led_red,led_green,led_blue)
                pixels.show()
                pixels.show()
                oled2.fill(0)
                oled2.text("Switch 1", 0, 0)
                oled2.show()
        elif gpio1input0 != "0b11111111":
            bit = gpio1.reg_bit(GPIO.INPUT0, 0)
            if bit == "0b0":
                pixels.set_pixel(0,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 10", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 1)
            if bit == "0b0":
                pixels.set_pixel(1,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 11", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 2)
            if bit == "0b0":
                pixels.set_pixel(2,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 12", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 3)
            if bit == "0b0":
                pixels.set_pixel(3,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 13", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 4)
            if bit == "0b0":
                pixels.set_pixel(4,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 14", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 5)
            if bit == "0b0":
                pixels.set_pixel(5,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 15", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 6)
            if bit == "0b0":
                pixels.set_pixel(6,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 16", 0, 0)
                oled1.show()
            bit = gpio1.reg_bit(GPIO.INPUT0, 7)
            if bit == "0b0":
                pixels.set_pixel(7,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 17", 0, 0)
                oled1.show()
        elif gpio1input1 != "0b11111111":
            bit = gpio1.reg_bit(GPIO.INPUT1, 0)
            if bit == "0b0":
                pixels.set_pixel(8,led_red,led_green,led_blue)
                pixels.show()
                oled1.fill(0)
                oled1.text("Switch 18", 0, 0)
                oled1.show()


#A ^c was entered, so turn off the LEDs
except:
    pixels.fill(0,0,0)
    pixels.show()