from abc import ABC, abstractmethod
from typing import Any, Union

class Servo(ABC):
    '''
    :param is_inversed: Whether the servo movement is inversed
                    (Reqired for mirroring right and left servos) 
    '''

    @abstractmethod
    def __init__(self,id: int, max_pos: int, min_pos: int) -> None:
        self._id = id
        self._max_pos = max_pos
        self._min_pos = min_pos
        self._pos = None
        self._is_inverted = False
    
    @abstractmethod
    def move(self, arg: Any, verbose: bool = False) -> None: ...

    
    def _generate_move_info(self, pos: int, time: int, verbose: bool) -> str:
        if time is 0:
            return (
                f'Object: {repr(self)}\n'
                f'Action: move({pos}, {verbose})\n'
            )
        else:
            return (
                f'Object: {repr(self)}\n'
                f'Action: move({pos}, {time}, {verbose})\n'
            )
 
    @property
    def id(self) -> int:
        return self._id

    @property
    def max_pos(self) -> int:
        return self._max_pos

    @property
    def min_pos(self) -> int:
        return self._min_pos

    @property
    def pos(self) -> Union[int, None]:
        return self._pos

    @property
    def is_inverted(self) -> bool:
        return self._is_inverted

    @pos.setter
    def pos(self, pos: int) -> None:
        if pos < self._min_pos or pos > self._max_pos:
            raise ValueError(f"Position must be between {self._min_pos}" \
                             f"and {self._max_pos}")
        self._pos = pos

    @is_inverted.setter
    def is_inverted(self, value: bool) -> None:
        self._is_inverted = value

    def __str__(self) -> str:
        return (f"Id {self.id},\n"
                f"Pos: {self.pos}\n")

    def __repr__(self) -> str:
        return f"Servo({self.id}, {self.max_pos}, {self.min_pos})"
