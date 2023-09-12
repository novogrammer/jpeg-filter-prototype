
import cv2
from cv2 import UMat
import time

from runner import run
import numpy as np


def filter_canny(img_before:UMat)->UMat:
  t=time.perf_counter()
  height,width,c = img_before.shape

  img_white = np.zeros((height,width,c),np.uint8)
  img_white += 255

  transform=cv2.getRotationMatrix2D((width / 2, height / 2), 45*t, 0.5)

  img_white_transformed = cv2.warpAffine(img_white,transform,(width,height))
  img_black_transformed = cv2.bitwise_not(img_white_transformed)
  img_before_transformed = cv2.warpAffine(img_before,transform,(width,height))
  img_after=cv2.bitwise_or(cv2.bitwise_and(img_before,img_black_transformed),img_before_transformed)
  
  
  return img_after


run(filter_canny)
