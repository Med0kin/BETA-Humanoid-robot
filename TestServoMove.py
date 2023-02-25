import tkinter as tk

import time
import numpy as np

from Servo import *

armjoint = [Servo]*8

gpio = Servo()

# Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
# Numeration         0  1  2  3   0  1    4  5  6  7
#                    0  1  2  3   8  9    4  5  6  7

#Create the servo objects
armjoint[0] = Servo(17)
armjoint[1] = Servo(27)
armjoint[2] = Servo(22)
armjoint[3] = Servo(10)

armjoint[4] = Servo(13)
armjoint[5] = Servo(19)
armjoint[6] = Servo(26)
armjoint[7] = Servo(21)

#Enter the servo number and the angle you want to move, press q to quit
while True:

    servo = input("Enter servo: ")
    angle = input("Enter angle: ")
    speed = input("Enter speed: ")
    armjoint[0].move_servo(cord[0],100)

    if servo == 'q':
        break