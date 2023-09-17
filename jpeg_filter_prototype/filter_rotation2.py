
from typing import Any
import cv2
from cv2 import UMat
import time
import os

from runner import run
import numpy as np
from my_timer import MyTimer

class FilterCanny2:
  def __init__(self) -> None:
    self.image_white = None
    self.image_white_transformed = None
    self.image_black_transformed = None
    self.image_before_transformed = None
    self.image_temp = None
  def prepare_images(self, image_base:UMat) -> None:
    height,width,c = image_base.shape
    self.image_white = np.zeros((height,width,c),np.uint8)
    self.image_white += 255
    self.image_white_transformed = self.image_white.copy()
    self.image_black_transformed = self.image_white.copy()
    self.image_before_transformed = self.image_white.copy()
    self.image_temp = self.image_white.copy()

  def __call__(self, image_before:UMat) -> UMat:
    height,width,c = image_before.shape
    t=time.perf_counter()
    if self.image_white is None or self.image_white.shape != image_before.shape:
      self.prepare_images(image_before)
    
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

filterCanny2=FilterCanny2()
run(filterCanny2)
