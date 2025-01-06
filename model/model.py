import serial
import time
from model import ServoController, Servo, BusServo, PWMServo

class Model:
    def __init__(self):
        self.serial = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=0.5)
        self.servos = (
            PWMServo(0,  2500, 500, 17),
            PWMServo(1,  2500, 500, 27),
            PWMServo(2,  2500, 500, 22),
            PWMServo(3,  2500, 500, 10),
            PWMServo(4,  2500, 500, 13),
            PWMServo(5,  2500, 500, 19),
            PWMServo(6,  2500, 500, 26),
            PWMServo(7,  2500, 500, 21),
            BusServo(10, 4095, 0, self.serial),
            BusServo(11, 4095, 0, self.serial),
            BusServo(12, 4095, 0, self.serial),
            BusServo(13, 4095, 0, self.serial),
            BusServo(14, 4095, 0, self.serial),
            BusServo(15, 4095, 0, self.serial),
            BusServo(16, 4095, 0, self.serial),
            BusServo(17, 4095, 0, self.serial)
        )
        self.servo_controller = ServoController(servos=self.servos, serial=self.serial)
        try:
            while(True):
                self.servo_controller.move(
                    [7],
                    [1800],
                    [2900],
                    verbose=True
                )
                time.sleep(3)
                self.servo_controller.move(
                    [7],
                    [1200],
                    [2900],
                    verbose=True
                )
                time.sleep(3)
        finally:
            self.serial.close()
            print("Serial closed")