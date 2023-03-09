import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import time
"""
PySide2 app for controlling robot
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide2 App")

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        self.setGeometry(300, 300, 800, 600)
        '''
        # Set background image
        p = self.palette()
        # p always scaled to window size
        p.setBrush(QPalette.Window, QBrush(QPixmap("bg.png").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        '''
        


        # Set window icon
        self.setWindowIcon(QIcon("icon.png"))
        # Initialize UI
        self.initUI()
        self.addButton()

    def initUI(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # Set background color
        p = QPalette()
        p.setColor(QPalette.Window, Qt.cyan)
        self.setPalette(p)

    # Button that displays image when clicked, and hides image when released
    def addButton(self):
        self.QPLabel = QLabel(self)
        self.QPLabel.setPixmap(QPixmap("serious.png"))
        self.QPLabel.setGeometry(0, 0, 800, 600)

        self.toplabel = QLabel(self)
        self.toplabel.setGeometry(0, 0, 800, 300)
        self.toplabel.mousePressEvent = self.mousePressEvent
        self.toplabel.mouseReleaseEvent = self.mouseReleaseEvent

        self.botlabel = QLabel(self)
        self.botlabel.setGeometry(0, 300, 800, 300)
        self.botlabel.mousePressEvent = self.mousePressEvent
        self.botlabel.mouseReleaseEvent = self.mouseReleaseEvent



        self.QPLabel.show()

    def mousePressEvent(self, event):
        #change image
        self.QPLabel.setPixmap(QPixmap("smile.png"))
        print("smile")
        self.QPLabel.show()



    def mouseReleaseEvent(self, event):
        #change image
        self.QPLabel.setPixmap(QPixmap("serious.png"))
        print("serious")
        self.QPLabel.show()



        

        
    



myapp = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(myapp.exec_())
window.show()