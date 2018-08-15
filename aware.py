"""Executable python file for the Aware program"""

from gui_classes import *

if __name__ == "__main__":
    program_data_folder = "C:/ProgramData/Aware"
    if not os.path.exists(program_data_folder):
        os.makedirs(program_data_folder)
    root = Tk()
    update_frame = UpdateInterface(root)
    discipline_frame = DisciplineInterface(root, tabs)
    root.mainloop()
