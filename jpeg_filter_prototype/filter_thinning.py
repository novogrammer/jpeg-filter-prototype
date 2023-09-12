
import cv2
from cv2 import UMat

from runner import run


def filter_thinning(image_before:UMat)->UMat:
    image_gray = cv2.cvtColor(image_before, cv2.COLOR_BGR2GRAY)

    _, image_binary = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY)

    image_after = cv2.ximgproc.thinning(image_binary)

    image_after = cv2.cvtColor(image_after, cv2.COLOR_GRAY2BGR)

    return image_after

run(filter_thinning)
