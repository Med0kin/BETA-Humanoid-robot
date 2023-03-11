import numpy as np
import cv2
import sys
import argparse
import time
import math

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

def estimate_pose(frame):
    global frame_count

    # Load camera calibration
    aruco_dict_type = cv2.aruco.DICT_5X5_100
    matrix_coefficients = np.load('calibration_matrix.npy')
    distortion_coefficients = np.load('distortion_coefficients.npy')


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