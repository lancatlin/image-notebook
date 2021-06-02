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

        self.bind('<1>', self.on_click)
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
        self.circle = self.origin.create_oval(10, 10, 30, 30)

    def on_click(self, event):
        print(event, event.x, event.y)
        self.origin.coords(self.circle, event.x, event.y,
                           event.x + 20, event.y + 20)

    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*self.margin) // 2
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
