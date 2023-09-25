
import cv2
from cv2 import UMat

import time
from runner import run
from my_timer import MyTimer
import math
import numpy as np

def filter_uzumaki(image_before:UMat)->UMat:
  t=time.perf_counter()
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
    a = math.tan(math.radians(math.sin(math.radians(t*45)) * 80))
    # mat = np.array([[1, 0, 0], [a, 1, 0]], dtype=np.float32)
    mat = np.array([[1, 0, 0], [a, 1, -polar_width*a*scale]], dtype=np.float32)
    image_skew=cv2.warpAffine(image_polar, mat,(math.floor(polar_width*scale),polar_height),borderMode=cv2.BORDER_WRAP)

  # return image_skew
  with MyTimer("warpPolar2"):
    image_after=cv2.warpPolar(image_skew,(width,height),(width*0.5,height*0.5),polar_width*0.8,flags+cv2.WARP_INVERSE_MAP)

  return image_after


run(filter_uzumaki)
