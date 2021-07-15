from micropython import const
import framebuf
import machine
import utime
import OLED

sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
    
    
oled0 = OLED.SSD1306_I2C(128, 64, i2c, 0x3C)
oled1 = OLED.SSD1306_I2C(128, 64, i2c, 0x3D)

oled0.poweron()
oled1.poweron()

oled0.text("screen 0", 0, 0)
oled1.text("screen 1", 0, 0)

oled0.show()
oled1.show()