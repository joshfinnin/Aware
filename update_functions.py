"""Module containing functions for updating the currently issued drawing folder"""

import os
import shutil
from drawing_classes import *
import logs
import settings


def generate_drg_objects(directory, delimiter=None):
    """Function for generating the drawing objects"""
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = dirpath + "/" + filename
            fname, extension = os.path.splitext(filepath)
            if delimiter is not None:
                fname = fname.split(delimiter)[0]
            date = os.path.getctime(filepath)
            drg_obj = DrawingFile(filepath, fname, date, extension)
            yield drg_obj


def match_criteria(drg_obj, drg_prefix, file_type):
    """Function returns a boolean indicating whether the drawing file matches the search criteria"""
    prefix_length = len(drg_prefix)
    if drg_obj.name[:prefix_length] == drg_prefix and drg_obj.extension == file_type:
        return True
    else:
        return False


def update_current_drawing_files(src_folder, dst_folder, ss_folder, drg_prefix, delimiter, file_types, project_folder_path):
    """Function that finds and migrates current drawings to the current drawing folder and supersedes old drawings."""
    # Find and migrate current drawings from the outgoing folder to the current folder
    for f_type in file_types:
        drg_objects = [drg for drg in generate_drg_objects(src_folder, delimiter) if match_criteria(drg, drg_prefix,
                                                                                                    f_type)]
        drg_group_names = {drg.name for drg in drg_objects}
        for drg_group_name in drg_group_names:
            matching_drgs = [drg for drg in drg_objects if drg.name == drg_group_name]
            drg_group = DrawingGroup(matching_drgs)
            current_drawing = drg_group.get_current_drawing()
            shutil.copy(current_drawing, dst_folder)

    # Find and supersede old drawings from the current folder to the superseded folder
        drg_objects = [drg for drg in generate_drg_objects(dst_folder, delimiter) if match_criteria(drg, drg_prefix,
                                                                                                    f_type)]
        drg_group_names = {drg.name for drg in drg_objects}
        for drg_group_name in drg_group_names:
            matching_drgs = [drg for drg in drg_objects if drg.name == drg_group_name]
            drg_group = DrawingGroup(matching_drgs)
            superseded_drawings = drg_group.get_superseded_drawings()
            for ss_drg in superseded_drawings:
                shutil.move(ss_drg, ss_folder)

    # Update log file to reflect last update
    log_file_path = logs.get_log_file_path(project_folder_path)
    logs.update_log(log_file_path)


if __name__ == "__main__":
    for dir, dirname, file in os.walk("C:/ProgramData/Aware"):
            print(dirname)



