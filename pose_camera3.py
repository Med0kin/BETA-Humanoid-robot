from tflite_runtime.interpreter import Interpreter
import os
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from pose_engine import PoseEngine
import time

engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
video = cv2.VideoCapture("/dev/video0")
time.sleep(1)
while True:
    ret, frame = video.read()
    if not ret:
        print("empty frame")
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(cv2.flip(frame, 1), (640, 480))
    jpg = Image.fromarray(frame).convert('RGB')

    poses, _ = engine.DetectPosesInImage(jpg)
    for pose in poses:
        print('\nPose Score: ', pose.score)
        for label, keypoint in pose.keypoints.items():
            print(' %-20s x=%-4d y=%-4d score=%.1f' %
                  (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
            if keypoint.score > 0.2:
                jpg = cv2.circle(jpg, (keypoint.point[0], keypoint.point[1]), 5, (0, 0, 255), -1)
    
            
    cv2.imshow("Frame", jpg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
video.release()
cv2.destroyAllWindows()