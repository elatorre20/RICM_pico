# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
# Taken from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

from micropython import const
import framebuf
import machine
import utime
import OLED

def img_read(filename):
    img = open(filename, 'rb')
    px = img.read()
    px = px[62:]
    array = bytearray(px)
    imgbuf = framebuf.FrameBuffer(array, 128,int((len(px)/16)), framebuf.MONO_HLSB)
    return(imgbuf)

sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
    
    
oled = OLED.SSD1306_I2C(128, 64, i2c)

oled.poweron()

oled.fill(0)

oled.show()

image = img_read('img/img.bmp')

oled.blit(image, 0,0)
oled.show()
