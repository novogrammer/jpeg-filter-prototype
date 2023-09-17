
from typing import Any
import cv2
from cv2 import UMat
import time
import os

from runner import run
import numpy as np
from my_timer import MyTimer

IMAGE_WIDTH=int(os.getenv("SENDER_IMAGE_WIDTH","480"))
IMAGE_HEIGHT=int(os.getenv("SENDER_IMAGE_HEIGHT","270"))

class FilterCanny2:
  def __init__(self,width:int,height:int) -> None:
    self.image_white = np.zeros((height,width,3),np.uint8)
    self.image_white += 255
    self.image_white_transformed = self.image_white.copy()
    self.image_black_transformed = self.image_white.copy()
    self.image_before_transformed = self.image_white.copy()
    self.image_temp = self.image_white.copy()
  def __call__(self, image_before:UMat) -> UMat:
    t=time.perf_counter()
    height,width,c = image_before.shape

    print(self.image_black_transformed.shape)
    print(image_before.shape)
    
    with MyTimer("transform"):
      transform=cv2.getRotationMatrix2D((width / 2, height / 2), 45*t, 0.5)
    with MyTimer("image_white_transformed"):
      cv2.warpAffine(self.image_white,transform,(width,height),self.image_white_transformed)
    with MyTimer("image_black_transformed"):
      cv2.bitwise_not(self.image_white_transformed,self.image_black_transformed)
    with MyTimer("image_before_transformed"):
      cv2.warpAffine(image_before,transform,(width,height),self.image_before_transformed)
    with MyTimer("image_temp"):
      cv2.bitwise_and(image_before,self.image_black_transformed,self.image_temp)
    with MyTimer("image_after"):
      image_after=cv2.bitwise_or(self.image_temp,self.image_before_transformed)
    return image_after

filterCanny2=FilterCanny2(IMAGE_WIDTH,IMAGE_HEIGHT)
run(filterCanny2)
