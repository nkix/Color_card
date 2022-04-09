import cv2
import cv2 as cv
import numpy as np
from color_analysis import color_analyze, color_classify


def img_seg_grab(img, lx, ly, width, height):
    """
    Do a image segmentation with GrabCut
    :param img: source image
    :param lx: top left x of rectangle
    :param ly: top left y of rectangle
    :param width: width of rectangle
    :param height: height of rectangle
    :return:
    """

    # set mask, background and foreground
    mask = np.zeros(img.shape[:2], np.uint8)
    background = np.zeros((1, 65), np.float64)
    foreground = np.zeros((1, 65), np.float64)

    # initialize the rectangular area which cover the foreground
    rect = (lx, ly, width, height)

    # GrubCut
    cv.grabCut(img, mask, rect, background, foreground, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img_seg = img * mask2[:, :, np.newaxis]

    return img_seg

