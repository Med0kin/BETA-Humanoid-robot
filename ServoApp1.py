import tkinter as tk
import sys
import time
import numpy as np

from servo_lib import *

armjoint = [Servo]*8

#try:
gpio = Servo()

# Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
# Numeration         0  1  2  3   0  1    4  5  6  7
#                    0  1  2  3   8  9    4  5  6  7

armjoint[0] = Servo(17) #17
armjoint[1] = Servo(27) #27
armjoint[2] = Servo(9)
armjoint[3] = Servo(11)

armjoint[4] = Servo(13)
armjoint[5] = Servo(19)
armjoint[6] = Servo(26)
armjoint[7] = Servo(21)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def map_pos(value):
    return round(translate(value, 0, 400, 0, 180))


root = tk.Tk()

def callback():
    for i in range(0, 4):
        try:
            armjoint[i].opened_thread = False
            armjoint[i].kill()
        except:
            print("Error")
    root.quit()
root.protocol("WM_DELETE_WINDOW", callback)
root.title('BETA Servo Manager')


bcg = "#3D82F0"
men = "#91B9F6"
blu = "#639BF3"
m_filter = ""


root.geometry("800x600")
root.config(bg = bcg)


w = 400
h = 400
x = w//2
y = h//2

tp_frame = tk.Frame(root)
tp_frame.pack(pady=20)

tframe1 = tk.Frame(tp_frame, bg=blu)
tframe1.pack(side=tk.LEFT)

tframe2 = tk.Frame(tp_frame, bg=blu)
tframe2.pack(side=tk.RIGHT)

tpad1 = tk.Canvas(tframe1, width=w, heigh=h, bg="white", cursor="dot")
tpad1.pack()

tpad2 = tk.Canvas(tframe2, width=w, heigh=h, bg="white", cursor="dot")
tpad2.pack()

circle1 = tpad1.create_oval(x, y, x+5, y+5, fill="black")

circle2 = tpad2.create_oval(x, y, x+5, y+5, fill="black")

coordinates1 = tk.Label(tframe1, text="Touchpad1", bg=men)
coordinates1.pack(pady=20)

coordinates2 = tk.Label(tframe2, text="Touchpad2", bg=men)
coordinates2.pack(pady=20)



def move1(event):
    global circle1
    pos = [event.x, event.y]
    for i in range(2):
        if(pos[i] < 0):
            pos[i] = 0
        elif(pos[i] > 400):
            pos[i] = 400

    tpad1.delete(circle1)
    circle1 = tpad1.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill="black")
    cord = [map_pos(pos[0]), 180-map_pos(pos[1])]

    coordinates1.config(text="Coordinates1 x: " + str(cord[0]) + ", y: " + str(cord[1]))

    armjoint[0].move_servo(cord[0]-90,100)
    armjoint[2].move_servo(cord[1]-90,100)


def move2(event):
    global circle2
    pos = [event.x, event.y]
    for i in range(2):
        if(pos[i] < 0):
            pos[i] = 0
        elif(pos[i] > 400):
            pos[i] = 400

    tpad2.delete(circle2)
    circle2 = tpad2.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill="black")
    cord = [map_pos(pos[0]), 180-map_pos(pos[1])]

    coordinates2.config(text="Coordinates2 x: " + str(cord[0]) + ", y: " + str(cord[1]))

    armjoint[1].move_servo(cord[0]-90,100)
    armjoint[3].move_servo(cord[1]-90,100)



tpad1.bind('<B1-Motion>', move1)
tpad2.bind('<B1-Motion>', move2)

root.mainloop()


