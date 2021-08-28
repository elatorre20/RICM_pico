import machine
import rp2                   # Get the Raspberry Pi Pico library
import utime

from machine import ADC, Pin      # Get the ADC and Pin libraries

sensor_potentiometer = machine.ADC(0)
sensor_slider_1 = machine.ADC(1)
sensor_slider_2 = machine.ADC(2)
sensor_vsys = machine.ADC(29)
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

Pin(29, Pin.IN) # Set VDC pin to input, turn off pull up/down

print("Move the sliders and rotate the potentiometer to change the readings.\n")
utime.sleep_ms(2000)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
# The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
# Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
    print("The PICO internal temperature is:", temperature)
    reading = sensor_vsys.read_u16() * conversion_factor * 3
    print("The VSYS voltage is:", reading)
    reading = sensor_potentiometer.read_u16() * conversion_factor
    print("Potentiometer voltage is:", reading)
    reading = sensor_slider_1.read_u16() * conversion_factor
    print("Slider 1 voltage is:", reading)
    reading = sensor_slider_2.read_u16() * conversion_factor
    print("Slider 2 voltage is:", reading)
    utime.sleep(2)

