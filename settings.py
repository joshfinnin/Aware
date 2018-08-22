"""Module containing functions for creating, editing and deleting settings files for the updates"""

from os import path, walk, makedirs
import csv

PROJECT_DATA_FOLDER = "C:/ProgramData/Aware"


class Settings:
    """Class containing data for all disciplines, and info about where to store data"""

    # Dictionary containing project folder info
    Projects = {}

    def __init__(self, folder):
        Settings.SETTING_FOLDER = folder
        Settings.FILE_PATH = folder + "/update_settings.csv"


class Project:
    """Class containing information specific to a project"""
    def __init__(self, settings, name, p_path):
        self.name = name
        self.project_path = p_path
        self.disciplines = {}
        settings.Projects[self.name] = self

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def project_path(self):
        return self.__project_path

    @project_path.setter
    def project_path(self, project_path):
        self.__project_path = project_path

# Do we need settings and project classes?  They might be entirely redundant if each Discipline Setting object is going
# to be created dynamically when a project is loaded anyway, or the settings are collected all at once from the state
# of the GUI.

# I think I can decouple the DisciplineSetting object from this safely, test it to see if it works, and then
# remove the redundant classes


class DisciplineSetting:
    """Object containing the settings for each discipline"""
    def __init__(self, d_name):
        # self.project = project
        self.d_name = d_name
        self.prefix = ""  # Used an empty string as giving None type was triggering the warning for non-string type
        self.delimiter = ""
        self.src_folder = None
        self.dst_folder = None
        self.ss_folder = None
        self.file_types = None
        # Update global settings list once DisciplineSetting object is created
        # self.project.disciplines[d_name] = self

    # @property
    # def project(self):
    #     return self.__project
    #
    # @project.setter
    # def project(self, project):
    #     self.__project = project

    @property
    def d_name(self):
        return self.__d_name

    @d_name.setter
    def d_name(self, d_name):
        self.__d_name = d_name

    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, prefix):
        if not isinstance(prefix, str):
            print("Prefix should be one or more characters of the alphabet. "
                  "Numbers and/or special characters should not be used.")
        else:
            self.__prefix = prefix

    @property
    def delimiter(self):
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delimiter):
        if not isinstance(delimiter, str):
            print("Delimiter should be one or more characters of the alphabet. "
                  "Numbers and/or special characters should not be used.")
        else:
            self.__delimiter = delimiter

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


def create_setting_file(discipline_settings, settings_file_path):
    """Function for creating a setting file to retain data for all disciplines"""
    settings_file = open(settings_file_path, 'w+')
    settings_lines = []
    headers = ("Discipline", "Prefix", "Delimiter", "Source", "Destination", "Superseded", "File Types")
    headers_joined = ",".join(headers) + "\n"
    settings_lines.append(headers_joined)
    for ds in discipline_settings.values():
        name = ds.d_name
        prefix = ds.prefix
        delimiter = ds.delimiter
        src_folder = ds.src_folder
        dst_folder = ds.dst_folder
        ss_folder = ds.ss_folder
        file_types = ds.file_types
        file_types = "/".join(file_types)  # Ensure the list of file types is aggregated into a single string
        setting_vars = (name, prefix, delimiter, src_folder, dst_folder, ss_folder, file_types)
        setting_string = ",".join(setting_vars) + "\n"
        settings_lines.append(setting_string)
    settings_file.writelines(settings_lines)
    settings_file.close()


def load_discipline_settings_file(file_path):
    """Function for loading settings data contained in a settings file.
    Creates and populates Project objects with the necessary data from the settings file."""
    # if path.isfile(file_path):
    #     project_folder_name = extract_folder_name(file_path)
    #     project_folder_path = get_project_folder_path(project_folder_name)
    #     project = Project(settings, project_folder_name, project_folder_path)
    with open(file_path, 'r') as settings_file:
        setting_dicts = csv.DictReader(settings_file)
        for ds in setting_dicts:
            name = ds["Discipline"]
            prefix = ds["Prefix"]
            delimiter = ds["Delimiter"]
            src_folder = ds["Source"]
            dst_folder = ds["Destination"]
            ss_folder = ds["Superseded"]
            file_types = ds["File Types"]
            file_types = set(file_types.split("/"))
            d_setting = DisciplineSetting(name)
            d_setting.prefix = prefix
            d_setting.delimiter = delimiter
            d_setting.src_folder = src_folder
            d_setting.dst_folder = dst_folder
            d_setting.ss_folder = ss_folder
            d_setting.file_types = file_types
    # else:
    #     raise FileNotFoundError


def implicit_load_project_settings():
    for dir, dirname, file_names in walk(PROJECT_DATA_FOLDER):
        project_folder_name = dirname[:3] + "000"
        project_folder = "J:/{parent}/{project}/Work//Internal/BIM_CDE".format(parent=project_folder_name,
                                                                               project=dirname)
        settings_file = project_folder + "/update_settings.csv"
        load_discipline_settings_file(settings_file)


def extract_folder_name(path):
    """Takes the BIM_CDE project folder path. Returns the project folder name."""
    fragments = path.split("/")
    folder = fragments[2]
    return folder


def create_project_data_folder(project_folder_path):
    folder_name = extract_folder_name(project_folder_path)
    project_data_folder = PROJECT_DATA_FOLDER + "/" + folder_name
    if not path.isdir(project_data_folder):
        makedirs(project_data_folder)


def create_settings_file_path(project_folder_path):
    settings_file_path = project_folder_path + "/update_settings.csv"
    return settings_file_path


def get_project_folder_path(project_folder_name):
    parent = project_folder_name[:3] + "000"
    project_folder = "J:/{parent}/{project}/Work//Internal/BIM_CDE".format(parent=parent,
                                                                           project=project_folder_name)
    return project_folder


