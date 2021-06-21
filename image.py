from PIL import Image as PImage
import numpy as np
import cv2


class Image:
    def __init__(self, filename):
        self.filename = filename
        self.name = filename.split('/')[-1]
        self.origin = PImage.open(filename)
        self.product = self.origin
        self.width = self.origin.width
        self.height = self.origin.height
        self.coords = None

    def default_vertexes(self):
        width = self.width
        height = self.height
        return np.array([
            (0, 0), (0, height),
            (width, height), (width, 0),
        ])

    def reset(self):
        self.coords = self.default_vertexes()

    def __str__(self):
        return self.filename.split('/')[-1]

    def array(self):
        return np.array(self.origin)

    def toPIL(self, img):
        return PImage.fromarray(img)

    def with_mask(self, mask):
        ''' mask the origin image '''
        img = self.array()
        img[mask == 0] = 0
        return self.toPIL(img)

    def transform(self, coords):
        ''' Transform the origin image to product
        @param
        coords: the coords picked from canvas
        @param
        '''
        self.coords = coords
        output = np.float32(
            [[0, 0], [0, self.height], [self.width, self.height], [self.width, 0]])
        img = self.array()
        M = cv2.getPerspectiveTransform(coords, output)
        result = cv2.warpPerspective(
            img, M, (self.width, self.height), flags=cv2.INTER_LINEAR)
        self.product = self.toPIL(result)
