from PIL import Image as PImage
import numpy as np
import cv2


class Image:
    '''Image hold the information of an image'''

    def __init__(self, filename):
        self.filename = filename
        self.name = filename.split('/')[-1]
        self.origin = PImage.open(filename)
        self.product = self.origin
        self.width = self.origin.width
        self.height = self.origin.height
        self.aspect_ratio = 4/3  # self.width / self.height
        self.coords = None

    def __str__(self):
        return self.filename.split('/')[-1]

    def array(self):
        return np.array(self.origin)

    def toPIL(self, img):
        return PImage.fromarray(img)

    def with_mask(self, mask):
        '''mask the origin image '''
        img = self.array()
        img[mask == 0] //= 2
        return self.toPIL(img)

    def transform(self, coords):
        ''' Transform the origin image to product
            @param coords: the coords picked from canvas
        '''
        self.coords = coords
        w, h = self.output_shape()
        output = np.float32(
            [[0, 0], [0, h], [w, h], [w, 0]])
        img = self.array()
        M = cv2.getPerspectiveTransform(coords, output)
        result = cv2.warpPerspective(
            img, M, self.output_shape(), flags=cv2.INTER_LINEAR)
        self.product = self.toPIL(result)

    def output_shape(self):
        return int(self.height * self.aspect_ratio), self.height
