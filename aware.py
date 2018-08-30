"""Executable python file for the Aware program"""

__name__ = "Aware"
__author__ = "Josh Finnin"
__version__ = "1.2.0"

from gui import *

if __name__ == "Aware":

    if not os.path.exists(PROJECT_DATA_FOLDER):
        os.makedirs(PROJECT_DATA_FOLDER)
    root = Tk()
    discipline_frame = DisciplineInterface(root, TABS)
    update_frame = UpdateInterface(root, discipline_frame)
    root.mainloop()


# TODO: Add a 'black list' feature for drawings to be ignored, even if they match all search criteria.

