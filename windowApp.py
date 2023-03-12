import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import qimage2ndarray
import pose_estim_lib as pe
import numpy as np



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

        self.video_size = QSize(320, 240)
        self.camera_mode = 1

        self.setup_UI()
        self.show()

    # d(-_-)b ~-=< USER INTERFACE >=-~ d(-_-)b
    def setup_UI(self):
        # Set window icon and background color
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white;")

        # Left and right layouts
        self.leftLayout = QFormLayout()
        self.rightLayout = QVBoxLayout()

        # Video stream label
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)
        self.setup_camera()
        self.leftLayout.addWidget(self.image_label)
        self.image_label.hide()

        # Main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout, 40)
        self.mainLayout.addLayout(self.rightLayout, 10)
        self.setLayout(self.mainLayout)

        self.create_image()
        
        # Main menu buttons
        for i, name in enumerate(["Camera", "Pose Estimation", "Button 3","Quit"]):
            btn = QPushButton(name)
            btn.clicked.connect(lambda: self.btn_clickMain(i))
            self.rightLayout.addWidget(btn)
            btn_count = i+1

        
        # hide buttons in right layout
        for i in range(btn_count):
            self.rightLayout.itemAt(i).widget().hide()
            


        



    # d(-_-)b ~-=< BUTTON FUNCTIONS >=-~ d(-_-)b
    def btn_clickMain(self, id):
        print(id)
        # Main menu
        if id == 0:
            # Camera
            self.swap_buttons(self.btns, self.btns1)

            # Show video stream
            self.timer.start(30)
            self.image_label.show()

        elif id == 1:
            # Pose Estimation
            self.swap_buttons(self.btns, self.btns2)

            self.timer.start(30)
            self.image_label.show()


        elif id == 2:
            # Button 3
            self.swap_buttons(self.btns, self.btns3)
        elif id == 3:
            # Quit
            self.close()

    def btn_click1(self, id):
        print(id)
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
            self.image_label.hide()


    def btn_click2(self, id):
        print(id)
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
            self.image_label.hide()

    def btn_click3(self, id):
        print(id)
        # Button 1 menu
        if id == 0:
            # Button 4
            pass
        elif id == 1:
            # Button 5
            pass
        elif id == 2:
            # Back
            self.swap_buttons(self.btns3, self.btns)



    # d(-_-)b ~-=< FUNCTIONS >=-~ d(-_-)b

    # Creates an image and adds it to the left layout
    def create_image(self):
        label1 = QLabel('Image', self)
        pixmap = QPixmap("serious.png")
        pixmap = pixmap.scaled(self.height-100, self.height-100, Qt.KeepAspectRatio)
        label1.setPixmap(pixmap)
        label1.setAlignment(Qt.AlignCenter)
        self.leftLayout.addRow(label1)

    # Camera capture setup
    def setup_camera(self):
        self.capture = cv2.VideoCapture("/dev/video2")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)

    # Displays the camera capture
    def display_video_stream(self):
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        if self.camera_mode == 1:
            frame, id_list = pe.estimate_pose(frame)
            print(id_list)
        image = qimage2ndarray.array2qimage(frame)
        self.image_label.setPixmap(QPixmap.fromImage(image))




# Main
myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
sys.exit()
