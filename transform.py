import tkinter as tk
import turtle
from PIL import Image, ImageTk


class TransformFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.margin = 10
        self.shape = (800, 800)
        self.grid_rowconfigure(3)
        self.grid_columnconfigure(2)
        self.selected = None

        origin_label = tk.Label(self, text='Origin', font=('Arial', 25))
        origin_label.grid(row=0, column=0)
        self.origin = tk.Canvas(
            self, width=self.controller.width // 2, height=self.controller.height, bg='black')
        self.origin.grid(row=1, column=0)

        product_label = tk.Label(self, text='Product', font=('Arial', 25))
        product_label.grid(row=0, column=1)
        self.product = tk.Canvas(
            self, width=self.controller.width // 2, height=self.controller.height, bg='black')
        self.product.grid(row=1, column=1)

        self.origin.tag_bind('vertex', '<Button-1>', self.on_click)
        self.origin.bind('<Motion>', self.on_motion)
        self.origin.bind('<ButtonRelease-1>', self.on_release)
        button = tk.Button(self, text='Manage',
                           command=lambda: controller.switch_frame('ManageFrame'))
        button.grid(row=2)
        self.show_image('test-data/2.jpg')

    def show_image(self, image_path):
        img = Image.open(image_path)
        width, height = self.image_size(img)

        img.thumbnail(self.image_size(img), Image.NEAREST)
        self.img = ImageTk.PhotoImage(img)

        self.origin.config(width=width, height=height)
        self.origin.create_image(
            (10, 10), anchor=tk.NW, image=self.img)

        self.product.config(width=width, height=height)
        self.product.create_image(
            (10, 10), anchor=tk.NW, image=self.img)

        self.r = r = 10
        self.vertexes = [
            self.origin.create_oval(
                x-r, y-r, x+r, y+r, fill='green', tags=('vertex'))
            for x, y in [
                (10, 10), (10, 500), (500, 500), (500, 10)
            ]
        ]
        return

    def on_click(self, event):
        print(event, event.x, event.y)
        self.selected = self.origin.find_closest(event.x, event.y)

    def on_motion(self, event):
        if self.selected:
            self.origin.coords(
                self.selected, (event.x-self.r, event.y-self.r, event.x + self.r, event.y + self.r))

    def on_release(self, event):
        self.selected = None

    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*self.margin) // 2
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
