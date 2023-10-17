import asyncio
class Servo:
    def __init__(self, id):
        self.id = id
        self.pos = 0
    



async def move(servo, target, speed):
    STEP = 10
    while target > servo.pos:
        servo.pos += STEP
        print(f"{servo.id}: {servo.pos}")
        await asyncio.sleep(speed)
    while target < servo.pos:
        servo.pos -= STEP
        print(f"{servo.id}: {servo.pos}")
        await asyncio.sleep(speed)
    servo.pos = target


async def main():
    
    servo_1 = Servo(1)
    servo_2 = Servo(2)
    
    while True:    
        task1 = asyncio.create_task(move(servo_1, 200, 0.1))
        task2 = asyncio.create_task(move(servo_2, 200, 0.1))
        await task1
        await task2

if __name__ == "__main__":
    asyncio.run(main())
