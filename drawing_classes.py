"""Class library for updating the current issued drawing folder"""

file_types = {".pdf", ".jpeg", ".ifc", ".dwg", ".dxf", ".3dm"}


class DrawingGroup:
    """Class containing the collection of all drawing files related to an individual drawing"""
    def __init__(self, drawing_list):
        self.drawing_list = list(drawing_list)
        self.sort_drawing_list()
        self.current_drawing = self.set_current_drawing()
        self.superseded_drawings = self.set_superseded_drawings()

    @staticmethod
    def get_date(drawing):
        return drawing.date

    def sort_drawing_list(self):
        """Sorts the drawing file list based on dates"""
        self.drawing_list = sorted(self.drawing_list, key=self.get_date)

    def set_current_drawing(self):
        """Sets the most recent drawing file"""
        return self.drawing_list[-1]

    def get_current_drawing(self):
        """Gets the most recent drawing file"""
        return self.current_drawing

    def set_superseded_drawings(self):
        """Sets the list of superseded drawings"""
        return self.drawing_list[:-1]

    def get_superseded_drawings(self):
        """Gets the list of superseded drawings"""
        return self.superseded_drawings


class DrawingFile:
    """Class containing drawing file data"""
    def __init__(self, filepath, name, date, extension):
        self.filepath = filepath
        self.name = name
        self.date = date
        self.extension = extension



