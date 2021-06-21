import os
import tkinter as tk

from welcome import WelcomeFrame
from transform import TransformFrame
from manage import ManageFrame
from image import Image


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 1600
        self.height = 900
        self.geometry(f'{self.width}x{self.height}')
        container = tk.Frame(self)
        container.pack(fill='both', expand=True, side='top')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.images = []
        self.frames = {}
        for F in (WelcomeFrame, ManageFrame, TransformFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.switch_frame('WelcomeFrame')

    def switch_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        frame.on_switch()

    def set_images(self, images):
        '''Being called by welcome frame'''
        self.images = images


if __name__ == "__main__":
    app = Application()
    app.set_images([
        Image('test-data/train.jpg'),
        Image('test-data/test.jpg'),
        # Image(os.path.join('test-data', f)) for f in os.listdir('test-data')
    ])
    app.switch_frame('TransformFrame')
    app.wm_title('Image Notebook')
    app.mainloop()
