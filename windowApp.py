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
import servo_lib

import cv2
import time
"""
PySide2 app for controlling robot
"""
class Window(QWidget):
    # d(-_-)b ~-=< INITIALIZATION >=-~ d(-_-)b
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Robot Control")

        self.width = 800
        self.height = 600
        self.setGeometry(100, 100, self.width, self.height)

        self.video_size = QSize(608, 456)
        self.camera_mode = 0

        self.setup_UI()
        self.show()

    # d(-_-)b ~-=< USER INTERFACE >=-~ d(-_-)b
    def setup_UI(self):


        # Set full screen
        #self.showFullScreen()

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

        self.create_text_box()
        self.change_text("Welcome to the robot control app!")
        self.face_functionality()

        # Buttons style and font
        btn_font = QFont("System", 12)        
        button_style = "background-color: #00accc; font: 20px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center;"
        
        # Main menu buttons
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

        # Can't figure out how to add this to for loop above without getting error
        btn[0].clicked.connect(lambda: self.btn_clickMain(0))
        btn[1].clicked.connect(lambda: self.btn_clickMain(1))
        btn[2].clicked.connect(lambda: self.btn_clickMain(2))
        btn[3].clicked.connect(lambda: self.btn_clickMain(3))



        # Camera buttons
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

        btn1[0].clicked.connect(lambda: self.btn_click1(0))
        btn1[1].clicked.connect(lambda: self.btn_click1(1))


        # Pose Estimation buttons
        self.btns2 = QButtonGroup(self)
        btn2 = []
        for i, name in enumerate(["Mode 0", "Back"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn2.append(btn_temp)
            btn2_count = i+1
            self.rightLayout.addWidget(btn2[i])
            self.btns2.addButton(btn2[i], i)

        btn2[0].clicked.connect(lambda: self.btn_click2(0))
        btn2[1].clicked.connect(lambda: self.btn_click2(1))

        self.btns_count = {self.btns: btn_count, self.btns1: btn1_count, self.btns2: btn2_count}
        self.hide_buttons(self.btns1)
        self.hide_buttons(self.btns2)


    def face_functionality(self):
        # default expression
        self.expression = "blinking"
        # Image
        self.create_image()
        self.make_robot_expressions()


        


        # d(-_-)b ~-=< BUTTON FUNCTIONALITY >=-~ d(-_-)b
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
                self.btns2.button(0).setText("Mode 1")
            else:
                self.camera_mode = 0
                self.btns2.button(0).setText("Mode 0")

        elif id == 1:
            # Back
            self.swap_buttons(self.btns2, self.btns)
            self.camera_mode = 0
            # Remove video stream
            self.timer.stop()
            self.camera_label.hide()
            self.img_label.show()



    # d(-_-)b ~-=< FUNCTIONS >=-~ d(-_-)b

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
        self.text_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.leftLayout.addWidget(self.text_label)
        
    def change_text(self, text):
        self.text_label.setText(text)

    # d(-_-)b ~-=< THREADS >=-~ d(-_-)b
    def make_robot_expressions(self):
        self.expression_thread = threading.Thread(target=self.express)
        self.expression_thread.start()
        self.expression_thread._stop = False

    # d(-_-)b ~-=< EXPRESSIONS (happens in thread) >=-~ d(-_-)b
    def express(self):
        while True:
            if self.expression == "none":
                self.change_image("neutral")
                time.sleep(1)

            if self.expression == "blinking":
                self.change_image("blink")
                time.sleep(0.1)
                self.change_image("neutral")
                time.sleep(2)

            if self.expression == "peeking":
                self.change_image("left_peek")
                time.sleep(1)
                self.change_image("top_left_peek")
                time.sleep(1)
                self.change_image("left_peek")
                time.sleep(1)
            self.change_text(s2t.s2t_text)
            if self.expression_thread._stop:
                break

    def react_to_text(self):
        self.react_thread = threading.Thread(target=self.react)
        self.react_thread.start()
        self.react_thread._stop = False

    def react(self):
        while True:
            # s2t_text to array of words
            s2t_text_list = s2t.s2t_text.split()
            if "hej" in s2t_text_list:
                self.expression = "none"

            if "mrugaj" in s2t_text_list:
                self.expression = "blinking"

            if self.react_thread._stop:
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
        ret, frame = self.video.read()
        if not ret:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frame = cv2.flip(frame, 1)

        if self.camera_mode == 1:
            frame, id_list = pe.estimate_pose(frame)
            print(id_list)
        # flip frame
        frame = cv2.flip(frame, 1)
        # convert to QImage
        image = qimage2ndarray.array2qimage(frame)
        # set image to image label
        self.camera_label.setPixmap(QPixmap.fromImage(image))
        # set image label size


# Main
servo_list = [10, 11, 12, 13, 14, 15, 16, 17]
angle_list = [0, 0, 0, 0, 0, 0, 0, 0]
servo = servo_lib.Servo()
servo.set_many_digital(servo_list, angle_list)
s2t = s2t_lib.speech_to_text()
myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
# Release the video capture
window.video.release()
# Close threads
window.expression_thread._stop = True
s2t.get_text_thread._stop = True
window.react_thread._stop = True
window.expression_thread.join()
s2t.get_text_thread.join()
window.react_thread.join()
servo.callback()
# Close the app
sys.exit()
