import socket
import struct
import cv2
import numpy

MY_IP = "127.0.0.1"
MY_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((MY_IP, MY_PORT))

sock.listen(1)

print("Waiting for connection...")

while True:
  conn, addr = sock.accept()
  print(f"Connected by {addr}")

  while True:
    data = conn.recv(4)
    if not data:
      print("Client disconnected.")
      conn.close()
      break
    size = struct.unpack('!I', data)[0]

    data = b''
    while len(data) < size:
      packet = conn.recv(size - len(data))
      if not packet:
        print("Client disconnected.")
        conn.close()
        break
      data += packet
    print("Received.")

    img_buf=numpy.frombuffer(data,dtype=numpy.uint8)
    img=cv2.imdecode(img_buf,cv2.IMREAD_COLOR)
    cv2.imshow("imdecode",img)
    cv2.waitKey(0)
  print("Waiting for next connection...")
