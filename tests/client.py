import cv2
import numpy as np
import socket

# Set up socket connection
HOST = '192.168.1.10'  # IP address of receiving computer
PORT = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Set up video capture
cap = cv2.VideoCapture("/dev/video0")  # use default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Send video stream
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Encode frame as JPEG image
    _, img_encoded = cv2.imencode('.jpg', frame)
    # Send image length and image data
    data = np.array(img_encoded)
    stringData = data.tostring()
    sock.sendall(str(len(stringData)).ljust(16).encode())
    sock.sendall(stringData)

# Clean up
cap.release()
cv2.destroyAllWindows()
sock.close()
