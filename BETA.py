import sys

from PySide2.QtWidgets import QApplication

from gui.controller.face_controller import FaceController
from gui.controller.buttons_controller import ButtonsController
from gui.view.view import Window


class Controller():
    def __init__(self, view, model) -> None:
        self._view = view
        self._model = model
        self._face_controller = FaceController(self._view.scene)
        self._buttons_controller = ButtonsController(
            self._view.dict_of_button_groups)
        self.start_app()

    def start_app(self) -> None:
        myapp.exec_()
        sys.exit()


if __name__ == "__main__":
    myapp = QApplication(sys.argv)
    view = Window()
    model = None
    controller = Controller(view, model)
