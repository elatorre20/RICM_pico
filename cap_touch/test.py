from utime import sleep
import cap_touch

sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)

sensor = cap_touch.IS31SE5100(i2c)

