# demo.py
# Kevin McAleer
# test the nRF24L01 modules to send and receive data
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0

from nrf24l01 import NRF24L01
from machine import SPI, Pin, PWM
from time import sleep
import struct


csn = Pin(17, mode=Pin.OUT, value=1) 
ce = Pin(21, mode=Pin.OUT, value=0)  
led = Pin(25, Pin.OUT)               # Onboard LED
payload_size = 4
spi = SPI(0)

#setup PWM outout
pwm1 = PWM(Pin(0))
pwm2 = PWM(Pin(1))
pwm1.freq(1000000)
pwm2.freq(1000000)

# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

#role = "send"
role = "receive"

if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"

def setup():
    print("Initialising the nRF24L0+ Module")
    nrf = NRF24L01(spi, csn, ce, channel= 78, payload_size=payload_size)
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
    for n in range(len(msg)):
        try:
            encoded_string = msg[n].encode()
            byte_array = bytearray(encoded_string)
            buf = struct.pack("s", byte_array)
            nrf.send(buf)
            # print(role,"message",msg[n],"sent")
            flash_led(1)
        except OSError:
            print(role,"Sorry message not sent")
    nrf.send("\n")
    nrf.start_listening()

#takes the output y value from display and turns it into a percentage for the duty cycle
#inverts it aswell because of the layout of the touch on display
def duty_cycle_gen(y_val):
    percentage = 1-(y_val[0]/320)
    return percentage

# main code loop
flash_led(1)
nrf = setup()
nrf.set_power_speed(0x06, 0x08)
print(nrf.reg_read(0x06))
nrf.start_listening()
auto_ack(nrf)

msg_string = ""
count = 0
while True:
    msg = 0
    if nrf.any():
        #print("Message received")
        package = nrf.recv()          
        message = struct.unpack('<i', package)
        print(message)
        pwm1.duty_u16(int(duty_cycle_gen(message)*65535))
        pwm2.duty_u16(int(duty_cycle_gen(message)*65535))

        # if (len(msg_string) <= 4):
        #     print("Y Value",msg_string, msg)
        #     msg_string = ""
        # else:
        #     msg_string = ""
        #     print("message too long, clearing buffer")




    
    