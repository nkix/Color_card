import sys
import getopt
import cv2 as cv
import os

import numpy as np

from color_analysis import color_analyze
from color_analysis import color_classify


def main(argv):
    """
    set the commands
    :param argv:
    """
    image_path = ''
    k = None
    color_max = 15
    show_rgb = False
    try:
        opts, args = getopt.getopt(argv, "hf:k:m:v:")
    except getopt.GetoptError:
        print('fail to compile')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('python color_app.py -f <input image> -k <k value> -m <max number of color> -v <show rgb value>')
            print('max number of color is default 15')
            print('show rgb value is default set to false, 0: False, 1: True')
            sys.exit()
        elif opt == "-f":
            image_path = arg
        elif opt == "-k":
            k = int(arg)
        elif opt == '-m':
            color_max = int(arg)
        elif opt == '-v':
            if int(arg) == 1:
                show_rgb = True

    if image_path != '' and k is not None:
        img = cv.imread(image_path)
        card, rgb_value = color_analyze(img, k, color_max, show_rgb)
        result = np.hstack((img, card))
        name = os.path.basename(image_path)
        color_classify(rgb_value, result, name)
        cv.imshow('result', result)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("need to provide right image path and k value")
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])