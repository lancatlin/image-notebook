import tkinter as tk
import turtle
import cv2
from PIL import ImageTk
from image import Image, make_thumbnail
from canvas import DragableCanvas


class TransformFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.margin = 10
        self.shape = (800, 800)
        self.current = 0

        canvas_ct = tk.Frame(self)
        canvas_ct.pack(side=tk.TOP)
        canvas_ct.grid_rowconfigure(2)
        canvas_ct.grid_columnconfigure(2)

        origin_label = tk.Label(canvas_ct, text='Origin', font=('Arial', 25))
        origin_label.grid(row=0, column=0)
        self.origin = DragableCanvas(
            canvas_ct, width=self.controller.width // 2, height=self.controller.height, bg='black')
        self.origin.grid(row=1, column=0)

        product_label = tk.Label(canvas_ct, text='Product', font=('Arial', 25))
        product_label.grid(row=0, column=1)
        self.product = tk.Canvas(
            canvas_ct, width=self.controller.width // 2, height=self.controller.height, bg='black')
        self.product.grid(row=1, column=1)

        button_ct = tk.Frame(self)
        button_ct.pack(side=tk.BOTTOM)

        manage = tk.Button(
            button_ct, text='Manage',
            command=lambda: controller.switch_frame('ManageFrame'))
        manage.pack(side=tk.LEFT)

        reset_button = tk.Button(
            button_ct, text='Reset', command=self.origin.draw_vertexes)
        reset_button.pack(side=tk.LEFT)

        previous_button = tk.Button(
            button_ct, text='Previous', command=lambda: self.move(False))
        previous_button.pack(side=tk.LEFT)

        next_button = tk.Button(button_ct, text='Next',
                                command=lambda: self.move(True))
        next_button.pack(side=tk.LEFT)

    def show(self):
        self.current = 0
        self.show_image(0)

    def show_image(self, index):
        if not self.controller.images:
            return

        image = self.controller.images[index]
        size = self.image_size(image)
        width, height = size

        self.thumbnail = ImageTk.PhotoImage(make_thumbnail(image.origin, size))

        self.origin.config(width=width, height=height)
        self.origin.create_image(
            (0, 0), anchor=tk.NW, image=self.thumbnail)
        self.origin.draw_vertexes()

        self.product.config(width=width, height=height)
        self.product.create_image(
            (0, 0), anchor=tk.NW, image=self.thumbnail)

    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*self.margin) // 2
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height

    def move(self, direction=True):
        '''Move to the next image or previous image
        direction: True is next, False is previous
        '''
        if direction:
            self.current += 1
        else:
            self.current -= 1
        self.current %= len(self.controller.images)

        self.show_image(self.current)
