import utime
import GPIO

# Cycles the gpio output values, reads them back, and checks the values
# Tests: PCA9555 U2 & U3

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c0=machine.I2C(0, sda=sda, scl=scl, freq=400000)

sda=machine.Pin(18)
scl=machine.Pin(19)
i2c1=machine.I2C(1, sda=sda, scl=scl, freq=400000)

gpio0 = GPIO.PCA9555(i2c0, 0x20)
gpio1 = GPIO.PCA9555(i2c1, 0x21)
gpio0.setup_outputs()
gpio1.setup_outputs()

print("All DIP switches must be in the OFF position.\n")
utime.sleep_ms(2000)

print("Setting U2 outputs high")
gpio0.all_high()
print("Checking if the U2 outputs are high.")
input0 = gpio0.reg_read(GPIO.INPUT0)
if input0 == "0b11111111":
    print("U2 Output 0 is OK")
else:
    print("U2 Output 0 is not OK")
    print("U2 Output 0 was:", input0, "Should be:", "0b11111111")
input1 = gpio0.reg_read(GPIO.INPUT1)
if input1 == "0b11111111":
    print("U2 Output 1 is OK")
else:
    print("U2 Output 1 is not OK")
    print("U2 Output 1 was:", input0, "Should be:", "0b11111111")

print("\nSetting U2 outputs low")
gpio0.all_low()
print("Checking if the U2 outputs are low.")
input0 = gpio0.reg_read(GPIO.INPUT0)
if input0 == bin(0b0):
    print("U2 Output 0 is OK")
else:
    print("U2 Output 0 is not OK")
    print("U2 Output 0 was:", input0, "Should be:", bin(0b0))
input1 = gpio0.reg_read(GPIO.INPUT1)
if input1 == bin(0b0):
    print("U2 Output 1 is OK")
else:
    print("U2 Output 1 is not OK")
    print("U2 Output 1 was:", input0, "Should be:", bin(0b0))

print("\nSetting U2 outputs to alternating 1s and 0s")
outputs = [0b10101010, 0b10101010]
gpio0.write_outputs(outputs)
print("Checking if the U2 outputs are alternating 1s and 0s.")
input0 = gpio0.reg_read(GPIO.INPUT0)
if input0 == bin(0b10101010):
    print("U2 Output 0 is OK")
else:
    print("U2 Output 0 is not OK")
    print("U2 Output 0 was:", input0, "Should be:", bin(0b10101010))
input1 = gpio0.reg_read(GPIO.INPUT1)
if input1 == bin(0b10101010):
    print("U2 Output 1 is OK")
else:
    print("U2 Output 1 is not OK")
    print("U2 Output 1 was:", input0, "Should be:", bin(0b10101010))

print("\nSetting U2 outputs to alternating 0s and 1s")
outputs = [0b01010101, 0b01010101]
gpio0.write_outputs(outputs)
print("Checking if the U2 outputs are alternating 0s and 1s.")
input0 = gpio0.reg_read(GPIO.INPUT0)
if input0 == bin(0b01010101):
    print("U2 Output 0 is OK")
else:
    print("U2 Output 0 is not OK")
    print("U2 Output 0 was:", input0, "Should be:", bin(0b01010101))
input1 = gpio0.reg_read(GPIO.INPUT1)
if input1 == bin(0b01010101):
    print("U2 Output 1 is OK")
else:
    print("U2 Output 1 is not OK")
    print("U2 Output 1 was:", input1, "Should be:", bin(0b01010101))

print("\nSetting U3 outputs high")
gpio1.all_high()
print("Checking if the U3 outputs are high.")
input0 = gpio1.reg_read(GPIO.INPUT0)
if input0 == "0b11111111":
    print("U3 Output 0 is OK")
else:
    print("U3 Output 0 is not OK")
    print("U3 Output 0 was:", input0, "Should be:", "0b11111111")
input1 = gpio1.reg_read(GPIO.INPUT1)
if input1 == "0b11111111":
    print("U3 Output 1 is OK")
