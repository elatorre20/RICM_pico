from utime import sleep
import GPIO

#cycles the gpio output values and reads them back
#tests: PCA9555 chip 1

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)

gpio0 = GPIO.PCA9555(i2c, 0x20)

gpio0.setup_outputs()
gpio0.all_high()

#should both return 11111111
print(gpio0.reg_read(GPIO.INPUT0))
print(gpio0.reg_read(GPIO.INPUT1))

gpio0.all_low()

#should both return 00000000
print(gpio0.reg_read(GPIO.INPUT0))
print(gpio0.reg_read(GPIO.INPUT1))