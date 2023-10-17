import os
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (QFrame, QGraphicsItem, QGraphicsPixmapItem,
                               QGraphicsScene, QGraphicsView)

class QFaceGraphicsScene(QGraphicsScene):
    def __init__(self, size: QSize, parent=None) -> None:
        super().__init__(parent)
        self._window_size = size
        self._items = list()
        self._setup_scene()

    def _setup_scene(self) -> None:
        _background_item = self._create_item("background_empty", self._window_size)
        _face_item = self._create_item("face", self._window_size)
        _left_eye_item = self._create_item("eye", QSize(50, 50))
        _right_eye_item = self._create_item("eye", QSize(50, 50))
        
        for item in self._items:
            self.addItem(item)

    def _create_item(self, name: str, size: QSize) -> QGraphicsPixmapItem:
        path = os.path.join(os.path.dirname(__file__), "resources", name + ".png")
        if not os.path.exists(path):
            raise Exception("Image not found at: {}".format(path))
        image = QPixmap(path)
        image = image.scaled(size.width(), size.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        item = QGraphicsPixmapItem(image)
        self._items.append(item)
        return item
    
    @property
    def items(self) -> list[QGraphicsPixmapItem]:
        return self._items
    
    @property
    def window_size(self) -> QSize:
        return self._window_size
    

class QFaceGraphicsView(QGraphicsView):
    def __init__(self, scene: QFaceGraphicsScene, size: QSize, parent=None) -> None:
        super().__init__(scene, parent)
        self._window_size = size
        self._setup_view()

    def _setup_view(self) -> None:
        self.setGeometry(0, 0, self._window_size.width(), self._window_size.height())
        self.setFixedHeight(self._window_size.height())
        self.setFixedWidth(self._window_size.width())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setAlignment(Qt.AlignCenter)
