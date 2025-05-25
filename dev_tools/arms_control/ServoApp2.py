import tkinter as tk
import time
import numpy as np
from Servos.Analog_servo2 import AServo

class ServoController:
    def __init__(self):
        self.servos = [
            AServo(17),  # left arm servos
            AServo(21),  # right arm servos
            AServo(27),
            AServo(26),
            AServo(22),
            AServo(19),
            AServo(10),
            AServo(13)
        ]
        for servo in self.servos:
            servo.set_range(270)

    def move_servo(self, idx, angle, speed=100):
        self.servos[idx].move_servo(angle, speed)

class ServoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.controller = ServoController()
        self.positions = [0]*8
        self.filenamevar = tk.StringVar(self.root, value="default")
        self.w = 350
        self.h = self.w
        self.x = self.w // 2
        self.y = self.h // 2
        self.arm = 0

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title('BETA Servo Manager')
        self.root.geometry("800x600")
        self.root.config(bg="#3D82F0")

        self.tp_frame = tk.Frame(self.root)
        self.tp_frame.pack(pady=10)

        self.tframe1 = tk.Frame(self.tp_frame, bg="#639BF3")
        self.tframe1.pack(side=tk.LEFT)

        self.tframe2 = tk.Frame(self.tp_frame, bg="#639BF3")
        self.tframe2.pack(side=tk.RIGHT)

        self.tpad1 = tk.Canvas(self.tframe1, width=self.w, height=self.h, bg="white", cursor="dot")
        self.tpad1.pack()
        self.circle1 = self.tpad1.create_oval(self.x, self.y, self.x+5, self.y+5, fill="black")
        self.coordinates1 = tk.Label(self.tframe1, text="Touchpad1", bg="#91B9F6")
        self.coordinates1.pack(pady=10)

        self.tpad2 = tk.Canvas(self.tframe2, width=self.w, height=self.h, bg="white", cursor="dot")
        self.tpad2.pack()
        self.circle2 = self.tpad2.create_oval(self.x, self.y, self.x+5, self.y+5, fill="black")
        self.coordinates2 = tk.Label(self.tframe2, text="Touchpad2", bg="#91B9F6")
        self.coordinates2.pack(pady=10)

        self.b_changearm = tk.Button(self.root, text="CHANGE ARM", command=self.change_arm, bg="#00ACCC")
        self.b_changearm.pack(anchor=tk.S, side=tk.RIGHT)
        self.b_export = tk.Button(self.root, text="EXPORT", command=self.export_positions, bg="#00ACCC")
        self.b_export.pack(anchor=tk.S, side=tk.RIGHT)
        self.filename_entry = tk.Entry(self.root, textvariable=self.filenamevar, bg="#00ACCC")
        self.filename_entry.pack(anchor=tk.S, side=tk.RIGHT)
        self.b_import = tk.Button(self.root, text="IMPORT", command=self.import_positions, bg="#00ACCC")
        self.b_import.pack(anchor=tk.S, side=tk.RIGHT)

        self.tpad1.bind('<B1-Motion>', lambda event: self.on_canvas_drag(event, 0))
        self.tpad2.bind('<B1-Motion>', lambda event: self.on_canvas_drag(event, 1))

    def on_close(self):
        for servo in self.controller.servos:
            try:
                servo.opened_thread = False
                servo.kill()
            except:
                print("Error")
        self.root.quit()

    def change_arm(self):
        self.arm = 1 - self.arm

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    def map_pos(self, value):
        return round(self.translate(value, 0, self.w, 500, 2500))

    def import_positions(self):
        filename = self.filenamevar.get()
        filename = '/home/pi/BETA-Humanoid-robot/Positions/' + filename + '.txt'
        self.positions = [0, 0, 0, 0, 0, 0, 0, 0]
        with open(filename, 'r') as f:
            for i in range(len(self.positions)):
                line = f.readline().split()
                self.positions[i] = int(line[1])
        for i in range(len(self.positions)):
            self.controller.move_servo(i, self.positions[i])

    def export_positions(self):
        filename = self.filenamevar.get()
        filename = '/home/pi/BETA-Humanoid-robot/Positions/' + filename + '.txt'
        with open(filename, 'w') as f:
            for i in range(len(self.positions)):
                f.write("%d %d\n" % (i, self.positions[i]))

    def on_canvas_drag(self, event, index_offset):
        pos = [event.x, event.y]
        for i in range(2):
            if pos[i] < 0:
                pos[i] = 0
            elif pos[i] > self.w:
                pos[i] = self.w

        if index_offset == 0:
            self.tpad1.delete(self.circle1)
            self.circle1 = self.tpad1.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill="black")
            x_pulse = self.map_pos(pos[0])
            y_pulse = 3000 - self.map_pos(pos[1])
            self.coordinates1.config(text="Coordinates1 x: " + str(x_pulse) + ", y: " + str(y_pulse))
            self.positions[self.arm+2] = x_pulse
            self.positions[self.arm+6] = y_pulse
            self.controller.move_servo(self.arm+2, x_pulse, 100)
            self.controller.move_servo(self.arm+6, y_pulse, 100)
        else:
            self.tpad2.delete(self.circle2)
            self.circle2 = self.tpad2.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill="black")
            x_pulse = self.map_pos(pos[0])
            y_pulse = 3000 - self.map_pos(pos[1])
            self.coordinates2.config(text="Coordinates2 x: " + str(x_pulse) + ", y: " + str(y_pulse))
            self.positions[self.arm] = x_pulse
            self.positions[self.arm+4] = y_pulse
            self.controller.move_servo(self.arm, x_pulse, 100)
            self.controller.move_servo(self.arm+4, y_pulse, 100)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ServoApp()
    app.run()