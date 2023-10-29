from model.TestServo import TestServo
from model.ServoController import ServoController

if __name__ == "__main__":
    servo1 = TestServo(1, 2200, 800)
    servo2 = TestServo(2, 2200, 800)
    servo3 = TestServo(3, 2200, 800)

    servo_controller = ServoController((servo1, servo2, servo3))


    servos = servo_controller._get_servos_by_ids([3, 1, 2])

    if servos == [servo1, servo2, servo3]:
        print("Success")
    else:
        print("Failure")
