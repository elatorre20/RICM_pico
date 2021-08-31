import machine
import utime
import OLED

#displays the display ID on the OLED screens
#tests: OLED module 0

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)
    
print("\nScanning I2C bus 0 on GP20 & GP21")
devices = i2c.scan()

if len(devices) == 0:
    print("\tNo I2C devices found!")
else:
    print("\tI2C devices found:", len(devices))

    for device in devices:
        print("\tDecimal address:", device, " | 7-bit hex address:", hex(device))

    print("\nTesting OLED @ 0x3c")
    print("Configuring OLED")
    oled0 = OLED.SSD1306_I2C(128, 64, i2c, 0x3C)

    print("Powering on OLED")
    oled0.poweron()

    print("Writing text to OLED")
    oled0.text("screen 1", 0, 0)

    print("Turning on OLED display")
    oled0.show()
