from utime import sleep
import GPIO

#cycles the gpio output values and reads them back
#tests: PCA9555 chip0

sda=machine.Pin(18)
scl=machine.Pin(19)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)

gpio0 = GPIO.PCA9555(i2c, 0x21)

gpio0.setup_outputs()
gpio0.write_outputs([GPIO.OUTPUT_HIGH, GPIO.OUTPUT_HIGH])

#should both return 11111111
print(gpio0.reg_read(GPIO.INPUT0))
print(gpio0.reg_read(GPIO.INPUT1))

gpio0.all_low()

#should both return 00000000
print(gpio0.reg_read(GPIO.INPUT0))
print(gpio0.reg_read(GPIO.INPUT1))