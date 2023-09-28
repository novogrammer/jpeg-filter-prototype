import os
import threading
import cv2
from cv2 import UMat
import numpy as np
from dotenv import load_dotenv
from my_timer import MyTimer
import serial
import time
from queue import Empty,Full, Queue
import math
from runner import run
load_dotenv()

WAIT_FOR_CONNECTION=2
BAUDRATE=115200
HANDSHAKE_FROM_PC="ready?\r\n"
HANDSHAKE_FROM_ARDUINO="ok.\r\n"

ARDUINO_HCSR04_DEVICE=os.getenv("FILTER_ARDUINO_HCSR04_DEVICE","")
print(f"ARDUINO_HCSR04_DEVICE: {ARDUINO_HCSR04_DEVICE}")
if ARDUINO_HCSR04_DEVICE=="":
  raise ValueError("ARDUINO_HCSR04_DEVICE is None")



arduinoSerial=serial.Serial(ARDUINO_HCSR04_DEVICE,BAUDRATE)
print("serial opening")
time.sleep(WAIT_FOR_CONNECTION)
a=str.encode(HANDSHAKE_FROM_PC)
print(HANDSHAKE_FROM_PC)
print(a)
arduinoSerial.write(str.encode(HANDSHAKE_FROM_PC))
arduinoSerial.flush()
print("serial sent")
handshakeFromArduino = arduinoSerial.readline().decode()
print("serial received")
print(handshakeFromArduino)
if handshakeFromArduino!=HANDSHAKE_FROM_ARDUINO:
  print(str.encode(handshakeFromArduino))
  raise RuntimeError("handshake failed")


distance_queue:Queue[int] = Queue(1)


def serial_receiver(distance_queue:Queue[int])->None:
  while True:
    distance=int.from_bytes(arduinoSerial.read(2),"big")
    print("serial received")
    print(distance)
    try:
      distance_queue.put(distance)
    except Full:
      pass


serial_receiver_thread = threading.Thread(target=serial_receiver, args=(distance_queue,))
# メインスレッドの終了と同時に強制終了
serial_receiver_thread.daemon = True
serial_receiver_thread.start()

distance=0

def filter_distance(image_before:UMat)->UMat:
  global distance
  height,width,c = image_before.shape

  try:
    distance=distance_queue.get(False)
  except Empty:
    pass
  print(distance)
  
  image_after=image_before.copy()
  ratio=min(distance / 1000.0,1.0)
  # h=int(ratio * height))
  # cv2.rectangle(image_after,
  #               (0,0),
  #               (int(width * 0.5), h ),
  #               (255, 0, 0), thickness=-1)

  # uzumaki.pyより

  flags = cv2.INTER_CUBIC + cv2.WARP_FILL_OUTLIERS + cv2.WARP_POLAR_LOG
  height,width,c = image_before.shape
  scale=1.5
  with MyTimer("warpPolar1"):
    r=math.sqrt(width**2+height**2)*0.5
    polar_width=math.floor(r)
    polar_height=math.floor(r * math.pi)
    image_polar=cv2.warpPolar(image_before,(math.floor(polar_width*scale),polar_height),(width*0.5,height*0.5),polar_width,flags)
  # return image_polar
  with MyTimer("skew"):
    a = math.tan(math.radians(math.sin(math.radians((1 - ratio)*90)) * 80))
    # mat = np.array([[1, 0, 0], [a, 1, 0]], dtype=np.float32)
    mat = np.array([[1, 0, 0], [a, 1, -polar_width*a*scale]], dtype=np.float32)
    image_skew=cv2.warpAffine(image_polar, mat,(math.floor(polar_width*scale),polar_height),borderMode=cv2.BORDER_WRAP)

  # return image_skew
  with MyTimer("warpPolar2"):
    image_after=cv2.warpPolar(image_skew,(width,height),(width*0.5,height*0.5),polar_width*0.8,flags+cv2.WARP_INVERSE_MAP)

  return image_after

run(filter_distance)
