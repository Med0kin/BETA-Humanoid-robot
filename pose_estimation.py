import numpy as np
import cv2
import sys
import argparse
import time
import math
from servo_lib import *
import TestArmKinematic as ak


ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

loc = np.zeros((6), dtype=(float,3))
rot = np.zeros((6), dtype=(float,3))
frame_count = 0

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])

# Estimate pose of aruco markers
# and return frame

def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    global frame_count

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()


    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients)
    
    ids_list = []

        # If markers are detected
    if len(corners) > 0:

        # Tweak so we have stable ids array that we use to determine which aruco markers we've got on screen
        ids_list = [0] * len(ids)
        for i in range(0, len(ids)):
            ids_list[i] = ids[i][0]

        # If number in ids_list is grater than 5 then break
        if max(ids_list) > 5:
            return frame, ids_list

        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
            
            # get rid of that nasty numpy value array error
            (rvec - tvec).any()

            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners) 

            # Draw Axis
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
            corners_array = corners[0]
            #print(corners_array[0][0])


            # Rodrigues to get rotation
            R = cv2.Rodrigues(rvec[0])[0]
            # Define rotation and location values
            loc[ids_list[i]] = tvec[0][0][0], tvec[0][0][1], tvec[0][0][2]
            rot[ids_list[i]] = rotationMatrixToEulerAngles(R)


    return frame, ids_list

# Create vector from 2 points in 3D space
def create_vector(p1, p2):
    return np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])

# Calculate length of vector
def vector_length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

# Calculate angle between 2 vectors
def angle_between_vectors(v1, v2):
    return math.acos(np.dot(v1, v2) / (vector_length(v1) * vector_length(v2)))


# Main function

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--K_Matrix", default="calibration_matrix.npy" ,help="Path to calibration matrix (numpy file)")
    ap.add_argument("-d", "--D_Coeff", default="distortion_coefficients.npy", help="Path to distortion coefficients (numpy file)")
    ap.add_argument("-t", "--type", type=str, default="DICT_5X5_100", help="Type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    
    if ARUCO_DICT.get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    aruco_dict_type = ARUCO_DICT[args["type"]]
    calibration_matrix_path = args["K_Matrix"]
    distortion_coefficients_path = args["D_Coeff"]
    
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    #video = cv2.VideoCapture(0)
    video = cv2.VideoCapture("/dev/video0")
    time.sleep(2.0)

    # Create servo objects
    armjoint = [Servo]*8

    gpio = Servo()

    armjoint[3] = Servo(17)
    armjoint[2] = Servo(27)
    armjoint[1] = Servo(22)
    armjoint[0] = Servo(10)

    armjoint[4] = Servo(11)
    armjoint[5] = Servo(9)
    armjoint[2].max_angle = 110
    armjoint[2].min_angle = -110
    armjoint[2].servo_range = 270
    armjoint[3].servo_range = 270

    servo_angle3 = 0
    while True:
        ret, frame = video.read()

        if not ret:
            break
        
        output, ids_list = pose_esitmation(frame, aruco_dict_type, k, d)

        servo_angle1 = ak.get_servo1_angle(rot[1][1])
        #if there aren't 2 markers on screen, set servo angle to 0
        if len(ids_list) == 2:
            servo_angle3 = ak.get_servo3_angle(vector_length(create_vector(loc[1], loc[2])))
        servo_angle4 = ak.get_servo4_angle(rot[1][0])

        
        print("servoangle: ", servo_angle3)


        #if round(armjoint[0].pos) != round(servo_angle1):
        #    armjoint[0].move_servo(round(servo_angle1), 50)
        if round(armjoint[0].pos) != round(90):
            armjoint[0].move_servo(90, 50)
        if round(armjoint[2].pos) != round(servo_angle3):
            armjoint[2].move_servo(round(-(180 - servo_angle3)), 70)
        if round(armjoint[3].pos) != round(servo_angle4):
            armjoint[3].move_servo(round(-servo_angle4), 70)



        cv2.imshow('Estimated Pose', cv2.resize(cv2.flip(output, 1), (800, 600)))

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    for i in range(0, 4):
        armjoint[i].opened_thread = False
        armjoint[i].kill()

