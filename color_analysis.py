import cv2
import numpy as np
import cv2 as cv
import collections
import colorsys


def color_classify(rgb, image, name):
    """
    This method will classify image to different files based on the dominant color
    :param rgb: the rgb value of dominant color of image
    :param image:
    :param name: name of image file
    :return:
    """
    # transfer rgb value to hsv
    r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)

    m = mx-mn

    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx

    h = h/2
    s = s*255.0
    v = v*255.0

    # range of colors
    # black
    if 0 <= v <= 46:
        path = 'classification/black/' + name
        cv.imwrite(path, image)
    # grey
    elif 0 <= s <= 43:
        path = 'classification/grey/' + name
        cv.imwrite(path, image)
    # white
    elif (0 <= s <= 30) and (221 <= v <= 255):
        path = 'classification/white/' + name
        cv.imwrite(path, image)
    elif 43 <= s <= 255:
        print("h=" + str(h))
        # orange
        if 11 <= h <= 25:
            path = 'classification/orange/' + name
            cv.imwrite(path, image)
        # yellow
        elif 26 <= h <= 34:
            path = 'classification/yellow/' + name
            cv.imwrite(path, image)
        # green
        elif 35 <= h <= 77:
            path = 'classification/green/' + name
            cv.imwrite(path, image)
        # cyan
        elif 78 <= h <= 99:
            path = 'classification/cyan/' + name
            cv.imwrite(path, image)
        # blue
        elif 100 <= h <= 124:
            path = 'classification/blue/' + name
            cv.imwrite(path, image)
        # purple
        elif 125 <= h <= 155:
            path = 'classification/purple/' + name
            cv.imwrite(path, image)
        # red
        else:
            path = 'classification/red/' + name
            cv.imwrite(path, image)


def color_analyze(image, k, color_max=15, show_rgb_value=False, isobj=False):
    """
    This method will analysis image, calculate color clusters with K-means
    :param color_max: the number of colors used in generation of colour card
    :param image: input image
    :param k: number of labels
    :param show_rgb_value: show rgb value on colour card
    :param isobj: boolean value to tell if image is output of grabcut
    :return: image with color distribution, main color
    """
    # k cannot be less than 3
    if k <= 3:
        k = 3

    # if the input image is segmented
    # may need k+1 color in case black should be replaced
    if isobj:
        k += 1

    # transfer image to array with color info in pixels
    data = np.float32(image).reshape((-1, 3))

    # terminate criteria (run 20 times or reach epsilon=1.0)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_MAX_ITER, 20, 1.0)

    # K-means
    ret, label, center = cv.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)

    # calculate color distribution
    if k >= color_max:
        k = color_max
    counter = collections.Counter(label.flatten())
    sorted_count = counter.most_common(k)

    # draw color card
    desired_height = image.shape[0]
    desired_width = 150
    width_colors = 150
    height_colors = desired_height/k

    color_card = np.ones((desired_height, desired_width, 3), dtype='uint8') * 255
    start = 0

    # number of pixels
    total = image.shape[0] * image.shape[1]
    r_sum = 0
    g_sum = 0
    b_sum = 0
    count = 0
    replace = False  # if there is black removed from card

    for items in sorted_count:
        if isobj and (count == k-1) and not replace:
            break
        end = start + height_colors
        # draw rectangle filled with color
        color = center[items[0]].tolist()
        if isobj and color[0] == 0 and color[1] == 0 and color[2] == 0:
            replace = True
            continue
        cv2.rectangle(color_card, (0, int(start)), (width_colors, int(end)), center[items[0]].tolist(), -1)

        if count < k//2 and count < color_max:
            normalized = items[1]/total
            r_sum += color_card[int(start), 0, 2] * normalized
            g_sum += color_card[int(start), 0, 1] * normalized
            b_sum += color_card[int(start), 0, 0] * normalized

        if show_rgb_value:
            # write RGB value of color
            r = color_card[int(start), 0, 2]
            g = color_card[int(start), 0, 1]
            b = color_card[int(start), 0, 0]
            text = " R:" + str(r) + " G:" + str(g) + " B:" + str(b)
            cv2.putText(color_card, text, (0, int(start+height_colors/2)), cv.FONT_HERSHEY_PLAIN, 0.7,
                        (int(255-r), int(255-g), int(255-b)), 1)

        count += 1
        start = end
    rgb = [r_sum, g_sum, b_sum]

    # connect image with color distribution
    return color_card, rgb


