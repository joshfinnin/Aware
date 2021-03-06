"""Executable python file for the Aware program"""

__name__ = "Aware"
__author__ = "Josh Finnin"
__version__ = "0.9.5"

from gui import *

if __name__ == "Aware":

    if not os.path.exists(PROJECT_DATA_FOLDER):
        os.makedirs(PROJECT_DATA_FOLDER)
    root = Tk()
    discipline_frame = DisciplineInterface(root, TABS)
    update_frame = UpdateInterface(root, discipline_frame, __author__, __version__)
    root.mainloop()

