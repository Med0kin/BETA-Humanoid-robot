import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

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

        # Set background image
        p = self.palette()
        # p always scaled to window size
        p.setBrush(QPalette.Window, QBrush(QPixmap("bg.png").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        

        self.setPalette(p)


        # Set window icon
        self.setWindowIcon(QIcon("icon.png"))
        # Set window size
        self.center()

    # Center the window on the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

myapp = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(myapp.exec_())