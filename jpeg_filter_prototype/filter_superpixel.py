
import cv2
from cv2 import UMat

from runner import run


def filter_superpixel(image_before:UMat)->UMat:
    height, width,channels = image_before.shape[:3]

    num_superpixels = 400
    num_levels = 4
    prior = 2
    histogram_bins = 5
    double_step=True

    num_iterations = 4

    seeds = cv2.ximgproc.createSuperpixelSEEDS(
      width,
      height,
      channels,
      num_superpixels,
      num_levels,
      prior,
      histogram_bins,
      double_step
    )

    # スーパーピクセルセグメンテーションを適用
    seeds.iterate(image_before, num_iterations)

    # 結果を取得
    labels = seeds.getLabels()
    contour_mask = seeds.getLabelContourMask(False)
    image_after:UMat=image_before.copy()
    image_after[0<contour_mask]=(0,255,255)

    return image_after

run(filter_superpixel)
