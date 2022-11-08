import json
import threading
import tkinter
from tkinter import *
import cv2 as cv
from PIL import ImageTk, Image

px = []
py = []


def on_mouse(event):
    px.append(event.x)
    py.append(event.y)
    return px, py


class AppMouseCr(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print('\033[1;36m init Class ...')
        self.image_merge = None
        self.image_tkinter = None
        self.win = None
        self.im = None
        self.data = {}
        self.img_size = 1050
        self.img = None
        self.my_canvas = None
        self.color_index = 1
        self.c = 0
        self.colors = [
            'cyan',
            'blue',
            'red',
            'pink',
            'green',
            'yellow',
            'purple',
            'white'
        ]

        self.name = 'lol.json'
        self.start()

    def callback(self):
        self.win.quit()

    @classmethod
    def create_circle(cls, x, y, r, canvas_name, color: str = 'black'):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas_name.create_oval(x0, y0, x1, y1, fill=color)

    def change_color(self, event):
        if self.color_index == len(self.colors) - 1:
            self.color_index = 0
        else:
            self.color_index += 1
        return 0 if self.color_index == len(self.colors) - 1 else self.color_index + 1

    def run(self):

        self.win = tkinter.Tk(className='almubdieuntech')
        self.win.geometry(f"{self.img_size}x{self.img_size}")
        container = tkinter.Frame(self.win, width=self.img_size, height=self.img_size)
        container.pack()
        container.place(anchor='center', relx=0.5, rely=0.5)
        if self.c == 0:
            self.img = cv.resize(cv.imread('dot.jpg'), (self.img_size, self.img_size))

            blue, green, red = cv.split(self.img)
            self.image_merge = cv.merge((red, green, blue))
            self.c = 1
        self.my_canvas = Canvas(self.win, height=self.img_size, width=self.img_size)

        self.my_canvas.pack()
        self.im = Image.fromarray(self.image_merge)
        self.image_tkinter = ImageTk.PhotoImage(image=self.im)
        self.my_canvas.move(self.my_canvas.create_image(self.img_size, self.img_size, image=self.image_tkinter),
                            -int(self.img_size / 2), -int(self.img_size / 2))
        # label = tkinter.Label(container, image=self.image_tkinter)
        # label.pack()
        self.win.bind('<Button-1>', on_mouse)
        self.win.bind('<Button-3>', self.change_color)

        self.win.mainloop()

    def change(self, in_px, in_py):

        self.image_merge[in_px[len(in_px) - 1], in_py[len(in_py) - 1]]

        if not f"{len(in_px)}" in self.data:
            self.data[f"{len(in_px)}"] = {
                'x': in_px[len(in_px) - 1],
                'y': in_py[len(in_py) - 1],
                'level': self.colors[self.color_index]
            }

        self.create_circle(in_px[len(in_px) - 1], in_py[len(in_py) - 1], 5, self.my_canvas,
                           color=self.colors[self.color_index])
        print(len(in_px))
        if len(in_px) % 2 == 0:
            with open(self.name, 'w') as w:
                json.dump(self.data, w)

        print(self.colors[self.color_index])
        self.win.update()
        self.win.update_idletasks()


if __name__ == "__main__":
    app = AppMouseCr()
    while True:
        if len(px) > 0:
            app.change(px, py)
