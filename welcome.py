import tkinter as tk


class WelcomeFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        label = tk.Label(self, text='Welcome')
        label.pack()

        button = tk.Button(self, text='Create',
                           command=lambda: controller.switch_frame('ManageFrame'))
        button.pack()
