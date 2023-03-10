import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
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
        self.UI()
        self.show()

    # d(-_-)b ~-=< USER INTERFACE >=-~ d(-_-)b
    def UI(self):
        # Set window icon and background color
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white;")

        # Left and right layouts
        self.leftLayout = QFormLayout()
        self.rightLayout = QVBoxLayout()

        # Main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout, 40)
        self.mainLayout.addLayout(self.rightLayout, 10)
        self.setLayout(self.mainLayout)

        self.createImage()
        
        # Main menu buttons
        self.btns = QButtonGroup(self)
        btnsCount = self.createButtons(self.btns, ["Button 1", "Button 2", "Button 3","Quit"])
        self.btns.idClicked.connect(self.btnClickMain)

        # Button 1 menu buttons
        self.btns1 = QButtonGroup(self)
        btns1Count = self.createButtons(self.btns1, ["Button 4", "Back"])
        self.btns1.idClicked.connect(self.btnClick1)

        # Button 2 menu buttons
        self.btns2 = QButtonGroup(self)
        btns2Count = self.createButtons(self.btns2, ["Button 5", "Back"])
        self.btns2.idClicked.connect(self.btnClick2)

        # Button 3 menu buttons
        self.btns3 = QButtonGroup(self)
        btns3Count = self.createButtons(self.btns3, ["Button 6", "Button 7", "Back"])
        self.btns3.idClicked.connect(self.btnClick3)

        # Dicitonary of number of buttons in each menu
        self.btnsCount = {self.btns : btnsCount, self.btns1 : btns1Count, self.btns2 : btns2Count, self.btns3 : btns3Count}

        # Hide all buttons except main menu
        self.hideButtons(self.btns1)
        self.hideButtons(self.btns2)
        self.hideButtons(self.btns3)



    # d(-_-)b ~-=< BUTTON FUNCTIONS >=-~ d(-_-)b

    def btnClickMain(self, id):
        print(id)
        # Main menu
        if id == 0:
            # Button 1
            self.sawpButtons(self.btns, self.btns1)
        elif id == 1:
            # Button 2
            self.sawpButtons(self.btns, self.btns2)
        elif id == 2:
            # Button 3
            self.sawpButtons(self.btns, self.btns3)
        elif id == 3:
            # Quit
            self.close()

    def btnClick1(self, id):
        print(id)
        # Button 1 menu
        if id == 0:
            # Button 4
            pass
        elif id == 1:
            # Back
            self.sawpButtons(self.btns1, self.btns)

    def btnClick2(self, id):
        print(id)
        # Button 1 menu
        if id == 0:
            # Button 4
            pass
        elif id == 1:
            # Back
            self.sawpButtons(self.btns2, self.btns)

    def btnClick3(self, id):
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
            self.sawpButtons(self.btns3, self.btns)



    # d(-_-)b ~-=< FUNCTIONS >=-~ d(-_-)b

    # Creates buttons from a btnsGroup and a list of button names
    def createButtons(self, btns , btnsList):
        # Set style and font for buttons
        btnFont = QFont("System", 12)
        buttonSyle = "background-color: cyan; font: 20px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center;"
        # Loop through the list of buttons to create
        for i, btn in enumerate(btnsList):
            btn = QPushButton(btn, self)
            btn.setStyleSheet(buttonSyle)
            btn.setFont(btnFont)
            btns.addButton(btn, i)
            self.rightLayout.addWidget(btn)
        # Return the number of buttons created
        return(i+1)

    # Hides all buttons in a btnsGroup
    def hideButtons(self, btnsGroup):
        for i in range(self.btnsCount[btnsGroup]):
            btnsGroup.button(i).hide()

    # Shows all buttons in a btnsGroup
    def showButtons(self, btnsGroup):
        for i in range(self.btnsCount[btnsGroup]):
            btnsGroup.button(i).show()

    # Hides all buttons in btnsGroup1 and shows all buttons in btnsGroup2
    def sawpButtons(self, btnsGroup1, btnsGroup2):
        self.hideButtons(btnsGroup1)
        self.showButtons(btnsGroup2)

    # Creates an image and adds it to the left layout
    def createImage(self):
        label1 = QLabel('Image', self)
        pixmap = QPixmap("serious.png")
        pixmap = pixmap.scaled(self.height-100, self.height-100, Qt.KeepAspectRatio)
        label1.setPixmap(pixmap)
        label1.setAlignment(Qt.AlignCenter)
        self.leftLayout.addRow(label1)

    


# Main
myapp = QApplication(sys.argv)
window = Window()
myapp.exec_()
sys.exit()
