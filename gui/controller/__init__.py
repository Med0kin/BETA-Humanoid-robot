# gui/controller/__init__.py

from pkgutil import extend_path
from .buttons_controller import ButtonsController
from .face_controller import FaceController

__path__ = extend_path(__path__, __name__)
__all__ = ["ButtonsController", "FaceController"]
