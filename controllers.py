import socket
import threading


class Controllers():
    def __init__(self):
        self.received_r = [0.0, 0.0, 0.0]
        self.received_t = [0.0, 0.0, 0.0]
        serverMACAddress = '20:17:03:01:62:62'
        port = 1
        self.s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.s.connect((serverMACAddress,port))
        self.get_text_thread_running = True
        self.get_text_thread = threading.Thread(target=self.listen)
        self.get_text_thread.start()

    def listen(self):
        print('Running listen thread')
        message = b''
        count_t = 0
        count_r = 0
        while True:
            if not self.get_text_thread_running:
                break
            byte_received = s.recv(1)
            message += byte_received
            if(byte_received == b't'):
                count_t = count_t + 1
            else:
                count_t = 0
            if(byte_received == b'r'):
                count_r = count_r + 1
            else:
                count_r = 0
            if count_t == 3 or count_r == 3: 
                #print('message received: ' + message.decode('utf-8').strip())
                num = None
                print(len(message))
                k = int((len(message)-3)/2)
                print(k)
                for i in range(k):
                    num = message[2*i+1]<<8 | message[2*i]
                    if count_t == 3:
                        self.received_t[i] = num/100
                    elif count_r == 3:
                        self.received_r[i] = num/100
                print("\nreceiver" + str(received_r))
                print("\ntransmitter" + str(received_t))
                message = b''

        s.close()