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

#first servo angle is based on hand-marker rotation
#second servo angle is based on z-axis location of hand-marker
#third servo angle is based on hand-marker distance from shoulder-marker




