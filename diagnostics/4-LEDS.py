from micropython import const
import machine
import utime
import LEDS

#cycles the LEDS on the controller chip
#tests: PCA9532 chip 0

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)

controller = LEDS.PCA9532(i2c, 0x60)

#NB requires that the resistor network RN4 and
#at least 1 LED connected to the chip have been installed

while(True):
     controller.all_on()
     utime.sleep_ms(100)
     controller.all_off()
     utime.sleep_ms(100)