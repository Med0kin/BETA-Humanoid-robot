import time
import numpy as np

from Analog_servo import AServo
from OCServo import OCServo
from OCServo import serial_ports
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
        self.armjoint[1] = AServo(27)
        self.armjoint[2] = AServo(22, 83)
        self.armjoint[3] = AServo(10)

        self.armjoint[4] = AServo(13)
        self.armjoint[5] = AServo(19, -80)
        self.armjoint[6] = AServo(26)
        self.armjoint[7] = AServo(21)
        self.armjoint[8] = AServo(9)      # hip 0
        self.armjoint[9] = AServo(11)     # hip 1
        servo180 = [2, 3, 4, 5]
        servo270 = [0, 1, 6, 7]

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

    def set_many_analog(self, position):
        if len(position[0]) != len(position[1]):
            raise Exception("Servo number and angle number mismatch")
        for i, a in position:
            if i >= 10:
                raise Exception("Servo number out of range")
            self.set(i, a)

    def set_many_digital(self, position):
        if len(position[0]) != len(position[1]):
            raise Exception("Servo number and angle number mismatch")
        for i, a in position:
            if i < 10:
                raise Exception("Servo number out of range")
        self.digital.syncsend(i, a)

    def get(self, servo):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            return self.armjoint[servo].get_angle()
        else:
            return self.digital.get(servo)


if __name__ == "__main__":
    position = ([10, 11, 12, 13, 14, 15, 16, 17], [0, 0, 0, 0, 0, 0, 0, 0])
    test = Servo()
    test.set_many_digital(position)
    time.sleep(1)
    test.callback()
    # for i in range(10):
    #     test.set(i, 0)
    #     time.sleep(0.5)
