import time
import RPi.GPIO as GPIO
import pigpio
import threading
import psutil
import os

class AServo:
    _registry = []

    def __init__(self, servoNum=None, target=1500):
        if servoNum is not None:
            self._registry.append(self)
            self.num = servoNum

            self.pos = 1500
            self.speed = 100
            self.target = target

            self.delay = time.sleep
            self.opened_thread = False

            self.servo = pigpio.pi()
            self.servo.set_mode(servoNum, pigpio.OUTPUT)
            self.servo.set_PWM_frequency(servoNum, 50)
            self.servo.set_servo_pulsewidth(self.num, 1500)

            self.run_thread()
        else:
            self.killer = GPIO.cleanup

    def kill(self):
        self.killer()

    def run_thread(self):
        self.thread = threading.Thread(target=self.servo_loop)
        self.opened_thread = True
        self.thread.start()
        return 1

    def move_servo(self, pulsewidth, speed=50):
        difference = abs(pulsewidth - self.pos)
        if difference < 5:
            return 1
        if speed < 1 or speed > 100:
            return 0
        if pulsewidth < 500:
            pulsewidth = 500
        elif pulsewidth > 2500:
            pulsewidth = 2500

        self.target = pulsewidth
        self.speed = speed
        return 1

    def set_pulsewidth(self, pulsewidth):
        self.servo.set_servo_pulsewidth(self.num, pulsewidth)
        self.pos = pulsewidth
        print("Position: ", self.pos)
        return 1

    def servo_loop(self):
        while True:
            self.delay(1 / self.speed)
            difference = abs(self.target - self.pos)
            step = 10 if difference > 10 else 1
            if self.pos < self.target:
                self.set_pulsewidth(self.pos + step)
            elif self.pos > self.target:
                self.set_pulsewidth(self.pos - step)
            if not self.opened_thread:
                break

    def stop_thread(self):
        self.opened_thread = False
        self.thread.join()
        return 1

    def set_range(self, srange):
        pass

    def get_angle(self):
        return self.pos