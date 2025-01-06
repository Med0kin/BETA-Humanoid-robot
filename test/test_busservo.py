from model import BusServo
from time import sleep
import serial

if __name__ == "__main__":
    serial = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=0.5)
    try:
        servo = BusServo(16, 0, 4095, serial)
        print(f"Servo ID: %d" % servo.id)
        while(1):
            sleep(1)
            servo.move(2200, 6,verbose = True)
            sleep(6)
            servo.move(800, 6,verbose = True)
            sleep(6)
    except:
        serial.close()
