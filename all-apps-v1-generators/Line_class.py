from GeometricEntity_class import GeometricEntity
from Tkinter import *


class Line(GeometricEntity):
    def __init__(self):
        pass

    def assertValid(self):
        pass

    def setParams(self, *params):
        """ Takes in the standard bounding box parameters, plus 'start' and 'extent' angles. """
        if len(params) != 4:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]
        return self

    def setAll(self, params, options):
        """ Expects params to be a tuple and options to be a dict.
        Supports chaining after instantiation. """
        if len(params) != 4:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]
        self.options = options
        # To allow chaining of operations
        return self

    def draw(self, canvas, mapping_x, mapping_y):
        self.id = canvas.create_line(mapping_x(self.x1), mapping_y(self.y1), mapping_x(self.x2), mapping_y(self.y2))
        self.applyOptions(canvas)
