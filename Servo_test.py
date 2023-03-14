import time
from Servos.Servo import Servo

servolist = [10, 11, 12, 13, 14, 15, 16, 17]
anglelist = [0, 0, 0, 0, 0, 0, 0, 0]
akcja = ['p13', 'rgdL1', 'rgdL2', 'rgdL1', 'rgdL2', 'rrR1', 'rrR2','rrR1','rrR2','fRL1','fRL2','fRL3','fRL4','fRL1','fRL2','fRL3','fRL4','pr1','pr','ch12','j22','default','pb1','default','pbn1','p13','pr1','pr']
test = Servo()
# test.set_many_digital(servolist, anglelist)
test.setsequence(akcja, 1)

test.callback()
# for i in range(10):
#     test.set(i, 0)
#     time.sleep(0.5)
