
import cv2
from cv2 import UMat

from runner import run


def filter_canny(image_before:UMat)->UMat:
  image_gray = cv2.cvtColor(image_before, cv2.COLOR_BGR2GRAY)
  image_after = cv2.Canny(image_gray, 100, 200)
  return image_after


run(filter_canny)
