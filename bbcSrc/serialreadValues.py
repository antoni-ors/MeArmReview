# Add your Python code here. E.g.
from microbit import *
import time

###### Initialization of the hardware ######

# Turn off display to use display pins as GPIO
display.off()

# initialize serial communication (UART over USB)
uart.init(baudrate=115200)

inStr = None
inValues = []

def inStr2inValues():
    global inValues
    inValues = [float(a) for a in inStr.split(',')]

def parseInputStr():
    global inStr
    msg = uart.read(1)
    ch = str(msg, 'UTF-8')
    if ch == 's':
        inStr = str()
    elif ch == 'e' and len(inStr)!= 0:
        inStr2inValues()
        inStr = None
        return True
    elif inStr != None:
        inStr += ch
    return False

while True:
    if (uart.any()):
        if(parseInputStr()):
            print (inValues)
