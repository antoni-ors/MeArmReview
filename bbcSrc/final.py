# Add your Python code here. E.g.
from microbit import *
import time

###### Initialization of the hardware ######

# Turn off display to use display pins as GPIO
display.off()

# initialize the pins to control the Servos
gripper = pin16
right = pin15
left = pin14
base = pin13
servos = [right, left, base, gripper]
for servo in servos:
    servo.set_analog_period_microseconds(20000)
    servo.write_analog(76)

# initialize serial communication (UART over USB)
uart.init(baudrate=115200)

inStr = None
servoValues = []
def inStr2servoValues():
    """
    split and cast the string into numbers
    """
    global servoValues, inStr
    servoValues = [int(a) for a in inStr.split(',')]


def parseInputStr():
    """
    filter the string input based on the starting and ending byte
    The string input should be comma separated and starting with `s` and ending with `e`
    It is not being checked that it is comma separated but it should be.

    example of string: "s19,80,60,110e"

    Returns True if this sequence of string is complete. Otherwise False
    """
    global inStr
    msg = uart.read(1)
    ch = str(msg, 'UTF-8')
    if ch == 's':
        inStr = str()
    elif ch == 'e' and len(inStr)!= 0:
        inStr2servoValues()
        inStr = None
        return True
    elif inStr != None:
        inStr += ch
    return False


servoMax = int(2.0 * 1023.0 / 20)-1
servoMin = int(1.0 * 1023.0 / 20)+1
def clampForServo(value):
    """
    clamp the servo value not to be out of the range to 
    avoid problems like overheating and burning the servo.
    To make sure servos are being command in their allowed range.
    """
    if value < servoMin:
        return servoMin
    elif value > servoMax:
        return servoMax
    else:
        return value


def updateServos():
    """
    Update servos
    """
    global servoValues, servos
    for i in range(4):
        # servoValues[i] = clampForServo(servoValues[i])
        servos[i].write_analog(servoValues[i])

# Main Loop
while True:
    if (uart.any()):
        if(parseInputStr()):
            if(len(servoValues) == 4):
                updateServos()
                #print(servoValues)
