from abc import ABC, abstractmethod
from multimethod import multimethod
from multipledispatch import dispatch

class Servo(ABC):
    
    @abstractmethod
    def move(self, position: int):
        print(f"Moving to {position}")

class SubServo(Servo):
    @multimethod
    def move(self, position: int):
        print(f"Moving to {position} (int method)")
    @multimethod
    def move(self, string: str):
        print(f"Moving to {string} (string method)")
    @multimethod
    def move(self, position: int, time: int):
        print(f"Moving to {position} in {time} (2x int method)")
    

if __name__ == "__main__":
    s = SubServo()

    s.move(5)
    s.move("five")
    s.move(5, 10)
