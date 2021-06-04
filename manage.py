import tkinter as tk
from scrollable_frame import ScrollableFrame
from canvas import ImageCanvas
from styles import MARGIN
from frame import Frame


COLUMN = 4


class ManageFrame(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        label = tk.Label(self, text='Manage')
        label.pack()
        button = tk.Button(self, text='Transform',
                           command=lambda: controller.switch_frame('TransformFrame'))
        button.pack()
        image_frame = ScrollableFrame(self)
        image_frame.pack(fill='both', expand=True)
        image_frame.scrollable_frame.grid_columnconfigure(COLUMN)

        self.image_frame = image_frame.scrollable_frame
        self.images = []

    def on_switch(self):
        if not self.images:
            for i in range(len(self.controller.images)):
                image = ImageFrame(
                    self.image_frame, self.controller)
                image.grid(row=i//COLUMN, column=i % COLUMN)
                self.images.append(image)
        self.show()

    def show(self):
        for i, image in enumerate(self.images):
            image.set_image(i)


class ImageFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.image = None
        self.grid_rowconfigure(3)
        self.grid_columnconfigure(1)

        self.canvas = PreviewImage(
            controller=controller, master=self)
        self.canvas.grid(row=0, column=0)

        self.label = tk.Label(self, text='Image')
        self.label.grid(row=1, column=0)

        buttons = tk.Frame(self)
        buttons.grid(row=2)

        backward = tk.Button(buttons, text='<')
        backward.pack(side=tk.LEFT)

        delete = tk.Button(buttons, text='X')
        delete.pack(side=tk.LEFT)

        forward = tk.Button(buttons, text='>')
        forward.pack(side=tk.LEFT)

    def set_image(self, image_index):
        image = self.controller.images[image_index]
        self.label.config(text=image.name)
        self.canvas.show_image(image)


class PreviewImage(ImageCanvas):
    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*MARGIN) // 4
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
