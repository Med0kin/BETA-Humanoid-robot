from Servo import *
import time


legjoint = [Servo_digit]*8



def define_digit():
    print("serDefined")
    legjoint[0] =  Servo_digit(10)
    time.sleep(0.025)
    legjoint[1] =  Servo_digit(11)
    time.sleep(0.025)
    '''
    legjoint[2] =  Servo_digit(12)
    time.sleep(0.025)
    legjoint[3] =  Servo_digit(13)
    time.sleep(0.025)
    legjoint[4] =  Servo_digit(14)
    time.sleep(0.025)
    legjoint[5] =  Servo_digit(15)
    time.sleep(0.025)
    legjoint[6] =  Servo_digit(16)
    time.sleep(0.025)
    legjoint[7] =  Servo_digit(17)
    time.sleep(0.025)
    '''


define_digit()


def squat(onof):
    if(onof==1):
        legjoint[0].rotate(1500, 500)
        legjoint[1].rotate(1500, 500)

  

while(1):
    x = input("Szpagat I/O: ")
    if(type(x) == str):
        if(x == 'exit'):
            break
        elif(x == '1'):
            squat(1)
        elif(x == '0'):
            squat(0)
        else:
            print("Invalid input")