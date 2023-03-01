import time
import numpy as np

from servo_lib import *

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

armjoint[0].servo_range = 270
armjoint[1].servo_range = 270
armjoint[1].max_angle = 180
armjoint[1].min_angle = -180

#Enter the servo number and the angle you want to move, press q to quit
while True:

    servo = input("Enter servo number: ")
    angle = input("Enter angle: ")
    speed = input("Enter speed: ")

    if servo == 'q' or angle == 'q' or speed == 'q':
        for i in range(8):
            armjoint[i].kill()
        break
    elif servo == 'r' or angle == 'r' or speed == 'r':
        for i in range(8):
            armjoint[i].move_servo(90,100)
        break
    else:
        armjoint[int(servo)].move_servo(int(angle),int(speed))
