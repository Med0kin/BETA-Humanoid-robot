import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QMainWindow, QStatusBar, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import QIcon, QPixmap, QFont

"""
PySide2 app for controlling robot
"""
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide2 App")
        self.setGeometry(300, 300, 300, 300)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        self.setWindowIcon(QIcon("icon.png"))
        self.center()
        #self.setButton()
        #self.createStatusBar()
        self.setIconModes()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())










    def setButton(self):
        btn = QPushButton("quit", self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(0, 100)
        btn.clicked.connect(self.quitApp)

        self.aboutBtn = QPushButton("About", self)
        self.aboutBtn.move(100, 100)
        self.aboutBtn.clicked.connect(self.aboutBox)

    def aboutBox(self):
        QMessageBox.about(self, "About", "This is a PySide2 app")

    def createStatusBar(self):
        self.myStatus = QStatusBar()
        self.myStatus.showMessage("status", 5000)
        self.setStatusBar(self.myStatus)


    def quitApp(self):
        choice = QMessageBox.question(self, 'Message',
                                      "Are you sure to quit?", QMessageBox.Yes |
                                      QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Closing")
            sys.exit()
        else:
            pass

    def setIconModes(self):
        # Active icon
        icon1 = QIcon("icon.png")
        label1 = QLabel('Icon 1', self)
        pixmap = icon1.pixmap(100, 100, QIcon.Active, QIcon.On)
        label1.setPixmap(pixmap)
        QToolTip.setFont(QFont('System', 10))
        label1.setToolTip('Active icon')
        # Disabled icon
        icon2 = QIcon("icon.png")
        label2 = QLabel('Icon 2', self)
        pixmap2 = icon2.pixmap(100, 100, QIcon.Disabled, QIcon.Off)
        label2.setPixmap(pixmap2)
        label2.move(100, 0)
        label2.setToolTip('Disabled icon')
        # Selected icon
        icon3 = QIcon("icon.png")
        label3 = QLabel('Icon 3', self)
        pixmap3 = icon3.pixmap(100, 100, QIcon.Selected, QIcon.On)
        label3.setPixmap(pixmap3)
        label3.move(200, 0)
        label3.setToolTip('Selected icon')

myapp = QApplication(sys.argv)
window = Window()
window.show()
myapp.exec_()
sys.exit()