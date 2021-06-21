import cv2
import numpy as np
from matplotlib import pyplot as plt


class VertexFinder:
    def __init__(self, img, coords):
        self.img = img
        self.mask = np.ones(img.shape[:2], dtype=np.uint8)
        cv2.fillConvexPoly(self.mask, coords, 0)
        self.set_threshold()

    def set_threshold(self, threshold=0.001):
        '''Set the color threshold from an image and mask'''
        self.lowest = np.zeros((3,), dtype=np.uint8)
        self.highest = np.zeros((3,), dtype=np.uint8)
        row, col = self.img.shape[:2]
        for i in range(3):
            histr = cv2.calcHist(
                images=[self.img], channels=[i], mask=self.mask, histSize=[257], ranges=[0, 256]
            ) / (row * col)

            for j, value in enumerate(histr):
                if value > threshold:
                    self.lowest[i] = j
                    break

            for j, value in enumerate(np.flip(histr)):
                if value > threshold:
                    self.highest[i] = 255-j
                    break

            plt.plot(histr, color=['b', 'g', 'r'][i])
            plt.xlim([0, 256])

    def masked(self, img):
        '''Mask the img with color threshold'''
        mask = cv2.inRange(img, self.lowest, self.highest)
        kernel = np.ones([7, 7], dtype=np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        result = img.copy()
        result[mask != 0] = 0
        return result


if __name__ == "__main__":
    img = cv2.imread('test-data/train.jpg', -1)
    coords = np.array([[948.88104,  571.6861],
                       [842.7949,  2652.1519],
                       [3860.3545,  2652.1519],
                       [3718.9062,   489.17468], ], dtype=np.int32)
    finder = VertexFinder(img, coords)

    test_img = cv2.imread('test-data/test.jpg', -1)

    result = finder.masked(test_img)

    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    plt.figure()
    plt.imshow(result)
    plt.show()
