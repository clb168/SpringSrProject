
from nrf24l01 import NRF24L01
from machine import SPI, Pin, Timer
from time import sleep
import touchSetup
from ili9341 import Display, color565
from xpt2046 import Touch
import nrf_simple #this is the file where I do the processing for sending and reciveing messages
from xgldc_font import XglcdFont
from sys import implementation
from os import uname
from micropython import const
from box_bounce import Box

GREEN = color565(127, 255, 0)
RED = color565(204, 0, 0)


### main code loop ###

#setting up the nrf module
nrf_simple.flash_led(1)
nrf = nrf_simple.setup()
nrf.set_power_speed(0x06, 0x08)
print(nrf.reg_read(0x06))
nrf.start_listening()
nrf_simple.auto_ack(nrf)


#setting up the display and touch module
x_passedTo_ISR = 0
y_passwsTo_ISR = 0

EVT_NO = const(0)
EVT_PenDown = const(1)
EVT_PenUp   = const(2)
event = EVT_NO

TimerReached = False

def xpt_touch(x, y):
    global event, x_passedTo_ISR, y_passedTo_ISR
    event = EVT_PenDown
    x_passedTo_ISR = x
    y_passedTo_ISR = y

display = touchSetup.createMyDisplay()
xptTouch = touchSetup.createXPT(xpt_touch)
unispace = XglcdFont('Unispace12x24.c', 12, 24)

display.fill_rectangle(0, 0, display.width, display.height/2, GREEN) #green top half for go - will make gradient later
display.fill_rectangle(0, 160, display.width, 159, RED) #red bottom half for stop - will make gradient later
display.draw_text(0, 0, "Green for Go!", unispace,
                  color565(255, 255, 255), background=GREEN)
display.draw_text(0, display.height-25, "Its a red light!", unispace,
                  color565(255, 255, 255), background=RED)


#making the slider box
ScrollBox = Box(display.width, display.height, 40, display, color565(255, 255, 255))
display.fill_vrect(230, 0, 10, 319, color565(255,255,255))
ScrollBox.draw(230, 180)

tim = Timer()
def TimerTick(timer):
    global TimerReached
    TimerReached = True

tim.init(freq=25, mode=Timer.PERIODIC, callback=TimerTick)

touching = False


counter = 0
lastY = 0

while True:
    
    curEvent = event
    event = EVT_NO
    if curEvent!= EVT_NO:
        if curEvent == EVT_PenDown:
            
            touching = True
            lastY = y_passedTo_ISR
            
            #touchXY = xptTouch.get_touch()
            #xptTouch.send_command(xptTouch.GET_Y)
    
            # if touchXY != None:
            #     touchX = touchXY[0]
            #     touchY = touchXY[1]
            
    if TimerReached:
        TimerReached = False
        
        if touching:
            buff = xptTouch.raw_touch()
            if buff is not None:
                counter += 1
                x, y = xptTouch.normalize(*buff)
                lastX = x
                lastY = y
                #display.fill_vrect(220, y-20, 10, 40, color565(255, 255, 255))
                ScrollBox.draw(230, y)
                # if counter == 2:
                #     counter = 0
                nrf_simple.send(nrf, y)
                    
                    
                      
            else:
                event = EVT_PenUp
                touching = False



    

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

