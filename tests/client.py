import cv2
import numpy as np
import socket
import struct

# Set up socket connection
HOST = '192.168.1.10'  # IP address of receiving computer
PORT = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Send video stream
cap = cv2.VideoCapture(0)
while True:
    # Capture frame
    ret, frame = cap.read()
    # Encode frame
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encimg = cv2.imencode('.jpg', frame, encode_param)
    # Debugging statements
    print(f"Encoded image size: {encimg.size}")
    # Send encoded frame
    data = np.array(encimg)
    stringData = data.tostring()
    sock.sendall(struct.pack('!I', len(stringData)))
    sock.sendall(stringData)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
sock.close()
