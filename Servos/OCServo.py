# Run tkinter code in another thread

import serial
import sys
import glob
import time


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    print(ports)
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            print()
            pass
    return result


def checksum(data):
    sum = 0
    for i in range(2, len(data)):
        sum += data[i]
    if sum > 255:
        sum = sum & 0xff
    print(sum)
    return ~sum & 0xff


# transform function that converts a given angle -180 to 180 to the 0 to 4095 range
def transform(angle):
    return int((angle + 180) * 4095 / 360)


def importpos(filename):
    filename = filename + '.txt'
    idlist = [0, 0, 0, 0, 0, 0, 0, 0]
    poslist = [0, 0, 0, 0, 0, 0, 0, 0]
    with open(filename, 'r') as f:
        for i in range(len(idlist)):
            line = f.readline().split()
            idlist[i] = int(line[0])
            poslist[i] = int(line[1])
        f.close()
    return idlist, poslist


class OCServo:

    def __init__(self, port):
        self.inputdata = ""
        self.pos = None
        self.value = 0
        self.serialPort = serial.Serial(port, 1_000_000, timeout=1)

    def write(self, data):
        self.serialPort.write(data)
        hex_data = ' '.join(hex(b)[2:].zfill(2) for b in data)
        print(f"Wrote: {hex_data}")

    def read(self, bytes_to_read=1):
        msg = self.serialPort.read(bytes_to_read)
        data = msg.hex(sep='/')
        print("Reading: " + str(data))
        return msg

    def callback(self):
        self.serialPort.close()

    def getlabelb(self, selection):
        self.inputdata = selection

    def test1(self):
        print(self.inputdata)

    def send(self, id, angle):
        datalength = 0
        instruction = 0x03
        address = 0x2a
        pos = transform(angle).to_bytes(2, 'little')
        print("Value sent: %d", transform(angle))
        data = bytearray([0xff, 0xff, id, datalength, instruction, address, pos[0], pos[1]])
        data[3] = len(data) - 3
        data.append(checksum(data))
        self.write(data)
        # self.read(100)
        time.sleep(0.5)

    def syncsend(self, idlist, poslist):
        datalength = 0
        instruction = 0x83
        address = 0x2a
        length = 0x04
        data = bytearray([0xff, 0xff, 0xfe, datalength, instruction, address, length])
        for i in range(len(idlist)):
            pos = transform(poslist[i]).to_bytes(2, 'little')
            data.append(idlist[i])
            data.append(pos[0])
            data.append(pos[1])
            data.append(0xe8)
            data.append(0x03)
        data[3] = len(data) - 3
        data.append(checksum(data))
        self.write(data)

    def importsyncsend(self, filename):
        idlist, poslist = importpos(filename)
        self.syncsend(idlist, poslist)

    def dolistofmoves(self, filenameslist):
        for filename in filenameslist:
            self.importsyncsend(filename)
            print("Sending: " + filename)
            time.sleep(1)

    def get(self, id):
        return self.pos[id]

# p1 ch11 ch2 ch3 ch42 ch51 ch62 ch7 ch8 ch91 ch10 ch110 then back to ch2


if __name__ == "__main__":
    ports = serial_ports()
    print(ports)
    servo = OCServo(ports[0])
    time.sleep(2)
    print("Sending p1")
    servo.importsyncsend('p13')
    time.sleep(2)
    print("Sending list of moves")
    # do a list of moves # p1 ch11 ch2 ch3 ch42 ch51 ch62 ch7 ch8 ch91 ch10 ch110
    servo.dolistofmoves(['p13', 'ch12', 'ch21', 'ch31', 'ch44', 'ch51','ch997', 'ch63',
                         'ch71', 'ch83', 'ch92', 'ch10', 'ch111', 'ch21', 'ch3', 'ch44',
                         'ch51', 'ch997', 'ch63', 'ch71', 'ch83', 'ch92', 'ch10', 'ch111',
                         'ch21', 'p13'])
    servo.callback()
