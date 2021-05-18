#makes some simple endlessly repeating patterns on the screen

# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
# Taken from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

from micropython import const
import framebuf
import machine
from utime import sleep
from random import randint
import OLED
        
class tictactoe:
    def __init__(self,screen,size,length):
        self.screen = screen
        self.x = int((screen.width - (length*size))/2)
        self.y = int((screen.height - (length*size))/2)
        self.size = size
        self.length = length
        columns = []
        for i in range(size):
            row = [None] * size
            columns = columns + [list.copy(row)]
        self.state = columns
        
    def draw_board(self):
        x = self.length + self.x
        y = 0 + self.y
        #horizontal
        for i in range(self.size-1):
            self.screen.line(x,y,x,y+(self.size*self.length),1)
            x = x + self.length
        x = 0 + self.x
        y = self.length + self.y
        #vertical
        for i in range(self.size-1):
            self.screen.line(x,y,x+(self.size*self.length),y,1)
            y = y + self.length
        self.screen.show()
    
    def place(self,x,y,char):
        self.state[y][x] = char
        self.update()
        self.check_win()
    
    def update(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 'x':
                    x = self.x + (j*self.length) + ((self.length-6)//2)
                    y = self.y + (i*self.length) + ((self.length-8)//2)
                    self.screen.text("x",x,y,1)
                if self.state[i][j] == 'o':
                    x = self.x + (j*self.length) + ((self.length-6)//2)
                    y = self.y + (i*self.length) + ((self.length-8)//2)
                    self.screen.text("o",x,y,1)
        self.screen.show()
        
        
    def check_win(self):
        sleep(1)
        #vertical
        for i in self.state:
            player = i[0]
            win = True
            for j in range(self.size):
                if(i[j] != player or i[j] == None):
                    win = False
            if win:
                self.screen.fill_rect(int((self.screen.width - 104)/2),int((self.screen.height - 10)/2),104,8,0)
                self.screen.text("player " + player + " won!",int((self.screen.width - 104)/2), int((self.screen.height - 9)/2))
                self.screen.show()
                while(True):
                    sleep(1)
        #horizontal
        for j in range(self.size):
            player = self.state[0][j]
            win = True
            for i in self.state:
                if(i[j] != player or i[j] == None):
                    win = False
            if win:
                self.screen.fill_rect(int((self.screen.width - 104)/2),int((self.screen.height - 10)/2),104,8,0)
                self.screen.text("player " + player + " won!",int((self.screen.width - 104)/2), int((self.screen.height - 9)/2))
                self.screen.show()
                while(True):
                    sleep(1)
        #diagonal
        player = self.state[0][0]
        win = True
        for i in range(self.size):
            if(self.state[i][i] != player or self.state[i][i] == None):
                    win = False
        if win:
                self.screen.fill_rect(int((self.screen.width - 104)/2),int((self.screen.height - 10)/2),104,8,0)
                self.screen.text("player " + player + " won!",int((self.screen.width - 104)/2), int((self.screen.height - 9)/2))
                self.screen.show()
                while(True):
                    sleep(1)
        x = 0
        y = self.size - 1
        player = self.state[y][x]
        win = True
        for i in range(self.size):
            if(self.state[y][x] != player or self.state[y][x] == None):
                    win = False
            x = x + 1
            y = y - 1
        if win:
                self.screen.fill_rect(int((self.screen.width - 104)/2),int((self.screen.height - 10)/2),104,8,0)
                self.screen.text("player " + player + " won!",int((self.screen.width - 104)/2), int((self.screen.height - 9)/2))
                self.screen.show()
                while(True):
                    sleep(1)
            
sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)

oled = OLED.SSD1306_I2C(128, 64, i2c)

oled.poweron()
oled.fill(0)
oled.show()

oled.text('TicTacToe!', 0,0)
oled.text('c. RICM 2021', 0, 16)
oled.show()

sleep(3)

oled.fill(0)
oled.show()

game = tictactoe(oled,3,20)

game.draw_board()

print('beginning game!')



