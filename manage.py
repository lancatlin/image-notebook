import tkinter as tk
from canvas import ImageCanvas
from styles import MARGIN


class ManageFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        label = tk.Label(self, text='Manage')
        label.pack()
        button = tk.Button(self, text='Transform',
                           command=lambda: controller.switch_frame('TransformFrame'))
        button.pack()

    def show(self):
        image1 = ImageFrame(self, self.controller, self.controller.images[0])
        image1.pack()


class ImageFrame(tk.Frame):
    def __init__(self, master, controller, image):
        super().__init__(master)
        self.master = master
        self.image = image
        self.grid_rowconfigure(3)
        self.grid_columnconfigure(1)

        label = tk.Label(self, text='Image')
        label.grid(row=0, column=0)

        self.canvas = PreviewImage(
            controller=controller, master=self)
        self.canvas.grid(row=1, column=0)
        self.canvas.show_image(self.image)

        buttons = tk.Frame(self)
        buttons.grid(row=2)

        backward = tk.Button(buttons, text='<')
        backward.pack(side=tk.LEFT)

        delete = tk.Button(buttons, text='X')
        delete.pack(side=tk.LEFT)

        forward = tk.Button(buttons, text='>')
        forward.pack(side=tk.LEFT)


class PreviewImage(ImageCanvas):
    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*MARGIN) // 4
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
