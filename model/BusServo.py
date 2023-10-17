import serial
from model.Servo import Servo
from multimethod import multimethod

class BusServo(Servo):
    def __init__(self,id: int, max_pos: int,
                 min_pos: int, serial: serial.Serial) -> None:
        '''
        Constructor for BusServo class
        :param id: ID of the servo
        :param max_pos: Maximum pos of the servo
        :param min_pos: Minimum pos of the servo
        :param serial: Serial port of the servo
        '''
        super().__init__(id, max_pos, min_pos)
        self._serial = serial;

    @multimethod
    def move(self, pos: int, verbose: bool = False) -> None: # type: ignore
        '''
        Moves the servo to the given position
        :param pos: Position to move to
        :param verbose: Whether to print the position
        '''
        if pos > 4095 or pos < 0:
            raise ValueError("Position must be between 0 and 4095")
        INSTRUCTION = 0x03
        ADDRESS = 0x2a
        pos_in_bytes = pos.to_bytes(2, 'little')
        data = bytearray([0xff, 0xff,
                          self.id, 0x00,
                          INSTRUCTION, ADDRESS,
                          pos_in_bytes[0], pos_in_bytes[1]])
        data[3] = len(data) - 3
        checksum = self._checksum(data)
        data.append(checksum)
        self.serial.write(data)
        if verbose:
            print(self._generate_move_info(pos, 0, verbose))

    @multimethod
    def move(self, pos: int, time: int, verbose: bool = False) -> None:
        '''
        Moves the servo to the given position in the given time
        :param pos: Position to move to
        :param time: Time to move to the position
        :param verbose: Whether to print the position
        '''
        #TODO: Implement move method for single BusServo that takes time
        pass

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
    def serial(self) -> serial.Serial:
        return self._serial

    def __str__(self) -> str:
        return super().__str__() + f"Serial: {self.serial}\n"

    def __repr__(self) -> str:
        return f"BusServo({self.id}, {self.max_pos}, {self.min_pos}, {self.serial})"
