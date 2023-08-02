import socket
import cv2
import numpy

MY_IP = "127.0.0.1"
MY_PORT = 5005

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((MY_IP, MY_PORT))

sock.listen(1)
conn, addr = sock.accept()
print(f"Connected by {addr}")

data = conn.recv(65535) # バッファサイズは適切に調整してください

img_buf=numpy.frombuffer(data,dtype=numpy.uint8)
img=cv2.imdecode(img_buf,cv2.IMREAD_COLOR)
cv2.imshow("imdecode",img)
cv2.waitKey(0)

# # 画像を保存するなどの処理
# with open('received_image.jpg', 'wb') as f:
#   f.write(data)


print("Received")
