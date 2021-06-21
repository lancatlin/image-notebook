import tkinter as tk
import numpy as np
from PIL import ImageTk
from styles import MARGIN
from image import Image
from PIL import Image as PImage
from vertexes import VertexFinder


def center(coords):
    return (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2


class ImageCanvas(tk.Canvas):
    def __init__(self, controller=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.image = None
        self.thumbnail = None
        self.image_to_show = 'product'

    def config_size(self, size):
        self.width, self.height = size
        self.config(width=self.width, height=self.height)

    def show_image(self, image):
        self.image = image
        size = self.image_size(image)
        self.config_size(size)

        self.make_thumbnail()

        self.create_image(
            (0, 0), anchor=tk.NW, image=self.thumbnail)

    def make_thumbnail(self):
        '''Make a thumbnail of an PIL image'''
        result = getattr(self.image, self.image_to_show).copy()
        result.thumbnail((self.width, self.height), PImage.NEAREST)
        self.thumbnail = ImageTk.PhotoImage(image=result)

    def image_size(self, image):
        if image.width > image.height:
            width = self.controller.width
            image_width = (width - 2*MARGIN) // 2
            image_height = int(image_width * (image.height / image.width))
            return image_width, image_height

        height = self.controller.height
        image_height = (height * 3) // 4
        image_width = int(image_height * (image.width / image.height))
        return image_width, image_height


class DragableCanvas(ImageCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 15
        self.selected = None
        self.image_to_show = 'origin'

        self.tag_bind('vertex', '<Button-1>', self.on_click)
        self.bind('<Motion>', self.on_motion)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.callback = None

        self.finder = VertexFinder()

    def switch_image(self, image):
        self.show_image(image)
        if image.coords is None and self.finder.learned:
            print('auto')
            self.auto()

    def show_image(self, image):
        self.finder.set_mask(image.array())
        super().show_image(image)
        self.draw_vertexes(self.image.coords)

    def make_thumbnail(self):
        '''Make a thumbnail of an PIL image'''
        result = self.image.with_mask(self.finder.mask)

        result.thumbnail((self.width, self.height), PImage.NEAREST)
        self.thumbnail = ImageTk.PhotoImage(image=result)

    def learn(self):
        '''Setup the vertex finder to use current img and coords'''
        self.finder.setup(self.image.array(), self.get_coords())
        print(self.finder.lowest)
        print(self.finder.highest)
        self.callback()

    def auto(self):
        self.transform(self.finder.vertexes(self.image.array()))

    def set_callback(self, callback):
        self.callback = callback

    def transform(self, coords=None):
        if coords is None:
            coords = self.get_coords()
        self.image.transform(coords.astype(np.float32))
        self.callback()

    def draw_vertexes(self, coords=None):
        self.delete('vertex')
        r = self.r
        if coords is None:
            coords = self.image.default_vertexes()

        coords = self.coords_transform(coords)
        [
            self.create_oval(
                x-r, y-r, x+r, y+r, fill='green', tags=('vertex'))
            for x, y in coords
        ]
        self.draw_lines()

    def coords_transform(self, coords):
        return coords * self.width / self.image.width

    def reset(self):
        self.image.reset()
        self.draw_vertexes()
        self.transform()

    def draw_lines(self):
        coords = self.get_coords()
        coords = self.coords_transform(coords).tolist()
        coords.append(coords[0])
        self.delete('lines')
        self.create_line(*coords, tags=('lines',), fill='green')

    def get_coords(self):
        coords = np.float32([center(self.coords(vertex))
                             for vertex in self.find_withtag('vertex')]) * self.image.width / self.width
        return coords

    def on_click(self, event):
        self.selected = self.find_closest(event.x, event.y)

    def on_motion(self, event):
        if self.selected:
            self.coords(
                self.selected, (event.x-self.r, event.y-self.r, event.x + self.r, event.y + self.r))
            self.draw_lines()

    def on_release(self, event):
        self.selected = None
        self.transform()
