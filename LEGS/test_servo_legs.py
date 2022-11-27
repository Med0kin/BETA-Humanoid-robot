##test

from servo_legs import *

import numpy as np


legjoint = [Servo_digit]*8
hip = [Servo]*2

def define_digit():
    print("serDefined")
    legjoint[0] =  Servo_digit(10)
    time.sleep(0.1)
    legjoint[1] =  Servo_digit(11)
    time.sleep(0.1)
    legjoint[2] =  Servo_digit(12)
    time.sleep(0.1)
    legjoint[3] =  Servo_digit(13)
    time.sleep(0.1)
    legjoint[4] =  Servo_digit(14)
    time.sleep(0.1)
    legjoint[5] =  Servo_digit(15)
    time.sleep(0.1)
    legjoint[6] =  Servo_digit(16)
    time.sleep(0.1)
    legjoint[7] =  Servo_digit(17)
    time.sleep(0.1)

define_digit()

while(1):
    ser = input("Enter a servo number: ")
    if ser == "exit":
        break
    pos = input("Enter a position: ")
    legjoint[int(ser)].rotate(int(pos))