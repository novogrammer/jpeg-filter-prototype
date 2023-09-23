import socket
import os
import cv2

capture=cv2.VideoCapture(0)
while capture.isOpened():
  result_read,frame=capture.read()
  if not result_read:
    print("not result_read")
    continue
  cv2.imshow("frame",frame)
  cv2.waitKey(1)



