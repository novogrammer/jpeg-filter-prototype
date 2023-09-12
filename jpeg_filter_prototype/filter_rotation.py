
import cv2
from cv2 import UMat
import time

from runner import run
import numpy as np
from my_timer import MyTimer


def filter_canny(image_before:UMat)->UMat:
  t=time.perf_counter()
  height,width,c = image_before.shape

  with MyTimer("image_white"):
    image_white = np.zeros((height,width,c),np.uint8)
    image_white += 255

  with MyTimer("transform"):
    transform=cv2.getRotationMatrix2D((width / 2, height / 2), 45*t, 0.5)

  with MyTimer("image_white_transformed"):
    image_white_transformed = cv2.warpAffine(image_white,transform,(width,height))
  with MyTimer("image_black_transformed"):
    image_black_transformed = cv2.bitwise_not(image_white_transformed)
  with MyTimer("image_before_transformed"):
    image_before_transformed = cv2.warpAffine(image_before,transform,(width,height))
  with MyTimer("image_temp"):
    image_temp=cv2.bitwise_and(image_before,image_black_transformed)
  with MyTimer("image_after"):
    image_after=cv2.bitwise_or(image_temp,image_before_transformed)
  return image_after


run(filter_canny)
