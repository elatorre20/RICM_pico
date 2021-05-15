#makes some simple endlessly repeating patterns on the screen

# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
# Taken from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

from micropython import const
import framebuf
import machine
from utime import sleep
from random import randint


# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP,  # display off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE,  # start at line 0
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,  # display on
            ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def rotate(self, rotate):
        self.write_cmd(SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(SET_SEG_REMAP | (rotate & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time

        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)
        
class tictactoe:
    def __init__(self,screen,x,y,size,length):
        self.screen = screen
        self.x = x
        self.y = y
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
                self.screen.fill_rect(12,12,104,8,0)
                self.screen.text("player " + player + " won!", 12, 12)
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
                self.screen.fill_rect(12,12,104,8,0)
                self.screen.text("player " + player + " won!", 12, 12)
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
                self.screen.fill_rect(12,12,104,8,0)
                self.screen.text("player " + player + " won!", 12, 12)
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
                self.screen.fill_rect(12,12,104,8,0)
                self.screen.text("player " + player + " won!", 12, 12)
                self.screen.show()
                while(True):
                    sleep(1)
            
sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)

# print('Scan i2c bus...')
# devices = i2c.scan()
# 
# if len(devices) == 0:
#     print("No i2c device !")
# else:
#     print('i2c devices found:',len(devices))
# 
# for device in devices:
#     print("Decimal address: ",device," | Hexa address: ",hex(device))
    


    
    
    
oled = SSD1306_I2C(128, 32, i2c)

oled.poweron()

oled.fill(0)

oled.show()

game = tictactoe(oled,50,2,3,10)

game.draw_board()

print('beginning game!')



