import socket

YOUR_IP = "127.0.0.1"
YOUR_PORT = 5005


# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((YOUR_IP, YOUR_PORT))

with open('sending_image.jpg', 'rb') as f:
  data = f.read()

sock.send(data)

print("Sent")
