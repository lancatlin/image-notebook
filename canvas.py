import tkinter as tk


def center(coords):
    return (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2


class DragableCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 15
        self.selected = None

        self.tag_bind('vertex', '<Button-1>', self.on_click)
        self.bind('<Motion>', self.on_motion)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def draw_vertexes(self):
        self.delete('vertex')
        r = self.r
        [
            self.create_oval(
                x-r, y-r, x+r, y+r, fill='green', tags=('vertex'))
            for x, y in [
                (10, 10), (10, 500), (500, 500), (500, 10)
            ]
        ]
        self.draw_lines()

    def draw_lines(self):
        coords = self.get_coords()
        coords.append(coords[0])
        self.delete('lines')
        self.create_line(*coords, tags=('lines',), fill='green')

    def get_coords(self):
        return [center(self.coords(vertex))
                for vertex in self.find_withtag('vertex')]

    def on_click(self, event):
        self.selected = self.find_closest(event.x, event.y)

    def on_motion(self, event):
        if self.selected:
            self.coords(
                self.selected, (event.x-self.r, event.y-self.r, event.x + self.r, event.y + self.r))
            self.draw_lines()

    def on_release(self, event):
        self.selected = None
        if self.callback:
            self.callback()
