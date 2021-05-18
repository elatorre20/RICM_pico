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

def display_time(screen, f, number):
    screen.fill(0)
    if(len(number) > 4):
        screen.text('invalid time or format')
        return
    if(len(number) < 4):
        for i in range(4):
            number = '0' + number
            if(len(number) == 4):
                break
    for i in number:
        if (int(i) not in [0,1,2,3,4,5,6,7,8,9]):
            screen.text('invalid time or format')
            return
    d0 = int(number[0])
    d1 = int(number[1])
    d2 = int(number[2])
    d3 = int(number[3])
    screen.blit(f.digits[d0], 0,0)
    screen.blit(f.digits[d1], 31,0)
    screen.blit(f.digits[10], 62,0)
    screen.blit(f.digits[d2], 66, 0)
    screen.blit(f.digits[d3], 97,0)
    screen.show()
    
class font():
    #requires images for each digit to be loaded into
    # the /img folder, with the name 0.bmp to 9.bmp,
    # with the separator named colon.bmp
    def __init__(self):
        digits = []
        digits = digits + [img_read('img/0.bmp')]
        digits = digits + [img_read('img/1.bmp')]
        digits = digits + [img_read('img/2.bmp')]
        digits = digits + [img_read('img/3.bmp')]
        digits = digits + [img_read('img/4.bmp')]
        digits = digits + [img_read('img/5.bmp')]
        digits = digits + [img_read('img/6.bmp')]
        digits = digits + [img_read('img/7.bmp')]
        digits = digits + [img_read('img/8.bmp')]
        digits = digits + [img_read('img/9.bmp')]
        digits = digits + [img_read('img/colon.bmp')]
        self.digits = digits
    
def time_sweep(screen, f):
    for i in range(10000):
        j = str(i)
        display_time(screen, f, j)
        #utime.sleep(0.001)
        
def stopwatch(screen, f):
    minutes = 0
    seconds = 0
    number = ''
    while(True):
        number = ''
        if(minutes > 99):
            return
        if(seconds == 60):
            seconds = 0
            minutes = minutes + 1
        if(seconds < 10):
            number = '0' + str(seconds)
            number = str(minutes) + number
            display_time(screen, f, number)
            utime.sleep(1)
            seconds = seconds + 1
            continue
        else:
            number = str(minutes) + str(seconds)
            display_time(screen, f, number)
            utime.sleep(1)
            seconds = seconds + 1
            continue
        

sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
    
    
oled0 = OLED.SSD1306_I2C(128, 64, i2c, 0x3C)
oled1 = OLED.SSD1306_I2C(128, 64, i2c, 0x3D)

oled0.poweron()
oled1.poweron()

seg7 = font()

oled0.fill(0)
oled0.show()

oled1.fill(0)
oled1.show()

image = img_read('img/img.bmp')

oled1.blit(image, 0,0)
oled1.show()

stopwatch(oled0, seg7)
