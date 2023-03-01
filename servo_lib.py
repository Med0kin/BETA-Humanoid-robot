import serial
import time
import RPi.GPIO as GPIO
import pigpio
import threading

'''
    This is a class for the analog servos
'''

class Servo:
    _registry = []
    def __init__(self, servoNum=None):
        if(servoNum != None):
            self._registry.append(self)
            self.num = servoNum

            self.pos = 0
            self.speed = 50
            self.target = 0

            self.delay = time.sleep
            self.servo_range = 180
            self.max_angle = 90
            self.min_angle = -90
            self.opened_thread = False

            self.servo = pigpio.pi()
            self.servo.set_mode(servoNum, pigpio.OUTPUT)
            self.servo.set_PWM_frequency(servoNum, 50 )
            self.servo.set_servo_pulsewidth(self.num, 1500)

            self.run_thread()
        else:
            pass
        self.killer = GPIO.cleanup

    def kill(self):
        #Kill the servo
        self.killer

    def run_thread(self):
        #Run the servo in a thread
        self.thread = threading.Thread(target=self.servo_loop)
        self.thread.start()
        self.opened_thread = True
        return 1
    
    def move_servo(self, angle, speed):
        #Move the servo
        #if speed isn't in range 1-100 then stop
        if angle == self.pos:
            return 1
        if speed < 1 or speed > 100:
            return 0
        #if angle isn't in range
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle

        self.target = angle
        self.speed = speed
        return 1

    def set_pulsewidth_from_angle(self, angle):
        #Set the pulsewidth of the servo from the angle (500-2500)

        #angle -> pulsewidth
        pulsewidth = round(1500 + ((angle/(self.servo_range/2))*1000))

        self.servo.set_servo_pulsewidth(self.num, pulsewidth)
        
        self.pos = angle
        print("Position: ", self.pos)
        return 1
    
    def servo_loop(self):
        while True:
            if self.pos > self.target:
                self.set_pulsewidth_from_angle(round(self.pos - 1))
            elif self.pos < self.target:
                self.set_pulsewidth_from_angle(round(self.pos + 1))
            self.delay(1/self.speed)

            if self.opened_thread == False:
                break

