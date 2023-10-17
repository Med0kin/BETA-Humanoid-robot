from model.PWMServo import PWMServo
from time import sleep

if __name__ == "__main__":
    servo = PWMServo(1, 2200, 800, 17)

    sleep(1)
    while(True):
        servo.move(2200, 4,verbose = True)
        sleep(6)
        servo.move(800, 4,verbose = True)
        sleep(6)
