"""Module containing classes for the Aware GUI"""

import tkinter.ttk as ttk
from tkinter import *


class MainWindow:
    def __init__(self, _root, tab_names):
        self.root = _root
        self.root.title("Aware")
        self.root.minsize(300, 300)
        self.window = Toplevel(self.root)
        self.weight_cells()
        self.tab_names = tab_names
        self.notebook = self.create_notebook()

    def weight_cells(self):
        for increment in range(30):
            self.window.rowconfigure(increment, weight=1)
            self.window.columnconfigure(increment, weight=1)

    def create_notebook(self):
        notebook = ttk.Notebook(master=self.window)
        for tab in self.tab_names:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=tab)
        notebook.grid(column=0, row=1, columnspan=1, rowspan=1, sticky=NSEW)
        return notebook


class InitialWindow:
    """Class for the window containing the initialisation information and setup info"""
    def __init__(self, _root):
        self.root = _root
        self.create_initialisation_frame()

    def create_initialisation_frame(self):
        i_frame = ttk.Frame(self.root)
        label = ttk.Label(i_frame)
        label.config(text="Initialising...")
        button = ttk.Button(i_frame)
        button.config(text="Press to continue")
        i_frame.grid(row=0, column=0, rowspan=10, columnspan=10)
        label.grid(row=0, column=0, rowspan=10, columnspan=10)
        return i_frame


class GUI:
    def __init__(self):
        self.root = Tk()
        self.iw = InitialWindow(self.root)
        self.mw = self.get_main()
        self.root.mainloop()

    def get_main(self):
        self.iw.destroy()
        mw = MainWindow(self.root, tabs)
        return mw


tabs = ["Structures", "Architecture", "Mechanical", "Electrical", "Facades", "Civil", "Geotechnical"]

if __name__ == "__main__":
    gui = GUI()

