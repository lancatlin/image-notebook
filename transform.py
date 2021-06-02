import tkinter as tk
import turtle
from PIL import Image, ImageTk
from canvas import DragableCanvas


class TransformFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.margin = 10
        self.shape = (800, 800)

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

        previous_button = tk.Button(button_ct, text='Previous')
        previous_button.pack(side=tk.LEFT)

        next_button = tk.Button(button_ct, text='Next')
        next_button.pack(side=tk.LEFT)

        self.show_image('test-data/2.jpg')

    def show_image(self, image_path):
        img = Image.open(image_path)
        width, height = self.image_size(img)

        img.thumbnail(self.image_size(img), Image.NEAREST)
        self.img = ImageTk.PhotoImage(img)

        self.origin.config(width=width, height=height)
        self.origin.create_image(
            (0, 0), anchor=tk.NW, image=self.img)
        self.origin.draw_vertexes()

        self.product.config(width=width, height=height)
        self.product.create_image(
            (0, 0), anchor=tk.NW, image=self.img)

    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*self.margin) // 2
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
