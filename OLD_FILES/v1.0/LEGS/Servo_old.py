'''
Nieaktualna wersja biblioteki
do sterowania serwomechanizmami
'''



import serial

serial = serial.Serial(port='/dev/ttyUSB0',baudrate=1000000 ,timeout=2)


def przemiel(x):
    if(x>15):
        return (255 - int(hex(x)[-2:],16))
    else:
        return (255 - x)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def map_pos(value):
    return round(translate(value, 0, 180, 0, 4095))



class Servo_digit(object):

    def __init__(self, id=None):
        self.id = id
        print("init1")
        serial.write(b'\xff\xff' + bytes([self.id])+ b'\x04\x02\x02\x01' + bytes([przemiel(self.id + 9)]))
        serial.write(b'\xff\xff' + bytes([self.id])+ b'\x04\x02\x02\x01' + bytes([przemiel(self.id + 15)]))
        print("init2")
        
    def rotate(self, angle, speed):
        print("rot1")
        msg = bytes([self.id]) + b'\x09\x03\x2a' + (angle).to_bytes(2, byteorder='little') + b'\x00\x00' + (speed).to_bytes(2, byteorder='little')
        sum = 0
        for i in range(10):
            sum += msg[i]

        msg = b'\xff\xff' + msg + bytes([przemiel(sum)])
        #serial.write(msg)
        print(msg)
        serial.write(msg)



class Servo(object):
    _registry = []
    def __init__(self, servoNum=None):
        import RPi.GPIO as GPIO
        import pigpio
        import time
        if(servoNum != None):
            self._registry.append(self)
            
            self.num = servoNum
            self.delay = time.sleep

            self.servo = pigpio.pi() 
            self.servo.set_mode(servoNum, pigpio.OUTPUT)
            
            self.servo.set_PWM_frequency(servoNum, 50 )
        else:
            pass
        self.killer = GPIO.cleanup

    def kill(self):
        self.killer

    def setAngle(self, angle):
        ang = 500 + ((angle/180)*2000)
        #x = 2+(ang/18)
        #print(x)
        
        self.servo.set_servo_pulsewidth(self.num, ang)

    def stop(self):
        self.servo.stop()
        #self.kill()
        print("\nGoodbye!")
        
