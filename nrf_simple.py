
from nrf24l01 import NRF24L01
from machine import SPI, Pin
from time import sleep
import struct



rf_csn = Pin(9, mode=Pin.OUT, value=1) 
rf_ce = Pin(7, mode=Pin.OUT, value=0)  
led = Pin(25, Pin.OUT)               # Onboard LED
payload_size = 4
rf_spi = SPI(1)


# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

"""
If you are receiving, use these pipes
send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"
"""

#current sending so using these
send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"

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
    nrf.stop_listening()
    buf = struct.pack('<i', msg)
    print(buf)
    try:
        nrf.send(buf)
    except OSError:
        print("Sorry message not sent")   
    nrf.start_listening()




