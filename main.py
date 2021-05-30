import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(
            self, text='Hello World\nClick me',
            command=self.say_hi)
        self.hi_there.pack(side='top')

        self.quit_button = tk.Button(
            self, text='QUIT', command=self.master.destroy
        )
        self.quit_button.pack(side='bottom')

    def say_hi(self):
        print('Hello world')


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
