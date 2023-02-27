import tkinter as tk

import time
import numpy as np

from speddo import *

armjoint = [Servo]*4

gpio = Servo()

#Create the servo objects
armjoint[0] = Servo(17)
armjoint[1] = Servo(27)
armjoint[2] = Servo(22)
armjoint[3] = Servo(10)

arm_lenght = 100

def rad_to_deg(rad):
    return rad * 180 / np.pi

#first servo angle is based on hand-marker rotation <- rot[x][1]
#second servo angle is based on z-axis location of hand-marker
#third servo angle is based on hand-marker distance from shoulder-marker
#fourth servo angle is based on hand-marker rotation <- rot[x][0]

#get first servo angle
def get_servo1_angle(servo ,rot):
    return rad_to_deg(rot[servo][1])

def get_servo2_angle(servo ,dist):

def get_servo3_angle(servo ,dist):
    return 1

#calculate angle in triangle having 3 sides
def get_angle(a,b,c):
    return np.arccos((a**2 + b**2 - c**2)/(2*a*b))







