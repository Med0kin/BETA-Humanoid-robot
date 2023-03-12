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
        self.camera_mode = 0

        self.setup_UI()
        self.show()

    # d(-_-)b ~-=< USER INTERFACE >=-~ d(-_-)b
    def setup_UI(self):


        # Set full screen
        self.showFullScreen()

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

        #self.create_image()

        btn_font = QFont("System", 12)
        button_style = "background-color: cyan; font: 20px;\
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
        


    # d(-_-)b ~-=< BUTTON FUNCTIONALITY >=-~ d(-_-)b
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
            # Show video stream
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
        label1 = QLabel('Image', self)
        pixmap = QPixmap("serious.png")
        pixmap = pixmap.scaled(self.height-100, self.height-100, Qt.KeepAspectRatio)
        label1.setPixmap(pixmap)
        label1.setAlignment(Qt.AlignCenter)
        self.leftLayout.addRow(label1)

    # Camera capture setup
    def setup_camera(self):
        #self.capture = cv2.VideoCapture("/dev/video0")
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.video = cv2.VideoCapture("/dev/video0")
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
        self.image_label.setPixmap(QPixmap.fromImage(image))
        # set image label size
        self.image_label.setScaledContents(True)
        
'''
        cv2.imshow('Estimated Pose', cv2.resize(cv2.flip(frame, 1), (800, 600)))

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.video.release()
            cv2.destroyAllWindows()'''




# Main
myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
sys.exit()
