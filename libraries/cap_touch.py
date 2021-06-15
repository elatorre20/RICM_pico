from micropython import const
import machine
from utime import sleep_ms

#library for using the IS31SE5100 8-channel capacitive touch sensor chip. Address pin must be tied for proper functioning.
#address range: 0x44-0x48


# register definitions
CONFIG    = const(0b00000000)
CH_CTL    = const(0b00000001)
STATE_1   = const(0b00000010)
STATE_2   = const(0b00000011)
INTERRUPT = const(0b00000100)

#commands and data
SENS_LOW   = const(0b00000100)
SENS_NORM  = const(0b00000000)
SENS_HIGH  = const(0b00000010)
CH_EN_ALL  = const(0b11111111)
CH_DIS_ALL = const(0b00000000)
INT_CLR    = const(0b00000000)
INT_NO_CLR = const(0b00000010)


class IS31SE5100():
    def __init__(self, i2c, address = 0x44):
        self.i2c = i2c
        self.address = address
        self.temp = bytearray(2)
        self.temp_read = bytearray(1)
        
    def reg_write(self, register, value):
        self.temp[0] = register
        self.temp[1] = value
        self.i2c.writeto(self.address, self.temp)
    
    def reg_read(self, register):
        self.i2c.readfrom_mem_into(self.address, register, self.temp_read)
        return(bin(self.temp_read[0]))
    
    
            
            