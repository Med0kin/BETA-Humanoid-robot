from model.Servo import Servo

class TestServo(Servo):
    def __init__(self, id: int, max_pos: int, min_pos: int) -> None:
        '''
        Constructor for TestServo class
        :param id: ID of the servo
        :param max_pos: Maximum pos of the servo
        :param min_pos: Minimum pos of the servo
        '''
        super().__init__(id, max_pos, min_pos)
        self._target_pos = 1500
        self._target_time = 0
    def move(self, pos: int, time: int = 0, verbose: bool = False) -> None:
        '''
        Moves the servo to the given position.
        :param pos: The target position to move the servo to.
        :param time: The time to reach the target position (default 0).
        :param verbose: Whether to print the position (default False).
        :raises ValueError: If the time is negative.
        :return: None
        '''
        if time < 0:
            raise ValueError("Time cannot be negative")
        self.target_pos = pos
        self.target_time = time
        if verbose:
            print(self._generate_move_info(pos, time, verbose))
    @property
    def target_pos(self) -> int:
        return self._target_pos
    @target_pos.setter
    def target_pos(self, pos: int) -> None:
        self._target_pos = pos
    @property
    def target_time(self) -> int:
        return self._target_time
    @target_time.setter
    def target_time(self, time: int) -> None:
        self._target_time = time
    def _generate_move_info(self, pos: int, time: int, verbose: bool) -> str:
        '''
        Generates the move info string
        :param pos: The target position to move the servo to.
        :param time: The time to reach the target position.
        :param verbose: Whether to print the position.
        :return: The move info string
        '''
        return "Moving servo {} to position {} in {} seconds".format(self.id, pos, time)
    def __str__(self) -> str:
        return super().__str__()
