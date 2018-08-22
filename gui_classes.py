"""Module containing classes for the Aware GUI"""

import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog as fd
from settings import *
from update_functions import *

PROJECT_FOLDER_PATH = None
SETTINGS_FILE_PATH = None
DISCIPLINE_SETTINGS = {}
DISCIPLINE_COUNT = 0
DISCIPLINE_FRAME = None


class UpdateInterface:
    def __init__(self, _root):
        self.master = _root
        self.create_frame()

    def create_frame(self):
        frame = ttk.Frame(self.master)
        frame.config(borderwidth=15)
        label = Label(frame)
        label.config(text="Updates", font=('Helvetica', 14, 'bold'))
        label.config(anchor=CENTER)
        label.place(x=0, y=0, width=80, height=40)

        project_folder_button = ttk.Button(frame)
        project_folder_button.config(text="Set project folder")
        project_folder_button.config(command=set_project_folder)
        project_folder_button.place(x=0, y=100)
        project_folder_label = Label(frame)
        project_folder_label.config(text="Please select a J drive project folder", font=("Helvetica", 10))
        project_folder_label.place(x=0, y=75)

        settings_label = Label(frame)
        settings_label.config(text="Settings files", font=("Helvetica", 10))
        settings_label.place(x=0, y=155)
        save_settings_button = ttk.Button(frame)
        save_settings_button.config(text="Save settings")
        save_settings_button.config(command=save_settings)
        save_settings_button.place(x=0, y=180)
        load_settings_button = ttk.Button(frame)
        load_settings_button.config(text="Load settings")
        load_settings_button.config(command=load_settings_file)
        load_settings_button.place(x=0, y=205)

        update_label = Label(frame)
        update_label.config(text="Update drawing folders", font=("Helvetica", 10))
        update_label.place(x=0, y=265)
        update_button = ttk.Button(frame)
        update_button.config(text="Update", command=update_drawings)
        update_button.place(x=0, y=290)

        frame.place(x=0, y=0, width=250, height=500)