else:
    print("U3 Output 1 is not OK")
    print("U3 Output 1 was:", input0, "Should be:", "0b11111111")

print("\nSetting U3 outputs low")
gpio1.all_low()
print("Checking if the U3 outputs are low.")
input0 = gpio1.reg_read(GPIO.INPUT0)
if input0 == bin(0b0):
    print("U3 Output 0 is OK")
else:
    print("U3 Output 0 is not OK")
    print("U3 Output 0 was:", input0, "Should be:", bin(0b0))
input1 = gpio1.reg_read(GPIO.INPUT1)
if input1 == bin(0b0):
    print("U3 Output 1 is OK")
else:
    print("U3 Output 1 is not OK")
    print("U3 Output 1 was:", input0, "Should be:", bin(0b0))

print("\nSetting U3 outputs to alternating 1s and 0s")
outputs = [0b10101010, 0b10101010]
gpio1.write_outputs(outputs)
print("Checking if the U3 outputs are alternating 1s and 0s.")
input0 = gpio1.reg_read(GPIO.INPUT0)
if input0 == bin(0b10101010):
    print("U3 Output 0 is OK")
else:
    print("U3 Output 0 is not OK")
    print("U3 Output 0 was:", input0, "Should be:", bin(0b10101010))
input1 = gpio1.reg_read(GPIO.INPUT1)
if input1 == bin(0b10101010):
    print("U3 Output 1 is OK")
else:
    print("U3 Output 1 is not OK")
    print("U3 Output 1 was:", input0, "Should be:", bin(0b10101010))

print("\nSetting U3 outputs to alternating 0s and 0s")
outputs = [0b01010101, 0b01010101]
gpio1.write_outputs(outputs)
print("Checking if the U3 outputs are alternating 1s and 0s.")
input0 = gpio1.reg_read(GPIO.INPUT0)
if input0 == bin(0b01010101):
    print("U3 Output 0 is OK")
else:
    print("U3 Output 0 is not OK")
    print("U3 Output 0 was:", input0, "Should be:", bin(0b01010101))
input1 = gpio1.reg_read(GPIO.INPUT1)
if input1 == bin(0b01010101):
    print("U3 Output 1 is OK")
else:
    print("U3 Output 1 is not OK")
    print("U3 Output 1 was:", input0, "Should be:", bin(0b01010101))

print("\nPress the buttons one at a time or set one of the DIP switches.")
print("Enter ^c to quit.\n")
utime.sleep_ms(2000)

gpio0.setup_inputs()
gpio1.setup_inputs()

while(True):
    gpio0input0 = gpio0.reg_read(GPIO.INPUT0)
    gpio0input1 = gpio0.reg_read(GPIO.INPUT1)
    gpio1input0 = gpio1.reg_read(GPIO.INPUT0)
    gpio1input1 = gpio1.reg_read(GPIO.INPUT1)
    if gpio0input0 != "0b11111111":
        bit = gpio0.reg_bit(GPIO.INPUT0, 0)
        if bit == "0b0":
            print("SW9 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 1)
        if bit == "0b0":
            print("SW8 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 2)
        if bit == "0b0":
            print("SW7 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 3)
        if bit == "0b0":
            print("SW6 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 4)
        if bit == "0b0":
            print("SW5 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 5)
        if bit == "0b0":
            print("SW4 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 6)
        if bit == "0b0":
            print("SW3 pressed")
        bit = gpio0.reg_bit(GPIO.INPUT0, 7)
        if bit == "0b0":
            print("SW2 pressed")
    elif gpio0input1 != "0b11111111":
        print("gpio0input1 Button pressed", gpio0input1)
        bit = gpio0.reg_bit(GPIO.INPUT1, 0)
        if bit == "0b0":
            print("SW1 pressed")
    elif gpio1input0 != "0b11111111":
        print("gpio1input0 Button pressed", gpio1input0)
    elif gpio1input1 != "0b11111111":
        print("gpio1input1 Button pressed", gpio1input1)
