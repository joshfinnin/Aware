"""Module for creating and updating the log files for Aware"""

from os import path
from time import strftime
from getpass import getuser


def get_log_file_path(project_folder_path: str):
    log_file_path = project_folder_path + "/log_file.csv"
    return log_file_path


def update_log(log_file_path: str):
    """Function that creates or updates a log file every time the drawings are updated"""
    if not path.isfile(log_file_path):
        with open(log_file_path, 'w+') as log_file:
            log_file.write("Date Updated,User\n")
    with open(log_file_path, 'a') as log_file:
        current_time = strftime("%X %x %Z")
        user = getuser()
        update_string = current_time + "," + user + "\n"
        log_file.write(update_string)


