"""Module containing classes for the Aware GUI"""

import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog as fd
from settings import *
from updates import *
from time import strftime


PROJECT_FOLDER_PATH = ""
SETTINGS_FILE_PATH = ""
DISCIPLINE_SETTINGS = {}
DISCIPLINE_COUNT = 0
TABS = ["Structures", "Architecture", "Mechanical", "Electrical", "Hydraulic", "Fire", "Facades", "Civil",
        "Geotechnical"]


class UpdateInterface:
    def __init__(self, _root, discipline_interface):
        self.master = _root
        self.discipline_interface = discipline_interface
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
        project_folder_button.place(x=0, y=100)
        project_folder_label = Label(frame)
        project_folder_label.config(text="Please select a J drive project folder", font=("Helvetica", 10, "bold"))
        project_folder_label.place(x=0, y=75)
        project_folder_description = Label(frame)
        project_folder_description.config(text="No folder set", font=("Helvetica", 10, "italic"))
        project_folder_description.place(x=0, y=125)
        wrap_update_buttons(project_folder_button, project_folder_description, set_project_folder)

        settings_label = Label(frame)
        settings_label.config(text="Settings files", font=("Helvetica", 10, "bold"))
        settings_label.place(x=0, y=175)
        save_settings_button = ttk.Button(frame)
        save_settings_button.config(text="Save settings")
        save_settings_button.place(x=0, y=200)
        save_settings_description = Label(frame)
        save_settings_description.config(text="Unsaved", font=("Helvetica", 10, "italic"), justify=LEFT)
        save_settings_description.place(x=0, y=225)
        wrap_save_settings_buttons(self.discipline_interface, save_settings_button, save_settings_description,
                                   DisciplineInterface.save_settings)

        load_settings_button = ttk.Button(frame)
        load_settings_button.config(text="Load settings")
        load_settings_button.config(command=load_settings_file)
        load_settings_button.place(x=0, y=260)

        update_label = Label(frame)
        update_label.config(text="Update drawing folders", font=("Helvetica", 10, "bold"))
        update_label.place(x=0, y=325)
        update_button = ttk.Button(frame)
        update_button.config(text="Update drawings")
        update_button.place(x=0, y=350)
        update_description = Label(frame)
        update_description.config(text="No update performed", font=("Helvetica", 10, "italic"), justify=LEFT)
        update_description.place(x=0, y=375)
        wrap_update_buttons(update_button, update_description, update_drawings)

        frame.place(x=0, y=0, width=300, height=675)


