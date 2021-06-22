import numpy as np

from vertexes import VertexFinder


class ImageController:
    def __init__(self, origin, product):
        self.image = None
        self.origin = origin
        self.origin.set_callback(self.set_coords)

        self.product = product
        self.coords = None
        self.aspect_ratio = 1

        self.finder = VertexFinder()

    def set_image(self, image):
        self.image = image
        self.finder.set_mask(self.image.array())
        self.image.aspect_ratio = self.aspect_ratio
        if image.coords is not None:
            self.coords = self.image.coords
        elif self.finder.learned:
            self.auto_detect_vertexes()
        else:
            self.coords = self.corners()
        self.update()

    def set_coords(self, coords):
        self.coords = coords
        self.update()

    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
        self.image.aspect_ratio = aspect_ratio
        self.update()

    def update(self):
        self.finder.set_mask(self.image.array())
        self.transform()
        origin = self.image.with_mask(self.finder.mask)
        self.origin.show_image(origin, self.coords)
        self.product.show_image(self.image.product)

    def learn(self):
        '''Setup the vertex finder to use current img and coords'''
        self.finder.setup(self.image.array(), self.coords)
        self.update()

    def auto_detect_vertexes(self):
        self.coords = self.finder.vertexes()

    def auto_command(self):
        self.auto_detect_vertexes()
        self.update()

    def transform(self):
        self.image.transform(self.coords.astype(np.float32))

    def reset(self):
        self.finder.reset()
        self.coords = self.corners()
        self.update()

    def corners(self):
        width = self.image.width
        height = self.image.height
        return np.array([
            (0, 0), (0, height),
            (width, height), (width, 0),
        ])
