
import tkinter as tk
import os

class ToolButton(tk.Button):
    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)
        self.config(padx=2, pady=2)
        if 'imgfile' in keyargs.keys() and keyargs['imgfile'] is not None and os.path.isfile(keyargs['imgfile']):
            ph = tk.PhotoImage(file=keyargs['imgfile'])
            self.config(image=ph)
            self.image = ph

class ToolSeparator(tk.Frame):
    def __init__(self, imgfile=None, *args, **keyargs):
        super().__init__(*args, **keyargs)
        self.config(padx=4,pady=2)        
        frm = tk.Frame(master=self,bg="#B3B3B3", width=2, height=24)
        frm.pack(fill=tk.Y)

class Toolbar(tk.Frame):
    def __init__(self, *args, **keyargs):    
        super().__init__(*args, **keyargs)
        self.config(padx=1, pady=1)
    
    def add(self, control):
        control.config(master=self)
        control.master = self
    
    def insert_button(self, image=None, onclick=None):
        btn = ToolButton(master=self, imgfile=image, command=onclick, width=22,height=22)
        btn.pack(anchor=tk.NW,side=tk.LEFT)
        return btn
    
    def insert_separator(self):
        sep = ToolSeparator(master=self)
        sep.pack(anchor=tk.NW,side=tk.LEFT, fill=tk.Y)
        return sep
