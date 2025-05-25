import sys
from PySide2.QtWidgets import QButtonGroup, QPushButton
from model.model import ServoController, Model, STT
import os
import time

class ButtonsController():
    def __init__(self, dict_of_button_groups, model: Model) -> None:
        self._dict_of_button_groups = dict_of_button_groups
        self._model = model
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
            self._model.servo_acrobat.move_to_position("hands", 1000)
            time.sleep(2)
            self._model.servo_acrobat.move_to_position("no1_x", 1000)
            for i in range(3):
                self._model.servo_acrobat.move_to_position("no2_x", 1000)
                self._model.servo_acrobat.move_to_position("no3_x", 200)
                self._model.servo_acrobat.move_to_position("no4_x", 500)
                self._model.servo_acrobat.move_to_position("no5_x", 100)
                self._model.servo_acrobat.move_to_position("no6_x", 1000)
                self._model.servo_acrobat.move_to_position("no7_x", 200)
                self._model.servo_acrobat.move_to_position("no8_x", 100)
                self._model.servo_acrobat.move_to_position("no9_x", 150)
                self._model.servo_acrobat.move_to_position("no10_x", 500)
                self._model.servo_acrobat.move_to_position("no11_x", 400)
                self._model.servo_acrobat.move_to_position("no12_x", 500)
                self._model.servo_acrobat.move_to_position("no13_x", 1000)
            self._model.servo_acrobat.move_to_position("no2_x", 1200)
            self._model.servo_acrobat.move_to_position("no1_x", 1000)
        elif button.text() == "Arms Control":
            os.system("python3 dev_tools/arms_control/ServoApp1.py")
        elif button.text() == "Settings":
            self.show_buttons("Settings")
        elif button.text() == "Quit":
            pwm_servos = self._model.servo_controller._get_servos_by_ids([0, 1, 2, 3, 4, 5, 6, 7])
            for pwm_servo in pwm_servos:
                pwm_servo._thread_stop_event.set()
            for pwm_servo in pwm_servos:
                pwm_servo._thread.join()
            self._model.sst.close_thread()
            sys.exit()

    def _camera_button_clicked(self, button: QPushButton) -> None:
        if button.text() == "Back":
            self.show_buttons("Main")

    def _settings_button_clicked(self, button: QPushButton) -> None:
        if button.text() == "Back":
            self.show_buttons("Main")
