from micropython import const
import machine
from utime import sleep_ms

#library for using a PCA9532 16-channel LED controller with a raspberry pi pico
#NB to get the chip to work, you cannot have the address pins or reset pin floating
#address range: 0x60-0x67

#still working out some kinks with losing packets, but im not sure if that is because of the physical cirtuit or this code

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



class PCA9532():
    def __init__(self, i2c, address = 0x60):
        self.i2c = i2c
        self.address = address
        self.temp = bytearray(2)
        self.temp_read = bytearray(1)
        #set PWM blink rate high enough for smooth dimming using duty cycle
        self.reg_write(PSC0, PWM_SMOOTH)
        self.reg_write(PSC1, PWM_SMOOTH)
        self.set_brightness(0, 127)
        self.set_brightness(1, 127)
        
    def reg_write(self, register, value):
        self.temp[0] = register
        self.temp[1] = value
        self.i2c.writeto(self.address, self.temp)
    
    def reg_read(self, register):
        self.i2c.readfrom_into(self.address, self.temp_read)
        return(self.temp_read[0])
    
    def write_leds(self, vals):
        temp = bytearray([LSX] + vals)
        self.i2c.writeto(self.address, temp)
        
    def set_brightness(self, pwm, level):
        #0 = off, 255 = full brightness
        if(level > 255 or level < 0):
            print('Brightness must be in the range 0,255')
            return
        if(pwm == 0):
            self.reg_write(PWM0, level)
        if(pwm == 1):
            self.reg_write(PWM1, level)
                
            
    def all_on(self):
        self.write_leds([LEDS_ON, LEDS_ON, LEDS_ON, LEDS_ON])
        
    def all_off(self):
        self.write_leds([LEDS_OFF, LEDS_OFF, LEDS_OFF, LEDS_OFF])
        
    def all_state(self, state):
        self.write_leds([state, state, state, state])
        
        