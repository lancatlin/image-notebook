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
                    master=self.image_frame,
                    controller=self.controller,
                    on_update=self.show,
                    on_pop=self.pop)
                image.grid(row=i//COLUMN, column=i % COLUMN)
                self.images.append(image)
        self.show()

    def show(self):
        for i, image in enumerate(self.images):
            image.set_image(i)

    def pop(self):
        image = self.images[-1]
        image.destroy()
        del self.images[-1]


class ImageFrame(tk.Frame):
    def __init__(self, master, controller, on_update, on_pop):
        super().__init__(master)
        self.controller = controller
        self.image = None
        self.grid_rowconfigure(3)
        self.grid_columnconfigure(1)
        self.index = None
        self.on_update = on_update
        self.on_pop = on_pop

        self.canvas = PreviewImage(
            controller=controller, master=self)
        self.canvas.grid(row=0, column=0)

        self.label = tk.Label(self, text='Image')
        self.label.grid(row=1, column=0)

        buttons = tk.Frame(self)
        buttons.grid(row=2)

        backward = tk.Button(
            buttons, text='<', command=lambda: self.switch(self.index-1))
        backward.pack(side=tk.LEFT)

        delete = tk.Button(buttons, text='X', command=self.delete)
        delete.pack(side=tk.LEFT)

        forward = tk.Button(buttons, text='>',
                            command=lambda: self.switch(self.index+1))
        forward.pack(side=tk.LEFT)

    def set_image(self, image_index):
        self.index = image_index
        image = self.controller.images[image_index]
        self.label.config(text=image.name)
        self.canvas.show_image(image)

    def switch(self, dest):
        images = self.controller.images
        images[self.index], images[dest] = images[dest], images[self.index]
        self.on_update()

    def delete(self):
        del self.controller.images[self.index]
        self.on_pop()
        self.on_update()


class PreviewImage(ImageCanvas):
    def image_size(self, image):
        width = self.controller.width
        image_width = (width - 2*MARGIN) // 4
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
