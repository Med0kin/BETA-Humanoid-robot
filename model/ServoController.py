import serial
from model import Servo, PWMServo, BusServo
from typing import Union, List, Tuple, Any
from array import array
from time import time

class ServoController:
    def __init__(self, servos: tuple = (), serial: serial.Serial = None) -> None:
        '''
        Constructor for ServoController class
        :param servos: Tuple of servos
        '''
        self._servos: tuple = servos
        self.serial = serial

    
    def move(self, servos: Union[list, tuple, array], positions: Union[list, tuple, array],
             times: Union[list, tuple, array, None] = None, verbose: bool = False) -> None:
        '''
        Moves the servos to the given positions in the given times (if given)
        :param servos: Servos to move (list, tuple or array)
        :param positions:
        '''
        DEFAULT_TIME = 1000
        if len(servos) != len(positions):
            raise ValueError("Servos and positions must be the same length")
        if times is not None and len(servos) != len(times):
            raise ValueError("Servos and times must be the same length")
        if times is None:
            times = [DEFAULT_TIME] * len(servos)

        int_type_check_list = [isinstance(servo, int) for servo in servos]
        servo_type_check_list = [isinstance(servo, Servo) for servo in servos]
        if all(int_type_check_list):
            servos = self._get_servos_by_ids(servos)
        elif all(servo_type_check_list):
            pass
        else:
            raise ValueError("Servos must be either all ints or all Servos")

        pwm_servos = tuple(servo for servo in servos if isinstance(servo, PWMServo))
        for servo in pwm_servos:
            servo.move(positions[servos.index(servo)], times[servos.index(servo)], verbose)
        
        bus_servos = tuple(servo for servo in servos if isinstance(servo, BusServo))
        bus_positions = [positions[servos.index(servo)] for servo in bus_servos]
        bus_times = [times[servos.index(servo)] for servo in bus_servos]
        self._move_multiple_bus(bus_servos, bus_positions, bus_times)
        if verbose:
            print(self._generate_move_info(servos, positions, times))
            
    def _generate_move_info(self, servos: Union[list, tuple, array], positions: Union[list, tuple, array], times: Union[list, tuple, array]) -> str:
        info = f"{time()} | Moving servos to positions:\n"
        for i in range(len(servos)):
            info += f"Servo {servos[i].id}: \t{servos[i].pos} -> {positions[i]} in {times[i]} ms\n"
        return info

    def _get_servos_by_ids(self, ids: Union[list, tuple, array]) -> list:
        servos = []
        for id in sorted(ids):
            for servo in self.servos:
                if servo.id == id:
                    servos.append(servo)
                    break
        if len(servos) != len(ids):
            raise ValueError("Not all IDs are valid")
        return servos
    
    def _move_multiple_bus(self, servos: Union[list, tuple, array], positions: Union[list, tuple, array], 
                           operation_time: Union[list, tuple, array]) -> None:
        data_length = 0
        INSTRUCTION = 0x83
        ADDRESS = 0x2a
        LENGTH = 0x04
        data = bytearray([0xff, 0xff, 0xfe, data_length, INSTRUCTION, ADDRESS, LENGTH])
        for i in range(len(servos)):
            if servos[i].is_inverted:
                positions[i] = 4095 - positions[i]          # Mirror the positions for left leg
            pos = positions[i].to_bytes(2, 'little')
            data.append(servos[i].id)
            data.append(pos[0])
            data.append(pos[1])
            spd = operation_time[i].to_bytes(2, 'little')
            data.append(spd[0])
            data.append(spd[1])
        data[3] = len(data) - 3
        data.append(self._checksum(data))
        self.serial.write(data)
        

    def _checksum(self, data: bytearray) -> int:
        '''
        Calculates the checksum of the data
        :param data: Data to calculate the checksum of
        :return: Checksum of the data
        '''
        checksum = 0
        for i in range(2, len(data)):
            checksum += data[i]
        if checksum > 255:
            checksum = checksum & 0xff
        return ~checksum & 0xff

    @property
    def servos(self) -> tuple:
        return self._servos

    @servos.setter
    def servos(self, servos: tuple) -> None:
        self._servos = servos

    def __len__(self) -> int:
        return len(self.servos)

    def __getitem__(self, index: int) -> Servo:
        return self.servos[index]
