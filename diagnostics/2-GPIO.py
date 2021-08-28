from utime import sleep
import GPIO

#cycles the gpio output values and reads them back
#tests: PCA9555 chip0

sda=machine.Pin(18)
scl=machine.Pin(19)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)

print("\nScanning I2C bus 0 on GP18 & GP19")
devices = i2c.scan()

if len(devices) == 0:
    print("\tNo I2C devices found!")
else:
    print("\tI2C devices found:", len(devices))

for device in devices:
    print("\tDecimal address:", device, " | 7-bit hex address:", hex(device))

print("\nTesting PCA9555 @ I2C = 0x21")

gpio0 = GPIO.PCA9555(i2c, 0x21)

print("Setting all PCA9555 outputs high")

gpio0.setup_outputs()
gpio0.all_high()

print("Reading all PCA9555 outputs")

#should both return 11111111
print(gpio0.reg_read(GPIO.INPUT0))
print(gpio0.reg_read(GPIO.INPUT1))

print("Setting all PCA9555 outputs low")
gpio0.all_low()

print("Reading all PCA9555 outputs")

#should both return 00000000
print(gpio0.reg_read(GPIO.INPUT0))
print(gpio0.reg_read(GPIO.INPUT1))