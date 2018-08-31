"""Module containing functions for creating, editing and deleting settings files for the updates"""

import csv
from os import path, makedirs

PROJECT_DATA_FOLDER = "C:/ProgramData/Aware"


class DisciplineSetting:
    """Object containing the settings for each discipline"""
    def __init__(self, d_name):
        # self.project = project
        self.d_name = d_name
        self.active = False
        self.prefix = ""  # Used an empty string as giving None type was triggering the warning for non-string type
        self.delimiter = ""
        self.exclusions = ""
        self.src_folder = ""
        self.dst_folder = ""
        self.ss_folder = ""
        self.file_types = []
        self.black_list = ""

    @property
    def d_name(self):
        return self.__d_name

    @d_name.setter
    def d_name(self, d_name):
        self.__d_name = d_name

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, active):
        self.__active = active

    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, prefix):
        if not isinstance(prefix, str):
            print("Prefix should be one or more characters of the alphabet. "
                  "Numbers and/or special characters should not be used.")
        else:
            self.__prefix = prefix.strip()

    @property
    def delimiter(self):
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delimiter):
        if not isinstance(delimiter, str):
            print("Delimiter should be one or more characters of the alphabet. "
                  "Numbers and/or special characters should not be used.")
        else:
            self.__delimiter = delimiter.strip()

    @property
    def exclusions(self):
        return self.__exclusions

    @exclusions.setter
    def exclusions(self, exclusions):
        split_exclusions = exclusions.split("#")
        self.__exclusions = [e.strip() for e in split_exclusions]

    @property
    def src_folder(self):
        return self.__src_folder

    @src_folder.setter
    def src_folder(self, src_folder):
        self.__src_folder = src_folder

    @property
    def dst_folder(self):
        return self.__dst_folder

    @dst_folder.setter
    def dst_folder(self, dst_folder):
        self.__dst_folder = dst_folder

    @property
    def ss_folder(self):
        return self.__ss_folder

    @ss_folder.setter
    def ss_folder(self, ss_folder):
        self.__ss_folder = ss_folder

    @property
    def file_types(self):
        return self.__file_types

    @file_types.setter
    def file_types(self, file_types):
        self.__file_types = file_types

    def update_setting(self, parameter, value):
        pass

    @property
    def black_list(self):
        return self.__black_list

    @black_list.setter
    def black_list(self, black_list):
        _black_list = black_list.split("\n")
        print(_black_list)
        _black_list = [drawing.split(".")[0] for drawing in _black_list]
        if self.delimiter != "":
            _black_list = [drawing.split(self.delimiter)[0] for drawing in _black_list]
        self.__black_list = _black_list


def create_setting_file(discipline_settings: dict, settings_file_path: str):
    """Function for creating a setting file to retain data for all disciplines"""
    settings_file = open(settings_file_path, 'w+')
    settings_lines = []
    headers = ("Discipline", "Prefix", "Delimiter", "Exclusions", "Black List", "Source", "Destination",
               "Superseded", "File Types")
    headers_joined = ",".join(headers) + "\n"
    settings_lines.append(headers_joined)
    for ds in discipline_settings.values():
        if ds.active:
            name = ds.d_name
            prefix = ds.prefix
            delimiter = ds.delimiter
            exclusions = ds.exclusions
            exclusions = "#".join(exclusions)
            black_list = ds.black_list
            black_list = "#".join(black_list)
            src_folder = ds.src_folder
            dst_folder = ds.dst_folder
            ss_folder = ds.ss_folder
            file_types = ds.file_types
            file_types = "/".join(file_types)
            setting_vars = (name, prefix, delimiter, exclusions, black_list,
                            src_folder, dst_folder, ss_folder, file_types)
            setting_string = ",".join(setting_vars) + "\n"
            settings_lines.append(setting_string)
    settings_file.writelines(settings_lines)
    settings_file.close()


def load_discipline_settings_file(settings_file_path: str, settings_cache: set):
    """Function for loading settings data contained in a settings file.
    Creates and populates Project objects with the necessary data from the settings file."""
    with open(settings_file_path, 'r') as settings_file:
        setting_dicts = csv.DictReader(settings_file)
        for ds in setting_dicts:
            name = ds["Discipline"]
            prefix = ds["Prefix"]
            delimiter = ds["Delimiter"]
            exclusions = ds["Exclusions"]
            black_list = ds["Black List"]
            src_folder = ds["Source"]
            dst_folder = ds["Destination"]
            ss_folder = ds["Superseded"]
            file_types = ds["File Types"]
            file_types = set(file_types.split("/"))
            d_setting = DisciplineSetting(name)
            d_setting.prefix = prefix
            d_setting.delimiter = delimiter
            d_setting.exclusions = exclusions.split("#")
            d_setting.black_list = "\n".join(black_list.split("#"))
            d_setting.src_folder = src_folder
            d_setting.dst_folder = dst_folder
            d_setting.ss_folder = ss_folder
            d_setting.file_types = file_types
            settings_cache.add(d_setting)


def extract_folder_name(path: str):
    """Takes the BIM_CDE project folder path. Returns the project folder name."""
    fragments = path.split("/")
    folder = fragments[2]
    return folder


def create_project_data_folder(project_folder_path: str):
    folder_name = extract_folder_name(project_folder_path)
    project_data_folder = PROJECT_DATA_FOLDER + "/" + folder_name
    if not path.isdir(project_data_folder):
        makedirs(project_data_folder)


def get_settings_file_path(project_folder_path: str):
    settings_file_path = project_folder_path + "/update_settings.csv"
    return settings_file_path


def get_project_folder_path(project_folder_name: str):
    parent = project_folder_name[:3] + "000"
    project_folder = "J:/{parent}/{project}/Work/Internal/BIM_CDE/03_PUBLISHED".format(parent=parent,
                                                                                       project=project_folder_name)
    return project_folder


