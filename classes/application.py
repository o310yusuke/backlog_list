# coding: utf-8

import tkinter as tk
from tkinter import font

class Application(tk.Frame):
    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.master = master
        self.title = title
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title(self.title)
        
        # アプリタイトルのフォント設定
        font_title = font.Font(size=14, weight='bold', underline=1)
        label_title = tk.Label(
            self.master,
            text=self.title,
            font=font_title
        )
        label_title.pack(side='top')

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
root.geometry('400x300')
app = Application(master=root, title=u'Backlog期限切れチケット抽出ツール')
app.mainloop()
