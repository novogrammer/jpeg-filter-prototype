
import cv2
from cv2 import UMat

from runner import run


def filter_thinning(img_before:UMat)->UMat:
    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)

    img_after = cv2.ximgproc.thinning(img_binary)

    img_after = cv2.cvtColor(img_after, cv2.COLOR_GRAY2BGR)

    return img_after

run(filter_thinning)
