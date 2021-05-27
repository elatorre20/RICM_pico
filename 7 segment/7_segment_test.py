from micropython import const
import machine
import utime
import LEDS

sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=1000)

controller = LEDS.PCA9532(i2c, 0x60)

while(True):
    controller.all_on()
    utime.sleep_ms(100)
    controller.all_off()
    utime.sleep_ms(100)