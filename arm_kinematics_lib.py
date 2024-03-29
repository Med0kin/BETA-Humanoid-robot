import time
import numpy as np
import math
'''
from servo_lib import *

armjoint = [Servo]*4
gpio = Servo()

#Create the servo objects
armjoint[0] = Servo(17)
armjoint[1] = Servo(27)
armjoint[2] = Servo(22)
armjoint[3] = Servo(10)
'''
arm_lenght = 0.15

# Create vector from 2 points in 3D space
def create_vector(p1, p2):
    return np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])

# Calculate length of vector
def vector_length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

# Calculate angle between 2 vectors
def angle_between_vectors(v1, v2):
    return math.acos(np.dot(v1, v2) / (vector_length(v1) * vector_length(v2)))

def rad_to_deg(rad):
    return rad * 180 / np.pi

#calculate angle in triangle having 3 sides (C is the angle)
def get_angle(a,b,c):
    return rad_to_deg(np.arccos((a**2 + b**2 - c**2)/(2*a*b)))

#first servo angle is based on hand-marker rotation <- rot[x][1]
#second servo angle is based on z-axis location of hand-marker
#third servo angle is based on hand-marker distance from shoulder-marker
#fourth servo angle is based on hand-marker rotation <- rot[x][0]

#get first servo angle
def get_servo1_angle(rot):
    return rad_to_deg(rot)
def get_servo2_angle(z_dist):
    return (90*z_dist)/arm_lenght
def get_servo3_angle(dist):
    if dist>arm_lenght:
        dist = arm_lenght
    return get_angle(arm_lenght/2,arm_lenght/2,dist)
def get_servo4_angle(rot):
    if rot > 0:
        return rad_to_deg(math.pi - rot)
    else:
        return rad_to_deg(-math.pi - rot)