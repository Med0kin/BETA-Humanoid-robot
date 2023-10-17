from gui.view.QFace import QFaceGraphicsScene
from PySide2.QtCore import QTimer, QPropertyAnimation
from PySide2.QtCore import Qt, QRectF, QEasingCurve
from PySide2.QtWidgets import QGraphicsPixmapItem


class FaceController():
    def __init__(self, scene: QFaceGraphicsScene) -> None:
        self.scene = scene
        self.set_default()
        
        self._blink_timer = QTimer()
        self._blink_timer.timeout.connect(self.blink)
        self._blink_timer.start(3000)

    def set_default(self) -> None:
        # Center the face
        item = self.scene.items[1]
        size = self.scene.window_size
        bounding_rect = item.boundingRect()
        width = size.width() / 2 - bounding_rect.width() / 2
        height = size.height() / 2 - bounding_rect.height() / 2
        item.setPos(width, height)
        # Center the eyes
        item = self.scene.items[2]
        bounding_rect = item.boundingRect()
        width = size.width() / 2 - bounding_rect.width() / 2
        height = size.height() / 2 - bounding_rect.height() / 2
        self.scene.items[2].setPos(width - 50, height - 50)
        self.scene.items[3].setPos(width + 50, height - 50)
        
    def blink(self) -> None:
        # TODO: Add blinking animation 
        self.animation = QPropertyAnimation(self.scene.items[2], b"geometry")
        self.animation.setDuration(10000)
        self.animation.setStartValue(QRectF(10, self.scene.items[2].y(), 50, 50))
        self.animation.setEndValue(QRectF(10, self.scene.items[2].y(), 100, 100))
        self.animation.start()
