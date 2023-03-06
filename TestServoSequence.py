#import servo_lib


''' 
Program that imports servo angles from txt file
and sends them to the servos
'''

# Open txt file and return list of angles
def get_angles(file_name):
    with open(file_name, 'r') as f:
        angles = f.read().splitlines()
        for i in range(18):
            if angles[i] != '':
                angles[i] = int(angles[i])
    return angles

# Setting all servo angles with given speed/operation time
def set_angles(angles, time):
    for i in range(18):
        if angles[i] != '':
            #servo_lib.set_angle(i, angles[i], time)
            print(angles[i])
        else:
            print('No angle')
    return angles

print(get_angles('angles.txt'))

#array with actual servo angles
angles = [0]*18
angles = set_angles(get_angles('angles.txt'), 1)
print (angles)
