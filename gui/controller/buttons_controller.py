import sys
from PySide2.QtWidgets import QButtonGroup, QPushButton


class ButtonsController():
    def __init__(self, dict_of_button_groups) -> None:
        self._dict_of_button_groups = dict_of_button_groups
        self.show_buttons("Main")
        self._add_button_connections()

    def _hide_all_buttons(self) -> None:
        for group in self._dict_of_button_groups.values():
            for button in group.buttons():
                button.hide()

    def show_buttons(self, group_name: str) -> None:
        self._hide_all_buttons()
        for button in self._dict_of_button_groups[group_name].buttons():
            button.show()

    def _add_button_connections(self) -> None:
        self._dict_of_button_groups["Main"].buttonClicked.connect(
            self._main_button_clicked)
        self._dict_of_button_groups["Camera"].buttonClicked.connect(
            self._camera_button_clicked)
        self._dict_of_button_groups["Settings"].buttonClicked.connect(
            self._settings_button_clicked)

    def _main_button_clicked(self, button: QPushButton) -> None:
        if button.text() == "Camera":
            self.show_buttons("Camera")
        elif button.text() == "Settings":
            self.show_buttons("Settings")
        elif button.text() == "Quit":
            sys.exit()

    def _camera_button_clicked(self, button: QPushButton) -> None:
        if button.text() == "Back":
            self.show_buttons("Main")

    def _settings_button_clicked(self, button: QPushButton) -> None:
        if button.text() == "Back":
            self.show_buttons("Main")
