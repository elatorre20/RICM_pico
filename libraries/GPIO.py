from micropython import const
import machine
from utime import sleep_ms

#library for using a PCA9555 16-channel I2C I/O expander with a raspberry pi pico
#NB to get the chip to work, you cannot have the address pins or reset pin floating
#address range: 0x20-0x27

# register definitions
INPUT0  = const(0b00000000)
INPUT1  = const(0b00000001)
OUTPUT0 = const(0b00000010)
OUTPUT1 = const(0b00000011)
PI0     = const(0b00000100)
PI1     = const(0b00000101)
CFG0    = const(0b00000110)
CFG1    = const(0b00000111)

# commands/data
OUTPUT_HIGH = const(0b11111111)
OUTPUT_LOW  = const(0b00000000)
CFG_INPUT   = const(0b11111111)
CFG_OUTPUT  = const(0b00000000)


class PCA9555():
    def __init__(self, i2c, address = 0x20):
        self.i2c = i2c
        self.address = address
        self.temp = bytearray(2)
        self.temp_read = bytearray(1)
        self.state = [0] * 16
        
    def reg_write(self, register, value):
        self.temp[0] = register
        self.temp[1] = value
        self.i2c.writeto(self.address, self.temp)
    
    def reg_read(self, register):
        self.i2c.readfrom_mem_into(self.address, register, self.temp_read)
        return(bin(self.temp_read[0]))
    
    def write_outputs(self, vals):
        self.reg_write(OUTPUT0, vals[0])
        self.reg_write(OUTPUT1, vals[1])
        
    def setup_inputs(self):
        self.reg_write(CFG0, CFG_INPUT)
        self.reg_write(CFG1, CFG_INPUT)
        
    def setup_outputs(self):
        self.reg_write(CFG0, CFG_OUTPUT)
        self.reg_write(CFG1, CFG_OUTPUT)
        
    def all_high(self):
        self.write_outputs([OUTPUT_HIGH, OUTPUT_HIGH])
        
    def all_low(self):
        self.write_outputs([OUTPUT_LOW, OUTPUT_LOW])
        
    
            
            
