import tkinter as tk


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
