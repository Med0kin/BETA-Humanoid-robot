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
        self.btns = QButtonGroup(self)
        btns_count = self.create_buttons(self.btns, ["Camera", "Pose Estimation", "Button 3","Quit"])
        self.btns.idClicked.connect(self.btn_clickMain)

        # Button 1 menu buttons
        self.btns1 = QButtonGroup(self)
        btns1_count = self.create_buttons(self.btns1, ["Pause", "Back"])
        self.btns1.idClicked.connect(self.btn_click1)

        # Button 2 menu buttons
        self.btns2 = QButtonGroup(self)
        btns2_count = self.create_buttons(self.btns2, ["Pause", "Back"])
        self.btns2.idClicked.connect(self.btn_click2)

        # Button 3 menu buttons
        self.btns3 = QButtonGroup(self)
        btns3_count = self.create_buttons(self.btns3, ["Button 6", "Button 7", "Back"])
        self.btns3.idClicked.connect(self.btn_click3)

        # Dicitonary of number of buttons in each menu
        self.btns_count = {self.btns : btns_count, self.btns1 : btns1_count, self.btns2 : btns2_count, self.btns3 : btns3_count}

        # Hide all buttons except main menu
        self.hide_buttons(self.btns1)
        self.hide_buttons(self.btns2)
        self.hide_buttons(self.btns3)



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

    # Creates buttons from a btnsGroup and a list of button names
    def create_buttons(self, btns , btnsList):
        # Set style and font for buttons
        btn_font = QFont("System", 12)
        button_style = "background-color: cyan; font: 20px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center;"
        # Loop through the list of buttons to create
        for i, btn in enumerate(btnsList):
            btn = QPushButton(btn, self)
            btn.setStyleSheet(button_style)
            btn.setFont(btn_font)
            btns.addButton(btn, i)
            self.rightLayout.addWidget(btn)
        # Return the number of buttons created
        return(i+1)

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
        label1 = QLabel('Image', self)
        pixmap = QPixmap("serious.png")
        pixmap = pixmap.scaled(self.height-100, self.height-100, Qt.KeepAspectRatio)
        label1.setPixmap(pixmap)
        label1.setAlignment(Qt.AlignCenter)
        self.leftLayout.addRow(label1)

    # Camera capture setup
    def setup_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.calib = np.load("calibration_matrix.npy")
        self.distortion = np.load("distortion_coefficients.npy")

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)

    # Displays the camera capture
    def display_video_stream(self):
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        if self.camera_mode == 1:
            frame, _ = pe.estimate_pose(frame, cv2.aruco.DICT_5X5_100, self.calib, self.distortion)
            print("Pose Estimation")

            image = qimage2ndarray.array2qimage(frame)
            self.image_label.setPixmap(QPixmap.fromImage(image))
        else:
            image = qimage2ndarray.array2qimage(frame)
            self.image_label.setPixmap(QPixmap.fromImage(image))

    


# Main
myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
sys.exit()
