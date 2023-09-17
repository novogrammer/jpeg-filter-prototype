from queue import Empty,Full, Queue
import socket
import os
import time
import threading
from typing import Callable, Literal, TypedDict
from cv2 import UMat
from dotenv import load_dotenv

from image_transfer import receive_image, send_image
import cv2
import numpy as np
from my_timer import MyTimer

# class ImageMessage(TypedDict):
#   name: Literal["before", "after"]
#   image: UMat

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



  def receiver(image_before_queue:Queue[UMat]):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_receive:
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
          image_buf=np.frombuffer(received_data,dtype=np.uint8)
          with MyTimer("decode image_before"):
            image_before=cv2.imdecode(image_buf,cv2.IMREAD_COLOR)
          try:
            image_before_queue.put(image_before)
          except Full:
            print("image_before_queue is Full")

        print("Waiting for next connection...")
  def converter(image_before_queue:Queue[UMat],image_after_queue:Queue[UMat]):
    while True:
      try:
        image_before=image_before_queue.get(True,0.1)
        with MyTimer("callback"):
          image_after=callback(image_before)
        print("Filtered.")
        try:
          image_after_queue.put(image_after)
        except Full:
          print("image_after_queue is Full")
      except Empty:
        pass

  def sender(image_after_queue:Queue[UMat],image_showing_queue:Queue[UMat]):
    while True:
      try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_send:
          sock_for_send.connect((YOUR_IP, YOUR_PORT))
          while True:
            try:
              image_after=image_after_queue.get(True,0.1)
              try:
                image_showing_queue.put(image_after)
              except Full:
                print("image_showing_queue is Full")

              with MyTimer("encode image_after"):
                ret,encoded = cv2.imencode(".jpg", image_after, (cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY))
              if not ret:
                print("Encode failed!!!")
                continue
              print("Encoded.")
              sending_data=encoded.tobytes()
              send_image(sock_for_send,sending_data)
              print("Sent.")
            except Empty:
              pass
      except socket.error as e:
        print(e)
        print("retry connect")
        time.sleep(1)

  image_before_queue:Queue[UMat]=Queue(100)
  image_after_queue:Queue[UMat]=Queue(100)
  image_showing_queue:Queue[UMat]=Queue(100)

  receiver_thread = threading.Thread(target=receiver, args=(image_before_queue,))
  # メインスレッドの終了と同時に強制終了
  receiver_thread.daemon = True
  receiver_thread.start()

  converter_thread = threading.Thread(target=converter, args=(image_before_queue,image_after_queue,))
  # メインスレッドの終了と同時に強制終了
  converter_thread.daemon = True
  converter_thread.start()

  sender_thread = threading.Thread(target=sender, args=(image_after_queue,image_showing_queue,))
  # メインスレッドの終了と同時に強制終了
  sender_thread.daemon = True
  sender_thread.start()


  window_name="filter"
  cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
  is_fullscreen=False

  while True:
    key = cv2.waitKey(1)
    if key == 27:
      break
    if key==ord("f"):
      if is_fullscreen:
        cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
        is_fullscreen=False
      else:
        cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        is_fullscreen=True
    try:
      image_showing=image_showing_queue.get(False)
      with MyTimer("imshow"):
        cv2.imshow(window_name,image_showing)
    except Empty:
      pass
      

  # 画面を閉じる
  cv2.destroyAllWindows()


