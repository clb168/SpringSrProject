
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
from micropython import const
from nrf24l01 import NRF24L01

AQUA = const(0X07FF)  # (0, 255, 255)
CYAN = color565(0, 255, 255)
PURPLE = color565(255, 0, 255)
WHITE = color565(255, 255, 255)
GREEN = color565(127, 255, 0)
RED = color565(204, 0, 0)
BLACK = color565(0, 0, 0)

class Control(object):
    """Touchscreen simple demo."""
    y = 0
    state = ""
    CYAN = color565(0, 255, 255)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)
    GREEN = color565(127, 255, 0)
    RED = color565(204, 0, 0)
    BLACK = color565(0, 0, 0)
    def __init__(self, display, spi2):
        """Initialize box.
        
        Args:
            display (ILI9341): display object
            spi2 (SPI): SPI bus
        """
    
        self.display = display
        self.touch = Touch(spi2, cs=Pin(1), int_pin=Pin(5),
                           int_handler=self.touchscreen_press)
        
        # Display initial message
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "Lets Ride!",
                                  self.BLACK,
                                  background=self.WHITE)
        
            # A small 5x5 sprite for the dot
        
        self.dot = bytearray(b'\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00')
    def stop_button_press(self, x, y):
        # Draw dot
        if (x >= 55 and x <= 185) and (y >= 180 and y <= 260):
            self.display.draw_circle(x-2 , y-10 , 5, WHITE)
            return "Stop_Button"
    def go_button_press(self, x, y):
        # Draw dot
        if (x >= 55 and x <= 185) and (y >= 60 and y <= 140):
            self.display.draw_circle(x-2 , y-10 , 5, WHITE)
            return "Go_Button"
        
    



    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        x = (self.display.width - 1) - x
        self.y = y
        
    
        # Display coordinates
        # self.display.draw_text8x8(self.display.width // 2 - 32,
        #                             self.display.height - 9,
        #                             "{0:03d}, {1:03d}".format(x, y),
        #                             self.CYAN)
        print(x, y)
        # #commenting these out for now
        # if self.stop_button_press(x, y) == "Stop_Button":
        #     self.state = "Stop_Button"
        # if self.go_button_press(x, y) == "Go_Button":
        #     self.state = "Go_Button"
        # print(self.state)

    def return_state(self):
        return self.state
    def clear_state(self):
        self.state = ""
    def return_y(self):
        return self.y


    
        
    
    




















# def test():
#     """Test code."""
#     spi = SPI(0, baudrate=40000000)
#     display = Display(spi, dc=Pin(20), cs=Pin(17), rst=Pin(21))
#     spi2 = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3), miso=Pin(0))


#     display.fill_rectangle(55, 60, 130, 80, GREEN) #Go button
#     display.fill_rectangle(55, 180, 130, 80, RED) #Stop button


    
#     StopNGo(display, spi2)
    
    


#     try:
#         while True:
#             idle()

#     except KeyboardInterrupt:
#         print("\nCtrl-C pressed.  Cleaning up and exiting...")
#     finally:
#         display.cleanup()


# test()