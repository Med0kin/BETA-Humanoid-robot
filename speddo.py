import serial
import time
import RPi.GPIO as GPIO
import pigpio
import threading

'''
    This is a class for the analog servos
'''

class Servo(threading.Thread):
    _registry = []
    def __init__(self, servoNum=None):
        if(servoNum != None):
            self._registry.append(self)
            
            threading.Thread.__init__(self)
            self.start()

            self.num = servoNum
            self.pos = 0
            self.delay = time.sleep
            self.servo_range = 180
            self.max_angle = 90
            self.min_angle = -90

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
        #Set the pulsewidth of the servo from the angle (500-2500)

        #if angle isn't in range 0-180 then stop
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle
            
        pulsewidth = round(1500 + ((angle/self.servo_range)*1000))

        self.servo.set_servo_pulsewidth(self.num, pulsewidth)
        self.pos = angle
        print("Position: ", self.pos)
        return 1
    
    def move_servo(self, angle, speed):
        #Move the servo
        #if speed isn't in range 1-100 then stop
        if speed < 1 or speed > 100:
            return 0
        
        while True:
            if self.pos == angle:
                return 1
            
            if self.pos > angle:
                self.set_pulsewidth_from_angle(round(self.pos - 1))
            else:
                self.set_pulsewidth_from_angle(round(self.pos + 1))
            self.delay(1/speed)