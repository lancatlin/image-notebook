import tkinter as tk


class DragableCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 10
        self.vertexes = []
        self.selected = None

        self.tag_bind('vertex', '<Button-1>', self.on_click)
        self.bind('<Motion>', self.on_motion)
        self.bind('<ButtonRelease-1>', self.on_release)

    def draw_vertexes(self):
        r = self.r
        self.vertexes = [
            self.create_oval(
                x-r, y-r, x+r, y+r, fill='green', tags=('vertex'))
            for x, y in [
                (10, 10), (10, 500), (500, 500), (500, 10)
            ]
        ]

    def on_click(self, event):
        print(event, event.x, event.y)
        self.selected = self.find_closest(event.x, event.y)

    def on_motion(self, event):
        if self.selected:
            self.coords(
                self.selected, (event.x-self.r, event.y-self.r, event.x + self.r, event.y + self.r))

    def on_release(self, event):
        self.selected = None
