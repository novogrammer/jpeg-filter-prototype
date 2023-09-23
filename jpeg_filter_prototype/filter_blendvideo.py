
import os
import cv2
from cv2 import UMat
from dotenv import load_dotenv

from runner import run
load_dotenv()
VIDEO_INDEX=int(os.getenv("FILTER_VIDEO_INDEX","0"))
print(f"VIDEO_INDEX: {VIDEO_INDEX}")

capture=cv2.VideoCapture(VIDEO_INDEX)

def filter_blendvideo(image_before:UMat)->UMat:
  if not capture.isOpened():
    print("not capture.isOpened()")
    return image_before

  result_read,frame=capture.read()
  if not result_read:
    print("not result_read")
    return image_before
  height,width,c = image_before.shape
  resized_frame=cv2.resize(frame, (width,height))
  # resized_frame=cv2.flip(resized_frame,1)
  image_after=cv2.addWeighted(image_before,0.5,resized_frame,0.5,0.0)
  return image_after

run(filter_blendvideo)
