import tkinter as tk
import turtle
from PIL import Image, ImageTk


class TransformFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.shape = (800, 600)
        self.canvas = tk.Canvas(
            self.master, width=self.shape[0], height=self.shape[1])
        self.canvas.pack(anchor=tk.NW)

    def show_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail(self.shape, Image.NEAREST)
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(
            (0, 0), anchor=tk.NW, image=self.img)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x1200')
    app = TransformFrame(root)
    app.show_image('test-data/3.png')
    root.mainloop()
