import machine
import utime
import random
import OLED
from machine import ADC, Pin      # Get the ADC and Pin libraries

#displays the display ID on the OLED screens
#tests: OLED module 1

paddle_length = 20
paddle_color = 1
paddle1_x = 50
paddle1_y = 63
paddle2_x = 50
paddle2_y = 63

ball_x = 20
ball_x_increase = True 
ball_y = 20
ball_y_increase = True
ball_height = 5
ball_width = 5
ball_color = 1

#Configure the ADCs for the sliders
sensor_slider_1 = machine.ADC(2)
sensor_slider_2 = machine.ADC(1)
conversion_factor = (128-20) / (65535)

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
print("\nScanning I2C bus 1 on GP18 & GP19")
devices1 = i2c1.scan()
if len(devices1) == 0:
    print("\t No I2C1 devices found!")
else:
    print("\t I2C devices found:", len(devices1))
    for device1 in devices1:
        print("\t Decimal address:", device1, " | 7-bit hex address:", hex(device1))

if len(devices0) == 0 or len(devices1) == 0: 
    print("\nSome I2C1 devices not found!")
else:
    print("\nTesting OLED @ 0x3c on I2C0")
    print("Configuring OLED DS1")
    oled1 = OLED.SSD1306_I2C(128, 64, i2c0, 0x3C)
    print("Powering on OLED DS1")
    oled1.poweron()
    print("Writing text to OLED DS1")
    oled1.text("screen 1", 0, 0)
    oled1.text("Micro PONG", 0, 10)
    print("Turning on OLED DS1 display")
    oled1.show()

    print("\nTesting OLED @ 0x3c on I2C1")
    print("Configuring OLED DS2")
    oled2 = OLED.SSD1306_I2C(128, 64, i2c1, 0x3C)
    print("Powering on OLED DS2")
    oled2.poweron()
    print("Writing text to OLED DS2")
    oled2.text("screen 2", 0, 0)
    oled2.text("Micro PONG", 0, 10)
    print("Turning on OLED DS2 display")
    oled2.show()

    utime.sleep_ms(3000)

    while(True):
        oled1.fill(0)
        oled1.hline(128 - paddle_length - paddle1_x,paddle1_y,paddle_length,paddle_color)
        oled1.rect(ball_x,ball_y,ball_width,ball_height,ball_color)
        oled1.show()
        
        oled2.fill(0)
        oled2.hline(paddle2_x,paddle2_y,paddle_length,paddle_color)
        oled2.rect(ball_x,ball_y,ball_width,ball_height,ball_color)
        oled2.show()

        if ball_x == (128 - ball_height):
            ball_x_increase = False

        if ball_x == 0:
            ball_x_increase = True

        if ball_x_increase:
            ball_x = ball_x + 1
        else:
            ball_x = ball_x - 1

        if ball_y == (64 - ball_height):
            ball_y_increase = False

        if ball_y == 0:
            ball_y_increase = True

        if ball_y_increase:
            ball_y = ball_y + 1
        else:
            ball_y = ball_y - 1
        
        paddle1_x = int(sensor_slider_1.read_u16() * conversion_factor)
        paddle2_x = int(sensor_slider_2.read_u16() * conversion_factor)