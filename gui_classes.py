"""Module containing classes for the Aware GUI"""

import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog as fd
import os
from settings import *


class UpdateInterface:
    def __init__(self, _root):
        self.master = _root
        self.create_frame()

    def create_frame(self):
        frame = ttk.Frame(self.master)
        frame.config(borderwidth=10)
        label = ttk.Label(frame)
        label.config(text="Update", font=("Bold", 14))
        label.config(anchor=CENTER, font="Underline")  # Underline doesn't seem to be working :/
        label.grid(column=1, row=1, columnspan=2, rowspan=1, pady=20)

        project_folder_button = ttk.Button(frame)
        project_folder_button.config(text="Set project folder")
        project_folder_button.config(command=set_project_folder)
        project_folder_button.grid(column=1, row=2, columnspan=2, rowspan=1)

        save_settings_button = ttk.Button(frame)
        save_settings_button.config(text="Save settings")
        save_settings_button.config(command=save_settings)
        save_settings_button.grid(column=1, row=3, columnspan=2, rowspan=1)

        load_settings_button = ttk.Button(frame)
        load_settings_button.config(text="Load settings")
        load_settings_button.config(command=load_settings_file)
        load_settings_button.grid(column=1, row=4, columnspan=2, rowspan=1)

        update_button = ttk.Button(frame)
        update_button.config(text="Update drawing folders")
        update_button.grid(column=1, row=5, columnspan=2, rowspan=4, pady=20)

        frame.grid(column=1, row=1, columnspan=1, rowspan=1)


class DisciplineInterface:
    def __init__(self, _root, tab_names):
        self.master = _root
        self.master.title("Aware")
        self.master.minsize(650, 300)
        self.weight_cells()
        self.tab_names = tab_names
        self.notebook = self.create_notebook()

    @staticmethod
    def get_folder_path():
        directory = fd.askdirectory()
        return directory

    def weight_cells(self):
        for increment in range(30):
            self.master.rowconfigure(increment, weight=1)
            self.master.columnconfigure(increment, weight=1)

    @staticmethod
    def create_tab_content(tab):
        """Use function to populate tabs with the necessary content"""
        # Things that tabs need to have:
        # TODO: Radio button to activate discipline
        # TODO: Text field for drawing prefix
        # TODO: FD button for source folder
        # TODO: FD button for destination folder
        # TODO: FD button for superseded folder
        # TODO: Checklist for tile types that can be accepted

        # Just realised that each tab needs to instantiate the DisciplineSetting object for it's Discipline to
        # capture the setting data

        activate = BooleanVar()

        check_button = ttk.Checkbutton(tab)
        check_button.config(text="Active?")
        check_button.config(variable=activate)  # Activate is now associated with the
        check_button.grid(column=1, row=1, columnspan=1, rowspan=1, pady=20, padx=10)

        prefix_label = ttk.Label(tab)
        prefix_label.config(text="Specify Drawing Prefix", anchor=E)
        prefix_label.grid(column=1, row=2, columnspan=3, rowspan=1)
        drawing_prefix_field = ttk.Entry(tab)
        drawing_prefix_field.grid(column=1, row=3, columnspan=3, rowspan=1, padx=10, pady=5)

        source_button = ttk.Button(tab)
        source_button.config(text="Set Source Folder")
        source_button.grid(column=1, row=4, columnspan=1, rowspan=2, padx=10, pady=25)

        destination_button = ttk.Button(tab)
        destination_button.config(text="Set Destination Folder")
        destination_button.grid(column=1, row=5, columnspan=1, rowspan=2, padx=10, pady=20)

        superseded_button = ttk.Button(tab)
        superseded_button.config(text="Set Superseded Folder")
        superseded_button.grid(column=1, row=6, columnspan=3, rowspan=2, padx=10, pady=20)

        print(tab.children)

    def create_notebook(self):
        notebook = ttk.Notebook(master=self.master)
        for tab in self.tab_names:
            frame = ttk.Frame(notebook)
            self.create_tab_content(frame)
            notebook.add(frame, text=tab)
        notebook.grid(column=2, row=1, columnspan=1, rowspan=1, sticky=NSEW)
        return notebook

# Need a method for capturing the content of many different save/load file buttons at once.
# I think the best way to do this might be a decorator pattern
# Let me refresh my memory about how this patter works


def grab_discipline_settings(notebook, tab_names):
    """Function for capturing the current state of discipline settings.  To be used when settings are saved,
    or the update function is run"""
    for tname in tab_names:
        tab = notebook.children[tname]
        active_button = tab.children[]

def save_settings():
    global project_folder_path, settings_file_path
    try:
        settings_file_path = create_settings_file_path(project_folder_path)
        create_setting_file(settings, settings_file_path)
    except NameError:
        print("Please ensure you have selected a project folder before saving your settings.")


def load_settings_file():
    global settings_file_path
    settings_file_path = fd.askopenfilename()
    load_discipline_settings_file(settings_file_path)


def set_project_folder():
    global project_folder_path
    project_folder_path = fd.askdirectory()
    folder_name = extract_folder_name(project_folder_path)
    project_folder_path = get_project_folder_path(folder_name)
    create_project_data_folder(project_folder_path)


settings = Settings("C:/Users/josh.finnin/Desktop/ACU")

tabs = ["Structures", "Architecture", "Mechanical", "Electrical", "Hydraulic", "Fire", "Facades", "Civil", "Geotechnical"]

if __name__ == "__main__":
    if not os.path.exists(PROJECT_DATA_FOLDER):
        os.makedirs(PROJECT_DATA_FOLDER)
    root = Tk()
    update_frame = UpdateInterface(root)
    discipline_frame = DisciplineInterface(root, tabs)
    root.mainloop()

