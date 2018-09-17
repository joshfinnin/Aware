"""Module for automated updates of the Current (Issued) folder based on previously defined settings."""

from os import walk
from time import sleep

import logs
from settings import *
from updates import *

DISCIPLINE_SETTINGS = set()


def update_all_drawing_folders():
    for dir, dirnames, filenames in walk(PROJECT_DATA_FOLDER):
        for dirname in dirnames:
            project_folder_path = get_project_folder_path(dirname)
            settings_file_path = get_settings_file_path(project_folder_path)
            load_discipline_settings_file(settings_file_path, DISCIPLINE_SETTINGS)
            update_count = 0
            print("Updating current drawings for project {}...".format(dirname))
            for d_setting in DISCIPLINE_SETTINGS:
                update_current_drawing_files(d_setting.src_folder, d_setting.dst_folder,
                                             d_setting.ss_folder, d_setting.prefix,
                                             d_setting.delimiter, d_setting.exclusions, d_setting.black_list,
                                             d_setting.file_types, project_folder_path)
                update_count += 1
                print("{} disciplines updated".format(update_count))
            print("Drawings updated for project {}".format(dirname))
            log_file_path = logs.get_log_file_path(project_folder_path)
            logs.update_log(log_file_path)
    print('Drawing update complete.')


if __name__ == "__main__":
    update_all_drawing_folders()
    sleep(4)
    exit()

