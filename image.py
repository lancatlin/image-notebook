from PIL import Image as PImage
import numpy as np
import cv2


class Image:
    def __init__(self, filename):
        self.filename = filename
        self.origin = PImage.open(filename)
        self.product = self.origin
        self.width = self.origin.width
        self.height = self.origin.height
        self.coords = []

    def __str__(self):
        return self.filename.split('/')[-1]

    def transform(self, coords, thumbnail_width):
        ''' Transform the origin image to product
        @param
        coords: the coords picked from canvas
        @param
        '''
        self.coords = coords
        coords = np.float32(coords) / thumbnail_width * self.width
        output = np.float32(
            [[0, 0], [0, self.height], [self.width, self.height], [self.width, 0]])
        img = np.array(self.origin)
        M = cv2.getPerspectiveTransform(coords, output)
        result = cv2.warpPerspective(
            img, M, (self.width, self.height), flags=cv2.INTER_LINEAR)
        self.product = PImage.fromarray(result)
