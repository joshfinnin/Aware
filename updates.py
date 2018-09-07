"""Module containing functions for updating the currently issued drawing folder using Aware"""

import os
import shutil
from time import sleep

import logs
from drawing_classes import DrawingFile, DrawingGroup


def generate_drg_objects(directory: str, delimiter=""):
    """Function for generating the drawing objects"""
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = dirpath + "/" + filename
            _, extension = os.path.splitext(filepath)
            if delimiter != "":
                filename = filename.split(".")[0].split(delimiter)[0].strip()
            date = os.path.getctime(filepath)
            drg_obj = DrawingFile(filepath, filename, date, extension)
            yield drg_obj


def check_string_inclusion(list_of_fragments: list, string_to_search: str):
    if list_of_fragments == [""]:
        return True
    else:
        for frag in list_of_fragments:
            if frag in string_to_search:
                return False
        return True


def check_black_list(black_list, string_to_search):
    set_black_list = set(black_list).symmetric_difference(set(""))
    if string_to_search in set_black_list:
        return False
    return True


def match_criteria(drg_obj: DrawingFile, drg_prefix: str, file_type: str, exclusions: list, black_list: list):
    """Function returns a boolean indicating whether the drawing file matches the search criteria"""
    prefix_length = len(drg_prefix)
    if drg_obj.name[:prefix_length] == drg_prefix and drg_obj.extension == file_type and \
            check_string_inclusion(exclusions, drg_obj.name) and check_black_list(black_list, drg_obj.name):
        return True
    else:
        return False


def update_current_drawing_files(src_folder: str, dst_folder: str, ss_folder: str, drg_prefix: str,
                                 delimiter: str, exclusions: list, black_list: list, file_types: list,
                                 project_folder_path: str):
    """Function that finds and migrates current drawings to the current drawing folder and supersedes old drawings."""
    # Find and migrate current drawings from the outgoing folder to the current folder
    try:
        for f_type in file_types:
            drg_objects = tuple(drg for drg in generate_drg_objects(src_folder, delimiter) if match_criteria(
                drg,
                drg_prefix,
                f_type,
                exclusions,
                black_list))

            drg_group_names = {drg.name for drg in drg_objects}
            for drg_group_name in drg_group_names:
                matching_drgs = [drg for drg in drg_objects if drg.name == drg_group_name]
                drg_group = DrawingGroup(matching_drgs)
                current_drawing = drg_group.get_current_drawing()
                try:
                    shutil.copy(current_drawing.filepath, dst_folder)
                except OSError:
                    print("OSError occurred for drawing {}.  This could be a permission error.".format(
                        current_drawing.name))

        # Find and supersede old drawings from the current folder to the superseded folder
            drg_objects = tuple(drg for drg in generate_drg_objects(dst_folder, delimiter) if match_criteria(
                drg,
                drg_prefix,
                f_type,
                exclusions,
                black_list))

            drg_group_names = {drg.name for drg in drg_objects}
            for drg_group_name in drg_group_names:
                matching_drgs = [drg for drg in drg_objects if drg.name == drg_group_name]
                drg_group = DrawingGroup(matching_drgs)
                superseded_drawings = drg_group.get_superseded_drawings()
                if not check_black_list(black_list, drg_group_name):
                    for bl_drg in drg_group.drawing_list:
                        shutil.move(bl_drg.filepath, ss_folder + "/" + bl_drg.name + bl_drg.extension)
                else:
                    for ss_drg in superseded_drawings:
                        shutil.move(ss_drg.filepath, ss_folder + "/" + ss_drg.name + ss_drg.extension)

        # Update log file to reflect last update
        log_file_path = logs.get_log_file_path(project_folder_path)
        logs.update_log(log_file_path)

    except PermissionError:
        try:
            sleep(1200)
            for f_type in file_types:
                drg_objects = tuple(
                    drg for drg in generate_drg_objects(src_folder, delimiter) if match_criteria(drg, drg_prefix,
                                                                                                 f_type, exclusions,
                                                                                                 black_list))
                drg_group_names = {drg.name for drg in drg_objects}
                for drg_group_name in drg_group_names:
                    matching_drgs = [drg for drg in drg_objects if drg.name == drg_group_name]
                    drg_group = DrawingGroup(matching_drgs)
                    current_drawing = drg_group.get_current_drawing()
                    shutil.copy(current_drawing.filepath, dst_folder)

                # Find and supersede old drawings from the current folder to the superseded folder
                drg_objects = tuple(
                    drg for drg in generate_drg_objects(dst_folder, delimiter) if match_criteria(drg, drg_prefix,
                                                                                                 f_type, exclusions,
                                                                                                 black_list))
                drg_group_names = {drg.name for drg in drg_objects}
                for drg_group_name in drg_group_names:
                    matching_drgs = [drg for drg in drg_objects if drg.name == drg_group_name]
                    drg_group = DrawingGroup(matching_drgs)
                    superseded_drawings = drg_group.get_superseded_drawings()
                    for ss_drg in superseded_drawings:
                        shutil.move(ss_drg.filepath, ss_folder)

            # Update log file to reflect last update
            log_file_path = logs.get_log_file_path(project_folder_path)
            logs.update_log(log_file_path)
        except PermissionError:
            print("Files in use.  Update will be performed later.")
            sleep(8)


