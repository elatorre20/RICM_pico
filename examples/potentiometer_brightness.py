import utime
import LEDS
import machine

#varies the brightness of the LEDS using the value of RV3

RV1 = machine.ADC(28)

sda0=machine.Pin(20)
scl0=machine.Pin(21)
i2c0=machine.I2C(0, sda=sda0, scl=scl0, freq=400000)

controller0 = LEDS.PCA9532(i2c0, 0x60)

sda1=machine.Pin(18)
scl1=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda1, scl=scl1, freq=400000)

controller1 = LEDS.PCA9532(i2c1, 0x61)

controller0.all_state(LEDS.LEDS_PWM0)
controller1.all_state(LEDS.LEDS_PWM0)

while(True):
    b = RV1.read_u16()//256
    controller0.set_brightness(0, b)
    controller1.set_brightness(0, b)
    print(b)
    
