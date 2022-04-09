import sys
import getopt
import cv2 as cv
import os
import numpy as np

from color_analysis import color_analyze, color_classify
from image_seg import img_seg_grab


def main(argv):
    """
    set the commands
    :param argv:
    """
    image_path = ''
    p_direct = ''
    k = None
    color_max = 15
    show_rgb = False
    is_obj = False
    is_package = False

    try:
        opts, args = getopt.getopt(argv, "hf:k:m:sop:")
    except getopt.GetoptError:
        print('fail to compile')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('apply on one file and show result:')
            print('python color_app.py -f <input image> -k <k value> -m <max number of color> -s -o')
            print('use -o to do image segmentation before analysis color')
            print('apply on all images in /images and classify them: ')
            print('python color_app.py -p <package directory> -k <k value> -m <max number of color> -s')
            print('max number of color is default 15')
            print('use -s to show rgb value of colour card')
            sys.exit()
        elif opt == "-f":
            image_path = arg
        elif opt == "-k":
            k = int(arg)
        elif opt == '-m':
            color_max = int(arg)
        elif opt == '-s':
            show_rgb = True
        elif opt == '-o':
            is_obj = True
        elif opt == '-p':
            is_package = True
            p_direct = arg

    if is_package and k is not None and p_direct != '':
        p = os.walk(p_direct)
        for path, dir_list, file_list in p:
            for file in file_list:
                fpath = path + '/' + str(file)
                print(fpath)
                img = cv.imread(fpath)
                card, rgb_value = color_analyze(img, k, color_max, show_rgb)
                result = np.hstack((img, card))
                color_classify(rgb_value, result, file)

    elif image_path != '' and k is not None:
        img = cv.imread(image_path)
        if is_obj:
            while True:
                r = cv.selectROI('roi', img, False, False)
                img_seg = img_seg_grab(img, r[0], r[1], r[2], r[3])
                cv.imshow("object", img_seg)
                key = cv.waitKey(0)
                cv.destroyAllWindows()
                if key == ord('r'):
                    continue
                else:
                    break
            card, rgb_value = color_analyze(img_seg, k, color_max, show_rgb, isobj=True)
        else:
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
