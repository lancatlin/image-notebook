class Image:
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return self.filename.split('/')[-1]
