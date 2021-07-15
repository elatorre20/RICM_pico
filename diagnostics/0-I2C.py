import machine
import utime

#scans the I2C ports for all devices
#tests: I2C buses, PCA9532s, PCA9555s, OLED modules
sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)

print('Scan i2c bus 0...')
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    
from micropython import const
import framebuf
import machine
import utime
import OLED

sda1=machine.Pin(18)
scl1=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda1, scl=scl1, freq=400000)

print('Scan i2c bus 1...')
devices1 = i2c1.scan()

if len(devices1) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices1))

for device in devices1:
    print("Decimal address: ",device," | Hexa address: ",hex(device))