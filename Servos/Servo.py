import time
import threading

from Servos.Analog_servo import AServo
from Servos.OCServo import OCServo
from Servos.OCServo import serial_ports
from pygame import mixer

mixer.init()

# def checkIfProcessRunning(processName):
#     """
#     Check if there is any running process that contains the given name processName.
#     """
#     # Iterate over the all the running process
#     for proc in psutil.process_iter():
#         try:
#             # Check if process name contains the given name string.
#             if processName.lower() in proc.name().lower():
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False

def importpos(filename):
    filename = '/home/pi/BETA-Humanoid-robot/Positions/' + filename + '.txt'
    idlist = [0, 0, 0, 0, 0, 0, 0, 0]
    poslist = [0, 0, 0, 0, 0, 0, 0, 0]
    with open(filename, 'r') as f:
        for i in range(len(idlist)):
            line = f.readline().split()
            idlist[i] = int(line[0])
            poslist[i] = int(line[1])
        f.close()
    return idlist, poslist

# /home/pi/BETA-Humanoid-robot/Positions/p13.txt
class Servo:
    def __init__(self):
        ports = serial_ports()
        if len(ports) == 0:
            raise Exception("No serial ports found")
        self.digital = OCServo(ports[0])
        # if checkIfProcessRunning("pigpiod"):
        #     os.system("sudo pigpiod")
        self.armjoint = [AServo]*10
        self.acrobations = ""
        self.walking = False
        self.choreographyswitch = True
        self.gpio = AServo()
        self.initialize()
        # Analog pins LtR   17 27 22 10   9 11   13 19 26 21  #
        # Numeration         0  1  2  3   0  1    4  5  6  7
        #                    0  1  2  3   8  9    4  5  6  7

        # Create the servo objects
        self.armjoint[0] = AServo(17)
        self.armjoint[2] = AServo(27)
        self.armjoint[4] = AServo(22, 60)
        self.armjoint[6] = AServo(10)

        self.armjoint[1] = AServo(21)
        self.armjoint[3] = AServo(26)
        self.armjoint[5] = AServo(19, -60)
        self.armjoint[7] = AServo(13)
        self.armjoint[8] = AServo(9)      # hip 0
        self.armjoint[9] = AServo(11)     # hip 1
        servo180 = [4, 5, 6, 7, 8, 9]
        servo270 = [0, 1, 2, 3]

        for i in servo180:
            self.armjoint[i].set_range(180)

        for i in servo270:
            self.armjoint[i].set_range(270)

    def callback(self):
        for i in self.armjoint:
            i.stop_thread()
        self.choreographyswitch = False
        self.acrobation.join()
        # self.gpio.kill()
        self.digital.callback()


    def set(self, servo, angle):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            self.armjoint[servo].move_servo(angle)
        else:
            self.digital.send(servo, angle)

    def set_many_analog(self, servos, angles):
        if len(servos) != len(angles):
            raise Exception("Servo number and angle number mismatch")
        for i in servos:
            if i >= 10:
                raise Exception("Servo number out of range")
            self.set(i, angles[i])
            time.sleep(0.1)

    def set_many_digital(self, servos, angles, speed=1000):
        if len(servos) != len(angles):
            raise Exception("Servo number and angle number mismatch")
        for x in servos:
            if x < 10 or x > 17:
                raise Exception("Servo number out of range")
        self.digital.syncsend(servos, angles, speed)

    def get(self, servo):
        if servo < 0 or servo > 17:
            raise Exception("Servo number out of range")
        elif servo < 10:
            return self.armjoint[servo].get_angle()
        else:
            return self.digital.get(servo)

    def setimport(self, filename, speed=1000):
        idlist, poslist = importpos(filename)
        if idlist[0] < 10:
            self.set_many_analog(idlist, poslist)
        else:
            self.set_many_digital(idlist, poslist, speed)

    def setsequence(self, filenames, averagetime=1):
        spd = averagetime * 1000
        for i in filenames:
            self.setimport(i, spd)
            time.sleep(averagetime)

    def dancing(self):
        self.is_dancing = True
        act1 = ['p13', 'rgdL1', 'rgdL2', 'rgdL1', 'rgdL2', 'rrR1', 'rrR2', 'rrR1', 'rrR2', 'fRL1', 'fRL2',
                'fRL3', 'fRL4', 'fRL1', 'fRL2', 'fRL3', 'fRL4', 'pr1', 'pr']
        act2 = [ 'ch12','j22']
        act3 = ['default']
        act4 = ['pb1', 'default']
        act5 = ['pbn1', 'p13', 'pr1', 'pr']
        self.setsequence(act1, 0.5)
        time.sleep(1)
        self.setsequence(act2, 1)
        self.setsequence(act3, 2)
        self.setsequence(act4, 4)
        self.setsequence(act5, 1)

    def wave(self):
        loop = ['pr', 'mach2', 'mach1', 'mach2', 'mach1', 'mach2', 'pr']
        self.setsequence(loop, 0.5)

    def squat(self):
        loop = ['start', 's1', 'start']
        self.setsequence(loop, 2)

    def rocking(self):
        loop = ['start', 'r1', 'r2', 'r1', 'r2', 'start']
        self.setsequence(loop)

    def rocking1(self):
        loop = ['r1']
        self.setsequence(loop)

    def rocking2(self):
        loop = ['r2']
        self.setsequence(loop)

    def standOnOneLeg(self):
        loop = ['start', 'w1', 'w2', 'w3', 'd1', 'w3', 'w2', 'w1', 'start']
        self.setsequence(loop
                         )

    def seaWave(self):
        loop = ['start', 'fRL1', 'fRL2',
                'fRL3', 'fRL4', 'fRL1', 'fRL2', 'fRL3', 'fRL4', 'pbn1', 'pr1']
        self.setsequence(loop)

    def matrix(self):
        loop = ['start', 'm1', 'fRL1', 'fRL2',
                'fRL3', 'fRL4', 'fRL1', 'fRL2', 'fRL3', 'fRL4', 'pbn1', 'start', 'pr1']
        self.setsequence(loop, 1)

    def jogging(self):
        loop = ['start', 'l1', 'l2',
                'l1', 'l2', 'l1', 'l2', 'start']
        self.setsequence(loop, 2)

    def jogging1(self):
        loop = ['l1']
        self.setsequence(loop)

    def jogging2(self):
        loop = ['l2']
        self.setsequence(loop)

    def inside(self):
        loop = ['i1']
        self.setsequence(loop)

    def outside(self):
        loop = ['o1']
        self.setsequence(loop)

    def insideOutside(self):
        loop = ['start', 'i1', 'o1',
                'i1', 'o1', 'i1', 'o1', 'start']
        self.setsequence(loop)

    def bow(self):
        loop = ['start', 'b1', 'start']
        self.setsequence(loop, 1)

    def ballerina(self):
        self.is_dancing = True
        act1 = ['start', 'w1', 'w2', 'w3', 'd1']
        act2 = ['default']
        act3 = ['pb1', 'default']
        act4 = ['w3', 'w2', 'w1', 'start']
        act5 = ['pbn1', 'pr1', 'pr']
        self.setsequence(act1, 1)
        self.setsequence(act2, 2)
        self.setsequence(act3, 4)
        self.setsequence(act4, 1)
        self.setsequence(act5, 1)

    #def ballerina(self):
    #    loop = ['start', 'w1', 'w2', 'w3', 'd1', 'default', 'pb1', 'default', 'w4', 'start', 'pbn1', 'pr1']
    #    self.setsequence(loop)

    def twist(self):
        loop = ['start', 'twist', 'w7', 'w15', 'w7', 'w15', 'w7', 'w15', 'w7', 'start', 'pbn1', 'pr1']
        self.setsequence(loop, 1)

    def techno(self):
        loop = ['start', 'rrR1', 'rrR2', 't', 't1', 't2', 't1', 'fRL1', 'fRL2',
                'fRL3', 'fRL4', 'fRL1', 'fRL2', 'fRL3', 'fRL4', 'pbn1', 'pr1']
        self.setsequence(loop)

    def hipHop(self):
        loop = ['start', 'r1', 'r2', 'r1', 'r2', 'r1', 'rgdL1', 'rgdL2', 'rgdL1', 'rgdL2', 'start', 'pbn1', 'pr1']
        self.setsequence(loop)

    def turnRight(self):
        loop = ['start', 'w15', 'w16', 'w18', 'start']
        self.setsequence(loop, 1)

    def turnLeft(self):
        loop = ['start', 'w7', 'w8',
                'w9', 'w10', 'w11', 'turnL', 'start',]
        self.setsequence(loop, 1)

    def walk(self):
        loop = ['start', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8',
                'w9', 'w10', 'w11', 'w12', 'w13', 'w14', 'w15', 'w16', 'w18', 'start'] #po wykonaniu powracasz do ch22 i zap�tlasz
        self.setsequence(loop, 0.5)

    def endlesswalking(self):
        self.walking = True
        start = ['start', 'w1', 'w2', 'w3']
        walk = ['w4', 'w5', 'w6', 'w7', 'w8',
                'w9', 'w10', 'w11', 'w12', 'w13', 'w14', 'w15', 'w16', 'w18']
        end = ['start']
        self.setsequence(start)
        while self.walking:
            self.setsequence(walk)
        self.setsequence(end)

    def coreography(self):
        while self.choreographyswitch:
            if self.acrobations == "dance":
                self.dancing()
                self.acrobations = ""
            elif self.acrobations == "walking":
                self.walk()
                self.acrobations = ""
            elif self.acrobations == "rocking":
                self.rocking()
                self.acrobations = ""
            elif self.acrobations == "rocking1":
                self.rocking1()
                self.acrobations = ""
            elif self.acrobations == "rocking2":
                self.rocking2()
                self.acrobations = ""
            elif self.acrobations == "inside":
                self.inside()
                self.acrobations = ""
            elif self.acrobations == "outside":
                self.outside()
                self.acrobations = ""
            elif self.acrobations == "standOnOneLeg":
                self.standOnOneLeg()
                self.acrobations = ""
            elif self.acrobations == "seaWave":
                self.seaWave()
                self.acrobations = ""
            elif self.acrobations == "matrix":
                self.matrix()
                self.acrobations = ""
            elif self.acrobations == "jogging":
                mixer.music.load('/home/pi/BETA-Humanoid-robot/Servos/jogging.mp3')
                mixer.music.set_volume(0.5)
                mixer.music.play()
                self.jogging()
                self.acrobations = ""
            elif self.acrobations == "jogging1":
                self.jogging1()
                self.acrobations = ""
            elif self.acrobations == "insideOutside":
                self.insideOutside()
                self.acrobations = ""
            elif self.acrobations == "bow":
                self.bow()
                self.acrobations = ""
            elif self.acrobations == "ballerina":
                mixer.music.load('/home/pi/BETA-Humanoid-robot/Servos/ballerina.mp3')
                mixer.music.set_volume(0.5)
                mixer.music.play()
                self.ballerina()
                self.acrobations = ""
            elif self.acrobations == "twist":
                mixer.music.load('/home/pi/BETA-Humanoid-robot/Servos/twist.mp3')
                mixer.music.set_volume(0.5)
                mixer.music.play()
                self.twist()
                self.acrobations = ""
            elif self.acrobations == "techno":
                self.techno()
                self.acrobations = ""
            elif self.acrobations == "hipHop":
                self.hipHop()
                self.acrobations = ""
            elif self.acrobations == "turnRight":
                self.turnRight()
                self.acrobations = ""
            elif self.acrobations == "turnLeft":
                self.turnLeft()
                self.acrobations = ""
            elif self.acrobations == "endlesswalking":
                self.endlesswalking()
                self.acrobations = ""
            elif self.acrobations == "wave":
                self.wave()
                self.acrobations = ""
            elif self.acrobations == "squat":
                self.squat()
                self.acrobations = ""
                

            else:
                time.sleep(0.5)

    def acrobate(self, acrobation):
        self.acrobations = acrobation

    def initialize(self):
        self.acrobation = threading.Thread(target=self.coreography)
        self.acrobation.start()
