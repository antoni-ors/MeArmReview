# Add your Python code here. E.g.
from microbit import *
import time

###### Initialization of the hardware ######

# Turn off display to use display pins as GPIO
display.off()

# initialize serial communication (UART over USB)
uart.init(baudrate=115200)

# initialize pins to read Joystick
joyLeftX = pin0
joyLeftY = pin1
joyRightX = pin3
joyRighty = pin2

# initialize the pins to control the Servos
gripper = pin16
right = pin15
left = pin14
base = pin13
gripper.set_analog_period_microseconds(20000)
right.set_analog_period_microseconds(20000)
left.set_analog_period_microseconds(20000)
base.set_analog_period_microseconds(20000)

####### helper functions #########
# Servo Related:
# move specific servo by specific amount

# move specific servo to specific angle

# Serial Related:
# Parse serial

# send proper response if required

# 

####### Main Body #########
while True:
    # Just read Joysticks and print them
    print ("----------------------------------")
    print ("joyLeftX:" , joyLeftX.read_analog())
    print ("joyLeftY:" , joyLeftY.read_analog())
    print ("joyRightX:" , joyRightX.read_analog())
    print ("joyRighty:" , joyRighty.read_analog())
    time.sleep(1)