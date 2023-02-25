import serial
import time
import RPi.GPIO as GPIO
import pigpio
import threading

'''
    This is a class for the analog servos
'''

serial = serial.Serial(port='/dev/ttyUSB0',baudrate=1000000 ,timeout=2)

class Servo(threading.Thread):
    _registry = []
    def __init__(self, servoNum=None):
        if(servoNum != None):
            self._registry.append(self)
            
            threading.Thread.__init__(self)
            self.start()

            self.num = servoNum
            self.pos = 90
            self.delay = time.sleep

            self.servo = pigpio.pi()
            self.servo.set_mode(servoNum, pigpio.OUTPUT)
            self.servo.set_PWM_frequency(servoNum, 50 )
            self.servo.set_servo_pulsewidth(self.num, 1500)

        else:
            pass
        self.killer = GPIO.cleanup

    def kill(self):
        #Kill the servo
        self.killer

    def set_pulsewidth_from_angle(self, angle):
        #Set the pulsewidth of the servo from the angle
        pulsewidth = 500 + ((angle/180)*2000)

        self.servo.set_servo_pulsewidth(self.num, pulsewidth)
        self.pos = angle

    def move_servo(self, angle, speed):
        #Move the servo
        
        #if speed isn't in range 1-100 then stop
        if speed < 1 or speed > 100:
            return 0

        for _ in range(speed):
            self.set_pulsewidth_from_angle(round(angle))
            self.delay(1/speed)
            if self.pos == angle:
                return 1
            
            
        


    