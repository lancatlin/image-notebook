import tkinter as tk
import turtle
from PIL import Image, ImageTk


class TransformFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.shape = (800, 600)
        self.canvas = tk.Canvas(
            self, width=self.shape[0], height=self.shape[1])
        self.canvas.pack(anchor=tk.NW)
        self.bind('<1>', self.on_click)
        button = tk.Button(self, text='Manage',
                           command=lambda: controller.switch_frame('ManageFrame'))
        button.pack()
        self.show_image('test-data/2.jpg')

    def show_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail(self.shape, Image.NEAREST)
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(
            (10, 10), anchor=tk.NW, image=self.img)
        self.circle = self.canvas.create_oval(10, 10, 30, 30)

    def on_click(self, event):
        print(event)
        self.canvas.coords(self.circle, event.x, event.y,
                           event.x + 20, event.y + 20)
