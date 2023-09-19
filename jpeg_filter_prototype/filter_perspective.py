
import cv2
from cv2 import UMat
import time

from runner import run
import numpy as np
from my_timer import MyTimer

import math


def filter_perspective(image_before:UMat)->UMat:
  t=time.perf_counter()
  height,width,c = image_before.shape

  proj2dto3d = np.array([[1,0,width*-0.5],
                        [0,1,height*-0.5],
                        [0,0,0],
                        [0,0,1]],np.float32)

  proj3dto2d = np.array([ [-100,0,width * 0.5,0],
                          [0,-100,height * 0.5,0],
                          [0,0,1,0] ],np.float32)
  
  translateCamera = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,width * -0.75],
    [0,0,0,1],
  ],np.float32)

  translateZ = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,width * 0.5],
    [0,0,0,1],
  ],np.float32)

  image_after = np.zeros((height,width,c),np.uint8)
  for i in range(4):
    rotY = math.radians(t * 0.1 * 360 + i * 90)
    cos_rotY = math.cos(rotY)
    sin_rotY = math.sin(rotY)
    if cos_rotY > 0:
      ry = np.array([
        [cos_rotY,0,-sin_rotY,0],
        [0,1,0,0],
        [sin_rotY,0,cos_rotY,0],
        [0,0,0,1]
      ],np.float32)
      transform = proj3dto2d.dot(translateCamera.dot(ry.dot(translateZ.dot(proj2dto3d))))

      image_transformed=cv2.warpPerspective(image_before,transform,(width,height))
      image_after=cv2.add(image_after,image_transformed)

  return image_after


run(filter_perspective)
