import threading
import time

from utils.gui_utils import get_screen_size
import customtkinter as ck
from customtkinter import *
from tkinter import scrolledtext

from tkinter import filedialog as fd
import tkinter.ttk as ttk
import json

ck.set_appearance_mode("System")
ck.set_default_color_theme('blue')


class JsonReaderGui(threading.Thread):
    def __init__(self):
        super(JsonReaderGui, self).__init__()
        self.editor = None
        self.button_send = None
        self.option_menu = None
        self.text_num_1 = None
        self.frame1 = None
        self.frame2 = None
        self.json_name = None
        self.win = None
        self.corner_radius = 15
        # self.
        self.width, self.height = [v // 2 for v in get_screen_size()]
        self.bg_color = 'black'
        # for i in range(10):
        #     setattr(self, f'text_num_{i}', StringVar())
        self.a = 5
        self.start()

    def run(self) -> None:
        self.win = ck.CTk('JsonReaderGUI almubdieunTech')
        self.text_num_1 = ck.StringVar()

        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)

        self.win.geometry(f'{self.width}x{self.height}')
        self.win.title('JsonReaderGUI almubdieunTech')
        # self.win.resizable(False, False)
        self.frame1 = ck.CTkFrame(master=self.win, height=self.height - 20, width=self.width - 150,
                                  corner_radius=self.corner_radius,
                                  bg='#899499')
        self.frame1.grid(row=0, column=0, )
        font_tuple = ("Calibri", 12, "bold")
        self.editor = scrolledtext.ScrolledText(self.frame1, height=self.height - 80, width=self.width - 200,
                                                bg='#414a4c', fg='#FFFFFF', font=font_tuple)
        self.editor.grid(row=0, column=0)
        self.frame2 = CTkFrame(self.win, height=self.height - 20, corner_radius=self.corner_radius, width=120,
                               bg='#899499')
        self.frame2.grid(row=0, column=1)
        self.option_menu = CTkOptionMenu(master=self.frame2, height=30, width=110, corner_radius=self.corner_radius,
                                         values=["System", "Light", "Dark"],
                                         command=self.change_appearance_mode)
        self.option_menu.grid(row=0, column=0, padx=10, pady=50)
        self.button_send = ck.CTkButton(self.frame2, width=110, height=30, text_color='white', text='Open',
                                        corner_radius=self.corner_radius,
                                        highlightbackground='lightgray', command=self.openfile)
        self.button_send.grid(row=1, column=0, padx=10, pady=50)

        self.win.mainloop()
        self.win.update()
        self.win.update_idletasks()

    def openfile(self):
        filetypes = (
            ('json files', '*.json'),
            ('All files', '*.*')
        )
        self.json_name = fd.askopenfilename(filetypes=filetypes)

        print(self.json_name)
        with open(self.json_name, 'r') as r:
            data = json.load(r)
        self.editor.delete(1.0,END)
        self.editor.insert(INSERT, data)

    def change_appearance_mode(self, theme):
        ck.set_appearance_mode(theme)
        print('\033[1;36m Changing Appearance Mode ... ')


def main():
    gui = JsonReaderGui()


if __name__ == "__main__":
    main()
