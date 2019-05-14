# Add your Python code here. E.g.
from microbit import *
import time

###### Initialization of the hardware ######

# Turn off display to use display pins as GPIO
display.off()

# initialize serial communication (UART over USB)
uart.init(baudrate=115200)

while True:
    if (uart.any()):
    	input = uart.read()
    	uart.write(input)