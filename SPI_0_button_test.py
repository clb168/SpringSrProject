from machine import Pin, SPI
import struct
from time import sleep

from RF.nrf24l01 import NRF24L01

led = Pin(25, Pin.OUT)                # LED
btn = Pin(28, Pin.IN, Pin.PULL_DOWN)  # button press
csn = Pin(17, mode=Pin.OUT, value=1)  # chip select not
ce  = Pin(21, mode=Pin.OUT, value=0)  # chip enable

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2 - swap these on the other Pico!
pipes = (b"\xd2\xf0\xf0\xf0\xf0", b"\xe1\xf0\xf0\xf0\xf0")

def setup():
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=4)
    nrf.set_power_speed(0x06, 0x08)
    print(nrf.reg_read(0x06))
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    led.value(0)
    return nrf

def flash_led(times:int=None):
    ''' Flashed the built in LED the number of times defined in the times parameter '''
    for _ in range(times):
        led.value(1)
        sleep(0.01)
        led.value(0)
        sleep(0.01)

def demo(nrf):
    state = 0 
    while True:
        if state != btn.value():
            state = btn.value()
            led.value(state)
            
            print("tx", state)
            nrf.stop_listening()
            try:
                nrf.send(struct.pack("i", state))
            except OSError:
                print('message lost')
            nrf.start_listening()
            
        if nrf.any():
            buf = nrf.recv()
            got = struct.unpack("i", buf)[0]
            print("rx", got)
            led.value(got)

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes
    

nrf = setup()
flash_led(1)
auto_ack(nrf)
demo(nrf)