import cv2
import numpy as np
from matplotlib import pyplot as plt


def detect_vertexes(img):
    edges = cv2.Canny(img, 50, 200)
    return edges


def histogram(img, mask, threshold=0.001):
    color = ('b', 'g', 'r')
    result = np.zeros((2, 3), dtype=np.uint8)
    for i, col in enumerate(color):
        histr = cv2.calcHist(
            images=[img], channels=[i], mask=mask, histSize=[257], ranges=[0, 256]
        ) / (img.shape[0] * img.shape[1])

        for j, value in enumerate(histr):
            if value > threshold:
                result[0, i] = j
                break

        for j, value in enumerate(np.flip(histr)):
            if value > threshold:
                result[1, i] = 255-j
                break

        plt.plot(histr, color=col)
        plt.xlim([0, 256])

    print(result)
    return result


if __name__ == "__main__":
    plt.figure()
    img = cv2.imread('test-data/train.jpg', -1)
    coords = np.array([[948.88104,  571.6861],
                       [842.7949,  2652.1519],
                       [3860.3545,  2652.1519],
                       [3718.9062,   489.17468], ], dtype=np.int32)
    mask = np.ones(img.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, coords, 0)
    #mask = 1-mask
    hist = histogram(img, mask)

    test_img = cv2.imread('test-data/test.jpg', -1)

    masked = cv2.inRange(test_img, hist[0], hist[1])

    kernel = np.ones([7, 7], dtype=np.uint8)
    masked = cv2.dilate(masked, kernel)

    test_img[masked != 0] = 0

    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    plt.figure()
    plt.imshow(test_img)
    plt.show()
    cv2.waitKey(0)
