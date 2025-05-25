import serial
import time
from model import STT, ServoController, Servo, BusServo, PWMServo, ServoAcrobat

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
            BusServo(10, 4095, 0, self.serial), #8
            BusServo(11, 4095, 0, self.serial), #9
            BusServo(12, 4095, 0, self.serial), #10
            BusServo(13, 4095, 0, self.serial), #11
            BusServo(14, 4095, 0, self.serial), #12
            BusServo(15, 4095, 0, self.serial), #13
            BusServo(16, 4095, 0, self.serial), #14
            BusServo(17, 4095, 0, self.serial) #15
        )
        for i in [9, 10, 12, 14]:
            self.servos[i].is_inverted = True
        self.servo_controller = ServoController(servos=self.servos, serial=self.serial)
        self.servo_acrobat = ServoAcrobat(servoController=self.servo_controller)
        self.stt = STT(self.servo_acrobat, self.servo_controller)
        self.servo_controller.move([1, 2, 3, 4, 5, 6], [1000, 2300, 1200, 1700, 700, 2000], [2000, 2000, 2000, 2000, 2000, 2000])
        time.sleep(2)
        self.servo_acrobat.move_to_position("no1_x", 1000)
        # for i in range(3):
        #     self.servo_acrobat.move_to_position("no2_x", 1000)
        #     self.servo_acrobat.move_to_position("no3_x", 200)
        #     self.servo_acrobat.move_to_position("no4_x", 500)
        #     self.servo_acrobat.move_to_position("no5_x", 100)
        #     self.servo_acrobat.move_to_position("no6_x", 1000)
        #     self.servo_acrobat.move_to_position("no7_x", 200)
        #     self.servo_acrobat.move_to_position("no8_x", 100)
        #     self.servo_acrobat.move_to_position("no9_x", 150)
        #     self.servo_acrobat.move_to_position("no10_x", 500)
        #     self.servo_acrobat.move_to_position("no11_x", 400)
        #     self.servo_acrobat.move_to_position("no12_x", 500)
        #     self.servo_acrobat.move_to_position("no13_x", 1000)
        # self.servo_acrobat.move_to_position("no2_x", 1200)
        # self.servo_acrobat.move_to_position("no1_x", 1000)
        #self.servo_controller.move([10, 11, 12, 13, 14, 15, 16, 17], [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000], [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000])
