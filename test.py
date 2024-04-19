from machine import Pin, PWM

# Define the pin
pwm_pin = PWM(Pin(0))

# Set the frequency
pwm_pin.freq(1000000)
temp = int(65535*0.5)
print (temp)
# Set the duty cycle
pwm_pin.duty_u16(temp)