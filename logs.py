"""Module for creating and updating the log files for Aware"""

from os import path
from time import strftime
from getpass import getuser


def update_log(settings):
    """Function that creates/updates a log file for every time the drawings are updated"""
    folder = settings.SETTING_FOLDER
    log_file_path = folder + "\\" + "log_file.csv"
    # Create log file if it does not already exist
    if not path.isfile(log_file_path):
        with open(log_file_path, 'w+') as log_file:
            log_file.write("Updates,User\n")
    with open(log_file_path, 'a') as log_file:
        current_time = strftime("%X %x %Z")
        user = getuser()
        update_string = current_time + "," + user + "\n"
        log_file.write(update_string)


