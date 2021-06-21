import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import turtle
from frame import Frame
from canvas import ImageCanvas, DragableCanvas


class TransformFrame(Frame):
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
            controller=self.controller, master=canvas_ct)
        self.origin.grid(row=1, column=0)
        self.origin.set_callback(self.transform)

        product_label = tk.Label(canvas_ct, text='Product', font=('Arial', 25))
        product_label.grid(row=0, column=1)
        self.product = ImageCanvas(
            controller=self.controller, master=canvas_ct)
        self.product.grid(row=1, column=1)

        button_ct = tk.Frame(self)
        button_ct.pack(side=tk.BOTTOM)

        manage = tk.Button(
            button_ct, text='Manage',
            command=lambda: controller.switch_frame('ManageFrame'))
        manage.pack(side=tk.LEFT)

        learn = tk.Button(
            button_ct, text='Learn', command=self.origin.learn)
        learn.pack(side=tk.LEFT)

        auto = tk.Button(
            button_ct, text='Auto', command=self.origin.auto)
        auto.pack(side=tk.LEFT)

        reset_button = tk.Button(
            button_ct, text='Reset', command=self.origin.reset)
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

    def reset(self):
        self.current = 0

    def on_switch(self):
        print(id(self.current_image()))
        self.origin.show_image(self.current_image())
        self.product.show_image(self.current_image())

    def current_image(self):
        return self.controller.images[self.current]

    def move(self, direction=True):
        '''Move to the next image or previous image
        direction: True is next, False is previous
        '''
        if direction:
            self.current += 1
        else:
            self.current -= 1
        self.current %= len(self.controller.images)

        self.on_switch()

    def transform(self):
        coords = self.origin.get_coords()
        self.current_image().transform(coords)
        self.origin.show_image(self.current_image())
        self.product.show_image(self.current_image())

    def export(self):
        filename = asksaveasfilename(
            defaultextension='.pdf', filetypes=(('PDF Files', ('*.pdf',)),))
        if not filename:
            return
        images = [image.product for image in self.controller.images]
        images[0].save(filename, save_all=True, append_images=images[1:])
