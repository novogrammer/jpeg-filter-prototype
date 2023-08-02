import socket
import struct
# import cv2
# import numpy

MY_IP = "127.0.0.1"
MY_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((MY_IP, MY_PORT))

sock.listen(1)

print("Waiting for connection...")

file_count = 0

while True:
  conn, addr = sock.accept()
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
    with open(filename, 'wb') as f:
      f.write(data)
    
    # img_buf=numpy.frombuffer(data,dtype=numpy.uint8)
    # img=cv2.imdecode(img_buf,cv2.IMREAD_COLOR)
    # cv2.imshow("imdecode",img)
    # cv2.waitKey(0)
  print("Waiting for next connection...")
