#makes some simple endlessly repeating patterns on the screen

# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
# Taken from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

from micropython import const
import framebuf
import machine
from utime import sleep 
from random import randint
import OLED
        
sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
    
#screensavers N.B. these are for a 32px
#half-height screen, change all the y max vals
#to 64 for the full-size 128*64 screen
    
def stars(screen, n=20):
    xpos = [0] * n
    ypos = [0] * n
    i = 0
    for j in range(n):
        x = randint(0, 127)
        y = randint(0, 32)
        xpos[j] = x
        ypos[j] = y
        screen.fill_rect(x,y,2,2,1)
        screen.show()
        sleep(1)
    while(True):
        x = randint(0, 127)
        y = randint(0, 32)
        screen.fill_rect(xpos[i],ypos[i],2,2,0)
        xpos[i] = x
        ypos[i] = y
        screen.fill_rect(x,y,2,2,1)
        screen.show()
        sleep(1)
        i = i + 1
        i = i % n
        
def letters(screen, n=20):
    xpos = [0] * n
    ypos = [0] * n
    i = 0
    for j in range(n):
        x = (randint(0, 127) // 8) * 8
        y = (randint(0, 24) // 8) * 8
        c = str(chr(randint(33, 126)))
        xpos[j] = x
        ypos[j] = y
        screen.text(c,x,y)
        screen.show()
        sleep(1)
    while(True):
        x = (randint(0, 127) // 8) * 8
        y = (randint(0, 24) // 8) * 8
        c = str(chr(randint(33, 126)))
        screen.fill_rect(xpos[i],ypos[i],8,8,0)
        xpos[i] = x
        ypos[i] = y
        screen.text(c,x,y)
        screen.show()
        sleep(1)
        i = i + 1
        i = i % n
        
def letterScan(screen, n=5, speed = 10):
    n = n + 1
    x = 0
    y = 0
    i = 33
    s = 1/speed
    while(True):
        #erase
        if((x - 8*n) < 0):
            erasex = (x - 8*n)
            lc = 1
            while(erasex < 0):
                erasex = erasex + 128
                lc = lc + 1
            erasey = - (8*lc)
            if(y < 8):
                erasey = 24
            else:
                erasey = y - 8
        else:
            erasex = (x - 8*n)
            erasey = y
        screen.fill_rect(erasex,erasey,9,8,0)
        #draw
        c = str(chr(i))
        screen.text(c,x,y)
        x = x + 8
        if(x > 127):
            x = x - 128
            y = y + 8
        if(y > 31):
            y = y - 32
        
        screen.show()
        sleep(s)
        if(i == 126):
            i = 32
        i = i + 1
        
        
        
def snake(screen, l=10, speed=6):
    x = 0
    y = 0
    s = 1/speed
    while(True):
        x = -l
        y = randint(0,31)
        while(x <= 128):
            screen.line(x,y,x+l,y,1)
            screen.line(x,y+1,x+l,y+1,1)
            screen.pixel(x-1, y, 0)
            screen.pixel(x-1, y+1, 0)
            screen.show()
            sleep(s)
            x = x + 1
            
        
    
    
    
oled = OLED.SSD1306_I2C(128, 64, i2c)

oled.poweron()

oled.fill(0)

oled.show()

snake(oled, 10)

    
    
    
    