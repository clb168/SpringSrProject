
from nrf24l01 import NRF24L01
from machine import SPI, Pin, idle
from time import sleep
import struct
from control import Control
from ili9341 import Display, color565
from xpt2046 import Touch

GREEN = color565(127, 255, 0)
RED = color565(204, 0, 0)

rf_csn = Pin(9, mode=Pin.OUT, value=1) 
rf_ce = Pin(7, mode=Pin.OUT, value=0)  
led = Pin(25, Pin.OUT)               # Onboard LED
payload_size = 20
rf_spi = SPI(1)


# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

role = "send"
#role = "receive"

if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"

def setup():
    print("Initialising the nRF24L0+ Module")
    nrf = NRF24L01(rf_spi, rf_csn, rf_ce, channel=78, payload_size=payload_size)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000) # enable auto-ack on all pipes

def flash_led(times:int=None):
    ''' Flashed the built in LED the number of times defined in the times parameter '''
    for _ in range(times):
        led.value(1)
        sleep(0.01)
        led.value(0)
        sleep(0.01)

def send(nrf, msg):
    print("sending message.", msg)
    nrf.stop_listening()
    
    # for n in range(len(msg)):
    encoded_string = msg.encode()
    
    byte_array = bytearray(encoded_string)
    print(byte_array)
    buf = struct.pack(f"{len(byte_array)}s", byte_array) 
    print(buf)
    try:
        nrf.send(buf)
        flash_led(1)
    except OSError:
        print("Sorry message not sent")   
    nrf.send("\n")
    nrf.start_listening()

# main code loop
#RF module
flash_led(1)
nrf = setup()
nrf.set_power_speed(0x06, 0x08)
print(nrf.reg_read(0x06))
nrf.start_listening()
auto_ack(nrf)
msg_string = ""

#Display module
spi = SPI(0, baudrate=40000000)
display = Display(spi, dc=Pin(20), cs=Pin(17), rst=Pin(21))
spi2 = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3), miso=Pin(0))


display.fill_rectangle(55, 60, 130, 80, GREEN) #Go button
display.fill_rectangle(55, 180, 130, 80, RED) #Stop button



ctrl = Control(display, spi2)

    
while True:
    print(ctrl.return_y())

# while True:
#     msg = ""
#     if role == "send":
#         # if ctrl.return_state() != "":
#         #     send(nrf, ctrl.return_state())
#         #     ctrl.clear_state()
#         send(nrf, "hello")
#         send(nrf, ctrl.return_state())
        
#         sleep(0.01) 
#         ctrl.clear_state() # delay for 10ms
#     else:
#         # Check for Messages
        
#         if nrf.any():
#             #print("Message received")
#             package = nrf.recv()          
#             message = struct.unpack("s",package)
#             msg = message[0].decode()
#             flash_led(1)

#             # Check for the new line character
#             if (msg == "\n") and (len(msg_string) <= 20):
#                 print("full message",msg_string, msg)
#                 msg_string = ""
#             else:
#                 if len(msg_string) <= 20:
#                     msg_string = msg_string + msg
#                 else:
#                     msg_string = ""

