# coding: utf8
import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import qimage2ndarray
import pose_estim_lib as pe
import s2t_lib
import numpy as np
import threading
from Servos.Servo import Servo
import arm_kinematics_lib as ak

import cv2
import time
"""
PySide2 app for controlling robot
"""


# Window class for the app
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Robot Control")

        self.width = 800
        self.height = 600
        self.setGeometry(100, 100, self.width, self.height)

        self.video_size = QSize(608, 456)
        self.camera_mode = 0

        self.expression_thread_running = True
        self.react_thread_running = True

        self.frame_counter = 0

        self.setup_UI()
        self.show()


# Setup UI
    def setup_UI(self):


        # Set full screen
        self.showFullScreen()

        # Set window icon and background color
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white;")

        # Left and right layouts
        self.leftLayout = QGridLayout()
        self.rightLayout = QVBoxLayout()

        # Video stream label
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(self.video_size)
        self.setup_camera()
        self.leftLayout.addWidget(self.camera_label)
        self.camera_label.hide()

        # Main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout, 40)
        self.mainLayout.addLayout(self.rightLayout, 10)
        self.setLayout(self.mainLayout)

        # Text box
        self.create_text_box()
        self.change_text("Welcome to the robot control app!")

        # Add face and reactions
        self.face_functionality()
        self.react_to_text()

        # Buttons style and font
        btn_font = QFont("System", 12)        
        button_style = "background-color: #00accc; font: 20px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center;"
        
        # MAIN MENU BUTTONS
        self.btns = QButtonGroup(self)
        btn = []
        for i, name in enumerate(["Camera", "Pose Estimation", "Button 3","Quit"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn.append(btn_temp)
            btn_count = i+1
            self.rightLayout.addWidget(btn[i])
            self.btns.addButton(btn[i], i)

        # Add button functionality
        # Can't figure out how to add this to for loop above without getting error
        btn[0].clicked.connect(lambda: self.btn_clickMain(0))
        btn[1].clicked.connect(lambda: self.btn_clickMain(1))
        btn[2].clicked.connect(lambda: self.btn_clickMain(2))
        btn[3].clicked.connect(lambda: self.btn_clickMain(3))



        # CAMERA BUTTONS
        self.btns1 = QButtonGroup(self)
        btn1 = []
        for i, name in enumerate(["Pause", "Back"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn1.append(btn_temp)
            btn1_count = i+1
            self.rightLayout.addWidget(btn1[i])
            self.btns1.addButton(btn1[i], i)

        # Add button functionality
        btn1[0].clicked.connect(lambda: self.btn_click1(0))
        btn1[1].clicked.connect(lambda: self.btn_click1(1))


        # POSE ESTIMATION BUTTONS
        self.btns2 = QButtonGroup(self)
        btn2 = []
        for i, name in enumerate(["Turned Off", "Back"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn2.append(btn_temp)
            btn2_count = i+1
            self.rightLayout.addWidget(btn2[i])
            self.btns2.addButton(btn2[i], i)

        # Add button functionality
        btn2[0].clicked.connect(lambda: self.btn_click2(0))
        btn2[1].clicked.connect(lambda: self.btn_click2(1))

        # Assign button count to each button group
        self.btns_count = {self.btns: btn_count, self.btns1: btn1_count, self.btns2: btn2_count}

        # Hide all buttons except main menu for start
        self.hide_buttons(self.btns1)
        self.hide_buttons(self.btns2)


    # Turn on face functionality
    def face_functionality(self):
        # default expression
        self.expression = "blinking"
        # Image
        self.create_image()
        self.make_robot_expressions()

    
    # BUTTONS REACTIONS
    def btn_clickMain(self, id):

        self.expression = "peeking"
        # Main menu
        if id == 0:
            # Camera
            self.swap_buttons(self.btns, self.btns1)
            # Show video stream & hide image
            self.img_label.hide()
            self.timer.start(30)
            self.camera_label.show()
        elif id == 1:
            # Pose Estimation
            self.swap_buttons(self.btns, self.btns2)
            # Show video stream & hide image
            self.img_label.hide()
            self.timer.start(30)
            self.camera_label.show()
        elif id == 2:
            # Button 3
            # disable/enable blinking
            if self.expression == "blinking":
                self.expression = "none"
                self.btns.button(2).setText("Enable Blinking")
            else:
                self.expression = "blinking"
                self.btns.button(2).setText("Disable Blinking")
        elif id == 3:
            # Quit
            self.stop_threads()
            self.close()

    def btn_click1(self, id):
        self.expression = "blinking"
        if id == 0:
            # Pause video stream or resume
            if self.timer.isActive():
                self.timer.stop()
                # Change button text
                self.btns1.button(0).setText("Resume")
            else:
                self.timer.start(30)
                # Change button text
                self.btns1.button(0).setText("Pause")
        elif id == 1:
            # Back
            self.swap_buttons(self.btns1, self.btns)
            # Remove video stream
            self.timer.stop()
            self.camera_label.hide()
            self.img_label.show()


    def btn_click2(self, id):
        self.expression = "blinking"
        # Button 1 menu
        if id == 0:

            # Switch camera mode
            if self.camera_mode == 0:
                self.camera_mode = 1
                self.btns2.button(0).setText("Pose Estim")
            elif self.camera_mode == 1:
                self.camera_mode = 2
                self.btns2.button(0).setText("Follow Mark")
            else:
                self.camera_mode = 0
                self.btns2.button(0).setText("Turned Off")

        elif id == 1:
            # Back
            self.swap_buttons(self.btns2, self.btns)
            self.camera_mode = 0
            # Remove video stream
            self.timer.stop()
            self.camera_label.hide()
            self.img_label.show()


    # Hides all buttons in a btnsGroup
    def hide_buttons(self, btnsGroup):
        for i in range(self.btns_count[btnsGroup]):
            btnsGroup.button(i).hide()

    # Shows all buttons in a btnsGroup
    def show_buttons(self, btnsGroup):
        for i in range(self.btns_count[btnsGroup]):
            btnsGroup.button(i).show()

    # Hides all buttons in btnsGroup1 and shows all buttons in btnsGroup2
    def swap_buttons(self, btnsGroup1, btnsGroup2):
        self.hide_buttons(btnsGroup1)
        self.show_buttons(btnsGroup2)

    # Creates an image and adds it to the left layout
    def create_image(self):
        self.img_label = QLabel('Image', self)
        #create path to image
        pixmap = QPixmap("neutral.png")
        # scale to the size of window
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.leftLayout.addWidget(self.img_label)

    # Changes the image in the left layout
    def change_image(self, image):
        pixmap = QPixmap(image + ".png")
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.img_label.setPixmap(pixmap)

    # Creates a text and adds it to the left layout
    def create_text_box(self):
        self.text_label = QLabel('Text', self)
        # Set font
        font = QFont()
        font.setPointSize(20)
        font.setFamily("System")
        self.text_label.setFont(font)
        # Change text color
        self.text_label.setStyleSheet("color: #00accc")
        # Set text alignment
        self.text_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.leftLayout.addWidget(self.text_label)
    
    # Changes the text in the left layout
    def change_text(self, text):
        self.text_label.setText(text)

    # FUCNTIONS FOR THREADS
    def make_robot_expressions(self):
        self.expression_thread_running = True
        self.expression_thread = threading.Thread(target=self.express)
        self.expression_thread.start()

    def react_to_text(self):
        self.react_thread_running = True
        self.react_thread = threading.Thread(target=self.react)
        self.react_thread.start()

    def stop_threads(self):
        self.expression_thread_running = False
        print("expression thread stopped")
        self.expression_thread.join()
        print("expression thread joined")
        self.react_thread_running = False
        print("react thread stopped")
        self.react_thread.join()
        print("react thread joined")
        s2t.close_thread()

    # EXPRESSIONS (happens in thread)
    def express(self):
        while True:
            if self.expression == "none":
                self.change_image("neutral")
                time.sleep(1)

            elif self.expression == "blinking":
                self.change_image("blink")
                time.sleep(0.1)
                self.change_image("neutral")
                time.sleep(2)

            elif self.expression == "peeking":
                self.change_image("left_peek")
                time.sleep(1)
                self.change_image("top_left_peek")
                time.sleep(1)
                self.change_image("left_peek")
                time.sleep(1)

            if self.expression_thread_running == False:
                print("expression thread stopped!")
                break

    # REACT TO TEXT (happens in thread)
    def react(self):
        while True:

            s2t_text_list = s2t.s2t_text.lower().split()

            text_received = s2t.s2t_text
            if len(text_received) > 30:
                text_received = text_received[:30] + "..."
            self.change_text(text_received)

            for txt in s2t_text_list:
                if txt in ["cześć", "hej", "witaj", "siema"]:
                    servo.acrobate("wave")
                elif txt == ("mrugaj"):
                    self.expression = "blinking"
                elif txt == ("podejrzyj"):
                    self.expression = "peeking"
                elif txt == ("przysiad"):
                    servo.setimport("p2")
                elif txt == ("wstawaj"):
                    servo.setimport("p13")
                elif txt == ("zatańcz"):
                    servo.acrobate("dancing")
                elif txt in ["chodź", "idź"]:
                    servo.acrobate("walking")
            if self.react_thread_running == False:
                print("react thread stopped!")
                break
            

    # Camera capture setup
    def setup_camera(self):
        self.video = cv2.VideoCapture("/dev/video0")
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)

    # Displays the camera capture
    def display_video_stream(self):
        self.frame_counter = self.frame_counter + 1
        ret, frame = self.video.read()
        if not ret:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # do it every 10 frames
        if self.frame_counter % 4 == 0:
            if self.camera_mode > 0:
                frame, id_list, loc, rot = pe.estimate_pose(frame)
                #if there are any markers on screen, control robot
                if self.camera_mode == 1:
                    if len(id_list) > 0:
                        self.control_with_estimated_pose(id_list, loc, rot)
                elif self.camera_mode == 2:
                    self.control_walking_with_marker(id_list, loc, rot)
            self.frame_counter = 0
        # flip frame
        frame = cv2.flip(frame, 1)
        # convert to QImage
        image = qimage2ndarray.array2qimage(frame)
        # set image to image label
        self.camera_label.setPixmap(QPixmap.fromImage(image))
        # set image label size

    def control_walking_with_marker(self, id_list, loc, rot):
        # if id_list is empty, stop walking
        if len(id_list) == 0:
            servo.walking = False
        else:
            z_ax = loc[id_list[0]][2]
            if z_ax > 0.1:
                servo.acrobate("endlesswalking")
            else:
                servo.warking = False


    def control_with_estimated_pose(self, id_list, loc, rot):
        # Rotation based
        servo_angle1 = ak.get_servo1_angle(rot[1][1])
        if round(servo.get(6)) != round(90):
            servo.set(6, 90)

        # Z axis distance based
        servo.set(4, 0)

        # Distance based
        if (1 in id_list) and (2 in id_list):
            servo_angle3 = ak.get_servo3_angle(ak.vector_length(ak.create_vector(loc[1], loc[2])))
            if round(servo.get(2)) != round(servo_angle3):
                servo.set(2, round(-(180 - servo_angle3)))

        # Rotation based
        servo_angle4 = ak.get_servo4_angle(rot[1][0])
        if round(servo.get(0)) != round(servo_angle4):
            servo.set(0, round(-servo_angle4))


# Main
servo = Servo()
servo.setimport("p13")
s2t = s2t_lib.speech_to_text()
myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
# Release the video capture
window.video.release()
# Close threads
servo.callback()
# Close the app
sys.exit()
