from micropython import const
import machine
import utime

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
        #states: 0 = off, 1 = on, 2 = PWM0, 3 = PWM1
        #leds 13, 14, 15 are digital-only 
        self.led_state = [0] * 16
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
        
    def update_state(self):
        def check_state(s):
            if s == '00':
                return 0
            if s == '01':
                return 1
            if s == '10':
                return 2
            if s == '11':
                return 3
        leds0 = str(self.reg_read(LS0))
        leds1 = str(self.reg_read(LS1))
        leds2 = str(self.reg_read(LS2))
        leds3 = str(self.reg_read(LS3))
        leds = leds0 + leds1 + leds2 + leds3
        for i in range (0, 16):
            led = leds[(2*i):((2*i)+2)]
            self.led_state[i] = check_state(led)
        
    def set_brightness(self, pwm, level):
        #0 = off, 255 = full brightness
        if(level > 255 or level < 0):
            print('Brightness must be in the range 0,255')
            return
        if(pwm == 0):
            self.reg_write(PWM0, level)
        if(pwm == 1):
            self.reg_write(PWM1, level)
            
    def set_led(self, led, state):
        self.update_state()
        self.led_state[led] = state
        regs = [LS0, LS1, LS2, LS3]
        j = 0
        b = ''
        for i in led_state:
            if i = 0:
                b = b + '00'
            elif i = 1:
                b = b + '01'
            elif i = 2:
                b = b + '10'
            elif i = 3:
                b = b + '11'
            if len(b) == 8:
                self.reg_write(regs[j], b)
                b = ''
                j = j + 1
                
            
    def all_on(self):
        self.reg_write(LS0, LEDS_ON)
        self.reg_write(LS1, LEDS_ON)
        self.reg_write(LS2, LEDS_ON)
        self.reg_write(LS3, LEDS_ON)
        
    def all_off(self):
        self.reg_write(LS0, LEDS_OFF)
        self.reg_write(LS1, LEDS_OFF)
        self.reg_write(LS2, LEDS_OFF)
        self.reg_write(LS3, LEDS_OFF)
        
        