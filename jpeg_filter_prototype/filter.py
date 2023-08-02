import socket
import struct
import os
from dotenv import load_dotenv
# import cv2
# import numpy

load_dotenv()

MY_IP=os.getenv("FILTER_MY_IP","127.0.0.1")
MY_PORT=int(os.getenv("FILTER_MY_PORT","5000"))
print(f"MY_IP: {MY_IP}")
print(f"MY_PORT: {MY_PORT}")

YOUR_IP=os.getenv("FILTER_YOUR_IP","127.0.0.1")
YOUR_PORT=int(os.getenv("FILTER_YOUR_PORT","5000"))
print(f"YOUR_IP: {YOUR_IP}")
print(f"YOUR_PORT: {YOUR_PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_send:
  sock_for_send.connect((YOUR_IP, YOUR_PORT))


  sock_for_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock_for_receive.bind((MY_IP, MY_PORT))

  sock_for_receive.listen(1)

  print("Waiting for connection...")

  file_count = 0

  while True:
    conn, addr = sock_for_receive.accept()
    print(f"Connected by {addr}")

    while True:
      file_count += 1
      filename = f'received_image_{file_count}.jpg'
      data = conn.recv(4)
      if not data:
        print("Client disconnected.")
        conn.close()
        break
      size = struct.unpack('!I', data)[0]

      data = b''
      isClosing = False
      while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
          isClosing = True
          break
        data += packet
      if isClosing:
        print("Client disconnected.")
        conn.close()
        break
      print("Received.")
      sock_for_send.send(struct.pack('!I', size))
      sock_for_send.sendall(data)
      print("Sent.")
      
      # img_buf=numpy.frombuffer(data,dtype=numpy.uint8)
      # img=cv2.imdecode(img_buf,cv2.IMREAD_COLOR)
      # cv2.imshow("imdecode",img)
      # cv2.waitKey(0)
    print("Waiting for next connection...")
