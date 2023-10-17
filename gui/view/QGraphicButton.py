from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QSize

class QGraphicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None) -> None:
        super(QGraphicButton, self).__init__(parent)
        self._pixmap = pixmap

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self._pixmap)

    def sizeHint(self) -> QSize:
        return self._pixmap.size()

    @property
    def pixmap(self) -> QPixmap:
        return self._pixmap\

    @pixmap.setter
    def pixmap(self, pixmap: QPixmap) -> None:
        self._pixmap = pixmap

