import time
import numpy as np

from Servos.Analog_servo import AServo
from Servos.OCServo import OCServo
from Servos.OCServo import serial_ports
import os
import psutil


# def checkIfProcessRunning(processName):
#     """
#     Check if there is any running process that contains the given name processName.
#     """
#     # Iterate over the all the running process
#     for proc in psutil.process_iter():
#         try:
#             # Check if process name contains the given name string.
#             if processName.lower() in proc.name().lower():
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False

def importpos(filename):
    filename = filename + '.txt'
    idlist = [0, 0, 0, 0, 0, 0, 0, 0]
    poslist = [0, 0, 0, 0, 0, 0, 0, 0]
    with open(filename, 'r') as f:
        for i in range(len(idlist)):
            line = f.readline().split()
            idlist[i] = int(line[0])
            poslist[i] = int(line[1])
        f.close()
    return idlist, poslist


class Servo:
    def __init__(self):
        ports = serial_ports()
        if len(ports) == 0:
            raise Exception("No serial ports found")
        self.digital = OCServo(ports[0])
        # if checkIfProcessRunning("pigpiod"):
        #     os.system("sudo pigpiod")
        self.armjoint = [AServo]*10

        self.gpio = AServo()

        # Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
        # Numeration         0  1  2  3   0  1    4  5  6  7
        #                    0  1  2  3   8  9    4  5  6  7

        # Create the servo objects
        self.armjoint[0] = AServo(17)
        self.armjoint[2] = AServo(27)
        self.armjoint[4] = AServo(22, 60)
        self.armjoint[6] = AServo(10)

        self.armjoint[1] = AServo(21)
        self.armjoint[3] = AServo(26)
        self.armjoint[5] = AServo(19, -60)
        self.armjoint[7] = AServo(13)
        self.armjoint[8] = AServo(9)      # hip 0
        self.armjoint[9] = AServo(11)     # hip 1
        servo180 = [4, 5, 6, 7, 8, 9]
        servo270 = [0, 1, 2, 3]

        for i in servo180:
            self.armjoint[i].set_range(180)

        for i in servo270:
            self.armjoint[i].set_range(270)

    def callback(self):
        for i in self.armjoint:
            i.stop_thread()
        # self.gpio.kill()
        self.digital.callback()


    def set(self, servo, angle):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            self.armjoint[servo].move_servo(angle)
        else:
            self.digital.send(servo, angle)

    def set_many_analog(self, servos, angles):
        if len(servos) != len(angles):
            raise Exception("Servo number and angle number mismatch")
        for i in servos:
            if i >= 10:
                raise Exception("Servo number out of range")
            self.set(i, angles[i])
            time.sleep(0.1)

    def set_many_digital(self, servos, angles):
        if len(servos) != len(angles):
            raise Exception("Servo number and angle number mismatch")
        for x in servos:
            if x < 10 or x > 17:
                raise Exception("Servo number out of range")
        self.digital.syncsend(servos, angles)

    def get(self, servo):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            return self.armjoint[servo].get_angle()
        else:
            return self.digital.get(servo)

    def setimport(self, filename):
        idlist, poslist = importpos(filename)
        if idlist[0] < 10:
            self.set_many_analog(idlist, poslist)
        else:
            self.set_many_digital(idlist, poslist)

    def setsequence(self, filenames, averagetime=1):
        for i in filenames:
            self.setimport(i)
            time.sleep(averagetime)

    def dance(self):
        act1 = ['p13', 'rgdL1', 'rgdL2', 'rgdL1', 'rgdL2', 'rrR1', 'rrR2', 'rrR1', 'rrR2', 'fRL1', 'fRL2',
                'fRL3', 'fRL4', 'fRL1', 'fRL2', 'fRL3', 'fRL4', 'pr1', 'pr', 'ch12', 'j22', 'default']
        act2 = ['default', 'pb1', 'default']
        act3 = ['pbn1', 'p13', 'pr1', 'pr']
        self.setsequence(act1, 1)
        self.setsequence(act2, 3)
        self.setsequence(act3, 1)

    def walk(self):
        loop = ['p13', 'ch12', 'ch22', 'ch3', 'ch44', 'ch51', 'ch9971', 'ch64', 'ch71', 'ch83', 'ch92', 'ch101', 'ch113'] #po wykonaniu powracasz do ch22 i zap�tlasz
        self.setsequence(loop)

