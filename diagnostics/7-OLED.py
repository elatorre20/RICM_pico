import machine
import utime
import OLED

#displays the display ID on the OLED screens
#tests: OLED module 1

sda=machine.Pin(18)
scl=machine.Pin(19)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
    
    
oled1 = OLED.SSD1306_I2C(128, 64, i2c, 0x3C)

oled1.poweron()

oled1.text("screen 1", 0, 0)

oled1.show()