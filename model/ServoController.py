from model.PWMServo import PWMServo
from model.BusServo import BusServo
from multimethod import multimethod
from typing import Union, List, Tuple, Any
from array import array

class ServoController:
    def __init__(self, servos: tuple = ()) -> None:
        '''
        Constructor for ServoController class
        :param servos: Tuple of servos
        '''
        self._servos = servos

    
    def move(self, servos: Union[list, tuple, array], positions: Union[list, tuple, array],
             times: Union[list, tuple, array, None] = None, verbose: bool = False) -> None:
        '''
        Moves the servos to the given positions in the given times (if given)
        :param servos: Servos to move (list, tuple or array)
        :param positions:
        '''
        if len(servos) != len(positions):
            raise ValueError("Servos and positions must be the same length")
        if times is not None and len(servos) != len(times):
            raise ValueError("Servos and times must be the same length")
        if times is None:
            times = [0] * len(servos)
        type_check_list = [isinstance(servo, int) for servo in servos]
        if all(type_check_list):
            servos = self._get_servos_by_ids(servos)
        pwm_servos = tuple(servo for servo in servos if isinstance(servo, PWMServo))
        bus_servos = tuple(servo for servo in servos if isinstance(servo, BusServo))
        

    def _get_servos_by_ids(self, ids: Union[list, tuple, array]) -> tuple:
        servos = ()
        for id in ids:
            servos = tuple(servo for servo in self.servos if servo.id == id)
        if len(servos) != len(ids):
            raise ValueError("Not all IDs are valid")
        return servos

    @property
    def servos(self) -> tuple:
        return self._servos

    @servos.setter
    def servos(self, servos: tuple) -> None:
        self._servos = servos

    def __len__(self) -> int:
        return len(self.servos)

    def __getitem__(self, index: int) -> Union[PWMServo, BusServo]:
        return self.servos[index]

