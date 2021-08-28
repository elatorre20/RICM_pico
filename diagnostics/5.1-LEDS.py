from micropython import const
import machine
import utime
import LEDS

#Blinks all LEDs successively
#tests: both PCA9532 LED chips at once

sda0=machine.Pin(20)
scl0=machine.Pin(21)
i2c0=machine.I2C(0, sda=sda0, scl=scl0, freq=400000)

controller0 = LEDS.PCA9532(i2c0, 0x60)

sda1=machine.Pin(18)
scl1=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda1, scl=scl1, freq=400000)

controller1 = LEDS.PCA9532(i2c1, 0x61)

#NB requires that the resistor network RN4 and
#All LEDS have been connected

for i in [LEDS.LS0, LEDS.LS1, LEDS.LS2, LEDS.LS3]:
    j = 1
    while j < 256:
        controller0.reg_write(i,j)
        utime.sleep_ms(500)
        j = (j*4)+1
        
controller0.all_off()
        
for i in [LEDS.LS0, LEDS.LS1, LEDS.LS2, LEDS.LS3]:
    j = 1
    while j < 256:
        controller1.reg_write(i,j)
        utime.sleep_ms(500)
        j = (j*4)+1
        
controller1.all_off()
controller0.all_off()

