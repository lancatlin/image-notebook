from PIL import Image as PImage


def make_thumbnail(img, size):
    result = img.copy()
    result.thumbnail(size, PImage.NEAREST)
    return result


class Image:
    def __init__(self, filename):
        self.filename = filename
        self.origin = PImage.open(filename)
        self.product = self.origin
        self.width = self.origin.width
        self.height = self.origin.height

    def __str__(self):
        return self.filename.split('/')[-1]
