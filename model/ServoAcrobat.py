from typing import Union
from model import ServoController
from time import sleep

class ServoAcrobat:
    """
    param servoController: ServoController
    """
    def __init__(self, servoController: ServoController) -> None:
        self._servoController = servoController

    def load_position(self, position_path: str) -> Union[tuple, None]:
        """
        Load a position from a file and move the servo to that position.
        :param position_path: Path to the position file.
        """
        print(f"moving robot to pos: {position_path}")
        servo_id_data = []
        position_data = []
        try:
            with open(position_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) == 2:
                            servo_id_data.append(int(parts[0]))
                            position_data.append(int(parts[1]))
                        else:
                            raise ValueError("Invalid line format in position file.")
            if len(servo_id_data) != len(position_data):
                raise ValueError("Mismatch between servo IDs and positions.")
        except FileNotFoundError:
            print(f"File not found: {position_path}")
            return None
        except ValueError as e:
            print(f"Error reading file: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        return (servo_id_data, position_data)
                
        
    
    def move_to_position(self, position_name: str, time: Union[int, float], blocking: bool = True) -> None:
        """
        Move the servo to a position loaded from a file.
        :param position_path: Path to the position file.
        :param time: Time to move to the position.
        """
        position_path = f"model/Positions/{position_name}.txt"
        data = self.load_position(position_path)
        print(f"data: {data}")
        if data:
            servo_id_data, position_data = data
            times = [time] * len(servo_id_data)
            self._servoController.move(servo_id_data, position_data, times)
        if blocking:
            sleep(time / 1000)
