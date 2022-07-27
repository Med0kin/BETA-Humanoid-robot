

from dis import dis
import sys, os
from time import sleep
import numpy as np
import cv2
import sys
import argparse
import time
import math
import io
from contextlib import redirect_stdout

from servo_squat import *

import time
import numpy as np

from Speed import *


legjoint = [Servo_digit]*8
armjoint = [Servo]*8
hip = [Servo]*2

#try:
gpio = Servo()


stdout = io.StringIO()

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

loc = np.zeros((6,1), dtype=(float,3))
rot = np.zeros((6,1), dtype=(float,3))
hip = np.zeros((2,1), dtype=(float,3))
knee = np.zeros((2,1), dtype=(float,3))
ankle = np.zeros((2,1), dtype=(float,3))
add_point = np.zeros((2,1), dtype=(float,3))
hip_id = 0
iks = 0

def distance(d1, d2):
    x1, y1, z1 = d1
    x2, y2, z2 = d2
    
    d = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2) * 1.0)
    return d

def distance_2d(d1, d2):
    x1, y1, z1 = d1
    x2, y2, z2 = d2

    a1 = x1, z1
    a2 = x2, z2
    
    d = math.dist(a1, a2)
    print("dist2d" + str(d))
    return d


def printAngle(A, B, C):
     
    # Square of lengths be a2, b2, c2
    a2 = distance(B, C)
    b2 = distance(A, C)
    c2 = distance(A, B)
 
    # length of sides be a, b, c
    a = math.sqrt(a2);
    b = math.sqrt(b2);
    c = math.sqrt(c2);
 
    # From Cosine law
    alpha = math.acos((b2 + c2 - a2) /
                         (2 * b * c));
    betta = math.acos((a2 + c2 - b2) /
                         (2 * a * c));
    gamma = math.acos((a2 + b2 - c2) /
                         (2 * a * b));
 
    # Converting to degree
    alpha = alpha * 180 / math.pi;
    betta = betta * 180 / math.pi;
    gamma = gamma * 180 / math.pi;
 
    # printing all the angles
    print("alpha : %f" %(alpha))
    print("betta : %f" %(betta))
    print("gamma : %f" %(gamma))

def average(a, b):
    # print("a: " + str(a))
    # print("b: " + str(b))
    c = (a + b) / 2
    return c

def polar2cart(r, theta, phi):
    #print("theta: " + str(theta))
    #print("phi: " + str(phi))
    return [
         r * math.sin(theta) * math.cos(phi),
         r * math.sin(theta) * math.sin(phi),
         r * math.cos(theta)
    ]


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











def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    global iks

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict, parameters=parameters,
                                                                cameraMatrix=matrix_coefficients,
                                                                distCoeff=distortion_coefficients)


    # If markers are detected
    if len(corners) > 0:

        # Tweak so we have stable ids array that we use to determine which aruco markers we've got on screen
        ids_list = [0] * len(ids)
        for i in range(0, len(ids)):
            ids_list[i] = ids[i][0]


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

            R = cv2.Rodrigues(rvec[0])[0]
            
            # Define rotation and location values
            loc[ids_list[i]] = tvec[0][0][0] * -100, tvec[0][0][1] * -100, tvec[0][0][2] * 100
            rot[ids_list[i]] = rotationMatrixToEulerAngles(R)
            
            

            # Creating objects based on specific object's locations
            hip[0] = polar2cart(-4, rot[0,0][1]+np.pi/2, rot[0,0][2]) + loc[0]
            hip[1] = polar2cart(4, rot[0,0][1]+np.pi/2, rot[0,0][2]) + loc[0]
            if (ids_list[i] == 1):
                knee[0] = loc[ids_list[i]]
            if (ids_list[i] == 2):
                knee[1] = loc[ids_list[i]]
            if (ids_list[i] == 3):
                ankle[0] = loc[ids_list[i]]
                print(ankle[0,0])
            if (ids_list[i] == 4):
                ankle[1] = loc[ids_list[i]]
                
            if (all(x in ids_list for x in [0, 3])):
                squat_height = 15
                if (distance(ankle[0], hip[0]) > squat_height):
                    squat(0)

                if (distance(ankle[0], hip[0]) < squat_height):
                    squat(1)
'''
            # If legs is visible
            if (all(x in ids_list for x in [0, 1, 2, 3, 4])):
                printAngle(hip[0,0], knee[0,0], ankle[0,0])
                printAngle(hip[1,0], knee[1,0], ankle[1,0])

            elif (all(x in ids_list for x in [0, 1, 3])): 
                print("distance: ")
                print(distance(hip[0,0], ankle[0,0]))
                printAngle(hip[0,0], knee[0,0], ankle[0,0])

            elif (all(x in ids_list for x in [0, 2, 4])): 
                print("distance: ")
                print(distance(hip[0,0], ankle[0,0]))
                printAngle(hip[1,0], knee[1,0], ankle[1,0])

            print(ids_list)
'''
    return frame




if __name__ == '__main__':

    video = cv2.VideoCapture("/dev/video0")
    sleep(1.0)

    try:

        ap = argparse.ArgumentParser()
        ap.add_argument("-k", "--K_Matrix", default="calibration_matrix.npy",
                        help="Path to calibration matrix (numpy file)")
        ap.add_argument("-d", "--D_Coeff", default="distortion_coefficients.npy",
                        help="Path to distortion coefficients (numpy file)")
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
        '''
        video = cv2.VideoCapture("/dev/video0")
        sleep(1.0)
        '''
        while True:
            ret, frame = video.read()
            # frame = cv2.flip(frame,1)
            if not ret:
                break

            output = pose_esitmation(frame, aruco_dict_type, k, d)

            cv2.imshow('Estimated Pose', cv2.resize(cv2.flip(output, 1), (1280, 960)))


            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

    # Error messenge provider
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Woah!", e.__class__, "occurred.")
        print()
        print("Happened in main")
        #print(e)
        print(exc_type, fname, exc_tb.tb_lineno)
        video.release()
        cv2.destroyAllWindows()