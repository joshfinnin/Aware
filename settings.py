"""Module containing functions for creating, editing and deleting settings files for the updates"""

from os import path, walk, makedirs
import csv

PROJECT_DATA_FOLDER = "C:\\ProgramData\\Aware"


class Settings:
    """Class containing data for all disciplines, and info about where to store data"""

    # Dictionary containing project folder info
    Projects = {}

    def __init__(self, folder):
        Settings.SETTING_FOLDER = folder
        Settings.FILE_PATH = folder + "\\" + "update_settings.csv"


class Project:
    """Class containing information specific to a project"""
    def __init__(self, settings, name, p_path):
        self.name = name
        self.project_path = p_path
        self.disciplines = {}
        settings.Projects[name] = self


class DisciplineSetting:
    """Object containing the settings for each discipline"""
    def __init__(self, project, d_name, prefix, src_folder, dst_folder, ss_folder, file_types):
        self.project = project
        self.d_name = d_name
        self.prefix = prefix
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.ss_folder = ss_folder
        self.file_types = file_types
        # Update global settings list once DisciplineSetting object is created
        self.project.disciplines[d_name] = self


def create_setting_file(settings):
    """Function for creating a setting file to retain data for all disciplines"""
    file_path = settings.FILE_PATH
    with open(file_path, 'w+') as settings_file:
        settings_lines = []
        headers = ("Discipline", "Prefix", "Source", "Destination", "Superseded", "File Types")
        headers_joined = ",".join(headers) + "\n"
        settings_lines.append(headers_joined)
        for ds in settings.Disciplines.values():
            name = ds.d_name
            prefix = ds.prefix
            src_folder = ds.src_folder
            dst_folder = ds.dst_folder
            ss_folder = ds.ss_folder
            file_types = ds.file_types
            file_types = "/".join(file_types)  # Ensure the list of file types is aggregated into a single string
            setting_vars = (name, prefix, src_folder, dst_folder, ss_folder, file_types)
            setting_string = ",".join(setting_vars) + "\n"
            settings_lines.append(setting_string)
        settings_file.writelines(settings_lines)


def load_discipline_settings_file(file_path):
    """Function for loading settings data contained in a settings file.
    Creates and populates Project objects with the necessary data from the settings file."""
    if path.isfile(file_path):
        project_folder_name = extract_folder_name(file_path)
        project_folder_path = get_project_folder_path(project_folder_name)
        project = Project(settings, project_folder_name, project_folder_path)
        with open(file_path, 'r') as settings_file:
            setting_dicts = csv.DictReader(settings_file)
            for ds in setting_dicts:
                name = ds["Discipline"]
                prefix = ds["Prefix"]
                src_folder = ds["Source"]
                dst_folder = ds["Destination"]
                ss_folder = ds["Superseded"]
                file_types = ds["File Types"]
                file_types = file_types.split("/")
                # The constructor for each object should automatically update the settings cache dictionary
                # So shouldn't need to do anything else other than instantiate the objects
                d_setting = DisciplineSetting(project, name, prefix, src_folder, dst_folder, ss_folder, file_types)
    else:
        raise FileNotFoundError


def implicit_load_project_settings():
    for dir, dirname, file_names in walk(PROJECT_DATA_FOLDER):
        project_folder_name = dirname[:3] + "000"
        project_folder = "J:\\{parent}\\{project}\\Work//Internal\\BIM_CDE".format(parent=project_folder_name,
                                                                                   project=dirname)
        settings_file = project_folder + "\\update_settings.csv"
        load_discipline_settings_file(settings_file)


def extract_folder_name(path):
    """Takes the BIM_CDE project folder path. Returns the project folder name."""
    fragments = path.split("\\")
    folder = fragments[2]
    return folder


def create_project_data_folder(project_folder_path):
    folder_name = extract_folder_name(project_folder_path)
    project_data_folder = PROJECT_DATA_FOLDER + "\\" + folder_name
    makedirs(project_data_folder)


def get_project_folder_path(project):
    project_folder_name = project[:3] + "000"
    project_folder = "J:\\{parent}\\{project}\\Work//Internal\\BIM_CDE".format(parent=project_folder_name,
                                                                               project=project)
    return project_folder

settings = Settings("C:\\Users\\josh.finnin\\Desktop\\ACU")

# Test functionality

# settings = Settings("C:\\Users\\josh.finnin\\Desktop\\ACU")

# d_test = DisciplineSetting("Structures", "S", "C:\\Users\\josh.finnin\\Desktop\\ACU",
#                            "C:\\Users\\josh.finnin\\Desktop\\ACU",
#                            "C:\\Users\\josh.finnin\\Desktop\\ACU",
#                            (".pdf", ".ifc"))
#
# d_test2 = DisciplineSetting("Mechanical", "M", "C:\\Users\\josh.finnin\\Desktop\\ACU",
#                             "C:\\Users\\josh.finnin\\Desktop\\ACU",
#                             "C:\\Users\\josh.finnin\\Desktop\\ACU",
#                             (".pdf", ".ifc"))
#
# create_setting_file("C:\\Users\\josh.finnin\\Desktop\\ACU", Settings)

