from machine import Pin, PWM
from utime import sleep
from micropython import const

#notes
G3 = const(196)
C4 = const(262)
D4 = const(294)
E4 = const(330)
F4 = const(349)
G4 = const(392)
A4 = const(440)
B4 = const(494)
C5 = const(524)
rest = const(0)

#duration
whole   = const(8)
half    = const(4)
quarter = const(2)
eighth  = const(1)

class buzzer():
    
    def __init__(self, pin):
        self.pin = PWM(Pin(pin))
        self.tempo = 120
        self.duty = 32767
        self.pin.duty_u16(0)
        
    def play_note(self, note, duration):
        if note == 0:
            sleep(((duration*(1/self.tempo))/2)*60)
            return
        self.pin.freq(note)
        self.pin.duty_u16(self.duty)
        sleep(((duration*(1/self.tempo))/2)*60)
        self.pin.duty_u16(0)
        sleep(0.01)
        
    def play_scale(self):
        self.play_note(C4, quarter)
        self.play_note(D4, quarter)
        self.play_note(E4, quarter)
        self.play_note(F4, quarter)
        self.play_note(G4, quarter)
        self.play_note(A4, quarter)
        self.play_note(B4, quarter)
        self.play_note(C5, quarter)
        self.play_note(C5, quarter)
        self.play_note(B4, quarter)
        self.play_note(A4, quarter)
        self.play_note(G4, quarter)
        self.play_note(F4, quarter)
        self.play_note(E4, quarter)
        self.play_note(D4, quarter)
        self.play_note(C4, quarter)
        
    def play_jingle(self):
        self.play_note(E4, quarter)
        self.play_note(E4, quarter)
        self.play_note(rest, quarter)
        self.play_note(E4, quarter)
        self.play_note(rest, quarter)
        self.play_note(C4, quarter)
        self.play_note(E4, quarter)
        self.play_note(rest, quarter)
        self.play_note(G4, quarter)
        self.play_note(rest, quarter)
        self.play_note(rest, half)
        self.play_note(G3, quarter)
        
        
        