class DisciplineInterface:
    def __init__(self, _root, tab_names):
        self.master = _root
        self.master.title("Aware")
        self.master.minsize(1000, 570)
        self.weight_cells()
        self.tab_names = tab_names
        self.tab_dict = {}
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

        activate = BooleanVar()

        check_button = ttk.Checkbutton(tab)
        check_button.config(text="Activate discipline?")
        check_button.config(variable=activate)
        check_button.place(x=20, y=20)
        check_button.var = activate

        prefix_label = Label(tab)
        prefix_label.config(text="Drawing Prefix:", font=("Helvetica", 10, "bold"))
        prefix_label.place(x=20, y=60)
        drawing_prefix_field = ttk.Entry(tab)
        drawing_prefix_field.place(x=130, y=60)
        prefix_description = Label(tab)
        prefix_description.config(text="(i.e. for drawing \'S-01-100\', the prefix would be \'S\')",
                                  font=("Helvetica", 10))
        prefix_description.place(x=20, y=85)

        # TODO: Add delimiter for splitting revision number from drawing name
        delimiter_label = Label(tab)
        delimiter_label.config(text="Revision Delimiter:", font=("Helvetica", 10, "bold"))
        delimiter_label.place(x=20, y=125)
        delimiter_field = ttk.Entry(tab)
        delimiter_field.place(x=150, y=125)
        delimiter_description = Label(tab)
        delimiter_description.config(text="(i.e. for drawing \'S-01-100[T01]\', the delimiter would be \'[\')",
                                     font=("Helvetica", 10))
        delimiter_description.place(x=20, y=150)

        folder_label = Label(tab)
        folder_label.config(text="Folders:", font=("Helvetica", 10, "bold"))
        folder_label.place(x=20, y=195)

        source_button = ttk.Button(tab)
        source_button.config(text="Set Source Folder")
        source_button.place(x=20, y=220)
        source_button_description = Label(tab)
        source_button_description.config(text="Folder to search for current drawings", font=("Helvetica", 10, "italic"))
        source_button_description.place(x=170, y=220)
        tab.src_folder = StringVar()
        wrap_folder_button(source_button, source_button_description, activate, tab.src_folder, set_folder)

        destination_button = ttk.Button(tab)
        destination_button.config(text="Set Destination Folder")
        destination_button.place(x=20, y=250)
        destination_button_description = Label(tab)
        destination_button_description.config(text="Folder to store current drawings", font=("Helvetica", 10, "italic"))
        destination_button_description.place(x=170, y=250)
        tab.dst_folder = StringVar()
        wrap_folder_button(destination_button, destination_button_description, activate, tab.dst_folder, set_folder)

        superseded_button = ttk.Button(tab)
        superseded_button.config(text="Set Superseded Folder")
        superseded_button.place(x=20, y=280)
        superseded_button_description = Label(tab)
        superseded_button_description.config(text="Folder to send superseded drawings", font=("Helvetica", 10, "italic"))
        superseded_button_description.place(x=170, y=280)
        tab.ss_folder = StringVar()
        wrap_folder_button(superseded_button, superseded_button_description, activate, tab.ss_folder, set_folder)

        file_types_label = Label(tab)
        file_types_label.config(text="File types to update:", font=("Helvetica", 10, "bold"))
        file_types_label.place(x=20, y=335)

        tab.pdf_bool = BooleanVar()
        cb_pdf = ttk.Checkbutton(tab)
        cb_pdf.config(text="PDF", variable=tab.pdf_bool)
        cb_pdf.place(x=30, y=360)

        tab.ifc_bool = BooleanVar()
        cb_ifc = ttk.Checkbutton(tab)
        cb_ifc.config(text="IFC", variable=tab.ifc_bool)
        cb_ifc.place(x=30, y=385)

        tab.dxf_bool = BooleanVar()
        cb_dxf = ttk.Checkbutton(tab)
        cb_dxf.config(text="DXF", variable=tab.dxf_bool)
        cb_dxf.place(x=30, y=410)

        tab.dwg_bool = BooleanVar()
        cb_dwg = ttk.Checkbutton(tab)
        cb_dwg.config(text="DWG", variable=tab.dwg_bool)
        cb_dwg.place(x=30, y=435)

        tab.jpeg_bool = BooleanVar()
        cb_jpeg = ttk.Checkbutton(tab)
        cb_jpeg.config(text="JPEG", variable=tab.jpeg_bool)
        cb_jpeg.place(x=30, y=460)

        tab.rhino_bool = BooleanVar()
        cb_3dm = ttk.Checkbutton(tab)
        cb_3dm.config(text="3DM", variable=tab.rhino_bool)
        cb_3dm.place(x=30, y=485)

    def create_notebook(self):
        notebook = ttk.Notebook(master=self.master)
        for tab in self.tab_names:
            frame = ttk.Frame(notebook)
            self.create_tab_content(frame)
            notebook.add(frame, text=tab)
            self.tab_dict[tab] = frame
        notebook.place(x=250, y=20, height=550, width=1200)
        return notebook


def grab_discipline_settings(notebook, tab_names):
    """Function for capturing the current state of discipline settings.
    To be used when settings are saved, or the update function is run"""
    for t_name in tab_names:
        # Update to access the variables from each discipline to create the DisciplineSetting objects
        # This function needs to be implemented by both the update button and the save settings button
        tab = notebook.tab_dict[t_name]
        active_button = tab.children['!checkbutton']
        active = active_button.var
        if active:

            prefix_raw = tab.children['!entry'].get()
            prefix = prefix_raw.strip()

            delimiter_raw = tab.children['!entry2'].get()
            delimiter = delimiter_raw.strip()

            d_setting = DISCIPLINE_SETTINGS[t_name]
            d_setting.prefix = prefix  # Set prefix
            if delimiter != "":
                d_setting.delimiter = delimiter  # Set delimiter
            else:
                d_setting.delimiter = ""

            d_setting.src_folder = tab.src_folder.get()
            d_setting.dst_folder = tab.dst_folder.get()
            d_setting.ss_folder = tab.ss_folder.get()

            file_types = []

            pdf_checked = tab.pdf_bool.get()
            if pdf_checked:
                file_types.append('.pdf')

            ifc_checked = tab.ifc_bool.get()
            if ifc_checked:
                file_types.append('.ifc')

            dxf_checked = tab.dxf_bool.get()
            if dxf_checked:
                file_types.append('.dxf')

            dwg_checked = tab.dwg_bool.get()
            if dwg_checked:
                file_types.append('.dwg')

            jpeg_checked = tab.jpeg_bool.get()
            if jpeg_checked:
                file_types.append('.jpeg')

            rhino_checked = tab.rhino_bool.get()
            if rhino_checked:
                file_types.append('.3dm')

            d_setting.file_types = file_types


