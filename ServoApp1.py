import tkinter as tk
import sys
import time
import numpy as np

from Servos.Analog_servo import AServo

armjoint = [AServo]*8

# try:
gpio = AServo()
root = tk.Tk()

# Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
# Numeration         0  1  2  3   0  1    4  5  6  7
#                    0  1  2  3   8  9    4  5  6  7
arm = 0
armspos = [0, 0, 0, 0, 0, 0, 0, 0]
filename = "default"
filenamevar = tk.StringVar(root, value=filename)
w = 350
h = w
x = w//2
y = h//2

# Left hand
armjoint[0] = AServo(17) #17
armjoint[2] = AServo(27) #27
armjoint[4] = AServo(22) 
armjoint[6] = AServo(10)

# Right hand
armjoint[1] = AServo(21)
armjoint[3] = AServo(26)
armjoint[5] = AServo(19)
armjoint[7] = AServo(13)

armjoint[0].set_range(270)
armjoint[1].set_range(270)
armjoint[2].set_range(270)
armjoint[3].set_range(270)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def changearm():
    global arm
    arm = 1 - arm


def map_pos(value):
    global w
    return round(translate(value, 0, w, 0, 180))


def exportpos():
    global armspos
    global filename
    global filenamevar
    filename = filenamevar.get()
    filename = filename + '.txt'
    with open(filename, 'w') as f:
        for i in range(len(armspos)):
            f.write("%d %d\n" % (i, armspos[i]))
        f.close()


def importpos():
    global armspos
    global filename
    global filenamevar
    filename = filenamevar.get()
    filename = filename + '.txt'
    armspos = [0, 0, 0, 0, 0, 0, 0, 0]
    with open(filename, 'r') as f:
        for i in range(len(armspos)):
            line = f.readline().split()
            armspos[i] = int(line[1])
        f.close()
    for i in range(len(armspos)):
        armjoint[i].move_servo(armspos[i])

def callback():
    for i in range(0, 8):
        try:
            armjoint[i].opened_thread = False
            armjoint[i].kill()
        except:
            print("Error")
    root.quit()


root.protocol("WM_DELETE_WINDOW", callback)
root.title('BETA Servo Manager')
root.geometry("800x600")


bcg = "#3D82F0"
men = "#91B9F6"
blu = "#639BF3"
m_filter = ""

root.title('Servo Manager')
root.geometry("800x600")
root.config(bg=bcg)


tp_frame = tk.Frame(root)
tp_frame.pack(pady=10)

tframe1 = tk.Frame(tp_frame, bg=blu)
tframe1.pack(side=tk.LEFT)

tframe2 = tk.Frame(tp_frame, bg=blu)
tframe2.pack(side=tk.RIGHT)

tpad1 = tk.Canvas(tframe1, width=w, height=h, bg="white", cursor="dot")
tpad1.pack()

tpad2 = tk.Canvas(tframe2, width=w, height=h, bg="white", cursor="dot")
tpad2.pack()

circle1 = tpad1.create_oval(x, y, x+5, y+5, fill="black")

circle2 = tpad2.create_oval(x, y, x+5, y+5, fill="black")

coordinates1 = tk.Label(tframe1, text="Touchpad1", bg=men)
coordinates1.pack(pady=10)

coordinates2 = tk.Label(tframe2, text="Touchpad2", bg=men)
coordinates2.pack(pady=10)

b_changearm = tk.Button(root, text="CHANGE ARM", command=changearm, bg="#00ACCC")
b_changearm.pack(anchor=tk.S, side=tk.RIGHT)
b_export = tk.Button(root, text="EXPORT", command=exportpos, bg="#00ACCC")
b_export.pack(anchor=tk.S, side=tk.RIGHT)
filename_entry = tk.Entry(root, textvariable=filenamevar, bg="#00ACCC")
filename_entry.pack(anchor=tk.S, side=tk.RIGHT)
b_export = tk.Button(root, text="IMPORT", command=importpos, bg="#00ACCC")
b_export.pack(anchor=tk.S, side=tk.RIGHT)


def move1(event):
    global circle1
    global arm
    global w
    global armspos
    pos = [event.x, event.y]
    for i in range(2):
        if pos[i] < 0:
            pos[i] = 0
        elif pos[i] > w:
            pos[i] = w

    tpad1.delete(circle1)
    circle1 = tpad1.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill="black")
    cord = [map_pos(pos[0]), 180-map_pos(pos[1])]

    coordinates1.config(text="Coordinates1 x: " + str(cord[0]) + ", y: " + str(cord[1]))

    armspos[arm+2] = cord[0]-90
    armspos[arm+6] = cord[1]-90
    armjoint[arm+2].move_servo(cord[0]-90, 100)
    armjoint[arm+6].move_servo(cord[1]-90, 100)


def move2(event):
    global circle2
    global arm
    global w
    pos = [event.x, event.y]
    for i in range(2):
        if pos[i] < 0:
            pos[i] = 0
        elif pos[i] > w:
            pos[i] = w

    tpad2.delete(circle2)
    circle2 = tpad2.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill="black")
    cord = [map_pos(pos[0]), 180-map_pos(pos[1])]

    coordinates2.config(text="Coordinates2 x: " + str(cord[0]) + ", y: " + str(cord[1]))

    armspos[arm] = cord[0]-90
    armspos[arm+4] = cord[1]-90
    armjoint[arm].move_servo(cord[0]-90, 100)
    armjoint[arm+4].move_servo(cord[1]-90, 100)


tpad1.bind('<B1-Motion>', move1)
tpad2.bind('<B1-Motion>', move2)

root.mainloop()
