
import cv2
from cv2 import UMat

from runner import run


def filter_canny(img_before:UMat)->UMat:
  img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
  img_after = cv2.Canny(img_gray, 100, 200)
  return img_after


run(filter_canny)
