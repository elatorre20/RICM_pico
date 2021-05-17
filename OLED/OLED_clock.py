# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
# Taken from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

from micropython import const
import framebuf
import machine
import utime


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

def img_read(filename):
    img = open(filename, 'rb')
    px = img.read()
    px = px[62:]
    array = bytearray(px)
    imgbuf = framebuf.FrameBuffer(array, 128,32, framebuf.MONO_HLSB)
    return(imgbuf)

def display_time(screen, f, number):
    screen.fill(0)
    if(len(number) > 4):
        screen.text('invalid time or format')
        return
    if(len(number) < 4):
        for i in range(4):
            number = '0' + number
            if(len(number) == 4):
                break
    for i in number:
        if (int(i) not in [0,1,2,3,4,5,6,7,8,9]):
            screen.text('invalid time or format')
            return
    d0 = int(number[0])
    d1 = int(number[1])
    d2 = int(number[2])
    d3 = int(number[3])
    screen.blit(f.digits[d0], 0,0)
    screen.blit(f.digits[d1], 31,0)
    screen.blit(f.digits[10], 62,0)
    screen.blit(f.digits[d2], 66, 0)
    screen.blit(f.digits[d3], 97,0)
    screen.show()
    
class font():
    def __init__(self):
        digits = []
        digits = digits + [img_read('img/0.bmp')]
        digits = digits + [img_read('img/1.bmp')]
        digits = digits + [img_read('img/2.bmp')]
        digits = digits + [img_read('img/3.bmp')]
        digits = digits + [img_read('img/4.bmp')]
        digits = digits + [img_read('img/5.bmp')]
        digits = digits + [img_read('img/6.bmp')]
        digits = digits + [img_read('img/7.bmp')]
        digits = digits + [img_read('img/8.bmp')]
        digits = digits + [img_read('img/9.bmp')]
        digits = digits + [img_read('img/colon.bmp')]
        self.digits = digits
    
def time_sweep(screen, f):
    for i in range(10000):
        j = str(i)
        display_time(screen, f, j)
        #utime.sleep(0.001)
        
def stopwatch(screen, f):
    minutes = 0
    seconds = 0
    number = ''
    while(True):
        print(minutes)
        print(seconds)
        number = ''
        if(minutes > 99):
            return
        if(seconds == 60):
            seconds = 0
            minutes = minutes + 1
        if(seconds < 10):
            number = '0' + str(seconds)
            number = str(minutes) + number
            display_time(screen, f, number)
            utime.sleep(1)
            seconds = seconds + 1
            continue
        else:
            number = str(minutes) + str(seconds)
            display_time(screen, f, number)
            utime.sleep(1)
            seconds = seconds + 1
            continue
        

sda=machine.Pin(26)
scl=machine.Pin(27)
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
    
    
oled = SSD1306_I2C(128, 32, i2c)

oled.poweron()

oled.text("hello world", 0, 0)

oled.show()

seg7 = font()


oled.fill(0)
oled.show()

stopwatch(oled, seg7)
