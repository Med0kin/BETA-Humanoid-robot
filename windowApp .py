import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import time
"""
PySide2 app for controlling robot
"""
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Robot Control")
        self.setGeometry(100, 100, 800, 600)
        self.UI()
        self.show()
        self.createButtons()

    # Setting up the UI
    def UI(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white;")

    def createButtons(self):
        buttonSyle = "background-color: cyan; font: bold 20px;\
                    border-radius: 10px; border: 2px solid black;\
                    padding: 10px; margin: 10px; text-align: center;"
        
        btnFont = QFont("System", 12)
        
        btn1 = QPushButton("Button 1", self)
        btn1.setStyleSheet(buttonSyle)
        btn1.clicked.connect(self.btn1Click)
        btn1.setFont(btnFont)
        btn1.move(100, 100)

        btn2 = QPushButton("Button 2", self)
        btn2.setStyleSheet(buttonSyle)
        btn2.clicked.connect(self.btn2Click)
        btn2.setFont(btnFont)
        btn2.move(100, 200)

        btn3 = QPushButton("Button 3", self)
        btn3.setStyleSheet(buttonSyle)
        btn3.clicked.connect(self.btn3Click)
        btn3.setFont(btnFont)
        btn3.move(100, 300)

        # show buttons
        btn1.show()
        btn2.show()
        btn3.show()



    def btn1Click(self):
        print("Button 1 clicked")

    def btn2Click(self):
        print("Button 2 clicked")

    def btn3Click(self):
        print("Button 3 clicked")

    


myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
sys.exit()
