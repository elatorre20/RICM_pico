import machine
import utime

#Reads and displays the values of the three ADC channels
#Tests: RV1, RV2, RV3

RV1 = machine.ADC(28)
RV2 = machine.ADC(27)
RV3 = machine.ADC(26)

while(True):
    print(RV1.read_u16()//256)
    print(RV2.read_u16()//256)
    print(RV3.read_u16()//256)
    utime.sleep_ms(50)