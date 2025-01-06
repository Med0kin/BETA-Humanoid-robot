from gui.view import QFaceGraphicsScene
from PySide2.QtCore import QTimer, QPropertyAnimation, QByteArray, QPointF, QParallelAnimationGroup
from PySide2.QtCore import Qt, QRectF, QEasingCurve
from PySide2.QtWidgets import QGraphicsPixmapItem


class FaceController():
    def __init__(self, scene: QFaceGraphicsScene) -> None:
        self.scene = scene
        self.set_default()
        
        self._blink_timer = QTimer()
        self._blink_timer.timeout.connect(self.blink)
        self._blink_timer.start(1000)

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
        self.scene.items[2]._setX(width - 50)
        self.scene.items[2]._setY(height - 50)
        self.scene.items[3]._setX(width + 50)
        self.scene.items[3]._setY(height - 50)
        # Set origin point
        point = QPointF(10, 25)
        self.scene.items[2].setTransformOriginPoint(point)
        
    def blink(self) -> None:
        # TODO: Add blinking animation 
        
        animation_y = QPropertyAnimation(self.scene.items[2], QByteArray(b"P_y_scale"))
        animation_y.setDuration(100)
        animation_y.setStartValue(1)
        animation_y.setEndValue(0.5)
        animation_x = QPropertyAnimation(self.scene.items[2], QByteArray(b"P_x_scale"))
        animation_x.setDuration(100)
        animation_x.setStartValue(1)
        animation_x.setEndValue(2)

        group = QParallelAnimationGroup()
        group.addAnimation(animation_x)
        group.addAnimation(animation_y)
        group.start()

