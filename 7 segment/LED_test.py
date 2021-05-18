from machine import Pin, PWM
from machine import Timer
from utime import sleep

red = PWM(Pin(18))
green = PWM(Pin(17))
blue = PWM(Pin(16))


red.freq(1000)
green.freq(1000)
blue.freq(1000)


def sweep(r,g,b):
    while(True):
        for brightness in range(65025):
            r.duty_u16(brightness)
            sleep(0.0001)
        for brightness in range(65025, 0, -1):
            r.duty_u16(brightness)
            sleep(0.0001)
        for brightness in range(65025):
            g.duty_u16(brightness)
            sleep(0.0001)
        for brightness in range(65025, 0, -1):
            g.duty_u16(brightness)
            sleep(0.0001)
        for brightness in range(65025):
            b.duty_u16(brightness)
            sleep(0.0001)
        for brightness in range(65025, 0, -1):
            b.duty_u16(brightness)
            sleep(0.0001)
            
def display_color(color, r = red, g = green, b = blue):
    if color_translate(color) != None:
        color = color_translate(color)
        r.duty_u16(int(color[0] * 65025))
        g.duty_u16(int(color[1] * 65025))
        b.duty_u16(int(color[2] * 65025))
    else:
        color = color_rgb(color)
        r.duty_u16(int(color[0] * 65025))
        g.duty_u16(int(color[1] * 65025))
        b.duty_u16(int(color[2] * 65025))
        
def color_translate(color):
    if(color == 'RED'):
        return([1,0,0])
    if(color == 'BLUE'):
        return([0,1,0])
    if(color == 'GREEN'):
        return([0,0,1])
    if(color == 'WHITE'):
        return([1,1,1])
    else:
        return(None)
    
def color_rgb(color):
    color[0] = color[0]/255
    color[1] = color[1]/255
    color[2] = color[2]/255
    return(color)
        
display_color('RED', red, blue, green)

