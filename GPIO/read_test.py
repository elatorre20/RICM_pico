import utime
import GPIO

#cycles the gpio output values and reads them back
#tests: PCA9555 chip 1

sda0=machine.Pin(20)
scl0=machine.Pin(21)
i2c0=machine.I2C(0, sda=sda0, scl=scl0, freq=400000)

gpio0 = GPIO.PCA9555(i2c0, 0x20)

sda1=machine.Pin(18)
scl1=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda1, scl=scl1, freq=400000)

gpio1 = GPIO.PCA9555(i2c1, 0x21)

gpio0.setup_inputs()
gpio1.setup_inputs()

while(True):
    print(gpio0.reg_read(GPIO.INPUT0))
    print(gpio0.reg_read(GPIO.INPUT1))
    print(gpio1.reg_read(GPIO.INPUT0))
    print(gpio1.reg_read(GPIO.INPUT1))
    utime.sleep(0.5)

