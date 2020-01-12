from machine import Pin, SPI
import time
import epaper2in7
import framebuf
import pics

from writer import Writer
import freesans20


# SPIV on ESP32
sck = Pin(18)
miso = Pin(19)
mosi = Pin(23)
dc = Pin(22)
cs = Pin(5)
rst = Pin(21)
busy = Pin(4)
# spi = SPI(2, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

print("We're in main")

w = 176
h = 264
x = 0
y = 0

e = epaper2in7.EPD(spi, cs, dc, rst, busy)
e.init()

print("Screen ready")


buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
black = 1
white = 0

fb.fill(white)
# fb.text("Hello World", 30, 0, white)

e.display_frame(buf)

fb.blit(pics.fb_thermometer, 10, 2)
fb.blit(pics.fb_humidity, 10, 62)
fb.blit(pics.fb_pressure, 10, 122)
fb.blit(pics.fb_light, 10, 182)

fb.text("23°C", 70, 20, black)

e.display_frame(buf)


class NotionalDisplay(framebuf.FrameBuffer):
    def __init__(self, width, height, buffer):
        self.width = width
        self.height = height
        self.buffer = buffer
        self.mode = framebuf.MONO_HLSB
        super().__init__(self.buffer, self.width, self.height, self.mode)

    def show(self):
        ...


my_display = NotionalDisplay(176, 264, buf)
wri = Writer(my_display, freesans20)

# verbose = False to suppress console output
Writer.set_textpos(my_display, 0, 0)

wri.printstring('Sunday\n')
print("Sunday printed")
wri.printstring('12 Aug 2018\n')
print("August printed")
wri.printstring('10.30am')
print("time printed")
my_display.show()

e.display_frame(buf)

while True:
    pass
