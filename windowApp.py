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

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

from tflite_runtime.interpreter import Interpreter
import os
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from pose_engine import PoseEngine
import time
import threading

frame = None
poses = None
"""
PySide2 app for controlling robot
"""
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
    
    

# Window class for the app
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Robot Control")

        self.width = 800
        self.height = 600
        self.setGeometry(100, 100, self.width, self.height)

        self.language = "pl"

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

        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QStackedLayout()
        self.head_container = QWidget()
        self.head_layout = QGridLayout(self.head_container)
        self.settings_contrainer = QWidget()
        self.settings_layout = QGridLayout(self.settings_contrainer)
        self.cam_container = QWidget()
        self.cam_layout = QVBoxLayout(self.cam_container)
        self.right_layout = QVBoxLayout()

        # Video stream label
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(self.video_size)
        self.setup_camera()
        self.cam_layout.addWidget(self.camera_label)

        # Layouts configuration
        self.main_layout.addLayout(self.left_layout, 40)
        self.main_layout.addLayout(self.right_layout, 20)
        self.left_layout.addWidget(self.settings_contrainer)
        self.left_layout.addWidget(self.head_container)
        self.left_layout.addWidget(self.cam_container)
        self.left_layout.setCurrentIndex(1)
        self.setLayout(self.main_layout)

        # Settings
        self.setup_settings()

        # Text box
        self.setup_text()
        self.change_text("Welcome to the robot control app!")

        # Add face and reactions
        self.setup_image()
        self.face_functionality()
        self.react_to_text()

        # Buttons
        self.setup_buttons()

    def setup_settings(self):
        self.pl_button = PicButton(QPixmap("flag_pl.png"))
        self.pl_button.clicked.connect(lambda: self.change_language("pl"))
        self.us_button = PicButton(QPixmap("flag_us.png"))
        self.us_button.clicked.connect(lambda: self.change_language("us"))
        self.cs_button = PicButton(QPixmap("flag_cs.png"))
        self.cs_button.clicked.connect(lambda: self.change_language("cs"))
        # resize
        self.pl_button.setFixedSize(100, 100)
        self.us_button.setFixedSize(100, 100)
        self.cs_button.setFixedSize(100, 100)
        self.settings_layout.addWidget(self.pl_button)
        self.settings_layout.addWidget(self.us_button)
        self.settings_layout.addWidget(self.cs_button)
        self.settings_layout.setAlignment(Qt.AlignCenter)
        # set press button reaction



    def change_language(self, language):
        self.language = language
        s2t.set_language(self.language)
        print("Language changed to: " + self.language)

    def setup_buttons(self):
        # STYLE
        btn_font = QFont("System", 12)        
        button_style = "QPushButton { background-color: #00accc; font: 40px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center; }\
                    QPushButton:pressed { background-color: #005666; }"
        
        # MAIN MENU BUTTONS
        self.btns = QButtonGroup(self)
        btn = []
        for i, name in enumerate(["Camera", "Arms Control", "Settings", "Quit"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn.append(btn_temp)
            btn_count = i+1
            self.right_layout.addWidget(btn[i])
            self.btns.addButton(btn[i], i)
        # Add button functionality
        # ISSUE: Can't figure out how to add this to for loop above without getting error
        btn[0].clicked.connect(lambda: self.btn_click(0))
        btn[1].clicked.connect(lambda: self.btn_click(1))
        btn[2].clicked.connect(lambda: self.btn_click(2))
        btn[3].clicked.connect(lambda: self.btn_click(3))



        # CAMERA BUTTONS
        self.btns_cam = QButtonGroup(self)
        btn_cam = []
        for i, name in enumerate(["Aruco", "Control", "Controlers", "Back"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn_cam.append(btn_temp)
            btn_cam_count = i+1
            self.right_layout.addWidget(btn_cam[i])
            self.btns_cam.addButton(btn_cam[i], i)
        # Add button functionality
        btn_cam[0].clicked.connect(lambda: self.btn_cam_click(0))
        btn_cam[1].clicked.connect(lambda: self.btn_cam_click(1))
        btn_cam[2].clicked.connect(lambda: self.btn_cam_click(2))
        btn_cam[3].clicked.connect(lambda: self.btn_cam_click(3))


        # CONFIGURATION BUTTONS
        self.btns_cfg = QButtonGroup(self)
        btn_cfg = []
        for i, name in enumerate(["Back"]):
            btn_temp = QPushButton(name)
            btn_temp.setFont(btn_font)
            btn_temp.setStyleSheet(button_style)
            btn_cfg.append(btn_temp)
            btn_cfg_count = i+1
            self.right_layout.addWidget(btn_cfg[i])
            self.btns_cfg.addButton(btn_cfg[i], i)
        # Add button functionality
        btn_cfg[0].clicked.connect(lambda: self.btn_cfg_click(0))

        # ENDING SETUP
        # Assign button count to each button group
        self.btns_count = {self.btns: btn_count, self.btns_cam: btn_cam_count, self.btns_cfg: btn_cfg_count}

        # Hide all buttons except main menu for start
        self.hide_buttons(self.btns_cam)
        self.hide_buttons(self.btns_cfg)

    
    # BUTTONS REACTIONS
    def btn_click(self, id):
        self.expression = "peeking"
        # Main menu
        if id == 0: # Camera
            self.swap_buttons(self.btns, self.btns_cam)
            # Show video stream & hide image
            self.timer.start(30)
        elif id == 1: # Arms control
            os.system('python3 ServoApp1.py')
        elif id == 2: # Settings
            self.swap_buttons(self.btns, self.btns_cfg)
            self.left_layout.setCurrentIndex(0)

        elif id == 3: # Quit
            self.stop_threads()
            self.close()

    def btn_cam_click(self, id):
        self.expression = "blinking"
        if id == 0:
            self.left_layout.setCurrentIndex(2)
            self.timer.start(30)
        elif id == 1:
            self.left_layout.setCurrentIndex(2)
            self.timer.start(30)
        elif id == 2:
            print("Controlers")
        elif id == 3:
            # Back
            self.swap_buttons(self.btns_cam, self.btns)
            # Remove video stream
            self.timer2.stop()
            self.timer.stop()
            self.left_layout.setCurrentIndex(1)


    def btn_cfg_click(self, id):
        self.expression = "blinking"
        if id == 0: # Back
            self.swap_buttons(self.btns_cfg, self.btns)
            self.left_layout.setCurrentIndex(1)

    ### BUTTONS FUNCTIONS
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

    ### IMAGE AND TEXT
    # Creates an image and adds it to the left layout
    def setup_image(self):
        self.img_label = QLabel('Image', self)
        #create path to image
        pixmap = QPixmap("neutral.png")
        # scale to the size of window
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.head_layout.addWidget(self.img_label)

    # Changes the image in the left layout
    def change_image(self, image):
        pixmap = QPixmap(image + ".png")
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.img_label.setPixmap(pixmap)

    # Creates a text and adds it to the left layout
    def setup_text(self):
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
        self.head_layout.addWidget(self.text_label)
    
    # Changes the text in the left layout
    def change_text(self, text):
        self.text_label.setText(text)


    ### THREADS HANDLING
    # Turn on face functionality
    def face_functionality(self):
        # Defult expression
        self.expression = "blinking"
        # Start expression thread
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

    ### FUNCTIONS PASSED TO THREADS
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
    def init_model(self, lang_path):
        global words, labels, training, output, model, data

        with open("languages/" + lang_path + "/intents.json") as file:
            data = json.load(file)

        with open("languages/" + lang_path + "/data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)

        tensorflow.compat.v1.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        model.load("languages/" + lang_path + "/model.tflearn")
        print("model loaded")


    def bag_of_words(self, s, words):
        
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)

    def react(self):
        lang = self.language
        self.init_model(lang)
        old_text = None
        
        while True:
            if self.react_thread_running == False:
                print("react thread stopped!")
                break
            if lang != self.language:
                lang = self.language
                self.init_model(lang)

            s2t_text_list = s2t.s2t_text.lower().split()
            if s2t_text_list == old_text:
                continue

            text_received = s2t.s2t_text
            if len(text_received) > 30:
                text_received = text_received[:30] + "..."
            self.change_text(text_received)

            if "beta" not in s2t_text_list and "robot" not in s2t_text_list:
                continue

            old_text = s2t_text_list

            inp = s2t.s2t_text.lower()

            results = model.predict([self.bag_of_words(inp, words)])
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            if results[0][results_index] > 0.65:
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']

                response = random.choice(responses)
                if response == "dance":
                    dances_list = ["ballerina", "twist", "techno", "hipHop"]
                    random_dance = random.randint(0, len(dances_list) - 1)
                    response = dances_list[random_dance]
                servo.acrobate(response)
            else:
                print("none found")

    

    # Camera capture setup
    def setup_camera(self):
        self.video = cv2.VideoCapture("/dev/video0")
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')

    def pose_with_controller(self):
        ret, frame_pure = self.video.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(cv2.flip(frame_pure, 1), (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(frame).convert('RGB')
        poses, _ = self.engine.DetectPosesInImage(jpg)
        #poses, _ = engine.DetectPosesInImage(jpg)
        if poses is not None:
            for pose in poses:
                print('\nPose Score: ', pose.score)
                for label, keypoint in pose.keypoints.items():
                    print(' %-20s x=%-4d y=%-4d score=%.1f' %
                        (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
                    if keypoint.score > 0.1:
                        frame = cv2.circle(frame, (round(keypoint.point[0]), round(keypoint.point[1])), 5, (0, 0, 255), -1)
                    print(type(round(keypoint.point[0])))

        frame = cv2.flip(frame, 1)
        # convert to QImage
        image = qimage2ndarray.array2qimage(frame)
        # set image to image label
        print("img changed")
        self.camera_label.setPixmap(QPixmap.fromImage(image))

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
servo.setimport("start")
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
