import socket
import os
from dotenv import load_dotenv

from image_transfer import receive_image, send_image
import cv2
import numpy

load_dotenv()

MY_IP=os.getenv("FILTER_MY_IP","127.0.0.1")
MY_PORT=int(os.getenv("FILTER_MY_PORT","5000"))
print(f"MY_IP: {MY_IP}")
print(f"MY_PORT: {MY_PORT}")

YOUR_IP=os.getenv("FILTER_YOUR_IP","127.0.0.1")
YOUR_PORT=int(os.getenv("FILTER_YOUR_PORT","5000"))
print(f"YOUR_IP: {YOUR_IP}")
print(f"YOUR_PORT: {YOUR_PORT}")

JPEG_QUALITY=int(os.getenv("FILTER_JPEG_QUALITY","80"))
print(f"JPEG_QUALITY: {JPEG_QUALITY}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_send:
  sock_for_send.connect((YOUR_IP, YOUR_PORT))


  sock_for_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock_for_receive.bind((MY_IP, MY_PORT))

  sock_for_receive.listen(1)

  print("Waiting for connection...")


  while True:
    conn_for_receive, addr = sock_for_receive.accept()
    print(f"Connected by {addr}")

    while True:

      received_data=receive_image(conn_for_receive)
      if received_data is None:
        print("Client disconnected.")
        conn_for_receive.close()
        break
      print("Received.")
      img_buf=numpy.frombuffer(received_data,dtype=numpy.uint8)
      img_before=cv2.imdecode(img_buf,cv2.IMREAD_COLOR)
      img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
      img_after = cv2.Canny(img_gray, 100, 200)

      # cv2.imshow("imdecode",img)
      # cv2.waitKey(0)
      print("Filtered.")
      ret,encoded = cv2.imencode(".jpg", img_after, (cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY))
      if not ret:
        print("Encode failed!!!")
        continue

      print("Encoded.")
      sending_data=encoded.tobytes()

      send_image(sock_for_send,sending_data)
      print("Sent.")
      
    print("Waiting for next connection...")
