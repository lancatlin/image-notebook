import tkinter as tk
from tkinter.filedialog import askopenfilenames
from image import Image


class WelcomeFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        label = tk.Label(self, text='Welcome')
        label.pack()

        self.selected_files = tk.Label(self)
        self.selected_files.pack()

        select_button = tk.Button(
            self, text='Open', command=self.select_files)
        select_button.pack()

        manage_button = tk.Button(
            self, text='OK', command=lambda: self.controller.switch_frame('ManageFrame'))
        manage_button.pack()

    def select_files(self):
        filenames = askopenfilenames(
            title='Open Images',
            filetypes=(('Image Files', ('*.jpg', '*.png')), ('All', '*'))
        )
        if filenames:
            self.controller.set_images(
                [Image(filename) for filename in filenames])
            self.selected_files.config(text=f'Selected {len(filenames)} files')
