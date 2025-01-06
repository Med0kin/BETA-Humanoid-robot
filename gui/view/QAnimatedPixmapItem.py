from PySide2.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide2.QtCore import QObject, Property


class QAnimatedPixmapItem(QObject, QGraphicsPixmapItem):
    def __init__(self, pixmap):
        QGraphicsPixmapItem.__init__(self, pixmap)
        QObject.__init__(self)
        self._x = self.x()
        self._y = self.y()
        self._scale = 0
        self._x_scale = 0
        self._y_scale = 0

    def _getX(self):
        return self._x

    def _setX(self, x):
        self._x = x
        self.setX(x)

    def _getY(self):
        return self._y

    def _setY(self, y):
        self._y = y
        self.setY(y)

    def _getScale(self):
        return self._scale
    
    def _setScale(self, scale):  
        self._scale = scale
        self.setScale(scale)

    def _getYScale(self):
        return self._y_scale

    def _setYScale(self, y_scale):
        self._y_scale = y_scale
        transform = self.transform()
        transform.reset()
        transform.translate(0, 25)
        transform.scale(1, y_scale)
        transform.translate(0, -25)
        self.setTransform(transform)

    def _getXScale(self):
        return self._x_scale

    def _setXScale(self, x_scale):
        self._x_scale = x_scale
        transform = self.transform()
        transform.reset()
        transform.translate(15, 0)
        transform.scale(x_scale, 1)
        transform.translate(-15, 0)
        self.setTransform(transform)
        
        
    P_x = Property(float, _getX, _setX)
    P_y = Property(float, _getY, _setY)
    P_scale = Property(float, _getScale, _setScale)
    P_y_scale = Property(float, _getYScale, _setYScale)
    P_x_scale = Property(float, _getXScale, _setXScale)
