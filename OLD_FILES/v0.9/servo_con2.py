import time
import numpy as np

from Speed import *


legjoint = [Servo_digit]*8
armjoint = [Servo]*8
hip = [Servo]*2

#try:
gpio = Servo()

# Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
# Numeration         0  1  2  3   0  1    4  5  6  7
#                    0  1  2  3   8  9    4  5  6  7

armjoint[0] = Servo(17)
armjoint[1] = Servo(27)
armjoint[2] = Servo(22)
armjoint[3] = Servo(10)

armjoint[4] = Servo(13)
armjoint[5] = Servo(19)
armjoint[6] = Servo(26)
armjoint[7] = Servo(21)

hip[0] = Servo(9)
hip[1] = Servo(11)

print(type(legjoint[0]))

def close():
    for i in armjoint:
        armjoint.stop()
    hip[0].stop()
    hip[1].stop()

    gpio.kill()
    
    print("Analog Servos Terminated")


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
'''
while(1):
    x = input("Input servo number: ")
    if(x != 'exit' and int(x) < 8):
        armjoint[int(x)].moveAngle(int(input("Input your desired angle: ")),int(input("Input your desired speed: ")))
    elif(x != 'exit' and int(x) < 10):
        armjoint[int(x)-8].moveAngle(int(input("Input your desired angle: ")),int(input("Input your desired speed: ")))
    elif(x != 'exit' and int(x) >= 10):
        a = map_pos(int(input("Input your desired angle: ")))
        print(a)
        legjoint[int(x)-10].rotate(a, 500)
        time.sleep(1)
    else:
        #close()
        #serial.close()
        print("end")
        break
'''



#except:

#serial.close()
def squat(onof):
    if(onof==1):
        legjoint[0].rotate(90, 100)
        time.sleep(0.1)
        
        '''
    else:
        legjoint[0].rotate(90,500)
        time.sleep(0.1)
        legjoint[1].rotate(90,500)
        time.sleep(0.1)
        legjoint[2].rotate(90,1000)
        time.sleep(0.1)
        legjoint[3].rotate(90,1000)
        time.sleep(0.1)
        legjoint[4].rotate(90,250)
        time.sleep(0.1)
        legjoint[5].rotate(90,250)
        time.sleep(0.1)
'''
define_digit()
time.sleep(2)
squat(0)
time.sleep(5)
squat(1)
time.sleep(5)
squat(0)
