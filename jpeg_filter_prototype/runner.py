from queue import Empty, Queue
import socket
import os
import threading
from typing import Callable, Literal, TypedDict
from cv2 import UMat
from dotenv import load_dotenv

from image_transfer import receive_image, send_image
import cv2
import numpy as np
import PySimpleGUI as sg
from my_timer import MyTimer

class ImageMessage(TypedDict):
  name: Literal["before", "after"]
  png_image: bytes

def run(callback:Callable[[UMat],UMat]):
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



  def socket_thread(image_queue:Queue[ImageMessage]):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_send:
      sock_for_send.connect((YOUR_IP, YOUR_PORT))


      sock_for_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock_for_receive.bind(("0.0.0.0", MY_PORT))

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
          with MyTimer("process"):

            img_buf=np.frombuffer(received_data,dtype=np.uint8)
            with MyTimer("decode img_before"):
              img_before=cv2.imdecode(img_buf,cv2.IMREAD_COLOR)
            with MyTimer("encode png_before"):
              png_before=cv2.imencode('.png', img_before)[1].tobytes() 
            with MyTimer("callback"):
              img_after=callback(img_before)
            with MyTimer("encode png_after"):
              png_after=cv2.imencode('.png', img_after)[1].tobytes() 

            # cv2.imshow("imdecode",img)
            # cv2.waitKey(0)
            print("Filtered.")
            with MyTimer("encode img_after"):
              ret,encoded = cv2.imencode(".jpg", img_after, (cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY))
            if not ret:
              print("Encode failed!!!")
              continue

            print("Encoded.")
          sending_data=encoded.tobytes()

          image_queue.put(
            ImageMessage(name="before",png_image=png_before)
          )
          image_queue.put(
            ImageMessage(name="after",png_image=png_after)
          )

          send_image(sock_for_send,sending_data)
          print("Sent.")
          
        print("Waiting for next connection...")

  image_queue:"Queue[ImageMessage]"=Queue()

  socket_thread = threading.Thread(target=socket_thread, args=(image_queue,))
  # メインスレッドの終了と同時に強制終了
  socket_thread.daemon = True
  socket_thread.start()


  sg.theme('LightBlue')


  layout = [
    [
      sg.Text('Before Image', size=(40, 1), justification='center', font='Helvetica 20',key='before_image_text'),
      sg.Text('After Image', size=(40, 1), justification='center', font='Helvetica 20',key='after_image_text'),
    ],
    [
      sg.Image(filename='', key='before_image'),
      sg.Image(filename='', key='after_image'),
    ],
  ]


  window = sg.Window('Filter',layout, location=(100, 100))
  while True:
      event,values=window.read(timeout=1)
      if event == sg.WIN_CLOSED:
          break
      try:
        image_message=image_queue.get(False)
        if image_message["name"]=="before":
          window["before_image"].update(data=image_message["png_image"])
        if image_message["name"]=="after":
          window["after_image"].update(data=image_message["png_image"])
      except Empty:
        pass
      

  # 画面を閉じる
  window.close()


