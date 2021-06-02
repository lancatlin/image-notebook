import tkinter as tk
from welcome import WelcomeFrame
from transform import TransformFrame
from manage import ManageFrame


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

        self.switch_frame('TransformFrame')

    def switch_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def set_images(self, images):
        self.images = images
        print([str(image) for image in images])


if __name__ == "__main__":
    app = Application()
    app.wm_title('Image Notebook')
    app.mainloop()
