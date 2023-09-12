
import cv2
from cv2 import UMat
import time

from runner import run
import numpy as np


def filter_canny(image_before:UMat)->UMat:
  t=time.perf_counter()
  height,width,c = image_before.shape

  image_white = np.zeros((height,width,c),np.uint8)
  image_white += 255

  transform=cv2.getRotationMatrix2D((width / 2, height / 2), 45*t, 0.5)

  image_white_transformed = cv2.warpAffine(image_white,transform,(width,height))
  image_black_transformed = cv2.bitwise_not(image_white_transformed)
  image_before_transformed = cv2.warpAffine(image_before,transform,(width,height))
  image_after=cv2.bitwise_or(cv2.bitwise_and(image_before,image_black_transformed),image_before_transformed)
  
  
  return image_after


run(filter_canny)
