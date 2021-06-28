import cv2
import numpy as np
from matplotlib import pyplot as plt


def distance(x, y, cx, cy):
    return (x-cx)**2 + (y-cy)**2


def filter(img, mask):
    result = np.ones(img.shape[:2], dtype=np.uint8)
    for i, frame in enumerate(cv2.split(img)):
        result *= mask[i][frame]
    return result


def closest(mask, cx, cy, value):
    '''Return the closest pixel to (cx, cy) which is 0'''
    nonzero = cv2.findNonZero((mask == value).astype(np.uint8))
    distances = (nonzero[:, :, 0] - cx) ** 2 + (nonzero[:, :, 1] - cy) ** 2
    idx = np.argmin(distances)
    return nonzero[idx][0]


class VertexFinder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.learned = False
        self.lowest = np.zeros((3,), dtype=np.uint8)
        self.highest = np.zeros((3,), dtype=np.uint8)
        self.threshold = np.zeros((3, 257), dtype=np.uint8)

    def setup(self, img, coords):
        mask = np.ones(img.shape[:2], dtype=np.uint8)
        cv2.fillConvexPoly(mask, coords.astype(np.int32), 0)
        self.set_threshold(img, mask)
        self.learned = True

    def set_threshold(self, img, mask, threshold=0.001):
        '''Set the color threshold from an image and mask'''
        row, col = img.shape[:2]
        plt.figure()
        self.threshold = np.zeros((3, 257), dtype=np.uint8)
        for i in range(3):
            histr = cv2.calcHist(
                images=[img], channels=[i], mask=mask, histSize=[257], ranges=[0, 256]
            ) / (row * col)

            self.threshold[i][histr[:, 0] > threshold] = 1

            plt.plot(histr, color=['b', 'g', 'r'][i])
            #plt.plot(self.threshold[i], color=['b', 'g', 'r'][i])
            plt.xlim([0, 256])

    def set_mask(self, img):
        '''Mask the img not in the color range'''
        masked = 1-filter(img, self.threshold)
        kernel = np.ones([9, 9], dtype=np.uint8)
        masked = cv2.erode(masked, kernel, iterations=1)
        masked = cv2.dilate(masked, kernel, iterations=1)
        self.mask = masked

    def vertexes(self):
        '''Get the vertexes by the color threshold
            return the closest points to the four corners'''
        row, col = self.mask.shape[:2]
        result = []

        _, labels, stats, _ = cv2.connectedComponentsWithStats(
            self.mask, connectivity=4)

        idx, value = -1, 0
        for i, s in enumerate(stats[1:]):
            if s[4] > value:
                idx = i+1
                value = s[4]

        for cx, cy in [
                (0, 0), (0, row), (col, row), (col, 0)]:
            result.append(closest(labels, cx, cy, idx))
        return np.array(result, dtype=np.int32)


if __name__ == "__main__":
    img = plt.imread('test-data/hist.jpg', 3)
    coords = np.array([[326.3241, 373.75494],
                       [316.83795, 804.4269],
                       [734.22925, 794.94073],
                       [734.22925, 493.28064]], dtype=np.int32)
    finder = VertexFinder()

    finder.setup(img, coords)

    finder.set_mask(img)

    preview = img.copy()
    preview[finder.mask == 0] //= 2
    plt.figure()
    plt.imshow(preview)

    test_img = cv2.imread('test-data/hist_test2.jpg', -1)

    finder.set_mask(test_img)
    vertexes = finder.vertexes()

    test_img[finder.mask == 0] //= 2

    for center in vertexes:
        test_img = cv2.circle(test_img, center, 30, (255, 255, 200), -1)

    result = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    plt.figure()
    plt.imshow(result)
    plt.show()
