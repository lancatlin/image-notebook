import tkinter as tk
from tkinter.filedialog import askopenfilenames

from scrollable_frame import ScrollableFrame
from canvas import ImageCanvas
import styles
from frame import Frame
from image import Image


COLUMN = 4


class ManageFrame(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        label = tk.Label(self, text='Image Notebook', font=styles.TITLE)
        label.pack()
        bt_frame = tk.Frame(self)
        bt_frame.pack()

        open_bt = tk.Button(
            bt_frame, text='Open Files', command=self.select_files)
        open_bt.pack(side=tk.LEFT)

        transform = tk.Button(bt_frame, text='Transform',
                              command=lambda: controller.switch_frame('TransformFrame'))
        transform.pack(side=tk.LEFT)
        image_frame = ScrollableFrame(self)
        image_frame.pack(fill='both', expand=True)
        image_frame.scrollable_frame.grid_columnconfigure(COLUMN)

        self.image_frame = image_frame.scrollable_frame
        self.images = []

    def select_files(self):
        '''Open a dialog to open files from os'''
        filenames = askopenfilenames(
            title='Open Images',
            filetypes=(('Image Files', ('*.jpg', '*.png')), ('All', '*'))
        )
        if filenames:
            images = [Image(filename)
                      for filename in filenames]
            self.controller.images += images
            self.append_images(len(images))

    def append_images(self, num):
        '''Append num of ImageFrame'''
        for i in range(len(self.images), len(self.images)+num):
            image = ImageFrame(
                master=self.image_frame,
                controller=self.controller,
                on_update=self.show,
                on_pop=self.pop)
            image.grid(row=i//COLUMN, column=i % COLUMN)
            self.images.append(image)
        self.show()

    def on_switch(self):
        self.show()

    def show(self):
        '''Set the images to show'''
        for i, image in enumerate(self.images):
            image.set_image(i)

    def pop(self):
        '''Remove one ImageFrame from the button'''
        image = self.images[-1]
        image.destroy()
        del self.images[-1]


class ImageFrame(tk.Frame):
    '''Frame that display an image and controlling buttons'''

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
        '''Set the image to display'''
        self.index = image_index
        image = self.controller.images[image_index]
        self.label.config(text=image.name)
        self.canvas.show_image(image.product)

    def switch(self, dest):
        '''Switch the image with dest'''
        images = self.controller.images
        images[self.index], images[dest] = images[dest], images[self.index]
        self.on_update()

    def delete(self):
        '''Delete the image'''
        del self.controller.images[self.index]
        self.on_pop()
        self.on_update()


class PreviewImage(ImageCanvas):
    '''Display the preview image'''

    def image_size(self, image):
        '''Set the size of preview image'''
        width = self.controller.width
        image_width = (width - 2*styles.MARGIN) // 4
        image_height = int(image_width * (image.height / image.width))
        return image_width, image_height