def count_active_disciplines(tabs):
    pass


def wrap_folder_button(button, label, active, variable, command):

    def inner():
        result = command(label, active)
        variable.set(result)
        return result

    button["command"] = inner


def lookup_discipline_name(frame_name):
    """Returns the name of the tab corresponding to the tkinter frame name"""
    tab_count_plus_one = len(tabs) + 1
    tab_suffixes = [str(n) for n in range(2, tab_count_plus_one)]
    tab_suffixes.insert(0, "")
    frames = ['!frame{}'.format(i) for i in tab_suffixes]
    tab_name_dict = {i: j for i, j in zip(frames, tabs)}
    return tab_name_dict[frame_name]


def set_folder(label, active):
    try:
        if active:
            folder = fd.askdirectory()  # Grab the folder
            if folder == "":
                label.config(text="Please select a valid folder", fg="red")
            else:
                label.config(text="One folder set: {}".format(folder), fg="green")
            return folder
        else:
            return None
    except NameError:
        print("Please ensure you select a valid directory and have set a project folder")
    except AttributeError:
        print("Please ensure you select a valid directory and have set a project folder")


def save_settings():
    global PROJECT_FOLDER_PATH, SETTINGS_FILE_PATH
    try:
        SETTINGS_FILE_PATH = create_settings_file_path(PROJECT_FOLDER_PATH)
        grab_discipline_settings(DISCIPLINE_FRAME, tabs)
        create_setting_file(DISCIPLINE_SETTINGS, SETTINGS_FILE_PATH)
    except NameError:
        print("Please ensure you have selected a project folder before saving your settings.")
    except AttributeError:
        print("Please select settings for at least one discipline before saving.")


def load_settings_file():
    global SETTINGS_FILE_PATH
    try:
        SETTINGS_FILE_PATH = fd.askopenfilename()
        load_discipline_settings_file(SETTINGS_FILE_PATH)
    except FileNotFoundError:
        print("Please select a valid settings file to load from.")


def set_project_folder():
    global PROJECT_FOLDER_PATH, SETTINGS_FILE_PATH, DISCIPLINE_SETTINGS
    try:
        temp_path = fd.askdirectory()
        folder_name = extract_folder_name(temp_path)
        PROJECT_FOLDER_PATH = get_project_folder_path(folder_name)
        SETTINGS_FILE_PATH = create_settings_file_path(PROJECT_FOLDER_PATH)
        create_project_data_folder(PROJECT_FOLDER_PATH)
        for tab in tabs:
            d_setting = DisciplineSetting(tab)
            DISCIPLINE_SETTINGS[tab] = d_setting
    except FileNotFoundError:
        print("Please select a valid directory before proceeding.")
    except IndexError:
        print("Please select a valid directory before proceeding.")


def update_drawings():
    print("Updating drawings...")
    for d_setting in DISCIPLINE_SETTINGS.values():
        update_current_drawing_files(d_setting.src_folder,
                                     d_setting.dst_folder,
                                     d_setting.ss_folder,
                                     d_setting.prefix,
                                     d_setting.delimiter,
                                     d_setting.file_types,
                                     PROJECT_FOLDER_PATH)
    print("Update completed.")


tabs = ["Structures", "Architecture", "Mechanical", "Electrical", "Hydraulic", "Fire", "Facades", "Civil",
        "Geotechnical"]

if __name__ == "__main__":
    # Create the settings object
    if not os.path.exists(PROJECT_DATA_FOLDER):
        os.makedirs(PROJECT_DATA_FOLDER)
    root = Tk()
    update_frame = UpdateInterface(root)
    DISCIPLINE_FRAME = DisciplineInterface(root, tabs)
    root.mainloop()

