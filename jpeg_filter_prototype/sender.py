import socket
import os

from dotenv import load_dotenv

from image_transfer import send_image

load_dotenv()

MY_IP=os.getenv("FILTER_MY_IP","127.0.0.1")
MY_PORT=int(os.getenv("FILTER_MY_PORT","5000"))
print(f"MY_IP: {MY_IP}")
print(f"MY_PORT: {MY_PORT}")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_send:
  sock_for_send.connect((MY_IP, MY_PORT))

  with open('sending_image.jpg', 'rb') as f:
    data = f.read()
  send_image(sock_for_send,data)

print("Sent.")
