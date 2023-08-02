import socket
import struct

YOUR_IP = "127.0.0.1"
YOUR_PORT = 5005


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect((YOUR_IP, YOUR_PORT))

  with open('sending_image.jpg', 'rb') as f:
    data = f.read()
  size = len(data)
  sock.send(struct.pack('!I', size))
  sock.sendall(data)

print("Sent")
