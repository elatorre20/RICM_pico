import machine
import utime
import OLED

#displays the display ID on the OLED screens
#tests: OLED module 0

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)
    
    
oled0 = OLED.SSD1306_I2C(128, 64, i2c, 0x3C)

oled0.poweron()

oled0.text("screen 0", 0, 0)

oled0.show()