import time
import numpy as np

from Speed import *


legjoint = [Servo_digit]*8

# Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
# Numeration         0  1  2  3   0  1    4  5  6  7
#                    0  1  2  3   8  9    4  5  6  7


def define_digit():
    print("serDefined")
    legjoint[0] =  Servo_digit(10)
    time.sleep(0.1)






def squat(onof):
    if(onof==1):
        legjoint[0].rotate(70, 500)
        time.sleep(0.1)
    else:
        legjoint[0].rotate(90,500)
        time.sleep(0.1)


define_digit()
time.sleep(2)
squat(0)
time.sleep(5)
squat(1)
time.sleep(5)
squat(0)