class DisciplineInterface:
    def __init__(self, _root, tab_names):
        self.master = _root
        self.master.title("Aware")
        self.master.minsize(1200, 675)
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
    def create_tab_content(tab: ttk.Notebook.tab):
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
                                  font=("Helvetica", 8))
        prefix_description.place(x=20, y=85)

        delimiter_label = Label(tab)
        delimiter_label.config(text="Revision Delimiter:", font=("Helvetica", 10, "bold"))
        delimiter_label.place(x=20, y=125)
        delimiter_field = ttk.Entry(tab)
        delimiter_field.place(x=150, y=125)
        delimiter_description = Label(tab)
        delimiter_description.config(text="(i.e. for drawing \'S-01-100[T01]\', the delimiter would be \'[\')",
                                     font=("Helvetica", 8))
        delimiter_description.place(x=20, y=150)

        exclusion_label = Label(tab)
        exclusion_label.config(text="Character Exclusions:", font=("Helvetica", 10, "bold"))
        exclusion_label.place(x=20, y=190)
        exclusion_field = ttk.Entry(tab)
        exclusion_field.place(x=170, y=190)
        exclusion_description = Label(tab)
        exclusion_description.config(text="(i.e. if \'SK\' exclusion is provided, drawing \'S-SK-01-100\' will be "
                                          "excluded\nfrom the search.\nMultiple entries can be provided by separating "
                                          "with a \'#\' delimiter)", font=("Helvetica", 8), justify=LEFT)
        exclusion_description.place(x=20, y=215)

        black_list_label = Label(tab)
        black_list_label.config(text="Black List", font=("Helvetica", 10, "bold"))
        black_list_label.place(x=460, y=20)
        black_list_text_box = Text(tab)
        black_list_text_box.config(width=50, height=10, borderwidth=2,
                                   bg="black", fg="white", font=("Helvetica", 10),
                                   insertbackground="white")
        black_list_text_box.place(x=460, y=45)
        black_list_description = Label(tab)
        black_list_description.config(text="(Drawings added to the black list will be excluded from the search,\n"
                                           "even if they match all search criteria and possess no exclusion criteria.\n"
                                           "Use the black list to override the search to ignore certain drawings.\n"
                                           "Each drawing in the black list should be entered on a different line.)",
                                      font=("Helvetica", 8),
                                      justify=LEFT)
        black_list_description.place(x=460, y=215)

        folder_label = Label(tab)
        folder_label.config(text="Folders:", font=("Helvetica", 10, "bold"))
        folder_label.place(x=20, y=275)

        source_button = ttk.Button(tab)
        source_button.config(text="Set Source Folder")
        source_button.place(x=20, y=300)
        source_button_description = Label(tab)
        source_button_description.config(text="Folder to search for current drawings", font=("Helvetica", 10, "italic"))
        source_button_description.place(x=170, y=300)
        tab.src_folder = StringVar()
        wrap_folder_buttons(source_button, source_button_description, activate, tab.src_folder, set_folder)

        destination_button = ttk.Button(tab)
        destination_button.config(text="Set Destination Folder")
        destination_button.place(x=20, y=325)
        destination_button_description = Label(tab)
        destination_button_description.config(text="Folder to store current drawings", font=("Helvetica", 10, "italic"))
        destination_button_description.place(x=170, y=325)
        tab.dst_folder = StringVar()
        wrap_folder_buttons(destination_button, destination_button_description, activate, tab.dst_folder, set_folder)

        superseded_button = ttk.Button(tab)
        superseded_button.config(text="Set Superseded Folder")
        superseded_button.place(x=20, y=350)
        superseded_button_description = Label(tab)
        superseded_button_description.config(text="Folder to send superseded drawings", font=("Helvetica", 10, "italic"))
        superseded_button_description.place(x=170, y=350)
        tab.ss_folder = StringVar()
        wrap_folder_buttons(superseded_button, superseded_button_description, activate, tab.ss_folder, set_folder)

        file_types_label = Label(tab)
        file_types_label.config(text="File types to update:", font=("Helvetica", 10, "bold"))
        file_types_label.place(x=20, y=400)

        tab.pdf_bool = BooleanVar()
        cb_pdf = ttk.Checkbutton(tab)
        cb_pdf.config(text="PDF", variable=tab.pdf_bool)
        cb_pdf.place(x=30, y=425)

        tab.ifc_bool = BooleanVar()
        cb_ifc = ttk.Checkbutton(tab)
        cb_ifc.config(text="IFC", variable=tab.ifc_bool)
        cb_ifc.place(x=30, y=450)

        tab.dxf_bool = BooleanVar()
        cb_dxf = ttk.Checkbutton(tab)
        cb_dxf.config(text="DXF", variable=tab.dxf_bool)
        cb_dxf.place(x=30, y=475)

        tab.dwg_bool = BooleanVar()
        cb_dwg = ttk.Checkbutton(tab)
        cb_dwg.config(text="DWG", variable=tab.dwg_bool)
        cb_dwg.place(x=30, y=500)

        tab.jpeg_bool = BooleanVar()
        cb_jpeg = ttk.Checkbutton(tab)
        cb_jpeg.config(text="JPEG", variable=tab.jpeg_bool)
        cb_jpeg.place(x=30, y=525)

        tab.rhino_bool = BooleanVar()
        cb_3dm = ttk.Checkbutton(tab)
        cb_3dm.config(text="3DM", variable=tab.rhino_bool)
        cb_3dm.place(x=30, y=550)

    def create_notebook(self):
        notebook = ttk.Notebook(master=self.master)
        for tab in self.tab_names:
            frame = ttk.Frame(notebook)
            self.create_tab_content(frame)
            notebook.add(frame, text=tab)
            self.tab_dict[tab] = frame
        notebook.place(x=300, y=20, height=675, width=1000)
        return notebook

    def save_settings(self, label: Label):
        global PROJECT_FOLDER_PATH, SETTINGS_FILE_PATH
        try:
            SETTINGS_FILE_PATH = get_settings_file_path(PROJECT_FOLDER_PATH)
            create_project_data_folder(PROJECT_FOLDER_PATH)
            for tab in TABS:
                d_setting = DisciplineSetting(tab)
                DISCIPLINE_SETTINGS[tab] = d_setting
            SETTINGS_FILE_PATH = get_settings_file_path(PROJECT_FOLDER_PATH)
            grab_discipline_settings(self, TABS)
            create_setting_file(DISCIPLINE_SETTINGS, SETTINGS_FILE_PATH)
            time = strftime("%D %T")
            label.config(text="Settings saved at: {}".format(time), fg="blue", justify=LEFT,
                         font=("Helvetica", 10, "italic"))
        except NameError:
            print("Please ensure you have selected a project folder before saving your settings.")
        except AttributeError:
            print("Please select settings for at least one discipline before saving.")


