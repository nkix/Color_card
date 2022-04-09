import cv2
import cv2 as cv
import numpy as np
from color_analysis import color_analyze, color_classify


def onmouse_pick_range(event, x, y, flags, param):
    lx, ly, rx, ry = 0, 0, 0, 0
    if event == cv.EVENT_LBUTTONDOWN and flags == cv.EVENT_FLAG_LBUTTON:
        lx, ly = x, y
    if event == cv.EVENT_LBUTTONUP:
        rx, ry = x, y
        if (rx > lx) and (ry > ly):
            width = rx - lx
            height = ry - ly
            img_seg_grab(img, lx, ly, width, height)
        else:
            return 0, 0, 0, 0


def img_seg_grab(img, lx, ly, width, height):

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

    card, rgb = color_analyze(img_seg, 10, isobj=True)
    result = np.hstack((img, card))

    cv2.imshow("dst", img_seg)
    cv.imshow('result', result)
    cv2.waitKey(0)


img = cv.imread('images/banana.jpg')
cv.namedWindow('object range select')
cv.setMouseCallback('object range select', onmouse_pick_range)

cv.imshow('object range select', img)

cv.waitKey(0)
cv.destroyAllWindows()





