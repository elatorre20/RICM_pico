import machine
from machine import Pin, PWM
import utime
import random
import OLED
#from machine import Pin, PWM
#from utime import sleep

#from machine import ADC, Pin      # Get the ADC and Pin libraries

#displays the display ID on the OLED screens
#tests: OLED module 1

paddle_width = 20
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

oled_height = 64
oled_width = 128

# create a Pulse Width Modulation Object on this pin
speaker_pin = 7
speaker = PWM(Pin(speaker_pin))
tones = { "B0": 31,"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46, "G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,"C2": 65, "CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98, "GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139, "D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185, "G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,"DS4": 311, "E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698, "FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661, "A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520, "AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978 }

#Configure the ADCs for the sliders
sensor_slider_1 = machine.ADC(2)
sensor_slider_2 = machine.ADC(1)
conversion_factor = (oled_width-20) / (65535)

#Configure the I2C0 controller
sda=machine.Pin(20)
scl=machine.Pin(21)
i2c0=machine.I2C(0, sda=sda, scl=scl, freq=400000)

#Configure the I2C1 controller
sda=machine.Pin(18)
scl=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda, scl=scl, freq=400000)

#code for beeps
def playtone(frequency):
    speaker.duty_u16(32768)
    speaker.freq(frequency)

def bequiet():
    speaker.duty_u16(0)

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
    oled1 = OLED.SSD1306_I2C(oled_width, oled_height, i2c0, 0x3C)
    print("Powering on OLED DS1")
    oled1.poweron()
    print("Writing text to OLED DS1")
    oled1.text("screen 1", 0, 0)
    oled1.text("Micro PONG", 0, 10)
    print("Turning on OLED DS1 display")
    oled1.show()

    print("\nTesting OLED @ 0x3c on I2C1")
    print("Configuring OLED DS2")
    oled2 = OLED.SSD1306_I2C(oled_width, oled_height, i2c1, 0x3C)
    print("Powering on OLED DS2")
    oled2.poweron()
    print("Writing text to OLED DS2")
    oled2.text("screen 2", 0, 0)
    oled2.text("Micro PONG", 0, 10)
    print("Turning on OLED DS2 display")
    oled2.show()

    utime.sleep_ms(3000)
    
    playtone(tones["A5"])
    utime.sleep_ms(100)
    bequiet()

    while(True):
        ball_x = random.randint(0,oled_width - ball_width)
        direction = random.randint(0,1)
        if direction == 0:
            ball_x_increase = False
        else:
            ball_x_increase = True
        ball_y = 1
        ball_y_increase = True

        while(True):
            oled1.fill(0)
            oled1.hline(oled_width - paddle_width - paddle1_x,paddle1_y,paddle_width,paddle_color)
            oled1.rect(ball_x,ball_y,ball_width,ball_height,ball_color)
            oled1.show()
            
            oled2.fill(0)
            oled2.hline(paddle2_x,paddle2_y,paddle_width,paddle_color)
            oled2.rect(ball_x,ball_y,ball_width,ball_height,ball_color)
            oled2.show()

            #Ball at right side of screen
            if ball_x == (oled_width - ball_height):
                ball_x_increase = False
                playtone(tones["B5"])
                utime.sleep_ms(30)
                bequiet()

            #Ball at left side of screen
            if ball_x == 0:
                ball_x_increase = True
                playtone(tones["B5"])
                utime.sleep_ms(30)
                bequiet()

            if ball_x_increase:
                ball_x = ball_x + 1
            else:
                ball_x = ball_x - 1

            #Ball at bottom of screen
            if ball_y == (oled_height - ball_height):
                ball_y_increase = False
                playtone(tones["C5"])
                utime.sleep_ms(30)
                bequiet()

            #Ball almost at bottom of screen, check to see if it hit the paddle
            if ball_y == (oled_height - ball_height - 1):
                if ball_x >= (paddle2_x - ball_height):
                    if ball_x <= (paddle2_x + paddle_width):
                        ball_y_increase = False
                        playtone(tones["C5"])
                        utime.sleep_ms(30)
                        bequiet()

            #Ball at bottom of screen, didn't hit paddle so restart
            if ball_y == (oled_height - ball_height):
                playtone(tones["A4"])
                utime.sleep_ms(200)
                bequiet()
                break

            #Ball at to of screen
            if ball_y == 0:
                ball_y_increase = True
                playtone(tones["A5"])
                utime.sleep_ms(30)
                bequiet()

            if ball_y_increase:
                ball_y = ball_y + 1
            else:
                ball_y = ball_y - 1
            
            paddle1_x = int(sensor_slider_1.read_u16() * conversion_factor)
            paddle2_x = int(sensor_slider_2.read_u16() * conversion_factor)
