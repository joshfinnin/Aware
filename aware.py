"""Executable python file for the Aware program"""

from gui import *

if __name__ == "__main__":

    if not os.path.exists(PROJECT_DATA_FOLDER):
        os.makedirs(PROJECT_DATA_FOLDER)
    root = Tk()
    discipline_frame = DisciplineInterface(root, TABS)
    update_frame = UpdateInterface(root, discipline_frame)
    root.mainloop()
