from GeometricEntity_class import GeometricEntity
from Tkinter import *


class Arc(GeometricEntity):
    def __init__(self):
        pass

    def assertValid(self):
        pass

    def setParams(self, *params):
        """ Takes in the standard bounding box parameters, plus 'start' and 'extent' angles. """
        if len(params) != 6:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]
        self.start = params[4]
        self.extent = params[5]
        return self

    def draw(self, canvas, mapping_x, mapping_y):
        self.id = canvas.create_arc(mapping_x(self.x1), mapping_y(self.y1), mapping_x(self.x2), mapping_y(self.y2), start=self.start, extent=self.extent)
        self.applyOptions(canvas)

    def setAllByCenterRadius(self, params, options):
        """ Expects: params to be a tuple: (center_x, center_y, radius, start_angle, extent_angle);
        options to be a dict.
        Supports chaining after instantiation. """
        self.center_x = params[0]
        self.center_y = params[1]
        self.radius = params[2]
        self.start = params[3]
        self.extent = params[4]
        # Convert to the bounding box representation
        self.x1 = self.center_x - self.radius
        self.y1 = self.center_y - self.radius
        self.x2 = self.center_x + self.radius
        self.y2 = self.center_y + self.radius
        options["style"] = ARC
        self.options = options
        return self
