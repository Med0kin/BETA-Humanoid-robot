import sys

from PySide2.QtWidgets import QApplication

from gui.controller import FaceController, ButtonsController
from gui.view import Window
from model.model import Model


class Controller():
    def __init__(self, view, model) -> None:
        self._view = view
        self._model = model
        self._face_controller = FaceController(self._view.scene)
        self._buttons_controller = ButtonsController(
            self._view.dict_of_button_groups,
            self._model)
        self.start_app()

    def start_app(self) -> None:
        myapp.exec_()
        sys.exit()


if __name__ == "__main__":
    myapp = QApplication(sys.argv)
    model = Model()
    view = Window()
    controller = Controller(view, model)
