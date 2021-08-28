import utime
import GPIO
import random
from ws2812b import ws2812b

#Scans for I2C devices on bus I2C0
#Reads switches on the PCA9555 and changes the color of the corresponding LEDs

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)

print("\nScanning I2C bus 0 on GP20 & GP21")
devices = i2c.scan()

if len(devices) == 0:
    print("\tNo I2C devices found!")
else:
    print("\tI2C devices found:", len(devices))

for device in devices:
    print("\tDecimal address:", device, " | 7-bit hex address:", hex(device))

print("\nUsing PCA9555 @ 0x20")

gpio0 = GPIO.PCA9555(i2c, 0x20)
gpio0.setup_inputs()

num_leds = 9
state_machine = 0
pin = 16
x = 0
y = 0
z = 0

print("Using WS2812B LEDs on pin:", pin)
pixels = ws2812b(num_leds, state_machine, pin, delay=0)
pixels.fill(0,0,50)
pixels.show()

print("\nPress the buttons one at a time to randomly change the corresponding LED color")
print("Enter ^c to quit.\n")
utime.sleep_ms(2000)

while(True):
    utime.sleep_ms(200)
    x = random.randint(0,63)
    y = random.randint(0,63)
    z = random.randint(0,63)
    gpio0input0 = gpio0.reg_read(GPIO.INPUT0)
    gpio0input1 = gpio0.reg_read(GPIO.INPUT1)
    if gpio0input0 != "0b11111111":
        bit = gpio0.reg_bit(GPIO.INPUT0, 0)
        if bit == "0b0":
            pixels.set_pixel(8,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 1)
        if bit == "0b0":
            pixels.set_pixel(7,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 2)
        if bit == "0b0":
            pixels.set_pixel(6,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 3)
        if bit == "0b0":
            pixels.set_pixel(5,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 4)
        if bit == "0b0":
            pixels.set_pixel(4,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 5)
        if bit == "0b0":
            pixels.set_pixel(3,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 6)
        if bit == "0b0":
            pixels.set_pixel(2,x,y,z)
            pixels.show()
        bit = gpio0.reg_bit(GPIO.INPUT0, 7)
        if bit == "0b0":
            pixels.set_pixel(1,x,y,z)
            pixels.show()
    elif gpio0input1 != "0b11111111":
        bit = gpio0.reg_bit(GPIO.INPUT1, 0)
        if bit == "0b0":
            pixels.set_pixel(0,x,y,z)
            pixels.show()
