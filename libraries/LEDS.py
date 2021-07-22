from micropython import const
import machine
from utime import sleep_ms

#library for using a PCA9532 16-channel LED controller with a raspberry pi pico
#NB to get the chip to work, you cannot have the address pins or reset pin floating
#address range: 0x60-0x67

# register definitions
# byte fields: 0-2: unused, 3: autoincrement flag, 4-7: register address
INPUT0 = const(0b00000000)
INPUT1 = const(0b00000001)
PSC0   = const(0b00000010)
PWM0   = const(0b00000011)
PSC1   = const(0b00000100)
PWM1   = const(0b00000101)
LSX    = const(0b00010110)
LS0    = const(0b00000110)
LS1    = const(0b00000111)
LS2    = const(0b00001000)
LS3    = const(0b00001001)

# commands/data
LEDS_ON   = const(0b01010101)
LEDS_OFF  =  const(0b00000000)
LEDS_PWM0 = const(0b10101010)
LEDS_PWM1 = const(0b11111111)
PWM_SMOOTH= const(0b00000010)
BLINK_FAST= const(0b00100000)
BLINK_SLOW= const(0b11111111)
#colors
WHITE   = const(0b00110101)
RED     = const(0b00010000)
GREEN   = const(0b00000100)
BLUE    = const(0b00000001)
CYAN    = const(0b00000101)
MAGENTA = const(0b00110001)
YELLOW  = const(0b00110100)

"""
LEDS as connected:

Chip 0 (: 
"""
class PCA9532():
    def __init__(self, i2c, address = 0x60):
        self.i2c = i2c
        self.address = address
        self.temp = bytearray(2)
        self.temp_read = bytearray(1)
        self.state = [0] * 16
        #set PWM blink rate high enough for smooth dimming using duty cycle
        self.reg_write(PSC0, PWM_SMOOTH)
        self.reg_write(PSC1, PWM_SMOOTH)
        #set PWMs to 50% and 25% brightness
        self.set_brightness(0, 127)
        self.set_brightness(1, 63)
        self.all_off()
        
    def reg_write(self, register, value):
        self.temp[0] = register
        self.temp[1] = value
        self.i2c.writeto(self.address, self.temp)
        self.update_state()
    
    def reg_read(self, register):
        self.i2c.readfrom_mem_into(self.address, register, self.temp_read)
        return(bin(self.temp_read[0]))
    
    def write_leds(self, vals):
        self.reg_write(LS0, vals[0])
        self.reg_write(LS1, vals[1])
        self.reg_write(LS2, vals[2])
        self.reg_write(LS3, vals[3])
        
    def set_brightness(self, pwm, level):
        #0 = off, 255 = full brightness
        if(level > 255 or level < 0):
            print('Brightness must be in the range 0,255')
            return
        if(pwm == 0):
            self.reg_write(PWM0, level)
        if(pwm == 1):
            self.reg_write(PWM1, level)
                
    def RGB_LED(self, num, color):
        r = None
        if(num == 0):
            r = LS0
        elif(num == 1):
            r = LS1
        elif(num == 2):
            r = LS2
        elif(num == 3):
            r = LS3
        self.reg_write(r, color)
        
    def all_on(self):
        self.write_leds([LEDS_ON, LEDS_ON, LEDS_ON, LEDS_ON])
        
    def all_off(self):
        self.write_leds([LEDS_OFF, LEDS_OFF, LEDS_OFF, LEDS_OFF])
        
    def all_state(self, state):
        self.write_leds([state, state, state, state])
        
    def update_state(self):
        a = self.reg_read(LS0)
        b = self.reg_read(LS1)
        c = self.reg_read(LS2)
        d = self.reg_read(LS3)
        s = ''
        for i in([a,b,c,d]):
            i = i[2:]
            while(len(i) < 8):
                i = '0' + i
            s = s + i
        i = 0
        while(s != ''):
            x = s[:2]
            self.state[i] = int(x, 2)
            i = i + 1
            s = s[2:]
            
    def write_LED(self, num, state):
        self.state[num] = state
        self.update_LEDS
    
    def update_LEDS(self):
        #add in something to update the chip LEDS from the state list
        return(0)
    
            
            