def grab_discipline_settings(discipline_interface: DisciplineInterface, tab_names: list):
    """Function for capturing the current state of discipline settings.
    To be used when settings are saved, or the update function is run"""
    for t_name in tab_names:
        # Update to access the variables from each discipline to create the DisciplineSetting objects
        # This function needs to be implemented by both the update button and the save settings button
        tab = discipline_interface.tab_dict[t_name]
        active_button = tab.children['!checkbutton']
        active = active_button.var.get()
        if active:

            prefix_raw = tab.children['!entry'].get()
            prefix = prefix_raw.strip()

            delimiter_raw = tab.children['!entry2'].get()
            delimiter = delimiter_raw.strip()

            exclusions = tab.children['!entry3'].get()

            d_setting = DISCIPLINE_SETTINGS[t_name]
            d_setting.active = True
            d_setting.prefix = prefix  # Set prefix
            d_setting.delimiter = delimiter  # Set delimiter

            d_setting.exclusions = exclusions
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


def wrap_folder_buttons(button: ttk.Button, label: Label, active: BooleanVar,
                        variable: StringVar, command):

    def inner():
        result = command(label, active)
        variable.set(result)
        return result

    button["command"] = inner


def wrap_update_buttons(button: ttk.Button, label: Label, command):

    def inner():
        command(label)

    button["command"] = inner


def wrap_save_settings_buttons(discipline_interface, button: ttk.Button, label: Label, command):

    def inner():
        command(discipline_interface, label)

    button["command"] = inner


def lookup_discipline_name(frame_name: str):
    """Returns the name of the tab corresponding to the tkinter frame name"""
    tab_count_plus_one = len(TABS) + 1
    tab_suffixes = [str(n) for n in range(2, tab_count_plus_one)]
    tab_suffixes.insert(0, "")
    frames = ['!frame{}'.format(i) for i in tab_suffixes]
    tab_name_dict = {i: j for i, j in zip(frames, TABS)}
    return tab_name_dict[frame_name]


def set_folder(label: Label, active: BooleanVar):
    try:
        if active:
            folder = fd.askdirectory()
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


def load_settings_file():
    global SETTINGS_FILE_PATH
    try:
        SETTINGS_FILE_PATH = fd.askopenfilename()
        load_discipline_settings_file(SETTINGS_FILE_PATH, DISCIPLINE_SETTINGS)  # TODO:  Need to resolve this
    except FileNotFoundError:
        print("Please select a valid settings file to load from.")


def set_project_folder(label: Label):
    global PROJECT_FOLDER_PATH
    try:
        temp_path = fd.askdirectory()
        if temp_path == "":
            label.config(text="Please select a valid project folder", fg="red", font=("Helvetica", 10))
        else:
            label.config(text="1 folder set:\n{}".format(temp_path), justify=LEFT,
                         fg="green", font=("Helvetica", 10))
            folder_name = extract_folder_name(temp_path)
            PROJECT_FOLDER_PATH = get_project_folder_path(folder_name)
    except FileNotFoundError:
        print("Please select a valid directory before proceeding.")
    except IndexError:
        print("Please select a valid directory before proceeding.")


def update_drawings(label: Label):
    global DISCIPLINE_COUNT
    label.config(text="Update...", fg="gray", font=("Helvetica", 10, "italic"))
    for d_setting in DISCIPLINE_SETTINGS.values():
        if not d_setting.active:
                pass
        else:
            update_current_drawing_files(d_setting.src_folder,
                                         d_setting.dst_folder,
                                         d_setting.ss_folder,
                                         d_setting.prefix,
                                         d_setting.delimiter,
                                         d_setting.exclusions,
                                         d_setting.file_types,
                                         PROJECT_FOLDER_PATH)
            DISCIPLINE_COUNT += 1
    time = strftime("%D %T")
    label.config(text="Update completed for {} disciplines at:\n{}".format(DISCIPLINE_COUNT, time), justify=LEFT,
                 fg="blue", font=("Helvetica", 10, "italic"))






