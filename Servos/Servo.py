import time
import numpy as np

from Analog_servo import AServo
from OCServo import OCServo
from OCServo import serial_ports


class Servo:
    def __int__(self):
        ports = serial_ports()
        if len(ports) == 0:
            raise Exception("No serial ports found")
        self.__digital = OCServo(ports[0])
        self.__armjoint = [AServo]*10

        self.gpio = AServo()

        # Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
        # Numeration         0  1  2  3   0  1    4  5  6  7
        #                    0  1  2  3   8  9    4  5  6  7

        # Create the servo objects
        self.__armjoint[0] = AServo(17)
        self.__armjoint[1] = AServo(27)
        self.__armjoint[2] = AServo(22)
        self.__armjoint[3] = AServo(10)

        self.__armjoint[4] = AServo(13)
        self.__armjoint[5] = AServo(19)
        self.__armjoint[6] = AServo(26)
        self.__armjoint[7] = AServo(21)
        self.__armjoint[8] = AServo(9)      # hip 0
        self.__armjoint[9] = AServo(11)     # hip 1
        servo180 = [2, 3, 4, 5]
        servo270 = [0, 1, 6, 7]

        for i in servo180:
            self.__armjoint[i].set_range(180)

        for i in servo270:
            self.__armjoint[i].set_range(270)

    def callback(self):
        self.gpio.kill()

    def set(self, servo, angle):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            self.__armjoint[servo].move_servo(angle)
        else:
            self.__digital.send(servo, angle)

    def get(self, servo):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            return self.__armjoint[servo].get_angle()
        else:
            return self.__digital.get(servo)


if __name__ == "__main__":
    test = Servo()
