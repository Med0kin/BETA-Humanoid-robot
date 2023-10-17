import threading
from model.Servo import Servo
import RPi.GPIO as GPIO
import pigpio as pg
from typing import Union
from time import sleep

class PWMServo(Servo):
    def __init__(self, id: int, max_pos: int,
                 min_pos: int, gpio_port: int,
                 servo_range: int = 180) -> None:
        '''
        Constructor for PWMServo class
        :param id: ID of the servo
        :param max_pos: Maximum pos of the servo
        :param min_pos: Minimum pos of the servo
        :param gpio_port: GPIO port of the servo
        :param servo_range: Range of the servo (default 180)
        '''
        super().__init__(id, max_pos, min_pos)
        self._MIN_SERVO_DUTY = 500
        self._MAX_SERVO_DUTY = 2500
        if max_pos > self._MAX_SERVO_DUTY or min_pos < self._MIN_SERVO_DUTY:
            raise ValueError("Position must be between 500 and 2500")
        self._servo_range = servo_range
        self._GPIO_PORT = gpio_port
        self._pigpio = self._setup_pigpiod(gpio_port)
        self._target_pos = None
        self._target_time = 0
        self._thread = None
        self._thread_stop_event = threading.Event()
        self._run_thread()

    def move(self, pos: int, time: int = 0, verbose: bool = False) -> None:
        '''
        Moves the servo to the given position.
        :param pos: The target position to move the servo to.
        :param time: The time to reach the target position (default 0).
        :param verbose: Whether to print the position (default False).
        :raises RuntimeError: If the thread is not running.
        :raises ValueError: If the time is negative.
        :return: None
        '''
        if self.thread_stop_event.is_set():
            raise RuntimeError("Thread is not running, thread_stop_event is set")
        if time < 0:
            raise ValueError("Time cannot be negative")
        self.target_pos = pos
        self.target_time = time
        if verbose:
            print(self._generate_move_info(pos, time, verbose))

    def _setup_pigpiod(self, gpio_port: int) -> pg.pi:
        '''
        Sets up the pigpiod daemon
        :param gpio_port: GPIO port of the servo
        :return: pigpio object
        '''
        pigpio = pg.pi()
        pigpio.set_mode(gpio_port, pg.OUTPUT)
        pigpio.set_PWM_frequency(gpio_port, 50)
        pigpio.set_servo_pulsewidth(gpio_port, 1500)
        self.pos = 1500
        return pigpio

    def _control_servo(self) -> None:
        """
        Controls the servo to move to the target position
        (it is meant to be run in a thread)
        """
        current_goal = self.pos
        while not self._thread_stop_event.is_set():
            if self.target_pos == self.pos:
                continue
            if self.target_pos == None:
                raise ValueError("Target position is None")
            if self.target_time == 0:
                self.pigpio.set_servo_pulsewidth(self.GPIO_PORT, self.target_pos)
                self.pos = self.target_pos
                continue

            STEP = 5
            #TODO: Figure out how to deal with type checking here
            current_goal = self.target_pos
            travel = int(abs(self.target_pos - self.pos))
            time_jump = self.target_time / (travel/STEP)
            pos_list = range(self.pos, self.target_pos, STEP)
            
            for pos in pos_list:
                if current_goal != self.target_pos:
                    break
                self.pigpio.set_servo_pulsewidth(self.GPIO_PORT, pos)
                sleep(time_jump)

    def _run_thread(self) -> None:
        self.thread = threading.Thread(target=self._control_servo)
    
    @property
    def servo_range(self) -> int:
        return self._servo_range
    
    @property
    def GPIO_PORT(self) -> int:
        return self._GPIO_PORT

    @property
    def pigpio(self) -> pg.pi:
        return self._pigpio
    
    @property
    def target_pos(self) -> Union[int, None]:
        return self._target_pos

    @property
    def target_time(self) -> int:
        return self._target_time
    
    @property
    def thread(self) -> Union[threading.Thread, None]:
        return self._thread

    @property
    def thread_stop_event(self) -> threading.Event:
        return self._thread_stop_event

    @target_pos.setter
    def target_pos(self, pos: int) -> None:
        self._target_pos = pos

    @target_time.setter
    def target_time(self, time: int) -> None:
        self._target_time = time

    @thread.setter
    def thread(self, thread: threading.Thread) -> None:
        self._thread = thread

    def __str__(self) -> str:
        return super().__str__() + f"Servo range: {self._servo_range}\n"

    def __repr__(self) -> str:
        return (f"PWMServo({self.id}, {self.max_pos}, {self.min_pos}, "
                f"{self.servo_range}, {self.pigpio})")

