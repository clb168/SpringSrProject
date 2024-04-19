from ili9341 import Display
from machine import Pin, SPI
from xpt2046 import Touch
from micropython import const


TFT_CS_PIN = const(17)
TFT_RST_PIN = const(21)
TFT_DC_PIN = const(20)

XPT_CLK_PIN = const(2)
XPT_MOSI_PIN = const(3)
XPT_MISO_PIN = const(0)

XPT_CS_PIN = const(1)
XPT_INT = const(5)

def createMyDisplay():
    spiTFT = SPI(0, baudrate=40000000)
    display = Display(spiTFT,
                      dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN))
    return display

def createXPT(touch_handler):
    spiXPT = SPI(0, baudrate=1000000,
                 sck=Pin(XPT_CLK_PIN), mosi=Pin(XPT_MOSI_PIN), miso=Pin(XPT_MISO_PIN))

    xpt = Touch(spiXPT, cs=Pin(XPT_CS_PIN), int_pin=Pin(XPT_INT),
                int_handler=touch_handler)

    return xpt

