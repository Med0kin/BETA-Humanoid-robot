from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QFont, QIcon, QPalette, QBrush
from PySide2.QtWidgets import (QButtonGroup, QPushButton, QHBoxLayout,
                               QVBoxLayout, QWidget)
from QFace import QFaceGraphicsScene, QFaceGraphicsView


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BETA")
        self.window_size = QSize(500, 400)
        self.setMinimumSize(self.window_size)
        self.setStyleSheet("background-color: white;")
        self.setup_ui()
        self.show()

    def setup_ui(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 10, 0)
        self._create_left_panel()
        self._create_right_panel()
        self.setLayout(self.main_layout)

    def _create_left_panel(self) -> None:
        self._scene = QFaceGraphicsScene(self.window_size)
        self._view = QFaceGraphicsView(self._scene, self.window_size)
        self.main_layout.addWidget(self._view)
 
    def _create_right_panel(self) -> None:
        layout = QVBoxLayout()
        button_font = QFont("System", 12)        
        button_style = "QPushButton { background-color: #00accc; font: 20px;\
                    border-radius: 10px; border: 2px solid grey;\
                    padding: 10px; margin: 10px; text-align: center; }\
                    QPushButton:pressed { background-color: #005666; }"
 
        self._dict_of_button_groups = {}
        DICT_OF_GROUP_BUTTONS_AND_NAMES = {
            "Main": ["Camera", "Arms Control", "Settings", "Quit"],
            "Camera": ["Take Photo", "Back"],
            "Settings": ["Back"]
        }
        for group_name, button_names in DICT_OF_GROUP_BUTTONS_AND_NAMES.items():
            button_group = QButtonGroup(self)
            for i, name in enumerate(button_names):
                button_temp = QPushButton(name)
                button_temp.setFont(button_font)
                button_temp.setStyleSheet(button_style)
                button_group.addButton(button_temp, i)
                layout.addWidget(button_temp)
                button_temp.hide()
            self._dict_of_button_groups[group_name] = button_group

        self.main_layout.addLayout(layout)

    @property
    def scene(self) -> QFaceGraphicsScene:
        return self._scene
 
    @property
    def view(self) -> QFaceGraphicsView:
        return self._view
 
    @property
    def dict_of_button_groups(self) -> dict[str, QButtonGroup]:
        return self._dict_of_button_groups
