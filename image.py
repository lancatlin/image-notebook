import PIL


class Image:
    def __init__(self, filename):
        self.filename = filename
        self.origin = PIL.Image.open(filename)
        self.product = self.origin

    def __str__(self):
        return self.filename.split('/')[-1]
