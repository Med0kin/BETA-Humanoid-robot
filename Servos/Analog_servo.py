import time
import RPi.GPIO as GPIO
import pigpio
import threading
import psutil
import os




'''
    This is a class for the analog servos where:
    servoNum = id of the servo
    pos = current position of the servo
    speed = speed of the servo
    target = target position of the servo

    max_angle = maximum angle of the servo
    min_angle = minimum angle of the servo
    servo_range = srange of the servo

    opened_thread = determines if the thread is open
'''


class AServo:
    _registry = []

    def __init__(self, servoNum=None):

        if servoNum is not None:
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
            self.servo.set_PWM_frequency(servoNum, 50)
            self.servo.set_servo_pulsewidth(self.num, 1500)

            self.run_thread()
        else:
            self.killer = GPIO.cleanup

    def kill(self):
        # Kill the servo
        self.killer()

    # This is the function that runs the servo_loop in a thread
    def run_thread(self):
        # Run the servo in a thread
        self.thread = threading.Thread(target=self.servo_loop)
        self.opened_thread = True
        self.thread.start()
        return 1

    # This is the function that sets the target position
    # and speed of the servo
    def move_servo(self, angle, speed=50):
        # Move the servo
        # if speed isn't in srange 1-100 then stop
        difference = abs(angle - self.pos)
        if difference < 5:
            return 1
        if speed < 1 or speed > 100:
            return 0
        # if angle isn't in srange
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle

        self.target = angle
        self.speed = speed
        return 1

    # Sets the pulsewidth of the servo from the angle (500-2500)
    # This is the function that actually moves the servo
    def set_pulsewidth_from_angle(self, angle):

        # angle -> pulsewidth
        pulsewidth = round(1500 + ((angle / (self.servo_range / 2)) * 1000))

        self.servo.set_servo_pulsewidth(self.num, pulsewidth)

        self.pos = angle
        print("Position: ", self.pos)
        return 1

    # This is the loop that runs in the thread
    # It moves the servo to the target position
    # at specified speed
    def servo_loop(self):
        while True:
            self.delay(1 / self.speed)
            if self.pos > self.target:
                self.set_pulsewidth_from_angle(round(self.pos - 1))
            elif self.pos < self.target:
                self.set_pulsewidth_from_angle(round(self.pos + 1))

            if not self.opened_thread:
                break

    # This is the function that stops the thread
    def stop_thread(self):
        self.opened_thread = False
        self.thread.join()
        return 1

    # This is the function that sets range of the servo
    def set_range(self, srange):
        self.servo_range = srange
        self.max_angle = srange / 2
        self.min_angle = - srange / 2
        return 1

    def get_angle(self):
        return self.pos
