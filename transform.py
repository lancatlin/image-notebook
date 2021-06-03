import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import turtle
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
            master=canvas_ct, width=self.controller.width // 2, height=self.controller.height, bg='black')
        self.origin.grid(row=1, column=0)
        self.origin.set_callback(self.transform)

        product_label = tk.Label(canvas_ct, text='Product', font=('Arial', 25))
        product_label.grid(row=0, column=1)
        self.product = tk.Label(
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

        export_button = tk.Button(
            button_ct, text='Export', command=self.export)
        export_button.pack(side=tk.LEFT)

    def show(self):
        self.current = 0
        self.show_image()

    def current_image(self):
        return self.controller.images[self.current]

    def show_image(self):
        if not self.controller.images:
            return

        image = self.current_image()
        size = self.image_size(image)
        width, height = size

        self.thumbnail = ImageTk.PhotoImage(make_thumbnail(image.origin, size))

        self.origin.config(width=width, height=height)
        self.origin.create_image(
            (0, 0), anchor=tk.NW, image=self.thumbnail)
        self.origin.draw_vertexes()

        self.show_product()

    def show_product(self):
        image = self.current_image()
        size = self.image_size(image)
        width, height = size
        self.product_thumbnail = ImageTk.PhotoImage(
            make_thumbnail(image.product, size))

        self.product.config(image=self.product_thumbnail,
                            width=width, height=height)

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

        self.show_image()

    def transform(self):
        coords = self.origin.get_coords()
        width, _ = self.image_size(self.current_image())
        self.current_image().transform(coords, width)
        self.show_product()

    def export(self):
        filename = asksaveasfilename(
            defaultextension='.pdf', filetypes=(('PDF Files', ('*.pdf',)),))
        print(filename)
        if not filename:
            return
        images = [image.product for image in self.controller.images]
        print(images)
        images[0].save(filename, save_all=True, append_images=images[1:])
