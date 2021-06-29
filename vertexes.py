import cv2
import numpy as np
from matplotlib import pyplot as plt


def distance(x, y, cx, cy):
    return (x-cx)**2 + (y-cy)**2


def filter(img, threshold):
    '''Create the mask of img with respect to threshold
        @param img: An BGR color image
        @param threshold: An (3, 257) ndarray record the color threshold
    '''
    result = np.ones(img.shape[:2], dtype=np.uint8)
    for i, frame in enumerate(cv2.split(img)):
        result *= threshold[i][frame]
    return result


def closest(mask, cx, cy):
    '''Return the closest pixel to (cx, cy) on the mask which is 0'''
    nonzero = cv2.findNonZero((mask).astype(np.uint8))
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
        '''Setup the color threshold by the image and the coords
            @param img: An BGR image
            @param coords: An (4, 2) array contains the coords of the vertexes
        '''
        mask = np.ones(img.shape[:2], dtype=np.uint8)
        cv2.fillConvexPoly(mask, coords.astype(np.int32), 0)
        self.set_threshold(img, mask)
        self.learned = True

    def set_threshold(self, img, mask, threshold=0.001):
        '''Set the color threshold from an image which not on the mask
            @param img: An BGR image
            @param mask: An binary image
        '''
        row, col = img.shape[:2]
        plt.figure()
        self.threshold = np.zeros((3, 257), dtype=np.uint8)
        for i in range(3):
            histr = cv2.calcHist(
                images=[img], channels=[i], mask=mask, histSize=[257], ranges=[0, 256]
            ) / (row * col)

            self.threshold[i][histr[:, 0] > threshold] = 1

            plt.plot(histr, color=['b', 'g', 'r'][i])
            plt.plot(threshold * self.threshold[i], color=['b', 'g', 'r'][i])
            plt.xlim([0, 256])

    def set_mask(self, img):
        '''Compute the mask of the image by the threshold
        '''
        mask = 1-filter(img, self.threshold)
        kernel = np.ones([9, 9], dtype=np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

        _, labels, stats, _ = cv2.connectedComponentsWithStats(
            mask, connectivity=4)

        idx, value = -1, 0
        for i, s in enumerate(stats[1:]):  # use [1:] to omit 0
            if s[4] > value:
                idx = i+1
                value = s[4]

        self.mask = (labels == idx).astype(np.uint8)

    def vertexes(self):
        '''Get the vertexes by the color threshold
            return the closest points to the four corners'''
        row, col = self.mask.shape[:2]
        result = []

        for cx, cy in [
                (0, 0), (0, row), (col, row), (col, 0)]:
            result.append(closest(self.mask, cx, cy))
        return np.array(result, dtype=np.int32)


if __name__ == "__main__":
    img = cv2.imread('test-data/hist_test.jpg', -1)
    coords = np.array([[201.10672, 259.92096],
                       [185.92885, 656.4427],
                       [521.73914, 652.6482],
                       [536.917, 371.8577]], dtype=np.int32)
    finder = VertexFinder()

    finder.setup(img, coords)

    test_img = cv2.imread('test-data/hist_test2.jpg', 3)

    finder.set_mask(test_img)
    vertexes = finder.vertexes()

    test_img[finder.mask == 0] //= 2

    for center in vertexes:
        test_img = cv2.circle(test_img, center, 30, (255, 255, 200), -1)

    result = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    plt.figure()
    plt.imshow(result)
    plt.show()
