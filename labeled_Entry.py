from tkinter import *


class Labeled_Entry(Entry):

    def __init__(self, master=None, label="",  textg='black', **kwargs):
        Entry.__init__(self, master, **kwargs)
        self.label = label
        self.textg = textg
        self.on_exit()
        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)

    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, END)
            self.config(fg=self.textg)

    def on_exit(self,  event=None):
        if not self.get():
            self.config(fg='gray')
            self.insert(0, self.label)
