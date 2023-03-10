import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import time
"""
PySide2 app for controlling robot
"""
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Robot Control")

        self.width = 800
        self.height = 600
        self.setGeometry(100, 100, self.width, self.height)
        self.UI()
        self.show()

    # Setting up the UI
    def UI(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white;")

        #make layouts for left and right side
        self.leftLayout = QFormLayout()
        self.rightLayout = QVBoxLayout()

        #make main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout, 40)
        self.mainLayout.addLayout(self.rightLayout, 10)
        self.setLayout(self.mainLayout)

        self.createImage()

        self.createButtons()

    def createButtons(self):
        btnFont = QFont("System", 12)
        buttonSyle = "background-color: cyan; font: 20px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center;"
        
        self.btns = QButtonGroup(self)
        for i, btn in enumerate(["Button 1", "Button 2", "Button 3","Quit"]):
            btn = QPushButton(btn, self)
            btn.setStyleSheet(buttonSyle)
            btn.setFont(btnFont)
            self.btns.addButton(btn, i)
            self.rightLayout.addWidget(btn)
        self.btns.idClicked.connect(self.btnClick)

    def btnClick(self, id):
        print(id)
        if id == 3:
            self.close()


    def createImage(self):

        label1 = QLabel('Image', self)
        pixmap = QPixmap("serious.png")
        pixmap = pixmap.scaled(self.height-100, self.height-100, Qt.KeepAspectRatio)
        label1.setPixmap(pixmap)
        label1.setAlignment(Qt.AlignCenter)
        self.leftLayout.addRow(label1)


myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
sys.exit()
